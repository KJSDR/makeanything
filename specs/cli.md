## Feature: CLI

### Accepts
- Valid log file path as positional argument to `summarize` command
- `--severity ERROR` (or WARNING / INFO / DEBUG) — filters events to that level only
- `--since "2024-01-15 09:05:00"` — filters events at or after that timestamp
- Both `--severity` and `--since` combined
- No filters — passes all parsed events to summarizer

### Rejects
- Non-existent file path (click raises UsageError before reaching summarizer)
- All events filtered out (prints "No matching log events found." and exits without calling summarizer)
