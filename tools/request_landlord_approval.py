"""request_landlord_approval - ask the landlord to authorise attendance, a quote or works.

Sends the email and opens a pending approval request that stays visible in the case
state until a decision is recorded with record_landlord_decision.
"""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import Field, model_validator

from tools._common import (
    IdAllocator,
    Recipient,
    SideEffectInput,
    Tool,
    ToolFailure,
    ToolInput,
    build_state,
    case_now,
    check_outbound_text,
    hours_from_now,
    iso,
    resolve_case_file,
)

RequestType = Literal[
    "attend_and_diagnose",      # permission to send a contractor to look / fix if minor
    "approve_quote",            # a priced quote needs sign-off
    "approve_works",            # specific works without a formal quote
    "second_quote",             # landlord asked for / we recommend a comparison quote
    "choose_contractor_route",  # our contractor vs landlord's own vs tenant self-fix
]
VatTreatment = Literal["includes_vat", "plus_vat_20", "no_vat_charged", "unknown"]


class ApprovalOption(ToolInput):
    label: str = Field(..., min_length=2, max_length=200)
    contractor: Optional[str] = Field(None, max_length=120)
    amount_gbp: Optional[float] = Field(None, ge=0, le=250_000)
    vat_treatment: VatTreatment = "unknown"


class RequestLandlordApprovalInput(SideEffectInput):
    landlord: Recipient
    request_type: RequestType
    issue_summary: str = Field(..., min_length=10, max_length=2000)
    options: list[ApprovalOption] = Field(default_factory=list, max_length=6)
    recommended_option: Optional[str] = Field(None, description="Label of the option you recommend.")
    proposed_spend_limit_gbp: Optional[float] = Field(
        None, ge=0, le=250_000, description="For attend_and_diagnose: fix on the day if under this amount."
    )
    response_needed_within_hours: int = Field(72, ge=1, le=336)
    subject: str = Field(..., min_length=3, max_length=200)
    email_body: str = Field(..., min_length=30, max_length=20_000, description="The complete email to the landlord.")
    attachments: list[str] = Field(default_factory=list, max_length=10, description="e.g. the quote PDF.")

    @model_validator(mode="after")
    def _consistency(self) -> "RequestLandlordApprovalInput":
        if self.landlord.role != "landlord":
            raise ValueError("landlord.role must be 'landlord'")
        if self.request_type == "approve_quote" and not any(o.amount_gbp is not None for o in self.options) \
                and not self.attachments:
            raise ValueError("approve_quote needs at least one option with amount_gbp or the quote attached")
        labels = [o.label for o in self.options]
        if self.recommended_option and self.recommended_option not in labels:
            raise ValueError("recommended_option must match one of the option labels")
        return self


def _gross(option: ApprovalOption) -> Optional[float]:
    if option.amount_gbp is None:
        return None
    return round(option.amount_gbp * 1.2, 2) if option.vat_treatment == "plus_vat_20" else option.amount_gbp


def _handle(params: RequestLandlordApprovalInput) -> tuple[dict, list[str]]:
    warnings = check_outbound_text(params.case_id, f"{params.subject}\n{params.email_body}")
    for path in params.attachments:
        resolve_case_file(params.case_id, path)
    state = build_state(params.case_id)
    pending_same = [
        a["id"] for a in state["approval_requests"].values()
        if a["status"] == "pending" and a["request_type"] == params.request_type
    ]
    if pending_same:
        warnings.append(f"An approval of the same type is already pending ({pending_same}); this is a chase/resend.")
    if state["closed"]:
        raise ToolFailure("case_closed", "Case is closed; reload or reopen it before requesting approval.")

    options = []
    for o in params.options:
        item = o.model_dump(exclude_none=True)
        item["gross_gbp"] = _gross(o)
        options.append(item)
        if o.amount_gbp is not None and o.vat_treatment == "unknown":
            warnings.append(f"VAT treatment unknown for '{o.label}'; state clearly whether VAT is included.")
    amounts = [o.amount_gbp for o in params.options if o.amount_gbp is not None]
    body = params.email_body.replace(",", "")
    if amounts and not any(
        variant in body for a in amounts for variant in {f"{a:g}", f"{a:.2f}", f"{a:.0f}"}
    ):
        warnings.append("Quoted amounts do not appear in the email body; make sure the landlord sees the price.")

    ids = IdAllocator(params.case_id)
    approval_id = ids.next("APR")
    message = {
        "id": ids.next("MSG"),
        "channel": "email",
        "status": "sent",
        "delivery": "simulated",
        "sent_at": iso(case_now(params.case_id)),
        "to": [params.landlord.model_dump(exclude_none=True)],
        "subject": params.subject,
        "body": params.email_body,
        "purpose": "approval_request",
        "attachments": params.attachments,
    }
    return {
        "id": approval_id,
        "status": "pending",
        "request_type": params.request_type,
        "issue_summary": params.issue_summary,
        "options": options,
        "recommended_option": params.recommended_option,
        "proposed_spend_limit_gbp": params.proposed_spend_limit_gbp,
        "requested_at": message["sent_at"],
        "response_due_by": hours_from_now(params.case_id, params.response_needed_within_hours),
        "message": message,
    }, warnings


TOOL = Tool(
    name="request_landlord_approval",
    description="""
Ask the landlord to authorise spending: permission to send a contractor (optionally with a
fix-on-the-day spend limit), approval of a priced quote, specific works, a second quote, or a
choice between our contractor, the landlord's own, or tenant self-fix. Sends the email and
opens a pending approval with a response deadline. State prices and whether VAT is included.
Record the landlord's reply with record_landlord_decision before assigning paid work.
""",
    input_model=RequestLandlordApprovalInput,
    handler=_handle,
    side_effect=True,
)
