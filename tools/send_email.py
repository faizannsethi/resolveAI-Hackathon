"""send_email - send an email to a tenant, landlord, contractor or other party (simulated delivery)."""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import Field

from tools._common import (
    Recipient,
    SideEffectInput,
    Tool,
    check_outbound_text,
    is_closed,
    iso,
    case_now,
    load_context,
    new_id,
    resolve_case_file,
    resolve_event,
)

Purpose = Literal[
    "acknowledgement", "status_update", "request_information", "approval_request", "instruction",
    "chase", "safety_advice", "quote_or_invoice", "closure", "other",
]


class SendEmailInput(SideEffectInput):
    to: list[Recipient] = Field(..., min_length=1, max_length=10)
    cc: list[Recipient] = Field(default_factory=list, max_length=10)
    subject: str = Field(..., min_length=3, max_length=200)
    body: str = Field(..., min_length=10, max_length=20_000)
    purpose: Purpose = Field(..., description="Why this email is being sent; used in the case summary.")
    attachments: list[str] = Field(
        default_factory=list, max_length=10, description="Case-relative file paths to attach."
    )
    in_reply_to_event: Optional[str] = Field(None, description="Event id this email responds to, if any.")
    allow_other_addresses: bool = Field(
        False, description="Set true only when deliberately mentioning another property's address."
    )


def _handle(params: SendEmailInput) -> tuple[dict, list[str]]:
    context = load_context(params.case_id)
    warnings = check_outbound_text(
        params.case_id, f"{params.subject}\n{params.body}", allow_other_addresses=params.allow_other_addresses
    )
    reply_to = resolve_event(params.case_id, params.in_reply_to_event)["id"] if params.in_reply_to_event else None
    files = [str(resolve_case_file(params.case_id, a).name) for a in params.attachments]

    if is_closed(params.case_id):
        warnings.append("Case is closed: this email is sent after closure. Reopen if work is needed.")
    if context.get("property") and context["property"].split(",")[0].lower() not in params.body.lower():
        warnings.append("Body does not mention the property address; recipients handling many properties may be confused.")
    roles = {r.role for r in params.to}
    if "tenant" in roles and "contractor" in roles:
        warnings.append("Tenant and contractor on one email: make sure no private landlord/cost details are included.")
    no_address = [r.role + (f" ({r.name})" if r.name else "") for r in params.to if not r.email]
    if no_address:
        warnings.append(f"No email address given for {no_address}; routed to the contact on file for the case.")

    return {
        "id": new_id(params.case_id, "MSG"),
        "channel": "email",
        "status": "sent",
        "delivery": "simulated",
        "sent_at": iso(case_now(params.case_id)),
        "to": [r.model_dump(exclude_none=True) for r in params.to],
        "cc": [r.model_dump(exclude_none=True) for r in params.cc],
        "subject": params.subject,
        "body": params.body,
        "purpose": params.purpose,
        "attachments": files,
        "in_reply_to_event": reply_to,
    }, warnings


TOOL = Tool(
    name="send_email",
    description="""
Send an email about the loaded case. Recipients are given by role (tenant, landlord,
contractor, agency_internal, block_management, other) with optional name/email. Fails if the
text contains unfilled placeholders such as [Name] or {date}, or mentions a property address
other than this case's (a common error). Attachments must be files from the case folder.
Repeating an identical call does not send twice. Write complete, ready-to-send text.
""",
    input_model=SendEmailInput,
    handler=_handle,
    side_effect=True,
)
