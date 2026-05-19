"""Minimal dummy training entrypoint for AutoResearch smoke tests."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for the dummy training script."""

    parser = argparse.ArgumentParser(description="Dummy training script for AutoResearch.")
    parser.add_argument("--lr", type=float, required=True)
    parser.add_argument("--batch-size", type=int, required=True)
    parser.add_argument("--output-dir", type=str, required=True)
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--trial-id", type=str, default="trial_unknown")
    parser.add_argument("--output-root", type=str, default="")
    return parser.parse_args()


def main() -> int:
    """Simulate a tiny training run and emit deterministic metrics."""

    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for _ in range(min(args.epochs, 3)):
        time.sleep(0.02)

    lr_score = max(0.0, min(1.0, 1.0 - abs(args.lr - 3e-4) * 900.0))
    batch_score = 1.0 if args.batch_size == 64 else 0.93
    epoch_score = max(0.0, min(1.0, 1.0 - abs(args.epochs - 12) / 12.0))

    map_score = round((0.56 + 0.17 * lr_score + 0.09 * batch_score + 0.08 * epoch_score) * 100.0, 4)
    rank1_score = round(min(99.9, map_score + 7.4 - (0.4 if args.batch_size == 32 else 0.0)), 4)
    loss_score = round(max(0.05, 1.32 - map_score / 100.0 - epoch_score * 0.12), 6)

    metrics = {
        "mAP": map_score,
        "rank1": rank1_score,
        "loss": loss_score,
    }

    (output_dir / "metrics.json").write_text(
        json.dumps(metrics, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    print(f"trial_id: {args.trial_id}")
    print(f"output_root: {args.output_root}")
    print(f"epochs: {args.epochs}")
    print(f"mAP: {map_score}")
    print(f"Rank-1: {rank1_score}")
    print(f"loss: {loss_score}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
