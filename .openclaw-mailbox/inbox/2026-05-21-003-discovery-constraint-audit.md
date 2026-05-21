# OpenClaw Inbox Prompt: Discovery Constraint Audit Before More Replay Cases

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

The previous run fixed the README/test drift and confirmed:

```text
PYTHONPATH=src pytest -q → 84 passed, 0 failed
```

However, full-universe discovery created no new HR-020 through HR-031 cases.

Previous response said:

- selected batch: none
- bullish: 0
- bearish: 0
- no review packets created
- evidence matrix unchanged
- constraints that prevented more cases:
  - 30-day minimum spacing
  - per-symbol monthly limit
  - per-symbol total limit
  - avoid-existing-window rule

This result may be legitimate, but before relaxing constraints or creating more cases we need a transparent constraint audit.

## Task — Build a discovery constraint audit

Do not create HR-020 through HR-031 yet.
Do not loosen constraints yet.
Do not promote any replay cases.

Create a diagnostic report that shows where candidates are being filtered out.

Create:

```text
runs/replay/discovery/discovery_constraint_audit.md
runs/replay/discovery/discovery_constraint_audit.csv
```

The audit should include both bullish and bearish discovery.

## Required audit sections

### 1. Data source verification

Show:

- artifact root currently used
- whether it is the full 11-symbol root
- whether old `data_refs/google_drive` samples are excluded
- whether `1Min` is blocked
- symbols discovered from the artifact index
- symbols with both `1Day` and `5Min` available

Expected artifact root:

```text
/home/scott/projects/openclaw-historical-market-data-extraction/artifacts/published/monster_historical_data_strategy_lab_1d_5m_v1.0
```

Expected symbols:

```text
SPY, QQQ, AAPL, MSFT, NVDA, AMZN, GOOGL, META, TSLA, AVGO, IWM
```

### 2. Raw candidate counts before diversification filters

For each side and symbol, report raw candidates found before filtering:

- bullish `close_above_resistance`
- bearish `close_below_support`

Columns:

- side
- symbol
- raw_candidate_count
- first_event_timestamp
- last_event_timestamp
- months_present

### 3. Filter-stage attrition table

Show how many candidates remain after each filter stage:

- raw candidates
- after excluding old sample sources
- after requiring full artifact root
- after excluding `1Min`
- after avoid-existing-window rule
- after 30-day spacing rule
- after max cases per symbol per month
- after max cases per symbol total
- final selected candidates

Do this separately for:

- bullish
- bearish
- combined

### 4. Existing HR window coverage

List existing HR-001 through HR-019 by:

- replay_id
- symbol
- side
- date
- classification
- replay_status

Also summarize:

- dates already occupied
- months already occupied
- symbols already occupied
- whether existing HR cases are causing over-blocking

### 5. Near-miss candidates

List the top 20 candidates that were rejected only because of diversification constraints.

For each near miss include:

- side
- symbol
- event timestamp
- setup type
- prior level
- close
- target hit after confirmation if available
- invalidation hit after confirmation if available
- which constraint rejected it
- whether it would be useful as coverage

### 6. Recommended constraint options

Do not apply changes automatically. Present options.

Include at least these options:

Option A — Keep strict constraints
- no new cases
- strongest anti-bias posture

Option B — Relax date spacing only
- reduce min spacing from 30 calendar days to 10 or 15
- keep symbol caps

Option C — Relax avoid-existing-window only
- allow new cases in same month but not same symbol/date
- keep symbol caps

Option D — Create targeted gap-fill cases
- choose scenarios missing from evidence matrix rather than pure date/symbol diversity
- examples: failed breakout reclaim, target already hit before confirmation, bearish no-trigger, bullish no-target-hit

Option E — Expand data or selector logic if raw counts are unexpectedly low
- only if the audit shows raw candidates are missing for many symbols

### 7. Recommendation

Make a recommendation for the next inbox prompt.

The recommendation should say whether we should:

- keep constraints strict and stop
- relax date spacing
- relax avoid-existing-window
- create targeted gap-fill cases
- investigate scanner/data issues

## Tests

Add/update tests if needed:

- audit report can be generated
- audit includes raw counts by symbol and side
- audit includes filter-stage attrition
- audit includes near-miss candidates when available
- audit does not create HR-020 through HR-031
- broker_action_allowed remains false

Run:

```text
PYTHONPATH=src pytest -q
```

## Deliverable

Write the response under:

```text
.openclaw-mailbox/outbox/2026-05-21-003-discovery-constraint-audit-response.md
```

The response should include:

1. Files changed.
2. Audit report paths.
3. Raw bullish candidate count.
4. Raw bearish candidate count.
5. Final selected candidate count under current constraints.
6. Main constraint causing the zero-case result.
7. Whether all 11 symbols are actually visible to discovery.
8. Whether the issue is data availability, scanner logic, or strict diversification filters.
9. Recommended next action.
10. Final test result.

Also reply in Discord with only:

```text
Mailbox response written: .openclaw-mailbox/outbox/2026-05-21-003-discovery-constraint-audit-response.md
```
