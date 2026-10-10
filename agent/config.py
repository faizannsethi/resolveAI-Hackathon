"""Agent configuration. Everything tunable lives here or in environment variables."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class AgentConfig:
    model: str = os.environ.get("AGENT_MODEL", "claude-opus-5-5")
    effort: str = os.environ.get("AGENT_EFFORT", "high")          # low | medium | high | xhigh | max
    max_tokens: int = int(os.environ.get("AGENT_MAX_TOKENS", "32000"))
    max_turns: int = int(os.environ.get("AGENT_MAX_TURNS", "30"))  # model calls per case
    use_fallbacks: bool = os.environ.get("AGENT_FALLBACKS", "1") == "1"
    betas: tuple[str, ...] = field(default_factory=lambda: ("server-side-fallback-2026-07-01",))


def load_api_key() -> str:
    """ANTHROPIC_API_KEY, else the key inside the local `api_key` file (never printed or logged)."""
    if os.environ.get("ANTHROPIC_API_KEY"):
        return os.environ["ANTHROPIC_API_KEY"]
    key_file = Path(os.environ.get("ANTHROPIC_API_KEY_FILE", PROJECT_ROOT / "api_key"))
    if key_file.exists():
        match = re.search(r"sk-ant-[A-Za-z0-9_\-]+", key_file.read_text(encoding="utf-8"))
        if match:
            return match.group(0)
    raise RuntimeError("No Anthropic API key: set ANTHROPIC_API_KEY or provide an api_key file.")
