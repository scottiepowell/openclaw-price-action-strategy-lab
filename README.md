# OpenClaw Price Action Strategy Lab

A repo for building a price action strategy lab with OpenClaw-assisted workflows.

## Initial setup goals

- Establish a safe Git baseline.
- Configure SSH-based GitHub access from the controller/OpenClaw host.
- Add an OpenClaw mailbox workflow for remote prompt execution.
- Build the lab structure from the prior strategy-lab pattern while keeping secrets and local data out of Git.

## Local clone target

Suggested local path:

```text
/home/scott/projects/openclaw-price-action-strategy-lab
```

## SSH remote

Use SSH for OpenClaw/local Git operations:

```bash
git@github.com:scottiepowell/openclaw-price-action-strategy-lab.git
```

## Safety

This project is not a live trading bot.

Do not commit:

- API keys
- broker credentials
- private SSH keys
- local market data dumps
- private trade journals
- account exports

Use `.example` files for configuration templates.
