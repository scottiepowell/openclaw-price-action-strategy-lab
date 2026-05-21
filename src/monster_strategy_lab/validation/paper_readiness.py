from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable
import csv

from monster_strategy_lab.replay import load_replay_case


READY_FOR_DRY_RUN = "READY_FOR_DRY_RUN"
READY_FOR_PAPER_REVIEW = "READY_FOR_PAPER_REVIEW"
NOT_READY = "NOT_READY"
BLOCKED_BY_REPLAY = "BLOCKED_BY_REPLAY"
BLOCKED_BY_AMBIGUITY = "BLOCKED_BY_AMBIGUITY"
BLOCKED_BY_FAILED_RECLAIM = "BLOCKED_BY_FAILED_RECLAIM"
BLOCKED_BY_TARGET_NOT_HIT = "BLOCKED_BY_TARGET_NOT_HIT"
BLOCKED_BY_NO_TRIGGER = "BLOCKED_BY_NO_TRIGGER"
BLOCKED_BY_INSUFFICIENT_DATA = "BLOCKED_BY_INSUFFICIENT_DATA"


@dataclass(frozen=True)
class PaperReadinessResult:
    candidate_id: str
    replay_id: str
    symbol: str
    side: str
    replay_status: str
    replay_outcome: str
    classification: str
    manual_review_status: str
    target_hit_after_confirmation: bool
    invalidation_hit_after_confirmation: bool
    readiness_status: str
    broker_action_allowed: bool
    blocking_reason: str
    next_action: str
    replay_supported: bool
    eligible_for_paper_review: bool


def _side_from_direction(direction: str) -> str:
    return "bearish" if direction.strip().lower() == "short" else "bullish"


def _bool_text(value: bool) -> str:
    return "true" if value else "false"


def _event_flags(case) -> tuple[bool, bool]:
    classification = (case.manual_review_classification or case.classification or "").lower().strip()
    if classification in {"confirmed_breakout", "confirmed_breakdown"}:
        return True, False
    if classification in {"confirmed_breakout_no_target_hit", "confirmed_breakdown_no_target_hit", "watch_no_trigger", "support_touch_no_trigger", "insufficient"}:
        return False, False
    if classification in {"failed_breakout", "failed_breakdown_reclaim", "contradicted"}:
        return False, True
    if classification == "ambiguous":
        return False, False
    return False, False


def _next_action(status: str) -> str:
    return {
        READY_FOR_PAPER_REVIEW: "paper review eligible; keep broker_action_allowed false",
        READY_FOR_DRY_RUN: "keep as dry-run only; do not promote to paper review",
        BLOCKED_BY_AMBIGUITY: "resolve the ambiguous replay outcome manually",
        BLOCKED_BY_FAILED_RECLAIM: "do not promote; failed/reclaim evidence blocks paper review",
        BLOCKED_BY_TARGET_NOT_HIT: "wait for target to be hit after confirmation",
        BLOCKED_BY_NO_TRIGGER: "watch/no-trigger; do not promote",
        BLOCKED_BY_INSUFFICIENT_DATA: "collect verified replay evidence and complete manual review",
        BLOCKED_BY_REPLAY: "fix replay evidence issues before reassessing",
    }.get(status, "review manually")


def assess_replay_case(case) -> PaperReadinessResult:
    replay_supported = case.evidence_type == "real_market_replay" and case.real_market_evidence and case.replay_status.upper() == "VERIFIED"

    target_hit_after_confirmation, invalidation_hit_after_confirmation = _event_flags(case)
    classification = (case.manual_review_classification or case.classification or "").lower().strip()
    replay_status = case.replay_status.upper().strip() or verification.replay_status
    manual_review_status = case.manual_review_status.lower().strip() or "pending"
    direction = str(case.raw.get("direction", "")).strip().lower()
    broker_action_allowed = bool(case.raw.get("broker_action_allowed", False))

    blocking_reason = ""
    readiness_status = NOT_READY
    eligible_for_paper_review = False

    if case.evidence_type in {"synthetic_fixture", "placeholder"} or not case.real_market_evidence:
        readiness_status = BLOCKED_BY_INSUFFICIENT_DATA
        blocking_reason = "synthetic fixture or non-real-market evidence cannot advance to paper review"
    elif classification in {"watch_no_trigger", "support_touch_no_trigger"}:
        readiness_status = BLOCKED_BY_NO_TRIGGER
        blocking_reason = "watch/no-trigger replay does not qualify for paper review"
    elif classification == "ambiguous":
        readiness_status = BLOCKED_BY_AMBIGUITY
        blocking_reason = "classification is ambiguous"
    elif classification in {"failed_breakdown_reclaim", "failed_breakout_reclaim", "failed_breakout"}:
        readiness_status = BLOCKED_BY_FAILED_RECLAIM
        blocking_reason = "failed/reclaim evidence blocks paper review"
    elif classification in {"confirmed_breakout_no_target_hit", "confirmed_breakdown_no_target_hit"}:
        readiness_status = BLOCKED_BY_TARGET_NOT_HIT
        blocking_reason = "target was not hit after confirmation"
    elif classification in {"insufficient", "candidate_for_manual_review"}:
        readiness_status = BLOCKED_BY_INSUFFICIENT_DATA
        blocking_reason = "insufficient replay evidence"
    elif replay_status == "NOT_VERIFIED" or manual_review_status == "pending":
        readiness_status = BLOCKED_BY_INSUFFICIENT_DATA
        if replay_status == "NOT_VERIFIED":
            blocking_reason = "replay_status is NOT_VERIFIED"
        else:
            blocking_reason = "manual review is pending"
    elif (
        replay_status == "VERIFIED"
        and case.evidence_type == "real_market_replay"
        and case.real_market_evidence
        and manual_review_status == "completed"
        and case.replay_outcome == "confirmed"
        and classification in {"confirmed_breakout", "confirmed_breakdown"}
        and target_hit_after_confirmation
        and not invalidation_hit_after_confirmation
        and not broker_action_allowed
    ):
        readiness_status = READY_FOR_PAPER_REVIEW
        blocking_reason = "none"
        eligible_for_paper_review = True
    else:
        readiness_status = READY_FOR_DRY_RUN
        blocking_reason = "meets replay support but not paper-review criteria"

    return PaperReadinessResult(
        candidate_id=case.related_candidate_id,
        replay_id=case.replay_id,
        symbol=case.symbol,
        side=_side_from_direction(direction),
        replay_status=replay_status,
        replay_outcome=case.replay_outcome,
        classification=classification,
        manual_review_status=manual_review_status,
        target_hit_after_confirmation=target_hit_after_confirmation,
        invalidation_hit_after_confirmation=invalidation_hit_after_confirmation,
        readiness_status=readiness_status,
        broker_action_allowed=False,
        blocking_reason=blocking_reason,
        next_action=_next_action(readiness_status),
        replay_supported=replay_supported,
        eligible_for_paper_review=eligible_for_paper_review,
    )


def _rows_to_csv(rows: list[PaperReadinessResult]) -> str:
    fieldnames = [
        "candidate_id",
        "replay_id",
        "symbol",
        "side",
        "replay_status",
        "replay_outcome",
        "classification",
        "manual_review_status",
        "target_hit_after_confirmation",
        "invalidation_hit_after_confirmation",
        "readiness_status",
        "broker_action_allowed",
        "blocking_reason",
        "next_action",
    ]
    from io import StringIO

    buf = StringIO()
    writer = csv.DictWriter(buf, fieldnames=fieldnames)
    writer.writeheader()
    for row in rows:
        writer.writerow(
            {
                "candidate_id": row.candidate_id,
                "replay_id": row.replay_id,
                "symbol": row.symbol,
                "side": row.side,
                "replay_status": row.replay_status,
                "replay_outcome": row.replay_outcome,
                "classification": row.classification,
                "manual_review_status": row.manual_review_status,
                "target_hit_after_confirmation": _bool_text(row.target_hit_after_confirmation),
                "invalidation_hit_after_confirmation": _bool_text(row.invalidation_hit_after_confirmation),
                "readiness_status": row.readiness_status,
                "broker_action_allowed": _bool_text(row.broker_action_allowed),
                "blocking_reason": row.blocking_reason,
                "next_action": row.next_action,
            }
        )
    return buf.getvalue()


def render_paper_readiness_matrix(rows: list[PaperReadinessResult]) -> str:
    lines = [
        "# Paper Readiness Matrix",
        "",
        "| candidate_id | replay_id | symbol | side | replay_status | replay_outcome | classification | manual_review_status | target_hit_after_confirmation | invalidation_hit_after_confirmation | readiness_status | broker_action_allowed | blocking_reason | next_action |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            "| "
            f"{row.candidate_id} | {row.replay_id} | {row.symbol} | {row.side} | {row.replay_status} | {row.replay_outcome} | {row.classification} | {row.manual_review_status} | "
            f"{_bool_text(row.target_hit_after_confirmation)} | {_bool_text(row.invalidation_hit_after_confirmation)} | {row.readiness_status} | {_bool_text(row.broker_action_allowed)} | {row.blocking_reason} | {row.next_action} |"
        )
    lines.extend(["", "## Boundary", "- No broker action allowed", "- No Alpaca order submission", "- No paper orders"])
    return "\n".join(lines).rstrip() + "\n"


def write_paper_readiness_matrix(repo_root: Path, replay_case_paths: Iterable[Path]) -> tuple[Path, Path, list[PaperReadinessResult]]:
    rows = [assess_replay_case(load_replay_case(path)) for path in replay_case_paths]
    rows.sort(key=lambda row: row.candidate_id)
    output_dir = repo_root / "runs" / "paper_readiness"
    output_dir.mkdir(parents=True, exist_ok=True)
    md_path = output_dir / "paper_readiness_matrix.md"
    csv_path = output_dir / "paper_readiness_matrix.csv"
    md_path.write_text(render_paper_readiness_matrix(rows))
    csv_path.write_text(_rows_to_csv(rows))
    return md_path, csv_path, rows


def render_paper_readiness_report(result: PaperReadinessResult) -> str:
    lines = [
        f"# {result.candidate_id} Paper Readiness",
        "",
        f"- replay_id: {result.replay_id}",
        f"- symbol: {result.symbol}",
        f"- side: {result.side}",
        f"- replay_supported: {str(result.replay_supported).lower()}",
        f"- eligible_for_paper_review: {str(result.eligible_for_paper_review).lower()}",
        f"- readiness_status: {result.readiness_status}",
        f"- replay_status: {result.replay_status}",
        f"- replay_outcome: {result.replay_outcome}",
        f"- classification: {result.classification}",
        f"- manual_review_status: {result.manual_review_status}",
        f"- target_hit_after_confirmation: {str(result.target_hit_after_confirmation).lower()}",
        f"- invalidation_hit_after_confirmation: {str(result.invalidation_hit_after_confirmation).lower()}",
        f"- broker_action_allowed: {str(result.broker_action_allowed).lower()}",
        f"- blocking_reason: {result.blocking_reason}",
        f"- next_action: {result.next_action}",
        "",
        "## Summary",
        f"{result.candidate_id} is {'eligible' if result.eligible_for_paper_review else 'not eligible'} for paper review.",
        "",
        "## Evidence",
        f"- replay evidence support: {str(result.replay_supported).lower()}",
        f"- broker action allowed: false",
        "",
        "## Boundary",
        "- No broker action allowed",
        "- No Alpaca order submission",
        "- No live trading",
    ]
    return "\n".join(lines).rstrip() + "\n"


def write_paper_readiness_report(repo_root: Path, result: PaperReadinessResult) -> Path:
    output_dir = repo_root / "runs" / "paper_readiness"
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{result.candidate_id}-readiness.md"
    path.write_text(render_paper_readiness_report(result))
    return path
