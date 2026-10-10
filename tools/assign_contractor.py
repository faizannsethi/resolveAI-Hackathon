"""assign_contractor - instruct a contractor, with an authorisation basis for any spend.

Every assignment must say why spending is allowed: a recorded landlord decision, an
emergency make-safe, a warranty/no-cost repair, or the agency's standing authority (off by
default; set AGENCY_STANDING_LIMIT_GBP to enable). The contractor is always told the spend
cap and to quote before exceeding it. The tenant is notified unless told otherwise.
"""

from __future__ import annotations

import os
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
    iso,
    load_context,
    resolve_event,
)

Trade = Literal[
    "plumbing", "drainage", "electrical", "gas_heating", "appliance_repair", "locksmith", "glazing_windows",
    "carpentry_doors", "roofing", "damp_mould", "pest_control", "cleaning", "gardening", "decorating_flooring",
    "general_maintenance", "other",
]
Purpose = Literal[
    "attend_diagnose_and_quote",  # look, report, quote before any paid work
    "attend_and_repair",          # fix on the day within the spend cap
    "quote_only",                 # e.g. a second comparison quote
    "complete_approved_works",    # quote already approved
    "warranty_repair",            # installer/manufacturer repair at no cost to landlord
    "emergency_make_safe",
]
Authorisation = Literal["landlord_decision", "emergency_make_safe", "warranty_or_no_cost", "agency_standing_authority"]
Urgency = Literal["emergency", "urgent", "routine"]
Credibility = Literal["confirmed", "credible", "uncertain", "doubtful"]
Corroboration = Literal[
    "photo_or_video", "professional_confirmed",  # contractor, gas engineer, fire service, etc.
    "multiple_independent_reports", "consistent_specific_details", "agency_verified_by_call",
    "third_party_report", "safety_screen_match",
]


class EmergencyAssessment(ToolInput):
    hazard: str = Field(..., min_length=5, max_length=300, description="The specific hazard, e.g. 'water through ceiling light'.")
    credibility: Credibility = Field(
        ..., description="confirmed/credible allow dispatch; uncertain/doubtful mean verify or escalate first."
    )
    evidence_events: list[str] = Field(..., min_length=1, max_length=10)
    corroboration: list[Corroboration] = Field(default_factory=list, max_length=7)
    doubts: list[str] = Field(
        default_factory=list, max_length=10,
        description="Anything pointing to exaggeration, panic, hoax or a resolved/old issue.",
    )
    rationale: str = Field(..., min_length=20, max_length=1500)


ATTEND_WITHIN = {"emergency": "within 4 hours", "urgent": "within 24 hours", "routine": "as soon as possible (target 14 days)"}


class AssignContractorInput(SideEffectInput):
    contractor_name: str = Field(..., min_length=2, max_length=120)
    trade: Trade
    purpose: Purpose
    urgency: Urgency
    job_description: str = Field(..., min_length=10, max_length=4000, description="What the contractor should do.")
    authorisation: Authorisation
    decision_id: Optional[str] = Field(None, pattern=r"^DEC-\d{3,}$", description="Required for landlord_decision.")
    authorisation_note: Optional[str] = Field(
        None, max_length=1000, description="Required for emergency, warranty and standing-authority assignments."
    )
    spend_limit_gbp: float = Field(..., ge=0, le=250_000, description="Gross cap incl. VAT; 0 for quote-only/no-cost.")
    contractor: Optional[Recipient] = None
    tenant: Optional[Recipient] = Field(None, description="Tenant contact to pass to the contractor (with consent).")
    access_notes: Optional[str] = Field(None, max_length=1000, description="Keys, codes, pets, availability.")
    landlord: Optional[Recipient] = Field(
        None, description="Landlord to inform. Emergency and no-cost jobs always send the landlord an FYI."
    )
    notify_tenant: bool = True
    emergency_assessment: Optional[EmergencyAssessment] = Field(
        None, description="Required for emergency_make_safe: is this a genuine, current hazard?"
    )
    replaces_job_id: Optional[str] = Field(None, pattern=r"^JOB-\d{3,}$")
    replacement_reason: Optional[str] = Field(None, max_length=500)

    @model_validator(mode="after")
    def _consistency(self) -> "AssignContractorInput":
        if self.authorisation == "landlord_decision" and not self.decision_id:
            raise ValueError("authorisation 'landlord_decision' requires decision_id (from record_landlord_decision)")
        if self.authorisation != "landlord_decision" and not (self.authorisation_note and len(self.authorisation_note) >= 15):
            raise ValueError("authorisation_note (15+ chars) is required unless authorised by a landlord decision")
        if self.authorisation == "emergency_make_safe" and self.urgency != "emergency":
            raise ValueError("emergency_make_safe authorisation requires urgency 'emergency'")
        if self.authorisation == "emergency_make_safe" and not self.emergency_assessment:
            raise ValueError("emergency_make_safe requires emergency_assessment (is the hazard genuine and current?)")
        if self.purpose in ("quote_only", "warranty_repair") and self.spend_limit_gbp > 0:
            raise ValueError(f"purpose '{self.purpose}' must have spend_limit_gbp 0")
        if self.replaces_job_id and not self.replacement_reason:
            raise ValueError("replacement_reason is required with replaces_job_id")
        if self.authorisation == "warranty_or_no_cost" and self.spend_limit_gbp > 0:
            raise ValueError("warranty_or_no_cost must have spend_limit_gbp 0; any cost needs landlord approval")
        if self.landlord and self.landlord.role != "landlord":
            raise ValueError("landlord.role must be 'landlord'")
        if self.contractor and self.contractor.role != "contractor":
            raise ValueError("contractor.role must be 'contractor'")
        if self.tenant and self.tenant.role != "tenant":
            raise ValueError("tenant.role must be 'tenant'")
        return self


def _check_authorisation(params: AssignContractorInput, state: dict) -> list[str]:
    warnings: list[str] = []
    if params.authorisation == "landlord_decision":
        decision = state["decisions"].get(params.decision_id)
        if not decision:
            raise ToolFailure("unknown_decision", f"No landlord decision {params.decision_id} recorded.")
        kind = decision["decision"]
        if kind in ("rejected", "landlord_arranging_own_contractor", "tenant_may_self_fix", "needs_more_information"):
            raise ToolFailure(
                "not_authorised",
                f"Landlord decision {params.decision_id} is '{kind}', which does not authorise our contractor.",
            )
        limit = decision.get("spend_limit_gbp")
        if limit is not None and params.spend_limit_gbp > limit:
            raise ToolFailure(
                "exceeds_landlord_limit",
                f"Spend cap £{params.spend_limit_gbp:.2f} exceeds the landlord's limit of £{limit:.2f}.",
            )
        if limit is None and params.purpose == "attend_and_repair" and params.spend_limit_gbp > 300:
            warnings.append("High fix-on-the-day cap without an explicit landlord limit; consider quote-first.")
    elif params.authorisation == "agency_standing_authority":
        standing = float(os.environ.get("AGENCY_STANDING_LIMIT_GBP", "0") or 0)
        if standing <= 0:
            raise ToolFailure(
                "no_standing_authority",
                "The agency has no standing spend authority configured. Get landlord approval first "
                "(or use emergency_make_safe if there is a genuine emergency).",
            )
        if params.spend_limit_gbp > standing:
            raise ToolFailure("exceeds_standing_authority",
                              f"Standing authority covers up to £{standing:.2f} only.")
    elif params.authorisation == "emergency_make_safe":
        assessment = params.emergency_assessment
        for ref in assessment.evidence_events:
            resolve_event(params.case_id, ref)
        if assessment.credibility in ("uncertain", "doubtful"):
            raise ToolFailure(
                "emergency_not_verified",
                f"Emergency credibility is '{assessment.credibility}'. Do not dispatch on an unverified report: "
                "give the tenant safety advice now, verify (call, ask for photos, safety_screen verify_by_asking), "
                "then reassess - or escalate_to_human if it cannot be verified quickly.",
                details={"doubts": assessment.doubts},
            )
        if not assessment.corroboration:
            warnings.append("Emergency dispatched on a single uncorroborated report; verify by phone as soon as possible.")
        if assessment.doubts and assessment.credibility == "credible":
            warnings.append(f"Dispatched despite doubts {assessment.doubts}; record the reasoning with add_note.")
        warnings.append("Emergency make-safe without prior approval (agent judgement): landlord sent an FYI. "
                        "Any work beyond making safe needs landlord approval.")
    return warnings


def _handle(params: AssignContractorInput) -> tuple[dict, list[str]]:
    context = load_context(params.case_id)
    state = build_state(params.case_id)
    if state["closed"]:
        raise ToolFailure("case_closed", "Case is closed; reload or reopen it before assigning work.")
    warnings = _check_authorisation(params, state)

    active = [
        j for j in state["jobs"].values()
        if j["trade"] == params.trade and j["status"] not in ("replaced", "cancelled", "closed")
    ]
    if params.replaces_job_id:
        if params.replaces_job_id not in state["jobs"]:
            raise ToolFailure("unknown_job", f"No job {params.replaces_job_id} to replace.")
    elif active and params.purpose != "quote_only":
        raise ToolFailure(
            "duplicate_assignment",
            f"{active[0]['id']} ({active[0]['contractor_name']}) is already active for {params.trade}. "
            "Use replaces_job_id to switch contractor, or purpose 'quote_only' for a comparison quote.",
        )

    prop = context.get("property") or "the property"
    texts = [params.job_description, params.access_notes or ""]
    warnings += check_outbound_text(params.case_id, "\n".join(texts))

    if params.tenant and (params.tenant.phone or params.tenant.email):
        tenant_line = f"Tenant: {params.tenant.name or 'tenant'} - {params.tenant.phone or params.tenant.email}"
    else:
        tenant_line = "Tenant contact: as held on the job portal for this property."
        warnings.append("No tenant contact passed; contractor relies on contact details on file.")

    if params.purpose in ("quote_only", "attend_diagnose_and_quote"):
        money = "Please attend, diagnose and send a quote with photos before carrying out any chargeable work."
    elif params.purpose == "warranty_repair":
        money = "This is a warranty / no-cost repair: please confirm in writing before any charge is incurred."
    else:
        money = (f"You are authorised up to £{params.spend_limit_gbp:,.2f} including VAT. If the work will cost more, "
                 "stop and send a quote with photos for approval before proceeding.")

    ids = IdAllocator(params.case_id)
    job_id = ids.next("JOB")
    now = iso(case_now(params.case_id))
    contractor_body = (
        f"Job {job_id} - {params.trade.replace('_', ' ')} ({params.urgency})\n"
        f"Property: {prop}\n\n{params.job_description}\n\n"
        f"Please attend {ATTEND_WITHIN[params.urgency]} and confirm the appointment time with us.\n"
        f"{money}\n{tenant_line}\n"
        + (f"Access: {params.access_notes}\n" if params.access_notes else "")
        + "Please send completion photos and your invoice quoting the job number."
    )
    messages = [{
        "id": ids.next("MSG"),
        "channel": "email",
        "status": "sent",
        "delivery": "simulated",
        "sent_at": now,
        "to": [(params.contractor.model_dump(exclude_none=True) if params.contractor
                else {"role": "contractor", "name": params.contractor_name})],
        "subject": f"New job {job_id}: {params.trade.replace('_', ' ')} at {prop}",
        "body": contractor_body,
        "purpose": "instruction",
    }]
    if params.notify_tenant:
        tenant_body = (
            f"Your repair at {prop} has been passed to {params.contractor_name}. They will contact you to arrange "
            f"a visit ({ATTEND_WITHIN[params.urgency]}). Please let them know about any pets or access needs."
        )
        if params.purpose in ("quote_only", "attend_diagnose_and_quote"):
            tenant_body += " The first visit is to assess the problem; any further work needs the landlord's approval."
        messages.append({
            "id": ids.next("MSG"),
            "channel": "email",
            "status": "sent",
            "delivery": "simulated",
            "sent_at": now,
            "to": [(params.tenant.model_dump(exclude_none=True) if params.tenant else {"role": "tenant"})],
            "subject": f"Repair update: {params.contractor_name} will be in touch",
            "body": tenant_body,
            "purpose": "status_update",
        })

    if params.authorisation in ("emergency_make_safe", "warranty_or_no_cost"):
        if params.authorisation == "emergency_make_safe":
            subject = f"Urgent - emergency make-safe instructed at {prop}"
            reason = (f"Because this is an emergency, we have instructed {params.contractor_name} to make the property safe "
                      f"without waiting for approval, capped at £{params.spend_limit_gbp:,.2f} including VAT.\n"
                      f"Hazard: {params.emergency_assessment.hazard} (assessed as {params.emergency_assessment.credibility}).")
            follow_on = "Any further repair beyond making safe will be quoted and sent to you for approval first."
        else:
            subject = f"For information - no-cost repair instructed at {prop}"
            reason = (f"We have instructed {params.contractor_name} to carry out this repair at no cost to you "
                      "(warranty / contractor's own remedial work), so no approval is needed.")
            follow_on = "If the contractor says any charge applies, we will come back to you for approval before it goes ahead."
        messages.append({
            "id": ids.next("MSG"),
            "channel": "email",
            "status": "sent",
            "delivery": "simulated",
            "sent_at": now,
            "to": [(params.landlord.model_dump(exclude_none=True) if params.landlord else {"role": "landlord"})],
            "subject": subject,
            "body": f"{reason}\n\nIssue: {params.job_description}\nReason: {params.authorisation_note}\n\n{follow_on}",
            "purpose": "status_update",
        })

    return {
        "id": job_id,
        "status": "assigned",
        "contractor_name": params.contractor_name,
        "trade": params.trade,
        "purpose": params.purpose,
        "urgency": params.urgency,
        "job_description": params.job_description,
        "authorisation": params.authorisation,
        "decision_id": params.decision_id,
        "authorisation_note": params.authorisation_note,
        "spend_limit_gbp": params.spend_limit_gbp,
        "emergency_assessment": (params.emergency_assessment.model_dump()
                                 if params.emergency_assessment else None),
        "replaces_job_id": params.replaces_job_id,
        "replacement_reason": params.replacement_reason,
        "assigned_at": now,
        "messages": messages,
    }, warnings


TOOL = Tool(
    name="assign_contractor",
    description="""
Instruct a contractor and (by default) notify the tenant. You must state the authorisation
basis: landlord_decision (with decision_id from record_landlord_decision), emergency_make_safe
(urgency 'emergency' only, keep to making safe), warranty_or_no_cost, or
agency_standing_authority (only if configured). Emergency and no-cost routes are the agent's
judgement call. Emergencies need an emergency_assessment: dispatch only if the hazard is
'confirmed' or 'credible' and current; 'uncertain' or 'doubtful' reports (panic, exaggeration,
hoax, already-resolved issue) are refused, so verify or escalate instead. For both routes: no approval is needed, the landlord is automatically sent an FYI, and a
no-cost job must have spend_limit_gbp 0. Fails if the spend cap exceeds the landlord's
limit, if the landlord declined or is using their own contractor, or if a job for the same
trade is already active (use replaces_job_id, or purpose 'quote_only' for a second quote). The
contractor is told the cap and to quote before exceeding it.
""",
    input_model=AssignContractorInput,
    handler=_handle,
    side_effect=True,
)
