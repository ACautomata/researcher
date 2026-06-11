---
title: "PC-SGG: Conformal Prediction and MLLM Aided Uncertainty Quantification in Scene Graph Generation"
tags:
  - scene-graph-generation
  - conformal-prediction
  - uncertainty
  - mllm
created: 2026-06-10
source: https://arxiv.org/pdf/2503.13947
confidence: full-paper
authors:
  - Sayak Nag
  - Udita Ghosh
  - Calvin-Khang Ta
  - Sarosij Bose
  - Jiachen Li
  - Amit K. Roy-Chowdhury
venue: arXiv Mar 2025
---

## Paper Info

- **Title**: Conformal Prediction and MLLM aided Uncertainty Quantification in Scene Graph Generation
- **Venue**: arXiv Mar 2025 (UC Riverside, Dolby)
- **Dataset**: VG150
- **Methods tested**: MOTIFS, MOTIFS-D, VCTREE, SQUAT, BGNN

## Abstract

首个将 Conformal Prediction 用于 SGG 不确定性量化的框架。类条件覆盖保证 + MLLM 后处理压缩预测集 >50%。cR@50 vs R@50 平均 +15.70pp, cmR@50 vs mR@50 +21.57pp。尾部类提升最显著。

## Method

### Conformal Prediction for SGG

对 object 和 predicate 分别计算类条件保形分位数，组合为 triplet 预测集。
理论覆盖保证：≥ (1-α_o)(1-α_r)，实验取 α_o=0.05, α_r=0.1。

### MLLM 后处理

BLIP-2 + FLAN-T5-XL, 1-shot MCQ prompt。token 似然阈值 τ=0.1 选择最可信条目。

## Experiments

| 方法+PC-SGG | cR@50 | cmR@50 |
|-------------|:---:|:---:|
| MOTIFS | 38.45 | 25.49 |
| VCTREE | 41.89 | 27.84 |
| SQUAT | 43.23 | 30.94 |
| BGNN | **46.32** | **32.52** |

### MLLM 效果

| 方法 | AvgSize (无MLLM) | AvgSize (有MLLM) |
|------|:---:|:---:|
| VCTREE | 818.76 → **389.24** |
| BGNN | 971.69 → **464.11** |

## Results

- cpSGG 使 recall-hit rate 大幅提升
- MLLM 压缩预测集 >50% 几乎不损失覆盖
- 尾部类提升最显著

## Limitations

1. 理论覆盖保证未能达成（SGG 高不确定性）
2. 仅 VG150 评估
3. 8-bit BLIP-2 可能上限有限

## Provenance

- **Source**: arXiv 2503.13947
- **Evidence level**: full-paper
