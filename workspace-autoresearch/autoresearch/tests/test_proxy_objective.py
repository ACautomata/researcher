"""Tests for proxy objective calculation."""

from __future__ import annotations

from auto_research.objective.proxy_objective import ProxyObjectiveCalculator


def test_single_metric_maximize() -> None:
    result = ProxyObjectiveCalculator().compute(
        {"mAP": 0.72},
        {"type": "single_metric", "primary_metric": "mAP", "direction": "maximize"},
    )

    assert result["score"] == 0.72
    assert result["passed_constraints"] is True


def test_single_metric_minimize() -> None:
    result = ProxyObjectiveCalculator().compute(
        {"loss": 0.25},
        {"type": "single_metric", "primary_metric": "loss", "direction": "minimize"},
    )

    assert result["score"] == -0.25


def test_weighted_sum() -> None:
    result = ProxyObjectiveCalculator().compute(
        {"mAP": 0.8, "Rank-1": 0.7, "mINP": 0.5},
        {
            "type": "weighted_sum",
            "direction": "maximize",
            "metrics": {"mAP": 0.6, "Rank-1": 0.3, "mINP": 0.1},
        },
    )

    assert result["score"] == 0.74
    assert result["details"]["contributions"]["mAP"] == 0.48


def test_missing_metric() -> None:
    result = ProxyObjectiveCalculator().compute(
        {"mAP": 0.8},
        {
            "type": "weighted_sum",
            "direction": "maximize",
            "metrics": {"mAP": 0.6, "Rank-1": 0.4},
        },
    )

    assert result["score"] == 0.48
    assert result["details"]["warnings"]


def test_constraint_pass() -> None:
    result = ProxyObjectiveCalculator().compute(
        {"Rank-1": 0.75, "training_time_hours": 3.0, "gpu_memory_gb": 12.0},
        {
            "type": "single_metric",
            "primary_metric": "Rank-1",
            "constraints": {
                "min_metrics": {"Rank-1": 0.7},
                "max_training_time_hours": 12,
                "max_gpu_memory_gb": 24,
            },
        },
    )

    assert result["passed_constraints"] is True
    assert result["violated_constraints"] == []


def test_constraint_fail() -> None:
    result = ProxyObjectiveCalculator().compute(
        {"Rank-1": 0.65, "training_time_hours": 14.0, "gpu_memory_gb": 30.0},
        {
            "type": "single_metric",
            "primary_metric": "Rank-1",
            "constraints": {
                "min_metrics": {"Rank-1": 0.7},
                "max_training_time_hours": 12,
                "max_gpu_memory_gb": 24,
            },
        },
    )

    assert result["passed_constraints"] is False
    assert "min_metrics.Rank-1" in result["violated_constraints"]
    assert "max_training_time_hours" in result["violated_constraints"]
    assert "max_gpu_memory_gb" in result["violated_constraints"]
