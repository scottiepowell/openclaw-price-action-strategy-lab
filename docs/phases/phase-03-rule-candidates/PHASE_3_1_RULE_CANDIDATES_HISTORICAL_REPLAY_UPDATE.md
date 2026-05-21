# PHASE_3_1_RULE_CANDIDATES_HISTORICAL_REPLAY_UPDATE.md

Status: Draft v0.1 — First Iteration / Historical Replay Update  
Created: 2026-05-14  
Source basis: Phase 1 Glossary v1.0, Phase 2 Strategy Concept Model v1.0, Phase 2.1 Concept Model Historical Replay Update v1.1, Phase 3 Rule Candidate Extraction v1.0, Phase 4 Example Library v1.0, Phase 5 Validation Matrix v1.0, Phase 5B Historical Validation Plan v1.0, and the Phase 3.1 prompt supplied in `Pasted text.txt`.

> Working note: This file is intentionally built as a first long-form iteration. It establishes the complete Phase 3.1 structure, conservative boundary language, candidate splits, replay matrices, contradiction plan, and Phase 6 handoff gates. Later iterations should deepen individual candidate cards with exact transcript/JPEG anchors and replay-case IDs after historical windows are labeled.


## 0. Purpose and Boundary

Phase 3.1 updates the original Phase 3 rule candidates using the replay-aware concept model from Phase 2.1 and the historical validation plan from Phase 5B.

Repo alignment:

- replay cases: `replay/cases/`
- contradiction cases: `replay/contradiction_cases/`
- replay labels: `replay/labels/`
- candidate indexes: `knowledge_base/rule_candidates/`
- historical data refs: `data_refs/historical_market_data/`

The original Phase 3 document extracted first-pass rule candidates from the glossary and concept model. Phase 3.1 does not replace that work. It revises, splits, downgrades, and extends those candidates so they can be evaluated against historical OHLCV replay evidence before Phase 6 rule refinement.

This is discovery and validation-preparation work only.

Boundary statements:

- This is not a final rulebook.
- This is not financial advice.
- This is not code.
- This is not a backtest.
- This is not Alpaca logic.
- This does not create order logic.
- This does not create executable strategy conditions.
- This does not authorize automated execution.
- This does not claim profitability, edge, win rate, expectancy, or risk/reward performance.
- This does not mark any candidate paper-trading-ready or live-trading-ready.
- This document updates rule candidates only.

Relationship to prior phases:

```text
Phase 1 defined vocabulary.
Phase 2 modeled concept relationships.
Phase 2.1 added historical replay concepts, replay labels, data-quality gates, and evidence maturity.
Phase 3 extracted first-pass rule candidates.
Phase 4 connected examples to rule candidates.
Phase 5 scored evidence strength and recommended keep/refine/split/downgrade/reject decisions.
Phase 5B planned historical validation and contradiction replay.
Phase 3.1 updates the rule candidates so they are ready for historical replay validation and later Phase 6 refinement.
```

Phase 3.1 must preserve the same central principle used in Phase 2 and Phase 3:

> A level break is not an entry. A level break is a candidate confirmation. It becomes an entry candidate only when direction, target, room to target, support/resistance context, timeframe context, and invalidation agree.

Historical replay does not change that principle. A historical replay confirmation is not a trade signal. A historical replay contradiction is not automatic rejection. A historical replay result only affects evidence maturity, candidate wording, split/refine decisions, no-trade filters, and Phase 6 readiness.


## 1. Updated Rule Candidate Philosophy

```text
No single level equals an entry.

A level interaction becomes meaningful only when it fits inside:
direction
  -> timeframe context
  -> current range
  -> support/resistance
  -> target
  -> confirmation
  -> room to target
  -> invalidation
  -> lifecycle state
```

Phase 3.1 adds a historical replay principle:

```text
No historical replay outcome equals an entry.

A replay outcome can:
  -> strengthen a candidate
  -> contradict a candidate
  -> make a candidate ambiguous
  -> show insufficient evidence
  -> force a split
  -> force a downgrade
  -> add a no-trade condition

A replay outcome cannot:
  -> create a final rule
  -> create a trading signal
  -> create order logic
  -> prove profitability
  -> authorize paper or live trading
```

A replay-confirmed relationship means only that a labeled concept relationship appeared in a historical bar window. It does not mean the relationship is profitable, repeatable across markets, suitable for automation, or ready for execution.

A replay-contradicted relationship is also useful. It may show that a candidate should be split, narrowed, downgraded, or converted into a no-trade filter. Contradiction replay is therefore not a failure of the project; it is part of the evidence-maturity process.


## 2. Updated Rule Maturity Labels

Original Phase 3 labels:

| Original Phase 3 Label |
|---|
| OBSERVATION |
| ANALYSIS RULE |
| WATCH RULE |
| ALERT RULE |
| CONFIRMATION CANDIDATE |
| ENTRY CANDIDATE |
| NO-TRADE RULE |
| LIFECYCLE RULE |
| EXECUTION CANDIDATE |

Phase 3.1 replaces or narrows those labels as follows:

| Phase 3.1 Label | Meaning |
|---|---|
| OBSERVATION | Concept appears in course material but is not decision-ready. |
| ANALYSIS CANDIDATE | Helps classify chart state only. |
| WATCH CANDIDATE | Identifies a level, zone, or condition worth monitoring. |
| CONFIRMATION CANDIDATE | Identifies evidence that a setup may be developing. |
| TARGET-ACTIVATION CANDIDATE | Suggests a target may become active if context agrees. |
| NO-TRADE FILTER CANDIDATE | Blocks or downgrades a setup. |
| ENTRY-CANDIDATE GATE | One required gate in an entry-readiness chain. |
| LIFECYCLE CANDIDATE | Controls state transitions such as watch, confirm, retire, complete, or invalidate. |
| HISTORICAL-REPLAY TEST CANDIDATE | Candidate is ready to be tested with labeled historical bars. |
| REPLAY-CONTRADICTION CANDIDATE | Candidate specifically needs failure-case testing. |
| DOWNGRADED CONCEPT | Keep as vocabulary/concept only until more evidence exists. |
| REJECTED CANDIDATE | Remove from rule-candidate set unless new evidence appears. |

Do not use `EXECUTION CANDIDATE` in Phase 3.1 except to state that no candidate qualifies. No Phase 3.1 candidate is execution-ready.


## 3. Updated Rule Candidate Template

Every Phase 3.1 candidate should eventually use this template. In this first iteration, the detailed candidate cards use a compact version of the template where a full card would be repetitive.

```markdown
## Rule Candidate: <name>

### Phase 3.1 Status
<OBSERVATION | ANALYSIS CANDIDATE | WATCH CANDIDATE | CONFIRMATION CANDIDATE | TARGET-ACTIVATION CANDIDATE | NO-TRADE FILTER CANDIDATE | ENTRY-CANDIDATE GATE | LIFECYCLE CANDIDATE | HISTORICAL-REPLAY TEST CANDIDATE | REPLAY-CONTRADICTION CANDIDATE | DOWNGRADED CONCEPT | REJECTED CANDIDATE>

### Prior Phase 3 Status
<original status>

### Phase 5 Decision
<Keep | Keep but refine | Split | Merge | Downgrade | Reject | Needs more examples>

### Source Concepts
- <Phase 1 / Phase 1.1 / Phase 2 / Phase 2.1 concepts>

### Source Evidence
- Transcript evidence:
- Snapshot-map evidence:
- JPEG evidence:
- Phase 4 example IDs:
- Phase 5 matrix notes:
- Phase 5B replay requirement:

### Purpose
What this candidate is trying to detect or classify.

### Required Context
What must already be labeled before this candidate matters.

### Historical Replay Data Needed
- 1-day:
- 5-minute:
- 1-minute:
- Symbols:
- Example-matched replay needed:
- Similar-structure replay needed:
- Contradiction replay needed:

### Required Replay Labels
Only include labels relevant to that candidate.

### Candidate Trigger
What causes this candidate to become relevant.

### Confirmation Evidence
What strengthens the candidate.

### Contradiction Evidence
What weakens, narrows, or contradicts the candidate.

### Invalidation / No-Trade Conditions
What cancels or blocks the candidate.

### Target Relationship
What target this candidate supports, activates, blocks, retires, or invalidates.

### Entry Relationship
State one of: no entry, watch only, confirmation only, target activation only, no-trade filter only, entry-candidate gate only, lifecycle state only.

### Replay Outcome Handling
Explain how confirmed, contradicted, ambiguous, or insufficient replay results should affect this candidate.

### Phase 6 Handoff
Explain what must be true before Phase 6 can refine this candidate.

### Boundary
State what this candidate does not prove and what it must not be used for.
```


## 4. Candidate Split Requirements From Phase 5 and Phase 2.1

Phase 5 showed that several Phase 3 candidates are too broad for replay validation. Phase 2.1 adds replay behavior labels that make these splits necessary.

### 4.1 78 Decision Level Split

Do not keep one broad `78 Decision Level` candidate. Split it into:

- 78 Test Candidate
- 78 Wick Break Candidate
- 78 Close Break Candidate
- 78 Hold / Retest Candidate
- 78 Reclaim Candidate
- 78 Failure / Rejection Candidate
- 78 Target-Activation Candidate
- 78 Invalidation Candidate

### 4.2 Entry Readiness Gate Split

Do not keep one broad `Entry Readiness Gate`. Split it into:

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

### 4.3 Last Green Candle Resistance Split

Split `Last Green Candle Resistance` into:

- Bigger Last Green Candle Resistance
- Smaller Last Green Candle Resistance
- Last Green Candle Body-Level Candidate
- Last Green Candle Middle-Level Candidate
- Last Green Candle Resistance Ladder Candidate
- Last Green Candle Source-Candle Selection Candidate

### 4.4 Same-Candle Range Refinement Split

Split `Same-Candle Range Refinement` into:

- Same-Candle Range Identification
- Same-Candle 50/61 Reaction Candidate
- Same-Candle 78 Decision Candidate
- Same-Candle Target Relationship Candidate
- Same-Candle No-Trade If No Break Candidate
- Same-Candle Overfit / Arbitrary Anchor Filter

### 4.5 Role Flip Split

Split role-flip candidates into:

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


## 5. Foundation Candidate Updates

### Rule Candidate: Direction State Identification

**Phase 3.1 Status:** ANALYSIS CANDIDATE  
**Prior Phase 3 Status:** ANALYSIS RULE  
**Phase 5 Decision:** Keep but refine

**Source concepts:** Direction, bullish, bearish, sideways, higher high, higher low, lower high, lower low, swing high, swing low, significant high break, significant low break, close break, wick test only, failed break.

**Purpose:** Classify market structure before any target, confirmation, or entry-adjacent candidate is evaluated.

**Required context:** Timeframe selected, meaningful swing points labeled, recent structure compared to prior structure, and higher-timeframe context noted.

**Historical replay data needed:**

- 1-day: daily direction shifts, significant highs/lows, target context.
- 5-minute: intraday bridge and whipsaw/follow-through windows.
- 1-minute: close-vs-wick behavior around structure levels.
- Symbols: SPY, QQQ, NVDA, TSLA, IWM, and open contradiction searches across available symbols.

**Required replay labels:** higher high, higher low, lower high, lower low, significant high break, significant low break, wick test only, close break, follow-through, failed break, choppy/sideways window, higher-timeframe conflict.

**Candidate trigger:** A new high, new low, break of significant swing point, higher low, lower high, or failed break occurs.

**Confirmation evidence:** Direction changes after a meaningful structural close break and shows follow-through, or holds new structure without immediate reclaim.

**Contradiction evidence:** Wick-only breaks fail, close breaks immediately reclaim, swings are not visually significant, or higher timeframe context contradicts the lower-timeframe direction.

**Invalidation / no-trade conditions:** Direction is unclear, choppy, sideways, or conflicting across timeframes.

**Target relationship:** Direction controls whether upside or downside targets are preferred, but it does not activate a target by itself.

**Entry relationship:** no entry.

**Replay outcome handling:** Confirmed replay strengthens only the direction-labeling language. Contradicted replay should refine wick/close/follow-through criteria or add choppy no-trade classifications. Ambiguous replay remains backlog. Insufficient replay causes no maturity change.

**Phase 6 handoff:** Phase 6 can refine this candidate only after swing significance, wick-vs-close behavior, failed-break handling, and timeframe conflict labels are defined.

**Boundary:** Direction is context only. It must not be used as an entry, alert, order trigger, or profitability claim.

---

### Rule Candidate: Timeframe Alignment Filter

**Phase 3.1 Status:** NO-TRADE FILTER CANDIDATE  
**Prior Phase 3 Status:** ANALYSIS RULE / NO-TRADE FILTER  
**Phase 5 Decision:** Keep but refine

**Purpose:** Prevent a lower-timeframe setup from being upgraded when it conflicts with higher-timeframe direction, target, support/resistance, or obstacle context.

**Replay labels:** daily context, five-minute bridge context, one-minute execution context, aligned, mixed, conflicting, higher-timeframe obstacle, target already hit.

**Historical replay should test:**

- Daily setup with one-minute confirmation.
- One-minute breaks that fail because daily context conflicts.
- Lower-timeframe setups that run directly into higher-timeframe obstacles.

**Entry relationship:** no-trade filter only. Lower-timeframe confirmation may remain watch/confirmation if higher context is missing or conflicting.

**Phase 6 handoff:** Requires a stable alignment taxonomy: aligned, mixed, conflicting, obstacle-conflict, and context-missing.

---

### Rule Candidate: Current Range Defines Active Map

**Phase 3.1 Status:** ANALYSIS CANDIDATE  
**Prior Phase 3 Status:** ANALYSIS RULE  
**Phase 5 Decision:** Keep but refine

**Purpose:** Require an active range map before support/resistance, 50/61, 78, target, invalidation, or target-room candidates are evaluated.

**Replay labels:** foundation range, current range, tighter range, same-candle range, stale range, replaced range, arbitrary anchor, ignored levels, semantic 50/61, 78, 1.0, zero, support, resistance, target.

**Historical replay should test:**

- Whether mapped ranges explain reactions.
- Whether current range changes after new highs/lows.
- Whether tighter ranges explain behavior better than broad ranges.
- When range selection becomes too subjective.

**Entry relationship:** no entry.

**Phase 6 handoff:** Requires range-anchor source labels, confidence labels, staleness labels, and range replacement conditions.


## 6. Range Selection and Refinement Candidate Updates

### Rule Candidate: Foundation Range First

**Phase 3.1 Status:** ANALYSIS CANDIDATE  
**Prior Phase 3 Status:** ANALYSIS RULE  
**Phase 5 Decision:** Keep but refine

Foundation Range First remains analysis-only. It starts the chart map with the clearest larger swing-to-swing structure before using tighter or same-candle refinement.

**Replay data needed:** 1-day bars first, with 5-minute bridge only when intraday structure is being compared to the daily/foundation range.

**Required replay labels:** foundation range, bigger range, swing high, swing low, broad support/resistance, target, stale/replaced state.

**Confirmation evidence:** Foundation range explains broad support, resistance, target, or obstacle behavior.

**Contradiction evidence:** Foundation range is stale, too broad for current behavior, or ignored while a tighter range explains reactions better.

**Phase 6 handoff:** The candidate can move forward as an analysis framework only after the replay process can label when the foundation range should be retained, refined, or retired.

---

### Rule Candidate: Tighter Range When Foundation Range Is Too Broad

**Phase 3.1 Status:** HISTORICAL-REPLAY TEST CANDIDATE  
**Prior Phase 3 Status:** REFINEMENT RULE  
**Phase 5 Decision:** Keep but refine

Tighter Range remains refinement-only unless replay evidence shows a clear relationship to target, invalidation, and higher-timeframe context.

**Replay data needed:** 5-minute and 1-minute bars with 1-day parent context.

**Required replay labels:** parent/foundation range, child/tighter range, local high/low, last meaningful candle, local 78, local target, target room, invalidation candidate, parent conflict.

**Confirmation evidence:** Tighter range creates clearer support/resistance, 78 behavior, target relationship, or invalidation than the broad range.

**Contradiction evidence:** Tighter range is arbitrary, selected after the move, contradicts the parent range, or fails to improve target-room/invalidation clarity.

**Phase 6 handoff:** Requires parent-child range labels and contradiction examples for arbitrary anchor selection.

---

### Rule Candidate: Same-Candle Range Refinement Family

Same-Candle Range is split and treated as lower-confidence until replay shows it explains behavior without overfitting.

| Split Candidate | Phase 3.1 Status | Entry Relationship | Replay Requirement |
|---|---|---|---|
| Same-Candle Range Identification | ANALYSIS CANDIDATE | no entry | Candle high/low defensibly defines immediate structure. |
| Same-Candle 50/61 Reaction Candidate | WATCH CANDIDATE | watch only | 50/61 reaction appears inside same-candle range. |
| Same-Candle 78 Decision Candidate | CONFIRMATION CANDIDATE | confirmation only | 78 behavior is labeled as test, wick break, close break, hold, or reclaim. |
| Same-Candle Target Relationship Candidate | TARGET-ACTIVATION CANDIDATE | target activation only | Target known before confirmation and not already hit. |
| Same-Candle No-Trade If No Break Candidate | NO-TRADE FILTER CANDIDATE | no-trade filter only | No close/hold beyond level keeps target inactive. |
| Same-Candle Overfit / Arbitrary Anchor Filter | REPLAY-CONTRADICTION CANDIDATE | no-trade filter only | Same-candle levels ignored or contradicted by larger structure. |

**Phase 6 handoff:** Same-candle candidates require example-matched replay, similar-structure replay, and contradiction replay before any refinement beyond watch/confirmation language.


## 7. Level Reaction Candidate Updates

### Rule Candidate: 50/61 Sweet Spot Reaction

**Phase 3.1 Status:** WATCH CANDIDATE  
**Prior Phase 3 Status:** WATCH RULE  
**Phase 5 Decision:** Keep but refine

The 50/61 area remains a watch zone only. It should not become an entry, alert-to-enter, or execution condition.

**Replay should search for:** support reaction, resistance reaction, price slicing through, no reaction, reaction with no target room, and reaction blocked by higher-timeframe obstacle.

**Required replay labels:** active range, range orientation, 50/61 zone, support/reaction behavior, resistance/rejection behavior, slice-through, target room, obstacle.

**Replay outcome handling:** Confirmed replay keeps this as a watch candidate. Contradicted replay does not reject the concept but should narrow when the zone matters. Ambiguous or insufficient replay blocks promotion.

---

### Rule Candidate Family: 78 Decision Level Split

The broad `78 Decision Level` candidate is retired as a single candidate. It becomes a family of behavior-specific candidates.

| 78 Split Candidate | Phase 3.1 Status | Replay Behavior | Target Relationship | No-Entry Boundary |
|---|---|---|---|---|
| 78 Test Candidate | WATCH CANDIDATE | test / approach | none yet | A test is watch-only. |
| 78 Wick Break Candidate | REPLAY-CONTRADICTION CANDIDATE | wick crosses but close does not accept | weak/uncertain | Wick-only is not an entry and may contradict. |
| 78 Close Break Candidate | CONFIRMATION CANDIDATE | candle closes beyond 78 | may support target activation | Close break is still not entry. |
| 78 Hold / Retest Candidate | CONFIRMATION CANDIDATE | close then hold/retest | strengthens target/confirmation evidence | Still needs target, room, invalidation, timeframe agreement. |
| 78 Reclaim Candidate | NO-TRADE FILTER CANDIDATE | break then reclaim | blocks or invalidates prior target activation | Reclaim is not an opposite entry. |
| 78 Failure / Rejection Candidate | REPLAY-CONTRADICTION CANDIDATE | test/fail/reject | may keep opposite target inactive | Failure is not automatic reversal entry. |
| 78 Target-Activation Candidate | TARGET-ACTIVATION CANDIDATE | close/hold with target known | activates range endpoint target if context agrees | Target activation is not entry. |
| 78 Invalidation Candidate | NO-TRADE FILTER CANDIDATE | reclaim/fail against idea | invalidates or downgrades candidate | Invalidation blocks, not reverses automatically. |

**Example distinction:**

```text
78 wick break
  -> weaker evidence
  -> may become contradiction evidence if price reclaims

78 close break
  -> stronger confirmation candidate
  -> still not entry

78 hold/retest
  -> stronger confirmation evidence
  -> still needs target, room, invalidation, and timeframe agreement

78 reclaim
  -> invalidation or contradiction evidence
```


## 8. Support / Resistance Candidate Updates

### Rule Candidate: Resistance Break Activates Next Upside Target

**Phase 3.1 Status:** TARGET-ACTIVATION CANDIDATE  
**Prior Phase 3 Status:** TARGET ACTIVATION CANDIDATE  
**Phase 5 Decision:** Keep but refine

This remains a target-activation candidate, not an entry candidate. A resistance break can suggest the next upside target becomes active only if direction, range, target, room, and higher-timeframe context agree.

**Contradiction searches:** break fails, wick-only break, no retest, target too close, higher-timeframe obstacle, level ignored.

---

### Rule Candidate: Support Break Activates Next Downside Target

**Phase 3.1 Status:** TARGET-ACTIVATION CANDIDATE  
**Prior Phase 3 Status:** TARGET ACTIVATION CANDIDATE  
**Phase 5 Decision:** Needs more examples

This candidate needs more direct bearish evidence and should not be assumed as a perfect mirror of the resistance-break candidate.

**Contradiction searches:** breakdown reclaims quickly, support ladder unclear, target too close, higher-timeframe support blocks path, level ignored.

---

### Role Flip Candidate Family

Role flips are sequence-based. A single break is not enough.

Bullish role flip sequence:

```text
prior resistance identified
  -> close/break above resistance
  -> retest from above
  -> hold
  -> target room remains
```

Bearish role flip sequence:

```text
prior support identified
  -> close/break below support
  -> retest from below
  -> reject
  -> target room remains
```

| Split Candidate | Phase 3.1 Status | Replay Requirement |
|---|---|---|
| Prior Resistance Identified | ANALYSIS CANDIDATE | Resistance must be identified before the break. |
| Resistance Close-Break | CONFIRMATION CANDIDATE | Close above resistance, not wick-only. |
| Resistance Retest From Above | CONFIRMATION CANDIDATE | Retest happens after the break. |
| Resistance Holds As Support | ENTRY-CANDIDATE GATE | Hold after retest plus target room and invalidation. |
| Prior Support Identified | ANALYSIS CANDIDATE | Support must be identified before the break. |
| Support Close-Break | CONFIRMATION CANDIDATE | Close below support, not wick-only. |
| Support Retest From Below | CONFIRMATION CANDIDATE | Retest from below after break. |
| Support Rejects As Resistance | ENTRY-CANDIDATE GATE | Rejection after retest plus target room and invalidation. |
| Role Flip Target-Room Gate | ENTRY-CANDIDATE GATE | Target room remains after the retest. |
| Failed Role Flip / Reclaim Filter | NO-TRADE FILTER CANDIDATE | Failed retest or reclaim blocks the setup. |

Support-becomes-resistance remains under-evidenced unless direct replay and transcript/JPEG evidence is added.


## 9. No-Fib / Candle-Derived Candidate Updates

### Rule Candidate Family: Last Green Candle Resistance

**Prior Phase 3 Status:** ANALYSIS RULE / WATCH RULE  
**Phase 5 Decision:** Split before rule writing

Last Green Candle Resistance has stronger evidence so far, but the broad candidate is too coarse. It is split into:

| Split Candidate | Phase 3.1 Status | Replay Purpose |
|---|---|---|
| Bigger Last Green Candle Resistance | WATCH CANDIDATE | Test higher-context candle-derived resistance/obstacle. |
| Smaller Last Green Candle Resistance | WATCH CANDIDATE | Test local candle-derived resistance. |
| Last Green Candle Body-Level Candidate | WATCH CANDIDATE | Compare body/open/close area as level source. |
| Last Green Candle Middle-Level Candidate | WATCH CANDIDATE | Compare middle/body placement as level source. |
| Last Green Candle Resistance Ladder Candidate | TARGET-ACTIVATION CANDIDATE | Test whether breaks point toward next resistance/high. |
| Last Green Candle Source-Candle Selection Candidate | REPLAY-CONTRADICTION CANDIDATE | Test whether selected candle was arbitrary. |

**Source-candle selection labels:** last meaningful green candle before drop/pause, candle body, candle middle, wick, overlapping candles, multiple nearby candidate candles, candle ignored, another candle mattered more.

Historical replay should test whether candle-derived levels explain behavior or whether selection is arbitrary.

---

### Rule Candidate: Last Red Candle Support

**Phase 3.1 Status:** DOWNGRADED CONCEPT  
**Prior Phase 3 Status:** OBSERVATION / ANALYSIS RULE  
**Phase 5 Decision:** Downgrade / Needs more examples

Last Red Candle Support should remain downgraded or needs-more-evidence unless historical replay and examples support it directly. It must not be assumed as a mirror image of Last Green Candle Resistance.

---

### Rule Candidate: Candle Body / Middle Level

**Phase 3.1 Status:** WATCH CANDIDATE

This candidate supports the no-fib method by labeling whether candle body, middle, wick, open, or close mattered in the replay. It does not create an entry.

---

### Rule Candidate: Resistance Ladder

**Phase 3.1 Status:** TARGET-ACTIVATION CANDIDATE

A break of one resistance may activate the next resistance or prior high as a target candidate. It remains target activation only.

---

### Rule Candidate: Support Ladder

**Phase 3.1 Status:** DOWNGRADED CONCEPT / NEEDS MORE EXAMPLES

Support Ladder remains under-evidenced until direct downside examples and replay windows support it.


## 10. Target Candidate Updates

### Rule Candidate: Target Must Be Defined Before Entry

**Phase 3.1 Status:** NO-TRADE FILTER CANDIDATE  
**Prior Phase 3 Status:** NO-TRADE RULE  
**Phase 5 Decision:** Keep

This remains one of the strongest no-trade candidates. No target means no entry-candidate upgrade.

**Replay should test:** target known before confirmation, no target exists, target already hit, target blocked by obstacle, and target too close after the first candle.

---

### Rule Candidate: Room-to-Target Gate

**Phase 3.1 Status:** ENTRY-CANDIDATE GATE  
**Prior Phase 3 Status:** ENTRY FILTER  
**Phase 5 Decision:** Keep but refine

Room-to-target must stay qualitative in Phase 3.1. Do not invent numeric thresholds.

**Replay labels:** gross room, effective room, consumed room, nearest obstacle, target too close, target blocked, target already hit.

---

### Rule Candidate: Target Hit / Play Over

**Phase 3.1 Status:** LIFECYCLE CANDIDATE  
**Prior Phase 3 Status:** LIFECYCLE RULE / NO-TRADE RULE  
**Phase 5 Decision:** Keep but refine

Target Hit / Play Over becomes a lifecycle/no-trade candidate that forces reassessment before any new setup.

---

### Replay-Specific Target Candidates

| Candidate | Phase 3.1 Status | Meaning |
|---|---|---|
| Target Candidate | ANALYSIS CANDIDATE | A possible destination exists but is not active yet. |
| Active Target | TARGET-ACTIVATION CANDIDATE | Target may be active if direction, level behavior, and context agree. |
| Blocked Target | NO-TRADE FILTER CANDIDATE | Target path is blocked by obstacle. |
| Target Too Close | NO-TRADE FILTER CANDIDATE | Effective room is qualitatively insufficient. |
| Target Already Hit | NO-TRADE FILTER CANDIDATE | Old objective is complete before setup readiness. |
| Target Reached | LIFECYCLE CANDIDATE | Target was reached after labeled confirmation. |
| Target Missed After Confirmation | REPLAY-CONTRADICTION CANDIDATE | Confirmation happened, then price failed/reclaimed before target. |
| Target Retired | LIFECYCLE CANDIDATE | Target no longer applies after completion or structure change. |
| New Target After New Range | LIFECYCLE CANDIDATE | New range creates a new target map. |


## 11. Entry Readiness Candidate Updates

Entry-adjacent candidates require the strongest caution in Phase 3.1. A replay may support watch or confirmation without supporting entry-candidate language.

### Rule Candidate: Daily Defines Setup, Minute Defines Entry

**Phase 3.1 Status:** LIFECYCLE CANDIDATE  
**Prior Phase 3 Status:** ENTRY WORKFLOW RULE  
**Phase 5 Decision:** Keep but refine

This remains a workflow rule, not a trigger. Daily context defines setup and target. Minute behavior refines timing only after higher context exists.

---

### Rule Candidate Family: Entry Readiness Gate Split

| Gate | Phase 3.1 Status | Required Question |
|---|---|---|
| Direction Gate | ENTRY-CANDIDATE GATE | Does proposed side agree with direction/context? |
| Target Gate | ENTRY-CANDIDATE GATE | Is the target defined before entry-candidate evaluation? |
| Room-to-Target Gate | ENTRY-CANDIDATE GATE | Is there qualitative room to target after obstacles? |
| Invalidation Gate | ENTRY-CANDIDATE GATE | Is the wrong-level visible and logically tied to the setup? |
| Timeframe Alignment Gate | ENTRY-CANDIDATE GATE | Does lower timeframe behavior agree with higher context? |
| Support/Resistance Context Gate | ENTRY-CANDIDATE GATE | Does support/resistance context support the proposed side? |
| Confirmation Quality Gate | ENTRY-CANDIDATE GATE | Is confirmation close/hold/retest quality strong enough? |
| No-Chase Gate | NO-TRADE FILTER CANDIDATE | Has the first move already consumed the path? |
| Higher-Timeframe Obstacle Gate | NO-TRADE FILTER CANDIDATE | Does a higher timeframe obstacle block the target path? |
| Target-Already-Hit Gate | NO-TRADE FILTER CANDIDATE | Has the target already been reached? |

For entry-adjacent candidates, all labels must be present before strengthening:

```text
[ ] direction
[ ] timeframe context
[ ] current range
[ ] support/resistance context
[ ] target
[ ] room to target
[ ] confirmation behavior
[ ] invalidation candidate
[ ] no-trade filters
[ ] target not already hit
[ ] no-chase condition reviewed
```

If any are missing, classify replay as supporting watch/confirmation only, not entry-candidate status.

---

### Rule Candidate: Do Not Chase First Candle

**Phase 3.1 Status:** NO-TRADE FILTER CANDIDATE  
**Prior Phase 3 Status:** NO-TRADE RULE  
**Phase 5 Decision:** Keep but refine

This remains a no-trade filter. Replay should identify impulse candles, consumed room, base/retest behavior, and target proximity.

---

### Rule Candidate: No Invalidation / No Trade

**Phase 3.1 Status:** NO-TRADE FILTER CANDIDATE  
**Prior Phase 3 Status:** NO-TRADE RULE  
**Phase 5 Decision:** Needs more examples

This needs stronger direct evidence but should remain a conservative safety candidate.

---

### Rule Candidate: Higher Timeframe Obstacle / No Trade

**Phase 3.1 Status:** NO-TRADE FILTER CANDIDATE  
**Prior Phase 3 Status:** NO-TRADE RULE  
**Phase 5 Decision:** Needs more examples

This remains conservative and obstacle-aware. Replay should search for lower-timeframe confirmations that immediately run into daily/weekly resistance or support.


## 12. Lifecycle Candidate Updates

Trading lifecycle and replay lifecycle must remain separate.

### Original Trading Lifecycle Candidates

| Candidate | Phase 3.1 Status | Update |
|---|---|---|
| Watch to Confirm | LIFECYCLE CANDIDATE | Can be strengthened by replay if watched levels are labeled and confirmation behavior occurs. |
| Confirm to Arm | LIFECYCLE CANDIDATE | Remains highly conservative and must not become execution logic. |
| Arm to Entry Candidate | ENTRY-CANDIDATE GATE | Highest-risk candidate; requires strongest replay labels and still no execution. |

No lifecycle candidate should move to actual `ENTER`, `MANAGE`, or `EXECUTION` logic in Phase 3.1.

### Replay-Aware Lifecycle States

```text
SELECT CANDIDATE
  -> VERIFY DATA QUALITY
  -> BUILD REPLAY WINDOW
  -> LABEL STRUCTURE
  -> TEST CANDIDATE
  -> CLASSIFY REPLAY OUTCOME
  -> UPDATE EVIDENCE MATURITY
  -> HAND OFF TO PHASE 6 BACKLOG
```

Replay lifecycle controls evidence maturity. Trading lifecycle controls conceptual setup state. Neither creates orders.


## 13. Historical Replay Candidate Matrix

The matrix below includes the major candidates and the required split sub-candidates for Phase 3.1. This is a replay-planning matrix, not a rulebook.

| Rule Candidate | Prior Phase 3 Status | Phase 3.1 Status | Phase 5 Decision | Replay Data Needed | Required Replay Labels | Confirmation Search | Contradiction Search | Candidate Impact Options | Phase 6 Readiness |
|---|---|---|---|---|---|---|---|---|---|
| Direction State Identification | ANALYSIS RULE | ANALYSIS CANDIDATE | Keep but refine | 1Day, 5Min, 1Min as needed | HH/HL/LH/LL, significant high/low break, wick_test_only, close_break, follow_through, failed_break | Meaningful structure break changes direction state | Wick-only break, whipsaw, higher-timeframe conflict | refine, split wick/close language, add choppy no-trade state | Ready after swing-significance and close-vs-wick labels are defined |
| Timeframe Alignment Filter | ANALYSIS RULE / NO-TRADE FILTER | NO-TRADE FILTER CANDIDATE | Keep but refine | 1Day + 5Min/1Min | daily_context, five_minute_bridge, one_minute_execution, aligned, mixed, conflicting, obstacle, target_already_hit | Lower timeframe behavior agrees with daily target/context | Lower timeframe break runs into daily obstacle or conflicts with daily context | keep/refine labels, add obstacle filter | Ready after conflict taxonomy is stable |
| Current Range Defines Active Map | ANALYSIS RULE | ANALYSIS CANDIDATE | Keep but refine | 1Day + 5Min | foundation_range, current_range, tighter_range, same_candle_range, stale, replaced, arbitrary_anchor, ignored_levels | Mapped range explains reactions/targets | Levels ignored, range stale, arbitrary anchors | refine range replacement and staleness language | Ready after anchor-selection labels are defined |
| Foundation Range First | ANALYSIS RULE | ANALYSIS CANDIDATE | Keep but refine | 1Day | foundation_range, bigger_range, target, broad support/resistance | Foundation range explains broad structure | Too broad/stale for current behavior | keep analysis-only, require refinement path | Ready when broad-vs-refined criteria are clear |
| Tighter Range When Foundation Range Is Too Broad | REFINEMENT RULE | HISTORICAL-REPLAY TEST CANDIDATE | Keep but refine | 5Min + 1Min with 1Day context | child_range, local anchors, last meaningful candle, local target, parent conflict | Tighter range explains behavior better than foundation range | Tighter range is arbitrary or contradicts parent range | keep refinement-only, add overfit filter | Ready after parent/child range labels are stable |
| Same-Candle Range Identification | ENTRY REFINEMENT CANDIDATE | ANALYSIS CANDIDATE | Split | 5Min + 1Min | same_candle_high, same_candle_low, candle_size_context, parent_range | Single candle defensibly defines immediate structure | Candle is arbitrary or ignored | keep lower confidence, require parent context | Ready after same-candle selection standard is documented |
| Same-Candle 50/61 Reaction Candidate | ENTRY REFINEMENT CANDIDATE | WATCH CANDIDATE | Split | 5Min + 1Min | same_candle_range, 50_61_zone, reaction, slice_through | Zone acts as local support/resistance | No reaction or no target room | watch-only, no entry | Ready after reaction labels are validated |
| Same-Candle 78 Decision Candidate | ENTRY REFINEMENT CANDIDATE | CONFIRMATION CANDIDATE | Split | 5Min + 1Min | same_candle_range, 78_test, wick_break, close_break, reclaim | Close/hold beyond same-candle 78 supports confirmation | Wick-only break or reclaim | split by behavior, keep no-entry boundary | Ready after target/invalidation labels exist |
| Same-Candle Target Relationship Candidate | ENTRY REFINEMENT CANDIDATE | TARGET-ACTIVATION CANDIDATE | Split | 5Min + 1Min | same_candle_target, target_active, target_too_close | Target identifiable before confirmation | Target already hit or too close | refine target activation only | Ready when target-before-confirmation is labeled |
| Same-Candle No-Trade If No Break Candidate | ENTRY REFINEMENT CANDIDATE | NO-TRADE FILTER CANDIDATE | Split | 5Min + 1Min | no_close_break, failed_break, target_inactive | No break keeps target/setup inactive | Later close-break/reclaim changes interpretation | preserve no-trade filter | Ready after no-break examples are labeled |
| Same-Candle Overfit / Arbitrary Anchor Filter | ENTRY REFINEMENT CANDIDATE | REPLAY-CONTRADICTION CANDIDATE | Split | 5Min + 1Min | arbitrary_anchor, ignored_levels, larger_range_override | Failure cases show when not to use same-candle range | Levels consistently respected | add filter or downgrade same-candle concepts | Ready after contradiction search |
| 50/61 Sweet Spot Reaction | WATCH RULE | WATCH CANDIDATE | Keep but refine | 1Day + 5Min | 50_61_zone, support_reaction, resistance_reaction, slice_through, no_reaction, no_target_room | Zone reaction appears in context | Price slices through or target room absent | keep watch-only | Ready after reaction taxonomy is stable |
| 78 Test Candidate | CONFIRMATION CANDIDATE | WATCH CANDIDATE | Split | 1Day, 5Min, 1Min | active_range, 78_level, test | Price interacts with 78 | No break, no reaction, ignored level | watch only; no promotion | Ready after test vs break labels are applied |
| 78 Wick Break Candidate | CONFIRMATION CANDIDATE | REPLAY-CONTRADICTION CANDIDATE | Split | 1Day, 5Min, 1Min | 78_level, wick_break, close_back_inside, reclaim | Wick precedes later accepted break only with follow-through | Wick fails or reclaims | downgrade wick-only evidence | Ready after failure cases are labeled |
| 78 Close Break Candidate | CONFIRMATION CANDIDATE | CONFIRMATION CANDIDATE | Split | 1Day, 5Min, 1Min | 78_level, close_break, target, room, obstacle | Close beyond 78 supports target activation | Immediate reclaim/no follow-through/obstacle | strengthen confirmation only, never entry alone | Ready after target and room labels are present |
| 78 Hold / Retest Candidate | CONFIRMATION CANDIDATE | CONFIRMATION CANDIDATE | Split | 5Min + 1Min | 78_close_break, retest, hold, target_room | Retest/hold strengthens confirmation | Retest fails or target room gone | possible stronger confirmation; still gate-dependent | Ready after sequence labels exist |
| 78 Reclaim Candidate | INVALIDATION CANDIDATE | NO-TRADE FILTER CANDIDATE | Split | 5Min + 1Min | break, reclaim, failed_break | Reclaim weakens prior break | Reclaim absent and hold continues | add invalidation/no-trade filter | Ready after reclaim windows are labeled |
| 78 Failure / Rejection Candidate | CONFIRMATION CANDIDATE / INVALIDATION CANDIDATE | REPLAY-CONTRADICTION CANDIDATE | Split | 1Day, 5Min, 1Min | test, reject, failed_break, target_inactive | Failure keeps opposite target inactive or weakens setup | Later reclaim/hold changes interpretation | split failure vs target inactive | Ready after direct failure examples |
| 78 Target-Activation Candidate | CONFIRMATION CANDIDATE | TARGET-ACTIVATION CANDIDATE | Split | 1Day + 5Min | 78_close_break, active_target, target_not_hit | Close/hold beyond 78 activates range endpoint target | Target already hit, blocked, too close | target activation only | Ready after target states are labeled |
| 78 Invalidation Candidate | INVALIDATION CANDIDATE | NO-TRADE FILTER CANDIDATE | Split | 5Min + 1Min | 78_reclaim, failed_hold, opposite_structure | Failure invalidates prior confirmation | Continued hold/follow-through | add invalidation language | Ready after wrong-level examples |
| Resistance Break Activates Next Upside Target | TARGET ACTIVATION CANDIDATE | TARGET-ACTIVATION CANDIDATE | Keep but refine | 1Day + 5Min | resistance, close_break, next_resistance, prior_high, target_room | Break/hold points to next upside target | Wick-only break, failed break, target too close, HTF obstacle | keep target activation, add room/obstacle filters | Ready after no-fib and range examples replayed |
| Support Break Activates Next Downside Target | TARGET ACTIVATION CANDIDATE | TARGET-ACTIVATION CANDIDATE | Needs more examples | 1Day + 5Min | support, close_break, next_support, prior_low, reclaim | Break/hold points to downside target | Quick reclaim, support ladder unclear | needs direct bearish evidence; do not mirror blindly | Blocked until direct bearish replay exists |
| Prior Resistance Identified | ENTRY CANDIDATE | ANALYSIS CANDIDATE | Split | 5Min + 1Min | prior_resistance, source, confidence | Level is defensible before break | Level selected after the fact | supports role-flip precondition only | Ready when source labels exist |
| Resistance Close-Break | ENTRY CANDIDATE | CONFIRMATION CANDIDATE | Split | 5Min + 1Min | resistance, close_break | Accepted break above prior resistance | Wick only or close back below | confirmation only | Ready after close-vs-wick labeling |
| Resistance Retest From Above | ENTRY CANDIDATE | CONFIRMATION CANDIDATE | Split | 5Min + 1Min | retest_from_above | Price returns to broken resistance | No retest or retest unclear | sequence evidence only | Ready after clean retest examples |
| Resistance Holds As Support | ENTRY CANDIDATE | ENTRY-CANDIDATE GATE | Split / Needs more examples | 5Min + 1Min | hold_after_retest, target_room, invalidation | Hold supports bullish continuation gate | Retest fails, target too close | entry gate only; no execution | Ready after full chain labels |
| Prior Support Identified | ENTRY CANDIDATE | ANALYSIS CANDIDATE | Split | 5Min + 1Min | prior_support, source, confidence | Support level known before break | After-the-fact support | role-flip precondition only | Needs direct bearish examples |
| Support Close-Break | ENTRY CANDIDATE | CONFIRMATION CANDIDATE | Split | 5Min + 1Min | support, close_break | Close below support | Wick only or reclaim | confirmation only | Needs direct bearish replay |
| Support Retest From Below | ENTRY CANDIDATE | CONFIRMATION CANDIDATE | Split | 5Min + 1Min | retest_from_below | Retest occurs from below | No retest or reclaim | sequence evidence only | Needs direct bearish replay |
| Support Rejects As Resistance | ENTRY CANDIDATE | ENTRY-CANDIDATE GATE | Split / Needs more examples | 5Min + 1Min | reject_after_retest, target_room | Rejects after retest from below | Reclaim or target too close | entry gate only; not execution | Blocked until direct evidence |
| Role Flip Target-Room Gate | ENTRY CANDIDATE | ENTRY-CANDIDATE GATE | Split | 5Min + 1Min with 1Day context | role_flip, target_room, obstacle | Room remains after retest/hold | Target already hit or too close | gate only | Ready after room labels |
| Failed Role Flip / Reclaim Filter | ENTRY CANDIDATE | NO-TRADE FILTER CANDIDATE | Split | 5Min + 1Min | failed_retest, reclaim | Failed role flip blocks setup | Hold continues | add no-trade filter | Ready after failure cases |
| Bigger Last Green Candle Resistance | ANALYSIS RULE / WATCH RULE | WATCH CANDIDATE | Split | 1Day | large_context_green_candle, body_middle | Bigger candle level frames resistance/obstacle | Level ignored or another level matters more | keep watch/obstacle only | Ready after no-fib bigger examples replayed |
| Smaller Last Green Candle Resistance | ANALYSIS RULE / WATCH RULE | WATCH CANDIDATE | Split | 5Min + 1Min | local_green_candle, body_middle | Local candle level explains smaller resistance | Selection arbitrary | keep watch only | Ready after local examples replayed |
| Last Green Candle Body-Level Candidate | ANALYSIS RULE / WATCH RULE | WATCH CANDIDATE | Split | 1Day + 5Min | source_candle_body, open_close_area | Body area reacts or breaks | Wick/middle/other candle matters more | refine placement | Ready after placement comparison |
| Last Green Candle Middle-Level Candidate | ANALYSIS RULE / WATCH RULE | WATCH CANDIDATE | Split | 1Day + 5Min | source_candle_middle | Middle/body explains reaction | Level ignored | refine placement rules | Ready after body-vs-middle labeling |
| Last Green Candle Resistance Ladder Candidate | ANALYSIS RULE / WATCH RULE | TARGET-ACTIVATION CANDIDATE | Split | 1Day + 5Min | ordered_resistance_levels, next_target | Break one resistance points to next level | Ladder skipped or target too close | target activation only | Ready after ladder examples |
| Last Green Candle Source-Candle Selection Candidate | ANALYSIS RULE / WATCH RULE | REPLAY-CONTRADICTION CANDIDATE | Split | 1Day + 5Min | last_meaningful_green, overlapping_candles, candle_ignored | Selected candle explains behavior | Another candle mattered more | refine selection ranking | Ready after contradiction search |
| Last Red Candle Support | OBSERVATION / ANALYSIS RULE | DOWNGRADED CONCEPT | Downgrade / Needs more examples | 1Day + 5Min | last_meaningful_red, body_middle, support_reaction | Direct support reaction or break behavior | Inferred mirror fails or evidence absent | keep as concept until direct support evidence | Blocked until evidence improves |
| Candle Body / Middle Level | ANALYSIS RULE / WATCH RULE | WATCH CANDIDATE | Keep but refine | 1Day + 5Min | body, middle, wick, overlap | Body/middle explains reaction better than wick | Wick/open/close matters more | refine placement taxonomy | Ready after placement study |
| Resistance Ladder | ANALYSIS RULE / WATCH RULE | TARGET-ACTIVATION CANDIDATE | Keep but refine | 1Day + 5Min | ordered_resistance, next_high | Break activates next resistance/high | Target too close, obstacle, failure | keep target activation only | Ready after ladder sequences |
| Support Ladder | OBSERVATION / ANALYSIS RULE | DOWNGRADED CONCEPT | Needs more examples | 1Day + 5Min | ordered_support, next_low | Break activates next support/low | Reclaim or no clear ladder | downgrade until direct evidence | Blocked until bearish support examples |
| Target Must Be Defined Before Entry | NO-TRADE RULE | NO-TRADE FILTER CANDIDATE | Keep | All timeframes | target_candidate, active_target, target_before_confirmation, target_already_hit | Target known before confirmation/gates | No target, target already hit, blocked target | strong no-trade/lifecycle filter | Ready for Phase 6 as conservative boundary |
| Room-to-Target Gate | ENTRY FILTER | ENTRY-CANDIDATE GATE | Keep but refine | 5Min + 1Min with 1Day target | gross_room, effective_room, consumed_room, obstacle | Qualitative path remains to target | Target too close or first candle consumed move | keep qualitative; no thresholds | Ready after qualitative examples |
| Target Hit / Play Over | LIFECYCLE RULE / NO-TRADE RULE | LIFECYCLE CANDIDATE | Keep but refine | 1Day + 5Min | target_reached, retired, new_range_required | Old objective complete and setup retired | Old setup reused after target hit | force reassessment/no-trade | Ready after target-hit labeling |
| Target Candidate | N/A replay-specific | ANALYSIS CANDIDATE | New replay-specific | All timeframes | candidate_target, source, confidence | Target identifiable from range/SR before confirmation | Target selected after move | maintain as candidate only | Ready after target source taxonomy |
| Active Target | N/A replay-specific | TARGET-ACTIVATION CANDIDATE | New replay-specific | All timeframes | active_target, context_agrees | Direction/level behavior activates target | Context conflicts/target blocked | activate target only, not entry | Ready after activation labels |
| Blocked Target | N/A replay-specific | NO-TRADE FILTER CANDIDATE | New replay-specific | 1Day + lower TF | obstacle_before_target | Obstacle blocks path | Obstacle absent | strengthen obstacle filter | Ready after obstacle examples |
| Target Too Close | N/A replay-specific | NO-TRADE FILTER CANDIDATE | New replay-specific | 5Min + 1Min | target_too_close, consumed_room | Room consumed before readiness | Room remains | strengthen room gate; no thresholds | Ready after qualitative labels |
| Target Already Hit | N/A replay-specific | NO-TRADE FILTER CANDIDATE | New replay-specific | All timeframes | already_hit, retired | Target reached before setup evaluation | Target not yet hit | retire old setup | Ready after replay labeling |
| Target Reached | N/A replay-specific | LIFECYCLE CANDIDATE | New replay-specific | All timeframes | target_reached | Price reaches labeled target | Target missed/reclaimed | completion evidence only | Ready after target state labels |
| Target Missed After Confirmation | N/A replay-specific | REPLAY-CONTRADICTION CANDIDATE | New replay-specific | All timeframes | confirmed_then_missed, reclaim, invalidation | Failure after confirmation shows narrowing needed | Target reached in context | split/refine/downgrade | Ready after failure cases |
| Target Retired | N/A replay-specific | LIFECYCLE CANDIDATE | New replay-specific | All timeframes | retired, setup_complete | Old target no longer applies | Old target still active | state transition only | Ready after completion criteria |
| New Target After New Range | N/A replay-specific | LIFECYCLE CANDIDATE | New replay-specific | 1Day + 5Min | new_range, new_target | New structure defines new target | Old range still controls | refine range replacement | Ready after range-change labels |
| Daily Defines Setup, Minute Defines Entry | ENTRY WORKFLOW RULE | LIFECYCLE CANDIDATE | Keep but refine | 1Day + 1Min | daily_context, minute_behavior, alignment | Minute behavior refines daily setup | Minute invents setup without daily target | workflow only, not trigger | Ready after cross-timeframe examples |
| Direction Gate | ENTRY CANDIDATE | ENTRY-CANDIDATE GATE | Split | All timeframes | direction, allowed_side, conflict | Side agrees with structure/context | Side conflicts or unclear | gate pass/fail only | Ready after direction labels |
| Target Gate | ENTRY CANDIDATE | ENTRY-CANDIDATE GATE | Split | All timeframes | target_defined, active_target | Target defined before readiness | No target/selected after move | gate only | Ready after target-before-confirmation examples |
| Room-to-Target Gate | ENTRY CANDIDATE | ENTRY-CANDIDATE GATE | Split | 5Min + 1Min | room_to_target, obstacle, consumed_room | Room remains | Too close/blocked | gate only, qualitative | Ready after room labels |
| Invalidation Gate | ENTRY CANDIDATE | ENTRY-CANDIDATE GATE | Split | 5Min + 1Min | wrong_level, invalidation_candidate | Clear wrong-level exists | No clear wrong-level | gate only | Needs direct evidence |
| Timeframe Alignment Gate | ENTRY CANDIDATE | ENTRY-CANDIDATE GATE | Split | 1Day + lower TF | aligned, mixed, conflicting | Lower TF agrees with higher context | Conflict/obstacle | gate or filter | Ready after alignment labels |
| Support/Resistance Context Gate | ENTRY CANDIDATE | ENTRY-CANDIDATE GATE | Split | All timeframes | support, resistance, role_flip, source | SR context agrees with side | Level ignored/conflicts | gate only | Ready after SR source labels |
| Confirmation Quality Gate | ENTRY CANDIDATE | ENTRY-CANDIDATE GATE | Split | 1Min + 5Min | close_break, hold, retest, reclaim | Confirmation quality strong enough | Weak wick/no follow-through | gate only | Ready after behavior labels |
| No-Chase Gate | ENTRY CANDIDATE | NO-TRADE FILTER CANDIDATE | Split | 1Min + 5Min | first_candle, consumed_room, base_retest | Base/retest appears; target not consumed | Move already ran to target | no-trade filter | Ready after impulse/retest examples |
| Higher-Timeframe Obstacle Gate | ENTRY CANDIDATE | NO-TRADE FILTER CANDIDATE | Split | 1Day + lower TF | obstacle, blocked_target | No obstacle blocks target | Daily/weekly obstacle in path | no-trade filter | Ready after obstacle labels |
| Target-Already-Hit Gate | ENTRY CANDIDATE | NO-TRADE FILTER CANDIDATE | Split | All timeframes | target_already_hit | Target not hit yet | Old objective already complete | retire setup/no-trade | Ready after target-hit labels |
| Do Not Chase First Candle | NO-TRADE RULE | NO-TRADE FILTER CANDIDATE | Keep but refine | 1Min + 5Min | impulse_candle, base, retest, consumed_room | Waiting produces structure | Immediate chase consumes target/reverses | preserve no-chase filter | Ready after chase/non-chase replay cases |
| No Invalidation / No Trade | NO-TRADE RULE | NO-TRADE FILTER CANDIDATE | Needs more examples | 1Min + 5Min | no_clear_wrong_level, invalidation_candidate | Setup rejected due to no wrong-level | Clear invalidation exists | keep conservative | Needs direct evidence |
| Higher Timeframe Obstacle / No Trade | NO-TRADE RULE | NO-TRADE FILTER CANDIDATE | Needs more examples | 1Day + lower TF | higher_timeframe_obstacle, blocked_target | Obstacle blocks lower-timeframe idea | Obstacle absent or target path clear | keep conservative filter | Ready after obstacle examples |
| Watch to Confirm | LIFECYCLE RULE | LIFECYCLE CANDIDATE | Keep but refine | All timeframes | watched_level, interaction, confirmation_behavior | Watched level develops into confirmation | Touch without confirmation | state transition only | Ready after lifecycle labels |
| Confirm to Arm | LIFECYCLE RULE | LIFECYCLE CANDIDATE | Split before rule writing | All timeframes | confirmation, target_room, invalidation, filters | All readiness fields present | Any missing field blocks arm | state-machine candidate only | Needs full-chain examples |
| Arm to Entry Candidate | LIFECYCLE RULE / ENTRY CANDIDATE | ENTRY-CANDIDATE GATE | Needs more examples | 1Min with higher context | all gates present | Every gate present and no filter blocks | Any missing gate; target hit; no invalidation | highest caution; no execution | Blocked until strongest replay evidence exists |

## 14. Candidate-to-Replay Priority Matrix

| Priority | Candidate | Related Phase 4 Examples | Symbols | Timeframes | Replay Reason | Contradiction Search Needed | Notes |
|---:|---|---|---|---|---|---|---|
| 1 | EX-014 / Entry Readiness Gate split | EX-014 | NVDA | 1Day, 5Min, 1Min | Tests resistance context + 78 break + target + no-chase boundary | Missing target, missing invalidation, target too close, first-candle chase | Highest priority because it stresses the entry-adjacent chain. |
| 2 | Tighter Range + Last Green Candle Resistance | EX-006 | IWM | 1Day, 5Min, maybe 1Min | Tests no-clean-swing-high condition and candle-derived anchor | Arbitrary anchor, selected candle ignored, parent range conflict | Use to split range refinement from no-fib resistance. |
| 3 | Same-Candle 78 No-Play Unless Break | EX-015 | IWM | 5Min, 1Min | Tests same-candle range, 78 behavior, and no-break/no-play boundary | Same-candle levels ignored, wick-only break, target already hit | Key lower-confidence candidate; contradiction search is essential. |
| 4 | 78 Target Activation | EX-009 | SPY / S&P 500 context | 1Day, 5Min | Tests 78 close/hold relationship to 1.0 target activation | Close beyond 78 but immediate reclaim; target too close/blocked | Must remain target activation, not entry. |
| 5 | Target Hit / Play Over | EX-013 | SPY / S&P 500 context | 1Day, 5Min | Tests setup retirement after target reached | Old setup reused after target hit without new range | Good lifecycle candidate. |
| 6 | Bigger/Smaller No-Fib Resistance | EX-017, EX-018 | META, GOOGL, AAPL, AMZN, NVDA if available | 1Day, 5Min | Tests candle-derived resistance, body/middle placement, ladder behavior | Selected candle ignored; another candle mattered more | Use to refine candle selection ranking. |
| 7 | Direction Shifts | EX-001, EX-003 | SPY / S&P 500 context and similar symbols | 1Day, 1Min | Tests significant high/low break, wick vs close, follow-through | Wick breaks, whipsaws, choppy windows | Use to refine direction state language. |
| 8 | Open contradiction basket | OPEN | QQQ, TSLA, AAPL, MSFT, META, GOOGL, AMZN, AVGO | 1Day, 5Min, 1Min | Search for failures across available symbols | False breaks, ignored levels, no target room, HTF obstacles | Do not use as profitability study. |

## 15. Contradiction Search Plan By Candidate

| Candidate | Contradiction Case To Search For | Expected Candidate Impact |
|---|---|---|
| 78 Close Break | Close beyond 78 but immediate reclaim | Split close-break from hold/retest; add reclaim filter. |
| 78 Wick Break | Wick beyond 78 but no close/follow-through | Downgrade wick-only evidence and keep watch/contradiction label. |
| 50/61 Reaction | Price slices through without reaction | Keep as watch-only; do not promote. |
| Same-Candle Range | Same-candle levels ignored | Add overfit/arbitrary-anchor filter or downgrade. |
| Last Green Candle Resistance | Selected candle ignored | Refine candle-selection ranking and body/middle placement. |
| Resistance Break Target | Break occurs but target too close | Add room-to-target gate; keep target activation only. |
| Support Break Target | Breakdown reclaims quickly | Require direct bearish evidence; do not mirror resistance logic automatically. |
| Resistance Becomes Support | Retest fails | Role flip requires full sequence and target room. |
| Support Becomes Resistance | Retest fails or reclaims | Needs more direct evidence before formalization. |
| Target Must Be Defined | Break occurs with no target | Preserve no-trade rule. |
| Target Hit / Play Over | Old setup reused after target hit | Require new range/new target before any new setup. |
| Entry Readiness Gate | Missing invalidation or target room | Downgrade to confirmation/watch only. |
| Higher Timeframe Obstacle | Lower timeframe confirms into obstacle | Preserve obstacle/no-trade filter. |

## 16. Replay Outcome Handling Rules

| Replay Outcome | Candidate Handling |
|---|---|
| confirmed | Strengthen evidence only within tested context. Do not promote to execution. |
| contradicted | Revise, split, downgrade, reject, or add no-trade filter. Do not automatically reject unless contradiction is repeated and direct. |
| ambiguous | Keep in backlog; do not promote. |
| insufficient | No maturity change. |
| data quality failed | Mark replay unusable and keep candidate status unchanged. |
| target already hit | Apply no-trade or lifecycle-retirement logic. |
| target too close | Strengthen room-to-target filter. |
| higher timeframe obstacle | Strengthen obstacle/no-trade filter. |
| missing invalidation | Strengthen no-invalidation/no-trade candidate. |

Confirmed replay does not mean profitable. Confirmed replay does not mean execution-ready. Contradicted replay does not automatically reject a candidate. Ambiguous replay should block promotion.


## 17. Updated Phase 3.1 Candidate Decisions

Phase 5 remains the starting decision source. Phase 3.1 updates those decisions with replay readiness and split requirements.

| Decision | Count in this first iteration | Meaning |
|---|---:|---|
| Downgrade / Needs more examples | 1 | Candidate cards/matrix rows currently assigned this decision. |
| Keep | 1 | Candidate cards/matrix rows currently assigned this decision. |
| Keep but refine | 14 | Candidate cards/matrix rows currently assigned this decision. |
| Needs more examples | 5 | Candidate cards/matrix rows currently assigned this decision. |
| New replay-specific | 9 | Candidate cards/matrix rows currently assigned this decision. |
| Split | 38 | Candidate cards/matrix rows currently assigned this decision. |
| Split / Needs more examples | 2 | Candidate cards/matrix rows currently assigned this decision. |
| Split before rule writing | 1 | Candidate cards/matrix rows currently assigned this decision. |


Decision handling rules:

- **Keep** means the candidate remains valid as a conservative candidate.
- **Keep but refine** means the candidate must be narrowed with replay labels before Phase 6.
- **Split** means the broad candidate is no longer acceptable as one candidate.
- **Downgrade** means keep the idea as vocabulary/concept only until evidence improves.
- **Needs more examples** means no final refinement should occur until direct transcript/JPEG/replay evidence is added.
- **Needs contradiction testing** means the candidate may look promising but must be tested against failure cases.
- **Phase 6 refinement candidate** means the candidate has a stable enough boundary for later conservative rewriting, not execution.


## 18. Phase 6 Handoff Criteria

A Phase 3.1 candidate can move into Phase 6 refinement only if:

```text
[ ] Candidate is clearly defined.
[ ] Candidate has a Phase 3.1 status.
[ ] Candidate has source concepts.
[ ] Candidate has transcript/JPEG/example evidence or a clearly stated evidence gap.
[ ] Candidate has a Phase 5 decision.
[ ] Candidate has a historical replay plan.
[ ] Data quality requirements are known.
[ ] Required replay labels are known.
[ ] Contradiction search is defined.
[ ] Candidate boundary is clear.
[ ] Candidate remains non-execution-ready.
```

For entry-adjacent candidates, also require:

```text
[ ] Direction gate defined.
[ ] Target gate defined.
[ ] Room gate defined.
[ ] Confirmation gate defined.
[ ] Invalidation gate defined.
[ ] Timeframe gate defined.
[ ] No-chase gate defined.
[ ] Obstacle gate defined.
[ ] Target-already-hit gate defined.
[ ] Replay contradiction search defined.
```

Any missing gate downgrades the replay result to watch/confirmation evidence only.


## 19. Terms and Candidates That Must Not Be Used Yet

The following terms are forbidden or premature in Phase 3.1:

- Buy Signal
- Sell Signal
- Trade Signal
- Automated Entry
- Execution Rule
- Alpaca Order Trigger
- Paper-Trading Ready
- Live-Trading Ready
- Backtested Edge
- Profitable Setup
- Win Rate
- Optimized Threshold
- Production Strategy
- Fully Validated Rule

These terms belong only to later development phases after formal rule refinement, testing design, backtest design, risk modeling, paper-trading authorization, and explicit human approval. Phase 3.1 is not that stage.


## 20. Phase 3.1 Summary

### Candidates kept

- Target Must Be Defined Before Entry.
- Direction State Identification, Timeframe Alignment Filter, Current Range Defines Active Map, Foundation Range First, Tighter Range, 50/61, Resistance Break Target Activation, Target Hit / Play Over, Daily-to-Minute Workflow, Do Not Chase First Candle, Watch to Confirm.

### Candidates refined

- Direction labels now distinguish wick test, close break, follow-through, failed break, and higher-timeframe conflict.
- Timeframe alignment now distinguishes aligned, mixed, conflicting, obstacle, and target-already-hit states.
- Current range now includes stale/replaced/arbitrary/ignored-level contradiction labels.
- Target model now separates candidate, active, blocked, too close, already hit, reached, missed, retired, and new target.

### Candidates split

- 78 Decision Level.
- Entry Readiness Gate.
- Last Green Candle Resistance.
- Same-Candle Range Refinement.
- Role Flip candidates.

### Candidates downgraded

- Last Red Candle Support.
- Support Ladder.
- Any support-side mirror candidate that lacks direct bearish transcript/JPEG/replay evidence.

### Candidates needing historical replay

- NVDA entry-readiness chain from EX-014.
- IWM tighter-range / last-green-candle examples from EX-006.
- IWM same-candle no-play-unless-break example from EX-015.
- SPY 78 target activation from EX-009.
- SPY target-hit/play-over from EX-013.
- No-fib resistance examples from EX-017 and EX-018.
- Direction-shift examples from EX-001 and EX-003.

### Candidates needing contradiction testing

- 78 wick break and 78 close break.
- Same-candle range.
- Last green candle source selection.
- Resistance and support break target activation.
- Role flips.
- Room-to-target and target-too-close filters.
- Higher-timeframe obstacle filter.

### Candidates blocked from Phase 6 until more evidence exists

- Support Becomes Resistance.
- Support Ladder.
- Last Red Candle Support.
- Arm to Entry Candidate.
- No Invalidation / No Trade, unless direct examples are labeled.

### Candidates ready for conservative Phase 6 refinement

Only candidates with clear boundaries should move forward, and even then only as conservative rule-refinement inputs:

- Target Must Be Defined Before Entry.
- Direction State Identification.
- Current Range Defines Active Map.
- 50/61 Sweet Spot Reaction as watch-only.
- 78 split candidates as behavior labels, not entries.
- Resistance Break Activates Next Upside Target as target-activation only.
- Target Hit / Play Over as lifecycle only.
- Timeframe Alignment / Higher Timeframe Obstacle as filters.

### Candidates explicitly not execution-ready

All candidates in this document are explicitly not execution-ready.

Final reminder:

```text
Phase 3.1 updates rule candidates only.
It does not create final trading rules.
It does not create executable logic.
It does not create Alpaca logic.
It does not run a backtest.
It does not claim profitability.
It does not authorize paper or live trading.
```
