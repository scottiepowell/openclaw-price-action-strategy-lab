from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
import csv
import importlib.util
import re

import yaml


REQUIRED_OHLCV_COLUMNS = ["symbol", "timeframe", "timestamp", "open", "high", "low", "close"]
OPTIONAL_METADATA_COLUMNS = ["volume", "trade_count", "vwap", "source", "feed", "adjustment", "downloaded_at"]


@dataclass(frozen=True)
class OhlcvFileInspection:
    path: Path
    file_type: str
    exists: bool
    row_count: int
    first_timestamp: str | None
    last_timestamp: str | None
    timezone: str | None
    source: str | None
    feed: str | None
    adjustment: str | None
    required_columns: list[str]
    missing_columns: list[str]
    duplicate_timestamps: int
    quality_status: str
    issues: list[str]


@dataclass(frozen=True)
class HistoricalMarketDataArtifact:
    symbol: str
    timeframe: str
    path: str
    file_type: str
    row_count: int | None
    first_timestamp: str | None
    last_timestamp: str | None
    timezone: str | None
    source: str | None
    feed: str | None
    adjustment: str | None
    data_quality_status: str = "NOT_CHECKED"


def _parse_timestamp(value: str | None) -> datetime | None:
    if not value:
        return None
    text = value.strip()
    if not text:
        return None
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    return parsed


def _timestamp_timezone_name(ts: datetime | None) -> str | None:
    if ts is None:
        return None
    if ts.tzinfo is None:
        return "unknown"
    if ts.tzinfo == timezone.utc:
        return "UTC"
    return str(ts.tzinfo)


def _row_float(row: dict[str, Any], column: str) -> float | None:
    raw = row.get(column)
    if raw is None:
        return None
    text = str(raw).strip()
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def _infer_symbol_timeframe(path: Path, first_row: dict[str, Any] | None = None) -> tuple[str | None, str | None]:
    stem = path.stem
    match = re.match(r"^(?P<symbol>[A-Z0-9]+)_(?P<timeframe>\d+(?:Min|Day|Hour|Week|Month))", stem)
    if match:
        return match.group("symbol"), match.group("timeframe")
    if first_row:
        return first_row.get("symbol"), first_row.get("timeframe")
    return None, None


def _inspect_csv(path: Path) -> OhlcvFileInspection:
    issues: list[str] = []
    if not path.exists():
        return OhlcvFileInspection(
            path=path,
            file_type=path.suffix.lstrip("."),
            exists=False,
            row_count=0,
            first_timestamp=None,
            last_timestamp=None,
            timezone=None,
            source=None,
            feed=None,
            adjustment=None,
            required_columns=REQUIRED_OHLCV_COLUMNS,
            missing_columns=REQUIRED_OHLCV_COLUMNS,
            duplicate_timestamps=0,
            quality_status="FAIL",
            issues=["file missing"],
        )

    with path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        header = reader.fieldnames or []
        missing_columns = [column for column in REQUIRED_OHLCV_COLUMNS if column not in header]
        if missing_columns:
            issues.append(f"missing required columns: {', '.join(missing_columns)}")

        rows = list(reader)

    row_count = len(rows)
    first_timestamp: datetime | None = None
    last_timestamp: datetime | None = None
    first_timezone: str | None = None
    duplicate_timestamps = 0
    seen_timestamps: set[str] = set()
    source = feed = adjustment = None

    for row in rows:
        timestamp = _parse_timestamp(str(row.get("timestamp", "")))
        if timestamp is None:
            issues.append("timestamp parse failed")
            continue
        if first_timestamp is None or timestamp < first_timestamp:
            first_timestamp = timestamp
            first_timezone = _timestamp_timezone_name(timestamp)
        if last_timestamp is None or timestamp > last_timestamp:
            last_timestamp = timestamp

        timestamp_key = timestamp.isoformat()
        if timestamp_key in seen_timestamps:
            duplicate_timestamps += 1
        else:
            seen_timestamps.add(timestamp_key)

        open_price = _row_float(row, "open")
        high_price = _row_float(row, "high")
        low_price = _row_float(row, "low")
        close_price = _row_float(row, "close")
        if None in {open_price, high_price, low_price, close_price}:
            issues.append(f"numeric parse failed at {timestamp_key}")
            continue

        if high_price < max(open_price, close_price, low_price):
            issues.append(f"high below candle body at {timestamp_key}")
        if low_price > min(open_price, close_price, high_price):
            issues.append(f"low above candle body at {timestamp_key}")

        source = source or str(row.get("source", "")).strip() or None
        feed = feed or str(row.get("feed", "")).strip() or None
        adjustment = adjustment or str(row.get("adjustment", "")).strip() or None

    if duplicate_timestamps:
        issues.append(f"duplicate timestamps: {duplicate_timestamps}")

    quality_status = "PASS" if not issues and not missing_columns else "FAIL"
    return OhlcvFileInspection(
        path=path,
        file_type=path.suffix.lstrip("."),
        exists=True,
        row_count=row_count,
        first_timestamp=first_timestamp.isoformat() if first_timestamp else None,
        last_timestamp=last_timestamp.isoformat() if last_timestamp else None,
        timezone=first_timezone,
        source=source,
        feed=feed,
        adjustment=adjustment,
        required_columns=REQUIRED_OHLCV_COLUMNS,
        missing_columns=missing_columns,
        duplicate_timestamps=duplicate_timestamps,
        quality_status=quality_status,
        issues=issues,
    )


def _inspect_parquet(path: Path) -> OhlcvFileInspection:
    if importlib.util.find_spec("pyarrow") is None:
        return OhlcvFileInspection(
            path=path,
            file_type=path.suffix.lstrip("."),
            exists=path.exists(),
            row_count=0,
            first_timestamp=None,
            last_timestamp=None,
            timezone=None,
            source=None,
            feed=None,
            adjustment=None,
            required_columns=REQUIRED_OHLCV_COLUMNS,
            missing_columns=REQUIRED_OHLCV_COLUMNS,
            duplicate_timestamps=0,
            quality_status="FAIL",
            issues=["parquet support requires pyarrow"],
        )

    import pyarrow.parquet as pq  # type: ignore[import-not-found]

    if not path.exists():
        return OhlcvFileInspection(
            path=path,
            file_type=path.suffix.lstrip("."),
            exists=False,
            row_count=0,
            first_timestamp=None,
            last_timestamp=None,
            timezone=None,
            source=None,
            feed=None,
            adjustment=None,
            required_columns=REQUIRED_OHLCV_COLUMNS,
            missing_columns=REQUIRED_OHLCV_COLUMNS,
            duplicate_timestamps=0,
            quality_status="FAIL",
            issues=["file missing"],
        )

    table = pq.read_table(path)
    header = table.column_names
    missing_columns = [column for column in REQUIRED_OHLCV_COLUMNS if column not in header]
    issues: list[str] = []
    if missing_columns:
        issues.append(f"missing required columns: {', '.join(missing_columns)}")

    rows = table.to_pylist()
    row_count = len(rows)
    first_timestamp: datetime | None = None
    last_timestamp: datetime | None = None
    first_timezone: str | None = None
    duplicate_timestamps = 0
    seen_timestamps: set[str] = set()
    source = feed = adjustment = None

    for row in rows:
        timestamp = _parse_timestamp(str(row.get("timestamp", "")))
        if timestamp is None:
            issues.append("timestamp parse failed")
            continue
        if first_timestamp is None or timestamp < first_timestamp:
            first_timestamp = timestamp
            first_timezone = _timestamp_timezone_name(timestamp)
        if last_timestamp is None or timestamp > last_timestamp:
            last_timestamp = timestamp
        timestamp_key = timestamp.isoformat()
        if timestamp_key in seen_timestamps:
            duplicate_timestamps += 1
        else:
            seen_timestamps.add(timestamp_key)

        open_price = _row_float(row, "open")
        high_price = _row_float(row, "high")
        low_price = _row_float(row, "low")
        close_price = _row_float(row, "close")
        if None in {open_price, high_price, low_price, close_price}:
            issues.append(f"numeric parse failed at {timestamp_key}")
            continue
        if high_price < max(open_price, close_price, low_price):
            issues.append(f"high below candle body at {timestamp_key}")
        if low_price > min(open_price, close_price, high_price):
            issues.append(f"low above candle body at {timestamp_key}")

        source = source or str(row.get("source", "")).strip() or None
        feed = feed or str(row.get("feed", "")).strip() or None
        adjustment = adjustment or str(row.get("adjustment", "")).strip() or None

    if duplicate_timestamps:
        issues.append(f"duplicate timestamps: {duplicate_timestamps}")

    quality_status = "PASS" if not issues and not missing_columns else "FAIL"
    return OhlcvFileInspection(
        path=path,
        file_type=path.suffix.lstrip("."),
        exists=True,
        row_count=row_count,
        first_timestamp=first_timestamp.isoformat() if first_timestamp else None,
        last_timestamp=last_timestamp.isoformat() if last_timestamp else None,
        timezone=first_timezone,
        source=source,
        feed=feed,
        adjustment=adjustment,
        required_columns=REQUIRED_OHLCV_COLUMNS,
        missing_columns=missing_columns,
        duplicate_timestamps=duplicate_timestamps,
        quality_status=quality_status,
        issues=issues,
    )


def inspect_ohlcv_file(path: Path) -> OhlcvFileInspection:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return _inspect_csv(path)
    if suffix == ".parquet":
        return _inspect_parquet(path)
    return OhlcvFileInspection(
        path=path,
        file_type=suffix.lstrip("."),
        exists=path.exists(),
        row_count=0,
        first_timestamp=None,
        last_timestamp=None,
        timezone=None,
        source=None,
        feed=None,
        adjustment=None,
        required_columns=REQUIRED_OHLCV_COLUMNS,
        missing_columns=REQUIRED_OHLCV_COLUMNS,
        duplicate_timestamps=0,
        quality_status="FAIL",
        issues=[f"unsupported file type: {path.suffix or '(none)'}"],
    )


def discover_historical_market_data_files(repo_root: Path) -> list[Path]:
    candidates: list[Path] = []
    for relative in [
        "data_refs/google_drive",
        "data_refs/historical_market_data",
        "artifacts",
        "runs",
        "knowledge_base/historic_artifacts",
    ]:
        root = repo_root / relative
        if not root.exists():
            continue
        for suffix in ("*.csv", "*.parquet"):
            candidates.extend(sorted(root.rglob(suffix)))
    unique: list[Path] = []
    seen: set[Path] = set()
    for path in candidates:
        if path in seen:
            continue
        seen.add(path)
        unique.append(path)
    return unique


def build_historical_market_data_inventory(file_paths: Iterable[Path], repo_root: Path | None = None) -> dict[str, Any]:
    repo_root = repo_root or Path.cwd()
    items: list[dict[str, Any]] = []
    for path in sorted({Path(p) for p in file_paths}):
        inspection = inspect_ohlcv_file(path)
        sample_row = None
        if inspection.exists and inspection.file_type == "csv":
            with path.open(newline="") as handle:
                reader = csv.DictReader(handle)
                sample_row = next(reader, None)
        symbol, timeframe = _infer_symbol_timeframe(path, sample_row)
        relative_path = str(path.relative_to(repo_root)) if path.is_relative_to(repo_root) else str(path)
        items.append(
            {
                "symbol": symbol,
                "timeframe": timeframe,
                "path": relative_path,
                "file_type": inspection.file_type,
                "row_count": inspection.row_count if inspection.exists else None,
                "first_timestamp": inspection.first_timestamp,
                "last_timestamp": inspection.last_timestamp,
                "timezone": inspection.timezone,
                "source": inspection.source,
                "feed": inspection.feed,
                "adjustment": inspection.adjustment,
                "data_quality_status": "NOT_CHECKED",
            }
        )
    return {
        "schema": "historical_market_data_artifact_index_v1",
        "status": "active",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "items": items,
    }


def write_historical_market_data_inventory(repo_root: Path, file_paths: Iterable[Path] | None = None) -> Path:
    file_paths = list(file_paths or discover_historical_market_data_files(repo_root))
    payload = build_historical_market_data_inventory(file_paths, repo_root=repo_root)
    output_path = repo_root / "data_refs" / "historical_market_data" / "artifact_index.yaml"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True))
    return output_path


def load_historical_market_data_inventory(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text())
    if not isinstance(data, dict):
        raise ValueError(f"Historical market data inventory {path} is not a mapping")
    return data


def render_replay_data_quality_report(
    replay_id: str,
    replay_case_path: Path,
    inspections: list[OhlcvFileInspection],
    *,
    can_be_real_market_replay: bool,
    blockers: list[str],
    date_window: str,
) -> str:
    lines = [
        f"# {replay_id} Data Quality Report",
        "",
        f"generated_at: {datetime.now(timezone.utc).isoformat()}",
        f"replay_case: {replay_case_path}",
        f"date_window: {date_window}",
        f"can_be_real_market_replay: {str(can_be_real_market_replay).lower()}",
        "",
        "## Files inspected",
    ]
    for inspection in inspections:
        lines.extend(
            [
                f"- path: {inspection.path}",
                f"  exists: {str(inspection.exists).lower()}",
                f"  file_type: {inspection.file_type}",
                f"  row_count: {inspection.row_count}",
                f"  first_timestamp: {inspection.first_timestamp}",
                f"  last_timestamp: {inspection.last_timestamp}",
                f"  timezone: {inspection.timezone}",
                f"  source: {inspection.source}",
                f"  feed: {inspection.feed}",
                f"  adjustment: {inspection.adjustment}",
                f"  quality_status: {inspection.quality_status}",
                f"  missing_columns: {inspection.missing_columns}",
                f"  duplicate_timestamps: {inspection.duplicate_timestamps}",
            ]
        )
        if inspection.issues:
            lines.append(f"  issues: {inspection.issues}")
    lines.extend(["", "## Summary"])
    if inspections and all(item.quality_status == "PASS" for item in inspections):
        lines.append("- data_quality_status: PASSED")
    else:
        lines.append("- data_quality_status: FAILED")
    if blockers:
        lines.append("- blocking_issues:")
        lines.extend(f"  - {blocker}" for blocker in blockers)
    else:
        lines.append("- blocking_issues: none")
    lines.append(f"- can_be_real_market_replay: {str(can_be_real_market_replay).lower()}")
    return "\n".join(lines)


def write_replay_data_quality_report(
    repo_root: Path,
    replay_id: str,
    replay_case_path: Path,
    inspections: list[OhlcvFileInspection],
    *,
    can_be_real_market_replay: bool,
    blockers: list[str],
    date_window: str,
) -> Path:
    output_dir = repo_root / "runs" / "replay"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{replay_id}_data_quality_report.md"
    output_path.write_text(
        render_replay_data_quality_report(
            replay_id,
            replay_case_path,
            inspections,
            can_be_real_market_replay=can_be_real_market_replay,
            blockers=blockers,
            date_window=date_window,
        )
    )
    return output_path
