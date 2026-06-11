---
title: "Devil's on the Edges: Selective Quad Attention for Scene Graph Generation (SQUAT)"
type: paper
domain: scene-graph
status: active
created: 2026-06-08
updated: 2026-06-08
tags:
  - scene-graph-generation
  - selective-attention
  - edge-selection
  - quad-attention
  - contextual-reasoning
  - CVPR-2023
  - transformer
raw_sources:
  - ../../../sources/scene-graph/2023-CVPR-Devils-on-the-Edges-Selective-Quad-Attention-for-Scene-Graph-Generation-SQUAT.pdf
  - ../../../sources/scene-graph/2023-CVPR-Devils-on-the-Edges-Selective-Quad-Attention-for-Scene-Graph-Generation-SQUAT.txt
related_pages:
  - bipartite-graph-network-with-adaptive-message-passing-unbiased-scene-graph-generation.md
  - fast-contextual-scene-graph-generation.md
evidence_level: full-paper
paper:
  title: "Devil's on the Edges: Selective Quad Attention for Scene Graph Generation"
  authors:
    - Deunsol Jung
    - Sanghyun Kim
    - Won Hwa Kim
    - Minsu Cho
  year: 2023
  venue: "IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2023"
  arxiv: null
  doi: null
  code: "http://cvlab.postech.ac.kr/research/SQUAT"
  project: null
classification:
  label: "Selective Quad Attention Network"
  task:
    - Scene Graph Generation (SGG)
    - Predicate Classification (PredCls)
    - Scene Graph Classification (SGCls)
    - Scene Graph Detection (SGDet)
  method_family:
    - Selective Quad Attention Network (SQUAT)
    - Edge Selection Module (ESM)
    - Quad Attention (N2N, N2E, E2N, E2E)
    - Multi-head Self-Attention
    - Bi-level Sampling
  modality:
    - RGB Image (2D)
  dataset:
    - Visual Genome
    - OpenImages v6
  backbone:
    - Faster R-CNN (ResNeXt-101-FPN)
---

# Devil's on the Edges: Selective Quad Attention for Scene Graph Generation (SQUAT)

## 概述

SQUAT 提出了一种针对场景图生成（SGG）的选择性四元注意力网络，核心思想是**边缘选择 + 四元注意力**。针对 SGG 中大量无关物体对（edges）干扰上下文推理的问题，SQUAT 通过边缘选择模块（ESM）筛选有效物体对，再通过四元注意力模块（quad attention）在节点和边缘之间进行四类注意力交互（N2N、N2E、E2N、E2E），实现更鲁棒的上下文推理。

## 动机与挑战

- 在 Visual Genome 数据集中，每张图像平均包含 38 个物体和 22 个关系，即仅约 **1%** 的物体对具有有效关系（即使目标检测完美）
- 现有方法（如 IMP、BGNN）在全连接图上进行消息传递，大量无关边缘会**干扰甚至恶化**上下文推理
- 实验表明：在不使用边缘选择的情况下，消息传递对 SGG 性能的提升有限甚至有害

## 方法

### 1. 节点检测模块（Node Detection）

- 使用预训练 Faster R-CNN (ResNeXt-101-FPN) 提取目标候选框和视觉特征
- 节点特征：`fi = Wo[Wv·vi; Wg·bi]`，融合视觉特征和边界框坐标
- 边缘特征：`fij = Wp[fi; fj]`，拼接两个节点特征

### 2. 边缘选择模块（Edge Selection Module, ESM）

- 使用 MLP 为每对物体预测相关性分数 `sij`
- 保留 top-ρ% 的物体对作为有效边缘
- 使用**三个独立的 ESM**：
  - **ESM_Q**：为 quad attention 选择待更新的查询边缘
  - **ESM_N2E**：为 node-to-edge 注意力选择 key-value 边缘
  - **ESM_E2E**：为 edge-to-edge 注意力选择 key-value 边缘
- 预训练策略：先冻结其他参数，仅用 LESM 训练 ESM 若干轮以稳定训练

### 3. 四元注意力模块（Quad Attention）

基于 Transformer decoder，每层执行四类注意力：

| 注意力类型 | 查询 | Key-Value | 作用 |
|-----------|------|-----------|------|
| N2N (Node-to-Node) | 节点 | 节点 | 节点间的自注意力 |
| N2E (Node-to-Edge) | 节点 | 有效边缘 | 节点获取边缘上下文 |
| E2N (Edge-to-Node) | 有效边缘 | 节点 | 边缘获取节点上下文 |
| E2E (Edge-to-Edge) | 有效边缘 | 有效边缘 | 边缘间的高阶交互 |

### 4. 训练目标

- 谓词分类：交叉熵损失 LPCE
- 边缘选择：二元交叉熵损失 LESM
- 总损失：`L = LPCE + λ·(1/3)·(L_Q_ESM + L_N2E_ESM + L_E2E_ESM)`
- 保持比率 ρ = 70%（SGDet 设置）
- 超参数 λ = 0.1
- 使用 bi-level sampling [19] 处理长尾分布

## 实验结果

### Visual Genome 数据集（mR@K 指标）

| 设置 | 指标 | SQUAT | BGNN (SOTA) | 提升 |
|------|------|-------|-------------|------|
| PredCls | mR@100 | **33.4** | 32.9 | +0.5 |
| SGCls | mR@100 | **18.8** | 16.5 | +2.3 |
| SGDet | mR@100 | **16.5** | 12.6 | +3.9 |

- **SGDet 是最具挑战性和现实意义的设置**，SQUAT 在此设置上大幅领先 SOTA 3.9 个点（+31%），因为该设置下检测框包含大量背景框，无效边缘更多
- 在 SGCls 和 PredCls 上也有所提升，任务越复杂提升越明显

### OpenImages v6 数据集

| 指标 | SQUAT | RU-Net | 其他 SOTA |
|------|-------|--------|-----------|
| R@50 | **75.8** | 76.9 | 76.5 (HL-Net) |
| wmAP_rel | **34.9** | 35.4 | 35.1 (HL-Net) |
| wmAP_phr | **35.9** (最佳) | 34.9 | 34.7 (HL-Net) |
| score_wtd | **43.5** (最佳) | 43.5 (持平) | 43.2 (HL-Net) |

- OpenImages v6 每张图像物体和关系较少，边缘选择优势不那么突出
- 但在 wmAP_phr 上大幅领先（35.9 vs 次优 34.9）

## 消融实验

### 边缘选择消融（SGDet mR@100）
- 完整模型：16.47（对应表中有 graph constraint 的版本？需核实 Table 3 中数据是另一个设置）
- 去除所有 ESM：15.00（-8.9%）
- 去除 ESM_Q：14.12（下降最大 → 查询选择最关键）
- 去除 ESM_N2E 和 ESM_E2E：14.12 和 14.85
- 三个 ESM 使用独立参数优于共享参数

### 注意力类型消融（SGDet mR@100）
- 完整四元注意力：16.47
- 去除 E2E：15.54（E2E 最重要）
- 去除 E2N：15.42
- 去除 N2E：15.30
- 去除 N2N：15.03（去除 N2N + N2E 性能差于去除 E2N + E2E？需确认具体消融实验排布）

### 消息传递消融（SGDet mR@100）
- 不进行消息传递（No）：8.68
- 全连接图消息传递（Full）：9.12（+0.44，提升极小）
- 使用 ESM（ES）：10.57（+1.89）
- 使用真实场景图（GT）：14.12（+5.44）
- → **无效边缘会严重干扰消息传递，移除无效边缘是关键**

## 讨论与结论

- SQUAT 在 **SGDet** 上提升最大（+3.9 mR@100），因为该设置下无关物体对最多，边缘选择最有效
- 三个独立的 ESM 模块各自选择不同的有效边缘集，说明更新查询边缘和作为 key-value 的边缘需要不同的判断标准
- E2E 注意力（被之前工作忽略）能捕获高阶边缘间关系，提供有价值的信息
- 边缘选择模块可作为即插即用模块应用于其他消息传递式 SGG 方法（实验验证了对 BGNN 也有提升）

## 关键洞见

1. **全连接图对 SGG 有害**：大多数物体对无有效关系，全连接图上的消息传递反而引入噪声
2. **选择什么更新（query 选择）比用什么更新（key-value 选择）更重要**
3. **E2E 注意力是新颖贡献**：被之前工作忽略，但对捕获高阶关系有帮助
4. **深度区分 ESM**：Q、N2E、E2E 需要三个独立 ESM，共享参数会降低性能
