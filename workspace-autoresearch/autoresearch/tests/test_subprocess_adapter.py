"""Tests for the generic subprocess adapter."""

from __future__ import annotations

from pathlib import Path
import sys
import time

from auto_research.adapters.subprocess_adapter import SubprocessAdapter


class _TrialStub:
    def suggest_float(
        self,
        name: str,
        low: float,
        high: float,
        *,
        log: bool = False,
        step: float | None = None,
    ) -> float:
        _ = (name, low, high, log, step)
        return 0.001

    def suggest_int(
        self,
        name: str,
        low: int,
        high: int,
        *,
        log: bool = False,
        step: int = 1,
    ) -> int:
        _ = (name, low, high, log, step)
        return 32

    def suggest_categorical(self, name: str, choices: list[object]) -> object:
        _ = name
        return choices[0]


def test_get_trial_dir_creates_expected_layout(tmp_path: Path) -> None:
    adapter = SubprocessAdapter(
        task_name="demo_task",
        base_command=[sys.executable, "-c", "print('ok')"],
        output_root=str(tmp_path),
    )

    trial_dir = Path(adapter.get_trial_dir(0))

    assert trial_dir.exists()
    assert trial_dir.name == "trial_000001"
    assert trial_dir.parent.name == "demo_task"
    assert trial_dir.parent.parent == tmp_path.resolve()


def test_build_command_appends_sampled_cli_arguments(tmp_path: Path) -> None:
    adapter = SubprocessAdapter(
        task_name="demo_task",
        base_command=[sys.executable, "train.py"],
        static_args=["--epochs", "10"],
        parameter_flags={"batch_size": "--batch-size"},
        output_root=str(tmp_path),
    )
    trial_dir = adapter.get_trial_dir(0)
    prepared = adapter.prepare_trial({"lr": 0.0003, "batch_size": 64, "use_amp": True}, trial_dir)

    command = adapter.build_command(prepared, trial_dir)

    assert command[:4] == [sys.executable, "train.py", "--epochs", "10"]
    assert "--lr" in command
    assert "0.0003" in command
    assert "--batch-size" in command
    assert "64" in command
    assert "--use-amp" in command


def test_run_trial_captures_logs_and_reports_success(tmp_path: Path) -> None:
    adapter = SubprocessAdapter(
        task_name="demo_task",
        base_command=[
            sys.executable,
            "-c",
            (
                "import sys; "
                "print('hello stdout'); "
                "print('hello stderr', file=sys.stderr)"
            ),
        ],
        output_root=str(tmp_path),
    )
    trial_dir = adapter.get_trial_dir(0)
    prepared = adapter.prepare_trial({}, trial_dir)
    command = adapter.build_command(prepared, trial_dir)

    result = adapter.run_trial(command, trial_dir, timeout=5)

    assert result["status"] == "success"
    assert result["success"] is True
    assert Path(result["stdout_log"]).read_text(encoding="utf-8").strip() == "hello stdout"
    assert Path(result["stderr_log"]).read_text(encoding="utf-8").strip() == "hello stderr"


def test_run_trial_reports_timeout_without_crashing(tmp_path: Path) -> None:
    adapter = SubprocessAdapter(
        task_name="timeout_task",
        base_command=[
            sys.executable,
            "-c",
            "import time; print('start'); time.sleep(2)",
        ],
        output_root=str(tmp_path),
    )
    trial_dir = adapter.get_trial_dir(0)
    prepared = adapter.prepare_trial({}, trial_dir)
    command = adapter.build_command(prepared, trial_dir)

    started_at = time.perf_counter()
    result = adapter.run_trial(command, trial_dir, timeout=1)
    elapsed = time.perf_counter() - started_at

    assert result["status"] == "timeout"
    assert result["success"] is False
    assert elapsed < 2
    assert Path(result["stdout_log"]).exists()
    assert Path(result["stderr_log"]).exists()


def test_run_trial_blocks_dangerous_command(tmp_path: Path) -> None:
    adapter = SubprocessAdapter(
        task_name="blocked_task",
        base_command=["rm", "-rf", "/"],
        output_root=str(tmp_path),
    )
    trial_dir = adapter.get_trial_dir(0)
    prepared = adapter.prepare_trial({}, trial_dir)

    result = adapter.run_trial(prepared["base_command"], trial_dir, timeout=5)

    assert result["status"] == "blocked"
    assert result["trial_status"] == "invalid"
    assert "Refusing to execute" in result["message"]


def test_sample_config_supports_common_search_space_types(tmp_path: Path) -> None:
    adapter = SubprocessAdapter(
        task_name="sample_task",
        base_command=[sys.executable, "-c", "print('ok')"],
        output_root=str(tmp_path),
        search_space={
            "lr": {"type": "float", "low": 1e-4, "high": 1e-2, "log": True},
            "batch_size": {"type": "int", "low": 16, "high": 64, "step": 16},
            "optimizer": {"type": "categorical", "choices": ["adam", "sgd"]},
            "use_amp": {"type": "bool"},
            "epochs": {"type": "fixed", "value": 10},
        },
    )

    sampled = adapter.sample_config(_TrialStub())

    assert sampled["lr"] == 0.001
    assert sampled["batch_size"] == 32
    assert sampled["optimizer"] == "adam"
    assert sampled["use_amp"] is False
    assert sampled["epochs"] == 10


def test_command_template_supports_builtin_variables(tmp_path: Path) -> None:
    adapter = SubprocessAdapter(
        task_name="template_task",
        base_command=[sys.executable],
        command_template=[
            sys.executable,
            "-c",
            "print('ok')",
            "--trial-dir",
            "{trial_dir}",
            "--trial-id",
            "{trial_id}",
            "--output-root",
            "{output_root}",
        ],
        output_root=str(tmp_path),
    )
    trial_dir = adapter.get_trial_dir(0)
    prepared = adapter.prepare_trial({"lr": 0.0003}, trial_dir)

    command = adapter.build_command(prepared, trial_dir)

    assert "--trial-dir" in command
    assert trial_dir in command
    assert "--trial-id" in command
    assert "trial_000001" in command
    assert str(tmp_path.resolve()) in command


def test_command_template_missing_variable_raises_clear_error(tmp_path: Path) -> None:
    adapter = SubprocessAdapter(
        task_name="template_task",
        base_command=[sys.executable],
        command_template=[
            sys.executable,
            "train.py",
            "--missing",
            "{missing_value}",
        ],
        output_root=str(tmp_path),
    )
    trial_dir = adapter.get_trial_dir(0)
    prepared = adapter.prepare_trial({}, trial_dir)

    try:
        adapter.build_command(prepared, trial_dir)
    except ValueError as exc:
        assert "placeholder 'missing_value'" in str(exc)
    else:
        raise AssertionError("Expected a clear missing placeholder error.")


def test_command_template_can_run_dummy_train_example(tmp_path: Path) -> None:
    adapter = SubprocessAdapter(
        task_name="dummy_task",
        base_command=[sys.executable],
        command_template=[
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
        output_root=str(tmp_path),
    )
    trial_dir = adapter.get_trial_dir(0)
    prepared = adapter.prepare_trial({"lr": 0.0003, "batch_size": 64}, trial_dir)
    command = adapter.build_command(prepared, trial_dir)

    result = adapter.run_trial(command, trial_dir, timeout=10)
    metrics = adapter.collect_metrics(trial_dir)

    assert result["status"] == "success"
    assert metrics["mAP"] > 0
    assert metrics["rank1"] > metrics["mAP"]
    assert "trial_000001" in result["stdout"]
