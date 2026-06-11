---
title: "CooK: Scene Graph Generation with Co-occurrence Knowledge and Learnable TF-l-IDF"
tags:
  - scene-graph-generation
  - co-occurrence
  - graph-laplacian
  - long-tail
  - ICML-2024
created: 2026-06-10
source: https://arxiv.org/pdf/2405.12648
confidence: full-paper
authors:
  - Hyeongjin Kim
  - Sangwon Kim
  - Dasom Ahn
  - Jong Taek Lee
  - Byoung Chul Ko
venue: ICML 2024
---

## Paper Info

- **Title**: Scene Graph Generation Strategy with Co-occurrence Knowledge and Learnable Graph Laplacian
- **Venue**: ICML 2024
- **Code**: None
- **Base**: MPNN (plugin for any MPNN-based SGG)

## Abstract

CooK 矩阵注入物体共现先验 + 可学习 TF-l-IDF 层缓解长尾。PredCls mR@100=37.2 (SOTA)，OI score_wtd=45.1 (SOTA)。插件可集成到 G-RCNN/GPS-Net/BGNN，平均 mR@100 +22.6%。

## Method

**CooK**: 条件概率 P(c_j|c_i) 作为 MPNN 消息传递权重
**TF-l-IDF**: 可学习 ε, γ 参数的特征平衡层

## Experiments

### VG

| 指标 | CooK | 对比最佳 |
|------|:---:|:---:|
| PredCls mR@50/100 | **35.4/37.2** | VETO+Rwt 33.1/35.1 |
| OI score_wtd | **45.1** | PE-Net 44.9 |

### 通用性

| 模型 | mR@50 (+ours) |
|------|:---:|
| G-RCNN | 5.8→**7.1** |
| GPS-Net | 6.7→**8.3** |
| BGNN | 10.7→**11.4** |

## Results

- Head 类下降 / Body/Tail 类显著提升
- 泛用于任意 MPNN-based SGG

## Limitations

1. 仅 MPNN-based 模型
2. 仅监督学习
3. 未在 Transformer-based 验证

## Provenance

- **Source**: arXiv 2405.12648
- **Evidence level**: full-paper
