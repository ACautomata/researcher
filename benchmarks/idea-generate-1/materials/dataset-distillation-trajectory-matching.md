---
title: "Trajectory Matching for Dataset Distillation on Long-Tailed Recognition"
authors: ["Bench Author"]
year: 2026
venue: "Bench Workshop"
arxiv: "2026.00001"
---

# Trajectory Matching for Dataset Distillation on Long-Tailed Recognition

## Abstract

We study dataset distillation via trajectory matching (TM) under long-tailed
class distributions. TM synthesizes a small image set by matching the parameter
trajectory of a network trained on the synthetic set to one trained on the full
data. On a CIFAR-10-LT (imbalance ratio 100) split, the synthetic set (1 img/cls
for head, 1 img/cls for tail) recovers 62.1% balanced accuracy for the full data,
but minority-class accuracy drops to 31.4% versus 71.2% on majority classes. We
attribute the gap to trajectory matching over-fitting head-class dynamics.

## Method

- Core: trajectory matching. A teacher network is trained on the real set; its
  per-step weights form a trajectory. A student trained on the synthetic set is
  optimized so its trajectory matches the teacher's via an L2 loss on weights.
- Synthetic budget: 10 images per class on CIFAR-10-LT (imbalance ratio 100).
- Optimizer: SGD, momentum 0.9, 200 outer steps, 50 inner steps.

## Experiments

- Dataset: CIFAR-10-LT, imbalance ratio 100 (head class 5000 imgs, tail 50 imgs).
- Baselines: random sampling, herding, K-Center.
- Metric: balanced accuracy, per-class accuracy (majority vs minority).

## Results

- Balanced accuracy: 62.1% (TM) vs 58.4% (random), 60.0% (herding).
- Majority-class accuracy: 71.2%.
- Minority-class accuracy: 31.4% (clear weakness).
- Distillation budget: 10 synthetic images per class; total synthesis cost ~4 GPU-hours.

## Limitations

Minority-class accuracy is the bottleneck. The synthetic minority images are
insufficient to reproduce tail-class decision boundaries. No class-aware weighting
is applied during matching.

## Reusable Claims

- TM recovers balanced accuracy within ~4 points of full-data training on CIFAR-LT.
- TM's minority-class accuracy is ~40 points below its majority-class accuracy.

## Open Questions

- Does class-aware reweighting of the trajectory loss improve minority accuracy?
- Would a class-balanced synthetic budget (more imgs/cls for tail) help within a fixed total budget?
