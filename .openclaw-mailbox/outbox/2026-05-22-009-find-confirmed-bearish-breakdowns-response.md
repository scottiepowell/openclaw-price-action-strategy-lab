# Strict Bearish Breakdown Candidates

## Files changed
- src/monster_strategy_lab/replay/discovery.py
- src/monster_strategy_lab/replay/__init__.py
- tests/unit/test_replay_discovery.py
- runs/replay/discovery/strict_bearish_breakdown_candidates.md
- runs/replay/discovery/strict_bearish_breakdown_candidates.csv
- replay/cases/HR-032.md
- replay/cases/HR-033.md
- replay/cases/HR-034.md
- replay/cases/HR-035.md
- runs/replay/HR-032_manual_review_packet.md
- runs/replay/HR-033_manual_review_packet.md
- runs/replay/HR-034_manual_review_packet.md
- runs/replay/HR-035_manual_review_packet.md
- runs/replay/HR-032_035_bearish_review_summary.md

## Candidate report paths
- runs/replay/discovery/strict_bearish_breakdown_candidates.md
- runs/replay/discovery/strict_bearish_breakdown_candidates.csv

## Count
- strict bearish candidates found: 9
- selected for HR creation: 4

## HR-032 through HR-035
- HR-032 / TSLA / 2023-07-20
- HR-033 / NVDA / 2023-12-19
- HR-034 / AVGO / 2023-12-19
- HR-035 / META / 2023-12-28

## Rejected malformed bearish candidates
- none were selected; the validation guard rejects any row where breakdown_close >= prior_support, downside_target >= breakdown_close, or invalidation_level <= breakdown_close
- weaker coverage candidate IWM was left out, but not for malformed geometry

## Status confirmation
- HR-032: NOT_VERIFIED / pending / broker_action_allowed false
- HR-033: NOT_VERIFIED / pending / broker_action_allowed false
- HR-034: NOT_VERIFIED / pending / broker_action_allowed false
- HR-035: NOT_VERIFIED / pending / broker_action_allowed false

## Test result
- PYTHONPATH=src pytest -q -> 89 passed
