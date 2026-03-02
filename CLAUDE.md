# CLAUDE.md

This file provides context and conventions for AI assistants (Claude Code and similar tools) working in this repository.

---

## Repository Overview

**Status:** Newly initialized repository — no source code has been committed yet.

**Remote:** `http://local_proxy@127.0.0.1:39051/git/kohiro00/test`

**Default branch:** `master`

**Last updated:** 2026-03-02

This file will be updated as the project evolves. Do not infer any language, framework, or architecture that is not supported by actual files in the repository.

---

## Project Structure

_To be filled in once source code is added._

When code is added, document the directory layout here. Example:

```
.
├── src/          # Application source code
├── tests/        # Test files
├── docs/         # Documentation
└── scripts/      # Build or utility scripts
```

---

## Development Setup

_To be filled in once the project is initialized._

Typical steps to document:
1. Prerequisites (language runtime versions, system dependencies)
2. Install dependencies
3. Configure environment variables (reference `.env.example`)
4. Run the application locally

---

## Common Commands

_To be filled in once tooling is established._

| Purpose | Command |
|---------|---------|
| Install dependencies | _(e.g., `npm install`, `pip install -r requirements.txt`)_ |
| Run dev server | _(e.g., `npm run dev`, `python manage.py runserver`)_ |
| Run tests | _(e.g., `npm test`, `pytest`)_ |
| Lint / format | _(e.g., `npm run lint`, `ruff check .`)_ |
| Build for production | _(e.g., `npm run build`)_ |

---

## Testing

_To be filled in once a test framework is chosen._

Document here:
- Test framework in use
- How to run the full test suite
- How to run a single test file or test case
- Coverage expectations or required thresholds

---

## Code Conventions

_To be filled in once a language and style guide are established._

Universal conventions to follow in the meantime:
- Prefer small, focused functions/modules with a single responsibility
- Write the minimum code that solves the problem — avoid over-engineering
- Do not comment self-evident code; comment only non-obvious logic
- Keep dependencies minimal and justified
- Never commit secrets, credentials, or environment-specific values

---

## Git Workflow

- **Default branch:** `master`
- **Feature branch naming:** `claude/<description>-<session-id>`
- **Active branches:**
  - `master` — stable base
  - `claude/claude-md-mm8lq3bep2vluuge-czeF1` — CLAUDE.md setup

### Rules

- Write clear, descriptive commit messages that explain *why* a change was made
- Never force-push to `master`
- Never skip commit hooks (`--no-verify`) without explicit instruction
- Push using: `git push -u origin <branch-name>`
- Only push to branches prefixed with `claude/` during AI-assisted sessions

---

## Environment Variables

_To be filled in once the project has configuration requirements._

Document expected variables here and reference a committed `.env.example` file.

---

## CI/CD

_To be filled in once a pipeline is configured._

Document:
- CI provider (e.g., GitHub Actions, CircleCI)
- Checks that run on pull requests
- Deployment targets and triggers

---

## Notes for AI Assistants

### General guidance

- **This repository is empty.** Do not assume any specific language, framework, or architecture without evidence from actual files.
- Always read existing files before editing them.
- Prefer editing existing files over creating new ones.
- Avoid generating files unless explicitly requested.
- Do not introduce security vulnerabilities (SQL injection, XSS, command injection, insecure dependencies, etc.).
- Confirm with the user before taking destructive or hard-to-reverse actions (deleting files, force-pushing, dropping data).

### When source code is added

Update this CLAUDE.md to reflect:
- The actual project structure (languages, frameworks, entry points)
- Real setup steps and common commands
- The test framework and how to run tests
- Lint/format tooling and configuration file locations
- Any environment variables required

### Branch and push rules

- Develop on the designated `claude/<description>-<session-id>` branch
- Never push to `master` directly during an AI session
- Use `git push -u origin <branch-name>` for all pushes
