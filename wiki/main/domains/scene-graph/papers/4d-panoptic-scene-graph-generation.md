---
title: "4D Panoptic Scene Graph Generation (PSG-4D)"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - 4D-scene-graph
  - panoptic-segmentation
  - RGB-D
  - point-cloud
  - spatio-temporal
  - dataset
raw_sources:
  - ../../../sources/scene-graph/2023-12-01-4D_Panoptic_Scene_Graph_Generation.pdf
  - ../../../sources/scene-graph/2023-12-01-4D_Panoptic_Scene_Graph_Generation.txt
paper:
  title: "4D Panoptic Scene Graph Generation"
  authors:
    - Jingkang Yang
    - Jun Cen
    - Wenxuan Peng
    - Shuai Liu
    - Fangzhou Hong
    - Xiangtai Li
    - Kaiyang Zhou
    - Qifeng Chen
    - Ziwei Liu
  year: 2023
  venue: NeurIPS 2023
  arxiv: "2405.10305"
  doi: null
  code: https://github.com/Jingkang50/PSG4D
  project: null
classification:
  label: PSG-4D / PSG4DFormer
  task:
    - 4D Panoptic Scene Graph Generation
    - Spatio-temporal Scene Understanding
    - Dynamic Scene Graph Generation
  method_family:
    - Two-Stage Framework
    - Mask2Former
    - DKNet
    - Spatial-Temporal Transformer
    - SA-Gate
  modality:
    - RGB-D Video
    - Point Cloud Video
    - 4D Panoptic Segmentation Masks
  datasets:
    - PSG4D-GTA
    - PSG4D-HOI
  metrics:
    - R@K
    - mR@K
    - vIoU
evidence_level: full-paper
---

## Overview

**PSG-4D** (NeurIPS 2023) 提出了一种新的 4D 全景场景图生成任务，将传统场景图从静态 3D 扩展到动态 4D（3D+时间）。该工作由南洋理工大学 S-Lab、港科大、北邮和浸会大学合作完成，核心贡献包括一个新任务、一个新数据集以及一个统一的基准模型 PSG4DFormer。

## Core Contributions

1. **新任务**：提出 4D Panoptic Scene Graph Generation (PSG-4D)，从 RGB-D 或点云视频序列中预测包含时序关系的 4D 全景场景图
2. **新数据集**：构建 PSG-4D 数据集，包含两个子集：
   - PSG4D-GTA：67 个第三人称合成视频（28K 帧），来自 GTA-V 游戏引擎，35 类物体、43 类关系
   - PSG4D-HOI：2973 个第一人称真实世界视频（891K 帧），来自 HOI4D 数据集，46 类物体、15 类关系
3. **统一框架**：提出 PSG4DFormer——两阶段 Transformer 模型，支持 RGB-D 和点云两种输入模态
4. **开源代码库**：提供完整的开源代码和机器人部署 demo

## Method

### Pipeline

PSG4DFormer 是一个两阶段框架：

**Stage 1: 4D Panoptic Segmentation**
- **RGB-D 输入**：使用 SA-Gate（分离-聚合门控）融合 RGB 和深度特征，再送入 Mask2Former 进行帧级全景分割
- **点云输入**：使用 DKNet (3D UNet + 稀疏卷积) 处理彩色点云
- **跟踪**：利用 UniTrack，直接复用分割阶段的实例嵌入（instance kernels 或 object queries）进行时序关联，获得 4D 特征管 (feature tubes) Q_i = {q^t_i}^T_{t=1}

**Stage 2: Relation Modeling**
- **Spatial-Temporal Transformer Encoder**：空间编码器聚合同帧所有物体的特征，时间编码器沿时间维度更新每个物体特征管
- **Relation Classification**：基于更新后的特征管对，使用轻量级全连接层进行帧级谓词分类
- 关系标注格式："object-1 relation object-2"，每个对象关联 mask tube 和持续时间

### 关键设计

- SA-Gate 的分离-聚合策略有效融合 RGB-D 的双模态信息
- 复用分割阶段特征进行跟踪，避免额外外观模型，在同一语义类别的实例间保持区分性
- 时空 Transformer 同时捕获空间交互和时序演化

## Dataset

### PSG-4D 数据集统计

| 子集 | 类型 | 视角 | 视频数 | 帧数 | 物体类别 | 关系类别 |
|------|------|------|--------|------|----------|----------|
| PSG4D-GTA | 合成 (GTA-V) | 第三人称 | 67 | 27,700 | 35 | 43 |
| PSG4D-HOI | 真实世界 | 第一人称 | 2,973 | 891,000 | 46 | 15 |

- PSG4D-GTA：平均时长 84 秒，共 28.3B 点云
- PSG4D-HOI：平均时长 20 秒，282 个室内场景
- 包含 4D panoptic segmentation masks 和细粒度的动态 scene graph 标注

### 数据集构建

- PSG4D-GTA：基于 SAIL-VOS 3D 数据集筛选 67 个无 NSFW 视频，使用 PVSG 标注流水线（SAM 自动标注 + AOT 传播 + 人工审核）
- PSG4D-HOI：直接使用 HOI4D 的 4D panoptic 标注，通过自动规则生成关系标注 + 人工校对

## Experiments

### 实验设置

- **RGB-D 分支**：ImageNet 预训练 ResNet-101 作为 RGB 和 Depth encoder，训练 12 epochs
- **点云分支**：DKNet 从头训练，200 epochs
- **Relation Model**：2 层 spatial + 2 层 temporal Transformer，额外训练 100 epochs
- **评估指标**：R@K 和 mR@K（K=20, 50, 100），要求 triplet 分类正确且 vIoU > 0.5
- 对比的变体：3DSGG 基线、PSG4DFormer/t（去除 temporal encoder）、PSG4DFormer/d（去除 depth 分支）

### 主结果 (Table 2)

| Input | Method | PSG4D-GTA R/mR@20 | PSG4D-GTA R/mR@50 | PSG4D-GTA R/mR@100 | PSG4D-HOI R/mR@20 | PSG4D-HOI R/mR@50 | PSG4D-HOI R/mR@100 |
|-------|--------|-------------------|-------------------|--------------------|-------------------|-------------------|--------------------|
| PC | 3DSGG | 1.48 / 0.73 | 2.16 / 0.79 | 2.92 / 0.85 | 3.46 / 2.19 | 3.15 / 2.47 | 4.96 / 2.84 |
| PC | PSG4DFormer/t | 2.25 / 1.03 | 2.67 / 1.72 | 3.14 / 2.05 | 3.26 / 2.04 | 3.16 / 2.35 | 4.18 / 2.64 |
| PC | **PSG4DFormer** | **4.33 / 2.10** | **4.83 / 2.93** | **5.22 / 3.13** | **5.36 / 3.10** | **5.61 / 3.95** | **6.76 / 4.17** |
| RGB-D | 3DSGG | 2.29 / 0.92 | 2.46 / 1.01 | 3.81 / 1.45 | 4.23 / 2.19 | 4.47 / 2.31 | 4.86 / 2.41 |
| RGB-D | PSG4DFormer/t | 4.43 / 1.34 | 4.89 / 2.42 | 5.26 / 2.83 | 4.44 / 2.37 | 4.83 / 2.43 | 5.21 / 2.84 |
| RGB-D | PSG4DFormer/d | 4.40 / 1.42 | 4.91 / 1.93 | 5.49 / 2.27 | 5.49 / 3.42 | 5.97 / 3.92 | 6.43 / 4.21 |
| RGB-D | **PSG4DFormer** | **6.68 / 3.31** | **7.17 / 3.85** | **7.22 / 4.02** | **5.62 / 3.65** | **6.16 / 4.16** | **6.28 / 4.97** |

### 关键发现

1. **RGB-D vs 点云**：RGB-D 输入普遍优于点云输入，尤其在 PSG4D-GTA 上差距明显（R@100: 7.22 vs 5.22），归因于 RGB-D 的 ImageNet 预训练优势
2. **深度信息的重要性**：去除 depth 分支（PSG4DFormer/d）后性能下降，验证了深度信息对 4D 场景理解的价值
3. **时序注意力的必要性**：去除 temporal encoder（PSG4DFormer/t）后性能接近 3DSGG 基线，时序建模是 4D SGG 的核心

## Real-World Application

论文展示了 PSG-4D 在服务机器人上的实际部署：
- 机器人搭载 RGB-D 传感器（硬件成本约 $1.2K）
- 每 30 秒将 PSG-4D 解析结果发送给 GPT-4
- GPT-4 根据场景图进行推理和规划，输出可执行动作
- 示例场景：检测到人乱扔瓶子 → 机器人执行清理和提醒

## Key Insights

- **4D 场景图是连接原始视觉感知和高层推理的桥梁**，作为 LLM 的环境接口
- **合成数据 (GTA) 和真实数据 (HOI) 互补**：合成数据提供多样化的关系和物体交互，真实数据提供生态效度
- **当前模型仅能处理简单场景**，在面对复杂真实环境时仍有显著局限
- **当前绝对性能较低（R@100 < 8%）**，表明 4D SGG 仍处于早期阶段，需要更高效的方法和更大规模的数据集

## Connections

- **前置工作**：[[panoptic-video-scene-graph-generation|PVSG (CVPR 2023)]] — PSG 的视频扩展，PSG-4D 在此基础上进一步引入 3D 空间信息
- **相关工作**：[[incremental-3d-scene-graph-prediction-from-rgb-sequences|Incremental 3D SGG]]、[[fdsg-forecasting-dynamic-scene-graphs|FDSG]]、[[hidynagraph|Hi-Dyna Graph]]
- **数据集关联**：SAIL-VOS 3D、HOI4D、EgoBody

## Limitations

- 数据集规模有限（仅 67 个合成 + ~3K 个真实视频），多样性和规模不足以支撑强泛化
- 绝对性能较低（R@100 < 8%），难以直接实际部署
- 只能处理简单场景，复杂环境下性能退化明显
- 两阶段框架存在级联误差传播
- 关系类别较少（PSG4D-HOI 仅 15 类关系）
