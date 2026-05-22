# Mailbox response

## Files changed
- `README.md`
- `tests/unit/test_replay_discovery.py`
- `replay/cases/HR-020.md` through `replay/cases/HR-031.md`
- `runs/replay/HR-020_manual_review_packet.md` through `runs/replay/HR-031_manual_review_packet.md`
- `runs/replay/HR-020_031_triage_summary.md`
- `runs/replay/discovery/date_diversified_candidates.md`
- `runs/replay/discovery/date_diversified_candidates.csv`
- `runs/replay/replay_evidence_matrix.md`
- `runs/replay/replay_evidence_matrix.csv`

## README / test drift
- Fixed: `README.md` now explicitly says this project is **not a live trading bot**.

## Task 1 test result
- `PYTHONPATH=src pytest tests/test_config.py::test_repo_scope_and_remaining_blockers_are_explicit -q` → passed

## Task 2 discovery result
- Selected batch created: **HR-020 through HR-031**
- Cases: HR-020 AVGO, HR-021 GOOGL, HR-022 AMZN, HR-023 TSLA, HR-024 MSFT, HR-025 AAPL, HR-026 SPY, HR-027 IWM, HR-028 AAPL, HR-029 QQQ, HR-030 NVDA, HR-031 META

## Symbols used
- AVGO, GOOGL, AMZN, TSLA, MSFT, AAPL, SPY, IWM, QQQ, NVDA, META

## Months covered
- 2023-05, 2023-07, 2023-08, 2023-09, 2023-10, 2023-12

## Counts
- Bullish: 6
- Bearish: 6

## Review packet paths
- `runs/replay/HR-020_manual_review_packet.md`
- `runs/replay/HR-021_manual_review_packet.md`
- `runs/replay/HR-022_manual_review_packet.md`
- `runs/replay/HR-023_manual_review_packet.md`
- `runs/replay/HR-024_manual_review_packet.md`
- `runs/replay/HR-025_manual_review_packet.md`
- `runs/replay/HR-026_manual_review_packet.md`
- `runs/replay/HR-027_manual_review_packet.md`
- `runs/replay/HR-028_manual_review_packet.md`
- `runs/replay/HR-029_manual_review_packet.md`
- `runs/replay/HR-030_manual_review_packet.md`
- `runs/replay/HR-031_manual_review_packet.md`

## Triage summary path
- `runs/replay/HR-020_031_triage_summary.md`

## Evidence matrix
- `runs/replay/replay_evidence_matrix.md`
- `runs/replay/replay_evidence_matrix.csv`

## Constraints
- 30-day spacing could not be perfectly maintained across all 12 chosen cases because the strongest available full-universe candidates cluster by month for some symbols.
- Kept the batch balanced, used the full 11-symbol handoff, avoided 1Min, and kept `broker_action_allowed: false`.

## Final full test result
- `PYTHONPATH=src pytest -q` → **86 passed, 0 failed**
