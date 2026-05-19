"""Tests for RTS to implementation plan generation."""

from __future__ import annotations

from auto_research.cli import build_rgb_ir_reid_example
from auto_research.planning.baseline_selector import BaselineSelector
from auto_research.planning.implementation_planner import ImplementationPlanner


def test_build_plan_from_valid_rts() -> None:
    rts = build_rgb_ir_reid_example("rgb_ir_attention_test")

    plan = ImplementationPlanner().build_plan(rts)

    assert "project" in plan
    assert "template" in plan
    assert "config_requirements" in plan
    assert plan["project"]["name"] == "rgb_ir_attention_test"


def test_select_rgb_ir_template() -> None:
    rts = build_rgb_ir_reid_example("rgb_ir_attention_test")
    rts.baseline.template = None
    rts.task.type = "rgb_ir_reid"

    result = BaselineSelector().select(rts)

    assert result["selected_template"] == "rgb_ir_reid"


def test_files_to_create_for_component() -> None:
    rts = build_rgb_ir_reid_example("rgb_ir_attention_test")
    rts.model.components.append(
        {
            "name": "cross_modal_attention",
            "type": "attention",
            "purpose": "Fuse RGB and IR features.",
        }
    )

    plan = ImplementationPlanner().build_plan(rts)

    paths = {item["path"] for item in plan["files_to_create"]}
    assert "models/cross_modal_attention.py" in paths


def test_files_to_create_for_custom_loss() -> None:
    rts = build_rgb_ir_reid_example("rgb_ir_attention_test")

    plan = ImplementationPlanner().build_plan(rts)

    paths = {item["path"] for item in plan["files_to_create"]}
    assert "losses/center_constraint.py" in paths


def test_task_card_requirements() -> None:
    rts = build_rgb_ir_reid_example("rgb_ir_attention_test")

    plan = ImplementationPlanner().build_plan(rts)
    task_card = plan["task_card_requirements"]

    assert "adapter" in task_card
    assert "search_space" in task_card
    assert "objective" in task_card
    assert task_card["objective"]["metric"] == "mAP"


def test_adapter_fallback() -> None:
    rts = build_rgb_ir_reid_example("rgb_ir_attention_test")
    rts.adapter.type = ""
    rts.adapter.train_entry = None
    rts.adapter.config_path = None

    plan = ImplementationPlanner().build_plan(rts)

    assert plan["adapter_requirements"]["adapter_type"] == "pytorch_yaml"
    assert plan["adapter_requirements"]["train_entry"] == "train.py"
    assert plan["adapter_requirements"]["config_path"] == "configs/config.yaml"


def test_render_markdown() -> None:
    rts = build_rgb_ir_reid_example("rgb_ir_attention_test")
    planner = ImplementationPlanner()
    plan = planner.build_plan(rts)

    markdown = planner.render_markdown(plan)

    assert "Implementation Plan" in markdown
    assert "Files to Create" in markdown
    assert "Task Card Requirements" in markdown
