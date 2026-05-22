# OpenClaw Inbox Prompt: Prepare HR-020 through HR-031 for Manual Review

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

## Context

The previous mailbox response clarified that HR-020 through HR-031 exist, are committed, and are pushed.

Known HR-020 through HR-031 state:

| replay_id | symbol | side | date | setup_type | suggested_classification | replay_status | manual_review_status | broker_action_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HR-020 | AVGO | bullish | 2023-05-30 | close_above_resistance | candidate_for_manual_review | NOT_VERIFIED | pending | false |
| HR-021 | GOOGL | bullish | 2023-07-25 | close_above_resistance | candidate_for_manual_review | NOT_VERIFIED | pending | false |
| HR-022 | AMZN | bullish | 2023-08-03 | close_above_resistance | candidate_for_manual_review | NOT_VERIFIED | pending | false |
| HR-023 | TSLA | bullish | 2023-09-11 | close_above_resistance | candidate_for_manual_review | NOT_VERIFIED | pending | false |
| HR-024 | MSFT | bullish | 2023-10-24 | close_above_resistance | candidate_for_manual_review | NOT_VERIFIED | pending | false |
| HR-025 | AAPL | bullish | 2023-12-05 | close_above_resistance | candidate_for_manual_review | NOT_VERIFIED | pending | false |
| HR-026 | SPY | bearish | 2023-07-06 | close_below_support | candidate_for_manual_review | NOT_VERIFIED | pending | false |
| HR-027 | IWM | bearish | 2023-08-08 | close_below_support | candidate_for_manual_review | NOT_VERIFIED | pending | false |
| HR-028 | AAPL | bearish | 2023-09-07 | close_below_support | candidate_for_manual_review | NOT_VERIFIED | pending | false |
| HR-029 | QQQ | bearish | 2023-10-06 | close_below_support | candidate_for_manual_review | NOT_VERIFIED | pending | false |
| HR-030 | NVDA | bearish | 2023-10-17 | close_below_support | candidate_for_manual_review | NOT_VERIFIED | pending | false |
| HR-031 | META | bearish | 2023-12-04 | close_below_support | candidate_for_manual_review | NOT_VERIFIED | pending | false |

Previous audit summary:

- raw bullish count: 898
- raw bearish count: 261
- final selected count: 12
- all 11 symbols usable: yes
- biggest filter block: avoid-existing-window / window occupancy, reinforced by symbol/month caps
- recommended next action: generate targeted gap-fill cases later, but first review HR-020 through HR-031
- previous test result: 88 passed

## Task

Prepare HR-020 through HR-031 for manual review.

Do not create new HR cases.
Do not run more discovery.
Do not promote any cases automatically.
Do not alter replay_status for HR-020 through HR-031.

Create:

```text
runs/replay/HR-020_031_manual_review_decision_sheet.md
```

For each case HR-020 through HR-031, summarize from its manual review packet:

- replay_id
- symbol
- side
- date
- setup_type
- prior support/resistance
- breakout/breakdown close
- target price
- invalidation level
- target_hit_after_confirmation
- invalidation_hit_after_confirmation
- max favorable move
- suggested_classification
- initial recommendation:
  - likely_confirmed
  - likely_ambiguous
  - likely_failed_reclaim
  - likely_target_not_hit
  - needs_visual_review
- concise reason

Also create a review priority section:

- review first
- review second
- review later

Prioritize cases that:

- have target_hit_after_confirmation true
- have invalidation_hit_after_confirmation false
- add symbol diversity
- add missing evidence buckets

Update:

```text
runs/replay/HR-020_031_triage_summary.md
```

All HR-020 through HR-031 must remain:

```text
replay_status: NOT_VERIFIED
manual_review_status: pending
broker_action_allowed: false
```

## Tests

Run:

```text
PYTHONPATH=src pytest -q
```

## Deliverable

Write the response under:

```text
.openclaw-mailbox/outbox/2026-05-22-005-prepare-hr020-031-manual-review-response.md
```

The response should include:

1. Files changed.
2. Decision sheet path.
3. Review priority order.
4. Cases that look strongest.
5. Cases that look weakest.
6. Confirmation that HR-020 through HR-031 remain NOT_VERIFIED / pending / broker_action_allowed false.
7. Final test result.

After committing, run:

```text
git push
```

Also reply in Discord with only:

```text
Mailbox response written and pushed: .openclaw-mailbox/outbox/2026-05-22-005-prepare-hr020-031-manual-review-response.md
```
