# Changelog

All notable changes to Casely are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).  
Versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.1.0] — 2026-09-04

### Fixed
- **Export no longer loses data silently.** Two cases produced a plausible-looking but wrong
  Excel file: a real line break inside a cell dropped every step after it, and an unescaped
  `|` shifted every value one column to the left. The exporter now detects both, names the
  file and the cause, skips the case and exits non-zero instead of writing a corrupted row.
- `SKILL.md` now states the formatting contract (`<br>` for line breaks, `\|` for literal
  pipes) in the generation phase, where the file actually gets written, rather than only in
  the export phase.

### Added
- **One combined workbook by default.** `export_to_xlsx.py` now writes a single
  `all_test_cases.xlsx` with one row per case, matching how TestRail, Qase, Zephyr and Xray
  import. Per-case files remain available with `--split`.
- **`references/test_design.md`** — equivalence partitioning, boundary values, decision
  tables, state transitions and error guessing, plus the quality bar for a written case and
  coverage integrity checks. Read before planning and generation.
- **Requirement gap reporting.** The plan phase now flags untestable wording, ambiguity,
  contradictions and missing error paths, with section references.
- Case IDs continue the numbering scheme found in the user's example file.
- Traceability: cases record the requirement or section they came from.
- Evals expanded to 8 cases with 34 formal assertions, covering the approval gate, the
  formatting contract, gap reporting and boundary technique.

### Removed
- `pyproject.toml`. `openpyxl` ships with Claude's code execution environment, so the skill
  needs no local Python setup at all.

### Changed
- README cut from 289 to 185 lines, with a placeholder for the walkthrough video.
- Skill description rewritten for more reliable triggering, including checklist, acceptance
  criteria, regression suite and Russian phrasings.

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
