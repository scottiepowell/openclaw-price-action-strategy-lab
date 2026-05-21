# Example to Snapshot Crosswalk

Starter mappings for Phase 4 example cards.

## EX-001 — Current Range

- Source transcript: `runs/month2_6_download/transcripts/MONTH 2/WHAT ARE CURRENT RANGES LESSON [awsgn46dne].txt`
- Snapshot refs:
  - `awsgn46dne:ts-000045` — "So what is current ranges, first of all?"
  - `awsgn46dne:ts-000270` — "what the current ranges are,"
  - `awsgn46dne:ts-000660` — "current range are we in?"
- Replay seed: `replay/cases/HR-001.md`

## EX-002 — 78 Decision Level

- Source transcript: `runs/month2_6_download/transcripts/MONTH 2/HOW TO USE THE FIB FOR CURRENT RANGES LESSON [a3ynlbskzm].txt`
- Snapshot refs:
  - `a3ynlbskzm:ts-000156` — "to the reversal level, which is the 786 level."
  - `a3ynlbskzm:ts-000170` — "and then the reversal level at the 78."
  - `q0fxq1o9gs:ts-000406` — "So that's the 78 level range of this high to this low"
- Replay seed: `tests/fixtures/replay_cases/verified_sample.md`

## EX-003 — 78 Target Activation

- Source transcript: `runs/month2_6_download/transcripts/MONTH 2/HOW TO USE THE FIB FOR CURRENT RANGES LESSON [a3ynlbskzm].txt`
- Snapshot refs:
  - `a3ynlbskzm:ts-000035` — target around 348 / 347 example
  - `a3ynlbskzm:ts-000091` — "that's when we're close to targets."
  - `a3ynlbskzm:ts-000098` — "Now this level on the fib is like your key reversal area"
- Replay seed: `tests/fixtures/replay_cases/verified_sample.md`

## EX-004 — Room to Target

- Source transcript: `runs/month2_6_download/transcripts/MONTH 2/HOW TO USE THE FIB FOR CURRENT RANGES LESSON [a3ynlbskzm].txt`
- Snapshot refs:
  - `a3ynlbskzm:ts-000035` — target example with only a small gap
  - `a3ynlbskzm:ts-000147` — "If the target is close."
  - `a3ynlbskzm:ts-000154` — "If it doesn't break there"
- Replay seed: `tests/fixtures/replay_cases/verified_sample.md`

## EX-005 — No-Trade Filters

- Source transcript: `runs/month2_6_download/transcripts/MONTH 2/MONTHLY CURRENT RANGE LESSON [q0fxq1o9gs].txt`
- Snapshot refs:
  - `q0fxq1o9gs:ts-000448` — "This is the 78 level."
  - `q0fxq1o9gs:ts-000658` — "we have to stop looking for selling pressure and downplays"
  - `a3ynlbskzm:ts-000109` — "If we do not leave this price fast, ... price is turning bearish."
- Replay seed: `replay/contradiction_cases/HC-001.md`

## Notes

- Snapshot refs are lightweight pointers, not visual confirmation.
- Use replay cases to test whether each example survives historical windows.
- Keep mappings conservative until the evidence is fully linked.
- These mappings are intentionally starter-level and should be refined once replay labels are added.
