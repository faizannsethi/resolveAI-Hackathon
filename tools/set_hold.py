"""set_hold - park the case while waiting on someone, with a mandatory follow-up time."""

from __future__ import annotations

from datetime import timedelta
from typing import Literal

from pydantic import Field

from tools._common import SideEffectInput, Tool, ToolFailure, build_state, case_now, iso, new_id, parse_datetime

Reason = Literal[
    "waiting_for_landlord", "waiting_for_tenant", "waiting_for_contractor", "waiting_for_parts",
    "waiting_for_third_party", "waiting_for_human_review", "other",
]
MAX_DAYS = 30


class SetHoldInput(SideEffectInput):
    reason: Reason
    waiting_for: str = Field(..., min_length=5, max_length=500, description="Exactly what we are waiting for.")
    follow_up_at: str = Field(..., description="ISO date-time to check again. Must be after now, within 30 days.")
    action_if_no_response: str = Field(
        ..., min_length=5, max_length=500, description="What to do at follow-up if nothing has arrived."
    )


def _handle(params: SetHoldInput) -> tuple[dict, list[str]]:
    warnings: list[str] = []
    state = build_state(params.case_id)
    if state["closed"]:
        raise ToolFailure("case_closed", "Case is closed; holds do not apply.")
    now = case_now(params.case_id)
    follow_up = parse_datetime(params.follow_up_at)
    if follow_up <= now:
        raise ToolFailure("follow_up_in_past", f"follow_up_at must be after now ({iso(now)}).")
    if follow_up > now + timedelta(days=MAX_DAYS):
        raise ToolFailure("follow_up_too_far", f"Follow-up must be within {MAX_DAYS} days; holds must not hide cases.")
    if follow_up > now + timedelta(days=7):
        warnings.append("Follow-up is more than 7 days away; make sure nobody is left without an update that long.")

    emergency_jobs = [j["id"] for j in state["jobs"].values() if j["urgency"] == "emergency"
                      and j["status"] not in ("closed", "replaced", "cancelled")]
    if emergency_jobs and follow_up > now + timedelta(hours=4):
        warnings.append(f"Emergency job(s) {emergency_jobs} open: follow up within 4 hours.")

    consecutive = 0
    for hold in reversed(state["holds"]):
        if hold["reason"] != params.reason:
            break
        consecutive += 1
    if consecutive >= 3:
        warnings.append(
            f"This is hold #{consecutive + 1} in a row for '{params.reason}'. Consider escalating, phoning, "
            "or changing approach instead of waiting again."
        )
    return {
        "id": new_id(params.case_id, "HOLD"),
        "reason": params.reason,
        "waiting_for": params.waiting_for,
        "set_at": iso(now),
        "follow_up_at": iso(follow_up),
        "action_if_no_response": params.action_if_no_response,
        "consecutive_same_reason": consecutive + 1,
    }, warnings


TOOL = Tool(
    name="set_hold",
    description="""
Put the case on hold while waiting for the landlord, tenant, contractor, parts or a third
party. You must say exactly what you are waiting for, when to follow up (after now, within 30
days) and what you will do if nothing arrives. Warns on long waits, open emergency jobs, and
repeated holds for the same reason (a sign to escalate or phone instead of waiting).
""",
    input_model=SetHoldInput,
    handler=_handle,
    side_effect=True,
)
