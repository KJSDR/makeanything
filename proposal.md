# Proposal: LogLens — AI-Powered Log File Summarizer CLI

## Problem

When something breaks in production, the first thing you do is open a log file. What you find is usually hundreds or thousands of lines of timestamps, stack traces, and noise. Finding the actual error and understanding what caused it means manually scanning through all of it, often under pressure.

There's no good reason a human should have to do that. The signal is in there; it just needs to be extracted.

## Solution

**LogLens** is a CLI tool that takes a log file as input and returns a structured, human-readable summary: what went wrong, when, how often, and what the likely cause is. Instead of grepping through 500 lines, you run one command and get the answer in seconds.

### Example Usage

```bash
loglens summarize ./logs/app.log
loglens summarize ./logs/app.log --severity error
loglens summarize ./logs/app.log --since 1h
```

### Example Output

```
LogLens Summary — app.log
─────────────────────────────────────────
Time range:   2025-04-24 13:00 → 14:32
Total lines:  1,842
Errors:       7  (5 unique)
Warnings:     23

⚠ Top Issues:
  1. [ERROR] Database connection timeout — 4 occurrences (first: 13:47)
  2. [ERROR] Auth service unreachable — 2 occurrences (first: 13:49)
  3. [ERROR] NullPointerException in UserService.java:84 — 1 occurrence

💡 Likely root cause: DB timeout at 13:47 appears to cascade into auth
   failures 2 minutes later. Recommend checking DB connection pool config.
─────────────────────────────────────────
```

## Requirements Checklist

- [x] **Project memory** — `CLAUDE.md` with project context, scoped instructions, and custom commands for common dev tasks (run tests, lint, summarize a sample log).
- [x] **Spec with teeth** — each feature has structured acceptance criteria with specific pass/fail conditions before implementation begins.
- [x] **Test-first** — tests are written and committed before the corresponding implementation. Note: parser and formatter specs/tests were written retroactively after initial prototyping; enforced correctly from summarizer onward.
- [x] **Scoped rules** — ruff configured in `pyproject.toml` with E, F, I rule sets.
- [ ] **Iterative refinement** — prompt decisions, model choice, and spec changes documented in `CHANGELOG.md`. Live refinement cycle (run → observe → tune → log before/after) still in progress.

## Tech Stack

- **Language:** Python (strong text processing, easy CLI with `argparse` or `click`)
- **AI:** Anthropic Claude API for natural language summarization and root cause inference
- **Testing:** `pytest` with fixtures covering edge cases (empty logs, malformed lines, large files)
- **Linting:** `ruff` for style enforcement

## Why This Is a Good Engineering Problem

- Solves something genuinely annoying (log triage is painful and universal)
- Clear inputs and outputs make it ideal for test-first development
- AI adds real value — pattern recognition and plain-English explanation are things regex can't do
- Scope is right: simple enough to ship in 2 weeks, rich enough to demonstrate real workflow skills