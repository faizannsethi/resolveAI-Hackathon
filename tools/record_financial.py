"""record_financial - record a quote, invoice or payment and check it against what was approved."""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import Field, model_validator

from tools._common import (
    SideEffectInput,
    Tool,
    ToolFailure,
    build_state,
    new_id,
    resolve_case_file,
    resolve_event,
)

Kind = Literal["quote", "invoice", "payment_confirmation", "credit_note"]
Vat = Literal["includes_vat", "plus_vat_20", "no_vat_charged", "unknown"]
Payer = Literal["landlord", "tenant", "warranty_or_contractor", "agency", "unknown"]
Route = Literal[
    "deduct_from_rent", "landlord_pays_contractor_directly", "invoice_forwarded_to_landlord",
    "tenant_recharge", "no_charge", "undecided",
]


class RecordFinancialInput(SideEffectInput):
    kind: Kind
    contractor_name: str = Field(..., min_length=2, max_length=120)
    job_id: Optional[str] = Field(None, pattern=r"^JOB-\d{3,}$")
    description: str = Field(..., min_length=3, max_length=1000)
    amount_gbp: float = Field(..., ge=0, le=250_000)
    vat_treatment: Vat
    payer: Payer
    payment_route: Route
    evidence_event: Optional[str] = Field(None, description="Event where the quote/invoice was received.")
    evidence_attachment: Optional[str] = Field(None, description="Case path of the quote/invoice document.")
    reference: Optional[str] = Field(None, max_length=80)

    @model_validator(mode="after")
    def _evidence(self) -> "RecordFinancialInput":
        if not self.evidence_event and not self.evidence_attachment:
            raise ValueError("provide evidence_event and/or evidence_attachment")
        if self.payment_route == "no_charge" and self.amount_gbp > 0:
            raise ValueError("payment_route 'no_charge' requires amount_gbp 0")
        return self


def _gross(amount: float, vat: Vat) -> float:
    return round(amount * 1.2, 2) if vat == "plus_vat_20" else round(amount, 2)


def _handle(params: RecordFinancialInput) -> tuple[dict, list[str]]:
    warnings: list[str] = []
    event = resolve_event(params.case_id, params.evidence_event) if params.evidence_event else None
    if params.evidence_attachment:
        resolve_case_file(params.case_id, params.evidence_attachment)
    state = build_state(params.case_id)
    job = None
    if params.job_id:
        job = state["jobs"].get(params.job_id)
        if not job:
            raise ToolFailure("unknown_job", f"No job {params.job_id}.")

    gross = _gross(params.amount_gbp, params.vat_treatment)
    if params.vat_treatment == "unknown":
        warnings.append("VAT treatment unknown: confirm with the contractor before asking the landlord to pay.")

    if job and params.kind == "quote" and gross > job["spend_limit_gbp"]:
        warnings.append(
            f"Quote £{gross:,.2f} exceeds the job's authorised £{job['spend_limit_gbp']:,.2f}: landlord approval "
            "is needed before work goes ahead (request_landlord_approval with request_type 'approve_quote')."
        )
    if params.kind == "invoice":
        quotes = [f for f in state["financials"] if f["kind"] == "quote" and
                  (f.get("job_id") == params.job_id if params.job_id else f["contractor_name"] == params.contractor_name)]
        ceiling = max([q["gross_gbp"] for q in quotes] + ([job["spend_limit_gbp"]] if job else []), default=None)
        if ceiling is not None and gross > ceiling + 0.01:
            warnings.append(
                f"Invoice £{gross:,.2f} is above the approved/quoted £{ceiling:,.2f} by £{gross - ceiling:,.2f}: "
                "query it with the contractor before passing to the landlord."
            )
        if ceiling is None:
            warnings.append("No quote or authorised cap on record to check this invoice against.")
    if params.payment_route == "tenant_recharge":
        warnings.append("Recharging the tenant needs evidence of tenant fault and should be confirmed with the landlord.")
    if params.payment_route == "deduct_from_rent" and params.payer != "landlord":
        raise ToolFailure("inconsistent_route", "deduct_from_rent means the landlord pays from rent collected.")

    return {
        "id": new_id(params.case_id, "FIN"),
        "kind": params.kind,
        "contractor_name": params.contractor_name,
        "job_id": params.job_id,
        "description": params.description,
        "amount_gbp": params.amount_gbp,
        "vat_treatment": params.vat_treatment,
        "gross_gbp": gross,
        "payer": params.payer,
        "payment_route": params.payment_route,
        "evidence_event": event["id"] if event else None,
        "evidence_attachment": params.evidence_attachment,
        "reference": params.reference,
    }, warnings


TOOL = Tool(
    name="record_financial",
    description="""
Record a quote, invoice, payment confirmation or credit note, with evidence (event and/or
attachment), VAT treatment, who pays, and the payment route (deduct from rent, landlord pays
directly, invoice forwarded, tenant recharge, no charge). Warns when a quote exceeds the job's
authorised cap (approval needed), when an invoice is higher than the quote or cap, and when VAT
treatment is unclear. Gross amounts include 20% VAT where amounts are '+VAT'.
""",
    input_model=RecordFinancialInput,
    handler=_handle,
    side_effect=True,
)
