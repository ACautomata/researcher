"""Simplified center constraint loss."""

from __future__ import annotations

import torch
from torch import nn


class CenterConstraintLoss(nn.Module):
    """A small center-style feature compactness loss."""

    def __init__(self):
        super().__init__()

    def forward(self, embeddings: torch.Tensor, labels: torch.Tensor | None = None) -> torch.Tensor:
        center = embeddings.mean(dim=0, keepdim=True)
        return ((embeddings - center) ** 2).mean()
