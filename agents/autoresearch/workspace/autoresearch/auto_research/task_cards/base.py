"""Task card schema placeholders."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class TaskCard:
    """Declarative description of how to optimize an external training task."""

    name: str
    adapter: str
    entrypoint: str
    search_space: dict[str, Any] = field(default_factory=dict)
    metric_rules: dict[str, Any] = field(default_factory=dict)
    scoring: dict[str, Any] = field(default_factory=dict)
