---
title: "CoPa-SG: Dense Scene Graphs with Parametric and Proto-Relations"
tags:
  - scene-graph-generation
  - dense-scene-graph
  - parametric
  - proto-relations
created: 2026-06-10
source: https://arxiv.org/pdf/2506.21357
confidence: full-paper
authors:
  - Julian Lorenz
  - Mrunmai Phatak
  - Robin Schön
  - et al.
venue: arXiv Jun 2025
---

## Paper Info

- **Title**: CoPa-SG: Dense Scene Graphs with Parametric and Proto-Relations
- **Venue**: arXiv Jun 2025 (Univ. Augsburg)
- **Code**: anonymous.4open.science/r/paper-26E0
- **Dataset**: COPA-SG (86M+ relations, 1.2k scenes, 36k images)

## Abstract

COPA-SG — 基于 Infinigen 的室内密集场景图数据集，100% 覆盖率。引入 parametric relations（关系附加角度/距离参数）和 proto-relations（体素场编码假设性关系）。8 种 predicate classes。

## Method

**Parametric relations**: `(subject, object, predicate, α, camera_extrinsics, test_direction)` — 连续参数
**Proto-relations**: `(anchor_object, predicate_class, volume/area)` — OpenVDB 体素场，支持 CSG

## Experiments

### 数据集对比

| 数据集 | #Relations | Coverage |
|--------|:---:|:---:|
| VG | 2.3M | 3.4% |
| PSG | 275K | 12.6% |
| **COPA-SG** | **86M** | **100%** |

### PredCls

| 方法 | mAP |
|------|:---:|
| DSFormer | **67.0** |
| VCTree | 63.9 |

### Parametric 预测 (RGB+4Blocks)

mAP 79.05, 参数误差 15.44°

## Results

- DSFormer 在 COPA-SG 上 > MotifNet/VCTree
- 多视图聚合 ~15 views 饱和，AP +6.2

## Limitations

1. 合成数据 domain gap 待验证
2. 参数误差 ~15° 仍有差距
3. Proto-relation 框架固有用例

## Provenance

- **Source**: arXiv 2506.21357
- **Evidence level**: full-paper
