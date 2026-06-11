---
title: "Relation-R1: Cognitive Chain-of-Thought Guided Reinforcement Learning for Panoptic SGG"
tags:
  - scene-graph-generation
  - panoptic-scene-graph
  - reinforcement-learning
  - chain-of-thought
  - AAAI-2026
created: 2026-06-10
source: https://arxiv.org/pdf/2504.14642
confidence: full-paper
code: https://github.com/HKUST-LongGroup/Relation-R1
authors:
  - Lin Li
  - Wei Chen
  - Jiahui Li
  - Kwang-Ting Cheng
  - Long Chen
venue: AAAI 2026
---

## Paper Info

- **Title**: Relation-R1: Progressively Cognitive CoT Guided Reinforcement Learning for Unified Relation Comprehension
- **Venue**: AAAI 2026
- **Base model**: Qwen2.5-VL-3B
- **Training**: SFT (template CoT + MLLM-CoT) → GRPO RL

## Abstract

首个 CoT + RL (GRPO) 统一视觉关系理解框架。PSG Recall 22.33, SWiG Grnd-all 30.18 (+14.48%)。3B 模型超越 13B。渐进 CoT 策略 + 联合训练协同效应。

## Method

**SFT**: 模板基 CoT (2 epoch) + 4k MLLM-CoT (Qwen2.5-VL-72B 生成)
**RL**: GRPO (格式 + 二元 + N 元三类奖励)

## Experiments

### PSG

| 方法 | Recall | mRecall |
|------|:---:|:---:|
| Relation-R1 (3B) | **22.33** | **20.07** |
| LLaVA-SpaceSGG (13B) | 15.43 | 13.23 |

### SWiG

| 方法 | Verb | Grnd-all |
|------|:---:|:---:|
| Relation-R1 | **57.26** | **30.18** |
| OpenSU | 50.10 | 15.70 |

### CoT 消融

渐进 CoT 最佳: Binary Recall 22.57, N-ary Verb 71.04
联合训练: Binary Recall 27.19, N-ary Verb 73.25

### Few-shot

1-shot Verb 31.67% (vs CoFormer 0.63%)

## Results

- SFT 记忆 + RL 泛化互补
- 渐进 CoT 优于纯模板或纯 MLLM-CoT
- 联合训练产生协同效应

## Limitations

1. 3B 模型较小，更大模型可能有更好表现
2. MLLM 生成 CoT 依赖 72B，计算开销大

## Provenance

- **Source**: arXiv 2504.14642
- **Evidence level**: full-paper
