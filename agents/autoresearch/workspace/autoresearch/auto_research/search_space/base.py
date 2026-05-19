"""Utilities for validating and sampling task-card-defined search spaces."""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
from typing import Any, Mapping, Sequence


_SUPPORTED_SEARCH_SPACE_TYPES = {"float", "int", "categorical", "bool"}


@dataclass(slots=True)
class SearchSpaceDefinition:
    """Container and helper wrapper for task-card-defined hyperparameter spaces."""

    parameters: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> tuple[bool, str]:
        """Validate the wrapped search space definition."""

        return validate_search_space(self.parameters)

    def sample(self, trial: Any) -> dict[str, Any]:
        """Sample parameter values from the wrapped search space."""

        return sample_from_search_space(trial, self.parameters)

    def hash(self) -> str:
        """Return a stable hash for the wrapped search space."""

        return hash_search_space(self.parameters)


def sample_from_search_space(trial: Any, search_space: dict[str, Any]) -> dict[str, Any]:
    """Sample one trial configuration from a validated search space definition.

    Args:
        trial: An Optuna-compatible trial object providing ``suggest_*`` methods.
        search_space: Search space mapping loaded from a YAML task card.

    Returns:
        A dictionary of sampled parameter values.

    Raises:
        ValueError: If the search space definition is invalid.
        RuntimeError: If the trial object is missing a required sampling method.
    """

    is_valid, message = validate_search_space(search_space)
    if not is_valid:
        raise ValueError(f"Invalid search space: {message}")

    sampled_config: dict[str, Any] = {}

    for name, spec in search_space.items():
        spec_type = spec["type"]

        if spec_type == "float":
            low = _coerce_float(spec["low"], field_name=f"{name}.low")
            high = _coerce_float(spec["high"], field_name=f"{name}.high")
            log = bool(spec.get("log", False))
            try:
                sampled_config[name] = trial.suggest_float(name, low, high, log=log)
            except AttributeError as exc:
                raise RuntimeError(
                    "The provided trial object does not implement 'suggest_float', "
                    f"which is required for parameter '{name}'."
                ) from exc
            continue

        if spec_type == "int":
            low = _coerce_int(spec["low"], field_name=f"{name}.low")
            high = _coerce_int(spec["high"], field_name=f"{name}.high")
            step = _coerce_int(spec.get("step", 1), field_name=f"{name}.step")
            try:
                sampled_config[name] = trial.suggest_int(name, low, high, step=step)
            except AttributeError as exc:
                raise RuntimeError(
                    "The provided trial object does not implement 'suggest_int', "
                    f"which is required for parameter '{name}'."
                ) from exc
            continue

        if spec_type == "categorical":
            choices = list(spec["choices"])
            try:
                sampled_config[name] = trial.suggest_categorical(name, choices)
            except AttributeError as exc:
                raise RuntimeError(
                    "The provided trial object does not implement 'suggest_categorical', "
                    f"which is required for parameter '{name}'."
                ) from exc
            continue

        if spec_type == "bool":
            try:
                sampled_config[name] = trial.suggest_categorical(name, [False, True])
            except AttributeError as exc:
                raise RuntimeError(
                    "The provided trial object does not implement 'suggest_categorical', "
                    f"which is required for boolean parameter '{name}'."
                ) from exc
            continue

        raise ValueError(
            f"Unsupported search space type for parameter '{name}': {spec_type!r}."
        )

    return sampled_config


def validate_search_space(search_space: dict[str, Any]) -> tuple[bool, str]:
    """Validate a task-card search space definition.

    Args:
        search_space: Search space mapping loaded from YAML.

    Returns:
        A tuple of ``(is_valid, message)``.
    """

    if not isinstance(search_space, dict):
        return False, "Search space must be a dictionary mapping parameter names to specs."

    for name, spec in search_space.items():
        if not isinstance(name, str) or not name.strip():
            return False, "Search space parameter names must be non-empty strings."

        if not isinstance(spec, dict):
            return False, f"Search space spec for parameter '{name}' must be a dictionary."

        spec_type = spec.get("type")
        if spec_type not in _SUPPORTED_SEARCH_SPACE_TYPES:
            return (
                False,
                f"Parameter '{name}' has unsupported type {spec_type!r}. "
                f"Supported types are: {sorted(_SUPPORTED_SEARCH_SPACE_TYPES)!r}.",
            )

        if spec_type == "float":
            is_valid, message = _validate_float_spec(name, spec)
            if not is_valid:
                return False, message
            continue

        if spec_type == "int":
            is_valid, message = _validate_int_spec(name, spec)
            if not is_valid:
                return False, message
            continue

        if spec_type == "categorical":
            is_valid, message = _validate_categorical_spec(name, spec)
            if not is_valid:
                return False, message
            continue

        if spec_type == "bool":
            unexpected_keys = sorted(set(spec) - {"type"})
            if unexpected_keys:
                return (
                    False,
                    f"Boolean parameter '{name}' does not accept extra fields: {unexpected_keys!r}.",
                )

    return True, "Search space is valid."


def hash_search_space(search_space: dict[str, Any]) -> str:
    """Return a stable hash for a validated search space definition.

    Args:
        search_space: Search space mapping loaded from YAML.

    Returns:
        A SHA-256 hex digest of the canonicalized search space.

    Raises:
        ValueError: If the search space definition is invalid.
    """

    is_valid, message = validate_search_space(search_space)
    if not is_valid:
        raise ValueError(f"Cannot hash invalid search space: {message}")

    normalized = _normalize_for_hash(search_space)
    serialized = json.dumps(normalized, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def _validate_float_spec(name: str, spec: Mapping[str, Any]) -> tuple[bool, str]:
    """Validate a float search space spec."""

    missing = [key for key in ("low", "high") if key not in spec]
    if missing:
        return False, f"Float parameter '{name}' is missing required fields: {missing!r}."

    unexpected_keys = sorted(set(spec) - {"type", "low", "high", "log"})
    if unexpected_keys:
        return (
            False,
            f"Float parameter '{name}' has unsupported fields: {unexpected_keys!r}.",
        )

    try:
        low = _coerce_float(spec["low"], field_name=f"{name}.low")
        high = _coerce_float(spec["high"], field_name=f"{name}.high")
    except ValueError as exc:
        return False, str(exc)

    if low >= high:
        return False, f"Float parameter '{name}' requires low < high, but received {low} and {high}."

    log = spec.get("log", False)
    if not isinstance(log, bool):
        return False, f"Float parameter '{name}.log' must be a boolean value."

    if log and (low <= 0 or high <= 0):
        return (
            False,
            f"Float parameter '{name}' uses log sampling, so both low and high must be > 0.",
        )

    return True, "ok"


def _validate_int_spec(name: str, spec: Mapping[str, Any]) -> tuple[bool, str]:
    """Validate an int search space spec."""

    missing = [key for key in ("low", "high") if key not in spec]
    if missing:
        return False, f"Integer parameter '{name}' is missing required fields: {missing!r}."

    unexpected_keys = sorted(set(spec) - {"type", "low", "high", "step"})
    if unexpected_keys:
        return (
            False,
            f"Integer parameter '{name}' has unsupported fields: {unexpected_keys!r}.",
        )

    try:
        low = _coerce_int(spec["low"], field_name=f"{name}.low")
        high = _coerce_int(spec["high"], field_name=f"{name}.high")
        step = _coerce_int(spec.get("step", 1), field_name=f"{name}.step")
    except ValueError as exc:
        return False, str(exc)

    if low > high:
        return False, f"Integer parameter '{name}' requires low <= high, but received {low} and {high}."

    if step <= 0:
        return False, f"Integer parameter '{name}.step' must be a positive integer."

    return True, "ok"


def _validate_categorical_spec(name: str, spec: Mapping[str, Any]) -> tuple[bool, str]:
    """Validate a categorical search space spec."""

    if "choices" not in spec:
        return False, f"Categorical parameter '{name}' is missing required field 'choices'."

    unexpected_keys = sorted(set(spec) - {"type", "choices"})
    if unexpected_keys:
        return (
            False,
            f"Categorical parameter '{name}' has unsupported fields: {unexpected_keys!r}.",
        )

    choices = spec["choices"]
    if not isinstance(choices, Sequence) or isinstance(choices, (str, bytes)):
        return (
            False,
            f"Categorical parameter '{name}.choices' must be a non-string sequence.",
        )

    if len(choices) == 0:
        return False, f"Categorical parameter '{name}.choices' cannot be empty."

    for index, choice in enumerate(choices):
        if isinstance(choice, bool):
            continue
        if isinstance(choice, (int, float, str)):
            continue
        return (
            False,
            f"Categorical parameter '{name}.choices[{index}]' must be a number, string, or boolean, "
            f"but received {type(choice).__name__}.",
        )

    return True, "ok"


def _coerce_float(value: Any, *, field_name: str) -> float:
    """Coerce a numeric search space value to float with clear errors."""

    if isinstance(value, bool):
        raise ValueError(f"Field '{field_name}' must be a float-compatible number, not a boolean.")

    if isinstance(value, (int, float)):
        return float(value)

    if isinstance(value, str):
        try:
            return float(value)
        except ValueError as exc:
            raise ValueError(
                f"Field '{field_name}' must be a float-compatible number, but received {value!r}."
            ) from exc

    raise ValueError(
        f"Field '{field_name}' must be a float-compatible number, but received {type(value).__name__}."
    )


def _coerce_int(value: Any, *, field_name: str) -> int:
    """Coerce an integer search space value with clear errors."""

    if isinstance(value, bool):
        raise ValueError(f"Field '{field_name}' must be an integer, not a boolean.")

    if isinstance(value, int):
        return value

    if isinstance(value, str):
        try:
            if value.strip() != value or value == "":
                raise ValueError
            return int(value)
        except ValueError as exc:
            raise ValueError(
                f"Field '{field_name}' must be an integer, but received {value!r}."
            ) from exc

    raise ValueError(
        f"Field '{field_name}' must be an integer, but received {type(value).__name__}."
    )


def _normalize_for_hash(value: Any) -> Any:
    """Normalize a validated search space into a deterministic JSON-safe structure."""

    if isinstance(value, dict):
        return {key: _normalize_for_hash(value[key]) for key in sorted(value)}

    if isinstance(value, list):
        return [_normalize_for_hash(item) for item in value]

    if isinstance(value, tuple):
        return [_normalize_for_hash(item) for item in value]

    return value
