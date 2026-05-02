# LogLens

CLI tool that ingests a log file and returns a structured summary: errors, warnings, time range, occurrence counts, and AI-inferred root cause.

```
$ loglens summarize tests/fixtures/sample.log

Time range: 2024-01-15 09:00:01 → 2024-01-15 09:20:03

Counts:
  ERROR: 6
  INFO: 4
  WARNING: 4

Top errors (6 total):
  - Database connection timeout after 30s (×3)
  - Out of memory: unable to allocate heap
  - Cache miss rate exceeded threshold

Root cause: Combined memory exhaustion and database connection pool depletion
under load, leading to cascading failures.

Recommendations:
  • Increase JVM heap size or application memory allocation
  • Expand database connection pool size to handle concurrent load
  • Implement circuit breaker pattern to fail fast when database is unavailable
```

## Usage

```bash
pip install -e .

loglens summarize app.log
loglens summarize app.log --severity error
loglens summarize app.log --since "2024-01-15 09:10:00"
```

Requires `ANTHROPIC_API_KEY` set in environment (or `.env` file).

## How It Works

```
parser.py → summarizer.py → formatter.py
```

1. **Parser** — reads log file, extracts timestamp/level/message per line
2. **Summarizer** — builds counts and time range, calls Claude API for root cause + recommendations, checks RAG store for similar past incidents
3. **Formatter** — renders structured terminal output

Claude API calls live only in `summarizer.py`. RAG store persists to `~/.loglens/past_analyses.json`.

## MCP Server

LogLens exposes an `analyze_log` tool via stdio MCP server, so any MCP-compatible client can call it programmatically.

```bash
python -m loglens.mcp_server
```

## Skills Demonstrated

| Requirement | Evidence |
|:--|:--|
| Project memory | `CLAUDE.md` with scoped instructions and custom commands (`/run-tests`, `/lint`, `/summarize-sample`) |
| Spec with teeth | `specs/` — structured acceptance criteria (Accepts/Rejects) written before each feature |
| Test-first | Commit history: `spec:` → `test:` → `feat:` order enforced from `summarizer` onward |
| Protocol integration | MCP server (`mcp_server.py`) exposes `analyze_log` tool over stdio |
| Scoped rules | `ruff` configured in `pyproject.toml` with E, F, I rule sets |
| Iterative refinement | `CHANGELOG.md` — 3 before/after entries from live run on `sample.log` (fence stripping, error deduplication, RAG tag context) |
| Custom protocol server ⭐ | Full MCP server with spec, tests, and acceptance criteria |

## Takeaways

**What worked:** Test-first made the formatter and summarizer changes today zero-risk — 23 tests caught nothing breaking. Specs-before-code forced me to define what "done" meant before writing anything. The RAG store turned out to be genuinely useful: repeat log patterns get faster, more accurate diagnoses on second run.

**What didn't:** Claude Haiku ignores "Return only valid JSON, no markdown" about 100% of the time — had to strip fences in code rather than relying on the prompt. The `--since` flag ended up using absolute timestamps instead of relative durations (`"2024-01-15 09:10:00"` not `1h`) because it was simpler and more precise for historical logs.

**What I'd change:** Complexity awareness was the one rubric item I didn't explicitly structure — major features got full spec/test/implement cycles but small tweaks went straight to code. Next time I'd define a size threshold upfront (e.g., > 20 lines changed = write spec first).

## Dev

```bash
# Install
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# Test
pytest -v

# Lint
ruff check loglens/ tests/

# Run on sample log
loglens summarize tests/fixtures/sample.log
```
