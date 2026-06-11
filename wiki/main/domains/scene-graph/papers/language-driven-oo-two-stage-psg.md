---
title: "Language-Driven Object-Oriented Two-Stage Method for Scene Graph Anticipation"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - scene-graph-anticipation
  - scene-graph-generation
  - llm
  - language-driven-sgg
  - video-understanding
  - long-horizon-prediction
  - arxiv-2025
raw_sources:
  - ../../../sources/scene-graph/2025-arXiv-Language-Driven-OO-Two-Stage-PSG.pdf
  - ../../../sources/scene-graph/2025-arXiv-Language-Driven-OO-Two-Stage-PSG.txt
related_pages:
  - fdsg-forecasting-dynamic-scene-graphs.md
  - hyperglm-hypergraph-for-video-scene-graph-generation-and-anticipation.md
  - motion-aware-contrastive-learning-temporal-panoptic-sgg.md
evidence_level: full-paper
paper:
  title: "Language-Driven Object-Oriented Two-Stage Method for Scene Graph Anticipation"
  abbreviated: "OOTSM"
  authors:
    - Xiaomeng Zhu
    - Changwei Wang
    - Haozhe Wang
    - Xinyu Liu
    - Fangzhen Lin
  affiliations:
    - HKUST
    - Qilu University of Technology
    - Shandong Computer Science Center
  year: 2025
  venue: arXiv 2025
  doi: null
  arxiv: "2509.05661"
  code: "https://github.com/ZhuXMMM/OOTSM"
  url: null
classification:
  label: Language-Driven Scene Graph Anticipation
  task:
    - Scene Graph Anticipation (SGA)
    - Linguistic Scene Graph Anticipation (LSGA)
    - Object Forecasting
    - Relation Forecasting
  method_family:
    - LLM Fine-Tuning (LoRA)
    - Two-Stage Decoupling (GOA + OORA)
    - Cosine-Weighted Loss
    - Transition (Gated KL) Loss
    - Textual Scene Graph Representation
  modality: Multimodal (Video + Text)
  datasets:
    - Action Genome
  metrics:
    - Recall@K (R@K)
    - Mean Recall@K (mR@K)
---

# Language-Driven Object-Oriented Two-Stage Method for Scene Graph Anticipation (OOTSM)

## Citation

Xiaomeng Zhu, Changwei Wang, Haozhe Wang, Xinyu Liu, Fangzhen Lin. "Language-Driven Object-Oriented Two-Stage Method for Scene Graph Anticipation." arXiv:2509.05661, 2025.

## One-Sentence Contribution

提出 **OOTSM（Object-Oriented Two-Stage Method）**，将场景图预测（Scene Graph Anticipation, SGA）形式化为语言域时序推理问题，通过 LLM 的两阶段架构（GOA 预测未来对象集合 + OORA 预测对象关系轨迹）实现长程关系预测，在 Action Genome 上显著超越强视觉 SGA 基线。

## Problem Setting

现有 SGA 方法的不足：
- 几乎完全依赖视觉特征中的时空信息进行关系预测，难以融入语义先验和常识时序规律，尤其长期预测能力受限。
- 视觉感知与语义推理联合优化，使得注入/测量语义先验的作用变得困难。
- 现有方法未显式建模未来帧中新对象的出现和旧对象的消失，假设对象集合静止不变。

作者提出 **Linguistic Scene Graph Anticipation (LSGA)** 形式化定义：给定时序文本化的场景图序列，预测未来帧的场景图结构。核心思路是将视觉感知与语言推理解耦，建立多模态 SGA 框架。

## Method

### 整体框架：OOTSM

OOTSM 采用模块化两阶段设计：

1. **Stage 1: GOA（Global Object Anticipation）** — 全局对象预测
   - 根据观测帧的全局场景图序列，预测未来帧中可能出现/消失的对象类别集合
   - 使用 cosine-weighted CE loss，对远期 token 降权以减少噪声梯度
   - 单轮自回归生成

2. **Stage 2: OORA（Object-Oriented Relation Anticipation）** — 面向对象的关系预测
   - 对 GOA 预测的每个对象，分别生成其与场景中所有相关对象的时序关系演化
   - 使用 **transition loss（gated KL divergence）** 正则化相邻帧间关系分布的平滑性
   - 搭配 BCE 分类头预测帧级关系标签

### 关键设计要点

- 所有关系输出保持**无序多标签三元组**形式，适应 LLM 的离散类别输出特性
- LLM 后端使用 **LoRA**（rank=32, α=32）微调，A100 40GB 单卡
- 上下文窗口 2048 token，根据观测比例 F ∈ {0.3, 0.5, 0.7, 0.9} 动态调整输出长度
- 推理时使用 nucleus sampling（temperature=0.7, top-p=0.4）
- 三种微调 LLM 后端均优于 API baselines：**Llama-3.2-3B Instruct** > Qwen2.5-1.5B Instruct > DeepSeek-R1-1.5B

## Experiments

### 数据集

- **Action Genome (AG)**：标准 SGA 基准，包含 11.4K 视频，35 个对象类，25 个关系类（attention、spatial、contact）

### 评估协议

- **R@K** 和 **mR@K**（K ∈ {10, 20, 50}），With Constraint 设置
- 观测比例 F ∈ {0.3, 0.5, 0.7, 0.9}

### 实验设置

| 设置 | 描述 |
|------|------|
| **Text-based LSGA** | 使用 GT 场景图标注，纯文本推理（无视觉模块） |
| **Video-based SGA (GAGS)** | 使用 GT 对象和 bbox（Action Genome 标注），评估完整 SGA pipeline |
| **Ablation** | 验证 cosine-weighted loss、transition loss、temporal reasoning 有效性 |

### Baselines

- **Text-based**: GPT-4o, GPT-4o-mini, DeepSeek-V3（zero-shot/one-shot API）
- **Video-based**: STTran, DSGDet, SceneSayerODE, SceneSayerSDE

### 关键结果

#### Text-based LSGA（GT 场景图，w/ GOA 设置）

| 方法 | R@10 / mR@10 | R@20 / mR@20 | R@50 / mR@50 |
|------|-------------|-------------|-------------|
| GPT-4o-mini | 47.5 / 31.6 | 49.5 / 37.3 | 49.6 / 37.5 |
| GPT-4o | 60.6 / 43.3 | 63.9 / 52.5 | 64.0 / 52.8 |
| DeepSeek-V3 | 55.1 / 39.7 | 57.9 / 46.8 | 57.9 / 47.1 |
| **OOTSM (Llama-3.2-3B Instruct)** | **68.4 / 41.5** | **73.6 / 56.0** | **73.6 / 56.0** |
| OOTSM (Qwen2.5-1.5B Instruct) | 61.8 / 36.3 | 65.3 / 43.8 | 65.3 / 43.8 |
| OOTSM (DeepSeek-R1-1.5B) | 61.0 / 35.3 | 65.6 / 44.2 | 65.6 / 44.2 |

#### Video-based SGA（GAGS 设置，With Constraint）

**F = 0.9（最高观测比例，最易）**

| 方法 | R@10 / mR@10 | R@20 / mR@20 | R@50 / mR@50 |
|------|-------------|-------------|-------------|
| SceneSayerSDE | 60.3 / 28.5 | 61.9 / 29.8 | 61.9 / 29.8 |
| **OOTSM w/o GOA (Ours)** | 61.2 / 31.3 | **69.8 / 43.2** | 70.1 / 43.8 |
| **OOTSM w/ GOA (Ours)** | 60.6 / **31.9** | **73.2 / 48.1** | **74.2 / 51.7** |

**F = 0.3（最低观测比例，最难）**

| 方法 | R@10 / mR@10 | R@20 / mR@20 | R@50 / mR@50 |
|------|-------------|-------------|-------------|
| SceneSayerSDE | 39.7 / 18.4 | 42.2 / 20.5 | 42.3 / 20.5 |
| **OOTSM w/o GOA (Ours)** | 38.8 / **19.5** | **48.3 / 31.5** | **49.3 / 33.7** |
| OOTSM w/ GOA (Ours) | 39.0 / **19.7** | 47.8 / **31.5** | 48.4 / 32.3 |

#### 关键提升总结

- **F=0.9 时**：OOTSM w/ GOA 在 mR@20 比 SceneSayerSDE 提升 **18.3%**（48.1 vs 29.8），mR@50 提升 **21.9%**（51.7 vs 29.8）
- **F=0.5 时**：OOTSM w/ GOA 在 mR@20 从 23.0 → 33.8（+10.8），mR@50 从 23.1 → 35.9（+12.8）
- **纯文本 LSGA**：OOTSM (Llama-3.2-3B Instruct) 在 R@20=73.6 超过 GPT-4o 的 63.9（+9.7），mR@20=56.0 超过 GPT-4o 的 52.5（+3.5）
- **GOA 有效性**：在 Video-based SGA 中 GOA 模块将 mR@20 平均提升约 4-5%（如 F=0.9: mR@50 43.8→51.7）
- **余弦加权 + transition loss 复合效果**：mR@20 从 53.9→56.0（+2.1%）

### Ablation

| 加权 | Transition | R@10 / mR@10 | R@20 / mR@20 | R@50 / mR@50 |
|------|-----------|-------------|-------------|-------------|
| ✗ | ✗ | 67.5 / 41.3 | 72.6 / 53.9 | 72.6 / 53.9 |
| ✗ | ✓ | 68.1 / 41.4 | 73.3 / 54.9 | 73.3 / 54.9 |
| ✓ | ✗ | 67.9 / 42.0 | 73.3 / 55.6 | 73.3 / 55.6 |
| ✓ | ✓ | **68.4 / 41.5** | **73.6 / 56.0** | **73.6 / 56.0** |

- 余弦加权主要提升尾类召回（mR@20 +1.7%）
- Transition loss 主要稳定常见关系模式
- 两者互补，组合达到最佳平衡

## Conclusion & Implications

- OOTSM 验证了**语言驱动范式**在场景图预测任务上的有效性——紧凑的 3B 微调 LLM 即可超越 GPT-4o 等大型 API 模型
- **GOA 显式预测未来对象集合**的能力是关键差异点，使长程预测中尾类关系显著受益（mR@50 提升 21.9%）
- 语言界面天然支持**无序多标签输出**，避免了 SGG 中常见的 N² 全对组合问题
- 为未来多模态 SGA 提供了一个灵活的模块化框架，视觉和语言组件可独立升级

## Open Questions

- 是否可以端到端整合视觉模块消除模态转换开销？
- 开放词汇对象表示能否进一步解决长尾识别失败？
- 自适应时序约束能否更好平衡平滑性和合理突变？

## References

- Action Genome: Ji et al., CVPR 2020 [4]
- SceneSayer: Peddi et al., ECCV 2024 [8]
- LSGA: 本文首次提出 (Linguistic SGA)
- Code: https://github.com/ZhuXMMM/OOTSM
