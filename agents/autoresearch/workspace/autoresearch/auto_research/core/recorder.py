"""Trial result recording helpers for study-level TSV and JSONL outputs."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Mapping

_RESULT_FIELDS = [
    "task_name",
    "trial_id",
    "status",
    "score",
    "trial_config",
    "metrics",
    "command",
    "trial_dir",
    "start_time",
    "end_time",
    "duration_seconds",
    "error_message",
]


@dataclass(slots=True)
class TrialRecorder:
    """Append-only recorder for study-level trial outputs."""

    output_dir: str

    @property
    def tsv_path(self) -> Path:
        """Return the path for the human-readable TSV output."""

        return Path(self.output_dir) / "results.tsv"

    @property
    def jsonl_path(self) -> Path:
        """Return the path for the full JSONL output."""

        return Path(self.output_dir) / "results.jsonl"

    def record_trial(self, record: Mapping[str, Any]) -> bool:
        """Safely append one trial record to both TSV and JSONL outputs.

        Write failures are swallowed and reported via the boolean return value,
        so a recorder problem never crashes the study loop.
        """

        try:
            normalized = normalize_trial_record(record)
            self._ensure_output_dir()
            self._append_tsv(normalized)
            self._append_jsonl(normalized)
            return True
        except Exception:
            return False

    def _ensure_output_dir(self) -> None:
        """Create the recorder output directory when it does not exist."""

        Path(self.output_dir).mkdir(parents=True, exist_ok=True)

    def _append_tsv(self, record: Mapping[str, Any]) -> None:
        """Append one TSV row and flush immediately."""

        file_exists = self.tsv_path.exists()
        with self.tsv_path.open("a", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=_RESULT_FIELDS,
                delimiter="\t",
                extrasaction="ignore",
            )
            if not file_exists:
                writer.writeheader()
            writer.writerow(_format_tsv_row(record))
            handle.flush()

    def _append_jsonl(self, record: Mapping[str, Any]) -> None:
        """Append one JSON object line and flush immediately."""

        with self.jsonl_path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(dict(record), ensure_ascii=True, sort_keys=True))
            handle.write("\n")
            handle.flush()


def build_trial_record(
    *,
    task_name: str,
    trial_id: str,
    status: str,
    score: float | None,
    trial_config: Mapping[str, Any] | None,
    metrics: Mapping[str, Any] | None,
    command: list[str] | None,
    trial_dir: str,
    start_time: str,
    end_time: str,
    duration_seconds: float | None,
    error_message: str,
) -> dict[str, Any]:
    """Build a canonical recorder payload."""

    return normalize_trial_record(
        {
            "task_name": task_name,
            "trial_id": trial_id,
            "status": status,
            "score": score,
            "trial_config": dict(trial_config or {}),
            "metrics": dict(metrics or {}),
            "command": list(command or []),
            "trial_dir": trial_dir,
            "start_time": start_time,
            "end_time": end_time,
            "duration_seconds": duration_seconds,
            "error_message": error_message,
        }
    )


def normalize_trial_record(record: Mapping[str, Any]) -> dict[str, Any]:
    """Normalize a record into the standard recorder schema."""

    return {
        "task_name": str(record.get("task_name", "")),
        "trial_id": str(record.get("trial_id", "")),
        "status": str(record.get("status", "")),
        "score": _coerce_optional_float(record.get("score")),
        "trial_config": _coerce_mapping(record.get("trial_config")),
        "metrics": _coerce_mapping(record.get("metrics")),
        "command": _coerce_command(record.get("command")),
        "trial_dir": str(record.get("trial_dir", "")),
        "start_time": _normalize_timestamp(record.get("start_time")),
        "end_time": _normalize_timestamp(record.get("end_time")),
        "duration_seconds": _coerce_optional_float(record.get("duration_seconds")),
        "error_message": str(record.get("error_message", "")),
    }


def utc_now_iso() -> str:
    """Return the current UTC time in ISO 8601 format."""

    return datetime.now(timezone.utc).isoformat()


def _format_tsv_row(record: Mapping[str, Any]) -> dict[str, str]:
    """Convert a normalized record into a TSV-friendly string mapping."""

    row: dict[str, str] = {}
    for field in _RESULT_FIELDS:
        value = record.get(field)
        if field in {"trial_config", "metrics", "command"}:
            row[field] = json.dumps(value, ensure_ascii=True, sort_keys=True)
        elif value is None:
            row[field] = ""
        else:
            row[field] = str(value)
    return row


def _coerce_mapping(value: Any) -> dict[str, Any]:
    """Coerce mapping-like values into plain dictionaries."""

    if isinstance(value, Mapping):
        return dict(value)
    return {}


def _coerce_command(value: Any) -> list[str]:
    """Coerce commands into ``list[str]``."""

    if not isinstance(value, list):
        return []
    return [str(item) for item in value]


def _coerce_optional_float(value: Any) -> float | None:
    """Coerce optional numeric values safely."""

    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _normalize_timestamp(value: Any) -> str:
    """Normalize optional timestamps into strings."""

    if value is None:
        return ""
    return str(value)
