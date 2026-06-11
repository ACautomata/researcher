---
title: "SceneGraphFusion: Incremental 3D Scene Graph Prediction from RGB-D Sequences"
type: paper
domain: scene-graph
status: active
created: 2026-06-10
updated: 2026-06-10
tags:
  - 3d-scene-graph
  - scene-graph-generation
  - incremental
  - rgb-d
  - CVPR-2021
  - graph-neural-network
  - attention
raw_sources:
  - raw/sources/2021-06-01-scenegraphfusion-incremental-3d-scene-graph-prediction.pdf
  - raw/sources/2021-06-01-scenegraphfusion-incremental-3d-scene-graph-prediction.txt
paper:
  title: "SceneGraphFusion: Incremental 3D Scene Graph Prediction from RGB-D Sequences"
  authors:
    - Shun-Cheng Wu
    - Johanna Wald
    - Keisuke Tateno
    - Nassir Navab
    - Federico Tombari
  year: 2021
  venue: CVPR 2021
  arxiv: null
  doi: null
  project: "https://shunchengwu.github.io/SceneGraphFusion"
  code: null
classification:
  label: 3d-scene-graph
  task:
    - Incremental 3D Scene Graph Generation
    - 3D Panoptic Segmentation
    - 3D Semantic Segmentation
  method_family: Graph Neural Network
  modality: RGB-D
  datasets:
    - 3RScan
    - 3DSSG
    - ScanNet v2
  metrics:
    - Recall@K (R@1, R@3, R@50, R@100)
    - Panoptic Quality (PQ)
    - Segmentation Quality (SQ)
    - Recognition Quality (RQ)
    - mean IoU
    - mean Average Precision (mAP)
evidence_level: full-paper
---

# SceneGraphFusion: Incremental 3D Scene Graph Prediction from RGB-D Sequences

## Citation

> Wu, S.-C., Wald, J., Tateno, K., Navab, N., & Tombari, F. (2021). SceneGraphFusion: Incremental 3D Scene Graph Prediction from RGB-D Sequences. *CVPR 2021*.

## One-Sentence Contribution

提出首个从 RGB-D 序列**增量**构建 3D 场景图的方法，通过图神经网络融合多帧预测，支持以 35Hz 实时运行并在场景增长时持续改进。

## Problem Setting

- **输入**：RGB-D 图像序列（来自移动摄像头）
- **输出**：全局一致的 3D 场景图，包含对象节点、语义标签和谓词关系（如 "standing on"、"attached to"）
- **挑战**：
  - 部分遮挡和不完整的几何信息（物体形状随时间变化）
  - 多帧预测融合时的一致性问题
  - 需要实时/增量处理，而非离线全局优化
- **场景**：室内环境，基于增量式几何分割（使用 [46] 的 geometric segmentation）

## Method

### 整体流程

1. **几何分割**：从 RGB-D 序列增量构建几何分割（geometric segments）
2. **特征提取**：对每个 segment 提取 PointNet 特征
3. **图构建**：将 segments 视为节点，构建图结构
4. **GNN 推理**：通过图神经网络（GNN）预测节点语义和边关系
5. **融合机制**：合并相同对象实例的节点，随新 segment 发现自然增长和改进

### 核心组件

- **PointNet 特征聚合**：从 primitive scene components 聚合 3D 特征
- **GNN 主干**：用于推理节点间关系和语义
- **Feature-wise Attention (FAT)**：提出的新注意力机制，针对增量重建场景中图数据的部分和缺失特性设计
  - FAT 显著优于 GAT 和 SDPA 等现有注意力机制（Table 2 验证）
- **融合机制（Fusion）**：从多个 RGB-D 帧的增量预测中融合，提升全局一致性
- **谓词损失（L_pred）**：联合学习关系能够提升对象分类效果（Table 3）

### FAT Attention

FAT 是论文的核心设计创新，用于处理增量 3D 场景中图结构部分和不完整的挑战。Table 2 显示 FAT（Ours FAT (f)）在 Relationship R@1 上达到 0.55，远超 GAT (0.12) 和 SDPA (0.39)。

## Experiments

### 数据集

- **3RScan**：包含 RGB-D 序列的室内数据集，用于增量设置
- **3DSSG**：3RScan 的 3D 场景图标注，含 160 个对象类和 26 个谓词类（完整实验）；减少版本含 20 个 NYUv2 对象类和 8 个谓词类（增量实验）
- **ScanNet v2**：用于 3D 语义/全景分割评估

### Baseline 方法

- **3DSSG [54]**：3D 场景图预测 baseline（无注意力）
- **PanopticFusion [31]**：3D 全景分割 baseline
- **SemanticFusion [29]**, **ProgressiveFusion [36]**, **FusionAware [60]**：增量语义分割 baseline
- **GAT [52]**, **SDPA [51]**：替代注意力机制消融

### 训练设置

- 架构：PointNet + GNN + FAT Attention
- 优化器、学习率、batch size、epoch 数等超参详情见论文附录
- 数据生成流程见 Sec. 5
- 硬件：具体信息在论文中有所描述（支持 CPU 上 35Hz 实时运行）

### 评估协议

- **场景图预测**：采用 top-n 评估指标（R@1, R@3, R@50, R@100），遵循 3DSSG [54] 协议
  - Relationship score = object × subject × predicate 概率乘积
  - Object 和 predicate 指标直接基于分类分数计算
- **全景分割**：Panoptic Quality (PQ), Segmentation Quality (SQ), Recognition Quality (RQ)，遵循 [22] 协议
- **语义分割**：mIoU 和 mAP

### 消融实验

- **FAT vs. 其他注意力机制**（GAT, SDPA, none）：Table 2
- **有无谓词损失 L_pred**：Table 3（使用 L_pred 后 R@1 从 0.26→0.55）
- **full scene vs. incremental**：Table 2 中 (f) vs. (i) 对比
- **有无融合机制**：Table 2 中 6⃝ vs. 7⃝ 对比

## Results

### 场景图预测（3DSSG，完整场景，Ground Truth 实例，160 对象/26 谓词）

SceneGraphFusion 在关系预测上以**+0.45 / +0.21**（R@50 / R@100）大幅超越 3DSSG [54]。

### 场景图预测（3RScan/3DSSG，几何分割，20 对象/8 谓词）

| 方法（Attention） | 场景 | Relationship R@1 | Relationship R@3 | Object R@1 | Object R@3 | Predicate R@1 | Predicate R@2 |
|---|---|---|---|---|---|---|---|
| 3DSSG (none) | 完整 | 0.38 | 0.59 | 0.61 | 0.85 | 0.83 | 0.98 |
| Ours (none) | 完整 | 0.41 | 0.62 | 0.62 | 0.88 | 0.84 | 0.98 |
| Ours (GAT) | 完整 | 0.12 | 0.22 | 0.25 | 0.64 | 0.85 | 0.98 |
| Ours (SDPA) | 完整 | 0.39 | 0.62 | 0.62 | 0.87 | 0.85 | 0.98 |
| **Ours (FAT)** | **完整** | **0.55** | **0.78** | **0.75** | **0.93** | **0.86** | **0.98** |
| Ours (FAT) | 增量 | 0.51 | 0.67 | 0.78 | 0.94 | 0.77 | 0.98 |
| Ours Fusion (FAT) | 增量 | 0.52 | 0.70 | 0.79 | 0.94 | 0.78 | 0.98 |

**关键发现**：
- FAT 在 Relationship R@1 (0.55) 上远超 3DSSG (0.38)、GAT (0.12) 和 SDPA (0.39)
- 增量推理（i）接近完整场景（f）性能，融合机制进一步提升
- GAT 在该 3D 场景图任务上表现灾难性差（仅 0.12 R@1）

### 谓词损失消融（Table 3）

| 设置 | Relationship R@1 | Relationship R@3 | Object R@1 | Object R@3 | Predicate R@1 | Predicate R@2 |
|---|---|---|---|---|---|---|
| Ours without L_pred | 0.26 | 0.36 | 0.62 | 0.87 | 0.59 | 0.75 |
| Ours with L_pred | **0.55** | **0.78** | **0.75** | **0.93** | **0.86** | **0.98** |

对象分类从 0.62 提升至 0.75，验证联合学习关系可显著提升对象分类。

### 3D 全景分割（ScanNet v2）

| 方法 | PQ | SQ | RQ |
|---|---|---|---|
| PanopticFusion [31] | 33.5 | 73.0 | 45.3 |
| Ours (NN mapping) | 31.5 | 72.9 | 42.2 |
| **Ours (skipped missing)** | **36.3** | **76.1** | **46.8** |

跳过未重建区域后，SceneGraphFusion 的 PQ (36.3) 和 SQ (76.1) 超越 PanopticFusion。

### 运行时

- **35Hz** 在 CPU 上运行（增量语义分割方法中领先，具体比较见论文 Sec. 6.3 和附录）

## Limitations

- 全景分割表现受限于未重建场景区域（缺失几何导致性能下降——NN mapping 版本 PQ 低于 PanopticFusion）
- 依赖外部几何分割算法 [46] 的质量，不稳定段会被排除
- 谓词仅支持支撑关系（support predicates），部分关系和低频关系被忽略
- 实验仅在 20 个对象类（增量设置）和 160 个对象类（完整场景）上进行，未测试更大规模对象集
- GAT 在该场景中表现极差，表明注意力机制的选择对 3D 图数据高度敏感

## Reusable Claims

- **Claim**: FAT 注意力机制设计了针对 3D 增量场景图数据中图结构部分和缺失特性的专用方案，在 Relationship R@1 上达到 0.55，远超 GAT (0.12) 和 SDPA (0.39)。
  - Evidence: Table 2 (SceneGraphFusion 论文)
  - Confidence: High

- **Claim**: 联合学习关系（谓词损失 L_pred）可使对象分类 R@1 从 0.62 提升至 0.75（+0.13）。
  - Evidence: Table 3 (SceneGraphFusion 论文)
  - Confidence: High

- **Claim**: 增量 3D 场景图预测可达 35Hz 实时运行，同时性能接近完整场景离线处理。
  - Evidence: Sec. 6.3 (SceneGraphFusion 论文)
  - Confidence: High

## Connections

- **3DSSG [54]**（Wald et al. 2020）：提供 3D 场景图数据标注和预测 baseline，SceneGraphFusion 在此基础上提升显著
- **PanopticFusion [31]**：3D 全景分割 baseline，SceneGraphFusion 的副产物全景分割与之力争
- **Incremental 3D Scene Graph Prediction from RGB Sequences**（后续工作）：从仅 RGB 序列做增量 3D 场景图预测
- **ZING-3D**（2025）：基于视觉语言模型的零样本增量 3D 场景图方法
- **3D Scene Graph**（Armeni et al. 2019, ICCV）：3D 场景图概念的开创性工作

## Open Questions

- FAT 注意力机制能否泛化到其他 3D 图推理任务（如 3D 点云关系检测）？
- 将 SceneGraphFusion 与 SLAM 系统更紧密集成能否完全避免外部几何分割的依赖？
- 在更大规模对象类别（>160）和更多样化谓词上的表现如何？
- 增量融合机制的最新改进方向（如基于 Transformer 的时序融合）能否进一步提升性能？

## Provenance

- Raw source: `raw/sources/2021-06-01-scenegraphfusion-incremental-3d-scene-graph-prediction.pdf` (CVPR 2021 open access PDF)
- Extracted text: `raw/sources/2021-06-01-scenegraphfusion-incremental-3d-scene-graph-prediction.txt`
- Evidence level: full-paper（全文 PDF 提取，11 页包括所有实验和分析）
- Access date: 2026-06-10
