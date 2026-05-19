"""Tests for generated PyTorch projects."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

import yaml

from auto_research.cli import build_rgb_ir_reid_example
from auto_research.generation.project_generator import ProjectGenerator
from auto_research.planning.implementation_planner import ImplementationPlanner
from auto_research.rts.schema import RTSBaseline


def _build_general_rts():
    rts = build_rgb_ir_reid_example("general_project")
    rts.task.type = "general_pytorch"
    rts.input.modalities = ["Tensor"]
    rts.output.type = "class_logits"
    rts.baseline = RTSBaseline(template="general_pytorch")
    rts.model.components = []
    rts.losses = [{"name": "cross_entropy", "weight": 1.0, "params": {}}]
    rts.goal.primary_metric = "accuracy"
    rts.goal.secondary_metrics = []
    rts.metrics = ["accuracy", "loss"]
    return rts


def _generate(tmp_path: Path, rts=None):
    rts = rts or build_rgb_ir_reid_example("rgb_ir_attention_test")
    plan = ImplementationPlanner().build_plan(rts)
    result = ProjectGenerator().generate(rts, plan, tmp_path / "generated_projects", overwrite=True)
    return rts, plan, result, Path(result["project_dir"])


def test_generate_general_project(tmp_path: Path) -> None:
    _rts, _plan, _result, project_dir = _generate(tmp_path, _build_general_rts())

    assert (project_dir / "train.py").exists()
    assert (project_dir / "configs" / "config.yaml").exists()


def test_generate_rgb_ir_project(tmp_path: Path) -> None:
    _rts, _plan, _result, project_dir = _generate(tmp_path)

    assert (project_dir / "models").is_dir()
    assert (project_dir / "losses").is_dir()
    assert (project_dir / "datasets").is_dir()


def test_generated_config_exists(tmp_path: Path) -> None:
    _rts, _plan, _result, project_dir = _generate(tmp_path)

    config_path = project_dir / "configs" / "config.yaml"
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))

    assert "project" in config
    assert "training" in config
    assert "dataset" in config
    assert "model" in config
    assert "losses" in config


def test_create_component_file(tmp_path: Path) -> None:
    rts = build_rgb_ir_reid_example("rgb_ir_attention_test")
    rts.model.components.append(
        {"name": "cross_modal_attention", "type": "attention", "purpose": "Fuse modalities."}
    )

    _rts, _plan, _result, project_dir = _generate(tmp_path, rts)

    assert (project_dir / "models" / "cross_modal_attention.py").exists()


def test_create_loss_file(tmp_path: Path) -> None:
    _rts, _plan, _result, project_dir = _generate(tmp_path)

    assert (project_dir / "losses" / "center_constraint.py").exists()


def test_generated_project_can_train_one_step(tmp_path: Path) -> None:
    _rts, _plan, _result, project_dir = _generate(tmp_path)

    completed = subprocess.run(
        [
            sys.executable,
            "train.py",
            "--config",
            "configs/config.yaml",
            "--max-steps",
            "1",
        ],
        cwd=project_dir,
        check=True,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert (project_dir / "outputs" / "metrics.json").exists()
    assert (project_dir / "outputs" / "checkpoint.pt").exists()
