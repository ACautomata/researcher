---
title: "AlignG: Learning Context-Conditioned Predicate Semantics via Prototype Feedback"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
authors: "NamGyu Jung, Chang Choi"
year: 2026
venue: "ICML 2026"
arxiv: "2602.05681"
code: "https://github.com/Namgyu97/AlignG-SGG.pytorch"
tags: [SGG, predicate-semantics, prototype-learning, context-adaptation, debiasing, ICML-2026]
raw_sources:
  - ../../../sources/scene-graph/2026-06-09-context-conditioned-predicate-semantics-sgg.pdf
  - ../../../sources/scene-graph/2026-06-09-context-conditioned-predicate-semantics-sgg.txt
evidence_level: full-paper
---

# AlignG: Learning Context-Conditioned Predicate Semantics via Prototype Feedback

**NamGyu Jung, Chang Choi** — Gachon University — ICML 2026

## 核心贡献

1. **新范式**: 将 SGG 中的谓词学习重构为**图像条件适配问题**，摒弃了以往静态原型范式
2. **AlignG 框架**: 两阶段原型反馈机制——(1) 根据图像特定的关系证据调整谓词原型，(2) 用调整后的原型重新校准关系特征
3. **SOTA 性能**: VG-150 和 GQA-200 上均取得最佳结果，F@100 SGDet 分别提升 +1.4 和 +2.7

## 问题背景

SGG 中的谓词存在严重的**多义性**（polysemy）。例如 "on" 在不同上下文中可能表示 spatial contact 或 functional usage。现有方法（如 PE-Net 的单原型、多原型分解、RA-SGG 的检索扩展）虽然引入结构化先验，但**原型表示在推理时保持静态**，无法根据图像特定的证据动态调整。

## 方法：AlignG

### 整体流程

```
全局原型 (R个) ←→ 交叉注意力 → 图像条件化原型 → GRU更新 → 校准关系特征
     ↑                                                       |
     └────────────────── 原型反馈 ───────────────────────────┘
```

### 核心组件

1. **上下文化谓词原型**（Contextualizing Predicate Prototypes）
   - 通过交叉注意力机制，让全局原型 $p_k$ 与图像中的关系候选 $e_j$ 交互
   - 得到图像条件化的原型 $\tilde{p}_k = f_\theta(p_k, E)$
   - 公式: $\tilde{p}_k = \sum_{j=1}^P \alpha_{kj} \cdot e_j$，其中 $\alpha$ 为注意力权重

2. **重新校准关系嵌入**（Recalibrating Relation Embeddings）
   - 用条件化后的原型 $\tilde{p}_k$ 修正关系候选表示
   - GRU-based 更新: $e_j' = \text{GRU}(e_j, \tilde{p}_{\text{best}})$
   - 对比连接（concatenation）策略，GRU 可更平滑地融合全局和局部信号

3. **训练目标**
   - **对齐损失**（Alignment Loss）: 拉近条件化原型 $\tilde{p}_k$ 与对应关系候选的距离
   - **分散损失**（Diversity Loss）: 不同条件化原型之间的散度惩罚，防止语义坍缩
   - **全局锚定**: $\tilde{p}_k$ 受全局语义中心 $p_k$ 约束，防止语义漂移

### 与基线对比的关键创新

| 方法 | 原型类型 | 推理时自适应 | 计算开销 |
|------|----------|-------------|---------|
| PE-Net (CVPR'23) | 单原型/谓词 | ❌ 静态 | 低 |
| MCL (TIP'25) | 多概念原型 | ❌ 静态 | 中 |
| RA-SGG (AAAI'25) | 外部检索原型 | ❌ 外部依赖 | 高（检索） |
| **AlignG (ours)** | 图像条件化原型 | ✅ 自适应 | 低（+7G FLOPs） |

## 实验结果

### VG-150 结果（SGDet）

| 指标 | PE-Net† | MCL† | RA-SGG† | **AlignG†** |
|------|---------|------|---------|-------------|
| R@100 | 30.7 | 27.3 | 26.0 | **25.9** |
| mR@100 | 12.4 | 14.9 | 14.4 | **19.7** |
| **F@100** | 17.7 | 19.3 | 18.5 | **23.8** |

**PredCls**: AlignG† 的 mR@100 = 42.6（比 MCL† 高 +0.2，比 PE-Net† 高 +8.8）
**SGCls**: AlignG† 的 mR@100 = 26.1（比 MCL† 高 +1.3），F@100 = 30.2

### GQA-200 结果（SGDet）

| 指标 | PE-Net | DPL† | RA-SGG† | **AlignG†** |
|------|--------|------|---------|-------------|
| mR@100 | 10.3 | 11.1 | 12.9 | **15.5** |
| **F@100** | 13.5 | 12.8 | 14.4 | **19.5** |

**PredCls**: mR@100 = 37.9（比 RA-SGG† 高 +1.1, 比 PE-Net 高 +10.8）
**SGCls**: F@100 = 20.4（比 RA-SGG† 高 +1.6）

### 关键消融发现

| 组件变体 | PredCls mR@100 | SGDet F@100 |
|----------|---------------|-------------|
| PE-Net backbone | 31.5 | 17.7 |
| + Edge update | 33.8 (+2.3) | 18.1 (+0.4) |
| + Concat proto align | 34.0 (+0.2) | 17.9 (-0.2) |
| + GRU proto align | **35.0 (+1.2)** | **18.2 (+0.5)** |
| + Reweighting (†) | **42.6** | **23.8** |

- GRU-based 原型更新比 concat-based 在所有任务上一致提升
- 重加权与原型反馈互补，不需要牺牲 recall 来换 mR

### 计算开销

| 方法 | FLOPs | 训练时间 | 推理 FPS | F@100 |
|------|-------|---------|---------|-------|
| PE-Net | 472.36G | 0.35s/iter | 30.84 | 20.4 |
| AlignG | 479.41G | 0.38s/iter | 30.14 | **21.3** |
| Δ | **+7.05G** | +0.03s | -0.70 FPS | **+0.9** |

### 谓词混淆分析

AlignG 对 PE-Net 困难混淆的解决比例：lying on vs laying on **42.6%**，carrying vs holding **26.9%**，watching vs looking at **21.4%**，walking on vs standing on 19.4%，riding vs standing on 11.5%。

## 讨论

- **优势**: 原型反馈将全局语义与局部图像证据桥接，在保持语义一致性的同时允许细粒度的上下文自适应
- **局限**: 矛盾背景线索或噪声检测可能误导每图像自适应，导致语义漂移
- **未来方向**: 时序一致性（视频理解）、置信度感知证据选择、更强大的全局语义锚定

## 关联论文

- [[prototype-based-embedding-network-scene-graph-generation|PE-Net (CVPR 2023)]] — 单原型基础框架
- [[multi-prototype-space-learning-commonsense-sgg|Multi-Prototype Space Learning (AAAI 2024)]] — 多概念分解
- [[ra-sgg-retrieval-augmented-scene-graph-generation-multi-prototype-learning|RA-SGG (AAAI 2025)]] — 外部检索增强

## 链接

- **代码**: https://github.com/Namgyu97/AlignG-SGG.pytorch
- **PDF**: [[raw/sources/2026-06-09-context-conditioned-predicate-semantics-sgg.pdf]]
