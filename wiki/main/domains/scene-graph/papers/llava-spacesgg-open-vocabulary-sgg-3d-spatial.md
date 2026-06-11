---
title: "LLaVA-SpaceSGG: Visual Instruct Tuning for Open-vocabulary Scene Graph Generation with Graph Space Disentanglement"
tags:
  - scene-graph-generation
  - open-vocabulary
  - llava
  - spatial-relations
  - mllm
  - 3d
created: 2026-06-10
source: https://arxiv.org/pdf/2412.06322
confidence: full-paper
code: https://github.com/Endlinc/LLaVA-SpaceSGG
authors:
  - Mingjie Xu
  - Mengyang Wu
  - Yuzhi Zhao
  - Jason Chun Lok Li
  - Weifeng Ou
venue: arXiv Dec 2024
---

## Paper Info

- **Title**: LLaVA-SpaceSGG: Visual Instruct Tuning for Open-vocabulary Scene Graph Generation with Enhanced Spatial Relations
- **Venue**: arXiv Dec 2024
- **Code**: https://github.com/Endlinc/LLaVA-SpaceSGG
- **Dataset**: SpaceSGG (40K instructions from 20K scenes), PSG

## Abstract

基于 MLLM 的开放词汇 SGG，引入 3D 空间关系（深度→点云→分层）。构建 SpaceSGG 指令微调数据集（三类 40K），两阶段训练，在 PSG 开放词汇设定下 Recall 15.43 (+8.6%)，mRecall 13.23 (+28.4%)。

## Method

### 3D 信息提取

Depth-Anything → 深度图 → 点云 → 分层算法（Z 轴深度范围覆盖 → 逐层分配）

### SpaceSGG 数据集 (40K)

| 数据类型 | 数量 | 用途 |
|---------|------|------|
| SpaceSGG-Desc | 10K | 结构化场景描述 |
| SpaceSGG-QA | 10K | 空间关系问答 |
| SpaceSGG-Conv | 20K | CoT 多轮对话 |

### 两阶段训练

Stage 1: 图像级对齐 (CC3M+LLaVA-Instruct)
Stage 2: 区域级微调 (CC12M+AS-1B+GRiT → AS-V2+SpaceSGG)

## Experiments

### PSG 开放词汇

| 方法 | Recall | mRecall |
|------|:---:|:---:|
| ASMv2 | 14.2 | 10.3 |
| TextPSG | 4.8 | – |
| **LLaVA-SpaceSGG** | **15.43** | **13.23** |

### 空间关系验证

| 方法 | 准确率 |
|------|:---:|
| LLaVA-1.5-13B | 45.13% |
| ASMv2-13B | 50.52% |
| **LLaVA-SpaceSGG** | **52.48%** |

### 消融

完整数据 (Desc+QA+Conv) 最佳: Recall 15.43, mRecall 13.23
Desc 提升 Recall, QA 提升空间准确率, Conv 平衡。

## Results

- Recall +8.6%, mRecall +28.4% vs ASMv2
- 空间准确率 52.48%
- 三类数据互补

## Limitations

1. 依赖 Depth-Anything（误差传递）
2. 生成数据存在噪声

## Connections

- **ASMv2** — MLLM-based SGG 基线
- **TextPSG** — 文本描述 PSG 方法
- **Depth-Anything** — 深度估计第三方依赖

## Provenance

- **Source**: arXiv 2412.06322
- **Evidence level**: full-paper
