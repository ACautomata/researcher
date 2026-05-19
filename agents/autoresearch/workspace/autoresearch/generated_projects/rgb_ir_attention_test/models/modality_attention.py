"""Generic generated model component placeholder."""

from __future__ import annotations

import torch
from torch import nn


class GenericComponent(nn.Module):
    """A minimal learnable component that preserves tensor shape."""

    def __init__(self, feature_dim: int = 128):
        super().__init__()
        self.proj = nn.Linear(feature_dim, feature_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return torch.relu(self.proj(x))
