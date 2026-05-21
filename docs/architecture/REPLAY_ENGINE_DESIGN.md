# Replay Engine Design

## Goal

Apply conservative labels to historical windows so the strategy work can be reviewed without hindsight bias.

## Responsibilities

- Read replay case records
- Join evidence references
- Apply conservative labels
- Preserve data-quality gates
- Emit audit-friendly reports

## Non-goals

- No backtesting claims
- No execution logic
- No trade recommendations

## Inputs

- replay case file
- source manifests
- evidence crosswalks
- historical OHLCV references
- contradiction references

## Output shape

Replay output should answer:

- what is the window?
- what is the visible range?
- what level is being referenced?
- what is the observed break behavior?
- what invalidates the candidate?
- what contradiction, if any, was found?

## Labeling rules

- Prefer conservative labels over ambiguous ones.
- Use explicit `hold`, `retest`, `reclaim`, `rejection`, or `invalidation candidate` labels only when the evidence supports them.
- Do not upgrade a label just because later price action would have made it profitable.
- If data quality is weak, mark the case incomplete instead of guessing.

## Quality gates

- source reference exists
- evidence crosswalk exists
- label meaning is unambiguous
- no live-trading implication is present

## Reports

Replay reports should summarize:

- case coverage
- open gaps
- contradictions found
- labels that need refinement
- cases ready for Phase 6 review
