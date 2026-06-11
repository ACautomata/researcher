---
title: "Scene Graph Generation with Role-Playing Large Language Models (SDSGG)"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - scene-graph-generation
  - open-vocabulary-sgg
  - large-language-models
  - role-playing-llm
  - multi-persona-collaboration
  - scene-specific-description
  - mutual-visual-adapter
  - NeurIPS-2024
raw_sources:
  - ../../../raw/sources/2024-12-01-Scene-Graph-Generation-Role-Playing-LLMs.pdf
  - ../../../raw/sources/2024-12-01-Scene-Graph-Generation-Role-Playing-LLMs.txt
related_pages:
  - cage-sgg-counterfactual-active-graph-evidence-open-vocabulary-sgg.md
  - language-supervised-open-vocabulary-scene-graph-vs3.md
evidence_level: full-paper
paper:
  title: "Scene Graph Generation with Role-Playing Large Language Models"
  abbreviated: "SDSGG"
  authors:
    - Guikun Chen
    - Jin Li
    - Wenguan Wang
  affiliations:
    - Zhejiang University
    - Changsha University of Science & Technology
  year: 2024
  venue: NeurIPS 2024
  doi: null
  arxiv: "2410.15364"
  code: https://github.com/guikunchen/SDSGG
  url: null
---

# SDSGG: Scene Graph Generation with Role-Playing Large Language Models

## 核心思想

现有开放词汇场景图生成（OVSGG）方法使用 CLIP 等视觉-语言模型，采用标准零样本流程——计算查询图像与各类别文本分类器的相似度。但这些文本分类器（category-level / part-level prompts）是**场景无关**（scene-agnostic）的，在不同上下文中保持不变，难以建模高方差的视觉关系。

本文提出 **SDSGG**（Scene-Specific Description based OVSGG），其核心洞察是：让 LLM 扮演不同角色（如生物学家、工程师等），从多个视角分析给定场景的判别性视觉特征，生成**场景特定的描述**（Scene-Specific Descriptions, SSDs），并自适应调整文本分类器的权重。

## 方法

### 三大模块

#### 1. 多角色协作（Multi-Persona Collaboration, MPC）— 文本部分

- 用 LLM（GPT-4）生成场景特定描述
- 让 LLM 扮演不同角色（如生物学家、工程师、艺术家），从不同视角讨论给定关系的判别性视觉特征
- 通过对话式 prompt 让多个角色分析 subject 和 object 的视觉特征，形成丰富多样的 SSDs
- 解决了单 prompt 生成的描述多样性不足、覆盖不全的问题

#### 2. 自归一化相似度计算（Self-normalized Similarity）— 重归一化

- 不同于以往将生成的描述简单视为同等重要的文本分类器
- 根据每个 SSD 与当前场景的相关性，**自适应调整**其影响力（renormalization）
- 场景相关（relevant）的描述获得更高权重，矛盾（contradictory）描述被抑制

#### 3. 互视觉适配器（Mutual Visual Adapter, MVA）— 视觉部分

- 轻量级可训练模块（lightweight trainable modules）
- 学习交互感知语义空间（interaction-aware semantic space）
- 用跨注意力（cross-attention）捕捉 subject 和 object 之间的复杂交互
- 包含 Directional Marker（DM）用于几何关系建模

### 总体架构

1. 用 LLM（MPC 策略）为每个关系类别生成 SSDs
2. 用 CLIP 文本编码器编码 SSDs，经自归一化处理后作为动态文本分类器
3. 用 CLIP 图像编码器提取图像特征
4. 通过 MVA 对 subject-object pair 视觉特征进行交互感知建模
5. 计算视觉-文本相似度进行分类

## 实验与结果

### 数据集与设置

- **数据集**：VG（Visual Genome）、GQA
- **分割**：base（70% 关系类别训练）/ novel（30% 关系类别推理时不可见）/ semantic（24 个语义关系类别）
- **评估指标**：Recall@K（R@K）和 Mean Recall@K（mR@K）
- **Baselines**：CLS（CLIP zero-shot）、Epic（ICCV 2023）、RECODE（NeurIPS 2023）

### 主要结果（VG 数据集）

| 分割 | 方法 | R@20 | R@50 | R@100 | mR@20 | mR@50 | mR@100 |
|------|------|------|------|-------|-------|-------|--------|
| **base** | CLS | 2.1 | 3.2 | 3.9 | 7.0 | 9.0 | 10.9 |
| | Epic | — | 22.6 | 27.2 | — | — | — |
| | **SDSGG** | **18.7** | **26.5** | **31.6** | **9.2** | **12.4** | **14.8** |
| **novel** | CLS | 13.2 | 18.1 | 22.2 | 11.5 | 17.9 | 23.8 |
| | Epic | — | 7.4 | 9.7 | — | — | — |
| | **SDSGG** | **18.4** | **25.4** | **29.6** | **17.1** | **25.2** | **31.2** |
| **semantic** | CLS | 7.2 | 10.9 | 13.2 | 9.4 | 14.0 | 17.6 |
| | RECODE⋆ | 10.6 | 18.3 | 25.0 | 10.7 | 18.7 | 27.8 |
| | **SDSGG** | **21.5** | **29.3** | **34.9** | **16.8** | **22.7** | **28.4** |

### 主要结果（GQA 数据集）

| 分割 | 方法 | R@20 | R@50 | R@100 | mR@20 | mR@50 | mR@100 |
|------|------|------|------|-------|-------|-------|--------|
| **base** | CLS | 4.2 | 6.4 | 7.9 | 8.9 | 13.2 | 15.3 |
| | **SDSGG** | **33.4** | **43.9** | **49.5** | **15.6** | **21.0** | **24.5** |
| **novel** | CLS | 21.3 | 28.3 | 32.1 | 16.6 | 27.0 | 29.4 |
| | **SDSGG** | **27.2** | **37.4** | **42.9** | **23.8** | **32.8** | **37.3** |

### 消融实验关键发现

- **MPC** w/o MPC 在 base split R@100 从 **31.6 降至 11.8**（↓63%），novel split 从 **30.0 降至 11.8**（↓61%），证实多角色协作的重要性
- **MVA + DM** 相比 baseline（MLP）在 base R@20/50/100 从 13.1/18.7/22.4 提升至 18.7/26.6/31.6

## 结论与贡献

1. **首次**将 LLM 角色扮演用于 OVSGG 的文本分类器生成，提出 MPC 策略产生场景特定描述
2. 提出自归一化相似度计算，动态调整每个 SSD 的影响力
3. 提出轻量级 MVA 模块，通过学习交互感知语义空间提升关系识别能力
4. 在 VG 和 GQA 上超越所有 SOTA 方法，尤其在 novel split 上提升显著（Epic 相比提升 18.0%/19.9% R@50/100）

## 局限与待办

- 不同角色选择的合理性及覆盖完整性未系统探讨（作者留作未来工作）
- 仅在 GPT-4 上实验，未探讨不同 LLM 规模的影响
- SSDs 生成依赖 LLM，存在计算开销
- 视觉部分 MVA 仍需一定量标注数据进行训练（弱监督，非 fully zero-shot）
