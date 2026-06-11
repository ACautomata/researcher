---
title: "ASMP: Learning Audio-Visual Dynamics Using Scene Graphs for Audio Source Separation"
tags:
  - scene-graph-generation
  - audio-visual
  - source-separation
  - audio-scene-graph
  - NeurIPS-2022
created: 2026-06-10
source: https://arxiv.org/pdf/2210.16472
confidence: full-paper
code: https://sites.google.com/site/metrosmiles/research/research-projects/asmp
authors:
  - Moitreya Chatterjee
  - Narendra Ahuja
  - Anoop Cherian
venue: NeurIPS 2022
---

## Paper Info

- **Title**: Learning Audio-Visual Dynamics Using Scene Graphs for Audio Source Separation
- **Venue**: NeurIPS 2022
- **Method**: 2.5D scene graph + GAT + GRU subgraph segmentation → U-Net separation

## Abstract

ASMP 框架：2.5D 场景图（MiDAS 伪深度 + Chamfer 距离 RBF 权重）引导音源分离。GAT+EdgeConv+GRU 递归分割声源子图。新任务：音频预测声源 3D 运动方向。

## Method

**2.5D SG**: MiDAS → ICP → FRCNN → RAFT → Chamfer RBF 边权重
**Segmentation**: GAT → EdgeConv → GRU 递归分割
**Separation**: U-Net 条件化子图嵌入
**Direction**: ResNet-18 从分离音频预测 8/26 方向

## Experiments

### Audio Separation

| 方法 | ASIW SDR | AVE SDR |
|------|:---:|:---:|
| AVSGS (前SOTA) | 8.8 | 5.8 |
| **ASMP (全模型)** | **9.6** | **7.2** |

### Direction Prediction

ASIW 10 类: 42.5% (+3.3% vs AVSGS)

### Human Preference

63% (ASIW) / 68% (AVE) 偏好 ASMP

### 消融

方向预测贡献 SDR +0.6dB
3D 空间距离贡献 SDR +0.2~0.5dB

## Results

- 2.5D 场景图 > 2D 等权重
- 方向预测双向收益：分离精度提升 + 自身任务可解
- 单帧隐含运动先验

## Limitations

1. 背景声音分离不理想
2. 依赖预训练检测器（稀有类别困难）
3. 方向预测为粗粒度分类

## Provenance

- **Source**: arXiv 2210.16472
- **Evidence level**: full-paper
