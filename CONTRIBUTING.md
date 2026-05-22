# Contributing to Casely

Thank you for your interest in improving Casely. Contributions of all kinds are welcome: bug fixes, new features, documentation improvements, and test coverage.

## How to contribute

### 1. Report a bug

Use the [bug report template](https://github.com/JohnWayneeee/casely-qa-skill/issues/new?template=bug_report.md).

Include:
- The command you ran (`/parse`, `/export`, etc.)
- What happened vs. what you expected
- Your Python version and OS
- A minimal reproduction if possible

### 2. Request a feature

Use the [feature request template](https://github.com/JohnWayneeee/casely-qa-skill/issues/new?template=feature_request.md).

Good feature requests explain the problem they solve, not just the implementation.

### 3. Submit a pull request

1. Fork the repository and create a branch from `main`:
   ```bash
   git checkout -b fix/your-fix-name
   ```

2. Make your changes. Keep them focused — one concern per PR.

3. Test your changes:
   ```bash
   uv sync
   # run a quick /init → /parse → /export cycle on sample data
   ```

4. Commit with a clear message:
   ```
   fix: handle missing columns in /style gracefully
   feat: add /generate security test type
   docs: clarify /plan output format in SKILL.md
   ```

5. Open a pull request against `main`. Describe what changed and how you tested it.

## Code style

- Python: follow PEP 8. No extra dependencies beyond `docling` and `openpyxl` unless discussed in an issue first.
- Markdown: use ATX headings (`##`), fenced code blocks with language tags.
- Keep the `SKILL.md` and `README.md` in sync if you change commands or workflow steps.

## Commit message convention

Use the imperative mood and one of these prefixes:

| Prefix | When to use |
|--------|-------------|
| `feat:` | New command, new capability |
| `fix:` | Bug fix |
| `docs:` | Documentation only |
| `refactor:` | Code change without behaviour change |
| `test:` | Adding or updating evals |
| `chore:` | Dependencies, CI, tooling |

## Questions

Open a [GitHub Discussion](https://github.com/JohnWayneeee/casely-qa-skill/discussions) or an issue tagged `question`.
