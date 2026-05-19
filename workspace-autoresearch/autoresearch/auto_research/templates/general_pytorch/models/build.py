"""Model factory."""

from __future__ import annotations

from models.baseline import BaselineModel


def build_model(config: dict) -> BaselineModel:
    """Build the baseline model."""

    return BaselineModel()
