"""Evaluation helpers and score normalization utilities."""

from __future__ import annotations

from auto_research.evaluators.base import (
    Evaluator,
    compute_score,
    normalize_metric_name,
    normalize_metrics,
)
from auto_research.evaluators.json_parser import parse_json_metrics
from auto_research.evaluators.log_parser import parse_log_metrics

__all__ = [
    "Evaluator",
    "compute_score",
    "normalize_metric_name",
    "normalize_metrics",
    "parse_json_metrics",
    "parse_log_metrics",
]
