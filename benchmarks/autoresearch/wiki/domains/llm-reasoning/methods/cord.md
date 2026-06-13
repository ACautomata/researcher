---
title: CoRD — Collaborative Reasoning Decoding
type: method
domain: llm-reasoning
status: active
created: 2026-05-24
updated: 2026-05-24
tags:
  - reasoning-distillation
  - long-cot
  - multi-teacher
  - step-wise-decoding
  - beam-search
source_pages:
  - wiki/domains/llm-reasoning/papers/distilling-long-cot-reasoning-cord.md
related_pages:
  - wiki/domains/llm-reasoning/concepts/long-cot-reasoning-distillation.md
  - wiki/domains/federated-learning/methods/fedhd.md
---

# CoRD — 多 Teacher 协同逐步解码推理蒸馏

## 定义

CoRD 将 Long-CoT 推理蒸馏重新定义为逐步协同解码过程——多个异构 teacher LRM 在每步提出候选推理步骤，通过基于预测困惑度（predictive perplexity）的选择机制和 beam search，联合构建高质量推理轨迹。学生模型（R1-Qwen-32B）在 AIME24/25 上可接近甚至超越所有单个 teacher。

## 核心机制

1. **Prompt-guided Step Segmentation**：
   - 在初始 prompt 中嵌入 `\<think\> ### Step` 标记，引导 LRM 将推理自然分割为语义连贯的功能性步骤。
   - 对比 line-break（纯格式分割，无语义一致性）和 prefix-based（基于 "wait"/"alternatively" 等标记，跨模型不一致）。
   - 优势：跨模型高度一致的步骤粒度，同时保持 semantic parity 和 style consistency。
2. **Perplexity-based Step Selection**：
   - 引入 meta-prover（teacher 池中最强模型，如 QwQ-32B）作为独立评分模型。
   - 选择使预测困惑度最高的候选步骤：$s_t^* = \arg\max_k p_{meta}(A | \tau_{<t} \oplus s_t^{(k)})$，其中 A 是 ground-truth answer。
   - 对比 PRM（过滤了可能 self-correct 的轨迹）、Binary Judgment（离散标签，无法区分细微质量差异）。
   - 关键发现：MCTS 的 trajectory-level reward 偏向全局强 teacher，削弱 teacher 间的步骤级互补性。
3. **Step-wise Decoding with Beam Search**：
   - 维护 top-B 条部分推理轨迹（B=4），每步扩展 B×K 条候选。
   - Greedy: 81.6% answer accuracy；MCTS: 89.6%（且计算成本高 2×）；Beam Search: 93.1%。
   - 计算复杂度 $O(T \cdot K \cdot M \cdot B)$，wall-clock 288.7s/题（MCTS 589.2s，Curation 168.3s，H200×4）。

## 假设

- Teacher 间的互补推理信号在推理过程中实时交互优于 post-hoc curation/integration。
- Predictive perplexity 作为连续质量信号优于离散判断（Binary Judgment）和依赖单一轨迹的评估（PRM）。
- Beam search 在步骤级保留多条轨迹优于 MCTS 的全局 reward 聚合。
- Prompt-guided segmentation 能实现异构 teacher 间的步骤粒度对齐。

## 证据

- arXiv:2605.02290, Yun et al., KAIST & UNIST，full-paper，有代码 (github.com/DISL-Lab/CoRD)。
- 异构 teacher（R1-Distill-Qwen-32B + QwQ-32B + Phi4-Reasoning-Plus）：Answer Accuracy 93.1%，Predictive Perplexity 0.774。
- 学生蒸馏：R1-Qwen-32B 在 AIME24 上 Pass@1 79.6%，AIME25 上 70.2%——超越所有单个 teacher（R1-Qwen-32B: 71.6%/53.8%, QwQ-32B: 77.9%/66.7%, Phi4: 78.9%/67.9%）。
- 选择准则 ablation：Predictive Perplexity (79.6/70.2) > Binary Judgment (77.7/66.3) > PRM (75.0/64.6) > Random (69.0/61.9)。
- 解码策略 ablation：Beam Search (79.6/70.2) > MCTS (75.8/66.3) > Greedy (76.7/66.5)。
- 等预算对比：Curation×2（336.6s）Pass@1 74.6 < CoRD 79.6——提升来自协同解码机制而非更多计算。
- 泛化：MATH500 94.8、TaTQA 95.2、PubMedQA 91.8（域外和开放域）。
- 跨模型家族：R1-Llama-8B 上 CoRD-Hetero 54.0 vs. Curation-Hetero 41.3。
- Collaboration Dynamics（Fig 2）：R1-Qwen-32B 和 QwQ-32B 主导早期步骤（≤40%），Phi4-Reasoning-Plus 主导后期步骤（≥80%）。
- Integration 失败：即使 DeepSeek-V3.2-Exp 作 integrator，推理坍缩为 Short-CoT（perplexity 0.199 vs. CoRD 0.774）——lost-in-the-middle 效应。

## 变体

- **CoRD-Homo**：同构 teacher（QwQ-32B × 3，不同 temperature），AIME24 75.8%。
- **CoRD-Hetero**：异构 teacher（R1-Qwen + QwQ + Phi4），AIME24 79.6%。
- 解码策略变体：Greedy / MCTS / Beam Search。
- 选择准则变体：Random / Max-length / PRM / Binary Judgment / Predictive Perplexity。

## 优势与局限

**优势**：
- 协同解码机制使 teacher 间出现专业化分工（早期 vs. 后期步骤主导）。
- Predictive perplexity 提供连续质量信号，保留可能 self-correct 的轨迹。
- 学生超越 teacher——蒸馏实现了真正的知识融合而非简单模仿。
- 域外泛化强（TaTQA 95.2, PubMedQA 91.8）。
- 跨模型家族有效（Llama-8B 也受益）。

**局限**：
- 仅覆盖英语单语数学推理，多语言未验证。
- 蒸馏仅用 SFT——未探索 DPO 等偏好学习。
- Teacher 池目前仅 3 个 Qwen/Phi 系列模型。
- Meta-prover 依赖 teacher 池中最强模型，最强模型不可用时受限。
- 开放域任务的 LLM-as-a-judge 评估可靠性有限。
- 未探索需要外部工具调用或代码执行的推理任务。

## 关联

- [Long-CoT Reasoning Distillation](../concepts/long-cot-reasoning-distillation.md)：所属概念页。
- [FedHD](../../federated-learning/methods/fedhd.md)：共享"受控增量整合"哲学——CoRD 用 step-wise decoding 逐步构建推理链，FedHD 用 curriculum federation 逐步融合跨机构数据。
- S1、LIMO：curation-based 蒸馏范式，CoRD 的直接对比 baseline。
- [Continual Distillation](../../distillation/papers/continual-distillation-teachers-different-domains.md)：CD 的序列 teacher 蒸馏 vs. CoRD 的并行多 teacher 协同——形成 teacher 利用方式的对比。

## 开放问题

- 多语言推理（中文、日文等）的泛化性？
- Teacher 池扩展到 5+ 模型（含 GPT-5/Claude）时的质量天花板？
- DPO/RLHF 引入 CoRD 管线对齐 teacher-student 推理风格？
- Code generation / theorem proving 等相邻长链推理任务的适用性？
- 每 domain 的最优步骤粒度学习？
- 更高效的小型 specialized verifier 替代 heavy meta-prover？
