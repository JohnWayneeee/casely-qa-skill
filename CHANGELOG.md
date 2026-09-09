# Changelog

All notable changes to Casely are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).  
Versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.2.0] — 2026-09-06

### Added
- **Postman collections for API test cases.** When the requirements describe an API — endpoints
  as method + path, an OpenAPI/Swagger file, `curl` examples, response schemas, status codes,
  an auth section — Casely now exports the API-level cases as a runnable Postman v2.1
  collection alongside the Excel file. It says so in the Phase 3 plan first, so the existing
  approval gate covers it and nobody receives an artefact they didn't ask for.
- **`scripts/build_postman_collection.py`** — assembles per-case JSON request specs into the
  collection, an environment file holding every variable, and a README covering import,
  variables, the Collection Runner and a Newman command for CI. Assertions are generated from
  each case's expected result rather than hand-written, so a typo cannot turn a broken
  endpoint into a green run.
- **Everything environment-specific becomes a variable.** `{{baseUrl}}`, `{{authToken}}`, entity
  ids and test data land in the environment file with descriptions and empty values, secrets
  typed as secrets. The value a case is actually testing stays literal — parameterizing
  `amount: 50001` would hide what the case checks.
- **The build refuses unsafe or unrunnable input**, the way the Excel exporter already did: a
  hardcoded host, anything shaped like a JWT or a secret key, a duplicated case id, a missing
  or invalid field. It names the file and exits non-zero rather than writing a collection that
  points at production or carries someone's token.
- **`references/api_collection.md`** — the signals that decide whether a collection is worth
  building, the request spec format, request chaining, and the variable and assertion rules.
- Evals extended with the plan-time offer, the no-endpoints case, and the variable rules.

### Changed
- Phase 5 is now "Export": Excel always, the Postman collection when the plan promised one.
- Casely never guesses an endpoint from a described flow. A spec that names screens but no
  paths gets a request for the API docs instead of a collection that 404s on first run.

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
  contradictions and missing error paths, with section references. Two patterns that read
  as understood are called out by name: a term the spec gates behaviour on without defining
  it, and an external dependency whose failure it never describes.
- Phase 3 cross-checks limits, thresholds and timeouts against the spec's own worked
  examples before the plan goes out, so a contradiction costs one approval instead of two.
- Phase 2 reports when the team's format has no column for the source requirement, and
  offers to add one, instead of dropping traceability without a word.
- Boundary coverage requires both sides of every edge, and an expected result may no longer
  offer a choice of outcomes.
- Case IDs continue the numbering scheme found in the user's example file.
- Traceability: cases record the requirement or section they came from.
- Evals expanded to 8 cases with 34 formal assertions, covering the approval gate, the
  formatting contract, gap reporting and boundary technique.

- **`benchmark/`** — a wallet spec with five planted defects, a team-style example file and a
  100-point rubric, so two runs of the skill can be compared on the same input.

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
