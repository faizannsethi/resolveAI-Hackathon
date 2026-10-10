"""Tests for every tool: happy paths, guardrails and failure handling, against the real practice cases."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from tools import TOOLS, call_tool, tool_specs
from tools._common import build_state, clear_injected_failures, inject_failures, read_ledger

ROOT = Path(__file__).resolve().parent.parent
CASES = ROOT / "Property Management"


@pytest.fixture(autouse=True)
def isolated_run(tmp_path, monkeypatch):
    monkeypatch.setenv("AGENT_RUN_DIR", str(tmp_path / "runs"))
    for var in ("AGENT_NOW", "ELEVENLABS_API_KEY", "TOOL_FAILURE_RATE", "AGENCY_STANDING_LIMIT_GBP"):
        monkeypatch.delenv(var, raising=False)
    clear_injected_failures()
    yield
    clear_injected_failures()


def load(case: str, **kw) -> dict:
    result = call_tool("load_case", {"case_path": str(CASES / case), **kw})
    assert result["ok"], result["error"]
    return result["data"]


def ok(result: dict) -> dict:
    assert result["ok"], result["error"]
    return result["data"]


def err(result: dict) -> str:
    assert not result["ok"], f"expected failure, got {result['data']}"
    return result["error"]["code"]


# --------------------------------------------------------------------------- registry & schemas


def test_registry_has_one_tool_per_file():
    files = {p.stem for p in (ROOT / "tools").glob("*.py") if not p.stem.startswith("_")}
    assert files == set(TOOLS)
    for spec in tool_specs():
        schema = json.dumps(spec["input_schema"])
        assert "$ref" not in schema and len(spec["description"]) > 80


def test_unknown_tool_and_invalid_input_are_structured():
    assert err(call_tool("nope")) == "unknown_tool"
    result = call_tool("send_sms", {"case_id": "x", "body": "hi"})
    assert err(result) == "invalid_input"
    assert {d["field"] for d in result["error"]["details"]} >= {"to", "purpose"}
    assert err(call_tool("load_case", {"case_path": str(CASES / "001"), "bogus": 1})) == "invalid_input"


# --------------------------------------------------------------------------- load_case


@pytest.mark.parametrize("case", sorted(p.name for p in CASES.iterdir()))
def test_every_practice_case_loads_without_leaking_outcome(case):
    data = load(case)
    expected = (CASES / case / "history.md").read_text().count('<a id="event-')
    assert data["event_count"]["visible"] == expected
    assert "outcome" not in data["other_sections"] and "overview" not in data["other_sections"]
    assert "status" not in data["details"] and "completed" not in data["details"]
    assert data["property"] and data["initial_request"]
    assert [e["n"] for e in data["events"]] == sorted(e["n"] for e in data["events"])


def test_cutoff_by_event_and_time_sets_now():
    data = load("011", cutoff_event=9)
    assert data["event_count"] == {"visible": 9, "total_in_source": 32, "history_cut": True}
    assert data["now"] == data["events"][-1]["timestamp"]
    assert data["now"].startswith("2026-12-03T11:34")
    by_time = load("011", cutoff_time="2026-12-03T00:00:00Z", case_id="t-011")
    assert by_time["events"][-1]["id"] == "event-007" and by_time["now"] == "2026-12-03T00:00:00Z"


def test_include_outcome_and_data_quality_flags():
    data = load("045", include_outcome=True)
    assert "outcome" in data["other_sections"]
    assert len(data["data_quality"]["other_property_addresses_mentioned"]) >= 5
    assert any("different property" in w for w in call_tool("load_case", {"case_path": str(CASES / "045")})["warnings"])


def test_raw_text_load_and_errors():
    data = ok(call_tool("load_case", {
        "raw_text": "Tenant at Flat 3, 12 Mill Road, Kingshaven, ZZ1 1ZZ says there is a smell of gas.",
        "case_id": "voice-intake-1",
    }))
    assert data["property"] == "Flat 3, 12 Mill Road, Kingshaven, ZZ1 1ZZ"
    assert err(call_tool("load_case", {"raw_text": "something broke"})) == "invalid_input"
    assert err(call_tool("load_case", {"case_path": "does/not/exist"})) == "not_found"


def test_reset_clears_ledger():
    load("011")
    ok(call_tool("add_note", {"case_id": "property-management-011", "category": "general", "text": "first run"}))
    load("011", reset=True)
    assert [e["tool"] for e in read_ledger("property-management-011")] == ["load_case"]


# --------------------------------------------------------------------------- read_attachment


def test_read_pdf_attachment_and_sandbox():
    case_id = load("008")["case_id"]
    data = ok(call_tool("read_attachment", {"case_id": case_id, "path": "attachments/attachment-02-estimate.pdf"}))
    assert "1,370" in data["text"] and data["kind"] == "pdf"
    assert err(call_tool("read_attachment", {"case_id": case_id, "path": "../../README.md"})) == "path_outside_case"
    missing = call_tool("read_attachment", {"case_id": case_id, "path": "attachments/nope.pdf"})
    assert err(missing) == "not_found" and missing["error"]["details"]["available"]


def test_future_attachments_are_hidden_before_cutoff():
    early = load("008", cutoff_event=5)
    assert all("invoice" not in a["path"] for a in early["attachments"])
    result = call_tool("read_attachment", {"case_id": early["case_id"], "path": "attachments/attachment-04-invoice.pdf"})
    assert err(result) == "not_found"
    late = load("008")
    assert any("invoice" in a["path"] for a in late["attachments"])


def test_read_attachment_requires_loaded_case():
    assert err(call_tool("read_attachment", {"case_id": "never-loaded", "path": "x.pdf"})) == "case_not_loaded"


# --------------------------------------------------------------------------- transcribe_audio


@pytest.fixture
def audio_case(tmp_path):
    folder = tmp_path / "Voice Cases" / "001"
    folder.mkdir(parents=True)
    (folder / "call.mp3").write_bytes(b"ID3fake-audio")
    (folder / "history.md").write_text("# Case\n")
    return folder


def test_transcribe_fails_cleanly_with_no_engines(audio_case):
    result = call_tool("transcribe_audio", {"path": str(audio_case / "call.mp3"), "engines": ["elevenlabs", "local_whisper"]})
    assert err(result) == "transcription_failed"
    assert [a["engine"] for a in result["error"]["details"]["attempts"]] == ["elevenlabs", "local_whisper"]


def test_transcribe_falls_back_to_sidecar(audio_case):
    (audio_case / "call.txt").write_text("Hello, there is water coming through the ceiling.")
    result = call_tool("transcribe_audio", {"path": str(audio_case / "call.mp3")})
    data = ok(result)
    assert data["engine"] == "sidecar" and "ceiling" in data["text"]
    assert any("fallback" in w for w in result["warnings"])


def test_transcribe_elevenlabs_diarisation(audio_case, monkeypatch):
    monkeypatch.setenv("ELEVENLABS_API_KEY", "test-key")

    class FakeResponse:
        status_code = 200
        def json(self):
            return {"text": "Hi my boiler is broken (crying)", "language_code": "en", "language_probability": 0.99,
                    "words": [
                        {"text": "Hi", "type": "word", "speaker_id": "speaker_0", "start": 0.0, "end": 0.2},
                        {"text": " ", "type": "spacing", "speaker_id": "speaker_0"},
                        {"text": "my boiler is broken", "type": "word", "speaker_id": "speaker_0", "start": 0.3, "end": 1.2},
                        {"text": "(crying)", "type": "audio_event", "speaker_id": "speaker_0", "start": 1.3},
                        {"text": "Okay", "type": "word", "speaker_id": "speaker_1", "start": 2.0, "end": 2.3},
                    ]}

    monkeypatch.setattr("tools.transcribe_audio.requests.post", lambda *a, **k: FakeResponse())
    data = ok(call_tool("transcribe_audio", {"path": str(audio_case / "call.mp3")}))
    assert data["engine"] == "elevenlabs"
    assert [s["speaker"] for s in data["segments"]] == ["speaker_0", "speaker_1"]
    assert data["audio_events"][0]["label"] == "crying"


def test_transcribe_rejects_non_audio(audio_case):
    assert err(call_tool("transcribe_audio", {"path": str(audio_case / "history.md")})) == "unsupported_type"


# --------------------------------------------------------------------------- safety_screen


@pytest.mark.parametrize("text,level,category", [
    ("I can smell gas in the kitchen", "emergency", "gas_leak"),
    ("Water is pouring through the ceiling onto the lights", "emergency", "major_water_leak"),
    ("The CO alarm keeps going off", "emergency", "carbon_monoxide"),
    ("We have no heating since Monday", "urgent", "no_heating_or_hot_water"),
    ("The front door won't lock", "urgent", "security"),
    ("Dishwasher does not complete its cycle", "routine", None),
])
def test_safety_screen_levels(text, level, category):
    data = ok(call_tool("safety_screen", {"text": text}))
    assert data["level"] == level
    if category:
        assert category in data["hazards"]


def test_safety_screen_negation_and_vulnerability():
    neg = ok(call_tool("safety_screen", {"text": "There is no smell of gas, the oven just won't heat."}))
    assert neg["level"] == "routine" and neg["negated_matches"]
    vuln = ok(call_tool("safety_screen", {"text": "No heating and I have a newborn baby at home."}))
    assert vuln["level"] == "emergency" and vuln["escalated_by_vulnerability"]
    legal = ok(call_tool("safety_screen", {"text": "If this isn't fixed I will contact my solicitor."}))
    assert "legal_or_complaint" in legal["escalation_flags"] and legal["requires_human_review"]


def test_safety_screen_on_case_cites_events():
    case_id = load("023")["case_id"]
    data = ok(call_tool("safety_screen", {"case_id": case_id}))
    assert data["level"] == "urgent" and "security" in data["hazards"]
    assert data["hazards"]["security"]["evidence"][0]["source"].startswith("event-")


# --------------------------------------------------------------------------- communication


def test_send_email_guardrails_and_idempotency():
    case_id = load("011", cutoff_event=9)["case_id"]
    base = {"case_id": case_id, "to": [{"role": "tenant", "name": "Amelia Nolan"}], "subject": "Dishwasher repair",
            "purpose": "status_update"}
    assert err(call_tool("send_email", {**base, "body": "Dear [Tenant Name], we will be in touch."})) == "unfilled_placeholder"
    wrong = call_tool("send_email", {**base, "body": "Update on Flat 5, 25 Harbour View, Cedarford, ZZ3 9ZZ repair."})
    assert err(wrong) == "address_mismatch"
    body = "Hi Amelia, the landlord has approved an engineer for the dishwasher at Flat 12, 78 Copperfield Walk."
    first = ok(call_tool("send_email", {**base, "body": body}))
    again = call_tool("send_email", {**base, "body": body})
    assert again["duplicate"] and again["data"]["id"] == first["id"] == "MSG-001"
    assert len(build_state(case_id)["messages"]) == 1


def test_sms_failure_injection_then_retry():
    case_id = load("011")["case_id"]
    args = {"case_id": case_id, "to": {"role": "tenant", "phone": "07700 900529"},
            "body": "Northbridge Lettings: please check your email about your dishwasher repair.", "purpose": "nudge_check_email"}
    inject_failures("send_sms", 1)
    failed = call_tool("send_sms", args)
    assert err(failed) == "transient_unavailable" and failed["error"]["retryable"]
    assert ok(call_tool("send_sms", args))["id"] == "MSG-001"
    assert [e["ok"] for e in read_ledger(case_id) if e["tool"] == "send_sms"] == [False, True]
    assert build_state(case_id)["failed_calls"][0]["tool"] == "send_sms"


def test_sms_rejects_internal_and_bad_phone():
    case_id = load("011")["case_id"]
    assert err(call_tool("send_sms", {"case_id": case_id, "to": {"role": "agency_internal"}, "body": "hello there",
                                       "purpose": "other"})) == "invalid_recipient"
    assert err(call_tool("send_sms", {"case_id": case_id, "to": {"role": "tenant", "phone": "abc"}, "body": "hello there",
                                       "purpose": "other"})) == "invalid_input"


def test_place_call_without_voice_key_still_logs():
    case_id = load("019")["case_id"]
    result = call_tool("place_call", {"case_id": case_id, "to": {"role": "landlord", "name": "Jenkins"},
                                      "purpose": "obtain_approval", "synthesize_audio": True,
                                      "script": "Hi Jenkins, calling about the garden clearance quote of around £600 at the property."})
    data = ok(result)
    assert data["id"] == "CALL-001" and data["audio_file"] is None
    assert any("Audio not generated" in w for w in result["warnings"])


# --------------------------------------------------------------------------- approvals, jobs, money


def _approve(case_id: str, **kw) -> str:
    return ok(call_tool("record_landlord_decision", {
        "case_id": case_id, "decision": "approved", "scope": "Send engineer to inspect dishwasher",
        "evidence_event": "event-009", **kw}))["id"]


def _assign(case_id: str, decision_id: str, **kw) -> dict:
    args = {"case_id": case_id, "contractor_name": "Oakfield Homes", "trade": "appliance_repair",
            "purpose": "attend_and_repair", "urgency": "routine",
            "job_description": "Dishwasher runs perpetually and never completes its cycle. Diagnose and repair.",
            "authorisation": "landlord_decision", "decision_id": decision_id, "spend_limit_gbp": 150,
            "tenant": {"role": "tenant", "name": "Amelia Nolan", "phone": "07700 900529"},
            "access_notes": "Two guinea pigs at the property.", **kw}
    return call_tool("assign_contractor", args)


def test_landlord_decision_requires_landlord_evidence():
    case_id = load("017")["case_id"]
    result = call_tool("record_landlord_decision", {"case_id": case_id, "decision": "approved",
                                                    "scope": "fix extractor", "evidence_event": "event-007"})
    assert err(result) == "evidence_not_from_landlord"
    assert err(call_tool("record_landlord_decision", {"case_id": case_id, "decision": "approved",
                                                      "scope": "fix extractor", "evidence_event": "event-099"})) == "unknown_event"


def test_assign_contractor_authorisation_rules():
    case_id = load("011", cutoff_event=9)["case_id"]
    assert err(call_tool("assign_contractor", {
        "case_id": case_id, "contractor_name": "X Ltd", "trade": "appliance_repair", "purpose": "attend_and_repair",
        "urgency": "routine", "job_description": "Fix the dishwasher please", "authorisation": "landlord_decision",
        "spend_limit_gbp": 100})) == "invalid_input"
    assert err(_assign(case_id, "DEC-009")) == "unknown_decision"
    standing = _assign(case_id, None, authorisation="agency_standing_authority",
                       authorisation_note="Agency standing authority for small repairs")
    assert err(standing) == "no_standing_authority"

    capped = _approve(case_id, decision="approved_with_limit", spend_limit_gbp=100)
    assert err(_assign(case_id, capped)) == "exceeds_landlord_limit"
    job = ok(_assign(case_id, capped, spend_limit_gbp=100))
    assert job["id"] == "JOB-001" and [m["to"][0]["role"] for m in job["messages"]] == ["contractor", "tenant"]
    assert "£100.00" in job["messages"][0]["body"]
    assert err(_assign(case_id, capped, spend_limit_gbp=90)) == "duplicate_assignment"
    second = ok(_assign(case_id, capped, purpose="quote_only", spend_limit_gbp=0, contractor_name="Willow Services"))
    assert second["id"] == "JOB-002"


def test_assign_blocked_when_landlord_uses_own_contractor():
    case_id = load("028")["case_id"]
    dec = ok(call_tool("record_landlord_decision", {"case_id": case_id, "decision": "landlord_arranging_own_contractor",
                                                    "scope": "Landlord will sort the loose garden pipe", "evidence_event": "event-007"}))["id"]
    result = call_tool("assign_contractor", {
        "case_id": case_id, "contractor_name": "Riverside Works", "trade": "plumbing", "purpose": "attend_and_repair",
        "urgency": "routine", "job_description": "Re-fix loose water pipe in back garden", "authorisation": "landlord_decision",
        "decision_id": dec, "spend_limit_gbp": 100})
    assert err(result) == "not_authorised"


def test_emergency_make_safe_needs_emergency_urgency():
    case_id = load("023")["case_id"]
    args = {"case_id": case_id, "contractor_name": "Juniper Surveying", "trade": "locksmith", "purpose": "emergency_make_safe",
            "urgency": "urgent", "job_description": "Balcony door cannot be locked; make secure",
            "authorisation": "emergency_make_safe", "authorisation_note": "Property cannot be secured overnight",
            "spend_limit_gbp": 150,
            "emergency_assessment": {"hazard": "Balcony door cannot be locked", "credibility": "credible",
                                     "evidence_events": ["event-003", "event-006"],
                                     "corroboration": ["consistent_specific_details", "safety_screen_match"],
                                     "rationale": "Tenant and landlord both describe a lock that will not turn; landlord agrees it needs sorting soon."}}
    assert err(call_tool("assign_contractor", args)) == "invalid_input"  # urgency is not 'emergency'
    no_assessment = {k: v for k, v in args.items() if k != "emergency_assessment"}
    assert err(call_tool("assign_contractor", {**no_assessment, "urgency": "emergency"})) == "invalid_input"
    result = call_tool("assign_contractor", {**args, "urgency": "emergency"})
    job = ok(result)
    assert [m["to"][0]["role"] for m in job["messages"]] == ["contractor", "tenant", "landlord"]
    assert "without waiting for approval" in job["messages"][-1]["body"]
    assert job["emergency_assessment"]["credibility"] == "credible"


@pytest.mark.parametrize("credibility", ["uncertain", "doubtful"])
def test_unverified_emergency_is_not_dispatched(credibility):
    case_id = ok(call_tool("load_case", {
        "raw_text": "OMG the whole flat is about to EXPLODE!!! I think I smelled gas yesterday, maybe, not sure now.",
        "case_id": "panic-report", "property_address": "Flat 3, 12 Mill Road, Kingshaven, ZZ1 1ZZ"}))["case_id"]
    result = call_tool("assign_contractor", {
        "case_id": case_id, "contractor_name": "Gas Safe Engineer Ltd", "trade": "gas_heating",
        "purpose": "emergency_make_safe", "urgency": "emergency", "job_description": "Investigate reported gas smell",
        "authorisation": "emergency_make_safe", "authorisation_note": "Reported smell of gas",
        "spend_limit_gbp": 200,
        "emergency_assessment": {"hazard": "Possible gas smell", "credibility": credibility,
                                 "evidence_events": ["event-001"],
                                 "doubts": ["Smell was yesterday and tenant is unsure", "Exaggerated language"],
                                 "rationale": "Single vague report about a past smell; needs verification by phone first."}})
    assert err(result) == "emergency_not_verified"
    assert "safety advice" in result["error"]["message"]
    assert build_state(case_id)["jobs"] == {}


def test_safety_screen_gives_verification_questions():
    data = ok(call_tool("safety_screen", {"text": "I can smell gas in the hallway"}))
    questions = data["hazards"]["gas_leak"]["verify_by_asking"]
    assert any("0800 111 999" in q for q in questions) and "credibility" in data["note"]


def test_no_cost_route_informs_landlord_and_must_be_free():
    case_id = load("036")["case_id"]
    args = {"case_id": case_id, "contractor_name": "Keystone Services", "trade": "plumbing", "purpose": "warranty_repair",
            "urgency": "routine", "job_description": "Replace faulty bath tap fitted in February",
            "authorisation": "warranty_or_no_cost", "spend_limit_gbp": 0,
            "authorisation_note": "Contractor's own faulty tap, replaced free of charge",
            "landlord": {"role": "landlord", "name": "Sawyer"}}
    job = ok(call_tool("assign_contractor", args))
    fyi = job["messages"][-1]
    assert fyi["to"][0] == {"role": "landlord", "name": "Sawyer"} and "no cost to you" in fyi["body"]
    assert err(call_tool("assign_contractor", {**args, "purpose": "attend_and_repair", "spend_limit_gbp": 50,
                                               "idempotency_key": "chargeable"})) == "invalid_input"


def test_schedule_and_money_checks():
    case_id = load("011", cutoff_event=9)["case_id"]
    job = ok(_assign(case_id, _approve(case_id)))["id"]
    past = call_tool("schedule_appointment", {"case_id": case_id, "job_id": job, "start": "2026-11-01T09:00",
                                              "access": "tenant_present", "confirmed_with": ["tenant"]})
    assert err(past) == "appointment_in_past"
    appt = ok(call_tool("schedule_appointment", {"case_id": case_id, "job_id": job, "start": "2026-12-07T09:00",
                                                 "end": "2026-12-07T12:00", "access": "tenant_present",
                                                 "confirmed_with": ["tenant", "contractor"]}))
    assert appt["status"] == "booked" and len(appt["messages"]) == 2
    assert build_state(case_id)["jobs"][job]["status"] == "scheduled"

    quote = call_tool("record_financial", {"case_id": case_id, "kind": "quote", "contractor_name": "Oakfield Homes",
                                           "job_id": job, "description": "Replacement dial", "amount_gbp": 160,
                                           "vat_treatment": "includes_vat", "payer": "landlord",
                                           "payment_route": "undecided", "evidence_event": "event-009"})
    assert any("exceeds the job's authorised" in w for w in quote["warnings"])
    invoice = call_tool("record_financial", {"case_id": case_id, "kind": "invoice", "contractor_name": "Oakfield Homes",
                                             "job_id": job, "description": "Dial replaced", "amount_gbp": 150,
                                             "vat_treatment": "plus_vat_20", "payer": "landlord",
                                             "payment_route": "deduct_from_rent", "evidence_event": "event-009"})
    assert ok(invoice)["gross_gbp"] == 180.0 and any("above the approved" in w for w in invoice["warnings"])
    assert err(call_tool("record_financial", {"case_id": case_id, "kind": "invoice", "contractor_name": "Oakfield Homes",
                                              "description": "Call-out", "amount_gbp": 10, "vat_treatment": "unknown",
                                              "payer": "tenant", "payment_route": "deduct_from_rent",
                                              "evidence_event": "event-009"})) == "inconsistent_route"


def test_landlord_approval_request_lifecycle():
    case_id = load("032", cutoff_event=12)["case_id"]
    apr = ok(call_tool("request_landlord_approval", {
        "case_id": case_id, "landlord": {"role": "landlord", "name": "Ellis"}, "request_type": "approve_quote",
        "issue_summary": "Toilet flush mechanism in second bedroom needs replacing",
        "options": [{"label": "Riverside Maintenance", "contractor": "Riverside Maintenance", "amount_gbp": 172.51,
                     "vat_treatment": "plus_vat_20"}],
        "recommended_option": "Riverside Maintenance", "subject": "Quote approval: toilet flush",
        "email_body": "Hi Ellis, the plumber has quoted £172.51 + VAT (£207.01 total) to replace the toilet flush "
                      "mechanism at Flat 10, 130 Lantern Quay. May they proceed?"}))
    assert apr["status"] == "pending" and apr["options"][0]["gross_gbp"] == 207.01
    assert get_state(case_id)["pending"]["approval_requests"] == [apr["id"]]


def get_state(case_id: str) -> dict:
    return ok(call_tool("get_case_state", {"case_id": case_id}))


# --------------------------------------------------------------------------- holds, items, escalation, closing


def test_hold_rules():
    case_id = load("001", cutoff_event=8)["case_id"]
    base = {"case_id": case_id, "reason": "waiting_for_landlord", "waiting_for": "Landlord to send contractor quotes",
            "action_if_no_response": "Phone the landlord"}
    assert err(call_tool("set_hold", {**base, "follow_up_at": "2025-10-01T09:00"})) == "follow_up_in_past"
    assert err(call_tool("set_hold", {**base, "follow_up_at": "2026-01-01T09:00"})) == "follow_up_too_far"
    for day in (14, 15, 16):
        ok(call_tool("set_hold", {**base, "follow_up_at": f"2025-10-{day}T09:00"}))
    fourth = call_tool("set_hold", {**base, "follow_up_at": "2025-10-17T09:00"})
    assert any("Consider escalating" in w for w in fourth["warnings"])
    state = get_state(case_id)
    assert state["status"] == "on_hold" and state["active_hold"]["follow_up_at"] == "2025-10-17T09:00:00Z"


def test_close_case_blockers_and_success():
    case_id = load("017")["case_id"]
    close_args = {"case_id": case_id, "outcome": "resolved_by_tenant_self_help", "payment_route": "no_charge",
                  "completion_evidence_events": ["event-011"],
                  "checks": {"work_completion_confirmed": "done", "tenant_informed": "done", "landlord_informed": "outstanding",
                             "invoice_handled": "not_applicable", "keys_returned": "not_applicable"},
                  "summary": "Tenant found the isolation switch beside the hob; extractor fan works."}

    item = ok(call_tool("track_open_item", {"case_id": case_id, "action": "open", "owner": "agency",
                                            "description": "Confirm to landlord the fan is working", "raised_in_event": "event-011"}))
    blocked = call_tool("close_case", close_args)
    assert err(blocked) == "open_items_remaining" and item["id"] in blocked["error"]["details"]["blockers"][0]
    ok(call_tool("track_open_item", {"case_id": case_id, "action": "resolve", "item_id": item["id"],
                                     "resolution": "Landlord emailed to confirm fan working"}))
    assert err(call_tool("close_case", close_args)) == "checks_outstanding"
    close_args["checks"]["landlord_informed"] = "done"
    closed = ok(call_tool("close_case", close_args))
    assert closed["id"] == "CLOSE-001" and get_state(case_id)["status"] == "closed"
    assert err(call_tool("close_case", {**close_args, "summary": close_args["summary"] + " again"})) == "already_closed"
    late = call_tool("send_email", {"case_id": case_id, "to": [{"role": "tenant"}], "subject": "Follow up",
                                    "purpose": "other", "body": "Just checking the extractor is still working well."})
    assert any("closed" in w for w in late["warnings"])


def test_escalation_blocks_closing():
    case_id = load("040")["case_id"]
    with_bad_priority = call_tool("escalate_to_human", {
        "case_id": case_id, "priority": "P2_same_day", "category": "safety_emergency",
        "summary": "x" * 50, "why_human_needed": "because it is dangerous", "facts_confirmed": ["a"],
        "recommended_next_steps": ["b"]})
    assert err(with_bad_priority) == "invalid_input"
    esc = ok(call_tool("escalate_to_human", {
        "case_id": case_id, "priority": "P3_next_working_day", "category": "conflicting_information",
        "summary": "Tenant swapped the washing machine themselves and left; landlord asked for an inspection of the faulty one.",
        "why_human_needed": "Landlord instruction conflicts with tenant action; needs a decision on next steps.",
        "facts_confirmed": ["Tenant installed own machine (event-008)", "Landlord wants inspection (event-009)"],
        "unknowns_or_conflicts": ["When the tenant returns from holiday"],
        "recommended_next_steps": ["Agree inspection date with tenant on return", "Update landlord"],
        "evidence_events": ["event-008", "event-009"]}))
    assert esc["routed_to"] == "property_manager_on_duty"
    result = call_tool("close_case", {
        "case_id": case_id, "outcome": "no_further_action", "payment_route": "not_applicable",
        "completion_evidence_events": ["event-008"],
        "checks": {k: "not_applicable" for k in ("work_completion_confirmed", "tenant_informed", "landlord_informed",
                                                  "invoice_handled", "keys_returned")},
        "summary": "Tenant swapped machine; nothing further."})
    assert err(result) == "open_items_remaining"
    assert get_state(case_id)["status"] == "awaiting_human"


def test_overdue_detection_and_ledger_audit():
    case_id = load("011", cutoff_event=5)["case_id"]
    ok(call_tool("request_landlord_approval", {
        "case_id": case_id, "landlord": {"role": "landlord", "name": "Turner"}, "request_type": "attend_and_diagnose",
        "issue_summary": "Dishwasher does not finish its cycle", "proposed_spend_limit_gbp": 120,
        "response_needed_within_hours": 48, "subject": "Dishwasher at Flat 12, 78 Copperfield Walk",
        "email_body": "Hi Turner, the tenant reports the dishwasher never finishes its cycle. May we send our appliance "
                      "engineer, fixing on the day if under £120?"}))
    load("011", cutoff_event=9)  # time moves on to the landlord's reply, 4 days later
    state = get_state(case_id)
    assert state["overdue"] and "Approval APR-001" in state["overdue"][0]
    tools_used = [e["tool"] for e in read_ledger(case_id)]
    assert tools_used == ["load_case", "request_landlord_approval", "load_case", "get_case_state"]
    assert all(re.match(r"\d{4}-\d\d-\d\dT", e["sim_time"]) for e in read_ledger(case_id))
