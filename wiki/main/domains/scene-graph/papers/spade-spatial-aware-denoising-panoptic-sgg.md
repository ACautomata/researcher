---
title: "SPADE: Spatial-Aware Denoising for Open-vocabulary Panoptic SGG"
tags:
  - scene-graph-generation
  - panoptic-scene-graph
  - open-vocabulary
  - diffusion-model
arxiv: "2507.05798"
created: 2026-06-10
source: https://arxiv.org/pdf/2507.05798
confidence: full-paper
authors:
  - Xin Hu
  - Ke Qin
  - Guiduo Duan
  - et al.
venue: arXiv Jul 2025
---

## Paper Info

SPADE — DDIM inversion 校准 + RGT 空间感知关系图 Transformer 的开放词汇全景 SGG。

## Method

**Stage 1**: DDIM inversion cross-attention → LoRA 微调扩散 UNet 适配 PSG
**Stage 2**: RGT (邻居+非邻居长程 + GCN 局部 + 关系查询构建)

## Key Results

### PSG

| 方法 | 闭集 R/mR@50 | 开集 R/mR@50 |
|------|:---:|:---:|
| OpenPSG | 42.8/38.9 | 21.2/19.8 |
| **SPADE** | **45.1/41.2** | **26.7/23.3** |

### VG

| 方法 | 闭集 R/mR@50 | 开集 R/mR@50 |
|------|:---:|:---:|
| OpenPSG | 32.7/13.5 | 20.4/9.4 |
| **SPADE** | **37.2/17.3** | **24.1/11.2** |

空间关系: NDR R@50 46.5, DR R@50 42.3 (差距仅 4.2% vs OpenPSG 6.6%)

## Provenance

- **Source**: arXiv 2507.05798
- **Evidence level**: full-paper
