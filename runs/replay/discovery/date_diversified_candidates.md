# Date-Diversified Replay Candidates

candidate_windows_found: 4
min_calendar_days_between_cases: 30
max_cases_per_symbol_per_month: 1
max_cases_per_symbol_total: 2
avoid_existing_replay_windows: true

## HR-016 (META)
- symbol: META
- side: bullish
- timestamp: 2023-06-08T14:40:00+00:00
- event_type: close_above_resistance
- prior_level: 263.655
- breakout_or_breakdown_amount: 0.08500000000003638
- lookback_bars: 12
- reason_selected: bullish close_above_resistance event
- distance_from_nearest_existing_case_days: 20
- has_1d_context: true

## HR-017 (SPY)
- symbol: SPY
- side: bullish
- timestamp: 2023-10-10T13:30:00+00:00
- event_type: close_above_resistance
- prior_level: 432.665
- breakout_or_breakdown_amount: 0.5049999999999955
- lookback_bars: 12
- reason_selected: bullish close_above_resistance event
- distance_from_nearest_existing_case_days: 20
- has_1d_context: true

## HR-018 (META)
- symbol: META
- side: bearish
- timestamp: 2023-12-14T14:30:00+00:00
- event_type: close_below_support
- prior_level: 333.63
- breakout_or_breakdown_amount: 0.4300000000000068
- lookback_bars: 12
- reason_selected: bearish close_below_support event
- distance_from_nearest_existing_case_days: 15
- has_1d_context: true

## HR-019 (SPY)
- symbol: SPY
- side: bearish
- timestamp: 2023-08-30T17:50:00+00:00
- event_type: close_below_support
- prior_level: 450.915
- breakout_or_breakdown_amount: 0.3050000000000068
- lookback_bars: 12
- reason_selected: bearish close_below_support event
- distance_from_nearest_existing_case_days: 20
- has_1d_context: true

## Diversity warnings
- date diversity improved: 4 month(s) selected
- symbol diversity warning: all selected cases are mixed

## Coverage / selection notes
- existing replay case dates: 19
- full 1Day + 5Min handoff data is now the replay source of truth
- old Google Drive sample exports are deprecated for diversified replay discovery
- 1Min remains blocked until the META 2023-2025 partial partitions are resolved

## Recommended next search
- bearish close_below_support discovery
- retain bullish/bearish month and symbol diversification constraints
- prefer 5Min over 1Min for date-diversified replay

## Boundary
- Generated report only
- No broker action allowed
