from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


ALLOWED_REPLAY_STATUSES = {
    "VERIFIED",
    "VERIFIED_FIXTURE_ONLY",
    "NOT_VERIFIED",
    "BLOCKED",
    "AMBIGUOUS",
    "CONTRADICTED",
    "MISSING",
}
ALLOWED_REPLAY_OUTCOMES = {
    "confirmed",
    "contradicted",
    "ambiguous",
    "insufficient",
    "placeholder",
}
ALLOWED_REPLAY_CLASSIFICATIONS = {
    "candidate_for_manual_review",
    "confirmed_breakout",
    "confirmed_breakout_no_target_hit",
    "confirmed_breakdown",
    "confirmed_breakdown_no_target_hit",
    "failed_breakout",
    "failed_breakdown_reclaim",
    "watch_no_trigger",
    "support_touch_no_trigger",
    "ambiguous",
    "insufficient",
    "contradicted",
    "blocked_data_quality",
}
ALLOWED_EVIDENCE_TYPES = {
    "real_market_replay",
    "synthetic_fixture",
    "template",
    "placeholder",
}
REQUIRED_LABELS = {"range", "support", "resistance", "target", "break_behavior", "invalidation"}


@dataclass(frozen=True)
class ReplayCase:
    replay_id: str
    symbol: str
    timeframe_stack: str
    date_window: str
    data_files: list[str]
    data_quality_status: str
    related_candidate_id: str
    related_examples: list[str]
    labels_present: list[str]
    replay_observations: list[str]
    classification: str
    replay_outcome: str
    replay_status: str
    manual_review_status: str
    manual_review_outcome: str
    manual_review_classification: str
    manual_reviewer_notes: str
    broker_action_allowed: bool
    evidence_type: str
    real_market_evidence: bool
    reviewer: str
    boundary: str
    raw: dict[str, Any]


@dataclass(frozen=True)
class ReplayVerificationResult:
    replay_status: str
    verified: bool
    fixture_only: bool
    blocking_reasons: list[str]


def _as_str(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        stripped = value.strip()
        return [stripped] if stripped else []
    return [str(value).strip()]


def _as_bool(value: Any, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"true", "yes", "1", "y"}:
            return True
        if normalized in {"false", "no", "0", "n"}:
            return False
    return bool(value)


def _manual_review_reasons(observations: list[str]) -> list[str]:
    text = " ".join(observations).lower()
    reasons: list[str] = []
    if "close_above_resistance not confirmed" in text:
        reasons.append("manual review notes: close_above_resistance not confirmed")
    if "target not reached" in text:
        reasons.append("manual review notes: target not reached during replay window")
    if "watch/no-trigger" in text or "watch only" in text:
        reasons.append("manual review notes: watch/no-trigger only")
    return reasons


def _load_frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text()
    if not text.startswith("---\n"):
        raise ValueError(f"Replay case {path} is missing YAML frontmatter")
    _, rest = text.split("---\n", 1)
    frontmatter, _, _ = rest.partition("\n---\n")
    if not frontmatter.strip():
        raise ValueError(f"Replay case {path} has empty YAML frontmatter")
    data = yaml.safe_load(frontmatter)
    if not isinstance(data, dict):
        raise ValueError(f"Replay case {path} frontmatter is not a mapping")
    return data


def load_replay_case_data(path: Path) -> dict[str, Any]:
    return _load_frontmatter(path)


def parse_replay_case(data: dict[str, Any]) -> ReplayCase:
    evidence_type = _as_str(data.get("evidence_type")).lower() or "placeholder"
    real_market_evidence = _as_bool(data.get("real_market_evidence"), False)
    classification = _as_str(data.get("classification")).lower() or "insufficient"
    return ReplayCase(
        replay_id=_as_str(data.get("replay_id")),
        symbol=_as_str(data.get("symbol")),
        timeframe_stack=_as_str(data.get("timeframe_stack")),
        date_window=_as_str(data.get("date_window")),
        data_files=_as_list(data.get("data_files")),
        data_quality_status=_as_str(data.get("data_quality_status")).upper(),
        related_candidate_id=_as_str(data.get("related_candidate_id")),
        related_examples=_as_list(data.get("related_examples")),
        labels_present=_as_list(data.get("labels_present")),
        replay_observations=_as_list(data.get("replay_observations")),
        classification=classification,
        replay_outcome=_as_str(data.get("replay_outcome")).lower(),
        replay_status=_as_str(data.get("replay_status")).upper(),
        manual_review_status=_as_str(data.get("manual_review_status")).lower() or "pending",
        manual_review_outcome=_as_str(data.get("manual_review_outcome")).lower(),
        manual_review_classification=_as_str(data.get("manual_review_classification")).lower(),
        manual_reviewer_notes=_as_str(data.get("manual_reviewer_notes")),
        broker_action_allowed=_as_bool(data.get("broker_action_allowed"), False),
        evidence_type=evidence_type,
        real_market_evidence=real_market_evidence,
        reviewer=_as_str(data.get("reviewer")),
        boundary=_as_str(data.get("boundary")),
        raw=data,
    )


def load_replay_case(path: Path) -> ReplayCase:
    return parse_replay_case(load_replay_case_data(path))


def replay_case_verification_result(case: ReplayCase) -> ReplayVerificationResult:
    labels = {label.lower() for label in case.labels_present}
    missing_labels = REQUIRED_LABELS - labels
    blocking_reasons: list[str] = []

    if case.evidence_type not in ALLOWED_EVIDENCE_TYPES:
        return ReplayVerificationResult(
            replay_status="BLOCKED",
            verified=False,
            fixture_only=False,
            blocking_reasons=[f"unknown evidence_type: {case.evidence_type}"],
        )

    if case.evidence_type in {"template", "placeholder"}:
        return ReplayVerificationResult(
            replay_status="NOT_VERIFIED",
            verified=False,
            fixture_only=False,
            blocking_reasons=[f"{case.evidence_type} replay cannot be verified"],
        )

    if not case.date_window.strip():
        blocking_reasons.append("date_window missing")
    if not case.data_files:
        blocking_reasons.append("data_files missing")
    if case.data_quality_status != "PASSED":
        blocking_reasons.append(f"data_quality_status not passed: {case.data_quality_status or 'missing'}")
    if missing_labels:
        blocking_reasons.append(f"labels missing: {', '.join(sorted(missing_labels))}")
    if case.replay_outcome == "placeholder":
        blocking_reasons.append("replay_outcome is placeholder")
    if case.classification not in ALLOWED_REPLAY_CLASSIFICATIONS:
        blocking_reasons.append(f"classification invalid: {case.classification or 'missing'}")
    if case.replay_status not in ALLOWED_REPLAY_STATUSES:
        blocking_reasons.append(f"replay_status invalid: {case.replay_status or 'missing'}")
    if not case.reviewer.strip():
        blocking_reasons.append("reviewer missing")
    if not case.boundary.strip():
        blocking_reasons.append("boundary missing")

    if case.evidence_type == "synthetic_fixture":
        if case.real_market_evidence:
            return ReplayVerificationResult(
                replay_status="BLOCKED",
                verified=False,
                fixture_only=True,
                blocking_reasons=["synthetic fixture cannot claim real_market_evidence true"],
            )
        if case.replay_status == "VERIFIED" and case.replay_outcome == "confirmed" and not blocking_reasons:
            return ReplayVerificationResult(
                replay_status="VERIFIED_FIXTURE_ONLY",
                verified=True,
                fixture_only=True,
                blocking_reasons=[],
            )
        return ReplayVerificationResult(
            replay_status="NOT_VERIFIED",
            verified=False,
            fixture_only=True,
            blocking_reasons=blocking_reasons or ["synthetic fixture not ready"],
        )

    if case.evidence_type == "real_market_replay":
        if not case.real_market_evidence:
            blocking_reasons.append("real_market_evidence is false")
            return ReplayVerificationResult(
                replay_status="BLOCKED",
                verified=False,
                fixture_only=False,
                blocking_reasons=blocking_reasons,
            )
        blocking_reasons.extend(_manual_review_reasons(case.replay_observations))
        if case.replay_status == "VERIFIED" and case.replay_outcome == "confirmed" and not blocking_reasons:
            return ReplayVerificationResult(
                replay_status="VERIFIED",
                verified=True,
                fixture_only=False,
                blocking_reasons=[],
            )
        if case.replay_status == "NOT_VERIFIED":
            blocking_reasons.append("replay_status is NOT_VERIFIED")
        elif case.replay_status != "VERIFIED":
            blocking_reasons.append(f"replay_status not verified: {case.replay_status or 'missing'}")
        if case.replay_outcome and case.replay_outcome != "confirmed":
            blocking_reasons.append(f"replay_outcome not confirmed: {case.replay_outcome}")
        if case.replay_status in {"CONTRADICTED", "AMBIGUOUS"} or case.replay_outcome in {"contradicted", "ambiguous"}:
            return ReplayVerificationResult(
                replay_status=case.replay_status or "CONTRADICTED",
                verified=False,
                fixture_only=False,
                blocking_reasons=blocking_reasons or [f"replay outcome not ready: {case.replay_outcome or 'missing'}"],
            )
        return ReplayVerificationResult(
            replay_status="NOT_VERIFIED",
            verified=False,
            fixture_only=False,
            blocking_reasons=blocking_reasons or ["real market replay not ready"],
        )

    # fallback for unexpected branch
    return ReplayVerificationResult(
        replay_status="NOT_VERIFIED",
        verified=False,
        fixture_only=False,
        blocking_reasons=blocking_reasons or ["replay not ready"],
    )
