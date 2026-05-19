"""Tests for optional PyTorch-style adapter implementations."""

from __future__ import annotations

from pathlib import Path
import sys

import yaml

from auto_research.adapters.pytorch_argparse_adapter import PyTorchArgparseAdapter
from auto_research.adapters.pytorch_yaml_adapter import PyTorchYamlAdapter
from auto_research.core.task_card import create_adapter_from_task_card, validate_task_card


def test_pytorch_yaml_adapter_writes_resolved_config_and_command(tmp_path: Path) -> None:
    base_config_path = tmp_path / "base.yaml"
    base_config_path.write_text(
        yaml.safe_dump(
            {
                "SOLVER": {"BASE_LR": 0.001, "WEIGHT_DECAY": 0.0005},
                "OUTPUT": {"DIR": "placeholder"},
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )

    adapter = PyTorchYamlAdapter(
        task_name="yaml_task",
        base_command=["python"],
        search_space={"lr": {"type": "float", "low": 1e-5, "high": 1e-3}},
        train_entry="examples/dummy_train.py",
        base_config_path=str(base_config_path),
        output_dir_key="OUTPUT.DIR",
        param_key_map={"lr": "SOLVER.BASE_LR"},
        output_root=str(tmp_path),
    )
    trial_dir = adapter.get_trial_dir(0)
    prepared = adapter.prepare_trial({"lr": 0.0003}, trial_dir)
    command = adapter.build_command(prepared, trial_dir)
    resolved_config = yaml.safe_load(
        Path(prepared["resolved_config_path"]).read_text(encoding="utf-8")
    )

    assert command[:3] == ["python", str((Path.cwd() / "examples/dummy_train.py").resolve()), "--config"]
    assert resolved_config["SOLVER"]["BASE_LR"] == 0.0003
    assert resolved_config["OUTPUT"]["DIR"] == trial_dir


def test_pytorch_argparse_adapter_builds_cli_flags_and_output_dir(tmp_path: Path) -> None:
    adapter = PyTorchArgparseAdapter(
        task_name="argparse_task",
        base_command=["python"],
        search_space={"lr": {"type": "float", "low": 1e-5, "high": 1e-3}},
        train_entry="examples/dummy_train.py",
        fixed_args=["--epochs", "10"],
        param_arg_map={"lr": "--learning-rate"},
        output_dir_arg="--save-dir",
        output_root=str(tmp_path),
    )
    trial_dir = adapter.get_trial_dir(0)
    prepared = adapter.prepare_trial({"lr": 0.0003}, trial_dir)
    command = adapter.build_command(prepared, trial_dir)

    assert command[:4] == [
        "python",
        str((Path.cwd() / "examples/dummy_train.py").resolve()),
        "--epochs",
        "10",
    ]
    assert "--learning-rate" in command
    assert "0.0003" in command
    assert "--save-dir" in command
    assert trial_dir in command


def test_task_card_can_create_pytorch_yaml_adapter(tmp_path: Path) -> None:
    base_config_path = tmp_path / "base.yaml"
    base_config_path.write_text(yaml.safe_dump({"OUTPUT": {"DIR": ""}}), encoding="utf-8")
    card = {
        "task_name": "yaml_card",
        "adapter": {
            "type": "pytorch_yaml",
            "train_entry": "examples/dummy_train.py",
            "base_config_path": str(base_config_path),
            "output_dir_key": "OUTPUT.DIR",
            "param_key_map": {"lr": "SOLVER.BASE_LR"},
        },
        "search_space": {
            "lr": {"type": "float", "low": 1e-5, "high": 1e-3, "log": True},
        },
        "score": {"primary_metric": "mAP", "invalid_score": -1_000_000_000},
    }

    is_valid, message = validate_task_card(card)
    adapter = create_adapter_from_task_card(card)

    assert is_valid is True
    assert message == "Task card is valid."
    assert isinstance(adapter, PyTorchYamlAdapter)


def test_task_card_can_create_pytorch_argparse_adapter() -> None:
    card = {
        "task_name": "argparse_card",
        "adapter": {
            "type": "pytorch_argparse",
            "train_entry": "examples/dummy_train.py",
            "fixed_args": ["--epochs", "10"],
            "param_arg_map": {"lr": "--learning-rate"},
            "output_dir_arg": "--output-dir",
        },
        "search_space": {
            "lr": {"type": "float", "low": 1e-5, "high": 1e-3, "log": True},
        },
        "score": {"primary_metric": "mAP", "invalid_score": -1_000_000_000},
    }

    is_valid, message = validate_task_card(card)
    adapter = create_adapter_from_task_card(card)

    assert is_valid is True
    assert message == "Task card is valid."
    assert isinstance(adapter, PyTorchArgparseAdapter)
