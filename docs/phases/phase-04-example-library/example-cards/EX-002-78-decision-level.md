# EX-002 — 78 Decision Level

## Purpose

Show the 78 level as a decision/confirmation boundary, not an entry by itself.

## Candidate family

- 78_test_candidate
- 78_wick_break_candidate
- 78_close_break_candidate
- 78_hold_retest_candidate
- 78_reclaim_candidate
- 78_failure_rejection_candidate
- 78_target_activation_candidate
- 78_invalidation_candidate

## What this example should show

- wick-only interaction is weaker than a close/hold sequence
- 78 break is a confirmation candidate only
- reclaim/failure behavior must stay separate from break behavior

## Evidence status

- source evidence: `runs/month2_6_download/transcripts/MONTH 2/HOW TO USE THE FIB FOR CURRENT RANGES LESSON [a3ynlbskzm].txt`
- snapshot refs: `a3ynlbskzm:ts-000156`, `a3ynlbskzm:ts-000170`, `q0fxq1o9gs:ts-000406`
- replay link: `tests/fixtures/replay_cases/verified_sample.md`

## Labels to capture later

- wick_break
- close_break
- hold
- retest
- reclaim
- failed_break

## Boundary

- no direct entry language
- no profitability claim
- no execution readiness
