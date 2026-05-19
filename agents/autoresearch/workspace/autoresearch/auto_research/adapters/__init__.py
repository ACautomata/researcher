"""Adapter interfaces for external training projects."""

from __future__ import annotations

from auto_research.adapters.base import TrainingAdapter
from auto_research.adapters.pytorch_argparse_adapter import PyTorchArgparseAdapter
from auto_research.adapters.pytorch_yaml_adapter import PyTorchYamlAdapter
from auto_research.adapters.subprocess_adapter import SubprocessAdapter

__all__ = [
    "TrainingAdapter",
    "SubprocessAdapter",
    "PyTorchYamlAdapter",
    "PyTorchArgparseAdapter",
]
