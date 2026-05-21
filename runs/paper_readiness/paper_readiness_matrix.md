# Paper Readiness Matrix

| candidate_id | replay_id | symbol | side | replay_status | replay_outcome | classification | manual_review_status | target_hit_after_confirmation | invalidation_hit_after_confirmation | readiness_status | broker_action_allowed | blocking_reason | next_action |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PTC-001 | HR-001 | AAPL | bullish | VERIFIED | insufficient | watch_no_trigger | pending | false | false | BLOCKED_BY_NO_TRIGGER | false | watch/no-trigger replay does not qualify for paper review | watch/no-trigger; do not promote |
| PTC-002 | HR-002 | SPY | bullish | VERIFIED | insufficient | watch_no_trigger | pending | false | false | BLOCKED_BY_NO_TRIGGER | false | watch/no-trigger replay does not qualify for paper review | watch/no-trigger; do not promote |
| PTC-003 | HR-003 | NVDA | bullish | VERIFIED | insufficient | insufficient | pending | false | false | BLOCKED_BY_INSUFFICIENT_DATA | false | insufficient replay evidence | collect verified replay evidence and complete manual review |
| PTC-004 | HR-004 | NVDA | bullish | VERIFIED | confirmed | confirmed_breakout | completed | true | false | READY_FOR_PAPER_REVIEW | false | none | paper review eligible; keep broker_action_allowed false |
| PTC-005 | HR-005 | AVGO | bullish | VERIFIED | confirmed | confirmed_breakout | completed | true | false | READY_FOR_PAPER_REVIEW | false | none | paper review eligible; keep broker_action_allowed false |
| PTC-006 | HR-006 | MSFT | bullish | VERIFIED | insufficient | confirmed_breakout_no_target_hit | completed | false | false | BLOCKED_BY_TARGET_NOT_HIT | false | target was not hit after confirmation | wait for target to be hit after confirmation |
| PTC-008 | HR-008 | AVGO | bearish | CONTRADICTED | contradicted | failed_breakdown_reclaim | completed | false | true | BLOCKED_BY_FAILED_RECLAIM | false | failed/reclaim evidence blocks paper review | do not promote; failed/reclaim evidence blocks paper review |
| PTC-009 | HR-009 | IWM | bearish | VERIFIED | confirmed | confirmed_breakdown | completed | true | false | READY_FOR_PAPER_REVIEW | false | none | paper review eligible; keep broker_action_allowed false |
| PTC-016 | HR-016 | META | bullish | VERIFIED | ambiguous | ambiguous | completed | false | false | BLOCKED_BY_AMBIGUITY | false | classification is ambiguous | resolve the ambiguous replay outcome manually |
| PTC-017 | HR-017 | SPY | bullish | VERIFIED | confirmed | confirmed_breakout | completed | true | false | READY_FOR_PAPER_REVIEW | false | none | paper review eligible; keep broker_action_allowed false |
| PTC-018 | HR-018 | META | bearish | VERIFIED | contradicted | failed_breakdown_reclaim | completed | false | true | BLOCKED_BY_FAILED_RECLAIM | false | failed/reclaim evidence blocks paper review | do not promote; failed/reclaim evidence blocks paper review |
| PTC-019 | HR-019 | SPY | bearish | VERIFIED | confirmed | confirmed_breakdown | completed | true | false | READY_FOR_PAPER_REVIEW | false | none | paper review eligible; keep broker_action_allowed false |

## Boundary
- No broker action allowed
- No Alpaca order submission
- No paper orders
