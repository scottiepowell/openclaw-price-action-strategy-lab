from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from monster_strategy_lab.paper.candidate import PaperTradeCandidate
from monster_strategy_lab.replay import load_replay_case, replay_case_verification_result


SCHEMA_OK = "PASS"
SCHEMA_FAIL = "FAIL"
EVIDENCE_PASS = "PASS"
EVIDENCE_INCOMPLETE = "INCOMPLETE"
EVIDENCE_BLOCKED = "BLOCKED"
REPLAY_VERIFIED = "VERIFIED"
REPLAY_VERIFIED_FIXTURE_ONLY = "VERIFIED_FIXTURE_ONLY"
REPLAY_NOT_VERIFIED = "NOT_VERIFIED"
REPLAY_MISSING = "MISSING"
REPLAY_BLOCKED = "BLOCKED"
REPLAY_AMBIGUOUS = "AMBIGUOUS"
REPLAY_CONTRADICTED = "CONTRADICTED"
STRATEGY_PASS = "PASS"
STRATEGY_INCOMPLETE = "INCOMPLETE"
STRATEGY_BLOCKED = "BLOCKED"
READY_FOR_DRY_RUN = "READY_FOR_DRY_RUN"
READY_FOR_PAPER_REVIEW = "READY_FOR_PAPER_REVIEW"
NOT_READY_FOR_ORDER_SUBMISSION = "NOT_READY_FOR_ORDER_SUBMISSION"
READY_STATUS_BLOCKED = "BLOCKED"
UNVERIFIED_MARKERS = {"not documented", "unknown", "tbd", "unverified", "placeholder", "missing"}


@dataclass(frozen=True)
class DryRunValidationResult:
    generated_at: str
    candidate_id: str
    symbol: str
    direction: str
    schema_status: str
    evidence_status: str
    replay_status: str
    strategy_logic_status: str
    paper_readiness_status: str
    broker_action_allowed: bool
    blocking_reasons: list[str]
    warnings: list[str]
    next_actions: list[str]
    required_levels: dict[str, Any]
    confirmation: dict[str, Any]
    context_checks: dict[str, Any]
    evidence_mapping: list[dict[str, Any]]
    replay_mapping: list[dict[str, Any]]


def _has_content(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, tuple, set)):
        return any(_has_content(item) for item in value)
    if isinstance(value, dict):
        return any(_has_content(item) for item in value.values())
    return True


def _clean_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def _looks_unverified(text: str) -> bool:
    lowered = text.lower()
    return any(marker in lowered for marker in UNVERIFIED_MARKERS)


def _missing_required_fields(candidate: PaperTradeCandidate) -> list[str]:
    required = {
        "candidate_id": candidate.candidate_id,
        "symbol": candidate.symbol,
        "direction": candidate.direction,
        "related_phase_3_1_rule_candidate": candidate.related_phase_3_1_rule_candidate,
        "evidence_links": candidate.evidence_links,
        "replay_case_links": candidate.replay_case_links,
        "timeframe_context": candidate.timeframe_context,
        "setup_timeframe": candidate.setup_timeframe,
        "execution_timeframe": candidate.execution_timeframe,
        "support_level": candidate.support_level,
        "resistance_level": candidate.resistance_level,
        "target_price": candidate.target_price,
        "entry_candidate_price": candidate.entry_candidate_price,
        "room_to_target": candidate.room_to_target,
        "invalidation_level": candidate.invalidation_level,
        "confirmation_behavior": candidate.confirmation_behavior,
        "confirmation_type": candidate.confirmation_type,
        "higher_timeframe_context": candidate.higher_timeframe_context,
        "higher_timeframe_obstacle_check": candidate.higher_timeframe_obstacle_check,
        "target_already_hit_check": candidate.target_already_hit_check,
        "no_trade_filters": candidate.no_trade_filters,
        "risk_notes": candidate.risk_notes,
        "boundary": candidate.boundary,
    }
    return [name for name, value in required.items() if not _has_content(value)]


def _supports_direction_model_only(text: str) -> bool:
    lowered = text.lower()
    return "direction-model" in lowered or "direction_model" in lowered or "direction model" in lowered


def _candidate_replay_case_paths(candidate: PaperTradeCandidate, repo_root: Path | None = None) -> list[Path]:
    paths: list[Path] = []
    base = repo_root or Path.cwd()
    for item in candidate.replay_case_links:
        raw = _clean_text(item.replay_case)
        if not raw:
            continue
        path = Path(raw)
        if not path.is_absolute():
            path = base / path
        paths.append(path)
    return paths


def _next_actions_for_not_verified() -> list[str]:
    return [
        "verify the historical data file paths for HR-001",
        "run data quality checks",
        "label support/resistance/target/invalidation",
        "verify close_above_resistance behavior",
        "check higher timeframe obstacle",
        "check whether target was already hit",
    ]


def _next_actions_from_replay_mapping(mapping: dict[str, Any]) -> list[str]:
    notes = " ".join(
        [
            f"replay_outcome: {mapping.get('replay_outcome', '')}",
            f"classification: {mapping.get('classification', '')}",
            f"notes: {mapping.get('notes', '')}",
            f"evidence_type: {mapping.get('evidence_type', '')}",
        ]
    )
    blockers = []
    if "data_files missing" in notes or "date_window missing" in notes:
        blockers.extend([
            "verify the historical data file paths for HR-001",
            "select a shared date window present in the files",
            "run data quality checks",
        ])
    if "labels missing" in notes:
        blockers.extend([
            "label support/resistance/target/invalidation",
            "verify close_above_resistance behavior",
            "check higher timeframe obstacle",
            "check whether target was already hit",
        ])
    if "replay_status is NOT_VERIFIED" in notes or "real market replay not ready" in notes:
        blockers.extend([
            "confirm the replay outcome from the inspected AAPL window",
            "promote HR-001 to VERIFIED only after the replay review is complete",
        ])
    if "manual review notes: close_above_resistance not confirmed" in notes or "manual review notes: target not reached during replay window" in notes:
        blockers.extend([
            "treat HR-001 as watch/no-trigger only",
            "do not promote HR-001 to paper review",
        ])
    if "classification: confirmed_breakout" in notes:
        blockers.append("confirmed_breakout replay still requires all other gates to pass")
    if "classification: confirmed_breakdown" in notes:
        blockers.append("confirmed_breakdown replay still requires all other gates to pass")
    if "classification: failed_breakout" in notes:
        blockers.append("failed_breakout blocks long breakout candidate promotion")
    if "classification: failed_breakdown_reclaim" in notes:
        blockers.append("failed_breakdown_reclaim blocks short breakdown candidate promotion")
    if "classification: ambiguous" in notes:
        blockers.append("ambiguous replay blocks paper review")
    if "classification: contradicted" in notes:
        blockers.append("contradicted replay blocks paper review")
    if "classification: blocked_data_quality" in notes:
        blockers.append("blocked data quality must be fixed before review")
    if "classification: confirmed_breakout_no_target_hit" in notes:
        blockers.append("confirmed_breakout_no_target_hit still needs target logic review")
    if "classification: confirmed_breakdown_no_target_hit" in notes:
        blockers.append("confirmed_breakdown_no_target_hit still needs target logic review")
    if "classification: support_touch_no_trigger" in notes:
        blockers.append("support_touch_no_trigger stays watch-only")
    if "real_market_evidence is false" in notes:
        blockers.append("set real_market_evidence true only for inspected market data")
    if "data_quality_status not passed" in notes:
        blockers.append("fix the OHLCV data quality issues before retrying")
    return blockers or _next_actions_for_not_verified()


def _verify_replay_cases(candidate: PaperTradeCandidate, repo_root: Path | None = None) -> tuple[str, list[str], list[dict[str, Any]], list[str]]:
    if not candidate.replay_case_links:
        return REPLAY_MISSING, ["no replay case links provided"], [], _next_actions_for_not_verified()

    replay_status = REPLAY_MISSING
    blocking_reasons: list[str] = []
    replay_mapping: list[dict[str, Any]] = []
    next_actions: list[str] = []

    for item, path in zip(candidate.replay_case_links, _candidate_replay_case_paths(candidate, repo_root)):
        if not path.exists():
            replay_status = REPLAY_MISSING
            replay_mapping.append(
                {
                    "replay_case": item.replay_case,
                    "replay_status": REPLAY_MISSING,
                    "replay_outcome": "missing",
                    "notes": "replay file not found",
                }
            )
            blocking_reasons.append(f"replay case missing: {item.replay_case}")
            next_actions = _next_actions_for_not_verified()
            continue

        case = load_replay_case(path)
        verification = replay_case_verification_result(case)
        symbol_mismatch = case.symbol.strip().upper() != candidate.symbol.strip().upper()
        candidate_mismatch = _clean_text(case.related_candidate_id) and _clean_text(case.related_candidate_id) != candidate.candidate_id
        if symbol_mismatch or candidate_mismatch:
            verification = type(verification)(
                replay_status=REPLAY_BLOCKED,
                verified=False,
                fixture_only=verification.fixture_only,
                blocking_reasons=verification.blocking_reasons
                + ([f"replay case symbol mismatch: {case.symbol} != {candidate.symbol}"] if symbol_mismatch else [])
                + ([f"replay case related_candidate_id mismatch: {case.related_candidate_id} != {candidate.candidate_id}"] if candidate_mismatch else []),
            )
        replay_mapping.append(
            {
                "replay_case": item.replay_case,
                "replay_status": verification.replay_status,
                "replay_outcome": case.replay_outcome or "insufficient",
                "classification": case.classification or "insufficient",
                "data_quality_status": case.data_quality_status or "UNKNOWN",
                "notes": f"{case.symbol} | {case.date_window} | {'; '.join(verification.blocking_reasons) or 'ok'}",
                "evidence_type": case.evidence_type,
                "real_market_evidence": case.real_market_evidence,
                "related_candidate_id": case.related_candidate_id,
            }
        )

        if verification.replay_status == REPLAY_VERIFIED_FIXTURE_ONLY:
            replay_status = REPLAY_VERIFIED_FIXTURE_ONLY
            continue
        if verification.replay_status == REPLAY_VERIFIED:
            replay_status = REPLAY_VERIFIED
            continue
        if verification.replay_status == REPLAY_BLOCKED:
            replay_status = REPLAY_BLOCKED
            blocking_reasons.extend(verification.blocking_reasons)
            continue
        if verification.replay_status == REPLAY_AMBIGUOUS:
            replay_status = REPLAY_AMBIGUOUS
            blocking_reasons.extend(verification.blocking_reasons)
            continue
        if verification.replay_status == REPLAY_CONTRADICTED:
            replay_status = REPLAY_CONTRADICTED
            blocking_reasons.extend(verification.blocking_reasons)
            continue

        replay_status = REPLAY_NOT_VERIFIED
        blocking_reasons.extend(verification.blocking_reasons or [f"replay case not verified: {case.replay_id}"])
        next_actions = _next_actions_from_replay_mapping(replay_mapping[-1])

    return replay_status, blocking_reasons, replay_mapping, next_actions


def validate_candidate(candidate: PaperTradeCandidate, repo_root: Path | None = None) -> DryRunValidationResult:
    missing_fields = _missing_required_fields(candidate)
    schema_status = SCHEMA_OK if candidate.schema == "paper_trade_candidate_v1" and not missing_fields else SCHEMA_FAIL

    warnings: list[str] = []
    blocking_reasons: list[str] = []

    evidence_status = EVIDENCE_PASS
    if not candidate.evidence_links:
        evidence_status = EVIDENCE_INCOMPLETE
        blocking_reasons.append("no evidence links provided")
    else:
        for item in candidate.evidence_links:
            if not _clean_text(item.link):
                evidence_status = EVIDENCE_INCOMPLETE
                blocking_reasons.append("evidence link missing")
            if not _clean_text(item.supports):
                evidence_status = EVIDENCE_INCOMPLETE
                blocking_reasons.append(f"evidence mapping missing for {item.link}")
            if _clean_text(item.supports).lower() in {"blocked", "contradiction", "contradictory"}:
                evidence_status = EVIDENCE_BLOCKED
                blocking_reasons.append(f"evidence blocks candidate: {item.link}")
            if item.link == "EX-001" and candidate.symbol.upper() == "AAPL" and candidate.direction == "long" and not _supports_direction_model_only(item.supports):
                warnings.append("EX-001 should be mapped as direction-model evidence only for this long AAPL candidate")

    if evidence_status == EVIDENCE_PASS and candidate.evidence_links:
        if any(_clean_text(item.supports).lower() == "legacy-unmapped" for item in candidate.evidence_links):
            evidence_status = EVIDENCE_INCOMPLETE
            blocking_reasons.append("legacy evidence links are not mapped to what they support")

    replay_status, replay_blocking_reasons, replay_mapping, next_actions = _verify_replay_cases(candidate, repo_root)
    blocking_reasons.extend(replay_blocking_reasons)

    strategy_logic_status = STRATEGY_PASS
    if any(not _has_content(level) for level in [candidate.support_level, candidate.resistance_level, candidate.target_price, candidate.invalidation_level]):
        strategy_logic_status = STRATEGY_INCOMPLETE
        blocking_reasons.append("missing support, resistance, target, or invalidation level")
    if not _has_content(candidate.room_to_target):
        strategy_logic_status = STRATEGY_INCOMPLETE
        blocking_reasons.append("room_to_target is missing")
    if not _has_content(candidate.confirmation_type) or _clean_text(candidate.confirmation_type).lower() in {"free_text", "free text", "text", "free-text"}:
        strategy_logic_status = STRATEGY_INCOMPLETE
        blocking_reasons.append("confirmation_type is not concrete enough")
    if not _has_content(candidate.timeframe_context) or not _has_content(candidate.setup_timeframe) or not _has_content(candidate.execution_timeframe):
        strategy_logic_status = STRATEGY_INCOMPLETE
        blocking_reasons.append("timeframe context is incomplete")
    if not _has_content(candidate.higher_timeframe_context) or not _has_content(candidate.higher_timeframe_obstacle_check):
        strategy_logic_status = STRATEGY_INCOMPLETE
        blocking_reasons.append("higher timeframe context or obstacle check is missing")
    if not _has_content(candidate.target_already_hit_check):
        strategy_logic_status = STRATEGY_INCOMPLETE
        blocking_reasons.append("target already hit check is missing")

    if _looks_unverified(candidate.higher_timeframe_obstacle_check):
        warnings.append("higher_timeframe_obstacle_check is not verified")
    if _looks_unverified(candidate.target_already_hit_check):
        warnings.append("target_already_hit_check is not verified")

    for item in candidate.no_trade_filters:
        status = _clean_text(item.status).lower()
        note = _clean_text(item.note)
        if status in {"blocked", "block", "fail"}:
            strategy_logic_status = STRATEGY_BLOCKED
            blocking_reasons.append(f"{item.id}: {status}" + (f" — {note}" if note else ""))
        elif status in {"warn", "warning", "advisory"}:
            warnings.append(f"{item.id}: {status}" + (f" — {note}" if note else ""))
        elif status and status not in {"pass", "ok", "clear"}:
            warnings.append(f"{item.id}: unknown status '{item.status}'" + (f" — {note}" if note else ""))

    if schema_status == SCHEMA_FAIL and missing_fields:
        blocking_reasons.extend(f"missing {field}" for field in missing_fields)

    if evidence_status == EVIDENCE_BLOCKED or replay_status in {REPLAY_BLOCKED, REPLAY_CONTRADICTED, REPLAY_AMBIGUOUS}:
        paper_readiness_status = READY_STATUS_BLOCKED
    else:
        replay_classifications = {str(item.get("classification", "")).lower() for item in replay_mapping if item.get("classification")}
        replay_data_quality_pass = all(str(item.get("data_quality_status", "")).upper() == "PASSED" for item in replay_mapping) if replay_mapping else False
        replay_real_market_evidence = all(bool(item.get("real_market_evidence", False)) for item in replay_mapping) if replay_mapping else False

        if any(classification in {"ambiguous", "contradicted", "blocked_data_quality"} for classification in replay_classifications):
            paper_readiness_status = READY_STATUS_BLOCKED
        elif any(classification == "failed_breakout" for classification in replay_classifications):
            paper_readiness_status = READY_STATUS_BLOCKED
        elif (
            replay_status == REPLAY_VERIFIED
            and evidence_status == EVIDENCE_PASS
            and strategy_logic_status == STRATEGY_PASS
            and replay_real_market_evidence
            and replay_data_quality_pass
            and any(classification == "confirmed_breakout" for classification in replay_classifications)
        ):
            paper_readiness_status = READY_FOR_PAPER_REVIEW
        elif any(classification in {"watch_no_trigger", "insufficient"} for classification in replay_classifications):
            paper_readiness_status = READY_FOR_DRY_RUN
        elif replay_status in {REPLAY_VERIFIED_FIXTURE_ONLY, REPLAY_NOT_VERIFIED}:
            paper_readiness_status = READY_FOR_DRY_RUN
        elif schema_status == SCHEMA_OK:
            paper_readiness_status = READY_FOR_DRY_RUN
        else:
            paper_readiness_status = NOT_READY_FOR_ORDER_SUBMISSION

    if replay_status == REPLAY_VERIFIED_FIXTURE_ONLY:
        warnings.append("replay_status is VERIFIED_FIXTURE_ONLY; synthetic fixture cannot advance paper review")
    if replay_status == REPLAY_VERIFIED and any(not item.get("real_market_evidence", False) for item in replay_mapping):
        blocking_reasons.append("real_market_evidence is false")
        paper_readiness_status = READY_FOR_DRY_RUN
    if replay_status == REPLAY_VERIFIED and any(item.get("evidence_type") == "synthetic_fixture" for item in replay_mapping):
        replay_status = REPLAY_VERIFIED_FIXTURE_ONLY
        paper_readiness_status = READY_FOR_DRY_RUN

    required_levels = {
        "support_level": candidate.support_level,
        "resistance_level": candidate.resistance_level,
        "target_price": candidate.target_price,
        "entry_candidate_price": candidate.entry_candidate_price,
        "invalidation_level": candidate.invalidation_level,
        "room_to_target": candidate.room_to_target,
    }
    confirmation = {
        "confirmation_type": candidate.confirmation_type,
        "confirmation_behavior": candidate.confirmation_behavior,
    }
    context_checks = {
        "timeframe_context": candidate.timeframe_context,
        "higher_timeframe_context": candidate.higher_timeframe_context,
        "higher_timeframe_obstacle_check": candidate.higher_timeframe_obstacle_check,
        "target_already_hit_check": candidate.target_already_hit_check,
    }
    evidence_mapping = [
        {"evidence_link": item.link, "supports": item.supports, "notes": item.notes or ""}
        for item in candidate.evidence_links
    ]

    return DryRunValidationResult(
        generated_at=datetime.now(timezone.utc).isoformat(),
        candidate_id=candidate.candidate_id,
        symbol=candidate.symbol,
        direction=candidate.direction,
        schema_status=schema_status,
        evidence_status=evidence_status,
        replay_status=replay_status,
        strategy_logic_status=strategy_logic_status,
        paper_readiness_status=paper_readiness_status,
        broker_action_allowed=False,
        blocking_reasons=blocking_reasons,
        warnings=warnings,
        next_actions=next_actions,
        required_levels=required_levels,
        confirmation=confirmation,
        context_checks=context_checks,
        evidence_mapping=evidence_mapping,
        replay_mapping=replay_mapping,
    )


def render_dry_run_report(candidate: PaperTradeCandidate, result: DryRunValidationResult) -> str:
    lines = [
        "# Dry Run Report",
        "",
        f"generated_at: {result.generated_at}",
        f"candidate_id: {result.candidate_id}",
        f"symbol: {result.symbol}",
        f"direction: {result.direction}",
        "",
        f"schema_status: {result.schema_status}",
        f"evidence_status: {result.evidence_status}",
        f"replay_status: {result.replay_status}",
        f"strategy_logic_status: {result.strategy_logic_status}",
        f"paper_readiness_status: {result.paper_readiness_status}",
        f"broker_action_allowed: {str(result.broker_action_allowed).lower()}",
        "",
        "## Blocking reasons",
    ]
    if result.blocking_reasons:
        lines.extend(f"- {reason}" for reason in result.blocking_reasons)
    else:
        lines.append("- none")

    lines.extend(["", "## Warnings"])
    if result.warnings:
        lines.extend(f"- {warning}" for warning in result.warnings)
    else:
        lines.append("- none")

    lines.extend(
        [
            "",
            "## Next actions",
        ]
    )
    if result.next_actions:
        lines.extend(f"- {action}" for action in result.next_actions)
    else:
        lines.append("- none")

    lines.extend(
        [
            "",
            "## Required levels",
            f"- support_level: {result.required_levels['support_level']}",
            f"- resistance_level: {result.required_levels['resistance_level']}",
            f"- target_price: {result.required_levels['target_price']}",
            f"- entry_candidate_price: {result.required_levels['entry_candidate_price']}",
            f"- invalidation_level: {result.required_levels['invalidation_level']}",
            f"- room_to_target: {result.required_levels['room_to_target']}",
            "",
            "## Confirmation",
            f"- confirmation_type: {result.confirmation['confirmation_type']}",
            f"- confirmation_behavior: {result.confirmation['confirmation_behavior']}",
            "",
            "## Context checks",
            f"- timeframe_context: {result.context_checks['timeframe_context']}",
            f"- higher_timeframe_context: {result.context_checks['higher_timeframe_context']}",
            f"- higher_timeframe_obstacle_check: {result.context_checks['higher_timeframe_obstacle_check']}",
            f"- target_already_hit_check: {result.context_checks['target_already_hit_check']}",
            "",
            "## Evidence mapping",
        ]
    )
    if result.evidence_mapping:
        for item in result.evidence_mapping:
            lines.extend(
                [
                    f"- evidence_link: {item['evidence_link']}",
                    f"  supports: {item['supports']}",
                    f"  notes: {item['notes']}",
                ]
            )
    else:
        lines.append("- none")

    lines.extend(["", "## Replay mapping"])
    if result.replay_mapping:
        for item in result.replay_mapping:
            lines.extend(
                [
                    f"- replay_case: {item['replay_case']}",
                    f"  replay_status: {item['replay_status']}",
                    f"  replay_outcome: {item['replay_outcome']}",
                    f"  classification: {item.get('classification', '')}",
                    f"  notes: {item['notes']}",
                    f"  evidence_type: {item.get('evidence_type', '')}",
                    f"  real_market_evidence: {str(item.get('real_market_evidence', False)).lower()}",
                ]
            )
    else:
        lines.append("- none")

    lines.extend(
        [
            "",
            "## Boundary",
            "- Dry-run only",
            "- No live-trade implication",
            "- No Alpaca order submission",
            "- No broker action allowed",
        ]
    )
    return "\n".join(lines)


def write_dry_run_report(repo_root: Path, candidate: PaperTradeCandidate, result: DryRunValidationResult) -> Path:
    output_dir = repo_root / "runs" / "dry_run"
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / f"{candidate.candidate_id}-dry-run-report.md"
    report_path.write_text(render_dry_run_report(candidate, result))
    return report_path
