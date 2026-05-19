"""Focused tests for the generic subprocess adapter."""

from __future__ import annotations

from pathlib import Path
import sys

from auto_research.adapters.subprocess_adapter import SubprocessAdapter


def test_subprocess_adapter_creates_expected_trial_layout(tmp_path: Path) -> None:
    adapter = SubprocessAdapter(
        task_name="dummy_hpo",
        base_command=[sys.executable, "-c", "print('ok')"],
        output_root=str(tmp_path),
    )

    trial_dir = Path(adapter.get_trial_dir(0))

    assert trial_dir.exists()
    assert trial_dir.name == "trial_000001"
    assert trial_dir.parent.name == "dummy_hpo"


def test_subprocess_adapter_runs_dummy_train_and_collects_metrics(tmp_path: Path) -> None:
    adapter = SubprocessAdapter(
        task_name="dummy_hpo",
        base_command=[sys.executable],
        command_template=[
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
        output_root=str(tmp_path),
    )
    trial_dir = adapter.get_trial_dir(0)
    prepared = adapter.prepare_trial({"lr": 0.0003, "batch_size": 64, "epochs": 2}, trial_dir)
    command = adapter.build_command(prepared, trial_dir)

    result = adapter.run_trial(command, trial_dir, timeout=10)
    metrics = adapter.collect_metrics(trial_dir)

    assert result["status"] == "success"
    assert (Path(trial_dir) / "train_stdout.log").exists()
    assert (Path(trial_dir) / "train_stderr.log").exists()
    assert metrics["mAP"] > 0
    assert metrics["rank1"] > 0


def test_subprocess_adapter_reports_missing_template_variable_clearly(tmp_path: Path) -> None:
    adapter = SubprocessAdapter(
        task_name="dummy_hpo",
        base_command=[sys.executable],
        command_template=[sys.executable, "examples/dummy_train.py", "--lr", "{missing_lr}"],
        output_root=str(tmp_path),
    )
    trial_dir = adapter.get_trial_dir(0)
    prepared = adapter.prepare_trial({}, trial_dir)

    try:
        adapter.build_command(prepared, trial_dir)
    except ValueError as exc:
        assert "placeholder 'missing_lr'" in str(exc)
    else:
        raise AssertionError("Expected a clear missing placeholder error.")
