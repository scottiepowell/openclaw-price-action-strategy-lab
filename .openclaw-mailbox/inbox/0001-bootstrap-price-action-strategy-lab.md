# Mailbox Task 0001 — Bootstrap Price Action Strategy Lab

## Objective

Bootstrap the `openclaw-price-action-strategy-lab` repository so it is ready for OpenClaw-driven development.

This repo should follow the same broad structure and workflow pattern as Scott's existing strategy lab, but this is a new price action strategy lab repo.

## Repo path

Expected local path:

```text
/home/scott/projects/openclaw-price-action-strategy-lab
```

## Remote

GitHub repo:

```text
git@github.com:scottiepowell/openclaw-price-action-strategy-lab.git
```

If the local repo uses HTTPS, switch it to SSH.

## Required first checks

Run and summarize:

```bash
cd /home/scott/projects/openclaw-price-action-strategy-lab 2>/dev/null || true
pwd || true
git status --short || true
git branch --show-current || true
git remote -v || true
ssh -T git@github.com || true
```

If the local repo does not exist, clone it:

```bash
mkdir -p /home/scott/projects
cd /home/scott/projects
git clone git@github.com:scottiepowell/openclaw-price-action-strategy-lab.git
cd openclaw-price-action-strategy-lab
```

## Desired baseline structure

Create a practical initial layout for the new lab:

```text
AGENTS.md
PROJECT_BRIEF.md
TODO.md
REPO_LAYOUT.md
configs/
  default.yaml
  risk_limits.example.yaml
  symbol_universe.yaml
docs/
  INDEX.md
  NEXT_ACTIONS.md
  architecture/
  operations/
  phases/
  prompts/
evidence/
knowledge_base/
  concepts/
  examples/
  glossary/
  rule_candidates/
  validation/
logs/
paper_validation/
replay/
runs/
src/
  price_action_strategy_lab/
    __init__.py
    __main__.py
    cli.py
    status.py
tests/
  test_smoke.py
artifacts/
  charts/.gitkeep
  exports/.gitkeep
  packages/.gitkeep
  reports/.gitkeep
```

Use placeholders and small starter files. Do not copy large data files or generated caches.

## AGENTS.md requirements

Create an `AGENTS.md` that tells OpenClaw/Codex:

- This is a price action strategy lab.
- It is for research, replay, paper validation, and documentation.
- It must not place live trades unless explicitly approved in a future separate task.
- It must never commit credentials, API keys, broker secrets, private keys, or account exports.
- Prefer small commits, dry-runs, testable scripts, and clear runbooks.
- Treat generated artifacts, logs, local market data, and secrets as local-only unless explicitly whitelisted.
- Use the mailbox workflow when direct CLI access from ChatGPT is not available.

## Python baseline

Create a minimal Python package:

```text
src/price_action_strategy_lab/__init__.py
src/price_action_strategy_lab/__main__.py
src/price_action_strategy_lab/cli.py
src/price_action_strategy_lab/status.py
```

Add a simple CLI command that can print repo status/config basics without needing external APIs.

Create/update:

```text
pyproject.toml
requirements.txt
tests/test_smoke.py
```

Run tests if possible:

```bash
python -m pytest
```

If pytest is not installed, note that in the response and do not force a system-wide install.

## Docs baseline

Create starter docs:

```text
docs/INDEX.md
docs/NEXT_ACTIONS.md
docs/architecture/SYSTEM_OVERVIEW.md
docs/architecture/DATA_FLOW.md
docs/operations/RUNBOOK.md
docs/operations/VALIDATION_CHECKLIST.md
```

## Git requirements

- Keep `.gitignore` intact and improve if needed.
- Do not commit `.venv`, `__pycache__`, real secrets, large market data, or generated outputs.
- Commit and push changes to the default branch.

## Expected response file

Write your response here:

```text
.openclaw-mailbox/outbox/0001-bootstrap-price-action-strategy-lab-response.md
```

## Response must include

- Whether local repo already existed or was cloned.
- Current branch.
- Remote URL.
- Whether SSH GitHub auth works.
- Files created/changed.
- Test result.
- Commit SHA.
- Push result.
- Exact next recommended task.

## Safety rules

- Do not commit secrets.
- Do not configure broker APIs yet.
- Do not place live or paper trades.
- Do not import large external datasets.
- If blocked, write a clear outbox response explaining the blocker.
