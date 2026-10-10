"""schedule_appointment - record a confirmed visit for a job and notify tenant and contractor."""

from __future__ import annotations

from datetime import timedelta
from typing import Literal, Optional

from pydantic import Field

from tools._common import (
    IdAllocator,
    SideEffectInput,
    Tool,
    ToolFailure,
    build_state,
    case_now,
    iso,
    load_context,
    parse_datetime,
)

Access = Literal["tenant_present", "keys_from_office", "key_safe", "management_key", "landlord_provides_access", "other"]


class ScheduleAppointmentInput(SideEffectInput):
    job_id: str = Field(..., pattern=r"^JOB-\d{3,}$")
    start: str = Field(..., description="ISO date-time of the visit start, e.g. '2026-10-14T09:00'. UTC if no zone.")
    end: Optional[str] = Field(None, description="ISO date-time the slot ends.")
    slot_description: Optional[str] = Field(None, max_length=200, description="e.g. 'AM slot, call 30 min ahead'.")
    access: Access
    access_details: Optional[str] = Field(None, max_length=500)
    confirmed_with: list[Literal["tenant", "contractor", "landlord"]] = Field(..., min_length=1)
    notify_parties: bool = True
    record_past_visit: bool = Field(
        False, description="Set true only to record a visit that already happened (date before now)."
    )


def _handle(params: ScheduleAppointmentInput) -> tuple[dict, list[str]]:
    warnings: list[str] = []
    state = build_state(params.case_id)
    if state["closed"]:
        raise ToolFailure("case_closed", "Case is closed.")
    job = state["jobs"].get(params.job_id)
    if not job:
        raise ToolFailure("unknown_job", f"No job {params.job_id}. Assign a contractor first.",
                          details={"jobs": list(state["jobs"])})
    if job["status"] in ("replaced", "cancelled", "closed"):
        raise ToolFailure("job_not_active", f"{params.job_id} is {job['status']}.")

    now = case_now(params.case_id)
    start = parse_datetime(params.start)
    end = parse_datetime(params.end) if params.end else None
    if end and end <= start:
        raise ToolFailure("invalid_slot", "Appointment end must be after start.")
    if start < now - timedelta(minutes=5) and not params.record_past_visit:
        raise ToolFailure(
            "appointment_in_past",
            f"Start {iso(start)} is before now ({iso(now)}). Check the date (records often mix up dates), "
            "or set record_past_visit=true if recording a visit that already took place.",
        )
    if start > now + timedelta(days=60):
        warnings.append("Appointment is more than 60 days away; check this is acceptable for the tenant and the issue.")
    if job["urgency"] == "emergency" and start > now + timedelta(hours=4) and not params.record_past_visit:
        warnings.append("Emergency job booked more than 4 hours out; confirm a make-safe is in place.")
    if job["urgency"] == "urgent" and start > now + timedelta(hours=24) and not params.record_past_visit:
        warnings.append("Urgent job booked more than 24 hours out.")
    if "tenant" not in params.confirmed_with and params.access == "tenant_present":
        warnings.append("Access relies on the tenant being present but the tenant has not confirmed the slot.")
    if start.weekday() >= 5:
        warnings.append("Appointment falls on a weekend; double-check the date.")

    prop = load_context(params.case_id).get("property") or "the property"
    when = iso(start) + (f" to {iso(end)}" if end else "") + (f" ({params.slot_description})" if params.slot_description else "")
    ids = IdAllocator(params.case_id)
    appt_id = ids.next("APT")
    messages = []
    if params.notify_parties and not params.record_past_visit:
        for role, text in (
            ("tenant", f"Your appointment with {job['contractor_name']} at {prop} is confirmed for {when}. "
                       "Please let us know if you need to change it."),
            ("contractor", f"Confirmed appointment for job {params.job_id} at {prop}: {when}. Access: "
                           f"{params.access.replace('_', ' ')}{' - ' + params.access_details if params.access_details else ''}."),
        ):
            messages.append({"id": ids.next("MSG"), "channel": "email", "status": "sent", "delivery": "simulated",
                             "sent_at": iso(now), "to": [{"role": role}], "subject": f"Appointment confirmed - {prop}",
                             "body": text, "purpose": "status_update"})
    return {
        "id": appt_id,
        "job_id": params.job_id,
        "status": "attended" if params.record_past_visit else "booked",
        "start": iso(start),
        "end": iso(end) if end else None,
        "slot_description": params.slot_description,
        "access": params.access,
        "access_details": params.access_details,
        "confirmed_with": params.confirmed_with,
        "messages": messages,
    }, warnings


TOOL = Tool(
    name="schedule_appointment",
    description="""
Record a confirmed visit slot for an existing job (from assign_contractor) and send
confirmations to tenant and contractor. Validates the date: it rejects slots in the past (the
records often contain wrong dates, so check against the latest event) unless
record_past_visit=true, and warns when an emergency or urgent job is booked too far out or when
access depends on a tenant who hasn't confirmed. A new booking supersedes the previous one.
""",
    input_model=ScheduleAppointmentInput,
    handler=_handle,
    side_effect=True,
)
