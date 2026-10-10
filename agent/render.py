"""Render ANSWER.md and REASONING.md from the decision, the tool ledger and the transcript.

Rendering is deterministic code, not model output: every action listed here is taken from the
ledger, so the answer files can only report what the system actually did.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from tools._common import read_ledger, run_dir

ACTION_LABELS = {
    "send_email": "Email", "send_sms": "SMS", "place_call": "Phone call",
    "request_landlord_approval": "Landlord approval requested", "record_landlord_decision": "Landlord decision recorded",
    "assign_contractor": "Contractor instructed", "schedule_appointment": "Appointment booked",
    "record_financial": "Quote/invoice recorded", "set_hold": "Case put on hold", "add_note": "Internal note",
    "track_open_item": "Open item", "escalate_to_human": "ESCALATED to human", "close_case": "Case closed",
}


def _who(recipients) -> str:
    if isinstance(recipients, dict):
        recipients = [recipients]
    return ", ".join(f"{r.get('role')}{' (' + r['name'] + ')' if r.get('name') else ''}" for r in recipients or [])


def _quote(text: str) -> str:
    return "\n".join("> " + line if line.strip() else ">" for line in (text or "").strip().splitlines())


def _describe(entry: dict) -> list[str]:
    tool, d, a = entry["tool"], entry.get("data") or {}, entry.get("args") or {}
    label = ACTION_LABELS.get(tool, tool)
    out: list[str] = []
    if tool in ("send_email", "send_sms"):
        out.append(f"**{d['id']} - {label} to {_who(d.get('to'))}** ({d.get('purpose')})"
                   + (f": *{d['subject']}*" if d.get("subject") else ""))
        out.append(_quote(d.get("body", "")))
    elif tool == "place_call":
        out.append(f"**{d['id']} - {label} to {_who(d.get('to'))}** ({d.get('purpose')}); outcome: {d.get('outcome')}")
        out.append(_quote(d.get("script", "")))
    elif tool == "request_landlord_approval":
        opts = "; ".join(f"{o['label']}" + (f" £{o['amount_gbp']:,.2f} ({o['vat_treatment']})" if o.get("amount_gbp") is not None else "")
                         for o in d.get("options", []))
        out.append(f"**{d['id']} - {label}** ({d['request_type']}){': ' + opts if opts else ''}; reply due {d.get('response_due_by')}")
        msg = d.get("message") or {}
        out.append(_quote(msg.get("body", "")))
    elif tool == "record_landlord_decision":
        limit = f", limit £{d['spend_limit_gbp']:,.2f}" if d.get("spend_limit_gbp") is not None else ""
        out.append(f"**{d['id']} - {label}:** {d['decision']}{limit}: {d['scope']} (evidence {d['evidence_event']})")
    elif tool == "assign_contractor":
        out.append(f"**{d['id']} - {label}:** {d['contractor_name']} ({d['trade']}, {d['purpose']}, {d['urgency']}), "
                   f"cap £{d['spend_limit_gbp']:,.2f}, authorised by {d['authorisation']}"
                   + (f" ({d['decision_id']})" if d.get("decision_id") else ""))
        if d.get("emergency_assessment"):
            ea = d["emergency_assessment"]
            out.append(f"  Emergency assessment: {ea['hazard']}, credibility **{ea['credibility']}**: {ea['rationale']}")
        for m in d.get("messages", []):
            out.append(f"  - {m['id']} email to {_who(m.get('to'))}: *{m.get('subject')}*")
    elif tool == "schedule_appointment":
        out.append(f"**{d['id']} - {label}** for {d['job_id']}: {d['start']}"
                   + (f" to {d['end']}" if d.get("end") else "") + f", access: {d['access']}")
    elif tool == "record_financial":
        out.append(f"**{d['id']} - {label}:** {d['kind']} from {d['contractor_name']} £{d['amount_gbp']:,.2f} "
                   f"({d['vat_treatment']}, gross £{d['gross_gbp']:,.2f}), payer {d['payer']}, route {d['payment_route']}")
    elif tool == "set_hold":
        out.append(f"**{d['id']} - {label}** ({d['reason']}): waiting for {d['waiting_for']}. Follow up {d['follow_up_at']}; "
                   f"if nothing arrives: {d['action_if_no_response']}")
    elif tool == "add_note":
        out.append(f"**{d['id']} - {label}** ({d['category']}): {d['text']}")
    elif tool == "track_open_item":
        out.append(f"**{d['id']} - {label} {d['action']}**: {d.get('description')}"
                   + (f" -> {d['resolution']}" if d.get("resolution") else ""))
    elif tool == "escalate_to_human":
        out.append(f"**{d['id']} - {label}** [{d['priority']}, {d['category']}, respond within {d['respond_within']}]")
        out.append(f"  Summary: {d['summary']}")
        out.append(f"  Why a human: {d['why_human_needed']}")
        if d.get("recommended_next_steps"):
            out.append("  Recommended: " + "; ".join(d["recommended_next_steps"]))
    elif tool == "close_case":
        out.append(f"**{d['id']} - {label}:** {d['outcome']}, payment {d['payment_route']}. {d['summary']}")
    else:
        out.append(f"**{tool}** {json.dumps(a)[:300]}")
    return out


def _bullets(items) -> str:
    items = list(items or [])
    return "\n".join(f"- {i}" for i in items) if items else "- none"


def render_answer(case_id: str, result: dict, answer_dir: Path, with_trace: bool = False) -> None:
    meta, decision = result["meta"], result["decision"]
    ledger = read_ledger(case_id)
    actions = [e for e in ledger if e.get("ok") and e.get("side_effect") and not e.get("duplicate")]
    failures = [e for e in ledger if not e.get("ok")]
    supplied = [e["args"].get("path") for e in ledger if e["tool"] in ("read_attachment", "transcribe_audio")]

    answer = [
        f"# Case {case_id}: decision at {meta.get('now')}",
        f"**Decision:** `{decision.get('decision')}`  |  **Risk:** {decision.get('risk_level', 'n/a')}  |  "
        f"**Escalated:** {'yes' if decision.get('escalated') else 'no'}  |  **Confidence:** {decision.get('confidence')}",
    ]
    if decision.get("safety_net"):
        answer.append(f"> The agent could not complete its own decision ({decision.get('safety_net_reason')}); "
                      "the case was escalated to a human automatically.")
    answer += [
        "## What the system received",
        f"- Case input: `{meta['case_path']}`, {meta['visible_events']} visible event(s), history cut at "
        f"{'event ' + str(meta['cutoff_event']) if meta.get('cutoff_event') else 'the end of the supplied history'}",
        f"- Documents read: {', '.join(sorted(set(p for p in supplied if p))) or 'none'}",
        "## Decision point",
        decision.get("decision_point", ""),
        "## Situation",
        decision.get("situation_summary", ""),
        "## Actions taken",
        "\n\n".join("\n".join(_describe(e)) for e in actions) or "No actions taken (deliberately).",
        "## Escalation",
        ("Escalated to a human: see the ESC entry above." if decision.get("escalated") else "Not escalated."),
        "## What failed",
        _bullets(f"{e['tool']} -> {e['error']['code']}: {e['error']['message']}" for e in failures),
        "## Next step",
        (lambda n: f"**{n.get('owner')}**: {n.get('action')}" + (f" (by {n['due_by']})" if n.get("due_by") else ""))(
            decision.get("next_step") or {}),
        "## Final result",
        f"`{decision.get('decision')}`: {decision.get('rationale', '')}",
    ]

    reasoning = [
        f"# Reasoning: {case_id}",
        "## Why this decision", decision.get("rationale", ""),
        "## Alternatives considered", _bullets(decision.get("alternatives_considered")),
        "## Safety and credibility", decision.get("hazard_assessment") or "No live hazard identified.",
        "## Evidence (events relied on)", _bullets(decision.get("evidence_events")),
        "## Conflicting or unreliable information", _bullets(decision.get("conflicts_and_noise")),
        "## Assumptions", _bullets(decision.get("assumptions")),
        "## Open questions", _bullets(decision.get("open_questions")),
        "## Red flags", _bullets(decision.get("red_flags")),
    ]
    transcript_file = run_dir() / case_id / "transcript.json"
    if transcript_file.exists():
        turns = json.loads(transcript_file.read_text()).get("turns", [])
        trace = []
        for t in turns:
            for th in t.get("thinking", []):
                trace.append(f"**Turn {t['turn']}, reasoning summary:** {th.strip()}")
            for tx in t.get("text", []):
                trace.append(f"**Turn {t['turn']}, note:** {tx.strip()}")
            for c in t.get("tool_calls", []):
                status = "ok" if c.get("ok") else f"FAILED ({c.get('error') or c.get('problems')})"
                trace.append(f"- turn {t['turn']}: `{c['tool']}` -> {status}" + (f" [{c['id']}]" if c.get("id") else ""))
        reasoning += ["## Agent trace (model reasoning summaries and tool calls)", "\n\n".join(trace) or "- none"]
    reasoning += [
        "## Full tool ledger",
        "| # | tool | ok | result / error |\n|---|---|---|---|\n" + "\n".join(
            f"| {e['seq']} | {e['tool']} | {'yes' if e['ok'] else 'no'} | "
            f"{(e.get('data') or {}).get('id', '') if e['ok'] and isinstance(e.get('data'), dict) else (e.get('error') or {}).get('code', '')}"
            f"{' (duplicate)' if e.get('duplicate') else ''} |" for e in ledger),
        "## Run metadata",
        f"- model `{meta['model']}`, effort `{meta['effort']}`, {meta['turns']} model turns, end: `{meta['end_reason']}`",
        f"- tokens: {meta['usage']}, est. cost ${meta['cost_usd']}, {meta['duration_s']}s",
    ]

    answer_dir.mkdir(parents=True, exist_ok=True)
    (answer_dir / "ANSWER.md").write_text("\n\n".join(answer) + "\n", encoding="utf-8")
    (answer_dir / "REASONING.md").write_text("\n\n".join(reasoning) + "\n", encoding="utf-8")
    if with_trace:
        trace_dir = answer_dir / "trace"
        trace_dir.mkdir(exist_ok=True)
        for name in ("decision.json", "transcript.json", "ledger.jsonl", "context.json"):
            src = run_dir() / case_id / name
            if src.exists():
                shutil.copy(src, trace_dir / name)
