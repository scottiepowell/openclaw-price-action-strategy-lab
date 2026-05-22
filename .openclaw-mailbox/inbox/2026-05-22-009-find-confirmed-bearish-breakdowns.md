# OpenClaw Inbox Prompt: Find Strict Confirmed Bearish Breakdown Candidates

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

The bearish review batch HR-027, HR-028, HR-029, HR-031 did not produce clean confirmed bearish cases.

Assessment:

- HR-027 / IWM: do not promote; watch/no-trigger or target-not-hit shape
- HR-028 / AAPL: do not promote; wick/touch only, no close below support, no target hit
- HR-029 / QQQ: do not promote; ambiguous/failure-like, invalidation before confirmation
- HR-031 / META: do not promote; no confirmed breakdown, no target hit

There were also suspicious field-shape issues in the bearish packet summaries. For a bearish breakdown, the breakdown close and downside target should be below support. Some reviewed rows showed values above support, which suggests either packet extraction, field labeling, or candidate selection needs a stricter bearish validation path.

Current evidence is bullish-heavy. We need roughly two more confirmed bearish replay examples before moving closer to paper execution.

## Task

Find strict confirmed bearish breakdown candidates only.

Do not promote anything in this prompt.
Do not create paper orders.
Do not submit anything to Alpaca.

Use the full 11-symbol `1Day + 5Min` artifact root already configured in the repo.

Do not use:

```text
1Min
data_refs/google_drive sample files
old SPY/META-only smoke handoff
```

## Strict bearish candidate requirements

A candidate can be selected for review only if it satisfies all of these event facts:

```text
side: bearish
setup_type: close_below_support
close_below_support: true
breakdown_close < prior_support
invalidation_level > breakdown_close
downside_target < breakdown_close
target_hit_after_confirmation: true
invalidation_hit_after_confirmation: false
```

Reject candidates where:

```text
breakdown_close >= prior_support
downside_target >= breakdown_close
invalidation_level <= breakdown_close
target_hit_after_confirmation is false
invalidation_hit_after_confirmation is true
classification is watch_no_trigger
classification is ambiguous
classification is failed_reclaim
```

## Output

Create a strict bearish review candidate report:

```text
runs/replay/discovery/strict_bearish_breakdown_candidates.md
runs/replay/discovery/strict_bearish_breakdown_candidates.csv
```

Include columns:

- symbol
- event_timestamp
- prior_support
- breakdown_close
- downside_target
- invalidation_level
- target_hit_after_confirmation
- invalidation_hit_after_confirmation
- min_low_after_confirmation
- max_close_after_confirmation
- suggested_classification
- reason_selected

Select the best candidates for manual review:

```text
HR-032 through HR-035
```

Only create these HR cases if strict candidates exist. If fewer than four exist, create fewer. If none exist, create none and explain why.

Each new HR case must remain:

```text
replay_status: NOT_VERIFIED
manual_review_status: pending
broker_action_allowed: false
```

Generate corresponding manual review packets for any created cases:

```text
runs/replay/HR-032_manual_review_packet.md
runs/replay/HR-033_manual_review_packet.md
runs/replay/HR-034_manual_review_packet.md
runs/replay/HR-035_manual_review_packet.md
```

Also create/update:

```text
runs/replay/HR-032_035_bearish_review_summary.md
```

## Important validation

Add a validation guard or test that catches the earlier suspicious bearish shape:

For every strict bearish selected candidate:

```text
breakdown_close < prior_support
downside_target < breakdown_close
invalidation_level > breakdown_close
```

If a candidate fails those relationships, it must not be selected.

## Tests

Add/update tests if needed:

- strict bearish selector rejects watch/no-trigger cases
- strict bearish selector rejects target-not-hit cases
- strict bearish selector rejects malformed bearish geometry
- strict bearish selector only emits candidates with target hit and no invalidation after confirmation
- generated HR-032 through HR-035, if any, remain NOT_VERIFIED / pending / broker_action_allowed false
- no Alpaca or broker dependency is introduced

Run:

```text
PYTHONPATH=src pytest -q
```

## Deliverable

Write the response under:

```text
.openclaw-mailbox/outbox/2026-05-22-009-find-confirmed-bearish-breakdowns-response.md
```

The response should include:

1. Files changed.
2. Strict bearish candidate report paths.
3. Number of strict bearish candidates found.
4. HR-032 through HR-035 created, if any.
5. Symbols/dates selected.
6. Any rejected malformed bearish candidates and why.
7. Confirmation all new cases remain NOT_VERIFIED / pending / broker_action_allowed false.
8. Final test result.

After committing, run:

```text
git push
```

Also reply in Discord with only:

```text
Mailbox response written and pushed: .openclaw-mailbox/outbox/2026-05-22-009-find-confirmed-bearish-breakdowns-response.md
```
