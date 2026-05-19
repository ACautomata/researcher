"""Simple baseline model."""

from __future__ import annotations

import torch
from torch import nn


class BaselineModel(nn.Module):
    """A tiny MLP classifier for dummy validation."""

    def __init__(self, input_dim: int = 32, hidden_dim: int = 64, num_classes: int = 4):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, num_classes),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)
