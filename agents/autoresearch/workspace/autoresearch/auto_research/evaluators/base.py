"""Metric normalization and scoring helpers for AutoResearch evaluators."""

from __future__ import annotations

import re
from typing import Any, Mapping, Protocol

from auto_research.core.base import RunResult

_CANONICAL_NAME_ALIASES = {
    "map": "mAP",
    "meanaverageprecision": "mAP",
    "rank1": "rank1",
    "top1": "rank1",
    "r1": "rank1",
    "minp": "mINP",
    "loss": "loss",
    "finalloss": "loss",
}

_PERCENT_STYLE_METRICS = {
    "mAP",
    "rank1",
    "mINP",
    "precision",
    "recall",
    "f1",
    "accuracy",
    "acc",
    "top5",
}


class Evaluator(Protocol):
    """Protocol for converting raw outputs into normalized scores."""

    def evaluate(self, raw_output: dict[str, Any]) -> RunResult:
        """Parse raw outputs and compute the score used by optimization."""


def normalize_metric_name(name: str) -> str:
    """Normalize metric names from external projects into canonical keys.

    Supported alias handling includes:

    - ``mAP`` / ``map`` / ``test_metrics/mAP`` -> ``mAP``
    - ``Rank-1`` / ``rank1`` / ``top1`` / ``test_metrics/top1`` -> ``rank1``
    - ``loss`` / ``final_loss`` -> ``loss``

    Args:
        name: Raw metric name from logs or structured output.

    Returns:
        A canonical metric name suitable for downstream scoring.
    """

    if not isinstance(name, str):
        raise TypeError(
            f"Metric name must be a string, but received {type(name).__name__}."
        )

    stripped_name = name.strip()
    if not stripped_name:
        raise ValueError("Metric name cannot be empty.")

    tail = stripped_name.replace("\\", "/").split("/")[-1].strip()
    compact = re.sub(r"[^a-zA-Z0-9]+", "", tail).lower()

    if compact in _CANONICAL_NAME_ALIASES:
        return _CANONICAL_NAME_ALIASES[compact]

    fallback = re.sub(r"[^a-zA-Z0-9]+", "_", tail).strip("_").lower()
    if not fallback:
        raise ValueError(f"Metric name '{name}' cannot be normalized.")

    return fallback


def normalize_metrics(metrics: dict[str, Any]) -> dict[str, float]:
    """Normalize metric names and values from nested external outputs.

    This helper flattens nested dictionaries, canonicalizes known metric names,
    and converts numeric strings or percentage strings into floats. Known score
    metrics such as ``mAP`` or ``rank1`` are normalized onto a 0-100 scale, so
    both ``0.753`` and ``75.3`` become ``75.3``.

    Args:
        metrics: Raw metric mapping, potentially nested.

    Returns:
        A flat dictionary of normalized metric names to float values.

    Raises:
        TypeError: If ``metrics`` is not a dictionary.
    """

    if not isinstance(metrics, dict):
        raise TypeError(
            f"Metrics must be provided as a dictionary, but received {type(metrics).__name__}."
        )

    normalized: dict[str, float] = {}
    for raw_name, raw_value in _flatten_metrics_mapping(metrics):
        try:
            metric_name = normalize_metric_name(raw_name)
        except (TypeError, ValueError):
            continue

        metric_value = _coerce_metric_value(metric_name, raw_value)
        if metric_value is None:
            continue

        normalized[metric_name] = metric_value

    return normalized


def compute_score(metrics: dict[str, Any], score_config: dict[str, Any]) -> float:
    """Compute a scalar optimization score from normalized metrics.

    Scoring formula:

    ``primary_metric + weighted_secondary_metrics - weighted_penalties``

    If the primary metric cannot be found, the function returns
    ``invalid_score`` instead of raising.

    Args:
        metrics: Raw or already-normalized metrics mapping.
        score_config: Scoring configuration loaded from a task card.

    Returns:
        The scalar score used for optimization, or ``invalid_score`` when the
        score cannot be computed safely.
    """

    if not isinstance(score_config, dict):
        return -1_000_000_000.0

    invalid_score_raw = score_config.get("invalid_score", -1_000_000_000.0)
    try:
        invalid_score = float(invalid_score_raw)
    except (TypeError, ValueError):
        invalid_score = -1_000_000_000.0

    try:
        normalized_metrics = normalize_metrics(metrics)
    except TypeError:
        return invalid_score

    primary_metric_name_raw = score_config.get("primary_metric")
    if not isinstance(primary_metric_name_raw, str) or not primary_metric_name_raw.strip():
        return invalid_score

    try:
        primary_metric_name = normalize_metric_name(primary_metric_name_raw)
    except (TypeError, ValueError):
        return invalid_score

    primary_metric_value = normalized_metrics.get(primary_metric_name)
    if primary_metric_value is None:
        return invalid_score

    score = float(primary_metric_value)

    secondary_metrics = score_config.get("secondary_metrics", {})
    if isinstance(secondary_metrics, Mapping):
        for raw_name, raw_weight in secondary_metrics.items():
            if not isinstance(raw_name, str):
                continue
            try:
                metric_name = normalize_metric_name(raw_name)
                weight = float(raw_weight)
            except (TypeError, ValueError):
                continue
            metric_value = normalized_metrics.get(metric_name)
            if metric_value is not None:
                score += metric_value * weight

    penalties = score_config.get("penalties", {})
    if isinstance(penalties, Mapping):
        for raw_name, raw_weight in penalties.items():
            if not isinstance(raw_name, str):
                continue
            try:
                metric_name = normalize_metric_name(raw_name)
                weight = float(raw_weight)
            except (TypeError, ValueError):
                continue
            metric_value = normalized_metrics.get(metric_name)
            if metric_value is not None:
                score -= metric_value * weight

    return score


def _flatten_metrics_mapping(
    metrics: Mapping[str, Any],
    prefix: str = "",
) -> list[tuple[str, Any]]:
    """Flatten nested metric mappings into ``(path, value)`` pairs."""

    flattened: list[tuple[str, Any]] = []
    for key, value in metrics.items():
        if not isinstance(key, str):
            continue

        path = f"{prefix}/{key}" if prefix else key
        if isinstance(value, Mapping):
            flattened.extend(_flatten_metrics_mapping(value, prefix=path))
            continue

        flattened.append((path, value))

    return flattened


def _coerce_metric_value(metric_name: str, raw_value: Any) -> float | None:
    """Convert raw metric values into normalized floats."""

    numeric_value: float | None
    if isinstance(raw_value, bool):
        return None

    if isinstance(raw_value, (int, float)):
        numeric_value = float(raw_value)
    elif isinstance(raw_value, str):
        stripped = raw_value.strip()
        if not stripped:
            return None

        is_percent = stripped.endswith("%")
        if is_percent:
            stripped = stripped[:-1].strip()

        try:
            numeric_value = float(stripped)
        except ValueError:
            return None

        if is_percent:
            return numeric_value
    else:
        return None

    if metric_name in _PERCENT_STYLE_METRICS and 0.0 <= numeric_value <= 1.0:
        return numeric_value * 100.0

    return numeric_value
