---
title: 跨域技术索引
type: index
domain: cross-cutting
status: active
created: 2026-06-07
updated: 2026-06-07
tags:
  - cross-domain
  - taxonomy
  - synthesis
---

# 跨域技术索引

> **作用**：按技术概念/模式找论文，而非按领域找论文。每个条目记录同一技术在不同领域中的不同用法和角色。

## 概念页

- [受控增量整合](controlled-incremental-integration.md)：CD (SE2D) × FedHD (Curriculum Federation) × CoRD (Step-wise Decoding) 的共性哲学——拒绝均匀融合，先稳定再扩展，选择性保留
- [遗忘机制的统一理解](forgetting-mechanisms.md)：UKF (Continual Distillation) × FL Catastrophic Forgetting 的共通根因与差异化缓解策略
- [跨模态耦合的三重角色](cross-modal-coupling.md)：Cross-Modal Coupling 在蒸馏（效率来源）/ 遗忘（主要障碍）/ OOD 检测（控制手段）中的截然不同角色

## 分类学页

- [Matching 方法家族分类](matching-family-taxonomy.md)：Distribution / Gradient / Trajectory / Correspondence / Feature / Curriculum / Step-wise Matching 的完整谱系

## 跨域对比页

- [防多数偏差：FedHarmony × COBRA 的均匀哲学](fedharmony-cobra-uniform-philosophy.md)：从联邦多标签学习和公平数据集蒸馏中独立发现的"拒绝按规模加权"共识

## 与其他入口的关系

```
领域入口 (wiki/index.md)          技术入口 (wiki/cross-cutting/index.md)
      ↓                                    ↓
按研究领域找论文                    按跨域概念/模式找论文
      ↓                                    ↓
distillation/papers/               controlled-incremental-integration.md
federated-learning/papers/         matching-family-taxonomy.md
llm-reasoning/papers/              cross-modal-coupling.md
                                   forgetting-mechanisms.md
      ↓                                    ↓
两套索引互相链接，同一篇论文可以从两个入口到达
```
