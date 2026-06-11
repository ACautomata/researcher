---
title: "Multi-Prototype Space Learning for Commonsense-Based Scene Graph Generation"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - scene-graph-generation
  - multi-prototype-learning
  - commonsense-sgg
  - optimal-transport
  - predicate-classification
  - AAAI-2024
  - prototype-space-optimization
raw_sources:
  - ../../../sources/scene-graph/2024-AAAI-Multi-Prototype-Space-Learning-for-Commonsense-SGG.pdf
  - ../../../sources/scene-graph/2024-AAAI-Multi-Prototype-Space-Learning-for-Commonsense-SGG.txt
related_pages:
  - prototype-based-embedding-network-scene-graph-generation.md
  - ra-sgg-retrieval-augmented-scene-graph-generation-multi-prototype-learning.md
  - hiker-sgg-hierarchical-knowledge-enhanced-robust-sgg.md
evidence_level: full-paper
paper:
  title: "Multi-Prototype Space Learning for Commonsense-Based Scene Graph Generation"
  abbreviated: "MPL"
  authors:
    - Lianggangxu Chen
    - Youqi Song
    - Yiqing Cai
    - Jiale Lu
    - Yang Li
    - Yuan Xie
    - Changbo Wang
    - Gaoqi He
  affiliations:
    - East China Normal University
    - Chongqing Key Laboratory of Precision Optics, Chongqing Institute of East China Normal University
  year: 2024
  venue: AAAI 2024
  doi: null
  arxiv: null
  code: null
  url: null
---

# Multi-Prototype Space Learning for Commonsense-Based Scene Graph Generation

## 核心思想

现有基于常识的场景图生成（C-SGG）方法采用单原型（single-prototype）表示每个谓词类别，但谓词视觉外观存在**大类内变异**（如 riding 类别包含 bicycle riding、horseback riding、wave riding 等视觉差异大的子类），导致分类错误。受认知科学中**现代原型范畴理论**（modern prototype category theory）启发，本文提出为每个谓词类别维护**多原型**（multi-prototype）表示，通过原型-谓词匹配、原型更新和原型空间优化三个步骤来解决该问题。

## 方法

### 架构总览

MPL 框架包含三个主要步骤：
1. **原型-谓词匹配（Prototype-Predicate Matching）**
2. **原型更新（Prototype Updating）**
3. **原型空间优化（Prototype Space Optimization）**

### Step 1: 初始谓词特征与原型提取

- 使用 Faster R-CNN + motif 上下文编码器获取视觉谓词特征
- 从预训练的常识图（commonsense graph, Zareian 2020）中提取初始原型特征
- 将每个谓词词向量发散为 K 个原型：`C = Vc + ρ`，其中 `ρ ~ U[-r, r]`

### Step 2: 三重最优传输（Triple-level Optimal Transport, TOT）

针对传统 OT 可能导致的错误匹配问题（如图 3(b)，视觉相似的 standing on 和 riding 可能被误匹配），提出 **TOT**——在计算最优传输矩阵时同时考虑：

- **Wasserstein 距离项**：谓词-原型相似度
- **三元组距离项**：object-predicate 距离 + subject-predicate 距离——利用视觉三元组与常识三元组的结构一致性来抑制错误匹配
- **KL 散度正则化**：避免退化解（trivial solutions）

TOT 包含两个超参数：`β` 控制两项权重（设为 0.1），`ε` 控制正则化强度（设为 0.05）。

传输矩阵通过 Sinkhorn-Knopp 算法迭代计算。

### Step 3: 原型更新

根据匹配结果，使用动量更新（momentum updating）更新每个原型：

`v_k_c = μ · v_k_c + (1-μ) · v_p_mean`

其中动量系数 `μ = 0.999`，`v_p_mean` 为匹配到该原型的谓词特征均值。

### Step 4: 原型空间优化

设计两个损失函数来优化原型空间：

1. **类间可分性损失（Inter-class Separability Loss, L_ICS）**：推动每个谓词实例靠近其匹配的原型，远离其他类别的原型
2. **类内紧致性损失（Intra-class Compactness Loss, L_ICC）**：使用 **Pseudo-Huber loss** 最小化谓词与其匹配原型之间的距离，对长尾场景更鲁棒

总损失：`L_C-SGG = L_focal + λ1 · L_ICS + λ2 · L_ICC`，其中 `λ1 = λ2 = 0.1`

### 关键超参数

| 参数 | 值 | 说明 |
|------|-----|------|
| K | 3 | 每个类别的原型数量 |
| μ | 0.999 | 动量更新系数 |
| β | 0.1 | TOT 权重平衡超参数 |
| ε | 0.05 | KL 正则化强度 |
| τ | 0.1 | L_ICS 温度参数 |
| δ | 0.1 | L_ICC Pseudo-Huber 形状参数 |
| r | 0.0001 | 初始原型采样半径 |

## 关键创新

1. **首个多原型 C-SGG 框架**：将谓词空间从单中心聚类变为多中心聚类，缓解大类内变异导致的误分类
2. **三重最优传输（TOT）**：融合 predicate-wise 和 triple-wise 距离，避免视觉相似谓词间的原型-谓词错误匹配
3. **原型空间优化损失**：显式优化 prototype-prototype 和 prototype-predicate 距离，提升类别可分性和类内紧致性

## 实验设置

- **数据集**：Visual Genome (VG) + Open Images V6
- **评价指标**：Recall@K（R@K）和 Mean Recall@K（mR@K），K ∈ {20, 50, 100}
- **任务**：SGDET、SGCLS、PREDCLS
- **实验环境**：Adam 优化器，batch size 4，初始学习率 backbone 0.0001 / MPL 0.0003，每 5 epoch 衰减 0.1
- **消融实验**：模块消融、原型数量 K 消融

## 实验结果

### VG 数据集（与 SOTA 对比）

| 任务 | R@20 | R@50 | R@100 | Mean |
|------|------|------|-------|------|
| **SGDET** | 37.6 | 42.2 | 28.8 | — |
| **SGCLS** | 48.0 | 49.2 | 39.8 | — |
| **PREDCLS** | 73.3 | 75.1 | 66.4 | — |
| **Average** | — | — | — | **54.2** |

> **对比基线**：PE-Net (54.2 vs 46.4 mean)、GB-Net (54.2 vs 44.7 mean)、KEM (54.2 vs 44.9 mean)、TXM (54.2 vs 45.0 mean)、VS³ (54.2 vs 41.9 mean)。**所有任务均取得 SOTA**。

### Open Images V6 数据集

| 指标 | Our method | 最佳基线 |
|------|-----------|----------|
| mR@50 | **43.98** | 42.43 (BGNN+SCR) |
| R@50 | **76.34** | 75.21 (BGNN+SCR) |
| wmAP rel | **37.11** | 36.98 (SGTR) |
| wmAP phr | **40.55** | 38.73 (SGTR) |
| wtd score | **44.43** | 42.99 (RelTR) |

### 消融实验（SGDET mR@50/mR@100）

| 设定 | mR@50 | mR@100 |
|------|-------|--------|
| Full method | **21.2** | **22.3** |
| w/o 多原型（单原型） | 18.8 | 19.8 |
| TOT → 传统 OT | 19.1 | 20.1 |
| w/o L_ICS & L_ICC | 19.7 | 20.7 |
| w/o L_ICS | 20.9 | 21.9 |
| w/o L_ICC | 20.7 | 21.7 |

> **关键发现**：TOT 比传统 OT 提升约 +1.1~+2.2 mR；多原型 (K=3) 比单原型 (K=1) 提升 +1.5~+1.7 mR；L_ICS 和 L_ICC 均有独立贡献。

### 原型数量 K 消融

| K | mR@50 | mR@100 |
|---|-------|--------|
| 1 | 19.7 | 20.6 |
| 2 | 20.1 | 21.1 |
| **3** | **21.2** | **22.3** |
| 4 | 19.9 | 20.9 |
| 5 | 19.3 | 20.2 |

> **K=3 最优**：更大的 K 引入噪声，性能下降。

## 定性分析

- **图 4**：展示 6 个成功纠正分类偏见的案例，如将"lying on"纠正为"riding"
- **图 5**：可视化 riding 类别的 3 个原型匹配结果（骑马、骑自行车、冲浪），验证原型的语义可解释性
- **图 6**：t-SNE 可视化显示多原型空间比单原型空间具有更好的类别可分性和类内紧致性

## 与相关方法的联系

- **PE-Net**：也使用原型学习，但 PE-Net 是单原型 + 嵌入空间对齐，本文首次引入多原型
- **RA-SGG**：也涉及多原型，但本文是首个提出完整多原型 C-SGG 框架的工作
- **TOT**：新颖地将 triple-wise 关系引入 OT 匹配，区分于传统 predicate-wise OT

## 局限

- 原型数量 K=3 通过实验确定，缺乏理论指导
- 多原型会增加参数量和计算开销（训练 15-16 小时）
- 在 mR 指标上仍有较大提升空间（SGDET mR@50 = 21.2，远低于 Recall @50 = 42.2），长期尾谓词处理仍有不足
