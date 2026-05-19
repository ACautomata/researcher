"""Loss factory with placeholder metric-learning losses."""

from __future__ import annotations

import torch
from torch import nn


class TripletPlaceholderLoss(nn.Module):
    """A differentiable placeholder for triplet supervision."""

    def forward(self, embeddings: torch.Tensor, labels: torch.Tensor) -> torch.Tensor:
        return embeddings.pow(2).mean() * 0.001


class CenterConstraintPlaceholderLoss(nn.Module):
    """A simple feature compactness constraint."""

    def forward(self, embeddings: torch.Tensor, labels: torch.Tensor) -> torch.Tensor:
        center = embeddings.mean(dim=0, keepdim=True)
        return ((embeddings - center) ** 2).mean()


def build_losses(config: dict) -> list[tuple[str, float, nn.Module]]:
    """Build configured losses."""

    configured = config.get("losses") or [{"name": "cross_entropy", "weight": 1.0}]
    losses: list[tuple[str, float, nn.Module]] = []
    for item in configured:
        name = item.get("name")
        weight = float(item.get("weight", 1.0))
        if name == "cross_entropy":
            losses.append((name, weight, nn.CrossEntropyLoss()))
        elif name == "triplet":
            losses.append((name, weight, TripletPlaceholderLoss()))
        elif name == "center_constraint":
            losses.append((name, weight, CenterConstraintPlaceholderLoss()))
    if not losses:
        losses.append(("cross_entropy", 1.0, nn.CrossEntropyLoss()))
    return losses
