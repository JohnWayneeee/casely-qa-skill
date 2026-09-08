# 🚀 Casely — AI QA Test Case Generator

<div align="center">

<img src="assets/opengraph-image.png" alt="Casely — AI QA Test Case Generator" width="720">

<br>

Turn requirements into TestRail-ready test cases in one conversation.

<br>

Attach a PDF, DOCX, or XLSX, approve one test plan, and Casely returns:

<br>

TestRail-ready Excel files using your team’s columns.<br>
Runnable Postman collections for API specs.<br>
A list of gaps, contradictions, and untestable requirements.

<br>

Built for QA engineers who want to spend less time formatting test cases and more time finding bugs.

<br>

**Star this repo if Casely saved you a work week.**

<br>

<a href="https://github.com/JohnWayneeee/casely-qa-skill">
  <img src="https://img.shields.io/badge/Star%20Casely%20on%20GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="Star Casely on GitHub">
</a>

<br><br>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-2.2.0-blue.svg)](https://github.com/JohnWayneeee/casely-qa-skill/releases)
[![Stars](https://img.shields.io/github/stars/JohnWayneeee/casely-qa-skill?style=flat&logo=github)](https://github.com/JohnWayneeee/casely-qa-skill)
[![Web app](https://img.shields.io/badge/Web%20app-casely.digital-ff6b6b?style=flat)](https://casely.digital/)

</div>

---

## Watch it work

https://github.com/user-attachments/assets/57f086c4-ec92-4a60-bc58-a00cc9757ee0

---

## The problem

You were hired to find bugs, and 40% of your week goes into writing test cases.

Requirements land as unstructured PDFs. Projects rename the columns, so you remap them each
sprint. One module takes two days to document, and then the TestRail import fails because the
headers don't match.

---

## How it works

Attach your files and say what you need:

> "Here are the requirements for the Payments module and two example test cases my team
> writes. Give me test cases for the refund flow."

Casely runs five phases in that same conversation:

| Phase | What happens |
|-------|--------------|
| **Intake** | Reads your PDF, DOCX or XLSX attachments. No parser, no OCR setup |
| **Style guide** | Copies the column structure and tone from your example file |
| **Test plan** | Proposes coverage, flags holes in the spec, then waits for your OK |
| **Generate** | Writes the cases using boundary values, decision tables and negative paths |
| **Export** | Builds one Excel file your TMS imports in a single pass, plus a Postman collection when the requirements describe an API |

You only get interrupted once, at the plan. Adjust the scope, drop a module, add negative
cases, or say "go".

---

## API requirements get a collection you can run

When the spec names endpoints — a path and a method, an OpenAPI file, `curl` examples, status
codes, an auth section — Casely says so in the plan and, once you approve, exports the API-level
cases as a Postman collection alongside the Excel file.

```
exports/
├── all_test_cases.xlsx                          # every case, your columns
├── casely_api_collection.postman_collection.json  # the API cases as requests
├── casely_api_environment.postman_environment.json # every variable, empty
└── casely_api_collection_README.md              # import, fill in, run, read results
```

- **Everything environment-specific is a variable.** `{{baseUrl}}`, `{{authToken}}`, entity ids.
  Fill them in once and the same file runs against dev, staging, or CI. The value a case is
  actually testing — `amount: 50001` — stays literal, because that is the point of the case.
- **No credentials in the file.** The build fails on anything shaped like a JWT or a secret key,
  so the collection is safe to commit next to the test cases.
- **Assertions come from the expected result.** Status code, response fields, error codes — one
  `pm.test` per thing the requirement promises, generated rather than hand-typed.
- **Requests are named after the cases.** A red assertion in Newman maps to a row in the Excel
  file without a lookup.
- **No endpoints in the spec, no collection.** Casely asks for the API docs instead of guessing
  a path that 404s on the first run.

Run it in the Collection Runner, or in CI:

```bash
newman run exports/casely_api_collection.postman_collection.json \
  -e exports/casely_api_environment.postman_environment.json \
  --env-var "authToken=$API_TOKEN"
```

---

## Install

**Claude Code**

```bash
bunx skills add JohnWayneeee/casely-qa-skill
# or: npx skills@latest add JohnWayneeee/casely-qa-skill
```

**claude.ai and Claude desktop**

1. Get the upload archive, already zipped with `casely/` at its root:
   [download casely-v2.2.0.zip](https://github.com/JohnWayneeee/casely-qa-skill/releases/download/v2.2.0/casely-v2.2.0.zip)
   from the [latest release](https://github.com/JohnWayneeee/casely-qa-skill/releases/latest).

   Building it yourself works too — just not GitHub's own "Download ZIP" button, which wraps
   everything in `casely-qa-skill-main/skill/casely/` instead of putting `SKILL.md` at the
   archive root, which is what claude.ai requires:
   ```bash
   git clone https://github.com/JohnWayneeee/casely-qa-skill.git
   cd casely-qa-skill/skill && zip -r casely.zip casely
   ```
2. On claude.ai, open **Settings → Capabilities**, turn on **Code execution** if it isn't
   already, then go to **Skills → Create skill** and upload the zip.
3. The Claude desktop app uses the same account, so the skill is available there too —
   nothing to install separately.
4. Start a chat, attach your files, describe what you need.

Nothing to install locally. The export step uses `openpyxl`, which already ships inside
Claude's code execution environment. Custom skills are private to your account (Pro, Max,
Team, or Enterprise plan required) and won't sync to a Claude Code install — set that up
separately with the command above.

**Pick Opus.** The plan phase decides what gets tested at all: which boundaries matter,
which conditions combine, which requirement is too vague to test. Smaller models write
acceptable cases from a plan they were handed, and miss the holes in the spec.

---

## What you get

- **`exports/all_test_cases.xlsx`** with one row per case and your own column headers. Import
  it once instead of forty times.
- **`results/*.md`**, one file per case, so you can review or version-control them separately.
- **A Postman collection, an environment file and run instructions** when the requirements
  describe an API — every base URL, token and id already pulled out into variables.
- **A list of holes in the spec**: contradictions, untestable wording ("should be fast"), and
  error paths the requirements never mention.

The export refuses to write a file it cannot read faithfully. A case that reaches TestRail
without its steps costs more than a failed export, so malformed input gets named and fixed
before delivery.

---

## FAQ

<details>
<summary>Do I need to run commands?</summary>

No. Attach the files, describe what you need, and answer when Casely asks which module to
cover. The one place it pauses is the test plan.

</details>

<details>
<summary>Can I use my team's own Excel columns?</summary>

That is the point. Attach an existing test case file and Casely copies the headers, their
order and the writing style. No config file.

</details>

<details>
<summary>Does it work with Russian requirements?</summary>

Yes. Casely writes the cases in the language of your examples.

</details>

<details>
<summary>Which test management systems can import the output?</summary>

Any tool that reads Excel: TestRail, Qase, Zephyr, Xray. The columns match whatever your team
already uses.

</details>

<details>
<summary>Can it produce API tests I can actually run?</summary>

Yes, when the requirements name endpoints. Casely says in the plan how many cases are
API-level, and after your approval it exports them as a Postman collection with an environment
file and a README. Base URL, tokens and entity ids are variables you fill in once; nothing is
hardcoded, and no credential ever lands in the file. Run it in Postman or with Newman in CI.
If the spec only describes screens and flows, Casely asks for the API docs rather than
inventing endpoints.

</details>

<details>
<summary>What about scanned PDFs?</summary>

Text-based PDFs, DOCX and XLSX work well. An image-only scan with no selectable text may not
extract cleanly, so export a text version when you can.

</details>

---

## Project structure

```
casely-qa-skill/
├── skill/casely/
│   ├── SKILL.md               # the skill definition and workflow
│   ├── scripts/
│   │   ├── export_to_xlsx.py            # Markdown → Excel exporter
│   │   └── build_postman_collection.py  # API cases → Postman collection
│   ├── references/            # test design, style analysis, export and API details
│   └── evals/                 # evaluation cases
├── examples/                  # sample spec + team style file, and a scoring rubric
├── docs/hosted-web-version.md
└── marketplace.json
```

---

## Hosted version for teams

This skill runs inside your AI assistant. If your team wants a browser UI, file uploads and a
review flow with no setup, join the early access list at
**[casely.digital](https://casely.digital/)**.

[More about the hosted version →](docs/hosted-web-version.md)

---

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

- 🐛 [Report a bug](https://github.com/JohnWayneeee/casely-qa-skill/issues/new?template=bug_report.md)
- 💡 [Request a feature](https://github.com/JohnWayneeee/casely-qa-skill/issues/new?template=feature_request.md)
- ⭐ [Star the repo](https://github.com/JohnWayneeee/casely-qa-skill/stargazers) if it saved you a work week

---

## License

[MIT](LICENSE)

<div align="center">

*Made for QA engineers who find bugs. Casely writes the documents.*

</div>
