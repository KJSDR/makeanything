from collections import Counter


def format_summary(summary: dict) -> str:
    tr = summary["time_range"]
    lines = [
        f"Time range: {tr['start']} → {tr['end']}",
        "",
        "Counts:",
        *[f"  {level}: {count}" for level, count in sorted(summary["counts"].items())],
        "",
    ]

    if summary["errors"]:
        error_counts = Counter(summary["errors"])
        top = error_counts.most_common(3)
        lines += [f"Top errors ({len(summary['errors'])} total):"]
        lines += [f"  - {msg} (×{count})" if count > 1 else f"  - {msg}" for msg, count in top]
        lines.append("")

    lines.append(f"Root cause: {summary['root_cause']}")

    if summary.get("recommendations"):
        lines += ["", "Recommendations:"]
        lines += [f"  • {r}" for r in summary["recommendations"]]

    if summary.get("rag_hit"):
        lines += ["", "[RAG] Similar past incident found — used as context in analysis."]

    return "\n".join(lines)
