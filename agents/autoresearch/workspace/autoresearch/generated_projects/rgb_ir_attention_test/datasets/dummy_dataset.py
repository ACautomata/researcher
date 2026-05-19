"""Dummy RGB-IR person re-identification dataset."""

from __future__ import annotations

import torch
from torch.utils.data import Dataset


class DummyDataset(Dataset):
    """Return paired RGB/IR tensors and identity labels."""

    def __init__(self, length: int = 64, num_classes: int = 4):
        self.length = length
        self.num_classes = num_classes

    def __len__(self) -> int:
        return self.length

    def __getitem__(self, index: int) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        generator = torch.Generator().manual_seed(index)
        rgb = torch.randn(3, 32, 16, generator=generator)
        ir = torch.randn(3, 32, 16, generator=generator)
        label = torch.tensor(index % self.num_classes, dtype=torch.long)
        return rgb, ir, label
