from pathlib import Path
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from loglens.cli import main

FIXTURE = str(Path(__file__).parent / "fixtures" / "sample.log")

FAKE_SUMMARY = {
    "counts": {"ERROR": 2},
    "time_range": {"start": "2024-01-15 09:00:01", "end": "2024-01-15 09:20:02"},
    "errors": ["Database timeout"],
    "warnings": [],
    "root_cause": "Pool exhausted",
    "recommendations": [],
    "rag_hit": False,
}


@pytest.fixture()
def mock_summarize():
    with patch("loglens.cli.summarizer.summarize", return_value=FAKE_SUMMARY) as m:
        yield m


def test_summarize_valid_file(mock_summarize):
    result = CliRunner().invoke(main, ["summarize", FIXTURE])
    assert result.exit_code == 0
    assert "Pool exhausted" in result.output
    mock_summarize.assert_called_once()


def test_summarize_nonexistent_file():
    result = CliRunner().invoke(main, ["summarize", "/no/such/file.log"])
    assert result.exit_code != 0


def test_severity_filter_passes_only_matching(mock_summarize):
    CliRunner().invoke(main, ["summarize", FIXTURE, "--severity", "ERROR"])
    events = mock_summarize.call_args[0][0]
    assert all(e.level == "ERROR" for e in events)


def test_severity_filter_case_insensitive(mock_summarize):
    result = CliRunner().invoke(main, ["summarize", FIXTURE, "--severity", "error"])
    events = mock_summarize.call_args[0][0]
    assert all(e.level == "ERROR" for e in events)
    assert result.exit_code == 0


def test_since_filter_excludes_earlier_events(mock_summarize):
    CliRunner().invoke(main, ["summarize", FIXTURE, "--since", "2024-01-15 09:10:00"])
    events = mock_summarize.call_args[0][0]
    assert all(e.timestamp >= "2024-01-15 09:10:00" for e in events)


def test_severity_and_since_combined(mock_summarize):
    CliRunner().invoke(
        main,
        ["summarize", FIXTURE, "--severity", "ERROR", "--since", "2024-01-15 09:15:00"],
    )
    events = mock_summarize.call_args[0][0]
    assert all(e.level == "ERROR" and e.timestamp >= "2024-01-15 09:15:00" for e in events)


def test_all_filtered_out_prints_message():
    result = CliRunner().invoke(
        main, ["summarize", FIXTURE, "--severity", "DEBUG"]
    )
    assert result.exit_code == 0
    assert "No matching log events found" in result.output


def test_all_filtered_out_does_not_call_summarizer(mock_summarize):
    CliRunner().invoke(main, ["summarize", FIXTURE, "--severity", "DEBUG"])
    mock_summarize.assert_not_called()
