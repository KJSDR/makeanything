import json
from collections import Counter

import anthropic

from loglens import rag
from loglens.parser import LogEvent


def summarize(events: list[LogEvent]) -> dict:
    counts = Counter(e.level for e in events)
    errors = [e.message for e in events if e.level == "ERROR"]
    warnings = [e.message for e in events if e.level == "WARNING"]
    time_range = {
        "start": events[0].timestamp if events else None,
        "end": events[-1].timestamp if events else None,
    }

    dominant_error = errors[0] if errors else ""
    past = rag.find_similar(dominant_error) if dominant_error else None
    past_context = (
        f"\nRelevant past incident: {past['dominant_error']}\nPast root cause: {past['root_cause']}\n"
        if past
        else ""
    )

    prompt = f"""Analyze these log events. Return JSON with keys: root_cause (string), recommendations (list of strings).
{past_context}
Counts: {dict(counts)}
Time range: {time_range['start']} to {time_range['end']}
Errors:
{chr(10).join(errors[:10])}
Warnings:
{chr(10).join(warnings[:10])}

Return only valid JSON, no markdown."""

    client = anthropic.Anthropic()
    msg = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )

    try:
        ai = json.loads(msg.content[0].text)
    except Exception:
        ai = {"root_cause": msg.content[0].text, "recommendations": []}

    result = {
        "counts": dict(counts),
        "time_range": time_range,
        "errors": errors,
        "warnings": warnings,
        "root_cause": ai.get("root_cause", ""),
        "recommendations": ai.get("recommendations", []),
        "rag_hit": past is not None,
    }

    if dominant_error:
        rag.save(dominant_error, result["root_cause"], dict(counts))

    return result
