"""Focused tests for metrics normalization, parsing, and scoring."""

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


def test_normalize_metrics_handles_decimal_and_percentage_inputs() -> None:
    normalized = normalize_metrics(
        {
            "test_metrics": {"mAP": 0.763, "top1": "84.5%"},
            "final_loss": "0.72",
        }
    )

    assert normalized["mAP"] == 76.3
    assert normalized["rank1"] == 84.5
    assert normalized["loss"] == 0.72


def test_compute_score_returns_invalid_score_when_primary_metric_is_missing() -> None:
    score = compute_score(
        metrics={"loss": 0.5},
        score_config={"primary_metric": "mAP", "invalid_score": -1_000_000_000},
    )

    assert score == -1_000_000_000


def test_json_and_log_parsers_read_common_outputs(tmp_path: Path) -> None:
    (tmp_path / "metrics.json").write_text(
        json.dumps({"mAP": 76.3, "rank1": 84.5, "loss": 0.72}),
        encoding="utf-8",
    )
    (tmp_path / "train_stdout.log").write_text(
        "\n".join(["mAP: 76.3", "Rank-1: 84.5", "loss: 0.72"]),
        encoding="utf-8",
    )

    parsed_json = parse_json_metrics(str(tmp_path))
    parsed_log = parse_log_metrics(str(tmp_path))

    assert parsed_json["mAP"] == 76.3
    assert parsed_json["rank1"] == 84.5
    assert parsed_log["mAP"] == 76.3
    assert parsed_log["rank1"] == 84.5
