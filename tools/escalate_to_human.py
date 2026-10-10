"""escalate_to_human - hand the case to a person with everything they need to act fast."""

from __future__ import annotations

from typing import Literal

from pydantic import Field, model_validator

from tools._common import (
    Recipient,
    SideEffectInput,
    Tool,
    ToolInput,
    case_now,
    iso,
    new_id,
    resolve_event,
)

Priority = Literal["P1_immediate", "P2_same_day", "P3_next_working_day"]
Category = Literal[
    "safety_emergency", "conflicting_information", "missing_information", "financial_decision",
    "liability_dispute", "legal_or_compliance", "complaint_or_vulnerability", "tool_or_system_failure",
    "outside_agent_authority", "other",
]
RESPONSE_TARGET = {"P1_immediate": "15 minutes", "P2_same_day": "4 working hours", "P3_next_working_day": "1 working day"}


class DraftMessage(ToolInput):
    to: Recipient
    channel: Literal["email", "sms", "call"]
    body: str = Field(..., min_length=10, max_length=5000)


class EscalateInput(SideEffectInput):
    priority: Priority
    category: Category
    summary: str = Field(..., min_length=40, max_length=3000, description="What is going on, in plain words.")
    why_human_needed: str = Field(..., min_length=15, max_length=1500)
    facts_confirmed: list[str] = Field(..., min_length=1, max_length=30)
    unknowns_or_conflicts: list[str] = Field(default_factory=list, max_length=30)
    actions_already_taken: list[str] = Field(default_factory=list, max_length=30)
    recommended_next_steps: list[str] = Field(..., min_length=1, max_length=15)
    draft_messages: list[DraftMessage] = Field(default_factory=list, max_length=6)
    evidence_events: list[str] = Field(default_factory=list, max_length=30)
    blocks_automation: bool = Field(True, description="If true, the agent must not act further until a human responds.")

    @model_validator(mode="after")
    def _rules(self) -> "EscalateInput":
        if self.category == "safety_emergency" and self.priority != "P1_immediate":
            raise ValueError("safety_emergency escalations must be P1_immediate")
        return self


def _handle(params: EscalateInput) -> tuple[dict, list[str]]:
    warnings: list[str] = []
    events = [resolve_event(params.case_id, ref)["id"] for ref in params.evidence_events]
    if not events:
        warnings.append("No evidence events cited; the reviewer will have to search the history themselves.")
    if params.category in ("conflicting_information", "missing_information") and not params.unknowns_or_conflicts:
        warnings.append("List the specific unknowns/conflicts so the reviewer knows what to resolve.")
    if params.category == "safety_emergency" and not any(d.to.role == "tenant" for d in params.draft_messages):
        warnings.append("Safety emergency without a drafted tenant safety message; consider sending safety advice now.")
    return {
        "id": new_id(params.case_id, "ESC"),
        "status": "open",
        "priority": params.priority,
        "respond_within": RESPONSE_TARGET[params.priority],
        "category": params.category,
        "summary": params.summary,
        "why_human_needed": params.why_human_needed,
        "facts_confirmed": params.facts_confirmed,
        "unknowns_or_conflicts": params.unknowns_or_conflicts,
        "actions_already_taken": params.actions_already_taken,
        "recommended_next_steps": params.recommended_next_steps,
        "draft_messages": [d.model_dump(exclude_none=True) for d in params.draft_messages],
        "evidence_events": events,
        "blocks_automation": params.blocks_automation,
        "escalated_at": iso(case_now(params.case_id)),
        "routed_to": "property_manager_on_duty" if params.priority != "P1_immediate" else "on_call_manager",
    }, warnings


TOOL = Tool(
    name="escalate_to_human",
    description="""
Hand the case to a human property manager. Use for safety emergencies (P1), conflicting or
missing information you cannot resolve, money or liability decisions beyond your authority,
legal/compliance or complaint matters, vulnerable occupants, or repeated tool failures.
Provide a self-contained handover: summary, why a human is needed, confirmed facts,
unknowns/conflicts, actions already taken, recommended next steps, ready-to-send draft
messages, and the event ids that prove it. Escalating is often the correct decision. Set
blocks_automation=false only if routine follow-ups may continue meanwhile.
""",
    input_model=EscalateInput,
    handler=_handle,
    side_effect=True,
)
