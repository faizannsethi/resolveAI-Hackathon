"""Shared plumbing for every tool.

Each tool module defines a pydantic input model and a handler, then wraps them in
``Tool``. The wrapper gives every tool the same behaviour:

* input validation with field-level error messages the agent can act on;
* a uniform result envelope: ``{"ok", "tool", "data", "warnings", "error"}``;
* an append-only per-case ledger of every call (successful or not), which is the
  audit trail used for ANSWER.md / REASONING.md;
* idempotency for side-effecting tools, so an agent retry never double-sends;
* optional failure injection so the agent's recovery paths can be exercised.

State lives on disk under ``$AGENT_RUN_DIR/<case_id>/`` (default ``runs/default``):

* ``context.json`` - written by ``load_case``: property, event index, simulated "now";
* ``ledger.jsonl`` - one JSON object per tool call;
* ``artifacts/``   - generated files (e.g. synthesised call audio).
"""

from __future__ import annotations

import hashlib
import json
import os
import random
import re
import traceback
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable, Literal, Optional

from dateutil import parser as date_parser
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CASE_ID_PATTERN = r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$"

RecipientRole = Literal[
    "tenant", "landlord", "contractor", "agency_internal", "block_management", "other"
]


# --------------------------------------------------------------------------- results


class ToolFailure(Exception):
    """Raised inside a handler to return a structured, expected failure."""

    def __init__(
        self,
        code: str,
        message: str,
        *,
        retryable: bool = False,
        details: Any = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.retryable = retryable
        self.details = details


def _envelope(tool: str, ok: bool, data: Any = None, warnings: list[str] | None = None,
              error: dict | None = None) -> dict:
    return {
        "ok": ok,
        "tool": tool,
        "data": data,
        "warnings": warnings or [],
        "error": error,
    }


# --------------------------------------------------------------------------- base input


class ToolInput(BaseModel):
    """Base for all tool inputs: unknown fields are rejected, strings are stripped."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class CaseScopedInput(ToolInput):
    case_id: str = Field(
        ...,
        pattern=CASE_ID_PATTERN,
        description="Case identifier returned by load_case (e.g. 'property-management-001').",
    )


class SideEffectInput(CaseScopedInput):
    idempotency_key: Optional[str] = Field(
        None,
        max_length=128,
        description=(
            "Optional. Repeating a call with the same key returns the original result instead "
            "of acting twice. If omitted, identical arguments are treated as a duplicate."
        ),
    )


class Recipient(ToolInput):
    role: RecipientRole
    name: Optional[str] = Field(None, max_length=120)
    email: Optional[str] = Field(None, max_length=254)
    phone: Optional[str] = Field(None, max_length=32)

    @field_validator("email")
    @classmethod
    def _valid_email(cls, value: Optional[str]) -> Optional[str]:
        if value and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value):
            raise ValueError("not a valid email address")
        return value

    @field_validator("phone")
    @classmethod
    def _valid_phone(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        if not re.fullmatch(r"\+?[\d\s()\-]{7,24}", value):
            raise ValueError("not a valid phone number")
        if len(re.sub(r"\D", "", value)) < 7:
            raise ValueError("phone number has too few digits")
        return value


# --------------------------------------------------------------------------- run storage


def run_dir() -> Path:
    return Path(os.environ.get("AGENT_RUN_DIR", PROJECT_ROOT / "runs" / "default"))


def case_dir(case_id: str) -> Path:
    if not re.fullmatch(CASE_ID_PATTERN, case_id):
        raise ToolFailure("invalid_case_id", f"Invalid case_id {case_id!r}.")
    path = run_dir() / case_id
    path.mkdir(parents=True, exist_ok=True)
    return path


def artifacts_dir(case_id: str) -> Path:
    path = case_dir(case_id) / "artifacts"
    path.mkdir(parents=True, exist_ok=True)
    return path


def load_context(case_id: str, *, required: bool = True) -> dict | None:
    path = run_dir() / case_id / "context.json"
    if not path.exists():
        if required:
            raise ToolFailure(
                "case_not_loaded",
                f"Case {case_id!r} has not been loaded. Call load_case first.",
            )
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def save_context(case_id: str, context: dict) -> None:
    path = case_dir(case_id) / "context.json"
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(context, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(path)


def read_ledger(case_id: str) -> list[dict]:
    path = run_dir() / case_id / "ledger.jsonl"
    if not path.exists():
        return []
    entries = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            entries.append(json.loads(line))
    return entries


def _append_ledger(case_id: str, entry: dict) -> dict:
    path = case_dir(case_id) / "ledger.jsonl"
    entry = {"seq": len(read_ledger(case_id)) + 1, **entry}
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False, default=str) + "\n")
    return entry


def successful_records(case_id: str, tool: str | None = None) -> list[dict]:
    """Ledger entries for successful, non-duplicate calls (optionally one tool only)."""
    return [
        e
        for e in read_ledger(case_id)
        if e.get("ok") and not e.get("duplicate") and (tool is None or e["tool"] == tool)
    ]


def new_id(case_id: str, prefix: str) -> str:
    """Sequential, human-readable ids such as ``MSG-003`` (unique within a case).

    Scans every id already issued in successful ledger entries, including ids nested
    inside a result (e.g. the messages a contractor assignment sends).
    """
    pattern = re.compile(r'"' + re.escape(prefix) + r'-(\d+)"')
    highest = 0
    for entry in read_ledger(case_id):
        if entry.get("ok") and not entry.get("duplicate"):
            for match in pattern.finditer(json.dumps(entry.get("data"))):
                highest = max(highest, int(match.group(1)))
    return f"{prefix}-{highest + 1:03d}"


class IdAllocator:
    """Issues several ids within one tool call without collisions."""

    def __init__(self, case_id: str) -> None:
        self.case_id = case_id
        self._issued: dict[str, int] = {}

    def next(self, prefix: str) -> str:
        if prefix not in self._issued:
            self._issued[prefix] = int(new_id(self.case_id, prefix).split("-")[-1])
        else:
            self._issued[prefix] += 1
        return f"{prefix}-{self._issued[prefix]:03d}"


# --------------------------------------------------------------------------- time


def parse_datetime(value: str) -> datetime:
    """Parse an ISO-ish timestamp; naive values are treated as UTC."""
    try:
        parsed = date_parser.parse(value)
    except (ValueError, OverflowError) as exc:
        raise ToolFailure("invalid_datetime", f"Could not parse datetime {value!r}.") from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def case_now(case_id: str | None = None) -> datetime:
    """The clock tools act on.

    Priority: ``AGENT_NOW`` env var, then the case's simulated "now" (the time of the
    last visible event, set by load_case), then wall-clock UTC.
    """
    if os.environ.get("AGENT_NOW"):
        return parse_datetime(os.environ["AGENT_NOW"])
    if case_id:
        context = load_context(case_id, required=False)
        if context and context.get("now"):
            return parse_datetime(context["now"])
    return datetime.now(timezone.utc)


def wall_now() -> str:
    return iso(datetime.now(timezone.utc))


# --------------------------------------------------------------------------- events & addresses


def normalise_event_ref(ref: str | int) -> str:
    """Accept 12, '12', '012', 'event-12', 'event-012' -> 'event-012'."""
    match = re.fullmatch(r"(?:event[-_ ]?)?0*(\d{1,5})", str(ref).strip(), flags=re.I)
    if not match:
        raise ToolFailure("invalid_event_ref", f"Not a valid event reference: {ref!r}.")
    return f"event-{int(match.group(1)):03d}"


def resolve_event(case_id: str, ref: str | int) -> dict:
    """Return the indexed event (id, timestamp, channel, from, to, excerpt) or fail."""
    event_id = normalise_event_ref(ref)
    context = load_context(case_id)
    event = context.get("events_index", {}).get(event_id)
    if not event:
        visible = context.get("visible_event_range") or "none"
        raise ToolFailure(
            "unknown_event",
            f"{event_id} is not a visible event in case {case_id} (visible: {visible}).",
        )
    return {"id": event_id, **event}


UK_POSTCODE = r"[A-Z]{1,2}\d[A-Z\d]?\s?\d[A-Z]{2}"
ADDRESS_PATTERN = re.compile(
    r"(?:Flat\s+\d+[A-Za-z]?,\s*)?\d+[A-Za-z]?\s+[A-Z][A-Za-z']+(?:\s+[A-Z][A-Za-z']+)*,"
    r"\s*[A-Z][A-Za-z' ]+?,\s*" + UK_POSTCODE
)


def normalise_address(address: str) -> str:
    return re.sub(r"[\s,]+", " ", address).strip().lower()


def find_addresses(text: str) -> list[str]:
    seen: list[str] = []
    for match in ADDRESS_PATTERN.finditer(text or ""):
        value = match.group(0).strip()
        if value not in seen:
            seen.append(value)
    return seen


PLACEHOLDER_PATTERN = re.compile(
    r"\[(?:insert|name|tenant|landlord|contractor|date|time|address|tbc|todo|xx+)[^\]]*\]"
    r"|\{\{?\s*[A-Za-z_][\w.]*\s*\}?\}"
    r"|<\s*(?:INSERT|NAME|DATE|ADDRESS|TBC)[^>]*>"
    r"|\bTODO\b|\bTBC\b|lorem ipsum",
    flags=re.I,
)


def check_outbound_text(case_id: str, text: str, *, allow_other_addresses: bool = False) -> list[str]:
    """Validate text that will be sent to a real person.

    Raises on unfilled template placeholders and on property addresses that are not the
    case property (a recurring error in the source data). Returns soft warnings.
    """
    placeholders = sorted({m.group(0) for m in PLACEHOLDER_PATTERN.finditer(text)})
    if placeholders:
        raise ToolFailure(
            "unfilled_placeholder",
            "Message contains unfilled template placeholders; replace them before sending.",
            details={"placeholders": placeholders},
        )
    warnings: list[str] = []
    context = load_context(case_id)
    prop = context.get("property")
    if prop:
        foreign = [a for a in find_addresses(text) if normalise_address(a) != normalise_address(prop)]
        if foreign and not allow_other_addresses:
            raise ToolFailure(
                "address_mismatch",
                "Message mentions a property address that is not this case's property. "
                "Correct it, or set allow_other_addresses=true if intentional.",
                details={"case_property": prop, "other_addresses": foreign},
            )
        if foreign:
            warnings.append(f"Message intentionally references other address(es): {foreign}")
    return warnings


# --------------------------------------------------------------------------- failure injection

_FAILURE_PLAN: dict[str, int] = {}
_RNG = random.Random(int(os.environ.get("TOOL_FAILURE_SEED", "7")))


def inject_failures(tool_name: str, count: int = 1) -> None:
    """Make the next ``count`` calls to ``tool_name`` fail transiently (tests / demos)."""
    _FAILURE_PLAN[tool_name] = _FAILURE_PLAN.get(tool_name, 0) + count


def clear_injected_failures() -> None:
    _FAILURE_PLAN.clear()


def _should_inject_failure(tool_name: str) -> bool:
    if _FAILURE_PLAN.get(tool_name, 0) > 0:
        _FAILURE_PLAN[tool_name] -= 1
        return True
    rate = float(os.environ.get("TOOL_FAILURE_RATE", "0") or 0)
    only = {t.strip() for t in os.environ.get("TOOL_FAILURE_ONLY", "").split(",") if t.strip()}
    if rate > 0 and (not only or tool_name in only):
        return _RNG.random() < rate
    return False


# --------------------------------------------------------------------------- schema helpers


def _inline_refs(schema: dict) -> dict:
    """Inline ``$defs`` references and drop noise so the schema is plain JSON Schema."""
    defs = schema.pop("$defs", {})

    def walk(node: Any) -> Any:
        if isinstance(node, dict):
            if "$ref" in node:
                target = defs[node["$ref"].split("/")[-1]]
                merged = {**walk(dict(target)), **{k: v for k, v in node.items() if k != "$ref"}}
                return walk(merged)
            return {k: walk(v) for k, v in node.items() if k != "title"}
        if isinstance(node, list):
            return [walk(v) for v in node]
        return node

    return walk(schema)


def _format_validation_error(exc: ValidationError) -> list[dict]:
    problems = []
    for err in exc.errors():
        problems.append(
            {
                "field": ".".join(str(p) for p in err.get("loc", ())) or "(root)",
                "problem": err.get("msg"),
                "got": err.get("input") if not isinstance(err.get("input"), dict) else "(object)",
            }
        )
    return problems


# --------------------------------------------------------------------------- tool wrapper


class Tool:
    """A callable tool with schema, validation, ledgering, idempotency and failure injection."""

    def __init__(
        self,
        *,
        name: str,
        description: str,
        input_model: type[ToolInput],
        handler: Callable[[Any], tuple[Any, list[str]] | Any],
        side_effect: bool,
        injectable: bool | None = None,
    ) -> None:
        self.name = name
        self.description = description.strip()
        self.input_model = input_model
        self.handler = handler
        self.side_effect = side_effect
        self.injectable = side_effect if injectable is None else injectable

    # Anthropic Messages API tool definition
    def spec(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": _inline_refs(self.input_model.model_json_schema()),
        }

    def __call__(self, args: dict | None = None, **kwargs: Any) -> dict:
        payload = {**(args or {}), **kwargs}
        try:
            params = self.input_model.model_validate(payload)
        except ValidationError as exc:
            return _envelope(
                self.name,
                False,
                error={
                    "code": "invalid_input",
                    "message": "Input failed validation; fix the listed fields and retry.",
                    "retryable": True,
                    "details": _format_validation_error(exc),
                },
            )

        case_id = getattr(params, "case_id", None)
        clean_args = params.model_dump(mode="json", exclude_none=True)

        # Idempotency: identical (or same-keyed) successful side-effect calls are not repeated.
        fingerprint = None
        if self.side_effect and case_id:
            key = clean_args.get("idempotency_key") or json.dumps(
                {k: v for k, v in clean_args.items() if k != "idempotency_key"}, sort_keys=True
            )
            fingerprint = hashlib.sha256(f"{self.name}|{key}".encode()).hexdigest()[:16]
            for entry in reversed(read_ledger(case_id)):
                if entry.get("fingerprint") == fingerprint and entry.get("ok"):
                    result = _envelope(
                        self.name,
                        True,
                        entry.get("data"),
                        ["Duplicate call: returning the original result; no action repeated."],
                    )
                    result["duplicate"] = True
                    self._record(case_id, clean_args, result, fingerprint, duplicate=True)
                    return result

        if self.injectable and _should_inject_failure(self.name):
            result = _envelope(
                self.name,
                False,
                error={
                    "code": "transient_unavailable",
                    "message": f"{self.name} backend temporarily unavailable (injected failure). Retry.",
                    "retryable": True,
                    "details": None,
                },
            )
            if case_id:
                self._record(case_id, clean_args, result, fingerprint)
            return result

        try:
            outcome = self.handler(params)
            data, warnings = outcome if isinstance(outcome, tuple) else (outcome, [])
            result = _envelope(self.name, True, data, warnings)
        except ToolFailure as exc:
            result = _envelope(
                self.name,
                False,
                error={
                    "code": exc.code,
                    "message": exc.message,
                    "retryable": exc.retryable,
                    "details": exc.details,
                },
            )
        except Exception as exc:  # noqa: BLE001 - tools must never crash the agent loop
            result = _envelope(
                self.name,
                False,
                error={
                    "code": "internal_error",
                    "message": f"{type(exc).__name__}: {exc}",
                    "retryable": False,
                    "details": traceback.format_exc(limit=3),
                },
            )

        if not case_id and result["ok"] and isinstance(result["data"], dict):
            case_id = result["data"].get("case_id")  # e.g. load_case derives its own id
        if case_id and (run_dir() / case_id).exists():
            self._record(case_id, clean_args, result, fingerprint)
        return result

    def _record(self, case_id: str, args: dict, result: dict, fingerprint: str | None,
                duplicate: bool = False) -> None:
        _append_ledger(
            case_id,
            {
                "tool": self.name,
                "ok": result["ok"],
                "duplicate": duplicate,
                "side_effect": self.side_effect,
                "sim_time": iso(case_now(case_id)),
                "wall_time": wall_now(),
                "args": args,
                "data": result["data"],
                "warnings": result["warnings"],
                "error": result["error"],
                "fingerprint": fingerprint,
            },
        )


def is_closed(case_id: str) -> bool:
    """True if close_case succeeded and the case was not reopened afterwards."""
    closed = False
    for entry in successful_records(case_id):
        if entry["tool"] == "close_case":
            closed = True
        elif entry["tool"] == "load_case":
            closed = False
    return closed


def resolve_case_file(case_id: str, raw: str) -> Path:
    """Resolve a path inside the case folder or the case's artifacts folder (no traversal)."""
    context = load_context(case_id)
    roots = [artifacts_dir(case_id).resolve()]
    if context.get("case_root"):
        roots.insert(0, Path(context["case_root"]).resolve())
    hidden = set(context.get("hidden_files", []))
    for root in roots:
        target = (root / raw).resolve()
        if (target == root or root in target.parents) and target.is_file() \
                and target.relative_to(root).as_posix() not in hidden:
            return target
    raise ToolFailure(
        "attachment_not_found",
        f"Cannot attach {raw!r}: not found in the case folder or generated artifacts.",
        details={"available": [a["path"] for a in context.get("attachments", [])]},
    )


def build_state(case_id: str) -> dict:
    """Replay the ledger into the current working state of a case."""
    state: dict[str, Any] = {
        "messages": [], "calls": [], "approval_requests": {}, "decisions": {}, "jobs": {},
        "appointments": {}, "financials": [], "holds": [], "notes": [], "open_items": {},
        "escalations": {}, "closed": None, "failed_calls": [],
    }
    for entry in read_ledger(case_id):
        tool, data = entry["tool"], entry.get("data") or {}
        if not entry.get("ok"):
            if entry.get("side_effect"):
                state["failed_calls"].append(
                    {"seq": entry["seq"], "tool": tool, "error": (entry.get("error") or {}).get("code")}
                )
            continue
        if entry.get("duplicate"):
            continue
        if tool == "load_case":
            state["closed"] = None  # reloading (e.g. new events after closure) reopens the case
        elif tool in ("send_email", "send_sms"):
            state["messages"].append(data)
        elif tool == "place_call":
            state["calls"].append(data)
        elif tool == "request_landlord_approval":
            state["approval_requests"][data["id"]] = data
            state["messages"].append(data["message"])
        elif tool == "record_landlord_decision":
            state["decisions"][data["id"]] = data
            if data.get("approval_request_id") in state["approval_requests"]:
                state["approval_requests"][data["approval_request_id"]]["status"] = "answered"
        elif tool == "assign_contractor":
            state["jobs"][data["id"]] = data
            if data.get("replaces_job_id") in state["jobs"]:
                state["jobs"][data["replaces_job_id"]]["status"] = "replaced"
            state["messages"].extend(data.get("messages", []))
        elif tool == "schedule_appointment":
            for appt in state["appointments"].values():
                if appt["job_id"] == data["job_id"] and appt["status"] == "booked":
                    appt["status"] = "superseded"
            state["appointments"][data["id"]] = data
            if data["job_id"] in state["jobs"] and state["jobs"][data["job_id"]]["status"] == "assigned":
                state["jobs"][data["job_id"]]["status"] = "scheduled"
            state["messages"].extend(data.get("messages", []))
        elif tool == "record_financial":
            state["financials"].append(data)
            job = state["jobs"].get(data.get("job_id") or "")
            if job and data["kind"] == "invoice":
                job["status"] = "invoiced"
            elif job and data["kind"] == "quote" and job["status"] in ("assigned", "scheduled"):
                job["status"] = "quoted"
        elif tool == "set_hold":
            for hold in state["holds"]:
                hold["active"] = False
            state["holds"].append({**data, "active": True})
        elif tool == "add_note":
            state["notes"].append(data)
        elif tool == "track_open_item":
            if data["action"] == "open":
                state["open_items"][data["id"]] = data
            elif data["id"] in state["open_items"]:
                state["open_items"][data["id"]].update(status="resolved", resolution=data.get("resolution"))
        elif tool == "escalate_to_human":
            state["escalations"][data["id"]] = data
        elif tool == "close_case":
            state["closed"] = data
            for hold in state["holds"]:
                hold["active"] = False
            for job in state["jobs"].values():
                if job["status"] not in ("replaced", "cancelled"):
                    job["status"] = "closed"
    return state


def hours_from_now(case_id: str, hours: float) -> str:
    return iso(case_now(case_id) + timedelta(hours=hours))
