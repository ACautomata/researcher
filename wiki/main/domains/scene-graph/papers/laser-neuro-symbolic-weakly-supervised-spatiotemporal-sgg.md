---
title: "LASER: Neuro-Symbolic Framework for Weakly-Supervised Spatio-Temporal Scene Graph Learning"
tags:
  - scene-graph-generation
  - neuro-symbolic
  - spatio-temporal
  - video
  - weak-supervision
  - ICLR-2025
created: 2026-06-10
source: https://arxiv.org/pdf/2304.07647
confidence: full-paper
authors:
  - Jiani Huang
  - Ziyang Li
  - Mayur Naik
  - Ser-Nam Lim
venue: ICLR 2025
---

## Paper Info

- **Title**: LASER: A Neuro-Symbolic Framework for Learning Spatial-Temporal Scene Graphs with Weak Supervision
- **Venue**: ICLR 2025
- **Method**: Video captions → STSL logical specs → neuro-symbolic alignment

## Abstract

弱监督 STSG 学习。LLM 将视频字幕转为 STSL 逻辑规范，Scallop 可微对齐检查器计算对齐概率。OpenPVSG Binary R@5 0.42 (超全监督 0.20)。10% 数据即达 70.75% 全量性能。

## Method

**STSL**: 基于 LTLf 的时空规范语言 (□, ♢, U, ⃝ 算子)
**3-shot GPT-4**: 字幕→STSL 程序 (失败率 <1%)
**Scallop**: 可微分概率推理引擎
**Loss**: 对比 + 时间跨度 + 语义

## Experiments

### OpenPVSG

| 方法 | Unary R@1 | Binary R@5 |
|------|:---:|:---:|
| IPS-Trans (全监督) | 14.67 | 0.20 |
| **LASER-CLIP (弱监督)** | **27.78** | **0.42** |

### 20BN

| 方法 | F1 |
|------|:---:|
| LASER-P (GT规范) | **0.77** |
| LASER (字幕) | **0.73** |
| GPA (弱监督) | 0.74 |

### 零样本迁移

LLaVA-Video → OpenPVSG: Unary R@1 0.2368

## Results

- 字幕驱动 STSG 弱监督超越全监督
- 10% 数据即达 70.75% 性能
- STSL 表达力强于传统动作序列

## Limitations

1. 可扩展性受限于视频长度
2. 字幕质量依赖
3. 长视频仍是开放问题

## Provenance

- **Source**: arXiv 2304.07647
- **Evidence level**: full-paper
