"""Offline tests for the voice layer (no ElevenLabs or Claude calls)."""

from __future__ import annotations

import pytest

from tools import call_tool
from voice.callback import strip_opening, tenant_update_from_ledger, to_speech
from voice.intake import build_case, has_tenant_speech

CALL = {
    "conversation_id": "conv_test123",
    "status": "done",
    "metadata": {"start_time_unix_secs": 1791640800, "call_duration_secs": 142,
                 "phone_call": {"external_number": "+447700900123"}},
    "analysis": {
        "call_summary_title": "Boiler not working",
        "transcript_summary": "Tenant reports no heating or hot water since yesterday; baby at home.",
        "data_collection_results": {
            "tenant_name": {"value": "Sofia Marsh"},
            "property_address": {"value": "Flat 2, 31 Marlowe Court, Kingshaven, ZZ5 7ZZ"},
            "callback_number": {"value": "+447700900123"},
            "issue_summary": {"value": "Combi boiler shows error E119 and won't fire. No heating or hot water since yesterday."},
            "hazard": {"value": "No heating or hot water"},
            "vulnerable_occupant": {"value": True},
            "access_notes": {"value": "Home all day, small dog"},
            "out_of_scope_requests": {"value": ""},
        },
    },
    "transcript": [
        {"role": "agent", "message": "Hello, you've reached the Northbridge Lettings repairs line."},
        {"role": "user", "message": "Hi, my boiler has stopped working and I have a newborn."},
        {"role": "agent", "message": "I'm sorry to hear that. Can you smell gas at all?"},
        {"role": "user", "message": "No, no smell of gas."},
    ],
}


@pytest.fixture(autouse=True)
def isolated(tmp_path, monkeypatch):
    monkeypatch.setenv("AGENT_RUN_DIR", str(tmp_path / "runs"))


def test_call_becomes_a_case_the_agent_can_load(tmp_path):
    folder = build_case(CALL, cases_dir=tmp_path / "cases")
    assert folder.name == "001"
    loaded = call_tool("load_case", {"case_path": str(folder)})
    assert loaded["ok"], loaded["error"]
    data = loaded["data"]
    assert data["property"] == "Flat 2, 31 Marlowe Court, Kingshaven, ZZ5 7ZZ"
    assert "E119" in data["initial_request"] and "Vulnerable occupant at the property: yes" in data["initial_request"]
    event = data["events"][0]
    assert (event["channel"], event["from"]) == ("Call", "Tenant")
    assert "Tenant: Hi, my boiler has stopped working" in event["body"]
    screen = call_tool("safety_screen", {"case_id": data["case_id"]})["data"]
    assert "no_heating_or_hot_water" in screen["hazards"]


def test_same_call_is_never_converted_twice(tmp_path):
    first = build_case(CALL, cases_dir=tmp_path / "cases")
    assert build_case(CALL, cases_dir=tmp_path / "cases") == first
    other = build_case({**CALL, "conversation_id": "conv_other"}, cases_dir=tmp_path / "cases")
    assert other.name == "002"


def test_update_prefers_call_script_then_safety_then_messages():
    tenant = {"role": "tenant"}
    ledger = [
        {"tool": "send_email", "ok": True, "data": {"to": [tenant], "purpose": "status_update", "body": "Status text"}},
        {"tool": "send_sms", "ok": True, "data": {"to": tenant, "purpose": "nudge_check_email", "body": "Check email"}},
        {"tool": "send_email", "ok": True, "data": {"to": [{"role": "landlord"}], "purpose": "approval_request", "body": "LL"}},
    ]
    assert tenant_update_from_ledger(ledger)["text"] == "Status text"
    ledger.append({"tool": "send_sms", "ok": True, "data": {"to": tenant, "purpose": "safety_advice", "body": "Leave now"}})
    assert tenant_update_from_ledger(ledger)["text"] == "Leave now"
    ledger.append({"tool": "place_call", "ok": True, "data": {"to": tenant, "script": "Script text"}})
    assert tenant_update_from_ledger(ledger)["source"] == "agent call script"
    assert tenant_update_from_ledger([e for e in ledger if e["data"].get("to") == [{"role": "landlord"}]]) is None


def test_to_speech_strips_email_furniture_and_limits_length():
    email = ("Dear Sofia,\n\nThanks for calling. An engineer will attend **tomorrow morning**.\n"
             "See https://example.com/x for details.\n\nKind regards,\nNorthbridge Lettings")
    spoken = to_speech(email)
    assert spoken == "Thanks for calling. An engineer will attend tomorrow morning. See for details."
    long = to_speech("Sentence one is here. " * 100, limit=200)
    assert len(long) < 260 and long.endswith("We'll send the full details in writing.")


def test_silent_calls_are_detected():
    assert has_tenant_speech(CALL)
    silent = {**CALL, "transcript": [{"role": "agent", "message": "Hello?"}, {"role": "user", "message": "..."},
                                     {"role": "user", "message": " … "}]}
    assert not has_tenant_speech(silent)


def test_agent_greeting_is_not_repeated_in_the_voice_update():
    script = ("Hello Fazal, this is Northbridge Lettings calling about the leak at flat 4. "
              "First, please turn off the water.")
    assert to_speech(script) == "First, please turn off the water."
    assert strip_opening("Please turn off the water. Hello again.") == "Please turn off the water. Hello again."
