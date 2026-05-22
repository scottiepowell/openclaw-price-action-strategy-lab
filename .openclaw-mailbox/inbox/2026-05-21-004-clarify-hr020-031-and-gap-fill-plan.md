# OpenClaw Inbox Prompt: Clarify HR-020–HR-031 State and Propose Gap-Fill Plan

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

## Context from previous audit response

The discovery constraint audit response reported:

```text
Raw bullish candidate count: 898
Raw bearish candidate count: 261
Final selected candidate count under current constraints: 12
All 11 symbols visible to discovery: yes
Diagnosis: strict diversification / window-occupancy filters, not scanner/data availability
Recommended next action: Option D, create targeted gap-fill cases
Final pytest: 88 passed
```

However, there is an apparent state ambiguity:

- The earlier full-universe discovery response said no HR-020 through HR-031 cases were created.
- The constraint audit says `avoid_existing_replay_windows` is blocking because the same date windows are already occupied by HR-020 through HR-031.

Before creating more cases, clarify the actual repo state.

## Task 1 — Clarify HR-020 through HR-031 state

Inspect the current repo from disk and report:

- Do `replay/cases/HR-020.md` through `HR-031.md` exist?
- Do corresponding manual review packets exist under `runs/replay/`?
- Are HR-020 through HR-031 included in `runs/replay/replay_evidence_matrix.md` and `.csv`?
- Are HR-020 through HR-031 included in `runs/replay/discovery/date_diversified_candidates.md` and `.csv`?
- Are they committed locally?
- Are they pushed to GitHub?
- What commit introduced them, if they exist?

If HR-020 through HR-031 exist, summarize them in a compact table:

- replay_id
- symbol
- side
- date
- setup_type
- suggested_classification
- replay_status
- manual_review_status
- broker_action_allowed

If they do not exist, explain why the audit refers to their occupied windows.

## Task 2 — Inspect the discovery constraint audit

Open and summarize:

```text
runs/replay/discovery/discovery_constraint_audit.md
runs/replay/discovery/discovery_constraint_audit.csv
```

Report:

- raw bullish count
- raw bearish count
- final selected count
- which filter stage removes the most candidates
- top near-miss candidates
- whether the audit proves all 11 symbols are usable

## Task 3 — Propose targeted gap-fill plan, but do not create cases yet

Do not create new HR cases in this prompt.

Create a planning report:

```text
runs/replay/discovery/targeted_gap_fill_plan.md
```

The plan should identify missing or weak evidence buckets from the replay evidence matrix.

Consider buckets such as:

- bullish failed breakout reclaim
- bullish target-not-hit
- bullish target already hit before confirmation
- bullish watch/no-trigger outside May 2023
- bearish confirmed breakdown on non-SPY/IWM symbols
- bearish no-target-hit
- bearish support touch no trigger
- bearish target already hit before confirmation
- bearish ambiguous
- additional confirmed examples across symbols not yet represented

For each proposed gap-fill target include:

- desired bucket
- why the bucket matters
- candidate selection rule
- suggested loosened constraint, if any
- expected source from audit near-misses
- whether it should remain NOT_VERIFIED and manual_review_status pending

## Task 4 — Recommendation

Recommend the next inbox prompt.

The recommendation should choose one of:

A. Manually review existing HR-020 through HR-031, if they exist.
B. Generate targeted gap-fill cases from near-miss candidates.
C. Re-run broad discovery with one carefully relaxed constraint.
D. Reconcile repo state if HR-020 through HR-031 exist locally but are not committed/pushed.

## Tests

Run:

```text
PYTHONPATH=src pytest -q
```

## Deliverable

Write the response under:

```text
.openclaw-mailbox/outbox/2026-05-21-004-clarify-hr020-031-and-gap-fill-plan-response.md
```

The response should include:

1. Files changed.
2. Whether HR-020 through HR-031 exist.
3. Whether they are committed/pushed.
4. Compact HR-020 through HR-031 table if they exist.
5. Audit summary.
6. Targeted gap-fill plan path.
7. Recommended next action.
8. Final test result.

After committing, run:

```text
git push
```

Also reply in Discord with only:

```text
Mailbox response written and pushed: .openclaw-mailbox/outbox/2026-05-21-004-clarify-hr020-031-and-gap-fill-plan-response.md
```
