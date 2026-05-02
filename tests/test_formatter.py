from loglens.formatter import format_summary


def _summary(**overrides):
    base = {
        "counts": {"ERROR": 2, "WARNING": 1, "INFO": 1},
        "time_range": {"start": "2024-01-15 09:00:01", "end": "2024-01-15 09:20:02"},
        "errors": ["Database timeout", "Out of memory"],
        "warnings": ["High memory usage"],
        "root_cause": "Connection pool exhausted",
        "recommendations": ["Increase pool size"],
        "rag_hit": False,
    }
    return {**base, **overrides}


def test_contains_time_range():
    out = format_summary(_summary())
    assert "2024-01-15 09:00:01" in out
    assert "2024-01-15 09:20:02" in out


def test_contains_counts():
    out = format_summary(_summary())
    assert "ERROR: 2" in out
    assert "WARNING: 1" in out


def test_contains_root_cause():
    out = format_summary(_summary())
    assert "Connection pool exhausted" in out


def test_shows_top_errors():
    out = format_summary(_summary())
    assert "Database timeout" in out


def test_shows_recommendations():
    out = format_summary(_summary())
    assert "Increase pool size" in out


def test_rag_hit_shows_notice():
    out = format_summary(_summary(rag_hit=True))
    assert "[RAG]" in out


def test_rag_hit_shows_incident_name():
    out = format_summary(_summary(rag_hit=True, rag_dominant_error="DB timeout"))
    assert "DB timeout" in out
    assert "Past incident matched" in out


def test_no_rag_hit_no_notice():
    out = format_summary(_summary(rag_hit=False))
    assert "[RAG]" not in out


def test_duplicate_errors_show_count():
    out = format_summary(_summary(errors=["DB timeout", "DB timeout", "DB timeout"]))
    assert "×3" in out
    assert "DB timeout" in out


def test_unique_errors_no_count():
    out = format_summary(_summary(errors=["DB timeout", "OOM"]))
    assert "×" not in out


def test_empty_errors_omits_section():
    out = format_summary(_summary(errors=[]))
    assert "Top errors" not in out


def test_empty_recommendations_omits_section():
    out = format_summary(_summary(recommendations=[]))
    assert "Recommendations" not in out
