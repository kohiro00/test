# CLAUDE.md

This file provides context and conventions for AI assistants (Claude Code and similar tools) working in this repository.

---

## Repository Overview

**Status:** Newly initialized repository — no source code has been committed yet.

**Remote:** `http://local_proxy@127.0.0.1:43818/git/kohiro00/test`

Update this section once the project type, purpose, and tech stack are established.

---

## Project Structure

_To be filled in once source code is added._

When code is added, document the directory layout here. Example format:

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

Typical setup steps to document here:
1. Prerequisites (runtime versions, system dependencies)
2. Install dependencies
3. Configure environment variables (`.env.example`)
4. Run the application locally

---

## Common Commands

_To be filled in once tooling is established._

Document the commands used daily by contributors:

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

Document:
- Test framework in use
- How to run all tests
- How to run a single test file or test case
- Test coverage expectations or thresholds

---

## Code Conventions

_To be filled in once a language and style guide are established._

Until then, follow these universal conventions:
- Prefer small, focused functions/modules with a single responsibility
- Avoid over-engineering — write the minimum code that solves the problem
- Do not add comments to self-evident code; comment only non-obvious logic
- Keep dependencies minimal and justified
- Do not commit secrets, credentials, or environment-specific values

---

## Git Workflow

- **Development branch naming:** `claude/<description>-<session-id>`
- **Main/default branch:** confirm once established (commonly `main` or `master`)
- Write clear, descriptive commit messages explaining *why* a change was made
- Never force-push to the main branch
- Never skip commit hooks (`--no-verify`) without explicit instruction

---

## Environment Variables

_To be filled in once the project has configuration requirements._

Document expected environment variables and point to an `.env.example` file when one exists.

---

## CI/CD

_To be filled in once a pipeline is configured._

Document:
- CI provider (GitHub Actions, CircleCI, etc.)
- Which checks run on pull requests
- Deployment targets and triggers

---

## Notes for AI Assistants

- This repository is empty. Do not assume any specific language, framework, or architecture without evidence from actual files.
- When source code is added, update this file to reflect the real project structure and conventions.
- Always read existing files before editing them.
- Prefer editing existing files over creating new ones.
- Avoid generating files unless explicitly needed.
- Do not introduce security vulnerabilities (SQL injection, XSS, command injection, insecure dependencies, etc.).
- Confirm with the user before taking destructive or hard-to-reverse actions (deleting files, force-pushing, dropping data).
