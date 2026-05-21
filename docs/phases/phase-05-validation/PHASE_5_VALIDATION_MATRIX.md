# Phase 5 Validation Matrix

## Purpose

Evaluate Phase 3 rule candidates and Phase 4 examples against evidence strength, contradiction risk, and readiness for conservative Phase 6 refinement.

## Repo alignment

- rule candidates: `knowledge_base/rule_candidates/`
- example library: `docs/phases/phase-04-example-library/`
- replay cases: `replay/cases/`
- contradiction cases: `replay/contradiction_cases/`
- validation notes: `docs/phases/phase-05-validation/validation-notes/`

## Validation goals

Phase 5 answers:
- which candidates are supported
- which candidates are weak
- which candidates need splitting
- which candidates need more examples
- which candidates need contradiction search
- which candidates are blocked by missing evidence

## Core statuses

- OBSERVATION
- ANALYSIS CANDIDATE
- WATCH CANDIDATE
- CONFIRMATION CANDIDATE
- TARGET-ACTIVATION CANDIDATE
- NO-TRADE FILTER CANDIDATE
- REPLAY-CONTRADICTION CANDIDATE
- DOWNGRADED CONCEPT
- REJECTED CANDIDATE

## Validation dimensions

- glossary support
- concept-model support
- transcript support
- JPEG / snapshot support
- replay support
- contradiction support
- target clarity
- room-to-target clarity
- invalidation clarity
- timeframe alignment
- no-trade filter strength

## Starter matrix

| Candidate family | Expected focus | Validation output |
|---|---|---|
| Direction | bias and context | support / weak / split |
| Current range | active map | support / refine |
| Support / resistance | level behavior | support / contradiction |
| 78 decision level | confirmation / invalidation | split / refine / reject |
| Target activation | target relationship | support / block |
| Room to target | entry filter | keep / downgrade |
| No-trade filters | safety gate | keep / strengthen |

## Boundary

This is not execution guidance.
This is not a backtest.
This is not paper-trade approval.
