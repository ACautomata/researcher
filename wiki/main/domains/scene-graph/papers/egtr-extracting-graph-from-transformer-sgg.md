---
title: "EGTR: Extracting Graph from Transformer for Scene Graph Generation"
tags:
  - scene-graph-generation
  - transformer
  - graph-extraction
  - efficient
arxiv: "2404.02072"
created: 2026-06-10
source: https://arxiv.org/pdf/2404.02072
confidence: full-paper
authors:
  - Kaifeng Gao
  - et al.
venue: CVPR 2024
---

## Paper Info

直接从 DETR decoder 特征中提取关系图。Relation Extractor（Gated Sum + 3 层 MLP）+ Adaptive Smoothing + Connectivity Prediction。无额外关系解码器。

## Key Results

| 基准 | 指标 | EGTR | 对比 |
|:---|:---:|:---:|:---:|
| VG | AP50 | **30.8** | SOTA + 参数量最少(42.5M) + FPS最快(14.7) |
| OI V6 | score | **48.6** | wmAPrel **42.0** 最高 |

硬负采样策略提升 AP 约 2 个点。Adaptive Smoothing 稳定训练。

## Provenance

- **Source**: arXiv 2404.02072
- **Note**: 原 URL 2401.02724 指向不同论文（数学论文），实际论文为 2404.02072
- **Evidence level**: full-paper
