"""End-to-end tests for the dummy AutoResearch workflow."""

from __future__ import annotations

from pathlib import Path
import sys
from types import SimpleNamespace

import yaml

from auto_research.core.study import main as study_main


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
        _ = step
        value = low
        self.params[name] = value
        return value

    def suggest_categorical(self, name: str, choices: list[object]) -> object:
        value = choices[-1]
        self.params[name] = value
        return value

    def set_user_attr(self, key: str, value: object) -> None:
        self.user_attrs[key] = value


def _build_fake_optuna_module() -> SimpleNamespace:
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
        "score": {
            "primary_metric": "mAP",
            "secondary_metrics": {"rank1": 0.2},
            "invalid_score": -1_000_000_000,
        },
        "constraints": {"timeout": 30, "max_trials": 3},
        "safety": {"allow_commands": ["python", "python3"]},
    }


def test_dummy_end_to_end_study_runs_trials_and_writes_outputs(tmp_path: Path, monkeypatch) -> None:
    output_root = tmp_path / "outputs"
    task_card_path = tmp_path / "dummy_hpo.yaml"
    task_card_path.write_text(
        yaml.safe_dump(_build_task_card(str(output_root)), sort_keys=False),
        encoding="utf-8",
    )

    fake_optuna = _build_fake_optuna_module()
    monkeypatch.setitem(sys.modules, "optuna", fake_optuna)

    exit_code = study_main(
        [
            "--task-card",
            str(task_card_path),
            "--study-name",
            "dummy-e2e",
            "--storage",
            str(tmp_path / "study.db"),
            "--n-trials",
            "2",
            "--direction",
            "maximize",
        ]
    )

    task_output_dir = output_root / "dummy_hpo"
    first_trial_dir = task_output_dir / "trial_000001"

    assert exit_code == 0
    assert fake_optuna.last_create_kwargs["load_if_exists"] is True
    assert first_trial_dir.exists()
    assert (first_trial_dir / "metrics.json").exists()
    assert (task_output_dir / "results.tsv").exists()
