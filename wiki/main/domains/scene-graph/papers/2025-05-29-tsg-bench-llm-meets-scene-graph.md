---
title: "TSG Bench: LLM Meets Scene Graph — Can Large Language Models Understand and Generate Scene Graphs?"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - llm-evaluation
  - scene-graph-benchmark
  - scene-graph-understanding
  - scene-graph-generation
  - action-decomposition
  - in-context-learning
  - chain-of-thought
  - error-refinement
  - hallucination
raw_sources:
  - ../../../sources/scene-graph/2025-05-29-LLM-Meets-Scene-Graph.pdf
  - ../../../sources/scene-graph/2025-05-29-LLM-Meets-Scene-Graph.txt
paper:
  title: "LLM Meets Scene Graph: Can Large Language Models Understand and Generate Scene Graphs? A Benchmark and Empirical Study"
  authors:
    - Dongil Yang
    - Minjin Kim
    - Sunghwan Kim
    - Beong-woo Kwak
    - Minjun Park
    - Jinseok Hong
    - Woontack Woo
    - Jinyoung Yeo
  year: 2025
  venue: arXiv preprint
  arxiv: "2505.19510"
  code: "https://github.com/docworlds/tsg-bench"
  project: "https://tsg-bench.netlify.app"
classification:
  label: LLM Scene Graph Benchmark
  task:
    - Scene Graph Understanding (SGDS, SGQA)
    - Scene Graph Generation (SA-SGG, MA-SGG)
    - Action Decomposition
    - Error Refinement
  method_family: Benchmark & Empirical Study
  modality: Text (narratives)
  datasets:
    - TSG Bench (self-constructed)
  metrics:
    - Accuracy (SGDS)
    - Exact Match / EM (SGQA)
    - Precision, Recall, Macro F1 (SA-SGG, MA-SGG)
evidence_level: full-paper
---

## Citation

Yang, D., Kim, M., Kim, S., Kwak, B., Park, M., Hong, J., Woo, W., Yeo, J. "LLM Meets Scene Graph: Can Large Language Models Understand and Generate Scene Graphs? A Benchmark and Empirical Study." arXiv:2505.19510, May 2025. [arXiv](https://arxiv.org/abs/2505.19510) | [Code](https://github.com/docworlds/tsg-bench) | [Demo](https://tsg-bench.netlify.app)

## One-Sentence Contribution

提出 TSG Bench，一个系统评估 LLM 在场景图理解（SGDS/SGQA）和生成（SA-SGG/MA-SGG）能力的基准，发现 LLM 在场景图理解上表现良好但生成任务（尤其是多动作分解）远逊于人类，10-shot ICL 可缓解但差距仍大。

## Problem Setting

- **目标**：系统评估 LLM 理解和生成场景图的能力，填补缺乏综合评估框架的空白
- **核心问题**：LLM 是否真正理解场景图中的空间和语义结构？能否从文本叙事中生成准确的场景图？
- **挑战**：
  - 现有工作将场景图用于 LLM（robotics, 3D 建模）但缺乏对其基本能力的评估
  - 动态场景（包含时间演变的动作序列）的推理比静态场景更复杂
  - 多动作叙事需要隐含的场景分解（implicit decomposition），这对 LLM 是主要瓶颈
- **设定**：构建 120 个真实世界场景（维护、烹饪、园艺等）的文本叙事-场景图数据对，设计四个任务覆盖理解和生成两个维度

## Method

### TSG Bench 基准

#### 数据表示

- 叙事 D = (d₁, ..., dₙ)，包含多个连贯的自然语言描述
- 每个描述 dᵢ 对应一组场景图 Gᵢ = (Gᵢ₁, ..., Gᵢₖ)，k 范围 1–8（平均 3.64），取决于描述的复杂性
- 每个场景图 Gᵢⱼ = (Vᵢⱼ, Eᵢⱼ)，以 (source node, edge, target node) 三元组表示
- 节点类别：{person, action, object, hand}
- 边类别：{verb, dobj, preposition}
- 预定义元素集 L 确保一致性（不含描述中的附加修饰语）

#### 四个评估任务

1. **SGDS (Scene Graph Description Selection)**：给定图形和四个描述，选最符合的描述。指标：Accuracy
2. **SGQA (Scene Graph Question Answering)**：给定图形和问题，选正确答案。指标：Exact Match (EM)
3. **SA-SGG (Single Action Scene Graph Generation)**：根据描述生成单个场景图。指标：Precision, Recall, F1
4. **MA-SGG (Multiple Action Scene Graph Generation)**：根据描述生成多个离散场景图（需动作分解）。指标：Precision, Recall, F1

#### 基准统计

| 属性 | 值 |
|------|-----|
| 场景数 | 120 |
| 描述数 | 2,041 |
| 场景图数 | 4,298 |
| 不同节点数 | 14,905 |
| 不同边数 | 11,820 |
| 领域覆盖 | maintenance, cooking, gardening 等 |
| SGQA 样本 | 500 |
| SGDS 样本 | 250 |
| SA-SGG 样本 | 1,188 |
| MA-SGG 样本 | 853 |

### 评估模型

**Proprietary**：GPT-4o, GPT-4o-mini, Claude-3.5-Sonnet, Claude-3.5-Haiku
**Open-source**：LLaMA-3.3-70B, Qwen-2.5-72B, Qwen-2.5-7B, DeepSeek-V3, Mixtral-8x22B, Mistral-large, Mistral-7B

并收集 30 个人类样本作为对照。

### 评估方法

- Zero-shot 提示（零样本）
- 额外评估 CoT（Chain-of-Thought）和 10-shot ICL
- Zero-shot 时 SGQA 用 Acc/EM，SGG 任务用 Precision/Recall/F1
- 消融实验：将生成任务分解为 node generation、edge generation、action decomposition 三个子任务单独评估
- 错误修正实验：提供含 4 类错误（Redundant/Missing/Mismatched/Reversed）的场景图，评估 LLM 修正能力
- 幻觉分析：统计 SA-SGG 中的幻觉元素数量

## Experiments

### 实验设置

- 全部采用 zero-shot prompting（无额外示例或训练）
- 理解任务：SGDS 输出单一字母答案（Acc），SGQA 输出单一元素（EM）
- 生成任务：输出结构化场景图三元组（Precision/Recall/F1）
- 额外实验：CoT prompting 和 10-shot ICL 的提升效果

### 主要结果

#### 理解任务（SGDS, SGQA）—— 所有模型表现良好

| 模型 | SGDS (Acc) | SGQA (EM) |
|------|-----------|-----------|
| Human | 98.33 | 88.00 |
| **Claude-3.5-Sonnet** | **98.40** | **90.60** |
| GPT-4o | 96.40 | 84.80 |
| GPT-4o-mini | 96.80 | 76.60 |
| Claude-3.5-Haiku | 97.20 | 82.00 |
| LLaMA-3.3-70B | 97.60 | 84.60 |
| Qwen-2.5-72B | 96.80 | 81.40 |
| DeepSeek-V3 | 96.40 | 79.60 |
| Mixtral-8x22B | 96.00 | 73.00 |
| Mistral-large | 96.40 | 82.40 |
| Qwen-2.5-7B | 93.60 | 73.40 |
| Mistral-7B | 90.14 | 58.20 |

#### 生成任务（SA-SGG, MA-SGG）—— 显著低于人类

| 模型 | SA-SGG (Prec/Rec/F1) | MA-SGG (Prec/Rec/F1) |
|------|---------------------|----------------------|
| Human | 85.22 / 81.00 / **82.50** | 78.80 / 72.90 / **75.60** |
| **Claude-3.5-Sonnet** | 69.75 / 69.33 / **68.43** | 60.77 / 57.91 / **58.80** |
| GPT-4o | 65.84 / 55.04 / 59.23 | 48.88 / 40.84 / 43.99 |
| GPT-4o-mini | 20.00 / 21.50 / 19.90 | 23.06 / 18.32 / 20.07 |
| Claude-3.5-Haiku | 38.31 / 36.82 / 36.77 | 27.00 / 23.97 / 24.95 |
| LLaMA-3.3-70B | 31.52 / 38.90 / 33.37 | 32.43 / 26.58 / 28.92 |
| Qwen-2.5-72B | 57.96 / 53.22 / 54.42 | 42.64 / 33.29 / 36.78 |
| DeepSeek-V3 | 55.79 / 55.11 / 54.45 | 43.67 / 36.66 / 39.34 |
| Mistral-large | 63.18 / 55.37 / 58.15 | 40.17 / 32.12 / 35.13 |
| Qwen-2.5-7B | 9.58 / 9.95 / 9.39 | 6.61 / 6.77 / 6.34 |
| Mistral-7B | 13.60 / 14.64 / 13.14 | 13.86 / 10.57 / 11.67 |

### 提升技术效果

| 方法 | SGDS (Acc) | SGQA (EM) | SA-SGG (F1) | MA-SGG (F1) |
|------|-----------|-----------|-------------|-------------|
| Claude-3.5-Sonnet (zero-shot) | 98.40 | 90.60 | 68.43 | 58.80 |
| + CoT | 98.00 | **94.00** | 69.57 | 64.36 |
| + **10-shot ICL** | **98.80** | 92.00 | **75.29** | **71.75** |
| GPT-4o (zero-shot) | 96.40 | 84.80 | 59.23 | 43.99 |
| + CoT | 96.80 | **90.00** | 67.13 | 44.79 |
| + **10-shot ICL** | **99.20** | 84.40 | 65.78 | **57.40** |

### 错误修正结果

| 错误类型 | w/o Error Type (GPT-4o/Claude) | w/ Error Type (GPT-4o/Claude) |
|---------|-------------------------------|------------------------------|
| Overall | 40.04 / 60.03 | **64.80** / **88.28** |
| Redundant | 64.38 / 70.02 | 73.29 / 93.06 |
| Missing | 46.67 / 82.25 | 58.42 / 80.89 |
| Mismatched | 10.81 / 38.29 | **58.92** / **81.94** |
| Reversed | 44.24 / 49.55 | 68.55 / **97.22** |

### 幻觉分析（SA-SGG 任务，1,188 样本）

| 模型 | 总幻觉数 | Desc. Elements | New Elements |
|------|---------|---------------|-------------|
| Claude-3.5-Sonnet | **17** | 14 | **3** |
| GPT-4o | 215 | 156 | 59 |
| Qwen-2.5-7B | 395 | 192 | 203 |
| Mistral-7B | 616 | 235 | 381 |

## Results

1. **理解 vs 生成能力差距显著**：最强模型 Claude-3.5-Sonnet 理解任务（SGDS 98.40, SGQA 90.60）接近甚至超过人类，但生成任务远低于人类（SA-SGG F1 68.43 vs 人类 82.50；MA-SGG F1 58.80 vs 人类 75.60）
2. **动作分解是主要瓶颈**：生成任务中模型精度高于召回率（如 Mistral-large: Prec 40.17 vs Rec 32.12），表示不能完整覆盖子场景。消融实验确认 action decomposition 是最大挑战
3. **ICL 大幅提升生成能力**：10-shot ICL 将 Claude-3.5-Sonnet 的 MA-SGG F1 从 58.80 提升到 71.75（+22.0%），接近人类 75.60。CoT 更有利于推理任务（SGQA）
4. **错误类型引导显著提高修正质量**：Claude-3.5-Sonnet 在知晓错误类型后修正 F1 从 60.03 升至 88.28（+47.1%），特别是 Reversed 类型从 49.55 → 97.22
5. **幻觉与小模型强相关**：Claude-3.5-Sonnet 仅 17 次幻觉（< 0.2%），而 Mistral-7B 达 616 次（> 51.9%）

## Limitations

- 基准数据基于 action-centric 场景图（源自 EASG 约定），人类节点、hand tracking 等可能不适用于所有场景图表示
- 评估完全基于文本（Text-Scene Graphs），未涵盖直接从视觉输入构建场景图的能力（图像/视频→场景图）
- 仅评估单轮/静态框架，缺乏交互式或 agent-in-the-loop 设置
- TSG Bench 构建使用预定义元素集 L 约束生成空间，与完全开放式生成评估存在差距
- 仅 30 个人类样本，统计可靠性有限

## Connections

- 与 [[domains/scene-graph/papers/textpsg-panoptic-scene-graph-from-textual-descriptions.md|TextPSG]] 共享文本→场景图的任务设定，但 TSG Bench 侧重 LLM 能力评估而非提出新方法
- 与 R1-SGG 互补：R1-SGG 用 RL 提升 MLLM 端到端 SGG 能力，TSG Bench 提供纯文本 LLM 场景图能力的基线评估
- 与 [[domains/scene-graph/papers/2025-05-30-hidynagraph.md|Hi-Dyna Graph]] 同属 LLM + 场景图交叉领域，Hi-Dyna Graph 侧重下游机器人应用
- TSG Bench 的 action decomposition 瓶颈发现与 PSG-4D / FDSG 等动态场景图工作相关

## Open Questions

- 如果直接将视觉特征（如 CLIP embedding）作为模型输入而非纯文本场景图表达，生成能力有无提升？
- 是否需要专门训练场景图生成功能的 LLM（如通过 RL 或 scene-graph-aware fine-tuning）？
- 从错误类型引导修正的结果看，LLM 理解场景图的能力远超生成能力——这个 gap 是否本质上源于训练数据分布？
- 120 个场景、11 个模型是否能推广到更多样化的场景图和新型 LLM 架构？

## Provenance

- arXiv:2505.19510v2 (May 29, 2025)
- Raw: `raw/sources/2025-05-29-LLM-Meets-Scene-Graph.pdf` (2.9MB, 26 pages)
- Extract: `raw/sources/2025-05-29-LLM-Meets-Scene-Graph.txt` (82,976 chars)
- Evidence: full-paper — 全文通读，所有实验结果和表均已捕获
