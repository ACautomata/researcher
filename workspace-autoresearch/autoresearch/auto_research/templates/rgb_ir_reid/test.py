"""Smoke test entry for generated RGB-IR projects."""

from __future__ import annotations

import argparse
from pathlib import Path

import torch
import yaml

from models.build import build_model


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/config.yaml")
    parser.add_argument("--mode", default="dummy-forward")
    args = parser.parse_args()
    config = yaml.safe_load(Path(args.config).read_text(encoding="utf-8")) or {}
    if args.mode != "dummy-forward":
        raise SystemExit(f"Unsupported test mode: {args.mode}")
    model = build_model(config)
    model.eval()
    with torch.no_grad():
        outputs = model(torch.randn(2, 3, 32, 16), torch.randn(2, 3, 32, 16))
    print(
        {
            "dummy_forward": True,
            "embedding_shape": list(outputs["embedding"].shape),
            "logits_shape": list(outputs["logits"].shape),
        }
    )
