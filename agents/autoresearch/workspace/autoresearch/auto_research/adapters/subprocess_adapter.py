"""Generic subprocess-based adapter for command-line training projects."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import json
import os
import shlex
import subprocess
import time
from typing import TYPE_CHECKING, Any, Mapping, Sequence

import yaml

from auto_research.adapters.base import TrainingAdapter
from auto_research.core.safety import ensure_command_is_safe, ensure_trial_dir_within_output_root
from auto_research.core.types import TrialStatus

if TYPE_CHECKING:
    from optuna.trial import Trial
else:
    Trial = Any


_SUPPORTED_SEARCH_SPACE_TYPES = {"float", "int", "categorical", "bool", "fixed"}


@dataclass(slots=True)
class SubprocessAdapter(TrainingAdapter):
    """Generic adapter for external training projects launched as subprocesses.

    The adapter is intentionally model-agnostic. It knows how to:

    - create per-trial output directories
    - sample trial parameters from Optuna
    - build CLI argument lists safely
    - run subprocesses without ``shell=True``
    - persist stdout and stderr logs
    - collect metrics from common output file formats
    """

    task_name: str
    base_command: list[str]
    command_template: list[str] | None = None
    search_space: dict[str, dict[str, Any]] = field(default_factory=dict)
    static_args: list[str] = field(default_factory=list)
    parameter_flags: dict[str, str] = field(default_factory=dict)
    fixed_config: dict[str, Any] = field(default_factory=dict)
    base_env: dict[str, str] = field(default_factory=dict)
    output_root: str = "outputs"
    allow_commands: list[str] = field(default_factory=lambda: ["python", "python3"])
    metrics_filenames: tuple[str, ...] = (
        "metrics.json",
        "metrics.yaml",
        "metrics.yml",
        "metrics.txt",
    )

    def __post_init__(self) -> None:
        """Validate the adapter configuration at construction time."""

        if not self.task_name.strip():
            raise ValueError("Task name cannot be empty for SubprocessAdapter.")

        if not self.base_command:
            raise ValueError("Base command cannot be empty for SubprocessAdapter.")

        if any(not isinstance(part, str) or not part.strip() for part in self.base_command):
            raise ValueError(
                "Base command must be a list of non-empty strings suitable for subprocess."
            )

        if self.command_template is not None:
            if not self.command_template:
                raise ValueError("Command template cannot be empty when provided.")
            if any(
                not isinstance(part, str) or not part.strip() for part in self.command_template
            ):
                raise ValueError(
                    "Command template must be a list of non-empty strings suitable for subprocess."
                )

        if any(not isinstance(arg, str) or not arg.strip() for arg in self.static_args):
            raise ValueError("Static arguments must be non-empty strings.")

        invalid_env = [
            key
            for key, value in self.base_env.items()
            if not isinstance(key, str) or not isinstance(value, str)
        ]
        if invalid_env:
            raise ValueError(
                "Base environment values must be string-to-string mappings. "
                f"Invalid keys: {invalid_env!r}."
            )

        if any(not isinstance(item, str) or not item.strip() for item in self.allow_commands):
            raise ValueError(
                "Allowed command list must contain only non-empty command names."
            )

        is_valid, message = self._validate_search_space()
        if not is_valid:
            raise ValueError(message)

    def get_trial_dir(self, trial_number: int) -> str:
        """Create and return the canonical output directory for a trial.

        Args:
            trial_number: The zero-based or one-based trial number.

        Returns:
            The absolute path of the created trial directory in the form
            ``outputs/{task_name}/trial_000001``.

        Raises:
            ValueError: If the trial number is negative.
            RuntimeError: If the directory cannot be created.
        """

        if trial_number < 0:
            raise ValueError(
                f"Trial number must be non-negative, but received: {trial_number!r}."
            )

        trial_path = Path(self.output_root) / self.task_name / f"trial_{trial_number + 1:06d}"
        try:
            trial_path.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            raise RuntimeError(
                f"Failed to create trial directory for task '{self.task_name}': '{trial_path}'."
            ) from exc

        resolved = str(trial_path.resolve())
        ensure_trial_dir_within_output_root(resolved, self.output_root)
        return resolved

    def prepare_trial(self, trial_config: dict[str, Any], trial_dir: str) -> dict[str, Any]:
        """Prepare a trial directory and persist the sampled configuration.

        Args:
            trial_config: The sampled hyperparameter configuration for this trial.
            trial_dir: The directory assigned to the current trial.

        Returns:
            A dictionary containing the normalized configuration and runtime metadata.

        Raises:
            ValueError: If the sampled configuration is invalid.
            RuntimeError: If the trial directory or config file cannot be created.
        """

        is_valid, message = self.validate_config(trial_config)
        if not is_valid:
            raise ValueError(f"Invalid trial configuration: {message}")

        ensure_trial_dir_within_output_root(trial_dir, self.output_root)

        trial_path = Path(trial_dir)
        try:
            trial_path.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            raise RuntimeError(f"Failed to create trial directory: '{trial_dir}'.") from exc

        normalized_config = dict(self.fixed_config)
        normalized_config.update(trial_config)
        resolved_trial_dir = str(trial_path.resolve())
        trial_id = str(normalized_config.get("trial_id", self._infer_trial_id(resolved_trial_dir)))
        output_root = str(Path(self.output_root).resolve())

        prepared_config: dict[str, Any] = {
            "task_name": self.task_name,
            "trial_dir": resolved_trial_dir,
            "trial_id": trial_id,
            "output_root": output_root,
            "parameters": normalized_config,
            "base_command": list(self.base_command),
            "command_template": list(self.command_template) if self.command_template else None,
            "static_args": list(self.static_args),
            "base_env": dict(self.base_env),
        }

        config_path = trial_path / "trial_config.yaml"
        try:
            config_path.write_text(
                yaml.safe_dump(prepared_config, sort_keys=True, allow_unicode=False),
                encoding="utf-8",
            )
        except OSError as exc:
            raise RuntimeError(
                f"Failed to write prepared trial configuration to '{config_path}'."
            ) from exc

        return prepared_config

    def build_command(self, prepared_config: dict[str, Any], trial_dir: str) -> list[str]:
        """Build a safe subprocess command from the prepared configuration.

        Args:
            prepared_config: The configuration returned by :meth:`prepare_trial`.
            trial_dir: The directory assigned to the current trial.

        Returns:
            A command list suitable for ``subprocess.run`` with ``shell=False``.

        Raises:
            ValueError: If the prepared configuration is missing required fields or
                would produce a dangerous command.
        """

        parameters = prepared_config.get("parameters")
        if not isinstance(parameters, dict):
            raise ValueError(
                "Prepared configuration must contain a 'parameters' mapping before command build."
            )

        command_template = prepared_config.get("command_template", self.command_template)
        if command_template is not None:
            if not isinstance(command_template, list):
                raise ValueError("Prepared command template must be a list of strings.")
            command = self._render_command_template(
                command_template=command_template,
                parameters=parameters,
                trial_dir=trial_dir,
                trial_id=str(prepared_config.get("trial_id", self._infer_trial_id(trial_dir))),
                output_root=str(prepared_config.get("output_root", Path(self.output_root).resolve())),
            )
        else:
            command = list(prepared_config.get("base_command", self.base_command))
            command.extend(prepared_config.get("static_args", self.static_args))

            for name, value in parameters.items():
                command.extend(self._parameter_to_cli_args(name, value))

        command = self._normalize_command_paths(command)
        self._ensure_command_is_safe(command)

        trial_path = Path(trial_dir)
        if not trial_path.exists():
            raise ValueError(
                f"Trial directory does not exist while building command: '{trial_dir}'."
            )

        return command

    def run_trial(
        self,
        command: list[str],
        trial_dir: str,
        timeout: int,
        env: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Execute a training command and persist process logs to the trial directory.

        Args:
            command: The command list to execute.
            trial_dir: The working directory for the trial process.
            timeout: Maximum allowed execution time in seconds.
            env: Optional environment variables to merge into the adapter base environment.

        Returns:
            A dictionary with execution status, timing, logs, and process metadata.
            The ``status`` field uses ``success``, ``failed``, ``timeout``, or
            ``blocked`` to make downstream handling straightforward.
        """

        trial_path = Path(trial_dir)
        stdout_path = trial_path / "train_stdout.log"
        stderr_path = trial_path / "train_stderr.log"

        if not command:
            return {
                "status": "failed",
                "trial_status": TrialStatus.FAILED.value,
                "success": False,
                "command": [],
                "command_text": "",
                "trial_dir": str(trial_path.resolve()),
                "return_code": None,
                "stdout": "",
                "stderr": "",
                "stdout_log": str(stdout_path.resolve()),
                "stderr_log": str(stderr_path.resolve()),
                "duration_seconds": 0.0,
                "timeout_seconds": timeout,
                "message": "Training command cannot be empty.",
            }

        if timeout <= 0:
            raise ValueError(f"Timeout must be a positive integer, but received: {timeout!r}.")

        if env is not None:
            invalid_env = [
                key
                for key, value in env.items()
                if not isinstance(key, str) or not isinstance(value, str)
            ]
            if invalid_env:
                raise ValueError(
                    "Environment variables must be a mapping of string keys to string values. "
                    f"Invalid keys: {invalid_env!r}."
                )

        def finalize_result(
            *,
            status: str,
            trial_status: TrialStatus,
            return_code: int | None,
            stdout: str,
            stderr: str,
            duration_seconds: float,
            message: str,
            timeout_seconds: int,
        ) -> dict[str, Any]:
            self._write_log(stdout_path, stdout)
            self._write_log(stderr_path, stderr)
            return {
                "status": status,
                "trial_status": trial_status.value,
                "success": status == "success",
                "command": list(command),
                "command_text": shlex.join(command),
                "trial_dir": str(trial_path.resolve()),
                "return_code": return_code,
                "stdout": stdout,
                "stderr": stderr,
                "stdout_log": str(stdout_path.resolve()),
                "stderr_log": str(stderr_path.resolve()),
                "duration_seconds": duration_seconds,
                "timeout_seconds": timeout_seconds,
                "message": message,
            }

        start_time = time.perf_counter()

        try:
            self._ensure_command_is_safe(command)
            ensure_trial_dir_within_output_root(str(trial_path.resolve()), self.output_root)
            trial_path.mkdir(parents=True, exist_ok=True)

            effective_env = dict(self.base_env)
            if env is not None:
                effective_env.update(env)

            process_env = os.environ.copy()
            process_env.update(effective_env)

            completed_process = subprocess.run(
                command,
                cwd=str(trial_path),
                env=process_env,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
                shell=False,
            )
        except ValueError as exc:
            duration_seconds = time.perf_counter() - start_time
            return finalize_result(
                status="blocked",
                trial_status=TrialStatus.INVALID,
                return_code=None,
                stdout="",
                stderr="",
                duration_seconds=duration_seconds,
                message=str(exc),
                timeout_seconds=timeout,
            )
        except subprocess.TimeoutExpired as exc:
            duration_seconds = time.perf_counter() - start_time
            stdout = self._coerce_process_output(exc.stdout)
            stderr = self._coerce_process_output(exc.stderr)
            return finalize_result(
                status="timeout",
                trial_status=TrialStatus.TIMEOUT,
                return_code=None,
                stdout=stdout,
                stderr=stderr,
                duration_seconds=duration_seconds,
                message=f"Training command exceeded the timeout limit of {timeout} seconds.",
                timeout_seconds=timeout,
            )
        except FileNotFoundError as exc:
            duration_seconds = time.perf_counter() - start_time
            return finalize_result(
                status="failed",
                trial_status=TrialStatus.FAILED,
                return_code=None,
                stdout="",
                stderr="",
                duration_seconds=duration_seconds,
                message=(
                    "Failed to start the training command because the executable "
                    f"was not found: '{command[0]}'."
                ),
                timeout_seconds=timeout,
            )
        except OSError as exc:
            duration_seconds = time.perf_counter() - start_time
            return finalize_result(
                status="failed",
                trial_status=TrialStatus.FAILED,
                return_code=None,
                stdout="",
                stderr="",
                duration_seconds=duration_seconds,
                message=f"Failed to execute the training command: {exc}.",
                timeout_seconds=timeout,
            )

        duration_seconds = time.perf_counter() - start_time
        status = "success" if completed_process.returncode == 0 else "failed"
        trial_status = (
            TrialStatus.COMPLETED if completed_process.returncode == 0 else TrialStatus.FAILED
        )
        message = (
            "Training command finished successfully."
            if completed_process.returncode == 0
            else f"Training command exited with a non-zero return code: {completed_process.returncode}."
        )

        return finalize_result(
            status=status,
            trial_status=trial_status,
            return_code=completed_process.returncode,
            stdout=completed_process.stdout,
            stderr=completed_process.stderr,
            duration_seconds=duration_seconds,
            message=message,
            timeout_seconds=timeout,
        )

    def collect_metrics(self, trial_dir: str) -> dict[str, Any]:
        """Collect metrics from common trial output files.

        The adapter looks for ``metrics.json``, ``metrics.yaml``, ``metrics.yml``,
        and ``metrics.txt`` in the trial directory. For plain text metrics, each
        line should use ``key=value`` or ``key: value`` format.

        Args:
            trial_dir: The directory assigned to the current trial.

        Returns:
            A mapping of parsed metric names to numeric values. If no recognized
            metrics file is present, an empty dictionary is returned.

        Raises:
            RuntimeError: If a metrics file exists but cannot be parsed safely.
        """

        trial_path = Path(trial_dir)
        for filename in self.metrics_filenames:
            metrics_path = trial_path / filename
            if not metrics_path.exists():
                continue

            try:
                if metrics_path.suffix == ".json":
                    data = json.loads(metrics_path.read_text(encoding="utf-8"))
                    return self._normalize_metrics_mapping(data, metrics_path)

                if metrics_path.suffix in {".yaml", ".yml"}:
                    data = yaml.safe_load(metrics_path.read_text(encoding="utf-8")) or {}
                    return self._normalize_metrics_mapping(data, metrics_path)

                if metrics_path.suffix == ".txt":
                    return self._parse_text_metrics(metrics_path)
            except (json.JSONDecodeError, yaml.YAMLError, OSError, ValueError, TypeError) as exc:
                raise RuntimeError(
                    f"Failed to parse metrics file '{metrics_path}': {exc}."
                ) from exc

        return {}

    def sample_config(self, trial: Trial) -> dict[str, Any]:
        """Sample hyperparameters from an Optuna trial using the configured search space.

        Args:
            trial: The active Optuna trial object.

        Returns:
            A dictionary of sampled hyperparameter values.

        Raises:
            ValueError: If the configured search space contains unsupported definitions.
        """

        sampled: dict[str, Any] = {}

        for name, spec in self.search_space.items():
            spec_type = spec.get("type")
            if spec_type not in _SUPPORTED_SEARCH_SPACE_TYPES:
                raise ValueError(
                    f"Unsupported search space type for parameter '{name}': {spec_type!r}."
                )

            if spec_type == "float":
                if "low" not in spec or "high" not in spec:
                    raise ValueError(
                        f"Float search space for '{name}' must define 'low' and 'high'."
                    )
                sampled[name] = trial.suggest_float(
                    name,
                    spec["low"],
                    spec["high"],
                    log=bool(spec.get("log", False)),
                    step=spec.get("step"),
                )
                continue

            if spec_type == "int":
                if "low" not in spec or "high" not in spec:
                    raise ValueError(
                        f"Integer search space for '{name}' must define 'low' and 'high'."
                    )
                sampled[name] = trial.suggest_int(
                    name,
                    spec["low"],
                    spec["high"],
                    log=bool(spec.get("log", False)),
                    step=spec.get("step", 1),
                )
                continue

            if spec_type == "categorical":
                choices = spec.get("choices")
                if not isinstance(choices, Sequence) or isinstance(choices, (str, bytes)):
                    raise ValueError(
                        f"Categorical search space for '{name}' must define a 'choices' sequence."
                    )
                sampled[name] = trial.suggest_categorical(name, list(choices))
                continue

            if spec_type == "bool":
                sampled[name] = trial.suggest_categorical(name, [False, True])
                continue

            if spec_type == "fixed":
                if "value" not in spec:
                    raise ValueError(
                        f"Fixed search space for '{name}' must define a 'value'."
                    )
                sampled[name] = spec["value"]

        return sampled

    def validate_config(self, trial_config: dict[str, Any]) -> tuple[bool, str]:
        """Validate a sampled trial configuration against the configured search space.

        Args:
            trial_config: The sampled hyperparameter configuration.

        Returns:
            A tuple of ``(is_valid, message)`` describing whether the config is usable.
        """

        if not isinstance(trial_config, dict):
            return False, "Trial configuration must be a dictionary."

        if not self.search_space:
            for name, value in trial_config.items():
                try:
                    self._parameter_to_cli_args(name, value)
                except ValueError as exc:
                    return False, str(exc)
            return True, "Trial configuration is valid."

        expected_keys = set(self.search_space)
        provided_keys = set(trial_config)

        unknown_keys = sorted(provided_keys - expected_keys)
        if unknown_keys:
            return False, f"Unknown trial configuration keys: {unknown_keys!r}."

        missing_keys = sorted(
            name
            for name, spec in self.search_space.items()
            if spec.get("type") != "fixed" and name not in trial_config
        )
        if missing_keys:
            return False, f"Missing required trial configuration keys: {missing_keys!r}."

        for name, value in trial_config.items():
            spec = self.search_space.get(name, {})
            is_valid, reason = self._validate_parameter_value(name, value, spec)
            if not is_valid:
                return False, reason

        return True, "Trial configuration is valid."

    def _validate_search_space(self) -> tuple[bool, str]:
        """Validate the adapter search space definition."""

        for name, spec in self.search_space.items():
            if not isinstance(name, str) or not name.strip():
                return False, "Each search space parameter name must be a non-empty string."

            if not isinstance(spec, dict):
                return False, f"Search space definition for '{name}' must be a dictionary."

            spec_type = spec.get("type")
            if spec_type not in _SUPPORTED_SEARCH_SPACE_TYPES:
                return (
                    False,
                    f"Unsupported search space type for parameter '{name}': {spec_type!r}.",
                )

        return True, "Search space is valid."

    def _validate_parameter_value(
        self,
        name: str,
        value: Any,
        spec: Mapping[str, Any],
    ) -> tuple[bool, str]:
        """Validate a sampled value against one parameter spec."""

        spec_type = spec.get("type")

        if spec_type == "float":
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                return False, f"Parameter '{name}' must be a float-compatible numeric value."
            low = spec.get("low")
            high = spec.get("high")
            if low is not None and value < low:
                return False, f"Parameter '{name}' must be >= {low}, but received {value}."
            if high is not None and value > high:
                return False, f"Parameter '{name}' must be <= {high}, but received {value}."
            return True, "ok"

        if spec_type == "int":
            if not isinstance(value, int) or isinstance(value, bool):
                return False, f"Parameter '{name}' must be an integer."
            low = spec.get("low")
            high = spec.get("high")
            if low is not None and value < low:
                return False, f"Parameter '{name}' must be >= {low}, but received {value}."
            if high is not None and value > high:
                return False, f"Parameter '{name}' must be <= {high}, but received {value}."
            return True, "ok"

        if spec_type == "categorical":
            choices = spec.get("choices", [])
            if value not in choices:
                return False, f"Parameter '{name}' must be one of {list(choices)!r}, but received {value!r}."
            return True, "ok"

        if spec_type == "bool":
            if not isinstance(value, bool):
                return False, f"Parameter '{name}' must be a boolean value."
            return True, "ok"

        if spec_type == "fixed":
            expected = spec.get("value")
            if value != expected:
                return False, f"Parameter '{name}' must equal the fixed value {expected!r}."
            return True, "ok"

        return False, f"Parameter '{name}' uses an unsupported search space type: {spec_type!r}."

    def _parameter_to_cli_args(self, name: str, value: Any) -> list[str]:
        """Convert one parameter into CLI arguments."""

        flag = self.parameter_flags.get(name, f"--{name.replace('_', '-')}")
        if not isinstance(flag, str) or not flag.strip():
            raise ValueError(f"CLI flag for parameter '{name}' must be a non-empty string.")

        if isinstance(value, bool):
            return [flag] if value else []

        if value is None:
            return []

        if isinstance(value, (str, int, float)):
            return [flag, str(value)]

        raise ValueError(
            f"Parameter '{name}' uses unsupported CLI value type: {type(value).__name__}."
        )

    def _render_command_template(
        self,
        command_template: Sequence[str],
        parameters: Mapping[str, Any],
        trial_dir: str,
        trial_id: str,
        output_root: str,
    ) -> list[str]:
        """Render a command template with trial parameters and runtime placeholders."""

        render_context: dict[str, Any] = {
            "task_name": self.task_name,
            "trial_dir": trial_dir,
            "trial_id": trial_id,
            "output_root": output_root,
            "output_dir": trial_dir,
        }
        render_context.update(parameters)

        command: list[str] = []
        for token in command_template:
            if not isinstance(token, str) or not token.strip():
                raise ValueError("Command template entries must be non-empty strings.")
            try:
                rendered = token.format_map(_SafeTemplateMapping(render_context))
            except ValueError as exc:
                raise ValueError(
                    f"Failed to render command template token {token!r}: {exc}."
                ) from exc
            if not rendered.strip():
                raise ValueError(
                    f"Rendered command template token became empty: original token {token!r}."
                )
            command.append(rendered)

        return command

    def _normalize_command_paths(self, command: list[str]) -> list[str]:
        """Normalize known relative script paths to absolute paths when safe to do so."""

        if len(command) < 2:
            return command

        executable_name = Path(command[0]).name.lower()
        looks_like_python = executable_name.startswith("python")
        script_candidate = Path(command[1])

        if looks_like_python and not script_candidate.is_absolute() and script_candidate.suffix == ".py":
            resolved_script = (Path.cwd() / script_candidate).resolve()
            if resolved_script.exists() and resolved_script.is_file():
                normalized = list(command)
                normalized[1] = str(resolved_script)
                return normalized

        return command

    def _infer_trial_id(self, trial_dir: str) -> str:
        """Infer a stable trial id from the trial directory path."""

        trial_path = Path(trial_dir)
        inferred = trial_path.name.strip()
        if inferred:
            return inferred
        return "trial_unknown"

    def _ensure_command_is_safe(self, command: Sequence[str]) -> None:
        """Reject obviously dangerous commands before execution."""

        ensure_command_is_safe(command, allow_commands=self.allow_commands, shell=False)

    def _normalize_metrics_mapping(
        self,
        data: Any,
        source_path: Path,
    ) -> dict[str, float]:
        """Normalize a parsed metrics mapping into numeric values only."""

        if not isinstance(data, dict):
            raise ValueError(
                f"Metrics file '{source_path}' must contain a mapping of metric names to values."
            )

        metrics: dict[str, float] = {}
        for key, value in data.items():
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                metrics[str(key)] = float(value)

        return metrics

    def _parse_text_metrics(self, metrics_path: Path) -> dict[str, float]:
        """Parse a plain text metrics file with ``key=value`` or ``key: value`` lines."""

        metrics: dict[str, float] = {}
        for raw_line in metrics_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue

            if "=" in line:
                key, raw_value = line.split("=", 1)
            elif ":" in line:
                key, raw_value = line.split(":", 1)
            else:
                continue

            key = key.strip()
            raw_value = raw_value.strip()
            if not key:
                continue

            try:
                metrics[key] = float(raw_value)
            except ValueError:
                continue

        return metrics

    def _write_log(self, path: Path, content: str) -> None:
        """Persist one process stream log to disk."""

        try:
            path.write_text(content, encoding="utf-8")
        except OSError as exc:
            raise RuntimeError(f"Failed to write process log file '{path}'.") from exc

    def _coerce_process_output(self, value: str | bytes | None) -> str:
        """Normalize subprocess outputs into text."""

        if value is None:
            return ""
        if isinstance(value, bytes):
            return value.decode("utf-8", errors="replace")
        return value


class _SafeTemplateMapping(dict[str, Any]):
    """Dictionary wrapper that raises clear errors for missing placeholders."""

    def __missing__(self, key: str) -> Any:
        raise ValueError(
            f"Command template references placeholder '{key}', but no value was provided."
        )
