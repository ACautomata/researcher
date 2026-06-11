---
title: "From Easy to Hard: Learning Curricular Shape-aware Features for Robust Panoptic Scene Graph Generation (CAFE)"
tags:
  - scene-graph-generation
  - panoptic-scene-graph
  - curriculum-learning
  - shape-aware
created: 2026-06-10
source: https://arxiv.org/pdf/2407.09191
confidence: full-paper
authors:
  - Hanrong Shi
  - Lin Li
  - Jun Xiao
  - Yueting Zhuang
  - Long Chen
venue: arXiv 2024 (submitted to IJCV)
---

## Paper Info

- **Title**: From Easy to Hard: Learning Curricular Shape-aware Features for Robust Panoptic Scene Graph Generation
- **Venue**: arXiv 2024 (submitted to IJCV)
- **Dataset**: PSG (48,749 images, 133 obj, 56 rel)
- **Backbone**: ResNet-50-FPN, Panoptic FPN

## Abstract

CAFE — 课程形状感知特征学习，模型无关的 PSG 框架。引入 mask/boundary 特征超越传统 bbox，三阶段课程学习按谓词认知难度分组训练。Mean 指标 VCTree+CAFE 40.6（SOTA），Tail R@100 从 0.3% 提升至 16.8%。

## Method

### 形状感知特征

- **Mask Features**: 二值掩码 erosion + Zernike moments → 256 维
- **Boundary Features**: subject∩object mask 轮廓 → 256 维

### 三阶段课程学习

| 阶段 | 谓词难度 | 特征 | 复杂度 |
|------|----------|------|--------|
| Stage-1 | 简单（over） | bbox | 低 |
| Stage-2 | 中等（walking on） | bbox + mask | 中 |
| Stage-3 | 困难（enclosing） | bbox + mask + boundary | 高 |

**Top-Down 知识蒸馏**保留下游知识。

## Experiments

### PredCls Mean（PSG）

| 基线 | Mean |
|------|:---:|
| Motifs+CAFE | **39.7** |
| VCTree+CAFE | **40.6** |
| Transformer+CAFE | **40.0** |

### SGDet Mean

| 方法 | Mean |
|------|:---:|
| VCTree+CAFE | **28.9**（vs DWIL 18.4） |

### Zero-shot Average

| 基线 | Average |
|------|:---:|
| Transformer+CAFE | **46.1**（vs 37.6）|

### 尾部提升

Tail R@100: Motifs 0.3% → CAFE **16.8%**

## Results

- 全面超越 SOTA: Mean +2.6 (40.6 vs C-SGG 38.0)
- SGDet 提升 +10.5 (28.9 vs 18.4)
- Zero-shot 提升 +8.5
- 单 NVIDIA 2080Ti 可训练

## Limitations

1. 仅两阶段 PSG 框架
2. 知识蒸馏增加训练开销
3. 未扩展到一阶段/视频

## Provenance

- **Source**: arXiv 2407.09191
- **Evidence level**: full-paper
