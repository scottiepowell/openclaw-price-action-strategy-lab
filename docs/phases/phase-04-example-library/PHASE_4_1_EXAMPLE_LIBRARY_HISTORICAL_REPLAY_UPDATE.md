# Phase 4.1 Example Library Historical Replay Update

## Purpose

Extend the example library so it can connect transcript/JPEG examples to historical replay cases and contradiction searches.

## Repo alignment

- example cards: `docs/phases/phase-04-example-library/example-cards/`
- replay cases: `replay/cases/`
- contradiction cases: `replay/contradiction_cases/`
- replay reports: `replay/reports/`
- historical data refs: `data_refs/historical_market_data/`

## Historical replay role

Historical replay helps determine whether a course example has a structurally similar market-data window.

It should be used to:
- strengthen examples
- weaken examples
- split broad examples into narrower candidate forms
- find contradictions
- mark missing data quality

## Boundary

- not a backtest
- not a profitability claim
- not execution logic
- not paper-order approval
