"""Small importable code snippets for generated custom modules."""

from __future__ import annotations


def model_component_snippet(name: str) -> str:
    """Return Python source for a model component."""

    if name == "cross_modal_attention":
        return _CROSS_MODAL_ATTENTION
    return _GENERIC_COMPONENT


def loss_snippet(name: str) -> str:
    """Return Python source for a loss module."""

    if name == "center_constraint":
        return _CENTER_CONSTRAINT
    if name == "contrastive":
        return _CONTRASTIVE
    return _GENERIC_LOSS


_CROSS_MODAL_ATTENTION = '''"""Simple cross-modal attention placeholder."""

from __future__ import annotations

import torch
from torch import nn


class CrossModalAttention(nn.Module):
    """Fuse two feature tensors with a small learned projection."""

    def __init__(self, feature_dim: int = 128):
        super().__init__()
        self.proj = nn.Linear(feature_dim * 2, feature_dim)

    def forward(self, rgb_feat: torch.Tensor, ir_feat: torch.Tensor) -> torch.Tensor:
        fused = torch.cat([rgb_feat, ir_feat], dim=-1)
        return torch.relu(self.proj(fused))
'''

_GENERIC_COMPONENT = '''"""Generic generated model component placeholder."""

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
'''

_CENTER_CONSTRAINT = '''"""Simplified center constraint loss."""

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
'''

_CONTRASTIVE = '''"""Simplified contrastive alignment loss."""

from __future__ import annotations

import torch
from torch import nn
import torch.nn.functional as F


class ContrastiveLoss(nn.Module):
    """Align two batches of features with cosine distance."""

    def __init__(self):
        super().__init__()

    def forward(self, x: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
        return (1.0 - F.cosine_similarity(x, y, dim=-1)).mean()
'''

_GENERIC_LOSS = '''"""Generic generated loss placeholder."""

from __future__ import annotations

import torch
from torch import nn


class GenericLoss(nn.Module):
    """Return a differentiable scalar for arbitrary tensor inputs."""

    def __init__(self):
        super().__init__()

    def forward(self, prediction: torch.Tensor, target: torch.Tensor | None = None) -> torch.Tensor:
        return prediction.float().mean() * 0.0 + prediction.float().pow(2).mean() * 0.001
'''
