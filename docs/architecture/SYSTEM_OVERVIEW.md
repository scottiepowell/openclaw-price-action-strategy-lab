# System Overview

## Purpose

This repository is the documentation and validation layer for the Monster Academy strategy work.

It turns raw course evidence into:

- structured strategy notes
- replay labels and contradiction cases
- conservative candidate definitions
- paper-validation readiness gates
- paper-trade journals and results

## Scope

- Strategy documentation
- Evidence organization
- Historical replay labeling
- Conservative candidate refinement
- Paper-validation preparation

## Boundaries

- No live trading
- No execution logic
- No raw evidence warehouse

## High-level flow

1. Evidence is captured elsewhere and referenced here.
2. Example and source manifests are linked into the knowledge base.
3. Replay cases are labeled conservatively against historical market data.
4. Contradictions are logged when a candidate fails a gate.
5. Surviving candidates are refined into paper-trade candidates.
6. Paper-only results are journaled and reviewed.

## Design principles

- A level break is not an entry.
- Labels should describe what is visible, not what is hoped for.
- No document here should imply live execution readiness.
- Every candidate should retain evidence traceability.

## Primary artifacts

- `knowledge_base/` for canonical concepts and candidates
- `evidence/` for manifests and crosswalks
- `replay/` for cases and contradiction records
- `paper_validation/` for readiness gates and journals
