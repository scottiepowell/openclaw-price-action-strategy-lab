# Candidate Promotion Criteria

## Purpose

Define when a refined rule candidate is ready to move into paper validation.

## Promotion criteria

A candidate may be promoted only if all of the following are true:

- the candidate definition is stable
- the target relationship is explicit
- the invalidation path is explicit and testable
- no-trade filters are explicit
- supporting replay evidence exists
- contradiction cases have been reviewed
- the language is paper-only and avoids live-trading assumptions
- the candidate cannot be mistaken for a live execution rule

## Required evidence

- source reference or crosswalk exists
- replay examples support the candidate
- contradiction notes do not defeat the candidate outright
- target and invalidation are both documented
- room-to-target or equivalent entry filter is documented where relevant

## Promotion outcomes

- **Promote**: the candidate meets all criteria and can move to paper validation
- **Split**: the candidate mixes two behaviors and must be separated first
- **Downgrade**: the candidate is too weak or ambiguous for promotion
- **Reject**: the evidence does not support paper-validation readiness

## Fail-fast conditions

Do not promote if any of these are present:

- ambiguous language
- missing evidence links
- profitability claims
- live-order wording
- unsupported execution assumptions
- missing contradiction review
- missing no-trade filters

## Related

- `promotion_checklist.md`
- `candidate_readiness_template.md`
- `no_trade_filters.md`
