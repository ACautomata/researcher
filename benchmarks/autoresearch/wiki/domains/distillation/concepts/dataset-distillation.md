---
title: Dataset Distillation
type: concept
domain: distillation
status: active
created: 2026-04-20
updated: 2026-05-05
tags:
  - machine-learning
  - dataset-distillation
  - data-efficiency
  - fairness
source_pages:
  - wiki/domains/distillation/papers/rethinking-long-tailed-dataset-distillation.md
  - wiki/domains/distillation/papers/correspondence-coverage-matters-multimodal-dataset-distillation.md
  - wiki/domains/distillation/papers/targeted-data-protection-diffusion-model-training-trajectory.md
  - wiki/domains/distillation/papers/fair-dataset-distillation-cobra.md
raw_sources:
  - raw/sources/2025-12-14-rethinking-long-tailed-dataset-distillation.pdf
  - raw/sources/2026-03-14-correspondence-coverage-matters-multimodal-dataset-distillation.md
  - raw/sources/2026-03-14-targeted-data-protection-diffusion-model-training-trajectory.md
  - raw/sources/2026-05-04-fair-dataset-distillation-cobra.pdf
---

# Dataset Distillation

## 定义

Dataset distillation 是把大规模训练集压缩成小规模合成数据或选择数据的研究问题。目标是在训练成本显著下降的情况下，尽量保留下游训练所需的学习信号。

## 当前理解

- 蒸馏数据集是完整训练集的紧凑代理。
- 常见评估设置会固定图像预算，例如 `IPC`（images per class）。
- 许多方法默认平衡数据分布，但长尾分布会让这些假设变弱。
- 当前 wiki 中的长尾论文认为，不平衡会造成 representation bias 和 Batch Normalization 统计偏移。
- 多模态蒸馏不能只看单模态相似性，还需要覆盖跨模态 correspondence patterns。
- 数据集蒸馏中的 trajectory matching 思想可以迁移到其他问题，例如 diffusion-model fine-tuning 的 targeted data protection。
- 蒸馏过程会放大原始数据中的子群体偏差——偏差来源于群体不平衡与子群体表示分离的交互作用，而非单一因素；仅靠蒸馏前/后的公平干预不够，蒸馏聚合目标本身必须公平化（COBRA）。

## 证据

- [Rethinking Long-tailed Dataset Distillation](../papers/rethinking-long-tailed-dataset-distillation.md)：认为长尾蒸馏应被视为统计偏置问题，而不是平衡蒸馏的直接扩展。
- [Correspondence Coverage Matters for Multi-Modal Dataset Distillation](../papers/correspondence-coverage-matters-multimodal-dataset-distillation.md)：强调 paired multi-modal distillation 中 correspondence coverage 是核心设计问题。
- [Targeted Data Protection for Diffusion Model by Matching Training Trajectory](../papers/targeted-data-protection-diffusion-model-training-trajectory.md)：说明 trajectory matching 可以从数据压缩迁移到 diffusion-model 保护。
- [Fair Dataset Distillation via COBRA](../papers/fair-dataset-distillation-cobra.md)：证明蒸馏偏差放大来自群体不平衡与表示分离的交互，提出公平重心对齐框架，兼容 DC/DM/CAFE/IDC/MTT 所有主流方法。

## 连接

- [Long-Tailed Dataset Distillation](../topics/long-tailed-dataset-distillation.md)：长尾蒸馏主题。
- [Multi-Modal Dataset Distillation](../topics/multimodal-dataset-distillation.md)：跨模态 correspondence 蒸馏主题。
- [Diffusion Model Data Protection](../topics/diffusion-model-data-protection.md)：展示蒸馏思想在防御控制中的迁移。
- [Fair Dataset Distillation](../topics/fair-dataset-distillation.md)：子群体公平蒸馏主题。

## 开放问题

- 数据集蒸馏的主要方法族应如何划分：trajectory matching、gradient matching、statistical alignment、distribution matching，还是其他？
- Statistical alignment 范式在非 ConvNet 架构（Transformer、ViT）上的适用性？
- 除 top-1 accuracy 外，还应关注 head-tail balance、calibration、robustness、compute、跨架构泛化中的哪些指标？
- 什么时候蒸馏会真正优于简单的数据选择或重加权？
- 哪些思想属于数据压缩本身，哪些可以作为通用 optimization-control 工具复用？
- Statistical alignment 能否与 generative/diffusion-based 蒸馏方法结合？
- 数据蒸馏中的公平性是否应成为标准评估维度（如同准确率一样）？如何量化 fairness-accuracy-efficiency 的三元 trade-off？
