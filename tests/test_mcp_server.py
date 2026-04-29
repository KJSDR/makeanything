from pathlib import Path
from unittest.mock import patch

import pytest

from loglens.mcp_server import analyze_log

FIXTURE = str(Path(__file__).parent / "fixtures" / "sample.log")

FAKE_SUMMARY = {
    "counts": {"ERROR": 2},
    "time_range": {"start": "2024-01-15 09:00:01", "end": "2024-01-15 09:20:02"},
    "errors": ["Database timeout"],
    "warnings": [],
    "root_cause": "Pool exhausted",
    "recommendations": ["Increase pool size"],
    "rag_hit": False,
}


@pytest.fixture(autouse=True)
def mock_summarize():
    with patch("loglens.mcp_server.summarizer.summarize", return_value=FAKE_SUMMARY):
        yield


def test_valid_file_returns_summary():
    result = analyze_log(FIXTURE)
    assert "Pool exhausted" in result


def test_valid_file_returns_string():
    result = analyze_log(FIXTURE)
    assert isinstance(result, str)


def test_nonexistent_file_returns_error_string():
    result = analyze_log("/no/such/file.log")
    assert "Error" in result
    assert "/no/such/file.log" in result


def test_nonexistent_file_does_not_raise():
    try:
        analyze_log("/no/such/file.log")
    except Exception as e:
        pytest.fail(f"raised unexpectedly: {e}")


def test_empty_log_returns_no_events_message(tmp_path):
    empty = tmp_path / "empty.log"
    empty.write_text("")
    result = analyze_log(str(empty))
    assert "No parseable log events" in result


def test_empty_log_does_not_call_summarizer(tmp_path):
    empty = tmp_path / "empty.log"
    empty.write_text("")
    with patch("loglens.mcp_server.summarizer.summarize") as mock:
        analyze_log(str(empty))
        mock.assert_not_called()
