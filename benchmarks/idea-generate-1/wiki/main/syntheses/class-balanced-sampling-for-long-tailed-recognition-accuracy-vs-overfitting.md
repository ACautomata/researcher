---
pageType: synthesis
id: synthesis.class-balanced-sampling-for-long-tailed-recognition-accuracy-vs-overfitting
title: "Class-Balanced Sampling for Long-Tailed Recognition: Accuracy vs Overfitting"
sourceIds:
  - arxiv:2026.00002
status: active
updatedAt: 2026-06-15T12:29:32.363Z
---

# Class-Balanced Sampling for Long-Tailed Recognition: Accuracy vs Overfitting

## Notes
<!-- openclaw:human:start -->
<!-- openclaw:human:end -->

## Summary
<!-- openclaw:wiki:generated:start -->
## 摘要

Class-balanced (CB) sampling reweights the training distribution so each class is drawn with equal probability, improving minority-class accuracy on long-tailed benchmarks. On CIFAR-10-LT (imbalance ratio 100), CB sampling raises minority-class accuracy from 31.4% to 64.8% but increases majority-class overfitting risk: training accuracy on majority classes reaches 99.7% while validation plateaus at 72.5%, a 27-point generalization gap. The paper analyzes the trade-off between minority recall and majority overfitting under a fixed model budget.

## 方法

- **采样器**：per-batch class-balanced sampling，每个类别等概率抽取
- **有效数量重加权**：beta=0.9999 effective-number weights
- **模型**：ResNet-32，200 epochs，SGD momentum 0.9，weight decay 5e-4

## 实验

- **数据集**：CIFAR-10-LT，imbalance ratio 100
- **基线**：instance-balanced sampling，square-root sampling
- **指标**：balanced accuracy、minority-class accuracy、majority generalization gap

## 结果

| 指标 | CB Sampling | Instance-Balanced |
|------|-------------|-------------------|
| Balanced accuracy | 65.2% | 62.1% |
| Minority-class accuracy | 64.8% | 31.4% |
| Majority-class training accuracy | 99.7% | — |
| Majority-class validation accuracy | 72.5% | — |
| Majority generalization gap | 27.2 points | — |

- 每类训练样本数：head 5000，tail 50

## 局限性

Majority-class overfitting 是主要失败模式。minority 类提升的代价是 majority 类泛化能力下降。该方法假设固定模型架构，未解决 tail 类别的表示崩溃问题。

## 可复用结论

- CB sampling 在 CIFAR-LT 上将 minority-class accuracy 提升约一倍（31.4% → 64.8%）
- CB sampling 引入约 27 点的 majority-class train/val 泛化差距

## 开放问题

- 能否通过少量 class-balanced 合成样本（来自 dataset distillation）在不引发 majority overfitting 的前提下获得 minority 提升？
- 在每个类中混合 distilled + balanced 样本是否可缓解 overfitting 风险？

## 文献信息

- **标题**：Class-Balanced Sampling for Long-Tailed Recognition: Accuracy vs Overfitting
- **作者**：Bench Author
- **年份**：2026
- **会议/期刊**：Bench Workshop
- **arXiv**：2026.00002
- **证据等级**：medium（摘要级）
<!-- openclaw:wiki:generated:end -->

## Related
<!-- openclaw:wiki:related:start -->
- No related pages yet.
<!-- openclaw:wiki:related:end -->
