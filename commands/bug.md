---
description: Write a bug report in your team's format from a trace ID, a monitoring link, pasted logs or a failed case, with personal data masked
argument-hint: "[trace or event ID, monitoring URL, failed case ID, or a short description]"
---

# Write a bug report

Arguments: $ARGUMENTS

Read `${CLAUDE_PLUGIN_ROOT}/skills/casely/references/bug_report.md` and follow it step by step
for the evidence in the arguments.

Hold to three rules from that file even if it fails to load:

1. **Read only.** Monitoring and tracker tools are used to get, list and search. Never resolve,
   assign, comment on, create or delete anything. The user files the bug.
2. **Mask first.** Tokens, emails, phone numbers, names, user and account ids, IP addresses and
   payment data never reach the report. The trace ID and the monitoring link stay.
3. **No guessing.** A field the evidence does not support says `unknown` and names who can answer.
