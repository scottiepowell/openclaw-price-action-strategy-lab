# OpenClaw Inbox Prompt: Review Strict Bearish Cases HR-032 through HR-035

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

Do not promote cases.
Do not modify replay_status.
Do not modify manual_review_status.
Do not add Alpaca order submission.
Do not add broker APIs.
Do not enable paper orders.
Do not create live trading.
Do not claim profitability.
Keep `broker_action_allowed: false` everywhere relevant.

## Context

Strict bearish breakdown discovery was completed successfully.

New pending cases:

```text
HR-032 / TSLA / 2023-07-20
HR-033 / NVDA / 2023-12-19
HR-034 / AVGO / 2023-12-19
HR-035 / META / 2023-12-28
```

These were selected using stricter bearish validation:

```text
breakdown_close < prior_support
downside_target < breakdown_close
invalidation_level > breakdown_close
target_hit_after_confirmation: true
invalidation_hit_after_confirmation: false
```

All four currently remain:

```text
replay_status: NOT_VERIFIED
manual_review_status: pending
broker_action_allowed: false
```

## Task

Review only:

```text
runs/replay/HR-032_manual_review_packet.md
runs/replay/HR-033_manual_review_packet.md
runs/replay/HR-034_manual_review_packet.md
runs/replay/HR-035_manual_review_packet.md
runs/replay/HR-032_035_bearish_review_summary.md
```

Do not modify project files except the required outbox response.
Do not promote cases.
Do not alter replay_status.
Do not alter manual_review_status.

For each case provide:

- symbol
- date
- setup type
- prior support
- breakdown close
- downside target
- invalidation level
- target_hit_after_confirmation
- invalidation_hit_after_confirmation
- max favorable move
- suggested classification
- recommended manual classification
- cautions / notes

Use recommendation buckets:

- likely_confirmed_breakdown
- likely_failed_reclaim
- likely_target_not_hit
- likely_ambiguous
- reject_or_block
- needs_more_review

## Output format

Write a compact markdown report with:

1. A table for HR-032 through HR-035.
2. A short paragraph per case.
3. Final recommendation section:
   - likely confirm
   - likely ambiguous
   - likely reject/blocked
   - needs more review
4. Explicit confirmation that all four remain pending.

## Tests

No test suite required unless you change helper logic.
If tests are run, report the result.

## Deliverable

Write the response under:

```text
.openclaw-mailbox/outbox/2026-05-22-010-review-strict-bearish-hr032-035-response.md
```

After committing, run:

```text
git push
```

Also reply in Discord with only:

```text
Mailbox response written and pushed: .openclaw-mailbox/outbox/2026-05-22-010-review-strict-bearish-hr032-035-response.md
```
