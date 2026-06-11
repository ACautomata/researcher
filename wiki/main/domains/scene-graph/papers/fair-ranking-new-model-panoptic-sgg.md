---
title: "A Fair Ranking and New Model for Panoptic Scene Graph Generation"
tags:
  - scene-graph-generation
  - panoptic-scene-graph
  - evaluation
  - DSFormer
arxiv: "2407.09216"
created: 2026-06-10
source: https://arxiv.org/pdf/2407.09216
confidence: full-paper
authors:
  - Julian Lorenz
  - Alexander Pest
  - Daniel Kienzle
  - et al.
venue: arXiv 2024
---

## Paper Info

揭示 MultiMPO 缺陷（重复 mask/关系），提出 SingleMPO 修正协议。DSFormer 二阶段架构（ResNet-50+ViT, 50M）。

## Key Results (PSG, SingleMPO)

| 方法 | SGGen mR@50 | 原MultiMPO差异 |
|------|:---:|:---:|
| HiLo | 18.33 | **-19.27** (虚高) |
| Pair-Net | 19.64 | -8.86 |
| **DSFormer** | **30.67** | **+11.03 vs HiLo** |

PredCls mR@50=40.06。二阶段方法不受评估漏洞影响。

## Provenance

- **Source**: arXiv 2407.09216
- **Evidence level**: full-paper
