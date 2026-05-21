# Phase 5.1 Validation Matrix Historical Replay Update

## Purpose

Extend the validation matrix so it can incorporate historical OHLCV replay, contradiction windows, and data-quality gating.

## Repo alignment

- replay cases: `replay/cases/`
- contradiction cases: `replay/contradiction_cases/`
- replay labels: `replay/labels/`
- historical data refs: `data_refs/historical_market_data/`
- replay reports: `replay/reports/`

## Historical replay role

Historical replay is used to:
- confirm structure labels
- weaken overbroad candidates
- split candidates into narrower forms
- test contradiction windows
- identify missing target or invalidation context

## Replay requirements

- parseable timestamps
- known timezone
- known symbol
- known timeframe
- known source
- known feed
- adjustment status known
- duplicate check completed
- missing bars checked
- OHLC sanity checked
- market-hours scope known

## Boundary

- not a backtest
- not profitability proof
- not execution logic
- not paper-order approval
