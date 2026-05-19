"""Read and write Research Task Specification files."""

from __future__ import annotations

from dataclasses import asdict, fields, is_dataclass
import json
from pathlib import Path
from typing import Any, TypeVar

import yaml

from auto_research.rts.schema import (
    RTSAdapter,
    RTSBaseline,
    RTSGoal,
    RTSImplementation,
    RTSInput,
    RTSMeta,
    RTSModel,
    RTSOutput,
    RTSTask,
    RTSTraining,
    RTSValidation,
    ResearchTaskSpecification,
)
from auto_research.utils.yaml import load_yaml

_T = TypeVar("_T")

_SECTION_TYPES: dict[str, type[Any]] = {
    "meta": RTSMeta,
    "task": RTSTask,
    "goal": RTSGoal,
    "input": RTSInput,
    "output": RTSOutput,
    "baseline": RTSBaseline,
    "model": RTSModel,
    "training": RTSTraining,
    "implementation": RTSImplementation,
    "validation": RTSValidation,
    "adapter": RTSAdapter,
}


def load_rts(path: str | Path) -> ResearchTaskSpecification:
    """Load an RTS document from a YAML or JSON file."""

    rts_path = Path(path)
    if not rts_path.exists():
        raise FileNotFoundError(f"RTS file does not exist: '{rts_path}'.")
    if not rts_path.is_file():
        raise FileNotFoundError(f"RTS path is not a file: '{rts_path}'.")

    suffix = rts_path.suffix.lower()
    if suffix in {".yaml", ".yml"}:
        data = load_yaml(rts_path)
    elif suffix == ".json":
        with rts_path.open("r", encoding="utf-8") as handle:
            loaded = json.load(handle)
        if not isinstance(loaded, dict):
            raise ValueError(f"RTS JSON at '{rts_path}' must contain an object.")
        data = loaded
    else:
        raise ValueError("RTS files must use a .yaml, .yml, or .json suffix.")

    return rts_from_dict(data)


def save_rts(rts: ResearchTaskSpecification, path: str | Path) -> None:
    """Save an RTS document to YAML or JSON, creating parent directories as needed."""

    rts_path = Path(path)
    rts_path.parent.mkdir(parents=True, exist_ok=True)
    data = rts_to_dict(rts)

    suffix = rts_path.suffix.lower()
    if suffix in {".yaml", ".yml"}:
        with rts_path.open("w", encoding="utf-8") as handle:
            yaml.safe_dump(data, handle, sort_keys=False, allow_unicode=True)
    elif suffix == ".json":
        with rts_path.open("w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
    else:
        raise ValueError("RTS files must use a .yaml, .yml, or .json suffix.")


def rts_to_dict(rts: ResearchTaskSpecification) -> dict[str, Any]:
    """Convert an RTS dataclass object to a plain dictionary."""

    if not isinstance(rts, ResearchTaskSpecification):
        raise TypeError("rts_to_dict expects a ResearchTaskSpecification instance.")
    return asdict(rts)


def rts_from_dict(data: dict[str, Any]) -> ResearchTaskSpecification:
    """Build an RTS object from a plain dictionary."""

    if not isinstance(data, dict):
        raise TypeError("RTS data must be a dictionary.")

    kwargs: dict[str, Any] = {}
    for key, value in data.items():
        section_type = _SECTION_TYPES.get(key)
        if section_type is not None:
            kwargs[key] = _coerce_dataclass(section_type, value, field_name=key)
        else:
            kwargs[key] = value

    return ResearchTaskSpecification(**kwargs)


def _coerce_dataclass(cls: type[_T], value: Any, *, field_name: str) -> _T:
    """Create a dataclass section from mapping data with clear errors."""

    if is_dataclass(value):
        return value
    if value is None:
        return cls()
    if not isinstance(value, dict):
        raise TypeError(f"RTS section '{field_name}' must be a mapping.")

    allowed_fields = {item.name for item in fields(cls)}
    filtered = {key: item for key, item in value.items() if key in allowed_fields}
    return cls(**filtered)
