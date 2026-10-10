"""track_open_item - keep side issues and unanswered questions from getting lost.

Real cases drift: a tenant mentions a fence, a landlord asks about a dog flap after closure.
Each such thread is opened here and must be resolved (or handed over) before close_case.
"""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import Field, model_validator

from tools._common import SideEffectInput, Tool, ToolFailure, build_state, case_now, iso, new_id, resolve_event

Owner = Literal["agency", "landlord", "tenant", "contractor", "block_management", "human_review"]


class TrackOpenItemInput(SideEffectInput):
    action: Literal["open", "resolve"]
    item_id: Optional[str] = Field(None, pattern=r"^ITEM-\d{3,}$", description="Required to resolve.")
    description: Optional[str] = Field(None, min_length=5, max_length=1000, description="Required to open.")
    raised_in_event: Optional[str] = None
    owner: Optional[Owner] = None
    resolution: Optional[str] = Field(None, min_length=5, max_length=1000, description="Required to resolve.")

    @model_validator(mode="after")
    def _fields(self) -> "TrackOpenItemInput":
        if self.action == "open" and not (self.description and self.owner):
            raise ValueError("opening an item needs description and owner")
        if self.action == "resolve" and not (self.item_id and self.resolution):
            raise ValueError("resolving an item needs item_id and resolution")
        return self


def _handle(params: TrackOpenItemInput) -> tuple[dict, list[str]]:
    now = iso(case_now(params.case_id))
    state = build_state(params.case_id)
    if params.action == "open":
        event = resolve_event(params.case_id, params.raised_in_event)["id"] if params.raised_in_event else None
        duplicates = [i["id"] for i in state["open_items"].values()
                      if i["status"] == "open" and i["description"].lower() == params.description.lower()]
        warnings = [f"Same item already open: {duplicates}"] if duplicates else []
        return {"id": new_id(params.case_id, "ITEM"), "action": "open", "status": "open",
                "description": params.description, "owner": params.owner, "raised_in_event": event,
                "opened_at": now}, warnings

    item = state["open_items"].get(params.item_id)
    if not item:
        raise ToolFailure("unknown_item", f"No open item {params.item_id}.",
                          details={"open_items": [i for i in state["open_items"] if state["open_items"][i]["status"] == "open"]})
    if item["status"] == "resolved":
        raise ToolFailure("already_resolved", f"{params.item_id} is already resolved.")
    return {"id": params.item_id, "action": "resolve", "status": "resolved",
            "description": item["description"], "resolution": params.resolution, "resolved_at": now}, []


TOOL = Tool(
    name="track_open_item",
    description="""
Open or resolve a side issue or unanswered question so it isn't lost, e.g. a second repair the
tenant mentions, a landlord question that needs a reply, or a missing invoice. action='open'
needs description and owner; action='resolve' needs item_id and resolution. close_case
refuses while items are still open.
""",
    input_model=TrackOpenItemInput,
    handler=_handle,
    side_effect=True,
)
