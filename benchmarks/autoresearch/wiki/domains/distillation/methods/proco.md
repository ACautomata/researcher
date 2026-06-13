---
title: ProCo — Promote Correspondence Coverage
type: method
domain: distillation
status: active
created: 2026-05-24
updated: 2026-05-24
tags:
  - dataset-distillation
  - multimodal-learning
  - correspondence-coverage
  - conditional-neural-fields
source_pages:
  - wiki/domains/distillation/papers/correspondence-coverage-matters-multimodal-dataset-distillation.md
related_pages:
  - wiki/domains/distillation/concepts/dataset-distillation.md
  - wiki/domains/distillation/topics/multimodal-dataset-distillation.md
---

# ProCo — 促进跨模态对应覆盖的多模态数据集蒸馏

## 定义

ProCo 是首个以跨模态 correspondence coverage 为核心优化目标的多模态数据集蒸馏方法，通过 retrieval-based correspondence consistency metric 聚类 + coverage-aware 正则化 + conditional neural fields 参数化，系统性地解决多模态 DD 中的 over-concentration 和 intra-modal bias 问题。

## 核心机制

1. **Correspondence Consistency Metric**：基于跨模态检索分布定义 correspondence 一致性度量，聚类揭示真实数据中的底层 correspondence 分布。
2. **Coverage-Aware Regularization**：从 correspondence clusters 选择代表性 patterns 初始化蒸馏数据，优化中同时促进代表性和多样性。
3. **Conditional Neural Fields**：替代直接像素/文本优化，高效参数化蒸馏数据，实现 elastic budget-efficacy trade-off。

## 假设

- 跨模态 correspondence coverage（而非 intra-modal similarity）是多模态 DD 的核心压缩目标。
- clustering-based initialization 能有效发现真实数据的 correspondence 分布。
- conditional neural fields 提供比直接优化更高效的参数化方式。

## 证据

- AAAI 2026，Dang et al.。
- 使用 10 倍更小蒸馏预算（vs. 先前多模态 DD 方法），超越 15%+。
- 在 Flickr30K、MS-COCO 图文检索任务上验证（R@1, R@5, R@10）。
- 证据等级：paper 为 skimmed，完整的定量数字和 ablation 尚未提取。

## 变体

无已知变体。ProCo 是目前唯一以 correspondence coverage 为核心的多模态 DD 方法。

## 优势与局限

**优势**：
- 首次系统性处理多模态 DD 的跨模态对应问题，而非延续单模态策略。
- Elastic budget-efficacy trade-off — 通过 conditional neural fields 灵活平衡压缩率与性能。
- 方法通用性：推向了 image-text paired data 的多模态蒸馏。

**局限**：
- 对 retrieval-based correspondence metric 的质量敏感性未分析。
- 三组件（clustering, regularization, conditional neural fields）的独立贡献（ablation）未知。
- 仅验证于 image-text，未扩展到 audio-text / video-text。
- Paper 为 skimmed 证据等级，完整定量结果待 PDF 全文获取后补充。

## 关联

- [Dataset Distillation](../concepts/dataset-distillation.md)：上位概念。
- [Multi-Modal Dataset Distillation](../topics/multimodal-dataset-distillation.md)：所属主题页。
- 与 FedHD 的 Gaussian-Mixture Alignment 共享"分布级匹配优于均值匹配"哲学。
- 与 COBRA 的 barycenter alignment 形成对比：ProCo 追求覆盖多样性，COBRA 追求群体公平性。

## 开放问题

- Clustering、regularization、conditional neural field 各组件的各自贡献（ablation）？
- 对 retrieval-based correspondence consistency metric 质量的敏感性？
- 能否迁移到 image-text 之外的模态组合（audio-text、video-text）？
- 多模态 correspondence coverage 与单模态 diversity objective 在数学上的精确关系？
