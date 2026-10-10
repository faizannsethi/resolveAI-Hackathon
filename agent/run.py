"""Command-line runner.

Reality Test (cases already cut by the organisers; one answer folder per case):
    python -m agent.run --cases-dir "<folder with case sub-folders>" --answers ANSWERS --workers 6

Practice on the public cases, each cut at a random point (train/test split in data/split.json):
    python -m agent.run --split train --seed 1 --workers 6
    python -m agent.run --split test --seed 1 --workers 6

Single case (optionally cut at an event):
    python -m agent.run --case "Property Management/011" --cutoff-event 9
"""

from __future__ import annotations

import argparse
import json
import os
import random
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from agent.config import PROJECT_ROOT, AgentConfig

PRACTICE_DIR = PROJECT_ROOT / "Property Management"
_print_lock = threading.Lock()


def log(message: str) -> None:
    with _print_lock:
        print(message, flush=True)


def answer_folder_name(case_path: Path) -> str:
    name = case_path.stem if case_path.is_file() else case_path.name
    return str(int(name)) if name.isdigit() else re.sub(r"[^A-Za-z0-9._-]+", "-", name).strip("-")


def discover_cases(cases_dir: Path) -> list[Path]:
    """Each sub-folder is a case; loose files at the top level are cases too."""
    found = [p for p in sorted(cases_dir.iterdir()) if p.is_dir() and not p.name.startswith(".")]
    found += [p for p in sorted(cases_dir.iterdir())
              if p.is_file() and p.suffix.lower() in {".md", ".json", ".txt"} and not p.name.startswith(".")]
    return found


def practice_jobs(split: str, seed: int, limit: int | None) -> list[dict]:
    from tools.load_case import _parse_events

    cases = json.loads((PROJECT_ROOT / "data" / "split.json").read_text())[split]
    jobs = []
    for number in cases[:limit] if limit else cases:
        folder = PRACTICE_DIR / number
        events = _parse_events((folder / "history.md").read_text(encoding="utf-8"), 4000, "history.md")
        rng = random.Random(f"{seed}-{number}")
        cutoff = rng.randint(1, len(events) - 1)  # at least one visible event and one hidden "next" event
        jobs.append({
            "case_path": folder, "answer_name": number, "cutoff_event": cutoff,
            # Kept for evaluation only; never shown to the agent.
            "ground_truth_next_events": [
                {k: e[k] for k in ("id", "timestamp", "channel", "from", "to", "body")}
                for e in events[cutoff: cutoff + 6]
            ],
        })
    return jobs


def run_one(job: dict, answers_root: Path, config: AgentConfig, force: bool) -> dict:
    from agent.loop import run_case
    from agent.render import render_answer

    answer_dir = answers_root / job["answer_name"]
    if (answer_dir / "ANSWER.md").exists() and not force:
        log(f"[{job['answer_name']}] already answered; skipping (use --force to redo)")
        return {"answer_name": job["answer_name"], "skipped": True}
    try:
        result = run_case(str(job["case_path"]), cutoff_event=job.get("cutoff_event"),
                          case_id=job.get("case_id"), task=job.get("task"), config=config, log=log)
        render_answer(result["meta"]["case_id"], result, answer_dir)
        return {"answer_name": job["answer_name"], "case_id": result["meta"]["case_id"],
                "decision": result["decision"].get("decision"), "escalated": result["decision"].get("escalated"),
                "end_reason": result["meta"]["end_reason"], "cost_usd": result["meta"]["cost_usd"],
                "duration_s": result["meta"]["duration_s"], "cutoff_event": job.get("cutoff_event")}
    except Exception as exc:  # noqa: BLE001 - one bad case must not stop the batch
        log(f"[{job['answer_name']}] CRASHED: {type(exc).__name__}: {exc}")
        answer_dir.mkdir(parents=True, exist_ok=True)
        (answer_dir / "ANSWER.md").write_text(
            f"# Case {job['answer_name']}\n\nThe system failed on this case: `{type(exc).__name__}: {exc}`.\n"
            "No automated decision was produced; this case needs a human.\n", encoding="utf-8")
        return {"answer_name": job["answer_name"], "error": f"{type(exc).__name__}: {exc}"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the property-management agent.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--case", help="One case folder or file.")
    source.add_argument("--cases-dir", help="Folder of cases (Reality Test).")
    source.add_argument("--split", choices=["train", "test"], help="Practice cases from data/split.json, randomly cut.")
    parser.add_argument("--cutoff-event", type=int, help="With --case: cut the history after this event.")
    parser.add_argument("--task", help="Optional question/instruction supplied with the case(s).")
    parser.add_argument("--seed", type=int, default=1, help="Random cut-off seed for --split.")
    parser.add_argument("--limit", type=int, help="Only the first N practice cases.")
    parser.add_argument("--run-name", help="Name for runs/<name> (ledgers, transcripts).")
    parser.add_argument("--answers", help="Where to write ANSWERS/<n>/ (default depends on mode).")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--force", action="store_true", help="Redo cases that already have an answer.")
    args = parser.parse_args(argv)

    stamp = time.strftime("%Y%m%d-%H%M%S")
    if args.split:
        run_name = args.run_name or f"{args.split}-seed{args.seed}"
        jobs = practice_jobs(args.split, args.seed, args.limit)
        answers_root = Path(args.answers) if args.answers else PROJECT_ROOT / "runs" / run_name / "answers"
    elif args.cases_dir:
        run_name = args.run_name or f"reality-{stamp}"
        cases = discover_cases(Path(args.cases_dir))
        jobs = [{"case_path": c, "answer_name": answer_folder_name(c), "task": args.task} for c in cases]
        answers_root = Path(args.answers) if args.answers else PROJECT_ROOT / "ANSWERS"
    else:
        run_name = args.run_name or f"single-{stamp}"
        case_path = Path(args.case)
        jobs = [{"case_path": case_path, "answer_name": answer_folder_name(case_path),
                 "cutoff_event": args.cutoff_event, "task": args.task}]
        answers_root = Path(args.answers) if args.answers else PROJECT_ROOT / "runs" / run_name / "answers"

    run_root = PROJECT_ROOT / "runs" / run_name
    run_root.mkdir(parents=True, exist_ok=True)
    os.environ["AGENT_RUN_DIR"] = str(run_root / "cases")
    if args.split:
        (run_root / "cutoffs.json").write_text(json.dumps(
            [{k: (str(v) if isinstance(v, Path) else v) for k, v in j.items()} for j in jobs], indent=2))

    config = AgentConfig()
    log(f"Running {len(jobs)} case(s) | model {config.model} effort {config.effort} | workers {args.workers}")
    log(f"Run folder: {run_root} | answers: {answers_root}")
    started = time.time()
    results = []
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        futures = [pool.submit(run_one, job, answers_root, config, args.force) for job in jobs]
        for future in as_completed(futures):
            results.append(future.result())

    results.sort(key=lambda r: r["answer_name"])
    summary = {
        "run_name": run_name, "cases": len(jobs), "duration_s": round(time.time() - started, 1),
        "total_cost_usd": round(sum(r.get("cost_usd") or 0 for r in results), 4),
        "decisions": {d: sum(1 for r in results if r.get("decision") == d)
                      for d in sorted({r.get("decision") for r in results if r.get("decision")})},
        "safety_net_or_errors": [r["answer_name"] for r in results
                                 if r.get("error") or (r.get("end_reason") not in (None, "submitted") and not r.get("skipped"))],
        "results": results,
    }
    (run_root / "summary.json").write_text(json.dumps(summary, indent=2))
    log(json.dumps({k: v for k, v in summary.items() if k != "results"}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
