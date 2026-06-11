---
title: "HOIverse: Synthetic Scene Graph Dataset With Human Object Interactions"
tags:
  - scene-graph-generation
  - synthetic-dataset
  - hoi
created: 2026-06-10
source: https://arxiv.org/pdf/2506.19639
confidence: full-paper
authors:
  - Mrunmai Phatak
  - Julian Lorenz
  - Nico Hörmann
  - et al.
venue: arXiv Jun 2025
---

## Paper Info

- **Title**: HOIverse: A Synthetic Scene Graph Dataset With Human Object Interactions
- **Venue**: arXiv Jun 2025 (Univ. Augsburg)
- **Method**: Infinigen + SMPL-X + automated relation annotation

## Abstract

融合 SGG 和 HOI 的合成数据集。Infinigen 场景 + SMPL-X 人体 + 自动化关系计算。525 场景，16.2k 图像，40k HOI，22M 关系标注。14 种交互类型。

## Dataset Scale

| 指标 | 值 |
|------|:---:|
| 场景 | 525 (Infinigen) |
| 图像 | ~16,200 |
| HOI 类型 | 14 种 |
| 关系标注 | ~22M |

### PredCls

| 方法 | mAP |
|------|:---:|
| DSFormer | **0.667** |
| VCTree | 0.511 |

## Results

- 首个 SGG+HOI 合成数据集
- 三种新参数化关系: looking at, pointing at, body facing
- 含第一人称视角和 3D 关键点

## Provenance

- **Source**: arXiv 2506.19639
- **Evidence level**: full-paper
