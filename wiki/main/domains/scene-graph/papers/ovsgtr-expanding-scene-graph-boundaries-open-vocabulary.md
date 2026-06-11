---
title: "OvSGTR: Expanding Scene Graph Boundaries — Fully Open-vocabulary SGG via Visual-Concept Alignment and Retention"
tags:
  - scene-graph-generation
  - open-vocabulary
  - visual-concept-alignment
  - knowledge-distillation
arxiv: "2311.10988"
created: 2026-06-10
source: https://arxiv.org/pdf/2311.10988
confidence: full-paper
authors:
  - Zijian Zhou
  - Miaojing Shi
  - Holger Caesar
venue: arXiv 2024 (Same group as VLPrompt/HiLo)
---

## Paper Info

全开放词汇 SGG 统一框架（OvSGTR），4 种场景：Closed-set / OvD / OvR / OvD+R。Visual-concept alignment + 知识蒸馏防止关系遗忘。

## Key Results

| 场景 | 指标 | 分数 |
|:---|:---:|:---:|
| Closed-set | R@100 (Swin-B) | **42.4** |
| OvD-SGG | Novel R@50 | **15.58** (+19.6% vs VS3) |
| OvR-SGG | Novel R@50 | **13.45** (from 0.34) |
| OvD+R-SGG | Joint R@100 | **21.02** |

蒸馏 λ=0.1 最优；COCO Caption 零样本 R@100=10.90。

## Provenance

- **Source**: arXiv 2311.10988
- **Evidence level**: full-paper
