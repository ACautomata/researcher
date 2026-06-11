---
title: "Enhancing SGG with Hierarchical Relationships and Commonsense"
tags:
  - scene-graph-generation
  - hierarchical-relations
  - commonsense-validation
  - WACV-2025
arxiv: "2311.12889"
created: 2026-06-10
source: https://arxiv.org/pdf/2311.12889
confidence: full-paper
authors:
  - Bowen Jiang
  - Zhijun Zhuang
  - et al.
venue: WACV 2025
code: https://github.com/bowen-upenn/scene_graph_commonsense
---

## Paper Info

HIERCOM 框架：分层关系头 (HIER) + 常识验证流水线 (COM)，即插即用模块。

## Method

- **HIER**: 基于 Bayes 的分层分类（4 超类别），监督对比损失
- **COM**: LLM (LLaMA-3-8B/GPT-3.5) 常识三元组验证，并支持蒸馏

## Key Results (VG PredCLS)

| 方法 | R@50 | mR@50 |
|------|:---:|:---:|
| Baseline+HIERCOM | **75.6** | **23.9** |
| Motifs+HIERCOM | 69.5 | 25.1 |
| VCTree+HIERCOM | 69.8 | 26.3 |
| Motifs+NICE+HIERCOM | 58.2 | 33.1 |
| Motifs+IETrans+HIERCOM | 60.4 | 38.0 |

长尾提升显著。LLaMA-3-8B ≈ GPT-3.5 验证效果。蒸馏后推理差异 <1%。

## Provenance

- **Source**: arXiv 2311.12889
- **Evidence level**: full-paper
