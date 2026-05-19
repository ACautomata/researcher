"""Tests for task card loading, validation, and adapter creation."""

from __future__ import annotations

from pathlib import Path
import sys

import pytest
import yaml

from auto_research.adapters.subprocess_adapter import SubprocessAdapter
from auto_research.core.task_card import (
    create_adapter_from_task_card,
    load_task_card,
    validate_task_card,
)


def _build_valid_task_card() -> dict:
    return {
        "task_name": "demo_hpo",
        "adapter": {
            "type": "subprocess",
            "command_template": [
                sys.executable,
                "examples/dummy_train.py",
                "--lr",
                "{lr}",
                "--batch-size",
                "{batch_size}",
                "--output-dir",
                "{trial_dir}",
            ],
        },
        "search_space": {
            "lr": {"type": "float", "low": 1e-5, "high": 1e-3, "log": True},
            "batch_size": {"type": "categorical", "choices": [32, 64]},
        },
        "score": {
            "primary_metric": "mAP",
            "secondary_metrics": {"rank1": 0.2},
            "invalid_score": -1_000_000_000,
        },
        "constraints": {"timeout": 300, "max_trials": 20},
    }


def test_load_task_card_reads_yaml_file(tmp_path: Path) -> None:
    card_path = tmp_path / "task_card.yaml"
    payload = _build_valid_task_card()
    card_path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")

    card = load_task_card(str(card_path))

    assert card["task_name"] == "demo_hpo"
    assert card["adapter"]["type"] == "subprocess"


def test_validate_task_card_accepts_valid_subprocess_card() -> None:
    is_valid, message = validate_task_card(_build_valid_task_card())

    assert is_valid is True
    assert message == "Task card is valid."


def test_validate_task_card_rejects_missing_required_field() -> None:
    card = _build_valid_task_card()
    del card["search_space"]

    is_valid, message = validate_task_card(card)

    assert is_valid is False
    assert "missing required field 'search_space'" in message


def test_validate_task_card_rejects_bad_adapter_type() -> None:
    card = _build_valid_task_card()
    card["adapter"]["type"] = "unknown_adapter"

    is_valid, message = validate_task_card(card)

    assert is_valid is False
    assert "Unsupported adapter.type" in message


def test_create_adapter_from_task_card_returns_subprocess_adapter() -> None:
    adapter = create_adapter_from_task_card(_build_valid_task_card())

    assert isinstance(adapter, SubprocessAdapter)
    assert adapter.task_name == "demo_hpo"
    assert adapter.command_template is not None


def test_adapter_created_from_task_card_renders_command_template(tmp_path: Path) -> None:
    adapter = create_adapter_from_task_card(_build_valid_task_card())
    trial_dir = adapter.get_trial_dir(0)
    prepared = adapter.prepare_trial({"lr": 0.0003, "batch_size": 64}, trial_dir)

    command = adapter.build_command(prepared, trial_dir)

    assert command[0] == sys.executable
    assert "--lr" in command
    assert "0.0003" in command
    assert "--batch-size" in command
    assert "64" in command
    assert str(Path(trial_dir)) in command


def test_validate_task_card_rejects_incomplete_pytorch_yaml_card() -> None:
    card = _build_valid_task_card()
    card["adapter"] = {"type": "pytorch_yaml"}

    is_valid, message = validate_task_card(card)

    assert is_valid is False
    assert "adapter.train_entry" in message


def test_validate_task_card_accepts_safety_section() -> None:
    card = _build_valid_task_card()
    card["safety"] = {
        "max_consecutive_failures": 5,
        "allow_commands": ["python", "python3"],
    }

    is_valid, message = validate_task_card(card)

    assert is_valid is True
    assert message == "Task card is valid."
