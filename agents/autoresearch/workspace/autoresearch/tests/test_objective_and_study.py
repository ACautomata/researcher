"""Tests for objective execution and study orchestration."""

from __future__ import annotations

from pathlib import Path
import sys
from types import SimpleNamespace

import yaml
import pytest

from auto_research.core.objective import create_objective
from auto_research.core.safety import SafetyStopStudyError
from auto_research.core.study import main as study_main
from auto_research.core.task_card import create_adapter_from_task_card


class _TrialStub:
    def __init__(self, number: int = 0) -> None:
        self.number = number
        self.params: dict[str, object] = {}
        self.user_attrs: dict[str, object] = {}

    def suggest_float(self, name: str, low: float, high: float, *, log: bool = False) -> float:
        value = high if log else low
        self.params[name] = value
        return value

    def suggest_int(self, name: str, low: int, high: int, *, step: int = 1) -> int:
        value = low
        self.params[name] = value
        return value

    def suggest_categorical(self, name: str, choices: list[object]) -> object:
        value = choices[-1]
        self.params[name] = value
        return value

    def set_user_attr(self, key: str, value: object) -> None:
        self.user_attrs[key] = value


def _build_dummy_task_card(output_root: str) -> dict:
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
                "--output-dir",
                "{trial_dir}",
                "--trial-id",
                "{trial_id}",
                "--output-root",
                "{output_root}",
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
        "constraints": {"timeout": 30, "max_trials": 2},
    }


def test_objective_runs_dummy_training_and_records_trial(tmp_path: Path) -> None:
    task_card = _build_dummy_task_card(str(tmp_path))
    adapter = create_adapter_from_task_card(task_card)
    objective = create_objective(task_card, adapter, dry_run=False)
    trial = _TrialStub(number=0)

    score = objective(trial)
    trial_dir = Path(tmp_path) / "dummy_hpo" / "trial_000001"

    assert score > 0
    assert trial_dir.exists()
    assert (trial_dir / "metrics.json").exists()
    assert (trial_dir / "trial_record.json").exists()
    assert (tmp_path / "dummy_hpo" / "results.tsv").exists()
    assert (tmp_path / "dummy_hpo" / "results.jsonl").exists()
    assert trial.user_attrs["status"] == "completed"


def test_objective_returns_invalid_score_on_failure(tmp_path: Path) -> None:
    task_card = _build_dummy_task_card(str(tmp_path))
    task_card["adapter"]["command_template"] = [sys.executable, "examples/does_not_exist.py"]
    adapter = create_adapter_from_task_card(task_card)
    objective = create_objective(task_card, adapter, dry_run=False)

    score = objective(_TrialStub(number=0))
    trial_dir = Path(tmp_path) / "dummy_hpo" / "trial_000001"
    record_text = (trial_dir / "trial_record.json").read_text(encoding="utf-8")

    assert score == -1_000_000_000
    assert '"status": "failed"' in record_text or '"status": "invalid"' in record_text


def test_objective_dry_run_prints_command_without_executing(tmp_path: Path, capsys) -> None:
    task_card = _build_dummy_task_card(str(tmp_path))
    adapter = create_adapter_from_task_card(task_card)
    objective = create_objective(task_card, adapter, dry_run=True)

    score = objective(_TrialStub(number=0))
    captured = capsys.readouterr()
    trial_dir = Path(tmp_path) / "dummy_hpo" / "trial_000001"

    assert score == -1_000_000_000
    assert "[dry-run]" in captured.out
    assert not (trial_dir / "metrics.json").exists()
    assert (trial_dir / "trial_record.json").exists()
    assert (tmp_path / "dummy_hpo" / "results.tsv").exists()


def test_objective_rejects_duplicate_configs(tmp_path: Path) -> None:
    task_card = _build_dummy_task_card(str(tmp_path))
    adapter = create_adapter_from_task_card(task_card)
    objective = create_objective(task_card, adapter, dry_run=False)

    first_score = objective(_TrialStub(number=0))
    second_score = objective(_TrialStub(number=1))

    assert first_score > 0
    assert second_score == -1_000_000_000


def test_objective_stops_after_max_consecutive_failures(tmp_path: Path) -> None:
    task_card = _build_dummy_task_card(str(tmp_path))
    task_card["adapter"]["command_template"] = [sys.executable, "examples/does_not_exist.py"]
    task_card["safety"] = {"max_consecutive_failures": 1}
    adapter = create_adapter_from_task_card(task_card)
    objective = create_objective(task_card, adapter, dry_run=False)

    first_score = objective(_TrialStub(number=0))
    assert first_score == -1_000_000_000

    with pytest.raises(SafetyStopStudyError):
        objective(_TrialStub(number=1))


def test_study_main_uses_fake_optuna_module(tmp_path: Path, monkeypatch) -> None:
    task_card = _build_dummy_task_card(str(tmp_path / "runs"))
    task_card_path = tmp_path / "dummy_hpo.yaml"
    task_card_path.write_text(yaml.safe_dump(task_card, sort_keys=False), encoding="utf-8")

    fake_optuna = _build_fake_optuna_module()
    monkeypatch.setitem(sys.modules, "optuna", fake_optuna)

    exit_code = study_main(
        [
            "--task-card",
            str(task_card_path),
            "--study-name",
            "dummy-study",
            "--storage",
            str(tmp_path / "study.db"),
            "--n-trials",
            "2",
            "--direction",
            "maximize",
            "--seed",
            "7",
        ]
    )

    assert exit_code == 0
    assert fake_optuna.last_create_kwargs["load_if_exists"] is True
    assert fake_optuna.last_create_kwargs["study_name"] == "dummy-study"
    assert fake_optuna.last_create_kwargs["storage"].startswith("sqlite:///")


def _build_fake_optuna_module() -> SimpleNamespace:
    """Create a tiny in-memory Optuna substitute for CLI tests."""

    class FakeStudy:
        def __init__(self) -> None:
            self.study_name = ""
            self.trials: list[SimpleNamespace] = []
            self.best_trial: SimpleNamespace | None = None

        def optimize(self, objective, n_trials=None, timeout=None, catch=()) -> None:
            _ = (timeout, catch)
            total = n_trials or 1
            for number in range(total):
                trial = _TrialStub(number=number)
                value = objective(trial)
                completed = SimpleNamespace(number=number, value=value, params=dict(trial.params))
                self.trials.append(completed)
                if self.best_trial is None or value > self.best_trial.value:
                    self.best_trial = completed

    class FakeSampler:
        def __init__(self, seed=None) -> None:
            self.seed = seed

    fake_module = SimpleNamespace()
    fake_module.last_create_kwargs = {}

    def create_study(**kwargs):
        fake_module.last_create_kwargs = kwargs
        study = FakeStudy()
        study.study_name = kwargs["study_name"]
        return study

    fake_module.create_study = create_study
    fake_module.samplers = SimpleNamespace(TPESampler=FakeSampler)
    return fake_module
