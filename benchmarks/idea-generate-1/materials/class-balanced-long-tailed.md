---
title: "Class-Balanced Sampling for Long-Tailed Recognition: Accuracy vs Overfitting"
authors: ["Bench Author"]
year: 2026
venue: "Bench Workshop"
arxiv: "2026.00002"
---

# Class-Balanced Sampling for Long-Tailed Recognition

## Abstract

Class-balanced (CB) sampling reweights the training distribution so each class
is drawn with equal probability, improving minority-class accuracy on long-tailed
benchmarks. On CIFAR-10-LT (imbalance ratio 100), CB sampling raises minority-class
accuracy from 31.4% to 64.8% but increases majority-class overfitting risk:
training accuracy on majority classes reaches 99.7% while validation plateaus at
72.5%, a 27-point generalization gap. We analyze the trade-off between minority
recall and majority overfitting under a fixed model budget.

## Method

- Sampler: per-batch class-balanced sampling (each class drawn uniformly).
- Effective number reweighting: beta=0.9999 effective-number weights.
- Model: ResNet-32, 200 epochs, SGD momentum 0.9, weight decay 5e-4.

## Experiments

- Dataset: CIFAR-10-LT, imbalance ratio 100.
- Baselines: instance-balanced sampling, square-root sampling.
- Metric: balanced accuracy, minority-class accuracy, majority generalization gap.

## Results

- Balanced accuracy: 65.2% (CB) vs 62.1% (instance-balanced).
- Minority-class accuracy: 64.8% (CB) vs 31.4% (instance).
- Majority-class training accuracy: 99.7%.
- Majority-class validation accuracy: 72.5% (overfitting gap = 27.2 points).
- Samples per class (training): head 5000, tail 50.

## Limitations

Majority-class overfitting is the dominant failure mode. Minority gains come at
the cost of majority generalization. The method assumes a fixed architecture and
does not address representation collapse on tail classes.

## Reusable Claims

- CB sampling roughly doubles minority-class accuracy on CIFAR-LT.
- CB sampling induces a ~27-point majority-class train/val gap.

## Open Questions

- Can a small class-balanced synthetic set (from dataset distillation) deliver
  minority gains without majority overfitting?
- Is the overfitting risk mitigated by mixing distilled + balanced samples per class?
