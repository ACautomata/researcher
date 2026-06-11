---
title: "Synthetic Visual Genome (SVG)"
tags:
  - scene-graph-generation
  - synthetic-dataset
  - visual-genome
  - robin
arxiv: "2506.07643"
created: 2026-06-10
source: https://www.arxiv.org/pdf/2506.07643
confidence: full-paper
authors:
  - Jae Sung Park
  - Zixian Ma
  - Linjie Li
  - et al.
venue: arXiv Jun 2025
code: https://synthetic-visual-genome.github.io/
---

## Paper Info

SVG 大规模合成场景图数据集（146K 图像/5.6M 关系/2.6M 对象），附带 ROBIN-3B 模型。

## Method

两阶段数据管线：GPT-4V 补全关系 → SG-EDIT 自蒸馏（ROBIN→GPT-4o→ROBIN）
ROBIN-3B：ConvNeXt-Large + Qwen2.5-3B，mask+坐标双表示，8192 context

## Key Results

| 基准 | ROBIN-3B | 说明 |
|------|:---:|------|
| VSR | 76.4 | +4.8 vs Qwen2.5-VL-3B |
| SugarCrepe | 90.1 | SOTA |
| What's Up | 86.2 | 超 Phi-3-Vision (78.7) |
| Referring Exp. | 88.8 avg | 超 ASM-V2-13B (87.3) |
| PSG R@20 | 21.0 | 开放生成最优 |

## Provenance

- **Source**: arXiv 2506.07643
- **Evidence level**: full-paper
