# Strategy Lab Milestone: Replay to Paper Review

## 1. Executive summary

Strategy Lab can now:
- organize replay cases and manual review packets
- summarize replay evidence in a replay evidence matrix
- gate candidates through a paper-readiness review
- maintain a paper-review queue and plan files
- maintain a manual-only paper-watch journal

Strategy Lab cannot yet:
- issue trade signals
- claim strategy profitability
- submit Alpaca paper orders
- connect to broker APIs for execution
- run live trading
- rely on 1Min replay approval

Current safety boundary:
- all replay and paper-review activity remains documentation-first and manual-only
- `broker_action_allowed` remains `false`
- paper review means observation and journaling only

## 2. Current pipeline

Current pipeline stages:
1. historical data handoff
   - replay consumes approved historical data references
   - the local artifact index now points at the approved full 11-symbol 1Day + 5Min handoff
   - replay discovery is configured to use the full published artifact root and to keep 1Min blocked
2. replay discovery
   - replay cases are documented under `replay/cases/`
3. manual review
   - manual review packets and decision sheets live under `runs/replay/`
4. evidence matrix
   - consolidated evidence lives in `runs/replay/replay_evidence_matrix.md`
5. paper-readiness gate
   - readiness decisions live in `runs/paper_readiness/paper_readiness_matrix.md`
6. paper-review queue
   - queued candidate plan files live under `runs/paper_review/`
7. paper-watch journal
   - manual watch records live under `runs/paper_journal/`

## 3. Evidence coverage summary

Based on `runs/replay/replay_evidence_matrix.md`:

- confirmed bullish examples
  - count: 3
  - replay ids: HR-004, HR-005, HR-017
- confirmed bearish examples
  - count: 2
  - replay ids: HR-009, HR-019
- watch/no-trigger examples
  - count: 2
  - replay ids: HR-001, HR-002
- target-not-hit examples
  - count: 2
  - replay ids: HR-006, HR-007
- failed/reclaim examples
  - count: 2
  - replay ids: HR-008, HR-018
- ambiguous examples
  - count: 1
  - replay ids: HR-016
- insufficient-data examples
  - count: 7
  - replay ids: HR-003, HR-010, HR-011, HR-012, HR-013, HR-014, HR-015

Coverage gaps still called out by the matrix:
- bullish failed-breakout reclaim: missing
- bullish target-already-hit-before-confirmation: missing
- bearish support-touch no-trigger: missing
- bearish target-already-hit-before-confirmation: missing
- more ambiguous examples would still help

## 4. Paper-readiness summary

READY_FOR_PAPER_REVIEW candidates:
- PTC-004
- PTC-005
- PTC-009
- PTC-017
- PTC-019

Blocked candidates:
- PTC-001 / PTC-002
  - reason: no trigger
- PTC-003
  - reason: insufficient data
- PTC-006
  - reason: target not hit after confirmation
- PTC-008 / PTC-018
  - reason: failed reclaim
- PTC-016
  - reason: ambiguous outcome

`broker_action_allowed` status:
- all current readiness rows remain `false`
- readiness promotion does not allow broker action

## 5. Paper-review queue summary

Queued candidates:
- PTC-004
- PTC-005
- PTC-009
- PTC-017
- PTC-019

Plan files:
- `runs/paper_review/PTC-004-paper-review-plan.md`
- `runs/paper_review/PTC-005-paper-review-plan.md`
- `runs/paper_review/PTC-009-paper-review-plan.md`
- `runs/paper_review/PTC-017-paper-review-plan.md`
- `runs/paper_review/PTC-019-paper-review-plan.md`

Manual approval status:
- queue markdown/CSV is now populated for the current READY_FOR_PAPER_REVIEW candidates
- queued candidates remain at `pending_human_approval`

No broker action boundary:
- no broker action is allowed for queued candidates
- no Alpaca submission is allowed
- paper review here means manual observation only

## 6. Paper-watch journal summary

Journal files:
- `runs/paper_journal/paper_watch_journal.md`
- `runs/paper_journal/paper_watch_journal.csv`
- `runs/paper_journal/PTC-004-journal.md`
- `runs/paper_journal/PTC-005-journal.md`
- `runs/paper_journal/PTC-009-journal.md`
- `runs/paper_journal/PTC-017-journal.md`
- `runs/paper_journal/PTC-019-journal.md`

Current watch statuses:
- PTC-004: pending
- PTC-005: pending
- PTC-009: pending
- PTC-017: pending
- PTC-019: pending

Manual-only scope:
- the journal index is now populated for the queued candidates
- all journal rows are manual-only
- no orders, broker calls, or performance claims are permitted

## 7. Data limitations

Current limitations:
- old sample data problem
  - `data_refs/google_drive/` still contains deprecated sample CSVs across the broader symbol list
  - those samples must not be used for date-diversified replay discovery
- full 1Day + 5Min handoff
  - the active replay source of truth is now the approved full 11-symbol 1Day + 5Min handoff
  - local artifact references and replay discovery config now point at that published artifact root
- current symbol coverage
  - the active artifact index now includes SPY, QQQ, AAPL, MSFT, NVDA, AMZN, GOOGL, META, TSLA, AVGO, and IWM
- 1Min remains blocked
  - 1Min is still blocked for replay and paper review
- partial coverage warnings
  - upstream full-artifact validation previously identified one partial yearly 5Min partition for AVGO 2023 even though the aggregate symbol/timeframe handoff passed
  - that warning should stay visible until data refs and manifests are refreshed here

## 8. Safety boundaries

Explicit boundaries:
- no trade signal
- no profitability claim
- no Alpaca order submission
- no live trading
- no broker action
- paper-review means manual observation only

Additional guardrail:
- readiness, queueing, and journaling are evidence-management steps, not execution approval

## 9. Recommended next paths

### A. Expand replay evidence across the full 11-symbol universe
Use the broader full 1Day + 5Min handoff to diversify replay discovery beyond the current SPY/META-heavy local reference state.

### B. Build a local paper simulation runner that writes only to the journal
Create a report-only or journal-only runner that records hypothetical paper-watch outcomes without touching broker APIs or order flows.

### C. Begin designing an Alpaca paper adapter, but keep it disabled behind explicit manual approval
Design the interface and controls for a future paper adapter, but keep execution disabled and uncallable by default.

## 10. Recommendation

Recommended next path: **A. Expand replay evidence across the full 11-symbol universe.**

Why this is the best next step:
- current replay diversity is still thin even after the handoff reconciliation
- the repo now has the right 11-symbol source wired in, so broader replay expansion is unblocked
- more mixed-symbol replay evidence will strengthen candidate confidence more than adapter design will
- it improves Strategy Lab quality without crossing any broker or execution boundary
