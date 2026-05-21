# PHASE_2_1_CONCEPT_MODEL_HISTORICAL_REPLAY_UPDATE.md

Status: Draft v1.0  
Source basis: Phase 1 Glossary v1.0, Phase 2 Strategy Concept Model, Phase 3 Rule Candidate Extraction, Phase 4 Example Library, Phase 5 Validation Matrix, Phase 5B Historical Validation Plan, available transcript / snapshot-map / JPEG references summarized in prior phases, and historical OHLCV inventory if later confirmed.  
Purpose: Update the original Phase 2 concept model so it can reason about historical market-data replay, cross-timeframe OHLCV evidence, contradiction testing, replay labels, data quality gates, and evidence maturity before Phase 6 rule refinement.

---

## 0. Purpose and Boundary

Phase 2.1 updates the original Phase 2 Strategy Concept Model by adding a historical replay layer. The original Phase 2 model explains how vocabulary terms interact: direction, timeframe context, current range, support/resistance, target, confirmation, entry candidate, invalidation, and lifecycle state. Phase 2.1 keeps that model intact, but extends it so the project can reason about historical 1-minute, 5-minute, and 1-day OHLCV bars.

This update is still discovery and modeling work. Historical data is not being used here to create a trading system. It is being modeled as another evidence source that can support, weaken, contradict, or clarify the course-derived concepts before Phase 6 rule refinement.

Boundary statements:

- This is not a final rulebook.
- This is not financial advice.
- This is not code.
- This is not a backtest.
- This is not Alpaca logic.
- This does not create order logic.
- This does not create executable strategy conditions.
- This does not authorize automated execution.
- This does not mark anything live-trading-ready, paper-trading-ready, or execution-ready.
- This does not claim profitability, win rate, edge, expectancy, or risk/reward performance.
- Historical data is being modeled for validation, contradiction testing, replay labeling, and evidence strengthening only.

Repo alignment:

- Replay cases live under `replay/cases/`.
- Contradiction cases live under `replay/contradiction_cases/`.
- Replay labels live under `replay/labels/`.
- Candidate indexes live under `knowledge_base/rule_candidates/`.
- Paper-readiness references live under `knowledge_base/rule_candidates/paper_trade_candidate_readiness.yaml`.

Relationship to prior phases:

```text
Phase 1
  -> defined vocabulary and core terms.

Phase 1.1
  -> will refine vocabulary after later discoveries.
  -> not available yet, so Phase 2.1 must not invent Phase 1.1 terms.

Phase 2
  -> modeled how the vocabulary terms interact.

Phase 2.1
  -> updates those relationships to include historical replay evidence.

Phase 3
  -> extracted rule candidates.
  -> candidates remain candidates only.

Phase 4
  -> created transcript/JPEG-linked examples.
  -> examples remain evidence examples only.

Phase 5
  -> evaluated evidence strength and recommended keep, revise, split, downgrade, reject, or needs-more-evidence decisions.

Phase 5B
  -> introduced historical replay planning.
  -> defined inventory, data quality, replay labeling, contradiction testing, and Phase 6 handoff principles.

Phase 2.1
  -> creates the concept model needed to reason about replay evidence before Phase 6.
```

Phase 2.1 should be read as a bridge between the conceptual strategy model and the historical validation plan. It does not replace either one.

---

## 1. Updated Core Philosophy

The original Phase 2 philosophy remains the foundation:

```text
Concept relationship does not equal rule.
Confirmation does not equal entry.
Entry candidate does not equal execution.
```

A concept relationship explains how one idea supports, depends on, modifies, weakens, or invalidates another idea. A rule is a later implementation decision. Phase 2.1 must preserve that separation.

The central strategy principle also remains unchanged:

> A level break is not an entry.  
> A level break is a candidate confirmation.  
> It becomes an entry candidate only when direction, target, room to target, support/resistance context, timeframe context, and invalidation agree.

Phase 2.1 adds a historical replay principle:

```text
Historical replay does not equal proof of profitability.
Historical replay does not equal a backtest.
Historical replay does not convert a candidate into a final rule.
Historical replay only adds evidence about whether a concept relationship appears, fails, or remains ambiguous in historical bars.
```

Evidence relationship model:

```text
Transcript / JPEG evidence
  -> defines what the course appears to teach

Historical replay evidence
  -> tests whether similar labeled behavior appears in OHLCV bars

Contradiction replay
  -> tests where the candidate fails, needs narrowing, or should be downgraded

Phase 6 rule refinement
  -> may later rewrite candidates more precisely
  -> still does not imply execution readiness
```

The model should therefore avoid premature language such as:

```text
78 break means buy.
Resistance break means enter.
Same-candle 78 break is a setup.
Last green candle always becomes resistance.
Historical replay confirmed the strategy works.
```

The correct Phase 2.1 language is more conservative:

```text
A 78 close-break can be replay-labeled as a target-activation candidate when the active range, target, support/resistance context, timeframe context, and invalidation labels are also present.
```

---

## 2. Phase 2.1 Evidence Stack

Phase 2 used concepts. Phase 2.1 adds evidence types. Each concept relationship should now be evaluated across a stack of evidence layers.

| Evidence Layer | What It Represents | Strength | Limitation |
|---|---|---|---|
| Glossary evidence | Defined vocabulary from the course extraction | Establishes meaning | Does not prove relationships or behavior |
| Transcript evidence | Instructor language and teaching sequence | Shows intent and explanation | May lack precise chart labels |
| Snapshot-map evidence | Timestamps and JPEG alignment | Anchors transcript to visual material | May still need manual inspection |
| JPEG evidence | Visual chart evidence | Shows actual marked levels and chart behavior | Can be subjective without labels |
| Phase 4 example evidence | Structured transcript/JPEG example records | Connects concepts to rule candidates | Examples are not final rules |
| Phase 5 matrix evidence | Support/contradiction/maturity evaluation | Organizes what to keep/refine/split | Mostly pre-replay validation |
| Historical replay evidence | Labeled OHLCV behavior across bars | Tests whether similar behavior appears or fails | Not profitability proof and not execution logic |
| Contradiction replay evidence | Failure / false-positive windows | Prevents overfitting | May require careful context separation |
| Phase 6 refinement evidence | Later conservative rule rewriting | Can improve candidate precision | Still not live execution readiness |

Phase 2.1 should treat evidence as cumulative but not automatic. A replay-confirmed example can strengthen a candidate, but only within the specific labels and context tested. A contradiction does not automatically reject a candidate; it may show that the candidate needs narrower language, better filters, or a split into smaller concepts.

---

## 3. Historical Replay Object Model

Phase 2 modeled strategy objects such as `Direction`, `Current Range`, `Target`, `Confirmation`, and `Entry Candidate`. Phase 2.1 adds a `Historical Replay Case` object.

A historical replay case is not a trade. It is a labeled evidence record.

### 3.1 Historical replay case

```text
Historical Replay Case
  contains:
    - replay id
    - source example id, if tied to Phase 4
    - symbol
    - date window
    - data files or data source references
    - data quality state
    - timeframe stack
    - labeled concept objects
    - candidate relationships tested
    - replay outcome
    - contradiction notes
    - evidence maturity impact
    - boundary flags
```

### 3.2 Replay case fields

| Field | Purpose |
|---|---|
| Replay ID | Unique identifier such as `HR-001` or `HC-001` |
| Example ID | Optional link to Phase 4 example such as `EX-014` |
| Symbol | SPY, QQQ, NVDA, TSLA, IWM, or another confirmed symbol |
| Date window | Exact window being replayed |
| Data timeframes | 1-day, 5-minute, 1-minute, or available subset |
| Data quality state | Passed, failed, unresolved, or blocked |
| Candidate tested | Phase 3 candidate being evaluated |
| Labels present | Range, support, resistance, 50/61, 78, target, break behavior, invalidation |
| Replay outcome | Confirmed, contradicted, ambiguous, insufficient |
| Candidate impact | Keep, revise, split, downgrade, reject, needs-more-evidence |
| Boundary flags | No backtest, no profitability claim, no execution readiness |

### 3.3 Replay object boundary

A replay object can say:

```text
This replay window contains a daily range, a 78 close-break, and a later move toward the labeled 1.0 target.
```

A replay object must not say:

```text
This strategy is profitable.
Buy when this pattern appears.
This is ready for Alpaca.
This should be automated.
```

---

## 4. Updated Timeframe Model for OHLCV Replay

The original Phase 2 timeframe model used top-down reasoning:

```text
Monthly
  -> Weekly
  -> Daily
  -> Minute
```

Phase 2.1 adapts this to the historical data inventory currently planned around 1-day, 5-minute, and 1-minute bars.

### 4.1 Replay timeframe roles

| Replay Timeframe | Conceptual Role | What It Can Validate | What It Must Not Do |
|---|---|---|---|
| 1-day bars | Higher-timeframe context | Daily direction, daily range anchors, daily support/resistance, daily target, daily 78 behavior | Must not create intraday entry claims |
| 5-minute bars | Intraday structure bridge | Day structure, cleaner intraday swings, local support/resistance, retest quality | Must not replace daily context |
| 1-minute bars | Execution-timeframe evidence | Close/wick behavior, base/retest, reclaim, immediate invalidation visibility | Must not invent trades disconnected from daily/current range context |

### 4.2 Step-down replay relationship

```text
1-day context
  -> identifies broad range, direction, target, and higher-timeframe obstacles

5-minute context
  -> checks whether intraday structure agrees or conflicts
  -> helps label local support/resistance and retest quality

1-minute context
  -> labels exact break, wick, close, hold, retest, reclaim, or rejection behavior
  -> supports entry-candidate evidence only if higher context is already present
```

The 1-minute chart is a microscope. It can clarify behavior around a level, but it must not become the source of the entire setup. If the daily context cannot be reconstructed, the replay can still support watch or confirmation labels, but it should not strengthen an entry-related candidate.

### 4.3 Timeframe conflict in replay

Replay labels should explicitly capture cross-timeframe agreement or conflict.

| Condition | Replay Label | Candidate Impact |
|---|---|---|
| Daily target and 1-minute break point in same direction | aligned | Can strengthen confirmation or workflow candidates |
| Daily resistance sits directly above 1-minute bullish break | obstacle_conflict | Can downgrade or block entry-candidate language |
| 1-minute bullish break occurs inside daily bearish context | mixed_or_conflicting | Keep as watch/confirmation only unless target context agrees |
| Daily target already hit before 1-minute trigger | target_already_hit | No-trade / retire old setup |
| 1-minute level break occurs with no daily range | context_missing | Insufficient for entry-candidate evidence |

---

## 5. Updated Market Structure Model with Replay Evidence

The original market structure model answers:

```text
What is price doing, and what directional bias is reasonable?
```

Phase 2.1 adds:

```text
Does replay evidence show the same structural relationship in bars, and where does it fail?
```

### 5.1 Direction replay labels

Direction should remain a state, not a single signal.

Replay direction labels should include:

| Label | Meaning |
|---|---|
| `higher_high` | Price formed a meaningful high above a prior high |
| `higher_low` | Price formed a meaningful low above a prior low |
| `lower_high` | Price formed a meaningful high below a prior high |
| `lower_low` | Price formed a meaningful low below a prior low |
| `significant_high_break` | A meaningful high broke |
| `significant_low_break` | A meaningful low broke |
| `wick_test_only` | Price tested beyond a level but did not close/hold |
| `close_break` | Candle closed beyond the level |
| `follow_through` | Price continued in the break direction after confirmation |
| `failed_break` | Break did not hold and price reclaimed the level |

### 5.2 Replay relationship

```text
Swing High / Swing Low labels
  -> create historical range candidates
  -> create support/resistance labels
  -> create target labels
  -> create direction evidence
  -> create contradiction windows when breaks fail or whipsaw
```

Historical replay should not assume every structural break changes direction. It should preserve uncertainty when swing significance is unclear, when price only wicks through the level, or when the higher timeframe conflicts.

---

## 6. Updated Range Model with Historical Replay

Phase 2 defines the current range as the active measured movement that produces support, resistance, 50/61, 78, 1.0, zero, target-room, and invalidation candidates. Phase 2.1 adds replay requirements around range selection, staleness, and contradiction testing.

### 6.1 Historical range label

A replay range label should identify:

| Range Field | Purpose |
|---|---|
| Symbol | Market being labeled |
| Timeframe | 1-day, 5-minute, or 1-minute |
| Orientation | Bullish, bearish, unclear |
| Anchor start | Swing high, swing low, candle high, candle low, or same candle |
| Anchor end | Swing high, swing low, candle high, candle low, or same candle |
| Anchor confidence | Low, medium, high |
| Parent range | Bigger/foundation range, if any |
| Child range | Tighter/smaller range, if any |
| Semantic levels | 50/61, 78, 1.0, zero, support, resistance, target |
| Staleness state | Active, challenged, stale, replaced, unclear |

### 6.2 Range selection replay questions

For every replay window, ask:

1. Is the foundation/current range visible from the bars?
2. Are the anchors obvious, or are they subjective?
3. Does the range explain actual price reactions?
4. Does a tighter range explain current behavior better than the foundation range?
5. Did the range become stale after a new high, new low, target hit, or structural shift?
6. Did the replay contradict the chosen range because price ignored its levels?

### 6.3 Range contradiction labels

| Contradiction Label | Meaning |
|---|---|
| `arbitrary_anchor` | The selected anchor is not visually defensible |
| `stale_range` | Price has moved into newer structure and old range no longer explains behavior |
| `ignored_levels` | Price does not react to the derived levels |
| `larger_range_override` | Bigger range explains behavior better than local range |
| `tighter_range_needed` | Foundation range is valid but too broad for current behavior |
| `same_candle_overfit` | Same-candle range appears forced or unhelpful |

These labels should affect evidence maturity, not create trade rules.

---

## 7. Updated Support/Resistance Model with Replay Evidence

Phase 2 treats support and resistance as zones generated by ranges, candles, prior highs/lows, and order/volume interpretation. Phase 2.1 adds a replay requirement: each support/resistance label should record both source and behavior.

### 7.1 Replay support/resistance source labels

| Source Label | Meaning |
|---|---|
| `range_level` | Level derived from current/foundation/tighter range |
| `fifty_61_zone` | Zone around 50 and 61.8 |
| `seventy_eight_level` | 78/78.6 decision level |
| `prior_high` | Prior high acting as resistance or magnet |
| `prior_low` | Prior low acting as support or magnet |
| `last_green_candle_body` | No-fib resistance from last meaningful green candle body/middle |
| `last_red_candle_body` | Possible no-fib support from last meaningful red candle body/middle |
| `same_candle_high_low` | Level from one candle’s range |
| `role_flip_level` | Broken resistance/support being retested from the other side |

### 7.2 Replay behavior labels

| Behavior Label | Meaning |
|---|---|
| `approach` | Price moves toward the level |
| `test` | Price touches or nears the level |
| `wick_break` | Wick crosses the level but close does not accept beyond it |
| `close_break` | Candle closes beyond level |
| `hold` | Price remains beyond level after break |
| `retest` | Price returns to the level after break |
| `reject` | Price moves away from level after test |
| `reclaim` | Price crosses back through after a break |
| `ignored` | Price passes through without meaningful reaction |

### 7.3 Role-flip replay sequence

Role flips require sequence labeling. A single touch is not enough.

Bullish role flip:

```text
prior resistance identified
  -> break or close above resistance
  -> retest from above
  -> hold after retest
  -> target room still present
  -> possible bullish role-flip evidence
```

Bearish role flip:

```text
prior support identified
  -> break or close below support
  -> retest from below
  -> reject after retest
  -> target room still present
  -> possible bearish role-flip evidence
```

If any step is missing, the replay should be labeled `ambiguous` or `insufficient` for role-flip evidence.

---

## 8. Updated Target Model with Replay Evidence

The original target model answers:

```text
Where is price expected to go if the setup works?
```

Phase 2.1 adds:

```text
Was the target identifiable before the confirmation, did price have room to reach it, and did historical bars support or contradict the target relationship?
```

### 8.1 Replay target states

| Target State | Meaning |
|---|---|
| `candidate` | Target is possible but not yet active |
| `active` | Target is supported by direction, level behavior, and context |
| `blocked` | Higher timeframe support/resistance or obstacle blocks path |
| `too_close` | Effective room to target is insufficient |
| `already_hit` | Target was reached before entry-candidate evaluation |
| `reached` | Price reached target after confirmation |
| `missed` | Price failed to reach target after confirmation and invalidated/reclaimed |
| `retired` | Target no longer applies because setup completed or range changed |
| `unclear` | Target cannot be reconstructed from available labels |

### 8.2 Target-room replay model

Room-to-target remains qualitative in Phase 2.1. Do not introduce numeric thresholds unless later evidence explicitly supports them.

Replay labels should distinguish:

```text
gross_room
  -> raw distance from candidate level to target

effective_room
  -> distance after accounting for nearest obstacle

consumed_room
  -> portion of the move already used by the first candle or impulse

target_status
  -> acceptable, weak, blocked, too_close, already_hit, unclear
```

### 8.3 Target contradiction labels

| Contradiction Label | Meaning |
|---|---|
| `target_not_defined_first` | Level breaks before target is known |
| `target_already_hit` | Move is already complete before candidate evaluation |
| `target_too_close` | First move consumed most of the path |
| `obstacle_before_target` | Larger support/resistance blocks the intended target |
| `target_missed_after_confirmation` | Confirmation occurred but price failed and reclaimed before target |
| `new_range_required` | Old target was completed; new setup requires new range |

---

## 9. Updated Confirmation Model with Replay Behavior

Phase 2 defines confirmation as evidence that a setup is becoming real, not as an automatic trade command. Phase 2.1 makes confirmation more granular by separating level interaction types.

### 9.1 Replay confirmation behaviors

| Behavior | Replay Meaning | Candidate Impact |
|---|---|---|
| `test` | Price interacted with level but did not break | Watch only |
| `wick_break` | Level crossed by wick only | Low-confidence confirmation or contradiction candidate |
| `close_break` | Candle closed beyond level | Stronger confirmation candidate |
| `hold` | Price stayed beyond level | Strengthens confirmation candidate |
| `retest` | Price returned to level after break | May support role-flip evidence |
| `reject` | Price tested and moved away | May support failure/rejection candidate |
| `reclaim` | Price broke then returned through level | Contradiction or invalidation evidence |
| `follow_through` | Price continued toward target | Strengthens target relationship evidence |
| `no_follow_through` | Price failed to continue | May require narrowing or downgrade |

### 9.2 Updated 78 relationship

The 78 level should be split into replay behavior types:

```text
78 test
78 wick break
78 close break
78 hold/retest
78 failure/reclaim
78 target-activation candidate
78 invalidation candidate
```

Each behavior type can receive different evidence maturity. A wick-only break should not be treated the same as a close-break followed by hold and target movement.

### 9.3 Confirmation boundary

A replay can strengthen confirmation language when it shows:

```text
active range exists
  -> 78 or support/resistance level is labeled
  -> price closes/holds/retests/rejects the level
  -> target is known
  -> price behavior moves toward or away from target as expected
```

A replay cannot turn confirmation into execution. Confirmation remains upstream of entry readiness.

---

## 10. Updated Entry-Candidate Model with Replay Gates

The original entry model requires direction, target, confirmation, support/resistance context, target room, invalidation, and timeframe agreement. Phase 2.1 adds replay evidence gates so entry-related candidates are treated with extra caution.

### 10.1 Entry-candidate replay requirements

Before a replay can strengthen an entry-related candidate, it must label:

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
[ ] whether target was already hit
[ ] whether first candle was chased or avoided
```

If any of those are missing, the replay may support analysis, watch, or confirmation language, but not entry-candidate language.

### 10.2 Entry readiness as split gates

Phase 2.1 should split the broad entry-readiness concept into smaller model gates:

| Gate | Required Question |
|---|---|
| Direction gate | Does the proposed side agree with direction/context? |
| Target gate | Is the target defined before the entry candidate? |
| Room gate | Is there sufficient qualitative room to target? |
| Confirmation gate | Is the confirmation behavior labeled and strong enough? |
| Support/resistance gate | Does level context agree with the proposed side? |
| Timeframe gate | Does lower timeframe behavior agree with higher timeframe context? |
| Invalidation gate | Is the wrong-level visible and logically tied to the setup? |
| No-chase gate | Has the first move already consumed the target path? |
| Obstacle gate | Does higher timeframe support/resistance block the path? |

A replay can pass some gates and fail others. Partial gate completion should be recorded rather than forced into a yes/no conclusion.

---

## 11. Updated Invalidation and No-Trade Model

Phase 2 includes invalidation and risk as conservative model concepts. Phase 2.1 strengthens them because historical replay is especially useful for finding failure cases.

### 11.1 Replay invalidation labels

| Invalidation Label | Meaning |
|---|---|
| `support_failed` | Bullish support failed to hold |
| `resistance_failed` | Bearish resistance failed to reject |
| `seventy_eight_reclaimed` | Price broke 78 but reclaimed back through it |
| `range_boundary_failed` | Price exited range against the idea |
| `target_already_hit` | No remaining objective from old setup |
| `higher_timeframe_obstacle` | Larger level blocks target path |
| `no_clear_wrong_level` | No defensible invalidation level can be labeled |
| `first_candle_chase` | First candle/impulse consumed the path before valid structure formed |

### 11.2 No-trade replay states

A historical replay can strengthen no-trade language when it shows:

```text
confirmation appears
  -> but target is too close
  -> or invalidation is absent
  -> or higher timeframe obstacle blocks path
  -> or target was already hit
  -> or price only wicked through a key level
  -> or first candle consumed most of the move
```

No-trade replay evidence is valuable. It protects the project from converting attractive chart moments into premature rules.

---

## 12. Data Quality Gate Model

Historical data must pass quality gates before it can affect candidate maturity. Bad or unknown data cannot confirm or contradict a rule candidate.

### 12.1 Data quality states

| State | Meaning | Candidate Impact |
|---|---|---|
| `passed` | Required checks passed for replay window | Replay may affect evidence status |
| `warning` | Minor issue exists but window remains usable with notes | Replay may affect evidence with caution |
| `failed` | Data error blocks reliable interpretation | Replay outcome must be insufficient |
| `unknown` | Quality not checked | Replay outcome must be insufficient |
| `not_available` | Needed timeframe or symbol missing | Replay cannot be evaluated |

### 12.2 Required gates

At minimum, each replay should record:

```text
[ ] timestamps parse correctly
[ ] timezone is known
[ ] regular/extended-hours scope is known
[ ] duplicate bars absent or resolved
[ ] OHLC sanity passes
[ ] volume exists or is explicitly unavailable
[ ] adjustment status is known or risk is documented
[ ] missing candles are understood
[ ] 1-minute to 5-minute relationship is checked when both are used
[ ] intraday to daily relationship is checked when cross-timeframe replay is used
```

If the historical data inventory is not available yet, Phase 2.1 should keep inventory fields as `TBD` rather than inventing availability.

---

## 13. Replay Label Taxonomy

Replay labels are not code and not executable conditions. They are a controlled vocabulary for manual review and later evidence comparison.

### 13.1 Core replay labels

| Category | Labels |
|---|---|
| Evidence source | transcript, snapshot_map, jpeg, historical_bar_replay, contradiction_replay |
| Data quality | passed, warning, failed, unknown, not_available |
| Timeframe role | higher_context, intraday_bridge, execution_microscope |
| Range state | active, stale, replaced, nested, unclear |
| Level type | support, resistance, 50_61, 78, 1_0, zero, prior_high, prior_low, candle_body |
| Break behavior | test, wick_break, close_break, hold, retest, reclaim, reject, ignored |
| Target behavior | candidate, active, reached, missed, blocked, too_close, already_hit, retired |
| Invalidation behavior | visible, triggered, absent, unclear |
| Replay outcome | confirmed, contradicted, ambiguous, insufficient |
| Candidate impact | keep, revise, split, downgrade, reject, needs_more_evidence |

### 13.2 Replay maturity labels

| Maturity | Meaning |
|---|---|
| `unlabeled` | Replay window exists but has not been labeled |
| `data_quality_blocked` | Replay cannot be used because data quality is unresolved |
| `partially_labeled` | Some range/level behavior is labeled, but required context is missing |
| `confirmation_labeled` | Level behavior is labeled well enough for confirmation analysis |
| `target_labeled` | Target path, obstacle, and target result are labeled |
| `entry_gate_labeled` | All entry-candidate gates are labeled, but still not execution-ready |
| `contradiction_labeled` | Failure or false-positive behavior is labeled |
| `phase_6_ready_candidate` | Evidence is strong enough to refine language in Phase 6, not to execute |

---

## 14. Evidence Maturity Model Before Phase 6

Phase 2.1 should update the evidence maturity model so each candidate has both course-derived maturity and replay-derived maturity.

### 14.1 Candidate maturity dimensions

| Dimension | Question |
|---|---|
| Transcript support | Did the instructor language directly support the relationship? |
| JPEG support | Does the chart visually support it? |
| Replay support | Do historical bars show similar labeled behavior? |
| Replay contradiction | Have failure cases been intentionally searched? |
| Data quality | Did the replay window pass quality gates? |
| Context completeness | Are direction, range, target, room, timeframe, and invalidation labeled? |
| Boundary clarity | Is it clear what the example does not prove? |
| Phase 6 readiness | Is it ready for conservative rewrite, not execution? |

### 14.2 Updated evidence status

| Evidence Status | Meaning |
|---|---|
| `course_supported` | Transcript/JPEG examples support the relationship |
| `course_ambiguous` | Course evidence exists but needs visual confirmation |
| `replay_confirmed` | Historical replay supports the specific labeled relationship |
| `replay_contradicted` | Historical replay exposes a failure or false-positive case |
| `replay_insufficient` | Data or labels are not enough to evaluate |
| `split_required` | Candidate is too broad and needs smaller behavior types |
| `downgrade_required` | Candidate should remain glossary/concept language for now |
| `phase_6_refinement_candidate` | Candidate may be rewritten conservatively in Phase 6 |

A candidate should not be moved to Phase 6 simply because it has one replay confirmation. It should also have visual support, contradiction review, and clear boundaries.

---

## 15. Candidate-Specific Phase 2.1 Updates

This section updates the original Phase 2 concept relationships for the main Phase 3 candidate families.

### 15.1 Direction State Identification

Phase 2 relationship:

```text
Swing highs/lows, higher lows, lower highs, support/resistance breaks, and range orientation contribute to direction.
```

Phase 2.1 update:

```text
Historical replay must separate wick tests, close breaks, failed breaks, and follow-through before strengthening direction labels.
```

Replay evidence needed:

- Significant high/low labels.
- Whether the break was wick-only or close-based.
- Whether price followed through.
- Whether higher timeframe context agreed.

### 15.2 Timeframe Alignment Filter

Phase 2 relationship:

```text
Higher timeframes provide context and lower timeframes refine entries.
```

Phase 2.1 update:

```text
Replay must label whether lower-timeframe confirmation aligned with, conflicted with, or was blocked by daily context.
```

Replay evidence needed:

- Daily target and obstacle labels.
- 5-minute/1-minute local structure labels.
- Conflict and obstacle flags.

### 15.3 Current Range Defines Active Map

Phase 2 relationship:

```text
Current range produces support, resistance, 50/61, 78, target, and invalidation candidates.
```

Phase 2.1 update:

```text
Replay must test whether the chosen range actually explains price behavior, or whether it becomes stale, arbitrary, or overridden by another range.
```

Replay evidence needed:

- Range anchors.
- Anchor confidence.
- Reaction or non-reaction at derived levels.
- Range replacement notes.

### 15.4 Tighter Range and Same-Candle Refinement

Phase 2 relationship:

```text
Tighter ranges refine broad structure when foundation ranges are too wide or unclear.
Same-candle ranges are temporary refinement tools when one candle defines immediate structure.
```

Phase 2.1 update:

```text
Replay must prove that tighter or same-candle labels explain behavior better than broader ranges, and must record when they appear forced or overfit.
```

Replay evidence needed:

- Parent range.
- Child/tighter range.
- Reason refinement was needed.
- Whether the refined levels worked or failed.

### 15.5 50/61 Sweet Spot Reaction

Phase 2 relationship:

```text
50/61 is a reaction zone, not an entry.
```

Phase 2.1 update:

```text
Replay should classify 50/61 outcomes as hold, reject, slice-through, ambiguous, or insufficient.
```

Replay evidence needed:

- Zone boundaries.
- Direction context.
- Reaction candle or absence of reaction.
- Target relationship after reaction.

### 15.6 78 Decision Level

Phase 2 relationship:

```text
78 is a decision/confirmation level and target-activation candidate, not an entry.
```

Phase 2.1 update:

```text
78 must be split into behavior labels: test, wick break, close break, hold/retest, failure/reclaim, target activation, invalidation candidate.
```

Replay evidence needed:

- 78 level.
- Break behavior.
- Target status.
- Reclaim/failure behavior.
- Timeframe context.

### 15.7 Last Green Candle Resistance and No-Fib Levels

Phase 2 relationship:

```text
No-fib resistance may derive from candle bodies/middles, especially last meaningful green candles before a drop or pause.
```

Phase 2.1 update:

```text
Replay must store the source candle, placement, ranking rationale, reaction behavior, and next-target relationship.
```

Replay evidence needed:

- Source candle OHLC.
- Placement: body middle, open, close, wick, or approximate zone.
- Reaction or break behavior.
- Whether another candle level mattered more.

### 15.8 Target Must Be Defined / Room-to-Target / Target Hit

Phase 2 relationship:

```text
Target must exist before entry readiness; target room matters; target hit completes the old setup.
```

Phase 2.1 update:

```text
Replay must label target before confirmation/entry-candidate evaluation, record whether target was already hit, and distinguish gross room from effective room after obstacles.
```

Replay evidence needed:

- Target label.
- Target path.
- Nearest obstacle.
- Target hit/missed/already hit.
- New range requirement after completion.

### 15.9 Entry Readiness and Lifecycle

Phase 2 relationship:

```text
Entry candidate requires direction, target, confirmation, room, invalidation, support/resistance context, and timeframe agreement.
```

Phase 2.1 update:

```text
Replay can only support entry-candidate language if all gates are labeled. Otherwise it supports watch, confirmation, or no-trade language only.
```

Replay evidence needed:

- Full gate checklist.
- Lifecycle state.
- No-trade filters.
- Invalidation candidate.

---

## 16. Contradiction Replay Model

Contradiction replay is not a failure of the project. It is a required validation layer.

### 16.1 Purpose

Contradiction replay asks:

```text
Where does this candidate fail?
Where does it need narrower context?
Where does it need a no-trade filter?
Where should it be split, downgraded, or rejected?
```

### 16.2 Contradiction types

| Contradiction Type | Example |
|---|---|
| `false_break` | Price closes beyond level but quickly reclaims and fails |
| `wick_only_failure` | Price wicks beyond 78 but does not close/hold |
| `target_too_close` | Confirmation appears after most of the move is gone |
| `higher_timeframe_obstacle` | Lower timeframe confirmation runs into major support/resistance |
| `stale_range` | Old range no longer explains current behavior |
| `arbitrary_anchor` | Range anchor appears forced |
| `ignored_candle_level` | Last-green-candle level is ignored |
| `failed_role_flip` | Break occurs but retest fails |
| `missing_invalidation` | Setup has no visible wrong-level |
| `data_quality_issue` | Replay cannot be evaluated because data is unreliable |

### 16.3 Contradiction outcome

A contradiction may lead to:

- keep but refine,
- split into smaller behavior types,
- add a no-trade filter,
- downgrade to concept-only,
- reject if repeated contradictions break the candidate,
- mark as needs-more-evidence if data is insufficient.

Contradiction replay should be recorded with the same care as confirming replay. The goal is not to defend candidates. The goal is to make the model harder to fool.

---

## 17. Historical Data Inventory Concept

The historical inventory is not yet confirmed in the provided source set. Phase 5B planned an inventory for SPY, QQQ, AAPL, MSFT, NVDA, TSLA, AMZN, META, GOOGL, IWM, NFLX, and other available symbols, but each entry remains subject to actual file inspection.

Phase 2.1 should therefore model inventory as a dependency.

### 17.1 Inventory object

| Field | Meaning |
|---|---|
| Symbol | Ticker or instrument |
| 1-minute available | Yes, no, unknown, blocked |
| 5-minute available | Yes, no, unknown, blocked |
| 1-day available | Yes, no, unknown, blocked |
| Date range | Confirmed start/end after file inspection |
| Source path | Google Drive or local project path |
| Session scope | RTH, extended hours, mixed, unknown |
| Adjustment status | Raw, adjusted, unknown |
| Vendor/source | Data source if known |
| Quality status | Passed, warning, failed, unknown |

### 17.2 Inventory boundary

Do not claim a symbol has historical data until the file exists and opens. Do not infer date coverage from a filename alone. Do not mix adjusted daily data with raw intraday data without marking the risk.

---

## 18. Updated Lifecycle Model for Replay Evidence

The original lifecycle was:

```text
DISCOVER
  -> MAP
  -> BIAS
  -> TARGET
  -> WATCH
  -> CONFIRM
  -> ARM
  -> ENTER
  -> MANAGE
  -> COMPLETE / INVALIDATE / RETIRE
```

Phase 2.1 should not use `ENTER` or `MANAGE` for historical replay modeling because this phase is not creating executed trades. Instead, replay should use evidence states.

### 18.1 Replay evidence lifecycle

```text
REPLAY_DISCOVER
  -> DATA_QUALITY_CHECK
  -> CONTEXT_LABEL
  -> RANGE_LABEL
  -> LEVEL_LABEL
  -> TARGET_LABEL
  -> BEHAVIOR_LABEL
  -> CONTRADICTION_CHECK
  -> OUTCOME_CLASSIFY
  -> CANDIDATE_IMPACT_RECOMMEND
  -> PHASE_6_BACKLOG_DECISION
```

### 18.2 Replay state definitions

| State | Meaning |
|---|---|
| `REPLAY_DISCOVER` | Replay window or candidate is selected |
| `DATA_QUALITY_CHECK` | OHLCV quality and timeframe alignment are checked |
| `CONTEXT_LABEL` | Daily/5-minute/1-minute context is labeled |
| `RANGE_LABEL` | Ranges and anchors are labeled |
| `LEVEL_LABEL` | Support, resistance, 50/61, 78, targets are labeled |
| `TARGET_LABEL` | Target and room-to-target are labeled |
| `BEHAVIOR_LABEL` | Wick/close/hold/retest/reclaim behavior is labeled |
| `CONTRADICTION_CHECK` | Failure cases are reviewed |
| `OUTCOME_CLASSIFY` | Confirmed, contradicted, ambiguous, or insufficient |
| `CANDIDATE_IMPACT_RECOMMEND` | Keep, revise, split, downgrade, reject, needs-more-evidence |
| `PHASE_6_BACKLOG_DECISION` | Candidate moves to Phase 6 backlog only if boundaries are clear |

This replay lifecycle is about evidence, not orders.

---

## 19. Phase 6 Handoff Model

Phase 2.1 prepares the concept model for Phase 6, but it does not perform Phase 6 rule refinement.

### 19.1 Minimum handoff requirements

A candidate may be handed to Phase 6 for conservative rewriting only when:

```text
[ ] Phase 3 candidate definition exists.
[ ] Phase 4 example support exists.
[ ] Phase 5 matrix decision exists.
[ ] Historical replay data quality is verified for at least one useful window, if replay is used.
[ ] Replay labels include range, level, target, and behavior.
[ ] Contradiction search has been attempted or explicitly marked pending.
[ ] Candidate boundary is clear.
[ ] Candidate remains non-execution-ready.
[ ] Candidate impact is keep, revise, split, downgrade, reject, or needs-more-evidence.
```

### 19.2 Stronger handoff standard for entry-related candidates

Entry-related candidates require more caution. They need:

```text
[ ] Direction label.
[ ] Timeframe context label.
[ ] Current range label.
[ ] Support/resistance label.
[ ] Target label.
[ ] Room-to-target label.
[ ] Confirmation behavior label.
[ ] Invalidation candidate label.
[ ] No-trade filter labels.
[ ] Target already-hit check.
[ ] First-candle chase check.
```

If those labels are missing, Phase 6 should not refine entry-candidate language. It may refine analysis, watch, confirmation, or no-trade language instead.

---

## 20. Open Questions for Phase 2.1

These questions should remain open until Phase 1.1 vocabulary refinement, visual labeling, and historical inventory inspection are available.

1. Which historical OHLCV files are actually available in Google Drive or local project storage?
2. What are the confirmed date ranges for SPY, QQQ, Mag 7, NVDA, TSLA, IWM, and other symbols?
3. Are the daily bars raw or adjusted?
4. Are the intraday bars regular session only or extended-hours mixed?
5. Do 1-minute bars aggregate cleanly into 5-minute bars?
6. Do intraday bars reconcile with daily highs/lows for the same session scope?
7. Which Phase 4 examples have exact symbol/date/timeframe anchors?
8. Which replay cases are example-matched versus similar-structure searches?
9. Which candidates have contradiction evidence, not only confirming evidence?
10. Which Phase 3 candidates should be split before any Phase 6 writing?
11. Which candidates remain too visual/manual for automation discussion?
12. What vocabulary changes will Phase 1.1 introduce after replay discoveries?

---

## 21. Conservative Phase 2.1 Summary

Phase 2.1 updates the strategy concept model by adding historical replay as an evidence layer. The update keeps the original Phase 2 chain intact:

```text
Timeframe context
  -> market structure
  -> current range
  -> support/resistance
  -> confirmation level
  -> target
  -> entry candidate
  -> invalidation/risk
  -> lifecycle decision
```

It extends that chain with replay validation:

```text
Historical data inventory
  -> data quality gate
  -> cross-timeframe context labels
  -> range and level labels
  -> target and room labels
  -> break/retest/reclaim labels
  -> contradiction review
  -> evidence maturity update
  -> Phase 6 backlog decision
```

Final Phase 2.1 principle:

```text
Historical replay can validate concepts.
Historical replay can contradict assumptions.
Historical replay can improve labels.
Historical replay can prepare Phase 6.

Historical replay does not create final trading rules.
Historical replay does not authorize automated execution.
Historical replay does not prove profitability.
Historical replay does not convert a level break into an entry.
```