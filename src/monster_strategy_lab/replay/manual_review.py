from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from monster_strategy_lab.data_sources import load_ohlcv_rows as _load_ohlcv_rows
from monster_strategy_lab.replay.case import load_replay_case


@dataclass(frozen=True)
class BarMatch:
    timestamp: str
    open: float
    high: float
    low: float
    close: float
    volume: str
    trade_count: str
    vwap: str
    distance: float


def load_ohlcv_rows(path: Path) -> list[dict[str, str]]:
    return _load_ohlcv_rows(path)


def _resolve_path(repo_root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else repo_root / path


def _float(value: Any) -> float:
    return float(value)


def _row_match(row: dict[str, str], level: float) -> BarMatch:
    values = [
        _float(row["open"]),
        _float(row["high"]),
        _float(row["low"]),
        _float(row["close"]),
    ]
    distance = min(abs(value - level) for value in values)
    return BarMatch(
        timestamp=row["timestamp"],
        open=_float(row["open"]),
        high=_float(row["high"]),
        low=_float(row["low"]),
        close=_float(row["close"]),
        volume=row.get("volume", ""),
        trade_count=row.get("trade_count", ""),
        vwap=row.get("vwap", ""),
        distance=distance,
    )


def nearest_bar(rows: list[dict[str, str]], level: float) -> BarMatch:
    if not rows:
        raise ValueError("no rows available")
    return min((_row_match(row, level) for row in rows), key=lambda match: (match.distance, match.timestamp))


def _first_index(rows: list[dict[str, str]], predicate) -> int | None:
    for idx, row in enumerate(rows):
        if predicate(row):
            return idx
    return None


def analyze_level_interactions(
    rows: list[dict[str, str]],
    *,
    support_level: float,
    resistance_level: float,
    target_price: float,
    invalidation_level: float,
) -> dict[str, Any]:
    support = nearest_bar(rows, support_level)
    resistance = nearest_bar(rows, resistance_level)
    target = nearest_bar(rows, target_price)
    invalidation = nearest_bar(rows, invalidation_level)

    resistance_touched = any(_float(row["high"]) >= resistance_level for row in rows)
    close_above_resistance = any(_float(row["close"]) > resistance_level for row in rows)
    target_close_hit = any(_float(row["close"]) >= target_price for row in rows)
    target_high_hit = any(_float(row["high"]) >= target_price for row in rows)
    invalidation_hit = any(_float(row["low"]) <= invalidation_level for row in rows)

    confirmation_index = _first_index(rows, lambda row: _float(row["close"]) > resistance_level)
    confirmation_rows = rows[confirmation_index:] if confirmation_index is not None else []
    pre_confirmation_rows = rows[:confirmation_index] if confirmation_index is not None else rows

    target_hit_before_confirmation = any(
        _float(row["high"]) >= target_price or _float(row["close"]) >= target_price
        for row in pre_confirmation_rows
    )
    target_hit_after_confirmation = any(
        _float(row["high"]) >= target_price or _float(row["close"]) >= target_price
        for row in confirmation_rows
    )
    invalidation_hit_before_confirmation = any(
        _float(row["low"]) <= invalidation_level
        for row in pre_confirmation_rows
    )
    invalidation_hit_after_confirmation = any(
        _float(row["low"]) <= invalidation_level
        for row in confirmation_rows
    )

    max_high_after_confirmation = max((_float(row["high"]) for row in confirmation_rows), default=float("nan"))
    max_close_after_confirmation = max((_float(row["close"]) for row in confirmation_rows), default=float("nan"))
    target_distance = target_price - resistance_level
    max_favorable_move = max_high_after_confirmation - resistance_level if confirmation_rows else float("nan")

    if not resistance_touched:
        suggested_classification = "insufficient"
    elif target_hit_before_confirmation:
        suggested_classification = "contradicted"
    elif close_above_resistance and target_hit_after_confirmation and not invalidation_hit_after_confirmation:
        suggested_classification = "confirmed_breakout"
    elif close_above_resistance and not target_hit_after_confirmation and not invalidation_hit_after_confirmation:
        suggested_classification = "confirmed_breakout_no_target_hit"
    elif close_above_resistance and invalidation_hit_after_confirmation and not target_hit_after_confirmation:
        suggested_classification = "failed_breakout"
    elif resistance_touched and not close_above_resistance:
        suggested_classification = "watch_no_trigger"
    elif close_above_resistance:
        suggested_classification = "ambiguous"
    else:
        suggested_classification = "blocked_data_quality"

    return {
        "support": support,
        "resistance": resistance,
        "target": target,
        "invalidation": invalidation,
        "resistance_touched": resistance_touched,
        "close_above_resistance": close_above_resistance,
        "target_hit_before_confirmation": target_hit_before_confirmation,
        "target_hit_after_confirmation": target_hit_after_confirmation,
        "invalidation_hit": invalidation_hit,
        "invalidation_hit_after_confirmation": invalidation_hit_after_confirmation,
        "target_already_hit_before_confirmation": target_hit_before_confirmation,
        "invalidation_hit_before_confirmation": invalidation_hit_before_confirmation,
        "target_close_hit": target_close_hit,
        "target_high_hit": target_high_hit,
        "max_high_after_confirmation": max_high_after_confirmation,
        "max_close_after_confirmation": max_close_after_confirmation,
        "target_distance": target_distance,
        "max_favorable_move": max_favorable_move,
        "suggested_classification": suggested_classification,
        "confirmation_index": confirmation_index,
    }


def _row_line(row: dict[str, str]) -> str:
    return (
        f"- {row['timestamp']} | O:{row['open']} H:{row['high']} L:{row['low']} C:{row['close']} "
        f"V:{row.get('volume', '')} T:{row.get('trade_count', '')} VWAP:{row.get('vwap', '')}"
    )


def _format_match(label: str, level: float, match: BarMatch) -> list[str]:
    return [
        f"- {label}: {level:.2f}",
        f"  nearest_5m_bar: {match.timestamp} | O:{match.open} H:{match.high} L:{match.low} C:{match.close} | distance:{match.distance:.4f}",
    ]


def render_manual_review_packet(repo_root: Path, replay_case_path: Path) -> str:
    case = load_replay_case(replay_case_path)
    rows_1d = [row for row in load_ohlcv_rows(_resolve_path(repo_root, case.data_files[0])) if case.date_window.split(" to ")[0] <= row["timestamp"][:10] <= case.date_window.split(" to ")[1]]
    rows_5m = [row for row in load_ohlcv_rows(_resolve_path(repo_root, case.data_files[1])) if case.date_window.split(" to ")[0] <= row["timestamp"][:10] <= case.date_window.split(" to ")[1]]

    support_level = float(rows_1d[0]["low"])
    resistance_level = float(max(rows_1d, key=lambda row: float(row["high"]))["high"])
    if case.symbol == "SPY":
        target_price = 418.0
    elif case.symbol == "NVDA":
        target_price = 323.0
    else:
        target_price = resistance_level + 2.0
    invalidation_level = support_level - (0.05 if case.symbol == "SPY" else 0.10)
    entry_candidate_price = resistance_level + (0.05 if case.symbol == "SPY" else 0.10)
    room_to_target = target_price - entry_candidate_price

    analysis = analyze_level_interactions(
        rows_5m,
        support_level=support_level,
        resistance_level=resistance_level,
        target_price=target_price,
        invalidation_level=invalidation_level,
    )

    target_already_hit_before_confirmation = analysis["target_already_hit_before_confirmation"]
    target_hit_after_confirmation = analysis["target_hit_after_confirmation"]

    lines = [
        f"# {case.replay_id} Manual Visual Review Packet",
        "",
        "## Replay case metadata",
        f"- replay_id: {case.replay_id}",
        f"- related_candidate_id: {case.related_candidate_id}",
        f"- symbol: {case.symbol}",
        f"- date_window: {case.date_window}",
        f"- timeframe_stack: {case.timeframe_stack}",
        "- data files:",
    ]
    lines.extend(f"  - {item}" for item in case.data_files)
    lines.extend([
        f"- data_quality_status: {case.data_quality_status}",
        "",
        "## 1D OHLCV rows for the replay window",
    ])
    lines.extend(_row_line(row) for row in rows_1d)
    lines.extend([
        "",
        "## 5m OHLCV excerpt for the replay window",
    ])
    excerpt_head = 12
    excerpt_tail = 12
    if len(rows_5m) > excerpt_head + excerpt_tail:
        for row in rows_5m[:excerpt_head]:
            lines.append(_row_line(row))
        lines.append(f"- ... {len(rows_5m) - excerpt_head - excerpt_tail} middle rows omitted ...")
        for row in rows_5m[-excerpt_tail:]:
            lines.append(_row_line(row))
    else:
        lines.extend(_row_line(row) for row in rows_5m)

    lines.extend([
        "",
        "## Level interaction analysis",
    ])
    for label, level, match in [
        ("support_level", support_level, analysis["support"]),
        ("resistance_level", resistance_level, analysis["resistance"]),
        ("target_price", target_price, analysis["target"]),
        ("invalidation_level", invalidation_level, analysis["invalidation"]),
    ]:
        lines.extend(_format_match(label, level, match))
    lines.extend([
        f"- any 5m close above resistance: {str(analysis['close_above_resistance']).lower()}",
        f"- any 5m high touched/exceeded resistance: {str(analysis['resistance_touched']).lower()}",
        f"- any 5m close reached/exceeded target: {str(analysis['target_close_hit']).lower()}",
        f"- target hit before confirmation: {str(target_already_hit_before_confirmation).lower()}",
        f"- target hit after confirmation: {str(target_hit_after_confirmation).lower()}",
        f"- invalidation hit before confirmation: {str(analysis['invalidation_hit_before_confirmation']).lower()}",
        f"- invalidation hit after confirmation: {str(analysis['invalidation_hit_after_confirmation']).lower()}",
        "",
        "## Candidate chart-level worksheet",
        f"- proposed support_level: {support_level:.2f}",
        f"- proposed resistance_level: {resistance_level:.2f}",
        f"- proposed target_price: {target_price:.2f}",
        f"- proposed invalidation_level: {invalidation_level:.2f}",
        f"- entry_candidate_price: {entry_candidate_price:.2f}",
        f"- room_to_target: {room_to_target:.2f}",
        f"- target_distance: {analysis['target_distance']:.2f}",
        f"- max_favorable_move: {analysis['max_favorable_move']:.2f}",
        f"- higher_timeframe_obstacle_check: TBD — manual chart review required",
        f"- target_already_hit_check: {'true' if target_already_hit_before_confirmation else 'false'}",
        "",
        "## Candidate event summary",
        f"- resistance_touched: {str(analysis['resistance_touched']).lower()}",
        f"- close_above_resistance: {str(analysis['close_above_resistance']).lower()}",
        f"- target_hit_before_confirmation: {str(target_already_hit_before_confirmation).lower()}",
        f"- target_hit_after_confirmation: {str(target_hit_after_confirmation).lower()}",
        f"- invalidation_hit: {str(analysis['invalidation_hit']).lower()}",
        f"- invalidation_hit_after_confirmation: {str(analysis['invalidation_hit_after_confirmation']).lower()}",
        f"- max_high_after_confirmation: {analysis['max_high_after_confirmation']:.2f}",
        f"- max_close_after_confirmation: {analysis['max_close_after_confirmation']:.2f}",
        f"- target_distance: {analysis['target_distance']:.2f}",
        f"- max_favorable_move: {analysis['max_favorable_move']:.2f}",
        f"- target_already_hit_before_confirmation: {str(target_already_hit_before_confirmation).lower()}",
        f"- suggested_classification: {analysis['suggested_classification']}",
        "",
        "## Manual promotion workflow",
        f"- manual_review_status: {case.manual_review_status or 'pending'}",
        f"- manual_review_outcome: {case.manual_review_outcome or 'TBD'}",
        f"- manual_review_classification: {case.manual_review_classification or 'TBD'}",
        f"- manual_reviewer_notes: {case.manual_reviewer_notes or 'TBD'}",
        f"- broker_action_allowed: {str(case.broker_action_allowed if case.raw.get('broker_action_allowed') is not None else False).lower()}",
        "",
        "## Manual visual review checklist",
    ])
    for item in [
        "Is support defensible?",
        "Is resistance defensible?",
        "Is target defensible?",
        "Is invalidation defensible?",
        "Did price close above resistance?",
        "Did price only wick/tap resistance?",
        "Did price reach target?",
        "Was target already hit before confirmation?",
        "Did target hit after confirmation?",
        "Did invalidation hit after confirmation?",
        "Was there a higher-timeframe obstacle?",
        "Was the case confirmed, ambiguous, insufficient, contradicted, or watch/no-trigger?",
    ]:
        lines.append(f"- [ ] {item}")
    lines.extend([
        "",
        "## Recommended classification options",
    ])
    for item in [
        "confirmed_breakout",
        "confirmed_breakout_no_target_hit",
        "failed_breakout",
        "watch_no_trigger",
        "ambiguous",
        "insufficient",
        "contradicted",
        "blocked_data_quality",
    ]:
        lines.append(f"- {item}")
    lines.extend([
        "",
        "## Boundary",
        "- No trade signal",
        "- No profitability claim",
        "- No execution readiness",
        "- No broker action allowed",
    ])
    return "\n".join(lines) + "\n"


def write_manual_review_packet(repo_root: Path, replay_case_path: Path, output_path: Path | None = None) -> Path:
    output_path = output_path or repo_root / "runs" / "replay" / f"{load_replay_case(replay_case_path).replay_id}_manual_review_packet.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_manual_review_packet(repo_root, replay_case_path))
    return output_path
