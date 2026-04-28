# POC Notes — LogLens RAG Prototype

## What I Built

A working RAG pipeline wired into the LogLens CLI.

**New files:**
- `loglens/parser.py` — parses generic log lines (`timestamp level message`) into `LogEvent` dataclasses
- `loglens/rag.py` — loads/saves/queries a local JSON store at `~/.loglens/past_analyses.json`
- `loglens/summarizer.py` — retrieves similar past incidents, injects them into Claude's prompt, saves new analysis back to store
- `loglens/formatter.py` — renders structured output to stdout
- `tests/fixtures/sample.log` — generic demo log with DB timeouts, memory warnings, and a crash

**Flow:**
```
log file → parser → rag lookup → Claude prompt + context → formatter → stdout
                                        ↑
                             past_analyses.json (grows each run)
```

## What Worked

- Parser correctly extracts all 14 events from `sample.log`
- RAG store saves and retrieves past analyses by string matching on dominant error
- On second run with similar errors, Claude receives prior root cause as context — output reflects it
- No vector DB, no embeddings — plain JSON + substring match is enough for a demo

## What Surprised Me

**RAG without embeddings works fine for controlled input.** For a demo with crafted log files, string matching on error type is totally sufficient. The "retrieval" step is dead simple but the effect is real — Claude's root cause on run 2 references the prior incident.

**The build tooling was finicky.** `setuptools.backends.legacy:build` (scaffolded default) is too new for pip's bundled pyproject-hooks. Switched to `setuptools.build_meta`. Also had to explicitly set `[tool.setuptools.packages.find]` because `specs/` directory triggered multi-package auto-discovery errors.

## To Run

```bash
# One-time setup
python3.12 -m venv .venv
.venv/bin/pip install -e ".[dev]"

# Set your API key
export ANTHROPIC_API_KEY=sk-...

# Run on the sample log
.venv/bin/loglens summarize tests/fixtures/sample.log

# Second run — RAG kicks in (similar errors recognized from first run)
.venv/bin/loglens summarize tests/fixtures/sample.log
```
