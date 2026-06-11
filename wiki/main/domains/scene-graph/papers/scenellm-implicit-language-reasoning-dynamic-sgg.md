---
title: "SceneLLM: Implicit Language Reasoning in LLM for Dynamic Scene Graph Generation"
tags:
  - scene-graph-generation
  - llm
  - dynamic
  - hidden-state-reasoning
  - video
created: 2026-06-10
source: https://arxiv.org/pdf/2412.11026
confidence: full-paper
authors:
  - Hang Zhang
  - Zhuoling Li
  - Jun Liu
venue: arXiv May 2025 (v2)
---

## Paper Info

- **Title**: SceneLLM: Implicit Language Reasoning in LLM for Dynamic Scene Graph Generation
- **Venue**: arXiv May 2025 (SUTD, Lancaster)
- **Dataset**: Action Genome (AG)
- **Backbone**: LLaMA-13B + LoRA

## Abstract

首个将 LLM 作为隐式语言推理分析器的动态 SGG 框架。V2L Mapping（VQ-VAE + SIA + OT）将视频转换为"场景句子"，LLaMA-13B 隐式推理 + SGG Predictor 解码。PREDCLS With Constraint R@10=74.1 (SOTA)。

## Method

### V2L Mapping

1. VQ-VAE 离散量化（码本 m=512, 维度 l=512）
2. SIA 空间聚合（汉字启发，HC+GCN 生成帧级 token）
3. OT 最优传输时间一致性

### LLM 隐式推理

LLaMA-13B + LoRA, 输入是隐式嵌入（非文本），取最后 block 隐藏特征作为推理结果。

### Two-stage Training

1. VQ-VAE 预训练 (300k iter)
2a. 冻结 VQ-VAE + LLM, 优化 MLP/GCN/SGG predictor (30k)
2b. 加入 LoRA 联合微调 (50k)

## Experiments

### With Constraint

| 任务 | R@10 | R@20 |
|------|:---:|:---:|
| PREDCLS | **74.1** | **77.8** |
| SGCLS | **53.7** | **55.0** |
| SGDET | **34.9** | **43.3** |

### 消融

- w/o LLM: R@10 从 53.7→38.9
- w/o discretization: 53.7→40.4
- w/o OT: 53.7→50.9
- LoRA 优于全参数微调 (53.7 vs 47.3)

## Results

- 隐式推理范式创新，不同于直接文本生成
- 空间编码受汉字偏旁结构启发
- OT 时间一致性显著优于 conv/clustering

## Limitations

1. 仅在 AG 封闭数据集评估
2. 开放世界泛化未知

## Provenance

- **Source**: arXiv 2412.11026
- **Evidence level**: full-paper
