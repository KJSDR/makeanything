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

### Refinement: RAG tag shows matched incident name (iterative refinement #3)

**Before:** `[RAG] Similar past incident found — used as context in analysis.` — generic, no info on which past incident matched.

**After:** `[RAG] Past incident matched: "Database connection timeout after 30s" — used as context.` — shows the dominant error from the matched past incident.

**Why:** Generic tag gave no signal. User couldn't tell if the RAG hit was relevant or a false positive. Showing the matched error string lets the user judge quality of the retrieval.

---

### Refinement: Deduplicate top errors with occurrence counts (iterative refinement #2)

**Before:** `Top errors (6 total):` listed same message three times — "Database connection timeout after 30s" × 3 with no count shown.

**After:** `formatter.py` uses `Counter.most_common(3)` on error list. Duplicate entries collapse to one line with `(×N)` suffix. Unique errors display unchanged.

**Why:** Repeated errors obscured variety. Top-3 of 6 errors were identical — user got no signal about second and third distinct error types.

---

### Refinement: Strip markdown fences before JSON parse (iterative refinement #1)

**Before:** Model returned ` ```json\n{...}\n``` ` despite "Return only valid JSON, no markdown" in prompt. `json.loads` raised, fallback set `root_cause` to the raw fenced string. Output showed ` ```json ` block in terminal.

**After:** `summarizer.py` strips leading ` ``` ` / ` ```json ` and trailing ` ``` ` before `json.loads`. Fenced responses now parse correctly. Malformed non-JSON still falls back to raw text as before.

**Why:** Haiku ignores the no-markdown instruction ~100% of the time on this prompt. Stripping fences in the parser is more reliable than prompt-only enforcement.

---

### Feature: RAG context injection (commit 39006d5)

**Decision:** If a past incident with a similar dominant error exists in `~/.loglens/past_analyses.json`, it is injected into the prompt as additional context before the log data.

**Why:** Repeat incidents (same service, same error pattern) benefit from prior root cause analysis. Without RAG, Claude re-derives the same conclusion from scratch each run. With it, the model can confirm or refine a known diagnosis. Substring match is sufficient for controlled log formats.
