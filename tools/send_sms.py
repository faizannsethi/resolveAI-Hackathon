"""send_sms - send a short text message (simulated delivery)."""

from __future__ import annotations

import math
from typing import Literal

from pydantic import Field

from tools._common import (
    Recipient,
    SideEffectInput,
    Tool,
    ToolFailure,
    case_now,
    check_outbound_text,
    is_closed,
    iso,
    new_id,
)

SEGMENT = 160
MAX_SEGMENTS = 4


class SendSmsInput(SideEffectInput):
    to: Recipient
    body: str = Field(..., min_length=5, max_length=SEGMENT * MAX_SEGMENTS)
    purpose: Literal["reminder", "nudge_check_email", "appointment", "safety_advice", "status_update", "other"]
    allow_other_addresses: bool = False


def _handle(params: SendSmsInput) -> tuple[dict, list[str]]:
    if params.to.role == "agency_internal":
        raise ToolFailure("invalid_recipient", "Use add_note or escalate_to_human for internal messages, not SMS.")
    warnings = check_outbound_text(params.case_id, params.body, allow_other_addresses=params.allow_other_addresses)
    segments = math.ceil(len(params.body) / SEGMENT)
    if segments > 1:
        warnings.append(f"Message is {len(params.body)} characters ({segments} SMS segments); keep SMS short.")
    if not params.to.phone:
        warnings.append("No phone number given; routed to the mobile number on file for the case.")
    if is_closed(params.case_id):
        warnings.append("Case is closed: this SMS is sent after closure.")
    return {
        "id": new_id(params.case_id, "MSG"),
        "channel": "sms",
        "status": "sent",
        "delivery": "simulated",
        "sent_at": iso(case_now(params.case_id)),
        "to": params.to.model_dump(exclude_none=True),
        "body": params.body,
        "purpose": params.purpose,
        "segments": segments,
    }, warnings


TOOL = Tool(
    name="send_sms",
    description="""
Send a short SMS to a tenant, landlord or contractor: appointment reminders, 'please check
your email' nudges, or urgent safety advice. Up to 640 characters; aim for one 160-character
segment. Same placeholder and wrong-address checks as send_email. Do not use for internal notes.
""",
    input_model=SendSmsInput,
    handler=_handle,
    side_effect=True,
)
