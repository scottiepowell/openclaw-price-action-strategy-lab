# Date-Diversified Replay Candidates

candidate_windows_found: 0
min_calendar_days_between_cases: 30
max_cases_per_symbol_per_month: 1
max_cases_per_symbol_total: 2
avoid_existing_replay_windows: true

## Selected candidates
- none eligible after applying the current 30-day spacing, per-symbol limits, and existing HR-001 through HR-019 replay windows

## Coverage / selection notes
- existing replay case dates: 19
- full 1Day + 5Min handoff data is still the replay source of truth
- old Google Drive sample exports are deprecated for diversified replay discovery
- 1Min remains blocked until the META 2023-2025 partial partitions are resolved

## Recommended next search
- re-run discovery only after new market-data coverage or case-window changes create fresh eligible windows
- keep broker_action_allowed false in replay cases

## Boundary
- Generated report only
- No broker action allowed
