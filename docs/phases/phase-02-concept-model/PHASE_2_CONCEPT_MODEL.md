# Monster Academy Strategy Guide
# Phase 2 — Strategy Concept Model

Status: Draft v1.0  
Source basis: Phase 1 Glossary v1.0, Month 1–6 transcript/snapshot-map material in Google Drive, and targeted review of current-range, target, tighter-range, and entry lessons.  
Purpose: Turn glossary terms into a repeatable concept framework that OpenClaw/Codex can reason over before converting anything into executable rules or Alpaca logic.

> This document is a strategy-modeling artifact, not financial advice. Its job is to define relationships, dependencies, decision states, and implementation boundaries.

## 0.1 Repo vocabulary alignment

This model uses the repo’s working terms:

- current range
- support / resistance
- target
- invalidation
- room to target
- no-trade filter
- candidate
- replay case
- contradiction case
- paper-validation candidate

These are the nouns Phase 3, Phase 4, Phase 5, and Phase 6 will reuse.

---

## 0. Core Philosophy

The Phase 1 glossary defines the terms. Phase 2 defines how those terms interact.

The most important distinction is:

- A **concept relationship** explains how one idea supports, depends on, modifies, or invalidates another idea.
- A **rule** is a later implementation decision that converts those relationships into explicit conditions.

A premature rule would be:

```text
If price breaks the 78 level, enter.
```

The concept model should instead say:

```text
A 78 break is a confirmation candidate.
It only becomes an entry candidate when direction, target room,
support/resistance context, and execution timeframe agree.
```

That distinction matters because the strategy is not built around one isolated level. It is built around a chain:

```text
Timeframe context
  -> market structure
  -> current range
  -> support/resistance
  -> reversal/confirmation level
  -> target
  -> entry candidate
  -> invalidation/risk
  -> trade lifecycle decision
```

---

## 1. Market Structure Model

### 1.1 Purpose

The market structure model answers:

```text
What is price doing, and what directional bias is reasonable?
```

Market structure is the top-level reasoning layer. It decides whether the system should favor bullish ideas, bearish ideas, or no trade.

### 1.2 Core objects

| Object | Meaning | Produces | Depends on |
|---|---|---|---|
| `Direction` | Expected bias: bullish, bearish, neutral, or transitioning | preferred trade side | higher timeframe context, current range, support/resistance behavior, 78 behavior |
| `Bullish Structure` | Price favors upside movement | calls/long bias, upside target search | higher lows, resistance breaks, support holds, bullish range behavior |
| `Bearish Structure` | Price favors downside movement | puts/short bias, downside target search | lower highs, support breaks, resistance rejections, bearish range behavior |
| `Turn Bullish` | Transition from bearish/neutral into upside | upside confirmation candidate | resistance break, 78 break/hold, higher target activation |
| `Turn Bearish` | Transition from bullish/neutral into downside | downside confirmation candidate | support break, 78 rejection/failure, lower target activation |
| `Swing High` | Meaningful local or major high | resistance, upside magnet, range anchor | candle structure and timeframe |
| `Swing Low` | Meaningful local or major low | support, downside magnet, range anchor | candle structure and timeframe |

### 1.3 Relationship map

```text
Swing High / Swing Low
  -> create ranges
  -> create support/resistance
  -> create targets
  -> provide evidence for direction

Higher Low
  -> supports bullish continuation
  -> strengthens support context
  -> can anchor a smaller bullish range

Lower High
  -> supports bearish continuation
  -> strengthens resistance context
  -> can anchor a smaller bearish range

Break of Resistance
  -> weakens bearish thesis
  -> strengthens bullish thesis
  -> may activate upside target
  -> requires follow-through/hold/retest context

Break of Support
  -> weakens bullish thesis
  -> strengthens bearish thesis
  -> may activate downside target
  -> requires follow-through/hold/retest context
```

### 1.4 Direction is not a single signal

Direction should be modeled as a weighted conclusion, not a boolean.

```yaml
direction:
  state: bullish | bearish | neutral | transitioning
  confidence: low | medium | high
  evidence:
    - higher_timeframe_bias
    - range_orientation
    - support_or_resistance_break
    - 78_behavior
    - target_activation
    - candle_follow_through
  conflicts:
    - higher_timeframe_opposition
    - nearby_major_resistance
    - nearby_major_support
    - insufficient_room_to_target
```

---

## 2. Timeframe Model

### 2.1 Purpose

The timeframe model answers:

```text
Which chart controls context, and which chart controls execution?
```

The strategy uses top-down analysis. Higher timeframes provide context and targets. Lower timeframes refine entries.

### 2.2 Timeframe hierarchy

| Timeframe | Role | Main output | Trade use |
|---|---|---|---|
| Monthly | Macro context | major direction, major range, major target | long-term bias, LEAP/month plays |
| Weekly | Intermediate structure | weekly direction, weekly support/resistance, weekly targets | swing bias, context for daily setups |
| Daily | Tactical structure | daily direction, current daily range, daily target | daily trades, swings, scalp bias |
| Minute / 1-minute | Execution | precise entry, break/hold/retest evidence | scalp entries, refined timing |

### 2.3 Step-down relationship

```text
Monthly
  -> defines macro bias and major target zones
Weekly
  -> confirms or conflicts with monthly structure
Daily
  -> translates higher timeframe context into current playable range
Minute
  -> times entries after the higher-level idea is already built
```

### 2.4 Timeframe conflict model

The model should explicitly represent conflicts.

```yaml
timeframe_context:
  monthly:
    direction: bullish
    target: major_resistance
  weekly:
    direction: bearish_rejection_from_resistance
    target: weekly_support
  daily:
    direction: bearish
    target: daily_low
  execution:
    timeframe: one_minute
    allowed_side: bearish_only_until_daily_target_hit
```

### 2.5 Practical interpretation

Higher timeframe context does not automatically create an entry. It limits what lower timeframe entries are allowed to mean.

Example:

```text
Weekly resistance rejection
  -> daily downside targets become more meaningful
  -> 1-minute bearish entries become valid candidates
  -> random 1-minute bullish candles should not be chased
```

---

## 3. Range Model

### 3.1 Purpose

The range model answers:

```text
What active price leg is price operating inside?
```

Ranges are the map. They produce support, resistance, sweet spots, 78 decision levels, endpoints, targets, and refinement zones.

### 3.2 Range types

| Range type | Definition | Use |
|---|---|---|
| `Current Range` | Active measured movement price is currently operating inside | primary decision map |
| `Bullish Range` | Meaningful low to meaningful high | upside structure, pullback support, upside target |
| `Bearish Range` | Meaningful high to meaningful low | downside structure, rally resistance, downside target |
| `Bigger Range` | Larger swing-to-swing structure | broad context, stronger levels |
| `Smaller Range` | Local movement inside bigger range | tighter targets and entries |
| `Foundation Range` | Clearest obvious swing high/low range | primary structure before refinement |
| `Tighter Range` | Refined local range when broader structure is too wide/unclear | scalp entries, closer S/R, redefined entry |
| `Same Candle Range` | Range drawn from one candle high/low | used when only one meaningful push/candle exists |

### 3.3 Range production model

```text
Current Range
  produces:
    - current support
    - current resistance
    - 50/61 sweet spot
    - 78 decision/reversal level
    - 1.0 target
    - zero target
    - invalidation boundary candidates
    - target-room measurement
    - next-range transition condition
```

### 3.4 Bullish range orientation

```text
Bullish Range = meaningful low -> meaningful high

Produces:
  50/61 area = pullback/support reaction area
  78 area    = decision/reversal/confirmation candidate
  1.0 level  = upside endpoint/target
  0 level    = opposite boundary/support failure area
```

### 3.5 Bearish range orientation

```text
Bearish Range = meaningful high -> meaningful low

Produces:
  50/61 area = rally/resistance reaction area
  78 area    = decision/reversal/confirmation candidate
  1.0 or 0   = downside endpoint/target, depending on fib orientation
```

The implementation should not assume one hard-coded fib orientation until the charting convention is standardized. The model should store both the anchor points and the semantic label of each level.

```yaml
range:
  id: range_001
  orientation: bullish | bearish
  anchor_a:
    type: swing_low | swing_high | candle_low | candle_high
    price: 100.00
    timestamp: 2026-01-01T09:30:00-05:00
  anchor_b:
    type: swing_high | swing_low | candle_high | candle_low
    price: 110.00
    timestamp: 2026-01-01T10:15:00-05:00
  semantic_levels:
    support_zone: [103.80, 105.00]
    resistance_zone: [107.80, 108.20]
    decision_78: 107.86
    target_1: 110.00
    opposite_boundary: 100.00
```

### 3.6 Range refinement logic

The model should distinguish broad context from executable precision.

```text
Foundation Range
  -> gives broad structure
  -> may be too wide for a clean entry
  -> can require refinement

Tighter Range
  -> used when swing highs/lows are unclear
  -> uses last meaningful candle, local high/low, or same-candle structure
  -> creates closer support/resistance and 78 levels
  -> can produce a redefined entry
```

### 3.7 Range selection priority

| Situation | Preferred range concept |
|---|---|
| Clear swing high and swing low exist | Foundation/current range |
| Broad range is valid but too wide for entry | Smaller/tighter range inside broader range |
| No clean swing high/swing low | Tighter current range |
| Only one meaningful candle/push exists | Same candle range |
| Price hit target and created new high/low | New current range |

---

## 4. Support/Resistance Model

### 4.1 Purpose

The support/resistance model answers:

```text
Where should price react, break, reject, hold, or retest?
```

Support and resistance are not just horizontal lines. They are zones generated by ranges, candles, prior highs/lows, and order/volume interpretation.

### 4.2 Sources of support/resistance

| Source | Produces | Confidence impact |
|---|---|---|
| Bigger range | bigger support/resistance | stronger context |
| Current range | current support/resistance | active trade map |
| Smaller/tighter range | local support/resistance | entry refinement |
| 50/61 area | reaction zone | watch for support/resistance behavior |
| 78 level | decision/reversal/confirmation zone | important but not standalone |
| Candle body/middle | no-fib support/resistance | price-action structure |
| Prior high/low | magnetic target or S/R | liquidity/order zone |
| Retest after break | role flip confirmation | validates break quality |

### 4.3 Role-flip model

```text
Resistance becomes support:
  price breaks above resistance
  -> price retests the level from above
  -> price holds
  -> bullish continuation confidence increases

Support becomes resistance:
  price breaks below support
  -> price retests the level from below
  -> price rejects
  -> bearish continuation confidence increases
```

### 4.4 No-fib support/resistance model

The fib is a teaching/measurement tool. The mature method reads levels directly from candles.

```text
No-Fib Level
  derives from:
    - candle body
    - candle middle
    - meaningful green/red candle before reversal/pause
    - prior swing high/low
    - order/volume zone implied by candle print

No-Fib Resistance
  often derives from:
    - last meaningful green candle before drop/pause
    - middle/body of candle
    - local prior high

No-Fib Support
  often derives from:
    - last meaningful red candle before push/reversal
    - middle/body of candle
    - local prior low
```

### 4.5 Support/resistance ladder

```text
Resistance Ladder:
  current resistance breaks
  -> next resistance becomes target
  -> prior high may become magnet
  -> after break, old resistance may become support

Support Ladder:
  current support breaks
  -> next support becomes target
  -> prior low may become magnet
  -> after break, old support may become resistance
```

---

## 5. Target Model

### 5.1 Purpose

The target model answers:

```text
Where is price expected to go if the setup works?
```

The target must be defined before the entry. Without a target, the model cannot determine whether there is enough room for a trade.

### 5.2 Target types

| Target type | Source | Use |
|---|---|---|
| `1.0 Target` | range endpoint | default range target after confirmation |
| `Zero Target` | opposite range endpoint | boundary or downside/upside target depending orientation |
| `Previous High Target` | prior high | upside magnet |
| `Previous Low Target` | prior low | downside magnet |
| `Closest Target` | nearest logical level | scalp feasibility |
| `Major Target` | monthly/weekly range or major S/R | swing/longer play |
| `Daily Target` | daily range/structure | daily trade objective |
| `Minute Target` | 1-minute range/ladder | scalp objective |
| `Extension Target` | 1.618/2.618 extension | only after normal target breaks |

### 5.3 Target activation model

```text
Target Candidate
  becomes Active Target when:
    - direction agrees
    - price breaks/holds/rejects the relevant level
    - target is not already hit
    - there is enough room from entry to target
    - higher timeframe context does not directly contradict it
```

### 5.4 Target-room model

```yaml
target_room:
  entry_candidate_price: 105.25
  target_price: 108.50
  gross_room: 3.25
  nearest_obstacle:
    type: resistance
    price: 106.10
  effective_room: 0.85
  status: insufficient | acceptable | strong
```

A target may be technically valid but not tradable if the entry is too close to the target or if an obstacle sits between entry and target.

### 5.5 Target completion model

```text
Target Hit
  -> setup objective complete
  -> play is over unless a new setup forms
  -> remove or retire old target
  -> reassess current range
  -> build new target only from new structure
```

---

## 6. Entry Model

### 6.1 Purpose

The entry model answers:

```text
Is there a specific, justified place to take the trade?
```

Entry comes late in the reasoning chain. It is downstream of direction, range, support/resistance, target, and confirmation.

### 6.2 Entry dependency graph

```text
Entry Candidate
  requires:
    - direction candidate
    - active target
    - support/resistance context
    - confirmation candidate
    - room to target
    - invalidation point
    - execution timeframe agreement
```

### 6.3 Entry types

| Entry type | Description | Needs |
|---|---|---|
| `Bullish Entry` | Entry expecting upside | support hold, resistance break, 78 confirmation, upside target |
| `Bearish Entry` | Entry expecting downside | resistance rejection, support break, 78 confirmation, downside target |
| `Redefined Entry` | More precise entry from tighter/smaller range | broad setup + refined local level |
| `Tighter Entry` | Entry using local/tighter range | closer S/R + target room |
| `One-Minute Bullish Entry` | Execution on 1-min chart | base, break, hold/retest, target |
| `One-Minute Bearish Entry` | Execution on 1-min chart | breakdown, rejection/retest, target |
| `No-Fib Entry` | Entry from candle/order structure | candle-derived levels + confirmation |

### 6.4 Entry is not equal to confirmation

```text
Confirmation candidate:
  "Price broke 78."

Entry candidate:
  "Price broke 78, direction agrees, target is active,
   there is room to target, support/resistance context agrees,
   and invalidation is defined."
```

### 6.5 Don’t chase model

```text
Large candle appears
  -> do not automatically enter
  -> check if target is already too close
  -> wait for base/retest/hold/rejection
  -> refine entry with tighter range if needed
```

### 6.6 Entry object schema

```yaml
entry_candidate:
  side: bullish | bearish
  source_timeframe: one_minute | five_minute | daily
  setup_context:
    direction_id: direction_001
    range_id: range_003
    target_id: target_002
    confirmation_id: confirmation_004
  trigger_type:
    - break_and_hold
    - breakdown_and_retest
    - resistance_rejection
    - support_hold
    - close_above_level
    - close_below_level
  entry_price_zone: [105.10, 105.35]
  invalidation:
    type: level_failure
    price: 104.70
  target:
    primary: 108.50
    secondary: null
  room_to_target: acceptable
  status: watch | armed | active | invalidated | complete
```

---

## 7. Confirmation Model

### 7.1 Purpose

The confirmation model answers:

```text
What evidence says the setup is becoming real?
```

Confirmation should be modeled as evidence, not as an automatic trade command.

### 7.2 Confirmation candidates

| Confirmation type | Bullish interpretation | Bearish interpretation |
|---|---|---|
| 78 break | possible reversal/continuation toward upside target | possible failure of bearish pressure |
| 78 rejection/failure | bullish attempt failed | bearish continuation likely |
| Close above level | buyers accepted above resistance | weakens bearish thesis |
| Close below level | sellers accepted below support | weakens bullish thesis |
| Break-and-hold | old resistance may become support | old support may become resistance |
| Retest and hold | validates breakout | validates breakdown if below support |
| Base after push | controlled continuation | avoid chasing first candle |
| Rejection from resistance | upside failure | bearish evidence |
| Support hold | bullish defense | downside failure |

### 7.3 78-level relationship

```text
78 Level
  role:
    - reversal candidate
    - confirmation candidate
    - decision level
    - target-activation filter
  does_not_equal:
    - automatic entry
    - automatic direction change
    - automatic target guarantee
```

### 7.4 Confirmation confidence

```yaml
confirmation:
  level_type: 78 | support | resistance | candle_body | prior_high_low
  behavior:
    - break
    - close_above
    - close_below
    - hold
    - reject
    - retest
  strength: low | medium | high
  requires_followthrough: true
  becomes_entry_candidate_only_if:
    - direction_agrees
    - target_active
    - room_to_target_sufficient
    - invalidation_defined
```

---

## 8. Invalidation/Risk Model

### 8.1 Purpose

The invalidation/risk model answers:

```text
What would prove the trade idea wrong or no longer worth taking?
```

The glossary has less explicit risk language than structure language, so this model should stay conservative and avoid overfitting. It should define invalidation candidates first, then rules later.

### 8.2 Invalidation candidates

| Concept | Bullish invalidation | Bearish invalidation |
|---|---|---|
| Support | support breaks/fails to hold | support breaks in favor, not invalidating unless target already hit |
| Resistance | resistance rejection may pause/kill long | resistance breaks/holds above, weakening short |
| 78 level | break fails and price returns below | breakdown fails and price returns above |
| Range boundary | price exits against expected side | price exits against expected side |
| Target already hit | no room remains | no room remains |
| Higher timeframe level | major resistance too close | major support too close |
| Retest failure | old resistance fails to hold as support | old support fails to hold as resistance |

### 8.3 Risk object schema

```yaml
risk_model:
  invalidation_level:
    type: support | resistance | 78 | range_boundary | candle_body
    price: 104.70
  reason: "Bullish thesis depends on support holding after breakout."
  max_loss_model:
    type: not_defined_yet
    note: "Position sizing rules belong to a later phase."
  trade_quality_flags:
    - target_too_close
    - level_conflict
    - higher_timeframe_against_trade
    - chasing_first_candle
    - no_retest_or_hold
```

### 8.4 Risk relationship principles

```text
No target -> no trade.
No invalidation -> no trade.
No room to target -> no trade.
Target already hit -> no new trade unless new setup forms.
Conflicting higher timeframe level nearby -> reduce confidence or wait.
```

---

## 9. Trade Setup Lifecycle

### 9.1 Purpose

The trade setup lifecycle answers:

```text
What state is the trade idea currently in?
```

This is important for OpenClaw and Alpaca because the system should not jump directly from “level identified” to “order submitted.”

### 9.2 Lifecycle states

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

### 9.3 State definitions

| State | Meaning | Allowed next states |
|---|---|---|
| `DISCOVER` | Identify ticker/timeframe/available candles | MAP, RETIRE |
| `MAP` | Build ranges, S/R, 50/61, 78, targets | BIAS, RETIRE |
| `BIAS` | Determine bullish/bearish/neutral/transition | TARGET, WATCH, RETIRE |
| `TARGET` | Define active target and target room | WATCH, RETIRE |
| `WATCH` | Wait for price near relevant level | CONFIRM, RETIRE |
| `CONFIRM` | Evidence appears: break, hold, reject, close | ARM, WATCH, INVALIDATE |
| `ARM` | Entry candidate is valid, waiting for execution condition | ENTER, WATCH, INVALIDATE |
| `ENTER` | Trade taken or order submitted | MANAGE |
| `MANAGE` | Monitor target, invalidation, new range | COMPLETE, INVALIDATE, RETIRE |
| `COMPLETE` | Target hit or planned objective done | RETIRE, MAP for new setup |
| `INVALIDATE` | Trade thesis failed | RETIRE, MAP for new setup |
| `RETIRE` | Stop tracking old idea | DISCOVER/MAP new setup |

### 9.4 Lifecycle guardrails

```text
Cannot enter from DISCOVER.
Cannot enter from MAP.
Cannot enter from BIAS.
Cannot enter from TARGET.
Cannot enter from WATCH unless confirmation exists.
Cannot enter from CONFIRM unless target room and invalidation exist.
Cannot re-enter after COMPLETE unless a new setup is mapped.
```

### 9.5 Setup lifecycle example

```yaml
setup_lifecycle:
  state: WATCH
  ticker: META
  timeframe_context:
    daily: bearish_from_resistance
    one_minute: waiting_for_breakdown
  current_range:
    orientation: bearish
    support_zone: [500.00, 501.00]
    resistance_zone: [508.00, 510.00]
    decision_78: 503.25
  active_target:
    type: previous_low
    price: 497.50
  watch_condition:
    - price_rejects_resistance
    - price_closes_below_78
    - room_to_target_remains_sufficient
  invalidation_candidate:
    type: reclaim_resistance
    price: 508.00
```

---

## 10. Alpaca Implementation Notes

### 10.1 Implementation boundary

Alpaca should not receive trade orders directly from raw glossary terms.

Bad architecture:

```text
Glossary term detected -> Alpaca order
```

Better architecture:

```text
Market data
  -> candle/range parser
  -> concept model objects
  -> setup lifecycle state machine
  -> rule engine
  -> risk/order checks
  -> Alpaca paper order
  -> execution log
```

### 10.2 Suggested component architecture

```text
/data
  CandleFeed
  AlpacaMarketDataClient
  HistoricalBarStore

/structure
  SwingPointDetector
  RangeBuilder
  FibLevelCalculator
  CandleLevelDetector
  SupportResistanceBuilder

/model
  DirectionModel
  TimeframeContextModel
  TargetModel
  ConfirmationModel
  RiskModel
  TradeSetupLifecycle

/rules
  RuleCandidateEvaluator
  RuleBacktester
  RuleVersionRegistry

/execution
  PaperTradeExecutor
  AlpacaOrderAdapter
  PositionMonitor
  TradeJournalWriter
```

### 10.3 Data objects to store

```yaml
candle:
  symbol: SPY
  timeframe: 1Min
  timestamp: 2026-01-01T09:31:00-05:00
  open: 500.00
  high: 501.25
  low: 499.80
  close: 500.90
  volume: 123456

range:
  id: range_001
  symbol: SPY
  timeframe: Daily
  orientation: bullish
  anchor_start: candle_or_swing_id
  anchor_end: candle_or_swing_id
  levels:
    fifty: 505.00
    sixty_one_eight: 506.18
    seventy_eight_six: 507.86
    one: 510.00
    zero: 500.00

setup:
  id: setup_001
  symbol: SPY
  side: bullish
  state: WATCH
  direction_confidence: medium
  range_id: range_001
  target_id: target_001
  confirmation_required:
    - close_above_78
    - hold_above_resistance
  invalidation_level: 504.80
```

### 10.4 Alpaca safety gates

Before sending any paper-trade order, require:

```text
1. Setup state == ARM.
2. Side is defined.
3. Target is defined.
4. Invalidation is defined.
5. Target room is sufficient.
6. Duplicate setup is not already active.
7. Market session is valid.
8. Buying power / position sizing check passes.
9. Paper trading mode is enabled.
10. Order reason is logged with concept IDs.
```

### 10.5 Avoiding brittle automation

Do not encode early rules like:

```python
if price > level_78:
    buy()
```

Prefer staged evaluation:

```python
if setup.state == "WATCH":
    confirmation = confirmation_model.evaluate(price_action, setup)
    if confirmation.valid:
        setup.state = "CONFIRM"

if setup.state == "CONFIRM":
    if target_model.has_room(setup) and risk_model.has_invalidation(setup):
        setup.state = "ARM"

if setup.state == "ARM":
    if execution_model.entry_triggered(setup):
        paper_executor.submit_order(setup)
```

### 10.6 Logging requirements

Every order candidate should log the concept chain:

```yaml
order_candidate_log:
  symbol: SPY
  side: bullish
  lifecycle_state: ARM
  reason_chain:
    - daily_direction_bullish
    - current_range_bullish
    - resistance_broke
    - 78_confirmed
    - target_active_previous_high
    - room_to_target_acceptable
    - invalidation_defined_below_support
  rejected_reasons: []
```

Rejected trades should also be logged:

```yaml
rejected_setup_log:
  symbol: SPY
  rejected_at_state: CONFIRM
  reason:
    - target_too_close
    - higher_timeframe_resistance_directly_overhead
    - no_clear_invalidation
```

---

## 11. Master Concept Relationship Map

```text
Timeframe Context
  produces:
    - allowed bias
    - major support/resistance
    - major target candidates
    - conflict warnings

Market Structure
  depends on:
    - swing highs/lows
    - higher lows/lower highs
    - breaks/rejections
    - range orientation
  produces:
    - bullish/bearish/neutral direction
    - transition state

Current Range
  depends on:
    - meaningful high/low anchors
    - current active movement
  produces:
    - support
    - resistance
    - 50/61 sweet spot
    - 78 decision level
    - 1.0 target
    - zero boundary/target

Support/Resistance
  depends on:
    - current range
    - bigger range
    - tighter range
    - candle/order levels
    - prior highs/lows
  produces:
    - reaction zones
    - break/retest candidates
    - invalidation candidates
    - target ladders

Target
  depends on:
    - range endpoint
    - prior high/low
    - support/resistance ladder
    - higher timeframe context
  produces:
    - trade objective
    - room-to-target calculation
    - play completion condition

Confirmation
  depends on:
    - price behavior at levels
    - close/break/hold/retest/rejection
    - 78 behavior
  produces:
    - stronger or weaker setup confidence
    - possible lifecycle transition from WATCH to CONFIRM

Entry
  depends on:
    - direction
    - target
    - confirmation
    - support/resistance context
    - target room
    - invalidation
  produces:
    - armed trade setup
    - possible order candidate

Invalidation/Risk
  depends on:
    - failed support/resistance behavior
    - failed 78 behavior
    - target room
    - higher timeframe conflict
  produces:
    - no-trade condition
    - exit/retire condition
    - quality score reduction

Trade Lifecycle
  coordinates:
    - all concept models
    - no-entry guardrails
    - completion/invalidation logic
    - Alpaca execution readiness
```

---

## 12. Rule Extraction Readiness Checklist

A relationship is ready to become a rule candidate only when these are defined:

```text
[ ] What concept does the rule depend on?
[ ] What timeframe does it apply to?
[ ] What is the required context?
[ ] What confirms it?
[ ] What invalidates it?
[ ] What target does it activate?
[ ] What would make it no-trade?
[ ] Is it for analysis, alerting, or order execution?
[ ] Can it be tested against examples/transcripts/JPEG snapshots?
[ ] Can it be logged as a reason chain?
```

---

## 13. Open Questions for Phase 3

These should be resolved before hard-coded rules or Alpaca execution logic:

1. Exact method for choosing candle body, middle, or wick in no-fib levels.
2. Exact criteria for when a foundation range is too wide and needs refinement.
3. Exact criteria for same-candle range selection.
4. Whether 78 confirmation requires wick break, candle close, retest, or hold by timeframe.
5. How much room to target is enough for scalps versus swings.
6. How to standardize fib orientation so 0/1.0 labels remain semantic instead of tool-dependent.
7. How to represent options-specific entries versus shares in the same lifecycle.
8. What position sizing and maximum risk rules should be applied before Alpaca integration.
9. How to backtest subjective candle/order levels without overfitting.
10. Which examples should become the canonical training/test set for OpenClaw.

---

## 14. Recommended Phase 3 Output

Phase 3 should not yet be “fully automated trading.” The next deliverable should be:

```text
PHASE_3_RULE_CANDIDATES.md
```

It should convert this concept model into candidate rules such as:

```text
Rule Candidate: 78 Confirmation Candidate
Context: Active current range exists.
Trigger: Price closes beyond 78 level.
Required filters: direction agreement, target active, room to target, S/R context.
Invalidation: price reclaims/fails the level or target already hit.
Execution status: alert/watch only until validated by examples.
```

