---
description: Run Casely's exported test cases in a browser through Playwright MCP and report pass, fail or blocked per case
argument-hint: "[base URL] [path to all_test_cases.xlsx or results/]"
---

# Run the test cases in a browser

Arguments: $ARGUMENTS

Walk the test cases Casely exported against a running web app and report what happened. You
are the tester at the keyboard: follow each case's steps literally, observe, and record. Do not
fix the app and do not rewrite the cases.

## Before the first case

1. **Playwright MCP must be connected.** Look for `browser_*` tools from the Playwright MCP
   server. If none are available, stop and tell the user to run, once:
   `claude mcp add playwright -- npx @playwright/mcp@latest`, then restart the session.
   Do not fall back to writing a Playwright script.
2. **Base URL.** Take it from the arguments. If missing, ask. Never guess a production URL;
   if the user gives one, confirm that running write actions (sign-ups, payments, deletes)
   there is intended.
3. **The cases.** Take the path from the arguments, else `exports/all_test_cases.xlsx`, else
   the Markdown files in `results/`. Read an `.xlsx` with `openpyxl`, never by eye.
4. **Pick what runs.** UI cases only. List the API cases (those also in the Postman
   collection) as "run with Newman" and skip them. Show the user the count and the first few
   IDs, and ask for a scope if there are more than 15 cases.
5. **Test data.** If a case needs credentials or data the case does not carry, ask once for
   all of it before starting. Never invent a password or a card number.

## Each case

1. Reset to a clean state: open the base URL in a fresh page; sign in again when the case's
   preconditions say so.
2. Satisfy the preconditions. If one cannot be met (no such user, feature flag off), mark the
   case **Blocked** with the reason and move on.
3. Perform each step with the Playwright tools. Take a snapshot after the step that carries
   the expected result.
4. Compare what the page shows with the expected result, literally. Close enough is a fail
   with a note, not a pass.
5. Record: ID, result (**Pass**, **Fail**, **Blocked**), and for a fail what the page showed
   instead and at which step. Save a screenshot for every fail and block under
   `run/screenshots/<ID>.png`.

## Report

Write `run/run_report.md`: date, base URL, a summary line (e.g. 12 pass, 2 fail, 1 blocked),
then a table with ID, Title, Result, Notes, Screenshot. Show the summary and the failed and
blocked rows in the chat, and offer to turn each failure into a bug report in the team's
format with `/casely:bug <ID>`.

Keep generated artefacts clean: no promotional notes inside the report.
