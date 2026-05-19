"""Generic YAML-config-based adapter for external PyTorch-style training projects."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml

from auto_research.adapters.subprocess_adapter import SubprocessAdapter


@dataclass(slots=True)
class PyTorchYamlAdapter(SubprocessAdapter):
    """Adapter for projects that launch training from a YAML config file.

    This adapter is intentionally generic. It does not assume any specific
    framework config schema beyond accepting a base YAML file and overriding
    selected keys via dot-path notation such as ``SOLVER.BASE_LR``.
    """

    train_entry: str = ""
    base_config_path: str = ""
    config_arg_name: str = "--config"
    output_dir_key: str = ""
    param_key_map: dict[str, str] = field(default_factory=dict)
    fixed_args: list[str] = field(default_factory=list)
    python_executable: str = "python"
    config_output_name: str = "resolved_config.yaml"

    def __post_init__(self) -> None:
        """Validate YAML-adapter-specific configuration and initialize the base adapter."""

        if not self.train_entry.strip():
            raise ValueError("PyTorchYamlAdapter requires a non-empty 'train_entry'.")
        if not self.base_config_path.strip():
            raise ValueError("PyTorchYamlAdapter requires a non-empty 'base_config_path'.")
        if not self.config_arg_name.strip():
            raise ValueError("PyTorchYamlAdapter requires a non-empty 'config_arg_name'.")
        if not self.output_dir_key.strip():
            raise ValueError("PyTorchYamlAdapter requires a non-empty 'output_dir_key'.")
        if any(not isinstance(arg, str) or not arg.strip() for arg in self.fixed_args):
            raise ValueError("PyTorchYamlAdapter 'fixed_args' must contain only non-empty strings.")

        self.base_command = [self.python_executable, self.train_entry]
        self.static_args = list(self.fixed_args)
        self.command_template = None
        SubprocessAdapter.__post_init__(self)

    def prepare_trial(self, trial_config: dict[str, Any], trial_dir: str) -> dict[str, Any]:
        """Prepare a resolved YAML config file for one trial."""

        prepared = SubprocessAdapter.prepare_trial(self, trial_config, trial_dir)
        config_data = self._load_base_config()
        parameters = dict(prepared["parameters"])

        for name, value in parameters.items():
            config_key = self.param_key_map.get(name, name)
            self._set_by_dot_path(config_data, config_key, value)

        self._set_by_dot_path(config_data, self.output_dir_key, prepared["trial_dir"])

        config_path = Path(prepared["trial_dir"]) / self.config_output_name
        try:
            config_path.write_text(
                yaml.safe_dump(config_data, sort_keys=False, allow_unicode=False),
                encoding="utf-8",
            )
        except OSError as exc:
            raise RuntimeError(
                f"Failed to write resolved YAML config for trial to '{config_path}'."
            ) from exc

        prepared["resolved_config_path"] = str(config_path.resolve())
        return prepared

    def build_command(self, prepared_config: dict[str, Any], trial_dir: str) -> list[str]:
        """Build the launch command using the resolved YAML config file."""

        resolved_config_path = prepared_config.get("resolved_config_path")
        if not isinstance(resolved_config_path, str) or not resolved_config_path.strip():
            raise ValueError(
                "Prepared configuration for PyTorchYamlAdapter must include 'resolved_config_path'."
            )

        command = list(self.base_command)
        command.extend(self.static_args)
        command.extend([self.config_arg_name, resolved_config_path])
        command = self._normalize_command_paths(command)
        self._ensure_command_is_safe(command)

        trial_path = Path(trial_dir)
        if not trial_path.exists():
            raise ValueError(
                f"Trial directory does not exist while building YAML adapter command: '{trial_dir}'."
            )

        return command

    def _load_base_config(self) -> dict[str, Any]:
        """Load the base YAML configuration file."""

        config_path = Path(self.base_config_path)
        if not config_path.is_absolute():
            config_path = (Path.cwd() / config_path).resolve()

        if not config_path.exists() or not config_path.is_file():
            raise FileNotFoundError(
                f"Base config file for PyTorchYamlAdapter does not exist: '{config_path}'."
            )

        try:
            payload = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
        except (OSError, yaml.YAMLError) as exc:
            raise RuntimeError(
                f"Failed to load base YAML config from '{config_path}': {exc}."
            ) from exc

        if not isinstance(payload, dict):
            raise ValueError(
                f"Base config file '{config_path}' must contain a YAML mapping at the top level."
            )

        return payload

    def _set_by_dot_path(self, config: dict[str, Any], dot_path: str, value: Any) -> None:
        """Set a nested config value using ``A.B.C`` style dot-path notation."""

        if not isinstance(dot_path, str) or not dot_path.strip():
            raise ValueError("Config override path must be a non-empty string.")

        keys = [part.strip() for part in dot_path.split(".") if part.strip()]
        if not keys:
            raise ValueError(f"Config override path '{dot_path}' is invalid.")

        current: dict[str, Any] = config
        for key in keys[:-1]:
            existing = current.get(key)
            if existing is None:
                current[key] = {}
                existing = current[key]
            if not isinstance(existing, dict):
                raise ValueError(
                    f"Cannot set config path '{dot_path}' because '{key}' is not a mapping."
                )
            current = existing

        current[keys[-1]] = value
