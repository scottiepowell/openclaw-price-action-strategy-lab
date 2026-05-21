from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
import csv
import re

from monster_strategy_lab.replay import load_replay_case
from monster_strategy_lab.validation.paper_readiness import READY_FOR_PAPER_REVIEW, assess_replay_case


PAPER_REVIEW_STATUS_PENDING_HUMAN_APPROVAL = "pending_human_approval"
PAPER_REVIEW_STATUS_APPROVED_FOR_PAPER_WATCH = "approved_for_paper_watch"
PAPER_REVIEW_STATUS_REJECTED = "rejected"
PAPER_REVIEW_STATUS_DEFERRED = "deferred"
PAPER_REVIEW_STATUSES = [
    PAPER_REVIEW_STATUS_PENDING_HUMAN_APPROVAL,
    PAPER_REVIEW_STATUS_APPROVED_FOR_PAPER_WATCH,
    PAPER_REVIEW_STATUS_REJECTED,
    PAPER_REVIEW_STATUS_DEFERRED,
]


@dataclass(frozen=True)
class PaperReviewQueueRow:
    candidate_id: str
    replay_id: str
    symbol: str
    side: str
    setup_type: str
    replay_classification: str
    entry_candidate_price: str
    target_price: str
    invalidation_level: str
    room_to_target: str
    risk_unit_placeholder: str
    paper_review_status: str
    broker_action_allowed: bool
    next_action: str


def _bool_text(value: bool) -> str:
    return "true" if value else "false"


def _packet_path(repo_root: Path, replay_id: str) -> Path:
    return repo_root / "runs" / "replay" / f"{replay_id}_manual_review_packet.md"


def _read_text(path: Path) -> str:
    return path.read_text() if path.exists() else ""


def _packet_value(text: str, key: str) -> str:
    match = re.search(rf"^- {re.escape(key)}:\s*(.+)$", text, flags=re.MULTILINE)
    return match.group(1).strip() if match else "TBD"


def _packet_value_any(text: str, keys: list[str]) -> str:
    for key in keys:
        value = _packet_value(text, key)
        if value != "TBD":
            return value
    return "TBD"


def _setup_type(side: str) -> str:
    return "close_below_support" if side == "bearish" else "close_above_resistance"


def _paper_review_next_action() -> str:
    return "await human approval; do not submit orders"


def build_paper_review_queue_rows(repo_root: Path, replay_case_paths: Iterable[Path]) -> list[PaperReviewQueueRow]:
    rows: list[PaperReviewQueueRow] = []
    for case_path in replay_case_paths:
        case = load_replay_case(case_path)
        readiness = assess_replay_case(case)
        if readiness.readiness_status != READY_FOR_PAPER_REVIEW:
            continue

        packet_text = _read_text(_packet_path(repo_root, case.replay_id))
        entry_price = _packet_value(packet_text, "entry_candidate_price")
        target_price = _packet_value(packet_text, "proposed target_price")
        invalidation_level = _packet_value(packet_text, "proposed invalidation_level")
        room_to_target = _packet_value_any(packet_text, ["room_to_target", "target_distance"])
        row = PaperReviewQueueRow(
            candidate_id=case.related_candidate_id,
            replay_id=case.replay_id,
            symbol=case.symbol,
            side="bearish" if case.raw.get("direction", "").lower() == "short" else "bullish",
            setup_type=_setup_type("bearish" if case.raw.get("direction", "").lower() == "short" else "bullish"),
            replay_classification=case.manual_review_classification or case.classification,
            entry_candidate_price=entry_price,
            target_price=target_price,
            invalidation_level=invalidation_level,
            room_to_target=room_to_target,
            risk_unit_placeholder="1R",
            paper_review_status=PAPER_REVIEW_STATUS_PENDING_HUMAN_APPROVAL,
            broker_action_allowed=False,
            next_action=_paper_review_next_action(),
        )
        rows.append(row)
    rows.sort(key=lambda row: row.candidate_id)
    return rows


def render_paper_review_queue(rows: list[PaperReviewQueueRow]) -> str:
    lines = [
        "# Paper Review Queue",
        "",
        "| candidate_id | replay_id | symbol | side | setup_type | replay_classification | entry_candidate_price | target_price | invalidation_level | room_to_target | risk_unit_placeholder | paper_review_status | broker_action_allowed | next_action |",
        "|---|---|---|---|---|---|---:|---:|---:|---:|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            "| "
            f"{row.candidate_id} | {row.replay_id} | {row.symbol} | {row.side} | {row.setup_type} | {row.replay_classification} | {row.entry_candidate_price} | {row.target_price} | {row.invalidation_level} | {row.room_to_target} | {row.risk_unit_placeholder} | {row.paper_review_status} | {_bool_text(row.broker_action_allowed)} | {row.next_action} |"
        )
    lines.extend(["", "## Boundary", "- No trade signal", "- No profitability claim", "- No broker action", "- No Alpaca submission"])
    return "\n".join(lines).rstrip() + "\n"


def _rows_to_csv(rows: list[PaperReviewQueueRow]) -> str:
    fieldnames = [
        "candidate_id",
        "replay_id",
        "symbol",
        "side",
        "setup_type",
        "replay_classification",
        "entry_candidate_price",
        "target_price",
        "invalidation_level",
        "room_to_target",
        "risk_unit_placeholder",
        "paper_review_status",
        "broker_action_allowed",
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
                "setup_type": row.setup_type,
                "replay_classification": row.replay_classification,
                "entry_candidate_price": row.entry_candidate_price,
                "target_price": row.target_price,
                "invalidation_level": row.invalidation_level,
                "room_to_target": row.room_to_target,
                "risk_unit_placeholder": row.risk_unit_placeholder,
                "paper_review_status": row.paper_review_status,
                "broker_action_allowed": _bool_text(row.broker_action_allowed),
                "next_action": row.next_action,
            }
        )
    return buf.getvalue()


def write_paper_review_queue(repo_root: Path, replay_case_paths: Iterable[Path]) -> tuple[Path, Path, list[PaperReviewQueueRow]]:
    rows = build_paper_review_queue_rows(repo_root, replay_case_paths)
    output_dir = repo_root / "runs" / "paper_review"
    output_dir.mkdir(parents=True, exist_ok=True)
    md_path = output_dir / "paper_review_queue.md"
    csv_path = output_dir / "paper_review_queue.csv"
    md_path.write_text(render_paper_review_queue(rows))
    csv_path.write_text(_rows_to_csv(rows))
    return md_path, csv_path, rows


def _plan_manual_approval_checklist() -> list[str]:
    return [
        "Replay evidence is verified and real-market-backed",
        "Paper review status remains pending_human_approval until manually approved",
        "Broker action stays false",
        "No Alpaca submission or live execution path exists",
        "Target and invalidation levels are documented",
        "No profitability claim is made",
    ]


def _packet_summary(packet_text: str) -> list[str]:
    lines: list[str] = []
    wanted_prefixes = (
        "- Discovery scanner",
        "- prior_resistance:",
        "- prior_support:",
        "- breakout_amount:",
        "- breakdown_amount:",
        "- close_above_resistance:",
        "- close_below_support:",
        "- target_hit_after_confirmation:",
        "- invalidation_hit_after_confirmation:",
        "- suggested_classification:",
    )
    for line in packet_text.splitlines():
        if any(line.startswith(prefix) for prefix in wanted_prefixes):
            lines.append(line)
    return lines[:8]


def render_paper_review_plan(row: PaperReviewQueueRow, packet_text: str, replay_observations: list[str]) -> str:
    evidence_summary_items = _packet_summary(packet_text)
    evidence_summary = "\n".join(evidence_summary_items) if evidence_summary_items else "- none"
    no_trade_filters = [
        "- real_market_replay only",
        "- verified replay evidence",
        "- manual_review_status completed",
        "- broker_action_allowed false",
        "- no Alpaca submission",
        "- no live trading",
    ]
    lines = [
        f"# {row.candidate_id} Paper Review Plan",
        "",
        f"- replay_id: {row.replay_id}",
        f"- symbol: {row.symbol}",
        f"- side: {row.side}",
        f"- paper_review_status: {PAPER_REVIEW_STATUS_PENDING_HUMAN_APPROVAL}",
        f"- broker_action_allowed: false",
        "",
        "## Replay evidence summary",
        evidence_summary,
        "",
        "## Entry condition",
        f"- {row.setup_type} replay supports a manual paper-review watch only; entry candidate price is {row.entry_candidate_price}.",
        "",
        "## Target condition",
        f"- target_price: {row.target_price}",
        f"- room_to_target: {row.room_to_target}",
        "",
        "## Invalidation condition",
        f"- invalidation_level: {row.invalidation_level}",
        "",
        "## No-trade filters",
        *no_trade_filters,
        "",
        "## Manual approval checklist",
    ]
    for item in _plan_manual_approval_checklist():
        lines.append(f"- [ ] {item}")
    lines.extend([
        "",
        "## Boundary",
        "- no trade signal",
        "- no profitability claim",
        "- no broker action",
        "- no Alpaca submission",
    ])
    return "\n".join(lines).rstrip() + "\n"


def write_paper_review_plan(repo_root: Path, row: PaperReviewQueueRow) -> Path:
    packet_text = _read_text(_packet_path(repo_root, row.replay_id))
    case = load_replay_case(repo_root / "replay" / "cases" / f"{row.replay_id}.md")
    output_dir = repo_root / "runs" / "paper_review"
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{row.candidate_id}-paper-review-plan.md"
    path.write_text(render_paper_review_plan(row, packet_text, case.replay_observations))
    return path
