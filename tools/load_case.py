"""load_case - parse a case into structured events and register it for the other tools.

Accepts the practice-case layout (``<case>/index.md``, ``history.md``, ``attachments/``),
a single markdown/text/JSON file, or raw text (e.g. a freshly transcribed tenant call).

By default it hides everything that would leak the ending (Overview, Outcome, Status,
Completed/Updated dates) and can cut the history at an event or a time, so the agent
sees exactly what was known at a decision point.
"""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from pydantic import Field, model_validator

from tools._common import (
    CASE_ID_PATTERN,
    PROJECT_ROOT,
    Tool,
    ToolFailure,
    ToolInput,
    case_dir,
    find_addresses,
    iso,
    normalise_address,
    parse_datetime,
    run_dir,
    save_context,
    wall_now,
)

AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".ogg", ".oga", ".flac", ".webm", ".mp4", ".aac", ".opus"}
LEAKY_DETAIL_KEYS = {"status", "updated", "completed"}
LEAKY_SECTIONS = {"overview", "outcome", "summary", "resolution", "result"}

EVENT_HEADER = re.compile(
    r"^##\s+(?P<ts>\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}(?::\d{2})?)\s*(?:UTC)?\s*[—\-–]+\s*event\s+(?P<n>\d+)\s*$",
    re.M | re.I,
)
FIELD_LINE = re.compile(r"^-\s+\*\*(?P<key>[^*:]+):\*\*\s*(?P<value>.*)$", re.M)
LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
MISSING_TRANSCRIPT = re.compile(
    r"(?:text|transcription|transcript)[^\n.]{0,40}(?:unavailable|absent|missing|not present|not available)"
    r"|\[no text",
    re.I,
)


class LoadCaseInput(ToolInput):
    case_path: Optional[str] = Field(
        None,
        description="Case folder (with index.md/history.md) or a single .md/.txt/.json file.",
    )
    raw_text: Optional[str] = Field(
        None,
        max_length=200_000,
        description="Use instead of case_path for a brand-new report, e.g. a call transcript.",
    )
    property_address: Optional[str] = Field(
        None, description="Property address, if known and not in the case files."
    )
    case_id: Optional[str] = Field(
        None,
        pattern=CASE_ID_PATTERN,
        description="Identifier to use. Defaults to '<track>-<number>' from the folder name.",
    )
    cutoff_event: Optional[int] = Field(
        None, ge=0, description="Only show events up to and including this event number."
    )
    cutoff_time: Optional[str] = Field(
        None, description="Only show events at or before this ISO timestamp (UTC if no zone)."
    )
    include_outcome: bool = Field(
        False,
        description="Show Overview/Outcome/Status sections. Keep false when deciding what to do.",
    )
    max_event_chars: int = Field(8000, ge=200, le=100_000)
    reset: bool = Field(
        False, description="Clear this case's previous ledger (start a fresh run of the case)."
    )

    @model_validator(mode="after")
    def _one_source(self) -> "LoadCaseInput":
        if bool(self.case_path) == bool(self.raw_text):
            raise ValueError("provide exactly one of case_path or raw_text")
        if self.raw_text and not self.case_id:
            raise ValueError("case_id is required when using raw_text")
        return self


# --------------------------------------------------------------------------- parsing


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def _derive_case_id(path: Path) -> str:
    base = path if path.is_dir() else path.parent
    number = base.name if path.is_dir() else path.stem
    track = base.parent.name if path.is_dir() else base.name
    candidate = f"{_slug(track)}-{_slug(number)}" if track else _slug(number)
    candidate = candidate[:64].strip("-.") or "case"
    if not re.fullmatch(CASE_ID_PATTERN, candidate):
        candidate = "case-" + re.sub(r"[^A-Za-z0-9]", "", candidate)[:50]
    return candidate


def _parse_sections(markdown: str) -> tuple[str, dict[str, str]]:
    title_match = re.search(r"^#\s+(.+)$", markdown, re.M)
    title = title_match.group(1).strip() if title_match else ""
    sections: dict[str, str] = {}
    parts = re.split(r"^##\s+(.+)$", markdown, flags=re.M)
    for i in range(1, len(parts) - 1, 2):
        sections[parts[i].strip().lower()] = parts[i + 1].strip()
    return title, sections


def _parse_events(markdown: str, max_chars: int, source: str) -> list[dict]:
    headers = list(EVENT_HEADER.finditer(markdown))
    events = []
    for idx, header in enumerate(headers):
        end = headers[idx + 1].start() if idx + 1 < len(headers) else len(markdown)
        block = markdown[header.end():end]
        block = re.sub(r'<a id="event-\d+"></a>\s*$', "", block.strip()).strip()
        fields = {m.group("key").strip().lower(): m.group("value").strip() for m in FIELD_LINE.finditer(block)}
        body = FIELD_LINE.sub("", block).strip()
        body = re.sub(r"\n{3,}", "\n\n", body)
        events.append(_make_event(
            number=int(header.group("n")),
            timestamp=header.group("ts"),
            channel=fields.get("channel", "Unknown"),
            sender=fields.get("from", "Unknown"),
            recipient=fields.get("to", "Not specified"),
            body=body,
            max_chars=max_chars,
            source=source,
        ))
    return events


def _make_event(*, number: int, timestamp: str | None, channel: str, sender: str, recipient: str,
                body: str, max_chars: int, source: str) -> dict:
    ts_iso = None
    if timestamp:
        try:
            ts_iso = iso(parse_datetime(timestamp))
        except ToolFailure:
            ts_iso = None
    attachments = [
        {"label": label, "path": target}
        for label, target in LINK.findall(body)
        if not target.startswith("#") and not target.startswith("http")
    ]
    truncated = len(body) > max_chars
    return {
        "id": f"event-{number:03d}",
        "n": number,
        "timestamp": ts_iso,
        "channel": channel or "Unknown",
        "from": sender or "Unknown",
        "to": recipient or "Not specified",
        "body": body[:max_chars] + ("\n…[truncated]" if truncated else ""),
        "attachments": attachments,
        "truncated": truncated,
        "source": source,
    }


def _events_from_json(data: Any, max_chars: int, source: str) -> tuple[dict, list[dict]]:
    meta = data if isinstance(data, dict) else {}
    raw_events = meta.get("events") or meta.get("history") or (data if isinstance(data, list) else [])
    events = []
    for i, item in enumerate(raw_events, start=1):
        if not isinstance(item, dict):
            item = {"body": str(item)}
        events.append(_make_event(
            number=int(item.get("n") or item.get("number") or i),
            timestamp=item.get("timestamp") or item.get("time") or item.get("date"),
            channel=str(item.get("channel") or item.get("type") or "Unknown"),
            sender=str(item.get("from") or item.get("sender") or "Unknown"),
            recipient=str(item.get("to") or item.get("recipient") or "Not specified"),
            body=str(item.get("body") or item.get("text") or item.get("content") or item.get("message") or ""),
            max_chars=max_chars,
            source=source,
        ))
    return meta, events


def _document_event(text: str, max_chars: int, source: str) -> dict:
    return _make_event(number=1, timestamp=None, channel="Document", sender="Unknown",
                       recipient="Not specified", body=text.strip(), max_chars=max_chars, source=source)


# --------------------------------------------------------------------------- handler


def _handle(params: LoadCaseInput) -> tuple[dict, list[str]]:
    warnings: list[str] = []
    title = ""
    details: dict[str, str] = {}
    sections: dict[str, str] = {}
    events: list[dict] = []
    files: list[Path] = []
    case_root: Path | None = None

    if params.raw_text:
        case_id = params.case_id
        events = [_document_event(params.raw_text, params.max_event_chars, "raw_text")]
        events[0]["channel"] = "Report"
    else:
        path = Path(params.case_path).expanduser()
        if not path.is_absolute():
            path = (PROJECT_ROOT / path) if not path.exists() else path.resolve()
        if not path.exists():
            raise ToolFailure("not_found", f"Case path does not exist: {params.case_path}")
        path = path.resolve()
        case_id = params.case_id or _derive_case_id(path)
        case_root = path if path.is_dir() else path.parent

        if path.is_dir():
            index = path / "index.md"
            history = path / "history.md"
            if index.exists():
                title, sections = _parse_sections(index.read_text(encoding="utf-8", errors="replace"))
            if history.exists():
                events = _parse_events(history.read_text(encoding="utf-8", errors="replace"),
                                       params.max_event_chars, "history.md")
            if not index.exists() and not history.exists():
                docs = sorted(p for p in path.iterdir() if p.suffix.lower() in {".md", ".txt", ".json"})
                if not docs:
                    raise ToolFailure("unrecognised_case", f"No index.md, history.md or documents in {path}")
                warnings.append("Non-standard case folder: documents loaded as individual events.")
                for i, doc in enumerate(docs, start=1):
                    ev = _document_event(doc.read_text(encoding="utf-8", errors="replace"),
                                         params.max_event_chars, doc.name)
                    ev.update(id=f"event-{i:03d}", n=i)
                    events.append(ev)
            files = [p for p in path.rglob("*") if p.is_file() and p.name not in {"index.md", "history.md"}]
        else:
            text = path.read_text(encoding="utf-8", errors="replace")
            if path.suffix.lower() == ".json":
                try:
                    meta, events = _events_from_json(json.loads(text), params.max_event_chars, path.name)
                except json.JSONDecodeError as exc:
                    raise ToolFailure("invalid_json", f"Could not parse {path.name}: {exc}") from exc
                title = str(meta.get("title", ""))
                details = {str(k).lower(): str(v) for k, v in (meta.get("details") or {}).items()}
            else:
                title, sections = _parse_sections(text)
                events = _parse_events(text, params.max_event_chars, path.name)
                if not events:
                    warnings.append("No structured events found; the whole file is loaded as one event.")
                    events = [_document_event(text, params.max_event_chars, path.name)]

    if "case details" in sections:
        for line in sections["case details"].splitlines():
            m = re.match(r"-\s+\*\*([^*:]+):\*\*\s*(.*)", line.strip())
            if m:
                details[m.group(1).strip().lower()] = m.group(2).strip()

    # ---- ordering & cutoff
    total_events = len(events)
    referenced_all = {att["path"] for e in events for att in e["attachments"]}
    order_issues = [
        f"{b['id']} ({b['timestamp']}) is earlier than {a['id']} ({a['timestamp']})"
        for a, b in zip(events, events[1:])
        if a["timestamp"] and b["timestamp"] and b["timestamp"] < a["timestamp"]
    ]
    cutoff_dt: datetime | None = parse_datetime(params.cutoff_time) if params.cutoff_time else None
    if params.cutoff_event is not None:
        events = [e for e in events if e["n"] <= params.cutoff_event]
    if cutoff_dt is not None:
        events = [e for e in events if not e["timestamp"] or parse_datetime(e["timestamp"]) <= cutoff_dt]
    cut = len(events) < total_events

    # ---- outcome hiding
    hidden: list[str] = []
    if not params.include_outcome:
        for key in list(sections):
            if key in LEAKY_SECTIONS:
                hidden.append(key)
                sections.pop(key)
        for key in list(details):
            if key in LEAKY_DETAIL_KEYS:
                hidden.append(f"details.{key}")
                details.pop(key)

    property_address = params.property_address or details.get("property")
    if not property_address:
        counts: dict[str, int] = {}
        for e in events:
            for a in find_addresses(e["body"]):
                counts[a] = counts.get(a, 0) + 1
        if counts:
            property_address = max(counts, key=counts.get)
            warnings.append(f"Property address inferred from message text: {property_address}")
        else:
            warnings.append("Property address unknown; address checks on outbound messages are disabled.")

    initial_request = sections.get("initial request")
    if not initial_request and events:
        first = events[0]["body"]
        initial_request = re.sub(r"^Request description:\s*", "", first) if first else None

    # ---- attachments & audio
    # Files referenced only by events after the cut-off did not exist yet at this point.
    referenced_visible = {att["path"] for e in events for att in e["attachments"]}
    hidden_files = sorted(referenced_all - referenced_visible)
    attachment_list = []
    for f in sorted(files):
        if case_root and f.relative_to(case_root).as_posix() in hidden_files:
            continue
        rel = f.relative_to(case_root).as_posix()
        attachment_list.append({
            "path": rel,
            "type": "audio" if f.suffix.lower() in AUDIO_EXTENSIONS else f.suffix.lower().lstrip(".") or "file",
            "bytes": f.stat().st_size,
        })
    linked_missing = []
    if case_root:
        for e in events:
            for att in e["attachments"]:
                if not (case_root / att["path"]).exists():
                    linked_missing.append({"event": e["id"], "path": att["path"]})

    # ---- data quality flags (so the agent treats noisy facts with care)
    prop_norm = normalise_address(property_address) if property_address else None
    foreign = []
    for e in events:
        others = [a for a in find_addresses(e["body"]) if prop_norm and normalise_address(a) != prop_norm]
        if others:
            foreign.append({"event": e["id"], "addresses": others})
    data_quality = {
        "unavailable_attachment_refs": [
            e["id"] for e in events if re.search(r"attachment[^\n]{0,80}unavailable|unavailable[^\n]{0,40}attachment", e["body"], re.I)
        ],
        "missing_transcripts": [e["id"] for e in events if MISSING_TRANSCRIPT.search(e["body"])],
        "extraction_failures": [
            e["id"] for e in events if re.search(r"expected data could not be extracted", e["body"], re.I)
        ],
        "other_property_addresses_mentioned": foreign,
        "out_of_order_timestamps": order_issues,
        "linked_attachments_missing_on_disk": linked_missing,
        "truncated_events": [e["id"] for e in events if e["truncated"]],
    }
    if foreign:
        warnings.append(
            f"{len(foreign)} event(s) mention a different property address; treat those details with caution."
        )

    # ---- simulated "now"
    stamps = [e["timestamp"] for e in events if e["timestamp"]]
    if cutoff_dt is not None:
        now = iso(cutoff_dt)
    elif stamps:
        now = max(stamps)
    elif details.get("created"):
        now = iso(parse_datetime(details["created"]))
    else:
        now = wall_now()

    # ---- register the case
    folder = case_dir(case_id)
    if params.reset:
        for name in ("ledger.jsonl",):
            (folder / name).unlink(missing_ok=True)
    context = {
        "case_id": case_id,
        "title": title,
        "property": property_address,
        "case_root": str(case_root) if case_root else None,
        "now": now,
        "loaded_at": wall_now(),
        "cutoff": {"event": params.cutoff_event, "time": params.cutoff_time},
        "visible_event_range": f"{events[0]['id']}..{events[-1]['id']}" if events else None,
        "events_index": {
            e["id"]: {
                "timestamp": e["timestamp"],
                "channel": e["channel"],
                "from": e["from"],
                "to": e["to"],
                "excerpt": e["body"][:240],
            }
            for e in events
        },
        "attachments": attachment_list,
        "hidden_files": hidden_files,
        "run_dir": str(run_dir()),
    }
    save_context(case_id, context)
    (folder / "events.json").write_text(json.dumps(events, indent=2, ensure_ascii=False), encoding="utf-8")

    data = {
        "case_id": case_id,
        "title": title,
        "details": details,
        "property": property_address,
        "initial_request": initial_request,
        "other_sections": {k: v for k, v in sections.items() if k not in {"case details", "initial request", "history", "attachments"}},
        "now": now,
        "events": events,
        "event_count": {"visible": len(events), "total_in_source": total_events, "history_cut": cut},
        "attachments": attachment_list,
        "audio_files": [a["path"] for a in attachment_list if a["type"] == "audio"],
        "hidden_sections": hidden,
        "data_quality": data_quality,
    }
    if data["audio_files"]:
        warnings.append("Audio files present: use transcribe_audio on them before deciding.")
    return data, warnings


TOOL = Tool(
    name="load_case",
    description="""
Load a case and register it so the other tools can act on it. Call this first.
Returns the case details, the initial request, every visible event (id, timestamp, channel,
from, to, body, linked attachments), the attachment list, any audio files, and data-quality
flags: unavailable attachments, missing transcripts, mentions of other property addresses,
out-of-order timestamps. Outcome/overview/status sections are hidden by default so the
decision is made only on what was known. Use cutoff_event or cutoff_time to stop the history
at a decision point. The simulated 'now' for all later tools becomes the last visible event time.
""",
    input_model=LoadCaseInput,
    handler=_handle,
    side_effect=False,
)
