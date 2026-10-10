"""transcribe_audio - turn a call recording / voice note into speaker-labelled text.

Engines are tried in order until one succeeds:

1. ``elevenlabs``    - ElevenLabs Speech-to-Text (Scribe): speaker diarisation, word
                       timings and non-speech audio events (alarm, crying, shouting...).
2. ``local_whisper`` - faster-whisper on this machine, if installed (offline backup).
3. ``sidecar``       - an existing transcript next to the audio (same name, .txt/.vtt/.srt/.json).

Every attempt is reported, so a failed or degraded transcription is visible in the trace.
"""

from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path
from typing import Literal, Optional

import requests
from pydantic import Field

from tools._common import (
    CASE_ID_PATTERN,
    PROJECT_ROOT,
    Tool,
    ToolFailure,
    ToolInput,
    load_context,
)

AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".ogg", ".oga", ".flac", ".webm", ".mp4", ".aac", ".opus"}
Engine = Literal["elevenlabs", "local_whisper", "sidecar"]
ELEVENLABS_STT_URL = "https://api.elevenlabs.io/v1/speech-to-text"
MAX_BYTES = 1_000_000_000


class TranscribeAudioInput(ToolInput):
    path: str = Field(..., description="Audio file. Relative to the case folder when case_id is given.")
    case_id: Optional[str] = Field(None, pattern=CASE_ID_PATTERN)
    language_code: Optional[str] = Field(
        None, pattern=r"^[a-z]{2,3}(-[A-Za-z]{2,4})?$", description="e.g. 'en'. Omit to auto-detect."
    )
    num_speakers: Optional[int] = Field(None, ge=1, le=32, description="Expected speakers, if known.")
    engines: list[Engine] = Field(
        default_factory=lambda: ["elevenlabs", "local_whisper", "sidecar"],
        min_length=1,
        description="Engines to try, in order.",
    )


def _resolve(params: TranscribeAudioInput) -> Path:
    raw = Path(params.path).expanduser()
    if params.case_id:
        root = (load_context(params.case_id) or {}).get("case_root")
        if root and not raw.is_absolute():
            root_path = Path(root).resolve()
            raw = (root_path / raw).resolve()
            if root_path not in raw.parents:
                raise ToolFailure("path_outside_case", "Audio must be inside the case folder.")
    if not raw.is_absolute():
        raw = (PROJECT_ROOT / raw).resolve()
    if not raw.is_file():
        raise ToolFailure("not_found", f"No audio file at {params.path!r}.")
    if raw.suffix.lower() not in AUDIO_EXTENSIONS:
        raise ToolFailure("unsupported_type", f"{raw.suffix} is not a supported audio format.")
    if raw.stat().st_size == 0:
        raise ToolFailure("empty_file", "Audio file is empty.")
    if raw.stat().st_size > MAX_BYTES:
        raise ToolFailure("file_too_large", "Audio file exceeds 1 GB.")
    return raw


def _segments_from_words(words: list[dict]) -> tuple[list[dict], list[dict]]:
    """Group word-level output into speaker turns and pull out audio events."""
    segments: list[dict] = []
    events: list[dict] = []
    for word in words:
        kind = word.get("type", "word")
        if kind == "audio_event":
            events.append({"label": word.get("text", "").strip("()[] "), "start": word.get("start"),
                           "speaker": word.get("speaker_id")})
            continue
        speaker = word.get("speaker_id") or "speaker_0"
        if not segments or segments[-1]["speaker"] != speaker:
            segments.append({"speaker": speaker, "start": word.get("start"), "end": word.get("end"), "text": ""})
        segments[-1]["text"] += word.get("text", "")
        if word.get("end") is not None:
            segments[-1]["end"] = word.get("end")
    for seg in segments:
        seg["text"] = re.sub(r"\s+", " ", seg["text"]).strip()
    return [s for s in segments if s["text"]], events


def _elevenlabs(path: Path, params: TranscribeAudioInput) -> dict:
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        raise ToolFailure("not_configured", "ELEVENLABS_API_KEY is not set.")
    form = {
        "model_id": os.environ.get("ELEVENLABS_STT_MODEL", "scribe_v1"),
        "diarize": "true",
        "tag_audio_events": "true",
        "timestamps_granularity": "word",
    }
    if params.language_code:
        form["language_code"] = params.language_code
    if params.num_speakers:
        form["num_speakers"] = str(params.num_speakers)

    last_error = "unknown error"
    for attempt in range(3):
        try:
            with path.open("rb") as handle:
                response = requests.post(
                    ELEVENLABS_STT_URL,
                    headers={"xi-api-key": key},
                    data=form,
                    files={"file": (path.name, handle)},
                    timeout=300,
                )
        except requests.RequestException as exc:
            last_error = f"network error: {exc}"
        else:
            if response.status_code == 200:
                body = response.json()
                segments, events = _segments_from_words(body.get("words") or [])
                return {
                    "text": (body.get("text") or "").strip(),
                    "language": body.get("language_code"),
                    "language_probability": body.get("language_probability"),
                    "segments": segments,
                    "audio_events": events,
                }
            if response.status_code in (401, 403):
                raise ToolFailure("auth_failed", "ElevenLabs rejected the API key.")
            if response.status_code not in (408, 429) and response.status_code < 500:
                raise ToolFailure("rejected", f"ElevenLabs HTTP {response.status_code}: {response.text[:300]}")
            last_error = f"HTTP {response.status_code}"
        time.sleep(1.5 * (attempt + 1))
    raise ToolFailure("unavailable", f"ElevenLabs failed after 3 attempts ({last_error}).", retryable=True)


def _local_whisper(path: Path, params: TranscribeAudioInput) -> dict:
    try:
        from faster_whisper import WhisperModel  # type: ignore
    except ImportError as exc:
        raise ToolFailure("not_installed", "faster-whisper is not installed.") from exc
    model = WhisperModel(os.environ.get("WHISPER_MODEL", "small"), device="auto", compute_type="int8")
    raw_segments, info = model.transcribe(str(path), language=params.language_code, vad_filter=True)
    segments = [
        {"speaker": "unknown", "start": round(s.start, 2), "end": round(s.end, 2), "text": s.text.strip()}
        for s in raw_segments
    ]
    return {
        "text": " ".join(s["text"] for s in segments).strip(),
        "language": info.language,
        "language_probability": info.language_probability,
        "segments": segments,
        "audio_events": [],
    }


def _sidecar(path: Path, _params: TranscribeAudioInput) -> dict:
    for ext in (".json", ".txt", ".vtt", ".srt", ".md"):
        candidate = path.with_suffix(ext)
        if candidate.is_file():
            raw = candidate.read_text(encoding="utf-8", errors="replace")
            if ext == ".json":
                try:
                    obj = json.loads(raw)
                    raw = obj.get("text") or json.dumps(obj)
                except json.JSONDecodeError:
                    pass
            if ext in (".vtt", ".srt"):
                raw = "\n".join(
                    line for line in raw.splitlines()
                    if line.strip() and "-->" not in line and not line.strip().isdigit() and line.strip() != "WEBVTT"
                )
            return {"text": raw.strip(), "language": None, "language_probability": None,
                    "segments": [], "audio_events": [], "sidecar_file": candidate.name}
    raise ToolFailure("no_sidecar", "No transcript file found next to the audio.")


ENGINES = {"elevenlabs": _elevenlabs, "local_whisper": _local_whisper, "sidecar": _sidecar}


def _handle(params: TranscribeAudioInput) -> tuple[dict, list[str]]:
    path = _resolve(params)
    attempts = []
    for engine in params.engines:
        try:
            result = ENGINES[engine](path, params)
        except ToolFailure as exc:
            attempts.append({"engine": engine, "ok": False, "code": exc.code, "message": exc.message})
            continue
        if not result["text"]:
            attempts.append({"engine": engine, "ok": False, "code": "empty_transcript",
                             "message": "Engine returned no speech."})
            continue
        attempts.append({"engine": engine, "ok": True})
        warnings = []
        if engine != params.engines[0]:
            warnings.append(f"Primary engine failed; transcript produced by fallback '{engine}'.")
        if engine == "sidecar":
            warnings.append("Using a pre-existing transcript: speaker labels and audio events are unavailable.")
        if engine != "elevenlabs":
            warnings.append("No diarisation: speaker identities must be inferred from content.")
        return {"path": params.path, "engine": engine, "attempts": attempts, **result}, warnings

    raise ToolFailure(
        "transcription_failed",
        "All transcription engines failed. Treat the call content as unknown and escalate or ask "
        "the caller to resend in writing.",
        retryable=any(a.get("code") == "unavailable" for a in attempts),
        details={"attempts": attempts},
    )


TOOL = Tool(
    name="transcribe_audio",
    description="""
Transcribe an audio file (call recording or voice note) into text with speaker turns,
timestamps and detected non-speech audio events (e.g. alarm, crying), which can signal
urgency. Uses ElevenLabs Speech-to-Text first, then a local Whisper model, then any transcript
file saved next to the audio. Check 'engine' and 'attempts' in the result: a fallback
transcript has no speaker labels. If every engine fails, do not guess what was said.
""",
    input_model=TranscribeAudioInput,
    handler=_handle,
    side_effect=False,
    injectable=True,
)
