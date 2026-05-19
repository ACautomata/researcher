"""Regex-based parsers for extracting metrics from training logs."""

from __future__ import annotations

from pathlib import Path
import re

from auto_research.evaluators.base import normalize_metrics

_METRIC_PATTERN = re.compile(
    r"(?P<name>[A-Za-z][A-Za-z0-9_/\-]*)\s*[:=]\s*(?P<value>[+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?%?)"
)


def parse_log_metrics(
    trial_dir: str,
    log_filename: str = "train_stdout.log",
) -> dict[str, float]:
    """Parse common scalar metrics from a training stdout log.

    Supported patterns include examples such as:

    - ``mAP: 75.3``
    - ``Rank-1: 84.2``
    - ``rank1=84.2``
    - ``loss: 0.812``

    When metrics appear multiple times, the latest match wins. Missing logs or
    unmatched patterns return an empty dictionary instead of raising.

    Args:
        trial_dir: The trial output directory.
        log_filename: The stdout log filename to inspect.

    Returns:
        A dictionary of normalized metric names to float values.
    """

    log_path = Path(trial_dir) / log_filename
    if not log_path.exists() or not log_path.is_file():
        return {}

    try:
        content = log_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return {}

    raw_metrics: dict[str, str] = {}
    for match in _METRIC_PATTERN.finditer(content):
        raw_metrics[match.group("name")] = match.group("value")

    return normalize_metrics(raw_metrics)
