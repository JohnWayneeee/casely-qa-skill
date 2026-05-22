# Changelog

All notable changes to Casely are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).  
Versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
