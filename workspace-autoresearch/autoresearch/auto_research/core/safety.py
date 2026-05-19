"""Centralized safety checks for commands, metrics, trial paths, and study execution."""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Mapping, Sequence

_DEFAULT_ALLOW_COMMANDS = ("python", "python3")
_DANGEROUS_EXECUTABLES = {"rm", "shutdown", "reboot", "mkfs", "dd"}
_DANGEROUS_COMMAND_PATTERNS: tuple[tuple[str, ...], ...] = (
    ("rm", "-rf"),
    ("rm", "-fr"),
)


class SafetyStopStudyError(RuntimeError):
    """Raised when a safety policy requests an early stop for the current study."""


@dataclass(slots=True)
class FailureTracker:
    """Track consecutive failures and stop the study when the configured limit is exceeded."""

    max_consecutive_failures: int | None = None
    consecutive_failures: int = 0

    def record_success(self) -> None:
        """Reset the failure counter after a successful trial."""

        self.consecutive_failures = 0

    def record_failure(self) -> None:
        """Increment the failure counter and stop when the limit is exceeded."""

        self.consecutive_failures += 1
        if (
            self.max_consecutive_failures is not None
            and self.max_consecutive_failures > 0
            and self.consecutive_failures > self.max_consecutive_failures
        ):
            raise SafetyStopStudyError(
                "Stopping study because consecutive failures exceeded the configured limit of "
                f"{self.max_consecutive_failures}."
            )


@dataclass(slots=True)
class DuplicateConfigTracker:
    """Track seen configuration hashes within one study execution."""

    seen_hashes: set[str] = field(default_factory=set)

    def check_and_add(self, trial_config: Mapping[str, Any]) -> tuple[bool, str]:
        """Record one config hash and report whether it is a duplicate."""

        config_hash = hash_trial_config(dict(trial_config))
        if config_hash in self.seen_hashes:
            return False, config_hash
        self.seen_hashes.add(config_hash)
        return True, config_hash


def validate_safety_config(safety: Any) -> tuple[bool, str]:
    """Validate the optional task-card safety section."""

    if safety in ({}, None):
        return True, "Safety config is valid."

    if not isinstance(safety, dict):
        return False, "Task card field 'safety' must be a dictionary when provided."

    max_failures = safety.get("max_consecutive_failures")
    if max_failures is not None:
        if (
            not isinstance(max_failures, int)
            or isinstance(max_failures, bool)
            or max_failures <= 0
        ):
            return False, "Task card field 'safety.max_consecutive_failures' must be a positive integer."

    allow_commands = safety.get("allow_commands")
    if allow_commands is not None:
        if not isinstance(allow_commands, list) or not allow_commands:
            return False, "Task card field 'safety.allow_commands' must be a non-empty list of strings."
        for item in allow_commands:
            if not isinstance(item, str) or not item.strip():
                return False, "Task card field 'safety.allow_commands' must contain only non-empty strings."

    return True, "Safety config is valid."


def resolve_allow_commands(safety: Mapping[str, Any] | None = None) -> list[str]:
    """Resolve the allowed executable list from a safety config."""

    if not isinstance(safety, Mapping):
        return list(_DEFAULT_ALLOW_COMMANDS)

    allow_commands = safety.get("allow_commands")
    if not isinstance(allow_commands, list) or not allow_commands:
        return list(_DEFAULT_ALLOW_COMMANDS)

    return [item.strip() for item in allow_commands if isinstance(item, str) and item.strip()]


def ensure_command_is_safe(
    command: Sequence[str],
    *,
    allow_commands: Sequence[str] | None = None,
    shell: bool = False,
) -> None:
    """Validate one command against shell, whitelist, and dangerous command rules."""

    if shell:
        raise ValueError("Refusing to execute commands with shell=True.")

    if not command:
        raise ValueError("Training command cannot be empty.")

    if any(not isinstance(part, str) or not part.strip() for part in command):
        raise ValueError("Training command must be a list of non-empty strings.")

    executable = command[0]
    executable_name = Path(executable).name.lower()
    normalized_executable = _normalize_executable_name(executable_name)
    allowed = {_normalize_executable_name(Path(item).name.lower()) for item in (allow_commands or _DEFAULT_ALLOW_COMMANDS)}

    if normalized_executable not in allowed:
        raise ValueError(
            "Refusing to execute command because the executable is not in the allowed list: "
            f"'{executable}'. Allowed commands: {sorted(allowed)!r}."
        )

    if normalized_executable in _DANGEROUS_EXECUTABLES:
        raise ValueError(f"Refusing to execute dangerous command '{executable}'.")

    lowered = [_normalize_executable_name(Path(part).name.lower()) if index == 0 else part.lower() for index, part in enumerate(command)]
    for pattern in _DANGEROUS_COMMAND_PATTERNS:
        if tuple(lowered[: len(pattern)]) == pattern:
            raise ValueError(
                "Refusing to execute a blocked command pattern: "
                f"{' '.join(command[: len(pattern)])}."
            )


def ensure_trial_dir_within_output_root(trial_dir: str, output_root: str) -> None:
    """Ensure a trial directory stays within the configured output root."""

    resolved_trial_dir = Path(trial_dir).resolve()
    resolved_output_root = Path(output_root).resolve()

    try:
        resolved_trial_dir.relative_to(resolved_output_root)
    except ValueError as exc:
        raise ValueError(
            f"Trial directory '{resolved_trial_dir}' must be located under output_root '{resolved_output_root}'."
        ) from exc


def ensure_metrics_are_finite(metrics: Mapping[str, Any]) -> None:
    """Ensure all numeric metrics are finite, rejecting NaN and Inf values."""

    for name, value in metrics.items():
        if isinstance(value, bool):
            continue
        if isinstance(value, (int, float)):
            numeric = float(value)
            if not math.isfinite(numeric):
                raise ValueError(
                    f"Metric '{name}' contains a non-finite value: {value!r}."
                )


def hash_trial_config(trial_config: Mapping[str, Any]) -> str:
    """Return a stable SHA-256 hash for a trial configuration."""

    normalized = _normalize_for_hash(dict(trial_config))
    serialized = json.dumps(normalized, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def _normalize_executable_name(name: str) -> str:
    """Normalize an executable name for whitelist and danger checks."""

    normalized = name.strip().lower()
    if normalized.endswith(".exe"):
        normalized = normalized[:-4]
    return normalized


def _normalize_for_hash(value: Any) -> Any:
    """Normalize a structure into a deterministic JSON-safe representation."""

    if isinstance(value, Mapping):
        return {str(key): _normalize_for_hash(value[key]) for key in sorted(value)}
    if isinstance(value, list):
        return [_normalize_for_hash(item) for item in value]
    if isinstance(value, tuple):
        return [_normalize_for_hash(item) for item in value]
    if isinstance(value, Path):
        return str(value)
    return value
