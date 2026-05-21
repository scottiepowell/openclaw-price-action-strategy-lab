from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import json

import yaml


SCHEMA_NAME = "paper_trade_candidate_v1"


@dataclass(frozen=True)
class EvidenceLink:
    link: str
    supports: str = ""
    notes: str | None = None


@dataclass(frozen=True)
class ReplayCaseLink:
    replay_case: str
    replay_status: str = "NOT_VERIFIED"
    replay_outcome: str = ""
    notes: str | None = None


@dataclass(frozen=True)
class NoTradeFilter:
    id: str
    status: str = "pass"
    note: str | None = None


@dataclass(frozen=True)
class PaperTradeCandidate:
    candidate_id: str
    schema: str
    title: str | None
    related_phase_3_1_rule_candidate: str
    evidence_links: list[EvidenceLink]
    replay_case_links: list[ReplayCaseLink]
    related_evidence_examples: list[str]
    related_evidence_replay_cases: list[str]
    symbol: str
    direction: str
    timeframe_context: str
    setup_timeframe: str
    execution_timeframe: str
    support_level: Any
    resistance_level: Any
    target_price: Any
    entry_candidate_price: Any
    room_to_target: Any
    invalidation_level: Any
    confirmation_behavior: str
    confirmation_type: str
    higher_timeframe_context: str
    higher_timeframe_obstacle_check: str
    target_already_hit_check: str
    no_trade_filters: list[NoTradeFilter]
    risk_notes: str
    boundary: str
    raw: dict[str, Any]


def load_candidate_data(path: Path) -> dict[str, Any]:
    suffix = path.suffix.lower()
    text = path.read_text()
    if suffix == ".json":
        return json.loads(text)
    if suffix in {".yaml", ".yml"}:
        data = yaml.safe_load(text)
        return data or {}
    raise ValueError(f"Unsupported candidate file type: {path.suffix}")


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        stripped = value.strip()
        return [stripped] if stripped else []
    return [str(value).strip()]


def _as_str(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def _parse_no_trade_filters(data: Any) -> list[NoTradeFilter]:
    if not data:
        return []
    filters: list[NoTradeFilter] = []
    for item in data:
        if isinstance(item, dict):
            filters.append(
                NoTradeFilter(
                    id=_as_str(item.get("id")),
                    status=_as_str(item.get("status")) or "pass",
                    note=_as_str(item.get("note")) or None,
                )
            )
        else:
            filters.append(NoTradeFilter(id=_as_str(item), status="pass", note=None))
    return filters


def _parse_evidence_links(data: Any) -> list[EvidenceLink]:
    if not data:
        return []
    links: list[EvidenceLink] = []
    for item in data:
        if isinstance(item, dict):
            links.append(
                EvidenceLink(
                    link=_as_str(item.get("link")),
                    supports=_as_str(item.get("supports")),
                    notes=_as_str(item.get("notes")) or None,
                )
            )
        else:
            links.append(EvidenceLink(link=_as_str(item)))
    return links


def _parse_replay_case_links(data: Any) -> list[ReplayCaseLink]:
    if not data:
        return []
    links: list[ReplayCaseLink] = []
    for item in data:
        if isinstance(item, dict):
            links.append(
                ReplayCaseLink(
                    replay_case=_as_str(item.get("replay_case")),
                    replay_status=_as_str(item.get("replay_status")) or "NOT_VERIFIED",
                    replay_outcome=_as_str(item.get("replay_outcome")),
                    notes=_as_str(item.get("notes")) or None,
                )
            )
        else:
            links.append(ReplayCaseLink(replay_case=_as_str(item)))
    return links


def parse_candidate(data: dict[str, Any]) -> PaperTradeCandidate:
    schema = _as_str(data.get("schema")) or SCHEMA_NAME
    evidence_links = _parse_evidence_links(data.get("evidence_links"))
    replay_case_links = _parse_replay_case_links(data.get("replay_case_links"))
    related_evidence = data.get("related_evidence") or {}
    if not isinstance(related_evidence, dict):
        related_evidence = {}

    if not evidence_links:
        evidence_links = [EvidenceLink(link=link, supports="legacy-unmapped") for link in _as_list(related_evidence.get("examples"))]
    if not replay_case_links:
        replay_case_links = [ReplayCaseLink(replay_case=link, replay_status="NOT_VERIFIED") for link in _as_list(related_evidence.get("replay_cases"))]

    return PaperTradeCandidate(
        candidate_id=_as_str(data.get("candidate_id")),
        schema=schema,
        title=_as_str(data.get("title")) or None,
        related_phase_3_1_rule_candidate=_as_str(data.get("related_phase_3_1_rule_candidate")),
        evidence_links=evidence_links,
        replay_case_links=replay_case_links,
        related_evidence_examples=_as_list(related_evidence.get("examples")),
        related_evidence_replay_cases=_as_list(related_evidence.get("replay_cases")),
        symbol=_as_str(data.get("symbol")),
        direction=_as_str(data.get("direction")).lower(),
        timeframe_context=_as_str(data.get("timeframe_context")),
        setup_timeframe=_as_str(data.get("setup_timeframe")),
        execution_timeframe=_as_str(data.get("execution_timeframe")),
        support_level=data.get("support_level"),
        resistance_level=data.get("resistance_level"),
        target_price=data.get("target_price"),
        entry_candidate_price=data.get("entry_candidate_price"),
        room_to_target=data.get("room_to_target"),
        invalidation_level=data.get("invalidation_level"),
        confirmation_behavior=_as_str(data.get("confirmation_behavior")),
        confirmation_type=_as_str(data.get("confirmation_type")),
        higher_timeframe_context=_as_str(data.get("higher_timeframe_context")),
        higher_timeframe_obstacle_check=_as_str(data.get("higher_timeframe_obstacle_check")),
        target_already_hit_check=_as_str(data.get("target_already_hit_check")),
        no_trade_filters=_parse_no_trade_filters(data.get("no_trade_filters")),
        risk_notes=_as_str(data.get("risk_notes")),
        boundary=_as_str(data.get("boundary")),
        raw=data,
    )


def load_candidate(path: Path) -> PaperTradeCandidate:
    return parse_candidate(load_candidate_data(path))
