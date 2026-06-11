---
title: Salient Temporal Encoding for Dynamic Scene Graph Generation
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - dynamic-scene-graph
  - temporal-encoding
  - saliency-attention
  - video-scene-graph
  - action-recognition
  - action-genome
  - sparse-temporal-connections
  - arxiv-2025
raw_sources:
  - ../../../sources/scene-graph/2025-arXiv-Salient-Temporal-Encoding-for-Dynamic-SGG.pdf
  - ../../../sources/scene-graph/2025-arXiv-Salient-Temporal-Encoding-for-Dynamic-SGG.txt
paper:
  title: Salient Temporal Encoding for Dynamic Scene Graph Generation
  authors:
    - Zhihao Zhu
  year: 2025
  venue: arXiv 2025
  arxiv: null
  doi: null
  code: null
  project: null
  affiliations:
    - Carnegie Mellon University
classification:
  label: STRE
  task:
    - Dynamic Scene Graph Generation
    - Spatial-Temporal Scene Graph Generation
    - Video Scene Graph Generation
  method_family:
    - Saliency Attention
    - Temporal Relation Encoding
    - Sparse Temporal Connection
    - Graph Convolution Network
  modality:
    - Video (RGB)
  datasets:
    - Action Genome
    - Charades
  metrics:
    - R@K
    - mR@K
    - mAPrel
    - wmAPrel
    - mAP
evidence_level: full-paper
---

# Salient Temporal Encoding for Dynamic Scene Graph Generation

## Citation

Zhihao Zhu. "Salient Temporal Encoding for Dynamic Scene Graph Generation." arXiv 2025.

## One-Sentence Contribution

提出 **STRE（Salient Temporal Relation Encoder）**，通过**选择性稀疏时序连接**（Saliency Attention）仅连接时域相关的物体对，并显式编码时域关系为场景图中的显式边，突破现有方法全连接稠密时序连接的局限，同时提升 Scene Graph Detection（+4.4% R@20）和下游 Action Recognition（+0.6% mAP）的性能。

## Problem Setting

**出发点**：现有动态场景图生成方法（如 STTran、APT）在帧间所有物体对上构建稠密时序连接，但**并非所有时序连接都编码有意义的时序动态**。稠密时序图引入大量噪声，且隐式编码难以解释。

**核心挑战**：
1. 如何自动识别哪些物体对之间存在有意义的时序交互？
2. 如何将时序关系表示为显式边而非聚合进空间特征的隐式表征？
3. 稀疏时序连接能否同时提升性能和效率？

**任务定义**：给定视频帧序列 V = {I₁, I₂, ..., I_T}，输出空间-时序场景图 G = (V, Eₛ, Eₜ)，其中 V 为物体节点集，Eₛ 为帧内空间关系边，Eₜ 为帧间时序关系边。

## Method

### 整体框架（三阶段）

1. **Spatial Scene Graph Proposal**：对每帧提取物体感知特征，通过 permutation-invariant structured prediction (PISP) 模块生成空间场景图。场景图经 GCN 更新节点嵌入，聚合局部空间上下文。

2. **Saliency Attention（核心创新）**：稀疏选择帧间需要建立时序连接的物体对。
   - 输入：上一帧更新后的 GCN 节点特征，当前帧检测到的物体特征
   - 对每个当前帧物体，计算其与上一帧所有物体特征的点积相似度
   - 选择 top-K 最相似的上一帧物体为其建立时序连接
   - 当 K=1 时效果最优（每个当前帧物体只连接 1 个最相关的上一帧物体）
   - **与 tracking 的区别**：tracking 只连接同类别、空间最近的物体；Saliency Attention 可以连接不同类别的物体对（如"人"↔"衣服"），只要它们共同参与同一事件

3. **Temporal Relation Encoder**：对通过 Saliency Attention 建立的稀疏时序边，使用两层 MLP 预测时序关系标签，输出的时序关系向量作为显式边特征注入场景图中

### STRE vs DTRE

- **STRE（稀疏）**：K=1，每个物体只连接 1 个上一帧物体 → 平均 1 条时序连接/物体
- **DTRE（稠密）**：修改 Saliency Attention 为全连接 → 平均 8 条时序连接/物体

### Action Recognition 应用

将 STRE 预测的空间-时序场景图构建 **Spatial-Temporal Scene Graph Feature Bank (ST-SGFB)**，输入 LFB（Long-Term Feature Bank）模型进行动作分类。

## Key Insights

1. **稀疏优于稠密**：STRE[K=1] 在所有指标上优于 DTRE（全连接），SGDet-R@20 提升 1.0%。说明多数帧间物体对不包含有用的时序信息，全连接引入噪声。
2. **跨类别时序连接**：Saliency Attention 能连接不同类别的物体（如"人"↔"衣服"），这是传统 tracking 方法无法做到的。
3. **显式时序编码**：将时序关系作为显式边而非隐式特征，增强了可解释性同时提升性能。
4. **显著效率优势**：STRE 参数量 21.7M、FLOPs 120M/帧，对比 STTran 的 91.8M 参数和 577M FLOPs/帧。

## Experiments

### Datasets

- **Action Genome**：基于 Charades 的视频级场景图标注，含 ~10K 视频，234 类时空关系
- **Charades**：动作识别数据集，9,848 视频，157 动作类，46 物体类型

### Evaluation Protocols

三种场景图评估协议（带约束）：
- Predicate Classification (PredCls)：使用 GT 物体检测框和标签
- Scene Graph Classification (SGCls)：使用 GT 物体检测框
- Scene Graph Detection (SGDet)：使用预测物体检测框

附加平衡指标：Mean Recall (mR)、mAPrel、wmAPrel

### Main Results

#### Spatial-Temporal Scene Graph Generation（Action Genome 数据集）

**Table 1 — With-constraint Recall@20 对比**

| 方法 | PredCls-R@20 | SGCls-R@20 | SGDet-R@20 |
|------|:-----------:|:---------:|:---------:|
| **Spatial methods** | | | |
| VRD | 54.7 | 33.3 | 24.5 |
| Motif Freq | 65.1 | 41.9 | 31.4 |
| MSDN | 68.5 | 45.1 | 32.4 |
| VCTREE | 69.3 | 45.3 | 32.6 |
| RelDN | 69.5 | 45.4 | 32.8 |
| GPS-Net | 69.9 | 46.5 | 33.1 |
| **Spatial-Temporal methods** | | | |
| STTran | 71.8 | 47.5 | 34.1 |
| APT | **73.8** | 48.9 | 36.1 |
| **STRE (ours)** | 71.4 | 48.5 | **38.4** |

**Table 2 — Mean Recall@50 对比**

| 方法 | PredCls-mR@50 | SGCls-mR@50 | SGDet-mR@50 |
|------|:------------:|:-----------:|:----------:|
| Freq Prior | 63.6 | 36.6 | 34.0 |
| G-RCNN | 61.3 | 38.2 | 34.9 |
| RelDN | 63.4 | 41.9 | 39.5 |
| TRACE | 65.3 | 43.2 | 40.1 |
| **STRE (ours)** | **67.5** | **44.2** | **42.7** |

**Table 3 — mAPrel / wmAPrel 对比**

| 方法 | PredCls-wmAPr | SGCls-wmAPr | SGDet-wmAPr |
|------|:------------:|:-----------:|:----------:|
| Freq Prior | 65.9 | 22.6 | 15.5 |
| G-RCNN | 70.8 | 22.5 | 15.5 |
| RelDN | 72.2 | 23.8 | 15.9 |
| TRACE | 75.2 | 24.6 | 16.5 |
| **STRE (ours)** | **80.1** | **26.7** | **17.9** |

#### Sparse vs Dense Comparison

**Table 4 — 稀疏 vs 稠密时序连接**

| 方法 | PredCls-R@20 | SGCls-R@20 | SGDet-R@20 |
|------|:-----------:|:---------:|:---------:|
| PISP（无时序） | 70.9 | 48.0 | 33.1 |
| **STRE[K=1]** | **71.4** | **48.5** | **38.4** |
| STRE[K=2] | 71.4 | 48.4 | 38.1 |
| STRE[K=3] | 71.3 | 48.4 | 38.0 |
| DTRE（稠密） | 71.0 | 48.2 | 37.4 |

#### Efficiency Comparison

**Table 5 — 模型效率**

| 方法 | #Params (M) | #FLOPs (M)/frame |
|------|:----------:|:---------------:|
| STTran | 91.8 | 577 |
| **STRE** | **21.7** | **120** |

#### Saliency Attention vs Tracking

**Table 6 — Saliency Attention vs Tracking**

| 方法 | PredCls-R@20 | SGCls-R@20 | SGDet-R@20 |
|------|:-----------:|:---------:|:---------:|
| Tracking-Based | 70.7 | 48.0 | 37.8 |
| **STRE (Saliency Attn)** | **71.4** | **48.5** | **38.4** |

#### Action Recognition（Charades 数据集）

**Table 7 — Action Recognition mAP 对比**

| 方法 | Backbone | mAP |
|------|----------|:--:|
| STAG | R50-I3D | 37.2 |
| I3D+NL | R101-I3D-NL | 37.5 |
| STRG | R101-I3D-NL | 39.7 |
| SlowFast | R101 | 42.1 |
| LFB | R101-I3D-NL | 42.5 |
| ASF | R101-I3D-NL | 44.2 |
| SGFB | R101-I3D-NL | 44.3 |
| OR2G | R101-I3D-NL | 44.9 |
| S-SGFB（spatial only） | R101-I3D-NL | 45.1 |
| **ST-SGFB（ours）** | **R101-I3D-NL** | **45.5** |

### Key Quantitative Results

| 指标 | 数值 | 对比 baseline |
|------|:---:|:------------:|
| SGDet-R@20 | **38.4** | STTran 34.1 (+4.3), APT 36.1 (+2.3) |
| SGDet-mR@50 | **42.7** | TRACE 40.1 (+2.6) |
| SGDet-wmAPr | **17.9** | TRACE 16.5 (+1.4) |
| PredCls-wmAPr | **80.1** | TRACE 75.2 (+4.9) |
| Action Recog. mAP (ST-SGFB) | **45.5** | SGFB 44.3 (+1.2), LFB 42.5 (+3.0) |
| STRE[K=1] vs DTRE | +1.0 (SGDet-R@20) | 稀疏优于稠密 |
| 参数量 | **21.7M** | STTran 91.8M (减少 76%) |
| FLOPs/帧 | **120M** | STTran 577M (减少 79%) |

## Limitations

1. **PredCls 提升有限**：在 PredCls 上只比 STTran 提升 0.8%@R20，说明时序信息对关系分类的帮助有限于具有预知物体检测框的前提。
2. **仅两帧间时序连接**：当前只在相邻帧之间建立时序连接，未来可探索跨多帧的长程时序连接。
3. **单作者论文**：来自 CMU 的独立工作，未见后续复现或扩展。

## Links and Cross-References

- 相关方法：[STTran: Spatial-Temporal Transformer for Dynamic Scene Graph Generation](sttran-spatial-temporal-transformer-dynamic-scene-graph-generation.md) — 基线方法，稠密时序 Transformer
- 相关方法：[APT: Anticipatory Pre-Training for Dynamic Scene Graph Generation](apt-anticipatory-pre-training-dynamic-sgg.md) — 使用额外无监督数据预训练
- 相关方法：[FDSG: Forecasting Dynamic Scene Graphs](fdsg-forecasting-dynamic-scene-graphs.md) — 时序动态场景图预测
- 相关方法：[OED: One-stage End-to-End Dynamic Scene Graph Generation](oed-one-stage-end-to-end-dynamic-scene-graph-generation.md) — 单阶段动态 SGG
- 相关方法：[Motion-aware Contrastive Learning for Temporal Panoptic SGG](motion-aware-contrastive-learning-temporal-panoptic-sgg.md) — 时序全景 SGG
- 下游任务：Action Recognition on Charades
