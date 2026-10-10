"""End to end: voice intake call -> case files -> the unchanged case agent -> MP3 voice update.

    python -m voice.pipeline --latest                     # newest finished intake call
    python -m voice.pipeline --case-folder voice/cases/001

Each run costs one case-agent run (Claude) plus a little ElevenLabs text-to-speech.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Optional

from voice.callback import voice_update
from voice.config import PROJECT_ROOT, VOICE_DIR
from voice.intake import intake


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Voice intake -> agent decision -> tenant voice update.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--latest", action="store_true")
    group.add_argument("--conversation-id")
    group.add_argument("--case-folder", help="Skip intake and use an existing voice/cases/<n> folder.")
    parser.add_argument("--no-voice-update", action="store_true", help="Stop after the agent's decision.")
    args = parser.parse_args(argv)

    folder = Path(args.case_folder) if args.case_folder else intake(args.conversation_id)
    print(f"[voice] case folder: {folder}")
    run_name = f"voice-{folder.name}"
    answers = VOICE_DIR / "answers"
    cmd = [sys.executable, "-m", "agent.run", "--case", str(folder), "--run-name", run_name,
           "--answers", str(answers), "--force"]
    print(f"[voice] running the case agent: {' '.join(cmd[1:])}")
    done = subprocess.run(cmd, cwd=PROJECT_ROOT)
    if done.returncode != 0:
        print("[voice] the case agent failed; no voice update made")
        return done.returncode
    print(f"[voice] decision written to {answers / str(int(folder.name))}/ANSWER.md")
    if args.no_voice_update:
        return 0
    record = voice_update(PROJECT_ROOT / "runs" / run_name, folder)
    print("[voice] voice update:", json.dumps({k: record.get(k) for k in ("mode", "update_source", "audio_file", "reason")},
                                              ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
