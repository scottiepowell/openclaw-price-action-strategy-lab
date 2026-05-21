# EX-003 — 78 Target Activation

## Purpose

Show the 78 level as a trigger for target activation when context agrees and a target exists.

## Candidate family

- target_exists
- room_to_target_exists
- target_activated
- target_relationship_context

## What this example should show

- a target must exist before activation matters
- activation is not the same as entry
- activation can be blocked by immediate reclaim or no room

## Evidence status

- source evidence: `runs/month2_6_download/transcripts/MONTH 2/HOW TO USE THE FIB FOR CURRENT RANGES LESSON [a3ynlbskzm].txt`
- snapshot refs: `a3ynlbskzm:ts-000035`, `a3ynlbskzm:ts-000091`, `a3ynlbskzm:ts-000098`
- replay link: `tests/fixtures/replay_cases/verified_sample.md`

## Labels to capture later

- target_exists
- target_activated
- blocked_target
- target_already_hit
- room_to_target

## Boundary

- confirmation label only
- not an order concept
- not a trade instruction
