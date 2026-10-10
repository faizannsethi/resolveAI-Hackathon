"""One-off setup: record the ElevenLabs intake agent and its voice in voice/state.json.

    python -m voice.setup                          # finds the agent named like "repairs line"
    python -m voice.setup --intake-agent-id agent_...

Re-running is safe. The voice recorded here is also used for the tenant's MP3 voice update.
"""

from __future__ import annotations

import argparse
import json
from typing import Optional

from voice.client import ElevenLabs
from voice.config import INTAKE_AGENT_NAME_HINT, load_state, save_state


def find_intake_agent(client: ElevenLabs, agent_id: Optional[str]) -> dict:
    if agent_id:
        return client.get_agent(agent_id)
    matches = [a for a in client.list_agents() if INTAKE_AGENT_NAME_HINT in (a.get("name") or "").lower()]
    if len(matches) != 1:
        raise SystemExit(f"Found {len(matches)} agents named like '{INTAKE_AGENT_NAME_HINT}'; pass --intake-agent-id.")
    return client.get_agent(matches[0]["agent_id"])


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Set up the voice layer.")
    parser.add_argument("--intake-agent-id", help="Existing intake agent (default: the one named like 'repairs line').")
    args = parser.parse_args(argv)

    client = ElevenLabs()
    previous = load_state()
    intake = find_intake_agent(client, args.intake_agent_id or previous.get("intake_agent_id"))
    tts = (intake.get("conversation_config") or {}).get("tts") or {}
    state = {"intake_agent_id": intake["agent_id"], "intake_agent_name": intake.get("name"),
             "voice_id": tts.get("voice_id"), "tts_model": tts.get("model_id")}
    save_state(state)
    print(json.dumps({**state, "talk_to_intake_in_browser":
                      f"https://elevenlabs.io/app/talk-to?agent_id={state['intake_agent_id']}"}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
