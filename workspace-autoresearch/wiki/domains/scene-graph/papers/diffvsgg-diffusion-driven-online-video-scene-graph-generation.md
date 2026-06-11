---
title: "DIFFVSGG: Diffusion-Driven Online Video Scene Graph Generation"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - video-scene-graph-generation
  - diffusion-model
  - online-vsgg
  - latent-diffusion-model
  - temporal-reasoning
  - arxiv-2025
  - action-genome
  - imagenet-vidvrd
raw_sources:
  - ../../../raw/sources/2025-arXiv-DIFFVSGG-Diffusion-Driven-Online-Video-Scene-Graph-Generation.pdf
  - ../../../raw/sources/2025-arXiv-DIFFVSGG-Diffusion-Driven-Online-Video-Scene-Graph-Generation.txt
related_pages:
  - hyperglm-hypergraph-for-video-scene-graph-generation-and-anticipation.md
  - oed-one-stage-end-to-end-dynamic-scene-graph-generation.md
  - motion-aware-contrastive-learning-temporal-panoptic-sgg.md
  - fdsg-forecasting-dynamic-scene-graphs.md
  - salient-temporal-encoding-dynamic-sgg.md
evidence_level: full-paper
paper:
  title: "DIFFVSGG: Diffusion-Driven Online Video Scene Graph Generation"
  abbreviated: "DIFFVSGG"
  authors:
    - Mu Chen
    - Liulei Li
    - Wenguan Wang
    - Yi Yang
  affiliations:
    - ReLER, CCAI, Zhejiang University
    - ReLER, AAII, University of Technology Sydney
  year: 2025
  venue: arXiv preprint (arXiv:2503.13957)
  doi: null
  arxiv: "2503.13957"
  code: "https://github.com/kagawa588/DiffVsgg"
  url: null
classification:
  label: "Diffusion-Driven Online Video Scene Graph Generation"
  task:
    - Video Scene Graph Generation (VSGG)
  method_family: Latent Diffusion Model (LDM)
  modality: Video
  datasets:
    - Action Genome
    - ImageNet-VidVRD
  metrics:
    - Recall@K (R@K)
    - mean Recall@K (mR@K)
    - mAP
    - Precision@K (P@K)
---

# DIFFVSGG: Diffusion-Driven Online Video Scene Graph Generation

## Citation

Mu Chen, Liulei Li, Wenguan Wang, Yi Yang. "DIFFVSGG: Diffusion-Driven Online Video Scene Graph Generation." arXiv:2503.13957, 2025.

## One-Sentence Contribution

首次将潜在扩散模型（LDM）引入在线视频场景图生成（VSGG），通过将物体分类、bbox回归、关系生成统一为共享特征嵌入上的去噪过程，并利用前帧预测作为条件引导当前帧的反向扩散，实现逐步迭代的在线场景图更新与时序推理。

## Method Overview

### 核心思想

将 VSGG 任务建模为**迭代场景图更新问题**。借鉴 LDM 的图像生成思路：

1. **统一特征嵌入**：将物体分类、bbox 回归、关系预测三个子任务的解码统一到一个共享的噪声嵌入中（每个物体对→一个嵌入向量）
2. **去噪过程**：在 LDM 内对这个嵌入进行 step-wise denoising，逐渐得到清晰指示物体对关系的 clean embedding
3. **任务特定头**：clean embedding 作为输入，分别送入物体分类头、场景图生成头等

### 在线时序推理

- 逐帧在线处理（不依赖完整视频）
- 前帧去噪结果作为**条件输入**，引导当前帧的 reverse diffusion
- 支持实时视频流处理，避免 GPU 内存瓶颈

### 架构设计

- **Stage 1**：预训练 LDM，使用 GT bbox 标注，100 epochs，lr=1e-4，batch=2048
- **Stage 2**：训练 classifier/projector heads，10 epochs，batch=8，lr=1e-5 (AdamW)
- 每个输入 clip 由 5 帧组成（随机时间间隔采样）
- 推理时 50 步 reverse diffusion，图像最长边 resize 到 720px

### vs Offline SGG 对比

| 方面 | 传统 Offline VSGG | DIFFVSGG (Online) |
|------|-------------------|-------------------|
| 输入 | 完整视频 | 逐帧 |
| 时序处理 | 帧级预测后全局聚合 | 条件去噪逐步推理 |
| GPU 内存 | 随视频长度增大 | 固定 |
| 实时性 | 不支持 | 支持 |
| 场景图更新 | 独立生成→后聚合 | 渐进式迭代更新 |

## Key Results

### Action Genome — With Constraint (ResNet-101 + Faster-RCNN)

| 方法 | PredCLS R@20 | PredCLS mR@20 | SGCLS R@20 | SGCLS mR@20 | SGDET R@20 | SGDET mR@20 |
|------|:-----------:|:------------:|:---------:|:-----------:|:---------:|:-----------:|
| STTran [15] | 71.8 | 40.1 | 47.5 | 28.0 | 34.1 | 20.8 |
| TEMPURA [68] | 71.5 | 46.3 | 48.3 | 35.2 | 33.4 | 22.6 |
| TR2 [96] | 73.8 | — | 48.7 | — | 35.5 | — |
| **DIFFVSGG (Ours)** | **74.5** | **50.2** | **53.7** | **38.4** | **39.9** | **23.6** |

### Action Genome — Without Constraint (ResNet-101 + Faster-RCNN)

| 方法 | PredCLS R@20 | PredCLS mR@20 | SGCLS R@20 | SGCLS mR@20 | SGDET R@20 | SGDET mR@20 |
|------|:-----------:|:------------:|:---------:|:-----------:|:---------:|:-----------:|
| STTran [15] | 94.2 | 67.7 | 63.7 | 50.1 | 36.2 | 29.7 |
| TEMPURA [68] | 94.2 | 85.1 | 64.7 | 61.1 | 38.1 | 33.9 |
| TR2 [96] | 96.6 | — | 64.4 | — | 39.2 | — |
| **DIFFVSGG (Ours)** | **94.5** | **90.5** | **70.5** | **64.2** | **42.5** | **37.0** |

### Action Genome — Without Constraint (ResNet-50 + DETR)

| 方法 | PredCLS R@20 | PredCLS mR@20 | SGCLS R@20 | SGCLS mR@20 | SGDET R@20 | SGDET mR@20 |
|------|:-----------:|:------------:|:---------:|:-----------:|:---------:|:-----------:|
| TPT [118] | 97.4 | — | — | — | 39.6 | — |
| OED [94] | 95.3 | — | — | — | 44.0 | — |
| **DIFFVSGG (Ours)** | **95.9** | **91.6** | **71.8** | **65.1** | **45.1** | **37.9** |

### ImageNet-VidVRD

| 方法 | RelDet mAP | RelDet R@50 | RelDet R@100 | RelTag P@1 | RelTag P@5 | RelTag P@10 |
|------|:---------:|:----------:|:-----------:|:---------:|:---------:|:----------:|
| VidVRD [78] | 8.58 | 5.54 | 6.37 | 43.00 | 28.90 | 20.80 |
| GCN [73] | 14.27 | 7.43 | 8.75 | 59.50 | 40.50 | 27.58 |
| STGC [59] | 18.38 | 11.21 | 13.69 | 60.00 | 43.10 | 32.24 |
| BIG [29] | 26.08 | 14.10 | 16.25 | 73.00 | 55.10 | 40.00 |
| HCM [101] | 29.68 | 17.97 | 21.45 | 78.50 | 57.40 | 43.55 |
| **DIFFVSGG (Ours)** | **30.15** | **18.10** | **21.51** | **79.95** | **58.80** | **43.71** |

## Analysis

### 优势

1. **在线能力**：首个将 LDM 用于在线 VSGG 的方法，支持实时逐帧处理
2. **统一框架**：三个子任务（物体分类、bbox 回归、关系生成）共享一个去噪嵌入，避免多阶段级联误差
3. **时序推理**：前帧→后帧的条件扩散，比传统帧级聚合后的 Transformer 后处理更自然的时序建模
4. **泛化性强**：同时验证于 Action Genome 和 ImageNet-VidVRD，覆盖人-物交互和通用关系

### 局限（来自论文自身讨论）

1. **多步推理效率**：50 步 reverse diffusion 推理耗时，论文建议引入 step-reduction 技术（如 [44, 102]）加速
2. **数据偏置**：Action Genome 的长尾分布导致 tail class 误分类（如 "writing" 误判为 "touching"）
3. **生成风险**：扩散模型的生成性质存在产生虚假内容的风险

### 与相关方法对比

- 与 **OED [94]** 相比（同样使用 ResNet-50+DETR）：在 PredCLS with constraint 下 R@10 提升 +1.8%，R@20 +1.4%，R@50 +1.4%
- 与 **TEMPURA [68]** 相比：在 with constraint 下 SGCLS mR@20 **38.4** vs 35.2（+3.2）
- 与 **DSG-DETR [27]** 相比：在 with constraint 下 SGCLS R@20 **53.7** vs 52.0（+1.7）
- 在 VidVRD 上与 **HCM [101]** 相比：RelDet mAP **30.15** vs 29.68（+0.47），RelTag P@1 **79.95** vs 78.50（+1.45）

## Datasets

### Action Genome (AG)
- 最大 VSGG 基准数据集
- 10K+ 视频，源自 Charades
- 25 个谓词类（分 attention/spatial/contact 三类）
- 1,715,568 条谓词实例，234,253 帧
- 35 物体类别，476,229 个 bbox

### ImageNet-VidVRD
- 35 个物体类别，132 个关系类别
- 非 human-centric，覆盖更广泛关系类型
- 每帧平均 9.7 个关系，2.5 个物体
- 评估：RelTag（精确率 P@K）和 RelDet（召回率 R@K + mAP）

## References

- Chen et al. "DIFFVSGG: Diffusion-Driven Online Video Scene Graph Generation." arXiv:2503.13957, 2025. [arXiv](https://arxiv.org/abs/2503.13957) | [Code](https://github.com/kagawa588/DiffVsgg)
