"""Core abstractions for AutoResearch."""

from __future__ import annotations

__all__ = [
    "ExperimentResult",
    "MetricsDict",
    "TrialRecord",
    "TrialStatus",
    "TrialRecorder",
    "create_objective",
    "create_adapter_from_task_card",
    "load_task_card",
    "validate_task_card",
]


def __getattr__(name: str):
    """Lazily resolve public core exports to avoid import cycles."""

    if name in {"ExperimentResult", "MetricsDict", "TrialRecord", "TrialStatus"}:
        from auto_research.core.types import (
            ExperimentResult,
            MetricsDict,
            TrialRecord,
            TrialStatus,
        )

        mapping = {
            "ExperimentResult": ExperimentResult,
            "MetricsDict": MetricsDict,
            "TrialRecord": TrialRecord,
            "TrialStatus": TrialStatus,
        }
        return mapping[name]

    if name in {"create_adapter_from_task_card", "load_task_card", "validate_task_card"}:
        from auto_research.core.task_card import (
            create_adapter_from_task_card,
            load_task_card,
            validate_task_card,
        )

        mapping = {
            "create_adapter_from_task_card": create_adapter_from_task_card,
            "load_task_card": load_task_card,
            "validate_task_card": validate_task_card,
        }
        return mapping[name]

    if name == "create_objective":
        from auto_research.core.objective import create_objective

        return create_objective

    if name == "TrialRecorder":
        from auto_research.core.recorder import TrialRecorder

        return TrialRecorder

    raise AttributeError(f"module 'auto_research.core' has no attribute {name!r}")
