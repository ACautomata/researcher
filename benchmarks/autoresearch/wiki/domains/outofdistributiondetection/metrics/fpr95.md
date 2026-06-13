---
title: FPR95 — False Positive Rate at 95% TPR
type: metric
domain: outofdistributiondetection
status: active
created: 2026-05-24
updated: 2026-05-24
tags:
  - ood-detection
  - evaluation
  - threshold-based
source_pages:
  - wiki/domains/outofdistributiondetection/papers/out-of-distribution-detection-with-negative-prompts.md
  - wiki/domains/outofdistributiondetection/papers/learning-transferable-negative-prompts-ood-detection.md
related_pages:
  - wiki/domains/outofdistributiondetection/methods/lsn.md
  - wiki/domains/outofdistributiondetection/methods/negprompt.md
  - wiki/domains/outofdistributiondetection/metrics/auroc.md
---

# FPR95 — 95% TPR 下的假阳性率

## 定义

FPR95 (False Positive Rate at 95% True Positive Rate) 衡量当 OOD 检测器正确识别 95% 的 ID 样本时，OOD 样本被误判为 ID 的比例（越低越好，0% 为完美）。计算方式：固定 TPR=95% 的阈值，计算该阈值下的 FPR = FP / (FP + TN)。

## 解读

- FPR95 < 10%：优秀的 OOD 检测能力（LSN ImageNet-100: 8.56%，NegPrompt ImageNet-1K: 23.01%）。
- FPR95 反映了 OOD 检测器在"几乎不丢失 ID 样本"的实用约束下的假阳性率——更贴近实际部署需求。
- 与 AUROC 互补：AUROC 评估全局排序质量，FPR95 评估高召回率区域的关键性能。

## 失效模式

- **对低 TPR 区域不敏感**：TPR=80% 时的 FPR 可能远高于 FPR95——FPR95 仅报告一个工作点。
- **依赖单一阈值**：不同的 TPR 目标（如 90% vs. 95%）可能导致完全不同的 FPR 值。
- **OOD 数据集选择偏差**：不同 OOD 测试集的 FPR95 差异巨大（ImageNet-100 OOD 远低于 ImageNet-1K OOD）。
- **ID 类数量敏感**：MCM 在 ImageNet-1K 上的 FPR95 43.55% vs. ImageNet-100 上的 32.58%——ID 类越多越难。

## 使用者

| 方法 | 数据集 | FPR95↓ |
|------|--------|--------|
| MCM (baseline) | ImageNet-100 | 32.58% |
| LSN (CoCoOp+LSN) | ImageNet-100 | **8.56%** |
| LSN (CoCoOp+LSN) | ImageNet-1K | **30.22%** |
| MCM (baseline) | ImageNet-1K | 43.55% |
| CLIPN | ImageNet-1K | 31.10% |
| CoOp | ImageNet-1K | 51.68% |
| NegPrompt | ImageNet-1K | **23.01%** |
| LoCoOp | ImageNet-1K | 28.66% |
| NegPrompt | ImageNet-1K Hard OOD | 8.18% |

## 关联

- [AUROC](auroc.md)：互补指标——联合报告是 OOD 检测论文的标准（LSN 和 NegPrompt 均同时报告两者）。
- [LSN](../methods/lsn.md)：FPR95 从 32.58%（MCM）降至 8.56%（ImageNet-100）——核心性能指标。
- [NegPrompt](../methods/negprompt.md)：FPR95 从 43.55%（MCM）降至 23.01%（ImageNet-1K）。

## 开放问题

- 是否应该标准化多 TPR 目标（如 FPR90, FPR95, FPR99）的报告协议？
- 不同 OOD benchmark 的 FPR95 可比性问题——OOD 数据集的 "hardness" 如何校准？
