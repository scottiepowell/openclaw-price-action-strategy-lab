from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
import csv

from monster_strategy_lab.replay import load_replay_case
from monster_strategy_lab.validation.paper_review import build_paper_review_queue_rows


WATCH_STATUS_PENDING = "pending"
WATCH_STATUS_ACTIVE_WATCH = "active_watch"
WATCH_STATUS_TRIGGERED = "triggered"
WATCH_STATUS_TARGET_HIT = "target_hit"
WATCH_STATUS_INVALIDATION_HIT = "invalidation_hit"
WATCH_STATUS_EXPIRED = "expired"
WATCH_STATUS_SKIPPED = "skipped"
WATCH_STATUS_CANCELLED = "cancelled"
WATCH_STATUSES = [
    WATCH_STATUS_PENDING,
    WATCH_STATUS_ACTIVE_WATCH,
    WATCH_STATUS_TRIGGERED,
    WATCH_STATUS_TARGET_HIT,
    WATCH_STATUS_INVALIDATION_HIT,
    WATCH_STATUS_EXPIRED,
    WATCH_STATUS_SKIPPED,
    WATCH_STATUS_CANCELLED,
]


@dataclass(frozen=True)
class PaperWatchJournalRow:
    journal_id: str
    candidate_id: str
    replay_id: str
    symbol: str
    side: str
    setup_type: str
    source_status: str
    paper_review_status: str
    watch_status: str
    planned_entry_condition: str
    planned_entry_price: str
    planned_target_price: str
    planned_invalidation_level: str
    observed_entry_time: str
    observed_entry_price: str
    observed_exit_time: str
    observed_exit_price: str
    observed_outcome: str
    notes: str
    broker_action_allowed: bool


def _bool_text(value: bool) -> str:
    return "true" if value else "false"


def build_paper_watch_journal_rows(repo_root: Path, replay_case_paths: Iterable[Path]) -> list[PaperWatchJournalRow]:
    queue_rows = build_paper_review_queue_rows(repo_root, replay_case_paths)
    rows: list[PaperWatchJournalRow] = []
    for index, queue_row in enumerate(queue_rows, start=1):
        rows.append(
            PaperWatchJournalRow(
                journal_id=f"PWJ-{index:03d}",
                candidate_id=queue_row.candidate_id,
                replay_id=queue_row.replay_id,
                symbol=queue_row.symbol,
                side=queue_row.side,
                setup_type=queue_row.setup_type,
                source_status="READY_FOR_PAPER_REVIEW",
                paper_review_status=queue_row.paper_review_status,
                watch_status=WATCH_STATUS_PENDING,
                planned_entry_condition=f"manual watch for {queue_row.setup_type}; no broker action",
                planned_entry_price=queue_row.entry_candidate_price,
                planned_target_price=queue_row.target_price,
                planned_invalidation_level=queue_row.invalidation_level,
                observed_entry_time="",
                observed_entry_price="",
                observed_exit_time="",
                observed_exit_price="",
                observed_outcome="",
                notes="manual paper-watch journal only; no order submission",
                broker_action_allowed=False,
            )
        )
    return rows


def render_paper_watch_journal(rows: list[PaperWatchJournalRow]) -> str:
    lines = [
        "# Paper Watch Journal",
        "",
        "Manual paper-watch tracking only. No orders, broker calls, or profitability claims.",
        "",
        "| journal_id | candidate_id | replay_id | symbol | side | setup_type | source_status | paper_review_status | watch_status | planned_entry_condition | planned_entry_price | planned_target_price | planned_invalidation_level | observed_entry_time | observed_entry_price | observed_exit_time | observed_exit_price | observed_outcome | notes | broker_action_allowed |",
        "|---|---|---|---|---|---|---|---|---|---|---:|---:|---:|---|---:|---|---:|---|---|---|",
    ]
    for row in rows:
        lines.append(
            "| "
            f"{row.journal_id} | {row.candidate_id} | {row.replay_id} | {row.symbol} | {row.side} | {row.setup_type} | {row.source_status} | {row.paper_review_status} | {row.watch_status} | {row.planned_entry_condition} | {row.planned_entry_price} | {row.planned_target_price} | {row.planned_invalidation_level} | {row.observed_entry_time} | {row.observed_entry_price} | {row.observed_exit_time} | {row.observed_exit_price} | {row.observed_outcome} | {row.notes} | {_bool_text(row.broker_action_allowed)} |"
        )
    lines.extend(["", "## Boundary", "- no trade signal", "- no profitability claim", "- no broker action", "- no Alpaca submission"])
    return "\n".join(lines).rstrip() + "\n"


def _rows_to_csv(rows: list[PaperWatchJournalRow]) -> str:
    fieldnames = [
        "journal_id",
        "candidate_id",
        "replay_id",
        "symbol",
        "side",
        "setup_type",
        "source_status",
        "paper_review_status",
        "watch_status",
        "planned_entry_condition",
        "planned_entry_price",
        "planned_target_price",
        "planned_invalidation_level",
        "observed_entry_time",
        "observed_entry_price",
        "observed_exit_time",
        "observed_exit_price",
        "observed_outcome",
        "notes",
        "broker_action_allowed",
    ]
    from io import StringIO

    buf = StringIO()
    writer = csv.DictWriter(buf, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({name: getattr(row, name) if name != "broker_action_allowed" else _bool_text(row.broker_action_allowed) for name in fieldnames})
    return buf.getvalue()


def render_paper_watch_journal_readme() -> str:
    return """# Paper Watch Journal

This directory is for manual paper-watch tracking only.

Allowed:
- record planned manual watch levels from paper-review plans
- record observed entry/exit times and prices after human observation
- mark outcomes such as pending, active_watch, triggered, target_hit, invalidation_hit, expired, skipped, or cancelled

Not allowed:
- no trade signal
- no profitability claim
- no broker action
- no Alpaca submission
- no paper order submission
- no position sizing calculation yet

`approved_for_paper_watch` only means a human may watch or simulate the case manually. It does not authorize order submission.
"""


def write_paper_watch_journal(repo_root: Path, replay_case_paths: Iterable[Path]) -> tuple[Path, Path, Path, list[PaperWatchJournalRow]]:
    rows = build_paper_watch_journal_rows(repo_root, replay_case_paths)
    output_dir = repo_root / "runs" / "paper_journal"
    output_dir.mkdir(parents=True, exist_ok=True)
    md_path = output_dir / "paper_watch_journal.md"
    csv_path = output_dir / "paper_watch_journal.csv"
    readme_path = output_dir / "README.md"
    md_path.write_text(render_paper_watch_journal(rows))
    csv_path.write_text(_rows_to_csv(rows))
    readme_path.write_text(render_paper_watch_journal_readme())
    return md_path, csv_path, readme_path, rows


def _evidence_summary(case) -> str:
    lines = []
    for item in case.replay_observations[:6]:
        lines.append(f"- {item}")
    return "\n".join(lines) if lines else "- none"


def render_paper_watch_journal_template(row: PaperWatchJournalRow, replay_observations: list[str]) -> str:
    evidence_summary = "\n".join(f"- {item}" for item in replay_observations[:6]) or "- none"
    return f"""# {row.candidate_id} Paper Watch Journal

## Candidate summary
- journal_id: {row.journal_id}
- candidate_id: {row.candidate_id}
- replay_id: {row.replay_id}
- symbol: {row.symbol}
- side: {row.side}
- setup_type: {row.setup_type}
- source_status: {row.source_status}
- paper_review_status: {row.paper_review_status}
- watch_status: {row.watch_status}
- broker_action_allowed: false

## Replay evidence summary
{evidence_summary}

## Planned entry / target / invalidation
- planned_entry_condition: {row.planned_entry_condition}
- planned_entry_price: {row.planned_entry_price}
- planned_target_price: {row.planned_target_price}
- planned_invalidation_level: {row.planned_invalidation_level}
- risk_unit_placeholder: not calculated

## Manual observation checklist
- [ ] Human approved this for manual paper watch
- [ ] Watch status updated from pending when observation begins
- [ ] Entry condition observed manually
- [ ] Target or invalidation observed manually
- [ ] Outcome recorded without broker execution
- [ ] No position size calculated

## Outcome section
- observed_entry_time:
- observed_entry_price:
- observed_exit_time:
- observed_exit_price:
- observed_outcome:
- notes:

## Boundary
- no trade signal
- no profitability claim
- no broker action
- no Alpaca submission
"""


def write_paper_watch_journal_template(repo_root: Path, row: PaperWatchJournalRow) -> Path:
    case = load_replay_case(repo_root / "replay" / "cases" / f"{row.replay_id}.md")
    output_dir = repo_root / "runs" / "paper_journal"
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{row.candidate_id}-journal.md"
    path.write_text(render_paper_watch_journal_template(row, case.replay_observations))
    return path

