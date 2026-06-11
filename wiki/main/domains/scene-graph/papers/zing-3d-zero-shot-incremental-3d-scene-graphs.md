---
title: "ZING-3D: Zero-shot Incremental 3D Scene Graphs via Hierarchical Alignment"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - 3d-scene-graph
  - zero-shot
  - incremental
  - vlm
  - open-vocabulary
  - arxiv-2025
raw_sources:
  - ../../../sources/scene-graph/2025-arXiv-ZING-Zero-shot-Incremental-3D-Scene-Graphs-via-Hierarchical-Alignment.pdf
  - ../../../sources/scene-graph/2025-arXiv-ZING-Zero-shot-Incremental-3D-Scene-Graphs-via-Hierarchical-Alignment.txt
evidence_level: full-paper
---

# ZING-3D: Zero-shot Incremental 3D Scene Graphs via Vision-Language Models

- **标题（EN）**: ZING-3D: Zero-shot Incremental 3D Scene Graphs via Vision-Language Models
- **作者**: Pranav Saxena, Jimmy Chiun
- **机构**: BITS Pilani Goa Campus（Saxena）, National University of Singapore（Chiun）
- **发表**: arXiv 2025
- **arXiv**: 待补充
- **代码**: 未提及

## 概述

ZING-3D 是一个零样本增量式3D场景图生成框架，利用预训练 VLM 的开放词汇推理能力，无需任务特定微调即可构建具有几何感知的3D场景图。处理流程：输入带姿态的 RGB 图像序列 → VLM 生成 2D 场景图 → Grounded-SAM2 分割 → 深度投影至3D → 增量融合为统一全局3D场景图。支持任务导向剪枝以适配下游导航任务。

## 方法

### 整体流程（Fig. 2）

1. **开放词汇物体检测**：使用 VLM（Gemini 2.5-Flash）从 RGB 图像中零样本识别物体，支持自然语言描述的任意类别，无需预定义类别集合。相比需手动提供 prompts 的 Grounded-SAM2，VLM 方式更具可扩展性。
2. **2D场景图生成**：VLM 估计物体间成对关系，捕获空间交互（"is to the right of", "is above", "is near"）和语义属性（物体所在房间类型），形成物体级+场景级的分层抽象。
3. **3D投影**：使用 Grounded-SAM2 获取精确分割掩码，结合深度图通过针孔相机模型反投影至3D空间：

   $$X = \frac{(u - c_x)}{f_x} \cdot d, \quad Y = d, \quad Z = \frac{(v - c_y)}{f_y} \cdot d$$

   结合机器人位姿（来自仿真元数据）变换至全局世界坐标系，取有效投影点的平均作为3D质心。
4. **增量更新**：随机器人探索，新观测逐步融合进统一全局3D图，形成随时间演化的结构化表示。
5. **任务导向剪枝（Task-Guided Pruning）**：根据 VLN 查询或目标物体，VLM 分析场景图选择最相关子图，结合机器人位姿过滤远距离/遮挡元素，生成紧凑、任务特异的子图。

### 分层结构

- 物体 node：开放词汇类别、3D位置、视觉特征、语义描述、关联房间类型
- 关系 edge：空间关系 + 语义关系 + 精确物间距离
- 场景级：物体 → 房间 → 完整场景，支持跨房间推理

## 实验

### 数据集
- **Replica Dataset**：每个场景单一房间
- **HM3D Dataset**：多房间场景

### 基线/比较
- 无直接基线比较（零样本设置，采用人工评估）
- 消融实验比较了三种 VLM 变体

### 评估指标
- **节点精度（Node Precision）**：人工评估节点标注正确的比例
- **房间精度（Room Precision）**：人工评估物体所在房间类型是否合理
- **重复检测数（Duplicates）**：冗余检测实例数
- **边精度（Edge Precision）**：人工评估空间关系标注正确的比例

### 主要结果

**场景图构建精度（Table I）**

| 数据集 | 场景 | Node Prec. | Room Prec. | Duplicates | Edge Prec. |
|-------|------|-----------|-----------|-----------|-----------|
| Replica | room0 | 0.98 | 0.93 | 0 | 0.97 |
| Replica | room1 | 0.97 | 1.0 | 0 | 0.96 |
| Replica | room2 | 0.97 | 1.0 | 0 | 0.98 |
| Replica | office0 | 0.98 | 0.97 | 1 | 1.0 |
| Replica | office1 | 0.96 | - | 0 | 0.98 |
| Replica | office2 | 0.97 | - | 0 | 0.95 |
| Replica | office3 | 0.95 | - | 1 | 0.92 |
| **Replica 平均** | | **0.97** | **0.96** | 0-1 | **0.96** |
| HM3D | 00801 | 0.97 | - | - | 0.97 |
| HM3D | 00820 | 0.95 | - | - | 0.96 |
| HM3D | 00877 | 0.97 | - | - | 1.0 |
| HM3D | 00894 | 0.96 | - | - | 0.98 |
| **HM3D 平均** | | **0.96** | **0.96** | - | **0.98** |

**VLM 消融实验（Table II）** —— 从10张带姿态观测生成中间2D场景图，在 Habitat-Sim 中4个场景平均：

| VLM | Time Taken (s) | Node Prec. | Valid Objects % | Edge Prec. |
|-----|---------------|-----------|----------------|-----------|
| Gemini 2.5-Flash-Lite | 4.21 | 0.93 | 91 | 0.93 |
| **Gemini 2.5-Flash** | **43.13** | **0.96** | **93** | **0.94** |
| Qwen2.5-VL-7B | 280 | 0.83 | 85 | 0.88 |

### 关键发现
1. 零样本节点标注精度约 96-97%（人工评估），边（空间关系）精度 96-98%
2. 重复检测极少（0-1/场景）
3. 房间类型推断准确率约 96%
4. Gemini 2.5-Flash 综合最优（节点 0.96/边 0.94），Flash-Lite 速度快但精度稍低（节点 0.93/边 0.93），Qwen2.5-VL-7B 耗时最长且精度最低（节点 0.83/边 0.88）
5. 支持 Vision-Language Navigation 任务导向剪枝，产生紧凑目标特异子图

## 与相关工作的关系

- 与 [[ccl-3dsgg-clip-driven-open-vocabulary-3d-scene-graph-generation.md|CCL-3DSGG]]（CVPR 2024）和 [[open3dsg-open-vocabulary-3d-scene-graphs-from-point-clouds.md|Open3DSG]]（CVPR 2024）相比：两者均为单次静态3D场景图生成（前者需标注训练，后者需点云输入），ZING-3D 支持增量更新和纯 RGB + 深度输入
- 与 [[incremental-3d-scene-graph-prediction-from-rgb-sequences.md|Incremental 3D Scene Graph]]（2023）相比：ZING-3D 是零样本（无需训练），后者是监督式
- 与 [[pixels-to-graphs-open-vocabulary-sgg-vlm.md|PGSG]]（CVPR 2024）和 [[open-world-scene-graph-generation-using-vlm.md|OwSGG]]（2025）相比：两者均为单张2D图像 SGG，ZING-3D 扩展至3D和增量
- 与 [[fungraph-functionality-aware-3d-scene-graphs.md|FunGraph]]（2025）和 [[gaussiangraph-3d-gaussian-scene-graph-generation.md|GaussianGraph]]（2025）相比：ZING-3D 无需任何3D表示学习（使用纯 VLM + 深度几何投影）

## 局限性

1. 使用人工评估而非自动化指标，难以进行公平的量化对比
2. 未报告 recall / mR 等标准 SGG 指标，仅报告精度
3. VLM 推理时间差异大（Flash-Lite 4.21s vs. Qwen 280s）
4. 依赖机器人位姿（仿真元数据），实际部署时需 SLAM/位姿估计
5. 没有与监督/全监督3D SGG 方法的定量对比
6. 仅评估单房间（Replica）和有限场景（HM3D 4个），规模有限
7. Grounded-SAM2 分割是像素级的，但论文未报告分割精度
