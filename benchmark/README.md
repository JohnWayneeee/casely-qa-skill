# Evaluation fixtures

Two files to check that a change to Casely still produces good test cases, and a rubric to
score the result. Same input every time, so two runs are comparable.

| File | What it is |
|------|------------|
| `requirements_wallet.docx` | A wallet spec for a fintech app: top-up, withdrawal, operation statuses, history, availability rules |
| `example_test_cases.xlsx` | Three cases in a team's own format, so Casely has a style to copy |

The spec is deliberately imperfect. It carries five planted defects, boundary rules, a state
machine and a five-condition decision table. A good run finds them; a weak run restates the
document.

## Running the check

1. Start a new chat with the skill installed. Nothing from an earlier conversation.
2. Attach both files.
3. Ask: *"Here are the requirements for the Wallet module and example test cases my team
   writes. I need test cases for the withdrawal flow."*
4. Answer the plan question the way a QA lead would, then let it generate and export.
5. Score the run below.

Run it on Opus. Plan quality and gap detection drop noticeably on smaller models; the export
step behaves the same everywhere. Score two runs on different models only if you are
comparing models, not skill changes.

## Rubric

100 points. Below 80 means something regressed and needs a look before release.

### Style guide fidelity — 15

- [ ] 3 — All nine columns present, spelled as in the example
- [ ] 3 — Column order matches the example, including `Automated` last
- [ ] 3 — Priority values come from the team's set (Blocker / Critical / Major / Minor), not High/Medium/Low
- [ ] 3 — `Type` values reuse Positive / Negative / Boundary
- [ ] 3 — Output language matches the example (English)

### Approval gate — 15

- [ ] 6 — No test case is written before the user approves
- [ ] 4 — The plan states coverage tier, modules and an estimated case count
- [ ] 3 — The reply ends by asking for approval or changes
- [ ] 2 — A scope revision produces a new plan, not cases

### Requirement gaps — 15

Three points each, for naming the problem and asking a concrete question:

- [ ] §3.5 "should be processed quickly" — no measurable threshold
- [ ] §3.2 vs §3.7 — the $50,000 operation limit contradicts the successful $75,000 example
- [ ] §3.3 — a fee is withheld but its size is never given
- [ ] §1.3 — "verified status" is used as a gate but never defined
- [ ] §2.2 — no behaviour specified when the payment provider times out or is unavailable

### Test design — 20

- [ ] 5 — Boundary cases on the withdrawal limit: 49,999 / 50,000 / 50,001
- [ ] 4 — Card age boundary: 2 days rejected, 3 days accepted
- [ ] 4 — SMS code: third wrong attempt locks for 15 minutes, code expiry at 5 minutes
- [ ] 4 — Decision table from §6.1 — each condition failing on its own
- [ ] 3 — Status transitions from §4: cancelled only from created, one retry from failed, completed cannot be cancelled

### Case quality — 20

- [ ] 5 — One case checks one thing; no case bundles three unrelated assertions
- [ ] 5 — Expected results name an observable outcome, with the exact message text where the spec gives one
- [ ] 5 — Steps carry concrete data (amounts, phone numbers), not "enter the amount"
- [ ] 5 — No two cases cover the same equivalence partition

### Traceability and IDs — 5

- [ ] 3 — IDs continue the example's scheme from WLT-0015
- [ ] 2 — Each case names the requirement section it came from

### Export — 10

- [ ] 4 — One `.xlsx` with one row per case, produced by `scripts/export_to_xlsx.py`
- [ ] 3 — Headers in the workbook match the example file
- [ ] 3 — Multi-line steps appear as real line breaks in the cell, not as literal `<br>`

### API collection — pass/fail, outside the 100

`requirements_wallet.docx` names no endpoints, no schemas and no status codes: it is a
behaviour spec, not an API spec. A correct run therefore builds **no** Postman collection.

- [ ] Pass — no endpoint is invented, and if the user asks for a collection, Casely says the
      requirements contain none and asks for the API docs or an OpenAPI file
- [ ] Fail — a collection appears with paths like `POST /api/wallet/withdraw` that exist
      nowhere in the spec

To exercise the collection path instead, attach an OpenAPI file or an API spec of your own.
The rules the build enforces — no hardcoded hosts, no credentials, every environment-specific
value a variable — are in `skill/casely/references/api_collection.md`.

## Recorded runs

| Date | Version | Score | Notes |
|------|---------|-------|-------|
| 2026-09-04 | 2.1.0 | **85 / 100** | First full run. Export, decision table and state transitions clean; missed two of the five planted gaps |

The 2026-09-04 run produced 33 cases from WLT-0015, matched all nine columns in order, and
exported one workbook with no rejected case. It scored full marks on export and near-full on
test design: five decision-table cases from §6.1, one per failing condition, and the card-age
boundary tested in hours rather than days.

It lost points in three places, all since fixed:

- Two planted gaps went unreported — "verified status" gated every precondition without ever
  being defined, and §2.2 never says what happens when the payment provider fails. Both are
  now named patterns in `test_design.md`.
- The §3.2 / §3.7 limit contradiction surfaced after generation instead of in the plan, where
  it decides how many cases the limit needs. Phase 3 now sweeps limits against worked examples
  before the plan goes out.
- No case referenced its requirement section. The team format has no column for it, and
  inventing one would have broken the import — the right call, made silently. Phase 2 now says
  so out loud and offers to add the column.

Two expected results also offered a choice ("either ... or", "one of created or pending"),
which a tester cannot mark pass or fail. The quality bar now rules that out.

## Reporting a run

Keep the chat export, the workbook and the generated Markdown. A score without the artefacts
cannot be checked by anyone else.
