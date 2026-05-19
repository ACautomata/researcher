"""Tiny two-stream RGB-IR baseline."""

from __future__ import annotations

import torch
from torch import nn
import torch.nn.functional as F


class BaselineModel(nn.Module):
    """A compact two-stream network producing embeddings and logits."""

    def __init__(self, embedding_dim: int = 128, num_classes: int = 4):
        super().__init__()
        flat_dim = 3 * 32 * 16
        self.rgb_encoder = nn.Sequential(nn.Flatten(), nn.Linear(flat_dim, embedding_dim), nn.ReLU())
        self.ir_encoder = nn.Sequential(nn.Flatten(), nn.Linear(flat_dim, embedding_dim), nn.ReLU())
        self.fusion = nn.Linear(embedding_dim * 2, embedding_dim)
        self.classifier = nn.Linear(embedding_dim, num_classes)

    def forward(self, rgb: torch.Tensor, ir: torch.Tensor) -> dict[str, torch.Tensor]:
        rgb_feat = self.rgb_encoder(rgb)
        ir_feat = self.ir_encoder(ir)
        embedding = F.normalize(torch.relu(self.fusion(torch.cat([rgb_feat, ir_feat], dim=1))), dim=1)
        logits = self.classifier(embedding)
        return {"embedding": embedding, "logits": logits}
