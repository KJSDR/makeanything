# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project: LogLens

CLI tool that ingests a log file and returns a structured summary: errors, warnings, time range, occurrence counts, and AI-inferred root cause. Built with Python + Anthropic Claude API. See `proposal.md` for full spec.

## Workflow Rules

**Test-first.** Write the test, commit it, then write the implementation. Commit history must show this order.

**Spec before code.** Each feature gets a spec written in `specs/` before any implementation starts. Format:
```
## Feature: <name>
### Accepts
- <pass condition>
### Rejects
- <fail condition>
```

**Ruff** for linting. Config in `pyproject.toml`. No other linters.

**Iterative refinement.** When output quality changes (prompt tuning, format changes), document the decision in `CHANGELOG.md`.

**Commit consistently.** Small, frequent commits throughout the project — not batched at the end. Graded on commit velocity.

## Custom Commands

Stored in `.claude/commands/`. Add commands for common dev tasks once project is scaffolded (run tests, lint, summarize a sample log).

## Architecture

Data flows `parser.py → summarizer.py → formatter.py`. CLI wires them together. Claude API calls live only in `summarizer.py`.

## Commands

> To be filled in once project is scaffolded and approved.

## Course Requirements Tracking

- [x] **Project memory** — this file
- [ ] **Spec with teeth** — acceptance criteria before each feature
- [ ] **Test-first** — tests committed before implementation
- [ ] **Scoped rules** — ruff config in `pyproject.toml`
- [ ] **Iterative refinement** — prompt/output changes logged in `CHANGELOG.md`

Presentation: Day 14, Wed May 6. Rubric grades workflow quality, not code complexity.
