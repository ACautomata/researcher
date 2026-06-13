---
title: AUROC — Area Under the ROC Curve
type: metric
domain: outofdistributiondetection
status: active
created: 2026-05-24
updated: 2026-05-24
tags:
  - ood-detection
  - evaluation
  - threshold-free
source_pages:
  - wiki/domains/outofdistributiondetection/papers/out-of-distribution-detection-with-negative-prompts.md
  - wiki/domains/outofdistributiondetection/papers/learning-transferable-negative-prompts-ood-detection.md
related_pages:
  - wiki/domains/outofdistributiondetection/methods/lsn.md
  - wiki/domains/outofdistributiondetection/methods/negprompt.md
  - wiki/domains/outofdistributiondetection/metrics/fpr95.md
---

# AUROC — ROC 曲线下面积

## 定义

AUROC (Area Under the Receiver Operating Characteristic curve) 衡量 OOD 检测器在所有可能阈值上的整体判别能力，值为 0-100%（越高越好）。通过变化 OOD score 的阈值，计算不同阈值下的 True Positive Rate（TPR = ID 正确识别率）和 False Positive Rate（FPR = OOD 被误判为 ID 的比率），绘制 ROC 曲线并计算曲线下面积。

## 解读

- AUROC = 100%：完美的 ID/OOD 分离。
- AUROC = 50%：随机猜测水平。
- AUROC > 95%：实用的 OOD 检测能力（negprompt 方法族的目标）。
- AUROC 是 threshold-free 指标——不需要选择特定的判别阈值，反映检测器的整体排序质量。

## 失效模式

- **类别不平衡**：AUROC 对 ID 和 OOD 样本比例不敏感——当 OOD 样本极多时，高 AUROC 仍可能导致高假阳性绝对数。
- **近 OOD vs. 远 OOD**：AUROC 将不同难度的 OOD 混合评估——在 hard OOD（如 ImageNet 细类间）上高 AUROC 可能掩盖在 simple OOD 上的退化。
- **不反映 OOD score 的校准质量**：排序正确不代表 score 的绝对值有意义——两条曲线可以有相同 AUROC 但完全不同的 score 分布。
- **对 open-vocabulary 场景的敏感性**：当 ID 类别数变化时，AUROC 的 baselines 也会漂移（NegPrompt 的发现）。

## 使用者

| 方法 | 数据集 | AUROC |
|------|--------|-------|
| LSN (CoCoOp+LSN) | ImageNet-100 | 98.05% |
| LSN (CoCoOp+LSN) | ImageNet-1K | 92.96% |
| NegPrompt | ImageNet-1K 常规 OOD | 94.81% |
| NegPrompt | ImageNet-1K Hard OOD | 97.96% |
| NegPrompt | Open-vocabulary (10% ID) | 96.46% |

## 关联

- [FPR95](fpr95.md)：AUROC 的互补指标——AUROC 评估整体排序，FPR95 评估低假阳性区域的实用性能。LSN 和 NegPrompt 均同时报告两者。
- [LSN](../methods/lsn.md)、[NegPrompt](../methods/negprompt.md)：wiki 中 AUROC 的主要使用者。
- ID 分类 Accuracy：[Accuracy](../../meta/metrics/accuracy.md)——OOD 检测方法需同时保持高 AUROC 和 ID Accuracy。

## 开放问题

- 如何设计对 open-vocabulary 设定（ID 类别数动态变化）鲁棒的 AUROC 变体？
- Near-OOD vs. Far-OOD 的分离评估是否应该成为 OOD benchmark 的标准？
