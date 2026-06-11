---
title: "Incremental 3D Semantic Scene Graph Prediction from RGB Sequences"
authors:
  - Shun-Cheng Wu
  - Keisuke Tateno
  - Nassir Navab
  - Federico Tombari
year: 2023
venue: CVPR 2023
arxiv: null
doi: null
code: "https://shunchengwu.github.io/MonoSSG"
domain: scene-graph
tags: [3d-scene-graph, incremental, rgb-only, sparse-slam, message-passing]
evidence_level: full-paper
status: active
task: 3D Semantic Scene Graph Prediction
method_family: [Incremental Entity Estimation, Message-Passing GNN]
modality: [RGB, sparse-point-cloud]
datasets: [3RScan]
metrics: [Recall, mRecall, AOS]
related_pages:
  - "../papers/3d-spatial-multimodal-knowledge-accumulation-scene-graph-prediction-point-cloud.md"
raw_source: raw/sources/2023-06-01-incremental_3d_scene_graph.pdf
created: 2026-06-08
updated: 2026-06-08
---

# Incremental 3D Semantic Scene Graph Prediction from RGB Sequences

## Citation

> Shun-Cheng Wu, Keisuke Tateno, Nassir Navab, Federico Tombari. "Incremental 3D Semantic Scene Graph Prediction from RGB Sequences." CVPR 2023.

## One-Sentence Contribution

提出首个仅依赖RGB图像序列的实时增量式3D语义场景图预测框架，通过置信度融合的增量实体估计和基于多视图特征的图神经网络，在3RScan数据集上超越现有方法。

## Problem Setting

从RGB图像序列中增量式预测全局一致的3D语义场景图（3D SSG）。输入为RGB图像+相机位姿（来自ORB-SLAM3），输出为随时间积累的一致3D场景图，包含实体（对象/结构）标签和实体间关系（支持关系等）。

挑战：
- 稀疏点云的非均匀分布导致实体融合困难
- 稀疏几何使节点表示不可靠
- 2D方法无法推理跨视角的关系

## Method

### 整体架构（增量式实体估计 + 场景图预测网络）

#### 1. 增量式实体估计（IEE）管线

- **Sparse Mapping**：ORB-SLAM3 重建稀疏点图
- **2D Entity Detection**：EntitySeg (ResNet50 backbone, COCO预训练+3RScan微调) 在关键帧上进行实例级分割
- **Oriented 3D BBox Extraction**：ApproxMVBB 从关联的3D点云计算有向3D边界框
- **Label Fusion**：**置信度融合方案** —— 不依赖重叠率（因稀疏点云分布不均），而是基于置信度权重融合来自多个视角的实体预测
  - 存储每个实体的概率估计 µ 和权重 ρ
  - 新预测到来时用 running average 更新
  - 权重上限 ρmax=100

#### 2. 场景图预测网络

- **Node Features**:
  - **Multi-view Feature**：对每个3D BBox，取视角最近的N帧，用ResNet18（ImageNet预训练，不微调）提取图像ROI特征 → 平均池化 → 实体特征
  - **Geometric Descriptor (gi)**：Gated geometric feature，使用gating机制控制几何信息流入节点特征
  - **Point Encoder**：vanilla PointNet（无learned feature transform）

- **Edge Features (Ri→j)**：
  - 实体i和j之间的相对位姿描述子（relative pose descriptor）
  - 编码两实体BBox中心连线向量和相对朝向

- **Message-Passing GNN**：
  - 使用feature-wise attention network (FAN) 加权相邻节点消息聚合
  - Message Passing层数：2
  - 节点和边特征通过MLP更新

- **Prediction**：
  - 节点分类：softmax
  - 边分类（单predicate）：softmax
  - 边分类（多predicate）：sigmoid + binary cross entropy

- **Fusion**：同IEE的running average融合多帧预测

### 关键设计对比

| 设计 | VGfM | Ours |
|------|------|------|
| 几何特征注入 | 直接拼接 | Gated（gate控制信息流） |
| 稀疏输入鲁棒性 | 下降 | 保持（gate可关闭不可靠信号） |
| 多视图特征 | 单帧 | 多帧平均池化 |

## Experiments

### 数据集
- **3RScan** dataset [60]
- 使用自定义train/test split（原始test split无场景图GT）
- 两种评估设置：
  - **Tbl. 1**：节点映射到20个NYUv2类别，8种predicate（7个支持关系+same part）
  - **Tbl. 2**：160个节点类别，26个predicate类别，多predicate估计

### 输入类型
三种输入比较（用不同分割方法产生实体）：
- **GT**：Ground Truth Segmentation [61]
- **Dense**：Geometric Segmentation [59]
- **Sparse**：论文提出的稀疏分割

### Baseline 方法
- **IMP** [66]：基于ROI裁剪图像特征的2D场景图方法 + 帧投票机制
- **VGfM** [15]：IMP扩展，加入几何特征和时序信息
- **3DSSG** [61]：3D场景图，用PointNet提取3D BBox特征
- **SGFN** [64]：3DSSG改进，加入attention和动态消息聚合

### 训练设置
- 所有方法在3RScan上从scratch训练至收敛
- EntitySeg: ResNet50 backbone, COCO预训练+3RScan微调
- Multi-view encoder: ResNet18, ImageNet预训练（不微调）
- Hyperparameters: τ=0.2, τC=0.5m, ρmax=100, message passing layers=2

### 评估指标
- **Recall** (top-1)：关系三元组(Rel.)、实体类别(Obj.)、predicate类别(Pred.)的recall
- **mRecall** (mean recall)：缓解类别不平衡影响
- **AOS** (Average Overlap Score)：增量标签关联评估

### 硬件
- CPU: Intel Core i7-8700 3.2GHz (12 threads)
- GPU: NVIDIA GeForce RTX 2080ti

## Results

### Table 1: 场景图预测（20 objects, 8 predicates）

| 输入 | 方法 | Recall Rel. | Recall Obj. | Recall Pred. | mRecall Obj. | mRecall Pred. |
|------|------|:-----------:|:-----------:|:------------:|:------------:|:-------------:|
| **GT** | IMP | 49.8 | 70.1 | 38.1 | 94.3 | 53.0 |
| | VGfM | 49.3 | 69.4 | 44.6 | 94.8 | 57.5 |
| | 3DSSG | 34.6 | 58.0 | 58.7 | 95.2 | 46.8 |
| | SGFN | 41.8 | 63.8 | 65.5 | 94.3 | 57.7 |
| | **Ours** | **66.1** | **81.2** | **71.5** | **95.6** | **77.4** |
| **Dense** | IMP | 25.8 | 51.8 | 23.0 | 90.4 | 30.0 |
| | VGfM | 28.3 | 53.3 | 24.4 | 90.7 | 31.6 |
| | 3DSSG | 17.5 | 41.4 | 26.6 | 88.2 | 31.9 |
| | SGFN | 31.4 | 56.7 | 30.5 | 89.6 | 38.3 |
| | **Ours** | **34.1** | **58.1** | **33.3** | **89.9** | **43.0** |
| **Sparse** | IMP | 7.9 | 27.5 | 14.0 | 90.7 | 20.6 |
| | VGfM | 8.2 | 26.9 | 15.4 | 90.8 | 17.6 |
| | 3DSSG | 0.9 | 9.7 | 15.1 | 87.9 | 5.9 |
| | SGFN | 1.7 | 12.6 | 14.4 | 88.9 | 8.3 |
| | **Ours** | **9.9** | **29.5** | **16.5** | **90.4** | **23.5** |
| | **Ours (i)** | **10.7** | **30.2** | **15.9** | **90.4** | **24.5** |

**关键发现**：
- Ours在几乎所有指标上超越所有baseline
- 2D方法（IMP, VGfM, Ours）在实体估计上优于3D方法（3DSSG, SGFN）；3D方法在predicate估计上有优势（因支持关系需要3D几何）
- 增量管线 (i) 在实体估计上进一步提升

### Table 2: 场景图预测（160 objects, 26 predicates, GT+FC）

| 方法 | Recall Rel. | Recall Obj. | Recall Pred. | mRecall Obj. | mRecall Pred. |
|------|:-----------:|:-----------:|:------------:|:------------:|:-------------:|
| IMP | 44.5 | 35.9 | 9.0 | 18.7 | 4.9 |
| VGfM | 44.5 | 37.9 | 14.7 | 17.9 | 6.5 |
| 3DSSG | 46.8 | 29.6 | 68.8 | 11.7 | 25.5 |
| SGFN | 45.2 | 29.4 | 42.8 | 11.8 | 13.5 |
| **Ours** | **52.7** | **56.7** | **50.4** | **27.2** | **23.9** |

**关键发现**：
- Ours在关系和实体估计上最优
- 3DSSG在predicate mRecall上最优（多predicate下联合3D BBox更适合）

### Table 3: 增量标签关联（AOS）

| 方法 | AOS (%) |
|------|:-------:|
| InSeg [58] | 38.6 |
| PanopticFusion [38] | 35.9 |
| **Ours** | **39.6** |

Ours比InSeg高1.0%，比PanopticFusion高3.7%。

### Table 4: 消融实验

| gi | Ri→j | Recall Rel. | Recall Obj. | Recall Pred. | mRecall Obj. | mRecall Pred. |
|:--:|:----:|:-----------:|:-----------:|:------------:|:------------:|:-------------:|
|   |   | 61.9 | 76.4 | 69.2 | 95.6 | 74.3 |
| ✓ |   | 62.9 | 77.9 | 64.3 | 95.9 | 74.2 |
|   | ✓ | 60.4 | 76.3 | 73.2 | 95.0 | 75.3 |
| ✓ | ✓ | 66.1 | 81.2 | 71.5 | 95.6 | 77.4 |

- 消融均在GT输入下进行
- gi（gated geometric feature）对实体分类有稳定提升
- Ri→j（relative pose descriptor）提升mRecall（处理类别不平衡），但降低Recall
- 两者结合达到最优Recall，但mRecall略差（有dominant class过拟合倾向）

### Table 5: 运行时分析

| 组件 | Sparse Mapping | 2D Entity Est. | Label Fusion | Scene Graph Est. |
|------|:-------------:|:--------------:|:------------:|:----------------:|
| 时间 | 14.7 ms | 124.6 ms | 14.2 ms | 52.5 ms |

整体不到206ms/帧，满足实时要求。

## Limitations

1. **低帧率序列问题**：3RScan序列帧率仅10Hz且存在运动模糊和抖动，论文在实验中使用了GT位姿来规避SLAM噪声
2. **纹理缺失区域**：ORB-SLAM3作为特征点法在无纹理区域失效，论文提出可替换为半直接法如SVO
3. **多视图编码器**：ResNet18作为多视图特征提取器是性能瓶颈，可替换更强backbone（但需权衡计算量）
4. **稀疏输入下predicate估计**：在Sparse输入下predicate Recall仅16.5%，仍有很大提升空间

## Reusable Claims

1. **多视图特征优于3D点特征**：在实体分类上，基于2D图像的多视图特征（Ours）始终优于基于3D点云的节点表示（3DSSG, SGFN）
2. **置信度融合优于重叠度融合**：在稀疏点云非均匀分布场景下，置信度权重融合（Ours的AOS=39.6%）优于基于重叠率的参考方案（InSeg=38.6%, PanopticFusion=35.9%）
3. **Gate机制提升几何特征的鲁棒性**：VGfM的几何特征拼接在稀疏输入下导致性能下降，而Ours的gated geometric feature（gi）在稀疏输入下仍保持稳定提升
4. **2D特征+3D几何互补**：实体分类用2D特征更优，支持关系（predicate）估计用3D几何更优——Ours结合两者取得整体最优

## Connections

- 与 [[3d-spatial-multimodal-knowledge-accumulation-scene-graph-prediction-point-cloud]]（SMKA，同为CVPR 2023）对比：SMKA针对点云场景图预测，引入外部知识图谱概念；本论文主要解决RGB序列实时增量预测，两种不同input modality
- 与 SGFN [64] 关系最密切，本工作显著改进 SGFN 的实体融合和图网络设计
- 在 3DSSG 数据集基准上比较，使用了20/160类两种评估协议

## Open Questions

1. **无GT位姿下的真实性能**：使用ORB-SLAM3实时SLAM获得的位姿误差对场景图性能的影响如何？
2. **跨数据集泛化性**：仅在3RScan上评估，在更广泛场景（如ScanNet、Matterport）上的迁移能力未知
3. **动态场景**：当前方法假设静态场景，Rosinol [48] 已在3D场景图中引入物体移动，本方法能否扩展？

## Provenance

- **来源**：`raw/sources/2023-06-01-incremental_3d_scene_graph.pdf`
- **提取文本**：`raw/sources/2023-06-01-incremental_3d_scene_graph.txt` (56075 chars)
- **证据等级**：full-paper（全文提取，数字和结构完整可用）
- **代码**：https://shunchengwu.github.io/MonoSSG
