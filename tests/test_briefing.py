"""Offline tests for the deterministic briefing (no API calls)."""

from __future__ import annotations

from pathlib import Path

import pytest

from agent.briefing import build_briefing
from tools._common import read_ledger

CASES = Path(__file__).resolve().parent.parent / "Property Management"
pytestmark = pytest.mark.skipif(not CASES.exists(), reason="public practice cases not present")


@pytest.fixture(autouse=True)
def isolated_run(tmp_path, monkeypatch):
    monkeypatch.setenv("AGENT_RUN_DIR", str(tmp_path / "runs"))


def test_all_visible_attachments_are_read_into_the_briefing():
    b = build_briefing(str(CASES / "008"), cutoff_event=38)
    paths = [d["path"] for d in b.attachments]
    assert "attachments/attachment-01-check-out-inspection-report.pdf" in paths
    assert all(d["text"] for d in b.attachments)
    assert "## Case attachments" in b.text and "Check-out inspection report" in b.text
    reads = [e for e in read_ledger(b.case_id) if e["tool"] == "read_attachment"]
    assert len(reads) == len(b.attachments)


def test_future_attachments_stay_out_of_the_briefing():
    b = build_briefing(str(CASES / "008"), cutoff_event=38)
    assert not any("invoice" in d["path"] for d in b.attachments)
    assert "attachment-04-invoice" not in b.text


def test_attachment_linked_events_and_case_without_attachments():
    b = build_briefing(str(CASES / "004"), cutoff_event=18)
    quote = next(d for d in b.attachments if "quotation" in d["path"])
    assert quote["linked_events"] == ["event-010"] and "£90" in quote["text"]
    assert build_briefing(str(CASES / "011"), cutoff_event=9).attachments == []


def test_attachment_budget_is_bounded():
    b = build_briefing(str(CASES / "005"), cutoff_event=30)
    assert sum(len(d["text"] or "") for d in b.attachments) <= 40_000 + 200
