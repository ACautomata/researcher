---
title: CoRD vs Curation — Long-CoT 推理蒸馏范式对比
type: comparison
domain: llm-reasoning
status: active
created: 2026-05-24
updated: 2026-05-24
tags:
  - reasoning-distillation
  - long-cot
  - paradigm-comparison
  - multi-teacher
source_pages:
  - wiki/domains/llm-reasoning/papers/distilling-long-cot-reasoning-cord.md
related_pages:
  - wiki/domains/llm-reasoning/methods/cord.md
  - wiki/domains/llm-reasoning/concepts/long-cot-reasoning-distillation.md
---

# CoRD vs Curation — Long-CoT 推理蒸馏范式对比

## 问题

现有 Long-CoT 推理蒸馏（如 S1、LIMO）采用策展式（curation）方法：各 teacher 独立生成完整推理轨迹，post-hoc 选择最佳轨迹。CoRD 提出逐步协同解码范式。两种范式的根本区别是什么？为什么协同解码优于策展式？

## 范围

- 范式维度：策展式（curation）vs. 协同解码式（step-wise collaborative decoding）。
- 方法维度：teacher 交互方式、选择准则、解码策略。
- 实验维度：推理质量、学生蒸馏性能、计算效率、teacher 互补性。
- 不包含：integration-based 方法（post-hoc 合并多 teacher 完整轨迹）——该方法的失败已在 CoRD paper 中充分证明（推理坍缩为 Short-CoT）。

## 对比表

| 维度 | Curation（策展式） | CoRD（协同解码式） |
|------|-------------------|---------------------|
| **范式** | Post-hoc selection（各 teacher 独立生成 → 事后选择最佳） | Real-time collaboration（逐步生成 → 每步选择最优步骤） |
| **Teacher 交互** | ❌ 无交互——各 teacher 独立完成推理，互补信号无法利用 | ✅ 实时交互——每步所有 teacher 提交候选，协同构建推理链 |
| **选择粒度** | Trajectory-level（选择整条最优推理轨迹） | Step-level（每步选择最优推理步骤） |
| **选择准则** | 依赖最终答案正确性（或轨迹级质量评分） | Predictive Perplexity（连续质量信号，考虑中间步骤的贡献） |
| **动态探索** | ❌ 无——轨迹生成是确定性的（或基于 temperature sampling），无法中途调整方向 | ✅ Beam Search 维护 top-B 条部分轨迹（B=4），每步扩展 B×K 候选，持续探索 |
| **Teacher 互补性** | 未利用——最强 teacher 主导选择，弱 teacher 的独特优势被丢弃 | 充分利用——出现专业化分工（R1-Qwen + QwQ 主导早期步骤，Phi4 主导后期步骤） |
| **自纠正轨迹** | POST-hoc 选择可能丢弃含 self-correction 的轨迹（看似有错但最终正确的路径） | Predictive Perplexity 连续评分——中间看似有错的步骤若最终提升答案概率，仍可保留 |
| **计算复杂度** | $O(TKB)$（各 teacher 独立生成，一次排序选择） | $O(T \cdot K \cdot M \cdot B)$（每步 meta-prover 评估 + beam 扩展） |
| **Wall-clock** | 168.3s/题 (H200×4) | 288.7s/题（~1.7× curation） |
| **等预算对比** | Curation×2 (336.6s) 仍低于 CoRD: AIME24 74.6 vs. 79.6 | CoRD 在更低总计算量下获得更高推理质量 |
| **最佳推理质量** | 84.8% (Hetero curation answer accuracy) | 93.1% (Hetero CoRD answer accuracy) |
| **学生蒸馏 (AIME24)** | 75.0% (R1-Qwen-32B, Hetero curation) | 79.6% (R1-Qwen-32B, Hetero CoRD) |
| **学生蒸馏 (AIME25)** | 62.1% (R1-Qwen-32B, Hetero curation) | 70.2% (R1-Qwen-32B, Hetero CoRD) |
| **代表方法** | S1 (Snell 2024), LIMO (Ye 2025) | CoRD (Yun 2026) |

## 发现

1. **根本差异在于 teacher 互补信号的利用时机**：Curation 是 "事后择优"——trajectory-level 选择只能基于最终结果判断优劣，丢弃了过程中其他 teacher 的有价值步骤。CoRD 是 "事中择优"——step-level 选择允许不同 teacher 在不同推理阶段发挥各自优势（Fig 2 显示了明确的专业化分工）。
2. **Predictive Perplexity 是关键使能技术**：连续质量信号使 step-level 选择成为可能——PRM 会过滤掉 self-correct 的轨迹（因为中间步骤可能被判定为低质量），Binary Judgment 的离散标签无法区分细微的质量差异。
3. **计算效率的 "Jevons paradox"**：CoRD 单题耗时 1.7× curation，但等预算下 curation 无法追上 CoRD——CoRD 的提升来自协同解码机制，而非更多计算。这意味着 CoRD 实际上是更高效的（在单位计算量下产出更高的推理质量）。
4. **范式转换的证据强度**：CoRD 在异构 teacher 下 answer accuracy 84.8% → 93.1%（+8.3%），学生 AIME24 75.0% → 79.6%（+4.6%）。等预算对比（Curation×2 vs. CoRD）进一步排除 "更多计算" 的混淆。
5. **Integration 的失败不是计算力的限制**：即使使用更强 integrator（DeepSeek-V3.2-Exp），Integration 仍导致推理坍缩为 Short-CoT (perplexity 0.199 vs. CoRD 0.774)。近 30K token 的 teacher Long-CoT 合并超出当前 LLM 长文本处理能力（lost-in-the-middle 效应）——说明 post-hoc 融合在可预见的未来不太可能超越逐步协同。

## 注意事项

- CoRD 的计算效率优势（等预算下胜过 curation）目前仅验证于 H200×4 的特定硬件设置——在不同硬件配置和 teacher 池规模下的泛化性待验证。
- Curation 方法简单且易于并行化——在小规模 teacher 池（2 个）或 teacher 质量差异悬殊（一个显著强于其他）时，curation 可能仍是实用的选择。

## 证据

- CoRD paper: arXiv:2605.02290, full-paper (21 页全文)。Table 2 (推理质量对比), Table 3 (学生蒸馏), Table 5-6 (选择准则和解码策略 ablation), Table 14-15 (计算效率 + 等预算对比), Fig 2 (collaboration dynamics 专业化分工)。
- S1 (Snell 2024), LIMO (Ye 2025): 作为 curation 范式的代表方法。

## 后续

- 在更多 teacher 池配置（5+ teachers）上验证 CoRD 对 curation 的优势是否继续扩大。
- 探索 "hybrid" 策略：curation 快速初筛 + CoRD 精细化逐步优化——平衡效率和质量。
- 将 CoRD 的逐步协同解码思想推广到 code generation、theorem proving 等相邻长链推理任务。
