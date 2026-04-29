# Changelog

## [Unreleased]

### Workflow note: test-first enforcement

Specs and tests for `parser` and `formatter` were written retroactively after initial prototyping (commits `98d9ff4`, `51b0a58`). Test-first workflow was enforced from `summarizer` onward — spec committed before tests, tests committed before implementation. Going forward all features follow this order.

---

### Spec change: `--since` flag uses absolute timestamp instead of relative duration

**Original proposal:** `--since 1h` (relative, e.g. "last hour")

**Implementation:** `--since "2024-01-15 09:10:00"` (absolute timestamp)

**Why:** Absolute timestamps match the format already present in log files — no parsing of duration strings, no ambiguity about what "now" means when processing a historical log. Simpler implementation, more precise filtering.

---


### Prompt: Structured JSON output enforced in prompt (commit 39006d5)

**Decision:** Prompt instructs Claude to return only valid JSON with keys `root_cause` (string) and `recommendations` (list). Ends with "Return only valid JSON, no markdown."

**Why:** Early draft returned prose. Parsing prose for downstream formatting was fragile. JSON gives deterministic field access and a clear fallback path when parsing fails.

**Fallback added:** If `json.loads` raises, raw text becomes `root_cause` and `recommendations` defaults to `[]`. Prevents crash on malformed model output.

---

### Prompt: Error/warning truncation to 10 lines (commit 39006d5)

**Decision:** Only first 10 errors and first 10 warnings are injected into the prompt (`errors[:10]`, `warnings[:10]`).

**Why:** Large log files can produce hundreds of errors. Sending all of them bloats the prompt, increases latency, and adds cost without meaningfully improving root cause accuracy — the pattern is usually visible in the first few occurrences.

---

### Model: claude-haiku-4-5 chosen over Sonnet (commit 39006d5)

**Decision:** `summarizer.py` uses `claude-haiku-4-5-20251001`.

**Why:** Root cause inference from structured log data is a low-complexity reasoning task. Haiku is fast and cheap enough for CLI use. Would revisit Sonnet if output quality on ambiguous logs proved insufficient.

---

### Feature: RAG context injection (commit 39006d5)

**Decision:** If a past incident with a similar dominant error exists in `~/.loglens/past_analyses.json`, it is injected into the prompt as additional context before the log data.

**Why:** Repeat incidents (same service, same error pattern) benefit from prior root cause analysis. Without RAG, Claude re-derives the same conclusion from scratch each run. With it, the model can confirm or refine a known diagnosis. Substring match is sufficient for controlled log formats.
