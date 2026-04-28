from loglens.parser import LogEvent, parse


def test_parses_single_error_line():
    events = parse("2024-01-15 09:10:33 ERROR Database connection timeout after 30s")
    assert len(events) == 1
    assert events[0].level == "ERROR"
    assert events[0].timestamp == "2024-01-15 09:10:33"
    assert events[0].message == "Database connection timeout after 30s"


def test_parses_all_levels():
    text = (
        "2024-01-15 09:00:01 INFO App started\n"
        "2024-01-15 09:00:02 DEBUG Init config\n"
        "2024-01-15 09:00:03 WARNING High memory\n"
        "2024-01-15 09:00:04 ERROR Crash\n"
    )
    events = parse(text)
    assert [e.level for e in events] == ["INFO", "DEBUG", "WARNING", "ERROR"]


def test_skips_malformed_lines():
    text = (
        "this is not a log line\n"
        "2024-01-15 09:00:01 INFO Valid line\n"
        "also garbage\n"
    )
    events = parse(text)
    assert len(events) == 1
    assert events[0].message == "Valid line"


def test_skips_blank_lines():
    text = "\n\n2024-01-15 09:00:01 INFO Hello\n\n"
    events = parse(text)
    assert len(events) == 1


def test_empty_input_returns_empty_list():
    assert parse("") == []


def test_skips_unknown_level():
    text = "2024-01-15 09:00:01 CRITICAL Something bad"
    events = parse(text)
    assert len(events) == 0


def test_multi_word_message_preserved():
    text = "2024-01-15 09:00:01 ERROR Failed to connect to database after 3 retries"
    events = parse(text)
    assert events[0].message == "Failed to connect to database after 3 retries"
