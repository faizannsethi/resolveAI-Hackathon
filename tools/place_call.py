"""place_call - log an outbound phone call with its script; optionally voice it with ElevenLabs.

Calls are simulated: the result is a call record with the script and, when
``synthesize_audio`` is true and ElevenLabs is configured, an MP3 of the message saved
under the case's artifacts folder. The other party's answer is unknown until a reply
event arrives, so the call outcome is always 'awaiting_response'.
"""

from __future__ import annotations

import os
import time
from typing import Literal, Optional

import requests
from pydantic import Field

from tools._common import (
    Recipient,
    SideEffectInput,
    Tool,
    ToolFailure,
    artifacts_dir,
    case_now,
    check_outbound_text,
    iso,
    new_id,
)

TTS_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
DEFAULT_VOICE = "21m00Tcm4TlvDq8ikWAM"


class PlaceCallInput(SideEffectInput):
    to: Recipient
    purpose: Literal[
        "urgent_safety", "arrange_access", "chase_response", "obtain_approval", "gather_information",
        "status_update", "other",
    ]
    script: str = Field(
        ..., min_length=20, max_length=4000,
        description="What will be said: opening, key points, questions to ask. Ready to speak aloud.",
    )
    voicemail_message: Optional[str] = Field(
        None, max_length=1000, description="Message to leave if there is no answer."
    )
    synthesize_audio: bool = Field(
        False, description="Generate an MP3 of the script (or voicemail) with ElevenLabs text-to-speech."
    )
    allow_other_addresses: bool = False


def _synthesize(text: str, out_path) -> None:
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        raise ToolFailure("not_configured", "ELEVENLABS_API_KEY is not set.")
    voice = os.environ.get("ELEVENLABS_VOICE_ID", DEFAULT_VOICE)
    last = "unknown error"
    for attempt in range(3):
        try:
            response = requests.post(
                TTS_URL.format(voice_id=voice),
                params={"output_format": "mp3_44100_128"},
                headers={"xi-api-key": key, "Content-Type": "application/json"},
                json={"text": text, "model_id": os.environ.get("ELEVENLABS_TTS_MODEL", "eleven_multilingual_v2")},
                timeout=120,
            )
        except requests.RequestException as exc:
            last = f"network error: {exc}"
        else:
            if response.status_code == 200 and response.content:
                out_path.write_bytes(response.content)
                return
            if response.status_code in (401, 403):
                raise ToolFailure("auth_failed", "ElevenLabs rejected the API key.")
            if response.status_code not in (408, 429) and response.status_code < 500:
                raise ToolFailure("rejected", f"ElevenLabs HTTP {response.status_code}: {response.text[:200]}")
            last = f"HTTP {response.status_code}"
        time.sleep(1.5 * (attempt + 1))
    raise ToolFailure("unavailable", f"Text-to-speech failed after 3 attempts ({last}).", retryable=True)


def _handle(params: PlaceCallInput) -> tuple[dict, list[str]]:
    text = params.script + "\n" + (params.voicemail_message or "")
    warnings = check_outbound_text(params.case_id, text, allow_other_addresses=params.allow_other_addresses)
    if params.to.role == "agency_internal":
        raise ToolFailure("invalid_recipient", "Use escalate_to_human to reach internal staff.")
    call_id = new_id(params.case_id, "CALL")
    record = {
        "id": call_id,
        "channel": "call",
        "status": "placed",
        "delivery": "simulated",
        "outcome": "awaiting_response",
        "placed_at": iso(case_now(params.case_id)),
        "to": params.to.model_dump(exclude_none=True),
        "purpose": params.purpose,
        "script": params.script,
        "voicemail_message": params.voicemail_message,
        "audio_file": None,
    }
    if not params.to.phone:
        warnings.append("No phone number given; dialled the number on file for the case.")
    if params.synthesize_audio:
        out = artifacts_dir(params.case_id) / f"{call_id}.mp3"
        try:
            _synthesize(params.voicemail_message or params.script, out)
            record["audio_file"] = f"artifacts/{out.name}"
        except ToolFailure as exc:
            # Voice is an enhancement: the call is still logged with its script.
            warnings.append(f"Audio not generated ({exc.code}: {exc.message}); script logged only.")
    return record, warnings


TOOL = Tool(
    name="place_call",
    description="""
Place (log) an outbound phone call: for urgent safety advice, arranging access, chasing a
non-responsive party, or getting a quick approval. Provide a ready-to-speak script and an
optional voicemail. The answer is not known until a reply event arrives, so follow up with
set_hold or a later check. With synthesize_audio=true, an MP3 of the message is generated
via ElevenLabs; if that fails, the call is still logged and a warning explains why.
""",
    input_model=PlaceCallInput,
    handler=_handle,
    side_effect=True,
)
