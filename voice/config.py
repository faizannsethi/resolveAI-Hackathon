"""Voice settings, ElevenLabs key loading and the small state file (intake agent id and voice)."""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

VOICE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = VOICE_DIR.parent
STATE_FILE = VOICE_DIR / "state.json"
CASES_DIR = VOICE_DIR / "cases"            # case folders built from calls (index.md + history.md)
RECORDINGS_DIR = VOICE_DIR / "recordings"  # call audio, kept outside case folders on purpose
CALLBACKS_DIR = VOICE_DIR / "callbacks"    # records of the voice updates produced
OUTBOX_DIR = VOICE_DIR / "outbox"          # MP3 voice updates for the tenant

INTAKE_AGENT_NAME_HINT = "repairs line"


def load_elevenlabs_key() -> str:
    """ELEVENLABS_API_KEY, else the first token of the local eleven_labs_api_key file (never printed)."""
    if os.environ.get("ELEVENLABS_API_KEY"):
        return os.environ["ELEVENLABS_API_KEY"].strip()
    key_file = Path(os.environ.get("ELEVENLABS_API_KEY_FILE", PROJECT_ROOT / "eleven_labs_api_key"))
    if key_file.exists():
        match = re.search(r"\S+", key_file.read_text(encoding="utf-8"))
        if match:
            return match.group(0)
    raise RuntimeError("No ElevenLabs key: set ELEVENLABS_API_KEY or create eleven_labs_api_key.")


def load_state() -> dict:
    return json.loads(STATE_FILE.read_text()) if STATE_FILE.exists() else {}


def save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, indent=2) + "\n")
