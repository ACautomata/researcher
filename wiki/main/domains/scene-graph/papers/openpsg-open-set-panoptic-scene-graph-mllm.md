---
title: "OpenPSG: Open-set Panoptic Scene Graph Generation via Large Multimodal Models"
tags:
  - scene-graph-generation
  - panoptic-scene-graph
  - open-set
  - MLLM
  - ECCV-2024
arxiv: "2407.11213"
created: 2026-06-10
source: https://arxiv.org/pdf/2407.11213
confidence: full-paper
authors:
  - Zijian Zhou
  - Miaojing Shi
  - Holger Caesar
venue: ECCV 2024
---

## Paper Info

首篇 open-set PSGG。利用 MLLM 语义空间 + 开放集关系分类头。预定义+开放关系联合建模。

## Key Results

| 场景 | 指标 | Score |
|:---|:---:|:---:|
| PSG closed PredCls | R@100 | **79.3** |
| PSG closed PredCls | mR@100 | **63.8** |
| PSG open PredCls | R@100 | **61.5** |
| PSG open PredCls | mR@100 | **46.0** |
| VG closed PredCls | R@100 | **71.4** |
| GQA closed | R@100 | **48.3** |

SGDet 在 PSG open-set 上 R@100=36.7, mR@100=25.4。

## Provenance

- **Source**: arXiv 2407.11213
- **Evidence level**: full-paper
