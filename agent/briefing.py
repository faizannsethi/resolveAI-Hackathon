"""Deterministic first step: load the case, screen it, read supplied documents, build the briefing.

This runs in code, not by the model, so the safety screen and document reading can never be
skipped. Every call goes through the normal tools, so it appears in the case ledger.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from tools import call_tool

TEXT_DOC_TYPES = {".md", ".txt", ".eml", ".json", ".csv", ".html", ".htm", ".pdf", ".vtt", ".srt"}
AUDIO_TYPES = {".mp3", ".wav", ".m4a", ".ogg", ".oga", ".flac", ".webm", ".mp4", ".aac", ".opus"}
CASE_FILES = {"index.md", "history.md"}
IMAGE_TYPES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".heic", ".bmp"}
MAX_DOC_CHARS = 15_000          # a newly supplied document (email, transcript, report)
MAX_ATTACHMENT_CHARS = 8_000    # each case attachment
MAX_ATTACHMENTS_TOTAL = 40_000  # all case attachments together


class BriefingError(RuntimeError):
    pass


@dataclass
class Briefing:
    case_id: str
    text: str
    case: dict
    screen: dict
    supplied_documents: list[dict] = field(default_factory=list)
    attachments: list[dict] = field(default_factory=list)


def _fmt_event(e: dict) -> str:
    when = (e.get("timestamp") or "time unknown").replace("T", " ").replace(":00Z", " UTC").replace("Z", " UTC")
    to = f" → {e['to']}" if e.get("to") and e["to"] not in ("Not specified", "Unspecified") else ""
    head = f"[{e['id']}] {when} | {e['channel']} | {e['from']}{to}"
    return f"{head}\n{e['body'].strip() or '(no text)'}"


def _read_document(case_id: str, path: str, max_chars: int) -> dict:
    """Read one file through the normal tools (so it is ledgered). Never raises."""
    suffix = Path(path).suffix.lower()
    if suffix in AUDIO_TYPES:
        result = call_tool("transcribe_audio", {"case_id": case_id, "path": path})
        if result["ok"]:
            return {"path": path, "kind": "audio", "text": result["data"]["text"][:max_chars],
                    "note": f"audio transcribed by {result['data']['engine']}"}
        return {"path": path, "kind": "audio", "text": None,
                "note": f"audio could not be transcribed ({result['error']['code']}); its content is unknown"}
    if suffix in IMAGE_TYPES:
        return {"path": path, "kind": "image", "text": None,
                "note": "image: contents not visible to the agent; do not assume what it shows"}
    if suffix not in TEXT_DOC_TYPES:
        return {"path": path, "kind": "other", "text": None, "note": f"unsupported file type {suffix or '(none)'}"}
    result = call_tool("read_attachment", {"case_id": case_id, "path": path, "max_chars": max_chars})
    if not result["ok"]:
        return {"path": path, "kind": "unreadable", "text": None,
                "note": f"could not be read ({result['error']['code']}): treat its content as unknown"}
    data = result["data"]
    note = (f"truncated at {max_chars} of {data['chars']} characters; use read_attachment (pages) for the rest"
            if data.get("truncated") else None)
    return {"path": path, "kind": data["kind"], "text": data["text"], "note": note}


def _supplied_documents(case: dict, case_id: str) -> list[dict]:
    """Files placed directly in the case folder (beside index.md/history.md): new emails, transcripts, reports."""
    docs = []
    for att in case.get("attachments", []):
        path = att["path"]
        if "/" in path or Path(path).name in CASE_FILES or Path(path).name.startswith("."):
            continue
        if Path(path).suffix.lower() in TEXT_DOC_TYPES | AUDIO_TYPES:
            docs.append(_read_document(case_id, path, MAX_DOC_CHARS))
    return docs


def _case_attachments(case: dict, case_id: str) -> list[dict]:
    """Every attachment visible at the cut-off is read in code, so it can never be overlooked."""
    linked: dict[str, list[str]] = {}
    for e in case.get("events", []):
        for att in e.get("attachments", []):
            linked.setdefault(att["path"], []).append(e["id"])
    docs, budget = [], MAX_ATTACHMENTS_TOTAL
    for att in case.get("attachments", []):
        path = att["path"]
        if "/" not in path:
            continue  # supplied documents are handled separately
        cap = max(0, min(MAX_ATTACHMENT_CHARS, budget))
        if cap < 500:
            doc = {"path": path, "kind": att["type"], "text": None,
                   "note": "not included (briefing size limit reached); read it with read_attachment"}
        else:
            doc = _read_document(case_id, path, cap)
            budget -= len(doc["text"] or "")
        doc["linked_events"] = linked.get(path, [])
        docs.append(doc)
    return docs


def _format_screen(screen: dict) -> str:
    lines = [f"Overall level: {screen['level'].upper()} (target: {screen['recommended_response']})"]
    for category, info in screen["hazards"].items():
        sources = ", ".join(f"{ev['source']} \"{ev['phrase']}\" (from {ev.get('from') or 'text'})"
                            for ev in info["evidence"][:6])
        lines.append(f"- {category} [{info['level']}]: {sources}")
        if info.get("verify_by_asking"):
            lines.append(f"  verify by asking: {' | '.join(info['verify_by_asking'])}")
        lines.append(f"  immediate advice if live: {info['advice']}")
    if screen["escalation_flags"]:
        lines.append(f"Flags: {', '.join(screen['escalation_flags'])}")
    if screen["negated_matches"]:
        lines.append(f"Ignored negated phrases: {', '.join(m['phrase'] for m in screen['negated_matches'][:6])}")
    lines.append("Reminder: matches are deliberately broad. Check each source (intake question, staff note, "
                 "old/resolved event?) before acting on it.")
    return "\n".join(lines)


def _format_quality(dq: dict) -> str:
    labels = {
        "unavailable_attachment_refs": "events referring to attachments that are unavailable",
        "missing_transcripts": "events whose text/transcript is missing",
        "extraction_failures": "provider emails the system could not parse",
        "other_property_addresses_mentioned": "events mentioning a different property address",
        "out_of_order_timestamps": "timestamps out of order",
        "linked_attachments_missing_on_disk": "linked attachments missing from the folder",
        "truncated_events": "events truncated for length",
    }
    lines = []
    for key, label in labels.items():
        value = dq.get(key)
        if not value:
            continue
        if key == "other_property_addresses_mentioned":
            shown = "; ".join(f"{v['event']}: {', '.join(v['addresses'])}" for v in value[:8])
        elif key == "linked_attachments_missing_on_disk":
            shown = ", ".join(f"{v['event']} ({v['path']})" for v in value[:8])
        else:
            shown = ", ".join(str(v) for v in value[:12])
        lines.append(f"- {label}: {shown}")
    return "\n".join(lines) if lines else "- none detected"


def build_briefing(
    case_path: str,
    *,
    case_id: Optional[str] = None,
    cutoff_event: Optional[int] = None,
    cutoff_time: Optional[str] = None,
    task: Optional[str] = None,
) -> Briefing:
    args = {"case_path": case_path, "reset": True}
    if case_id:
        args["case_id"] = case_id
    if cutoff_event is not None:
        args["cutoff_event"] = cutoff_event
    if cutoff_time:
        args["cutoff_time"] = cutoff_time
    loaded = call_tool("load_case", args)
    if not loaded["ok"]:
        raise BriefingError(f"load_case failed: {loaded['error']['code']}: {loaded['error']['message']}")
    case = loaded["data"]
    case_id = case["case_id"]

    screen_result = call_tool("safety_screen", {"case_id": case_id})
    screen = screen_result["data"] if screen_result["ok"] else {
        "level": "unknown", "recommended_response": "screen failed - judge manually", "hazards": {},
        "escalation_flags": [], "negated_matches": []}
    docs = _supplied_documents(case, case_id)
    attachments = _case_attachments(case, case_id)
    for doc in docs + attachments:
        if doc["text"]:
            extra = call_tool("safety_screen", {"text": doc["text"]})
            if extra["ok"] and extra["data"]["hazards"]:
                doc["screen_level"] = extra["data"]["level"]
                doc["screen_hazards"] = list(extra["data"]["hazards"])

    events = case["events"]
    details = "\n".join(f"- {k}: {v}" for k, v in case["details"].items()) or "- (none supplied)"
    attachment_blocks = []
    for doc in attachments:
        where = (f"arrived with {', '.join(sorted(set(doc['linked_events'])))}" if doc["linked_events"]
                 else "not linked to any visible event, so its date is unknown")
        header = f"### {doc['path']} ({doc['kind']}; {where})"
        if doc.get("screen_hazards"):
            header += (f" - hazard keywords found: {doc['screen_hazards']} "
                       "(may be standard report wording; judge in context)")
        body = doc["text"] if doc["text"] else ""
        if doc.get("note"):
            body = (body + "\n" if body else "") + f"[{doc['note']}]"
        attachment_blocks.append(f"{header}\n{body}")
    attachments_section = "\n\n".join(attachment_blocks) if attachment_blocks else "None."
    extra_sections = "\n\n".join(f"## {k.title()}\n{v}" for k, v in case.get("other_sections", {}).items() if v)

    doc_blocks = []
    for doc in docs:
        header = f"### {doc['path']} ({doc['kind']})"
        if doc.get("screen_hazards"):
            header += f" - safety screen: {doc['screen_level']} {doc['screen_hazards']}"
        body = doc["text"] if doc["text"] else f"[{doc['note']}]"
        doc_blocks.append(f"{header}\n{body}")
    docs_section = "\n\n".join(doc_blocks) if doc_blocks else "None."

    latest = events[-3:] if events else []
    parts = [
        f"# Case briefing: {case_id}",
        f"Title: {case.get('title') or '(none)'}",
        f"Property: {case.get('property') or 'UNKNOWN'}",
        f"Current time (latest visible event): {case['now']}",
        f"Visible history: {len(events)} event(s){' ending at ' + events[-1]['id'] if events else ''}. "
        "Nothing after this point is known.",
        "## Case details\n" + details,
        "## Initial request\n" + (case.get("initial_request") or "(not stated)"),
    ]
    if extra_sections:
        parts.append(extra_sections)
    if task:
        parts.append("## Question / task supplied with this case\n" + task)
    parts += [
        "## Newly supplied documents (read carefully: often the latest input)\n" + docs_section,
        "## Case attachments (text extracted automatically; use these facts and cite them)\n" + attachments_section,
        "## Data-quality flags\n" + _format_quality(case["data_quality"]),
        "## Safety screen (automatic, rule-based)\n" + _format_screen(screen),
        "## Full event history (oldest first)\n" + ("\n\n".join(_fmt_event(e) for e in events) or "(no events)"),
        "## Most recent event(s)\n" + ("\n\n".join(_fmt_event(e) for e in latest) or "(no events)"),
        "## Your task\nDecide and carry out the agency's next step at this point in the case, then call "
        "submit_decision exactly once.",
    ]
    return Briefing(case_id=case_id, text="\n\n".join(parts), case=case, screen=screen,
                    supplied_documents=docs, attachments=attachments)
