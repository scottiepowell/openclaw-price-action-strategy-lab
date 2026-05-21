# Phase 6 Candidate Promotion Criteria

## Purpose

Define when a refined rule candidate may be promoted into paper-validation readiness.

## Scope

This applies after Phase 5 validation and before Phase 7 paper validation.

It is a documentation gate, not an execution rule.

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

## Notes

Use this doc together with:

- `../PHASE_6_RULE_REFINEMENT.md`
- `../PHASE_6_PAPER_TRADE_READINESS_GATES.md`
- `../../../../paper_validation/readiness_gates/promotion_checklist.md`
- `../../../../paper_validation/readiness_gates/candidate_readiness_template.md`
