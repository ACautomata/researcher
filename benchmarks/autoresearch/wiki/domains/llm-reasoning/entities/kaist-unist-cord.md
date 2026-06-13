---
title: KAIST & UNIST — CoRD 团队
type: entity
domain: llm-reasoning
status: active
created: 2026-05-24
updated: 2026-05-24
tags:
  - research-group
  - llm-reasoning
  - knowledge-distillation
source_pages:
  - wiki/domains/llm-reasoning/papers/distilling-long-cot-reasoning-cord.md
related_pages:
  - wiki/domains/llm-reasoning/methods/cord.md
  - wiki/domains/llm-reasoning/concepts/long-cot-reasoning-distillation.md
---

# KAIST & UNIST — CoRD 团队

## 描述

韩国科学技术院（KAIST）与蔚山科学技术院（UNIST）的联合研究团队，由 DISL Lab (Data Intelligence & Systems Lab) 主导。在 wiki 中因 CoRD（Collaborative Reasoning Decoding）论文出现。

## 当前理解

- **团队组成**：Taewon Yun, Jisu Shin, Jeonghwan Choi, Seunghwan Bang, Hwanjun Song（通讯作者）。
- **所属机构**：KAIST (Korea Advanced Institute of Science and Technology) & UNIST (Ulsan National Institute of Science and Technology)。
- **Lab**：DISL Lab (Data Intelligence & Systems Lab)，代码托管在 github.com/DISL-Lab。
- **研究兴趣**：Long-CoT 推理蒸馏、多 teacher 知识蒸馏、逐步解码、推理质量评估。

## 证据

- CoRD (arXiv:2605.02290, 2026)：提出逐步协同解码范式，在 AIME24/25 上学生模型超越所有单个 teacher。
- 代码仓库：github.com/DISL-Lab/CoRD。
- 实验资源：8×NVIDIA H100 GPU + 4×NVIDIA H200 GPU（用于 meta-prover 推理）。
- 教师池：R1-Distill-Qwen-32B、QwQ-32B、Phi4-Reasoning-Plus。
- 学生模型：R1-Qwen-7B/14B/32B、R1-Llama-8B（跨架构验证）。

## 关联

- [CoRD](../methods/cord.md)：该团队在 wiki 中的核心方法贡献。
- [Long-CoT Reasoning Distillation](../concepts/long-cot-reasoning-distillation.md)：所属研究领域。
- 该团队的工作与 distillation 域的 Continual Distillation（CD）形成对比——CoRD 是并行多 teacher 协同，CD 是序列 teacher 蒸馏。

## 开放问题

- 团队在 code generation、theorem proving 等相邻长链推理任务上的后续工作？
- 与 DeepSeek、Qwen 等 teacher 模型开发团队的协作关系？
