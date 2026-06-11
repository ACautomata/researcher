---
title: "Multiview Scene Graph (MSG)"
tags:
  - scene-graph-generation
  - multiview
  - topological-mapping
  - NeurIPS-2024
arxiv: "2410.11187"
created: 2026-06-10
source: https://arxiv.org/pdf/2410.11187v1
confidence: full-paper
authors:
  - Juexiao Zhang
  - Gao Zhu
  - Sihang Li
  - et al.
venue: NeurIPS 2024
code: https://ai4ce.github.io/MSG/
---

## Paper Info

从无位姿 RGB 图像构建 place+object 拓扑图，不依赖 metric map/depth/pose。

## Method

**AoMSG**: DINOv2 encoder + DETR-like Transformer decoder + 联合对比学习 place/object embeddings

## Key Results

| 方法 | R@1 | PP IoU | PO IoU (GT det) |
|------|:---:|:---:|:---:|
| AoMSG-4 | **98.3** | **42.2** | **74.2** |
| SepMSG-Linear | 96.9 | 34.9 | 59.3 |
| NetVLAD | 96.6 | 35.5 | — |

MLLM pilot: GPT-4o PP IoU=63.0, PO IoU=85.0 (单场景, 22 images)

## Provenance

- **Source**: arXiv 2410.11187
- **Evidence level**: full-paper
