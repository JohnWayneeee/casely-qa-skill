# Export Guide: Markdown to Excel

How Casely turns generated Markdown test cases into Excel for TMS import (Phase 5).

## Default: one file, one row per case

`export_to_xlsx.py` writes a single workbook — `all_test_cases.xlsx` — with one row per test
case, because TestRail, Qase, Zephyr and Xray all import one file and map its columns once.
Separate files per case would mean repeating that import for every case.

```bash
python <skill-path>/scripts/export_to_xlsx.py [results_dir] [output_dir] [--split] [--name FILE]
```

- `results_dir` — where the `.md` test cases live (default: `results`)
- `output_dir` — where Excel files are written (default: `exports`)
- `--split` — write one Excel file per case instead of the combined workbook. Use only when
  the user wants per-case files for review or version control rather than import.
- `--name` — rename the combined workbook (default: `all_test_cases.xlsx`)

Only `openpyxl` is required, and it is already present in Claude's code execution environment.

## It refuses bad input instead of quietly mangling it

A test case that reaches TestRail without its steps is worse than one that never exported, so
the script validates each file and skips the ones it cannot read faithfully. It exits non-zero
and names each problem:

| Problem | Cause | Fix |
|---------|-------|-----|
| "the row is cut off at …" | A real line break inside a cell — Markdown ends the row there, so the rest of the case would vanish | Write line breaks as `<br>` |
| "row has N cells but the header has M" | An unescaped `|` in the text splits the row and shifts every value | Escape it as `\|` |
| "no Markdown table found" | The file isn't a one-row table | Rewrite per the Phase 4 formatting contract |

Fix the flagged Markdown and run the export again. Never present a partial export as complete.

## Formatting details

- `<br>` and `\|` are decoded back into real newlines and pipes inside the Excel cell.
- Cells wrap text and align to the top; the header row is bold, centered, and frozen.
- Column widths auto-fit the longest line, clamped between 10 and 60 characters.
- If test cases somehow carry different column structures, each structure gets its own sheet
  and the script warns — rather than forcing rows into columns they don't belong to.
