"""The agent loop: briefing -> Claude with tools -> submit_decision, with a code-level safety net."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Callable, Optional

import anthropic

from agent.briefing import Briefing, BriefingError, build_briefing
from agent.config import PROJECT_ROOT, AgentConfig, load_api_key
from agent.decision import SUBMIT_DECISION_SPEC, validate_decision
from tools import call_tool, tool_specs
from tools._common import case_dir, read_ledger

SYSTEM_PROMPT = (PROJECT_ROOT / "agent" / "prompts" / "system.md").read_text(encoding="utf-8")

# The case is loaded by the briefing; the model must not reload it (that could reveal later events).
AGENT_TOOLS = [
    "read_attachment", "safety_screen", "get_case_state",
    "send_email", "send_sms", "place_call",
    "request_landlord_approval", "record_landlord_decision", "assign_contractor", "schedule_appointment",
    "record_financial", "set_hold", "add_note", "track_open_item", "escalate_to_human", "close_case",
]
# Allowed while a blocking escalation is open: reading, notes, holds and messages to people.
ALLOWED_WHILE_BLOCKED = {"read_attachment", "safety_screen", "get_case_state", "add_note", "track_open_item",
                         "set_hold", "send_email", "send_sms", "place_call", "escalate_to_human"}
MAX_TOOL_RESULT_CHARS = 12_000
MAX_SUBMIT_ATTEMPTS = 4
# USD per million tokens for claude-opus-5-5 (input, output, cache write, cache read).
PRICES = {"input": 4.0, "output": 20.0, "cache_write": 5.0, "cache_read": 0.20}


def _block_to_dict(block: Any) -> dict:
    return block.model_dump(mode="json", exclude_none=True) if hasattr(block, "model_dump") else dict(block)


def _tool_result_text(result: dict) -> str:
    text = json.dumps(result, ensure_ascii=False, default=str)
    if len(text) > MAX_TOOL_RESULT_CHARS:
        text = text[:MAX_TOOL_RESULT_CHARS] + '... [truncated: call again with narrower parameters if needed]'
    return text


def _blocking_escalation_open(case_id: str) -> bool:
    for entry in read_ledger(case_id):
        if entry.get("ok") and entry["tool"] == "escalate_to_human" and (entry.get("data") or {}).get("blocks_automation"):
            return True
    return False


class AgentRun:
    def __init__(self, config: AgentConfig, client: anthropic.Anthropic, log: Callable[[str], None]):
        self.config = config
        self.client = client
        self.log = log
        self.transcript: list[dict] = []
        self.usage = {"input": 0, "output": 0, "cache_write": 0, "cache_read": 0}
        self.tools = tool_specs(AGENT_TOOLS) + [SUBMIT_DECISION_SPEC]

    # ------------------------------------------------------------------ model call
    def _call_model(self, messages: list) -> Any:
        params: dict[str, Any] = dict(
            model=self.config.model,
            max_tokens=self.config.max_tokens,
            system=SYSTEM_PROMPT,
            tools=self.tools,
            messages=messages,
            thinking={"type": "adaptive", "display": "summarized"},
            output_config={"effort": self.config.effort},
            cache_control={"type": "ephemeral"},
        )
        if self.config.use_fallbacks:
            params.update(betas=list(self.config.betas), fallbacks="default")
        with self.client.beta.messages.stream(**params) as stream:
            message = stream.get_final_message()
        u = message.usage
        self.usage["input"] += u.input_tokens or 0
        self.usage["output"] += u.output_tokens or 0
        self.usage["cache_write"] += getattr(u, "cache_creation_input_tokens", 0) or 0
        self.usage["cache_read"] += getattr(u, "cache_read_input_tokens", 0) or 0
        return message

    def cost_usd(self) -> float:
        return round(sum(self.usage[k] * PRICES[k] for k in PRICES) / 1_000_000, 4)

    # ------------------------------------------------------------------ main loop
    def run(self, briefing: Briefing) -> tuple[Optional[dict], str]:
        """Returns (decision or None, end_reason)."""
        case_id = briefing.case_id
        messages: list = [{"role": "user", "content": briefing.text}]
        submit_attempts = 0
        nudges = 0

        for turn in range(1, self.config.max_turns + 1):
            try:
                message = self._call_model(messages)
            except anthropic.APIError as exc:
                self.log(f"API error on turn {turn}: {type(exc).__name__}: {exc}")
                self.transcript.append({"turn": turn, "api_error": f"{type(exc).__name__}: {exc}"})
                return None, f"api_error: {type(exc).__name__}"

            record = {"turn": turn, "model": message.model, "stop_reason": message.stop_reason,
                      "thinking": [], "text": [], "tool_calls": []}
            for block in message.content:
                if block.type == "thinking" and getattr(block, "thinking", ""):
                    record["thinking"].append(block.thinking)
                elif block.type == "text" and block.text.strip():
                    record["text"].append(block.text)
                elif block.type == "fallback":
                    record["text"].append(f"[model fallback: {_block_to_dict(block)}]")
            self.transcript.append(record)

            if message.stop_reason == "refusal":
                details = getattr(message, "stop_details", None)
                record["refusal"] = _block_to_dict(details) if details else None
                return None, "model_refusal"

            messages.append({"role": "assistant", "content": message.content})
            tool_uses = [b for b in message.content if b.type == "tool_use"]

            if not tool_uses:
                if message.stop_reason == "max_tokens":
                    messages.append({"role": "user", "content": "Your response was cut off. Continue, keep it concise, "
                                                                "and finish by calling submit_decision."})
                    continue
                nudges += 1
                if nudges > 2:
                    return None, "no_submit_decision"
                messages.append({"role": "user", "content": "You have not submitted a decision. Finish any remaining "
                                                            "actions, then call submit_decision."})
                continue

            results = []
            decision: Optional[dict] = None
            for use in tool_uses:
                args = use.input if isinstance(use.input, dict) else {}
                if use.name == "submit_decision":
                    submit_attempts += 1
                    decision, problems = validate_decision(case_id, args)
                    if decision:
                        content, is_error = "Decision recorded. The run is complete.", False
                    else:
                        content, is_error = "Decision rejected:\n- " + "\n- ".join(problems), True
                    record["tool_calls"].append({"tool": "submit_decision", "ok": not is_error,
                                                 "problems": None if decision else problems})
                elif use.name not in AGENT_TOOLS:
                    content, is_error = json.dumps({"ok": False, "error": {"code": "tool_not_available",
                                                    "message": f"{use.name} is not available to the agent."}}), True
                    record["tool_calls"].append({"tool": use.name, "ok": False, "error": "tool_not_available"})
                elif use.name not in ALLOWED_WHILE_BLOCKED and _blocking_escalation_open(case_id):
                    content = json.dumps({"ok": False, "error": {
                        "code": "blocked_pending_human_review",
                        "message": "A blocking escalation is open: a human must decide before further workflow or "
                                   "money actions. You may still send safety advice or holding messages, add notes "
                                   "or set a hold."}})
                    is_error = True
                    record["tool_calls"].append({"tool": use.name, "ok": False, "error": "blocked_pending_human_review"})
                else:
                    if "case_id" in (tool_specs([use.name])[0]["input_schema"].get("properties") or {}):
                        args = {**args, "case_id": case_id}
                    result = call_tool(use.name, args)
                    content, is_error = _tool_result_text(result), not result["ok"]
                    record["tool_calls"].append({
                        "tool": use.name, "ok": result["ok"], "input": args,
                        "id": (result.get("data") or {}).get("id") if isinstance(result.get("data"), dict) else None,
                        "error": (result.get("error") or {}).get("code"), "warnings": result.get("warnings"),
                        "duplicate": result.get("duplicate", False)})
                    self.log(f"  {use.name}: {'ok' if result['ok'] else 'FAILED ' + result['error']['code']}")
                results.append({"type": "tool_result", "tool_use_id": use.id, "content": content, "is_error": is_error})

            messages.append({"role": "user", "content": results})
            if decision:
                return decision, "submitted"
            if submit_attempts >= MAX_SUBMIT_ATTEMPTS:
                return None, "submit_decision_invalid"

        return None, "max_turns"


def _safety_net_escalation(case_id: str, reason: str, briefing: Optional[Briefing]) -> dict:
    """When the agent could not finish, hand the case to a human with what is known. Never fail silently."""
    facts = []
    if briefing:
        case = briefing.case
        facts.append(f"Property: {case.get('property')}")
        facts.append(f"Initial request: {(case.get('initial_request') or '')[:300]}")
        if case["events"]:
            last = case["events"][-1]
            facts.append(f"Latest event {last['id']} ({last['channel']} from {last['from']}): {last['body'][:300]}")
        facts.append(f"Safety screen level: {briefing.screen.get('level')}")
    actions = [f"{e['tool']} -> {(e.get('data') or {}).get('id', 'ok')}"
               for e in read_ledger(case_id) if e.get("ok") and e.get("side_effect") and not e.get("duplicate")]
    level = briefing.screen.get("level") if briefing else None
    result = call_tool("escalate_to_human", {
        "case_id": case_id,
        "priority": "P1_immediate" if level == "emergency" else "P2_same_day",
        "category": "tool_or_system_failure",
        "summary": f"The automated agent could not complete its decision for this case ({reason}). "
                   "A property manager needs to review the latest event and decide the next step.",
        "why_human_needed": f"Agent run ended without a validated decision: {reason}.",
        "facts_confirmed": facts or ["Case could not be loaded"],
        "actions_already_taken": actions,
        "recommended_next_steps": ["Review the latest event and the actions already taken",
                                   "Decide and send the next communication"],
        "blocks_automation": True,
    })
    escalation_id = (result.get("data") or {}).get("id")
    return {
        "decision_point": "Agent could not complete the decision automatically.",
        "situation_summary": f"Automated run ended early ({reason}); case handed to a human with context.",
        "stage": "other", "decision": "escalate",
        "rationale": f"Safety net: the agent run ended with '{reason}', so the case was escalated rather than left "
                     "unattended or guessed.",
        "alternatives_considered": [], "risk_level": level if level in ("emergency", "urgent", "routine") else "urgent",
        "hazard_assessment": None, "actions_taken": [a.split(" -> ")[-1] for a in actions] + ([escalation_id] if escalation_id else []),
        "escalated": bool(escalation_id), "evidence_events": [], "conflicts_and_noise": [], "assumptions": [],
        "open_questions": [], "red_flags": [],
        "next_step": {"owner": "human_reviewer", "action": "Review and decide the next step", "due_by": None},
        "confidence": "low", "safety_net": True, "safety_net_reason": reason,
        "escalation_error": None if result["ok"] else result["error"],
    }


def run_case(
    case_path: str,
    *,
    case_id: Optional[str] = None,
    cutoff_event: Optional[int] = None,
    cutoff_time: Optional[str] = None,
    task: Optional[str] = None,
    config: Optional[AgentConfig] = None,
    client: Optional[anthropic.Anthropic] = None,
    log: Callable[[str], None] = print,
) -> dict:
    """Run the agent on one case snapshot. Writes decision.json and transcript.json beside the ledger."""
    config = config or AgentConfig()
    client = client or anthropic.Anthropic(api_key=load_api_key(), max_retries=4)
    started = time.time()
    agent = AgentRun(config, client, log)
    briefing: Optional[Briefing] = None
    try:
        briefing = build_briefing(case_path, case_id=case_id, cutoff_event=cutoff_event,
                                  cutoff_time=cutoff_time, task=task)
        case_id = briefing.case_id
        log(f"[{case_id}] briefing ready ({len(briefing.case['events'])} events, screen={briefing.screen.get('level')})")
        decision, end_reason = agent.run(briefing)
    except BriefingError as exc:
        decision, end_reason = None, f"briefing_failed: {exc}"
        case_id = case_id or Path(case_path).name

    if decision is None:
        log(f"[{case_id}] safety net engaged: {end_reason}")
        decision = _safety_net_escalation(case_id, end_reason, briefing) if briefing else {
            "decision": "escalate", "safety_net": True, "safety_net_reason": end_reason, "actions_taken": [],
            "situation_summary": "Case could not be loaded.", "confidence": "low"}

    meta = {
        "case_id": case_id, "case_path": str(case_path), "cutoff_event": cutoff_event, "cutoff_time": cutoff_time,
        "task": task, "end_reason": end_reason, "model": config.model, "effort": config.effort,
        "turns": len(agent.transcript), "usage": agent.usage, "cost_usd": agent.cost_usd(),
        "duration_s": round(time.time() - started, 1),
        "visible_events": len(briefing.case["events"]) if briefing else 0,
        "now": briefing.case["now"] if briefing else None,
    }
    folder = case_dir(case_id)
    (folder / "decision.json").write_text(json.dumps({"meta": meta, "decision": decision}, indent=2, ensure_ascii=False))
    (folder / "transcript.json").write_text(json.dumps(
        {"meta": meta, "briefing": briefing.text if briefing else None, "turns": agent.transcript},
        indent=2, ensure_ascii=False, default=str))
    log(f"[{case_id}] {decision.get('decision')} | {end_reason} | {meta['turns']} turns | ${meta['cost_usd']} | {meta['duration_s']}s")
    return {"meta": meta, "decision": decision}
