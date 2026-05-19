"""Objective construction for running task-card-driven Optuna trials."""

from __future__ import annotations

from dataclasses import asdict
import json
import math
from pathlib import Path
import time
from typing import TYPE_CHECKING, Any, Callable

from auto_research.adapters.base import TrainingAdapter
from auto_research.core.recorder import TrialRecorder, build_trial_record, utc_now_iso
from auto_research.core.safety import (
    DuplicateConfigTracker,
    FailureTracker,
    SafetyStopStudyError,
    ensure_metrics_are_finite,
    ensure_trial_dir_within_output_root,
)
from auto_research.core.types import ExperimentResult, TrialRecord, TrialStatus
from auto_research.evaluators.base import compute_score, normalize_metrics
from auto_research.evaluators.json_parser import parse_json_metrics
from auto_research.evaluators.log_parser import parse_log_metrics
from auto_research.search_space.base import sample_from_search_space

if TYPE_CHECKING:
    from optuna.trial import Trial
else:
    Trial = Any


def create_objective(
    task_card: dict[str, Any],
    adapter: TrainingAdapter,
    *,
    dry_run: bool = False,
    trial_timeout: int | None = None,
) -> Callable[[Trial], float]:
    """Create an Optuna objective callable from a task card and adapter.

    Args:
        task_card: Parsed task card definition.
        adapter: Configured adapter instance for the external training project.
        dry_run: When true, print commands but do not execute training.
        trial_timeout: Optional per-trial timeout override in seconds.

    Returns:
        A callable suitable for ``optuna.study.Study.optimize``.
    """

    score_config = task_card.get("score", {})
    constraints = task_card.get("constraints", {})
    safety_config = task_card.get("safety", {})
    invalid_score = _resolve_invalid_score(score_config)
    effective_trial_timeout = trial_timeout or _resolve_trial_timeout(constraints)
    recorder = TrialRecorder(_get_recorder_output_dir(adapter=adapter, task_card=task_card))
    failure_tracker = FailureTracker(safety_config.get("max_consecutive_failures"))
    duplicate_tracker = DuplicateConfigTracker()

    def objective(trial: Trial) -> float:
        """Run a single optimization trial from sampling to score reporting."""

        trial_number = _safe_trial_number(trial)
        trial_id = f"trial_{trial_number + 1:06d}"
        trial_dir = _get_trial_dir(adapter=adapter, trial_number=trial_number, trial_id=trial_id)
        output_root = str(getattr(adapter, "output_root", "outputs"))
        start_time = utc_now_iso()
        started_at = time.perf_counter()

        try:
            ensure_trial_dir_within_output_root(trial_dir, output_root)
            sampled_config = sample_from_search_space(trial, task_card.get("search_space", {}))
            is_unique, config_hash = duplicate_tracker.check_and_add(sampled_config)
            if not is_unique:
                return _finalize_failed_trial(
                    recorder=recorder,
                    failure_tracker=failure_tracker,
                    task_name=str(task_card.get("task_name", "")),
                    trial=trial,
                    trial_id=trial_id,
                    trial_dir=trial_dir,
                    sampled_config=sampled_config,
                    prepared_config={},
                    command=[],
                    score=invalid_score,
                    status=TrialStatus.INVALID,
                    message=f"Duplicate trial configuration detected with hash '{config_hash}'.",
                    metadata={"config_hash": config_hash},
                    start_time=start_time,
                    duration_seconds=time.perf_counter() - started_at,
                )

            is_valid, validation_message = adapter.validate_config(sampled_config)
            if not is_valid:
                return _finalize_failed_trial(
                    recorder=recorder,
                    failure_tracker=failure_tracker,
                    task_name=str(task_card.get("task_name", "")),
                    trial=trial,
                    trial_id=trial_id,
                    trial_dir=trial_dir,
                    sampled_config=sampled_config,
                    prepared_config={},
                    command=[],
                    score=invalid_score,
                    status=TrialStatus.INVALID,
                    message=f"Trial configuration is invalid: {validation_message}",
                    start_time=start_time,
                    duration_seconds=time.perf_counter() - started_at,
                )

            prepared_config = adapter.prepare_trial(sampled_config, trial_dir)
            command = adapter.build_command(prepared_config, trial_dir)

            if dry_run:
                print(f"[dry-run] {trial_id}: {' '.join(command)}")
                return _finalize_failed_trial(
                    recorder=recorder,
                    failure_tracker=failure_tracker,
                    task_name=str(task_card.get("task_name", "")),
                    trial=trial,
                    trial_id=trial_id,
                    trial_dir=trial_dir,
                    sampled_config=sampled_config,
                    prepared_config=prepared_config,
                    command=command,
                    score=invalid_score,
                    status=TrialStatus.INVALID,
                    message="Dry-run mode enabled. Command was printed but not executed.",
                    metadata={"dry_run": True},
                    start_time=start_time,
                    duration_seconds=time.perf_counter() - started_at,
                    count_failure=False,
                )

            execution_result = adapter.run_trial(
                command=command,
                trial_dir=trial_dir,
                timeout=effective_trial_timeout,
            )
            metrics = _collect_trial_metrics(adapter=adapter, trial_dir=trial_dir)
            ensure_metrics_are_finite(metrics)
            score = compute_score(metrics, score_config)
            if not math.isfinite(score):
                raise ValueError(f"Computed score is not finite: {score!r}.")

            trial_status = _resolve_trial_status(
                execution_result.get("trial_status"),
                execution_result.get("status"),
            )
            if score == invalid_score and trial_status == TrialStatus.COMPLETED:
                trial_status = TrialStatus.INVALID

            record = TrialRecord(
                trial_id=trial_id,
                status=trial_status,
                sampled_config=sampled_config,
                prepared_config=prepared_config,
                result=ExperimentResult(
                    status=trial_status,
                    metrics=metrics,
                    score=score,
                    message=str(execution_result.get("message", "")),
                    trial_dir=trial_dir,
                    command=list(command),
                    return_code=execution_result.get("return_code"),
                    duration_seconds=_coerce_optional_float(
                        execution_result.get("duration_seconds")
                    ),
                    metadata={
                        "dry_run": False,
                        "execution": execution_result,
                    },
                ),
                notes="Trial finished.",
            )
            _write_trial_record(trial_dir=trial_dir, record=record)
            recorder.record_trial(
                build_trial_record(
                    task_name=str(task_card.get("task_name", "")),
                    trial_id=trial_id,
                    status=trial_status.value,
                    score=score,
                    trial_config=sampled_config,
                    metrics=metrics,
                    command=command,
                    trial_dir=trial_dir,
                    start_time=start_time,
                    end_time=utc_now_iso(),
                    duration_seconds=time.perf_counter() - started_at,
                    error_message=""
                    if trial_status == TrialStatus.COMPLETED
                    else str(execution_result.get("message", "")),
                )
            )
            _set_trial_user_attrs(
                trial=trial,
                trial_dir=trial_dir,
                command=command,
                status=trial_status.value,
                score=score,
            )
            if trial_status == TrialStatus.COMPLETED:
                failure_tracker.record_success()
            else:
                failure_tracker.record_failure()
            return float(score)
        except SafetyStopStudyError:
            raise
        except Exception as exc:
            return _finalize_failed_trial(
                recorder=recorder,
                failure_tracker=failure_tracker,
                task_name=str(task_card.get("task_name", "")),
                trial=trial,
                trial_id=trial_id,
                trial_dir=trial_dir,
                sampled_config={},
                prepared_config={},
                command=[],
                score=invalid_score,
                status=TrialStatus.FAILED,
                message=f"Trial failed with an unexpected error: {exc}.",
                metadata={"exception_type": type(exc).__name__},
                start_time=start_time,
                duration_seconds=time.perf_counter() - started_at,
            )

    return objective


def _collect_trial_metrics(adapter: TrainingAdapter, trial_dir: str) -> dict[str, float]:
    """Collect and normalize metrics from all supported trial outputs."""

    merged_metrics: dict[str, Any] = {}

    try:
        merged_metrics.update(adapter.collect_metrics(trial_dir))
    except Exception:
        pass

    merged_metrics.update(parse_json_metrics(trial_dir))
    merged_metrics.update(parse_log_metrics(trial_dir))

    return normalize_metrics(merged_metrics)


def _resolve_invalid_score(score_config: dict[str, Any]) -> float:
    """Resolve the configured invalid score with a safe fallback."""

    try:
        return float(score_config.get("invalid_score", -1_000_000_000.0))
    except (TypeError, ValueError):
        return -1_000_000_000.0


def _resolve_trial_timeout(constraints: dict[str, Any]) -> int:
    """Resolve per-trial timeout from task card constraints."""

    timeout = constraints.get("timeout", 3600)
    if isinstance(timeout, int) and not isinstance(timeout, bool) and timeout > 0:
        return timeout
    return 3600


def _safe_trial_number(trial: Trial) -> int:
    """Extract a stable trial number from an Optuna-like trial object."""

    number = getattr(trial, "number", 0)
    if isinstance(number, int) and number >= 0:
        return number
    return 0


def _get_trial_dir(adapter: TrainingAdapter, trial_number: int, trial_id: str) -> str:
    """Resolve the per-trial directory using the adapter when possible."""

    get_trial_dir = getattr(adapter, "get_trial_dir", None)
    if callable(get_trial_dir):
        return str(get_trial_dir(trial_number))

    fallback_path = Path("outputs") / trial_id
    fallback_path.mkdir(parents=True, exist_ok=True)
    return str(fallback_path.resolve())


def _resolve_trial_status(raw_trial_status: Any, raw_status: Any) -> TrialStatus:
    """Convert adapter execution state into a ``TrialStatus`` value."""

    for candidate in (raw_trial_status, raw_status):
        if not isinstance(candidate, str):
            continue

        normalized = candidate.strip().lower()
        if normalized == "success":
            normalized = TrialStatus.COMPLETED.value
        if normalized == "blocked":
            normalized = TrialStatus.INVALID.value

        try:
            return TrialStatus(normalized)
        except ValueError:
            continue

    return TrialStatus.FAILED


def _coerce_optional_float(value: Any) -> float | None:
    """Coerce optional float-like values safely."""

    if value is None:
        return None

    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _get_recorder_output_dir(adapter: TrainingAdapter, task_card: dict[str, Any]) -> str:
    """Resolve the study-level output directory used by the recorder."""

    task_name = str(task_card.get("task_name", "task"))
    output_root = getattr(adapter, "output_root", None)
    if isinstance(output_root, str) and output_root.strip():
        return str((Path(output_root) / task_name).resolve())
    return str((Path("outputs") / task_name).resolve())


def _write_trial_record(trial_dir: str, record: TrialRecord) -> None:
    """Persist one trial record as JSON."""

    record_path = Path(trial_dir) / "trial_record.json"
    payload = asdict(record)
    record_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True),
        encoding="utf-8",
    )


def _set_trial_user_attrs(
    trial: Trial,
    *,
    trial_dir: str,
    command: list[str],
    status: str,
    score: float,
) -> None:
    """Attach useful debugging metadata to an Optuna-like trial if supported."""

    setter = getattr(trial, "set_user_attr", None)
    if not callable(setter):
        return

    setter("trial_dir", trial_dir)
    setter("command", list(command))
    setter("status", status)
    setter("score", score)


def _finalize_failed_trial(
    *,
    recorder: TrialRecorder,
    failure_tracker: FailureTracker,
    task_name: str,
    trial: Trial,
    trial_id: str,
    trial_dir: str,
    sampled_config: dict[str, Any],
    prepared_config: dict[str, Any],
    command: list[str],
    score: float,
    status: TrialStatus,
    message: str,
    metadata: dict[str, Any] | None = None,
    start_time: str,
    duration_seconds: float | None,
    count_failure: bool = True,
) -> float:
    """Persist a failed or invalid trial record and return a fallback score."""

    Path(trial_dir).mkdir(parents=True, exist_ok=True)
    record = TrialRecord(
        trial_id=trial_id,
        status=status,
        sampled_config=sampled_config,
        prepared_config=prepared_config,
        result=ExperimentResult(
            status=status,
            metrics={},
            score=score,
            message=message,
            trial_dir=trial_dir,
            command=list(command),
            return_code=None,
            duration_seconds=None,
            metadata=metadata or {},
        ),
        notes=message,
    )
    _write_trial_record(trial_dir=trial_dir, record=record)
    recorder.record_trial(
        build_trial_record(
            task_name=task_name,
            trial_id=trial_id,
            status=status.value,
            score=score,
            trial_config=sampled_config,
            metrics={},
            command=command,
            trial_dir=trial_dir,
            start_time=start_time,
            end_time=utc_now_iso(),
            duration_seconds=duration_seconds,
            error_message=message,
        )
    )
    _set_trial_user_attrs(
        trial=trial,
        trial_dir=trial_dir,
        command=command,
        status=status.value,
        score=score,
    )
    if count_failure:
        failure_tracker.record_failure()
    return float(score)
