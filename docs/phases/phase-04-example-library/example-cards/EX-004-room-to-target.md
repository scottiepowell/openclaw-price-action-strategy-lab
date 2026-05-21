# EX-004 — Room to Target

## Purpose

Show when there is enough room for the idea to remain valid, and when the setup should be filtered out.

## Candidate family

- room_to_target_exists
- target_already_hit
- higher_timeframe_obstacle
- no_chase / consumed_room filters

## What this example should show

- room to target is a gate, not a signal
- nearby obstacles or already-hit targets block the setup
- this can stop a candidate before deeper confirmation logic

## Evidence status

- source evidence: `runs/month2_6_download/transcripts/MONTH 2/HOW TO USE THE FIB FOR CURRENT RANGES LESSON [a3ynlbskzm].txt`
- snapshot refs: `a3ynlbskzm:ts-000035`, `a3ynlbskzm:ts-000147`, `a3ynlbskzm:ts-000154`
- replay link: `tests/fixtures/replay_cases/verified_sample.md`

## Labels to capture later

- room_to_target
- target_already_hit
- higher_timeframe_obstacle
- blocked_target
- context_missing

## Boundary

- conservative filter only
- no profitability claim
- no execution readiness
