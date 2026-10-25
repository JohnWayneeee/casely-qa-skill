# Connectors: Jira, Confluence and read-only setup

## Contents
- Reading Jira and Confluence (for Casely)
- What Casely uses
- 1. Atlassian admin: allow read and search only
- 2. Claude Code: deny the write tools
- 3. claude.ai, Cowork and the desktop app
- Other connectors

## Reading Jira and Confluence

The plugin ships Atlassian's remote MCP server (`.mcp.json`). The user signs in once on
Atlassian's own OAuth page. If the Atlassian tools are not available in this session, ask the
user to connect Atlassian, or to paste or export the text. Never ask for an API token or a
password in the chat.

- **One issue.** Read the issue, its acceptance criteria and its linked issues. Use the issue
  key as the requirement reference (SKILL.md, Phase 2 step 5).
- **An epic, a sprint or a filter.** Find the issues with one JQL search (`parent = PAY-100`,
  `sprint in openSprints() AND project = PAY`). List the keys and titles you found, with the
  count, and ask which to cover before you read them all. Twenty issues read without asking
  cost the user context and time they may not have wanted to spend.
- **A Confluence page.** Read the page the user named. Read its child pages only when the user
  asks, or when the page says the details live there.
- **Read only, always.** Never create, edit, comment on, transition, link or delete anything,
  even when the tools allow it and the user asks. If the user wants the cases in Jira, give them
  the export to import and say why in one line: an agent that writes to the team's tracker can
  overwrite work nobody can restore. Offer the setup below if write tools are visible.

The rest of this file is advice for the user. A rule in a prompt is not a lock, so the user
gives the connector read access only. Then a mistake by the agent cannot change the tracker.

## What Casely uses

Atlassian splits the tools of its remote MCP server into permission groups
([supported tools](https://support.atlassian.com/atlassian-rovo-mcp-server/docs/supported-tools/),
checked 2026-10-25):

| Group | Casely needs it | Examples |
|---|---|---|
| `read_jira`, `read_confluence` | Yes | `getJiraIssue`, `getConfluenceContent` |
| `search_jira`, `search_confluence` | Yes | `searchJiraIssuesUsingJql`, `searchConfluence` |
| `write_jira`, `write_confluence` | No | `createJiraIssue`, `editJiraIssue`, `updateConfluenceContent` |
| `delete_jira`, `manage_jira` | No | Off by default in Atlassian |

## 1. Atlassian admin: allow read and search only

An organization admin opens Atlassian Administration, the Rovo MCP server settings, the
Permissions tab, and leaves only the read and search groups on
([Atlassian docs](https://support.atlassian.com/security-and-access-policies/docs/configure-atlassian-mcp-server-permissions/)).
This covers every client: Claude Code, claude.ai, Cowork, the desktop app.

## 2. Claude Code: deny the write tools

Without admin rights, block the write tools on your own machine. Add this to
`.claude/settings.json` in the project, or to `~/.claude/settings.json` for every project.
A denied tool is removed from Claude's context, so the agent cannot call it.

```json
{
  "permissions": {
    "deny": [
      "mcp__plugin_casely_atlassian__create*",
      "mcp__plugin_casely_atlassian__edit*",
      "mcp__plugin_casely_atlassian__update*",
      "mcp__plugin_casely_atlassian__transition*",
      "mcp__plugin_casely_atlassian__add*",
      "mcp__plugin_casely_atlassian__manage*",
      "mcp__plugin_casely_atlassian__delete*",
      "mcp__plugin_casely_atlassian__upload*",
      "mcp__plugin_casely_atlassian__set*",
      "mcp__plugin_casely_atlassian__copy*",
      "mcp__plugin_casely_atlassian__move*",
      "mcp__plugin_casely_atlassian__archive*",
      "mcp__plugin_casely_atlassian__unarchive*",
      "mcp__plugin_casely_atlassian__restore*",
      "mcp__plugin_casely_atlassian__convert*",
      "mcp__plugin_casely_atlassian__remove*",
      "mcp__plugin_casely_atlassian__replace*",
      "mcp__plugin_casely_atlassian__enable*",
      "mcp__plugin_casely_atlassian__disable*",
      "mcp__plugin_casely_atlassian__complete*",
      "mcp__plugin_casely_atlassian__reopen*",
      "mcp__plugin_casely_atlassian__watch*",
      "mcp__plugin_casely_atlassian__unwatch*",
      "mcp__plugin_casely_atlassian__star*",
      "mcp__plugin_casely_atlassian__unstar*"
    ]
  }
}
```

- Every read and search tool starts with `get`, `list`, `lookup`, `search`, `download`,
  `export`, `resolve` or `diff`, so none of them is blocked.
- `mcp__plugin_casely_atlassian__` is the name Claude Code gives the server the plugin ships.
  If you added Atlassian yourself (`claude mcp add atlassian ...`), the prefix is
  `mcp__atlassian__`.
- Atlassian adds tools over time. Compare the list above with the supported tools page when you
  update the plugin.

## 3. claude.ai, Cowork and the desktop app

These apps don't read `settings.json`. Use the admin setting from step 1. If the connector
settings let you switch off single tools, switch off the write tools.

## Other connectors

The same rule holds for a test management system, a monitoring tool or a wiki: give Casely a
read-only token or a read-only role, and deny the write tools in Claude Code the same way.
