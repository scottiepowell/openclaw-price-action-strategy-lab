# Dry Run Report

generated_at: 2026-05-18T00:52:23.935838+00:00
candidate_id: PTC-001
symbol: AAPL
direction: long

schema_status: PASS
evidence_status: PASS
replay_status: NOT_VERIFIED
strategy_logic_status: PASS
paper_readiness_status: READY_FOR_DRY_RUN
broker_action_allowed: false

## Blocking reasons
- manual review notes: close_above_resistance not confirmed
- manual review notes: target not reached during replay window
- manual review notes: watch/no-trigger only
- replay_outcome not confirmed: insufficient

## Warnings
- higher_timeframe_obstacle_check is not verified
- target_already_hit_check is not verified

## Next actions
- treat HR-001 as watch/no-trigger only
- do not promote HR-001 to paper review

## Required levels
- support_level: 100.0
- resistance_level: 105.0
- target_price: 110.0
- entry_candidate_price: 105.25
- invalidation_level: 98.5
- room_to_target: 4.75

## Confirmation
- confirmation_type: close_above_resistance
- confirmation_behavior: Wait for close above resistance before considering paper validation.

## Context checks
- timeframe_context: 1D + 5m
- higher_timeframe_context: Daily context from replay notes.
- higher_timeframe_obstacle_check: not documented
- target_already_hit_check: not documented

## Evidence mapping
- evidence_link: EX-001
  supports: direction-model only
  notes: Used as long AAPL direction-model evidence, not as direct trade permission.

## Replay mapping
- replay_case: replay/cases/HR-001.md
  replay_status: NOT_VERIFIED
  replay_outcome: insufficient
  classification: watch_no_trigger
  notes: AAPL | 2023-05-15 to 2023-05-18 | manual review notes: close_above_resistance not confirmed; manual review notes: target not reached during replay window; manual review notes: watch/no-trigger only; replay_outcome not confirmed: insufficient
  evidence_type: real_market_replay
  real_market_evidence: true

## Boundary
- Dry-run only
- No live-trade implication
- No Alpaca order submission
- No broker action allowed