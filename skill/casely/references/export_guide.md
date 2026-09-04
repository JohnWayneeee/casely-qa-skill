# Export Guide: Markdown to Excel

This guide describes how Casely converts generated Markdown test cases into formatted Excel
files for TMS import (Phase 5 of the workflow).

## Overview

The `export_to_xlsx.py` script parses Markdown tables and recreates them in an Excel workbook
using the `openpyxl` library.

## Features

- **Column Mapping:** Automatically maps Markdown headers to Excel columns.
- **Formatting:** Applies bold fonts and centered alignment to headers.
- **Auto-Width:** Calculates appropriate column widths based on content.
- **Multi-line Support:** Correctly handles line breaks (`<br>` or `\n`) within cells.
- **Atomic 1:1 Export:** One `.md` test case in `results/` becomes exactly one `.xlsx` file in
  `exports/`, with the same base name.

## Usage

Run the script from the command line:

```bash
python scripts/export_to_xlsx.py <results_dir> <output_dir>
```

- `results_dir`: Directory containing the `.md` files to export. Defaults to `results/` in the
  current working directory if omitted.
- `output_dir`: Directory where the `.xlsx` files will be created (one per Markdown file).
  Defaults to `exports/` in the current working directory if omitted.

There is no project auto-detection: Casely no longer maintains a persistent `projects/`
directory tree. Run the script from wherever the current conversation's `results/` folder
lives, or pass explicit paths.

## Handling Special Characters

Multi-line cell content using `<br>` or literal newlines is converted to wrapped text within
the cell. Column widths auto-fit to the longest line in each column, capped between 10 and 60
characters.
