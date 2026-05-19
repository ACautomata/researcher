"""Training entry for generated RGB-IR projects."""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml

from datasets.dummy_dataset import DummyDataset
from losses.build import build_losses
from models.build import build_model
from trainers.trainer import Trainer


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/config.yaml")
    parser.add_argument("--max-steps", type=int, default=None)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    config = yaml.safe_load(Path(args.config).read_text(encoding="utf-8")) or {}
    if args.dry_run:
        DummyDataset()
        build_model(config)
        build_losses(config)
        print("dry-run ok")
        return
    metrics = Trainer(config, max_steps=args.max_steps).train()
    print(metrics)


if __name__ == "__main__":
    main()
