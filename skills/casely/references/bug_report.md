# Bug report from a trace ID or a failed case

Casely writes one bug report in the team's own format from evidence: a trace or event ID, a
monitoring link, pasted logs, or a failed case from `run/run_report.md`. It never files the bug
itself. The user files it.

## Contents
- 1. Input
- 2. The team's bug format
- 3. Evidence from monitoring
- 4. Mask before writing
- 5. Write the report
- 6. Deliver
- Saved bug style format

## 1. Input

Take what the user gave: a trace ID, an event or issue ID, a monitoring URL, a description,
pasted log lines, or a case ID from the last browser run. Several bugs at once: write them one
by one, one file each. Nothing to go on: ask for one of these, in one question.

## 2. The team's bug format

1. **Saved style first.** Look for `.casely/bug-style.md` in the project (Claude Code), or a
   `bug-style.md` that is attached, in the Project knowledge (claude.ai) or in the working folder
   (Cowork). Found: use it and say so in one line.
2. **No saved style:** ask once for one to three bug reports the team already filed (export,
   screenshot or pasted text). Copy the field names and their order exactly, the title pattern,
   the severity and priority values, and the tone. Read `.xlsx` or `.csv` with code, not by eye.
3. **No examples:** use this default and say so: Title, Environment, Steps to reproduce, Expected
   result, Actual result, Severity, Evidence, Notes.
4. **Offer once to save the format** (format at the end of this file). Real data from the
   examples never goes into the saved file: names, emails, phones, customer names, user and
   account ids, tokens, internal hostnames become placeholders (`<user email>`, `<host>`). A new
   example that changes the fields needs the user's yes before the saved file changes.

## 3. Evidence from monitoring

1. **Find a read tool.** Look at the connected MCP tools for the monitoring system the team uses:
   GlitchTip, Sentry, Datadog, Grafana, Jaeger or another tracing tool, or the company's own
   server. Use only tools that get, list or search. Never resolve, assign, mute, comment on or
   delete an event, even when the tool allows it and the user asks: the event belongs to the
   team's triage.
2. **Fetch by the ID.** Get the event or trace: error type and message, stack trace (top frames
   in the app's own code), request method, path and status, release or version, environment,
   browser or OS, timestamp, and the breadcrumbs or spans before the error.
3. **No tool, or no access.** Many testers get no monitoring access. Ask the user to paste the
   event JSON, the log lines around the timestamp, or an export, and work from that. Never ask
   for a monitoring API token or a password in the chat.
4. **A failed case from `/casely:run`.** Use the case's steps and expected result, what the page
   showed, and the screenshot path from `run/run_report.md`.
5. **Duplicates.** If the Atlassian tools are connected, run one read-only JQL search for open
   bugs with the same error message or endpoint, and list matches with their keys. Don't decide
   it is a duplicate; let the user decide.

Never fill a gap by guessing. A field the evidence does not support says `unknown` and names
who can answer it ("ask the backend team for the release").

## 4. Mask before writing

Before any evidence goes into the report, replace:

| Data | Replace with |
|---|---|
| Bearer tokens, JWTs, API keys, cookies, session ids, passwords | `<token>` |
| Emails, phone numbers, personal names | `<user email>`, `<phone>`, `<name>` |
| User, account and customer ids | `<user id>` |
| IP addresses | `<ip>` |
| Card numbers and other payment data | `<card>` |

Keep the trace or event ID and the monitoring link: developers need them, and they reveal
nothing about the user. Keep the shape of the data that matters (`amount: 50001` stays).

## 5. Write the report

- **Title** in the team's pattern. Default: where, what, under which condition
  ("Withdrawal: 500 on POST /v1/withdrawals when amount equals the daily limit").
- **Steps to reproduce** from the failed case or from the breadcrumbs and request. Steps taken
  from a trace and not reproduced by a person get the note "steps inferred from the trace, not
  reproduced".
- **Expected result** from the requirement or the test case when one is known; otherwise ask.
  Never invent the expected behaviour.
- **Actual result**: what happened, with the status code and error message.
- **Environment**: environment, release, browser or OS, timestamp with timezone.
- **Severity and priority** only if the team's format has them, using the team's values, with
  one line of reason. The user can change them.
- **Evidence**: trace or event link, at most 20 masked log lines, screenshot path.

## 6. Deliver

Save the report as `bugs/<trace-or-case-id>_<short_title>.md` and show it in the chat. In
claude.ai and Cowork, deliver the file. Say that the user files it in their tracker: Casely
does not create issues. No promotional note inside the report.

## Saved bug style format

````markdown
# Casely bug style

Saved: 2026-10-25 from 3 example reports

## Fields
Title | Environment | Steps to reproduce | Expected result | Actual result | Severity | Evidence

## Title pattern
<Module>: <what fails> when <condition>

## Values
Severity: Blocker, Critical, Major, Minor
Language: English

## Example
Title: Login: 500 on POST /auth/login when the password has 64 characters
Environment: staging, release <version>, Chrome 130
Steps to reproduce: 1. Open /login<br>2. Enter <user email> and a 64-character password<br>3. Press Sign in
Expected result: The dashboard opens
Actual result: 500 Internal Server Error
Severity: Major
Evidence: <trace link>
````
