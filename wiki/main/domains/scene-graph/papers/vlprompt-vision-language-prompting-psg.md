---
title: "VLPrompt: Vision-Language Prompting for Panoptic Scene Graph Generation"
tags:
  - scene-graph-generation
  - panoptic-scene-graph
  - vision-language-prompting
  - llm
arxiv: "2311.16492"
created: 2026-06-10
source: https://arxiv.org/pdf/2311.16492
confidence: full-paper
authors:
  - Zijian Zhou
  - Miaojing Shi
  - Holger Caesar
venue: arXiv (Under Review)
code: https://github.com/franciszzj/VLPrompt
---

## Paper Info

首个将 LLM 引入 PSG。Relation Proposer + Relation Judger 双提示提取常识 → 双 decoder 门控融合。

## Key Results (PSG)

| 方法 | R@100 | mR@100 |
|------|:---:|:---:|
| HiLo | 43.0 | 33.1 |
| **VLPrompt** | **52.4** | **53.7** |

罕见关系 mR@100 提升 +13.8 (37.9→51.7)。推理时无需 LLM（预提取效率同 152ms）。

## Provenance

- **Source**: arXiv 2311.16492
- **Evidence level**: full-paper
