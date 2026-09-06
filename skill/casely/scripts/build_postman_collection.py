"""
Casely API Export — turns generated API test cases into a Postman collection.

Phase 4 writes one small JSON request spec per API test case (see
references/api_collection.md). This script assembles them into a single
Postman v2.1 collection the user imports once and runs with the Collection
Runner or Newman, plus an environment file holding the variables they need to
fill in, plus a short README telling them what to do with both.

Everything that changes between environments — the base URL, tokens, account
ids, test data — is emitted as a {{variable}}, never as a literal. The script
refuses to write a collection that carries a real-looking credential or a
hardcoded host, because a collection with someone's token in it is a
collection that must not be committed or shared.
"""

import argparse
import json
import re
import sys
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

DEFAULT_API_DIR = "api"
DEFAULT_OUTPUT_DIR = "exports"
DEFAULT_COLLECTION_NAME = "Casely API Tests"
COLLECTION_SCHEMA = "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"

BASE_URL_VAR = "baseUrl"
AUTH_TOKEN_VAR = "authToken"
API_KEY_VAR = "apiKey"

HTTP_METHODS = {
    "GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS", "TRACE",
}

VARIABLE_PATTERN = re.compile(r"\{\{([A-Za-z0-9_\-.]+)\}\}")

# Keys whose value belongs in an environment file marked secret, never in the
# collection that gets committed next to the test cases.
SECRET_KEY_PATTERN = re.compile(
    r"(token|secret|password|passwd|apikey|api_key|authorization|credential|"
    r"client_secret|private_key|signature)",
    re.IGNORECASE,
)

# Shapes that are almost always a real credential rather than a placeholder.
CREDENTIAL_VALUE_PATTERNS = [
    (re.compile(r"\beyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}"), "a JWT"),
    (re.compile(r"\bsk-[A-Za-z0-9_\-]{16,}"), "an API secret key"),
    (re.compile(r"\b(ghp|gho|ghu|ghs|github_pat)_[A-Za-z0-9_]{16,}"), "a GitHub token"),
    (re.compile(r"\bxox[abprs]-[A-Za-z0-9\-]{10,}"), "a Slack token"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "an AWS access key id"),
    (re.compile(r"\b[A-Fa-f0-9]{32,}\b"), "a long hex secret"),
]

HARDCODED_HOST_PATTERN = re.compile(r"^\s*https?://(?!\{\{)", re.IGNORECASE)


class SpecError(Exception):
    """An API test case spec that cannot be turned into a request faithfully."""


# --------------------------------------------------------------------------
# Reading and validating specs
# --------------------------------------------------------------------------


def _as_list(value: Any, field: str) -> List[Any]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise SpecError(f"'{field}' must be a list.")
    return value


def _scan_for_credentials(spec: Dict[str, Any]) -> Optional[str]:
    """Return a description of the first real-looking credential found."""
    blob = json.dumps(spec, ensure_ascii=False)
    for pattern, label in CREDENTIAL_VALUE_PATTERNS:
        match = pattern.search(blob)
        if match:
            return (
                f"the spec contains what looks like {label} "
                f"({match.group(0)[:12]}…). Replace it with a "
                "{{variable}} — the collection is meant to be shared."
            )
    return None


def validate_spec(spec: Dict[str, Any]) -> None:
    """Raise SpecError when the spec would produce a broken or unsafe request."""
    if not isinstance(spec, dict):
        raise SpecError("the file must hold a single JSON object.")

    for field in ("id", "title", "method", "path"):
        if not str(spec.get(field, "")).strip():
            raise SpecError(f"'{field}' is required and must not be empty.")

    method = str(spec["method"]).upper()
    if method not in HTTP_METHODS:
        raise SpecError(
            f"'{method}' is not an HTTP method. Use one of: "
            f"{', '.join(sorted(HTTP_METHODS))}."
        )

    path = str(spec["path"])
    if HARDCODED_HOST_PATTERN.match(path):
        raise SpecError(
            f"'path' is a hardcoded host ({path[:40]}…). Write the path only "
            f"('/v1/orders') and let the collection prepend {{{{{BASE_URL_VAR}}}}}, "
            "so the same run works against dev, staging and production."
        )
    if not path.startswith("/") and not path.startswith("{{"):
        raise SpecError(
            f"'path' must start with '/' (got {path[:40]!r})."
        )

    credential = _scan_for_credentials(spec)
    if credential:
        raise SpecError(credential)

    expect = spec.get("expect")
    if expect is not None and not isinstance(expect, dict):
        raise SpecError("'expect' must be an object.")
    if isinstance(expect, dict):
        status = expect.get("status")
        if status is not None and not isinstance(status, int):
            raise SpecError("'expect.status' must be an integer status code.")

    body = spec.get("body")
    if body is not None:
        if not isinstance(body, dict) or "mode" not in body:
            raise SpecError(
                "'body' must be an object with a 'mode' "
                "('raw', 'formdata', 'urlencoded' or 'none')."
            )
        if body["mode"] == "raw" and not isinstance(body.get("raw", ""), str):
            raise SpecError("'body.raw' must be a string.")


def read_specs(api_path: Path) -> Tuple[List[Dict[str, Any]], List[str]]:
    """Read every API test case spec, separating valid ones from broken ones."""
    specs: List[Dict[str, Any]] = []
    problems: List[str] = []
    seen_ids: Dict[str, str] = {}

    for json_file in sorted(api_path.glob("*.json")):
        try:
            spec = json.loads(json_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            problems.append(f"{json_file.name}: invalid JSON — {exc}")
            continue

        try:
            validate_spec(spec)
        except SpecError as exc:
            problems.append(f"{json_file.name}: {exc}")
            continue

        case_id = str(spec["id"]).strip()
        if case_id in seen_ids:
            problems.append(
                f"{json_file.name}: case id {case_id!r} is already used by "
                f"{seen_ids[case_id]}. One id is one scenario."
            )
            continue
        seen_ids[case_id] = json_file.name

        spec["_source"] = json_file.name
        specs.append(spec)

    return specs, problems


# --------------------------------------------------------------------------
# Building the collection
# --------------------------------------------------------------------------


def _js(value: Any) -> str:
    """Render a Python value as a JavaScript literal for a test script."""
    return json.dumps(value, ensure_ascii=False)


def build_test_script(spec: Dict[str, Any]) -> List[str]:
    """Turn the spec's 'expect' block into Postman assertions.

    Generated rather than hand-written: the assertions then match the expected
    result of the test case exactly, and a typo in a hand-rolled pm.test()
    cannot turn a failing endpoint into a green run.
    """
    expect = spec.get("expect") or {}
    saves = _as_list(spec.get("saveFromResponse"), "saveFromResponse")
    json_checks = _as_list(expect.get("jsonPath"), "expect.jsonPath")
    lines: List[str] = []

    status = expect.get("status")
    if status is not None:
        lines.append(f'pm.test("Status code is {status}", function () {{')
        lines.append(f"    pm.response.to.have.status({status});")
        lines.append("});")

    max_time = expect.get("maxResponseTimeMs")
    if isinstance(max_time, int):
        lines.append(f'pm.test("Response time is under {max_time} ms", function () {{')
        lines.append(f"    pm.expect(pm.response.responseTime).to.be.below({max_time});")
        lines.append("});")

    for header in _as_list(expect.get("headers"), "expect.headers"):
        key = header.get("key")
        if not key:
            continue
        if "equals" in header:
            lines.append(
                f'pm.test("Header {key} is {header["equals"]}", function () {{'
            )
            lines.append(
                f"    pm.expect(pm.response.headers.get({_js(key)}))"
                f".to.eql({_js(header['equals'])});"
            )
        else:
            lines.append(f'pm.test("Header {key} is present", function () {{')
            lines.append(
                f"    pm.expect(pm.response.headers.has({_js(key)})).to.be.true;"
            )
        lines.append("});")

    for needle in _as_list(expect.get("bodyContains"), "expect.bodyContains"):
        lines.append(f'pm.test("Body contains {needle}", function () {{')
        lines.append(f"    pm.expect(pm.response.text()).to.include({_js(needle)});")
        lines.append("});")

    if json_checks or saves:
        if lines:
            lines.append("")
        lines.append("const body = pm.response.json();")

    for check in json_checks:
        path = check.get("path")
        if not path:
            continue
        if "equals" in check:
            lines.append(f'pm.test("{path} equals {check["equals"]}", function () {{')
            lines.append(
                f"    pm.expect(body).to.have.nested.property({_js(path)}, "
                f"{_js(check['equals'])});"
            )
        elif "contains" in check:
            lines.append(f'pm.test("{path} contains {check["contains"]}", function () {{')
            lines.append(f"    pm.expect(body).to.have.nested.property({_js(path)});")
            lines.append(
                f"    pm.expect(String(body{_dot(path)})).to.include("
                f"{_js(check['contains'])});"
            )
        elif "type" in check:
            lines.append(f'pm.test("{path} is a {check["type"]}", function () {{')
            lines.append(
                f"    pm.expect(body{_dot(path)}).to.be.a({_js(check['type'])});"
            )
        else:
            lines.append(f'pm.test("{path} is present", function () {{')
            lines.append(f"    pm.expect(body).to.have.nested.property({_js(path)});")
        lines.append("});")

    for save in saves:
        var_name = save.get("var")
        path = save.get("path")
        if not var_name or not path:
            continue
        lines.append("")
        lines.append(
            f"// Hands {{{{{var_name}}}}} to the cases that run after this one."
        )
        lines.append(f"pm.collectionVariables.set({_js(var_name)}, body{_dot(path)});")

    lines.extend(str(line) for line in _as_list(spec.get("tests"), "tests"))

    return lines


def _dot(path: str) -> str:
    """Render a dotted JSON path as safe JavaScript member access."""
    out = ""
    for segment in re.split(r"\.(?![^\[]*\])", path):
        match = re.match(r"^([^\[\]]*)((?:\[\d+\])*)$", segment)
        if not match:
            return f"[{_js(path)}]"
        name, indexes = match.groups()
        if name:
            out += f"[{_js(name)}]"
        out += indexes
    return out


def build_url(spec: Dict[str, Any]) -> Dict[str, Any]:
    path = str(spec["path"])
    query = _as_list(spec.get("query"), "query")

    if path.startswith("{{"):
        raw_base, raw_path = "", path
        host = [path.split("/")[0]]
        segments = [s for s in path.split("/")[1:] if s != ""]
    else:
        raw_base = f"{{{{{BASE_URL_VAR}}}}}"
        raw_path = path
        host = [raw_base]
        segments = [s for s in path.split("/") if s != ""]

    raw = f"{raw_base}{raw_path}"
    if query:
        pairs = "&".join(
            f"{item.get('key', '')}={item.get('value', '')}" for item in query
        )
        raw = f"{raw}?{pairs}"

    url: Dict[str, Any] = {"raw": raw, "host": host, "path": segments}
    if query:
        url["query"] = [
            {
                "key": str(item.get("key", "")),
                "value": str(item.get("value", "")),
                **({"description": item["description"]} if item.get("description") else {}),
            }
            for item in query
        ]
    return url


def build_auth(spec: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Per-request auth. Most cases inherit the collection's bearer token."""
    auth = str(spec.get("auth", "inherit")).lower()
    if auth in ("", "inherit"):
        return None
    if auth == "none":
        return {"type": "noauth"}
    if auth == "bearer":
        return {
            "type": "bearer",
            "bearer": [
                {"key": "token", "value": f"{{{{{AUTH_TOKEN_VAR}}}}}", "type": "string"}
            ],
        }
    if auth == "apikey":
        return {
            "type": "apikey",
            "apikey": [
                {"key": "key", "value": "X-API-Key", "type": "string"},
                {"key": "value", "value": f"{{{{{API_KEY_VAR}}}}}", "type": "string"},
                {"key": "in", "value": "header", "type": "string"},
            ],
        }
    return None


def build_description(spec: Dict[str, Any]) -> str:
    """What a reviewer sees in Postman: the test case behind the request."""
    parts: List[str] = []
    if spec.get("description"):
        parts.append(str(spec["description"]))
    if spec.get("preconditions"):
        parts.append(f"**Preconditions:** {spec['preconditions']}")
    expect = spec.get("expect") or {}
    if expect.get("status"):
        parts.append(f"**Expected status:** {expect['status']}")
    if spec.get("requirement"):
        parts.append(f"**Requirement:** {spec['requirement']}")
    parts.append(f"_Test case {spec['id']} — generated by Casely._")
    return "\n\n".join(parts)


def build_request_item(spec: Dict[str, Any]) -> Dict[str, Any]:
    headers = [
        {
            "key": str(header.get("key", "")),
            "value": str(header.get("value", "")),
            "type": "text",
            **({"description": header["description"]} if header.get("description") else {}),
        }
        for header in _as_list(spec.get("headers"), "headers")
    ]

    request: Dict[str, Any] = {
        "method": str(spec["method"]).upper(),
        "header": headers,
        "url": build_url(spec),
        "description": build_description(spec),
    }

    auth = build_auth(spec)
    if auth:
        request["auth"] = auth

    body = spec.get("body")
    if isinstance(body, dict) and body.get("mode") not in (None, "none"):
        request["body"] = dict(body)
        if body.get("mode") == "raw":
            request["body"].setdefault(
                "options", {"raw": {"language": body.get("language", "json")}}
            )
            request["body"].pop("language", None)

    item: Dict[str, Any] = {
        "name": f"{spec['id']} — {spec['title']}",
        "request": request,
        "response": [],
    }

    script = build_test_script(spec)
    if script:
        item["event"] = [
            {
                "listen": "test",
                "script": {"type": "text/javascript", "exec": script},
            }
        ]

    prerequest = _as_list(spec.get("preRequest"), "preRequest")
    if prerequest:
        item.setdefault("event", []).append(
            {
                "listen": "prerequest",
                "script": {"type": "text/javascript", "exec": [str(l) for l in prerequest]},
            }
        )

    return item


def group_into_folders(specs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Nest requests under the folder path each spec declares."""
    root: List[Dict[str, Any]] = []
    folders: Dict[str, Dict[str, Any]] = {}

    for spec in specs:
        folder_path = str(spec.get("folder", "")).strip()
        item = build_request_item(spec)

        if not folder_path:
            root.append(item)
            continue

        parent_items = root
        trail = ""
        for name in [part.strip() for part in folder_path.split("/") if part.strip()]:
            trail = f"{trail}/{name}" if trail else name
            folder = folders.get(trail)
            if folder is None:
                folder = {"name": name, "item": []}
                folders[trail] = folder
                parent_items.append(folder)
            parent_items = folder["item"]
        parent_items.append(item)

    return root


# --------------------------------------------------------------------------
# Variables
# --------------------------------------------------------------------------


def collect_variables(
    specs: List[Dict[str, Any]],
) -> Tuple[List[str], Dict[str, str], Dict[str, str]]:
    """Find every {{variable}} used, plus declared descriptions and defaults.

    Variables written by a test (saveFromResponse) are chained inside the run,
    so they belong in the collection with an empty value rather than in the
    list the user has to fill in by hand.
    """
    used: List[str] = [BASE_URL_VAR, AUTH_TOKEN_VAR]
    descriptions: Dict[str, str] = {
        BASE_URL_VAR: "API root without a trailing slash, e.g. https://api.stage.example.com",
        AUTH_TOKEN_VAR: (
            "Bearer token the collection authenticates with. Every request "
            "inherits it unless the case says otherwise."
        ),
    }
    defaults: Dict[str, str] = {}
    runtime: set = set()

    for spec in specs:
        for save in _as_list(spec.get("saveFromResponse"), "saveFromResponse"):
            if save.get("var"):
                runtime.add(str(save["var"]))

        for declared in _as_list(spec.get("variables"), "variables"):
            key = str(declared.get("key", "")).strip()
            if not key:
                continue
            if declared.get("description"):
                descriptions.setdefault(key, str(declared["description"]))
            if declared.get("value"):
                defaults.setdefault(key, str(declared["value"]))
            if key not in used:
                used.append(key)

        blob = json.dumps(
            {k: v for k, v in spec.items() if k != "variables"}, ensure_ascii=False
        )
        for name in VARIABLE_PATTERN.findall(blob):
            if name not in used:
                used.append(name)

    for name in sorted(runtime):
        if name not in used:
            used.append(name)
        descriptions.setdefault(name, "Set at runtime by an earlier request in the run.")

    return used, descriptions, defaults


def is_secret(name: str) -> bool:
    return bool(SECRET_KEY_PATTERN.search(name))


# --------------------------------------------------------------------------
# Output files
# --------------------------------------------------------------------------


def _stable_id(seed: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"casely://{seed}"))


def build_collection(
    specs: List[Dict[str, Any]],
    collection_name: str,
    variables: List[str],
    descriptions: Dict[str, str],
    defaults: Dict[str, str],
) -> Dict[str, Any]:
    return {
        "info": {
            "_postman_id": _stable_id(collection_name),
            "name": collection_name,
            "schema": COLLECTION_SCHEMA,
            "description": (
                f"{len(specs)} API test cases generated by Casely from the "
                "requirements.\n\nEvery environment-specific value is a "
                f"{{{{variable}}}} — set them in the accompanying environment "
                "file before running. The collection carries no credentials."
            ),
        },
        "auth": {
            "type": "bearer",
            "bearer": [
                {"key": "token", "value": f"{{{{{AUTH_TOKEN_VAR}}}}}", "type": "string"}
            ],
        },
        "variable": [
            {
                "key": name,
                "value": defaults.get(name, ""),
                "type": "string",
                **({"description": descriptions[name]} if name in descriptions else {}),
            }
            for name in variables
        ],
        "item": group_into_folders(specs),
    }


def build_environment(
    env_name: str,
    variables: List[str],
    descriptions: Dict[str, str],
    defaults: Dict[str, str],
) -> Dict[str, Any]:
    return {
        "id": _stable_id(env_name),
        "name": env_name,
        "values": [
            {
                "key": name,
                "value": defaults.get(name, ""),
                "type": "secret" if is_secret(name) else "default",
                "enabled": True,
            }
            for name in variables
        ],
        "_postman_variable_scope": "environment",
    }


def build_readme(
    collection_file: str,
    environment_file: str,
    collection_name: str,
    case_count: int,
    variables: List[str],
    descriptions: Dict[str, str],
) -> str:
    rows = "\n".join(
        f"| `{name}` | {'yes' if is_secret(name) else 'no'} | "
        f"{descriptions.get(name, 'Test data used by one or more requests.')} |"
        for name in variables
    )

    return f"""# {collection_name} — how to run it

{case_count} API test cases, exported as a Postman collection. Nothing in these
files is environment-specific: the base URL, the tokens and the test data are
all variables you fill in once.

## 1. Import

In Postman: **Import** → drop in both files.

- `{collection_file}` — the requests and their assertions
- `{environment_file}` — the variables, all empty

Newman works from the same two files, no import needed.

## 2. Fill in the variables

Open the imported environment and set a value for each row. Select it in the
environment picker (top right) before running, or the requests will fire at an
empty host.

| Variable | Secret | What it is |
|----------|--------|------------|
{rows}

Variables marked secret hold credentials. Postman keeps their values out of
exports, so keep them in the environment and never paste one into a request.

Variables described as *set at runtime* are filled by an earlier request in the
run — leave them empty.

## 3. Run

**Collection Runner:** open the collection → **Run** → pick the environment →
**Run {collection_name}**. Requests execute in folder order, so a case that
creates an entity runs before the one that reads it.

**Newman (CI):**

```bash
npm install -g newman
newman run {collection_file} \\
  -e {environment_file} \\
  --env-var "{AUTH_TOKEN_VAR}=$API_TOKEN" \\
  --reporters cli,junit --reporter-junit-export results.xml
```

Pass secrets with `--env-var` from your CI secret store rather than committing
them into the environment file. The JUnit report drops straight into most CI
test reporters.

## 4. Read the results

Each request asserts the expected result of its test case — status code, and
the response fields the requirement names. A failed assertion names the case id
in the request title, so it maps one-to-one onto the row in the Excel export.

Requests are ordered and named by test case id. If a case needs data that does
not exist yet in your environment, create it once and store its id in the
matching variable — that is what the non-secret variables are for.
"""


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Casely API Export — API test cases to a Postman collection"
    )
    parser.add_argument(
        "api_dir", nargs="?", default=DEFAULT_API_DIR,
        help=f"Directory holding the .json request specs (default: '{DEFAULT_API_DIR}')",
    )
    parser.add_argument(
        "output_path", nargs="?", default=DEFAULT_OUTPUT_DIR,
        help=f"Directory to write the collection to (default: '{DEFAULT_OUTPUT_DIR}')",
    )
    parser.add_argument(
        "--collection-name", default=DEFAULT_COLLECTION_NAME,
        help=f"Name of the collection (default: '{DEFAULT_COLLECTION_NAME}')",
    )
    parser.add_argument(
        "--slug", default="casely_api",
        help="File name stem for the generated files (default: 'casely_api')",
    )
    parser.add_argument(
        "--no-readme", action="store_true",
        help="Skip the run instructions file",
    )
    args = parser.parse_args()

    api_path = Path(args.api_dir)
    if not api_path.exists():
        print(f"Error: API spec directory not found: {args.api_dir}")
        sys.exit(1)

    out_dir = Path(args.output_path)
    out_dir.mkdir(parents=True, exist_ok=True)

    specs, problems = read_specs(api_path)

    if not specs and not problems:
        print(f"Warning: No .json request specs found in {args.api_dir}")
        return

    if specs:
        variables, descriptions, defaults = collect_variables(specs)
        collection_file = f"{args.slug}_collection.postman_collection.json"
        environment_file = f"{args.slug}_environment.postman_environment.json"
        env_name = f"{args.collection_name} — fill in"

        collection = build_collection(
            specs, args.collection_name, variables, descriptions, defaults
        )
        (out_dir / collection_file).write_text(
            json.dumps(collection, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )

        environment = build_environment(env_name, variables, descriptions, defaults)
        (out_dir / environment_file).write_text(
            json.dumps(environment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )

        written = [collection_file, environment_file]

        if not args.no_readme:
            readme_file = f"{args.slug}_collection_README.md"
            (out_dir / readme_file).write_text(
                build_readme(
                    collection_file, environment_file, args.collection_name,
                    len(specs), variables, descriptions,
                ),
                encoding="utf-8",
            )
            written.append(readme_file)

        print(
            f"Built {len(specs)} API requests into {out_dir}/{collection_file}"
        )
        print(f"Variables to fill in: {', '.join(variables)}")
        print("Wrote: " + ", ".join(written))

    if problems:
        print(f"\n{len(problems)} API test case(s) were NOT exported:")
        for problem in problems:
            print(f"  - {problem}")
        print("\nFix the specs above and run the build again.")
        sys.exit(1)


if __name__ == "__main__":
    main()
