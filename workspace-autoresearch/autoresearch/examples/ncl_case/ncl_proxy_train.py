"""NCL-style proxy trainer for AutoResearch case validation.

The CVPR 2022 NCL paper evaluates long-tailed recognition with multi-expert
collaborative learning, hard category mining, and optional self-supervised
feature enhancement. This script preserves that experimental shape while
replacing expensive PyTorch training with deterministic metric generation.
It is intended to validate AutoResearch orchestration, not NCL accuracy.
"""

from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="NCL CIFAR100-LT proxy experiment.")
    parser.add_argument("--dataset", default="cifar100_lt")
    parser.add_argument("--imbalance-factor", type=int, default=100)
    parser.add_argument("--num-experts", type=int, required=True)
    parser.add_argument("--base-lr", type=float, required=True)
    parser.add_argument("--weight-decay", type=float, required=True)
    parser.add_argument("--batch-size", type=int, required=True)
    parser.add_argument("--diversity-factor", type=float, required=True)
    parser.add_argument("--hcm-ratio", type=float, required=True)
    parser.add_argument("--contrastive-ratio", type=float, required=True)
    parser.add_argument("--epochs", type=int, default=12)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--trial-id", default="trial_unknown")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    time.sleep(min(args.epochs, 5) * 0.02)

    lr_score = _log_closeness(args.base_lr, target=0.1, width=0.75)
    wd_score = _log_closeness(args.weight_decay, target=5e-4, width=0.8)
    diversity_score = _linear_closeness(args.diversity_factor, target=0.6, width=0.55)
    hcm_score = _linear_closeness(args.hcm_ratio, target=1.0, width=0.8)
    contrast_score = _linear_closeness(args.contrastive_ratio, target=0.4, width=0.8)
    expert_score = {2: 0.82, 3: 1.0, 4: 0.94}.get(args.num_experts, 0.78)
    batch_score = {64: 1.0, 128: 0.93, 32: 0.9}.get(args.batch_size, 0.88)

    accuracy = (
        38.5
        + 4.2 * diversity_score
        + 3.4 * hcm_score
        + 1.6 * contrast_score
        + 3.8 * lr_score
        + 1.4 * wd_score
        + 1.0 * batch_score
        + 2.5 * expert_score
    )
    many_acc = accuracy + 6.3 - 1.3 * args.contrastive_ratio
    medium_acc = accuracy + 1.2 + 1.4 * hcm_score
    few_acc = accuracy - 7.0 + 3.2 * diversity_score + 2.2 * contrast_score
    loss = 2.1 - accuracy / 100.0 + 0.18 * (1.0 - lr_score) + 0.1 * (1.0 - diversity_score)

    metrics = {
        "accuracy": round(accuracy, 4),
        "many_acc": round(many_acc, 4),
        "medium_acc": round(medium_acc, 4),
        "few_acc": round(few_acc, 4),
        "loss": round(max(0.2, loss), 6),
        "dataset": args.dataset,
        "imbalance_factor": args.imbalance_factor,
    }

    (output_dir / "metrics.json").write_text(
        json.dumps(metrics, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    print(f"trial_id: {args.trial_id}")
    print(f"dataset: {args.dataset}")
    print(f"imbalance_factor: {args.imbalance_factor}")
    print(f"accuracy: {metrics['accuracy']}")
    print(f"many_acc: {metrics['many_acc']}")
    print(f"medium_acc: {metrics['medium_acc']}")
    print(f"few_acc: {metrics['few_acc']}")
    print(f"loss: {metrics['loss']}")
    return 0


def _linear_closeness(value: float, *, target: float, width: float) -> float:
    return max(0.0, 1.0 - abs(value - target) / width)


def _log_closeness(value: float, *, target: float, width: float) -> float:
    if value <= 0.0 or target <= 0.0:
        return 0.0
    return max(0.0, 1.0 - abs(math.log10(value) - math.log10(target)) / width)


if __name__ == "__main__":
    raise SystemExit(main())
