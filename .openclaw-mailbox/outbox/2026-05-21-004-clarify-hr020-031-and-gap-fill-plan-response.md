Files changed:
- runs/replay/discovery/targeted_gap_fill_plan.md
- .openclaw-mailbox/outbox/2026-05-21-004-clarify-hr020-031-and-gap-fill-plan-response.md

HR-020 through HR-031:
- exist on disk: yes
- manual review packets exist: yes
- included in runs/replay/replay_evidence_matrix.md and .csv: yes
- included in runs/replay/discovery/date_diversified_candidates.md and .csv: yes
- committed locally: yes
- pushed to GitHub: yes
- commit that introduced them: d870f32

Compact HR-020 through HR-031 table:
| replay_id | symbol | side | date | setup_type | suggested_classification | replay_status | manual_review_status | broker_action_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HR-020 | AVGO | bullish | 2023-05-30 | close_above_resistance | candidate_for_manual_review | NOT_VERIFIED | pending | false |
| HR-021 | GOOGL | bullish | 2023-07-25 | close_above_resistance | candidate_for_manual_review | NOT_VERIFIED | pending | false |
| HR-022 | AMZN | bullish | 2023-08-03 | close_above_resistance | candidate_for_manual_review | NOT_VERIFIED | pending | false |
| HR-023 | TSLA | bullish | 2023-09-11 | close_above_resistance | candidate_for_manual_review | NOT_VERIFIED | pending | false |
| HR-024 | MSFT | bullish | 2023-10-24 | close_above_resistance | candidate_for_manual_review | NOT_VERIFIED | pending | false |
| HR-025 | AAPL | bullish | 2023-12-05 | close_above_resistance | candidate_for_manual_review | NOT_VERIFIED | pending | false |
| HR-026 | SPY | bearish | 2023-07-06 | close_below_support | candidate_for_manual_review | NOT_VERIFIED | pending | false |
| HR-027 | IWM | bearish | 2023-08-08 | close_below_support | candidate_for_manual_review | NOT_VERIFIED | pending | false |
| HR-028 | AAPL | bearish | 2023-09-07 | close_below_support | candidate_for_manual_review | NOT_VERIFIED | pending | false |
| HR-029 | QQQ | bearish | 2023-10-06 | close_below_support | candidate_for_manual_review | NOT_VERIFIED | pending | false |
| HR-030 | NVDA | bearish | 2023-10-17 | close_below_support | candidate_for_manual_review | NOT_VERIFIED | pending | false |
| HR-031 | META | bearish | 2023-12-04 | close_below_support | candidate_for_manual_review | NOT_VERIFIED | pending | false |

Audit summary:
- raw bullish count: 898
- raw bearish count: 261
- final selected count: 12
- biggest filter block: avoid-existing-window / window occupancy, with symbol/month caps reinforcing it
- top near-misses: repeated AVGO/NVDA bullish windows plus META bearish windows from the May cluster
- all 11 symbols usable: yes

Targeted gap-fill plan path:
- runs/replay/discovery/targeted_gap_fill_plan.md

Recommended next action:
- B. Generate targeted gap-fill cases from near-miss candidates.

Final test result:
- PYTHONPATH=src pytest -q → 88 passed
