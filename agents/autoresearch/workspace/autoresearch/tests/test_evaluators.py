"""Tests for evaluator utilities and parsers."""

from __future__ import annotations

import json
from pathlib import Path

from auto_research.evaluators.base import (
    compute_score,
    normalize_metric_name,
    normalize_metrics,
)
from auto_research.evaluators.json_parser import parse_json_metrics
from auto_research.evaluators.log_parser import parse_log_metrics


def test_normalize_metric_name_maps_common_aliases() -> None:
    assert normalize_metric_name("mAP") == "mAP"
    assert normalize_metric_name("map") == "mAP"
    assert normalize_metric_name("test_metrics/mAP") == "mAP"
    assert normalize_metric_name("Rank-1") == "rank1"
    assert normalize_metric_name("top1") == "rank1"
    assert normalize_metric_name("final_loss") == "loss"


def test_normalize_metrics_handles_nested_keys_and_scales() -> None:
    metrics = {
        "test_metrics": {
            "mAP": 0.753,
            "top1": "84.2%",
        },
        "final_loss": "0.812",
    }

    normalized = normalize_metrics(metrics)

    assert normalized["mAP"] == 75.3
    assert normalized["rank1"] == 84.2
    assert normalized["loss"] == 0.812


def test_compute_score_uses_invalid_score_when_primary_metric_is_missing() -> None:
    score = compute_score(
        metrics={"loss": 0.5},
        score_config={
            "primary_metric": "mAP",
            "secondary_metrics": {"rank1": 0.2},
            "invalid_score": -1_000_000_000,
        },
    )

    assert score == -1_000_000_000


def test_compute_score_combines_primary_secondary_and_penalties() -> None:
    score = compute_score(
        metrics={
            "test_metrics": {"mAP": 0.753, "Rank-1": 0.842, "mINP": 0.601},
            "training_time": 120,
        },
        score_config={
            "primary_metric": "mAP",
            "secondary_metrics": {"rank1": 0.2, "mINP": 0.1},
            "penalties": {"training_time": 0.001},
            "invalid_score": -1_000_000_000,
        },
    )

    expected = 75.3 + 84.2 * 0.2 + 60.1 * 0.1 - 120 * 0.001
    assert abs(score - expected) < 1e-9


def test_parse_json_metrics_reads_common_result_files(tmp_path: Path) -> None:
    payload = {
        "test_metrics": {
            "mAP": 0.753,
            "top1": 0.842,
        },
        "final_loss": 0.812,
    }
    (tmp_path / "metrics.json").write_text(json.dumps(payload), encoding="utf-8")

    parsed = parse_json_metrics(str(tmp_path))

    assert parsed["mAP"] == 75.3
    assert parsed["rank1"] == 84.2
    assert parsed["loss"] == 0.812


def test_parse_log_metrics_extracts_common_log_patterns(tmp_path: Path) -> None:
    (tmp_path / "train_stdout.log").write_text(
        "\n".join(
            [
                "epoch=10",
                "mAP: 75.3",
                "Rank-1: 84.2",
                "rank1=84.2",
                "loss: 0.812",
            ]
        ),
        encoding="utf-8",
    )

    parsed = parse_log_metrics(str(tmp_path))

    assert parsed["mAP"] == 75.3
    assert parsed["rank1"] == 84.2
    assert parsed["loss"] == 0.812


def test_parsers_return_empty_metrics_when_files_are_missing() -> None:
    missing_dir = str(Path("S:/auto_research/nonexistent_trial_dir"))

    assert parse_json_metrics(missing_dir) == {}
    assert parse_log_metrics(missing_dir) == {}
