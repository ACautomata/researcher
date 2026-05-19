"""Tests for centralized safety policy helpers."""

from __future__ import annotations

from pathlib import Path

import pytest

from auto_research.core.safety import (
    DuplicateConfigTracker,
    FailureTracker,
    SafetyStopStudyError,
    ensure_command_is_safe,
    ensure_metrics_are_finite,
    ensure_trial_dir_within_output_root,
    hash_trial_config,
    validate_safety_config,
)


def test_validate_safety_config_accepts_valid_input() -> None:
    is_valid, message = validate_safety_config(
        {
            "max_consecutive_failures": 5,
            "allow_commands": ["python", "python3"],
        }
    )

    assert is_valid is True
    assert message == "Safety config is valid."


def test_ensure_command_is_safe_allows_python_and_blocks_shell() -> None:
    ensure_command_is_safe(["python", "train.py"], shell=False)

    with pytest.raises(ValueError, match="shell=True"):
        ensure_command_is_safe(["python", "train.py"], shell=True)


def test_ensure_command_is_safe_blocks_disallowed_and_dangerous_commands() -> None:
    with pytest.raises(ValueError, match="allowed list"):
        ensure_command_is_safe(["bash", "train.sh"])

    with pytest.raises(ValueError, match="Refusing to execute"):
        ensure_command_is_safe(["rm", "-rf", "/"])


def test_ensure_trial_dir_within_output_root_rejects_escape(tmp_path: Path) -> None:
    safe_trial_dir = tmp_path / "task" / "trial_000001"
    safe_trial_dir.mkdir(parents=True)
    ensure_trial_dir_within_output_root(str(safe_trial_dir), str(tmp_path))

    with pytest.raises(ValueError, match="must be located under output_root"):
        ensure_trial_dir_within_output_root(str(tmp_path.parent), str(tmp_path))


def test_ensure_metrics_are_finite_rejects_nan() -> None:
    ensure_metrics_are_finite({"mAP": 75.3, "loss": 0.8})

    with pytest.raises(ValueError, match="non-finite"):
        ensure_metrics_are_finite({"mAP": float("nan")})


def test_hash_trial_config_is_stable_and_duplicate_tracker_detects_reuse() -> None:
    left = {"lr": 0.001, "batch_size": 64}
    right = {"batch_size": 64, "lr": 0.001}

    assert hash_trial_config(left) == hash_trial_config(right)

    tracker = DuplicateConfigTracker()
    assert tracker.check_and_add(left)[0] is True
    assert tracker.check_and_add(right)[0] is False


def test_failure_tracker_stops_after_limit() -> None:
    tracker = FailureTracker(max_consecutive_failures=1)
    tracker.record_failure()

    with pytest.raises(SafetyStopStudyError):
        tracker.record_failure()
