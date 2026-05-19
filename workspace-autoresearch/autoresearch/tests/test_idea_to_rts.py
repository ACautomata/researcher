"""Tests for heuristic idea to RTS conversion."""

from __future__ import annotations

from pathlib import Path

from auto_research.planning.idea_to_rts import IdeaToRTSConverter
from auto_research.readers.idea_reader import IdeaReader
from auto_research.rts.validation import RTSValidator


def test_rgb_ir_reid_idea() -> None:
    rts = IdeaToRTSConverter().convert(
        "设计一个用于RGB-IR跨模态行人重识别的双流网络。",
        project_name="rgb_ir_attention_test",
    )

    assert rts.task.type == "rgb_ir_reid"
    assert rts.input.modalities == ["RGB", "IR"]
    assert rts.output.type == "embedding"
    assert rts.goal.primary_metric == "mAP"
    assert RTSValidator().validate(rts)["passed"] is True


def test_attention_component() -> None:
    rts = IdeaToRTSConverter().convert(
        "设计一个用于RGB-IR跨模态行人重识别的双流网络，加入跨模态注意力融合模块。",
        project_name="rgb_ir_attention_test",
    )

    component_names = {item["name"] for item in rts.model.components}
    assert "cross_modal_attention" in component_names


def test_center_constraint_loss() -> None:
    rts = IdeaToRTSConverter().convert(
        "设计一个用于RGB-IR跨模态行人重识别的方法，加入中心约束损失。",
        project_name="rgb_ir_center_test",
    )

    loss_names = {item["name"] for item in rts.losses}
    assert "center_constraint" in loss_names


def test_unknown_idea_fallback_general_pytorch() -> None:
    rts = IdeaToRTSConverter().convert(
        "探索一种通用训练流程，用于验证新的模块设计。",
        project_name="generic_test",
    )

    assert rts.task.type == "general_pytorch"
    assert rts.baseline.template == "general_pytorch"


def test_idea_file_input(tmp_path: Path) -> None:
    idea_path = tmp_path / "idea.md"
    idea_path.write_text(
        "# Idea\n\n设计一个用于RGB-IR跨模态行人重识别的双流网络。",
        encoding="utf-8",
    )

    idea_text = IdeaReader().read_from_file(idea_path)
    rts = IdeaToRTSConverter().convert(idea_text, project_name="file_idea_test")

    assert "RGB-IR" in idea_text
    assert rts.task.type == "rgb_ir_reid"
