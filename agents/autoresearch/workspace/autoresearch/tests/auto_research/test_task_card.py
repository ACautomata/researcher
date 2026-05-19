"""Focused tests for YAML task cards and adapter creation."""

from __future__ import annotations

from pathlib import Path
import sys

import yaml

from auto_research.adapters.subprocess_adapter import SubprocessAdapter
from auto_research.core.task_card import (
    create_adapter_from_task_card,
    load_task_card,
    validate_task_card,
)


def _build_task_card(output_root: str) -> dict:
    return {
        "task_name": "dummy_hpo",
        "adapter": {
            "type": "subprocess",
            "output_root": output_root,
            "command_template": [
                sys.executable,
                "examples/dummy_train.py",
                "--lr",
                "{lr}",
                "--batch-size",
                "{batch_size}",
                "--epochs",
                "{epochs}",
                "--output-dir",
                "{trial_dir}",
            ],
        },
        "search_space": {
            "lr": {"type": "float", "low": 1e-5, "high": 1e-3, "log": True},
            "batch_size": {"type": "categorical", "choices": [32, 64]},
            "epochs": {"type": "int", "low": 1, "high": 3},
        },
        "score": {"primary_metric": "mAP", "invalid_score": -1_000_000_000},
        "constraints": {"timeout": 30, "max_trials": 5},
        "safety": {"allow_commands": ["python", "python3"]},
    }


def test_load_task_card_reads_yaml(tmp_path: Path) -> None:
    card_path = tmp_path / "dummy_hpo.yaml"
    card_path.write_text(
        yaml.safe_dump(_build_task_card(str(tmp_path)), sort_keys=False),
        encoding="utf-8",
    )

    loaded = load_task_card(str(card_path))

    assert loaded["task_name"] == "dummy_hpo"
    assert loaded["adapter"]["type"] == "subprocess"


def test_validate_task_card_accepts_subprocess_card(tmp_path: Path) -> None:
    assert validate_task_card(_build_task_card(str(tmp_path))) == (True, "Task card is valid.")


def test_validate_task_card_rejects_missing_required_field(tmp_path: Path) -> None:
    card = _build_task_card(str(tmp_path))
    del card["search_space"]

    is_valid, message = validate_task_card(card)

    assert is_valid is False
    assert "missing required field 'search_space'" in message


def test_create_adapter_from_task_card_returns_subprocess_adapter(tmp_path: Path) -> None:
    adapter = create_adapter_from_task_card(_build_task_card(str(tmp_path)))

    assert isinstance(adapter, SubprocessAdapter)
    assert adapter.task_name == "dummy_hpo"


def test_task_card_adapter_renders_trial_command(tmp_path: Path) -> None:
    adapter = create_adapter_from_task_card(_build_task_card(str(tmp_path)))
    trial_dir = adapter.get_trial_dir(0)
    prepared = adapter.prepare_trial({"lr": 0.0003, "batch_size": 64, "epochs": 2}, trial_dir)

    command = adapter.build_command(prepared, trial_dir)

    assert command[0] == sys.executable
    assert any(Path(part).name == "dummy_train.py" for part in command)
    assert "0.0003" in command
    assert "64" in command
    assert "2" in command
    assert trial_dir in command
