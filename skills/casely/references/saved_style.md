# Saved style (`casely-style.md`)

A team attaches its example test cases once. Casely turns them into this file, and later
conversations read the file instead of asking for the example again (SKILL.md, Phase 1 step 5
and Phase 2 step 7).

## Where it lives

| Surface | Location | Who keeps it |
|---|---|---|
| Claude Code | `.casely/style.md` in the project root | Casely writes and updates it |
| claude.ai | Project knowledge, as `casely-style.md` | The user uploads the delivered file |
| Cowork | The working folder, as `casely-style.md` | Casely writes it there |
| Desktop chat | Attached to the next conversation | The user keeps the delivered file |

## Format

Keep the headings and their order. Casely reads the file by these headings.

````markdown
# Casely style

Saved: 2026-10-25 from TC_examples.xlsx

## Columns
ID | Title | Preconditions | Steps | Expected Result | Priority | Requirement

## IDs
Scheme: PAY-NNN
Last ID used: PAY-042

## Language and tone
Language: Russian
Preconditions: numbered list
Steps: imperative, one action per step, `<br>` between steps
Expected result: one sentence per check, present tense
Priority values: High, Medium, Low

## Requirement column
Requirement: Jira issue key (PAY-142)

## Example row
| PAY-001 | Login with a valid email | 1. A user <user email> exists | 1. Open /login<br>2. Enter <user email> and <password> | The dashboard opens | High | PAY-12 |
````

## Rules

- **Headers exactly as the example has them,** in the same order, including ones that look
  redundant. The TMS import is mapped to them.
- **One example row, with placeholders.** Replace names, emails, phones, customer and company
  names, account ids, tokens and internal URLs: `<user email>`, `<customer>`, `<token>`. Keep
  the shape of the data (a boundary like `50 001` stays) and drop the identity.
- **No requirements text, no test data sets, no credentials.** The file holds the format only.
- **`Requirement column`** is `none` when the team format has no reference column.
- **Updating.** A new example that changes columns needs the user's yes before the file
  changes. In Claude Code, update `Last ID used` after each export; nothing else changes
  without the user asking.
