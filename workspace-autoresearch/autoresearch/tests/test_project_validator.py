"""Tests for generated project validation."""

from __future__ import annotations

from pathlib import Path

from auto_research.cli import build_rgb_ir_reid_example
from auto_research.generation.project_generator import ProjectGenerator
from auto_research.planning.implementation_planner import ImplementationPlanner
from auto_research.validation.project_validator import ProjectValidator


def _generate_project(tmp_path: Path) -> Path:
    rts = build_rgb_ir_reid_example("rgb_ir_attention_test")
    plan = ImplementationPlanner().build_plan(rts)
    result = ProjectGenerator().generate(
        rts=rts,
        plan=plan,
        output_dir=tmp_path / "generated_projects",
        overwrite=True,
    )
    return Path(result["project_dir"])


def test_validate_generated_project(tmp_path: Path) -> None:
    project_dir = _generate_project(tmp_path)

    result = ProjectValidator(timeout=120).validate(project_dir)

    assert Path(result["validation_result_path"]).exists()
    assert Path(result["validation_report_path"]).exists()


def test_validation_passed_for_generated_project(tmp_path: Path) -> None:
    project_dir = _generate_project(tmp_path)

    result = ProjectValidator(timeout=120).validate(project_dir)

    assert result["passed"] is True


def test_missing_config_fails(tmp_path: Path) -> None:
    project_dir = _generate_project(tmp_path)
    (project_dir / "configs" / "config.yaml").unlink()

    result = ProjectValidator(timeout=120).validate(project_dir)

    assert result["passed"] is False
    assert result["errors"]


def test_metrics_json_valid_check(tmp_path: Path) -> None:
    project_dir = _generate_project(tmp_path)

    result = ProjectValidator(timeout=120).validate(project_dir)
    check_names = {check["name"] for check in result["checks"]}

    assert "metrics_json_valid" in check_names
