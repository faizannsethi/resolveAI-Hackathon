"""Turn a finished intake call into a case folder (index.md + history.md) the agent already understands.

    python -m voice.intake --latest            # newest finished call to the intake agent
    python -m voice.intake --conversation-id conv_...

The call becomes event-001 (Channel: Call, From: Tenant): the voice agent's summary, the extracted
fields and the full transcript. Call audio is saved under voice/recordings/, outside the case
folder, so the case agent works from the transcript and never re-transcribes it.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from voice.client import ElevenLabs
from voice.config import CASES_DIR, RECORDINGS_DIR, load_state


def _field(conversation: dict, name: str) -> Optional[str]:
    results = ((conversation.get("analysis") or {}).get("data_collection_results") or {})
    value = (results.get(name) or {}).get("value")
    if value is None or (isinstance(value, str) and not value.strip()):
        return None
    return str(value).strip()


def _when(conversation: dict) -> datetime:
    start = (conversation.get("metadata") or {}).get("start_time_unix_secs")
    return datetime.fromtimestamp(start, tz=timezone.utc) if start else datetime.now(timezone.utc)


def _transcript(conversation: dict) -> str:
    lines = []
    for turn in conversation.get("transcript") or []:
        text = (turn.get("message") or "").strip()
        if not text:
            continue
        who = "Agency voice assistant" if turn.get("role") == "agent" else "Tenant"
        lines.append(f"{who}: {text}")
    return "\n".join(lines)


def has_tenant_speech(conversation: dict) -> bool:
    """False for silent calls (every caller turn empty or '...'): nothing to build a case from."""
    return any(re.sub(r"[.\s…]", "", turn.get("message") or "")
               for turn in conversation.get("transcript") or [] if turn.get("role") == "user")


def next_case_number(cases_dir: Path = CASES_DIR) -> str:
    existing = [int(p.name) for p in cases_dir.glob("*") if p.is_dir() and p.name.isdigit()]
    return f"{(max(existing) + 1) if existing else 1:03d}"


def build_case(conversation: dict, cases_dir: Path = CASES_DIR, number: Optional[str] = None) -> Path:
    """Write voice/cases/<n>/index.md and history.md for one call. Returns the case folder."""
    cases_dir.mkdir(parents=True, exist_ok=True)
    for existing in cases_dir.glob("*/index.md"):
        if f"`{conversation['conversation_id']}`" in existing.read_text(encoding="utf-8"):
            return existing.parent  # already converted; never duplicate a call
    number = number or next_case_number(cases_dir)
    folder = cases_dir / number
    folder.mkdir(parents=True, exist_ok=False)

    analysis = conversation.get("analysis") or {}
    meta = conversation.get("metadata") or {}
    when = _when(conversation).strftime("%Y-%m-%d %H:%M:%S UTC")
    name = _field(conversation, "tenant_name")
    address = _field(conversation, "property_address")
    issue = _field(conversation, "issue_summary") or analysis.get("transcript_summary") or "(not captured)"
    hazard = _field(conversation, "hazard")
    vulnerable = _field(conversation, "vulnerable_occupant")
    access = _field(conversation, "access_notes")
    callback = _field(conversation, "callback_number") or ((meta.get("phone_call") or {}).get("external_number"))
    other = _field(conversation, "out_of_scope_requests")
    title = analysis.get("call_summary_title") or "Repair reported by phone"

    details = [
        "- **Source role:** Tenant",
        f"- **Created:** {when}",
        f"- **Property:** {address or 'Not confirmed on the call'}",
        "- **Received via:** Phone call to the Northbridge Lettings repairs line (voice assistant)",
        f"- **Tenant:** {name or 'Not given'}",
        f"- **Callback number:** {callback or 'Not given'}",
        f"- **Call reference:** `{conversation['conversation_id']}`",
    ]
    extra = [f"- Most serious safety signal described: {hazard or 'none described'}",
             f"- Vulnerable occupant at the property: {'yes' if str(vulnerable).lower() == 'true' else 'no / not stated'}",
             f"- Access notes: {access or 'none given'}"]
    if other:
        extra.append(f"- Other matters raised (not repairs): {other}")

    index = "\n".join([
        f"# Case {number}: {title}", "", "## Case details", "", *details, "",
        "## Initial request", "", issue, "", "Additional details provided:", *extra, "",
        "## History", "", "[Read the complete event history](history.md).", "",
    ])
    duration = meta.get("call_duration_secs")
    body = "\n".join([
        f"Inbound phone call to the repairs line{f' ({duration} seconds)' if duration else ''}, handled by the "
        "agency's voice assistant. Fields captured on the call are listed in the case details.",
        "",
        f"Call summary: {analysis.get('transcript_summary') or '(no summary produced)'}",
        "",
        "Transcript:",
        _transcript(conversation) or "(transcript unavailable)",
    ])
    history = "\n".join([
        f"# Case {number} history", "", "Total events: 1", "",
        '<a id="event-001"></a>', f"## {when} — event 001", "",
        "- **Channel:** Call", "- **From:** Tenant", "- **To:** Agency / system", "", body, "",
    ])
    (folder / "index.md").write_text(index, encoding="utf-8")
    (folder / "history.md").write_text(history, encoding="utf-8")
    return folder


def save_audio(client: ElevenLabs, conversation: dict, number: str) -> Optional[Path]:
    if not conversation.get("has_audio", True):
        return None
    try:
        audio = client.get_conversation_audio(conversation["conversation_id"])
    except Exception:  # noqa: BLE001 - audio is a convenience, the transcript is what matters
        return None
    RECORDINGS_DIR.mkdir(parents=True, exist_ok=True)
    path = RECORDINGS_DIR / f"{number}-{conversation['conversation_id']}.mp3"
    path.write_bytes(audio)
    return path


def latest_finished_conversation(client: ElevenLabs, agent_id: str) -> Optional[str]:
    conversations = client.list_conversations(agent_id)
    conversations.sort(key=lambda c: c.get("start_time_unix_secs") or 0, reverse=True)
    for c in conversations:
        if c.get("status") in ("done", "processing"):
            return c["conversation_id"]
    return None


def intake(conversation_id: Optional[str] = None, *, client: Optional[ElevenLabs] = None) -> Path:
    client = client or ElevenLabs()
    if not conversation_id:
        agent_id = load_state().get("intake_agent_id")
        if not agent_id:
            raise SystemExit("No intake agent recorded. Run: python -m voice.setup")
        conversation_id = latest_finished_conversation(client, agent_id)
        if not conversation_id:
            raise SystemExit("No finished calls to the intake agent yet.")
    conversation = client.wait_until_processed(conversation_id)
    if conversation.get("status") != "done":
        raise SystemExit(f"Call {conversation_id} is '{conversation.get('status')}', not finished; try again shortly.")
    if not has_tenant_speech(conversation):
        raise SystemExit(f"Call {conversation_id} has no speech from the caller (microphone muted or not shared?). "
                         "No case was created.")
    folder = build_case(conversation)
    save_audio(client, conversation, folder.name)
    return folder


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Convert an intake call into a case folder.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--latest", action="store_true", help="Newest finished call to the intake agent.")
    group.add_argument("--conversation-id", help="A specific ElevenLabs conversation id.")
    args = parser.parse_args(argv)
    folder = intake(args.conversation_id)
    print(json.dumps({"case_folder": str(folder)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
