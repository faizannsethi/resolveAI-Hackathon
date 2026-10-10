"""add_note - add an internal note to the case (never sent to anyone)."""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import Field

from tools._common import SideEffectInput, Tool, case_now, iso, new_id, resolve_event

Category = Literal[
    "decision_rationale", "data_quality", "call_summary", "assumption", "policy_reference", "handover", "general",
]


class AddNoteInput(SideEffectInput):
    category: Category
    text: str = Field(..., min_length=5, max_length=5000)
    related_events: list[str] = Field(default_factory=list, max_length=20)
    pinned: Optional[bool] = Field(False, description="Pin important context for the next person on the case.")


def _handle(params: AddNoteInput) -> dict:
    events = [resolve_event(params.case_id, ref)["id"] for ref in params.related_events]
    return {
        "id": new_id(params.case_id, "NOTE"),
        "category": params.category,
        "text": params.text,
        "related_events": events,
        "pinned": bool(params.pinned),
        "created_at": iso(case_now(params.case_id)),
    }


TOOL = Tool(
    name="add_note",
    description="""
Add an internal note to the case file. Use it to record decision rationale, assumptions,
data-quality problems (e.g. 'event-016 mentions a different address'), call summaries and
handover context. Notes are never sent to tenants, landlords or contractors. Cite related
event ids where possible.
""",
    input_model=AddNoteInput,
    handler=_handle,
    side_effect=True,
)
