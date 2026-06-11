---
title: "ReLaGS: Relational Language Gaussian Splatting"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - 3d-gaussian-splatting
  - scene-graph-generation
  - open-vocabulary-scene-graph
  - language-field-distillation
  - hierarchical-reasoning
  - relational-reasoning
  - graph-neural-network
  - zero-shot-transfer
  - arXiv-2026
raw_sources:
  - ../../../sources/scene-graph/2026-03-18-ReLaGS-Relational-Language-Gaussian-Splatting.pdf
  - ../../../sources/scene-graph/2026-03-18-ReLaGS-Relational-Language-Gaussian-Splatting.txt
related_pages:
  - gaussiangraph-3d-gaussian-scene-graph-generation.md
  - open3dsg-open-vocabulary-3d-scene-graphs-from-point-clouds.md
  - cage-sgg-counterfactual-active-graph-evidence-open-vocabulary-sgg.md
evidence_level: full-paper
paper:
  title: "ReLaGS: Relational Language Gaussian Splatting"
  abbreviated: "ReLaGS"
  authors:
    - Yaxu Xie
    - Abdalla Arafa
    - Alireza Javanmardi
    - Christen Millerdurai
    - Jia Cheng Hu
    - Shaoxiang Wang
    - Alain Pagani
    - Didier Stricker
  year: 2026
  venue: "arXiv (preprint)"
  arXiv: "2603.17605"
  code: null
  paper_url: "https://arxiv.org/abs/2603.17605"
  project_url: "https://dfki-av.github.io/ReLaGS/"
  affiliation: "DFKI / RPTU Kaiserslautern-Landau / University of Modena and Reggio Emilia"
---

# ReLaGS: Relational Language Gaussian Splatting

## 概述

ReLaGS 提出一个统一框架，将**层级化语言蒸馏高斯场景**与**开放词汇 3D 场景图**有机结合，在无需场景特定训练的条件下同时支持层级语义推理和关系推理。现有方法（如 RelationField、THGS、GaussianGraph）要么缺乏层级语义组织，要么无法高效捕获物体间关系，或依赖昂贵的逐场景优化。ReLaGS 通过三阶段流水线解决这一问题：层级高斯场景构建（基于 THGS + 改进）、语言特征注册、3D 场景图构建。

## 方法

### 核心架构

1. **Multi-Hierarchy Gaussian Representation**：基于 THGS 框架，对 3D Gaussian 场进行由下而上的层级聚类（sub-part → part → object），受多级 SAM 掩码引导，形成嵌套的语义层级结构 S(1),...,S(L)。

2. **Maximum Weight Pruning (MWP)**：去除在所有训练视图中贡献权重低于阈值 τ_contrib 的浮动高斯体（floaters），改善几何精度和层级聚类边界完整性。

3. **Robust Outlier-Aware Feature Aggregation (ROFA)**：聚合物体的多视图 CLIP 特征时，计算每个特征的 Z-score（基于与其他特征的余弦相似度），滤除 z_i < -τ_lang 的异常视图特征，得到一致的物体嵌入表示。

4. **3D Scene Graph Construction**：

   - **LLM-based Lifting**：利用 SoM (Set-of-Mark) 策略 + GPT-4V 对 2D 视图标注关系三元组 ⟨s,p,o⟩，通过像素-高斯对应关系提升到 3D。
   - **GNN-based Prediction**：轻量残差图神经网络 F_θ 直接从物体语言-几何融合特征预测关系嵌入，预训练于 3RScan 数据集，可直接零样本迁移到新场景。

5. **Hierarchical & Relational Querying**：
   - 层级搜索：在嵌套聚类树中自顶向下检索，自动区分物体级与部件级查询。
   - 三元组关系查询：在 3D 场景图上进行 ⟨s,p,o⟩ 关系检索，综合 subject-文本、object-文本、predicate-关系三种相似度排序。

## 关键贡献

1. 首个在同一 Gaussian 场中统一层级语义和关系推理的无需训练框架。
2. 提出 MWP 和 ROFA 两种改进模块，显著提升层级场景重建的几何和语义质量。
3. 提供两种 3D 场景图构建方案：LLM 标注提升（高精度但稀疏）和 GNN 预测（高效可扩展）。

## 实验与结果

### 3D 场景图预测（3DSSG RIO10 子集）

| 方法 | 场景无关 | Object R@5 | Object R@10 | Predicate R@3 | Predicate R@5 |
|------|---------|-----------|------------|-------------|-------------|
| ConceptGraphs [10] | ✗ | 0.37 | 0.46 | 0.74 | 0.79 |
| RelationField [19] | ✗ | 0.69 | 0.80 | 0.76 | 0.82 |
| Ours (VLM Lifting) | ✗ | 0.68 | 0.79 | 0.10 | 0.35 |
| Open3DSG [18] | ✓ | 0.56 | 0.61 | 0.58 | 0.65 |
| **Ours (GNN Pred.)** | ✓ | **0.68** | **0.79** | **0.79** | **0.87** |

- Predicate R@3: 0.79（比 RelationField 高 0.3），R@5: 0.87（比 RelationField 高 0.5）
- 比 RelationField 快 **4.7×**、内存效率高 **7.6×**

### 关系引导的 3D 实例分割（ScanNet++）

| 方法 | mIoU | 场景无关 |
|------|------|---------|
| Lerf [16] | 0.25 | ✗ |
| OpenNeRF [8] | 0.45 | ✗ |
| LangSplat [30] | 0.49 | ✗ |
| RelationField [19] | 0.53 | ✗ |
| THGS [7] | 0.29 | ✓ |
| Ours w/o MH | 0.54 | ✓ |
| **Ours** | **0.56** | ✓ |

- mIoU **0.56**，超越有训练的 RelationField (0.53) 和所有训练无关方法。

### 开放词汇分割（LeRF-OVS）

| 方法 | Mean | Figurines | Ramen | Teatime | Waldo Kitchen | T-F |
|------|------|-----------|-------|---------|---------------|-----|
| LangSplatV2 [23] | 56.4 | 51.4 | 72.2 | 59.1 | 59.9 | ✗ |
| LAGA [3] | 64.1 | 55.6 | 70.9 | 65.6 | 64.0 | ✗ |
| THGS [7] | 54.9 | 57.3 | 43.5 | 68.3 | 50.7 | ✓ |
| **Ours** | **64.4** | **64.7** | 51.2 | **81.0** | 60.6 | ✓ |

### 开放词汇语义分割（ScanNet）

| 方法 | 19 cls mIoU | 15 cls mIoU | 15 cls mAcc | 10 cls mIoU | 10 cls mAcc |
|------|------------|------------|------------|------------|------------|
| THGS [7] | 34.39 | 39.61 | 57.07 | 46.38 | 64.74 |
| Occam's [5] | 31.93 | 34.25 | 53.71 | 45.16 | 64.39 |
| **Ours** | 32.35 | **40.04** | **60.59** | **47.17** | **66.08** |

### 消融实验（LeRF-OVS）

| 变体 | Figurines | Ramen | Teatime | Kitchen | Mean |
|------|-----------|-------|---------|---------|------|
| Base (THGS baseline) | 52.05 | 47.19 | 76.77 | 47.5 | 55.88 |
| Base + MWP | 59.16 | 47.41 | 80.98 | 60.59 | 62.04 |
| Base + MWP + ROFA (完整) | **64.69** | **51.15** | **80.98** | **60.6** | **64.36** |

- MWP 贡献最大提升（+6.16 Mean IoU），ROFA 在密集遮挡场景（Figurines、Ramen）效果最显著。

### 运行时与内存

- 场景图构建 < **15 分钟**
- 渲染帧率 > **200 fps**
- 语义结构化表示内存开销 < **25%**

## 分析

### 与相关方法对比

| 维度 | RelationField | GaussianGraph | THGS | ReLaGS (Ours) |
|------|--------------|--------------|------|---------------|
| 训练要求 | 逐场景优化 | 场景特定训练 | 无需训练 | 无需训练 |
| 层级语义 | ✗ | ✗ | ✓ (object only) | ✓ (sub-part/part/object) |
| 关系推理 | ✓ (implicit) | ✓ (implicit) | ✗ | ✓ (explicit 场景图) |
| 显式场景图 | ✗ | ✗ | ✗ | ✓ |
| 渲染帧率 | < 10 fps | — | > 200 fps | > 200 fps |
| 内存效率 | 1× | — | — | 7.6× 优于 RelationField |

### 局限性

- VLM-based 关系提升在 3D 场景图预测中表现差（Predicate R@3 = 0.10），因缺乏空间推理能力。
- 在 ScanNet 19 类子集上 mIoU (32.35) 低于部分方法，作者归因于评估协议中无法使用 MWP 组件。
- 对 τ_contrib 和 τ_lang 超参数敏感，需针对场景调整。

## 笔记

- 使用 Jina-Embedding-V3 作为关系嵌入空间，支持开放词汇谓词查询。
- MWP 基于最大加权去除策略，灵感来自高斯泼溅中透明度权重的观察。
- ROFA 在 Ramen 场景（透明/半透明表面）和 Figurines（密集排列/遮挡）场景中效果最显著。
