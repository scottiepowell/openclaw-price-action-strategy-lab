# EX-005 — No-Trade Filters

## Purpose

Collect cases where the correct outcome is to stay out because the setup is incomplete, stale, or overfit.

## Candidate family

- higher_timeframe_obstacle
- context_missing
- target_already_hit
- same_candle_overfit
- arbitrary_anchor
- tighter_range_needed
- invalidation_missing

## What this example should show

- some apparent setups are blocked before confirmation
- a missing invalidation should prevent promotion
- same-candle or arbitrary-anchor cases should stay conservative

## Evidence status

- source evidence: `runs/month2_6_download/transcripts/MONTH 2/MONTHLY CURRENT RANGE LESSON [q0fxq1o9gs].txt`
- snapshot refs: `q0fxq1o9gs:ts-000448`, `q0fxq1o9gs:ts-000658`, `a3ynlbskzm:ts-000109`
- replay link: `replay/contradiction_cases/HC-001.md`

## Labels to capture later

- obstacle_conflict
- context_missing
- target_already_hit
- tighter_range_needed
- arbitrary_anchor
- invalidation_missing

## Boundary

- no-trade filter only
- not a backtest
- not execution logic
