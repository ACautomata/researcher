---
title: Federated Learning
type: concept
domain: federated-learning
status: active
created: 2026-05-05
updated: 2026-05-05
tags:
  - federated-learning
  - distributed-machine-learning
  - privacy-preserving
  - aggregation
source_pages:
  - wiki/domains/federated-learning/papers/fedact-concurrent-federated-intelligence.md
  - wiki/domains/federated-learning/papers/fedharmony-heterogeneous-label-correlations-federated-multi-label.md
  - wiki/domains/federated-learning/papers/fedkper-generalization-personalization-medical-fl.md
---

# Federated Learning

## 定义

Federated Learning (FL) 是一种分布式机器学习范式：多个客户端在本地数据上训练模型，仅向中央服务器共享模型参数或梯度更新，服务器通过聚合（通常为加权平均）形成全局模型。核心形式化目标为：

$$\min_w F(w) = \sum_{k=1}^K \frac{n_k}{N} F_k(w)$$

其中 $K$ 为参与设备数，$n_k = |D_k|$ 为客户端 $k$ 的本地样本量，$N = \sum_k n_k$，$F_k(w)$ 为客户端 $k$ 的经验损失。

## 当前理解

### 核心维度

- **统计异质性（statistical heterogeneity）**：跨客户端非 IID 数据分布，导致局部模型偏移，降低全局泛化能力。
- **系统异质性（system heterogeneity）**：设备计算能力、通信带宽、存储容量差异。
- **隐私维度**：FL 虽不共享原始数据，但共享参数仍可能泄露敏感信息，需要 DP/HE 等增强技术。
- **个性化（personalization）**：全局模型与本地数据分布之间的权衡——pFL 增强本地适配但削弱全局性能。

### 当前 wiki 覆盖的子方向

本域覆盖以下联邦学习相关方向：
- 隐私增强（DP、HE 集成）
- 聚合权重优化（hypergradient、learnable weights）
- 联邦多标签学习（label correlation drift）
- 多作业调度（multi-job FL）
- 联邦遗忘（federated unlearning）
- 联邦蒸馏（federated distillation）
- 联邦 contextual bandits（sketched FL bandits）
- 个性化联邦学习（FedKPer）
- 面向特定应用的 FL（医疗、天气、ITS 安全）

## 证据

- 12 篇 ingested 论文覆盖了从基础 FL 聚合方法到特定领域应用的全谱。
- 与现有 `distillation` 域的交叉点：[FedHD](../papers/fedhd-federated-distillation-whole-slide-image.md)（联邦数据集蒸馏）和 [EASE](../papers/ease-federated-multimodal-unlearning.md)（与多模态蒸馏共享 cross-modal 技术栈）。
- 与现有 `autonomous-driving` 域的交叉点：[PALCAS](../autonomous-driving/papers/palcas-priority-aware-lane-change-federated-rl.md)（FedRL 变道决策）。

### 当前 wiki 的主题线程

- [Federated Distillation and Unlearning](../topics/federated-distillation-and-unlearning.md)：蒸馏与遗忘的统一分析——cross-modal coupling 的双重角色。
- [FL Heterogeneity and Optimization](../topics/fl-heterogeneity-and-optimization.md)：聚合/任务/系统三层异质性的优化方法。

## 连接

- [FedHD](../papers/fedhd-federated-distillation-whole-slide-image.md)：联邦数据集蒸馏用于 WSIs。
- [EASE](../papers/ease-federated-multimodal-unlearning.md)：联邦多模态遗忘，Anchor Principle。
- 与 `distillation` 域的 [Dataset Distillation](../../distillation/concepts/dataset-distillation.md) 交叉——FedHD 将 DD 迁移到联邦设定。

## 开放问题

- 联邦数据集蒸馏与集中式 DD 在效率-效用 trade-off 上的系统比较。
- 联邦遗忘对多模态模型的最优 anchor 消除策略。
- 跨域 FL（如 `distillation` × `federated-learning`）的统一框架可能性。
