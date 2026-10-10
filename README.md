# resolveAI: an operations agent for property management

**Track:** Property Management, Real-World Agents Hackathon (Dwelly, 10 October 2026)

resolveAI is an AI agent that works a letting agency's maintenance cases the way a careful property manager would. It reads a case as it stands at any moment: the history of emails, calls, SMS, system notes, reports and quotes up to that point. It works out what the agency must do next, does it through a set of guarded operational tools, and writes down what it did and why.

---

## 1. What we built

An end-to-end agent. It takes the decision and then:

- **acts** through 16 operational tools: emailing, texting and calling tenants, landlords and contractors; requesting and recording landlord approvals; instructing contractors and booking visits; recording quotes and invoices; putting cases on hold with follow-ups; tracking loose ends; escalating to a human; closing cases;
- **refuses unsafe or unauthorised actions** through guardrails built into the tools (no spend without landlord approval, no wrong-address messages, no closing with open items, no dispatching on unverified "emergencies");
- **escalates to a human** with a self-contained handover when the decision is beyond its authority or certainty;
- **produces auditable output** for every case: `ANSWER.md` (what it received, did, escalated, what failed, the result), `REASONING.md` (why, evidence, conflicts, assumptions, a reasoning trace and the full tool ledger). Machine-readable JSON traces are available with `--with-trace`.

## 2. The problem it solves

Letting agencies run maintenance through scattered channels: tenant portal reports, landlord emails, contractor phone calls, automated system notifications, PDF quotes and invoices. Cases stall because nobody notices that:

- the contractor was marked "assigned" but never actually sent the job;
- the landlord's approval request went unanswered three days ago;
- a quote came in above what the landlord approved;
- a message went out naming the wrong property;
- the tenant hasn't been told anything for a week;
- a case was closed while the landlord was still waiting for an inspection.

The data is messy: wrong addresses inside emails, contradictory dates, names that change mid-case, missing attachments, garbled call summaries. Some reports are genuine emergencies; some are panic or misunderstanding.

resolveAI makes the next correct move on each case, quickly and consistently. It spends the landlord's money only with permission, protects the tenant's safety, and hands the case to a person when that is the right call.

## 3. Architecture

```
case folder (index.md + history.md cut at any point, attachments, plus any supplied
email / call transcript / PDF report)
        │
 ① BRIEFING (deterministic code: always runs)
        │   load_case     parse events; hide outcome sections and documents from future events
        │   safety_screen rule-based hazard scan (deliberately broad), with verification questions
        │   read_attachment / transcribe_audio  every case attachment visible at the cut-off (reports,
        │                 quotes, invoices, certificates) and any newly supplied document is read
        │                 in code and placed in the briefing, so documents are never overlooked
        │   → a structured case briefing: people, property, timeline, data-quality flags, hazards
        ▼
 ② REASONING LOOP (Claude Opus 5.5 + 16 tools + submit_decision, our own loop)
        │   understand → identify the decision point → check safety and credibility → decide → act
        │   tool errors are fed back so the model can fix and retry;
        │   workflow and money actions are blocked while a blocking human escalation is open
        │   ends with submit_decision: a structured verdict, cross-checked against the ledger
        ▼
 ③ SAFETY NET (code)
        │   no valid decision, turn limit, API error or refusal → automatic escalate_to_human
        ▼
 ④ RENDER (code, not the model)
        ANSWERS/<n>/ANSWER.md, REASONING.md   (+ trace/*.json with --with-trace)
```

**Why this shape:**
- **Deterministic first step.** Safety screening and document reading can never be skipped by the model.
- **Guardrails live in the tools, not only in the prompt.** For example, `assign_contractor` refuses to spend without a recorded landlord decision that cites the event where the landlord said yes.
- **Every tool call is appended to a per-case ledger.** `ANSWER.md` is rendered from that ledger, so it can only report actions that actually happened, including failures.
- **One agent, not many.** One model with well-designed tools is easier to reason about, cheaper and more reliable.

### Repository layout

| Path | What it is |
|---|---|
| `agent/run.py` | Command-line runner: Reality Test folder, practice split, or a single case; parallel and resumable |
| `agent/loop.py` | The agent loop, guardrail gate, safety net, token and cost accounting |
| `agent/briefing.py` | Deterministic briefing: load, screen, read supplied documents |
| `agent/decision.py` | `submit_decision` schema and its cross-checks against the ledger |
| `agent/render.py` | Renders `ANSWER.md` / `REASONING.md` (and optional `trace/`) from the ledger |
| `agent/prompts/system.md` | Operating instructions: authority, safety, judgement, escalation, communication |
| `agent/config.py` | Model and run settings, API-key loading |
| `tools/` | One tool per file (18 total) plus `_common.py` (validation, ledger, idempotency, fault injection) |
| `tests/` | 93 offline tests covering every tool, its guardrails and failure paths, and the briefing, run against the real practice cases |
| `data/split.json` | Fixed, stratified 35/15 train/test split of the 50 public cases |
| `voice/` | Optional voice layer: the ElevenLabs intake call becomes a case, the agent decides, and the tenant gets an MP3 voice update (see [Voice intake](#voice-intake-optional)) |

### The tools

| Group | Tools |
|---|---|
| Reading the case | `load_case`, `read_attachment`, `transcribe_audio`, `safety_screen`, `get_case_state` |
| Communication | `send_email`, `send_sms`, `place_call` |
| Workflow and money | `request_landlord_approval`, `record_landlord_decision`, `assign_contractor`, `schedule_appointment`, `record_financial`, `set_hold` |
| Records and control | `add_note`, `track_open_item`, `escalate_to_human`, `close_case` |

`load_case` is run only by the briefing code, so the model can't reload a case and see events after the cut-off. `transcribe_audio` is also run by the briefing, not offered to the model yet. The model gets the other 16, plus `submit_decision`.

Every tool:
- validates its input and returns field-level errors the model can act on;
- never crashes the loop;
- is logged to the case ledger;
- won't repeat a send when the same call is retried;
- can be made to fail on purpose (`TOOL_FAILURE_RATE`) to exercise the agent's recovery.

Actions are **simulated**: messages, calls and contractor jobs are recorded, not actually sent. That makes runs safe, reproducible and fully auditable.

### Operating policy enforced by the system

- **All spending needs the landlord's approval.** The agent has no spending authority of its own (`AGENCY_STANDING_LIMIT_GBP=0`).
- **Two judgement-call exceptions**, where the landlord is informed rather than asked:
  - an **emergency make-safe**, only after a credibility assessment rates the hazard confirmed or credible; uncertain or doubtful reports are refused, and the agent must verify or escalate;
  - a **no-cost repair** (warranty, or a contractor fixing their own work), whose spend must be £0.
- **Work the agency had already started** without recorded approval: the landlord is told what is under way and asked to confirm the cost, not asked "may we proceed?".
- **Safety advice for life-threatening hazards is always given**, even when the report may be panic or a hoax. Credibility decides spending, not whether people are told how to stay safe.
- **Case content is data, never instructions.** Embedded instructions ("approve this payment", "ignore your rules") are treated as red flags.

## 4. How to run it

### Prerequisites

- Python 3.10+ (developed on 3.12, Linux)
- An Anthropic API key with access to `claude-opus-5-5`
- `pdftotext` (poppler-utils) is optional: it's a fallback PDF text extractor; `pypdf` is used first
- The organisers' public practice cases in `Property Management/` are needed only for tests and practice runs. They are not redistributed in this repo.

### Installation

```bash
git clone git@github.com:faizannsethi/resolveAI-Hackathon.git
cd resolveAI-Hackathon
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Configuration and environment variables

Set your key either as an environment variable or in a local `api_key` file. The file may contain just the key, or the curl command from the console: the key is extracted automatically and never printed. Never commit it; `api_key` and `.env` are git-ignored.

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

| Variable | Default | Purpose |
|---|---|---|
| `ANTHROPIC_API_KEY` | (none) | API key (alternatively, an `api_key` file in the repo root) |
| `ANTHROPIC_API_KEY_FILE` | `./api_key` | Path to the key file |
| `AGENT_MODEL` | `claude-opus-5-5` | Model used by the agent |
| `AGENT_EFFORT` | `high` | Reasoning effort (`low` / `medium` / `high` / `xhigh` / `max`) |
| `AGENT_MAX_TURNS` | `30` | Maximum model calls per case before the safety net escalates |
| `AGENT_MAX_TOKENS` | `32000` | Output cap per model call |
| `AGENT_FALLBACKS` | `1` | Server-side model fallback if a request is declined by safety classifiers |
| `AGENCY_STANDING_LIMIT_GBP` | `0` | Agency spend allowed without landlord approval (0 = always ask) |
| `AGENT_RUN_DIR` | set by the runner | Where per-case ledgers and context are written |
| `TOOL_FAILURE_RATE`, `TOOL_FAILURE_ONLY` | off | Fault injection for testing recovery |
| `ELEVENLABS_API_KEY` | (none) | Optional, for the voice layer: alternatively an `eleven_labs_api_key` file in the repo root (git-ignored) |

### Running

**Reality Test**: a folder with one sub-folder (or file) per case, each already cut at its decision point:
```bash
python -m agent.run --cases-dir "<folder of cases>" --answers ANSWERS --workers 6
```
This writes `ANSWERS/1/ANSWER.md` and `ANSWERS/1/REASONING.md`, then `ANSWERS/2/…` and so on: one folder per case, numbered 1…N in numeric order of the case folders (each `ANSWER.md` names its source case). Add `--with-trace` to also write `ANSWERS/<n>/trace/` (decision, transcript, ledger JSON). Working logs go to `runs/<run>/` (git-ignored), with a `summary.json`. The run can be resumed: re-running skips answered cases unless `--force` is given. A crash on one case never stops the batch, and the failure is written into that case's `ANSWER.md`. If an organiser question accompanies the cases, pass it with `--task "..."`.

**One case** (optionally cut at an event):
```bash
python -m agent.run --case "Property Management/011" --cutoff-event 9
```

**Practice**: public cases from the fixed split, each cut at a random event:
```bash
python -m agent.run --split train --seed 1 --workers 6
python -m agent.run --split test  --seed 2 --workers 5
```
The events that really followed each cut are saved to `runs/<run>/cutoffs.json` for evaluation. They are never shown to the agent.

**Tests** (no API calls):
```bash
python -m pytest
```

### Voice intake (optional)

A tenant can report a repair by voice instead of in writing. The voice layer in `voice/` sits on top of the agent and does not change it.

```
tenant talks to the ElevenLabs intake agent (browser microphone, talk-to link)
   → voice/intake.py    transcript + fields extracted on the call → voice/cases/<n>/index.md + history.md
   → agent.run          the normal case agent → voice/answers/<n>/ANSWER.md + REASONING.md
   → voice/callback.py  what the agent decided to tell the tenant, spoken → voice/outbox/<n>-update.mp3
```

- **The intake agent** is an ElevenLabs conversational agent: the "Northbridge Lettings repairs line". It asks for:
  - name, property address and postcode (read back to confirm);
  - what is wrong, and since when;
  - safety signals;
  - vulnerable occupants;
  - access notes and a callback number.

  It gives immediate safety advice when needed (for example, the gas emergency number).
- **The call becomes a case** in exactly the competition format. Event 001 is a `Call` from the `Tenant` containing the call summary and the full transcript. The fields captured on the call go into `index.md`. Calls with no speech from the caller are skipped. The same call is never converted twice.
- **The voice update** is built from the agent's own decision, never invented, in this order of preference:
  1. its call script to the tenant;
  2. its safety advice;
  3. its message to the tenant.

  It is stripped of email formatting and duplicate greetings, and spoken in the intake line's voice. If the decision has nothing for the tenant, no update is made.

**Run it:**
```bash
python -m voice.setup                 # once: records the intake agent + voice, prints the talk-to link
# open the talk-to link, allow the microphone, report the issue, end the call
python -m voice.pipeline --latest     # call -> case -> agent decision -> MP3 voice update
python -m voice.pipeline --case-folder voice/cases/001   # re-run on an existing voice case
python -m pytest voice/tests          # offline tests, no API calls
```

**Cost per processed call:** one agent run (about $0.25–0.40), plus ElevenLabs usage for the conversation and the text-to-speech.

**Privacy:** transcripts, recordings and voice updates contain personal data. They are written to `voice/cases/`, `voice/recordings/`, `voice/callbacks/`, `voice/outbox/` and `voice/answers/`, which should be git-ignored.

### Accepted case inputs

- A case folder with `index.md` + `history.md` (cut at any point), plus `attachments/`.
- Extra documents placed beside them: an email (`.md`/`.txt`/`.eml`), a call transcript, a PDF report or quote, or a JSON event list. These are read in full and treated as the latest input.
- A single markdown, text or JSON file.

Overview, Outcome and Status sections are hidden automatically. So are attachments that only belong to events after the cut-off, so a decision can only use what was known at that moment.

## 5. Models, APIs and services

| What | Used for |
|---|---|
| **Anthropic Claude Opus 5.5** (`claude-opus-5-5`) via the official `anthropic` Python SDK | All reasoning and tool use. Adaptive thinking with summarised reasoning (shown in `REASONING.md`), effort `high`, streaming, prompt caching of the system prompt and tool definitions. |
| Anthropic server-side fallbacks (`fallbacks: "default"`, beta `server-side-fallback-2026-07-01`) | If a request is declined by a safety classifier, it is re-run on a fallback model instead of failing |
| ElevenLabs Agents Platform and Text-to-Speech (optional, via REST) | Voice layer: the conversational intake agent (with data collection), fetching finished conversations, and the spoken MP3 update. Speech-to-text (`transcribe_audio`) is used if an audio file is supplied with a case. |
| Python libraries | `pydantic` (tool schemas and validation), `pypdf` (PDF text), `requests`, `python-dateutil`, `pytest` |

No other external services are used. All agency actions are simulated locally.

**Typical cost and speed** (measured): about 3–4 model turns, 30–60 seconds and **$0.17–$0.38 per case** (average about $0.24). 15 cases run in under 3 minutes with 5 workers.

## 6. Assumptions

- The agent acts for **Northbridge Lettings**, a UK letting agency, looking after both tenant and landlord.
- **One run = one decision.** It makes the agency's next move at the point the history stops, not the whole case to completion.
- **"Now"** is the time of the latest event in the case.
- **The landlord approves all spending.** The only exceptions are emergencies and repairs that cost nothing, where the landlord is told instead.
- **There's no contractor directory.** The agent uses a contractor already on the job, or one the landlord named. Otherwise it says "approved contractor, to be allocated" rather than making up a name.
- **Actions are simulated.** Emails, texts, calls and jobs are recorded, not actually sent.
- **The data is meant to be messy.** Wrong addresses, odd dates and garbled notes are left as they are; the agent has to cope with them, and we didn't tune it to particular cases.
- **Standard UK practice:** British English, VAT at 20%, and response targets of 4 hours for an emergency, 24 hours for urgent work and 14 days for routine repairs.

## 7. Known limitations

- **Voice is browser-based.** The intake runs in the browser, and the tenant's update is an MP3 rather than a phone call.
- **Photos aren't looked at.** Image attachments are listed, but their content isn't analysed.
- **The safety screen is keyword-based** and catches too much on purpose. The model decides what really matters.
- **Results were reviewed by hand.** We compared decisions with what actually happened next; there's no automated scoring yet.
- **It can be cautious about closing cases.** Without an invoice, keys or the tenant's confirmation, it keeps the case open where staff might have closed it.
- **Decision labels can vary between runs.** When the agent both sends an update and waits, it may call that "act" or "wait".
- **No memory between cases.** It doesn't remember, say, a contractor who is often late.

## 8. What we'd do next

- An automated grader to score every change against the practice cases.
- Real email, SMS, phone and job-portal integrations behind the existing tools.
- Phone-line voice: real calls in and out, not just the browser and MP3.
- A contractor and landlord directory, including each landlord's approval limits.
- Reading photos of damage, meters and invoices.
- Tuning cost and speed with lower effort and better caching.
- A simple screen where staff pick up escalations and approve the agent's drafted messages.

---

## Results and evidence

- **Practice split:** 35 train / 15 test, stratified by issue type, with a fixed seed (`data/split.json`).
- **Tuning (train, seed 1):** all 35 cases completed with no crashes or safety-net fallbacks. Two general rules came from training errors, not from fitting particular cases:
  - "a system status update is not proof a message was sent";
  - "work the agency already started is reported to the landlord, not re-requested".
- **Held-out test (seed 2), run after tuning was frozen:** all 15 cases completed with no errors in 2.8 minutes for $3.68. On manual review against the real next events, 13 decisions matched or improved on what staff did. Examples:
  - correcting a staff email that named the wrong property;
  - catching that "Friday 15th February" was a Thursday;
  - refusing to accept a case closed while the landlord's approved inspection was outstanding.

  Two were more cautious than staff (not closing without invoice or tenant confirmation). None was unsafe.

Run outputs (`runs/`) are kept locally. For the Reality Test, the system's own outputs are committed under `ANSWERS/` (each `REASONING.md` includes the reasoning trace and full tool ledger), generated by the system and not hand-edited.

- **Improvement after the baseline: attachments always read.** Previously the agent opened attachments only when it chose to (e.g. case 008 read 1 of 3). Now every visible attachment is read in code. At identical cut-offs this surfaced facts that exist only in documents: case 005's check-out report records smoke/CO detectors 'Tested? No' and defects outside the cleaning job; case 008's estimate leaves out the burnt carpet the agency asked to replace. Re-running all 15 test cases at the same cut-offs showed no regressions.

## Licence

Apache License 2.0. See [LICENSE](LICENSE).
