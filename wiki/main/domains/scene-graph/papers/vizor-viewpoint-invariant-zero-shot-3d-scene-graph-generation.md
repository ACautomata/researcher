---
title: "VIZOR: Viewpoint-Invariant Zero-Shot Scene Graph Generation for 3D Scene Reasoning"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags: [3D-SGG, zero-shot, viewpoint-invariant, open-vocabulary, object-grounding, arXiv-2026]
raw_sources:
  - ../../../sources/scene-graph/2026-arXiv-VIZOR-Viewpoint-Invariant-Zero-Shot-SGG.pdf
  - ../../../sources/scene-graph/2026-arXiv-VIZOR-Viewpoint-Invariant-Zero-Shot-SGG.txt
evidence_level: full-paper
---

# VIZOR: Viewpoint-Invariant Zero-Shot Scene Graph Generation for 3D Scene Reasoning

> arXiv 2602.00637, Jan 2026

## 摘要

VIZOR 提出首个**零样本、训练无关**的视角不变3D场景图生成框架。给定原始3D场景网格（mesh），直接构建稠密、视角不变的3D场景图。空间关系基于每个物体的前置朝向（front-facing direction）定义，确保不依赖观测者视角。同时推断开放词汇的空间/接近关系。

## 核心贡献

1. **首个零样本视角不变3D SGG**: 训练无关，仅需场景网格输入，无需RGB-D序列或标注数据集
2. **物体中心关系生成**: 基于每个物体的内在朝向建模空间关系，不受观测者视角影响
3. **稠密开放词汇场景图**: 节点含聚合多视角属性（颜色/几何/功能/描述），边为开放词汇关系对
4. **下游任务验证**: 在文本驱动的开放词汇物体定位（object grounding）上显著超越 SOTA 零样本方法

## 方法架构

### 三阶段流程

**阶段1：物体分割与前置朝向估计（Sec 3.1）**
- 使用 Mask3D 进行实例级3D分割
- 对每个物体，构建圆形相机轨迹（N个等距视角），渲染多视图图像
- 利用 Shap-E 生成该类别3D物体作为参考 → 参考图像库
- MLLM 比较渲染视图与参考图像，选择最匹配的前置视角
- 对称物体模糊时选择朝向场景中心的方向

**阶段2：节点属性提取（Sec 3.2）**
- 多视角渲染（前/顶/底 + 间隔视图）→ MLLM → 结构化JSON（颜色/几何/功能/结构/描述）
- LLM 聚合多视角 JSON 得到统一的节点属性集

**阶段3：边关系计算（Sec 3.3）**
- 基于物体中心、前置方向向量计算距离 + 角度
- 几何规则推导初始空间关系（front/behind/left/right/above/below/on 等）
- LLM 结合节点属性和几何特征生成开放词汇关系描述（含 "near"/"far" 等）

### 关键参数
- N = 12 个渲染视角（默认；与精度/代价平衡）
- K = 1500 关系剪枝（下游 grounding 时取 top-K 关系）
- 距离过滤器保留 3m 内物体对

## 实验结果

### 场景图构建（Replica，人类评估）

| 指标 | CG | CG-D | VIZOR (LLaMA) | VIZOR (GPT) |
|------|-----|------|--------------|------------|
| Node Precision | 0.71 | 0.61 | 0.65 | **0.88** |
| Front-View Precision | — | — | — | **0.88**（avg） |
| Edge Precision | — | — | 0.65 | 0.67 |
| # Edges (avg) | — | — | — | **276** |

- **Node Precision**: VIZOR-GPT 0.88，超越 CG 的 0.71（+17%）
- 比 CG 产生显著更稠密的图（最大场景 420 关系 vs CG 的稀疏图）

### 开放词汇物体定位（Replica 场景，人类评估 Top-1 Recall）

| 查询类型 | #Queries | CG-CLIP | CG-LLM | VIZOR-LLaMA | **VIZOR-GPT** |
|---------|----------|---------|-------|------------|--------------|
| Descriptive | 20 | 0.59 | 0.61 | 0.75 | **0.63** |
| Affordance | 5 | 0.43 | 0.57 | **0.80** | **0.80** |
| Negation | 5 | 0.26 | 0.80 | **0.90** | **1.00** |
| Complex-Spatial | 30 | 0.20 | 0.28 | 0.58 | **0.67** |
| **Overall** | 60 | 0.37 | 0.56 | 0.76 | **0.78** |

- VIZOR-GPT **Overall 0.78** vs CG-LLM 0.56（**+22% 提升**）
- Complex-Spatial 查询: **0.67** vs CG-LLM 0.28（**+39% 提升**）

### 开放词汇物体定位（Nr3D 数据集，Grounding Accuracy %）

| 方法 | Type | Overall | Easy | Hard | View-Dep | View-Indep |
|------|------|---------|------|------|---------|-----------|
| ReferIt3D | Supervised | 35.6 | 43.6 | 27.9 | 32.5 | 37.1 |
| ViL3DRel | Supervised | **64.4** | 70.2 | 57.4 | 62.0 | 64.5 |
| ZS-3DVG | Zero-shot | 39.0 | 46.5 | 31.7 | 36.8 | 40.0 |
| SeeGround | Zero-shot | 46.1 | 54.8 | 38.3 | 42.3 | 48.2 |
| VLM-Grounder | Zero-shot | 48.0 | 55.2 | 39.5 | 45.8 | 49.4 |
| **VIZOR-GPT (Ours)** | **Zero-shot** | **52.81** | **62.52** | **43.48** | 43.02 | **57.66** |

- **零样本 SOTA**: 52.81%，超越 VLM-Grounder 48.0（**+4.81%**）
- 接近部分全监督方法（如 SAT 49.2, 3D-SPS 51.5）
- 注意: 使用 GT object proposals（沿袭 ZS-3DVG 评估协议）

### 设计选择分析

**前置朝向估计方法对比（Front-View Precision %）:**

| 方法 | 扩散参考 | 前视图 | Front-View Precision |
|------|---------|--------|-------------------|
| ViT cosine similarity | ✗ | ✓ | 82.35 |
| Direct MLLM Query | ✗ | ✗ | 80.22 |
| LLM + 2D diffusion ref | ✓ | ✗ | 58.82 |
| **VIZOR** | ✗ | ✓ | **85.71** |

**视角数量影响（38 objects from Replica room0/office0）:**

| #Views | Front-View Prec (%) | Avg Time (Sec) | Avg Tokens |
|--------|-------------------|---------------|-----------|
| 8 | 82.36 | 4.02 | 1,045 |
| 12 | 85.71 | 6.67 | 1,387 |
| 16 | 86.24 | 10.03 | 1,726 |
| 20 | 86.92 | 14.21 | 2,081 |

**节点属性质量（1-5 Likert 评分）:**

| 变体 | Color | Geometry |
|------|-------|---------|
| VIZOR-LLaMA Single View | 3.62 | 2.27 |
| VIZOR-LLaMA Multi View | 3.68 | 2.28 |
| VIZOR-GPT Single View | 3.82 | 4.05 |
| **VIZOR-GPT Multi View** | **3.86** | **4.25** |

### 失败分析（1,645 关系，4 场景）

- **对称物体**: 37% 失败率（241/638），因对称物体的多个候选前视图等距场景中心
- **不完整物体**: MLLM 无法识别部分物体的几何结构
- **独立关系/噪声物体**: 失败率较低

## 分析与讨论

### 核心创新价值

VIZOR 的核心突破在于将 3D 场景图生成中的**视角偏置**问题彻底解决——传统的 3DSSG 等数据集的标注基于标注者的固定视角，导致 "left/right" 等方向在不同视角下矛盾。VIZOR 以前朝向为锚点定义关系，实现真正的视角不变性。

### 与现有零样本方法的比较

- **ConceptGraphs**: VIZOR 构建更稠密的图（276 vs ~50 边），节点精度更高（0.88 vs 0.71），在复杂空间推理上大幅领先（+39%）
- **VLM-Grounder / SeeGround**: VIZOR 的图结构显式捕获了全局场景布局和关系，弥补了纯 LLM 检索缺乏空间推理的不足

### 局限

1. 依赖 Mask3D 的 200 类可识别类别
2. 对称物体的前向估计准确率仅 63%（37% 失败率）
3. 定性/人类评估为主，缺乏标准化 SGG 指标（Recall/mRecall）
4. Nr3D 实验使用 GT proposals（非完全端到端）
5. 计算开销较大（MLLM 多视图推理）

### 开源与可重复性

项目页面提供代码和模型，但论文中未明确说明开源许可证。

---

## 相关页面

- [[conceptgraphs-open-vocabulary-3d-scene-graphs|ConceptGraphs: Open-Vocabulary 3D Scene Graphs for Perception and Planning]]
- [[open3dsg-open-vocabulary-3d-scene-graphs-from-point-clouds|Open3DSG: Open-Vocabulary 3D Scene Graphs from Point Clouds]]
- [[zing-3d-zero-shot-incremental-3d-scene-graphs|ZING-3D: Zero-shot Incremental 3D Scene Graphs via Vision-Language Models]]
- [[ccl-3dsgg-clip-driven-open-vocabulary-3d-scene-graph-generation|CCL-3DSGG: CLIP-Driven Open-Vocabulary 3D Scene Graph Generation]]
