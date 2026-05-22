# OpenClaw Inbox Prompt: Promote HR-032, HR-034, HR-035 and Classify HR-033

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

The strict bearish review batch produced the following packet-derived review assessment:

| replay_id | symbol | date | review decision | classification | outcome |
| --- | --- | --- | --- | --- | --- |
| HR-032 | TSLA | 2023-07-20 | promote | confirmed_breakdown | confirmed |
| HR-033 | NVDA | 2023-12-19 | do not promote as confirmed target-hit | confirmed_breakdown_no_target_hit | insufficient / target_not_hit |
| HR-034 | AVGO | 2023-12-19 | promote | confirmed_breakdown | confirmed |
| HR-035 | META | 2023-12-28 | promote | confirmed_breakdown | confirmed |

Review rationale:

- HR-032: clean breakdown, downside target hit after confirmation, invalidation not hit after confirmation.
- HR-034: tight geometry, but valid breakdown, downside target hit after confirmation, invalidation not hit after confirmation.
- HR-035: small breakdown amount, but target hit and continued lower, invalidation not hit after confirmation.
- HR-033: valid breakdown structure but downside target was not hit; keep as target-not-hit evidence rather than confirmed target-hit evidence.

Previous response path:

```text
.openclaw-mailbox/outbox/2026-05-22-010-review-strict-bearish-hr032-035-response.md
```

## Task

Update the relevant replay case files and downstream generated artifacts according to the accepted packet-derived manual review.

### Promote these cases

```text
HR-032:
  replay_status: VERIFIED
  manual_review_status: completed
  replay_outcome: confirmed
  classification: confirmed_breakdown
  broker_action_allowed: false

HR-034:
  replay_status: VERIFIED
  manual_review_status: completed
  replay_outcome: confirmed
  classification: confirmed_breakdown
  broker_action_allowed: false

HR-035:
  replay_status: VERIFIED
  manual_review_status: completed
  replay_outcome: confirmed
  classification: confirmed_breakdown
  broker_action_allowed: false
```

### Classify but do not promote as confirmed target-hit

```text
HR-033:
  replay_status: VERIFIED
  manual_review_status: completed
  replay_outcome: insufficient
  classification: confirmed_breakdown_no_target_hit
  broker_action_allowed: false
```

Add reviewer notes indicating:

```text
Packet-derived manual review accepted by Scott/ChatGPT; no separate chart screenshot review performed.
```

Do not modify unrelated HR cases except through regenerated summaries/matrices if needed.

## Regenerate downstream artifacts

Regenerate/update:

```text
runs/replay/replay_evidence_matrix.md
runs/replay/replay_evidence_matrix.csv
runs/replay/HR-032_035_bearish_review_summary.md
runs/paper_readiness/paper_readiness_matrix.md
runs/paper_readiness/paper_readiness_matrix.csv
runs/paper_review/paper_review_queue.md
runs/paper_review/paper_review_queue.csv
runs/paper_journal/paper_watch_journal.md
runs/paper_journal/paper_watch_journal.csv
```

Create/update individual readiness / review / journal files for any newly eligible candidates if the codebase requires them.

Expected behavior:

- HR-032, HR-034, HR-035 linked PTC candidates may enter `READY_FOR_PAPER_REVIEW` if the existing paper-readiness rules are satisfied.
- HR-033 should be blocked from `READY_FOR_PAPER_REVIEW` because it is `confirmed_breakdown_no_target_hit` / insufficient.
- `broker_action_allowed` remains false everywhere.
- No broker or Alpaca code is added.
- No paper order is submitted.

## Tests

Add/update tests if needed:

- HR-032, HR-034, HR-035 are VERIFIED / completed / confirmed / confirmed_breakdown.
- HR-033 is VERIFIED / completed / insufficient / confirmed_breakdown_no_target_hit.
- HR-033 does not enter READY_FOR_PAPER_REVIEW.
- HR-032, HR-034, HR-035 enter READY_FOR_PAPER_REVIEW only if their PTC links exist and fields satisfy existing rules.
- `broker_action_allowed` remains false for all.
- no Alpaca or broker dependency is introduced.

Run:

```text
PYTHONPATH=src pytest -q
```

## Deliverable

Write the response under:

```text
.openclaw-mailbox/outbox/2026-05-22-011-promote-bearish-hr032-034-035-and-classify-hr033-response.md
```

The response should include:

1. Files changed.
2. Confirmation HR-032, HR-034, HR-035 were promoted.
3. Confirmation HR-033 was classified as target-not-hit / insufficient, not promoted into confirmed target-hit readiness.
4. Resulting statuses/classifications for HR-032, HR-033, HR-034, HR-035.
5. Whether corresponding PTC candidates entered READY_FOR_PAPER_REVIEW.
6. Updated paper-review queue count.
7. Updated paper-watch journal count.
8. Confirmation `broker_action_allowed` remains false.
9. Final test result.

After committing, run:

```text
git push
```

Also reply in Discord with only:

```text
Mailbox response written and pushed: .openclaw-mailbox/outbox/2026-05-22-011-promote-bearish-hr032-034-035-and-classify-hr033-response.md
```
