---
title: "Pair-Net: Pair then Relation for Panoptic Scene Graph Generation"
tags:
  - scene-graph-generation
  - panoptic-scene-graph
  - pair-proposal
  - TPAMI-2024
arxiv: "2307.08699"
created: 2026-06-10
source: https://arxiv.org/pdf/2307.08699
confidence: full-paper
authors:
  - Jinghao Wang
  - Zhengyu Wen
  - Xiangtai Li
  - et al.
venue: IEEE TPAMI 2024
code: https://github.com/king159/Pair-Net
---

## Paper Info

Pair Proposal Network (PPN) + Matrix Learner (CNN) 显式建模 subject-object 配对。揭示 PSG 瓶颈是 pair recall 而非分割质量。

## Key Results (PSG)

| 方法 | mR@20 | R@20 | Pair R@20 |
|------|:---:|:---:|:---:|
| PSGFormer | 14.5 | 18.0 | 28.6 |
| Pair-Net | **24.7** | **29.6** | **52.7** |

CNN-tiny (0.2M) 最佳。Seesaw Loss > 其他 loss。正样本权重至关重要（无则 mR@20=0.6）。

## Provenance

- **Source**: arXiv 2307.08699
- **Evidence level**: full-paper
