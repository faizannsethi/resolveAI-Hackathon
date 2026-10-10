"""get_case_state - summarise everything the agent has done on a case and what is pending."""

from __future__ import annotations

from datetime import timedelta

from pydantic import Field

from tools._common import CaseScopedInput, Tool, build_state, case_now, iso, load_context, parse_datetime


class GetCaseStateInput(CaseScopedInput):
    include_message_bodies: bool = Field(False, description="Include full text of messages sent.")


def _handle(params: GetCaseStateInput) -> dict:
    context = load_context(params.case_id)
    state = build_state(params.case_id)
    now = case_now(params.case_id)

    if not params.include_message_bodies:
        for msg in state["messages"]:
            msg["body"] = (msg.get("body") or "")[:160] + ("…" if len(msg.get("body") or "") > 160 else "")
        for job in state["jobs"].values():
            job.pop("messages", None)
        for appt in state["appointments"].values():
            appt.pop("messages", None)
        for req in state["approval_requests"].values():
            req.pop("message", None)

    active_hold = next((h for h in reversed(state["holds"]) if h["active"]), None)
    overdue = []
    if active_hold and parse_datetime(active_hold["follow_up_at"]) <= now:
        overdue.append(f"Hold {active_hold['id']} follow-up was due {active_hold['follow_up_at']}")
    for req in state["approval_requests"].values():
        if req["status"] == "pending" and parse_datetime(req["response_due_by"]) <= now:
            overdue.append(f"Approval {req['id']} response was due {req['response_due_by']}")
    for appt in state["appointments"].values():
        if appt["status"] == "booked" and parse_datetime(appt["start"]) + timedelta(days=1) <= now:
            overdue.append(f"Appointment {appt['id']} ({appt['start']}) passed with no recorded result")

    pending = {
        "approval_requests": [r["id"] for r in state["approval_requests"].values() if r["status"] == "pending"],
        "open_items": [i["id"] for i in state["open_items"].values() if i["status"] == "open"],
        "open_escalations": [e["id"] for e in state["escalations"].values() if e["status"] == "open"],
        "active_jobs": [j["id"] for j in state["jobs"].values() if j["status"] in ("assigned", "scheduled", "quoted", "invoiced")],
    }
    blocked = any(e["blocks_automation"] for e in state["escalations"].values() if e["status"] == "open")
    return {
        "case_id": params.case_id,
        "property": context.get("property"),
        "now": iso(now),
        "visible_events": context.get("visible_event_range"),
        "status": "closed" if state["closed"] else ("awaiting_human" if blocked else ("on_hold" if active_hold else "active")),
        "active_hold": active_hold,
        "pending": pending,
        "overdue": overdue,
        "counts": {"messages_sent": len(state["messages"]), "calls": len(state["calls"]),
                   "failed_tool_calls": len(state["failed_calls"])},
        **state,
    }


TOOL = Tool(
    name="get_case_state",
    description="""
Return the current working state of a case as built from every action taken so far: status
(active / on_hold / awaiting_human / closed), active hold, pending approvals, open items and
escalations, jobs, appointments, quotes and invoices, landlord decisions, messages sent,
overdue follow-ups, and failed tool calls. Call it before deciding, and before closing.
""",
    input_model=GetCaseStateInput,
    handler=_handle,
    side_effect=False,
)
