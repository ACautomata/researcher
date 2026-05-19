"""Dummy tensor classification dataset."""

from __future__ import annotations

import torch
from torch.utils.data import Dataset


class DummyDataset(Dataset):
    """Return random tensors and class labels."""

    def __init__(self, length: int = 64, input_dim: int = 32, num_classes: int = 4):
        self.length = length
        self.input_dim = input_dim
        self.num_classes = num_classes

    def __len__(self) -> int:
        return self.length

    def __getitem__(self, index: int) -> tuple[torch.Tensor, torch.Tensor]:
        generator = torch.Generator().manual_seed(index)
        x = torch.randn(self.input_dim, generator=generator)
        y = torch.tensor(index % self.num_classes, dtype=torch.long)
        return x, y
