# 🚀 Casely — AI QA Test Case Generator

<div align="center">

<img src="assets/opengraph-image.png" alt="Casely — AI QA Test Case Generator: PDF requirements to TestRail-ready Excel in 8 minutes" width="720">

**Turn messy PDF requirements into TestRail-ready test cases in 8 minutes.**  
*Free, open-source AI skill for Claude Code, Cursor, and any AI IDE.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.5.0-blue.svg)](https://github.com/JohnWayneeee/casely-qa-skill/releases)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Stars](https://img.shields.io/github/stars/JohnWayneeee/casely-qa-skill?style=flat&logo=github)](https://github.com/JohnWayneeee/casely-qa-skill/stargazers)
[![Issues](https://img.shields.io/github/issues/JohnWayneeee/casely-qa-skill)](https://github.com/JohnWayneeee/casely-qa-skill/issues)
[![Casely Web](https://img.shields.io/badge/Hosted%20Version-casely.digital-ff6b6b?style=flat)](https://casely.digital/)

</div>

---

## The problem every QA engineer knows

You were hired to **find bugs**. Instead, you spend 40% of your week writing test cases.

Requirements scattered across 10 PDF files. Every project has different column names — manual reformatting every time. A single module takes 2 days to document. Then the TestRail import fails because the headers don't match.

> ❌ Requirements buried in PDF/DOCX/XLSX files with no structure  
> ❌ Each project reinvents column names — manual mapping every sprint  
> ❌ 50 test cases = 2–3 business days of repetitive writing  
> ❌ TestRail import breaks due to column mismatches  
> ❌ No coverage plan = missed edge cases and bugs reaching production  

**Every hour writing test cases is an hour not spent testing.**

---

## What Casely does

Casely is your **Virtual QA Lead**. It reads your requirements, learns your team's exact format, and writes the test cases — atomic, structured, and import-ready.

```
Requirements PDF → /parse → /style → /plan → /generate → /export → TestRail ✅
```

| Step | Command | What happens |
|------|---------|--------------|
| **Extract** | `/parse` | Docling OCR pulls tables and text from any PDF/DOCX |
| **Learn** | `/style` | Casely reads your existing Excel and clones your column structure |
| **Plan** | `/plan` | Generates a coverage map: "47 tests across 6 modules" |
| **Write** | `/generate` | Creates atomic `.md` test cases — one file per test |
| **Deliver** | `/export` | Batch-converts everything to TestRail-ready Excel |

Open `exports/functional_TC001_happy_path.xlsx` — it's a 1:1 match to your team's template, ready for immediate import.

---

## Why QA teams switch to Casely

| | Casely | Manual writing | Traditional tools |
|---|:---:|:---:|:---:|
| Parses any format (PDF/DOCX/XLSX) | ✅ | ❌ | ❌ |
| Matches **your** column structure | ✅ | ❌ | ❌ |
| Generates a test plan automatically | ✅ | ❌ | ❌ |
| 1 test case = 1 file (atomic, reviewable) | ✅ | ❌ | ⚠️ bulk only |
| TestRail / Qase ready out of the box | ✅ | ❌ | ⚠️ manual fix |
| Works with English **and** Russian docs | ✅ | ❌ | ❌ |
| Free, runs locally, no cloud lock-in | ✅ | ✅ | ❌ |

---

## ⚡ Quick Start

> **Prerequisites:** Python 3.10+ and [uv](https://github.com/astral-sh/uv)

### Option A — Skills CLI (recommended)

```bash
# with bunx
bunx skills add JohnWayneeee/casely-qa-skill

# or npx
npx skills@latest add JohnWayneeee/casely-qa-skill
```

### Option B — Clone & run

```bash
git clone https://github.com/JohnWayneeee/casely-qa-skill.git
cd casely-qa-skill
uv sync
```

Drop your files into the project folder and run the workflow:

```
/init my-project
/parse
/style
/plan
/generate functional AccountTransfer
/export
```

---

## 8-minute walkthrough

<details>
<summary><strong>Step 1 — Initialize</strong></summary>

```bash
/init my-project
```

Drop two files into `projects/my-project/input/`:
- `requirements.pdf` — your specification document
- `example.xlsx` — an existing test case file your team already uses

Casely learns your column structure from the example. No config needed.

</details>

<details>
<summary><strong>Step 2 — Parse & plan</strong></summary>

```bash
/parse    # extracts text and tables from your PDF via Docling OCR
/style    # reads your example.xlsx and clones the column structure exactly
/plan     # output: "Detected 6 modules. Recommended: 47 test cases."
```

You now have a full coverage strategy before writing a single test case.

</details>

<details>
<summary><strong>Step 3 — Generate</strong></summary>

```bash
/generate functional AccountTransfer
```

Casely writes 10+ atomic `.md` files — one per test case. Review and edit in any text editor or Git UI before exporting.

</details>

<details>
<summary><strong>Step 4 — Export</strong></summary>

```bash
/export
```

Every `.md` file becomes a separate Excel file matching your team's template exactly. Import into TestRail, Qase, or any TMS — no manual reformatting.

</details>

---

## Command reference

| Command | Action | Notes |
|---------|--------|-------|
| `/init [name]` | Scaffold project workspace | Run once per project |
| `/parse` | Extract from PDF/DOCX | High-fidelity OCR via Docling |
| `/style` | Clone your Excel column format | Reads your example — zero config |
| `/plan` | Build ISTQB-aligned coverage map | Shows module breakdown and estimates |
| `/generate [type]` | Write atomic test cases | Produces one `.md` per test |
| `/export` | Convert all `.md` to Excel | Batch output, import-ready |

Supported generation types: `functional`, `negative`, `integration`, `boundary`, `smoke`, `security`

---

## Under the hood

- **Docling Engine** — advanced OCR and table extraction for complex, multi-column PDFs including scanned documents
- **Atomic design** — 1 test case = 1 source file = 1 Excel; no monolithic spreadsheets to untangle
- **Style Guide System** — no hardcoded columns; Casely learns from your existing files and replicates the exact structure
- **Language agnostic** — generates test cases in English or Russian, matching the language of your documents

---

## Project structure

```
casely-qa-skill/
├── skill/casely/
│   ├── SKILL.md              # AI skill definition and full workflow
│   ├── scripts/
│   │   ├── casely_parser.py  # Document → Markdown converter (Docling)
│   │   └── export_to_xlsx.py # Markdown → Excel exporter
│   ├── references/           # Technical reference docs
│   └── evals/                # Evaluation test cases
├── docs/
│   └── hosted-web-version.md # Hosted version details
├── assets/                   # Images and branding
├── pyproject.toml            # Python dependencies
└── marketplace.json          # Skill marketplace metadata
```

---

## Hosted version for teams

This open-source skill runs locally in your AI IDE.

If you want a **browser UI, file uploads, team review flow, and zero local setup**:

**[casely.digital](https://casely.digital/)** — join the early access list

The hosted version is built for QA teams that want to turn requirements into review-ready test cases without writing code or running local scripts.

[Learn more about the hosted version →](docs/hosted-web-version.md)

---

## FAQ

<details>
<summary>Does it work with scanned PDFs?</summary>

Yes. Casely uses Docling's OCR pipeline, which handles scanned documents, embedded tables, and mixed-format pages.

</details>

<details>
<summary>Can I use my own Excel column structure?</summary>

That's the core feature. Drop your existing template into `input/` and run `/style`. Casely reads your column names and replicates them exactly — no configuration file needed.

</details>

<details>
<summary>Does it support Russian-language requirements?</summary>

Yes. The parser and generator work with English and Russian documents. Column names in your Excel template are preserved as-is.

</details>

<details>
<summary>Which test management systems are supported for import?</summary>

Any TMS that accepts Excel import: TestRail, Qase, Zephyr, Xray, and plain Excel. Because Casely replicates your own column structure, the output matches whatever format your team already uses.

</details>

<details>
<summary>What's the difference between the skill and the hosted version?</summary>

The skill runs locally inside your AI IDE (Claude Code, Cursor, etc.) — full control, no cloud, free forever.  
The hosted version at [casely.digital](https://casely.digital/) adds a browser UI, team review workflows, and cloud storage — no local setup required.

</details>

---

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

- 🐛 **Found a bug?** [Open an issue](https://github.com/JohnWayneeee/casely-qa-skill/issues/new?template=bug_report.md)
- 💡 **Have an idea?** [Request a feature](https://github.com/JohnWayneeee/casely-qa-skill/issues/new?template=feature_request.md)
- ⭐ **Did it help?** Star the repo — it helps other QA engineers find this tool

---

## ⭐ Star History

If Casely saved you a work week, a star helps others find it.

[![Star History Chart](https://api.star-history.com/svg?repos=JohnWayneeee/casely-qa-skill&type=Date)](https://star-history.com/#JohnWayneeee/casely-qa-skill&Date)

---

## License

[MIT](LICENSE) — free to use, modify, and distribute.

---

<div align="center">

*Made for QA engineers who were hired to find bugs, not write documents.*

**[casely.digital](https://casely.digital/) — the hosted version for teams**

</div>
