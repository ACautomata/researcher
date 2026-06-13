---
title: Equalized Odds Difference (EOD)
type: metric
domain: distillation
status: active
created: 2026-05-24
updated: 2026-05-24
tags:
  - fairness
  - group-bias
  - classification
source_pages:
  - wiki/domains/distillation/papers/fair-dataset-distillation-cobra.md
related_pages:
  - wiki/domains/distillation/methods/cobra.md
  - wiki/domains/meta/metrics/accuracy.md
---

# Equalized Odds Difference (EOD)

## 定义

Equalized Odds Difference (EOD) 衡量分类器在不同子群体上的预测公平性。EOD ↓（越低越好，0% 为完美公平）：

$$EOD = \max_{a,a' \in A, y \in Y} |P(\hat{Y}=y | A=a, Y=y) - P(\hat{Y}=y | A=a', Y=y)|$$

其中 A 为敏感属性（如种族、性别），Y 为真实标签，$\hat{Y}$ 为预测标签。COBRA 同时报告 EODM（max over groups）和 EODA（mean over groups）。

## 解读

- **EOD = 0%**：完美公平——所有群体在各类别上的 TPR 和 FPR 完全相同。
- **EOD 越高**：越不公平——多数群体享受远高于少数群体的正确分类率。
- **EOD 与 Accuracy 的关系**：理想情况是 EOD ↓ + Acc ↑（COBRA 在多数设置下实现），但存在 trade-off（MTT-BFFHQ: EOD -23.84% 但 Acc -9.78%）。
- 在数据集蒸馏中，EOD 衡量**合成数据训练出的模型**的公平性——而非原始数据的公平性。

## 失效模式

- **对群体标签依赖**：需要敏感属性标注，完全无标签场景无法计算。
- **仅评估群体间差异**：不反映个体级公平性（individual fairness）。
- **多敏感属性交互**：EOD 通常针对单属性计算——race × gender 的交叉群体公平性可能被掩盖。
- **小群体不敏感**：极小的少数群体即使 EOD 恶化，对数值影响也有限——需结合最差群体准确率。
- **评估分布**：COBRA 的测试集是 group-balanced——若实际部署分布不平衡，EOD 的参考价值有限。

## 使用者

| 论文 | 数据集 | Vanilla | COBRA | 降幅 |
|------|--------|---------|-------|------|
| COBRA | CIFAR10-S (DM) | 56.25 | 20.18 | -36.07 |
| COBRA | C-MNIST (FG) | 100.00 | 6.71 | -93.29 |
| COBRA | C-MNIST (BG) | 100.00 | 7.04 | -92.96 |
| COBRA | C-FMNIST (FG) | 99.20 | 15.93 | -83.27 |
| COBRA | BFFHQ (DM) | 44.80 | 15.73 | -29.07 |
| COBRA | UTKFace | 35.53 | 20.78 | -14.75 |

## 关联

- [Accuracy](../../meta/metrics/accuracy.md)：必须联合报告——EOD 单独无法反映整体性能。
- [COBRA](../methods/cobra.md)：wiki 中 EOD 的主要使用者，7 个 benchmark 上系统验证。
- FairDD (NeurIPS 2025)：使用相同 metric 的直接 baseline。

## 开放问题

- 如何设计不依赖群体标签的公平性评估（与 EOD 互补）？
- 多敏感属性交互（intersectional fairness）的评估协议？
- EOD 在非分类任务（回归、检索、生成）中的对应 metric？
