from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from monster_strategy_lab.data_sources import load_ohlcv_rows
from monster_strategy_lab.replay.discovery import (
    discover_close_below_support_events_for_symbol,
    discover_events_for_symbol,
)
from monster_strategy_lab.replay.case import ReplayCase, load_replay_case
from monster_strategy_lab.validation.historical_data import (
    OhlcvFileInspection,
    inspect_ohlcv_file,
    write_replay_data_quality_report,
)


@dataclass(frozen=True)
class ReplayBatchRow:
    replay_id: str
    related_candidate_id: str
    symbol: str
    date_window: str
    data_quality_status: str
    replay_status: str
    replay_outcome: str
    classification: str
    candidate_impact: str
    next_action: str



def _resolve_relative(repo_root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else repo_root / path


def _format_float(value: float | None) -> str:
    if value is None:
        return ""
    return f"{value:.2f}"



def _candidate_impact(classification: str) -> tuple[str, str]:
    classification = classification.lower().strip()
    if classification == "candidate_for_manual_review":
        return "manual review pending", "perform manual visual review"
    if classification == "confirmed_breakout":
        return "possible paper-review candidate if all gates pass", "manual visual review"
    if classification == "confirmed_breakout_no_target_hit":
        return "confirmed breakout without target hit; keep manual review pending", "manual visual review"
    if classification == "confirmed_breakdown":
        return "possible paper-review candidate if all gates pass", "manual visual review"
    if classification == "confirmed_breakdown_no_target_hit":
        return "confirmed breakdown without target hit; keep manual review pending", "manual visual review"
    if classification == "failed_breakout":
        return "blocks long breakout candidate promotion", "do not promote long breakout candidate"
    if classification == "failed_breakdown_reclaim":
        return "blocks short breakdown candidate promotion", "do not promote short breakdown candidate"
    if classification == "watch_no_trigger":
        return "watch/no-trigger only; no paper review", "keep as dry-run/watch"
    if classification == "support_touch_no_trigger":
        return "support touch only; no paper review", "keep as dry-run/watch"
    if classification == "ambiguous":
        return "paper review blocked until clarified", "perform manual visual review"
    if classification == "insufficient":
        return "insufficient for promotion; keep dry-run", "perform manual visual review"
    if classification == "contradicted":
        return "paper review blocked; evidence conflicts", "treat as contradicted"
    if classification == "blocked_data_quality":
        return "blocked until data quality is fixed", "rerun data quality checks"
    return "needs review", "manual review required"


def _case_side(case: ReplayCase) -> str:
    direction = str(case.raw.get("direction", "")).lower().strip()
    return "bearish" if direction == "short" else "bullish"


def _case_event(repo_root: Path, case: ReplayCase):
    obs_text = " ".join(case.replay_observations)
    if _case_side(case) == "bullish":
        events = discover_events_for_symbol(repo_root, case.symbol)
    else:
        events = discover_close_below_support_events_for_symbol(repo_root, case.symbol)
    for event in events:
        if event.timestamp in obs_text:
            return event
    return events[0] if events else None


def _triage_priority(side: str, breakout_amount: float, target_hit: bool, invalidation_hit: bool) -> tuple[str, str]:
    if target_hit or invalidation_hit:
        return "high", "clear follow-through or invalidation needs manual check"
    if breakout_amount >= 1.0:
        return "medium", "meaningful move but follow-through is not fully resolved"
    return "low", "small move; lower urgency unless manual review finds a contradiction"


def _case_date(case: ReplayCase) -> str:
    return case.date_window.split(" to ")[0]


def _case_target_price(side: str, prior_level: float, breakout_amount: float) -> float:
    delta = max(1.0, breakout_amount * 2)
    return prior_level + delta if side == "bullish" else prior_level - delta


def _case_target_hit(side: str, target_price: float, event: Any) -> bool:
    if side == "bullish":
        return any(
            value is not None and value >= target_price
            for value in (event.max_high_next_6_bars, event.max_high_next_12_bars, event.max_high_next_24_bars)
        )
    return any(
        value is not None and value <= target_price
        for value in (event.min_low_next_6_bars, event.min_low_next_12_bars, event.min_low_next_24_bars)
    )


def _case_max_favorable_move(side: str, event: Any) -> float:
    if side == "bullish":
        highs = [value for value in (event.max_high_next_6_bars, event.max_high_next_12_bars, event.max_high_next_24_bars) if value is not None]
        return max(highs) - event.close if highs else 0.0
    lows = [value for value in (event.min_low_next_6_bars, event.min_low_next_12_bars, event.min_low_next_24_bars) if value is not None]
    return event.close - min(lows) if lows else 0.0


def _case_suggested_classification(side: str, target_hit: bool, invalidation_hit: bool) -> str:
    if side == "bullish":
        if target_hit and not invalidation_hit:
            return "confirmed_breakout"
        if not target_hit and not invalidation_hit:
            return "confirmed_breakout_no_target_hit"
        if invalidation_hit and not target_hit:
            return "failed_breakout"
        return "ambiguous"
    if target_hit and not invalidation_hit:
        return "confirmed_breakdown"
    if not target_hit and not invalidation_hit:
        return "confirmed_breakdown_no_target_hit"
    if invalidation_hit and not target_hit:
        return "failed_breakdown_reclaim"
    return "ambiguous"


def render_replay_triage_summary(
    repo_root: Path,
    replay_case_paths: Iterable[Path],
    *,
    title: str = "HR-010 through HR-015 Triage Summary",
) -> str:
    lines = [
        f"# {title}",
        "",
        "| replay_id | symbol | side | event timestamp | setup type | prior level | breakout/breakdown close | amount | target price | target hit | invalidation hit | max favorable move | suggested classification | priority | reason |",
        "|---|---|---|---|---|---:|---:|---:|---:|---|---|---:|---|---|---|",
    ]
    for replay_case_path in replay_case_paths:
        case = load_replay_case(replay_case_path)
        side = _case_side(case)
        event = _case_event(repo_root, case)
        if event is None:
            continue
        prior_level = event.prior_resistance if side == "bullish" else event.prior_support
        amount = event.breakout_amount if side == "bullish" else event.breakdown_amount
        target_price = _case_target_price(side, prior_level, amount)
        target_hit = _case_target_hit(side, target_price, event)
        invalidation_hit = event.did_price_reclaim_below_resistance if side == "bullish" else event.did_price_reclaim_above_support
        max_favorable_move = _case_max_favorable_move(side, event)
        suggested = _case_suggested_classification(side, target_hit, invalidation_hit)
        priority, reason = _triage_priority(side, amount, target_hit, invalidation_hit)
        setup_type = "close_above_resistance" if side == "bullish" else "close_below_support"
        lines.append(
            "| "
            f"{case.replay_id} | {case.symbol} | {side} | {event.timestamp} | {setup_type} | "
            f"{_format_float(prior_level)} | {_format_float(event.close)} | {_format_float(amount)} | {_format_float(target_price)} | "
            f"{str(target_hit).lower()} | {str(invalidation_hit).lower()} | {_format_float(max_favorable_move)} | "
            f"{suggested} | {priority} | {reason} |"
        )
    lines.extend([
        "",
        "## Boundary",
        "- Manual review summary only",
        "- No trade signal",
        "- No broker action allowed",
    ])
    return "\n".join(lines).rstrip() + "\n"


def write_replay_triage_summary(
    repo_root: Path,
    replay_case_paths: Iterable[Path],
    *,
    filename: str = "HR-010_015_triage_summary.md",
    title: str = "HR-010 through HR-015 Triage Summary",
) -> Path:
    output_path = repo_root / "runs" / "replay" / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_replay_triage_summary(repo_root, replay_case_paths, title=title))
    return output_path


def _paper_readiness_impact(classification: str) -> str:
    classification = classification.lower().strip()
    if classification == "candidate_for_manual_review":
        return "manual review pending"
    if classification in {"confirmed_breakout", "confirmed_breakdown"}:
        return "potentially promotable after manual gates"
    if classification in {"confirmed_breakout_no_target_hit", "confirmed_breakdown_no_target_hit"}:
        return "manual review pending; target not fully met"
    if classification in {"watch_no_trigger", "support_touch_no_trigger"}:
        return "keep as dry-run/watch"
    if classification in {"failed_breakout", "failed_breakdown_reclaim"}:
        return "promotion blocked"
    if classification == "ambiguous":
        return "paper review blocked until clarified"
    if classification == "insufficient":
        return "insufficient for promotion; keep dry-run"
    if classification == "contradicted":
        return "paper review blocked; evidence conflicts"
    if classification == "blocked_data_quality":
        return "blocked until data quality is fixed"
    return "needs review"


def _lower(value: str | None) -> str:
    return (value or "").lower().strip()


def _direction_from_case(case: ReplayCase) -> str:
    direction = _lower(case.raw.get("direction") if isinstance(case.raw, dict) else None)
    if direction in {"long", "short"}:
        return direction
    classification = _lower(case.classification)
    if classification.startswith("confirmed_breakdown") or classification.startswith("failed_breakdown") or classification == "support_touch_no_trigger":
        return "short"
    return "long"


def _side_from_case(case: ReplayCase) -> str:
    direction = _direction_from_case(case)
    if direction == "long":
        return "bullish"
    if direction == "short":
        return "bearish"
    return "unknown"


def _setup_type(case: ReplayCase) -> str:
    direction = _direction_from_case(case)
    classification = _lower(case.classification)
    if direction == "short" or classification in {"confirmed_breakdown", "confirmed_breakdown_no_target_hit", "support_touch_no_trigger", "failed_breakdown_reclaim"}:
        return "close_below_support"
    return "close_above_resistance"


def _bool_text(value: bool) -> str:
    return "true" if value else "false"


def _event_flags_from_case(case: ReplayCase) -> tuple[str, str]:
    classification = _lower(case.manual_review_classification or case.classification)
    if classification in {"confirmed_breakout", "confirmed_breakdown"}:
        return "true", "false"
    if classification in {"confirmed_breakout_no_target_hit", "confirmed_breakdown_no_target_hit", "watch_no_trigger", "support_touch_no_trigger", "insufficient", "candidate_for_manual_review", "ambiguous", "blocked_data_quality"}:
        return "false", "false"
    if classification in {"failed_breakout", "failed_breakdown_reclaim"}:
        return "false", "true"
    if classification == "contradicted":
        return "false", "false"
    return "false", "false"


def _bucket_rows() -> list[dict[str, str]]:
    return [
        {"bucket": "bullish_confirmed_breakout_target_hit", "side": "bullish"},
        {"bucket": "bullish_breakout_no_target_hit", "side": "bullish"},
        {"bucket": "bullish_watch_no_trigger", "side": "bullish"},
        {"bucket": "bullish_failed_breakout_reclaim", "side": "bullish"},
        {"bucket": "bullish_target_already_hit_before_confirmation", "side": "bullish"},
        {"bucket": "bearish_confirmed_breakdown_target_hit", "side": "bearish"},
        {"bucket": "bearish_breakdown_no_target_hit", "side": "bearish"},
        {"bucket": "bearish_support_touch_no_trigger", "side": "bearish"},
        {"bucket": "bearish_failed_breakdown_reclaim", "side": "bearish"},
        {"bucket": "bearish_target_already_hit_before_confirmation", "side": "bearish"},
        {"bucket": "data_quality_blocked", "side": "unknown"},
        {"bucket": "insufficient_coverage", "side": "unknown"},
        {"bucket": "ambiguous", "side": "unknown"},
    ]


def _bucket_for_row(row: dict[str, str]) -> str:
    classification = _lower(row.get("classification"))
    direction = _lower(row.get("direction"))
    target_after = _lower(row.get("target_hit_after_confirmation"))
    invalidation_after = _lower(row.get("invalidation_hit_after_confirmation"))
    if direction == "long":
        if classification == "confirmed_breakout" and target_after == "true":
            return "bullish_confirmed_breakout_target_hit"
        if classification == "confirmed_breakout_no_target_hit":
            return "bullish_breakout_no_target_hit"
        if classification == "watch_no_trigger":
            return "bullish_watch_no_trigger"
        if classification == "failed_breakout" or invalidation_after == "true":
            return "bullish_failed_breakout_reclaim"
        if classification == "contradicted":
            return "bullish_target_already_hit_before_confirmation"
        if classification in {"insufficient", "candidate_for_manual_review"}:
            return "insufficient_coverage"
        if classification == "ambiguous":
            return "ambiguous"
        if classification == "blocked_data_quality":
            return "data_quality_blocked"
        return "insufficient_coverage"
    if classification == "confirmed_breakdown" and target_after == "true":
        return "bearish_confirmed_breakdown_target_hit"
    if classification == "confirmed_breakdown_no_target_hit":
        return "bearish_breakdown_no_target_hit"
    if classification == "support_touch_no_trigger":
        return "bearish_support_touch_no_trigger"
    if classification == "failed_breakdown_reclaim" or invalidation_after == "true":
        return "bearish_failed_breakdown_reclaim"
    if classification == "contradicted":
        return "bearish_target_already_hit_before_confirmation"
    if classification in {"insufficient", "candidate_for_manual_review"}:
        return "insufficient_coverage"
    if classification == "ambiguous":
        return "ambiguous"
    if classification == "blocked_data_quality":
        return "data_quality_blocked"
    return "insufficient_coverage"


def _bucket_status(count: int, has_examples: bool) -> str:
    if count > 0:
        return "covered"
    return "needs_more_examples" if has_examples else "missing"


def build_replay_evidence_matrix_rows(repo_root: Path, replay_case_paths: Iterable[Path]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for replay_case_path in replay_case_paths:
        case = load_replay_case(replay_case_path)
        target_hit_after_confirmation, invalidation_hit_after_confirmation = _event_flags_from_case(case)
        rows.append(
            {
                "replay_id": case.replay_id,
                "related_candidate_id": case.related_candidate_id,
                "symbol": case.symbol,
                "date_window": case.date_window,
                "direction": _direction_from_case(case),
                "side": _side_from_case(case),
                "setup_type": _setup_type(case),
                "replay_status": case.replay_status,
                "replay_outcome": case.replay_outcome,
                "classification": case.classification,
                "manual_review_status": case.manual_review_status,
                "target_hit_after_confirmation": target_hit_after_confirmation,
                "invalidation_hit_after_confirmation": invalidation_hit_after_confirmation,
                "evidence_type": case.evidence_type,
                "real_market_evidence": _bool_text(case.real_market_evidence),
                "paper_readiness_impact": _paper_readiness_impact(case.classification),
                "next_action": _candidate_impact(case.classification)[1],
            }
        )
    return rows


def _render_matrix_csv(rows: list[dict[str, str]]) -> str:
    import csv
    from io import StringIO

    fieldnames = [
        "replay_id",
        "related_candidate_id",
        "symbol",
        "date_window",
        "direction",
        "side",
        "setup_type",
        "replay_status",
        "replay_outcome",
        "classification",
        "manual_review_status",
        "target_hit_after_confirmation",
        "invalidation_hit_after_confirmation",
        "evidence_type",
        "real_market_evidence",
        "paper_readiness_impact",
        "next_action",
    ]
    buffer = StringIO()
    writer = csv.DictWriter(buffer, fieldnames=fieldnames, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({name: row.get(name, "") for name in fieldnames})
    return buffer.getvalue()


def _coverage_buckets(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    buckets = {item["bucket"]: {"bucket": item["bucket"], "count": 0, "replay_ids": []} for item in _bucket_rows()}
    for row in rows:
        bucket = _bucket_for_row(row)
        entry = buckets[bucket]
        entry["count"] += 1
        entry["replay_ids"].append(row["replay_id"])

    rendered: list[dict[str, str]] = []
    for item in _bucket_rows():
        entry = buckets[item["bucket"]]
        status = _bucket_status(entry["count"], item["bucket"] in {"insufficient_coverage", "ambiguous", "data_quality_blocked"})
        rendered.append(
            {
                "bucket": item["bucket"],
                "count": str(entry["count"]),
                "replay_ids": ", ".join(entry["replay_ids"]) if entry["replay_ids"] else "none",
                "status": status,
            }
        )
    return rendered


def _date_distribution_summary(case_paths: list[Path]) -> dict[str, Any]:
    cases = [load_replay_case(path) for path in case_paths]
    dates = [case.date_window.split(" to ")[0] for case in cases]
    parsed_dates = [datetime.fromisoformat(date.replace(" ", "T")).date() for date in dates if date]
    by_year: dict[str, int] = {}
    by_month: dict[str, int] = {}
    by_symbol: dict[str, int] = {}
    by_side: dict[str, int] = {}
    by_classification: dict[str, int] = {}
    for case, date_str in zip(cases, parsed_dates):
        by_year[str(date_str.year)] = by_year.get(str(date_str.year), 0) + 1
        by_month[date_str.strftime("%Y-%m")] = by_month.get(date_str.strftime("%Y-%m"), 0) + 1
        by_symbol[case.symbol] = by_symbol.get(case.symbol, 0) + 1
        side = "bearish" if str(case.raw.get("direction", "")).lower().strip() == "short" else "bullish"
        by_side[side] = by_side.get(side, 0) + 1
        by_classification[case.classification] = by_classification.get(case.classification, 0) + 1
    clustered = False
    if parsed_dates:
        for start in sorted(set(parsed_dates)):
            window_count = sum(1 for d in parsed_dates if 0 <= (d - start).days <= 5)
            if window_count >= max(3, len(parsed_dates) // 2 + 1):
                clustered = True
                break
    return {
        "count_by_year": by_year,
        "count_by_month": by_month,
        "count_by_symbol": by_symbol,
        "count_by_side": by_side,
        "count_by_classification": by_classification,
        "earliest_replay_date": min(parsed_dates).isoformat() if parsed_dates else "",
        "latest_replay_date": max(parsed_dates).isoformat() if parsed_dates else "",
        "clustered_windows_warning": clustered,
    }


def render_replay_evidence_matrix(
    rows: list[dict[str, str]],
    coverage: list[dict[str, str]],
    date_summary: dict[str, Any] | None = None,
) -> str:
    date_summary = date_summary or {}
    lines = ["# Replay Evidence Matrix", ""]
    for row in rows:
        lines.extend(
            [
                f"## {row['replay_id']}",
                f"- replay_id: {row['replay_id']}",
                f"- related_candidate_id: {row['related_candidate_id']}",
                f"- symbol: {row['symbol']}",
                f"- date_window: {row['date_window']}",
                f"- direction: {row['direction']}",
                f"- side: {row['side']}",
                f"- setup_type: {row['setup_type']}",
                f"- replay_status: {row['replay_status']}",
                f"- replay_outcome: {row['replay_outcome']}",
                f"- classification: {row['classification']}",
                f"- manual_review_status: {row['manual_review_status']}",
                f"- target_hit_after_confirmation: {row['target_hit_after_confirmation']}",
                f"- invalidation_hit_after_confirmation: {row['invalidation_hit_after_confirmation']}",
                f"- evidence_type: {row['evidence_type']}",
                f"- real_market_evidence: {row['real_market_evidence']}",
                f"- paper_readiness_impact: {row['paper_readiness_impact']}",
                f"- next_action: {row['next_action']}",
                "",
            ]
        )
    lines.extend(["## Coverage Summary", ""])
    for item in coverage:
        lines.extend(
            [
                f"### {item['bucket']}",
                f"- count: {item['count']}",
                f"- replay_ids: {item['replay_ids']}",
                f"- status: {item['status']}",
                "",
            ]
        )
    lines.extend([
        "## Date Distribution Summary",
        f"- earliest replay date: {date_summary.get('earliest_replay_date', '')}",
        f"- latest replay date: {date_summary.get('latest_replay_date', '')}",
        f"- clustered_windows_warning: {str(date_summary.get('clustered_windows_warning', False)).lower()}",
        "",
        "### count by year",
    ])
    for key, value in sorted(date_summary.get("count_by_year", {}).items()):
        lines.append(f"- {key}: {value}")
    lines.append("")
    lines.append("### count by month")
    for key, value in sorted(date_summary.get("count_by_month", {}).items()):
        lines.append(f"- {key}: {value}")
    lines.append("")
    lines.append("### count by symbol")
    for key, value in sorted(date_summary.get("count_by_symbol", {}).items()):
        lines.append(f"- {key}: {value}")
    lines.append("")
    lines.append("### count by side")
    for key, value in sorted(date_summary.get("count_by_side", {}).items()):
        lines.append(f"- {key}: {value}")
    lines.append("")
    lines.append("### count by classification")
    for key, value in sorted(date_summary.get("count_by_classification", {}).items()):
        lines.append(f"- {key}: {value}")
    recent_ids = {f"HR-{idx:03d}" for idx in range(10, 16)}
    recent_rows = [row for row in rows if row["replay_id"] in recent_ids]
    if recent_rows:
        symbols = {row["symbol"] for row in recent_rows}
        months = sorted({row.get("date_window", "")[:7] for row in recent_rows if row.get("date_window")})
        lines.extend(
            [
                "",
                "## Selection warnings",
                f"- date diversity improved: HR-010 through HR-015 now span {', '.join(months) if months else 'multiple months'}",
                f"- symbol diversity still weak: HR-010 through HR-015 are all {', '.join(sorted(symbols)) if symbols else 'unknown'}",
            ]
        )
    lines.extend([
        "",
        "## Coverage Gaps",
        "- bullish_failed_breakout_reclaim: missing",
        "- bullish_target_already_hit_before_confirmation: missing",
        "- bearish_support_touch_no_trigger: missing",
        "- bearish_target_already_hit_before_confirmation: missing",
        "- data_quality_blocked: needs_more_examples",
        "- ambiguous: needs_more_examples",
        "- note: the active artifact index now points at the full 11-symbol 1Day + 5Min handoff, but current replay evidence is still concentrated in a smaller subset of symbols and dates.",
        "",
        "## Recommended Next Search",
        "- bearish close_below_support discovery",
        "- diversify replay dates beyond May 2023 if additional sample data becomes available",
        "- keep broker_action_allowed false in replay cases",
    ])
    lines.extend(
        [
            "## Boundary",
            "- Generated report only",
            "- Source of truth remains replay/cases/HR-*.md",
            "- No broker action allowed",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def write_replay_evidence_matrix(repo_root: Path, replay_case_paths: Iterable[Path] | None = None) -> Path:
    replay_case_paths = list(replay_case_paths or sorted((repo_root / "replay" / "cases").glob("HR-*.md")))
    rows = build_replay_evidence_matrix_rows(repo_root, replay_case_paths)
    coverage = _coverage_buckets(rows)
    date_summary = _date_distribution_summary(list(replay_case_paths))
    output_dir = repo_root / "runs" / "replay"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "replay_evidence_matrix.md"
    output_path.write_text(render_replay_evidence_matrix(rows, coverage, date_summary))
    csv_path = output_dir / "replay_evidence_matrix.csv"
    csv_path.write_text(_render_matrix_csv(rows))
    return output_path



def inspect_replay_case(repo_root: Path, replay_case_path: Path) -> tuple[ReplayCase, list[OhlcvFileInspection], list[Path]]:
    case = load_replay_case(replay_case_path)
    data_paths = [_resolve_relative(repo_root, raw) for raw in case.data_files]
    inspections = [inspect_ohlcv_file(path) for path in data_paths]
    return case, inspections, data_paths



def write_replay_case_data_quality_report(repo_root: Path, replay_case_path: Path) -> Path:
    case = load_replay_case(replay_case_path)
    inspections = [inspect_ohlcv_file(_resolve_relative(repo_root, raw)) for raw in case.data_files]
    blockers = []
    can_be_real_market_replay = all(item.quality_status == "PASS" for item in inspections)
    if not can_be_real_market_replay:
        blockers.extend(
            [
                f"{inspection.path.name}: {issue}"
                for inspection in inspections
                for issue in inspection.issues
            ]
        )
    return write_replay_data_quality_report(
        repo_root,
        case.replay_id,
        replay_case_path,
        inspections,
        can_be_real_market_replay=can_be_real_market_replay,
        blockers=blockers,
        date_window=case.date_window,
    )



def build_replay_batch_rows(repo_root: Path, replay_case_paths: Iterable[Path]) -> list[ReplayBatchRow]:
    rows: list[ReplayBatchRow] = []
    for replay_case_path in replay_case_paths:
        case, inspections, _ = inspect_replay_case(repo_root, replay_case_path)
        data_quality_status = "PASSED" if inspections and all(item.quality_status == "PASS" for item in inspections) else "FAILED"
        classification = case.classification
        if data_quality_status != "PASSED" and classification not in {"blocked_data_quality", "contradicted"}:
            classification = "blocked_data_quality"
        impact, next_action = _candidate_impact(classification)
        rows.append(
            ReplayBatchRow(
                replay_id=case.replay_id,
                related_candidate_id=case.related_candidate_id,
                symbol=case.symbol,
                date_window=case.date_window,
                data_quality_status=data_quality_status,
                replay_status=case.replay_status,
                replay_outcome=case.replay_outcome,
                classification=classification,
                candidate_impact=impact,
                next_action=next_action,
            )
        )
    return rows



def render_replay_batch_summary(rows: list[ReplayBatchRow]) -> str:
    lines = [
        "# Replay Batch Summary",
        "",
        f"generated_at: {datetime.now(timezone.utc).isoformat()}",
        "",
    ]
    for row in rows:
        lines.extend(
            [
                f"## {row.replay_id}",
                f"- replay_id: {row.replay_id}",
                f"- related_candidate_id: {row.related_candidate_id}",
                f"- symbol: {row.symbol}",
                f"- date_window: {row.date_window}",
                f"- data_quality_status: {row.data_quality_status}",
                f"- replay_status: {row.replay_status}",
                f"- replay_outcome: {row.replay_outcome}",
                f"- classification: {row.classification}",
                f"- candidate impact: {row.candidate_impact}",
                f"- next action: {row.next_action}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"



def write_replay_batch_summary(repo_root: Path, replay_case_paths: Iterable[Path]) -> Path:
    rows = build_replay_batch_rows(repo_root, replay_case_paths)
    output_dir = repo_root / "runs" / "replay"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "replay_batch_summary.md"
    output_path.write_text(render_replay_batch_summary(rows))
    return output_path
