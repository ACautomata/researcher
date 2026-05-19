"""Loss factory."""

from __future__ import annotations

from torch import nn


def build_losses(config: dict) -> list[tuple[str, float, nn.Module]]:
    """Build configured losses."""

    configured = config.get("losses") or [{"name": "cross_entropy", "weight": 1.0}]
    losses: list[tuple[str, float, nn.Module]] = []
    for item in configured:
        if item.get("name") == "cross_entropy":
            losses.append(("cross_entropy", float(item.get("weight", 1.0)), nn.CrossEntropyLoss()))
    if not losses:
        losses.append(("cross_entropy", 1.0, nn.CrossEntropyLoss()))
    return losses
