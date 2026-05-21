---
replay_id: SAMPLE-VERIFIED
related_candidate_id: PTC-TEST-001
symbol: AAPL
direction: long
date_window: 2026-05-01 to 2026-05-05
timeframe_stack: 1D + 5m
data_files:
  - tests/fixtures/replay_cases/aapl_1d_fixture.csv
  - tests/fixtures/replay_cases/aapl_5m_fixture.csv
data_quality_status: PASSED
source_evidence:
  - EX-001
chart_levels:
  support_level: 100.0
  resistance_level: 105.0
  target_price: 110.0
  invalidation_level: 98.5
labels_present:
  - range
  - support
  - resistance
  - target
  - break_behavior
  - invalidation
context_checks:
  higher_timeframe_obstacle_check: clear
  target_already_hit_check: clear
replay_observations:
  - Synthetic fixture used for validator testing only.
replay_outcome: confirmed
replay_status: VERIFIED
evidence_type: synthetic_fixture
real_market_evidence: false
reviewer_notes: Synthetic fixture only. Not real market evidence.
boundary: No trade signal, no profitability claim, no execution readiness.
---

# SAMPLE-VERIFIED

## Replay window
2026-05-01 to 2026-05-05

## Summary
Synthetic verified replay fixture for validator testing only.

## replay_id
SAMPLE-VERIFIED

## related_candidate_id
PTC-TEST-001

## symbol
AAPL

## direction
long

## date_window
2026-05-01 to 2026-05-05

## timeframe_stack
1D + 5m

## data_files
- tests/fixtures/replay_cases/aapl_1d_fixture.csv
- tests/fixtures/replay_cases/aapl_5m_fixture.csv

## data_quality_status
PASSED

## source evidence
- EX-001

## chart levels
- support_level: 100.0
- resistance_level: 105.0
- target_price: 110.0
- invalidation_level: 98.5

## labels_present
- range
- support
- resistance
- target
- break_behavior
- invalidation

## context checks
- higher_timeframe_obstacle_check: clear
- target_already_hit_check: clear

## replay observations
- Synthetic fixture used for validator testing only.

## replay outcome
confirmed

## replay status
VERIFIED

## reviewer notes
Synthetic fixture only. Not real market evidence.

## Notes
Synthetic fixture only. Not real market evidence.

## boundary
- No trade signal
- No profitability claim
- No execution readiness
