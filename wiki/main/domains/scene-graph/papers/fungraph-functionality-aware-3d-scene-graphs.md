# FunGraph: Functionality-Aware 3D Scene Graphs for Language-Prompted Scene Interaction

[[scene-graph]] | [[3dsg]] | [[affordance]] | [[functional-elements]]

- **Title**: FunGraph: Functionality-Aware 3D Scene Graphs for Language-Prompted Scene Interaction
- **Authors**: Dennis Rotondi, Fabio Scaparro, Hermann Blum, Kai O. Arras
- **Affiliations**: University of Stuttgart (Socially Intelligent Robotics Lab), University of Bonn (Robot Perception and Learning Lab)
- **Venue**: IROS 2025
- **arXiv**: [2503.07909v2](https://arxiv.org/abs/2503.07909)
- **Project**: https://fungraph.github.io
- **Code**: https://fungraph.github.io
- **Evidence Level**: full-paper
- **Status**: active
- **Date**: 2026-06-09

## 概述

FunGraph 是首个在 3D 场景图（3DSG）中显式建模**功能交互元素（functional elements）** 和 **intra-object 关系**的框架。传统 3DSG 只建模到 room 和 object 级别，无法支持机器人的细粒度场景交互（如"打开冰箱门"、"调节恒温器"）。FunGraph 将 functional interactive elements（把手、按钮、旋钮、开关等）作为独立的子节点纳入 3DSG 层次结构，通过 intra-object "has-part" 关系与父对象建立连接。

## 方法

### Pipeline

1. **2D 数据生成**：从 SceneFun3D 数据集的 3D 标注点云投影生成带 bounding box 的 2D 图像标注（274,022 个标注，132,635 张图像）
2. **2D 检测**：训练 RT-DETR（在 ST 切片数据集上），用于检测图像中的功能性交互元素
3. **3D 场景图生成**：基于 ConceptGraphs [3] 风格的 pipeline，包含检测 → 节点创建（多视角几何+语义融合）→ 边创建（inter-object spatial + intra-object has-part）
4. **上下文标签精炼**：使用 GPT-4o 对对象-功能元素组进行语义描述精炼

### 关键设计

- 采用 YOLO-World v8.2 检测 objects + RT-DETR 检测 functional elements
- SAM2 做通用分割，GPT-4o 做 VLM 推理
- **Slicing-aided Hyper Inference (SAHI)** 用于提高小目标检测性能
- intra-object 关系不破坏 3DSG 的层次属性（单父节点、局部性、不相交子节点）

## 实验与结果

### 实验 1：2D 功能元素检测（Table I）

| Model | Dataset | mAP50:95 | mAP50 |
|-------|---------|----------|-------|
| YOLO-World v8.2 | zero-shot | 0.0 | 0.0 |
| GroundingDINO | zero-shot | 0.0 | 0.7 |
| YOLOv11 | T | 7.5 | 22.4 |
| **RT-DETR** | **T** | **8.6** | **26.7** |
| YOLOv11 | ST | 13.6 | 15.0 |
| **RT-DETR** | **ST** | **21.0** | **26.2** |

- 零样本检测器完全无法检测功能元素（mAP ≈ 0）
- RT-DETR + ST（切片训练）效果最佳
- SAHI 主要提升 bounding box 精度（mAP50:95 从 8.6→21.0），而非检测率（mAP50 持平）

### 实验 2：3D 功能元素分割（Table II）

| Affordance | AP | AP50 | AP25 | AP10 |
|------------|------|------|------|------|
| Foot Push | 0.0 | 0.0 | 20.0 | 46.7 |
| Tip Push | 10.0 | 19.9 | 28.4 | 28.4 |
| Rotate | 6.1 | 19.9 | 25.6 | 28.6 |
| Pinch Pull | 1.7 | 6.6 | 24.8 | 31.5 |
| Hook Pull | 0.0 | 0.0 | 10.1 | 10.1 |
| Hook Turn | 9.5 | 25.2 | 37.7 | 59.0 |
| Key Press | 14.1 | 40.4 | 65.8 | 65.8 |
| **Average** | **5.9** | **16.0** | **30.3** | **38.6** |

- Mask3D-F 基准（SceneFun3D 报告）参考值：AP=[7.9], AP50=[18.3], AP25=[26.6]
- 与 3D 直接分割方法（Mask3D-F）效果相当
- Foot Push 和 Hook Pull 表现差（背景噪声导致遮罩不完美）
- 置信度消融（Table III）：θbbox=0.4 最优（AP25=30.3）

### 实验 3：Affordance Grounding（Table IV）

| Method | AP25 | AP>0 |
|--------|------|------|
| ConceptGraphs [3] | 0.0 | 31.3 |
| **FunGraph (ours)** | **33.3** | **58.6** |

- 在 SceneFun3D 的 10 个场景、99 个任务查询上评估
- FunGraph AP25=33.3% **显著优于** ConceptGraphs 的 0.0%（ConceptGraphs 只能返回完整 object 点云，缺乏功能元素粒度）
- SceneFun3D [5] 最优模型 AP25=17.5（参考值）
- 3DSG 表示比直接点云检索更适合回答任务驱动的 affordance 查询

### 实验 4：标签精炼消融（Table V）

| Method | Correct | Partial | Wrong |
|--------|---------|---------|-------|
| CLIP | 30.0% | 28.0% | 42.0% |
| GPT-No-Context | 52.0% | 28.0% | 20.0% |
| **GPT-Context** | **78.0%** | **16.0%** | **6.0%** |

- GPT-Context（结合对象上下文）正确率 78%，远超其他方法
- 功能元素尺寸小导致 CLIP bag-of-words 行为失效

## 主要结论

1. **首个**在 3DSG 中系统引入 intra-object 关系的框架
2. 2D→3D 的投影方法可以在不依赖高价 LiDAR 的情况下达到与 3D SOTA 相当的分割性能
3. 3DSG 格式天然适合 LLM 解析，在 task-driven affordance grounding 上优于直接点云方法
4. 适用于低成本 RGB-D 传感器的机器人平台

## 局限性

- 未建模 intermediate object parts（如 knob 与 drawer 的关系而非 knob 与 cabinet）
- 跨对象共享功能元素（如烤箱+灶台上的旋钮）容易产生关联错误
- 依赖 SceneFun3D 的资源，覆盖范围有限
- 数据集提供的相机位姿有时不精确，影响 3D 融合质量

## Provenance

- **来源文件**: `sources/scene-graph/2025-06-09-FunGraph.pdf` (6.2 MB)
- **提取文本**: `sources/scene-graph/2025-06-09-FunGraph.txt` (47.7 KB)

## 关联论文

- [[conceptgraphs-open-vocabulary-3d-scene-graphs]] — Vision-and-Language 3DSG 基础架构
- [[scene-function-3d-fine-grained-functionality-affordance-understanding-3d-scenes]] — 功能元素标注数据集
- [[incremental-3d-scene-graph-prediction-from-rgb-sequences]] — 增量 3DSG 预测
- [[hierarchical-open-vocabulary-3d-scene-graphs-for-language-grounded-robot-navigation]] — 层次化 3DSG
