Files changed:
- src/monster_strategy_lab/replay/discovery.py
- src/monster_strategy_lab/replay/__init__.py
- tests/unit/test_replay_discovery.py
- runs/replay/discovery/discovery_constraint_audit.md
- runs/replay/discovery/discovery_constraint_audit.csv

Audit report paths:
- runs/replay/discovery/discovery_constraint_audit.md
- runs/replay/discovery/discovery_constraint_audit.csv

Raw bullish candidate count: 898
Raw bearish candidate count: 261
Final selected candidate count under current constraints: 12

Main constraint causing the zero-case rerun result:
- avoid_existing_replay_windows, with the same date windows already occupied by HR-020 through HR-031; symbol/month caps reinforce the block.

All 11 symbols visible to discovery:
- yes

Diagnosis:
- not a scanner/data availability problem
- not a 1Min leak problem
- it’s the strict diversification / window-occupancy filters

Recommended next action:
- Option D: create targeted gap-fill cases instead of relaxing the broad date-spacing or avoid-existing-window rules

Final test result:
- PYTHONPATH=src pytest -q → 88 passed
