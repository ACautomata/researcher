---
title: Accuracy (Top-1 / Top-5)
type: metric
domain: meta
status: active
created: 2026-05-24
updated: 2026-05-24
tags:
  - classification
  - evaluation
  - standard
source_pages:
  - wiki/domains/distillation/papers/rethinking-long-tailed-dataset-distillation.md
  - wiki/domains/distillation/papers/fair-dataset-distillation-cobra.md
  - wiki/domains/federated-learning/papers/fedhd-federated-distillation-whole-slide-image.md
related_pages:
  - wiki/domains/distillation/methods/rldd.md
  - wiki/domains/distillation/methods/cobra.md
  - wiki/domains/outofdistributiondetection/methods/lsn.md
---

# Accuracy（分类准确率）

## 定义

Top-1 Accuracy = 正确分类的样本数 / 总样本数。Top-5 Accuracy = 真实标签在 top-5 预测中的样本数 / 总样本数。wiki 中使用 Accuracy 作为评估指标的论文超过 9 篇，是最广泛的跨域共享指标。

## 解读

- **高 Accuracy**：模型在整体测试分布上表现好——但掩盖了类别级和群体级性能差异。
- **在蒸馏中**：通常与压缩比（IPC）、不平衡因子（IF）一起报告，用于评估 budget-efficacy trade-off。
- **在公平性中**：必须与 EOD 等公平性指标联合报告——单独 Accuracy 无法检测子群体偏差。

## 失效模式

- **类别不平衡**：Accuracy 对 tail class 性能不敏感，head class 主导整体数值。
- **子群体偏差**：多数群体的高准确率可以掩盖少数群体的极低准确率（COBRA 的核心 motivation）。
- **评估分布偏移**：当测试分布与训练分布不一致时，Accuracy 可能给出虚假的安全感。
- **标签噪声**：错误标签直接污染 Accuracy 的参考基准。

## 使用者

| 论文 | 设置 | 典型值 |
|------|------|--------|
| RLDD | CIFAR-100-LT (IPC=10) | 47.1% |
| COBRA | CIFAR10-S (DM, IPC=10) | 44.5% (EOD 20.18) |
| FedHD | CAMELYON16 (异构) | 91.2% |
| FedSD2C | Tiny-ImageNet (ResNet-18) | 26.83% |
| CoRD | AIME24 (Pass@1) | 79.6% |
| PALCAS | 60% CAV DSR | 93.97% |
| LSN | ImageNet-100 (CoCoOp+LSN) | 97.64% (AUROC) |

## 关联

- [Equalized Odds Difference](../../distillation/metrics/equalized-odds.md)：Accuracy 的公平性补充——联合报告才能完整评估。
- [AUROC](../outofdistributiondetection/metrics/auroc.md)：OOD 检测中的 Accuracy 等价物。
- RLDD、COBRA、FedHD、FedSD2C 中均为主要或次要指标。

## 开放问题

- 在极端长尾和多群体场景下，是否需要 weighted accuracy 或 group-balanced accuracy 替代标准 Accuracy？
