"""Foundational typed placeholders for the core package."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class RunContext:
    """Minimal execution context placeholder for a single optimization trial."""

    trial_id: str
    task_name: str
    parameters: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class RunResult:
    """Normalized result placeholder returned by an adapter or evaluator."""

    score: float
    metrics: dict[str, float] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
