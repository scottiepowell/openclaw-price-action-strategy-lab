# Monster Academy Strategy Lab

## Overview

Monster Academy Strategy Lab is the strategy-documentation, replay-validation, and paper-validation workspace for the Monster Academy trading-strategy extraction project.

This repository is designed to sit between two other projects:

```text
openclaw-monster-academy-archiver
  -> captures course transcripts, snapshots, snapshot maps, and raw lesson evidence

openclaw-historical-market-data-extraction
  -> acquires and validates historical OHLCV data

openclaw-monster-academy-strategy-lab
  -> organizes strategy documents, replay labels, rule-candidate validation, and paper-account validation
```

The Strategy Lab is not a live trading bot. It is not an automated execution system. It may eventually support Alpaca paper-account validation after candidates pass conservative readiness gates.

For the current checkpoint summary, see `docs/STRATEGY_LAB_MILESTONE_REPLAY_TO_PAPER_REVIEW.md`.

## Core principle

```text
A level break is not an entry.

A level break is a candidate confirmation.

It becomes an entry candidate only when direction, target, room to target,
support/resistance context, timeframe context, and invalidation agree.
```

This principle applies to all historical replay, candidate refinement, dry-run validation, and paper-account testing.

## What this repo is for

Use this repository to:

- store canonical phase documents
- organize glossary and concept-model artifacts
- track rule candidates and candidate splits
- connect candidates to transcript/JPEG examples
- maintain validation matrices
- define historical replay labels
- track historical replay cases
- track contradiction cases
- prepare Phase 6 conservative rule refinement
- define paper-trade readiness gates
- run dry-run paper validation
- later validate mature candidates in an Alpaca paper account
- journal paper-validation outcomes
- revise or reject candidates based on evidence

## What this repo is not for

Do not use this repository to:

- scrape course content
- download Wistia videos
- store large raw transcript/JPEG libraries
- store large OHLCV datasets
- submit live trades
- connect to a live Alpaca account
- implement live trading logic
- treat course examples as final rules
- treat historical replay as proof of profitability
- treat paper trades as live-readiness approval

## Recommended setup

Recommended location:

```bash
mkdir -p /home/scott/projects/openclaw-monster-academy-strategy-lab
cd /home/scott/projects/openclaw-monster-academy-strategy-lab
```

Suggested initial files:

```text
AGENTS.md
PROJECT_BRIEF.md
README.md
TODO.md
requirements.txt
.env.example
.gitignore
```

## Directory structure

```text
.
├── AGENTS.md
├── PROJECT_BRIEF.md
├── README.md
├── TODO.md
├── requirements.txt
├── .env.example
├── .gitignore
│
├── docs/
│   ├── phases/
│   ├── architecture/
│   ├── operations/
│   └── prompts/
│
├── knowledge_base/
│   ├── glossary/
│   ├── concepts/
│   ├── rule_candidates/
│   ├── examples/
│   ├── validation_matrices/
│   ├── replay_labels/
│   └── paper_trade_findings/
│
├── evidence/
│   ├── google_drive_refs/
│   ├── source_manifests/
│   └── evidence_crosswalks/
│
├── data_refs/
│   ├── historical_market_data/
│   ├── alpaca/
│   └── google_drive/
│
├── replay/
│   ├── cases/
│   ├── contradiction_cases/
│   ├── labels/
│   └── reports/
│
├── paper_validation/
│   ├── readiness_gates/
│   ├── paper_trade_candidates/
│   ├── alpaca_paper_runs/
│   ├── journals/
│   └── reports/
│
├── configs/
├── src/
├── tests/
├── runs/
├── artifacts/
└── logs/
```

## Phase documents

Canonical phase documents should live under:

```text
docs/phases/
```

Recommended layout:

```text
docs/phases/phase-01-glossary/
├── PHASE_1_GLOSSARY.md
├── PHASE_1_1_GLOSSARY_REFINEMENT.md
└── notes/

docs/phases/phase-02-concept-model/
├── PHASE_2_CONCEPT_MODEL.md
├── PHASE_2_1_CONCEPT_MODEL_HISTORICAL_REPLAY_UPDATE.md
└── diagrams/

docs/phases/phase-03-rule-candidates/
├── PHASE_3_RULE_CANDIDATES.md
├── PHASE_3_1_RULE_CANDIDATES_HISTORICAL_REPLAY_UPDATE.md
└── candidate-cards/

docs/phases/phase-04-example-library/
├── PHASE_4_EXAMPLE_LIBRARY.md
├── PHASE_4_1_EXAMPLE_LIBRARY_HISTORICAL_REPLAY_UPDATE.md
└── example-cards/

docs/phases/phase-05-validation/
├── PHASE_5_VALIDATION_MATRIX.md
├── PHASE_5_1_VALIDATION_MATRIX_HISTORICAL_REPLAY_UPDATE.md
├── PHASE_5B_HISTORICAL_VALIDATION_PLAN.md
└── validation-notes/

docs/phases/phase-06-rule-refinement/
├── PHASE_6_RULE_REFINEMENT.md
├── PHASE_6_PAPER_TRADE_READINESS_GATES.md
└── candidate-promotions/

docs/phases/phase-07-paper-validation/
├── PHASE_7_ALPACA_PAPER_VALIDATION_PLAN.md
├── PHASE_7_PAPER_TRADE_RESULTS.md
└── paper-validation-reports/

docs/phases/phase-08-live-readiness-review/
├── PHASE_8_LIVE_READINESS_REVIEW.md
└── risk-review/
```

## Evidence and Google Drive references

Raw course and Drive artifacts should generally remain in Google Drive or the archiver repo.

Use this repo for indexes, references, and crosswalks:

```text
evidence/google_drive_refs/
├── transcripts/
├── snapshot_maps/
├── jpeg_snapshots/
├── lesson_indexes/
└── drive_inventory/
```

Useful manifests:

```text
evidence/source_manifests/
├── transcript_manifest.yaml
├── snapshot_manifest.yaml
├── historical_data_manifest.yaml
└── paper_trade_manifest.yaml
```

Useful crosswalks:

```text
evidence/evidence_crosswalks/
├── phase_to_source_crosswalk.md
├── example_to_snapshot_crosswalk.md
├── rule_candidate_to_example_crosswalk.md
└── replay_case_to_candidate_crosswalk.md
```

## Historical replay

Historical replay cases belong under:

```text
replay/cases/
```

Contradiction cases belong under:

```text
replay/contradiction_cases/
```

Replay labels belong under:

```text
replay/labels/
```

Example labels:

```text
range_labels/
support_resistance_labels/
target_labels/
break_behavior_labels/
invalidation_labels/
```

Replay cases are evidence records, not trades.

A replay case can say:

```text
This window contains a daily range, a 78 close-break, and later movement toward the labeled target.
```

A replay case must not say:

```text
Buy when this happens.
This strategy is profitable.
This is ready for Alpaca live trading.
```

## Paper validation

Paper validation belongs under:

```text
paper_validation/
```

Recommended subfolders:

```text
paper_validation/readiness_gates/
paper_validation/paper_trade_candidates/
paper_validation/alpaca_paper_runs/
paper_validation/journals/
paper_validation/reports/
```

Paper validation should begin with dry-run observation before paper orders are enabled.

Paper validation should test candidate behavior, not chase profit.

## Alpaca policy

Use Alpaca paper-account validation only after Phase 6 readiness gates exist.

Required boundaries:

- paper mode only
- no live account keys
- no order submission by default
- dry-run mode first
- explicit approval before enabling paper orders
- paper journal required
- abort rules required
- no live-readiness claims

## Suggested Python package layout

```text
src/monster_strategy_lab/
├── __init__.py
├── cli.py
├── config/
├── evidence/
├── replay/
├── labeling/
├── validation/
├── paper/
├── alpaca/
└── reports/
```

Do not implement trading logic until the documentation, replay labels, and paper-readiness gates are stable.

## Suggested CLI direction

Future CLI commands may include:

```bash
python -m monster_strategy_lab.cli inventory
python -m monster_strategy_lab.cli validate-docs
python -m monster_strategy_lab.cli replay-case HR-001
python -m monster_strategy_lab.cli contradiction-case HC-001
python -m monster_strategy_lab.cli paper-dry-run --candidate PTC-001
python -m monster_strategy_lab.cli paper-report --run RUN-001
```

These commands are suggestions only until implemented.

## Current initialization checklist

1. Add `AGENTS.md`.
2. Add `PROJECT_BRIEF.md`.
3. Add `README.md`.
4. Add `TODO.md`.
5. Create the recommended directory tree.
6. Move or copy phase documents into `docs/phases/`.
7. Create source manifests under `evidence/source_manifests/`.
8. Create historical data references under `data_refs/historical_market_data/`.
9. Create replay templates under `replay/cases/` and `replay/contradiction_cases/`.
10. Create paper candidate templates under `paper_validation/paper_trade_candidates/`.
11. Do not implement paper orders until Phase 6 readiness gates exist.

## Development posture

Use small, auditable changes.

Prefer Markdown, YAML manifests, and tests before code-heavy automation.

Prefer dry-run and report-only commands before any paper-account action.

Every candidate promotion should be evidence-backed and reversible.
