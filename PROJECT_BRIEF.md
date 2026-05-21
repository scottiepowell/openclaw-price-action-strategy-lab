# PROJECT_BRIEF.md — Monster Academy Strategy Lab

## Project name

`openclaw-monster-academy-strategy-lab`

Recommended repo root:

```text
/home/scott/projects/openclaw-monster-academy-strategy-lab
```

## Mission

Monster Academy Strategy Lab is the evidence, replay, validation, and paper-validation workspace for turning the Monster Academy course material into a documented, testable, and conservative strategy model.

The project is not a live trading bot. It is not an Alpaca execution system. Its job is to organize course-derived strategy artifacts, connect them to transcript/JPEG evidence, validate them against historical OHLCV replay, refine surviving rule candidates, and later test only mature candidates in an Alpaca paper account.

## Relationship to adjacent repositories

This project should remain separate from the capture and data-acquisition projects.

```text
openclaw-monster-academy-archiver
  -> captures Wistia/course material, transcripts, snapshots, snapshot maps, and raw evidence

openclaw-historical-market-data-extraction
  -> acquires, validates, normalizes, packages, and optionally uploads historical OHLCV data

openclaw-monster-academy-strategy-lab
  -> organizes strategy documents, evidence links, replay labels, validation matrices, Phase 6 rule refinement, and paper-account validation
```

The Strategy Lab may reference artifacts from the archiver and historical data extraction repos, but it should not become the raw data warehouse or course-capture tool.

## Core boundary

This project is staged validation work.

It may eventually support Alpaca paper-account validation after candidates pass conservative readiness gates.

It must not start by implementing live trading, paper orders, or automated execution.

## Strategy principle

Preserve the central project principle:

```text
A level break is not an entry.

A level break is a candidate confirmation.

It becomes an entry candidate only when:
  direction agrees,
  target exists,
  room to target exists,
  support/resistance context agrees,
  timeframe context agrees,
  invalidation is defined,
  and no-trade filters are clear.
```

Historical replay and paper trading do not change that principle.

## Non-goals

Do not build live trading logic.

Do not connect to a live Alpaca account.

Do not submit live orders.

Do not treat Phase 3 or Phase 3.1 candidates as executable rules.

Do not convert a 78 break, support break, resistance break, candle-derived level, or target activation into a buy/sell signal by itself.

Do not claim profitability, win rate, edge, expectancy, or production readiness.

Do not optimize thresholds for profitability before the strategy evidence model is stable.

Do not let historical replay or paper validation bypass the documentation phases.

## Project stages

### Stage 1 — Documentation and evidence organization

Organize all phase documents, rule candidates, examples, evidence crosswalks, source manifests, and Google Drive references.

Outputs:

- canonical phase documents
- source manifests
- example-to-rule crosswalks
- transcript/JPEG reference indexes
- historical data artifact references

No Alpaca trading.

### Stage 2 — Historical replay labeling

Use historical 1-day, 5-minute, and 1-minute OHLCV data to label replay windows.

Replay labels may include:

- current range
- foundation range
- tighter range
- same-candle range
- support
- resistance
- 50/61 zone
- 78 level
- target
- target hit
- target missed
- wick break
- close break
- hold
- retest
- reclaim
- rejection
- invalidation candidate
- higher-timeframe obstacle
- target already hit

No Alpaca trading.

### Stage 3 — Phase 6 conservative rule refinement

Convert surviving candidates into refined, conservative paper-trade candidate definitions.

This stage defines:

- required context
- target relationship
- room-to-target gate
- invalidation requirements
- no-trade filters
- replay evidence requirements
- contradiction evidence requirements

No automatic order placement.

### Stage 4 — Dry-run paper validation

Run the system in observation mode.

Allowed dry-run output:

```text
Candidate observed.
Target exists.
Room exists.
No-trade filters passed.
Would have submitted paper order.
```

No orders are submitted in this stage.

### Stage 5 — Alpaca paper-account validation

Only after a candidate passes Phase 6 readiness gates, the system may submit paper-only orders to an Alpaca paper account.

The goal is not profit optimization. The goal is to validate whether the candidate definition behaves as expected.

Paper validation should answer:

- Did the candidate appear under the expected context?
- Was the target known before the paper entry?
- Was there enough room to target?
- Did invalidation work?
- Did no-trade filters prevent bad setups?
- Was the entry late, early, or structurally invalid?
- Did higher-timeframe context help or hurt?
- Should the candidate be kept, revised, split, downgraded, or rejected?

### Stage 6 — Paper results review and candidate revision

Use paper validation evidence to update candidate maturity.

Possible outcomes:

- keep
- keep but refine
- split
- downgrade
- reject
- needs more evidence
- needs more contradiction cases

No candidate becomes live-ready automatically.

## Recommended directory model

```text
.
├── AGENTS.md
├── PROJECT_BRIEF.md
├── README.md
├── TODO.md
├── requirements.txt
├── .env.example
├── .gitignore
├── docs/
├── knowledge_base/
├── evidence/
├── data_refs/
├── replay/
├── paper_validation/
├── configs/
├── src/
├── tests/
├── runs/
├── artifacts/
└── logs/
```

## Phase document location

Store canonical phase documents under:

```text
docs/phases/
```

Recommended phase folders:

```text
docs/phases/phase-01-glossary/
docs/phases/phase-02-concept-model/
docs/phases/phase-03-rule-candidates/
docs/phases/phase-04-example-library/
docs/phases/phase-05-validation/
docs/phases/phase-06-rule-refinement/
docs/phases/phase-07-paper-validation/
docs/phases/phase-08-live-readiness-review/
```

Keep machine-readable indexes and extracted structured records in:

```text
knowledge_base/
```

## Google Drive artifact policy

Raw Google Drive artifacts should generally remain in Google Drive or the archiver repo.

Strategy Lab should store:

- Drive references
- source manifests
- transcript indexes
- snapshot indexes
- JPEG reference indexes
- selected small excerpts
- evidence crosswalks
- replay mappings

Do not copy large transcript dumps, snapshot directories, JPEG libraries, or market-data files into this repo unless explicitly needed for a test fixture or canonical small sample.

## Historical data policy

The historical data extraction repo should own the large OHLCV artifacts.

Strategy Lab should store references and derived labels:

```text
data_refs/historical_market_data/
replay/labels/
replay/cases/
replay/reports/
```

Historical data files may inform replay cases only after data quality checks pass.

## Alpaca paper-account policy

Alpaca paper-account work belongs under:

```text
paper_validation/
```

Use paper validation only after Phase 6 candidate readiness gates are satisfied.

Paper validation must remain separate from live trading.

Required paper-validation safety boundaries:

- paper account only
- no live credentials
- explicit config flag for paper mode
- no default order submission
- dry-run mode first
- paper trade journal required
- abort rules required
- no candidate promoted without review

## Evidence maturity model

Evidence should mature through this sequence:

```text
Course concept
  -> transcript/JPEG example
  -> Phase 4 example
  -> Phase 5 evidence score
  -> historical replay label
  -> contradiction search
  -> Phase 6 conservative candidate
  -> dry-run observation
  -> paper validation
  -> paper result review
```

Do not skip from course concept directly to paper trade.

## Success criteria

This project is successful when it produces a well-organized, auditable workflow that can answer:

- What does the course appear to teach?
- Which examples support each concept?
- Which rule candidates are supported, contradicted, weak, or unclear?
- Which candidates survive historical replay?
- Which candidates fail contradiction testing?
- Which candidates are ready for conservative Phase 6 refinement?
- Which candidates are safe to test in a paper account?
- What did paper validation reveal?

The project is not successful merely because it submits paper trades.

## Current expected source documents

The repo should be initialized with the existing phase artifacts:

- Phase 1 Glossary
- Phase 2 Strategy Concept Model
- Phase 2.1 Historical Replay Concept Model Update
- Phase 3 Rule Candidate Extraction
- Phase 3.1 Historical Replay Rule Candidate Update
- Phase 4 Example Library
- Phase 4.1 Historical Replay Example Library Update
- Phase 5 Validation Matrix
- Phase 5.1 Historical Replay Validation Matrix Update
- Phase 5B Historical Validation Plan

Future documents should include:

- Phase 6 Rule Refinement
- Phase 6 Paper Trade Readiness Gates
- Phase 7 Alpaca Paper Validation Plan
- Phase 7 Paper Validation Results
- Phase 8 Live Readiness Review, if ever considered

