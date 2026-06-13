---
title: MS-COCO
type: dataset
domain: distillation
status: active
created: 2026-05-24
updated: 2026-05-24
tags:
  - multimodal
  - image-text-retrieval
  - dataset-distillation
  - benchmark
source_pages:
  - wiki/domains/distillation/papers/correspondence-coverage-matters-multimodal-dataset-distillation.md
related_pages:
  - wiki/domains/distillation/methods/proco.md
  - wiki/domains/distillation/topics/multimodal-dataset-distillation.md
---

# MS-COCO

## 描述

MS-COCO (Microsoft Common Objects in Context) 是大规模图像-文本配对数据集，包含超过 330K 图像，每张图像配有 5 个人工标注的英文描述（caption）。在 wiki 中作为 ProCo 多模态数据集蒸馏的核心 benchmark 之一出现，用于图文检索任务（image-text retrieval）。

## 使用场景

- 多模态数据集蒸馏：ProCo 的图文检索 benchmark——验证 correspondence coverage 在真实世界多模态数据上的有效性。
- 评估指标：Recall@K (R@1, R@5, R@10)，衡量蒸馏数据在检索任务上的 budget-efficacy trade-off。

## 划分与协议

- 标准 1K 测试分割（5,000 测试图像）和 5K 测试分割（25,000 测试图像）两种评估协议。
- ProCo 使用标准图文检索评估设置（具体分割细节待 PDF 全文确认）。

## 已知问题

- Caption 质量不一致——部分标注过于笼统或包含主观描述。
- 图文检索任务的评估协议在社区中不完全统一（1K vs. 5K test split）。
- 作为多模态 DD benchmark 时，蒸馏预算的设置（IPC/image-text pairs）缺乏统一标准。

## 使用者

- **ProCo**：在 10 倍更小蒸馏预算下超越先前方法 15%+（具体 R@K 数值待 PDF 全文获取）。

## 关联

- [Flickr30K](#)（待创建）：另一个多模态 DD benchmark，与 MS-COCO 共享图文检索评估协议。
- [ProCo](../methods/proco.md)：使用 MS-COCO 作为多模态 DD 的核心 benchmark。
- [Multi-Modal Dataset Distillation](../topics/multimodal-dataset-distillation.md)：所属主题页。

## 开放问题

- MS-COCO 蒸馏在更大规模变体（full 330K）上的 scaling 行为？
- 不同 caption 标注质量对蒸馏数据 correspondence 质量的影响？
- 多模态 DD 中 MS-COCO 与 Flickr30K 的 benchmark 一致性？
