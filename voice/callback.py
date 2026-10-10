"""Produce the tenant's voice update: the spoken version of what the agent decided to tell them.

The update is taken from the agent's ledger, never invented here: a call script to the tenant if the
agent wrote one, otherwise its message to the tenant (email/SMS, contractor notice, or a drafted
message in an escalation). It is spoken in the intake line's voice and saved as an MP3 in
voice/outbox/. If the decision has nothing for the tenant, no voice update is made.

    python -m voice.callback --run-dir runs/voice-001 --case-folder voice/cases/001
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from voice.client import ElevenLabs
from voice.config import CALLBACKS_DIR, OUTBOX_DIR, load_state

MAX_SPOKEN_CHARS = 900
GREETING = re.compile(r"^(dear|hi|hello|good (morning|afternoon|evening))\b[^.!?]*,?$", re.I)
# A sign-off is a short closing line on its own ("Kind regards,", "Thanks"), not "Thanks for calling...".
SIGN_OFF = re.compile(r"^(kind regards|best regards|warm regards|regards|many thanks|thanks|thank you|"
                      r"yours sincerely|yours faithfully|best wishes|best)[,.!]?$", re.I)
OPENING = re.compile(r"^(hello|hi|hey|dear|good (morning|afternoon|evening))\b", re.I)


def read_case_details(case_folder: Path) -> dict:
    details = {}
    for line in (case_folder / "index.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"-\s+\*\*([^*:]+):\*\*\s*(.*)", line.strip())
        if m:
            details[m.group(1).strip().lower()] = m.group(2).strip().strip("`")
    return details


def _to_tenant(recipients) -> bool:
    if isinstance(recipients, dict):
        recipients = [recipients]
    return any((r or {}).get("role") == "tenant" for r in recipients or [])


def tenant_update_from_ledger(ledger: list[dict]) -> Optional[dict]:
    """Pick what the agent decided to tell the tenant, in order of preference."""
    calls, messages, drafts = [], [], []
    for e in ledger:
        if not e.get("ok") or e.get("duplicate"):
            continue
        d = e.get("data") or {}
        if e["tool"] == "place_call" and _to_tenant(d.get("to")):
            calls.append(d.get("script") or "")
        elif e["tool"] in ("send_email", "send_sms") and _to_tenant(d.get("to")) and d.get("purpose") != "nudge_check_email":
            messages.append((d.get("purpose"), d.get("body") or ""))
        elif e["tool"] in ("assign_contractor", "schedule_appointment"):
            messages += [("status_update", m.get("body") or "") for m in d.get("messages", []) if _to_tenant(m.get("to"))]
        elif e["tool"] == "escalate_to_human":
            drafts += [m.get("body") or "" for m in d.get("draft_messages", []) if _to_tenant(m.get("to"))]
    if calls:
        return {"source": "agent call script", "text": calls[-1]}
    safety = [b for p, b in messages if p == "safety_advice"]
    if safety:
        return {"source": "agent safety advice to tenant", "text": safety[-1]}
    if messages:
        return {"source": "agent message to tenant", "text": messages[0][1]}
    if drafts:
        return {"source": "tenant message drafted in the escalation", "text": drafts[0]}
    return None


def to_speech(text: str, limit: int = MAX_SPOKEN_CHARS) -> str:
    """Strip email furniture (greeting, sign-off, markdown) and keep it short enough to say on a call."""
    kept = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if not kept and GREETING.match(line):
            continue
        if SIGN_OFF.match(line):
            break
        kept.append(line)
    spoken = " ".join(kept)
    spoken = re.sub(r"https?://\S+", "", spoken)
    spoken = re.sub(r"[*_#>`|]", "", spoken)
    spoken = re.sub(r"\s+", " ", spoken).strip()
    spoken = strip_opening(spoken)
    if len(spoken) > limit:
        cut = spoken[:limit]
        end = max(cut.rfind(". "), cut.rfind("? "), cut.rfind("! "))
        spoken = (cut[: end + 1] if end > limit // 2 else cut.rstrip() + "…") + \
            " We'll send the full details in writing."
    return spoken


def strip_opening(text: str) -> str:
    """Drop the agent's own greeting ("Hello Fazal, this is Northbridge Lettings calling about...").

    The voice update adds one standard greeting, so a second one in the script would be repeated.
    """
    sentences = re.split(r"(?<=[.!?])\s+", text)
    dropped = 0
    while sentences and dropped < 2 and (OPENING.match(sentences[0]) or "this is northbridge" in sentences[0].lower()):
        sentences.pop(0)
        dropped += 1
    return " ".join(sentences)


def find_case_run(run_dir: Path) -> Path:
    cases = [p for p in (run_dir / "cases").iterdir() if (p / "ledger.jsonl").exists()]
    if len(cases) != 1:
        raise SystemExit(f"Expected one case in {run_dir}/cases, found {len(cases)}.")
    return cases[0]


def voice_update(run_dir: Path, case_folder: Path, *, client: Optional[ElevenLabs] = None) -> dict:
    case_run = find_case_run(run_dir)
    ledger = [json.loads(line) for line in (case_run / "ledger.jsonl").read_text().splitlines() if line.strip()]
    decision = json.loads((case_run / "decision.json").read_text())["decision"]
    details = read_case_details(case_folder)
    update = tenant_update_from_ledger(ledger)

    record = {
        "case_folder": str(case_folder), "agent_decision": decision.get("decision"),
        "created_at": datetime.now(timezone.utc).isoformat(), "mode": None,
    }
    if not update:
        record.update(mode="none", reason="The agent's decision contains nothing for the tenant, so no voice update was made.")
        return _save(case_folder, record)

    voice_id = load_state().get("voice_id")
    if not voice_id:
        raise SystemExit("No voice recorded. Run: python -m voice.setup")
    name = (details.get("tenant") or "").replace("Not given", "").strip() or "there"
    address = (details.get("property") or "").replace("Not confirmed on the call", "").strip() or "your home"
    spoken = to_speech(update["text"])
    message = (f"Hello {name}, this is Northbridge Lettings with an update about your repair at {address}. "
               f"{spoken} Thank you, goodbye.")
    client = client or ElevenLabs()
    OUTBOX_DIR.mkdir(parents=True, exist_ok=True)
    out = OUTBOX_DIR / f"{case_folder.name}-update.mp3"
    out.write_bytes(client.tts(message, voice_id))
    record.update(mode="voice_message", update_source=update["source"], audio_file=str(out), spoken_text=message)
    return _save(case_folder, record)


def _save(case_folder: Path, record: dict) -> dict:
    CALLBACKS_DIR.mkdir(parents=True, exist_ok=True)
    (CALLBACKS_DIR / f"{case_folder.name}.json").write_text(json.dumps(record, indent=2, ensure_ascii=False))
    return record


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Make the tenant's MP3 voice update from the agent's decision.")
    parser.add_argument("--run-dir", required=True, help="runs/<run-name> of the agent run for this case.")
    parser.add_argument("--case-folder", required=True, help="voice/cases/<n>")
    args = parser.parse_args(argv)
    record = voice_update(Path(args.run_dir), Path(args.case_folder))
    print(json.dumps(record, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
