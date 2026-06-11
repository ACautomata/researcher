---
title: "Hallucinate, Ground, Repeat: EM-Grounding for Generalized Visual Relationship Detection"
tags:
  - scene-graph-generation
  - llm
  - hallucination
  - weakly-supervised
  - expectation-maximization
created: 2026-06-10
source: https://arxiv.org/pdf/2506.05651
confidence: full-paper
authors:
  - Shanmukha Vellamcheti
  - Sanjoy Kundu
  - Sathyanarayanan N. Aakur
venue: arXiv Jun 2025
---

## Paper Info

- **Title**: Hallucinate, Ground, Repeat: A Framework for Generalized Visual Relationship Detection
- **Venue**: arXiv Jun 2025 (Auburn University)
- **Code**: None
- **Base SGG architecture**: IS-GGT (decoder-only transformer)

## Abstract

EM-Grounding：将 LLM 作为符号先验，通过 EM 迭代将 LLM "幻觉"候选场景图与视觉证据对齐。无需 GT 三元组，475 张训练图像即可工作。PredCls Seen mR@50=15.9, Unseen=13.1, Mixed=11.3。

## Method

**E-Step**: GPT-4o 为每个物体对生成最多 5 个候选谓词，构成多重关系超图
**M-Step**: IS-GGT 解码器通过交叉熵损失对齐幻觉三元组与视觉特征
**迭代精炼**: 3 轮内收敛，置信度 τ=0.8

## Experiments

### PredCls (5,777 VG test)

| 方法 | Seen mR@50 | Unseen mR@50 | Mixed mR@50 |
|------|:---:|:---:|:---:|
| IS-GGT (全监督) | 13.0 | 0.0 | 5.2 |
| GPT-4o (无视觉对齐) | 12.4 | 8.2 | 5.6 |
| **EM-Grounding (无GT)** | **15.9** | **13.1** | **11.3** |

### VG 官方测试集 (100× 监督差距)

475 张训练 → mR@50=11.8, mR@100=17.2 (超过 IMP+ 9.8 和 Motifs 14.0)

## Results

- 符号先验 + 视觉对齐解耦推理与定位
- 迭代精炼有效滤除 LLM 幻觉噪声
- 零标签可达全监督性能

## Limitations

1. 依赖前置物体检测（错误传递）
2. 符号先验仅用物体标签（无视觉/空间上下文）
3. 仍限于预定义谓词空间

## Provenance

- **Source**: arXiv 2506.05651
- **Evidence level**: full-paper
