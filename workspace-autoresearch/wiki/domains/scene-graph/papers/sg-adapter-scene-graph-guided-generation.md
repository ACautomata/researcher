---
title: "Scene Graph Guided Generation: Enable Accurate Relations Generation in Text-to-Image Models via Textural Rectification (SG-Adapter)"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - scene-graph-guided-generation
  - sg-adapter
  - text-to-image
  - diffusion-models
  - relation-leakage
  - token-triplet-attention
  - iccv-2025
  - sgg-downstream
raw_sources:
  - ../../../raw/sources/2025-ICCV-SG-Adapter-scene-graph-guided-generation.pdf
  - ../../../raw/sources/2025-ICCV-SG-Adapter-scene-graph-guided-generation.txt
related_pages:
  - sg2im-scene-graph-to-image-generation.md
  - reversion-relation-inversion.md
evidence_level: full-paper
paper:
  title: "Scene Graph Guided Generation: Enable Accurate Relations Generation in Text-to-Image Models via Textural Rectification"
  authors:
    - Guibao Shen
    - Luozhou Wang
    - Jiantao Lin
    - Wenhang Ge
    - Chaozhe Zhang
    - Xin Tao
    - Di Zhang
    - Pengfei Wan
    - Guangyong Chen
    - Yijun Li
    - Ying-cong Chen
  year: 2025
  venue: ICCV 2025
  arxiv: null
  code: null
  project: null
classification:
  label: "Scene Graph Guided Text-to-Image Generation"
  task:
    - text-to-image-generation
    - relation-controlled-generation
    - scene-graph-to-image-generation
  method_family: adapter-based-diffusion-control
  modality: text-image
  datasets:
    - MultiRels
    - Flickr30k
  metrics:
    - SG-IoU
    - Entity-IoU
    - Relation-IoU
    - Relation Accuracy
    - Entity Accuracy
    - FID
    - Inception Score
---

## Citation

Guibao Shen, Luozhou Wang, Jiantao Lin, Wenhang Ge, Chaozhe Zhang, Xin Tao, Di Zhang, Pengfei Wan, Guangyong Chen, Yijun Li, Ying-cong Chen. "Scene Graph Guided Generation: Enable Accurate Relations Generation in Text-to-Image Models via Textural Rectification." ICCV 2025.

## One-Sentence Contribution

提出 SG-Adapter，利用场景图的结构化表示作为文本编码后处理模块，通过 Token-Triplet 注意力掩码纠正 CLIP 文本编码器中因因果注意力导致的"关系泄漏"问题，实现精确的多关系文生图控制。

## Problem Setting

- **输入**：文本描述（caption） + 场景图（从 caption 经 NLP parser 或 GPT-4 提取的关系三元组集合）
- **输出**：符合文本描述且所有实体-关系对应关系正确的图像
- **核心挑战**：CLIP 文本编码器的因果注意力掩码导致 token 间非语义的上下文混杂——当 caption 包含多个独立的主-谓-宾结构时，某个关系会错误地"泄漏"到不相关的实体上（如"a man holds a cake and a woman holds an apple"中，"holds a cake"可能错误地影响"a woman"的嵌入）
- **评估**：传统 FID/CLIP-Score 无法感知关系对应关系，需要专门的 relation-aware 度量

## Method

### 核心观察

CLIP 文本编码器的因果注意力掩码允许每个 token 关注所有之前出现的 token，这导致属于不同主-谓-宾三元组的 token 之间发生非语义的相互作用（关系泄漏）。直接替换 CLIP 的注意力掩码在推理时会导致分布外问题。

### SG-Adapter 架构

1. **场景图表示构建**：对 caption 中的每个三元组 T_k = (subject_k, relation_k, object_k)，分别用 CLIP 编码各元素并拼接/投影为统一的 triplet embedding e_k = l(concat(E_T(s_k), E_T(r_k), E_T(o_k)))，所有三元组 embedding 组成场景图表示 e ∈ ℝ^{K×D}。

2. **Token-Triplet 映射**：定义映射函数 ω(·) 将每个 token i 映射到其所属的三元组索引，建立 token-to-triplet 对应关系。

3. **交叉注意力 + SG Mask**：设计基于 transformer 的 adapter f(·)，包含一个交叉注意力层。以文本 embedding w 为 Q，场景图 embedding e 为 K/V，引入 Token-Triplet 注意力掩码 M^{sg}（仅允许 token 关注其对应的三元组 embedding），实现 w' = f(w, e, M^{sg})。

4. **集成方式**：SG-Adapter 作为 CLIP 编码器后的 plug-in 模块，与 Stable Diffusion 的 U-Net 协同训练，训练损失为标准扩散噪声预测损失 L_t。

### MultiRels 数据集

构建了一个 309 张图像的多关系场景图-图像配对数据集，包含：
- **ReVersion** 子集：99 张图像，单关系，10 种"难"关系（如 shake hands with, sit back to back）
- **Multi-Relations** 子集：210 张手工收集图像，每张 1-4 个（多为多个）显著关系，精心标注准确场景图

### GPT-4V 评估指标

提出三个基于 GPT-4V 的自动评估指标：
- **SG-IoU**：整体场景图三元组逐组 IoU
- **Entity-IoU**：实体集合 IoU
- **Relation-IoU**：关系集合 IoU

## Experiments

### 数据集与设置

- **训练**：MultiRels 数据集（309 张图像）
- **测试**：20 个测试场景，每个场景重组 MultiRels 中 2-3 个随机选择的关系
- **图像质量评估**：MS-COCO-Stuff 验证集 5000 张图像计算 FID
- **SG-to-Image 评估**：Flickr30k 数据集（NLP 提取场景图），随机采样 200 样本计算 GPT-4V 指标

### Baseline 方法（T2I 实验）

- Stable Diffusion (SD) — 原始模型
- Finetune CLIP — 直接微调 CLIP 文本编码器
- GLIGEN Adapter — 在 U-Net 中引入场景图 token
- LoRA Adapter — 低秩适配，无场景图信息
- SG-Adapter (Ours)

### Baseline 方法（SG2I 实验）

SG2IM, PasteGAN, SGDiff, SceneGenie, R3CD, ISGC, SG-Adapter (Ours)

### 消融实验

- 是否使用 SG Mask（Token-Triplet 注意力掩码）

## Results

### T2I 自动指标 + 人工评估 (Table 1)

| 方法 | SG-IoU ↑ | Entity-IoU ↑ | Relation-IoU ↑ | Rel Acc (Human) | Ent Acc (Human) | FID ↓ |
|------|----------|-------------|---------------|-----------------|-----------------|-------|
| Stable Diffusion | 0.157 | 0.673 | 0.526 | 5.38% | 5.48% | 25.0 |
| Finetune CLIP | 0.198 | 0.499 | 0.635 | 5.38% | 6.78% | 58.2 |
| GLIGEN Adapter | 0.141 | 0.689 | 0.546 | 5.72% | 5.58% | 27.4 |
| LoRA Adapter | 0.145 | 0.653 | 0.540 | 5.96% | 5.05% | 27.5 |
| **SG-Adapter** | **0.623** | **0.812** | **0.753** | **77.6%** | **77.1%** | **26.2** |

**SG-Adapter 在 SG-IoU 上比 SD 提升约 4 倍（0.623 vs 0.157），Relation Accuracy 从 5.38% 提升至 77.6%。** 所有 baseline 虽然生成了正确的实体和关系，但无法将其正确对应分配（高 Entity-IoU/Relation-IoU 但极低 SG-IoU）。

### 消融实验 (Table 2)

| 方法 | SG-IoU ↑ | Entity-IoU ↑ | Relation-IoU ↑ | FID ↓ |
|------|----------|-------------|---------------|-------|
| w/o SG Mask | 0.316 | 0.742 | 0.668 | 26.7 |
| **SG-Adapter (with SG Mask)** | **0.623** | **0.812** | **0.753** | **26.1** |

**SG Mask 带来 SG-IoU 近 2 倍提升（0.316 → 0.623）**，验证了 token-triplet 精确对应机制的核心作用。

### SG-to-Image 对比 (Table 3, Flickr30k)

| 方法 | FID ↓ | Inception Score ↑ | SG-IoU ↑ | Entity-IoU ↑ | Relation-IoU ↑ |
|------|-------|-------------------|----------|-------------|---------------|
| SG2IM | 99.1 | 8.20 | 0.085 | 0.297 | 0.253 |
| PasteGAN | 79.1 | 12.3 | 0.091 | 0.382 | 0.297 |
| SGDiff | 36.2 | 17.8 | 0.122 | 0.436 | 0.394 |
| **SG-Adapter** | **25.1** | **57.8** | **0.413** | **0.729** | **0.681** |

在 SG-to-Image 任务上，SG-Adapter 的 FID 25.1 显著优于 SGDiff 36.2，SG-IoU 0.413 vs. SGDiff 0.122，展示了 adapter 策略利用预训练 T2I 模型高保真生成能力的优势。

## Limitations

- MultiRels 数据集因隐私原因对人脸进行了匿名化处理，可能引入伪影
- 数据集规模较小（309 张图像），泛化性受限于此
- GPT-4V-based 评估在大规模验证集上 API 调用成本过高

## Reusable Claims

- **Claim 1**: CLIP 文本编码器中的因果注意力掩码是关系泄漏（relation leakage）的根本原因——允许不同语义三元组的 token 相互干扰
- **Claim 2**: 直接替换 CLIP 注意力掩码会引发分布外问题，在编码后通过 adapter 修正是更可行的方案
- **Claim 3**: 场景图引导的文生图需专门的 relation-aware 评估指标（如 SG-IoU），传统 FID/CLIP-Score 无法感知关系对应关系
- **Claim 4**: 在 SG→Image 任务上，adapter 范式（利用预训练 T2I 模型）比端到端训练范式（SG2IM、SGDiff）在图像质量上显著占优

## Connections

- SGG 下游应用方向：该论文展示场景图作为结构化先验在生成任务中的价值，与 SGG 上游方法（如 PE-Net、SQUAT、VS³）形成完整闭环——SGG 提取场景图 → SG-Adapter 利用场景图引导生成
- 与 **ReVersion** 方法的关系：SG-Adapter 也具备学习新复杂单关系的能力作为副产品
- 与 **GLIGEN** / **ControlNet** 等 adapter 方法的关系：SG-Adapter 作用于文本编码端而非 U-Net，是更轻量的干预方式
- 与 **Structured Diffusion Guidance** (Feng et al., 2022) 的关系：该工作利用语言学结构指导扩散但未彻底解决根因（因果注意力），SG-Adapter 通过专门设计的 adapter 进行根本性修复

## Open Questions

- 更大规模的多关系场景图数据集是否进一步提升 relation correctness？
- SG-Adapter 能否泛化到超出 MultiRels 中出现的视觉概念？
- 是否可能在不需要 GPT-4V 提取场景图的情况下，让模型端到端学习 token-triplet 对应关系？
- 该 adapter 范式是否适用于视频生成中更复杂的时空关系控制？

## Provenance

- **raw_sources**: raw/sources/2025-ICCV-SG-Adapter-scene-graph-guided-generation.pdf (5.2 MB, 10 pages)
- **提取文本**: raw/sources/2025-ICCV-SG-Adapter-scene-graph-guided-generation.txt (41749 字符)
- **提取方法**: pymupdf
- **证据等级**: full-paper — 全文精读，提取了完整的 Method、Experiments、Results 章节
- **审查日期**: 2026-06-09
