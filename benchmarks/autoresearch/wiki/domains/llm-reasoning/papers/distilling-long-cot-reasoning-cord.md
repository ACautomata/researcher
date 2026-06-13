---
title: Distilling Long-CoT Reasoning through Collaborative Step-wise Multi-Teacher Decoding
type: paper
domain: llm-reasoning
status: active
created: 2026-05-05
updated: 2026-05-05
tags:
  - reasoning-distillation
  - long-cot
  - multi-teacher
  - step-wise-decoding
  - knowledge-distillation
paper:
  title: Distilling Long-CoT Reasoning through Collaborative Step-wise Multi-Teacher Decoding
  authors:
    - Taewon Yun
    - Jisu Shin
    - Jeonghwan Choi
    - Seunghwan Bang
    - Hwanjun Song
  year: 2026
  venue: arXiv preprint
  arxiv: "2605.02290"
  doi: ""
  code: "https://github.com/DISL-Lab/CoRD"
  project: ""
classification:
  label: llm-reasoning
  task:
    - reasoning distillation
    - long-chain-of-thought
  method_family:
    - multi-teacher knowledge distillation
    - step-wise decoding
    - beam search
  modality:
    - text
  datasets:
    - LIMO-v1
    - AIME24
    - AIME25
    - MATH500
    - TaTQA
    - PubMedQA
  metrics:
    - Pass@1
    - predictive perplexity
    - answer accuracy
evidence_level: full-paper
raw_sources:
  - raw/sources/2026-04-26-distilling-long-cot-reasoning-cord.pdf
related_pages:
  - wiki/domains/llm-reasoning/concepts/long-cot-reasoning-distillation.md
  - wiki/domains/llm-reasoning/methods/cord.md
  - wiki/domains/llm-reasoning/comparisons/cord-vs-curation.md
---

## Citation

Yun, T., Shin, J., Choi, J., Bang, S., & Song, H. (2026). Distilling Long-CoT Reasoning through Collaborative Step-wise Multi-Teacher Decoding. *arXiv preprint arXiv:2605.02290*. KAIST & UNIST.

## One-Sentence Contribution

提出 CoRD（Collaborative Reasoning Decoding），将 Long-CoT 推理蒸馏重新定义为**逐步协同解码**过程——多个异构 teacher LRM 在每步提出候选推理步骤，通过基于预测困惑度（predictive perplexity）的选择机制和 beam search，联合构建高质量推理轨迹，学生模型在 AIME24/25 上接近甚至超越 teacher 水平。

## Problem Setting

大型推理模型（DeepSeek-R1、QwQ、Phi4-Reasoning-Plus 等）通过 test-time scaling 实现极强的复杂推理能力，但完整推理成本极高。现有推理蒸馏方案（如 S1、LIMO）采用**策展式（curation）**方法：各 teacher 独立生成完整推理轨迹，然后 post-hoc 选择最佳轨迹。这种方案存在两个根本局限：(1) teacher 间的互补推理信号无法交互——每个 teacher 独立生成轨迹，无法在推理过程中利用其他 teacher 的强项；(2) 缺乏动态探索——post-hoc 选择只能基于最终结果，无法在推理中适时调整方向。

CoRD 将推理蒸馏重新定义为逐步协同自回归解码过程：每个推理步骤作为一个"token"，teacher 提出的候选步骤形成"解码词表"，通过逐步选择累积最优推理链。

## Method

**CoRD 三核心组件**：

1. **Prompt-guided Step Segmentation（提示引导步骤分割）**：
   - 在初始 prompt 中嵌入 `<think> ### Step` 标记，引导 LRM 在生成过程中将推理自然分割为语义连贯的功能性步骤
   - 对比 line-break（纯格式分割，无语义一致性）和 prefix-based（基于 "wait"/"alternatively" 等标记，跨模型不一致）
   - 优势：跨模型高度一致的步骤粒度，同时保持 semantic parity 和 style consistency

2. **Perplexity-based Step Selection（预测困惑度步骤选择）**：
   - 引入 meta-prover（独立评分模型，使用 teacher 池中最强的 QwQ-32B）
   - 在步骤 $t$，给定当前推理前缀 $\tau_{<t}$ 和第 $k$ 个 teacher 提出的候选步骤 $s_t^{(k)}$，计算条件概率 $p_{meta}(A | \tau_{<t} \oplus s_t^{(k)})$，其中 $A$ 是 ground-truth answer
   - 选择使预测困惑度最高的候选步骤 $s_t^* = \arg\max_k p_{meta}(A | \tau_{<t} \oplus s_t^{(k)})$
   - 对比方法：Random/Max-length Selection（噪声大）、PRM（过滤了可能 self-correct 的轨迹）、Binary Judgment（离散标签，无法区分细微质量差异）

3. **Step-wise Decoding with Beam Search（带束搜索的逐步解码）**：
   - 维护 top-$B$ 条部分推理轨迹（$B=4$），每步扩展 $B \times K$ 条候选
   - 贪婪解码仅 81.6% answer accuracy，MCTS 仅 89.6%（且计算成本高 2×），Beam Search 93.1%
   - MCTS 偏向全局强 teacher 而非局部最适合特定步骤的 teacher，削弱互补性

**计算复杂度**：$O(T \cdot K \cdot M \cdot B)$，其中 $T$ 为推理步数，$K$ 为 teacher 数，$M$ 为 meta-prover 开销，$B$ 为 beam size。MCTS 为 $O(TK\log(TMB))$，curation 为 $O(TKB)$。实际 wall-clock：CoRD 288.7s/题 vs. MCTS 589.2s/题 vs. Curation 168.3s/题（H200×4）。

## Experiments

**Teacher 配置**：
- 同构（Homogeneous）：QwQ-32B × 3（temperature ∈ {0.5, 0.6, 0.7}）
- 异构（Heterogeneous）：R1-Distill-Qwen-32B + QwQ-32B + Phi4-Reasoning-Plus（temperature 固定 0.6）
- 所有公平比较下，总生成轨迹数量均等（4 条）

**Base 数据集**：LIMO-v1（817 题，数学）、S1k-1.1（1000 题）、LIMO-v2（800 题）

**学生模型**：R1-Qwen-7B/14B/32B（监督微调）、R1-Llama-8B（跨架构验证）

**训练设置**：SFT only，batch size 8，5 epochs，lr 5e-6 cosine，max seq 20480，DeepSpeed Stage-3，8×NVIDIA H100

**评估**：AIME24、AIME25、MATH500（域内）、TaTQA（域外表阅读）、PubMedQA（开放域生物医学 QA），Pass@1（16 次平均）

**Baseline 蒸馏管线**：
- Curation：各 teacher 独立生成完整轨迹 → post-hoc 选择最佳（S1/LIMO 范式）
- Integration：GPT5o-mini 作为外部 integrator 合并多 teacher 完整轨迹（post-hoc 融合）

**Ablation 维度**：
- 步骤分割方法（line-break / prefix / prompt-guided）
- 步骤选择准则（Random / Max-length / PRM / Binary Judgment / Predictive Perplexity）
- 解码策略（Greedy / MCTS / Beam Search）
- Meta-prover 强度（QwQ-32B / Phi-4 / R1-Qwen）
- 计算预算匹配（Curation×2 vs. CoRD）
- Integration 强度（GPT5o-mini vs. DeepSeek-V3.2-Exp）

## Results

**推理质量**（Table 2, LIMO-v1）：

| Teacher 配置 | Pipeline | Answer Acc (%) | Predictive Perplexity |
|-------------|----------|---------------|----------------------|
| Homo. | Curation | 77.4 | 0.664 |
| Homo. | Integration | 88.6 | 0.215 |
| Homo. | **CoRD** | **90.0** | **0.726** |
| Hetero. | Curation | 84.8 | 0.652 |
| Hetero. | Integration | 91.2 | 0.223 |
| Hetero. | **CoRD** | **93.1** | **0.774** |

**学生蒸馏性能**（Table 3, AIME Pass@1）：

| Pipeline | 7B | 14B | 32B |
|----------|-----|------|------|
| w/o Distillation | 51.3/37.5 | 68.1/50.6 | 71.6/53.8 |
| Curation-Homo | 55.8/40.2 | 72.5/54.7 | 74.2/62.7 |
| Integration-Homo | 7.9/5.4 | 7.1/6.3 | 11.9/6.9 |
| CoRD-Homo | 58.5/42.9 | 73.7/59.3 | 75.8/64.4 |
| Curation-Hetero | 56.6/42.1 | 68.1/54.6 | 75.0/62.1 |
| Integration-Hetero | 8.3/3.8 | 7.5/4.0 | 12.7/9.0 |
| **CoRD-Hetero** | **60.8/45.6** | **74.8/62.3** | **79.6/70.2** |

**关键**：CoRD-Hetero 训练的 R1-Qwen-32B 在 AIME24 上 Pass@1 79.6%，超越所有单个 teacher（R1-Qwen-32B: 71.6%, QwQ-32B: 77.9%, Phi4: 78.9%）；在 AIME25 上 70.2%，同样超越所有 teacher（53.8%, 66.7%, 67.9%）。

**步骤分割 Ablation**（Table 4, 异构 teacher, R1-Qwen-32B）：Prompt-guided > Prefix > Line-break（AIME25: 70.2 vs. 67.3 vs. 67.7）

**选择准则 Ablation**（Table 5）：Predictive Perplexity (79.6/70.2) > Binary Judgment (77.7/66.3) > PRM (75.0/64.6) > Random (69.0/61.9) > Max-length (68.8/59.0)

**解码策略 Ablation**（Table 6）：Beam Search (79.6/70.2) > MCTS (75.8/66.3) > Greedy (76.7/66.5)

**泛化性**（Table 7, R1-Qwen-32B）：
- MATH500：CoRD-Hetero 94.8 vs. Curation-Hetero 93.4 vs. w/o 92.1
- TaTQA（域外）：CoRD-Hetero **95.2** vs. Curation-Hetero 88.2 vs. w/o 87.3
- PubMedQA（开放域）：CoRD-Hetero **91.8** vs. Curation-Hetero 88.4 vs. w/o 86.0

**与 S1/LIMO 数据集对比**（Fig 3）：在等量数据下，CoRD 生成的数据训练的学生在 AIME24 和 AIME25 上均显著超越原始 curated datasets。

**计算效率**（Table 14, H200×4）：CoRD 288.7s/题，MCTS 589.2s，Curation 168.3s。CoRD 在 MCTS 约一半时间内获得更高推理质量。

**等预算对比**（Table 15）：即使将 Curation 计算预算翻倍匹配 CoRD（336.6s），Curation×2 的 Pass@1 仍低于 CoRD（AIME24: 74.6 vs. 79.6），说明 CoRD 的提升来自协同解码机制而非单纯更多计算。

**跨模型家族**（Table 12, R1-Llama-8B）：CoRD-Hetero AIME24 54.0 vs. Curation-Hetero 41.3，跨 Llama 模型家族依然有效。

**Meta-prover 强度**（Table 9）：更强 meta-prover 持续提升推理质量和蒸馏性能。弱 meta-prover 降低效果。

**Collaboration Dynamics**（Fig 2）：CoRD 展现专业化分工——R1-Qwen-32B 和 QwQ-32B 主导早期步骤（≤40%，问题表述与约束分析），Phi4-Reasoning-Plus 主导后期步骤（≥80%，综合推理结论）。

**Integration 失败分析**：即使使用更强 integrator DeepSeek-V3.2-Exp，Integration 仍导致推理坍缩为 Short-CoT（predictive perplexity 仅 0.199 vs. CoRD 0.774），原因是近 30K token 的 teacher Long-CoT 合并超出当前 LLM 长文本处理能力（lost-in-the-middle 效应）。

## Limitations

1. 主要评估仅覆盖英语单语数学推理（AIME），多语言泛化性未验证
2. 蒸馏仅使用 SFT；未探索 DPO 等偏好学习方法进一步对齐 teacher-student 推理风格差异
3. Teacher 池限制在 3 个 Qwen/Phi 系列模型，扩展性到更多/更强的 teacher（如 GPT-5, Claude）未测试
4. Meta-prover 依赖 teacher 池中最强模型，当最强模型不可用时方案受限
5. 开放域任务的评估（PubMedQA）依赖 LLM-as-a-judge，评分可靠性可能有限
6. 对需要外部工具调用或代码执行的多模态推理任务的适用性未探索

## Reusable Claims

- Claim: 逐步协同解码（step-wise collaborative decoding）显著优于 post-hoc curation 和 post-hoc integration，核心在于 teacher 间的互补推理信号在推理过程中实时交互。
  Evidence: [CoRD](distilling-long-cot-reasoning-cord.md), Table 2-3—异构 teacher 下 CoRD Pass@1 79.6 vs. Curation 75.0 vs. Integration 12.7。
  Scope: 数学推理（AIME24/25、MATH500）。Confidence: high。

- Claim: predictive perplexity 作为步骤级选择准则优于 PRM 和 Binary Judgment，因为它提供了连续的质量信号，允许模型保留可能 self-correct 的轨迹。
  Evidence: [CoRD](distilling-long-cot-reasoning-cord.md), Table 5—Predictive Perplexity 79.6 vs. PRM 75.0 vs. Binary Judgment 77.7。
  Scope: AIME24/25, R1-Qwen-32B student。Confidence: high。

- Claim: beam search 在逐步协同解码中优于 MCTS，因为 MCTS 的 trajectory-level reward 会偏向全局强 teacher 而削弱 teacher 间的步骤级互补性。
  Evidence: [CoRD](distilling-long-cot-reasoning-cord.md), Table 6 + Fig 5—Beam Search 79.6 vs. MCTS 75.8。
  Scope: AIME24/25, R1-Qwen-32B。Confidence: medium。

- Claim: prompt-guided step segmentation 通过同时保持语义一致性和风格一致性，使异构 teacher 能在共享步骤框架内有效协作。
  Evidence: [CoRD](distilling-long-cot-reasoning-cord.md), Table 4—Prompt-guided 79.6 vs. Prefix 77.1 vs. Line-break 76.7。
  Scope: AIME24/25, 3 个异构 teacher。Confidence: medium。

- Claim: CoRD 生成的推理数据质量超越了手动 curated datasets（S1k-1.1、LIMO-v1/v2），在等量数据下训练的学生性能更高。
  Evidence: [CoRD](distilling-long-cot-reasoning-cord.md), Fig 3—CoRD 在 AIME24 和 AIME25 上全面超越原始 curated datasets。
  Scope: LIMO-v1/v2, S1k-1.1。Confidence: medium。

## Connections

- [Long-CoT Reasoning Distillation](../concepts/long-cot-reasoning-distillation.md)：本域概念页，CoRD 是核心论文之一
- S1 (Snell et al., 2024)、LIMO (Ye et al., 2025)：curation-based 推理蒸馏的典型代表，CoRD 的直接对比 baseline
- DeepSeek-R1 (Guo et al., 2025)：teacher 模型之一，定义了 Long-CoT 推理范式
- 与 `distillation` 域的连接：CoRD 使用 "knowledge distillation"（模型压缩），与数据集蒸馏截然不同

## Open Questions

1. CoRD 对多语言推理（中文、日文等非英语数学推理）的泛化性？
2. 当 teacher 池扩展到 5+ 模型（包括闭源 GPT-5/Claude）时，协同解码的质量天花板在哪？
3. 如何将 DPO/RLHF 等偏好学习引入 CoRD 管线，进一步对齐 teacher-student 推理风格？
4. CoRD 是否适用于 code generation / theorem proving 等需要长链推理的相邻任务？
5. step segmentation 策略能否进一步优化——例如学习每个 domain 的最优步骤粒度？
6. 更高效的 meta-prover 设计（如小型 specialized verifier）能否在几乎不损失质量的前提下进一步降低元评分成本？

## Provenance

- 从 PDF `raw/sources/2026-04-26-distilling-long-cot-reasoning-cord.pdf`（arXiv 2605.02290v1，21 页）全文中提取。
- 全文阅读：包括方法描述（§4.1-4.4）、主实验（Table 2-3）、ablation（Table 4-6）、泛化（Table 7）、等预算对比（Table 15）、协同动态分析（Fig 2）、计算效率（Table 14）、跨模型验证（Table 12）、附录所有结果。
- 代码：https://github.com/DISL-Lab/CoRD。
