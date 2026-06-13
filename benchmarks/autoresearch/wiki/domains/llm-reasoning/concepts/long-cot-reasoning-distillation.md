---
title: Long-CoT 推理蒸馏
type: concept
domain: llm-reasoning
status: active
created: 2026-05-05
updated: 2026-05-05
tags:
  - reasoning-distillation
  - long-cot
  - knowledge-distillation
  - step-wise-decoding
source_pages:
  - wiki/domains/llm-reasoning/papers/distilling-long-cot-reasoning-cord.md
related_pages: []
---

## Definition

Long-CoT（长链思维）推理蒸馏是将大型推理模型（LRM，如 DeepSeek-R1、QwQ-32B、Phi4-Reasoning-Plus）通过 test-time scaling 产生的冗长、探索性推理轨迹，压缩为可用于监督微调（SFT）高质量训练数据的过程。目标是让学生模型（通常更小、推理更快）在推理能力上接近甚至超越 teacher LRM。

与经典知识蒸馏（只匹配输出概率分布）不同，Long-CoT 推理蒸馏需要保留推理过程的**结构**——包括问题分解、多路径探索、验证、纠错和综合等步骤。

## Current Understanding

目前主要有三种蒸馏范式：

1. **策展式（Curation）**：如 S1、LIMO——各 teacher 独立生成完整推理轨迹 → post-hoc 评分选择最佳轨迹。简单但 teacher 信号无交互，产生大量废弃轨迹。

2. **后融合式（Post-hoc Integration）**：如 Integration baseline——外部模型合并多 teacher 完整轨迹。面临长文本 lost-in-the-middle 问题，通常导致轨迹坍缩为 Short-CoT。

3. **逐步协同解码（Step-wise Collaborative Decoding）**：如 CoRD——在推理过程中逐步融合多 teacher 信号，通过每一步的候选评估和 beam search 构建最优轨迹。这是当前最先进的方法，在 AIME24/25 上实现 near-teacher 水平。

## Evidence

- CoRD 异构 teacher 配置在 AIME24 上 Pass@1 79.6%，超越所有单个 teacher（R1-Qwen-32B: 71.6%, QwQ-32B: 77.9%, Phi4: 78.9%）。来源：[CoRD](../papers/distilling-long-cot-reasoning-cord.md), Table 3。
- predictive perplexity 作为步骤级选择准则显著优于 PRM 和 Binary Judgment。来源：[CoRD](../papers/distilling-long-cot-reasoning-cord.md), Table 5。
- step-wise collaborative decoding 在域外任务（TaTQA: 95.2%）和开放域任务（PubMedQA: 91.8%）上均有效泛化。来源：[CoRD](../papers/distilling-long-cot-reasoning-cord.md), Table 7。

## Connections

- 经典知识蒸馏（Hinton et al., 2015）：输出层概率匹配；Long-CoT 蒸馏需要匹配推理轨迹结构
- S1 (Snell et al., 2024)、LIMO (Ye et al., 2025)：curation-based 推理蒸馏的奠基工作
- DeepSeek-R1 (Guo et al., 2025)：定义了 Long-CoT reasoning 的 RL 训练范式
- 与 `distillation` 域的区分：Long-CoT 蒸馏是**模型级知识蒸馏**（训练更好的学生模型），而数据集蒸馏是**数据级压缩**（合成更小的训练集）

## Open Questions

1. 如何超越 SFT-only 蒸馏，引入 RL/DPO 进一步对齐 teacher-student 推理风格？
2. 跨语言推理蒸馏的有效性？
3. 对代码生成、定理证明等相邻长链推理任务的泛化性？
4. 更高效 meta-prover（小型专用验证模型）的可行性和质量 trade-off？
5. multi-modal Long-CoT 推理（视觉+语言）的蒸馏策略？
