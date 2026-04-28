import json
from pathlib import Path

_STORE = Path.home() / ".loglens" / "past_analyses.json"


def load() -> list[dict]:
    if not _STORE.exists():
        return []
    return json.loads(_STORE.read_text())


def save(dominant_error: str, root_cause: str, counts: dict) -> None:
    store = load()
    store.append({"dominant_error": dominant_error, "root_cause": root_cause, "counts": counts})
    _STORE.parent.mkdir(parents=True, exist_ok=True)
    _STORE.write_text(json.dumps(store, indent=2))


def find_similar(dominant_error: str) -> dict | None:
    needle = dominant_error.lower()
    for entry in load():
        haystack = entry["dominant_error"].lower()
        if needle in haystack or haystack in needle:
            return entry
    return None
