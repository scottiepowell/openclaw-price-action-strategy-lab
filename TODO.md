# TODO.md — Monster Academy Strategy Lab

## Current priority

Initialize the Strategy Lab as a separate repository focused on documentation, evidence organization, historical replay preparation, Phase 6 rule refinement, and later Alpaca paper-account validation.

Do not begin with trading automation.

---

## Phase 0 — Repo initialization

### P0.1 Create repo

- [x] Create repo folder:

```bash
mkdir -p /home/scott/projects/openclaw-monster-academy-strategy-lab
cd /home/scott/projects/openclaw-monster-academy-strategy-lab
```

- [x] Initialize Git:

```bash
git init
```

- [x] Add initial files:

```text
AGENTS.md
PROJECT_BRIEF.md
README.md
TODO.md
requirements.txt
.env.example
.gitignore
```

### P0.2 Create base directory tree

- [x] Create docs folders:

```text
docs/phases/phase-01-glossary/
docs/phases/phase-02-concept-model/
docs/phases/phase-03-rule-candidates/
docs/phases/phase-04-example-library/
docs/phases/phase-05-validation/
docs/phases/phase-06-rule-refinement/
docs/phases/phase-07-paper-validation/
docs/phases/phase-08-live-readiness-review/
docs/architecture/
docs/operations/
docs/prompts/
```

- [x] Create knowledge-base folders:

```text
knowledge_base/glossary/
knowledge_base/concepts/
knowledge_base/rule_candidates/
knowledge_base/examples/
knowledge_base/validation_matrices/
knowledge_base/replay_labels/
knowledge_base/paper_trade_findings/
```

- [x] Create evidence folders:

```text
evidence/google_drive_refs/transcripts/
evidence/google_drive_refs/snapshot_maps/
evidence/google_drive_refs/jpeg_snapshots/
evidence/google_drive_refs/lesson_indexes/
evidence/google_drive_refs/drive_inventory/
evidence/source_manifests/
evidence/evidence_crosswalks/
```

- [x] Create data reference folders:

```text
data_refs/historical_market_data/
data_refs/alpaca/
data_refs/google_drive/
```

- [x] Create replay folders:

```text
replay/cases/
replay/contradiction_cases/
replay/labels/range_labels/
replay/labels/support_resistance_labels/
replay/labels/target_labels/
replay/labels/break_behavior_labels/
replay/labels/invalidation_labels/
replay/reports/
```

- [x] Create paper-validation folders:

```text
paper_validation/readiness_gates/
paper_validation/paper_trade_candidates/
paper_validation/alpaca_paper_runs/dry_run/
paper_validation/alpaca_paper_runs/simulated_orders/
paper_validation/alpaca_paper_runs/paper_orders/
paper_validation/journals/daily_journal/
paper_validation/journals/trade_review/
paper_validation/journals/failure_reviews/
paper_validation/reports/
```

- [x] Create implementation folders:

```text
configs/
src/monster_strategy_lab/
tests/unit/
tests/integration/
tests/fixtures/
tests/live_opt_in/
runs/replay/
runs/validation/
runs/dry_run/
runs/paper_validation/
artifacts/reports/
artifacts/exports/
artifacts/charts/
artifacts/packages/
logs/replay/
logs/validation/
logs/alpaca_paper/
logs/errors/
```

---

## Phase 1 — Move phase documents into canonical folders

- [x] Add Phase 1 document:

```text
docs/phases/phase-01-glossary/PHASE_1_GLOSSARY.md
```

- [x] Add future Phase 1.1 placeholder:

```text
docs/phases/phase-01-glossary/PHASE_1_1_GLOSSARY_REFINEMENT.md
```

- [x] Add Phase 2 documents:

```text
docs/phases/phase-02-concept-model/PHASE_2_CONCEPT_MODEL.md
docs/phases/phase-02-concept-model/PHASE_2_1_CONCEPT_MODEL_HISTORICAL_REPLAY_UPDATE.md
```

- [x] Add Phase 3 documents:

```text
docs/phases/phase-03-rule-candidates/PHASE_3_RULE_CANDIDATES.md
docs/phases/phase-03-rule-candidates/PHASE_3_1_RULE_CANDIDATES_HISTORICAL_REPLAY_UPDATE.md
```

- [x] Add Phase 4 documents:

```text
docs/phases/phase-04-example-library/PHASE_4_EXAMPLE_LIBRARY.md
docs/phases/phase-04-example-library/PHASE_4_1_EXAMPLE_LIBRARY_HISTORICAL_REPLAY_UPDATE.md
```

- [x] Add Phase 5 documents:

```text
docs/phases/phase-05-validation/PHASE_5_VALIDATION_MATRIX.md
docs/phases/phase-05-validation/PHASE_5_1_VALIDATION_MATRIX_HISTORICAL_REPLAY_UPDATE.md
docs/phases/phase-05-validation/PHASE_5B_HISTORICAL_VALIDATION_PLAN.md
```

- [x] Add Phase 6 placeholders:

```text
docs/phases/phase-06-rule-refinement/PHASE_6_RULE_REFINEMENT.md
docs/phases/phase-06-rule-refinement/PHASE_6_PAPER_TRADE_READINESS_GATES.md
docs/phases/phase-06-rule-refinement/candidate-promotions/PHASE_6_CANDIDATE_PROMOTION_CRITERIA.md
```

- [x] Add Phase 7 placeholders:

```text
docs/phases/phase-07-paper-validation/PHASE_7_ALPACA_PAPER_VALIDATION_PLAN.md
docs/phases/phase-07-paper-validation/PHASE_7_PAPER_TRADE_RESULTS.md
```

- [x] Add Phase 8 placeholder:

```text
docs/phases/phase-08-live-readiness-review/PHASE_8_LIVE_READINESS_REVIEW.md
```

---

## Phase 2 — Source manifests and evidence references

### P2.1 Google Drive references

- [x] Create transcript index:

```text
evidence/google_drive_refs/transcripts/transcript_index.yaml
```

- [x] Create snapshot-map index:

```text
evidence/google_drive_refs/snapshot_maps/snapshot_map_index.yaml
```

- [x] Create JPEG snapshot index:

```text
evidence/google_drive_refs/jpeg_snapshots/jpeg_snapshot_index.yaml
```

- [x] Create lesson index:

```text
evidence/google_drive_refs/lesson_indexes/lesson_index.yaml
```

- [x] Create Drive inventory summary:

```text
evidence/google_drive_refs/drive_inventory/google_drive_inventory.md
```

### P2.2 Source manifests

- [x] Create transcript manifest:

```text
evidence/source_manifests/transcript_manifest.yaml
```

- [x] Create snapshot manifest:

```text
evidence/source_manifests/snapshot_manifest.yaml
```

- [x] Create historical data manifest:

```text
evidence/source_manifests/historical_data_manifest.yaml
```

- [x] Create paper trade manifest placeholder:

```text
evidence/source_manifests/paper_trade_manifest.yaml
```

### P2.3 Evidence crosswalks

- [x] Create phase-to-source crosswalk:

```text
evidence/evidence_crosswalks/phase_to_source_crosswalk.md
```

- [x] Create example-to-snapshot crosswalk:

```text
evidence/evidence_crosswalks/example_to_snapshot_crosswalk.md
```

- [x] Create rule-candidate-to-example crosswalk:

```text
evidence/evidence_crosswalks/rule_candidate_to_example_crosswalk.md
```

- [x] Create replay-case-to-candidate crosswalk:

```text
evidence/evidence_crosswalks/replay_case_to_candidate_crosswalk.md
```

---

## Phase 3 — Historical data references

- [x] Create historical data artifact index:

```text
data_refs/historical_market_data/artifact_index.yaml
```

- [x] Create local path example file:

```text
data_refs/historical_market_data/local_paths.example.yaml
```

- [x] Create data quality summary:

```text
data_refs/historical_market_data/data_quality_summary.md
```

- [x] Record known symbols:

```text
SPY
QQQ
AAPL
MSFT
NVDA
AMZN
GOOGL
META
TSLA
AVGO
IWM
```

- [x] Record known timeframes:

```text
1Min
5Min
1Day
```

- [x] Record whether files are local, in Google Drive, or produced by the historical data extraction repo.
- [ ] Do not copy large OHLCV files into this repo unless explicitly required.

---

## Phase 4 — Replay templates

### P4.1 Replay case template

- [x] Create:

```text
replay/cases/OPEN-HR-template.md
```

Template should include:

```text
Replay ID
Linked Example ID
Symbol
Date window
Data files
Data quality status
Timeframes used
Concepts labeled
Phase 3.1 candidates tested
Replay labels
Replay outcome
Contradiction notes
Phase 6 impact
Boundary: no trade signal, no profitability claim, no execution readiness
```

### P4.2 Contradiction case template

- [x] Create:

```text
replay/contradiction_cases/HC-template.md
```

Template should include:

```text
Contradiction ID
Candidate being challenged
Failure type
Symbol
Date window
Replay labels
Why this weakens or narrows the candidate
Decision impact
Boundary
```

### P4.3 Label dictionaries

- [x] Create range label dictionary:

```text
replay/labels/range_labels/range_label_dictionary.yaml
```

- [x] Create support/resistance label dictionary:

```text
replay/labels/support_resistance_labels/support_resistance_label_dictionary.yaml
```

- [x] Create target label dictionary:

```text
replay/labels/target_labels/target_label_dictionary.yaml
```

- [x] Create break behavior label dictionary:

```text
replay/labels/break_behavior_labels/break_behavior_label_dictionary.yaml
```

- [x] Create invalidation label dictionary:

```text
replay/labels/invalidation_labels/invalidation_label_dictionary.yaml
```

---

## Phase 5 — Candidate index and structured knowledge base

- [x] Create candidate index:

```text
knowledge_base/rule_candidates/candidate_index.yaml
```

- [x] Create 78 decision family index:

```text
knowledge_base/rule_candidates/78_decision_level_family.yaml
```

- [x] Create current range candidate index:

```text
knowledge_base/rule_candidates/current_range_candidates.yaml
```

- [x] Create support/resistance candidate index:

```text
knowledge_base/rule_candidates/support_resistance_candidates.yaml
```

- [x] Create target activation candidate index:

```text
knowledge_base/rule_candidates/target_activation_candidates.yaml
```

- [x] Create no-trade filter index:

```text
knowledge_base/rule_candidates/no_trade_filters.yaml
```

- [x] Create paper-trade candidate readiness index:

```text
knowledge_base/rule_candidates/paper_trade_candidate_readiness.yaml
```

---

## Phase 6 — Rule refinement preparation

Do not start this until Phase 3.1, Phase 4.1, and Phase 5.1 are organized in the repo.

- [x] Create Phase 6 rule refinement document.
- [x] Create Phase 6 paper-trade readiness gate document.
- [x] Define candidate promotion criteria.
- [x] Define required evidence before paper validation.
- [x] Define required contradiction search before paper validation.
- [x] Define no-trade filters.
- [x] Define invalidation requirements.
- [x] Define target requirements.
- [x] Define room-to-target requirements.
- [x] Define timeframe alignment requirements.
- [x] Define support/resistance context requirements.
- [x] Mirror candidate promotion criteria into `paper_validation/readiness_gates/`.

No Alpaca paper orders in this phase.

---

## Phase 7 — Paper validation preparation

Do not start this until Phase 6 readiness gates exist.

### P7.1 Paper account config

- [x] Create Alpaca paper config example:

```text
data_refs/alpaca/paper_account_config.example.yaml
```

- [x] Create symbol universe config:

```text
data_refs/alpaca/symbol_universe.yaml
```

- [x] Create feed config example:

```text
data_refs/alpaca/feed_config.example.yaml
```

- [ ] Do not commit real API keys.
- [ ] Do not use live account keys.

### P7.2 Paper candidate template

- [x] Create:

```text
paper_validation/paper_trade_candidates/PTC-template.md
```

Template should include:

```text
Paper Candidate ID
Related Phase 3.1 candidate
Related replay cases
Related contradiction cases
Required context
Target
Room to target
Invalidation
No-trade filters
Dry-run status
Paper order status
Results
Review decision
Boundary
```

### P7.3 Readiness gates

- [x] Create:

```text
paper_validation/readiness_gates/candidate_readiness_template.md
paper_validation/readiness_gates/no_trade_filters.md
paper_validation/readiness_gates/promotion_checklist.md
```

### P7.4 Journals

- [x] Create daily journal template:

```text
paper_validation/journals/daily_journal/daily_journal_template.md
```

- [x] Create trade review template:

```text
paper_validation/journals/trade_review/trade_review_template.md
```

- [x] Create failure review template:

```text
paper_validation/journals/failure_reviews/failure_review_template.md
```

---

## Phase 8 — Future code scaffolding

Do not build order logic yet.

- [x] Create Python package skeleton:

```text
src/monster_strategy_lab/__init__.py
src/monster_strategy_lab/cli.py
src/monster_strategy_lab/config/
src/monster_strategy_lab/evidence/
src/monster_strategy_lab/replay/
src/monster_strategy_lab/labeling/
src/monster_strategy_lab/validation/
src/monster_strategy_lab/paper/
src/monster_strategy_lab/alpaca/
src/monster_strategy_lab/reports/
```

- [x] Add tests for config loading.
- [x] Add tests for manifest parsing.
- [x] Add tests for replay label schemas.
- [x] Add tests for candidate readiness gate schemas.
- [x] Add tests for paper validation dry-run output.
- [ ] Do not implement real order submission until explicitly approved.

---

## Phase 9 — Safety and operations documents

- [x] Create system overview:

```text
docs/architecture/SYSTEM_OVERVIEW.md
```

- [x] Create data flow document:

```text
docs/architecture/DATA_FLOW.md
```

- [x] Create replay engine design:

```text
docs/architecture/REPLAY_ENGINE_DESIGN.md
```

- [x] Create paper validation design:

```text
docs/architecture/PAPER_VALIDATION_DESIGN.md
```

- [x] Create Alpaca boundaries document:

```text
docs/architecture/ALPACA_BOUNDARIES.md
```

- [x] Create runbook:

```text
docs/operations/RUNBOOK.md
```

- [x] Create validation checklist:

```text
docs/operations/VALIDATION_CHECKLIST.md
```

- [x] Create paper account checklist:

```text
docs/operations/PAPER_ACCOUNT_CHECKLIST.md
```

- [x] Create incident and abort rules:

```text
docs/operations/INCIDENT_AND_ABORT_RULES.md
```

---

## Important blockers before paper trading

Do not submit Alpaca paper orders until all of the following exist:

- [x] Phase 6 rule refinement document.
- [x] Phase 6 paper-trade readiness gates.
- [x] At least one paper-trade candidate file.
- [x] Linked replay evidence for that candidate.
- [x] Linked contradiction evidence or contradiction-search note.
- [x] Target definition.
- [x] Room-to-target requirement.
- [x] Invalidation definition.
- [x] No-trade filters.
- [x] Higher-timeframe context requirement.
- [x] Dry-run report.
- [x] Paper account checklist.
- [x] Abort rules.
- [x] Explicit paper-only config.

---

## Near-term next actions

1. Create repo and directory tree.
2. Add AGENTS.md, PROJECT_BRIEF.md, README.md, and TODO.md.
3. Place phase documents under `docs/phases/`.
4. Create evidence and source manifest placeholders.
5. Create replay and contradiction templates.
6. Create paper-candidate templates but do not enable paper trading.
7. Ask OpenClaw/Codex to validate the repo structure and generate missing placeholder files.

---

## OpenClaw handoff prompt seed

```text
You are working in /home/scott/projects/openclaw-monster-academy-strategy-lab.

Read AGENTS.md, PROJECT_BRIEF.md, README.md, and TODO.md first.

Initialize the repository structure exactly as described in TODO.md.

Do not implement trading logic.
Do not submit Alpaca orders.
Do not connect to live trading.
Do not copy large Google Drive artifacts or OHLCV files into this repo.

Create directories, placeholder README files where useful, source manifest templates, replay case templates, contradiction case templates, and paper-trade candidate templates.

Report:
1. files created
2. directories created
3. validation command run
4. anything intentionally left as placeholder
5. next recommended step
```
