---
title: "R1-SGG: Compile Scene Graphs with Reinforcement Learning"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - scene-graph-generation
  - reinforcement-learning
  - multimodal-llm
  - GRPO
  - visual-instruction-tuning
  - end-to-end-sgg
  - arxiv-2025
raw_sources:
  - ../../../sources/scene-graph/2025-arXiv-R1-SGG-Compile-Scene-Graphs-with-Reinforcement-Learning.pdf
  - ../../../sources/scene-graph/2025-arXiv-R1-SGG-Compile-Scene-Graphs-with-Reinforcement-Learning.txt
related_pages:
  - cage-sgg-counterfactual-active-graph-evidence-open-vocabulary-sgg.md
evidence_level: full-paper
paper:
  title: "R1-SGG: Compile Scene Graphs with Reinforcement Learning"
  abbreviated: "R1-SGG"
  authors:
    - Zuyao Chen
    - Jinlin Wu
    - Zhen Lei
    - Marc Pollefeys
    - Chang Wen Chen
  affiliations:
    - The Hong Kong Polytechnic University
    - ETH Zürich
    - CAIR, HKISI-CAS
    - Institute of Automation, CAS
    - Microsoft
  year: 2025
  venue: arXiv 2025 (arXiv:2504.13617v4)
  doi: null
  arxiv: "2504.13617"
  code: null
  url: null
---

# R1-SGG: Compile Scene Graphs with Reinforcement Learning

## 核心思想

现有 SGG 方法通常将任务解耦为物体检测 + 关系分类两个子任务，传统模型受限于标注分布，LLM 驱动的弱监督方法则精度不足。多模态大模型（M-LLM）有潜力以端到端方式直接从图像生成场景图，但面临指令遵循差、重复预测、定位不准等挑战。

**R1-SGG** 提出两阶段训练框架：首先在场景图数据集上进行监督微调（SFT），随后通过强化学习（GRPO）结合图中心化的规则奖励（graph-centric rewards）来优化 M-LLM 的结构化场景图生成能力。

**核心创新**：
- 基于 GRPO 的强化学习用于端到端 SGG（首次探索）
- 三组图中心奖励：Hard Recall、Hard Recall+Relax、Soft Recall，对齐标准 SGDET 指标
- 格式一致性奖励（format reward）确保输出符合结构化 schema

## 方法

### 框架总览

1. **SFT 阶段**：在 VG150/PSG 数据集上对 M-LLM（Qwen2-VL-2B/7B）进行视觉指令微调，使用 prompt-response 对和交叉熵 loss
2. **RL 阶段**：使用 GRPO（Group Relative Policy Optimization）在线策略优化，结合图中心奖励信号

### 奖励设计

#### 格式奖励（Format Reward）
- 当输出遵循 `<think>...</think><answer>...</answer>` 格式且 `<answer>` 段包含 "objects" 和 "relationships" 关键词时奖励为 1，否则为 0

#### Hard Recall（硬召回）
- 严格对齐 SGDET 标准召回指标
- 正例条件：预测的三元组标签完全匹配 ground-truth（subject/predicate/object）且 bbox IoU > 0.5
- 稀疏但指标对齐

#### Hard Recall + Relax（松弛硬召回）
- 用实体嵌入的余弦相似度替代精确标签匹配，提供更平滑的梯度信号

#### Soft Recall（软召回）
- 将奖励构建为二分图匹配问题（类似 DETR），用 embedding 相似度 + IoU + bbox L1 距离的组合代价进行节点和边级别的密集匹配
- 代价函数：cost = λ1·(1 - cos(emb)) + λ2·(1 - IoU) + λ3·||bi - bj||₁

### 训练配置
- SFT：3 epochs，batch size 128，4×A100（80GB），AdamW，lr=1e-5
- RL：1 epoch，batch size 32，每样本 8 个 generation，16×GH200（120GB），AdamW，lr=6e-7

## 实验

### 数据集
- **VG150**：150 object / 50 relation categories，训练 56,224 对，验证 5,000 对
- **PSG（Panoptic Scene Graph）**：80 thing / 53 stuff / 56 relation categories，训练 46,563 对，测试 2,186 对

### 评估指标
- **SGDET protocol**：Recall、mean Recall（mRecall）、AP@50（目标检测）、Failure Rate（格式一致性）

### VG150 主结果

| 方法 | 参数量 | Failure Rate (%) | AP@50 | Recall | mRecall |
|------|:-----:|:----------------:|:-----:|:------:|:-------:|
| IMP | — | — | 20.91 | 17.85 | 2.66 |
| MOTIFS | — | — | 29.56 | 27.21 | 7.84 |
| VCTree | — | — | 28.13 | 24.87 | 8.47 |
| OvSGTR | — | — | 33.39 | 26.74 | 5.83 |
| GPT-4o | — | 2.94 | 0.00 | 0.00 | 0.00 |
| Gemini 1.5 Flash | — | 1.10 | 0.51 | 0.10 | 0.08 |
| Qwen2-VL-2B | 2B | 59.96 | 2.18 | 0.07 | 0.18 |
| +SFT | 2B | 72.42 | 8.10 | 5.47 | 1.46 |
| Qwen2-VL-7B | 7B | 54.46 | 6.07 | 0.69 | 0.80 |
| +SFT | 7B | 39.54 | 14.18 | 9.62 | 3.30 |
| **R1-SGG-Zero (2B)** | 2B | 0.34 | 12.30 | 11.89 | 5.70 |
| **R1-SGG (2B)** | 2B | **0.10** | 17.87 | 21.09 | 7.48 |
| **R1-SGG-Zero (7B)** | 7B | 0.04 | 15.59 | 18.34 | 8.32 |
| **R1-SGG (7B)** | 7B | **0.08** | **19.47** | **23.75** | **11.43** |

- **关键结果**：R1-SGG (7B) 达到 Recall 23.75%、mRecall 11.43%，大幅超越传统 SGG 方法和商业/开源 M-LLM
- RL 将 Failure Rate 从 SFT 的 39.54%-72.42% 降至 **0.08%-0.10%**（几乎消失）
- even SFT alone的 M-LLM 在 mRecall 上（3.30%）仍不及传统方法 MOTIFS（7.84%），而 R1-SGG 的 mRecall（11.43%）首次让 M-LLM 超越传统 SGG 方法

### PSG 主结果

| 方法 | 参数量 | Failure Rate (%) | AP@50 | Recall | mRecall |
|------|:-----:|:----------------:|:-----:|:------:|:-------:|
| PSGFormer | — | — | — | 18.60 | 16.70 |
| Qwen2-VL-7B+SFT | 7B | 0.96 | 40.79 | 24.73 | 17.11 |
| **R1-SGG-Zero (7B)** | 7B | 0.00 | 32.92 | 37.00 | 32.04 |
| **R1-SGG (7B)** | 7B | **0.00** | **42.05** | **43.48** | **33.71** |

- PSG 上 R1-SGG (7B) Recall **43.48%**，mRecall **33.71%**，Failure Rate 降至零
- 显著超越 PSGFormer（Recall 18.60%, mRecall 16.70%）和所有 M-LLM 基线

### 跨域泛化

- VG150 训练的 SFT 模型在 PSG 上仅 Recall 3.03%/mRecall 1.36%，泛化性差
- R1-SGG-Zero（无 SFT）跨域泛化更鲁棒
- R1-SGG（SFT+RL）在领域内最佳，但跨域泛化受 SFT 过拟合影响

### 奖励消融（VG150, 7B）

| 设置 | 稀疏性 | 指标对齐 | Failure Rate (%) | AP@50 | Recall (%) | mRecall (%) |
|------|:-----:|:--------:|:----------------:|:-----:|:----------:|:-----------:|
| Hard Recall | 稀疏 | ✓ | 0.08 | 19.47 | **23.75** | **11.43** |
| Hard Recall+Relax | 中等 | ✗ | 0.02 | 19.93 | 24.05 | 9.61 |
| Soft Recall | 密集 | ✗ | 0.06 | 18.73 | 21.92 | 5.61 |

- Hard Recall 尽管奖励稀疏但 mRecall 最高（11.43%），说明奖励与评估指标对齐比平滑性更重要

### 额外分析

- **KL 正则化**：移除 KL 正则化反而提升性能，特别是显著降低 Failure Rate
- **采样长度**：1024 足矣，增至 2048 无额外收益
- **Group Size**：8→16 稳定训练，平衡计算成本采用 8
- **Think 模式**：Qwen2-VL 在 RL 后难以生成 `<think>` 标签，说明仅靠规则奖励不足以触发类似 CoT 的抽象推理

## 结论

- **首次**将 RL（GRPO）应用于 M-LLM 的端到端场景图生成任务
- 图中心奖励（Hard Recall）虽稀疏但与评估指标对齐，效果最佳
- SFT + RL 联合训练比只做其一更优：SFT 提供初始化，RL 精调结构正确性
- VG150 和 PSG 双基准上均超越传统 SGG 方法和已有 M-LLM 基线
- RL 几乎消除了输出格式错误（Failure Rate 骤降至 <1%）
- 局限性：跨域泛化受 SFT 过拟合限制；CoT 推理模式难以自动涌现
