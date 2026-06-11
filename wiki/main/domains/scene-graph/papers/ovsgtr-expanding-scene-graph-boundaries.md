---
title: "From Data to Modeling: Fully Open-Vocabulary Scene Graph Generation (OvSGTR)"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - scene-graph-generation
  - open-vocabulary-sgg
  - fully-open-vocabulary-sgg
  - ovd-sgg
  - ovr-sgg
  - ovdr-sgg
  - visual-concept-alignment
  - knowledge-distillation
  - relation-aware-pretraining
  - transformer
  - ECCV-2024
  - arXiv-2025
raw_sources:
  - ../../../sources/scene-graph/2024-ECCV-Expanding-Scene-Graph-Boundaries.pdf
  - ../../../sources/scene-graph/2024-ECCV-Expanding-Scene-Graph-Boundaries.txt
  - ../../../sources/scene-graph/2025-arXiv-FDtM-Fully-Open-Vocabulary-SGG.pdf
  - ../../../sources/scene-graph/2025-arXiv-FDtM-Fully-Open-Vocabulary-SGG.txt
related_pages:
  - language-supervised-open-vocabulary-scene-graph-vs3.md
  - cage-sgg-counterfactual-active-graph-evidence-open-vocabulary-sgg.md
evidence_level: full-paper
paper:
  title: "From Data to Modeling: Fully Open-Vocabulary Scene Graph Generation"
  abbreviated: "OvSGTR"
  authors:
    - Zuyao Chen
    - Jinlin Wu
    - Zhen Lei
    - Chang Wen Chen
  affiliations:
    - The Hong Kong Polytechnic University
    - Centre for Artificial Intelligence and Robotics, HKISI-CAS
    - Institute of Automation, Chinese Academy of Sciences
    - University of Chinese Academy of Sciences
  year: 2025
  venue: arXiv 2505.20106 (journal version, preceding ECCV 2024 as 2311.10988)
  arxiv: "2505.20106"
  code: https://github.com/gpt4vision/OvSGTR/
  url: https://arxiv.org/abs/2505.20106
  doi: null
classification:
  label: "Fully Open Vocabulary SGG"
  task:
    - Scene Graph Generation
    - Open Vocabulary Object Detection
    - Open Vocabulary Relation Recognition
  method_family:
    - DETR-like Transformer
    - Visual-Concept Alignment
    - Knowledge Distillation
    - Weakly-supervised Relation Pre-training
    - Scene Parser-based Pipeline
    - LLM-based Pipeline (GPT4SGG)
    - Multimodal LLM-based Pipeline (MegaSG)
  modality:
    - Image
    - Text
  datasets:
    - VG150
    - COCO Captions
    - Flickr30k
    - SBU Captions
    - GPT4SGG
    - MegaSG
  metrics:
    - Recall@K
    - Mean Recall@K
---

# OvSGTR: From Data to Modeling — Fully Open-Vocabulary Scene Graph Generation

> **版本说明**：本文最早以标题 *Expanding Scene Graph Boundaries: Fully Open Vocabulary Scene Graph Generation via Visual Concept Alignment and Retention* 发表于 ECCV 2024（arXiv 2311.10988）。2025 年 arXiv 更新版（2505.20106）更名为 *From Data to Modeling: Fully Open-Vocabulary Scene Graph Generation*，系统性地扩展了关系感知预训练管线（场景解析器/LLM/多模态 LLM 三种管线对比）和基于 MegaSG 的大规模预训练实验。本页涵盖两个版本的全部内容。

## 核心思想

系统性地将 SGG 从封闭集扩展到全开放词汇设置（同时覆盖节点和边的开放集识别），提出 **OvSGTR**（Open-vocabulary Scene Graph Transformers）统一框架。

核心贡献：
1. **SGG 场景四分类**：Closed-set SGG / OvD-SGG（开放词汇物体检测）/ OvR-SGG（开放词汇关系识别）/ OvD+R-SGG（全开放词汇，同时含未见物体和未见关系）
2. **视觉-概念对齐（Visual-Concept Alignment）**：利用图像-文本描述数据进行弱监督关系预训练，将视觉特征与文本概念空间对齐
3. **三种关系感知预训练管线**（2025 扩展）：场景解析器（Scene Parser）/ LLM（GPT4SGG）/ 多模态 LLM（Gemini→MegaSG），系统对比其零样本 SGG 效果
4. **视觉-概念保持与知识蒸馏（Visual-Concept Retention + Knowledge Distillation）**：在微调新数据集时保留预训练的语义空间，有效缓解关系类别的灾难性遗忘

## 问题设置

### SGG 四场景分类

| 场景 | 物体类别 | 关系类别 | 难度 | 已有工作 |
|------|---------|---------|------|---------|
| **Closed-set SGG** | 封闭集（全部可见） | 封闭集（全部可见） | ★ | IMP, MOTIFS, VCTREE, SGTR, VS³ 等 |
| **OvD-SGG** | 开放词汇（基类+新颖类） | 封闭集 | ★★ | VS³, SVRP |
| **OvR-SGG** | 封闭集 | 开放词汇（基类+新颖类） | ★★★ | 本文首次 |
| **OvD+R-SGG** | 开放词汇 | 开放词汇 | ★★★★ | 本文首次 |

标签集 C 拆分为互不相交的 base classes C_B 和 novel classes C_N。

### OvR-SGG 与 OvD+R-SGG 的挑战

- 缺少关系感知的预训练模型（相对于物体感知有 CLIP/GLIP）
- 训练时新颖关系被移除，模型需从 "background" 中区分新颖关系
- 关系标注数据稀缺且昂贵
- **灾难性遗忘**：在细粒度 SGG 数据上微调时，模型会遗忘从图像-描述数据中学到的关系语义

## 方法

### OvSGTR 整体架构

DETR-like 端到端 transformer 架构，冻结图像骨干（Swin-T/Swin-B）和文本编码器（BERT-base），仅微调 transformer 解码器和关系头：

1. **视觉编码器**：Swin Transformer（冻结 Grounding DINO 初始化），提取多尺度视觉特征
2. **文本编码器**：BERT（冻结），提取文本特征
3. **Transformer 解码器**：Deformable DETR 编码器-解码器，通过交叉注意力融合视觉和文本特征，输出 K 个预测节点的 hidden features
4. **关系头**：轻量级两层 MLP，拼接 subject 特征、object 特征和关系查询 embedding → `e_{si→oj} = f_θ([v_si, v_oj, r])`

### 视觉-概念对齐

**节点级对齐**：预测节点与 GT 节点做二分图匹配（标准 DETR 方式），最大化匹配对的视觉-文本相似度。

**边级对齐**：边特征与关系文本特征的相似度通过 sigmoid 二值交叉熵损失优化。

### 三种关系感知预训练管线（2025 扩展核心）

| 管线 | 数据来源 | 规模 | 标注方式 | 质量 |
|------|---------|------|---------|------|
| **场景解析器（Scene Parser）** | COCO Caption | ~104k 图像 | off-the-shelf 语言解析器 [33] 从 caption 提取三元组 | 较低：解析不准确、定位模糊、标注有偏 |
| **LLM 管线** | COCO Caption（GPT4SGG [27]） | ~113k 图像 | GPT-4 生成密集场景图 | 中：优于 parser 但缺乏定位 |
| **多模态 LLM 管线** | Gemini 1.5 Flash（MegaSG [43]） | ~644k 图像（从 1M 筛选） | Gemini 直接生成含位置信息的三元组 | 高：含 grounding 信息、密集型高 |

三种管线均仅提供弱监督伪标签（无人工标注关系框），用于关系感知预训练。

### 视觉-概念保持（知识蒸馏）

微调时冻结初始预训练模型作为 teacher，student 的边缘特征与 teacher 对同一负样本的特征尽可能接近 → L1 蒸馏损失 L_distill。总损失：L = L_bce + λ·L_distill，最佳 λ=0.1。

## 实验结果

### 实验设置

- **数据集**：VG150（150 个物体类别、50 个关系类别）
  - 训练 70%（~76,000 图像）、验证 5,000、测试 ~14,700（排除 Grounding DINO 预训练用过的图像）
- **零样本预训练评估数据**：
  - COCO Caption（104k，场景解析器）
  - GPT4SGG（113k，LLM 管线）
  - MegaSG（644k，多模态 LLM 管线，CLIP 相似度<0.9 筛选以避免信息泄露）
- **评估协议**：SGDET（SGGen），Recall@K（K=20/50/100）和 Mean Recall@K
- **实现**：Swin-T/Swin-B backbone，BERT-base text encoder，100 个 object queries，frozen backbone + text encoder
- **训练**：8×NVIDIA A100 GPU，AdamW 优化器

### 零样本关系感知预训练效果（2025 新增）

在 VG150 上评估不同预训练管线的零样本 SGG 性能（SGDet + PredCls）：

| 模型 | 预训练数据 | SGDet R@20/50/100 | PredCls R@20/50/100 |
|------|-----------|-------------------|--------------------|
| VS3 (Swin-T) | COCO Caption (104k) | 4.56/5.79/6.79 | 12.30/16.77/19.40 |
| VS3 (Swin-L) | COCO Caption (104k) | 4.82/6.20/7.48 | 12.54/17.28/19.89 |
| **OvSGTR (Swin-T)** | COCO Caption (104k) | **6.61/8.92/10.90** | **16.65/22.44/26.64** |
| **OvSGTR (Swin-B)** | COCO Caption (104k) | **6.85/9.33/11.47** | **16.82/22.79/27.04** |
| VS3 (Swin-T) | GPT4SGG (113k) | 4.92/6.32/7.22 | 13.90/17.06/18.60 |
| VS3 (Swin-L) | GPT4SGG (113k) | 5.07/7.40/9.50 | 14.53/18.72/20.73 |
| **OvSGTR (Swin-T)** | GPT4SGG (113k) | **7.35/9.66/11.14** | **21.03/24.43/25.98** |
| **OvSGTR (Swin-B)** | GPT4SGG (113k) | **7.65/10.10/11.73** | **21.13/24.78/26.25** |
| VS3 (Swin-T) | MegaSG (644k) | 5.56/8.19/10.17 | 23.81/29.64/32.18 |
| VS3 (Swin-L) | MegaSG (644k) | 9.74/14.80/18.80 | 31.88/38.77/41.76 |
| **OvSGTR (Swin-T)** | MegaSG (644k) | **9.94/13.92/17.17** | **37.12/44.10/47.09** |
| **OvSGTR (Swin-B)** | MegaSG (644k) | **10.36/14.61/18.13** | **39.04/45.86/48.54** |

> **关键发现**：MegaSG 多模态 LLM 管线带来最大增益。OvSGTR(Swin-B, MegaSG) 零样本 PredCls R@100 = 48.54，显著高于场景解析器（27.04）和 LLM 管线（26.25），验证了 grounding 信息的重要性。

### 全监督 Closed-set SGG（VG150 SGDET）

| 模型 | 主干 | 参数量（可训练/总） | R@20 | R@50 | R@100 | mR@20 | mR@50 | mR@100 | 推理时间 |
|------|------|--------|------|------|-------|-------|-------|-------|---------|
| VS³ | Swin-L | 124M/432M | 27.3 | 36.0 | 40.9 | 4.4 | 6.5 | 7.8 | 0.24s |
| **OvSGTR** | Swin-B | 41M/238M | 27.8 | 36.4 | 42.4 | 5.2 | 7.4 | 9.0 | 0.19s |
| **OvSGTR⋆ (MegaSG)** | Swin-B | 41M/238M | **28.6** | **37.6** | **43.4** | **5.8** | **8.3** | **10.2** | 0.19s |

> OvSGTR (41M 可训练参数) 以更轻量架构超越 VS³ (93M-124M 可训练参数)。MegaSG 预训练带来额外提升（R@100 42.4→43.4，mR@100 9.0→10.2）。

### OvD-SGG（开放词汇物体检测）

| 模型 | Base+Novel (Object) PredCls R@50/100 | Base+Novel SGDet R@50/100 | Novel (Object) SGDet R@50/100 |
|------|--------------------------------------|---------------------------|-------------------------------|
| VS³ (Swin-T) | 46.73/49.11 | 14.49/17.87 | 10.24/13.44 |
| **OvSGTR (Swin-B)** | 59.83/61.34 | **21.35/26.22** | **15.58/19.96** |
| **OvSGTR⋆ (Swin-B)** | **60.93/62.49** | 21.21/26.12 | 15.78/20.47 |

> Novel Object PredCls R@50: OvSGTR (59.01) vs VS³ (46.91) — 提升 **12.1 点** (25.7% relative)

### OvR-SGG（开放词汇关系识别）

15 个关系类别作为 novel（VG150 共 50 关系），训练仅含 base 关系标注（44,333 图像）。

| 模型 | Base+Novel (Relation) SGDet R@50/100 | Novel (Relation) SGDet R@50/100 |
|------|--------------------------------------|---------------------------------|
| VS³ (Swin-T) | 15.63/17.29 | 0.00/0.00 |
| OvSGTR (Swin-T, w/o distill) | 18.09/20.41 | 0.00/0.00 |
| **OvSGTR (Swin-T, w/ distill)** | 20.46/23.86 | **13.45/16.19** |
| **OvSGTR⋆ (Swin-T, MegaSG)** | **25.40/29.71** | **17.02/21.15** |
| **OvSGTR (Swin-B, w/ distill)** | 22.89/26.65 | **16.39/19.72** |

> **关键发现**：
> - 无蒸馏时新颖关系 SGDet R@50=0（灾难性遗忘）
> - 知识蒸馏使新颖关系跳升至 13.45 (Swin-T) / 16.39 (Swin-B)
> - MegaSG 预训练进一步提至 17.02 (Swin-T)，PredCls Novel R@50 达 12.23

### OvD+R-SGG（全开放词汇，最困难场景）

36,425 训练图像，同时去除 novel 物体和 novel 关系。

| 模型 | Joint Base+Novel R@50/100 | Novel (Object) R@50/100 | Novel (Relation) R@50/100 |
|------|---------------------------|-------------------------|--------------------------|
| VS³ (Swin-T) | 5.87/7.19 | 5.98/7.47 | 0.00/0.00 |
| OvSGTR (Swin-T, w/ distill) | 13.50/16.37 | 14.32/17.48 | 9.19/11.18 |
| **OvSGTR⋆ (Swin-T, MegaSG)** | 15.15/18.82 | 12.49/16.29 | **13.68/17.19** |
| **OvSGTR (Swin-B, w/ distill)** | 17.14/21.03 | **17.58/21.70** | 14.62/18.22 |
| **OvSGTR⋆ (Swin-B, MegaSG)** | **17.84/21.95** | 15.66/19.84 | **17.15/21.05** |

> OvSGTR(Swin-B, w/ distill) Joint R@50=17.14 超越 VS³(5.87) 近 **3 倍**；MegaSG 预训练进一步提升 Novel Relation 到 17.15（R@50）。

### 消融实验

**关系查询数量**：1 个关系查询效果最佳（R@50=39.48），多个查询增加优化负担。

**蒸馏系数 λ**：

| λ | Base+Novel R@50 (start→end) | Novel R@50 (start→end) |
|---|----------------------------|------------------------|
| 0 (无蒸馏) | 7.25 → 13.74 | 10.78 → **0.32** |
| **0.1** | **7.25 → 16.00** | **10.78 → 11.54** |
| 0.3 | 7.25 → 14.35 | 10.78 → 10.71 |
| 0.5 | 7.25 → 13.34 | 10.78 → 10.90 |

> λ=0 时 Novel R@50 从 10.78 骤降至 **0.32**（灾难性遗忘）；λ=0.1 时保持 11.54，同时 Base+Novel 从 13.74 提升至 **16.00**。

## 关键洞见

1. **一阶段 DETR 架构优于两阶段 R-CNN 方法**：OvSGTR 用简单 MLP 关系头超越复杂的消息传递机制，验证了 DETR-like 端到端框架在 SGG 中的优势
2. **关系灾难性遗忘是开放词汇 SGG 的核心问题**：无蒸馏时新颖关系性能从 10.78 趋近于 0；知识蒸馏有效保持预训练语义空间
3. **弱监督关系预训练有效**：通过文本解析器获取伪标签，即使使用轻量级 Grounding DINO-B 也超越了 GLIP-L 的 VS³
4. **全开放词汇 OvD+R-SGG 仍有巨大提升空间**：Joint R@100 仅 21.02（Swin-B），远低于封闭集 R@100=42.4，存在约 2 倍差距

## 关键洞见（2025 扩展版新增）

1. **预训练管线对比揭示 grounding 的重要性**：场景解析器（R@100=27.04）< GPT4SGG(26.25) << MegaSG(48.54)，多模态 LLM 提供带 grounding 信息的场景图是关键增益来源
2. **MegaSG 预训练显著提升各级 SGG 场景**：零样本 PredCls R@100 从 27.04→48.54（+21.5 点）；全监督 Closed-set R@100 从 42.4→43.4；OvR-SGG Novel SGDet R@50 从 13.45→17.02
3. **OvD+R-SGG 中 Novel Relation 仍是瓶颈**：即便使用 MegaSG+Swin-B，Joint Novel Relation R@100=21.05（SGDet），远低于 Novel Object R@50=15.66—关系识别比物体识别困难得多
4. **VL 模型（CLIP/GLIP/Grounding DINO）对开放集物体检测有效，但对关系识别不够**：需额外关系感知预训练弥补

## 局限

- 场景解析器准确率有限，影响预训练质量（已被 LLM 和多模态 LLM 管线超越）
- 多模态 LLM 管线依赖 Gemini，数据筛选后仅 644k 图像，仍有标注噪声
- 语言监督结果偏向简单谓词
- OvD+R-SGG Joint R@100=21.95，距封闭集 R@100=43.4 差距约 2 倍，全开放词汇 SGG 仍在早期

## 关联

- **直接前身**：[VS³](language-supervised-open-vocabulary-scene-graph-vs3.md)（CVPR 2023）首次实现语言监督+开放词汇 SGG，但仅支持 OvD-SGG；OvSGTR 扩展到全开放词汇
- **同期工作**：[CAGE-SGG](cage-sgg-counterfactual-active-graph-evidence-open-vocabulary-sgg.md)（2026）从另一角度（因果主动学习）解决开放词汇 SGG
- **基础模型**：Grounding DINO 提供 DETR-like 检测基线，GPT-4 / Gemini 提供 LLM 场景图标注能力
- **技术复用**：知识蒸馏策略首系统应用于 SGG 关系灾难性遗忘

## 开放问题

1. 能否用更强大的多模态 LLM（如 GPT-4V/Gemini Pro）生成更精确的场景图伪标签？
2. 结构化场景图表示是否有助于减轻 LLM 幻觉？
3. OvD+R-SGG 的 Joint R@100=21.95 距封闭集 43.4 差距约 2 倍，是否存在更有效的统一范式？
4. 预训练管线三大方案中，成本和质量的 Pareto 最优方案是什么？
