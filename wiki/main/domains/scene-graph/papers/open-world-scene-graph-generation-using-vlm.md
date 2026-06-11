---
title: "Open World Scene Graph Generation using Vision Language Models"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - scene-graph-generation
  - open-world
  - open-vocabulary
  - vision-language-models
  - zero-shot
  - training-free
  - llava
  - qwen
  - arxiv-2025
raw_sources:
  - ../../../sources/scene-graph/2025-06-09-Open_World_Scene_Graph_Generation_using_VLM.pdf
  - ../../../sources/scene-graph/2025-06-09-Open_World_Scene_Graph_Generation_using_VLM.txt
related_pages:
  - pixels-to-graphs-open-vocabulary-sgg-vlm.md
  - ovsgtr-expanding-scene-graph-boundaries.md
  - language-supervised-open-vocabulary-scene-graph-vs3.md
  - cage-sgg-counterfactual-active-graph-evidence-open-vocabulary-sgg.md
evidence_level: full-paper
paper:
  title: "Open World Scene Graph Generation using Vision Language Models"
  abbreviated: "OwSGG"
  authors:
    - Amartya Dutta
    - Kazi Sajeed Mehrab
    - Medha Sawhney
    - Abhilash Neog
    - Mridul Khurana
    - Sepideh Fatemi
    - Aanish Pradhan
    - M. Maruf
    - Ismini Lourentzou
    - Arka Daw
    - Anuj Karpatne
  affiliations:
    - Virginia Tech
    - Oak Ridge National Lab
    - University of Illinois Urbana-Champaign
  year: 2025
  venue: arXiv 2025
  doi: null
  arxiv: "2506.08189"
  code: null
  url: null
classification:
  keywords:
    - scene graph generation
    - open world SGG
    - vision language models
    - zero-shot
    - training-free
  tasks:
    - Scene Graph Generation (SGG)
    - Open Vocabulary Relationship Prediction (OVR)
    - Open Vocabulary Detection + Relation (OvD+R)
    - Open World SGG (OW)
  datasets:
    - Visual Genome (VG150)
    - Open Images V6 (OIV6)
    - Panoptic Scene Graph (PSG)
  models:
    - LLaVA-Next 7B
    - Qwen2-VL 7B
    - Qwen2-VL 72B
  backbones:
    - Grounding DINO (object detection)
    - SimCSE (semantic embedding)
    - Depth Anything (geometric refinement)
---

# Open World Scene Graph Generation using Vision Language Models (OwSGG)

**arXiv 2025** | [[2506.08189]](https://arxiv.org/abs/2506.08189) | Virginia Tech / Oak Ridge / UIUC

## 1. 核心贡献

OwSGG 是首个 **完全训练无关（training-free）**、**模型无关（model-agnostic）** 的开放世界场景图生成框架。核心思想：将 SGG 形式化为 **零样本结构化推理问题**，直接利用预训练 VLM 的固有知识来生成场景图，无需任何任务级微调或数据集特定训练。

**主要贡献：**

1. **OwSGG 框架**：端到端、训练无关、模型无关的 SGG pipeline，集成 VLM 多模态提示、嵌入对齐和轻量级 pair refinement
2. **开放世界评估协议**：首次形式化定义 **Open World (OW)** 设置——测试时同时面临未见对象和未见关系，提供零样本 SGG 的标准化基准
3. **全面评估**：在 VG150、OIV6、PSG 三个主流数据集上评估 LLaVA-Next 和 Qwen2-VL 系列模型，涵盖 Close Vocabulary、Zero-Shot、OVR、OvD+R、OW 五个设置
4. **发现**：VLMs 在无需任务训练的情况下，在开放世界设置下可匹配或超越训练过的基线模型

## 2. 方法论

OwSGG pipeline 包含五个步骤：

### 2.1 Entity Generation（实体生成）

直接提示 VLM 生成图像中存在的候选对象类别/实体。

### 2.2 Entity Mapping（实体映射）

将 VLM 生成的自由形式实体名称对齐到数据集预定义的对象类别：
- 使用 **SimCSE**（对比文本编码器）计算预测实体与数据集类别的语义相似度
- 保留 top-k 个相似度在 δ 邻域内的候选类别

### 2.3 Entity Detection（实体检测）

使用 **Grounding DINO** 定位已映射实体在图像中的具体实例及其边界框。

### 2.4 Pair Refinement（对候选对精炼）

结合 **几何过滤** 和 **语义过滤** 筛选有意义的候选对象对：
- 几何维度：2D IoU + 深度差异（Depth Anything）
- 语义维度：对象类别嵌入相似度（SimCSE）
- 综合公式：$S_{\text{pair}} = \alpha \cdot S_{\text{geo}} + (1 - \alpha) \cdot S_{\text{sem}}$
- 默认 α = 0.5，top_k = 25

### 2.5 场景图生成

对精炼后的候选对构造结构化提示，输入 VLM 进行关系预测，输出格式化为 subject-predicate-object 三元组。通过实体映射和同义词标准化实现与标准评估协议兼容。

## 3. 评估设置

### 任务定义

| 设置 | 对象 | 关系 | 描述 |
|------|------|------|------|
| **Close Vocabulary (CS)** | 已见 | 已见 | 完整三元组在训练中出现过 |
| **Zero-Shot (ZS)** | 已见 | 已见 | 三元组组合未见，但成分已见 |
| **Open Vocabulary Relations (OVR)** | 已见 | **未见** | 预测未见关系 |
| **Open Vocabulary Detection + Relations (OvD+R)** | **未见** OR **未见** | 至少一个未见 |
| **Open World (OW)** | **未见** | **未见** | 最严格：两者均未见 |

### 评估指标

- **Recall@K (R@K)**: top-K 预测中召回的真实关系比例
- **mean Recall@K (mR@K)**: 按谓词类别平均的召回率

### 数据集

- Visual Genome (VG150): 150 对象, 50 关系
- Open Images V6 (OIV6): 601 对象, 30 关系
- Panoptic Scene Graph (PSG): 133 对象, 56 关系

### Backbone VLMs

- LLaVA-Next 7B
- Qwen2-VL 7B
- Qwen2-VL 72B

## 4. 实验结果

### 4.1 Close Vocabulary / Zero-Shot SGG (Table 1)

**OIV6 PredCls (CloseVocab mR@100):**

| 方法 | mR@20/50/100 | R@20/50/100 |
|------|:---:|:---:|
| HEIRCOM [12] | – / – / – | – / 85.4 / – |
| OwSGG (LLaVA-next) | 59.92 / 66.82 / **70.24** | 59.88 / 66.81 / 70.22 |
| OwSGG (Qwen7b) | 56.91 / 67.59 / **73.51** | 56.88 / 67.6 / 73.47 |
| **OwSGG (Qwen72b)** | **71.54 / 79.83 / 83.76** | **71.56 / 79.86 / 83.78** |

> OwSGG Qwen72b 在 OIV6 PredCls 上 R@100 = **83.78**，超越 SGTR (59.9)、ReIDN (72.8)、GPS-Net (74.7) 等所有训练过的基线。

**OIV6 PredCls Zero-Shot R@100:** OwSGG Qwen72b = **47.14**（显著高于其他基线）

**VG150 PredCls (CloseVocab R@50):**
- IMP: 44.8, MOTIFS: 65.2, VCTree+HIERCOM: 69.8, CooK: 62.1
- OwSGG (LLaVA): 14.87, OwSGG (Qwen7b): 8.9, **OwSGG (Qwen72b): 13.44**
> 在复杂 VG 数据集上，训练无关方法仍远低于训练过的方法

**PSG SGDet (CloseVocab R@50):**
- PSGTR: 32.1, SGTR: 33.1, PGSG: 32.7
- **OwSGG (Qwen72b): 10.68**（零样本）

### 4.2 Open Vocabulary Relations (OVR) — Table 2

**PSG SGDet OVR R@100:**

| 方法 | R@50/100 |
|------|:---:|
| OvSGTR [3] | 13.45 / 16.19 |
| PGSG [22] | – / – |
| **OwSGG (Qwen72b)** | **10.42 / 13.54** |
| OwSGG (LLaVA) | 8.31 / 10.49 |

**PSG SGDet OVR mR@100:** **OwSGG (Qwen72b) = 13.35**（最高）

> OwSGG Qwen72b 在 PSG OVR 设置下超越所有基线（mR@100: 13.35 vs. PGSG 11.3, OvSGTR 未报告 PSG 结果）。

**VG150 PredCls OVR R@100:** OwSGG Qwen72b = **11.02**（接近 CaCao 9.7，超越其他训练方法）

### 4.3 Open World SGG (OW) — Table 3

**VG150 SGDet Open World (novel Object & Relation) R@100:**

| 方法 | R@50/100 |
|------|:---:|
| IMP [38] | 0.00 / 0.00 |
| MOTIFS [45] | 0.00 / 0.00 |
| VCTREE [32] | 0.00 / 0.00 |
| TDE [33] | 0.00 / 0.00 |
| OvSGTR (Swin-B) [3] | 5.97 / 10.06† |
| **OwSGG (Qwen72b)** | **1.61 / 2.41** |
| OwSGG (LLaVA) | 1.92 / 2.56 |

> 传统 SGG 方法在严格 OW 设置下完全失败（R@100 = 0.00）。OwSGG 在此设置下取得非零结果，OwSGG (LLaVA) R@100 = 2.56。OvSGTR 在开放词汇设置下训练过，因此仍更高（10.06）。OwSGG 是首个无需任务训练的 Open World 基准。

### 4.4 Ablation 结果

- α（几何 vs 语义过滤权重）= 0.5 附近 F1 最优
- top_k（保留候选对数）= 25 平衡召回与噪声
- **SimCSE** 对比 **SBERT**：SimCSE 在 PSG/OIV6 上带来约 **5%** 的召回增益
- 深度+语义组合过滤 >> 纯几何过滤（尤其在开放设置下）

## 5. 局限与未来方向

1. **级联误差**：依赖多个预训练组件（Grounding-DINO、SimCSE、Depth Anything），各环节误差可累积
2. **可扩展性**：构造文本提示对检测到的对象对进行 VLM 推理，受限于 VLM 上下文长度，O(n²) 配对数量随检测对象数增长
3. **VG 复杂场景性能有限**：在 Visual Genome 的复杂设置下与训练过的方法差距仍然显著
4. **Pair refinement 效率**：虽然已减轻计算负担，仍有进一步优化空间

## 6. Reusable Claims

1. **训练无关的开放世界 SGG 可行**：VLMs 在无需任务训练的条件下能够在严格 Open World 设置中生成非零的场景图关系预测，这是首次形式化且可量化的训练无关开放世界 SGG 基准。
2. **VLMs 在简单、结构化的数据集上表现最佳**：在 OIV6（仅 30 个关系类别）上 Qwen72B 超越所有训练过的模型（R@100 = 83.78）；在 PSG（56 类别）上竞争力强；在 VG150（50 类别，更复杂场景）上仍落后。
3. **模型大小与性能正相关**：Qwen2-VL 72B 全面优于 7B 变体，差距显著。
4. **语义+几何联合过滤 > 单一维度**：Pair refinement 的 α = 0.5 组合方案在开放设置下性能最优。
5. **SimCSE > SBERT**：对比监督的嵌入模型在语义对齐上表现约好 5% 召回率。
6. **传统 SGG 在严格 OW 设置下完全失效**：IMP/MOTIFS/VCTREE/TDE 在 novel Object & Relation 上 R@100 = 0.00。

## 7. Connections

- 与 **PGSG**[22]（2024 CVPR）同为 VLM-based SGG 方法，但 PGSG 包含任务级微调，OwSGG 完全训练无关
- 与 **OvSGTR**[3]（2024）同为开放词汇 SGG，OvSGTR 使用训练策略实现更高性能但依赖标注数据
- 与 **VS³**[48]（2023 CVPR）和 **RAHP**[27] 在 OVR/OvD+R 设置下有直接定量比较
- 扩展了 **Open Vocabulary SGG** 设定，引入了更严格的 **Open World** 定义（novel Object AND novel Relation）
- 与 **CaCao**[43]、**CooK**[14] 等开放词汇方法在 VG 上有定量对比

## Provenance

- **Evidence Level**: full-paper
- **Source**: arXiv 2506.08189, 22 pages
- **Extraction**: PyMuPDF, ~77K chars
- **Verification**: 文本完整，包含所有 4 张表格和评估细节
