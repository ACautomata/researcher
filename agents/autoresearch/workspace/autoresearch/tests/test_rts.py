"""Tests for Research Task Specification schema, IO, and validation."""

from __future__ import annotations

from pathlib import Path

from auto_research.cli import build_rgb_ir_reid_example
from auto_research.rts.io import load_rts, rts_from_dict, rts_to_dict, save_rts
from auto_research.rts.schema import ResearchTaskSpecification
from auto_research.rts.validation import RTSValidator


def test_create_rts() -> None:
    rts = build_rgb_ir_reid_example("rgb_ir_attention_test")

    assert isinstance(rts, ResearchTaskSpecification)
    assert rts.meta.project_name == "rgb_ir_attention_test"
    assert rts.task.type == "rgb_ir_reid"
    assert rts.adapter.type == "pytorch_yaml"


def test_save_and_load_yaml(tmp_path: Path) -> None:
    rts = build_rgb_ir_reid_example("rgb_ir_attention_test")
    path = tmp_path / "rts_example.yaml"

    save_rts(rts, path)
    loaded = load_rts(path)

    assert loaded.meta.project_name == "rgb_ir_attention_test"
    assert loaded.input.modalities == ["RGB", "IR"]
    assert loaded.goal.primary_metric == "mAP"


def test_validate_passed() -> None:
    rts = build_rgb_ir_reid_example("rgb_ir_attention_test")

    result = RTSValidator().validate(rts)

    assert result["passed"] is True
    assert result["errors"] == []


def test_invalid_optimization_direction_fails_validation() -> None:
    rts = build_rgb_ir_reid_example("rgb_ir_attention_test")
    rts.goal.optimization_direction = "larger_is_better"

    result = RTSValidator().validate(rts)

    assert result["passed"] is False
    assert "goal.optimization_direction" in result["errors"][0]


def test_invalid_adapter_type_fails_validation() -> None:
    rts = build_rgb_ir_reid_example("rgb_ir_attention_test")
    rts.adapter.type = "custom_runner"

    result = RTSValidator().validate(rts)

    assert result["passed"] is False
    assert any("adapter.type" in error for error in result["errors"])


def test_rts_dict_round_trip() -> None:
    rts = build_rgb_ir_reid_example("rgb_ir_attention_test")

    loaded = rts_from_dict(rts_to_dict(rts))

    assert loaded.meta.project_name == rts.meta.project_name
    assert loaded.search_space["batch_size"]["choices"] == [32, 64]
