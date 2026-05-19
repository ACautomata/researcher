"""JSON-based metric parsers for external training outputs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from auto_research.evaluators.base import normalize_metrics

_DEFAULT_JSON_FILENAMES = ("metrics.json", "result.json", "summary.json")


def parse_json_metrics(
    trial_dir: str,
    filenames: tuple[str, ...] = _DEFAULT_JSON_FILENAMES,
) -> dict[str, float]:
    """Parse metrics from common JSON result files in a trial directory.

    Missing files or malformed JSON do not raise; the function returns whatever
    metrics can be recovered, or an empty dictionary when none are found.

    Args:
        trial_dir: The trial output directory.
        filenames: Candidate JSON filenames to inspect.

    Returns:
        A dictionary of normalized metric names to float values.
    """

    trial_path = Path(trial_dir)
    parsed_metrics: dict[str, float] = {}

    for filename in filenames:
        file_path = trial_path / filename
        if not file_path.exists() or not file_path.is_file():
            continue

        try:
            payload: Any = json.loads(file_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue

        if not isinstance(payload, dict):
            continue

        parsed_metrics.update(normalize_metrics(payload))

    return parsed_metrics
