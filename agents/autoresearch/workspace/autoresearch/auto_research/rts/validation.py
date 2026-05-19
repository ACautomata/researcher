"""Validation helpers for Research Task Specification documents."""

from __future__ import annotations

from typing import Any

from auto_research.rts.schema import ResearchTaskSpecification

_SOURCE_TYPES = {"idea", "paper", "manual"}
_OPTIMIZATION_DIRECTIONS = {"maximize", "minimize"}
_ADAPTER_TYPES = {"pytorch_argparse", "pytorch_yaml", "subprocess"}


class RTSValidator:
    """Validate RTS objects before generation or training handoff."""

    def validate(self, rts: ResearchTaskSpecification) -> dict[str, Any]:
        """Validate an RTS object and return pass status, errors, and warnings."""

        errors: list[str] = []
        warnings: list[str] = []

        if not isinstance(rts, ResearchTaskSpecification):
            return {
                "passed": False,
                "errors": ["Expected a ResearchTaskSpecification instance."],
                "warnings": [],
            }

        if not _has_text(rts.meta.project_name):
            errors.append("meta.project_name must be a non-empty string.")

        if rts.meta.source_type not in _SOURCE_TYPES:
            errors.append(
                "meta.source_type must be one of: idea, paper, manual."
            )

        if not _has_text(rts.task.type):
            errors.append("task.type must be a non-empty string.")

        if not _has_text(rts.task.research_problem):
            errors.append("task.research_problem must be a non-empty string.")

        if not _has_text(rts.goal.primary_metric):
            errors.append("goal.primary_metric must be a non-empty string.")

        if rts.goal.optimization_direction not in _OPTIMIZATION_DIRECTIONS:
            errors.append("goal.optimization_direction must be either maximize or minimize.")

        if not rts.input.modalities:
            errors.append("input.modalities must contain at least one modality.")

        if not _has_text(rts.output.type):
            errors.append("output.type must be a non-empty string.")

        errors.extend(_validate_search_space(rts.search_space))

        if not rts.validation.required_checks:
            errors.append("validation.required_checks must contain at least one check.")

        adapter_type = rts.adapter.type
        if adapter_type and adapter_type not in _ADAPTER_TYPES:
            errors.append(
                "adapter.type must be one of: pytorch_argparse, pytorch_yaml, subprocess."
            )

        if not adapter_type:
            warnings.append(
                "adapter.type is empty; training handoff will require an adapter selection later."
            )

        return {
            "passed": not errors,
            "errors": errors,
            "warnings": warnings,
        }


def _validate_search_space(search_space: dict[str, Any]) -> list[str]:
    """Validate RTS search-space shape without binding to an HPO backend."""

    errors: list[str] = []
    if not search_space:
        return errors

    if not isinstance(search_space, dict):
        return ["search_space must be a dictionary when provided."]

    for param_name, spec in search_space.items():
        prefix = f"search_space.{param_name}"
        if not isinstance(spec, dict):
            errors.append(f"{prefix} must be a dictionary.")
            continue

        spec_type = spec.get("type")
        if not _has_text(spec_type):
            errors.append(f"{prefix}.type is required.")
            continue

        if spec_type == "categorical":
            choices = spec.get("choices")
            if not isinstance(choices, list) or not choices:
                errors.append(f"{prefix}.choices must be a non-empty list for categorical type.")
        elif spec_type in {"float", "int"}:
            if "low" not in spec or "high" not in spec:
                errors.append(f"{prefix} must define both low and high for {spec_type} type.")

    return errors


def _has_text(value: Any) -> bool:
    """Return True when a value is a non-empty string after stripping whitespace."""

    return isinstance(value, str) and bool(value.strip())
