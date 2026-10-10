"""safety_screen - deterministic hazard and escalation screen over text or a whole case.

A rule-based safety net that runs alongside the model's own judgement. It deliberately
over-flags (high recall): matches can be false positives - a question in an intake form, a
staff note, an old event - and the agent must judge each in context. It is not tuned to
specific cases. Its job is to make sure an obvious phrase like "smell of gas" is never
missed because a request was classified ROUTINE upstream.
Matches carry the event they came from, so stale hazards in old events can be told apart
from live ones.
"""

from __future__ import annotations

import json
import re
from typing import Literal, Optional

from pydantic import Field, model_validator

from tools._common import CASE_ID_PATTERN, Tool, ToolFailure, ToolInput, run_dir

Level = Literal["emergency", "urgent", "routine"]
LEVEL_RANK = {"routine": 0, "urgent": 1, "emergency": 2}

# (category, level, patterns, immediate advice)
RULES: list[tuple[str, Level, list[str], str]] = [
    ("gas_leak", "emergency",
     [r"smell(?:s|ing)?\s+(?:of\s+)?gas", r"gas\s+(?:leak|smell|escape)", r"leaking\s+gas", r"hiss\w*[^.]{0,30}gas"],
     "Leave the property, do not use switches or flames, open windows, call the National Gas Emergency line 0800 111 999."),
    ("carbon_monoxide", "emergency",
     [r"carbon\s+monoxide", r"\bCO\b\s+(?:alarm|detector)", r"(?:co|carbon)\s+alarm\s+(?:going off|sounding|beeping)"],
     "Get everyone outside into fresh air, call 0800 111 999, seek medical help if anyone feels unwell."),
    ("fire_smoke", "emergency",
     [r"\bon fire\b", r"\bfire\b(?!\s*(?:door|alarm test|safety check|extinguisher service))", r"smoke\s+(?:coming|pouring|from)",
      r"burning\s+smell|smell\s+of\s+burning", r"\bscorch(?:ed|ing)\b", r"smoke\s+alarm\s+(?:going off|sounding)"],
     "If there is fire or smoke, get out and call 999."),
    ("electrical_danger", "emergency",
     [r"exposed\s+wir", r"\bspark(?:s|ing)\b", r"electric(?:al)?\s+shock", r"water\s+(?:in|into|near|through)\s+(?:the\s+)?(?:socket|light|fuse|consumer unit|electrics)",
      r"(?:socket|plug|switch)\s+(?:is\s+)?(?:burnt|burning|melted|smoking)"],
     "Do not touch it; switch off at the consumer unit only if safe to do so; keep away from water near electrics."),
    ("major_water_leak", "emergency",
     [r"\bflood(?:ing|ed)?\b", r"burst\s+pipe", r"water\s+(?:is\s+)?(?:pouring|gushing|flowing|coming)\s+(?:in|through|out|from)",
      r"ceiling\s+(?:is\s+)?(?:collaps|bulg|sagging|caving)", r"leak\w*\s+through\s+(?:the\s+)?ceiling", r"can'?t\s+stop\s+the\s+(?:water|leak)"],
     "Turn off the water at the stopcock, move valuables and keep away from electrics near the water."),
    ("structural", "emergency",
     [r"(?:ceiling|wall|roof|balcony|stair\w*)\s+(?:has\s+)?(?:collapsed|fell|fallen|falling)", r"falling\s+(?:masonry|brick|plaster)",
      r"(?:crack|cracks)\s+(?:is\s+|are\s+)?(?:widening|getting bigger)"],
     "Keep everyone away from the affected area."),
    ("injury_or_health", "emergency",
     [r"\binjur(?:ed|y|ies)\b", r"\bbleeding\b", r"can'?t\s+breathe", r"\bunconscious\b", r"\bambulance\b", r"made\s+(?:me|us|him|her|them)\s+(?:ill|sick|unwell)"],
     "If anyone is hurt or unwell, call 999 or NHS 111."),
    ("sewage", "urgent",
     [r"\bsewage\b", r"toilet\s+(?:is\s+)?overflow", r"waste\s+water\s+(?:coming|backing)\s+up"],
     "Avoid contact with the waste water and keep children and pets away."),
    ("no_heating_or_hot_water", "urgent",
     [r"no\s+(?:heating|heat|hot\s+water)", r"boiler\s+(?:is\s+)?(?:not working|broken|broke|leaking|keeps\s+\w+|lost\s+pressure|won'?t)",
      r"radiators?\s+(?:are\s+|is\s+)?(?:cold|not\s+(?:working|heating))", r"heating\s+(?:is\s+)?(?:not working|broken|off)"],
     "Check the boiler pressure and thermostat; use safe temporary heaters if available."),
    ("no_water_or_power", "urgent",
     [r"no\s+(?:running\s+)?water\b", r"no\s+(?:electricity|power)", r"power\s+cut", r"(?:electricity|power)\s+(?:has\s+)?gone\s+off"],
     "Check whether neighbours are affected (possible supplier outage) and the consumer unit."),
    ("security", "urgent",
     [r"(?:can'?t|cannot|can\s+not|won'?t|unable\s+to)\s+(?:be\s+)?lock", r"not\s+(?:turning\s*/\s*)?locking", r"(?:break|broke)[- ]in", r"\bburglar",
      r"locked\s+out", r"(?:front|back|entrance|main)\s+door\s+(?:won'?t|will\s+not|doesn'?t|does\s+not)\s+(?:lock|shut|close)",
      r"(?:smashed|broken)\s+(?:window|door|glass)"],
     "The property may not be secure: arrange a make-safe (boarding / lock change) promptly."),
    ("glass_hazard", "urgent",
     [r"\bshatter", r"broken\s+glass", r"cracked\s+(?:glass|pane)"],
     "Keep clear of broken or loose glass."),
    ("damp_mould", "urgent",
     [r"\bmou?ld\b", r"\bdamp\b(?!\s+(?:paint|proof\w*\s+paint))", r"condensation"],
     "Damp and mould are health hazards; investigate promptly, especially with vulnerable occupants."),
    ("pests", "urgent",
     [r"\brats?\b", r"\bmice\b", r"cockroach", r"bed\s*bugs?", r"wasps?'?\s+nest"],
     "Avoid contact and store food sealed until pest control attends."),
    ("asbestos", "urgent", [r"asbestos"], "Do not disturb the material."),
]

ESCALATION_RULES: list[tuple[str, list[str]]] = [
    ("vulnerable_occupant",
     [r"\bbaby\b", r"\binfant\b", r"newborn", r"pregnan", r"\belderly\b", r"\bdisabl", r"wheelchair", r"\basthma",
      r"oxygen", r"dialysis", r"mental\s+health", r"\bcarer\b", r"\bvulnerable\b", r"terminal(?:ly)?\s+ill", r"chemotherapy"]),
    ("legal_or_complaint",
     [r"solicitor", r"legal\s+action", r"\bcourt\b", r"ombudsman", r"environmental\s+health", r"formal\s+complaint", r"\bsue\b",
      r"section\s+(?:21|8)\b", r"\beviction\b", r"harass", r"discriminat", r"deposit\s+dispute", r"trading\s+standards"]),
    ("tenant_distress",
     [r"\bdesperate\b", r"\bunbearable\b", r"\bfurious\b", r"\bdisgusted\b", r"\bunacceptable\b", r"(?:weeks|months)\s+(?:now|without)",
      r"still\s+(?:not|no|waiting)", r"nobody\s+(?:has\s+)?(?:come|called|replied)"]),
]

# A negation counts only if it sits within three words of the match ("no smell of gas"),
# so "if this isn't fixed I will contact my solicitor" still flags the solicitor.
NEGATION = re.compile(r"(?:\bno|\bnot|n't|\bnever|\bwithout|\bno\s+sign\s+of)\s+(?:[\w'-]+\s+){0,3}$", re.I)
# Questions that help tell a live hazard from a misunderstanding, exaggeration or hoax.
# Safety advice is given regardless; the answers decide how far and how fast to spend.
VERIFY_QUESTIONS = {
    "gas_leak": ["Is the smell strong and throughout the property or faint near one appliance?",
                 "Have you turned off the gas at the meter and called 0800 111 999? What reference did they give?",
                 "Has the gas network engineer attended or capped the supply?"],
    "carbon_monoxide": ["Is the CO alarm still sounding after airing the room / going outside?",
                        "Does anyone have headaches, dizziness or nausea?", "Which appliance is near the alarm?"],
    "fire_smoke": ["Is there flame or visible smoke right now, or a smell only?", "Have the fire service been called?",
                   "Where exactly is the smell or smoke coming from?"],
    "electrical_danger": ["Can you see exposed wires, scorch marks or sparking right now?",
                          "Has the circuit tripped, and does it trip again when reset?", "Is water near the electrics?"],
    "major_water_leak": ["Is water still flowing after turning off the stopcock?", "How much water and where is it spreading?",
                         "Is water near lights, sockets or the consumer unit?", "Can you send a photo or video?"],
    "structural": ["Has anything actually fallen, or is it cracking/sagging?", "Is the area kept clear?",
                   "Can you send a photo?"],
    "injury_or_health": ["Is anyone hurt right now and have emergency services been called?"],
    "sewage": ["Is sewage inside the home or only outside?", "Is it the only toilet?"],
    "no_heating_or_hot_water": ["Is there no heating at all, or only some radiators?", "What does the boiler display show?",
                                "Is anyone vulnerable (very young, elderly, unwell) in the home?"],
    "no_water_or_power": ["Are neighbours affected too (possible supplier outage)?", "Has the consumer unit tripped?"],
    "security": ["Can the property be secured at all right now (another lock, another door)?",
                 "Is there damage from a break-in, and has it been reported to the police (crime reference)?"],
    "glass_hazard": ["Is glass broken or only cracked, and is it at a height or ground level?", "Can you send a photo?"],
    "damp_mould": ["Where is the mould and how large an area?", "Does anyone with breathing problems live there?",
                   "Can you send photos?"],
    "pests": ["What have you seen, where, and how often?", "Can you send a photo?"],
    "asbestos": ["What material is suspected and has it been disturbed or damaged?"],
}

RESPONSE_TIMES = {"emergency": "make safe within 4 hours (attend immediately if life at risk)",
                  "urgent": "attend within 24 hours", "routine": "attend within 14 days"}


class SafetyScreenInput(ToolInput):
    text: Optional[str] = Field(None, max_length=200_000, description="Text to screen.")
    case_id: Optional[str] = Field(
        None, pattern=CASE_ID_PATTERN, description="Screen every visible event of a loaded case."
    )
    only_events_after: Optional[str] = Field(
        None, description="With case_id: ignore events at or before this event id (e.g. 'event-010')."
    )

    @model_validator(mode="after")
    def _source(self) -> "SafetyScreenInput":
        if not self.text and not self.case_id:
            raise ValueError("provide text and/or case_id")
        return self


def _scan(text: str, source: str, timestamp: Optional[str], sender: Optional[str]) -> list[dict]:
    hits = []
    for category, level, patterns, advice in RULES:
        for pattern in patterns:
            for m in re.finditer(pattern, text, re.I):
                negated = bool(NEGATION.search(text[max(0, m.start() - 40): m.start()]))
                hits.append({"category": category, "level": level, "phrase": m.group(0), "negated": negated,
                             "source": source, "timestamp": timestamp, "from": sender, "advice": advice})
    for flag, patterns in ESCALATION_RULES:
        for pattern in patterns:
            for m in re.finditer(pattern, text, re.I):
                negated = bool(NEGATION.search(text[max(0, m.start() - 40): m.start()]))
                hits.append({"category": flag, "level": "flag", "phrase": m.group(0), "negated": negated,
                             "source": source, "timestamp": timestamp, "from": sender, "advice": None})
    return hits


def _handle(params: SafetyScreenInput) -> tuple[dict, list[str]]:
    warnings: list[str] = []
    hits: list[dict] = []
    if params.text:
        hits += _scan(params.text, "text", None, None)
    if params.case_id:
        events_file = run_dir() / params.case_id / "events.json"
        if not events_file.exists():
            raise ToolFailure("case_not_loaded", f"Case {params.case_id!r} not loaded. Call load_case first.")
        events = json.loads(events_file.read_text(encoding="utf-8"))
        if params.only_events_after:
            from tools._common import normalise_event_ref

            after = int(normalise_event_ref(params.only_events_after).split("-")[1])
            events = [e for e in events if e["n"] > after]
        for e in events:
            hits += _scan(e["body"], e["id"], e.get("timestamp"), e.get("from"))

    live = [h for h in hits if not h["negated"]]
    hazards = [h for h in live if h["level"] != "flag"]
    flags = sorted({h["category"] for h in live if h["level"] == "flag"})
    level = max((h["level"] for h in hazards), key=LEVEL_RANK.get, default="routine")

    escalated_by_vulnerability = False
    if "vulnerable_occupant" in flags and level == "urgent" and any(
        h["category"] in {"no_heating_or_hot_water", "damp_mould", "no_water_or_power", "security"} for h in hazards
    ):
        level = "emergency"
        escalated_by_vulnerability = True
        warnings.append("Urgent hazard combined with a vulnerable occupant: treated as emergency.")

    categories: dict[str, dict] = {}
    for h in hazards:
        entry = categories.setdefault(h["category"], {"level": h["level"], "advice": h["advice"], "evidence": [],
                                                      "verify_by_asking": VERIFY_QUESTIONS.get(h["category"], [])})
        entry["evidence"].append({k: h[k] for k in ("source", "timestamp", "from", "phrase")})

    if any(h["negated"] for h in hits):
        warnings.append("Some matches were negated (e.g. 'no smell of gas') and were ignored; see negated_matches.")
    if params.case_id and hazards:
        warnings.append("Matches may come from old events; check timestamps to decide if the hazard is still live.")

    return {
        "level": level,
        "recommended_response": RESPONSE_TIMES[level],
        "hazards": categories,
        "escalation_flags": flags,
        "escalated_by_vulnerability": escalated_by_vulnerability,
        "requires_human_review": level == "emergency" or "legal_or_complaint" in flags,
        "negated_matches": [{k: h[k] for k in ("category", "phrase", "source")} for h in hits if h["negated"]],
        "note": ("Rule-based screen; it does not judge credibility. Always give the safety advice for "
                 "life-threatening hazards, then verify (verify_by_asking, photos, call) before committing spend."),
    }, warnings


TOOL = Tool(
    name="safety_screen",
    description="""
Deterministic hazard screen. Pass free text and/or a loaded case_id. It flags gas, carbon
monoxide, fire, electrical danger, major leaks, structural risk, injury, sewage, loss of
heating/water/power, security, glass, damp/mould, pests and asbestos, plus vulnerable
occupants, legal/complaint language and tenant distress. Returns an overall level (emergency,
urgent, routine), target response time, immediate safety advice, and the event each match
came from. Negated phrases ('no smell of gas') are ignored. It over-flags on purpose: a match
may come from an intake question, a staff note or an old, already-resolved event, so check
each match's source and context before acting on it. It does not judge credibility: each
hazard includes verify_by_asking questions to tell a genuine, current hazard from a
misunderstanding, panic or hoax. Always give safety advice for life-threatening hazards, even
when in doubt; use verification to decide on spending. Never dismiss a live hazard reported
by a tenant or contractor without a clear, stated reason.
""",
    input_model=SafetyScreenInput,
    handler=_handle,
    side_effect=False,
)
