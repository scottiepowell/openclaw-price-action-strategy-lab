# OpenClaw Inbox Prompt: Fix Test Drift, Then Run Full-Universe Replay Discovery

## Repo

Work in this repo only:

```text
/home/scott/projects/openclaw-monster-academy-strategy-lab
```

This prompt is delivered through the GitHub-backed mailbox in:

```text
scottiepowell/openclaw-price-action-strategy-lab
.openclaw-mailbox/inbox/
```

## Boundary

Do not add Alpaca order submission.
Do not add broker APIs.
Do not enable paper orders.
Do not create live trading.
Do not claim profitability.
Keep `broker_action_allowed: false` everywhere relevant.

## Context from previous mailbox response

The previous status response reported:

- Current branch: `master`
- Paper-readiness matrix: 12 rows total
- READY_FOR_PAPER_REVIEW candidates: `PTC-004`, `PTC-005`, `PTC-009`, `PTC-017`, `PTC-019`
- Paper-review queue: 5 rows
- Paper-watch journal: 5 rows
- Replay evidence matrix: 25 entries total
- Artifact index points at the full 11-symbol `1Day + 5Min` handoff
- Replay discovery config uses `1Day + 5Min` only and blocks `1Min`
- Old sample files under `data_refs/google_drive` are deprecated/excluded for replay discovery

Important issue found:

```text
PYTHONPATH=src pytest -q → 83 passed, 1 failed
Failure: tests/test_config.py::test_repo_scope_and_remaining_blockers_are_explicit
Reason: README missing phrase: not a live trading bot
```

## Task 1 — Fix the failing README/test drift first

Before running new discovery, fix the failing README wording assertion.

Update `README.md` so it clearly states the project is:

```text
not a live trading bot
```

Preserve the safety boundary language:

- no trade signal
- no profitability claim
- no broker action
- no Alpaca order submission
- no live trading

Then run:

```text
PYTHONPATH=src pytest tests/test_config.py::test_repo_scope_and_remaining_blockers_are_explicit -q
```

Then run the full suite:

```text
PYTHONPATH=src pytest -q
```

Do not proceed to Task 2 until the suite is green.

## Task 2 — Run full-universe date/symbol-diversified replay discovery

Once tests are green, run a fresh full-universe date-diversified and symbol-diversified replay discovery pass using the reconciled artifact index.

Use only:

```text
1Day
5Min
```

Do not use:

```text
1Min
data_refs/google_drive sample files
old SPY/META-only smoke handoff
```

Active artifact root should be:

```text
/home/scott/projects/openclaw-historical-market-data-extraction/artifacts/published/monster_historical_data_strategy_lab_1d_5m_v1.0
```

Expected symbol universe:

```text
SPY, QQQ, AAPL, MSFT, NVDA, AMZN, GOOGL, META, TSLA, AVGO, IWM
```

Discovery goals:

- find new candidates across the full 11-symbol universe
- prefer different symbols
- prefer different months
- avoid existing HR-001 through HR-019 windows when possible
- include both bullish `close_above_resistance` and bearish `close_below_support`
- respect `max_cases_per_symbol_total`
- respect `max_cases_per_symbol_per_month`
- maintain at least 30 calendar days between selected cases when possible

Create the next batch only if valid candidates exist:

```text
HR-020 through HR-031
```

Target, if available without forcing weak duplicates:

- 6 bullish candidates
- 6 bearish candidates
- at least 6 different symbols if possible
- spread across multiple months

If fewer valid candidates exist under the constraints, create fewer and explain why. Do not force weak or duplicate cases.

Each new replay case must remain:

```text
replay_status: NOT_VERIFIED
manual_review_status: pending
broker_action_allowed: false
```

Generate/update:

```text
replay/cases/HR-020.md through HR-031 as applicable
runs/replay/HR-020_manual_review_packet.md through HR-031 as applicable
runs/replay/HR-020_031_triage_summary.md
runs/replay/discovery/date_diversified_candidates.md
runs/replay/discovery/date_diversified_candidates.csv
runs/replay/replay_evidence_matrix.md
runs/replay/replay_evidence_matrix.csv
```

Each manual review packet should include:

- replay metadata
- 1D context
- 5Min event window
- prior support/resistance calculation
- breakout/breakdown candle
- target
- invalidation
- event flags
- suggested classification
- manual_review_status: pending
- broker_action_allowed: false

## Task 3 — Tests

Add/update tests if needed:

- README safety wording remains explicit
- discovery uses full 11-symbol artifact root
- old sample files are not used
- `1Min` is not used
- generated cases remain `NOT_VERIFIED`
- `broker_action_allowed` remains false
- evidence matrix includes new cases
- triage summary includes new batch
- selector respects symbol/date diversity as much as available data allows

Run:

```text
PYTHONPATH=src pytest -q
```

## Deliverable

Write the response under:

```text
.openclaw-mailbox/outbox/2026-05-21-002-fix-readme-and-run-full-universe-discovery-response.md
```

The response should include:

1. Files changed.
2. Whether the README/test drift was fixed.
3. Test result after Task 1.
4. Selected HR-020 through HR-031 cases, if any.
5. Symbols used.
6. Months covered.
7. Bullish count.
8. Bearish count.
9. Review packet paths.
10. Triage summary path.
11. Updated evidence matrix path.
12. Any constraints that prevented more cases.
13. Final full test result.

Also reply in Discord with only:

```text
Mailbox response written: .openclaw-mailbox/outbox/2026-05-21-002-fix-readme-and-run-full-universe-discovery-response.md
```
