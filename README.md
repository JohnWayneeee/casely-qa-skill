# 🚀 Casely — AI QA Test Case Generator

<div align="center">

<img src="assets/opengraph-image.png" alt="Casely — AI QA Test Case Generator: attach requirements, get TestRail-ready Excel" width="720">

**Attach your requirements. Get TestRail-ready test cases back. No commands to learn.**  
*Free, open-source AI skill for Claude Code, claude.ai, and the Claude desktop app.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/JohnWayneeee/casely-qa-skill/releases)
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

Casely is your **Virtual QA Lead**. You don't run commands or set up a project — you attach
files and say what you need, in plain language, in one conversation:

> "Here's the spec for the Payments module and a couple of test cases my team already writes.
> Give me test cases for the refund flow."

Casely reads the attachments, learns your team's exact format, plans coverage, **checks in
with you once on the plan before writing anything**, then generates atomic test cases and
exports them to Excel.

```
Attach requirements + examples → Casely plans coverage → you approve → test cases + Excel ✅
```

| Phase | What happens |
|-------|--------------|
| **Intake & scope** | Casely reads your PDF/DOCX/XLSX attachments directly — no parsing step, no OCR setup |
| **Style guide** | Reads your example test cases and clones the column structure exactly |
| **Test plan** | Proposes a coverage map — "47 tests across 6 modules" — and **waits for your OK** |
| **Generate** | Writes atomic `.md` test cases — one file per test — only after you approve |
| **Export** | Converts everything to TestRail-ready Excel |

This works the same way whether you're in Claude Code, claude.ai in the browser, or the Claude
desktop app — because it's just a conversation.

---

## Why QA teams switch to Casely

| | Casely | Manual writing | Traditional tools |
|---|:---:|:---:|:---:|
| Reads any format (PDF/DOCX/XLSX) — no setup | ✅ | ❌ | ❌ |
| Matches **your** column structure | ✅ | ❌ | ❌ |
| Plans coverage and waits for your approval | ✅ | ❌ | ❌ |
| 1 test case = 1 file (atomic, reviewable) | ✅ | ❌ | ⚠️ bulk only |
| TestRail / Qase ready out of the box | ✅ | ❌ | ⚠️ manual fix |
| Works with English **and** Russian docs | ✅ | ❌ | ❌ |
| No commands, no project scaffolding | ✅ | ✅ | ❌ |
| Free, runs locally, no cloud lock-in | ✅ | ✅ | ❌ |

---

## ⚡ Quick Start

### Claude Code

```bash
# with bunx
bunx skills add JohnWayneeee/casely-qa-skill

# or npx
npx skills@latest add JohnWayneeee/casely-qa-skill
```

Then, in any project:

> "Casely, here are the requirements for AccountTransfer and our existing test cases —
> generate functional test cases for the happy path."

Attach the files in the same message. That's the whole workflow — Casely asks anything else it
needs to know.

### claude.ai (web) and Claude desktop

1. Download the skill from this repository (or clone it) and zip the `skill/casely/` folder.
2. In claude.ai, go to **Settings → Features → Skills** and upload the zip.
3. Start a chat, attach your requirements (and example test cases, if you have any), and
   describe what you need — Casely triggers automatically.

> **Prerequisites:** none for claude.ai/desktop. For Claude Code, Python 3.10+ and
> [uv](https://github.com/astral-sh/uv) are used for the Excel export step
> (`uv sync` from the repo root).

---

## 8-minute walkthrough

<details>
<summary><strong>Step 1 — Attach and ask</strong></summary>

Attach your requirements document and, if you have one, an example test case file your team
already uses. Say what you need:

> "Requirements for AccountTransfer attached, plus an example XLSX. Generate functional test
> cases for the happy path."

No `/init`, no folder setup — Casely reads the files in the same message.

</details>

<details>
<summary><strong>Step 2 — Casely scopes and learns your style</strong></summary>

If the requirements cover multiple features and you didn't say which one, Casely lists what it
found and asks which to cover. It then reads your example file and clones its column structure
and tone exactly — no config file, no manual mapping.

</details>

<details>
<summary><strong>Step 3 — Approve the plan</strong></summary>

Casely proposes a coverage plan: "Detected 6 modules. Recommended: 47 test cases across smoke,
critical, and full tiers." **It waits here** — adjust scope, add or drop a module, change test
types, or just say "go."

</details>

<details>
<summary><strong>Step 4 — Generate and export</strong></summary>

Once you approve, Casely writes one atomic `.md` file per test case, then converts each one to
a matching `.xlsx` file — ready to import into TestRail, Qase, or any TMS, with your exact
column headers.

</details>

---

## Under the hood

- **Native document reading** — Claude reads PDF/DOCX/XLSX attachments directly; no bundled
  parser, no OCR dependency, nothing extra to install
- **One approval gate** — the workflow only stops once, on the test plan, so you stay in
  control without babysitting every step
- **Atomic design** — 1 test case = 1 source file = 1 Excel file; no monolithic spreadsheets to
  untangle
- **Style Guide System** — no hardcoded columns; Casely learns from your existing files and
  replicates the exact structure
- **Language agnostic** — generates test cases in English or Russian, matching the language of
  your documents

---

## Project structure

```
casely-qa-skill/
├── skill/casely/
│   ├── SKILL.md               # AI skill definition and full workflow
│   ├── scripts/
│   │   └── export_to_xlsx.py  # Markdown → Excel exporter
│   ├── references/            # Technical reference docs
│   └── evals/                 # Evaluation test cases
├── docs/
│   └── hosted-web-version.md  # Hosted version details
├── assets/                    # Images and branding
├── pyproject.toml             # Python dependencies
└── marketplace.json           # Skill marketplace metadata
```

---

## Hosted version for teams

This open-source skill runs inside your AI assistant — Claude Code, claude.ai, or desktop.

If you want a **browser UI, file uploads, team review flow, and zero local setup**:

**[casely.digital](https://casely.digital/)** — join the early access list

The hosted version is built for QA teams that want to turn requirements into review-ready test cases without writing code or running local scripts.

[Learn more about the hosted version →](docs/hosted-web-version.md)

---

## FAQ

<details>
<summary>Does it work with scanned PDFs?</summary>

Casely relies on Claude's native document reading, which handles standard PDF/DOCX/XLSX text
and tables. A scanned PDF with no selectable text (image-only) may not extract cleanly —
prefer a text-based export of the document when possible.

</details>

<details>
<summary>Can I use my own Excel column structure?</summary>

That's the core feature. Attach your existing example test case file when you start the
conversation. Casely reads your column names and replicates them exactly — no configuration
file needed.

</details>

<details>
<summary>Does it support Russian-language requirements?</summary>

Yes. Casely works with English and Russian documents and generates test cases in the same
language as your examples.

</details>

<details>
<summary>Which test management systems are supported for import?</summary>

Any TMS that accepts Excel import: TestRail, Qase, Zephyr, Xray, and plain Excel. Because
Casely replicates your own column structure, the output matches whatever format your team
already uses.

</details>

<details>
<summary>Do I need to run any commands?</summary>

No. Attach your files and describe what you need — Casely triggers automatically and asks for
anything else it needs. The only point where it stops and waits for you is the test plan,
before it writes any test cases.

</details>

<details>
<summary>What's the difference between the skill and the hosted version?</summary>

The skill runs inside your AI assistant (Claude Code, claude.ai, desktop) — full control, free
forever. The hosted version at [casely.digital](https://casely.digital/) adds a browser UI,
team review workflows, and cloud storage — no local setup required.

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
