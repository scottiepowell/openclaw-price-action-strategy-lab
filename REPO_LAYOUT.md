openclaw-monster-academy-strategy-lab/
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
│   │   ├── phase-01-glossary/
│   │   │   ├── PHASE_1_GLOSSARY.md
│   │   │   ├── PHASE_1_1_GLOSSARY_REFINEMENT.md
│   │   │   └── notes/
│   │   │
│   │   ├── phase-02-concept-model/
│   │   │   ├── PHASE_2_CONCEPT_MODEL.md
│   │   │   ├── PHASE_2_1_CONCEPT_MODEL_HISTORICAL_REPLAY_UPDATE.md
│   │   │   └── diagrams/
│   │   │
│   │   ├── phase-03-rule-candidates/
│   │   │   ├── PHASE_3_RULE_CANDIDATES.md
│   │   │   ├── PHASE_3_1_RULE_CANDIDATES_HISTORICAL_REPLAY_UPDATE.md
│   │   │   └── candidate-cards/
│   │   │
│   │   ├── phase-04-example-library/
│   │   │   ├── PHASE_4_EXAMPLE_LIBRARY.md
│   │   │   ├── PHASE_4_1_EXAMPLE_LIBRARY_HISTORICAL_REPLAY_UPDATE.md
│   │   │   └── example-cards/
│   │   │
│   │   ├── phase-05-validation/
│   │   │   ├── PHASE_5_VALIDATION_MATRIX.md
│   │   │   ├── PHASE_5_1_VALIDATION_MATRIX_HISTORICAL_REPLAY_UPDATE.md
│   │   │   ├── PHASE_5B_HISTORICAL_VALIDATION_PLAN.md
│   │   │   └── validation-notes/
│   │   │
│   │   ├── phase-06-rule-refinement/
│   │   │   ├── PHASE_6_RULE_REFINEMENT.md
│   │   │   ├── PHASE_6_PAPER_TRADE_READINESS_GATES.md
│   │   │   └── candidate-promotions/
│   │   │
│   │   ├── phase-07-paper-validation/
│   │   │   ├── PHASE_7_ALPACA_PAPER_VALIDATION_PLAN.md
│   │   │   ├── PHASE_7_PAPER_TRADE_RESULTS.md
│   │   │   └── paper-validation-reports/
│   │   │
│   │   └── phase-08-live-readiness-review/
│   │       ├── PHASE_8_LIVE_READINESS_REVIEW.md
│   │       └── risk-review/
│   │
│   ├── architecture/
│   │   ├── SYSTEM_OVERVIEW.md
│   │   ├── DATA_FLOW.md
│   │   ├── REPLAY_ENGINE_DESIGN.md
│   │   ├── PAPER_VALIDATION_DESIGN.md
│   │   └── ALPACA_BOUNDARIES.md
│   │
│   ├── operations/
│   │   ├── RUNBOOK.md
│   │   ├── VALIDATION_CHECKLIST.md
│   │   ├── PAPER_ACCOUNT_CHECKLIST.md
│   │   └── INCIDENT_AND_ABORT_RULES.md
│   │
│   └── prompts/
│       ├── openclaw-prompts/
│       ├── codex-prompts/
│       └── phase-generation-prompts/
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
│   │   ├── transcripts/
│   │   ├── snapshot_maps/
│   │   ├── jpeg_snapshots/
│   │   ├── lesson_indexes/
│   │   └── drive_inventory/
│   │
│   ├── source_manifests/
│   │   ├── transcript_manifest.yaml
│   │   ├── snapshot_manifest.yaml
│   │   ├── historical_data_manifest.yaml
│   │   └── paper_trade_manifest.yaml
│   │
│   └── evidence_crosswalks/
│       ├── phase_to_source_crosswalk.md
│       ├── example_to_snapshot_crosswalk.md
│       ├── rule_candidate_to_example_crosswalk.md
│       └── replay_case_to_candidate_crosswalk.md
│
├── data_refs/
│   ├── historical_market_data/
│   │   ├── README.md
│   │   ├── local_paths.example.yaml
│   │   └── artifact_index.yaml
│   │
│   ├── alpaca/
│   │   ├── paper_account_config.example.yaml
│   │   ├── symbol_universe.yaml
│   │   └── feed_config.example.yaml
│   │
│   └── google_drive/
│       ├── drive_paths.example.yaml
│       └── upload_download_notes.md
│
├── replay/
│   ├── cases/
│   │   ├── HR-001.md
│   │   ├── HR-002.md
│   │   └── OPEN-HR-template.md
│   │
│   ├── contradiction_cases/
│   │   ├── HC-001.md
│   │   └── HC-template.md
│   │
│   ├── labels/
│   │   ├── range_labels/
│   │   ├── support_resistance_labels/
│   │   ├── target_labels/
│   │   ├── break_behavior_labels/
│   │   └── invalidation_labels/
│   │
│   └── reports/
│       ├── replay_summary.md
│       ├── contradiction_summary.md
│       └── replay_quality_report.md
│
├── paper_validation/
│   ├── readiness_gates/
│   │   ├── candidate_readiness_template.md
│   │   ├── no_trade_filters.md
│   │   └── promotion_checklist.md
│   │
│   ├── paper_trade_candidates/
│   │   ├── PTC-001.md
│   │   └── PTC-template.md
│   │
│   ├── alpaca_paper_runs/
│   │   ├── run_manifest.yaml
│   │   ├── dry_run/
│   │   ├── simulated_orders/
│   │   └── paper_orders/
│   │
│   ├── journals/
│   │   ├── daily_journal/
│   │   ├── trade_review/
│   │   └── failure_reviews/
│   │
│   └── reports/
│       ├── paper_validation_summary.md
│       ├── rule_candidate_performance.md
│       └── invalidation_failures.md
│
├── configs/
│   ├── default.yaml
│   ├── symbol_universe.yaml
│   ├── replay_config.yaml
│   ├── paper_validation_config.example.yaml
│   └── risk_limits.example.yaml
│
├── src/
│   └── monster_strategy_lab/
│       ├── __init__.py
│       ├── cli.py
│       ├── config/
│       ├── evidence/
│       ├── replay/
│       ├── labeling/
│       ├── validation/
│       ├── paper/
│       ├── alpaca/
│       └── reports/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── fixtures/
│   └── live_opt_in/
│
├── runs/
│   ├── replay/
│   ├── validation/
│   ├── dry_run/
│   └── paper_validation/
│
├── artifacts/
│   ├── reports/
│   ├── exports/
│   ├── charts/
│   └── packages/
│
└── logs/
    ├── replay/
    ├── validation/
    ├── alpaca_paper/
    └── errors/