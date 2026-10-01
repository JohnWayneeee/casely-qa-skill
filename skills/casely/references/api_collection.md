# API Collection — turning API test cases into a runnable Postman collection

Read this when the requirements describe an API. It covers three things: how to
tell an API feature from a UI one, how a written test case becomes a request,
and what belongs in a variable instead of in the request.

## Contents

- [When Casely offers a collection](#when-casely-offers-a-collection)
- [The request spec format](#the-request-spec-format)
- [From a test case to a request](#from-a-test-case-to-a-request)
- [Variables: what gets extracted and why](#variables-what-gets-extracted-and-why)
- [Assertions](#assertions)
- [Chaining requests](#chaining-requests)
- [Building and validating](#building-and-validating)
- [What the user receives](#what-the-user-receives)

---

## When Casely offers a collection

A Postman collection is only worth building when the requirements carry enough
to make a request that actually fires. Decide from the spec, not from the word
"API" appearing somewhere in it.

**Strong signals — one is enough:**

- Endpoints written as method + path (`POST /v1/wallet/withdraw`).
- An OpenAPI/Swagger file, a Postman collection, or `curl` examples attached.
- Request/response bodies, JSON schemas, or field tables per endpoint.
- Documented status codes and error codes (`422 LIMIT_EXCEEDED`).
- An auth section: bearer tokens, API keys, OAuth scopes, signed headers.

**Weak signals — need at least two, plus a real path somewhere:**

- The user asked for "API tests", or the example test cases have API-level rows.
- The style guide has columns like `Endpoint`, `Method`, `Request`, `Response`.
- Rate limits, idempotency keys, pagination, webhooks, HTTP headers.
- The plan's Level column says API for one or more modules.

**Do not build a collection when:**

- The spec describes screens and flows and never names an endpoint. Guessing
  `POST /api/login` from "the user logs in" produces a collection that 404s on
  first run and costs more trust than it saves. Say what is missing instead:
  "the requirements describe the flows but no endpoints — send me the API docs
  or an OpenAPI file and I'll add a runnable collection."
- Only some modules are API-level. Then build the collection from those modules
  only, and say which cases it covers and which stayed manual.

**Where this gets decided:** name it in the **Phase 3 plan**, inside the same
approval the user already gives — "12 of the 18 cases are API-level, so I'll
also produce a Postman collection for those." The user can decline there. Never
surprise them with an extra artifact after the fact, and never make the
collection the reason to skip the Excel export: the collection is an addition
to the test cases, never a replacement for them.

---

## The request spec format

Phase 4 writes one `.json` file per API case into a working `api/` folder,
alongside the Markdown case in `results/`. The build script assembles them —
hand-writing collection JSON invites a schema mistake that Postman rejects on
import, and hand-writing assertion JavaScript invites a typo that makes a
broken endpoint pass.

Name each file `{id}_{short_description}.json`, matching the Markdown case.

```json
{
  "id": "API-001",
  "title": "Withdrawal within the daily limit is accepted",
  "folder": "Wallet / Withdrawal",
  "method": "POST",
  "path": "/v1/wallets/{{walletId}}/withdraw",
  "query": [{ "key": "dry_run", "value": "false" }],
  "headers": [{ "key": "Content-Type", "value": "application/json" }],
  "auth": "inherit",
  "body": {
    "mode": "raw",
    "raw": "{\n  \"amount\": 49999,\n  \"currency\": \"USD\"\n}"
  },
  "expect": {
    "status": 201,
    "jsonPath": [
      { "path": "data.status", "equals": "PENDING" },
      { "path": "data.id" }
    ]
  },
  "saveFromResponse": [{ "var": "withdrawalId", "path": "data.id" }],
  "requirement": "REQ-004",
  "preconditions": "Wallet {{walletId}} holds more than 50 000 USD.",
  "variables": [
    { "key": "walletId", "description": "Id of a funded test wallet" }
  ]
}
```

| Field | Required | Notes |
|-------|----------|-------|
| `id` | yes | The test case id. One id, one request, one scenario. |
| `title` | yes | The case title. Becomes the request name with the id. |
| `method` | yes | Any HTTP method. |
| `path` | yes | Path only, starting with `/`. The builder prepends `{{baseUrl}}`. |
| `folder` | no | `Module / Submodule`, nested with `/`. Groups the run. |
| `query` | no | `{key, value, description}`. Values may be `{{variables}}`. |
| `headers` | no | Content type, idempotency keys, locale. Never credentials. |
| `auth` | no | `inherit` (default), `none`, `bearer`, `apikey`. |
| `body` | no | `{mode: "raw", raw: "..."}`, or `formdata` / `urlencoded`. |
| `expect` | no | Drives the generated assertions — see below. |
| `saveFromResponse` | no | `{var, path}` — chains a value into later requests. |
| `preRequest` | no | Extra JavaScript lines, when setup genuinely needs them. |
| `tests` | no | Extra assertion lines the `expect` block cannot express. |
| `requirement` | no | Requirement or section id. Keeps traceability in Postman. |
| `preconditions` | no | Shown in the request description, for whoever runs it. |
| `variables` | no | `{key, value, description}` for the variables this case introduces. |

---

## From a test case to a request

The collection is the same suite in an executable form, not a second suite.
Keep them aligned:

- **One case, one request.** A case that needs three calls to set up its state
  is either three cases, or one request plus a `preRequest` script — decide the
  same way the atomicity rule in `test_design.md` decides it.
- **The negative cases matter most here.** A collection of happy paths proves an
  endpoint answers, not that it validates. Every boundary and error case in the
  plan gets a request: `50000` and `50001`, missing token, malformed JSON,
  wrong content type, unknown id.
- **Same ids, same order.** The request name is `{id} — {title}`, so a red
  assertion in Newman maps to a row in the Excel file without a lookup.
- **Cases that cannot be automated stay manual.** A case whose expected result is
  an email arriving or a screen rendering does not become a request. Leave it in
  the Markdown suite and say so.

---

## Variables: what gets extracted and why

A collection with a host and a token baked into it works on one machine, for one
week, for one person. Everything that changes between environments, runs, or
people is a variable.

**Always variables:**

| Variable | Holds |
|----------|-------|
| `baseUrl` | API root, no trailing slash. The builder adds this to every path. |
| `authToken` | Bearer token. Set as collection-level auth; requests inherit it. |
| `apiKey` | API key, when the spec authenticates that way instead. |

**Also variables:** any id the requests operate on (`walletId`, `orderId`,
`userId`), tenant or account ids, test user credentials, callback URLs, and any
value the spec says differs per environment.

**Not variables:** the values a case is actually testing. `amount: 50001` is the
boundary under test — parameterizing it hides what the case checks.

Rules the builder enforces, so keep to them from the start:

1. **No hardcoded hosts.** Write `/v1/orders`, never `https://api.prod…/v1/orders`.
   A path that names production is a collection someone runs against production.
2. **No real credentials, anywhere.** No token in a header, a body, or a variable
   default. The build fails on anything shaped like a JWT, an `sk-` key, or a long
   hex secret. Tokens are the user's to paste in, or to pass from CI.
3. **Every variable is declared.** Anything written as `{{name}}` lands in the
   environment file with an empty value and a description, so the user has one
   checklist to fill in rather than a scavenger hunt through requests.

---

## Assertions

Assertions are generated from `expect`, not hand-written, so they say exactly
what the test case's expected result says.

| Key | Produces |
|-----|----------|
| `status` | `pm.response.to.have.status(201)` |
| `jsonPath[].equals` | nested property equals a value |
| `jsonPath[].contains` | nested property contains a substring |
| `jsonPath[].type` | nested property is a `string`/`number`/`array`/`object` |
| `jsonPath[]` (path only) | the field is present |
| `headers[]` | a response header is present, or equals a value |
| `bodyContains[]` | the raw body includes a string |
| `maxResponseTimeMs` | response time is below a stated budget |

The quality bar from `test_design.md` applies unchanged. An expected result of
"returns an error" gives you `expect.status` and nothing else, which asserts
almost nothing — go back to the spec for the status code and the error code. If
the spec does not state them, that is a gap to report, not a value to invent.

Add `maxResponseTimeMs` only where the requirements state a budget. A number
you made up turns into a flaky test on someone's CI.

---

## Chaining requests

Some cases need an entity that another case creates. Two ways, in order of
preference:

1. **`saveFromResponse`** on the creating case, `{{var}}` in the dependent one.
   The builder writes `pm.collectionVariables.set(...)`, and the runner passes
   the value forward. Put both in the same folder, creation first — the runner
   executes in file order.
2. **A variable the user fills in** (`walletId`) when the entity has to exist
   beforehand. It lands in the environment file with a description saying what
   kind of record it needs to be.

Independence still holds as a goal: a request that only passes because another
one ran first is fragile, so chain when the API leaves no alternative, and use a
pre-existing fixture when it does.

---

## Building and validating

```bash
python <skill-path>/scripts/build_postman_collection.py api exports \
  --collection-name "Wallet API Tests" --slug wallet_api
```

- `api` — directory of request specs (default `api`)
- `exports` — output directory (default `exports`)
- `--collection-name` — what the collection is called in Postman
- `--slug` — file name stem (default `casely_api`)
- `--no-readme` — skip the run instructions

Like the Excel exporter, it refuses rather than mangles. A non-zero exit names
the file and the reason: invalid JSON, a missing field, a method that is not a
method, a duplicated case id, a hardcoded host, a credential-shaped string.
Fix the spec and run it again — never hand over a collection whose build
reported failures.

---

## What the user receives

Three files in `exports/`:

- `<slug>_collection.postman_collection.json` — schema v2.1, imports into
  Postman, Insomnia (via import), and runs under Newman.
- `<slug>_environment.postman_environment.json` — every variable, empty, with
  secrets typed as secrets so Postman keeps them out of shared exports.
- `<slug>_collection_README.md` — import, fill in, run, read the results,
  including a ready Newman command for CI.

Tell them what to do in one line rather than making them open the README to find
out there is something to do: "Import both files, fill in `baseUrl` and
`authToken` in the environment, then Run. The README has the Newman command for
CI." Delivering a collection whose variables are empty without saying they are
empty reads as a broken export.
