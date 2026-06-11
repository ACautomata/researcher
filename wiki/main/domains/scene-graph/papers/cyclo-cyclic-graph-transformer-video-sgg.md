---
title: "CYCLO: Cyclic Graph Transformer for Multi-Object Relationship Modeling in Aerial Videos"
tags:
  - scene-graph-generation
  - graph-transformer
  - video
  - aerial
  - NeurIPS-2024
arxiv: "2406.01029"
created: 2026-06-10
source: https://arxiv.org/pdf/2406.01029
confidence: full-paper
authors:
  - Trong-Thuan Nguyen
  - Pha Nguyen
  - Xin Li
  - et al.
venue: NeurIPS 2024
---

## Paper Info

循环注意力机制（mod T 索引环形拓扑），首个航拍 VidSGG AeroEye 数据集（2260 视频/4300万+关系）。

## Key Results (AeroEye PredCls)

| 方法 | R@20 | mR@20 |
|------|:---:|:---:|
| Transformer | 53.25 | 14.25 |
| HIG | 54.18 | 18.37 |
| **CYCLO** | **56.20** | **19.23** |

PVSG R@20=5.83 (+1.23 vs HIG)。η=1 最优（非排列等变验证）。

## Provenance

- **Source**: arXiv 2406.01029
- **Evidence level**: full-paper
