"""Tests for generated project to task_card.yaml conversion."""

from __future__ import annotations

from pathlib import Path

import pytest

from auto_research.cli import build_rgb_ir_reid_example
from auto_research.core.task_card import validate_task_card
from auto_research.generation.project_generator import ProjectGenerator
from auto_research.generation.task_card_generator import TaskCardGenerator
from auto_research.planning.implementation_planner import ImplementationPlanner
from auto_research.validation.project_validator import ProjectValidator


def _generate_project(tmp_path: Path, *, validate: bool = True) -> tuple[Path, dict]:
    rts = build_rgb_ir_reid_example("rgb_ir_attention_test")
    plan = ImplementationPlanner().build_plan(rts)
    result = ProjectGenerator().generate(
        rts=rts,
        plan=plan,
        output_dir=tmp_path / "generated_projects",
        overwrite=True,
    )
    project_dir = Path(result["project_dir"])
    if validate:
        ProjectValidator(timeout=120).validate(project_dir)
    return project_dir, plan


def test_generate_task_card_after_validation(tmp_path: Path) -> None:
    project_dir, plan = _generate_project(tmp_path)
    output_path = project_dir / "task_card.yaml"

    task_card = TaskCardGenerator().generate(project_dir, plan, output_path=output_path)

    assert output_path.exists()
    is_valid, message = validate_task_card(task_card)
    assert is_valid, message


def test_task_card_contains_adapter(tmp_path: Path) -> None:
    project_dir, plan = _generate_project(tmp_path)

    task_card = TaskCardGenerator().generate(project_dir, plan)

    assert "adapter" in task_card
    assert task_card["adapter"]["type"]
    assert task_card["adapter"]["train_entry"]
    assert task_card["adapter"]["base_config_path"]


def test_task_card_contains_search_space(tmp_path: Path) -> None:
    project_dir, plan = _generate_project(tmp_path)

    task_card = TaskCardGenerator().generate(project_dir, plan)

    assert "search_space" in task_card
    assert "lr" in task_card["search_space"]


def test_task_card_contains_objective(tmp_path: Path) -> None:
    project_dir, plan = _generate_project(tmp_path)

    task_card = TaskCardGenerator().generate(project_dir, plan)

    assert task_card["objective"]["metric"]
    assert task_card["objective"]["direction"]
    assert task_card["score"]["primary_metric"] == task_card["objective"]["metric"]


def test_fail_without_validation(tmp_path: Path) -> None:
    project_dir, plan = _generate_project(tmp_path, validate=False)

    with pytest.raises(FileNotFoundError, match="validation_result.json"):
        TaskCardGenerator().generate(project_dir, plan)


def test_allow_unvalidated(tmp_path: Path) -> None:
    project_dir, plan = _generate_project(tmp_path, validate=False)

    task_card = TaskCardGenerator().generate(project_dir, plan, allow_unvalidated=True)

    assert task_card["task_name"] == "rgb_ir_attention_test"
