---
title: "Improving Scene Graph Generation with Superpixel-based Interaction Learning"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - scene-graph-generation
  - superpixel
  - interaction-learning
  - fine-grained-interaction
  - ACM-MM-2023
  - plug-and-play
  - clustering
raw_sources:
  - ../../../raw/sources/2023-ACM-MM-Improving-Scene-Graph-Generation-with-Superpixel-based-Interaction-Learning.pdf
  - ../../../raw/sources/2023-ACM-MM-Improving-Scene-Graph-Generation-with-Superpixel-based-Interaction-Learning.txt
related_pages:
  - prototype-based-embedding-network-scene-graph-generation.md
  - is-ggt-iterative-scene-graph-generation-with-generative-transformers.md
evidence_level: full-paper
paper:
  title: "Improving Scene Graph Generation with Superpixel-Based Interaction Learning"
  authors:
    - Jingyi Wang
    - Can Zhang
    - Jinfa Huang
    - Botao Ren
    - Zhidong Deng
  year: 2023
  venue: "Proceedings of the 31st ACM International Conference on Multimedia (MM '23), Ottawa, ON, Canada"
  arxiv: "2308.02339"
  doi: "10.1145/3581783.3611889"
  code: null
  project: null
classification:
  label: "Superpixel-based Interaction Learning for SGG"
  task:
    - Scene Graph Generation (SGG)
    - Predicate Classification (PredCls)
    - Scene Graph Classification (SGCls)
    - Scene Graph Detection (SGGen)
  method_family:
    - Superpixel-based Feature Extraction
    - Intra-Entity Interaction Modeling
    - Cross-Entity Interaction (Transformer Attention)
    - Plug-and-Play Block
  modality:
    - RGB Image (2D)
  dataset:
    - Visual Genome
    - Open Images V6
  backbone:
    - Faster R-CNN (ResNeXt-101-FPN)
---

# Improving Scene Graph Generation with Superpixel-based Interaction Learning

## 概述

本文提出**Superpixel-based Interaction Learning (SIL)**，一种通用即插即用的范式，将场景图生成中的粗粒度框级交互（box-level interaction）提升为细粒度超像素级交互（superpixel-level interaction）。核心思路是将图像视为一组点（point set），通过聚类算法聚合成超像素，在超像素层面建模实体内部（intra-entity）和跨实体（cross-entity）的交互。

SIL 可以无缝集成到任何现有的框级 SGG 方法中。在 Visual Genome 和 Open Images V6 两个基准上，SIL 稳定提升所有基线的性能（PredCls mR 平均提升 +2.0%），并超越此前 SOTA。

## 动机与挑战

- 现有 SGG 方法普遍使用检测器输出的**框级特征**（box-level features）建模实体间关系
- 框级交互存在两个根本缺陷：
  1. **实体层面**：框级特征无法区分实体内部不同子区域（如 "person" 框内的头/手/躯干），丢失了重要的细粒度信息
  2. **关系层面**：框级交互无法捕获关系发生的关键子区域，并且会被冗余背景信息干扰（例如 "holding" 发生在手和物体接触的区域，而非整个框）
- 此前尚未有工作将超像素引入场景图生成领域来解决这一粗粒度问题

## 方法

### SIL Block 三大组件

SIL 将原始框级特征转换为超像素级特征，并注入细粒度交互，整体流程如图 2 所示。

### 1. Superpixel Clustering（超像素聚类）

- 将图像特征图视为点集：$F \in \mathbb{R}^{M \times D}$（$M$ 为空间位置数，$D$ 为特征维度）
- 使用上下文聚类（Context Clustering）[37] 算法将 $M$ 个点聚类为 $C$ 个超像素，获得聚类中心特征 $T \in \mathbb{R}^{C \times D}$
- 每个聚类中心代表一个超像素，覆盖图像中相似视觉特征的连续或非连续区域
- 默认聚类中心数 $C=49$

### 2. Intra-Entity Interaction（实体内部交互）

- 根据边界框将超像素分配给对应实体：第 $k$ 个实体内的超像素集合为 $P^{BT}_k$
- 计算实体参考特征 $g_k$（框内特征均值或 backbone 对应位置特征），见公式 (4)
- 为每个超像素分配权重 $w_{(j,k)}$，衡量该超像素对实体 $k$ 的重要性：
  $$w_{(j,k)} = \frac{\exp(F^{SC}_j \cdot g_k^\top)}{\sum_{j'} \exp(F^{SC}_{j'} \cdot g_k^\top)}$$
- 加权融合更新超像素特征：$F^{IN}_k = \{F^{SC}_j + g_k \times w_{(j,k)}\}$
- 通过加权区分同一实体内的不同子区域，实现实体内部的细粒度交互

### 3. Cross-Entity Interaction（跨实体交互）

- 使用 **Multi-Head Self-Attention**（Transformer Encoder）在所有超像素之间建模跨实体交互：
  $$F^{CR} = \text{MultiHead}(F^{IN}, F^{IN}, F^{IN})$$
- 每个 head 的 embedding 维度为 32，默认使用 2 层 encoder
- 将跨实体交互后的特征 $F^{CR}$ 分配回对应空间位置，得到 SIL 输出 $F^{SIL}$

### 整体架构

- SIL 采用**层级式超像素交互学习网络**，包含多个 SIL block
- 交互程度逐层加深（默认 2 层 cross-entity interaction）
- SIL block 输出的 $F^{SIL}$ 替换原始特征图，输入任意 relation prediction 模块

### 关键特性

- **即插即用**：SIL 不依赖特定 baseline 结构（RNN/GNN/GCN 均可）
- **无需额外标注**：仅基于无监督聚类，不引入额外监督信号
- **早期交互**：相比传统方法在 relation 模块才建模交互，SIL 在更早的特征提取阶段就注入交互信息

## 实验结果

### Visual Genome 主要结果（mR@K 指标）

#### Table 1: SIL 在 7 个 baseline 上的提升

| Method | PredCls mR@20 | PredCls mR@50 | PredCls mR@100 | SGCls mR@50 | SGCls mR@100 | SGGen mR@50 | SGGen mR@100 |
|--------|:-----------:|:-----------:|:-----------:|:---------:|:---------:|:---------:|:---------:|
| **MOTIFS+SIL** | 13.6 (+1.9) | 16.9 (+2.1) | 18.4 (+2.3) | 10.2 (+1.9) | 10.8 (+2.0) | 7.3 (+0.5) | 8.5 (+0.6) |
| **G-RCNN+SIL** | 15.3 (+1.8) | 18.1 (+1.4) | 19.4 (+2.0) | 10.7 (+1.6) | 11.1 (+1.5) | 6.9 (+0.8) | 7.6 (+0.9) |
| **KERN+SIL** | 16.0 (+1.3) | 18.8 (+1.8) | 21.0 (+1.6) | 10.5 (+1.5) | 11.7 (+1.7) | 6.9 (+0.6) | 7.9 (+0.6) |
| **VCTree+SIL** | 14.5 (+1.3) | 18.1 (+1.4) | 19.6 (+1.4) | 12.6 (+0.8) | 13.9 (+1.4) | 7.6 (+0.2) | 8.9 (+0.2) |
| **GPS-Net+SIL** | 19.1 (+1.7) | 23.8 (+2.5) | 25.2 (+2.4) | 13.2 (+1.4) | 14.0 (+1.4) | 9.1 (+0.4) | 10.4 (+0.6) |
| **BGNN+SIL** | 27.9 (+3.0) | 32.9 (+3.4) | 35.0 (+3.2) | 15.7 (+1.4) | 16.8 (+2.0) | 11.1 (+0.7) | 13.1 (+0.6) |
| **PE-Net+SIL** | 26.9 (+1.1) | 33.1 (+1.7) | 35.3 (+1.8) | 19.9 (+1.7) | 20.7 (+1.4) | 13.0 (+0.7) | 15.1 (+0.8) |

- PredCls 任务平均提升 **+2.0%** mR，最高单点提升 **+3.4%**（BGNN mR@50）
- 所有 7 个 baseline 在所有三个任务上均获得稳定提升，无退化情况

#### Table 2: 与 SOTA 方法对比

| Method | Type | PredCls mR@100 | SGCls mR@100 | SGGen mR@100 |
|--------|:----:|:------------:|:-----------:|:-----------:|
| VTransE [65] | Box-based | 15.8 | 8.7 | 6.1 |
| RelDN [66] | Box-based | 17.2 | 9.6 | 7.3 |
| GBNet-β [60] | Box-based | 24.0 | 13.4 | 8.5 |
| IS-GGT [20] | Box-based | 31.9 | 18.9 | 11.3 |
| IWSL [34] | Box-based | 32.1 | 18.9 | 15.9 |
| PE-Net [68] | Box-based | 33.5 | 19.3 | 14.3 |
| **Ours (PE-Net+SIL)** | **Superpixel-based** | **35.3** | **20.7** | **15.1** |

在 PredCls mR@100 上全面超越所有 SOTA 方法，达到 **35.3%**。

### Open Images V6 结果

| Method | R@50 | wmAPrel | wmAPphr | scorewtd |
|--------|:---:|:------:|:-------:|:-------:|
| MOTIFS+SIL | 72.3 (+0.7) | 30.4 (+0.5) | 31.8 (+0.2) | 39.4 (+0.5) |
| G-RCNN+SIL | 75.5 (+1.0) | 33.8 (+0.6) | 34.7 (+0.5) | 42.5 (+0.6) |
| GPS-Net+SIL | 75.7 (+0.9) | 33.9 (+1.0) | 34.9 (+0.9) | 42.7 (+1.0) |
| BGNN+SIL | 76.4 (+1.4) | 34.2 (+0.7) | 35.0 (+0.8) | 43.0 (+0.9) |
| PE-Net+SIL | 77.1 (+0.6) | 37.2 (+0.6) | 37.8 (+0.4) | 45.5 (+0.6) |

- SIL 在 OI V6 上也取得一致提升
- PE-Net+SIL 综合 scorewtd 达到 **45.5**，超越全部对比方法

### 消融实验

#### 组件消融（Table 4，PredCls on VG，Motif baseline）

| SC | IEI(w/weight) | CEI | mR@20 | mR@50 | mR@100 |
|:--:|:-----------:|:--:|:----:|:----:|:-----:|
| ✗ | ✗ | ✗ | 12.31 | 15.03 | 16.10 |
| ✓ | ✗ | ✗ | 12.59 | 15.54 | 16.75 |
| ✓ | ✓(no weight) | ✗ | 12.61 | 15.76 | 17.08 |
| ✓ | ✓(weighted) | ✗ | 13.16 | 16.40 | 17.70 |
| ✓ | ✓(w/o weight)* | ✓ | 13.12 | 16.52 | 17.78 |
| ✓ | ✓(weighted) | ✓ | **13.62** | **16.91** | **18.36** |

> \* IEI w/o weight 标记为 #，weighted IEI 标记为 

- 三个组件各有贡献，完整 SIL 实现最大提升（+1.31/+1.88/+2.26）
- 加权超像素比无权重版本进一步带来改善（最后两行对比）
- **Cross-Entity Interaction 贡献最大**：单独加上 CEI 带来 +0.85/+1.37/+1.60 提升

#### 聚类中心数影响

- 测试 4, 9, 25, 49, 81 个中心
- 性能随中心数增加小幅提升，SIL 对此不高度敏感
- 默认选用 **49** 作为性能-内存权衡

#### 交互深度影响

- 测试 0/1/2/3 层 cross-entity encoder
- 随层数从 0 增加到 2，性能逐步提升
- 3 层时因信息混淆而性能下降，默认选用 **2 层**

## 关键洞察

1. **超像素的首次引入**：将超像素概念引入 SGG 领域，将框级粗粒度交互提升到超像素级细粒度交互
2. **特征解耦**：通过聚类将粗粒度框特征解耦为多个超像素，增强实体表征的区分度
3. **跨实体注意力**：在超像素层面使用 transformer attention 建模跨实体交互，比在实体层面更精细
4. **即插即用**：SIL block 不依赖特定架构，可以无侵入地集成到任何现有 SGG 方法中
5. **无额外监督**：聚类和交互建模全部基于无监督方式，不依赖额外的标注或预训练
6. **广泛适用**：在 RNN (MOTIFS)、GNN (BGNN)、GCN (KERN) 等不同架构上均有效

## 局限与对比

- SIL 的聚类中心数为超参数（默认 49），不同场景可能需要调优
- 增加超像素数量会带来额外计算开销和显存消耗
- 与 IS-GGT（CVPR 2023）的选择性边缘处理不同，SIL 侧重于特征层面的细粒度增强而非图结构优化
- SIL 与 SQUAT（CVPR 2023）互补：SQUAT 关注边缘级四元注意力，SIL 关注超像素级特征建模
- 在 SGDet 任务上提升幅度（约 +0.5~0.9）相对 PredCls（约 +1.0~3.4）较小，说明实体检测误差对超像素级交互有一定干扰
