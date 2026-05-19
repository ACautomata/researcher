"""Base abstractions for integrating external training projects."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
import os
import subprocess
import time
from typing import TYPE_CHECKING, Any

from auto_research.core.types import TrialStatus

if TYPE_CHECKING:
    from optuna.trial import Trial
else:
    Trial = Any


class TrainingAdapter(ABC):
    """Abstract base class for external training project integrations.

    Concrete adapters translate AutoResearch trial inputs into the execution
    format expected by an external training project. The base class does not
    assume any specific model, framework, or configuration style.
    """

    @abstractmethod
    def prepare_trial(self, trial_config: dict[str, Any], trial_dir: str) -> dict[str, Any]:
        """Prepare a single trial before launch.

        Implementations may write temporary config files, expand relative paths,
        or transform sampled parameters into the format expected by the external
        project.

        Args:
            trial_config: The sampled hyperparameter configuration for this trial.
            trial_dir: The directory assigned to the current trial.

        Returns:
            A prepared configuration mapping ready for command construction.

        Raises:
            ValueError: If the provided trial configuration is invalid.
            RuntimeError: If the trial environment cannot be prepared.
        """

    @abstractmethod
    def build_command(self, prepared_config: dict[str, Any], trial_dir: str) -> list[str]:
        """Build the command used to launch one training run.

        Args:
            prepared_config: The configuration returned by :meth:`prepare_trial`.
            trial_dir: The directory assigned to the current trial.

        Returns:
            A command list suitable for ``subprocess`` execution.

        Raises:
            ValueError: If the prepared configuration cannot be converted into a
                valid command.
        """

    def run_trial(
        self,
        command: list[str],
        trial_dir: str,
        timeout: int,
        env: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Execute a training command in the trial directory.

        This method is intentionally generic so it can be reused by adapters for
        command-line tools, PyTorch entrypoints, or YAML-driven training
        projects without embedding any project-specific logic.

        Args:
            command: The command list to execute.
            trial_dir: The working directory for the trial process.
            timeout: Maximum allowed execution time in seconds.
            env: Optional environment variables to merge into the current
                process environment.

        Returns:
            A dictionary containing execution metadata such as status, return
            code, stdout, stderr, duration, and the executed command.

        Raises:
            ValueError: If the command, timeout, or environment is invalid.
            FileNotFoundError: If the trial directory does not exist.
            RuntimeError: If the subprocess cannot be started.
        """

        if not command:
            raise ValueError("Training command cannot be empty.")

        if any(not isinstance(part, str) or not part.strip() for part in command):
            raise ValueError(
                "Training command must be a list of non-empty strings suitable for subprocess."
            )

        if timeout <= 0:
            raise ValueError(f"Timeout must be a positive integer, but received: {timeout!r}.")

        trial_path = Path(trial_dir)
        if not trial_path.exists():
            raise FileNotFoundError(
                f"Trial directory does not exist and cannot be used for execution: '{trial_dir}'."
            )
        if not trial_path.is_dir():
            raise FileNotFoundError(
                f"Trial path exists but is not a directory: '{trial_dir}'."
            )

        if env is not None:
            invalid_items = [
                key for key, value in env.items() if not isinstance(key, str) or not isinstance(value, str)
            ]
            if invalid_items:
                raise ValueError(
                    "Environment variables must be a mapping of string keys to string values. "
                    f"Invalid keys: {invalid_items!r}."
                )

        process_env = os.environ.copy()
        if env is not None:
            process_env.update(env)

        start_time = time.perf_counter()

        try:
            completed_process = subprocess.run(
                command,
                cwd=str(trial_path),
                env=process_env,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            duration_seconds = time.perf_counter() - start_time
            return {
                "status": TrialStatus.TIMEOUT.value,
                "command": command,
                "trial_dir": str(trial_path),
                "return_code": None,
                "stdout": exc.stdout or "",
                "stderr": exc.stderr or "",
                "duration_seconds": duration_seconds,
                "timeout_seconds": timeout,
                "message": f"Training command exceeded the timeout limit of {timeout} seconds.",
            }
        except FileNotFoundError as exc:
            executable = command[0]
            raise RuntimeError(
                "Failed to start the training command because the executable was not found: "
                f"'{executable}'."
            ) from exc
        except OSError as exc:
            raise RuntimeError(
                "Failed to start the training command due to an operating system error: "
                f"{exc}."
            ) from exc

        duration_seconds = time.perf_counter() - start_time
        status = (
            TrialStatus.COMPLETED.value
            if completed_process.returncode == 0
            else TrialStatus.FAILED.value
        )

        return {
            "status": status,
            "command": command,
            "trial_dir": str(trial_path),
            "return_code": completed_process.returncode,
            "stdout": completed_process.stdout,
            "stderr": completed_process.stderr,
            "duration_seconds": duration_seconds,
            "timeout_seconds": timeout,
            "message": "Training command finished successfully."
            if completed_process.returncode == 0
            else f"Training command exited with a non-zero return code: {completed_process.returncode}.",
        }

    @abstractmethod
    def collect_metrics(self, trial_dir: str) -> dict[str, Any]:
        """Collect metrics produced by a completed trial.

        Args:
            trial_dir: The directory assigned to the current trial.

        Returns:
            A dictionary of parsed metrics and optional metadata.

        Raises:
            FileNotFoundError: If expected output files are missing.
            RuntimeError: If metrics cannot be parsed from the trial outputs.
        """

    @abstractmethod
    def sample_config(self, trial: Trial) -> dict[str, Any]:
        """Sample a hyperparameter configuration from an Optuna trial.

        Args:
            trial: The active Optuna trial object.

        Returns:
            A trial configuration dictionary that can later be validated and prepared.
        """

    @abstractmethod
    def validate_config(self, trial_config: dict[str, Any]) -> tuple[bool, str]:
        """Validate whether a sampled configuration is acceptable.

        Args:
            trial_config: The sampled hyperparameter configuration.

        Returns:
            A tuple of ``(is_valid, message)``. The message should explain why the
            configuration is invalid or provide a short success note.
        """
