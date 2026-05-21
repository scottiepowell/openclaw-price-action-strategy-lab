# Phase 5B Historical Validation Plan

## Purpose

Plan the historical replay workflow used to validate, narrow, or contradict the Phase 3 candidate set before Phase 6 refinement.

## Repo alignment

- historical data refs: `data_refs/historical_market_data/`
- replay cases: `replay/cases/`
- contradiction cases: `replay/contradiction_cases/`
- replay labels: `replay/labels/`
- reports: `replay/reports/`

## Validation workflow

1. confirm available data windows
2. verify data quality
3. label current range / support / resistance / target context
4. label break behavior and invalidation behavior
5. compare candidate behavior to the replay window
6. search for contradiction windows
7. record candidate impact
8. decide keep / refine / split / downgrade / reject

## Output artifacts

- replay case records
- contradiction case records
- replay summary reports
- candidate impact notes

## Boundary

- no live trading
- no order submission
- no profitability claims
- no execution-ready language
