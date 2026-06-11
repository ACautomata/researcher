---
title: "HATS: Hazard-Aware Traffic Scene Graph Generation"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags: [traffic-sgg, hazard-awareness, knowledge-graph, autonomous-driving, arXiv-2026]
raw_sources:
  - ../../../sources/scene-graph/2026-hazard-aware-traffic-scene-graph-generation.pdf
  - ../../../sources/scene-graph/2026-hazard-aware-traffic-scene-graph-generation.txt
evidence_level: full-paper
---

# Hazard-Aware Traffic Scene Graph Generation (HATS)

> 危险感知交通场景图生成 — 基于知识图谱和深度线索的自驾场景图生成方法。

## 摘要

维持复杂驾驶场景中的态势感知需要持续优先关注众多场景实体中的关键目标，并理解显著危险如何影响自车。现有研究擅长检测特定语义类别和视觉显著区域，但缺乏评估安全相关性的能力。同时，通用空间谓词（无论是仅针对前景对象还是对所有场景实体建模）在驾驶场景中都不充分。本文引入新任务 **Traffic Scene Graph Generation (TSGG)**，捕获显著危险与自车之间的交通特定关系。提出框架显式使用交通事故数据和深度线索补充视觉特征和语义信息进行推理。输出通过颜色编码严重程度、标注作用机制和相对位置来强调显著危险。在 Cityscapes 上创建关系标注，从 5 个角度评估 10 个任务。

## 方法

### 整体框架 (HATS)

HATS 包含两个分支：

1. **主场景图分支 (SG Branch)**：
   - **Panoptic Segmentation (PS) Module**: 基于 ResNet50 的 Mask2Former，进行全景分割
   - **Ego-path Related Entities Selection (ERES)**: 通过可学习的交叉注意力机制筛选与自车路径相关的候选实体
   - **Traffic Scene Graph Generation (TSGG)**: 生成以自车为中心的交通场景图，包含机制、方位和严重度三个维度

2. **辅助知识分支 (KG Branch)**：
   - 构建 16,066 节点、153,488 边的交通事故事件知识图谱
   - 4 阶段流水线：节点构建 → 结构关系连线 → 因果边补充 → 桥接节点对齐
   - **KGE 模块**: 字面感知节点初始化 + FiLM 限定符感知消息传递 + Transformer 三元素评分器

### ERES 模块

通过 Mask2Former 的 mask 特征图提取路径表示，经多头交叉注意力计算各实体与自车路径的相关性得分，筛选候选实体。融合三个信号（实体内容、全局上下文、门控路径条件）构建用于下游分类的特征。

### KGE 模块

- 字面感知初始化：7 个分类属性和 5 个数值属性（CRASH 节点）联合编码
- 超关系边支持：通过 FiLM 机制自适应调节带限定符的消息传递
- Transformer 三元素评分器：头节点+关系 token 通过 Transformer 编码后与所有尾节点嵌入计算得分
- 1-to-N 过滤多标签分类训练策略

### TSGG 模块

轻量级视差编码器补充几何线索。每个候选实体构建 4 种表示（视觉、语义、几何、KGE），通过门控融合机制自适应加权。三个专用分类头：
- **Mechanism Head**: 8 类作用机制（control, edge_proximity, fixed_object_near_edge, head_on, intersection, rear_end, sideswipe, cross_traffic_conflict）
- **Side Head**: 3 类相对方位（left, front, right）
- **Severity Head**: 4 级严重度（info, caution, imminent, relevant_but_not_critical），通过多头注意力注入 KG 先验

## 实验与结果

### 数据集
- **Cityscapes**: 标注 820 张图像，8:1:1 划分
- **NHTSA KG**: 16,066 节点、153,488 边，8:1:1 划分
- **训练平台**: 单张 A40 GPU

### 核心结果

#### KGE 评估 (表 II)

| 指标 | Object Prediction | Subject Prediction | Triplet Prediction |
|------|------------------|--------------------|--------------------|
| StarE MRR | 38.66 | 77.21 | 57.94 |
| **OUR-1HOP MRR** | **88.04** | **96.76** | **92.40** |
| **OUR-1HOP H@10** | **99.77** | **99.74** | **99.75** |

#### Hazard Prioritization (表 III)

| 指标 | OURS | CFHP [7] |
|------|------|----------|
| mAP@10 | **82.90** | 60.97 |
| MRR@10 | **96.60** | 77.78 |
| NDCG@10 | **89.47** | 56.95 |

#### SGDet (表 IV)

| 方法 | R@50 / mR@50 |
|------|-------------|
| MOTIFS [33] | 29.68 / 9.38 |
| VCTREE [34] | 29.60 / 5.23 |
| PSGTR [15] | 23.72 / 12.21 |
| **OUR** | **62.79 / 76.13** |

#### 实体相关性分类 (表 V)

| 方法 | P | R | F1 | AUC | MAE↓ |
|------|---|---|----|-----|------|
| MOTIFS-sgdet | 85.73 | 50.90 | 61.61 | 77.11 | 0.270 |
| PSGTR | 87.62 | 31.74 | 44.24 | 62.88 | 0.327 |
| **OUR** | **96.96** | **94.07** | **95.03** | **97.20** | **0.047** |

#### 实体显著性分类 (表 V)

| 方法 | P | R | F1 | AUC | MAE↓ |
|------|---|---|----|-----|------|
| CFHP [7] | 88.14 | 49.77 | 62.49 | 62.39 | 0.233 |
| **OUR** | **95.85** | **87.78** | **90.89** | **92.17** | **0.103** |

#### 消融实验 — Severity (表 VI, R@1/mR@1)

| 变体 | R@1/mR@1 |
|------|----------|
| HATS w/o ERES | 31.27 / 35.32 |
| HATS w/o KGE | 42.03 / 44.99 |
| HATS w/o Depth | 41.21 / 43.15 |
| **HATS (full)** | **80.10 / 80.72** |

#### 消融实验 — Mechanism (表 VI, R@1/mR@1)

| 变体 | R@1/mR@1 |
|------|----------|
| HATS w/o ERES | 30.33 / 32.32 |
| HATS w/o KGE | 42.52 / 43.62 |
| HATS w/o Depth | 35.65 / 37.59 |
| **HATS (full)** | **73.16 / 73.65** |

#### 训练集规模影响

准确率从 5% 训练集时的 **0.437±0.016** 提升至 80% 时的 **0.684±0.005**，标准偏差持续下降表明模型稳定性随数据增加而提升。

### 主要发现

1. **ERES 模块是关键前置条件**：去除 ERES 导致三任务 R@1 下降 >40%，且 KGE 和 Depth 模块在无 ERES 时几乎无效
2. **KGE 先验对 Severity 预测至关重要**：几何相似但语义不同的场景（如对向车辆 vs. 同向）需要事故知识区分
3. **Depth 线索解决空间歧义**：相邻车道侧撞 vs. 隔线停车需要相对距离和横向偏移信息
4. **互补设计的协同效应**：ablation 中各组件单独去除均显著下降，全模型最优

## 贡献

1. 提出 **TSGG** 新问题：以自车为中心，强调显著危险及其交通特定关系，在 Cityscapes 上标注基线
2. 提出 4 阶段流水线构建统一交通事故 KG + 支持超关系边和多属性节点的 KGE 方法，在三项任务上超越基线
3. 首次将交通事故数据用于交通图像理解，显式将 KGE 作为补充模态，用历史事故记录指导严重度评估

## 相关论文

- [[PSGTR]]: Panoptic Scene Graph Generation
- [[MOTIFS]]: Neural Motifs for Scene Graph Parsing
- [[VCTREE]]: Learning to Compose Dynamic Tree Structures
- [[panoptic-video-scene-graph-generation]]: 视频级场景图
- [[flow-based-sgg]]: 基于流匹配的场景图生成
- [[hiker-sgg]]: 层次化知识增强的场景图生成

## 局限与未来工作

- 当前专注单帧图像，未来扩展到视频推理
- 采用更强的分割骨干网络提升性能
- 标注仅 820 张 Cityscapes 图像，更多数据可进一步提升性能
