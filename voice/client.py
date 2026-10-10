"""Thin ElevenLabs REST client: intake conversations, agent lookup and text-to-speech."""

from __future__ import annotations

import time
from typing import Any, Optional

import requests

from voice.config import load_elevenlabs_key

BASE_URL = "https://api.elevenlabs.io"


class ElevenLabsError(RuntimeError):
    def __init__(self, status: int, message: str):
        super().__init__(f"ElevenLabs HTTP {status}: {message}")
        self.status = status


class ElevenLabs:
    def __init__(self, api_key: Optional[str] = None, base_url: str = BASE_URL, timeout: int = 60):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers["xi-api-key"] = api_key or load_elevenlabs_key()

    def _request(self, method: str, path: str, *, raw: bool = False, **kwargs: Any) -> Any:
        last = "no response"
        for attempt in range(3):
            try:
                response = self.session.request(method, self.base_url + path, timeout=self.timeout, **kwargs)
            except requests.RequestException as exc:
                last = f"network error: {exc}"
            else:
                if response.ok:
                    return response.content if raw else (response.json() if response.content else {})
                if response.status_code not in (408, 429) and response.status_code < 500:
                    raise ElevenLabsError(response.status_code, response.text[:500])
                last = f"HTTP {response.status_code}"
            time.sleep(1.5 * (attempt + 1))
        raise ElevenLabsError(0, f"failed after retries ({last})")

    # -- agents ---------------------------------------------------------------------------------
    def list_agents(self) -> list[dict]:
        return self._request("GET", "/v1/convai/agents", params={"page_size": 100}).get("agents", [])

    def get_agent(self, agent_id: str) -> dict:
        return self._request("GET", f"/v1/convai/agents/{agent_id}")

    # -- conversations -------------------------------------------------------------------------
    def list_conversations(self, agent_id: str, page_size: int = 20) -> list[dict]:
        return self._request("GET", "/v1/convai/conversations",
                             params={"agent_id": agent_id, "page_size": page_size}).get("conversations", [])

    def get_conversation(self, conversation_id: str) -> dict:
        return self._request("GET", f"/v1/convai/conversations/{conversation_id}")

    def get_conversation_audio(self, conversation_id: str) -> bytes:
        return self._request("GET", f"/v1/convai/conversations/{conversation_id}/audio", raw=True)

    def wait_until_processed(self, conversation_id: str, timeout_s: int = 300) -> dict:
        """Calls are analysed after they end; wait for status 'done' so the extracted fields exist."""
        deadline = time.time() + timeout_s
        while True:
            conversation = self.get_conversation(conversation_id)
            if conversation.get("status") in ("done", "failed") or time.time() > deadline:
                return conversation
            time.sleep(5)

    # -- text to speech (voice-message fallback) -----------------------------------------------
    def tts(self, text: str, voice_id: str, model_id: str = "eleven_multilingual_v2") -> bytes:
        return self._request("POST", f"/v1/text-to-speech/{voice_id}", raw=True,
                             params={"output_format": "mp3_44100_128"},
                             json={"text": text, "model_id": model_id})
