---
title: "Scene-Graph ViT: End-to-End Open-Vocabulary Visual Relationship Detection"
tags:
  - scene-graph-generation
  - open-vocabulary
  - vit
  - vrd
arxiv: "2403.14270"
created: 2026-06-10
source: https://arxiv.org/pdf/2403.14270
confidence: full-paper
authors:
  - Tim Salzmann
  - Markus Ryll
  - Alex Bewley
  - Matthias Minderer
venue: arXiv 2024 (Google DeepMind)
---

## Paper Info

纯编码器开放词汇 VRD。OWL-ViT + Relationship Attention（分离 subject/object MLP）。两阶段硬注意力选择。B/32 达 52.8 FPS。

## Key Results

| 基准 | 方法 | mR@100 |
|------|:---:|:---:|
| VG150 | DT2-ACBS | 24.4 |
| VG150 | **SG-ViT L/14** | **26.1** |
| GQA200 | SHA+GCL | 20.1 |
| GQA200 | **SG-ViT L/14** | **22.9** |

HICO-DET mAP 38.11（稀有关 33.71 vs UniVRD 28.90）。

## Provenance

- **Source**: arXiv 2403.14270
- **Evidence level**: full-paper
