from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd
import yaml


def _stringify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if hasattr(value, "isoformat") and not isinstance(value, str):
        try:
            return value.isoformat()
        except TypeError:
            pass
    if pd.isna(value):
        return ""
    return str(value)


def load_ohlcv_rows(path: Path) -> list[dict[str, str]]:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        with path.open(newline="") as f:
            return list(csv.DictReader(f))
    if suffix == ".parquet":
        frame = pd.read_parquet(path)
        if "timestamp" in frame.columns:
            frame = frame.sort_values("timestamp")
        rows: list[dict[str, str]] = []
        for record in frame.to_dict(orient="records"):
            rows.append({key: _stringify(value) for key, value in record.items()})
        return rows
    raise ValueError(f"Unsupported OHLCV file type: {path.suffix or '(none)'}")


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text())
    return data if isinstance(data, dict) else {}


def _resolve_path(repo_root: Path, value: Any) -> Path:
    path = Path(str(value))
    return path if path.is_absolute() else repo_root / path


def _resolve_manifest_path(manifest_root: Path, value: Any) -> Path:
    path = Path(str(value))
    if path.is_absolute():
        return path
    candidates = [manifest_root / path]
    if len(manifest_root.parents) >= 3:
        candidates.append(manifest_root.parents[2] / path)
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[-1]


def load_replay_handoff_manifest(repo_root: Path) -> tuple[dict[str, Any], Path] | tuple[None, None]:
    config_path = repo_root / "configs" / "replay_discovery.yaml"
    config = load_yaml(config_path)
    manifest_path_value = config.get("handoff_manifest_path")
    artifact_root_value = config.get("replay_data_root") or config.get("artifact_root")

    if manifest_path_value:
        manifest_path = _resolve_path(repo_root, manifest_path_value)
    elif artifact_root_value:
        manifest_path = _resolve_path(repo_root, artifact_root_value) / "strategy_lab_handoff.yaml"
    else:
        return None, None

    if not manifest_path.exists():
        return None, None
    manifest = load_yaml(manifest_path)
    return manifest, manifest_path.parent


def resolve_historical_market_data_paths(repo_root: Path, symbol: str) -> dict[str, Path]:
    manifest, manifest_root = load_replay_handoff_manifest(repo_root)
    if manifest:
        allowed = {str(item) for item in (manifest.get("allowed_for_replay") or [])}
        blocked = {str(item) for item in (manifest.get("blocked_for_replay") or [])}
        full_paths = manifest.get("full_data_paths") or {}
        symbol_paths = full_paths.get(symbol.upper()) or full_paths.get(symbol) or {}
        if isinstance(symbol_paths, dict):
            resolved: dict[str, Path] = {}
            for timeframe, path_values in symbol_paths.items():
                timeframe = str(timeframe)
                if allowed and timeframe not in allowed:
                    continue
                if timeframe in blocked:
                    continue
                if isinstance(path_values, (list, tuple)):
                    path_value = path_values[0] if path_values else None
                else:
                    path_value = path_values
                if not path_value:
                    continue
                resolved[timeframe] = _resolve_manifest_path(manifest_root, path_value)
            if resolved:
                return resolved

    index_path = repo_root / "data_refs" / "historical_market_data" / "artifact_index.yaml"
    index = load_yaml(index_path)
    allowed = {str(item) for item in (index.get("allowed_for_replay") or [])}
    blocked = {str(item) for item in (index.get("blocked_for_replay") or [])}
    items = index.get("items") or []
    if isinstance(items, list):
        resolved: dict[str, Path] = {}
        for item in items:
            if not isinstance(item, dict):
                continue
            if str(item.get("symbol", "")).upper() != symbol.upper():
                continue
            timeframe = str(item.get("timeframe", ""))
            if allowed and timeframe not in allowed:
                continue
            if timeframe in blocked:
                continue
            if str(item.get("artifact_kind", "")).lower() != "full":
                continue
            path_value = item.get("path")
            if not timeframe or not path_value:
                continue
            resolved[timeframe] = _resolve_path(repo_root, path_value)
        if resolved:
            return resolved

    base = repo_root / "data_refs" / "google_drive"
    fallback = {
        "1Day": base / f"{symbol}_1Day_sample.csv",
        "5Min": base / f"{symbol}_5Min_sample.csv",
    }
    return {tf: path for tf, path in fallback.items() if path.exists()}


def resolve_full_historical_data_root(repo_root: Path) -> Path | None:
    index_path = repo_root / "data_refs" / "historical_market_data" / "artifact_index.yaml"
    index = load_yaml(index_path)
    artifact_root = index.get("artifact_root")
    if artifact_root:
        root = Path(str(artifact_root))
        return root if root.is_absolute() else repo_root / root
    return None
