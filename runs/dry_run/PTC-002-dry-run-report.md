# Dry Run Report

generated_at: 2026-05-18T00:52:23.939719+00:00
candidate_id: PTC-002
symbol: SPY
direction: long

schema_status: PASS
evidence_status: PASS
replay_status: NOT_VERIFIED
strategy_logic_status: PASS
paper_readiness_status: READY_FOR_DRY_RUN
broker_action_allowed: false

## Blocking reasons
- labels missing: break_behavior, invalidation, range, resistance, support, target
- replay_status is NOT_VERIFIED
- replay_outcome not confirmed: insufficient

## Warnings
- higher_timeframe_obstacle_check is not verified
- target_already_hit_check is not verified

## Next actions
- label support/resistance/target/invalidation
- verify close_above_resistance behavior
- check higher timeframe obstacle
- check whether target was already hit
- confirm the replay outcome from the inspected AAPL window
- promote HR-001 to VERIFIED only after the replay review is complete

## Required levels
- support_level: TBD
- resistance_level: TBD
- target_price: TBD
- entry_candidate_price: TBD
- invalidation_level: TBD
- room_to_target: TBD

## Confirmation
- confirmation_type: close_above_resistance
- confirmation_behavior: Wait for manual visual review before considering paper validation.

## Context checks
- timeframe_context: 1D + 5m
- higher_timeframe_context: TBD
- higher_timeframe_obstacle_check: TBD
- target_already_hit_check: TBD

## Evidence mapping
- evidence_link: EX-002
  supports: direction-model only
  notes: Dry-run placeholder until manual visual review passes.

## Replay mapping
- replay_case: replay/cases/HR-002.md
  replay_status: NOT_VERIFIED
  replay_outcome: insufficient
  classification: insufficient
  notes: SPY | 2023-05-15 to 2023-05-17 | labels missing: break_behavior, invalidation, range, resistance, support, target; replay_status is NOT_VERIFIED; replay_outcome not confirmed: insufficient
  evidence_type: real_market_replay
  real_market_evidence: true

## Boundary
- Dry-run only
- No live-trade implication
- No Alpaca order submission
- No broker action allowed