---
title: "Hydra-SGG: Hybrid Relation Assignment for One-stage Scene Graph Generation"
tags:
  - scene-graph-generation
  - one-stage
  - hybrid-assignment
  - ICLR-2025
arxiv: "2409.10262"
created: 2026-06-10
source: https://arxiv.org/pdf/2409.10262
confidence: full-paper
authors:
  - Zeyu Zhang
  - et al.
venue: ICLR 2025
---

## Paper Info

发现 one-to-one 指派中 Self-Attention 冲突问题。每类固定 6 个查询（Hydra Branch）+ 混合指派。

## Key Results

| 基准 | 指标 | Hydra-SGG | 之前SOTA |
|:---|:---:|:---:|:---:|
| VG150 | mR@50 | **16.0** | 12.4 (PE-Net) |
| OpenImages V6 | score_wtd | **50.0** | — |
| GQA | mR@50 | **12.7** | — |

10× 收敛加速。无需专用去偏即超越 IETrans/CFA。仅 12 epoch 已达最佳。

## Provenance

- **Source**: arXiv 2409.10262
- **Evidence level**: full-paper
