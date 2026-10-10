"""Tool registry. One tool per module; each module exposes ``TOOL``.

Usage::

    from tools import TOOLS, call_tool, tool_specs
    result = call_tool("load_case", {"case_path": "Property Management/001"})
    specs = tool_specs()  # pass to the Anthropic Messages API as `tools=`
"""

from __future__ import annotations

from importlib import import_module

from tools._common import Tool, _envelope

TOOL_MODULES = [
    # perception
    "load_case",
    "read_attachment",
    "transcribe_audio",
    "safety_screen",
    "get_case_state",
    # communication
    "send_email",
    "send_sms",
    "place_call",
    # workflow & money
    "request_landlord_approval",
    "record_landlord_decision",
    "assign_contractor",
    "schedule_appointment",
    "record_financial",
    "set_hold",
    # record keeping & control
    "add_note",
    "track_open_item",
    "escalate_to_human",
    "close_case",
]

TOOLS: dict[str, Tool] = {}
for _module in TOOL_MODULES:
    _tool = import_module(f"tools.{_module}").TOOL
    assert _tool.name == _module, f"tools/{_module}.py defines tool {_tool.name!r}"
    TOOLS[_tool.name] = _tool


# Built but not offered to the agent yet: voice work is deferred until the core agent is final.
DEFERRED_TOOLS = {"transcribe_audio"}
ACTIVE_TOOLS = [n for n in TOOL_MODULES if n not in DEFERRED_TOOLS]


def tool_specs(names: list[str] | None = None) -> list[dict]:
    """Anthropic-format tool definitions for the given tools (default: active tools only)."""
    return [TOOLS[n].spec() for n in (names or ACTIVE_TOOLS)]


def call_tool(name: str, args: dict | None = None) -> dict:
    """Dispatch a tool call by name. Never raises: unknown tools return an error envelope."""
    tool = TOOLS.get(name)
    if tool is None:
        return _envelope(name, False, error={
            "code": "unknown_tool", "message": f"No tool named {name!r}.", "retryable": False,
            "details": {"available": TOOL_MODULES},
        })
    return tool(args or {})


__all__ = ["TOOLS", "TOOL_MODULES", "ACTIVE_TOOLS", "DEFERRED_TOOLS", "tool_specs", "call_tool"]
