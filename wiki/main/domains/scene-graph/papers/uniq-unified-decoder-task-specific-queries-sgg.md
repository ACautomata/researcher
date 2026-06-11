---
title: "UniQ: Unified Decoder with Task-specific Queries for Efficient Scene Graph Generation"
tags:
  - scene-graph-generation
  - efficient
  - unified-decoder
  - one-stage
  - ACM-MM-2024
created: 2026-06-10
source: https://arxiv.org/pdf/2501.05687
confidence: full-paper
authors:
  - Xinyao Liao
  - Wei Wei
  - Dangyang Chen
  - Yuanyuan Fu
venue: ACM MM 2024
---

## Paper Info

- **Title**: UniQ: Unified Decoder with Task-specific Queries for Efficient Scene Graph Generation
- **Venue**: ACM MM 2024
- **Code**: None
- **Backbone**: ResNet-101
- **Dataset**: Visual Genome (VG150)

## Abstract

One-stage SGG 面临**弱纠缠**问题：三元组需要耦合特征（关系推理）和解耦特征（分类定位）。UniQ 提出统一 decoder + 任务特定 query（STS）范式：三种 query（subject/object/predicate）输入共享 decoder，通过关系感知查询融合（RQ）和三重组自注意力（TSA）建模耦合关系。AP50 28.6，参数量仅 66.8M（比 SOTA 少 ≥28%）。

## Method

### 核心问题

One-stage SGG 需要同时建模：
- **耦合特征**：三元组内共享，用于关系推理
- **解耦特征**：每个子任务独有，用于精确定位/分类

现有方法要么单一 decoder 缺耦合（PSGTR），要么多 decoder 缺解耦（PSGFormer）。

### STS 范式架构

1. **三种任务特定 query**：Q_s（subject）, Q_o（object）, Q_p（predicate）
2. **关系感知查询融合（RQ）**：每层 decoder 前 MLP 融合三组查询
3. **耦合三重组自注意力（TSA）**：reshape 为三元组序列（3, bs×N, d），建模三元组内相互影响
4. **解耦并行解码**：三组 query 沿 batch 拼接，共享 decoder 参数

### 训练策略

- Set prediction（匈牙利匹配），**K=3** group queries（Group DETR 风格）
- 无偏重加权：α=0.07, β=0.75

## Experiments

### VG150 主要结果

| 指标 | UniQ (biased) | UniQ†♦ (unbiased) |
|------|:---:|:---:|
| AP50 | 28.6 | 28.4 |
| mR@20/50/100 | 6.3/8.5/9.6 | 11.3/16.8/21.1 |
| R@20/50/100 | 25.2/30.5/33.2 | 20.1/30.0/36.2 |
| hR@20/50/100 | 10.2/13.3/14.9 | 14.5/21.5/26.7 |
| Params | **66.8M** | **66.8M** |

### 与 SOTA 对比

- mR@50/100 超越 IterSG†♦ 0.5/0.8
- hR@20/50/100 均为 one-stage 最佳
- 参数量减少 ≥28%（vs IterSG 93.2M, SGTR 166.5M）

### 零样本 / No-graph

| 方法 | zs-R@50 | zs-R@100 | ng-R@50 | ng-R@100 |
|------|:---:|:---:|:---:|:---:|
| UniQ (biased) | **2.8** | **3.9** | **34.0** | **38.6** |
| UniQ♦ (unbiased) | **3.2** | **4.5** | 32.1 | 37.6 |

### 消融

- STS vs TTS（三 decoder）：性能相当，参数少 **25%**
- **RQ 最重要**：去掉 RQ 后 R@100 ↓3.3
- TSA 仅 +1.3M 参数，R@20 ↑2.2

## Results

- **66.8M** 参数（≥28% fewer）
- **AP50 28.6**，有偏 R@20 为所有方法中最高
- zs-R/ng-R 均最优
- STS 范式可迁移到多 decoder 架构（如 IterSG）

## Limitations

1. 仅在 VG150 评估
2. Reweighted loss 比 TDE/GCL 等去偏方法改进有限
3. K≥3 时 mR@K 提升停滞

## Connections

- **PSGTR** 和 **PSGFormer**、**IterSGG** — one-stage SGG 对比基线
- **Group DETR** — one-to-many assignment 借鉴
- **SGTR** / **Relationformer** — 参数量显著更少

## Provenance

- **Source**: arXiv 2501.05687
- **Venue**: ACM MM 2024
- **Evidence level**: full-paper
