"""close_case - close a case only when the work is evidenced and nothing is left hanging."""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import Field

from tools._common import (
    SideEffectInput, Tool, ToolFailure, ToolInput, build_state, case_now, iso, new_id, resolve_event,
)

Outcome = Literal[
    "resolved_by_contractor", "resolved_by_landlord_own_contractor", "resolved_by_tenant_self_help",
    "resolved_under_warranty", "no_fault_found", "tenant_responsibility_advised", "duplicate_request",
    "withdrawn_by_tenant", "declined_by_landlord", "no_further_action",
]
Payment = Literal[
    "no_charge", "landlord_pays_contractor_directly", "deduct_from_rent", "invoice_forwarded_to_landlord",
    "warranty", "tenant_recharge", "not_applicable",
]
Check = Literal["done", "not_applicable", "outstanding"]


class Checks(ToolInput):
    work_completion_confirmed: Check
    tenant_informed: Check
    landlord_informed: Check
    invoice_handled: Check
    keys_returned: Check


class CloseCaseInput(SideEffectInput):
    outcome: Outcome
    payment_route: Payment
    completion_evidence_events: list[str] = Field(
        ..., min_length=1, max_length=10, description="Events proving the outcome (e.g. contractor or tenant confirmation)."
    )
    checks: Checks
    summary: str = Field(..., min_length=20, max_length=2000)
    override_reason: Optional[str] = Field(
        None, min_length=20, max_length=1000,
        description="Only to close despite an 'outstanding' check; explains why that is acceptable.",
    )


DIRECT_EVIDENCE = {
    "resolved_by_contractor": ("contractor", "provider", "maintenance"),
    "resolved_by_landlord_own_contractor": ("landlord",),
    "resolved_by_tenant_self_help": ("tenant",),
}


def _handle(params: CloseCaseInput) -> tuple[dict, list[str]]:
    warnings: list[str] = []
    state = build_state(params.case_id)
    if state["closed"]:
        raise ToolFailure("already_closed", f"Case already closed ({state['closed']['id']}).")

    blockers = []
    blockers += [f"{e['id']} escalation is open ({e['category']})" for e in state["escalations"].values()
                 if e["status"] == "open" and e["blocks_automation"]]
    blockers += [f"{a['id']} landlord approval request is still pending" for a in state["approval_requests"].values()
                 if a["status"] == "pending"]
    blockers += [f"{i['id']} open item: {i['description']}" for i in state["open_items"].values() if i["status"] == "open"]
    if blockers:
        raise ToolFailure(
            "open_items_remaining",
            "Cannot close while items are unresolved. Resolve them (track_open_item / record_landlord_decision) "
            "or wait for human review.",
            details={"blockers": blockers},
        )

    outstanding = [name for name, value in params.checks.model_dump().items() if value == "outstanding"]
    if outstanding and not params.override_reason:
        raise ToolFailure(
            "checks_outstanding",
            f"Checks still outstanding: {outstanding}. Complete them or give override_reason.",
        )
    if outstanding:
        warnings.append(f"Closed with outstanding checks {outstanding}: {params.override_reason}")

    evidence = [resolve_event(params.case_id, ref) for ref in params.completion_evidence_events]
    expected = DIRECT_EVIDENCE.get(params.outcome)
    if expected and not any(any(word in e.get("from", "").lower() for word in expected) or
                            e.get("channel", "").lower() in {"note", "call"} for e in evidence):
        warnings.append(
            f"Outcome '{params.outcome}' is not backed by a message from the {expected[0]} or an agency note/call; "
            "make sure completion was actually confirmed."
        )
    if params.payment_route == "no_charge" and any(f["kind"] == "invoice" and f["gross_gbp"] > 0 for f in state["financials"]):
        warnings.append("Payment route 'no_charge' but a non-zero invoice is on record.")
    if params.payment_route == "tenant_recharge":
        warnings.append("Closing with a tenant recharge: ensure the tenant was told and the landlord agreed.")
    active_jobs = [j["id"] for j in state["jobs"].values() if j["status"] in ("assigned", "scheduled", "quoted")]
    if active_jobs and params.outcome not in ("resolved_by_contractor", "resolved_under_warranty"):
        warnings.append(f"Job(s) {active_jobs} are still active; tell the contractor the job is cancelled/closed.")

    return {
        "id": new_id(params.case_id, "CLOSE"),
        "outcome": params.outcome,
        "payment_route": params.payment_route,
        "completion_evidence_events": [e["id"] for e in evidence],
        "checks": params.checks.model_dump(),
        "summary": params.summary,
        "override_reason": params.override_reason,
        "closed_at": iso(case_now(params.case_id)),
    }, warnings


TOOL = Tool(
    name="close_case",
    description="""
Close the case. Requires the outcome, payment route, the event(s) proving completion, a
checklist (work confirmed, tenant informed, landlord informed, invoice handled, keys returned:
each done / not_applicable / outstanding) and a summary. Refuses while there is an open
blocking escalation, a pending landlord approval, or an unresolved open item (e.g. an
unanswered landlord question). Refuses outstanding checks unless override_reason explains why.
Do not close just because the history has gone quiet.
""",
    input_model=CloseCaseInput,
    handler=_handle,
    side_effect=True,
)
