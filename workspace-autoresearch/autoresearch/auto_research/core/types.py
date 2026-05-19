"""Common type definitions shared across the AutoResearch core."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, TypeAlias

MetricsDict: TypeAlias = dict[str, float]


class TrialStatus(str, Enum):
    """Lifecycle states for a training trial."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"
    INVALID = "invalid"


@dataclass(slots=True)
class ExperimentResult:
    """Normalized result produced by one executed training experiment."""

    status: TrialStatus
    metrics: MetricsDict = field(default_factory=dict)
    score: float | None = None
    message: str = ""
    trial_dir: str | None = None
    command: list[str] = field(default_factory=list)
    return_code: int | None = None
    duration_seconds: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class TrialRecord:
    """Record describing one optimization trial from sampling to completion."""

    trial_id: str
    status: TrialStatus = TrialStatus.PENDING
    sampled_config: dict[str, Any] = field(default_factory=dict)
    prepared_config: dict[str, Any] = field(default_factory=dict)
    result: ExperimentResult | None = None
    notes: str = ""
