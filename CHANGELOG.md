# Changelog

All notable changes to Casely are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).  
Versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.0.0] — 2026-09-04

### Changed — full workflow overhaul
- **Replaced the command-driven workflow with a single conversation.** `/init`, `/parse`,
  `/style`, `/plan`, `/generate`, and `/export` no longer exist as commands. Attach requirement
  documents and (optionally) example test cases, describe what you need, and Casely runs the
  whole pipeline in one conversation.
- **Dropped the `docling` parser and OCR dependency entirely.** Claude reads PDF/DOCX/XLSX
  attachments natively; `scripts/casely_parser.py` and `references/parser_usage.md` are
  removed. `openpyxl` is now the only dependency.
- **Added a mandatory approval gate on the test plan.** Casely always stops after proposing
  coverage (modules, tiers, estimated case count) and waits for explicit approval before
  generating any test case. Every other phase proceeds without extra confirmation.
- **Removed persistent `projects/<name>/` scaffolding.** Each conversation is self-contained;
  `export_to_xlsx.py` now defaults to `results/` → `exports/` in the working directory instead
  of auto-detecting a project folder.
- Rewrote `SKILL.md`, `README.md`, evals, and reference docs around the new flow. This is the
  same skill everywhere: Claude Code, claude.ai (web), and the Claude desktop app.

### Why
The command-based flow assumed a local terminal and a persistent project folder — a poor fit
for QA engineers who mostly use Claude in the browser or desktop app. The new flow needs
nothing but an attachment and a sentence.

---

## [1.5.0] — 2026-05-22

### Added
- `/generate security` type for device metadata and access-control test cases
- Multi-project support: `projects/` directory with isolated workspaces per project
- Smart project auto-detection in `/parse` and `/export` (picks the most recently modified project)
- Russian-language document support across all workflow steps

### Changed
- `/init` now runs `uv sync` from the repository root instead of `uv add`, avoiding `pyproject.toml` mutation
- `/export` now produces one `.xlsx` file per test case (atomic 1:1 mapping) instead of a single monolithic file
- Style guide is now treated as the single source of truth — column names are never renamed or omitted

### Fixed
- Column mismatch during TestRail import caused by hardcoded header names
- `/parse` failing silently on scanned PDFs without selectable text

---

## [1.0.0] — 2026-02-26

### Added
- Initial release: `/init`, `/parse`, `/style`, `/plan`, `/generate`, `/export` workflow
- Docling-based OCR for PDF and DOCX requirements
- Excel export with configurable column mapping from example files
- ISTQB-aligned test planning with module breakdown and coverage estimates
- English and Russian language support
