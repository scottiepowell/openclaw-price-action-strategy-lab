# Monster Academy Strategy Guide
# Phase 3 — Rule Candidate Extraction

Status: Draft v1.0  
Purpose: Convert the Phase 1 glossary and Phase 2 concept model into structured, testable rule candidates.

Repo alignment:

- glossary: `docs/phases/phase-01-glossary/`
- concept model: `docs/phases/phase-02-concept-model/`
- replay cases: `replay/cases/`
- contradiction cases: `replay/contradiction_cases/`
- replay labels: `replay/labels/`
- candidate indexes: `knowledge_base/rule_candidates/`

This document does **not** define final trading rules.  
This document does **not** define Alpaca execution logic.  
This document defines rule candidates that must later be validated against transcripts, JPEG snapshots, ticker examples, and chart examples.

Source basis includes the Phase 1 glossary, Phase 2 concept model, direction lessons, current-range lessons, tighter-range lessons, target lessons, and no-fib/candle-derived level lessons.

---

## 0. Core Modeling Principle

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

A 78 break, support break, resistance break, or candle-derived level break is not automatically an entry.

It is first a **confirmation candidate**.

It becomes an **entry candidate** only when direction, target room, support/resistance context, timeframe context, and invalidation agree.

---

## 1. Rule Maturity Labels

| Status | Meaning |
|---|---|
| `OBSERVATION` | A relationship seen in the strategy, but not yet structured enough for decisions |
| `ANALYSIS RULE` | Useful for interpreting the chart |
| `WATCH RULE` | Strong enough to monitor a level or condition |
| `ALERT RULE` | Strong enough to notify that price is approaching or interacting with a meaningful level |
| `CONFIRMATION CANDIDATE` | Evidence that a setup may be developing |
| `ENTRY CANDIDATE` | Context is strong enough to prepare a possible trade idea |
| `NO-TRADE RULE` | Blocks entry or suppresses the setup |
| `LIFECYCLE RULE` | Controls movement between setup states |
| `EXECUTION CANDIDATE` | Possible future paper-trading rule after validation; not live execution |

Most Phase 3 rules should remain `ANALYSIS`, `WATCH`, `ALERT`, or `CONFIRMATION CANDIDATE`.

---

## 2. Rule Candidate Template

Each rule candidate should use this structure:

```markdown
## Rule Candidate: <name>

### Status
<status>

### Source Concepts
- <glossary/concept terms>

### Source Evidence
- <transcript/JPEG/snapshot-map references>

### Purpose
What this rule is trying to detect.

### Required Context
What must already be true before this rule matters.

### Trigger
What activates the rule candidate.

### Confirmation
What strengthens the rule candidate.

### Invalidation
What cancels the rule candidate.

### Target Relationship
What target this rule activates, supports, blocks, or completes.

### Entry Relationship
Whether this creates:
- no entry
- watch condition
- confirmation condition
- entry candidate
- paper-trade candidate later

### No-Trade Conditions
When this rule should be ignored or rejected.

### Implementation Notes
How this could later become model/state-machine logic.

### Validation Examples Needed
Which transcript/JPEG/chart examples should be used to validate it.
```

---

# 3. Foundation Rules

Foundation rules must be evaluated before target, confirmation, or entry rules.

---

## Rule Candidate: Direction State Identification

### Status
`ANALYSIS RULE`

### Source Concepts
- Direction
- Bullish
- Bearish
- Sideways
- Higher high
- Higher low
- Lower high
- Lower low
- Swing high
- Swing low

### Source Evidence
Direction lessons emphasize identifying highs, lows, lower highs, broken lows, and whether price is still bearish or turning bullish. Weekly direction material also connects direction to monthly, weekly, and daily alignment.

### Purpose
Classify the market state before any setup is considered.

### Required Context
- A timeframe is selected.
- Meaningful swing highs/lows are visible.
- Recent structure can be compared to prior structure.

### Trigger
A new high, low, higher low, lower high, support break, or resistance break forms.

### Confirmation
Bullish direction is strengthened by:
- breaking a prior significant high
- forming a higher low
- holding above support
- moving toward upside target

Bearish direction is strengthened by:
- breaking a prior significant low
- forming a lower high
- rejecting from resistance
- moving toward downside target

Sideways direction is strengthened by:
- price breaking both highs and lows without continuation
- price remaining inside a broad range
- lack of clear target follow-through

### Invalidation
- Price breaks the opposite structural level.
- Higher timeframe direction conflicts.
- Price fails to follow through after a break.

### Target Relationship
Direction controls whether upside or downside targets should be preferred.

### Entry Relationship
Creates no entry. It only defines the allowed bias.

### No-Trade Conditions
- Direction is unclear.
- Market is sideways and no scalp-specific setup exists.
- Higher timeframe direction conflicts with the proposed side.

### Implementation Notes
Represent direction as a state, not a boolean:

```yaml
direction:
  state: bullish | bearish | sideways | transitioning_bullish | transitioning_bearish | unclear
  confidence: low | medium | high
  evidence:
    - swing_break
    - higher_low
    - lower_high
    - support_hold
    - resistance_break
  conflicts:
    - higher_timeframe_conflict
    - target_already_hit
    - range_unclear
```

### Validation Examples Needed
- Monthly direction examples
- Weekly direction examples
- Daily direction examples
- Sideways/consolidation examples

---

## Rule Candidate: Timeframe Alignment Filter

### Status
`ANALYSIS RULE / NO-TRADE FILTER`

### Source Concepts
- Monthly direction
- Weekly direction
- Daily direction
- Minute direction
- Top-down analysis
- Step-down process

### Source Evidence
The weekly direction source notes that monthly, weekly, and daily direction matter even when scalping, and that aligned directions create a more optimal play context.

### Purpose
Prevent a lower-timeframe setup from being treated as valid when it conflicts with higher-timeframe context.

### Required Context
- At least two timeframes have been reviewed.
- Higher-timeframe support/resistance or target context is known.
- Execution timeframe is known.

### Trigger
A lower-timeframe setup appears.

### Confirmation
Setup quality increases when:
- monthly, weekly, and daily direction align
- lower timeframe agrees with daily context
- target path does not run directly into higher-timeframe support/resistance

### Invalidation
Setup quality decreases when:
- lower timeframe opposes higher timeframe
- price is directly below higher-timeframe resistance for longs
- price is directly above higher-timeframe support for shorts
- higher-timeframe target has already been hit

### Target Relationship
Higher timeframe can define major targets and obstacles.

### Entry Relationship
Can downgrade an apparent entry candidate to watch-only or no-trade.

### No-Trade Conditions
- Higher timeframe directly contradicts the trade side.
- Higher timeframe level blocks the nearest target.
- Lower timeframe setup is isolated and not connected to a larger setup.

### Implementation Notes
Represent this as a filter before entry readiness:

```yaml
timeframe_alignment:
  monthly: bullish | bearish | sideways | unclear
  weekly: bullish | bearish | sideways | unclear
  daily: bullish | bearish | sideways | unclear
  execution: one_minute | five_minute | daily
  alignment: aligned | mixed | conflicting
  allowed_side: bullish | bearish | both | none
```

### Validation Examples Needed
- Weekly direction lesson
- Daily direction examples
- Scalp examples where daily context controls minute entry

---

## Rule Candidate: Current Range Defines Active Map

### Status
`ANALYSIS RULE`

### Source Concepts
- Current range
- Bullish range
- Bearish range
- Support
- Resistance
- 50/61 sweet spot
- 78 level
- 1.0 target
- Zero level

### Source Evidence
Current-range and tighter-range lessons repeatedly use ranges to define 78 levels, support/resistance, and endpoint targets. The tighter-range transcript shows a bearish range marked from high to low, with the 78 level marked and the one/zero endpoints used as targets depending on price behavior.

### Purpose
Require the active price leg to be mapped before confirmation or entry rules are evaluated.

### Required Context
- Meaningful high/low anchors exist.
- Range orientation can be defined.
- Current price location relative to the range is known.

### Trigger
Price begins operating inside a measurable move.

### Confirmation
The range is useful if price reacts around:
- 50/61
- 78
- range endpoint
- support/resistance derived from the range

### Invalidation
- Range anchors are unclear.
- Price creates a new high/low and changes the active range.
- A larger range overrides the local range.

### Target Relationship
The current range produces the first set of target candidates.

### Entry Relationship
No entry. It creates the map used by later rules.

### No-Trade Conditions
- No active range can be identified.
- Current range conflicts with higher timeframe structure.
- Price has already reached the range target.

### Implementation Notes
Store ranges semantically, not only by fib label:

```yaml
range:
  orientation: bullish | bearish
  anchor_start: swing_high | swing_low | candle_high | candle_low
  anchor_end: swing_high | swing_low | candle_high | candle_low
  levels:
    fifty: null
    sixty_one_eight: null
    seventy_eight_six: null
    one: null
    zero: null
  semantic_targets:
    upside_target: null
    downside_target: null
```

### Validation Examples Needed
- Current range lessons
- Weekly current range lesson
- Current range livestream examples
- Tighter range examples

---

# 4. Range Selection and Refinement Rules

---

## Rule Candidate: Foundation Range First

### Status
`ANALYSIS RULE`

### Source Concepts
- Foundation range
- Bigger range
- Current range
- Swing high
- Swing low

### Source Evidence
The tighter-range/foundation-current-range lesson explicitly says the instructor is going over price using both foundations and tighter ranges.

### Purpose
Start with the clearest larger range before refining to smaller ranges.

### Required Context
- Clear swing high and swing low exist.
- Larger structure is visible.

### Trigger
A new chart/timeframe is being mapped.

### Confirmation
Foundation range is useful if:
- it explains broad support/resistance
- it provides major target levels
- price is still operating inside it

### Invalidation
- Foundation range is too wide for execution.
- Price action has shifted to a newer local range.
- Foundation range lacks usable entry precision.

### Target Relationship
Provides major or broad targets.

### Entry Relationship
No direct entry. May require refinement.

### No-Trade Conditions
- Trader attempts to enter only from broad range without local precision.
- Target room cannot be measured from a usable entry zone.

### Implementation Notes
Use foundation ranges for context and smaller ranges for precision.

### Validation Examples Needed
- Month 4 tighter range with foundation current ranges
- Weekly current range examples

---

## Rule Candidate: Tighter Range When Foundation Range Is Too Broad

### Status
`REFINEMENT RULE`

### Source Concepts
- Tighter range
- Smaller range
- Redefined entry
- Current movement range
- Same candle range

### Source Evidence
Dedicated tighter-current-range and tighter-range-entry lessons support this rule family, including lessons on redefined entries and when to use tighter ranges.

### Purpose
Use a smaller range when the broad range is valid but not precise enough for entry.

### Required Context
- Broad range exists.
- Entry from broad range would be too wide, late, or unclear.
- Local candle structure exists.

### Trigger
Price is inside a broad range but needs tighter support/resistance or a closer 78 decision level.

### Confirmation
Tighter range is useful if it creates:
- clearer support
- clearer resistance
- clearer 78
- better target-room calculation
- tighter invalidation

### Invalidation
- Tighter range conflicts with bigger structure.
- Tighter range target is already hit.
- Tighter range does not improve entry quality.

### Target Relationship
Can create a nearer target or refine the target path.

### Entry Relationship
Can support a redefined entry candidate after confirmation.

### No-Trade Conditions
- Tighter range is arbitrary.
- Range is chosen only to force a trade.
- No target room improvement exists.

### Implementation Notes
Represent tighter ranges as child objects of broader ranges:

```yaml
range:
  id: range_big_001
  child_ranges:
    - range_tight_001
    - range_tight_002
```

### Validation Examples Needed
- Tighter current range with redefined entry
- Tighter range in bullish ranges
- Tighter range from bearish to bullish

---

## Rule Candidate: Same-Candle Range Refinement

### Status
`ENTRY REFINEMENT CANDIDATE`

### Source Concepts
- Same candle range
- Candle range
- Tighter current range
- One-minute entry
- 78 level

### Source Evidence
The tighter-current-range lesson set is associated with redefined entries and situations where normal swing structure is not clean.

### Purpose
Use one candle’s high/low as a temporary range when no clean swing structure exists.

### Required Context
- No clean swing high/low exists.
- A meaningful candle defines the immediate price structure.
- There is a valid higher-level setup.
- Target is known.

### Trigger
Price interacts with the same-candle range’s decision level.

### Confirmation
- Candle closes beyond the same-candle 78.
- Price holds beyond the level.
- Target room remains.
- Invalidation can be placed logically.

### Invalidation
- Price only wicks through.
- Price reclaims the same-candle level.
- Target is too close.
- Same-candle range conflicts with larger structure.

### Target Relationship
Usually points to a nearby current-range endpoint, prior high/low, or next support/resistance.

### Entry Relationship
Can create a one-minute entry candidate, but not an execution rule.

### No-Trade Conditions
- Same-candle range is used without higher timeframe setup.
- No target exists.
- No invalidation exists.
- Target has already been hit.

### Implementation Notes
Same-candle ranges should be marked as temporary and lower-confidence unless validated by follow-through.

### Validation Examples Needed
- Tesla one-candle/same-candle examples
- Tighter current range entry lesson
- One-minute entry examples

---

# 5. Level Reaction Rules

---

## Rule Candidate: 50/61 Sweet Spot Reaction

### Status
`WATCH RULE`

### Source Concepts
- 50 level
- 61.8 level
- 50/61 sweet spot
- Support
- Resistance
- Buying pressure
- Selling pressure

### Source Evidence
The glossary identifies the 50/61 sweet spot as a reaction zone, while current-range lessons use range levels as support/resistance decision areas.

### Purpose
Monitor price reaction inside the 50/61 area of an active range.

### Required Context
- Active range exists.
- 50 and 61.8 are mapped.
- Direction is known.

### Trigger
Price enters or tests the 50/61 zone.

### Confirmation
Bullish:
- price holds the zone
- buying pressure appears
- higher low forms

Bearish:
- price rejects from the zone
- selling pressure appears
- lower high forms

### Invalidation
- Price slices through without reaction.
- No target room remains.
- Higher timeframe conflict exists.
- No invalidation level can be defined.

### Target Relationship
A successful reaction can support movement toward the range endpoint or next resistance/support.

### Entry Relationship
Creates watch condition only.

### No-Trade Conditions
- Treating 50/61 touch as automatic entry.
- No direction.
- No active range.
- No target.

### Implementation Notes
The 50/61 should be stored as a zone, not an exact line.

### Validation Examples Needed
- Monthly current range lesson
- Weekly current range lesson
- Current range livestream examples

---

## Rule Candidate: 78 Decision Level

### Status
`CONFIRMATION CANDIDATE`

### Source Concepts
- 78 / 78.6 level
- Reversal level
- Confirmation
- Current range
- 1.0 target
- Zero target

### Source Evidence
The tighter-range/foundation-current-range transcript states that the instructor marks the 786 level, watches whether price breaks it, and uses the one or zero level as the target depending on behavior.

### Purpose
Identify when price is interacting with a major decision level.

### Required Context
- Active range exists.
- 78 level is mapped.
- Direction candidate exists.
- Target exists.
- Support/resistance context is known.

### Trigger
Price tests, breaks, closes beyond, holds above/below, or rejects from the 78 level.

### Confirmation
Strong confirmation requires:
- close beyond 78
- hold/retest beyond 78
- direction agrees
- target room exists
- no major obstacle blocks the move

### Invalidation
- Price only wicks through 78.
- Price closes back inside prior structure.
- Target already hit.
- Higher timeframe support/resistance blocks the path.

### Target Relationship
Can activate movement toward the range endpoint, prior high/low, or next target.

### Entry Relationship
Creates confirmation condition only.

### No-Trade Conditions
- Entering simply because price touched 78.
- Entering simply because price wicked through 78.
- No target.
- No room to target.
- No invalidation.

### Implementation Notes
Represent 78 behavior separately:

```yaml
level_interaction:
  level_type: seventy_eight_six
  behavior: test | wick_break | close_break | hold | reject | reclaim
  confirmation_strength: low | medium | high
```

### Validation Examples Needed
- How to use fib for current ranges
- Tighter range lessons
- Redefined entry lessons
- Current range livestream examples

---

## Rule Candidate: 78 Failure / Rejection

### Status
`CONFIRMATION CANDIDATE / INVALIDATION CANDIDATE`

### Source Concepts
- 78 level
- Reversal level
- Failed break
- Rejection
- Invalidation

### Purpose
Detect when price fails at 78 and the active idea should be weakened, invalidated, or reversed into a watch condition.

### Required Context
- Active range exists.
- 78 level is mapped.
- Bias or target expectation exists.

### Trigger
Price tests 78 but fails to close or hold beyond it.

### Confirmation
- Rejection candle appears.
- Price closes back inside the range.
- Price moves away from 78.
- Lower timeframe structure turns against the attempted break.

### Invalidation
- Price later reclaims and holds beyond 78.
- New range forms.
- Target path reopens.

### Target Relationship
May cancel one target and activate an opposite-side target candidate.

### Entry Relationship
Can cancel a setup or create an opposite-side watch condition. It should not immediately create an opposite entry.

### No-Trade Conditions
- Reversing immediately without target/invalidation.
- Treating a single rejection wick as a full setup.

### Implementation Notes
Failed 78 behavior should downgrade setup confidence before creating any opposite-side candidate.

### Validation Examples Needed
- 78 rejection examples
- Bearish-to-bullish tighter range examples
- Bullish-to-bearish reversal examples

---

# 6. Support / Resistance Rules

---

## Rule Candidate: Resistance Break Activates Next Upside Target

### Status
`TARGET ACTIVATION CANDIDATE`

### Source Concepts
- Resistance
- Resistance ladder
- Prior high
- Magnetic high
- Upside target

### Source Evidence
The no-fib resistance model in the glossary says resistance can form a ladder where breaking one resistance makes the next prior high or resistance the next target.

### Purpose
Identify when a resistance break activates the next upside target.

### Required Context
- Resistance level is known.
- Next resistance or prior high is known.
- Direction is bullish or transitioning bullish.

### Trigger
Price breaks above resistance.

### Confirmation
- Candle closes above resistance.
- Price holds above the broken level.
- Resistance retest becomes support.
- There is room to next target.

### Invalidation
- Break fails.
- Price closes back below resistance.
- Target is too close.
- Higher timeframe resistance blocks the path.

### Target Relationship
Activates next upside target.

### Entry Relationship
Creates target activation or confirmation condition, not automatic entry.

### No-Trade Conditions
- No room to next target.
- Target already hit.
- Break is only a wick.
- Higher timeframe resistance is immediately overhead.

### Implementation Notes
Store resistance ladders as ordered target paths.

### Validation Examples Needed
- No-fib resistance lessons
- Weekly/daily target lessons
- Current range livestream examples

---

## Rule Candidate: Support Break Activates Next Downside Target

### Status
`TARGET ACTIVATION CANDIDATE`

### Source Concepts
- Support
- Support ladder
- Prior low
- Magnetic low
- Downside target

### Purpose
Identify when a support break activates the next downside target.

### Required Context
- Support level is known.
- Next support or prior low is known.
- Direction is bearish or transitioning bearish.

### Trigger
Price breaks below support.

### Confirmation
- Candle closes below support.
- Price holds below broken support.
- Retest rejects from below.
- There is room to next downside target.

### Invalidation
- Price reclaims support.
- Breakdown fails.
- Target is too close.
- Higher timeframe support blocks the path.

### Target Relationship
Activates next downside target.

### Entry Relationship
Creates target activation or confirmation condition, not automatic entry.

### No-Trade Conditions
- No room to downside target.
- Support is directly below.
- Target already hit.
- Breakdown is only a wick.

### Implementation Notes
Support ladders should be stored like resistance ladders, but ordered downward.

### Validation Examples Needed
- Daily target lessons
- Current range livestream lesson
- Bearish current range examples

---

## Rule Candidate: Resistance Becomes Support

### Status
`ENTRY CANDIDATE`

### Source Concepts
- Resistance becomes support
- Break and hold
- Retest
- Bullish continuation

### Purpose
Confirm that a bullish break has been accepted.

### Required Context
- Price broke above resistance.
- Upside target is active.
- Direction supports bullish continuation.
- Room to target remains.

### Trigger
Price retests the broken resistance from above.

### Confirmation
- Retest holds.
- Candle closes upward after retest.
- Higher low forms.
- Lower timeframe confirms continuation.

### Invalidation
- Price loses the retested level.
- Price closes back below resistance.
- Target already hit.
- No room remains.

### Target Relationship
Supports continuation toward upside target.

### Entry Relationship
Can create bullish entry candidate.

### No-Trade Conditions
- No retest.
- Retest fails.
- Target too close.
- Higher timeframe resistance blocks trade.

### Implementation Notes
This should be represented as a role-flip confirmation object.

### Validation Examples Needed
- Resistance role-flip examples
- One-minute bullish entries
- No-fib resistance break examples

---

## Rule Candidate: Support Becomes Resistance

### Status
`ENTRY CANDIDATE`

### Source Concepts
- Support becomes resistance
- Breakdown
- Retest after breakdown
- Bearish continuation

### Purpose
Confirm that a bearish breakdown has been accepted.

### Required Context
- Price broke below support.
- Downside target is active.
- Direction supports bearish continuation.
- Room to target remains.

### Trigger
Price retests broken support from below.

### Confirmation
- Retest rejects.
- Candle closes downward after retest.
- Lower high forms.
- Lower timeframe confirms continuation.

### Invalidation
- Price reclaims support.
- Price closes back above support.
- Target already hit.
- No room remains.

### Target Relationship
Supports continuation toward downside target.

### Entry Relationship
Can create bearish entry candidate.

### No-Trade Conditions
- No retest.
- Retest fails.
- Target too close.
- Higher timeframe support blocks trade.

### Implementation Notes
This should be represented as bearish role-flip confirmation.

### Validation Examples Needed
- Bearish one-minute entries
- Support breakdown examples
- Daily-to-minute examples

---

# 7. No-Fib / Candle-Derived Rules

---

## Rule Candidate: Last Green Candle Resistance

### Status
`ANALYSIS RULE / WATCH RULE`

### Source Concepts
- No-fib resistance
- Last green candle resistance
- Middle-of-candle resistance
- Positive orders
- Positive volume

### Purpose
Identify local resistance without using the fib tool.

### Required Context
- No-fib method is being used.
- A meaningful green candle appears before a drop, pause, or rejection.
- Price later returns toward that candle area.

### Trigger
Price tests the body/middle of the selected green candle.

### Confirmation
- Price rejects from the candle-derived level.
- Price breaks and holds above it.
- Next resistance or prior high becomes target.
- Level aligns with other structure.

### Invalidation
- Candle selection is ambiguous.
- Price ignores the level.
- Nearby higher timeframe level is more important.

### Target Relationship
A break can activate the next resistance/prior high target.

### Entry Relationship
Creates watch or confirmation condition.

### No-Trade Conditions
- Candle is selected arbitrarily.
- No target exists after break.
- Target room is insufficient.

### Implementation Notes
Store candle-derived levels with source candle ID and level type:

```yaml
candle_level:
  source: last_green_candle
  placement: body_middle | body_open | body_close | wick
  role: resistance
```

### Validation Examples Needed
- No-fib resistance lessons
- Meta/Google entry lessons
- Apple/NVDA no-fib examples

---

## Rule Candidate: Last Red Candle Support

### Status
`OBSERVATION / ANALYSIS RULE`

### Source Concepts
- No-fib support
- Red candle
- Selling orders
- Candle body
- Middle of candle

### Purpose
Identify local support without using the fib tool.

### Required Context
- No-fib method is being used.
- A meaningful red candle appears before a push, pause, or reversal.
- Price later returns toward that candle area.

### Trigger
Price tests the body/middle of the selected red candle.

### Confirmation
- Price holds the candle-derived level.
- Price breaks below it and continues.
- Level aligns with prior support/swing structure.

### Invalidation
- Candle selection is ambiguous.
- Price ignores the level.
- Higher timeframe level is more important.

### Target Relationship
A break can activate the next lower support/prior low.

### Entry Relationship
Creates watch or confirmation condition.

### No-Trade Conditions
- No clear candle selection.
- No target.
- No invalidation.
- No room.

### Implementation Notes
This needs more validation than last-green-candle resistance.

### Validation Examples Needed
- Dedicated no-fib support examples
- Bearish entries without fib
- Current range livestream downside examples

---

# 8. Target Rules

---

## Rule Candidate: Target Must Be Defined Before Entry

### Status
`NO-TRADE RULE`

### Source Concepts
- Target
- Closest target
- Previous high target
- Previous low target
- 1.0 target
- Zero target

### Source Evidence
Target lessons are explicitly present in the Drive source set, including weekly target and daily target lessons.

### Purpose
Prevent entries without a defined destination.

### Required Context
- A setup idea exists.
- Direction or confirmation exists.

### Trigger
A setup attempts to move from confirmation into entry readiness.

### Confirmation
Entry can continue only if:
- target is known
- target has not already been hit
- target room is measurable
- target path is not blocked

### Invalidation
- No target exists.
- Target already hit.
- Target is too close.
- Target path is blocked.

### Target Relationship
This rule controls whether any target is valid enough to support entry.

### Entry Relationship
Blocks entry if no target exists.

### No-Trade Conditions
- No target.
- Target already reached.
- Nearest target too close.
- Support/resistance obstacle sits before target.

### Implementation Notes
Target should be required before lifecycle can move to `ARM`.

### Validation Examples Needed
- Daily target lesson part 1 and 2
- Weekly target lesson
- Current range livestream examples

---

## Rule Candidate: Room-to-Target Gate

### Status
`ENTRY FILTER`

### Source Concepts
- Room to target
- Closest target
- Target hit
- Play over
- Entry toward target

### Purpose
Prevent trades where the destination is too close or blocked.

### Required Context
- Candidate entry zone exists.
- Target exists.
- Nearest obstacle is known.
- Invalidation level is known.

### Trigger
A setup reaches confirmation state.

### Confirmation
- Effective room to target is acceptable.
- Obstacle-free path exists.
- Target has not already been hit.
- Reward justifies invalidation distance.

### Invalidation
- Target too close.
- Target already hit.
- Major support/resistance before target.
- Invalidation distance too large.

### Target Relationship
Determines whether the active target is tradable.

### Entry Relationship
Required before entry candidate can become armed.

### No-Trade Conditions
- Entry is too close to target.
- First candle already consumed the move.
- Setup has no measurable room.

### Implementation Notes
Later phases need a numeric threshold, but Phase 3 should keep this qualitative until examples are validated.

### Validation Examples Needed
- Daily target part 2
- One-minute entry lessons
- Current range livestream examples

---

## Rule Candidate: Target Hit / Play Over

### Status
`LIFECYCLE RULE / NO-TRADE RULE`

### Source Concepts
- Target hit
- Play over
- New target
- New current range

### Purpose
Retire a setup after the expected move has completed.

### Required Context
- Active setup exists.
- Target is defined.

### Trigger
Price reaches target.

### Confirmation
- Target was the original objective.
- No new range has been mapped.
- No new target has been created.

### Invalidation
This rule is lifted only when:
- new range forms
- new target is defined
- new confirmation appears
- setup lifecycle resets

### Target Relationship
Completes the active target.

### Entry Relationship
Blocks re-entry from the old setup.

### No-Trade Conditions
- Trader attempts to force another entry after target hit.
- No new structure exists.

### Implementation Notes
When target is hit, lifecycle should move to `COMPLETE` or `RETIRE`.

### Validation Examples Needed
- Current range livestream examples
- Target lesson examples
- Tesla/NVDA/SPY examples

---

# 9. Entry Readiness Rules

---

## Rule Candidate: Daily Defines Setup, Minute Defines Entry

### Status
`ENTRY WORKFLOW RULE`

### Source Concepts
- Daily direction
- Minute direction
- One-minute entry
- Step-down process
- Target

### Source Evidence
Current range livestream and entry-focused lessons are tied to using current range context with lower-timeframe entry refinement.

### Purpose
Prevent the one-minute chart from inventing trades disconnected from daily/current-range context.

### Required Context
- Daily or higher timeframe setup exists.
- Target is known.
- Current range is mapped.
- One-minute chart is used for timing only.

### Trigger
Price approaches a daily/current-range level.

### Confirmation
- One-minute close/break/retest agrees with the higher timeframe idea.
- One-minute entry has room to target.
- One-minute invalidation is clear.

### Invalidation
- Minute setup conflicts with daily setup.
- Daily target already hit.
- Daily level blocks trade.
- One-minute structure is choppy.

### Target Relationship
Minute entry should aim toward the target already defined by higher context.

### Entry Relationship
Can convert watch condition into entry candidate.

### No-Trade Conditions
- One-minute chart creates a trade with no daily target.
- One-minute setup goes against higher timeframe context.
- Target too close.

### Implementation Notes
Treat execution timeframe as subordinate to source timeframe.

### Validation Examples Needed
- One-minute bullish entry
- One-minute bearish entry
- Current range livestream
- Daily target lessons

---

## Rule Candidate: Entry Readiness Gate

### Status
`ENTRY CANDIDATE`

### Source Concepts
- Entry
- Confirmation
- Target
- Invalidation
- Room to target
- Support/resistance
- Timeframe context

### Purpose
Define the minimum required conditions before calling something an entry candidate.

### Required Context
All must exist:
- direction
- current range
- active target
- confirmation
- room to target
- invalidation
- support/resistance context
- timeframe agreement

### Trigger
A confirmed setup attempts to become entry-ready.

### Confirmation
Entry candidate is valid only if:
- direction agrees
- target is active
- room is sufficient
- confirmation exists
- invalidation is clear
- no-trade filters are false

### Invalidation
Any missing required condition cancels entry readiness.

### Target Relationship
Entry must point toward a valid target.

### Entry Relationship
Creates entry candidate, not execution.

### No-Trade Conditions
- No target.
- No invalidation.
- No room.
- Higher timeframe conflict.
- Target already hit.
- Chasing first candle.

### Implementation Notes
Represent this as a gate:

```yaml
entry_readiness:
  direction: pass | fail
  target: pass | fail
  confirmation: pass | fail
  room_to_target: pass | fail
  invalidation: pass | fail
  timeframe_alignment: pass | fail
  no_trade_filters: pass | fail
  status: not_ready | candidate
```

### Validation Examples Needed
- Meta/Google entry lesson
- Tesla one-candle range play
- Current range livestream
- SPY/NVDA examples

---

# 10. No-Trade and Invalidation Rules

---

## Rule Candidate: Do Not Chase First Candle

### Status
`NO-TRADE RULE`

### Source Concepts
- Don’t chase first candle
- Wait for confirmation
- Base after push
- Retest
- Target room

### Purpose
Prevent impulsive entries after a large candle or initial break.

### Required Context
- Large candle or fast move appears.
- No base/retest/hold has formed.
- Target may now be close.

### Trigger
Price breaks strongly or moves rapidly toward target.

### Confirmation of No-Trade
- No retest.
- No base.
- Target too close.
- No invalidation.
- Price is extended.

### Invalidation of No-Trade
No-trade condition can be lifted if:
- price bases
- price retests and holds/rejects
- tighter range forms
- target room remains
- invalidation becomes clear

### Target Relationship
Protects against entering after most of the target move is already complete.

### Entry Relationship
Blocks entry.

### No-Trade Conditions
This rule itself is a no-trade condition.

### Implementation Notes
Should be evaluated before entry readiness.

### Validation Examples Needed
- Daily direction examples
- One-minute entry examples
- Tighter range examples

---

## Rule Candidate: No Invalidation / No Trade

### Status
`NO-TRADE RULE`

### Source Concepts
- Invalidation
- Support failure
- Resistance failure
- 78 failure
- Risk

### Purpose
Prevent trades where the “wrong” condition is undefined.

### Required Context
- Setup has direction, target, and confirmation.
- Entry idea is being considered.

### Trigger
Setup attempts to move into entry candidate state.

### Confirmation of No-Trade
No-trade condition is active if:
- no support/resistance invalidation exists
- no 78 failure point exists
- no range boundary invalidation exists
- risk would be arbitrary

### Invalidation of No-Trade
No-trade condition is lifted when:
- invalidation level is defined
- invalidation reason is tied to setup logic
- risk can be described

### Target Relationship
Target must be paired with invalidation.

### Entry Relationship
Blocks entry.

### No-Trade Conditions
This rule itself is a no-trade condition.

### Implementation Notes
Require:

```yaml
invalidation:
  level: required
  reason: required
```

### Validation Examples Needed
- Entry lessons
- Failed 78 examples
- Support/resistance role-flip examples

---

## Rule Candidate: Higher Timeframe Obstacle / No Trade

### Status
`NO-TRADE RULE`

### Source Concepts
- Bigger support
- Bigger resistance
- Higher timeframe context
- Target room
- Timeframe conflict

### Purpose
Reject setups where a major higher-timeframe level blocks the target path.

### Required Context
- Higher timeframe support/resistance is known.
- Lower timeframe setup appears.
- Target path is mapped.

### Trigger
A setup attempts to activate target or entry.

### Confirmation of No-Trade
- Major resistance sits directly above bullish setup.
- Major support sits directly below bearish setup.
- Target is beyond the obstacle.
- Effective room to target is insufficient.

### Invalidation of No-Trade
- Obstacle breaks and holds.
- New target is defined.
- Higher timeframe context changes.

### Target Relationship
Can block or reduce target validity.

### Entry Relationship
Blocks or downgrades entry candidate.

### No-Trade Conditions
This rule itself is a no-trade condition.

### Implementation Notes
Use obstacle-aware target room:

```yaml
target_room:
  gross_room: 3.25
  nearest_obstacle: 1.00
  effective_room: 1.00
  status: insufficient
```

### Validation Examples Needed
- Weekly target lesson
- Daily target lessons
- Higher timeframe conflict examples

---

# 11. Lifecycle Transition Rules

---

## Rule Candidate: Watch to Confirm

### Status
`LIFECYCLE RULE`

### Source Concepts
- Watch condition
- Confirmation
- Break
- Close
- Hold
- Rejection
- Retest

### Purpose
Move a setup from passive observation into confirmation.

### Required Context
- Setup is in `WATCH`.
- Relevant level is mapped.
- Target candidate exists.

### Trigger
Price interacts with watched level.

### Confirmation
One or more:
- close beyond level
- hold beyond level
- rejection from level
- retest
- base formation
- support/resistance role flip

### Invalidation
- Price moves away without confirmation.
- Level is ignored.
- Target hit before entry.
- Direction changes.

### Target Relationship
Confirmation must point toward an active target.

### Entry Relationship
Moves from watch to confirmation, not entry.

### No-Trade Conditions
- No target.
- No invalidation.
- Higher timeframe conflict.

### Implementation Notes
Lifecycle transition:

```text
WATCH -> CONFIRM
```

### Validation Examples Needed
- 78 break examples
- Support/resistance break examples
- One-minute entry examples

---

## Rule Candidate: Confirm to Arm

### Status
`LIFECYCLE RULE`

### Source Concepts
- Entry readiness
- Target room
- Invalidation
- No-trade filters
- Confirmation

### Purpose
Move a confirmed setup into armed state only after all filters pass.

### Required Context
- Setup is in `CONFIRM`.
- Confirmation exists.
- Target exists.

### Trigger
System evaluates readiness.

### Confirmation
All must be true:
- direction agrees
- target active
- room sufficient
- invalidation defined
- timeframe does not conflict
- no-trade filters false

### Invalidation
- target too close
- no invalidation
- target already hit
- higher timeframe obstacle
- first candle chase

### Target Relationship
Target must remain valid.

### Entry Relationship
Moves from confirmation to armed.

### No-Trade Conditions
Any failed readiness gate blocks transition.

### Implementation Notes

```text
CONFIRM -> ARM
```

### Validation Examples Needed
- Entry lessons
- Current range livestream
- Daily target examples

---

## Rule Candidate: Arm to Entry Candidate

### Status
`LIFECYCLE RULE / ENTRY CANDIDATE`

### Source Concepts
- Armed setup
- One-minute entry
- Break and hold
- Retest
- Support/resistance role flip

### Purpose
Identify when an armed setup has an actionable entry candidate.

### Required Context
- Setup is in `ARM`.
- Execution timeframe is selected.
- Entry trigger is defined.

### Trigger
Execution timeframe confirms entry condition.

### Confirmation
Examples:
- one-minute close beyond trigger level
- retest holds/rejects
- base forms after push
- support/resistance role flip confirms

### Invalidation
- entry trigger fails
- price reclaims invalidation level
- target hit before entry
- room disappears

### Target Relationship
Entry candidate must still point to active target.

### Entry Relationship
Creates entry candidate. Still not live execution.

### No-Trade Conditions
- No room.
- No invalidation.
- Target hit.
- Execution timeframe conflicts.

### Implementation Notes
This is the highest maturity allowed in Phase 3 unless later validation promotes it.

### Validation Examples Needed
- One-minute bullish entries
- One-minute bearish entries
- Same-candle range examples

---

# 12. Alpaca Readiness Classification

No Phase 3 rule should be treated as Alpaca execution-ready.

| Rule Type | Alpaca readiness |
|---|---|
| Direction state | Analysis only |
| Timeframe alignment | Analysis/filter only |
| Current range mapping | Analysis only |
| 50/61 reaction | Watch/alert only |
| 78 decision | Confirmation only |
| Support/resistance break | Target activation/confirmation only |
| Role flip | Entry candidate only |
| Same-candle range | Entry refinement candidate only |
| Room-to-target | Entry filter |
| No-trade rules | Safety filters |
| Lifecycle rules | State-machine candidates |
| Actual order placement | Not Phase 3 |

Future paper-trading readiness requires:

```text
setup_state == ARM
side defined
target defined
room sufficient
invalidation defined
entry trigger confirmed
no-trade filters false
paper trading mode enabled
order reason logged
```

---

# 13. Phase 3 Validation Matrix Starter

| Rule Candidate | Current maturity | Evidence strength | Needs JPEG validation? | Needs more transcript examples? |
|---|---|---:|---:|---:|
| Direction State Identification | Analysis | Strong | Yes | Yes |
| Timeframe Alignment Filter | Analysis / No-Trade | Strong | Yes | Yes |
| Current Range Defines Active Map | Analysis | Strong | Yes | Yes |
| Foundation Range First | Analysis | Medium | Yes | Yes |
| Tighter Range Refinement | Refinement | Strong | Yes | Yes |
| Same-Candle Range | Entry refinement | Medium | Yes | Yes |
| 50/61 Sweet Spot Reaction | Watch | Medium | Yes | Yes |
| 78 Decision Level | Confirmation | Strong | Yes | Yes |
| 78 Failure / Rejection | Confirmation / Invalidation | Medium | Yes | Yes |
| Resistance Break Target Activation | Target activation | Medium | Yes | Yes |
| Support Break Target Activation | Target activation | Medium | Yes | Yes |
| Resistance Becomes Support | Entry candidate | Medium | Yes | Yes |
| Support Becomes Resistance | Entry candidate | Medium | Yes | Yes |
| Last Green Candle Resistance | Analysis / Watch | Medium | Yes | Yes |
| Last Red Candle Support | Observation / Analysis | Low-Medium | Yes | Yes |
| Target Must Be Defined | No-trade | Strong | Yes | Yes |
| Room-to-Target Gate | Entry filter | Strong | Yes | Yes |
| Target Hit / Play Over | Lifecycle / No-trade | Strong | Yes | Yes |
| Don’t Chase First Candle | No-trade | Medium | Yes | Yes |
| No Invalidation / No Trade | No-trade | Medium | Yes | Yes |
| Higher Timeframe Obstacle | No-trade | Medium | Yes | Yes |
| Watch to Confirm | Lifecycle | Strong | Yes | Yes |
| Confirm to Arm | Lifecycle | Medium | Yes | Yes |
| Arm to Entry Candidate | Lifecycle / Entry candidate | Medium | Yes | Yes |

---

# 14. Open Questions for Phase 4 and Phase 5

These should not be forced in Phase 3:

1. What exact candle close is required for a valid break on monthly, weekly, daily, and one-minute charts?
2. How much room to target is enough for scalps versus swings?
3. When should same-candle range be preferred over tighter current range?
4. How exactly should candle body, middle, and wick be selected in no-fib levels?
5. Is last-red-candle support equally supported by examples, or is it an inferred mirror of last-green-candle resistance?
6. How should sideways direction be handled: no trade, scalp only, or reduced confidence?
7. What makes a 78 break strong enough to move from confirmation into armed state?
8. How should target-hit behavior reset the setup lifecycle?
9. Which examples become canonical validation examples?
10. Which rules are testable by code versus still requiring visual/manual review?

---

# 15. Clean Phase 3 Summary

The clean rule structure is:

```text
Foundation:
  direction
  timeframe alignment
  current range

Range refinement:
  foundation range
  tighter range
  same-candle range

Level interaction:
  50/61 reaction
  78 decision
  support/resistance break
  role flip

Target:
  target defined
  target room
  target hit

Entry readiness:
  daily setup -> minute entry
  confirmation
  invalidation
  no-trade filters

Lifecycle:
  watch
  confirm
  arm
  entry candidate
  complete
  invalidate
  retire
```

The core rule remains:

```text
A level break is not an entry.

A level break is a candidate confirmation.

It becomes an entry candidate only when:
direction agrees,
target exists,
room to target exists,
support/resistance context agrees,
timeframe context agrees,
and invalidation is defined.
```
