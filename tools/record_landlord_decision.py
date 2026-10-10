"""record_landlord_decision - record what the landlord decided, citing the event that proves it.

Paid work can only be assigned against a recorded decision (or an emergency/warranty basis),
so this is the audit point for every pound spent.
"""

from __future__ import annotations

import re
from typing import Literal, Optional

from pydantic import Field, model_validator

from tools._common import (
    SideEffectInput,
    Tool,
    ToolFailure,
    build_state,
    new_id,
    resolve_event,
)

Decision = Literal[
    "approved",                             # go ahead, no explicit cap
    "approved_with_limit",                  # go ahead up to spend_limit_gbp
    "rejected",                             # do not proceed
    "landlord_arranging_own_contractor",    # agency only tracks progress
    "tenant_may_self_fix",                  # landlord happy for tenant to sort it
    "needs_more_information",               # landlord asked a question / wants photos / second quote
]
LANDLORD_HINT = re.compile(r"\b(?:landlord|LL|owner)\b|approv|go ahead|authoris|authoriz", re.I)


class RecordLandlordDecisionInput(SideEffectInput):
    decision: Decision
    scope: str = Field(..., min_length=5, max_length=1000, description="What exactly the decision covers.")
    evidence_event: str = Field(..., description="Event id where the landlord gave this decision, e.g. 'event-012'.")
    approval_request_id: Optional[str] = Field(None, pattern=r"^APR-\d{3,}$")
    spend_limit_gbp: Optional[float] = Field(None, ge=0, le=250_000, description="Gross cap, incl. VAT.")
    conditions: list[str] = Field(default_factory=list, max_length=10)
    question_from_landlord: Optional[str] = Field(None, max_length=1000)

    @model_validator(mode="after")
    def _consistency(self) -> "RecordLandlordDecisionInput":
        if self.decision == "approved_with_limit" and self.spend_limit_gbp is None:
            raise ValueError("approved_with_limit requires spend_limit_gbp")
        if self.decision == "needs_more_information" and not self.question_from_landlord:
            raise ValueError("needs_more_information requires question_from_landlord")
        return self


def _handle(params: RecordLandlordDecisionInput) -> tuple[dict, list[str]]:
    warnings: list[str] = []
    event = resolve_event(params.case_id, params.evidence_event)
    sender = event.get("from", "")
    from_landlord = "landlord" in sender.lower()
    agency_record = event.get("channel", "").lower() in {"note", "call", "update", "hold"} and \
        LANDLORD_HINT.search(event.get("excerpt", ""))
    if not from_landlord and not agency_record:
        raise ToolFailure(
            "evidence_not_from_landlord",
            f"{event['id']} is from {sender!r} ({event.get('channel')}), not the landlord. A landlord decision "
            "must cite a landlord message or an agency note/call recording the landlord's instruction.",
            details={"event": event},
        )
    if not from_landlord:
        warnings.append(f"Decision evidenced by an agency {event.get('channel')} rather than the landlord directly.")

    state = build_state(params.case_id)
    if params.approval_request_id:
        request = state["approval_requests"].get(params.approval_request_id)
        if not request:
            raise ToolFailure("unknown_approval_request", f"No approval request {params.approval_request_id}.")
        if request["status"] != "pending":
            warnings.append(f"{params.approval_request_id} was already answered; recording an updated decision.")
    if params.decision == "approved" and params.spend_limit_gbp is None:
        warnings.append("Approved without a stated cap: send a quote back for approval if costs grow beyond a minor repair.")

    previous = [d["id"] for d in state["decisions"].values() if d["evidence_event"] == event["id"]]
    if previous:
        warnings.append(f"This event already backs decision(s) {previous}.")

    return {
        "id": new_id(params.case_id, "DEC"),
        "decision": params.decision,
        "scope": params.scope,
        "spend_limit_gbp": params.spend_limit_gbp,
        "conditions": params.conditions,
        "question_from_landlord": params.question_from_landlord,
        "approval_request_id": params.approval_request_id,
        "evidence_event": event["id"],
        "evidence_from": sender,
        "evidence_timestamp": event.get("timestamp"),
    }, warnings


TOOL = Tool(
    name="record_landlord_decision",
    description="""
Record the landlord's decision and cite the event that proves it (a landlord email, or an
agency note/call recording the landlord's instruction). Decisions: approved,
approved_with_limit (give spend_limit_gbp, including VAT), rejected,
landlord_arranging_own_contractor, tenant_may_self_fix, needs_more_information. Conditions
such as 'fix if simple, quote if expensive' go in conditions. Fails if the cited event is from
the tenant or contractor: a tenant saying 'the landlord agreed' is not approval.
""",
    input_model=RecordLandlordDecisionInput,
    handler=_handle,
    side_effect=True,
)
