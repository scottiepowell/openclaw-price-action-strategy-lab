# AGENTS.md — Monster Academy Strategy Lab

## Project

Name: `openclaw-monster-academy-strategy-lab`

Recommended root:

```text
/home/scott/projects/openclaw-monster-academy-strategy-lab
```

## Mission

You are developing the Monster Academy strategy-analysis and validation project.

This project turns course-derived material, strategy documents, transcript/JPEG evidence, and historical OHLCV replay evidence into a conservative, auditable strategy knowledge base.

The project may eventually support a future application that analyzes market structure, support/resistance, targets, replay labels, and candidate setup states.

The project must not build a live-trading bot.

The project must not place trades.

The project must not create execution-ready rules unless Scott explicitly creates a later approved execution project with separate boundaries.

## Relationship to other repos

This project is separate from:

```text
/home/scott/projects/openclaw-monster-academy-archiver
/home/scott/projects/openclaw-historical-market-data-extraction
```

Use the archiver repo for:

- Wistia/course capture
- transcript extraction
- snapshot extraction
- raw lesson URLs
- raw media/download runs
- capture logs
- raw capture status files

Use the historical market data extraction repo for:

- Alpaca market-data download
- OHLCV normalization
- data packaging
- data-quality reports
- Parquet/CSV artifacts
- optional Google Drive upload

Use this strategy-lab repo for:

- strategy knowledge-base documents
- glossary and concept-model updates
- rule-candidate analysis
- example-library evidence organization
- validation matrices
- historical replay labels
- contradiction cases
- Phase 6 conservative rule refinement
- non-execution analysis tooling
- future UI or review workflows, if approved

Do not merge capture/extraction logic into this repo unless Scott explicitly approves.

Do not turn the archiver into the strategy app.

The clean boundary is:

```text
archiver repo
  -> captures course evidence

historical data extractor repo
  -> captures market-data evidence

strategy lab repo
  -> interprets and validates evidence
```

## Repo boundary

Operate only inside this repo unless Scott explicitly asks.

Do not modify:

```text
/home/scott/projects/openclaw-self
/home/scott/projects/openclaw-home-media
/home/scott/projects/openclaw-monster-academy-archiver
/home/scott/projects/openclaw-historical-market-data-extraction
other /home/scott/projects/* repositories
~/.openclaw
/etc
/opt
/var
```

Do not scan unrelated projects.

Use absolute paths only when necessary and explain why.

When referencing source artifacts from other repos, prefer read-only paths and document the source path in a manifest or evidence record.

## Non-goals and safety boundaries

Do not build live trading logic.

Do not implement Alpaca order placement.

Do not submit paper orders.

Do not submit live orders.

Do not connect to brokerage trading endpoints.

Do not create options order logic.

Do not create final buy/sell signals.

Do not claim profitability.

Do not claim win rate, edge, expectancy, or risk/reward performance unless a later approved research process explicitly produces those metrics with documented assumptions.

Do not promote any candidate to live-trading readiness.

Do not promote any candidate to paper-trading readiness unless Scott creates a separate paper-trading research phase and explicitly approves it.

Do not treat any of the following as an automatic entry:

- 78 break
- 78 close break
- support break
- resistance break
- candle-derived level break
- same-candle range interaction
- current-range target activation
- role flip
- last green candle resistance break
- last red candle support break
- higher-high / lower-low direction shift

Preserve this principle:

```text
A level break is not an entry.

A level break is a candidate confirmation.

It becomes an entry candidate only when:
direction agrees,
target exists,
room to target exists,
support/resistance context agrees,
timeframe context agrees,
confirmation quality is adequate,
and invalidation is defined.
```

Even then, in this project it remains an analysis label, not an order.

## Financial and compliance boundary

All work in this repo is educational, analytical, and research-oriented.

Do not present output as financial advice.

Do not tell Scott to buy, sell, short, hold, or trade a symbol.

Do not recommend position size, stop loss, take profit, expiration, contract selection, or order type.

Do not optimize for profitability without an explicit later research scope.

Do not create code that can accidentally place orders.

If a task appears to cross into trading execution, stop and ask Scott to create or approve a separate execution-boundary document first.

## Strategy source context

The strategy knowledge base currently includes or may include:

- Phase 1 Glossary
- Phase 2 Strategy Concept Model
- Phase 2.1 Concept Model Historical Replay Update
- Phase 3 Rule Candidate Extraction
- Phase 3.1 Rule Candidates Historical Replay Update
- Phase 4 Example Library
- Phase 4.1 Example Library Historical Replay Update
- Phase 5 Validation Matrix
- Phase 5.1 Validation Matrix Historical Replay Update
- Phase 5B Historical Validation Plan
- transcript files
- snapshot-map files
- JPEG snapshot references
- historical OHLCV data inventory and manifests

These documents are evidence and modeling artifacts.

They are not final trading rules.

## Required reading order

Before making changes:

1. Read this `AGENTS.md`.
2. Read `PROJECT_BRIEF.md` when the task needs full project context.
3. Read `TODO.md` when the task concerns priorities.
4. Read `docs/INDEX.md` if present.
5. Read only the phase documents directly relevant to the task.
6. Read source evidence only as needed.
7. Inspect only files directly relevant to the task.
8. Make the smallest safe change.
9. Validate using targeted tests, document checks, or dry-runs.
10. Report exact files changed, validation performed, and known risks.

Do not load huge transcript sets, JPEG trees, logs, market-data files, or generated artifacts unless the task requires them.

Do not scan the whole repository by default.

## Recommended project layout

Use this structure unless Scott approves a different one:

```text
.
├── AGENTS.md
├── PROJECT_BRIEF.md
├── README.md
├── TODO.md
├── requirements.txt
├── pyproject.toml
├── .gitignore
├── configs/
│   ├── symbols.yaml
│   ├── replay_defaults.yaml
│   └── source_paths.example.yaml
├── docs/
│   ├── INDEX.md
│   ├── phases/
│   │   ├── phase-1-glossary/
│   │   ├── phase-2-concept-model/
│   │   ├── phase-2-1-historical-replay-model/
│   │   ├── phase-3-rule-candidates/
│   │   ├── phase-3-1-rule-candidates-replay/
│   │   ├── phase-4-example-library/
│   │   ├── phase-4-1-example-library-replay/
│   │   ├── phase-5-validation-matrix/
│   │   ├── phase-5-1-validation-matrix-replay/
│   │   ├── phase-5b-historical-validation-plan/
│   │   └── phase-6-rule-refinement/
│   ├── decisions/
│   ├── architecture/
│   ├── workflows/
│   └── handoff/
├── knowledge_base/
│   ├── glossary/
│   ├── concepts/
│   ├── rule_candidates/
│   ├── examples/
│   ├── validation/
│   ├── replay_cases/
│   ├── contradiction_cases/
│   ├── evidence_manifests/
│   └── source_indexes/
├── data_refs/
│   ├── README.md
│   ├── course_artifacts_manifest.yaml
│   ├── historical_data_manifest.yaml
│   └── google_drive_manifest.yaml
├── src/
│   └── monster_strategy_lab/
│       ├── __init__.py
│       ├── cli.py
│       ├── config.py
│       ├── evidence/
│       ├── replay/
│       ├── validation/
│       ├── reports/
│       └── models/
├── tests/
│   ├── fixtures/
│   ├── test_config.py
│   ├── test_evidence_models.py
│   ├── test_replay_case_schema.py
│   └── test_validation_matrix_schema.py
├── notebooks/
│   └── README.md
├── reports/
├── runs/
├── logs/
└── artifacts/
```

## Documentation organization rules

Use `docs/phases/` for human-authored phase documents.

Use `knowledge_base/` for normalized, queryable, or structured strategy knowledge.

Use `data_refs/` for references to external artifacts, not large raw files.

Use `runs/` for generated run outputs.

Use `reports/` for human-readable summaries.

Use `artifacts/` for generated files intended to be preserved or shared.

Do not store large raw video, audio, JPEG collections, Parquet datasets, or downloaded market-data warehouses in this repo unless Scott explicitly approves.

Prefer manifests pointing to the archiver repo, historical data repo, or Google Drive.

## Naming conventions

Use stable phase names:

```text
PHASE_1_GLOSSARY.md
PHASE_2_CONCEPT_MODEL.md
PHASE_2_1_CONCEPT_MODEL_HISTORICAL_REPLAY_UPDATE.md
PHASE_3_RULE_CANDIDATES.md
PHASE_3_1_RULE_CANDIDATES_HISTORICAL_REPLAY_UPDATE.md
PHASE_4_EXAMPLE_LIBRARY.md
PHASE_4_1_EXAMPLE_LIBRARY_HISTORICAL_REPLAY_UPDATE.md
PHASE_5_VALIDATION_MATRIX.md
PHASE_5_1_VALIDATION_MATRIX_HISTORICAL_REPLAY_UPDATE.md
PHASE_5B_HISTORICAL_VALIDATION_PLAN.md
PHASE_6_RULE_REFINEMENT.md
```

When creating iterations, use:

```text
v0.1
v0.2
v1.0
v1.1
```

Do not overwrite prior phase documents without preserving history or creating an updated version.

## Evidence model

Treat every claim as evidence-bound.

Allowed evidence types:

```text
glossary_evidence
concept_model_evidence
rule_candidate_evidence
example_library_evidence
validation_matrix_evidence
transcript_evidence
snapshot_map_evidence
jpeg_reference_evidence
historical_ohlcv_evidence
historical_replay_evidence
contradiction_replay_evidence
manual_review_evidence
```

Every replay or validation artifact should be able to point back to:

- source document
- lesson or transcript
- timestamp, if known
- JPEG path or snapshot reference, if known
- symbol
- timeframe
- date window
- data file or manifest
- reviewer or run id
- data quality status

## Historical replay boundary

Historical replay is allowed only for:

- validation
- contradiction testing
- evidence maturity
- replay labeling
- example strengthening
- candidate narrowing
- candidate splitting
- no-trade filter discovery
- Phase 6 readiness assessment

Historical replay is not a backtest.

Historical replay is not a profitability claim.

Historical replay is not an order simulator.

Historical replay must not create trade recommendations.

## Historical replay object expectations

Use replay cases like:

```yaml
replay_case:
  replay_id: HR-001
  linked_example_id: EX-014
  symbol: NVDA
  date_window:
    start:
    end:
  timeframes:
    - 1Day
    - 5Min
    - 1Min
  data_files:
    one_day:
    five_minute:
    one_minute:
  data_quality_status: pending | passed | blocked | insufficient
  labels:
    direction:
    current_range:
    support:
    resistance:
    fifty_61_zone:
    seventy_eight_level:
    target:
    break_behavior:
    retest_behavior:
    invalidation_candidate:
    room_to_target:
    higher_timeframe_obstacle:
  outcome: not_started | confirmed | contradicted | ambiguous | insufficient
  boundary:
    backtest_result: false
    profitability_claim: false
    execution_ready: false
```

## Replay labels

Use conservative behavior labels:

```text
approach
test
wick_break
close_break
hold
retest
reject
reclaim
failed_break
follow_through
target_hit
target_missed
target_already_hit
target_retired
obstacle_conflict
context_missing
range_stale
range_replaced
arbitrary_anchor
ignored_level
tighter_range_needed
same_candle_overfit
```

Do not collapse these labels into a generic `entry` label.

## Data quality gates

Before any replay outcome is used to change candidate maturity, confirm:

```text
timestamp parseable
timezone known
symbol known
timeframe known
source known
feed known
adjustment known
duplicates checked
missing bars checked
OHLC sanity checked
volume availability known
market-hours scope known
cross-timeframe alignment checked when needed
```

If data quality is not checked, use:

```yaml
replay_outcome:
  status: insufficient
  reason: data_quality_unverified
```

Do not upgrade candidates using unchecked data.

## Candidate maturity rules

Use conservative statuses:

```text
OBSERVATION
ANALYSIS CANDIDATE
WATCH CANDIDATE
CONFIRMATION CANDIDATE
TARGET-ACTIVATION CANDIDATE
NO-TRADE FILTER CANDIDATE
ENTRY-CANDIDATE GATE
LIFECYCLE CANDIDATE
HISTORICAL-REPLAY TEST CANDIDATE
REPLAY-CONTRADICTION CANDIDATE
DOWNGRADED CONCEPT
REJECTED CANDIDATE
```

Do not use `EXECUTION CANDIDATE` unless the task is explicitly about documenting that no candidate qualifies.

No candidate is execution-ready in this project.

## Required candidate split discipline

Split broad candidates before replay or Phase 6 refinement.

### 78 Decision Level

Split into:

- 78 Test Candidate
- 78 Wick Break Candidate
- 78 Close Break Candidate
- 78 Hold / Retest Candidate
- 78 Reclaim Candidate
- 78 Failure / Rejection Candidate
- 78 Target-Activation Candidate
- 78 Invalidation Candidate

### Entry Readiness Gate

Split into:

- Direction Gate
- Target Gate
- Room-to-Target Gate
- Invalidation Gate
- Timeframe Alignment Gate
- Support/Resistance Context Gate
- Confirmation Quality Gate
- No-Chase Gate
- Higher-Timeframe Obstacle Gate
- Target-Already-Hit Gate

### Last Green Candle Resistance

Split into:

- Bigger Last Green Candle Resistance
- Smaller Last Green Candle Resistance
- Last Green Candle Body-Level Candidate
- Last Green Candle Middle-Level Candidate
- Last Green Candle Resistance Ladder Candidate
- Last Green Candle Source-Candle Selection Candidate

### Same-Candle Range

Split into:

- Same-Candle Range Identification
- Same-Candle 50/61 Reaction Candidate
- Same-Candle 78 Decision Candidate
- Same-Candle Target Relationship Candidate
- Same-Candle No-Trade If No Break Candidate
- Same-Candle Overfit / Arbitrary Anchor Filter

### Role Flip

Split into:

- Prior Resistance Identified
- Resistance Close-Break
- Resistance Retest From Above
- Resistance Holds As Support
- Prior Support Identified
- Support Close-Break
- Support Retest From Below
- Support Rejects As Resistance
- Role Flip Target-Room Gate
- Failed Role Flip / Reclaim Filter

## Source artifact handling

For transcript and JPEG evidence:

- Prefer manifests and indexes.
- Do not bulk-copy raw JPEGs unless approved.
- Do not OCR images unless absolutely necessary.
- Do not treat a JPEG reference as visually confirmed until reviewed.
- Preserve exact lesson names and timestamps when known.
- Mark missing exact timestamps as `TBD`, not guessed.

For historical OHLCV:

- Prefer manifests pointing to the historical data repo or Google Drive.
- Do not load entire large datasets unless required.
- Use small windows for replay labeling.
- Use samples for schema tests.
- Keep generated replay labels separate from raw data.

## Suggested implementation style

Use clean, modular Python only when the task requires code.

Preferred libraries:

```text
pydantic
pandas
pyarrow
PyYAML
rich
pytest
```

Optional:

```text
pandas-market-calendars
plotly
streamlit
duckdb
ruff
mypy
```

Do not add dependencies without a clear reason.

Do not build UI first. Model the evidence and validation workflow first.

## CLI expectations

If a CLI is implemented later, prefer commands like:

```bash
python -m monster_strategy_lab.cli validate-docs
python -m monster_strategy_lab.cli build-index
python -m monster_strategy_lab.cli validate-replay-case --case knowledge_base/replay_cases/HR-001.yaml
python -m monster_strategy_lab.cli summarize-matrix
python -m monster_strategy_lab.cli check-evidence-links
```

Do not implement trading commands.

Do not implement commands named:

```text
trade
buy
sell
short
order
execute
submit-order
paper-trade
live-trade
```

unless a later separately approved project changes the boundary.

## Testing requirements

Normal tests must not require live API credentials.

Tests should focus on:

- config parsing
- phase document index validation
- evidence manifest schema
- replay case schema
- data-quality report schema
- validation matrix schema
- link/path sanity checks
- no-execution boundary checks
- candidate maturity transitions
- contradiction-case handling

Any tests using real market data must use small fixtures or approved sample files.

## Google Drive boundary

Google Drive may be used as a source of transcripts, snapshot maps, JPEG references, and historical data artifacts.

Do not upload large artifacts without Scott's approval.

Do not modify Google Drive files unless explicitly instructed.

Do not delete or reorganize Google Drive files.

If a Google Drive source is used, record:

- file name
- folder path
- export date or access date
- source type
- related phase/example/replay ID

## OpenClaw/Codex operating rules

Be conservative.

Prefer read-only inspection first.

Prefer small diffs.

Prefer explicit file paths.

Prefer manifests over copying raw data.

Do not perform broad repository scans unless the task requires it.

Do not repeatedly reread files already inspected in the same session.

Do not paste huge transcripts, CSVs, Parquet previews, logs, or generated reports into chat.

For large outputs, write files and summarize paths.

When uncertain, create a draft artifact and mark assumptions rather than silently deciding.

## Completion standard

For every change, report:

1. Files changed
2. Why the change was made
3. Source evidence used
4. Validation command or dry-run command
5. What was not validated
6. Rollback plan
7. Known risks or assumptions
8. Whether any boundary was approached

## Rollback standard

Before major refactors:

- show intended files
- avoid deleting source artifacts
- use git status
- keep changes easy to revert
- avoid formatting unrelated files
- avoid mass renames unless approved

Rollback plan should usually be:

```bash
git diff -- <files>
git checkout -- <files>
```

or, for new files:

```bash
rm <file>
```

## Preferred first tasks for this repo

1. Create `docs/INDEX.md`.
2. Move or copy phase documents into `docs/phases/`.
3. Create `data_refs/course_artifacts_manifest.yaml`.
4. Create `data_refs/historical_data_manifest.yaml`.
5. Create `knowledge_base/replay_cases/README.md`.
6. Create a replay-case YAML schema.
7. Create a validation-matrix schema.
8. Create a small `validate-docs` command.
9. Create Phase 6 planning docs only after Phase 5.1 is stable.
10. Do not build trading logic.
