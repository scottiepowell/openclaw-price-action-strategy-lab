# Replay Cases

Replay cases are structured evidence records for historical windows inspected by hand.

## Replay types

- `real_market_replay`: inspected market history from a real AAPL window
- `synthetic_fixture`: a test-only replay example with real-looking values, not real evidence
- `template`: a blank starter used for authoring
- `placeholder`: an unfinished case with missing evidence

## What a replay case is

A replay case documents what was seen in a specific market window:
- the symbol
- the date window
- the timeframe stack
- the labels that were actually present
- the observed outcome
- the replay status

## What it is not

A replay case is not:
- a trade signal
- a backtest
- a profitability claim
- an automated bot rule
- broker execution logic

## PTC vs HR

- `PTC-*` = paper-trade candidate
- `HR-*` = historical replay case

A PTC is the candidate definition.
An HR case is the evidence record used to support or contradict it.

## Verified vs fixture-only

- `VERIFIED` means a real market replay passed verification checks
- `VERIFIED_FIXTURE_ONLY` means a synthetic fixture looks valid for tests, but cannot support paper readiness

Synthetic fixtures are for unit tests only.
They may help validate parser and gating logic, but they cannot upgrade a candidate to paper review.

## What BLOCKED means

`BLOCKED` means replay evidence cannot support the candidate because the case is unusable or contradictory.

## What AMBIGUOUS means

`AMBIGUOUS` means the window was inspected, but the evidence does not cleanly support or reject the candidate.

## What CONTRADICTED means

`CONTRADICTED` means the replay evidence conflicts with the candidate definition.

## How replay supports paper candidates

Replay cases help answer:
- was the setup actually present?
- was the target known first?
- was there room to target?
- was the break behavior the one the candidate expects?
- was invalidation visible?
- did higher timeframe context help or block the setup?

## Boundary

- Replay is not a trade
- Replay is not a backtest
- Replay is not profitability proof
- Replay stays paper-validation adjacent only
