---
title: Multi-Modal Dataset Distillation
type: topic
domain: distillation
status: active
created: 2026-04-20
updated: 2026-05-05
tags:
  - dataset-distillation
  - multimodal-learning
  - vision-language
  - correspondence-coverage
source_pages:
  - wiki/domains/distillation/papers/correspondence-coverage-matters-multimodal-dataset-distillation.md
raw_sources:
  - raw/sources/2026-03-14-correspondence-coverage-matters-multimodal-dataset-distillation.md
---

# Multi-Modal Dataset Distillation

## 当前论点

多模态数据集蒸馏的核心不是压缩每个模态内部的视觉或文本特征，而是保留足够多样的跨模态 correspondence patterns。当蒸馏集极小时，paired semantics 的覆盖度（coverage）和多样性（diversity）可能比单模态 fidelity 更重要。ProCo 提出的 correspondence consistency metric + conditional neural fields 参数化组合为此提供了一个系统框架。

## 范围

- Paired 或 aligned multi-modal datasets（image-text）的蒸馏。
- 在紧预算下保留跨模态语义的方法。
- 面向多模态蒸馏数据的 coverage、diversity 和 representativeness 目标。
- 高效参数化方案（conditional neural fields 等）在固定 budget 下容纳更多蒸馏样本。

## 关键线索

- 跨模态 correspondence 是核心压缩单元，单模态 similarity 无法替代——这是 ProCo 的核心 motivation。
- Retrieval-based correspondence consistency metric 可以刻画并聚类 correspondence patterns，揭示真实数据集的底层 correspondence 分布。
- Coverage-aware initialization（从聚类中选代表性 patterns）+ diversity regularization（防止 over-concentration）。
- Conditional neural fields 提供比直接像素/文本优化更高效的参数化，支持 elastic budget-efficacy trade-off。
- ProCo 在 10x 更小蒸馏预算下超越先前方法 15%+（Flickr30K, MS-COCO, image-text retrieval）。

## 原子 Claims

- 声明：多模态数据集蒸馏应以 correspondence coverage 为核心目标，而非 intra-modal similarity。
  证据：ProCo (AAAI 2026)，correspondence-based clustering + coverage regularization 在 10x 更小预算下超先前方法 15%+。
  范围：paired image-text dataset distillation。
  置信度：medium。
  张力：wiki 还缺少与其他多模态 DD 方法（Phased Teacher Models、Asynchronous Matching, ICLR 2026）的直接比较。

- 声明：Retrieval-based correspondence consistency 可以有效聚类代表性蒸馏数据。
  证据：ProCo 方法——cross-modal retrieval distributions 作为 correspondence consistency metric。
  范围：ProCo 式多模态蒸馏。
  置信度：medium。
  张力：对 retrieval metric 和 backbone 选择的敏感性未量化。

- 声明：Conditional neural fields 是实现 elastic budget-efficacy trade-off 的关键参数化手段。
  证据：ProCo 在多个压缩比下均展现优越性能。
  范围：多模态数据集蒸馏的参数化策略。
  置信度：medium。
  张力：需要与其他参数化方案（latent codes、hypernetworks）直接比较。

## 证据

- [Correspondence Coverage Matters for Multi-Modal Dataset Distillation (ProCo)](../papers/correspondence-coverage-matters-multimodal-dataset-distillation.md)：AAAI 2026，coverage-aware multi-modal DD，skimmed。
- [Dataset Distillation](../concepts/dataset-distillation.md)：该主题所属的上位概念。

## 张力

- 当前证据主要基于一篇论文的摘要和公开元数据（skimmed），full-paper 内容获取后需要进一步充实。
- 多模态 DD 领域正在迅速发展——需要与其他同期方法（ICLR 2026 上出现多篇相关工作）比较。

## 开放问题

- 跨模态 correspondence coverage 的最优度量——retrieval-based？contrastive-based？optimal transport？
- 多模态 coverage objective 应如何与 retrieval、classification 或 generation 任务互动？
- 当 paired semantics 成为主约束时，哪些单模态蒸馏理论仍然适用？
- Conditional neural fields 是否最适参数化方案，还是 latent diffusion models 作为参数化工具更有效？
