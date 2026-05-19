"""Task card loading, validation, and adapter factory helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from auto_research.adapters.base import TrainingAdapter
from auto_research.adapters.pytorch_argparse_adapter import PyTorchArgparseAdapter
from auto_research.adapters.pytorch_yaml_adapter import PyTorchYamlAdapter
from auto_research.adapters.subprocess_adapter import SubprocessAdapter
from auto_research.core.safety import resolve_allow_commands, validate_safety_config
from auto_research.search_space.base import validate_search_space
from auto_research.utils.yaml import load_yaml

_SUPPORTED_ADAPTER_TYPES = {"subprocess", "pytorch_yaml", "pytorch_argparse"}
_IMPLEMENTED_ADAPTER_TYPES = {"subprocess", "pytorch_yaml", "pytorch_argparse"}


def load_task_card(path: str) -> dict[str, Any]:
    """Load a task card YAML file into a dictionary.

    Args:
        path: Path to the YAML task card file.

    Returns:
        A dictionary containing the parsed task card.

    Raises:
        FileNotFoundError: If the task card file does not exist.
        RuntimeError: If the task card cannot be read or parsed.
        ValueError: If the task card content is not a mapping.
    """

    card_path = Path(path)
    if not card_path.exists():
        raise FileNotFoundError(f"Task card file does not exist: '{path}'.")
    if not card_path.is_file():
        raise FileNotFoundError(f"Task card path is not a file: '{path}'.")

    try:
        card = load_yaml(card_path)
    except FileNotFoundError:
        raise
    except TypeError as exc:
        raise ValueError(f"Task card at '{path}' must contain a YAML mapping.") from exc
    except Exception as exc:
        raise RuntimeError(f"Failed to load task card from '{path}': {exc}.") from exc

    if not isinstance(card, dict):
        raise ValueError(f"Task card at '{path}' must contain a YAML mapping.")

    return card


def validate_task_card(card: dict[str, Any]) -> tuple[bool, str]:
    """Validate a task card definition before adapter creation.

    Args:
        card: Parsed task card dictionary.

    Returns:
        A tuple of ``(is_valid, message)``.
    """

    if not isinstance(card, dict):
        return False, "Task card must be a dictionary."

    task_name = card.get("task_name")
    if not isinstance(task_name, str) or not task_name.strip():
        return False, "Task card is missing required field 'task_name' or it is empty."

    adapter = card.get("adapter")
    if not isinstance(adapter, dict):
        return False, "Task card is missing required field 'adapter' or it is not a dictionary."

    adapter_type = adapter.get("type")
    if not isinstance(adapter_type, str) or not adapter_type.strip():
        return False, "Task card adapter is missing required field 'type'."
    if adapter_type not in _SUPPORTED_ADAPTER_TYPES:
        return (
            False,
            f"Unsupported adapter.type '{adapter_type}'. Supported types are: "
            f"{sorted(_SUPPORTED_ADAPTER_TYPES)!r}.",
        )

    if adapter_type == "subprocess":
        command_template = adapter.get("command_template")
        if not isinstance(command_template, list) or not command_template:
            return (
                False,
                "Subprocess task card requires 'adapter.command_template' as a non-empty list.",
            )
        invalid_tokens = [
            token
            for token in command_template
            if not isinstance(token, str) or not token.strip()
        ]
        if invalid_tokens:
            return (
                False,
                "Subprocess adapter command_template must contain only non-empty strings.",
            )
    elif adapter_type == "pytorch_yaml":
        required_fields = ["train_entry", "base_config_path", "output_dir_key"]
        for field_name in required_fields:
            value = adapter.get(field_name)
            if not isinstance(value, str) or not value.strip():
                return (
                    False,
                    f"PyTorch YAML task card requires non-empty 'adapter.{field_name}'.",
                )
        if "config_arg_name" in adapter:
            value = adapter.get("config_arg_name")
            if not isinstance(value, str) or not value.strip():
                return False, "Task card field 'adapter.config_arg_name' must be a non-empty string."
        is_valid, message = _validate_optional_string_mapping(
            adapter.get("param_key_map", {}),
            field_name="adapter.param_key_map",
        )
        if not is_valid:
            return False, message
        is_valid, message = _validate_optional_string_list(
            adapter.get("fixed_args", []),
            field_name="adapter.fixed_args",
        )
        if not is_valid:
            return False, message
    elif adapter_type == "pytorch_argparse":
        required_fields = ["train_entry", "output_dir_arg"]
        for field_name in required_fields:
            value = adapter.get(field_name)
            if not isinstance(value, str) or not value.strip():
                return (
                    False,
                    f"PyTorch argparse task card requires non-empty 'adapter.{field_name}'.",
                )
        is_valid, message = _validate_optional_string_mapping(
            adapter.get("param_arg_map", {}),
            field_name="adapter.param_arg_map",
        )
        if not is_valid:
            return False, message
        is_valid, message = _validate_optional_string_list(
            adapter.get("fixed_args", []),
            field_name="adapter.fixed_args",
        )
        if not is_valid:
            return False, message

    search_space = card.get("search_space")
    if not isinstance(search_space, dict):
        return (
            False,
            "Task card is missing required field 'search_space' or it is not a dictionary.",
        )
    is_valid_search_space, search_space_message = validate_search_space(search_space)
    if not is_valid_search_space:
        return False, f"Invalid search_space: {search_space_message}"

    score = card.get("score")
    if not isinstance(score, dict):
        return False, "Task card is missing required field 'score' or it is not a dictionary."

    primary_metric = score.get("primary_metric")
    if not isinstance(primary_metric, str) or not primary_metric.strip():
        return False, "Task card score is missing required field 'primary_metric'."

    secondary_metrics = score.get("secondary_metrics", {})
    is_valid_secondary, secondary_message = _validate_metric_weights(
        secondary_metrics,
        field_name="score.secondary_metrics",
    )
    if not is_valid_secondary:
        return False, secondary_message

    penalties = score.get("penalties", {})
    is_valid_penalties, penalties_message = _validate_metric_weights(
        penalties,
        field_name="score.penalties",
    )
    if not is_valid_penalties:
        return False, penalties_message

    if "invalid_score" in score:
        try:
            float(score["invalid_score"])
        except (TypeError, ValueError):
            return False, "Task card field 'score.invalid_score' must be numeric."

    constraints = card.get("constraints", {})
    if constraints is not None and not isinstance(constraints, dict):
        return False, "Task card field 'constraints' must be a dictionary when provided."

    if isinstance(constraints, dict):
        timeout = constraints.get("timeout")
        if timeout is not None:
            if not isinstance(timeout, int) or isinstance(timeout, bool) or timeout <= 0:
                return False, "Task card field 'constraints.timeout' must be a positive integer."

        max_trials = constraints.get("max_trials")
        if max_trials is not None:
            if not isinstance(max_trials, int) or isinstance(max_trials, bool) or max_trials <= 0:
                return False, "Task card field 'constraints.max_trials' must be a positive integer."

    safety = card.get("safety", {})
    is_valid_safety, safety_message = validate_safety_config(safety)
    if not is_valid_safety:
        return False, safety_message

    return True, "Task card is valid."


def create_adapter_from_task_card(card: dict[str, Any]) -> TrainingAdapter:
    """Create an adapter instance from a validated task card.

    Args:
        card: Parsed task card dictionary.

    Returns:
        A configured adapter instance.

    Raises:
        ValueError: If the task card is invalid.
        NotImplementedError: If the adapter type is recognized but not yet implemented.
    """

    is_valid, message = validate_task_card(card)
    if not is_valid:
        raise ValueError(f"Cannot create adapter from invalid task card: {message}")

    adapter = card["adapter"]
    adapter_type = adapter["type"]

    if adapter_type not in _IMPLEMENTED_ADAPTER_TYPES:
        raise NotImplementedError(
            f"Adapter type '{adapter_type}' is reserved but not implemented yet."
        )

    if adapter_type == "subprocess":
        search_space = card["search_space"]
        output_root = adapter.get("output_root", "outputs")
        env = _coerce_string_mapping(adapter.get("env", {}), field_name="adapter.env")
        metrics_filenames = _coerce_metrics_filenames(adapter.get("metrics_filenames"))
        allow_commands = resolve_allow_commands(card.get("safety", {}))

        return SubprocessAdapter(
            task_name=card["task_name"],
            base_command=[adapter["command_template"][0]],
            command_template=list(adapter["command_template"]),
            search_space=search_space,
            base_env=env,
            output_root=output_root,
            metrics_filenames=metrics_filenames,
            allow_commands=allow_commands,
        )

    if adapter_type == "pytorch_yaml":
        output_root = adapter.get("output_root", "outputs")
        env = _coerce_string_mapping(adapter.get("env", {}), field_name="adapter.env")
        metrics_filenames = _coerce_metrics_filenames(adapter.get("metrics_filenames"))
        fixed_args = _coerce_string_list(adapter.get("fixed_args", []), field_name="adapter.fixed_args")
        param_key_map = _coerce_string_mapping(
            adapter.get("param_key_map", {}),
            field_name="adapter.param_key_map",
        )
        allow_commands = resolve_allow_commands(card.get("safety", {}))

        return PyTorchYamlAdapter(
            task_name=card["task_name"],
            base_command=["python"],
            search_space=card["search_space"],
            base_env=env,
            output_root=output_root,
            metrics_filenames=metrics_filenames,
            train_entry=str(adapter["train_entry"]),
            base_config_path=str(adapter["base_config_path"]),
            config_arg_name=str(adapter.get("config_arg_name", "--config")),
            output_dir_key=str(adapter["output_dir_key"]),
            param_key_map=param_key_map,
            fixed_args=fixed_args,
            python_executable=str(adapter.get("python_executable", "python")),
            config_output_name=str(adapter.get("config_output_name", "resolved_config.yaml")),
            allow_commands=allow_commands,
        )

    if adapter_type == "pytorch_argparse":
        output_root = adapter.get("output_root", "outputs")
        env = _coerce_string_mapping(adapter.get("env", {}), field_name="adapter.env")
        metrics_filenames = _coerce_metrics_filenames(adapter.get("metrics_filenames"))
        fixed_args = _coerce_string_list(adapter.get("fixed_args", []), field_name="adapter.fixed_args")
        param_arg_map = _coerce_string_mapping(
            adapter.get("param_arg_map", {}),
            field_name="adapter.param_arg_map",
        )
        allow_commands = resolve_allow_commands(card.get("safety", {}))

        return PyTorchArgparseAdapter(
            task_name=card["task_name"],
            base_command=["python"],
            search_space=card["search_space"],
            base_env=env,
            output_root=output_root,
            metrics_filenames=metrics_filenames,
            train_entry=str(adapter["train_entry"]),
            fixed_args=fixed_args,
            param_arg_map=param_arg_map,
            output_dir_arg=str(adapter["output_dir_arg"]),
            python_executable=str(adapter.get("python_executable", "python")),
            allow_commands=allow_commands,
        )

    raise NotImplementedError(
        f"Adapter type '{adapter_type}' is not implemented."
    )


def _validate_metric_weights(
    value: Any,
    *,
    field_name: str,
) -> tuple[bool, str]:
    """Validate secondary metric or penalty weight mappings."""

    if value in ({}, None):
        return True, "ok"

    if not isinstance(value, Mapping):
        return False, f"Task card field '{field_name}' must be a dictionary when provided."

    for key, weight in value.items():
        if not isinstance(key, str) or not key.strip():
            return False, f"Task card field '{field_name}' must use non-empty string metric names."
        try:
            float(weight)
        except (TypeError, ValueError):
            return False, f"Weight for '{field_name}.{key}' must be numeric."

    return True, "ok"


def _coerce_string_mapping(value: Any, *, field_name: str) -> dict[str, str]:
    """Coerce an optional string mapping with clear validation errors."""

    if value in ({}, None):
        return {}

    if not isinstance(value, Mapping):
        raise ValueError(f"Task card field '{field_name}' must be a dictionary.")

    result: dict[str, str] = {}
    for key, item in value.items():
        if not isinstance(key, str) or not isinstance(item, str):
            raise ValueError(
                f"Task card field '{field_name}' must map string keys to string values."
            )
        result[key] = item

    return result


def _coerce_string_list(value: Any, *, field_name: str) -> list[str]:
    """Coerce an optional string list with clear validation errors."""

    if value in ({}, None, []):
        return []

    if not isinstance(value, list):
        raise ValueError(f"Task card field '{field_name}' must be a list of strings.")

    result: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise ValueError(
                f"Task card field '{field_name}' must contain only non-empty strings."
            )
        result.append(item)

    return result


def _coerce_metrics_filenames(value: Any) -> tuple[str, ...]:
    """Coerce optional metrics filename overrides."""

    if value in ({}, None):
        return ("metrics.json", "metrics.yaml", "metrics.yml", "metrics.txt")

    if not isinstance(value, list) or not value:
        raise ValueError(
            "Task card field 'adapter.metrics_filenames' must be a non-empty list of strings."
        )

    filenames: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise ValueError(
                "Task card field 'adapter.metrics_filenames' must contain only non-empty strings."
            )
        filenames.append(item)

    return tuple(filenames)


def _validate_optional_string_mapping(value: Any, *, field_name: str) -> tuple[bool, str]:
    """Validate an optional string-to-string mapping."""

    try:
        _coerce_string_mapping(value, field_name=field_name)
    except ValueError as exc:
        return False, str(exc)
    return True, "ok"


def _validate_optional_string_list(value: Any, *, field_name: str) -> tuple[bool, str]:
    """Validate an optional list of strings."""

    try:
        _coerce_string_list(value, field_name=field_name)
    except ValueError as exc:
        return False, str(exc)
    return True, "ok"
