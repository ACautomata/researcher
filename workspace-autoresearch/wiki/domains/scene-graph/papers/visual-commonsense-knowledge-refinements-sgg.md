---
title: "Visual Commonsense Driven Knowledge Refinements for Scene Graph Generation"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - scene-graph-generation
  - commonsense-reasoning
  - knowledge-refinement
  - answer-set-programming
  - neuro-symbolic
  - panoptic-scene-graph
  - spatial-commonsense
  - functional-commonsense
  - rule-mining
  - zero-shot-recall
  - constraint-violation-rate
  - arXiv-2026
raw_sources:
  - ../../../raw/sources/2026-06-09-visual-commonsense-knowledge-refinements-sgg.pdf
  - ../../../raw/sources/2026-06-09-visual-commonsense-knowledge-refinements-sgg.txt
related_pages:
  - assured-autonomy-neuro-symbolic-perception-sgg.md
  - hiKer-sgg-hierarchical-knowledge-enhanced-robust-sgg.md
  - acc-interaction-centric-knowledge-infusion-sgg.md
  - cage-sgg-counterfactual-active-graph-evidence-open-vocabulary-sgg.md
  - aligng-context-conditioned-predicate-semantics-prototype-feedback.md
evidence_level: full-paper
paper:
  title: "Visual Commonsense Driven Knowledge Refinements for Scene Graph Generation"
  abbreviated: "Commonsense SGG Refinement"
  authors:
    - Maëlic Neau
    - Salim Baloch
    - Jakob Suchan
    - Zoe Falomir
    - Mehul Bhatt
  year: 2026
  venue: "arXiv (preprint)"
  arXiv: "2606.06369"
  code: null
  paper_url: "https://arxiv.org/abs/2606.06369"
  affiliation: "Umeå University / Constructor University Bremen / Örebro University / CoDesign Lab EU"
---

# Visual Commonsense Driven Knowledge Refinements for Scene Graph Generation

## 概述

本文提出一个**模型无关的、语义引导的知识精炼框架**，通过从训练数据中系统挖掘视觉常识约束（空间、功能、定性关系规律），在推理阶段使用**声明式常识推理（Answer Set Programming, ASP）** 修正和精炼 SGG 模型的排序预测。该方法无需手动规则编写、无需模型重训练，且可跨数据集和架构迁移。核心洞见：SGG 训练信号在长尾组合空间中极度稀疏，单纯靠端到端训练无法从单对梯度中恢复常识结构约束；常识规则作为后处理一致性层，是解决该问题的有效补充。

## 方法

### 核心架构

方法分为两个阶段：

**阶段一：离线常识规则挖掘**（Mining）
从训练标注中挖掘三类独立规则族，编译为数据集特定的 ASP 程序 Π_D：

1. **I. 几何空间分布（Spatial）**：对每个有序主体-客体对（携带谓词 p），计算：
   - **RCC5 拓扑关系**：DR（分离）、PO（部分交叠）、PP（真包含）、PPI（被包含）、EQ（相等）
   - **9 方向关系**：above, below, left, right 及其交集，same-center
   - **边界框统计**：面积比、纵横比、交集等
   - 使用 **KS 检验（α=0.05）** 检验条件分布 P(relation | s, o) 与无条件分布 P(relation) 是否有显著差异，过滤统计无意义规则
   - Verifier 步骤基于验证集评估，保留有正收益的规则（剪枝约 69.1% 的候选规则）

2. **II. 功能约束（Functional）**：谓词级别和三元组级别的功能基数约束，如 "riding" 通常主体为人、客体为马或自行车

3. **III. 关系规律（Relational）**：对称性（Symmetry）、逆关系（Inverse）、组合（Composition），从数据中自动挖掘

此外引入 **超类抽象（Super-class abstraction）**，将细粒度对象类泛化为 k=12 个粗粒度的超类，缓解标注稀疏性。

**阶段二：推理时 ASP 精炼**（Refinement）
- 神经 SGG 模型输出的排序预测 + 候选对的空间关系 → 翻译为 ASP facts
- ASP choice rules 根据置信度排名非确定性地选择候选关系赋值
- ASP integrity constraints 强制满足常识一致性条件
- 使用**溯因推理（Abductive Reasoning）** 选择全局一致的 refined scene graph

### 关键技术细节

- **规则挖掘统计检验**：KS 检验（α=0.05）判断条件分布与无条件分布差异的显著性
- **Verifier 剪枝**：在验证集上评估每条规则的边际贡献，保留 F1@K 正贡献的规则（τ=0.09 阈值下最优，允许小幅规则违反以应对标注噪声）
- **PSG 数据集规则规模**：104,671 条三元组级 + 1,169 条谓词级 + 9 条关系规则被挖掘；经过 Verifier 后保留 32,665 条（30.9%）
- **多规则协同**：约 42.8% 的改变对触发了 3+ 种规则类型，仅 25% 由单一规则驱动

## 实验与结果

### 基准与模型

- **数据集**：PSG (Panoptic Scene Graph), Visual Genome 150 (VG150), IndoorVG
- **模型**：Motifs (LSTM)、Transformer、**REACT++**（跨注意力+原型学习）
- **检测骨干**：统一使用 YOLOv12m
- **指标**：Recall@K (R@K)、meanRecall@K (mR@K)、F1@K（调和平均）、Recall@n（n=GT关系数）、零样本 Recall (zsR@K)、约束违反率 (CVR)

### 主要结果

| 数据集 | 规则配置 | F1@K | ΔF1@K | 重分配比例 |
|--------|---------|------|-------|-----------|
| **PSG** | Baseline | 29.59 | — | — |
| PSG | Base rules | 30.43 | +0.84 | 16.5% |
| PSG | Super-class rules | **30.74** | **+1.15** | 18.2% |
| **IndoorVG** | Baseline | 25.29 | — | — |
| IndoorVG | Base rules | 26.08 | +0.79 | 28.6% |
| IndoorVG | Super-class rules | **26.15** | **+0.86** | 29.6% |
| **VG150** | Baseline | 17.63 | — | — |
| VG150 | Base rules | 18.34 | +0.71 | 23.5% |
| VG150 | Super-class rules | **18.49** | **+0.87** | 26.7% |

### 跨模型泛化（PSG）

| 模型 | 规则配置 | F1@K | ΔF1@K |
|------|---------|------|-------|
| Motifs | Baseline | 17.83 | — |
| Motifs | Base rules | **18.18** | **+0.35** |
| Transformer | Baseline | 22.68 | — |
| Transformer | Base rules | **23.13** | **+0.45** |

### 零样本 Recall 与约束违反率降低

| 数据集 | 配置 | zsR@20 | zsR@50 | zsR@100 | CVR ↓ |
|--------|------|--------|--------|---------|-------|
| VG150 | Baseline | 0.85 | 1.58 | 2.37 | 12.44 |
| VG150 | Ours | 0.97 | 1.87 | 2.74 | **0.93** |
| IndoorVG | Baseline | 1.77 | 3.14 | 4.66 | 8.50 |
| IndoorVG | Ours | 1.98 | 3.55 | 4.79 | **0.67** |
| PSG | Baseline | 1.80 | 3.11 | 4.31 | 11.56 |
| PSG | Ours | 2.30 | 3.71 | 5.21 | **0.95** |

### 消融分析

- **规则类型归因**（PSG，REACT++，685 个 FP→TP 转换）：
  - BBox（边界框）规则贡献最大（34.5% FP→TP），其次是 RCC5（13.6%）和方向规则（3.5%）
  - 功能规则贡献 10.7%，关系规则（对称/逆/组合）无贡献（在 PSG 中未挖掘到有效规则）
- **阈值 τ 调优**：τ=0.09 最优，允许轻微规则违反以适应标注噪声
- **超类抽象增益**：相对提升 +0.07 至 +0.26 F1@K

## 分析与讨论

### 优势

1. **模型无关**：在 Motifs、Transformer、REACT++ 三种架构上均获得一致提升
2. **无需重训练**：推理时后处理，不改变原模型训练过程
3. **零样本能力**：zsR@100 在 PSG 上 +21%（4.31→5.21），可恢复训练中未见过的三元组组合
4. **CVR 大幅降低**：CVR 从 8.5-12.4% 降至 <1%
5. **ASP 推理可解释**：每条规则修改都可追溯到具体的 commonsense 约束
6. **超类抽象支持开放词汇**：新对象类若可映射到已有超类，则可直接应用

### 局限

1. **规则质量依赖标注质量**：噪声数据集（VG150、IndoorVG）的改善幅度低于高质量标注的 PSG
2. **Symmetry/Inverse 规则难以挖掘**：标注中天然缺少双向标注，导致关系规则贡献几乎为零
3. **推理开销**：ASP 推理在 CPU 上约需额外计算（文中报告在 PSG 上的运行时）
4. **仅处理谓词修正**：不做对象检测的修正，依赖上游检测器质量

## 关键结论

该工作证明：结构化视觉常识推理作为后处理一致性层，是纯数据驱动 SGG 的高效可行补充。规则挖掘+ASP 溯因推理的组合，在不改变模型架构和训练流程的情况下，可在三个基准、三种架构上获得一致的 F1@K 提升，同时大幅降低约束违反率并提升零样本泛化能力。

## 笔记与待验证

- 方法在更大规模数据集（如 OpenImages）上的扩展性待验证
- 超类数量 k=12 是否最优，是否可以自动化选择
- 规则挖掘中的 KS 检验 α=0.05 是否对噪声敏感
- ASP 推理能否扩展到视频 SGG（动态关系推理）
