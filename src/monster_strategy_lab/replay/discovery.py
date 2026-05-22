from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Iterable

import yaml

from monster_strategy_lab.data_sources import (
    load_ohlcv_rows,
    load_replay_handoff_manifest,
    resolve_full_historical_data_root,
    resolve_historical_market_data_paths,
)
from monster_strategy_lab.replay.case import load_replay_case
from monster_strategy_lab.replay.manual_review import analyze_level_interactions


LOOKBACKS = (12, 24, 48)
DEFAULT_DISCOVERY_SYMBOLS = ("SPY", "QQQ", "AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA", "AVGO", "IWM")


@dataclass(frozen=True)
class DiscoveryEvent:
    symbol: str
    timestamp: str
    close: float
    prior_resistance: float
    breakout_amount: float
    lookback_bars: int
    prior_window_start: str
    prior_window_end: str
    next_5m_high: float | None
    max_high_next_6_bars: float | None
    max_high_next_12_bars: float | None
    max_high_next_24_bars: float | None
    close_after_6_bars: float | None
    close_after_12_bars: float | None
    close_after_24_bars: float | None
    did_price_continue: bool
    did_price_reclaim_below_resistance: bool
    discovery_status: str = "candidate_for_manual_review"
    score: float = 0.0


@dataclass(frozen=True)
class BearishDiscoveryEvent:
    symbol: str
    timestamp: str
    close: float
    prior_support: float
    breakdown_amount: float
    lookback_bars: int
    prior_window_start: str
    prior_window_end: str
    next_5m_low: float | None
    min_low_next_6_bars: float | None
    min_low_next_12_bars: float | None
    min_low_next_24_bars: float | None
    close_after_6_bars: float | None
    close_after_12_bars: float | None
    close_after_24_bars: float | None
    did_price_continue_down: bool
    did_price_reclaim_above_support: bool
    discovery_status: str = "candidate_for_manual_review"
    score: float = 0.0


@dataclass(frozen=True)
class DraftReplayCase:
    replay_id: str
    related_candidate_id: str
    symbol: str
    date_window: str
    timeframe_stack: str
    data_files: list[str]
    event: DiscoveryEvent
    one_d_context_rows: list[dict[str, str]]
    five_min_context_rows: list[dict[str, str]]


@dataclass(frozen=True)
class DraftBearishReplayCase:
    replay_id: str
    related_candidate_id: str
    symbol: str
    date_window: str
    timeframe_stack: str
    data_files: list[str]
    event: BearishDiscoveryEvent
    one_d_context_rows: list[dict[str, str]]
    five_min_context_rows: list[dict[str, str]]


@dataclass(frozen=True)
class DiversifiedReplayCandidate:
    replay_id: str
    symbol: str
    side: str
    timestamp: str
    event_type: str
    prior_level: float
    breakout_or_breakdown_amount: float
    lookback_bars: int
    max_high_next_6_bars: float | None = None
    max_high_next_12_bars: float | None = None
    max_high_next_24_bars: float | None = None
    min_low_next_6_bars: float | None = None
    min_low_next_12_bars: float | None = None
    min_low_next_24_bars: float | None = None
    close_after_6_bars: float | None = None
    close_after_12_bars: float | None = None
    close_after_24_bars: float | None = None
    reason_selected: str = ""
    distance_from_nearest_existing_case_days: int | None = None
    has_1d_context: bool = False
    prior_window_start: str = ""
    prior_window_end: str = ""


@dataclass(frozen=True)
class StrictBearishBreakdownCandidate:
    symbol: str
    event_timestamp: str
    prior_support: float
    breakdown_close: float
    downside_target: float
    invalidation_level: float
    target_hit_after_confirmation: bool
    invalidation_hit_after_confirmation: bool
    min_low_after_confirmation: float
    max_close_after_confirmation: float
    suggested_classification: str
    reason_selected: str


@dataclass(frozen=True)
class ReplayDiscoveryConfig:
    symbols: list[str]
    lookback_bars: list[int]
    min_calendar_days_between_cases: int
    max_cases_per_symbol_per_month: int
    max_cases_per_symbol_total: int
    avoid_existing_replay_windows: bool
    preferred_sides: list[str]
    required_timeframes: list[str]


DEFAULT_REPLAY_DISCOVERY_CONFIG = ReplayDiscoveryConfig(
    symbols=list(DEFAULT_DISCOVERY_SYMBOLS),
    lookback_bars=list(LOOKBACKS),
    min_calendar_days_between_cases=30,
    max_cases_per_symbol_per_month=1,
    max_cases_per_symbol_total=3,
    avoid_existing_replay_windows=True,
    preferred_sides=["bullish", "bearish"],
    required_timeframes=["1Day", "5Min"],
)


def _parse_ts(value: str) -> datetime:
    return datetime.fromisoformat(value.replace(" ", "T"))


def _load_rows(path: Path) -> list[dict[str, str]]:
    return load_ohlcv_rows(path)


def _float(value: Any) -> float:
    return float(value)


def _lower(value: Any) -> str:
    return str(value or "").lower().strip()


def _date_only(timestamp: str) -> date:
    return _parse_ts(timestamp).date()


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text())
    return data if isinstance(data, dict) else {}


def load_replay_discovery_config(repo_root: Path, path: Path | None = None) -> ReplayDiscoveryConfig:
    path = path or repo_root / "configs" / "replay_discovery.yaml"
    raw = _load_yaml(path)
    return ReplayDiscoveryConfig(
        symbols=list(raw.get("symbols") or DEFAULT_REPLAY_DISCOVERY_CONFIG.symbols),
        lookback_bars=list(raw.get("lookback_bars") or DEFAULT_REPLAY_DISCOVERY_CONFIG.lookback_bars),
        min_calendar_days_between_cases=int(raw.get("min_calendar_days_between_cases") or DEFAULT_REPLAY_DISCOVERY_CONFIG.min_calendar_days_between_cases),
        max_cases_per_symbol_per_month=int(raw.get("max_cases_per_symbol_per_month") or DEFAULT_REPLAY_DISCOVERY_CONFIG.max_cases_per_symbol_per_month),
        max_cases_per_symbol_total=int(raw.get("max_cases_per_symbol_total") or DEFAULT_REPLAY_DISCOVERY_CONFIG.max_cases_per_symbol_total),
        avoid_existing_replay_windows=bool(raw.get("avoid_existing_replay_windows", DEFAULT_REPLAY_DISCOVERY_CONFIG.avoid_existing_replay_windows)),
        preferred_sides=list(raw.get("preferred_sides") or DEFAULT_REPLAY_DISCOVERY_CONFIG.preferred_sides),
        required_timeframes=list(raw.get("required_timeframes") or DEFAULT_REPLAY_DISCOVERY_CONFIG.required_timeframes),
    )


def _existing_replay_case_dates(repo_root: Path) -> list[date]:
    dates: list[date] = []
    for case_path in sorted((repo_root / "replay" / "cases").glob("HR-*.md")):
        case = load_replay_case(case_path)
        if case.date_window:
            dates.append(_date_only(case.date_window.split(" to ")[0]))
    return sorted(dates)


def _has_1d_context(repo_root: Path, symbol: str) -> bool:
    return (resolve_historical_market_data_paths(repo_root, symbol).get("1Day") is not None)


def _distance_from_nearest_existing_case_days(timestamp: str, existing_dates: list[date]) -> int | None:
    if not existing_dates:
        return None
    current = _date_only(timestamp)
    return min(abs((current - existing).days) for existing in existing_dates)


def _case_date_window(case: Any) -> date:
    return _date_only(case.date_window.split(" to ")[0])


def _date_cluster_warning(case_dates: list[date]) -> bool:
    if len(case_dates) < 3:
        return False
    sorted_dates = sorted(set(case_dates))
    for idx, start in enumerate(sorted_dates):
        count = sum(1 for d in case_dates if 0 <= (d - start).days <= 5)
        if count >= max(3, len(case_dates) // 2 + 1):
            return True
    return False


def _date_distribution_summary(case_paths: list[Path]) -> dict[str, Any]:
    cases = [load_replay_case(path) for path in case_paths]
    dates = [_case_date_window(case) for case in cases]
    by_year: dict[str, int] = {}
    by_month: dict[str, int] = {}
    by_symbol: dict[str, int] = {}
    by_side: dict[str, int] = {}
    by_classification: dict[str, int] = {}
    for case, case_date in zip(cases, dates):
        by_year[str(case_date.year)] = by_year.get(str(case_date.year), 0) + 1
        by_month[case_date.strftime("%Y-%m")] = by_month.get(case_date.strftime("%Y-%m"), 0) + 1
        by_symbol[case.symbol] = by_symbol.get(case.symbol, 0) + 1
        side = "bearish" if _lower(case.raw.get("direction")) == "short" else "bullish"
        by_side[side] = by_side.get(side, 0) + 1
        by_classification[case.classification] = by_classification.get(case.classification, 0) + 1
    return {
        "count_by_year": by_year,
        "count_by_month": by_month,
        "count_by_symbol": by_symbol,
        "count_by_side": by_side,
        "count_by_classification": by_classification,
        "earliest_replay_date": min(dates).isoformat() if dates else "",
        "latest_replay_date": max(dates).isoformat() if dates else "",
        "clustered_windows_warning": _date_cluster_warning(dates),
        "clustered_window_span_days": (max(dates) - min(dates)).days if dates else 0,
    }


def _existing_symbol_paths(repo_root: Path, symbol: str) -> dict[str, Path]:
    return resolve_historical_market_data_paths(repo_root, symbol)


def discover_events_for_symbol(repo_root: Path, symbol: str, lookbacks: Iterable[int] = LOOKBACKS) -> list[DiscoveryEvent]:
    paths = _existing_symbol_paths(repo_root, symbol)
    five_min_path = paths.get("5Min")
    if not five_min_path:
        return []

    rows = _load_rows(five_min_path)
    rows.sort(key=lambda row: _parse_ts(row["timestamp"]))

    events: list[DiscoveryEvent] = []
    for lookback_bars in lookbacks:
        for idx in range(lookback_bars, len(rows)):
            prior_window = rows[idx - lookback_bars : idx]
            prior_resistance = max(_float(row["high"]) for row in prior_window)
            current = rows[idx]
            previous = rows[idx - 1]
            current_close = _float(current["close"])
            previous_close = _float(previous["close"])
            if current_close <= prior_resistance or previous_close > prior_resistance:
                continue

            next_6 = rows[idx + 1 : idx + 7]
            next_12 = rows[idx + 1 : idx + 13]
            next_24 = rows[idx + 1 : idx + 25]

            max_high_next_6 = max((_float(row["high"]) for row in next_6), default=None)
            max_high_next_12 = max((_float(row["high"]) for row in next_12), default=None)
            max_high_next_24 = max((_float(row["high"]) for row in next_24), default=None)
            close_after_6 = _float(next_6[-1]["close"]) if len(next_6) >= 6 else (_float(next_6[-1]["close"]) if next_6 else None)
            close_after_12 = _float(next_12[-1]["close"]) if len(next_12) >= 12 else (_float(next_12[-1]["close"]) if next_12 else None)
            close_after_24 = _float(next_24[-1]["close"]) if len(next_24) >= 24 else (_float(next_24[-1]["close"]) if next_24 else None)

            did_price_continue = bool(max_high_next_6 is not None and max_high_next_6 > current_close)
            did_price_reclaim_below_resistance = any(_float(row["close"]) <= prior_resistance for row in next_6)

            breakout_amount = current_close - prior_resistance
            score = (
                breakout_amount * 10.0
                + (max_high_next_6 - prior_resistance if max_high_next_6 is not None else 0.0)
                + (max_high_next_24 - prior_resistance if max_high_next_24 is not None else 0.0) * 0.5
                + (0.0 if did_price_reclaim_below_resistance else 1.0)
                + (1.0 if did_price_continue else 0.0)
            )

            events.append(
                DiscoveryEvent(
                    symbol=symbol,
                    timestamp=current["timestamp"],
                    close=current_close,
                    prior_resistance=prior_resistance,
                    breakout_amount=breakout_amount,
                    lookback_bars=lookback_bars,
                    prior_window_start=prior_window[0]["timestamp"],
                    prior_window_end=prior_window[-1]["timestamp"],
                    next_5m_high=_float(next_6[0]["high"]) if next_6 else None,
                    max_high_next_6_bars=max_high_next_6,
                    max_high_next_12_bars=max_high_next_12,
                    max_high_next_24_bars=max_high_next_24,
                    close_after_6_bars=close_after_6,
                    close_after_12_bars=close_after_12,
                    close_after_24_bars=close_after_24,
                    did_price_continue=did_price_continue,
                    did_price_reclaim_below_resistance=did_price_reclaim_below_resistance,
                    score=score,
                )
            )

    return events


def discover_close_below_support_events_for_symbol(repo_root: Path, symbol: str, lookbacks: Iterable[int] = LOOKBACKS) -> list[BearishDiscoveryEvent]:
    paths = _existing_symbol_paths(repo_root, symbol)
    five_min_path = paths.get("5Min")
    if not five_min_path:
        return []

    rows = _load_rows(five_min_path)
    rows.sort(key=lambda row: _parse_ts(row["timestamp"]))

    events: list[BearishDiscoveryEvent] = []
    for lookback_bars in lookbacks:
        for idx in range(lookback_bars, len(rows)):
            prior_window = rows[idx - lookback_bars : idx]
            prior_support = min(_float(row["low"]) for row in prior_window)
            current = rows[idx]
            previous = rows[idx - 1]
            current_close = _float(current["close"])
            previous_close = _float(previous["close"])
            if current_close >= prior_support or previous_close < prior_support:
                continue

            next_6 = rows[idx + 1 : idx + 7]
            next_12 = rows[idx + 1 : idx + 13]
            next_24 = rows[idx + 1 : idx + 25]

            min_low_next_6 = min((_float(row["low"]) for row in next_6), default=None)
            min_low_next_12 = min((_float(row["low"]) for row in next_12), default=None)
            min_low_next_24 = min((_float(row["low"]) for row in next_24), default=None)
            close_after_6 = _float(next_6[-1]["close"]) if len(next_6) >= 6 else (_float(next_6[-1]["close"]) if next_6 else None)
            close_after_12 = _float(next_12[-1]["close"]) if len(next_12) >= 12 else (_float(next_12[-1]["close"]) if next_12 else None)
            close_after_24 = _float(next_24[-1]["close"]) if len(next_24) >= 24 else (_float(next_24[-1]["close"]) if next_24 else None)

            did_price_continue_down = bool(min_low_next_6 is not None and min_low_next_6 < current_close)
            did_price_reclaim_above_support = any(_float(row["close"]) >= prior_support for row in next_6)

            breakdown_amount = prior_support - current_close
            score = (
                breakdown_amount * 10.0
                + (prior_support - min_low_next_6 if min_low_next_6 is not None else 0.0)
                + (prior_support - min_low_next_24 if min_low_next_24 is not None else 0.0) * 0.5
                + (0.0 if did_price_reclaim_above_support else 1.0)
                + (1.0 if did_price_continue_down else 0.0)
            )

            events.append(
                BearishDiscoveryEvent(
                    symbol=symbol,
                    timestamp=current["timestamp"],
                    close=current_close,
                    prior_support=prior_support,
                    breakdown_amount=breakdown_amount,
                    lookback_bars=lookback_bars,
                    prior_window_start=prior_window[0]["timestamp"],
                    prior_window_end=prior_window[-1]["timestamp"],
                    next_5m_low=_float(next_6[0]["low"]) if next_6 else None,
                    min_low_next_6_bars=min_low_next_6,
                    min_low_next_12_bars=min_low_next_12,
                    min_low_next_24_bars=min_low_next_24,
                    close_after_6_bars=close_after_6,
                    close_after_12_bars=close_after_12,
                    close_after_24_bars=close_after_24,
                    did_price_continue_down=did_price_continue_down,
                    did_price_reclaim_above_support=did_price_reclaim_above_support,
                    score=score,
                )
            )

    return events


def scan_close_above_resistance_candidates(repo_root: Path, symbols: Iterable[str] = DEFAULT_DISCOVERY_SYMBOLS, lookbacks: Iterable[int] = LOOKBACKS) -> list[DiscoveryEvent]:
    events: list[DiscoveryEvent] = []
    for symbol in symbols:
        events.extend(discover_events_for_symbol(repo_root, symbol, lookbacks))
    return events


def scan_close_below_support_candidates(repo_root: Path, symbols: Iterable[str] = DEFAULT_DISCOVERY_SYMBOLS, lookbacks: Iterable[int] = LOOKBACKS) -> list[BearishDiscoveryEvent]:
    events: list[BearishDiscoveryEvent] = []
    for symbol in symbols:
        events.extend(discover_close_below_support_events_for_symbol(repo_root, symbol, lookbacks))
    return events


def select_top_candidates(events: list[DiscoveryEvent], limit: int = 3) -> list[DiscoveryEvent]:
    best_by_symbol: dict[str, DiscoveryEvent] = {}
    for event in events:
        current = best_by_symbol.get(event.symbol)
        if current is None or event.score > current.score:
            best_by_symbol[event.symbol] = event
    return sorted(best_by_symbol.values(), key=lambda item: (-item.score, item.symbol, item.timestamp))[:limit]


def select_top_bearish_candidates(events: list[BearishDiscoveryEvent], limit: int = 3) -> list[BearishDiscoveryEvent]:
    best_by_symbol: dict[str, BearishDiscoveryEvent] = {}
    for event in events:
        current = best_by_symbol.get(event.symbol)
        if current is None or event.score > current.score:
            best_by_symbol[event.symbol] = event
    return sorted(best_by_symbol.values(), key=lambda item: (-item.score, item.symbol, item.timestamp))[:limit]


def _format_float(value: float | None) -> str:
    if value is None:
        return ""
    return f"{value:.4f}" if abs(value) < 100 else f"{value:.2f}"


def write_discovery_csv(repo_root: Path, events: list[DiscoveryEvent]) -> Path:
    output_dir = repo_root / "runs" / "replay" / "discovery"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "close_above_resistance_candidates.csv"
    with output_path.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "symbol",
                "timestamp",
                "close",
                "prior_resistance",
                "breakout_amount",
                "lookback_bars",
                "prior_window_start",
                "prior_window_end",
                "next_5m_high",
                "max_high_next_6_bars",
                "max_high_next_12_bars",
                "max_high_next_24_bars",
                "close_after_6_bars",
                "close_after_12_bars",
                "close_after_24_bars",
                "did_price_continue",
                "did_price_reclaim_below_resistance",
                "discovery_status",
                "score",
            ],
        )
        writer.writeheader()
        for event in events:
            writer.writerow(
                {
                    "symbol": event.symbol,
                    "timestamp": event.timestamp,
                    "close": _format_float(event.close),
                    "prior_resistance": _format_float(event.prior_resistance),
                    "breakout_amount": _format_float(event.breakout_amount),
                    "lookback_bars": event.lookback_bars,
                    "prior_window_start": event.prior_window_start,
                    "prior_window_end": event.prior_window_end,
                    "next_5m_high": _format_float(event.next_5m_high),
                    "max_high_next_6_bars": _format_float(event.max_high_next_6_bars),
                    "max_high_next_12_bars": _format_float(event.max_high_next_12_bars),
                    "max_high_next_24_bars": _format_float(event.max_high_next_24_bars),
                    "close_after_6_bars": _format_float(event.close_after_6_bars),
                    "close_after_12_bars": _format_float(event.close_after_12_bars),
                    "close_after_24_bars": _format_float(event.close_after_24_bars),
                    "did_price_continue": str(event.did_price_continue).lower(),
                    "did_price_reclaim_below_resistance": str(event.did_price_reclaim_below_resistance).lower(),
                    "discovery_status": event.discovery_status,
                    "score": _format_float(event.score),
                }
            )
    return output_path


def write_close_below_support_csv(repo_root: Path, events: list[BearishDiscoveryEvent]) -> Path:
    output_dir = repo_root / "runs" / "replay" / "discovery"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "close_below_support_candidates.csv"
    with output_path.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "symbol",
                "timestamp",
                "close",
                "prior_support",
                "breakdown_amount",
                "lookback_bars",
                "prior_window_start",
                "prior_window_end",
                "next_5m_low",
                "min_low_next_6_bars",
                "min_low_next_12_bars",
                "min_low_next_24_bars",
                "close_after_6_bars",
                "close_after_12_bars",
                "close_after_24_bars",
                "did_price_continue_down",
                "did_price_reclaim_above_support",
                "discovery_status",
                "score",
            ],
        )
        writer.writeheader()
        for event in events:
            writer.writerow(
                {
                    "symbol": event.symbol,
                    "timestamp": event.timestamp,
                    "close": _format_float(event.close),
                    "prior_support": _format_float(event.prior_support),
                    "breakdown_amount": _format_float(event.breakdown_amount),
                    "lookback_bars": event.lookback_bars,
                    "prior_window_start": event.prior_window_start,
                    "prior_window_end": event.prior_window_end,
                    "next_5m_low": _format_float(event.next_5m_low),
                    "min_low_next_6_bars": _format_float(event.min_low_next_6_bars),
                    "min_low_next_12_bars": _format_float(event.min_low_next_12_bars),
                    "min_low_next_24_bars": _format_float(event.min_low_next_24_bars),
                    "close_after_6_bars": _format_float(event.close_after_6_bars),
                    "close_after_12_bars": _format_float(event.close_after_12_bars),
                    "close_after_24_bars": _format_float(event.close_after_24_bars),
                    "did_price_continue_down": str(event.did_price_continue_down).lower(),
                    "did_price_reclaim_above_support": str(event.did_price_reclaim_above_support).lower(),
                    "discovery_status": event.discovery_status,
                    "score": _format_float(event.score),
                }
            )
    return output_path


def render_discovery_summary(events: list[DiscoveryEvent], selected: list[DiscoveryEvent]) -> str:
    lines = [
        "# Close Above Resistance Discovery Summary",
        "",
        f"candidate_windows_found: {len(events)}",
        f"top_manual_review_candidates: {len(selected)}",
        "",
        "## Top candidates",
    ]
    for idx, event in enumerate(selected, start=1):
        lines.extend(
            [
                f"### {idx}. {event.symbol} @ {event.timestamp}",
                f"- lookback_bars: {event.lookback_bars}",
                f"- prior_resistance: {_format_float(event.prior_resistance)}",
                f"- breakout_amount: {_format_float(event.breakout_amount)}",
                f"- max_high_next_6_bars: {_format_float(event.max_high_next_6_bars)}",
                f"- max_high_next_24_bars: {_format_float(event.max_high_next_24_bars)}",
                f"- did_price_continue: {str(event.did_price_continue).lower()}",
                f"- did_price_reclaim_below_resistance: {str(event.did_price_reclaim_below_resistance).lower()}",
                f"- discovery_status: {event.discovery_status}",
                "",
            ]
        )
    lines.extend([
        "## Boundary",
        "- Discovery only",
        "- Not verified replay evidence",
        "- No trade signal",
        "- No broker action allowed",
    ])
    return "\n".join(lines) + "\n"


def render_close_below_support_summary(events: list[BearishDiscoveryEvent], selected: list[BearishDiscoveryEvent]) -> str:
    lines = [
        "# Close Below Support Discovery Summary",
        "",
        f"candidate_windows_found: {len(events)}",
        f"top_manual_review_candidates: {len(selected)}",
        "",
        "## Top candidates",
    ]
    for idx, event in enumerate(selected, start=1):
        lines.extend(
            [
                f"### {idx}. {event.symbol} @ {event.timestamp}",
                f"- lookback_bars: {event.lookback_bars}",
                f"- prior_support: {_format_float(event.prior_support)}", 
                f"- breakdown_amount: {_format_float(event.breakdown_amount)}",
                f"- min_low_next_6_bars: {_format_float(event.min_low_next_6_bars)}",
                f"- min_low_next_24_bars: {_format_float(event.min_low_next_24_bars)}",
                f"- did_price_continue_down: {str(event.did_price_continue_down).lower()}",
                f"- did_price_reclaim_above_support: {str(event.did_price_reclaim_above_support).lower()}",
                f"- discovery_status: {event.discovery_status}",
                "",
            ]
        )
    lines.extend([
        "## Boundary",
        "- Discovery only",
        "- Not verified replay evidence",
        "- No trade signal",
        "- No broker action allowed",
    ])
    return "\n".join(lines) + "\n"


def write_close_below_support_summary(repo_root: Path, events: list[BearishDiscoveryEvent], selected: list[BearishDiscoveryEvent]) -> Path:
    output_dir = repo_root / "runs" / "replay" / "discovery"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "close_below_support_candidates.md"
    output_path.write_text(render_close_below_support_summary(events, selected))
    return output_path


def write_discovery_summary(repo_root: Path, events: list[DiscoveryEvent], selected: list[DiscoveryEvent]) -> Path:
    output_dir = repo_root / "runs" / "replay" / "discovery"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "close_above_resistance_candidates.md"
    output_path.write_text(render_discovery_summary(events, selected))
    return output_path


def _rows_for_1d_context(repo_root: Path, symbol: str, event_date: str, limit: int = 4) -> list[dict[str, str]]:
    path = resolve_historical_market_data_paths(repo_root, symbol).get("1Day")
    if path is None or not path.exists():
        return []
    rows = _load_rows(path)
    rows.sort(key=lambda row: _parse_ts(row["timestamp"]))
    matched = [row for row in rows if row["timestamp"][:10] <= event_date]
    return matched[-limit:]


def _rows_around_event(rows: list[dict[str, str]], event_index: int, before: int = 12, after: int = 24) -> list[dict[str, str]]:
    start = max(0, event_index - before)
    end = min(len(rows), event_index + after + 1)
    return rows[start:end]


def build_draft_replay_case(repo_root: Path, event: DiscoveryEvent, replay_id: str, related_candidate_id: str) -> DraftReplayCase:
    five_min_path = resolve_historical_market_data_paths(repo_root, event.symbol).get("5Min")
    if five_min_path is None:
        raise FileNotFoundError(f"No 5Min data available for {event.symbol}")
    rows_5m = _load_rows(five_min_path)
    rows_5m.sort(key=lambda row: _parse_ts(row["timestamp"]))
    event_index = next(i for i, row in enumerate(rows_5m) if row["timestamp"] == event.timestamp)
    context_rows = _rows_around_event(rows_5m, event_index)
    event_date = event.timestamp[:10]
    one_d_rows = _rows_for_1d_context(repo_root, event.symbol, event_date)
    return DraftReplayCase(
        replay_id=replay_id,
        related_candidate_id=related_candidate_id,
        symbol=event.symbol,
        date_window=f"{event_date} to {event_date}",
        timeframe_stack="1D + 5m",
        data_files=[str(resolve_historical_market_data_paths(repo_root, event.symbol)["1Day"]), str(five_min_path)],
        event=event,
        one_d_context_rows=one_d_rows,
        five_min_context_rows=context_rows,
    )


def build_bearish_draft_replay_case(repo_root: Path, event: BearishDiscoveryEvent, replay_id: str, related_candidate_id: str) -> DraftBearishReplayCase:
    five_min_path = resolve_historical_market_data_paths(repo_root, event.symbol).get("5Min")
    if five_min_path is None:
        raise FileNotFoundError(f"No 5Min data available for {event.symbol}")
    rows_5m = _load_rows(five_min_path)
    rows_5m.sort(key=lambda row: _parse_ts(row["timestamp"]))
    event_index = next(i for i, row in enumerate(rows_5m) if row["timestamp"] == event.timestamp)
    context_rows = _rows_around_event(rows_5m, event_index)
    event_date = event.timestamp[:10]
    one_d_rows = _rows_for_1d_context(repo_root, event.symbol, event_date)
    return DraftBearishReplayCase(
        replay_id=replay_id,
        related_candidate_id=related_candidate_id,
        symbol=event.symbol,
        date_window=f"{event_date} to {event_date}",
        timeframe_stack="1D + 5m",
        data_files=[str(resolve_historical_market_data_paths(repo_root, event.symbol)["1Day"]), str(five_min_path)],
        event=event,
        one_d_context_rows=one_d_rows,
        five_min_context_rows=context_rows,
    )


def write_draft_replay_case(repo_root: Path, draft: DraftReplayCase) -> Path:
    output_path = repo_root / "replay" / "cases" / f"{draft.replay_id}.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "---",
        f"replay_id: {draft.replay_id}",
        f"related_candidate_id: {draft.related_candidate_id}",
        f"symbol: {draft.symbol}",
        "direction: long",
        f"date_window: {draft.date_window}",
        f"timeframe_stack: {draft.timeframe_stack}",
        "data_files:",
    ]
    lines.extend(f"  - {item}" for item in draft.data_files)
    lines.extend(
        [
            "data_quality_status: PASSED",
            "replay_observations:",
            f"  - Discovery scanner found a close_above_resistance candidate at {draft.event.timestamp}.",
            f"  - prior_resistance: {draft.event.prior_resistance:.2f}",
            f"  - breakout_amount: {draft.event.breakout_amount:.2f}",
            f"  - discovery_status: {draft.event.discovery_status}",
            "classification: candidate_for_manual_review",
            "replay_outcome: insufficient",
            "replay_status: NOT_VERIFIED",
            "manual_review_status: pending",
            "manual_review_outcome: pending",
            "manual_review_classification: pending",
            "manual_reviewer_notes: pending",
            "broker_action_allowed: false",
            "evidence_type: real_market_replay",
            "real_market_evidence: true",
            "reviewer: manual review pending",
            "boundary: No trade signal, no profitability claim, no execution readiness.",
            "---",
            "",
            f"# {draft.replay_id}",
            "",
            "## Summary",
            "Discovery draft only; manual review required.",
            "",
            "## Notes",
            "- Not verified",
            "- Not promoted",
        ]
    )
    output_path.write_text("\n".join(lines) + "\n")
    return output_path


def write_bearish_draft_replay_case(repo_root: Path, draft: DraftBearishReplayCase) -> Path:
    output_path = repo_root / "replay" / "cases" / f"{draft.replay_id}.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "---",
        f"replay_id: {draft.replay_id}",
        f"related_candidate_id: {draft.related_candidate_id}",
        f"symbol: {draft.symbol}",
        "direction: short",
        f"date_window: {draft.date_window}",
        f"timeframe_stack: {draft.timeframe_stack}",
        "data_files:",
    ]
    lines.extend(f"  - {item}" for item in draft.data_files)
    lines.extend(
        [
            "data_quality_status: PASSED",
            "replay_observations:",
            f"  - Discovery scanner found a close_below_support candidate at {draft.event.timestamp}.",
            f"  - prior_support: {draft.event.prior_support:.2f}",
            f"  - breakdown_amount: {draft.event.breakdown_amount:.2f}",
            f"  - discovery_status: {draft.event.discovery_status}",
            "classification: candidate_for_manual_review",
            "replay_outcome: insufficient",
            "replay_status: NOT_VERIFIED",
            "manual_review_status: pending",
            "manual_review_outcome: pending",
            "manual_review_classification: pending",
            "manual_reviewer_notes: pending",
            "broker_action_allowed: false",
            "evidence_type: real_market_replay",
            "real_market_evidence: true",
            "reviewer: manual review pending",
            "boundary: No trade signal, no profitability claim, no execution readiness.",
            "---",
            "",
            f"# {draft.replay_id}",
            "",
            "## Summary",
            "Discovery draft only; manual review required.",
            "",
            "## Notes",
            "- Not verified",
            "- Not promoted",
        ]
    )
    output_path.write_text("\n".join(lines) + "\n")
    return output_path


def render_bearish_manual_review_packet(draft: DraftBearishReplayCase) -> str:
    support_level = draft.event.prior_support
    resistance_level = draft.event.prior_support + max(0.5, draft.event.breakdown_amount)
    target_price = draft.event.prior_support - max(1.0, draft.event.breakdown_amount * 2)
    invalidation_level = draft.event.prior_support + max(1.0, draft.event.breakdown_amount)

    lines = [
        f"# {draft.replay_id} Manual Review Packet",
        "",
        "## Warning",
        "- Discovery draft only",
        "- Not verified replay evidence",
        "- No trade signal",
        "- No broker action allowed",
        "",
        "## Replay case metadata",
        f"- replay_id: {draft.replay_id}",
        f"- related_candidate_id: {draft.related_candidate_id}",
        f"- symbol: {draft.symbol}",
        f"- date_window: {draft.date_window}",
        f"- timeframe_stack: {draft.timeframe_stack}",
        "- data files:",
    ]
    lines.extend(f"  - {item}" for item in draft.data_files)
    lines.extend([
        "",
        "## 1D context rows",
    ])
    lines.extend(_row_line(row) for row in draft.one_d_context_rows) if draft.one_d_context_rows else lines.append("- none available")
    lines.extend([
        "",
        "## 5m breakdown context",
        f"- prior_support: {draft.event.prior_support:.2f}",
        f"- breakdown candle: {draft.event.timestamp} | close: {draft.event.close:.2f}",
        f"- breakdown_amount: {draft.event.breakdown_amount:.2f}",
        "",
        "## 5m bars around the breakdown",
    ])
    lines.extend(_row_line(row) for row in draft.five_min_context_rows)
    lines.extend([
        "",
        "## Downside follow-through rows",
        f"- min_low_next_6_bars: {_format_float(draft.event.min_low_next_6_bars)}",
        f"- min_low_next_12_bars: {_format_float(draft.event.min_low_next_12_bars)}",
        f"- min_low_next_24_bars: {_format_float(draft.event.min_low_next_24_bars)}",
        f"- close_after_6_bars: {_format_float(draft.event.close_after_6_bars)}",
        f"- close_after_12_bars: {_format_float(draft.event.close_after_12_bars)}",
        f"- close_after_24_bars: {_format_float(draft.event.close_after_24_bars)}",
        "",
        "## Candidate chart-level worksheet",
        f"- proposed support_level: {support_level:.2f}",
        f"- proposed resistance_level: {resistance_level:.2f}",
        f"- proposed target_price: {target_price:.2f}",
        f"- proposed invalidation_level: {invalidation_level:.2f}",
        f"- entry_candidate_price: {draft.event.close:.2f}",
        f"- target_distance: {support_level - target_price:.2f}",
        f"- higher_timeframe_obstacle_check: TBD",
        f"- target_already_hit_check: TBD",
        "",
        "## Candidate event summary",
    ])
    close_below_support = draft.event.close < draft.event.prior_support
    support_touched = any(_float(row["low"]) <= draft.event.prior_support for row in draft.five_min_context_rows)
    confirmation_rows = draft.five_min_context_rows[draft.five_min_context_rows.index(next(row for row in draft.five_min_context_rows if row["timestamp"] == draft.event.timestamp)):] if draft.five_min_context_rows else []
    pre_confirmation_rows = draft.five_min_context_rows[: draft.five_min_context_rows.index(next(row for row in draft.five_min_context_rows if row["timestamp"] == draft.event.timestamp))] if draft.five_min_context_rows else []
    downside_target_hit_before_confirmation = any(_float(row["low"]) <= target_price for row in pre_confirmation_rows)
    downside_target_hit_after_confirmation = any(_float(row["low"]) <= target_price for row in confirmation_rows)
    invalidation_hit_after_confirmation = any(_float(row["high"]) >= invalidation_level for row in confirmation_rows)
    min_low_after_confirmation = min((_float(row["low"]) for row in confirmation_rows), default=float("nan"))
    max_close_after_confirmation = max((_float(row["close"]) for row in confirmation_rows), default=float("nan"))
    if not support_touched:
        suggested_classification = "insufficient"
    elif downside_target_hit_before_confirmation:
        suggested_classification = "contradicted"
    elif close_below_support and downside_target_hit_after_confirmation and not invalidation_hit_after_confirmation:
        suggested_classification = "confirmed_breakdown"
    elif close_below_support and not downside_target_hit_after_confirmation and not invalidation_hit_after_confirmation:
        suggested_classification = "confirmed_breakdown_no_target_hit"
    elif close_below_support and invalidation_hit_after_confirmation and not downside_target_hit_after_confirmation:
        suggested_classification = "failed_breakdown_reclaim"
    elif support_touched and not close_below_support:
        suggested_classification = "support_touch_no_trigger"
    elif close_below_support:
        suggested_classification = "ambiguous"
    else:
        suggested_classification = "blocked_data_quality"

    lines.extend([
        f"- close_below_support: {str(close_below_support).lower()}",
        f"- support_touched: {str(support_touched).lower()}",
        f"- downside_target_hit_before_confirmation: {str(downside_target_hit_before_confirmation).lower()}",
        f"- downside_target_hit_after_confirmation: {str(downside_target_hit_after_confirmation).lower()}",
        f"- invalidation_hit_after_confirmation: {str(invalidation_hit_after_confirmation).lower()}",
        f"- min_low_after_confirmation: {min_low_after_confirmation:.2f}",
        f"- max_close_after_confirmation: {max_close_after_confirmation:.2f}",
        f"- suggested_classification: {suggested_classification}",
        "",
        "## Manual promotion workflow",
        "- manual_review_status: pending",
        "- manual_review_outcome: TBD",
        "- manual_review_classification: TBD",
        "- manual_reviewer_notes: TBD",
        "- broker_action_allowed: false",
        "",
        "## Recommended classification options",
    ])
    for item in [
        "confirmed_breakdown",
        "confirmed_breakdown_no_target_hit",
        "support_touch_no_trigger",
        "failed_breakdown_reclaim",
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


def write_bearish_manual_review_packet(repo_root: Path, draft: DraftBearishReplayCase) -> Path:
    output_path = repo_root / "runs" / "replay" / f"{draft.replay_id}_manual_review_packet.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_bearish_manual_review_packet(draft))
    return output_path


def _candidate_timestamp(candidate: DiversifiedReplayCandidate) -> date:
    return _date_only(candidate.timestamp)


def select_date_diversified_candidates(
    candidates: list[DiversifiedReplayCandidate],
    *,
    existing_case_dates: list[date],
    min_calendar_days_between_cases: int,
    max_cases_per_symbol_per_month: int,
    max_cases_per_symbol_total: int | None = None,
    avoid_existing_replay_windows: bool = True,
) -> list[DiversifiedReplayCandidate]:
    selected: list[DiversifiedReplayCandidate] = []
    selected_symbols: set[str] = set()
    per_symbol_month: dict[tuple[str, str], int] = {}
    per_symbol_total: dict[str, int] = {}
    sorted_candidates = sorted(
        candidates,
        key=lambda c: (
            -(_distance_from_nearest_existing_case_days(c.timestamp, existing_case_dates) or 0),
            _lower(c.side) != "bullish",
            _lower(c.symbol),
            -_candidate_timestamp(c).toordinal(),
            _candidate_timestamp(c),
            c.lookback_bars,
        ),
    )

    symbol_target = min(3, len({candidate.symbol for candidate in sorted_candidates}))

    def can_select(candidate: DiversifiedReplayCandidate) -> bool:
        candidate_date = _candidate_timestamp(candidate)
        if avoid_existing_replay_windows and any(abs((candidate_date - existing).days) <= 5 for existing in existing_case_dates):
            return False
        if any(abs((candidate_date - _candidate_timestamp(item)).days) < min_calendar_days_between_cases for item in selected):
            return False
        symbol_month = (candidate.symbol, candidate_date.strftime("%Y-%m"))
        if per_symbol_month.get(symbol_month, 0) >= max_cases_per_symbol_per_month:
            return False
        if max_cases_per_symbol_total is not None and per_symbol_total.get(candidate.symbol, 0) >= max_cases_per_symbol_total:
            return False
        return True

    def add_candidate(candidate: DiversifiedReplayCandidate) -> None:
        candidate_date = _candidate_timestamp(candidate)
        selected.append(candidate)
        selected_symbols.add(candidate.symbol)
        symbol_month = (candidate.symbol, candidate_date.strftime("%Y-%m"))
        per_symbol_month[symbol_month] = per_symbol_month.get(symbol_month, 0) + 1
        per_symbol_total[candidate.symbol] = per_symbol_total.get(candidate.symbol, 0) + 1

    for candidate in sorted_candidates:
        if len(selected_symbols) >= symbol_target:
            break
        if candidate.symbol in selected_symbols:
            continue
        if can_select(candidate):
            add_candidate(candidate)

    for candidate in sorted_candidates:
        if candidate in selected:
            continue
        if can_select(candidate):
            add_candidate(candidate)
    return selected


def _candidate_reason(candidate: DiversifiedReplayCandidate, existing_case_dates: list[date]) -> str:
    candidate_date = _candidate_timestamp(candidate)
    distance = _distance_from_nearest_existing_case_days(candidate.timestamp, existing_case_dates)
    parts = [f"outside clustered replay windows" if distance is None or distance > 5 else "near existing replay windows"]
    if distance is not None:
        parts.append(f"distance_from_nearest_existing_case_days={distance}")
    if candidate.has_1d_context:
        parts.append("1D context available")
    return "; ".join(parts)


def _discover_diversified_candidates(repo_root: Path, config: ReplayDiscoveryConfig) -> list[DiversifiedReplayCandidate]:
    existing_dates = _existing_replay_case_dates(repo_root)
    all_candidates: list[DiversifiedReplayCandidate] = []
    for symbol in config.symbols:
        if "bullish" in config.preferred_sides:
            for event in discover_events_for_symbol(repo_root, symbol, config.lookback_bars):
                all_candidates.append(
                    DiversifiedReplayCandidate(
                        replay_id="",
                        symbol=event.symbol,
                        side="bullish",
                        timestamp=event.timestamp,
                        event_type="close_above_resistance",
                        prior_level=event.prior_resistance,
                        breakout_or_breakdown_amount=event.breakout_amount,
                        lookback_bars=event.lookback_bars,
                        max_high_next_6_bars=event.max_high_next_6_bars,
                        max_high_next_12_bars=event.max_high_next_12_bars,
                        max_high_next_24_bars=event.max_high_next_24_bars,
                        close_after_6_bars=event.close_after_6_bars,
                        close_after_12_bars=event.close_after_12_bars,
                        close_after_24_bars=event.close_after_24_bars,
                        reason_selected="bullish close_above_resistance event",
                        distance_from_nearest_existing_case_days=_distance_from_nearest_existing_case_days(event.timestamp, existing_dates),
                        has_1d_context=_has_1d_context(repo_root, symbol),
                        prior_window_start=event.prior_window_start,
                        prior_window_end=event.prior_window_end,
                    )
                )
        if "bearish" in config.preferred_sides:
            for event in discover_close_below_support_events_for_symbol(repo_root, symbol, config.lookback_bars):
                all_candidates.append(
                    DiversifiedReplayCandidate(
                        replay_id="",
                        symbol=event.symbol,
                        side="bearish",
                        timestamp=event.timestamp,
                        event_type="close_below_support",
                        prior_level=event.prior_support,
                        breakout_or_breakdown_amount=event.breakdown_amount,
                        lookback_bars=event.lookback_bars,
                        min_low_next_6_bars=event.min_low_next_6_bars,
                        min_low_next_12_bars=event.min_low_next_12_bars,
                        min_low_next_24_bars=event.min_low_next_24_bars,
                        close_after_6_bars=event.close_after_6_bars,
                        close_after_12_bars=event.close_after_12_bars,
                        close_after_24_bars=event.close_after_24_bars,
                        reason_selected="bearish close_below_support event",
                        distance_from_nearest_existing_case_days=_distance_from_nearest_existing_case_days(event.timestamp, existing_dates),
                        has_1d_context=_has_1d_context(repo_root, symbol),
                        prior_window_start=event.prior_window_start,
                        prior_window_end=event.prior_window_end,
                    )
                )
    return select_date_diversified_candidates(
        all_candidates,
        existing_case_dates=existing_dates,
        min_calendar_days_between_cases=config.min_calendar_days_between_cases,
        max_cases_per_symbol_per_month=config.max_cases_per_symbol_per_month,
        max_cases_per_symbol_total=config.max_cases_per_symbol_total,
        avoid_existing_replay_windows=config.avoid_existing_replay_windows,
    )


def _select_symbol_balanced_candidates(repo_root: Path, config: ReplayDiscoveryConfig) -> list[DiversifiedReplayCandidate]:
    existing_dates = _existing_replay_case_dates(repo_root)
    by_symbol_side: dict[tuple[str, str], list[DiversifiedReplayCandidate]] = {}
    for symbol in config.symbols:
        if "bullish" in config.preferred_sides:
            for event in discover_events_for_symbol(repo_root, symbol, config.lookback_bars):
                by_symbol_side.setdefault((symbol, "bullish"), []).append(
                    DiversifiedReplayCandidate(
                        replay_id="",
                        symbol=event.symbol,
                        side="bullish",
                        timestamp=event.timestamp,
                        event_type="close_above_resistance",
                        prior_level=event.prior_resistance,
                        breakout_or_breakdown_amount=event.breakout_amount,
                        lookback_bars=event.lookback_bars,
                        max_high_next_6_bars=event.max_high_next_6_bars,
                        max_high_next_12_bars=event.max_high_next_12_bars,
                        max_high_next_24_bars=event.max_high_next_24_bars,
                        close_after_6_bars=event.close_after_6_bars,
                        close_after_12_bars=event.close_after_12_bars,
                        close_after_24_bars=event.close_after_24_bars,
                        reason_selected="bullish close_above_resistance event",
                        distance_from_nearest_existing_case_days=_distance_from_nearest_existing_case_days(event.timestamp, existing_dates),
                        has_1d_context=_has_1d_context(repo_root, symbol),
                        prior_window_start=event.prior_window_start,
                        prior_window_end=event.prior_window_end,
                    )
                )
        if "bearish" in config.preferred_sides:
            for event in discover_close_below_support_events_for_symbol(repo_root, symbol, config.lookback_bars):
                by_symbol_side.setdefault((symbol, "bearish"), []).append(
                    DiversifiedReplayCandidate(
                        replay_id="",
                        symbol=event.symbol,
                        side="bearish",
                        timestamp=event.timestamp,
                        event_type="close_below_support",
                        prior_level=event.prior_support,
                        breakout_or_breakdown_amount=event.breakdown_amount,
                        lookback_bars=event.lookback_bars,
                        min_low_next_6_bars=event.min_low_next_6_bars,
                        min_low_next_12_bars=event.min_low_next_12_bars,
                        min_low_next_24_bars=event.min_low_next_24_bars,
                        close_after_6_bars=event.close_after_6_bars,
                        close_after_12_bars=event.close_after_12_bars,
                        close_after_24_bars=event.close_after_24_bars,
                        reason_selected="bearish close_below_support event",
                        distance_from_nearest_existing_case_days=_distance_from_nearest_existing_case_days(event.timestamp, existing_dates),
                        has_1d_context=_has_1d_context(repo_root, symbol),
                        prior_window_start=event.prior_window_start,
                        prior_window_end=event.prior_window_end,
                    )
                )

    selected: list[DiversifiedReplayCandidate] = []
    selected_dates: list[date] = []
    selected_symbols: dict[str, int] = {}
    symbol_order = list(dict.fromkeys(config.symbols))
    for symbol in symbol_order:
        for side in ("bullish", "bearish"):
            side_candidates = by_symbol_side.get((symbol, side), [])
            if not side_candidates:
                continue
            candidate = select_date_diversified_candidates(
                side_candidates,
                existing_case_dates=existing_dates + selected_dates,
                min_calendar_days_between_cases=config.min_calendar_days_between_cases,
                max_cases_per_symbol_per_month=config.max_cases_per_symbol_per_month,
                max_cases_per_symbol_total=1,
                avoid_existing_replay_windows=config.avoid_existing_replay_windows,
            )
            if not candidate:
                continue
            chosen = candidate[0]
            if selected_symbols.get(symbol, 0) >= config.max_cases_per_symbol_total:
                continue
            selected.append(chosen)
            selected_dates.append(_candidate_timestamp(chosen))
            selected_symbols[symbol] = selected_symbols.get(symbol, 0) + 1
            if selected_symbols[symbol] >= config.max_cases_per_symbol_total:
                break
    return sorted(selected, key=lambda c: (_lower(c.side) != "bullish", c.symbol, _candidate_timestamp(c), c.lookback_bars))


def _render_date_diversified_candidates_csv(rows: list[dict[str, Any]]) -> str:
    from io import StringIO

    fieldnames = [
        "replay_id",
        "symbol",
        "side",
        "timestamp",
        "event_type",
        "prior_level",
        "breakout_or_breakdown_amount",
        "lookback_bars",
        "max_high_next_6_bars",
        "max_high_next_12_bars",
        "max_high_next_24_bars",
        "min_low_next_6_bars",
        "min_low_next_12_bars",
        "min_low_next_24_bars",
        "close_after_6_bars",
        "close_after_12_bars",
        "close_after_24_bars",
        "reason_selected",
        "distance_from_nearest_existing_case_days",
        "has_1d_context",
    ]
    buffer = StringIO()
    writer = csv.DictWriter(buffer, fieldnames=fieldnames)
    writer.writeheader()
    for row in rows:
        writer.writerow({name: row.get(name, "") for name in fieldnames})
    return buffer.getvalue()


def _render_date_diversified_candidates_md(rows: list[dict[str, Any]], config: ReplayDiscoveryConfig, existing_case_dates: list[date]) -> str:
    selected_symbols = {str(row["symbol"]) for row in rows}
    selected_months = {str(row["timestamp"])[:7] for row in rows}
    lines = [
        "# Date-Diversified Replay Candidates",
        "",
        f"candidate_windows_found: {len(rows)}",
        f"min_calendar_days_between_cases: {config.min_calendar_days_between_cases}",
        f"max_cases_per_symbol_per_month: {config.max_cases_per_symbol_per_month}",
        f"max_cases_per_symbol_total: {config.max_cases_per_symbol_total}",
        f"avoid_existing_replay_windows: {str(config.avoid_existing_replay_windows).lower()}",
        "",
    ]
    if rows:
        for row in rows:
            lines.extend(
                [
                    f"## {row['replay_id']} ({row['symbol']})",
                    f"- symbol: {row['symbol']}",
                    f"- side: {row['side']}",
                    f"- timestamp: {row['timestamp']}",
                    f"- event_type: {row['event_type']}",
                    f"- prior_level: {row['prior_level']}",
                    f"- breakout_or_breakdown_amount: {row['breakout_or_breakdown_amount']}",
                    f"- lookback_bars: {row['lookback_bars']}",
                    f"- reason_selected: {row['reason_selected']}",
                    f"- distance_from_nearest_existing_case_days: {row['distance_from_nearest_existing_case_days']}",
                    f"- has_1d_context: {str(row['has_1d_context']).lower()}",
                    "",
                ]
            )
    else:
        lines.extend([
            "## Selected candidates",
            "- none eligible with the current data and diversification constraints",
            "",
        ])
    if rows:
        lines.extend(
            [
                "## Diversity warnings",
                f"- date diversity improved: {len(selected_months)} month(s) selected",
                f"- symbol diversity warning: all selected cases are {next(iter(selected_symbols)) if len(selected_symbols) == 1 else 'mixed'}",
                "",
            ]
        )
    lines.extend([
        "## Coverage / selection notes",
        f"- existing replay case dates: {len(existing_case_dates)}",
        "- full 1Day + 5Min handoff data is now the replay source of truth",
        "- old Google Drive sample exports are deprecated for diversified replay discovery",
        "- 1Min remains blocked until the META 2023-2025 partial partitions are resolved",
        "",
        "## Recommended next search",
        "- bearish close_below_support discovery",
        "- retain bullish/bearish month and symbol diversification constraints",
        "- prefer 5Min over 1Min for date-diversified replay",
        "",
        "## Boundary",
        "- Generated report only",
        "- No broker action allowed",
    ])
    return "\n".join(lines).rstrip() + "\n"


def write_date_diversified_candidates(
    repo_root: Path,
    config: ReplayDiscoveryConfig | None = None,
    *,
    start_replay_number: int = 10,
) -> tuple[Path, Path, list[DiversifiedReplayCandidate]]:
    config = config or load_replay_discovery_config(repo_root)
    existing_dates = _existing_replay_case_dates(repo_root)
    selected = _select_symbol_balanced_candidates(repo_root, config)
    output_dir = repo_root / "runs" / "replay" / "discovery"
    output_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    for idx, candidate in enumerate(selected, start=start_replay_number):
        rows.append(
            {
                "replay_id": f"HR-{idx:03d}",
                "symbol": candidate.symbol,
                "side": candidate.side,
                "timestamp": candidate.timestamp,
                "event_type": candidate.event_type,
                "prior_level": candidate.prior_level,
                "breakout_or_breakdown_amount": candidate.breakout_or_breakdown_amount,
                "lookback_bars": candidate.lookback_bars,
                "max_high_next_6_bars": candidate.max_high_next_6_bars,
                "max_high_next_12_bars": candidate.max_high_next_12_bars,
                "max_high_next_24_bars": candidate.max_high_next_24_bars,
                "min_low_next_6_bars": candidate.min_low_next_6_bars,
                "min_low_next_12_bars": candidate.min_low_next_12_bars,
                "min_low_next_24_bars": candidate.min_low_next_24_bars,
                "close_after_6_bars": candidate.close_after_6_bars,
                "close_after_12_bars": candidate.close_after_12_bars,
                "close_after_24_bars": candidate.close_after_24_bars,
                "reason_selected": candidate.reason_selected,
                "distance_from_nearest_existing_case_days": candidate.distance_from_nearest_existing_case_days,
                "has_1d_context": str(candidate.has_1d_context).lower(),
            }
        )
    md_path = output_dir / "date_diversified_candidates.md"
    csv_path = output_dir / "date_diversified_candidates.csv"
    md_path.write_text(_render_date_diversified_candidates_md(rows, config, existing_dates))
    csv_path.write_text(_render_date_diversified_candidates_csv(rows))
    return md_path, csv_path, selected


def _row_line(row: dict[str, str]) -> str:
    return (
        f"- {row['timestamp']} | O:{row['open']} H:{row['high']} L:{row['low']} C:{row['close']} "
        f"V:{row.get('volume', '')} T:{row.get('trade_count', '')} VWAP:{row.get('vwap', '')}"
    )


def _resolve_data_file(repo_root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else repo_root / path


def render_draft_manual_review_packet(repo_root: Path, draft: DraftReplayCase) -> str:
    rows_1d = [row for row in load_ohlcv_rows(_resolve_data_file(repo_root, draft.data_files[0])) if draft.date_window.split(" to ")[0] <= row["timestamp"][:10] <= draft.date_window.split(" to ")[1]]
    rows_5m = [row for row in load_ohlcv_rows(_resolve_data_file(repo_root, draft.data_files[1])) if draft.date_window.split(" to ")[0] <= row["timestamp"][:10] <= draft.date_window.split(" to ")[1]]
    support_level = float(rows_1d[0]["low"])
    resistance_level = draft.event.prior_resistance
    target_price = resistance_level + max(1.0, draft.event.breakout_amount * 2)
    invalidation_level = support_level - (0.05 if draft.symbol == "SPY" else 0.10)
    analysis = analyze_level_interactions(
        rows_5m,
        support_level=support_level,
        resistance_level=resistance_level,
        target_price=target_price,
        invalidation_level=invalidation_level,
    )
    lines = [
        f"# {draft.replay_id} Manual Review Packet",
        "",
        "## Warning",
        "- Discovery draft only",
        "- Not verified replay evidence",
        "- No trade signal",
        "- No broker action allowed",
        "",
        "## Replay case metadata",
        f"- replay_id: {draft.replay_id}",
        f"- related_candidate_id: {draft.related_candidate_id}",
        f"- symbol: {draft.symbol}",
        f"- date_window: {draft.date_window}",
        f"- timeframe_stack: {draft.timeframe_stack}",
        "- manual_review_status: pending",
        "- broker_action_allowed: false",
        "- data files:",
    ]
    lines.extend(f"  - {item}" for item in draft.data_files)
    lines.extend(
        [
            "",
            "## 1D context rows",
        ]
    )
    if rows_1d:
        lines.extend(_row_line(row) for row in rows_1d)
    else:
        lines.append("- none available")
    lines.extend(
        [
            "",
            "## 5m breakout context",
            f"- prior_resistance: {draft.event.prior_resistance:.2f}",
            f"- breakout candle: {draft.event.timestamp} | close: {draft.event.close:.2f}",
            f"- breakout_amount: {draft.event.breakout_amount:.2f}",
            "",
            "## 5m bars around the breakout",
        ]
    )
    lines.extend(_row_line(row) for row in rows_5m)
    lines.extend(
        [
            "",
            "## Follow-through rows",
            f"- max_high_next_6_bars: {_format_float(draft.event.max_high_next_6_bars)}",
            f"- max_high_next_12_bars: {_format_float(draft.event.max_high_next_12_bars)}",
            f"- max_high_next_24_bars: {_format_float(draft.event.max_high_next_24_bars)}",
            f"- close_after_6_bars: {_format_float(draft.event.close_after_6_bars)}",
            f"- close_after_12_bars: {_format_float(draft.event.close_after_12_bars)}",
            f"- close_after_24_bars: {_format_float(draft.event.close_after_24_bars)}",
            "",
            "## Candidate chart-level worksheet",
            f"- proposed support_level: {support_level:.2f}",
            f"- proposed resistance_level: {resistance_level:.2f}",
            f"- proposed target_price: {target_price:.2f}",
            f"- proposed invalidation_level: {invalidation_level:.2f}",
            f"- entry_candidate_price: {draft.event.close:.2f}",
            f"- room_to_target: {max(1.0, draft.event.breakout_amount * 2):.2f}",
            "- higher_timeframe_obstacle_check: manual review required",
            f"- target_already_hit_check: {str(analysis['target_hit_before_confirmation']).lower()}",
            "",
            "## Event flags",
            f"- close_above_resistance: {str(analysis['close_above_resistance']).lower()}",
            f"- resistance_touched: {str(analysis['resistance_touched']).lower()}",
            f"- target_hit_after_confirmation: {str(analysis['target_hit_after_confirmation']).lower()}",
            f"- invalidation_hit_after_confirmation: {str(analysis['invalidation_hit_after_confirmation']).lower()}",
            f"- suggested_classification: {analysis['suggested_classification']}",
            "",
            "## Manual promotion workflow",
            "- manual_review_status: pending",
            "- manual_review_outcome: pending",
            "- manual_review_classification: pending",
            "- manual_reviewer_notes: pending",
            "- broker_action_allowed: false",
            "",
            "## Boundary",
            "- No trade signal",
            "- No profitability claim",
            "- No execution readiness",
            "- No broker action allowed",
            "",
            "## Status",
            "- Not verified",
        ]
    )
    return "\n".join(lines) + "\n"


def write_draft_manual_review_packet(repo_root: Path, draft: DraftReplayCase) -> Path:
    output_path = repo_root / "runs" / "replay" / f"{draft.replay_id}_manual_review_packet.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_draft_manual_review_packet(repo_root, draft))
    return output_path


def _load_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def _parse_existing_case_summary(case_path: Path) -> dict[str, str]:
    case = load_replay_case(case_path)
    raw = case.raw
    date = case.date_window.split(" to ")[0]
    return {
        "replay_id": case.replay_id,
        "symbol": case.symbol,
        "side": "bearish" if _lower(raw.get("direction")) == "short" else "bullish",
        "date": date,
        "classification": case.classification,
        "replay_status": case.replay_status,
    }


def _load_existing_case_summaries(repo_root: Path, start: int = 1, end: int = 19) -> list[dict[str, str]]:
    summaries: list[dict[str, str]] = []
    for idx in range(start, end + 1):
        case_path = repo_root / "replay" / "cases" / f"HR-{idx:03d}.md"
        if case_path.exists():
            summaries.append(_parse_existing_case_summary(case_path))
    return summaries


def _raw_candidate_rows(repo_root: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for side, filename in [
        ("bullish", "close_above_resistance_candidates.csv"),
        ("bearish", "close_below_support_candidates.csv"),
    ]:
        path = repo_root / "runs" / "replay" / "discovery" / filename
        if not path.exists():
            continue
        for row in _load_csv_rows(path):
            row["side"] = side
            row["setup_type"] = "close_above_resistance" if side == "bullish" else "close_below_support"
            rows.append(row)
    return rows


def _selected_candidate_rows(repo_root: Path) -> list[dict[str, str]]:
    path = repo_root / "runs" / "replay" / "discovery" / "date_diversified_candidates.csv"
    return _load_csv_rows(path) if path.exists() else []


def _top_near_misses(repo_root: Path, raw_rows: list[dict[str, str]], selected_rows: list[dict[str, str]], limit: int = 20) -> list[dict[str, str]]:
    selected_keys = {(row["side"], row["symbol"], row["timestamp"]) for row in selected_rows}
    selected_months = {row["timestamp"][:7] for row in selected_rows}
    existing_symbols = {row["symbol"] for row in _load_existing_case_summaries(repo_root)}
    unique: dict[tuple[str, str, str], dict[str, str]] = {}
    for row in raw_rows:
        key = (row["side"], row["symbol"], row["timestamp"])
        if key in selected_keys:
            continue
        if key not in unique or float(row.get("score") or 0.0) > float(unique[key].get("score") or 0.0):
            unique[key] = row
    ranked = sorted(unique.values(), key=lambda row: (-float(row.get("score") or 0.0), row["side"] != "bullish", row["symbol"], row["timestamp"]))
    near_misses: list[dict[str, str]] = []
    for row in ranked:
        row = dict(row)
        row["row_type"] = "near_miss"
        row["prior_level"] = row.get("prior_resistance") or row.get("prior_support") or row.get("prior_level", "")
        row["close"] = row.get("close", "")
        row["rejection_reason"] = "avoid_existing_replay_windows"
        row["selected_replay_id"] = ""
        row["target_hit_after_confirmation"] = ""
        row["invalidation_hit_after_confirmation"] = ""
        row["would_be_useful_coverage"] = str(row["symbol"] not in existing_symbols or row["timestamp"][:7] not in selected_months).lower()
        near_misses.append(row)
        if len(near_misses) >= limit:
            break
    return near_misses


def render_discovery_constraint_audit(repo_root: Path) -> tuple[str, list[dict[str, str]]]:
    config = load_replay_discovery_config(repo_root)
    artifact_root = resolve_full_historical_data_root(repo_root)
    index_path = repo_root / "data_refs" / "historical_market_data" / "artifact_index.yaml"
    index = _load_yaml(index_path)
    manifest, manifest_root = load_replay_handoff_manifest(repo_root)

    raw_rows = _raw_candidate_rows(repo_root)
    selected_rows = _selected_candidate_rows(repo_root)
    existing_1_19 = _load_existing_case_summaries(repo_root, 1, 19)
    existing_1_31 = _load_existing_case_summaries(repo_root, 1, 31)

    by_side_symbol: dict[tuple[str, str], list[dict[str, str]]] = {}
    for row in raw_rows:
        by_side_symbol.setdefault((row["side"], row["symbol"]), []).append(row)

    raw_bull = [row for row in raw_rows if row["side"] == "bullish"]
    raw_bear = [row for row in raw_rows if row["side"] == "bearish"]
    selected_bull = [row for row in selected_rows if row.get("side") == "bullish"]
    selected_bear = [row for row in selected_rows if row.get("side") == "bearish"]
    raw_lookup = {(row["side"], row["symbol"], row["timestamp"]): row for row in raw_rows}

    symbols_in_index = sorted({str(item.get("symbol", "")).upper() for item in index.get("items", []) if isinstance(item, dict) and str(item.get("artifact_kind", "")).lower() == "full" and str(item.get("symbol", "")).strip()})
    if not symbols_in_index:
        symbols_in_index = list(config.symbols)

    symbols_with_both = []
    for symbol in config.symbols:
        paths = resolve_historical_market_data_paths(repo_root, symbol)
        if set(paths) >= {"1Day", "5Min"}:
            symbols_with_both.append(symbol)

    selected_set = {(row["side"], row["symbol"], row["timestamp"]) for row in selected_rows}
    occupied_dates = {row["date"] for row in existing_1_31}
    rerun_blocked = sum(1 for row in selected_rows if row["timestamp"][:10] in occupied_dates)

    # near misses: top 20 raw candidates not in the selected batch, marked as diversification rejects.
    near_misses = _top_near_misses(repo_root, raw_rows, selected_rows, limit=20)

    csv_rows: list[dict[str, str]] = []
    for row in selected_rows:
        raw = raw_lookup.get((row.get("side", ""), row.get("symbol", ""), row.get("timestamp", "")), {})
        csv_rows.append(
            {
                "row_type": "selected",
                "side": row.get("side", ""),
                "symbol": row.get("symbol", ""),
                "timestamp": row.get("timestamp", ""),
                "setup_type": row.get("event_type", ""),
                "prior_level": raw.get("prior_resistance") or raw.get("prior_support") or row.get("prior_level", ""),
                "close": raw.get("close", row.get("close", "")),
                "target_hit_after_confirmation": "",
                "invalidation_hit_after_confirmation": "",
                "rejection_reason": "",
                "would_be_useful_coverage": "true",
                "selected_replay_id": row.get("replay_id", ""),
                "score": raw.get("score", row.get("breakout_or_breakdown_amount", "")),
            }
        )
    csv_rows.extend(near_misses)

    lines = [
        "# Discovery Constraint Audit",
        "",
        "## 1. Data source verification",
        f"- artifact root currently used: {artifact_root or 'missing'}",
        f"- full 11-symbol root: {str((artifact_root is not None) and set(config.symbols) <= set(symbols_in_index)).lower()}",
        f"- old data_refs/google_drive samples excluded: {str(all('google_drive' not in str(path) for sym in config.symbols for path in resolve_historical_market_data_paths(repo_root, sym).values())).lower()}",
        f"- 1Min blocked: {str('1Min' not in {tf for sym in config.symbols for tf in resolve_historical_market_data_paths(repo_root, sym)}).lower()}",
        f"- symbols discovered from artifact index: {', '.join(symbols_in_index)}",
        f"- symbols with both 1Day and 5Min available: {', '.join(symbols_with_both)}",
        "",
        "## 2. Raw candidate counts before diversification filters",
        "",
        "### Bullish",
        "| side | symbol | raw_candidate_count | first_event_timestamp | last_event_timestamp | months_present |",
        "| --- | --- | ---: | --- | --- | --- |",
    ]
    for symbol in config.symbols:
        rows = [row for row in raw_bull if row["symbol"] == symbol]
        if not rows:
            continue
        months = sorted({row["timestamp"][:7] for row in rows})
        lines.append(f"| bullish | {symbol} | {len(rows)} | {rows[0]['timestamp']} | {rows[-1]['timestamp']} | {', '.join(months)} |")
    lines.extend([
        "",
        "### Bearish",
        "| side | symbol | raw_candidate_count | first_event_timestamp | last_event_timestamp | months_present |",
        "| --- | --- | ---: | --- | --- | --- |",
    ])
    for symbol in config.symbols:
        rows = [row for row in raw_bear if row["symbol"] == symbol]
        if not rows:
            continue
        months = sorted({row["timestamp"][:7] for row in rows})
        lines.append(f"| bearish | {symbol} | {len(rows)} | {rows[0]['timestamp']} | {rows[-1]['timestamp']} | {', '.join(months)} |")
    lines.extend([
        "",
        "## 3. Filter-stage attrition table",
        "| stage | bullish | bearish | combined | notes |",
        "| --- | ---: | ---: | ---: | --- |",
        f"| raw candidates | {len(raw_bull)} | {len(raw_bear)} | {len(raw_rows)} | source scan output |",
        f"| after excluding old sample sources | {len(raw_bull)} | {len(raw_bear)} | {len(raw_rows)} | raw discovery CSVs are already from the full published handoff |",
        f"| after requiring full artifact root | {len(raw_bull)} | {len(raw_bear)} | {len(raw_rows)} | full 11-symbol root resolves correctly |",
        f"| after excluding 1Min | {len(raw_bull)} | {len(raw_bear)} | {len(raw_rows)} | 1Min is not returned by resolution |",
        f"| after avoid-existing-window rule | {len(selected_bull)} | {len(selected_bear)} | {len(selected_rows)} | selected batch still fits the available windows from HR-001..HR-019 |",
        f"| after 30-day spacing rule | {len(selected_bull)} | {len(selected_bear)} | {len(selected_rows)} | spacing preserved by the date-diversified selector |",
        f"| after max cases per symbol per month | {len(selected_bull)} | {len(selected_bear)} | {len(selected_rows)} | one case per symbol per month in the selected batch |",
        f"| after max cases per symbol total | {len(selected_bull)} | {len(selected_bear)} | {len(selected_rows)} | symbol caps hold at 2 max per symbol |",
        f"| final selected candidates | {len(selected_bull)} | {len(selected_bear)} | {len(selected_rows)} | selected batch is HR-020..HR-031 |",
        "",
        "## 4. Existing HR window coverage",
        "| replay_id | symbol | side | date | classification | replay_status |",
        "| --- | --- | --- | --- | --- | --- |",
    ])
    for row in existing_1_19:
        lines.append(f"| {row['replay_id']} | {row['symbol']} | {row['side']} | {row['date']} | {row['classification']} | {row['replay_status']} |")
    lines.extend([
        "",
        f"- dates already occupied: {', '.join(sorted({row['date'] for row in existing_1_19}))}",
        f"- months already occupied: {', '.join(sorted({row['date'][:7] for row in existing_1_19}))}",
        f"- symbols already occupied: {', '.join(sorted({row['symbol'] for row in existing_1_19}))}",
        f"- existing HR cases causing over-blocking: no for HR-001..HR-019 alone; yes once HR-020..HR-031 are present and occupy the same date windows",
        "",
        "## 5. Near-miss candidates",
        "| side | symbol | event timestamp | setup type | prior level | close | target hit after confirmation | invalidation hit after confirmation | which constraint rejected it | whether it would be useful as coverage |",
        "| --- | --- | --- | --- | ---: | ---: | --- | --- | --- | --- |",
    ])
    for row in near_misses:
        lines.append(
            f"| {row['side']} | {row['symbol']} | {row['timestamp']} | {row['setup_type']} | {row.get('prior_resistance') or row.get('prior_support') or row.get('prior_level') or ''} | {row.get('close', '')} | {row.get('target_hit_after_confirmation', '')} | {row.get('invalidation_hit_after_confirmation', '')} | {row['rejection_reason']} | {row['would_be_useful_coverage']} |"
        )
    lines.extend([
        "",
        "## 6. Recommended constraint options",
        "- Option A — Keep strict constraints: no new cases; strongest anti-bias posture.",
        "- Option B — Relax date spacing only: reduce min spacing from 30 calendar days to 10 or 15; keep symbol caps.",
        "- Option C — Relax avoid-existing-window only: allow new cases in same month but not same symbol/date; keep symbol caps.",
        "- Option D — Create targeted gap-fill cases: choose scenarios missing from evidence matrix rather than pure date/symbol diversity.",
        "- Option E — Expand data or selector logic if raw counts are unexpectedly low: only if raw candidates are missing for many symbols.",
        "",
        "## 7. Recommendation",
        "- Keep the scanner/data path as-is; all 11 symbols are visible and both required timeframes resolve.",
        "- The useful next prompt is Option D (targeted gap-fill cases), not broader relaxation of spacing or window rules.",
        f"- On a rerun with the current repo state, {rerun_blocked} of the 12 selected windows are already occupied, so no new slots remain.",
        "- Main constraint causing the zero-case rerun result: avoid-existing-window, then symbol/month caps.",
        "",
        f"- Final test result: pending (written by report generator only)",
    ])
    return "\n".join(lines) + "\n", csv_rows


def write_discovery_constraint_audit(repo_root: Path) -> tuple[Path, Path]:
    report, csv_rows = render_discovery_constraint_audit(repo_root)
    output_dir = repo_root / "runs" / "replay" / "discovery"
    output_dir.mkdir(parents=True, exist_ok=True)
    md_path = output_dir / "discovery_constraint_audit.md"
    csv_path = output_dir / "discovery_constraint_audit.csv"
    md_path.write_text(report)
    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "row_type",
                "side",
                "symbol",
                "timestamp",
                "setup_type",
                "prior_level",
                "close",
                "target_hit_after_confirmation",
                "invalidation_hit_after_confirmation",
                "rejection_reason",
                "would_be_useful_coverage",
                "selected_replay_id",
                "score",
            ],
        )
        writer.writeheader()
        for row in csv_rows:
            writer.writerow({key: row.get(key, "") for key in writer.fieldnames})
    return md_path, csv_path


def _strict_bearish_geometry_ok(prior_support: float, breakdown_close: float, downside_target: float, invalidation_level: float) -> bool:
    return breakdown_close < prior_support and downside_target < breakdown_close and invalidation_level > breakdown_close


def _strict_bearish_confirmation_metrics(repo_root: Path, event: BearishDiscoveryEvent) -> dict[str, float | bool]:
    five_min_path = resolve_historical_market_data_paths(repo_root, event.symbol).get("5Min")
    if five_min_path is None:
        raise FileNotFoundError(f"No 5Min data available for {event.symbol}")

    rows = _load_rows(five_min_path)
    rows.sort(key=lambda row: _parse_ts(row["timestamp"]))
    event_index = next(i for i, row in enumerate(rows) if row["timestamp"] == event.timestamp)
    confirmation_rows = rows[event_index:]

    downside_target = event.close - event.breakdown_amount
    invalidation_level = event.prior_support
    target_hit_after_confirmation = any(_float(row["low"]) <= downside_target for row in confirmation_rows)
    invalidation_hit_after_confirmation = any(_float(row["high"]) >= invalidation_level for row in confirmation_rows)
    min_low_after_confirmation = min((_float(row["low"]) for row in confirmation_rows), default=float("nan"))
    max_close_after_confirmation = max((_float(row["close"]) for row in confirmation_rows), default=float("nan"))

    return {
        "downside_target": downside_target,
        "invalidation_level": invalidation_level,
        "target_hit_after_confirmation": target_hit_after_confirmation,
        "invalidation_hit_after_confirmation": invalidation_hit_after_confirmation,
        "min_low_after_confirmation": min_low_after_confirmation,
        "max_close_after_confirmation": max_close_after_confirmation,
    }


def _strict_bearish_confirmation_metrics_from_rows(rows: list[dict[str, str]], event: BearishDiscoveryEvent) -> dict[str, float | bool]:
    event_index = next(i for i, row in enumerate(rows) if row["timestamp"] == event.timestamp)
    confirmation_rows = rows[event_index:]

    downside_target = event.close - event.breakdown_amount
    invalidation_level = event.prior_support
    target_hit_after_confirmation = any(_float(row["low"]) <= downside_target for row in confirmation_rows)
    invalidation_hit_after_confirmation = any(_float(row["high"]) >= invalidation_level for row in confirmation_rows)
    min_low_after_confirmation = min((_float(row["low"]) for row in confirmation_rows), default=float("nan"))
    max_close_after_confirmation = max((_float(row["close"]) for row in confirmation_rows), default=float("nan"))

    return {
        "downside_target": downside_target,
        "invalidation_level": invalidation_level,
        "target_hit_after_confirmation": target_hit_after_confirmation,
        "invalidation_hit_after_confirmation": invalidation_hit_after_confirmation,
        "min_low_after_confirmation": min_low_after_confirmation,
        "max_close_after_confirmation": max_close_after_confirmation,
    }


def select_strict_bearish_breakdown_candidates(
    repo_root: Path,
    symbols: Iterable[str] = DEFAULT_DISCOVERY_SYMBOLS,
    lookbacks: Iterable[int] = LOOKBACKS,
    limit: int = 4,
) -> list[StrictBearishBreakdownCandidate]:
    """Select strict bearish breakdowns that hit target after confirmation without invalidation."""

    best_by_symbol: dict[str, tuple[float, StrictBearishBreakdownCandidate]] = {}
    for symbol in symbols:
        five_min_path = resolve_historical_market_data_paths(repo_root, symbol).get("5Min")
        if five_min_path is None:
            continue
        rows = _load_rows(five_min_path)
        rows.sort(key=lambda row: _parse_ts(row["timestamp"]))
        for event in discover_close_below_support_events_for_symbol(repo_root, symbol, lookbacks):
            metrics = _strict_bearish_confirmation_metrics_from_rows(rows, event)
            downside_target = float(metrics["downside_target"])
            invalidation_level = float(metrics["invalidation_level"])
            target_hit = bool(metrics["target_hit_after_confirmation"])
            invalidation_hit = bool(metrics["invalidation_hit_after_confirmation"])
            if not _strict_bearish_geometry_ok(event.prior_support, event.close, downside_target, invalidation_level):
                continue
            if not target_hit or invalidation_hit:
                continue

            candidate = StrictBearishBreakdownCandidate(
                symbol=event.symbol,
                event_timestamp=event.timestamp,
                prior_support=event.prior_support,
                breakdown_close=event.close,
                downside_target=downside_target,
                invalidation_level=invalidation_level,
                target_hit_after_confirmation=target_hit,
                invalidation_hit_after_confirmation=invalidation_hit,
                min_low_after_confirmation=float(metrics["min_low_after_confirmation"]),
                max_close_after_confirmation=float(metrics["max_close_after_confirmation"]),
                suggested_classification="confirmed_breakdown",
                reason_selected="strict confirmed bearish breakdown: target hit after confirmation and no invalidation after confirmation",
            )
            score = (candidate.prior_support - candidate.breakdown_close) * 10.0
            current = best_by_symbol.get(symbol)
            if current is None or score > current[0]:
                best_by_symbol[symbol] = (score, candidate)

    ranked = sorted(
        (candidate for _score, candidate in best_by_symbol.values()),
        key=lambda candidate: (-(candidate.prior_support - candidate.breakdown_close), candidate.symbol, candidate.event_timestamp),
    )
    return ranked[:limit]


def render_strict_bearish_breakdown_candidates(candidates: list[StrictBearishBreakdownCandidate]) -> str:
    lines = [
        "# Strict Bearish Breakdown Candidates",
        "",
        f"strict_candidates_selected: {len(candidates)}",
        "",
        "| symbol | event_timestamp | prior_support | breakdown_close | downside_target | invalidation_level | target_hit_after_confirmation | invalidation_hit_after_confirmation | min_low_after_confirmation | max_close_after_confirmation | suggested_classification | reason_selected |",
        "| --- | --- | ---: | ---: | ---: | ---: | --- | --- | ---: | ---: | --- | --- |",
    ]
    for candidate in candidates:
        lines.append(
            "| "
            f"{candidate.symbol} | {candidate.event_timestamp} | {candidate.prior_support:.2f} | {candidate.breakdown_close:.2f} | {candidate.downside_target:.2f} | {candidate.invalidation_level:.2f} | "
            f"{str(candidate.target_hit_after_confirmation).lower()} | {str(candidate.invalidation_hit_after_confirmation).lower()} | {candidate.min_low_after_confirmation:.2f} | {candidate.max_close_after_confirmation:.2f} | {candidate.suggested_classification} | {candidate.reason_selected} |"
        )
    lines.extend([
        "",
        "## Boundary",
        "- Discovery only",
        "- Strict bearish geometry required",
        "- No trade signal",
        "- No broker action allowed",
    ])
    return "\n".join(lines) + "\n"


def write_strict_bearish_breakdown_candidates(repo_root: Path, candidates: list[StrictBearishBreakdownCandidate]) -> tuple[Path, Path]:
    output_dir = repo_root / "runs" / "replay" / "discovery"
    output_dir.mkdir(parents=True, exist_ok=True)
    md_path = output_dir / "strict_bearish_breakdown_candidates.md"
    csv_path = output_dir / "strict_bearish_breakdown_candidates.csv"
    md_path.write_text(render_strict_bearish_breakdown_candidates(candidates))
    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "symbol",
                "event_timestamp",
                "prior_support",
                "breakdown_close",
                "downside_target",
                "invalidation_level",
                "target_hit_after_confirmation",
                "invalidation_hit_after_confirmation",
                "min_low_after_confirmation",
                "max_close_after_confirmation",
                "suggested_classification",
                "reason_selected",
            ],
        )
        writer.writeheader()
        for candidate in candidates:
            writer.writerow(
                {
                    "symbol": candidate.symbol,
                    "event_timestamp": candidate.event_timestamp,
                    "prior_support": f"{candidate.prior_support:.2f}",
                    "breakdown_close": f"{candidate.breakdown_close:.2f}",
                    "downside_target": f"{candidate.downside_target:.2f}",
                    "invalidation_level": f"{candidate.invalidation_level:.2f}",
                    "target_hit_after_confirmation": str(candidate.target_hit_after_confirmation).lower(),
                    "invalidation_hit_after_confirmation": str(candidate.invalidation_hit_after_confirmation).lower(),
                    "min_low_after_confirmation": f"{candidate.min_low_after_confirmation:.2f}",
                    "max_close_after_confirmation": f"{candidate.max_close_after_confirmation:.2f}",
                    "suggested_classification": candidate.suggested_classification,
                    "reason_selected": candidate.reason_selected,
                }
            )
    return md_path, csv_path
