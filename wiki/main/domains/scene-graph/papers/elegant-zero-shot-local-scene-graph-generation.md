---
title: "ELEGANT: Less is More — Zero-Shot Local Scene Graph Generation via Foundation Models"
tags:
  - scene-graph-generation
  - zero-shot
  - foundation-model
  - local-scene-graph
created: 2026-06-10
source: https://arxiv.org/pdf/2310.01356
confidence: full-paper
authors:
  - Shu Zhao
  - Huijuan Xu
venue: arXiv Oct 2023
---

## Paper Info

- **Title**: Less is More: Toward Zero-Shot Local Scene Graph Generation via Foundation Models
- **Venue**: arXiv Oct 2023
- **Method**: ELEGANT
- **Metric**: ECLIPSE (entity-level CLIPScore)

## Abstract

零样本局部场景图生成，只提取与给定 subject 相关的实体和关系。三基础模型协作：GroundedSAM（感知）+ GPT-3.5（推理）+ BLIP2（验证）。ECLIPSE=21.54 (VG), 21.32 (GQA)。

## Method

### Three-stage

1. **Perception** (GroundedSAM) — 检测开放词汇对象
2. **Reasoning** (GPT-3.5) — 推理候选关系三元组
3. **Verification** (BLIP2) — VQA 验证

### CoCa 策略

LLM 校准被 VLM 错误拒绝的三元组。恢复 **5012** 个三元组。

### ECLIPSE 指标

CLIPScore + 惩罚函数，用于开放词汇场景图评估。

## Experiments

### Best ECLIPSE

| 配置 | ECLIPSE |
|------|:---:|
| GroundedSAM + GPT-3.5 + BLIP2 OPT 6.7B | **21.54** (VG) |
| GroundedSAM + GPT-3.5 + BLIP2 FlanT5 XXL | **21.32** (GQA) |

### 封闭词汇对比 (20 rel)

| 方法 | R@50 | mR@50 |
|------|:---:|:---:|
| VisualDS | 38.21 | 24.94 |
| **ELEGANT** | **41.04** | **29.78** |

### VQA 下游

| 场景图 | ACC |
|--------|:---:|
| 无场景图 | 50.4 |
| 全局场景图 | 54.2 |
| **局部场景图** | **58.3** (+7.9%) |

## Results

- 开放词汇实体类别 ~4x, 关系类别 ~25x, 三元组 ~7x 多于封闭方法
- CoCa 恢复 42% 被误拒三元组
- 局部场景图在 VQA 始终优于全局

## Limitations

1. GPT-3.5 非开源，复现性受限
2. Verifier 仅探索 BLIP2
3. Subject 选择未自动化

## Provenance

- **Source**: arXiv 2310.01356
- **Evidence level**: full-paper
