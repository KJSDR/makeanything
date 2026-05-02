import json
from unittest.mock import MagicMock, patch

import pytest

from loglens.parser import LogEvent
from loglens.summarizer import summarize


def _events(*specs):
    return [LogEvent(timestamp=ts, level=lvl, message=msg) for ts, lvl, msg in specs]


EVENTS = _events(
    ("2024-01-15 09:00:01", "ERROR", "Database timeout"),
    ("2024-01-15 09:05:00", "WARNING", "High memory usage"),
    ("2024-01-15 09:10:00", "ERROR", "Out of memory"),
    ("2024-01-15 09:20:02", "INFO", "Service restarted"),
)

AI_RESPONSE = {"root_cause": "Connection pool exhausted", "recommendations": ["Increase pool size"]}


def _mock_client(text):
    msg = MagicMock()
    msg.content = [MagicMock(text=text)]
    client = MagicMock()
    client.messages.create.return_value = msg
    return client


@pytest.fixture(autouse=True)
def no_rag(monkeypatch):
    monkeypatch.setattr("loglens.summarizer.rag.find_similar", lambda _: None)
    monkeypatch.setattr("loglens.summarizer.rag.save", lambda *_: None)


@pytest.fixture()
def mock_client(monkeypatch):
    client = _mock_client(json.dumps(AI_RESPONSE))
    monkeypatch.setattr("loglens.summarizer.anthropic.Anthropic", lambda: client)
    return client


def test_counts_levels(mock_client):
    result = summarize(EVENTS)
    assert result["counts"]["ERROR"] == 2
    assert result["counts"]["WARNING"] == 1
    assert result["counts"]["INFO"] == 1


def test_time_range(mock_client):
    result = summarize(EVENTS)
    assert result["time_range"]["start"] == "2024-01-15 09:00:01"
    assert result["time_range"]["end"] == "2024-01-15 09:20:02"


def test_errors_list(mock_client):
    result = summarize(EVENTS)
    assert "Database timeout" in result["errors"]
    assert "Out of memory" in result["errors"]


def test_warnings_list(mock_client):
    result = summarize(EVENTS)
    assert "High memory usage" in result["warnings"]


def test_root_cause_from_api(mock_client):
    result = summarize(EVENTS)
    assert result["root_cause"] == "Connection pool exhausted"


def test_recommendations_from_api(mock_client):
    result = summarize(EVENTS)
    assert "Increase pool size" in result["recommendations"]


def test_rag_hit_false_when_no_match(mock_client):
    result = summarize(EVENTS)
    assert result["rag_hit"] is False


def test_rag_hit_true_when_match(monkeypatch):
    past = {"dominant_error": "Database timeout", "root_cause": "Pool exhausted"}
    monkeypatch.setattr("loglens.summarizer.rag.find_similar", lambda _: past)
    monkeypatch.setattr("loglens.summarizer.rag.save", lambda *_: None)
    client = _mock_client(json.dumps(AI_RESPONSE))
    monkeypatch.setattr("loglens.summarizer.anthropic.Anthropic", lambda: client)
    result = summarize(EVENTS)
    assert result["rag_hit"] is True


def test_malformed_json_fallback(monkeypatch):
    monkeypatch.setattr("loglens.summarizer.rag.find_similar", lambda _: None)
    monkeypatch.setattr("loglens.summarizer.rag.save", lambda *_: None)
    client = _mock_client("not json at all")
    monkeypatch.setattr("loglens.summarizer.anthropic.Anthropic", lambda: client)
    result = summarize(EVENTS)
    assert result["root_cause"] == "not json at all"
    assert result["recommendations"] == []


def test_fenced_json_parsed(monkeypatch):
    monkeypatch.setattr("loglens.summarizer.rag.find_similar", lambda _: None)
    monkeypatch.setattr("loglens.summarizer.rag.save", lambda *_: None)
    fenced = f"```json\n{json.dumps(AI_RESPONSE)}\n```"
    client = _mock_client(fenced)
    monkeypatch.setattr("loglens.summarizer.anthropic.Anthropic", lambda: client)
    result = summarize(EVENTS)
    assert result["root_cause"] == "Connection pool exhausted"
    assert result["recommendations"] == ["Increase pool size"]


def test_no_errors_events(monkeypatch):
    monkeypatch.setattr("loglens.summarizer.rag.find_similar", lambda _: None)
    monkeypatch.setattr("loglens.summarizer.rag.save", lambda *_: None)
    client = _mock_client(json.dumps(AI_RESPONSE))
    monkeypatch.setattr("loglens.summarizer.anthropic.Anthropic", lambda: client)
    events = _events(("2024-01-15 09:00:00", "INFO", "All good"))
    result = summarize(events)
    assert result["errors"] == []
    assert result["rag_hit"] is False
