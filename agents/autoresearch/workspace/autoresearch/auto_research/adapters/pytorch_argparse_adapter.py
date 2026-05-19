"""Generic argparse-style adapter for external PyTorch training projects."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from auto_research.adapters.subprocess_adapter import SubprocessAdapter


@dataclass(slots=True)
class PyTorchArgparseAdapter(SubprocessAdapter):
    """Adapter for training entrypoints driven by argparse-style CLI flags."""

    train_entry: str = ""
    fixed_args: list[str] = field(default_factory=list)
    param_arg_map: dict[str, str] = field(default_factory=dict)
    output_dir_arg: str = "--output-dir"
    python_executable: str = "python"

    def __post_init__(self) -> None:
        """Validate argparse-adapter-specific configuration and initialize the base adapter."""

        if not self.train_entry.strip():
            raise ValueError("PyTorchArgparseAdapter requires a non-empty 'train_entry'.")
        if not self.output_dir_arg.strip():
            raise ValueError("PyTorchArgparseAdapter requires a non-empty 'output_dir_arg'.")
        if any(not isinstance(arg, str) or not arg.strip() for arg in self.fixed_args):
            raise ValueError(
                "PyTorchArgparseAdapter 'fixed_args' must contain only non-empty strings."
            )

        self.base_command = [self.python_executable, self.train_entry]
        self.static_args = list(self.fixed_args)
        self.parameter_flags = dict(self.param_arg_map)
        self.command_template = None
        SubprocessAdapter.__post_init__(self)

    def prepare_trial(self, trial_config: dict[str, Any], trial_dir: str) -> dict[str, Any]:
        """Prepare one trial with an injected output-dir parameter."""

        prepared = SubprocessAdapter.prepare_trial(self, trial_config, trial_dir)
        parameters = dict(prepared["parameters"])
        parameters["_output_dir"] = prepared["trial_dir"]
        prepared["parameters"] = parameters
        return prepared

    def build_command(self, prepared_config: dict[str, Any], trial_dir: str) -> list[str]:
        """Build an argparse-style training command."""

        parameters = prepared_config.get("parameters")
        if not isinstance(parameters, dict):
            raise ValueError(
                "Prepared configuration for PyTorchArgparseAdapter must contain 'parameters'."
            )

        command = list(self.base_command)
        command.extend(self.static_args)

        for name, value in parameters.items():
            if name == "_output_dir":
                command.extend([self.output_dir_arg, str(value)])
                continue
            flag = self.param_arg_map.get(name, f"--{name.replace('_', '-')}")
            command.extend(self._parameter_to_cli_args_from_flag(name=name, flag=flag, value=value))

        command = self._normalize_command_paths(command)
        self._ensure_command_is_safe(command)

        trial_path = Path(trial_dir)
        if not trial_path.exists():
            raise ValueError(
                f"Trial directory does not exist while building argparse adapter command: '{trial_dir}'."
            )

        return command

    def _parameter_to_cli_args_from_flag(self, name: str, flag: str, value: Any) -> list[str]:
        """Convert one parameter to CLI args using an explicit flag mapping."""

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
