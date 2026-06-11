---
title: "3D Scene Graph: A Structure for Unified Semantics, 3D Space, and Camera"
type: paper
domain: scene-graph
status: active
created: 2026-06-10
updated: 2026-06-10
tags:
  - 3d-scene-graph
  - scene-graph-generation
  - foundational
  - 3D-space
  - ICCV-2019
raw_sources:
  - raw/sources/2019-10-01-3d-scene-graph-unified-semantics-3d-space-camera.pdf
  - raw/sources/2019-10-01-3d-scene-graph-unified-semantics-3d-space-camera.txt
paper:
  title: "3D Scene Graph: A Structure for Unified Semantics, 3D Space, and Camera"
  authors:
    - Iro Armeni
    - Zhi-Yang He
    - JunYoung Gwak
    - Amir R. Zamir
    - Martin Fischer
    - Jitendra Malik
    - Silvio Savarese
  year: 2019
  venue: ICCV 2019
  project: "http://3dscenegraph.stanford.edu"
  arxiv: null
  doi: null
  code: null
classification:
  label: foundational
  task:
    - 3D Scene Graph Generation
  method_family:
    - Mask R-CNN + Framing + Multi-View Consistency
  modality:
    - RGB Panorama
    - 3D Mesh
  datasets:
    - Gibson Environment Database
  metrics:
    - AP (Average Precision)
    - AP.50
    - AP.75
    - AR (Average Recall)
    - mAP (for predicate classification)
    - F1-score / IoU (for amodal mask)
evidence_level: full-paper
---

# 3D Scene Graph: A Structure for Unified Semantics, 3D Space, and Camera

> Iro Armeni, Zhi-Yang He, JunYoung Gwak, Amir R. Zamir, Martin Fischer, Jitendra Malik, Silvio Savarese. Stanford University / UC Berkeley. ICCV 2019.
> Project: [http://3dscenegraph.stanford.edu](http://3dscenegraph.stanford.edu)

## 一句话贡献

**首次将 Scene Graph 范式扩展到 3D 空间**，定义了一个四层图结构（Building → Room → Object → Camera），并提出基于 Framing + Multi-View Consistency 的半自动构建框架，将 3D 场景图从人工标注转变为可自动生成的统一语义表示。

## 问题设置

- **输入**：3D mesh 模型 + 注册全景 RGB 图像 + 相机参数（来自 Matterport3D 或 Gibson 数据库）
- **输出**：3D Scene Graph——覆盖整个建筑的四层图，每层包含节点（实体）、属性（特征）和边（关系）
- **核心挑战**：人工标注语义标注在 3D 建筑尺度上极其劳动密集（prohibitively labor heavy），现有 2D 检测器直接用于全景图时因视角截断、观测不一致等问题表现不佳

## 3D Scene Graph 结构

### 四层结构（Fig. 1）

| 层次 | 节点示例 | 属性示例 | 关系示例 |
|------|---------|---------|---------|
| Building | 住宅楼 | Function, Area, Number of Floors | — |
| Room (Space) | 客厅、卧室、浴室 | Scene Category, Shape, Size, Illumination, Floor Number | Same Parent Building, Spatial Order |
| Object | 床、沙发、桌子 | Class, Material, Color, Shape, Area, Action Affordance | Same Parent Room, Occlusion, Spatial Order, Relative Magnitude |
| Camera | RGB 相机位置 | FOV, Modality, Pose, Resolution | Parent Space |

### 属性分类（Table 1）

- **Object**: Action Affordance, Area, Class, Color, ID, Location, Material, Occupancy, Shape, Size, Spatial Span, Texture, Volume
- **Space (Room)**: Area, ID, Illumination, Location, Occupancy, Scene Category, Shape, Size, Spatial Span, Volume
- **Building**: Area, Building Reference Center, Function, ID, Number of Floors, Shape, Size, Volume
- **Camera**: Field Of View, ID, Modality, Pose, Resolution

### 关系分类（Table 1）

- **Object-Object**: Amodal Mask, Occlusion Relationship, Same Parent Room, Spatial Order, Relative Magnitude
- **Object-Space**: Parent Space
- **Sound-Object**: Occlusion Relationship, Spatial Order
- **Space-Space**: Spatial Order, Parent Building, Relative Magnitude
- **Camera-Space**: Parent Space

## 方法

### 总体框架（Fig. 2）

**Pipeline: Input → Framing (2D robustification) → Multi-View Consistency (3D robustification) → Space Graph**

### 1. Framing（全景图像帧采样与聚合）

目标：解决 2D 检测器对图像边缘的部分遮挡物体检测不准的问题。

- 在全景图上**密集采样** rectilinear 图像：yaw [-180°, 180°, 15°], pitch [-15°, 15°, 15°], FoV [75°, 105°, 15°] → 每张全景图 225 张 800×800 图像
- 每张图像用 **Mask R-CNN** 检测（confidence ≥ 0.7）
- **加权投票聚合**回全景图：权重 = (检测置信度) / (检测中心到图像中心的距离)，兼顾置信度和物体居中程度
- 按类连接组件 → 全景上的实例分割掩码

### 2. Multi-View Consistency（多视角一致性）

目标：解决单张全景图投影到 3D mesh 时的标签泄漏、重建误差和相机对齐误差。

- 将所有全景标签投影到 3D mesh 表面
- **加权投票聚合**面标签：权重 = (所有相机到该面的总距离) / (当前相机到面的距离)，即越近的相机投票权重越大
- 按检测实例级聚合（而非逐面投票）：对接收同一实例投票的面组 Fobj，取最一致的标签
- 最后 3D 级连接组件 → 最终 3D 实例分割

### 3. 用户验证（可选）

开发 Web 界面通过 Amazon Mechanical Turk 进行人工验证和校正。但**自动化结果在无验证时已足够用于许多实际任务**（Section 5.3）。

### 4. 属性与关系计算

使用 off-the-shelf 学习和分析方法自动计算各节点的属性和节点间关系。

## 实验

### 数据集
- **Gibson Environment Database**: 572 个完整建筑，提供 3D mesh 模型、RGB 全景图和相机姿态信息
- 语义类别来自 COCO（物体）、MINC（材质）、DTD（纹理）
- 评估在 Gibson tiny split 上进行人工验证

### 评估设定
- **2D评估**：在全景图上评估，使用 COCO 评价协议
- **3D评估**：在 mesh 上投影后评估

### 基线
**2D 基线**：
1. Mask R-CNN [18]: 在全景图上采样 6 张无重叠 rectilinear 图像，检测结果投影回全景图
2. Mask R-CNN + Framing: 应用第一个鲁棒化机制
3. Mask R-CNN + Framing + MVC (Ours): 完整方法

**3D 基线**：
1. Mask R-CNN + Pano Projection: 简单投影 + 逐面多数投票
2. Mask R-CNN + Framing + Pano Projection
3. Mask R-CNN + Framing + MVC (Ours): 完整方法

### 检测器设置
- 主检测器：Mask R-CNN with Bells & Whistles (Detectron)，ResNeXt-152 (32x8d) + FPN，ImageNet-5K 预训练 + COCO fine-tune，报告 AP 41.5 on COCO
- 次级检测器（消融）：BlitzNet [15]，AP 34.1 on COCO

### 人工标注时间对比

3D Scene Graph 自动化 vs 人工标注时间（Table 3）：

| 方法 | AP | 耗时 (h) |
|------|----|---------|
| Ours fully automatic (FA) | 0.389 | 0 |
| Ours + manual verification (MV) | 0.97 | 03:18:02 |
| Fully manual 2D (FM 2D) | 1 | 12:44:10 |
| Fully manual 3D (FM 3D) [7] | 1 | 10:18:06 |

> 注：全手动 3D 标注仅 12 个类别（ours 62 类）且为专业标注员。

## 结果

### 主要结果：自动检测性能（Table 2）

| 模态 | 方法 | AP | AP.50 | AP.75 | AR |
|------|------|-----|-------|-------|----|
| **2D** | Mask R-CNN [18] | 0.079 | 0.166 | 0.070 | 0.151 |
| 2D | Ours w/ Framing | 0.160 | 0.316 | 0.147 | 0.256 |
| **2D** | **Ours w/ Framing + MVC** | **0.485** | **0.610** | **0.495** | **0.537** |
| 3D | Mask R-CNN + Pano Projection | 0.222 | 0.445 | 0.191 | 0.187 |
| 3D | Ours w/ Framing + Pano Projection | 0.306 | 0.539 | 0.322 | 0.261 |
| **3D** | **Ours w/ Framing + MVC** | **0.409** | **0.665** | **0.421** | **0.364** |

**关键发现**：Framing + MVC 在 2D 上相比原始 Mask R-CNN 提升 **AP 6.1×**（0.079→0.485），在 3D 上提升 **AP 1.84×**（0.222→0.409）。

### 不同检测器鲁棒性（Table 4）

| 方法 | Mask R-CNN (AP 41.5) | BlitzNet (AP 34.1) |
|------|---------------------|-------------------|
| Baseline | 0.079 | 0.095 |
| + Framing | +0.081 | +0.103 |
| + Framing + MVC | +0.406 | +0.189 |
| Baseline 3D | 0.222 | 0.076 |
| + Framing + Pano Proj | +0.084 | +0.089 |
| + Framing + MVC | +0.187 | +0.169 |

**关键发现**：两种检测器均从鲁棒化机制中获得相似幅度的提升，表明机制与检测器无关。

### Scene Graph Predicate 分类结果（Table 5）

| Predicate | Baseline（统计猜测） | Ours |
|-----------|-------------------|------|
| Spatial Order (mAP) | 0.255 | **0.712** |
| Relative Volume (mAP) | 0.555 | **0.820** |

- **Spatial Order**：给定 RGB rectilinear 图像和可见分割掩码，预测目标物体在前/后、左/右。训练用 ResNet34，使用自动生成的掩码（Gibson medium split）。
- **Relative Volume**：预测目标物体体积比另一物体大/小。

### Amodal Mask 分割结果（Table 6）

| 方法 | F1-avg | IoU-avg |
|------|--------|---------|
| Avg. Amodal Mask | 0.479 | 0.405 |
| Avg. Class Specific Amodal Mask | 0.545 | 0.455 |
| **Amodal Prediction (Ours)** | **0.672** | **0.549** |

Occluded 区域的 F1 大幅领先：0.414 (Ours) vs 0.097 (Class Specific) vs 0.000 (Avg)，表明模型成功学习了 amodal 感知。

## 局限性

1. **限于静态室内场景**：不包括室外相关属性或动作相关关系
2. **物体类别稀疏**：当前标注在某些区域偏稀疏，计划扩展至更多常见室内物体
3. **依赖预定义类别**：自动检测受限于 COCO 预定义类别集（62 类），相对于 Visual Genome 的自由文本标注更受限制
4. **仍需验证步骤**：虽然自动化结果可独立使用，但高精度场景仍需人工验证

## 可复用 Claims

1. **3D 空间作为语义锚点更稳定**：相比 2D 图像，3D 空间对各种参数变化更不敏感，且可投影到任意视觉观测，提供免费的 3D amodal、遮挡和开敞空间分析
2. **Framing + Multi-View Consistency 是通用鲁棒化机制**：可在不改变底层检测器的情况下显著提升 2D→3D 语义标注质量（~6× AP 提升），且检测器无关
3. **场景图结构天然适合 3D 分层语义**：Building→Room→Object→Camera 四层结构可容纳多类型语义，且跨层和层内关系均可编码
4. **自动生成 2D 场景图的优势**：从 3D 场景图可投影任意数量的空间一致 2D 场景图，为 2D 任务提供自动标注

## 影响力与关联

- **开创性工作**：定义了 3D 场景图的概念和结构，后续几乎所有的 3D 场景图工作均引用此论文
- **数据集贡献**：将 Gibson Environment 数据库从纯几何扩展为带语义标注的资源
- **后续相关工作**：
  - [3DSSG / Incremental 3D Scene Graph](incremental-3d-scene-graph-prediction-from-rgb-sequences.md): 从 RGB 序列增量构建 3D 场景图
  - [CCL-3DSGG](ccl-3dsgg-clip-driven-open-vocabulary-3d-scene-graph-generation.md): CLIP-Driven 开放词汇 3D 场景图
  - [FunGraph](fungraph-functionality-aware-3d-scene-graphs.md): 功能感知 3D 场景图
  - [Open3DSG](open3dsg-open-vocabulary-3d-scene-graphs-from-point-clouds.md): 开放词汇 3D 场景图
  - [ZING-3D](zing-3d-zero-shot-incremental-3d-scene-graphs.md): 零样本增量式 3D 场景图

## 开放问题

1. 如何扩展到动态场景和室外场景？
2. 如何在无需人工验证的条件下达到完全自动的高精度 3D 场景图构建？
3. 3D 场景图在机器人导航、语义搜索等下游任务中的实际价值是否超过其构建开销？

## 来源追溯

- **PDF 源**: `raw/sources/2019-10-01-3d-scene-graph-unified-semantics-3d-space-camera.pdf`
- **提取文本**: `raw/sources/2019-10-01-3d-scene-graph-unified-semantics-3d-space-camera.txt`
- **Evidence level**: full-paper（全文精读，10页正文完整提取）
