# Paper Validation Design

## Goal

Observe mature candidates in a paper-only environment and record whether they behave the way the evidence promised.

## Responsibilities

- Support dry-run observation
- Record paper-validation candidates
- Track journaled outcomes
- Preserve abort rules and no-trade filters

## Boundaries

- Paper only
- No live account activity
- No automatic order logic

## Stages

### Dry-run

Record what would have happened, without submitting an order.

### Paper run

Record the paper-only order context and result.

### Review

Compare the observed result to the readiness gate and candidate definition.

## Required fields

- candidate id
- source evidence links
- gate status
- no-trade filter status
- target context
- invalidation context
- outcome notes

## Review questions

- Was the candidate present under the expected context?
- Was the target known before the entry?
- Was there room to target?
- Did a no-trade filter block an invalid setup?
- Was the entry early, late, or structurally wrong?

## Decision outcomes

- keep
- keep but refine
- split
- downgrade
- reject
- needs more evidence
- needs more contradiction cases
