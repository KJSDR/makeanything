# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project: LogLens

CLI tool that ingests a log file and returns a structured summary: errors, warnings, time range, occurrence counts, and AI-inferred root cause. Built with Python + Anthropic Claude API. See `proposal.md` for full spec.

## Workflow Rules

**Test-first.** Write the test, commit it, then write the implementation. Commit history must show this order.

**Spec before code.** Each feature needs written acceptance criteria (pass/fail conditions) before any implementation starts.

**Ruff** for linting. Config in `pyproject.toml`. No other linters.

**Iterative refinement.** When output quality changes (prompt tuning, format changes), document the decision in `CHANGELOG.md`.

## Commands

> To be filled in once project is scaffolded and approved.

## Course Requirements Tracking

- [ ] **Project memory** — this file
- [ ] **Spec with teeth** — acceptance criteria before each feature
- [ ] **Test-first** — tests committed before implementation
- [ ] **Scoped rules** — ruff config in `pyproject.toml`
- [ ] **Iterative refinement** — prompt/output changes logged in `CHANGELOG.md`

Presentation: Day 14, Wed May 6. Rubric grades workflow quality, not code complexity.
