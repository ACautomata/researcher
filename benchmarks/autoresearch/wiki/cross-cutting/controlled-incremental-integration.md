---
title: 受控增量整合 — 跨域统一视角
type: concept
domain: cross-cutting
status: active
created: 2026-06-07
updated: 2026-06-07
tags:
  - incremental-integration
  - cross-domain
  - curriculum-learning
  - distillation
  - federated-learning
  - reasoning
source_pages:
  - wiki/domains/distillation/papers/continual-distillation-teachers-different-domains.md
  - wiki/domains/federated-learning/papers/fedhd-federated-distillation-whole-slide-image.md
  - wiki/domains/llm-reasoning/papers/distilling-long-cot-reasoning-cord.md
related_pages:
  - wiki/cross-cutting/forgetting-mechanisms.md
  - wiki/cross-cutting/matching-family-taxonomy.md
---

# 受控增量整合 — 跨域统一视角

## 定义

受控增量整合（Controlled Incremental Integration）是指在多知识源场景中，**不一次性均匀融合所有信号，而是先建立稳定基线，再逐步、有选择地引入异构知识**的通用策略。该模式在三个不同领域独立出现，共享同一哲学但各有具体实现。

## 三域体现

| 领域 | 论文 | 场景 | 实现方式 |
|------|------|------|---------|
| **Distillation** | CD (SE2D) | 教师模型序列顺序蒸馏 | 先日志蒸馏当前教师，再用上一 checkpoint 在外部数据上做 self-distillation 保持旧知识 |
| **Federated Learning** | FedHD | 多医院 WSI 联邦蒸馏 | 先真实 WSI 数据训练基础表示，再逐步引入合成数据的 curriculum federation |
| **LLM Reasoning** | CoRD | 多 teacher 协同推理 | 每步让所有 teacher 提候选步骤，用 predictive perplexity 动态选最优，而非一次性合并完整轨迹 |

## 共性哲学

1. **拒绝均匀融合**：CD 的 SE2D 不把新旧教师 logits 简单平均；FedHD 不把真实数据和合成数据等权混合；CoRD 不把所有 teacher 输出 uniform ensemble
2. **先稳定再扩展**：先建立基线性能（第一个教师/真实数据/第一个推理步骤），再逐步引入异构信号
3. **选择性保留**：每一步引入新信息时，有明确的机制保护旧信息（SE2D 的 logit 保持、FedHD 的 curriculum federation、CoRD 的 beam search 保留 top-B 轨迹）

## 区别

| 维度 | SE2D | FedHD | CoRD |
|------|------|-------|------|
| 整合时机 | 训练时（每步蒸馏） | 训练时（curriculum 阶段切换） | 推理时（每步解码） |
| 知识粒度 | 教师级（整个模型） | 数据级（合成样本批次） | 步骤级（单步推理） |
| 保护机制 | Logit 保持（self-distillation） | Gaussian-Mixture Alignment | Beam search + predictive perplexity |
| 遗忘对象 | 先前教师的未见领域知识 | 先前医院的分布特性 | 先前步骤的推理方向 |

## 证据

- CD/SE2D：CIFAR20 上 SE2D forgetting 4.44 vs Self-Dist 8.32（-46.6%）；Digits forgetting 3.73 vs Self-Dist 5.58（-33.2%）
- FedHD：CAMELYON16 +2.5% Acc vs FedWSIDD，CAMELYON17 +5.5%
- CoRD：AIME24 Pass@1 79.6% vs Curation 75.0%（+4.6pp）；beam search 79.6% vs MCTS 75.8%

## 开放问题

- 受控增量整合的"最优步长"：什么时候引入新信号？引入多少？
- 能否在训练时和推理时之间建立统一的理论框架（目前 SE2D/FedHD 在训练时，CoRD 在推理时）？
- 更大规模 teacher 序列（10+）或更多数据源的极限场景下，该策略是否仍然有效？
