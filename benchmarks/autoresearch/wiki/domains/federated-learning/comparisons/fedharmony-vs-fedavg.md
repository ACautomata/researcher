---
title: FedHarmony vs FedAvg — 联邦多标签聚合策略对比
type: comparison
domain: federated-learning
status: active
created: 2026-05-24
updated: 2026-05-24
tags:
  - federated-learning
  - multi-label
  - aggregation
  - label-correlation
source_pages:
  - wiki/domains/federated-learning/papers/fedharmony-heterogeneous-label-correlations-federated-multi-label.md
related_pages:
  - wiki/domains/federated-learning/concepts/federated-learning.md
---

# FedHarmony vs FedAvg — 联邦多标签聚合策略对比

## 问题

在多标签联邦学习中，FedAvg 按数据量加权聚合模型参数。但当各客户端的标签分布高度异质时，这种策略为什么失效？FedHarmony 如何通过 consensus correlation 替代数据量加权来解决问题？

## 范围

- 方法维度：聚合策略（数据量加权 vs. consensus correlation 加权）、异质性处理。
- 场景维度：多标签分类（multi-label）——每个样本可有多个标签，标签共现关系是关键信息。
- 不包含：FedHarmony 与其他非 FedAvg 聚合策略（如 FedProx、SCAFFOLD）的直接比较——本对比聚焦于聚合权重设计哲学。

## 对比表

| 维度 | FedAvg | FedHarmony |
|------|--------|------------|
| **聚合权重** | 客户端数据量比例（$w_k = n_k / \sum n_i$） | 客户端标签共识相关性（consensus correlation） |
| **核心假设** | 数据量大的客户端贡献更好的梯度方向 | 标签相关性与全局共识一致的客户端贡献更可靠的知识 |
| **异质性处理** | 无显式处理——异质场景下多数客户端主导、少数客户端被淹没 | 显式建模——标签相关性差异被识别并降权 |
| **多标签场景** | 忽略标签共现结构——每个标签独立聚合一视同仁 | 利用标签共现关系——标签相关性共识度高的客户端权重高 |
| **偏差风险** | 数据量偏差 + 标签分布偏差污染全局模型 | 降低偏差（按数据量加权 → 按标签结构质量加权） |
| **适用场景** | 数据分布 IID 或轻度异质 | 多标签、标签分布高度异质 |

## 发现

1. **FedAvg 在多标签中的核心问题**：当不同客户端的标签共现关系差异巨大时（如客户端 A 的 "dog" 总与 "park" 共现，客户端 B 的 "dog" 总与 "home" 共现），FedAvg 按数据量加权会促使全局模型偏向数据量大的客户端的标签关系——如果这种关系是客户端特有的（spurious），全局模型会学到错误的标签共现模式。
2. **FedHarmony 的关键创新**：将聚合从 "谁的样本多听谁的" 切换为 "谁的标签关系与全局共识一致听谁的"。这本质上是在聚合阶段执行了标签结构的去偏——与 COBRA 在蒸馏中拒绝按群体比例加权形成哲学对称。
3. **数据量与标签质量的分离**：大数据量 ≠ 高标签质量（标签相关性可能被特定客户端的采集偏差污染）。FedHarmony 分离了这两个维度——大数据量但低共识的客户端不会被完全丢弃，只是权重降低。

## 注意事项

- FedHarmony paper 在 wiki 中的 evidence_level 和完整实验数据待确认——本对比基于 AGENTS.md 和已有 paper 页中记录的有限信息进行方法层面分析。
- 本对比聚焦于聚合权重设计的哲学差异，而非具体的性能数值——完整的定量对比需在 FedHarmony paper 升级为 full-paper 后补充。

## 证据

- FedHarmony: wiki paper 页（证据等级待确认）。核心主张：用 consensus correlation 替代数据量加权以防止多数偏差污染全局。

## 后续

- 将 FedHarmony paper 升级为 full-paper 后，补充定量对比（FedAvg vs. FedHarmony 在具体数据集上的 mAP、F1 等指标差异）。
- 探索 consensus correlation 加权策略在非多标签联邦学习场景（如单标签异质分类、联邦回归）中的适用性。
- 与 COBRA 的 barycenter alignment 建立跨域方法比较页（两者共享 "拒绝均匀加权" 的哲学）。
