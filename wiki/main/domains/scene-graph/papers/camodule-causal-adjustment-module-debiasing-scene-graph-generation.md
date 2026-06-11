---
title: "CAModule: A Causal Adjustment Module for Debiasing Scene Graph Generation"
authors: "Li Liu, Shuzhou Sun, Shuaifeng Zhi, Fan Shi, Zhen Liu, Janne Heikkilä, Yongxiang Liu"
year: 2025
venue: "arXiv 2025 (TPAMI under review)"
arxiv: null
doi: null
code: null
domain: scene-graph
evidence_level: full-paper
tags: [scene-graph-generation, debiasing, causal-inference, long-tail, zero-shot]
status: active
raw_sources:
  - ../../../sources/scene-graph/2025-arXiv-CAModule-Causal-Adjustment-Module-for-Debiasing-Scene-Graph-Generation.pdf
  - ../../../sources/scene-graph/2025-arXiv-CAModule-Causal-Adjustment-Module-for-Debiasing-Scene-Graph-Generation.txt
---

# CAModule: A Causal Adjustment Module for Debiasing Scene Graph Generation

> Liu et al. arXiv 2025 (TPAMI under review)

## 概述

提出 **CAModule**（Causal Adjustment Module），通过因果推断建模 SGG 模型中的偏置来源，在 triplet 级别（<subject, predicate, object>）输出细粒度的 logit adjustment factors，纠正有偏预测。核心创新有两方面：(1) 揭示**对象分布**和**对象对分布**的倾斜是比关系长尾更深的偏置根源；(2) 引入**中介变量**（co-occurrence distribution）构建 Mediator-based Causal Chain Model ([MCCM](#mccm))，丰富因果建模。

## 方法

### 偏置分析

传统 SGG 去偏工作仅关注关系类别的长尾分布，但本文发现：

- 对象分布本身高度倾斜（如 "man" 4.7% vs "bird" 0.4%），见 Fig. 1(a)
- 对象对分布同样极度倾斜（如 <man, shirt> 远多于 <man, tree>），见 Fig. 1(c)
- 即使是同一关系类别（如 "on"），不同 triplet 的准确率差异极大（0%~100%），见 Fig. 1(e)
- 这说明需要 **triplet 级别**的 logit adjustment，而非粗粒度的关系类别级别调整

### Mediator-based Causal Chain Model (MCCM)

标准 SGG 训练遵循链式因果结构（Causal Chain Model, CCM）: O → P → R（对象→对象对→关系）

MCCM 在 O→P 之间引入中介变量 **C**（co-occurrence distribution），衡量任意两个对象同时出现在同一场景中的概率：

$$
C_{ij} = \frac{Count(<r_i, r_j>)}{Count(r_i) + Count(r_j)}
$$

结构方程（Structural Causal Model, SCM）变为：

```
O = P(O)
C = F̃_O(O, P(O))
P = F̃_1(O, P(O)) + F̃_C(C, P(C))
R = F̃_2(P, P(P))
```

C 的作用：
- 为不太可能同时出现的对象对（如 <man, tree>）赋予低权重
- 为现实场景中高频共现的对象对（如 <man, shirt>）赋予高权重
- 通过条件互信息量化 triplet 自身的不确定性

### CAModule 架构

轻量级 Transformer 架构，输入 4 个观测分布：O（对象分布）、C（共现分布）、P（对象对分布）、R（关系分布），输出 triplet 级 adjustment factors。

Key design:
- 每次推理只做一次前向模型推断（区别于 TDE [27] 的两次推断）
- Adjustment factors 在 **隐空间**隐式学习，而非基于频率的倒数等显式先验
- Triplet 级调整 vs 关系级调整的区别见图 5

### Zero-shot 关系组合

MCCM 具备零样本关系组合能力：通过组合已知关系类型和对象对，生成训练集中未出现的零样本关系。

**两个推理规则：**
- **Rule 1（主体相似性）：** 若对象 A 和 B 属性相似且 A 与某对象形成关系 R，则 B 也可与该对象形成关系 R
- **Rule 2（客体相似性）：** 对称规则，基于客体相似性推演

对对象对分布 P 的优化（CAModule-P 消融）可进一步提升零样本识别性能。

## 实验

### 设置

- **数据集：** VG150（150 obj/50 rel）、GQA（200 obj/100 rel）、Open Images V6（601 obj/30 rel）
- **框架：** MotifsNet [2]、VCTree [46]、Transformer [63]
- **评估模式：** PredCls、SGCls、SGDet
- **指标：** mR@K、R@K、MR@K、zR@K

### VG150 主要结果（Table 1, Table 6）

**CAModule（完整版，d=✓, cos=✓）在 VG150 上的表现：**

| 框架 | 模式 | mR@20 | mR@50 | mR@100 | zR@20 | zR@50 | zR@100 |
|------|------|-------|-------|--------|-------|-------|--------|
| MotifsNet | PredCls | 32.5 | 36.7 | 39.3 | 9.5 | 16.7 | 20.3 |
| MotifsNet | SGCls | 18.8 | 21.1 | 24.7 | 2.1 | 5.1 | 7.6 |
| MotifsNet | SGDet | 11.7 | 16.3 | 18.2 | 1.4 | 2.1 | 3.7 |
| VCTree | PredCls | 35.2 | 38.4 | 40.5 | 8.1 | 14.5 | 18.4 |
| VCTree | SGCls | 21.7 | 23.2 | 25.9 | 1.3 | 5.1 | 7.2 |
| VCTree | SGDet | 12.3 | 16.4 | 19.6 | 1.1 | 1.6 | 3.2 |
| Transformer | PredCls | 34.1 | 37.6 | 39.4 | 8.5 | 15.4 | 19.7 |

> 注：SGDet 和部分数值来自 Table 6 消融实验的最佳配置行

**SOTA 对比：** 在 VG150 PredCls 模式下以 VCTree 为 backbone，CAModule 在 mR@100 上超过 TransRwt (2.7%)、PPDL (8.6%)、RTPB (6.8%)、NICEST (9.3%)。

### OI V6 结果（Table 4）

| 方法 | R@50 | mR@50 | wmAP_rel |
|------|------|-------|----------|
| CAModule | 77.4 | 43.7 | 40.3 |

CAModule 在 mR@50 上超过 HetSGG (0.5%) 到 BGNN (3.2%)。

### Zero-shot 结果（Table 5）

CAModule vs CAModule-P（无对象对分布优化）在 zR@K 上的显著提升：

| 框架 | 模式 | CAModule zR@20/50/100 | CAModule-P zR@20/50/100 |
|------|------|----------------------|------------------------|
| MotifsNet | PredCls | 7.3/10.8/16.7 | 4.2/7.0/9.5 |
| VCTree | PredCls | 7.7/11.3/14.5 | 4.3/6.6/8.1 |
| Transformer | PredCls | 7.9/9.6/15.4 | 4.1/6.4/8.5 |

### 消融（Table 6, Table 7）

CAModule 中两个关键超参数：α（Euclidean distance 权重）和 β（cosine similarity 权重），阈值分别设为 0.7 和 0.4。

- 同时启用 Euclidean distance 和 cosine similarity 的组合效果最佳（参见 Table 6 行 4）
- 与 vanilla logit adjustment（关系级调整，调整因子设为关系频率倒数）对比，vanilla 方法几乎无去偏效果，验证了论文关于 triplet 级调整必要性的分析

## 关键洞察

1. **偏置根源的深入分析：** 对象分布和对象对分布的倾斜是比关系长尾更深的偏置源头，论文通过因果建模量化了这一发现
2. **中介变量的引入：** Co-occurrence distribution 作为中介变量，提供对 triplet 自身不确定性的先验知识
3. **Zero-shot 能力：** MCCM 的结构性和 Rule 1/Rule 2 推理规则使零样本关系识别成为可能
4. **轻量级设计：** CAModule 是轻量级 Transformer 模块，可即插即用于任何 SGG 框架

## Provenance

- **来源文件**: `sources/scene-graph/2025-arXiv-CAModule-Causal-Adjustment-Module-for-Debiasing-Scene-Graph-Generation.pdf`
- **提取文本**: `sources/scene-graph/2025-arXiv-CAModule-Causal-Adjustment-Module-for-Debiasing-Scene-Graph-Generation.txt`

## 局限性

1. 无法从零样本对象对（训练集中从未出现的对象组合）生成零样本关系
2. 对零样本对象对的推理依赖 Rule 1/Rule 2 的相似性假设，不够完备
3. zR@K 在 SGDet 和 SGCls 模式下表现仍有限（SGDet zR@100 < 10%）

## 关联方法

- [[cage-sgg-counterfactual-active-graph-evidence-open-vocabulary-sgg|CAGE-SGG]]：同属因果/反事实去偏的 SGG 方法
- [[compositional-feature-augmentation-for-unbiased-scene-graph-generation|CFA]]：基于特征增强的去偏方法
- [[scalable-theory-driven-regularization-scene-graph-generation|Theory-Driven Regularization]]：基于理论驱动的 SGG 正则化
- TDE [27]：反事实去偏基线，需两次推断
- TsCM [55]：两阶段因果建模，分别处理长尾和语义混淆

## 术语

- `MCCM` — Mediator-based Causal Chain Model，中介变量因果链模型
- `CAModule` — Causal Adjustment Module，因果调整模块
- `triplet-level adjustment` — 在 <subject, predicate, object> 三元组级别的细粒度调整
- `CAModule-P` — 无对象对分布优化的消融变体
