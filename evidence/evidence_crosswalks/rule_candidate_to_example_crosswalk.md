# Rule Candidate to Example Crosswalk

Starter mappings for the current candidate families.

## current_range_identification

- example: `docs/phases/phase-04-example-library/example-cards/EX-001-current-range.md`
- support: active range boundaries and range replacement behavior
- replay seed: `replay/cases/HR-001.md`

## current_range_target_relationship

- example: `docs/phases/phase-04-example-library/example-cards/EX-001-current-range.md`
- support: range context before 78/target logic
- replay seed: `replay/cases/HR-001.md`

## 78_decision_level_family

- example: `docs/phases/phase-04-example-library/example-cards/EX-002-78-decision-level.md`
- support: 78 as a decision / confirmation boundary, not a standalone entry
- replay seed: `tests/fixtures/replay_cases/verified_sample.md`

## target_activation

- example: `docs/phases/phase-04-example-library/example-cards/EX-003-78-target-activation.md`
- support: target relationship becomes active when the setup reaches the right context
- replay seed: `tests/fixtures/replay_cases/verified_sample.md`

## room_to_target

- example: `docs/phases/phase-04-example-library/example-cards/EX-004-room-to-target.md`
- support: entry should be blocked when room is too small
- replay seed: `tests/fixtures/replay_cases/verified_sample.md`

## no_trade_filters

- example: `docs/phases/phase-04-example-library/example-cards/EX-005-no-trade-filters.md`
- support: explicit blockers and conservative stay-out conditions
- replay seed: `replay/contradiction_cases/HC-001.md`
