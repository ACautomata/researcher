"""Baseline template selection for implementation planning."""

from __future__ import annotations

from typing import Any

from auto_research.rts.schema import ResearchTaskSpecification

DEFAULT_TEMPLATE_NAMES = [
    "general_pytorch",
    "image_classification",
    "object_detection",
    "semantic_segmentation",
    "pose_estimation",
    "person_reid",
    "rgb_ir_reid",
    "shadow_removal",
    "diffusion_restoration",
]


class BaselineSelector:
    """Select the best baseline template from RTS hints and task type."""

    def __init__(self, template_names: list[str] | None = None):
        """Initialize the selector with an optional supported template list."""

        self.template_names = template_names or list(DEFAULT_TEMPLATE_NAMES)
        self._template_set = set(self.template_names)

    def select(self, rts: ResearchTaskSpecification) -> dict[str, Any]:
        """Select a baseline template for an RTS object."""

        warnings: list[str] = []
        fallback_template = "general_pytorch"
        task_type = rts.task.type
        baseline_template = rts.baseline.template

        if _has_text(baseline_template):
            selected = str(baseline_template)
            if selected not in self._template_set:
                warnings.append(
                    f"Baseline template '{selected}' is not in the supported template list."
                )
            if _has_text(task_type) and task_type in self._template_set and selected != task_type:
                warnings.append(
                    f"task.type '{task_type}' conflicts with baseline.template '{selected}'."
                )
            return {
                "selected_template": selected,
                "fallback_template": fallback_template,
                "reason": "RTS baseline.template is explicitly provided.",
                "warnings": warnings,
            }

        if _has_text(task_type) and task_type in self._template_set:
            return {
                "selected_template": str(task_type),
                "fallback_template": fallback_template,
                "reason": "Selected template by matching RTS task.type.",
                "warnings": warnings,
            }

        warnings.append(
            "No explicit baseline template or recognized task.type was provided; "
            "falling back to general_pytorch."
        )
        return {
            "selected_template": fallback_template,
            "fallback_template": fallback_template,
            "reason": "Fallback template selected because the task is not recognized.",
            "warnings": warnings,
        }


def _has_text(value: Any) -> bool:
    """Return True when value is a non-empty string."""

    return isinstance(value, str) and bool(value.strip())
