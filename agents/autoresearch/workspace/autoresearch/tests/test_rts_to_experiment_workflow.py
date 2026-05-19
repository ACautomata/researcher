"""Tests for the end-to-end RTS to experiment workflow."""

from __future__ import annotations

from pathlib import Path

from auto_research.cli import build_rgb_ir_reid_example
from auto_research.rts.io import save_rts
from auto_research.rts.schema import ResearchTaskSpecification
from auto_research.workflows.rts_to_experiment_workflow import RtsToExperimentWorkflow


def test_run_from_rts_without_training(tmp_path: Path) -> None:
    rts_path = tmp_path / "rts.yaml"
    save_rts(build_rgb_ir_reid_example("rgb_ir_attention_test"), rts_path)

    result = RtsToExperimentWorkflow().run(
        rts_path=rts_path,
        output_dir=tmp_path / "generated_projects",
        overwrite=True,
    )

    project_dir = Path(result["project_dir"])
    assert project_dir.exists()
    assert (project_dir / "requirement.md").exists()
    assert (project_dir / "implementation_plan.yaml").exists()
    assert (project_dir / "validation_result.json").exists()
    assert (project_dir / "task_card.yaml").exists()
    assert (project_dir / "final_report.md").exists()


def test_workflow_validation_passed(tmp_path: Path) -> None:
    rts_path = tmp_path / "rts.yaml"
    save_rts(build_rgb_ir_reid_example("rgb_ir_attention_test"), rts_path)

    result = RtsToExperimentWorkflow().run(
        rts_path=rts_path,
        output_dir=tmp_path / "generated_projects",
        overwrite=True,
    )

    assert result["validation_passed"] is True


def test_workflow_no_training_by_default(tmp_path: Path) -> None:
    rts_path = tmp_path / "rts.yaml"
    save_rts(build_rgb_ir_reid_example("rgb_ir_attention_test"), rts_path)

    result = RtsToExperimentWorkflow().run(
        rts_path=rts_path,
        output_dir=tmp_path / "generated_projects",
        overwrite=True,
    )

    assert result["training_submitted"] is False


def test_workflow_invalid_rts_stops(tmp_path: Path) -> None:
    rts_path = tmp_path / "invalid_rts.yaml"
    invalid = ResearchTaskSpecification()
    save_rts(invalid, rts_path)

    result = RtsToExperimentWorkflow().run(
        rts_path=rts_path,
        output_dir=tmp_path / "generated_projects",
        overwrite=True,
        allow_invalid_rts=False,
    )

    assert result["success"] is False
    assert result["errors"]
    assert Path(result["final_report_path"]).exists()
