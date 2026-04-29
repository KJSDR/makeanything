## Feature: Summarizer

### Accepts
- Non-empty list of `LogEvent` objects with timestamp, level, message fields
- Events with any mix of ERROR / WARNING / INFO / DEBUG levels
- Lists with no errors (root cause still returned, errors list empty)
- Lists with no warnings (warnings list empty)
- Valid JSON response from Claude API with `root_cause` and `recommendations` keys
- Malformed Claude JSON response (falls back: raw text as root_cause, empty recommendations)
- RAG hit (past similar incident found — injected into prompt, rag_hit=True in result)
- No RAG hit (rag_hit=False in result)

### Rejects
- Empty event list (behaviour undefined — caller must filter before passing)

### Returns
Dict with keys:
- `counts` — dict of level → int
- `time_range` — dict with `start` and `end` timestamps
- `errors` — list of error messages
- `warnings` — list of warning messages
- `root_cause` — string
- `recommendations` — list of strings
- `rag_hit` — bool
