---
title: "HyperGLM: HyperGraph for Video Scene Graph Generation and Anticipation"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - video-scene-graph-generation
  - hypergraph
  - scene-graph-anticipation
  - multimodal-llm
  - relation-reasoning
  - cvpr-2025
  - video-question-answering
  - video-captioning
  - relation-reasoning
  - vsgr-dataset
raw_sources:
  - ../../../sources/scene-graph/2025-CVPR-HyperGLM-HyperGraph-for-Video-Scene-Graph-Generation.pdf
  - ../../../sources/scene-graph/2025-CVPR-HyperGLM-HyperGraph-for-Video-Scene-Graph-Generation.txt
  - ../../../raw/sources/2025-CVPR-HyperGLM-HyperGraph-for-Video-Scene-Graph-Generation.txt
related_pages:
  - salient-temporal-encoding-dynamic-sgg.md
  - motion-aware-contrastive-learning-temporal-panoptic-sgg.md
  - oed-one-stage-end-to-end-dynamic-scene-graph-generation.md
  - fdsg-forecasting-dynamic-scene-graphs.md
evidence_level: full-paper
paper:
  title: "HyperGLM: HyperGraph for Video Scene Graph Generation and Anticipation"
  abbreviated: "HyperGLM"
  authors:
    - Trong-Thuan Nguyen
    - Pha Nguyen
    - Jackson Cothren
    - Alper Yilmaz
    - Khoa Luu
  affiliations:
    - University of Arkansas
    - Ohio State University
  year: 2025
  venue: CVPR 2025
  doi: null
  arxiv: null
  code: null
  url: https://uark-cviu.github.io/projects/HyperGLM
classification:
  label: "Video Scene Graph Generation via HyperGraph and LLM"
  task:
    - Video Scene Graph Generation (VidSGG)
    - Scene Graph Anticipation (SGA)
    - Video Question Answering (VQA)
    - Video Captioning (VC)
    - Relation Reasoning (RR)
  method_family: HyperGraph + Multimodal LLM
  modality: Video
  datasets:
    - VSGR (proposed, 1.9M frames)
    - PVSG
    - Action Genome
  metrics:
    - Recall (R@K)
    - mean Recall (mR@K)
    - Accuracy
    - Precision
    - F1 Score
    - CIDEr
    - MENTOR
    - ROUGE-L
    - BLEU-4
---

# HyperGLM: HyperGraph for Video Scene Graph Generation and Anticipation

## Citation

Trong-Thuan Nguyen, Pha Nguyen, Jackson Cothren, Alper Yilmaz, Khoa Luu. "HyperGLM: HyperGraph for Video Scene Graph Generation and Anticipation." CVPR 2025.

## One-Sentence Contribution

提出基于超图（HyperGraph）与多模态 LLM 的 HyperGLM 框架，通过融合实体场景图（spatial）与过程图（procedural/causal temporal）构建统一超图并注入 LLM 进行视频场景图生成、预测和推理，同时发布大规模 VSGR 数据集（190 万帧，涵盖五类任务）。

## Problem Setting

传统视频场景图（VidSGG）方法受限于 pairwise 关系建模，难以捕获 multi-object 高阶关系和时间依赖。已有数据集仅支持 SGG 和 SGA 任务，缺乏 VQA、VC、RR 等推理任务标注。作者将问题形式化为：

- **SGG**：为每帧 t 生成场景图 G_t，最小化负对数似然
- **SGA**：基于已观测帧（≤t）预测未来帧 t+n 的场景图

其中场景图 G_t = (V_G, E_G)，V_G 包含物体特征、bbox 和类别，E_G 包含 pairwise 关系 r_{ij}。

## Method

### 核心架构（Fig. 3）

图像编码器（CLIP-ViT-L-336）→ MLP 投影器 → 时序聚合器 → 统一超图 → 语言模型（Mistral-7B-Instruct）

### 1. 过程图（Procedural Graph）构建

过程图 P = (V_P, E_P) 建模关系类别的时序因果演�变：
- V_P 为所有 distinct 关系类别 r^{ij}_t
- E_P 为关系间的因果转换边 (r_m, r_n)
- 转换概率 w(r_m, r_n) 通过观测频率计算（式 3）
- 自环去除后归一化（式 4）
- 预测下一帧关系：r^{ij}_{t+1} = argmax P(r_n | r^{ij}_t, v^{i,j})（式 5）

### 2. 统一超图（Unified HyperGraph）构建

H = (V_H, E_H)，其中：
- V_H 包含所有实体节点 v^i_t 和关系类别节点 V_P
- E_H 包含 pairwise 关系 E_{G_t}（空间）和时序转换边 E_P（因果演变）
- 超边（hyperedges）将多个节点连接，建模高阶关系

### 3. Random-walk 超图构建（Algorithm 1）

通过 N_w 次随机游走（交替节点→超边→节点），生成采样超边集合 E_sampled，近似子图匹配。最优超边数 60（N_w=60, N_l=7）。关键数学性质：置换等变性（permutation equivariance）和超边顺序不变性（invariance to hyperedge order）。

### 4. 超图注入 LLM

视频帧由 CLIP-ViT-L-336 → 2-layer MLP → Mistral-7B-Instruct。每帧编码为 10 tokens（1 CLS + 9 个 3×3 平均池化）。LoRA（rank=128, scaling=256）微调所有线性层，无需视觉-语言对齐预训练。

## Experiments

### 数据集
- **VSGR（本文提出）**：3,748 视频 / 1,841,243 帧，来源自 ASPIRe 和 AeroEye。涵盖第三方、自拍、无人机三种视角。支持 5 任务：SGG、SGA、VQA、VC、RR
  - 82,532 video-caption pairs（平均 893 chars/video）
  - 74,856 question-answer pairs（约 20 问/视频）
  - 61,120 relation reasoning tasks（约 16 task/视频）
- **PVSG**：153K 帧，仅用于 SGG
- **Action Genome**：234.3K 帧，仅用于 SGA

### 训练设置
- Backbone：CLIP-ViT-L-336 编码视频帧
- LLM：Mistral-7B-Instruct
- LoRA rank=128, scaling=256
- Batch size 128, 2 epochs, 4×GPU
- 训练约 6 小时

### 评估指标
- SGG/SGA：Recall (R@K) 和 mean Recall (mR@K)，K ∈ {10, 20, 50, 100}
- VQA/RR：Accuracy, Precision, Recall, F1
- VC：CIDEr, MENTOR, ROUGE-L, BLEU-4

### Baseline 方法
- SGG：Transformer [52], HIG [34], CYCLO [35], HyperGraph (ablation)
- SGA（VSGR）：STTran+ [5], DSGDetr+ [11], STTran++ [5], DSGDetr++ [11], SceneSayerODE [36], SceneSayerSDE [36]
- VQA：Video-ChatGPT [32], Video-LLaVA-7B [30], MovieChat [41], Chat-UniVi-7B [20]
- VC：MV-GPT [38], CoCap [40], UniVL+MELTR [24]
- RR：Video-LLaVA-7B, MA-LMM [14], LLaMA-VID-7B [29]

### 消融实验
1. **超边数量**：0–120 超边。最优 60 超边（R@20 最高）；过多超边引入冗余（Fig. 6）
2. **视频输入比例 F**：0.3 / 0.5 / 0.7。更多已观测帧提升性能（Table 2）
3. **HyperGraph vs HyperGLM**：注入 LLM 后持续优于纯超图

## Results

### SGG 任务（Table 3）

| 方法 | PVSG R@20 | PVSG R@50 | PVSG R@100 | VSGR R@20 | VSGR R@50 | VSGR R@100 |
|------|-----------|-----------|------------|-----------|-----------|------------|
| Transformer [52] | 4.0 / 1.8 | 4.4 / 1.9 | 4.9 / 2.0 | 25.7 / 6.3 | 34.5 / 6.5 | 43.5 / 7.0 |
| CYCLO [35] | 5.8 / 2.0 | 6.1 / 2.2 | 6.7 / 2.3 | 29.4 / 7.1 | 36.4 / 7.7 | 47.7 / 7.7 |
| HyperGraph (w/o LLM) | 6.5 / 2.2 | 7.0 / 2.4 | 7.5 / 2.6 | 31.6 / 7.8 | 38.8 / 8.3 | 50.3 / 8.5 |
| **HyperGLM (Ours)** | **7.5 / 2.8** | **8.1 / 3.7** | **8.5 / 3.9** | **35.8 / 9.2** | **42.3 / 10.1** | **54.7 / 10.4** |

→ VSGR 上 HyperGLM 的 R@20 = 35.8，超越 CYCLO 的 29.4 提升 6.4

### SGA 任务（Table 4，F=0.9）

| 方法 | Action Genome R@10 | Action Genome R@50 | VSGR R@10 | VSGR R@50 |
|------|--------------------|--------------------|-----------|-----------|
| SceneSayerSDE [36] | 37.3 / 20.8 | 61.6 / 46.8 | 27.5 / 16.0 | 58.2 / 40.0 |
| **HyperGLM (Ours)** | **38.8 / 22.3** | **65.2 / 48.6** | **30.2 / 18.1** | **59.3 / 43.4** |

→ Action Genome R@10 = 38.8，VSGR R@10 = 30.2

### VQA 任务（Table 5）

| 方法 | Accuracy | Precision | Recall | F1 |
|------|----------|-----------|--------|-----|
| Chat-UniVi-7B [20] | 44.3 | 45.6 | 43.2 | 44.4 |
| **HyperGLM (Ours)** | **45.4** | **47.2** | **44.3** | **45.7** |

### VC 任务（Table 6）

| 方法 | CIDEr | MENTOR | ROUGE-L | BLEU-4 |
|------|-------|--------|---------|--------|
| MV-GPT [38] | 57.1 | 37.5 | 62.5 | 47.2 |
| **HyperGLM (Ours)** | 54.5 | 30.7 | **64.9** | **48.8** |

→ ROUGE-L 64.9 超过 MV-GPT 的 62.5

### RR 任务（Table 7）

| 方法 | Accuracy | Precision | Recall | F1 |
|------|----------|-----------|--------|-----|
| LLaMA-VID-7B [29] | 44.1 | 45.2 | 43.5 | 44.3 |
| **HyperGLM (Ours)** | **47.2** | **48.4** | **46.5** | **47.4** |

### SGA 多输入比例（Table 2, F=0.7）

F=0.7 时，Action Genome R@10 = 35.7 / mR@10 = 19.5，VSGR R@10 = 25.1 / mR@10 = 13.5

### 消融：超图 vs 无 LLM（Table 3）

| 对比 | PVSG R@20 | VSGR R@20 |
|------|-----------|-----------|
| HyperGraph w/o LLM | 6.5 | 31.6 |
| HyperGLM (+ LLM) | 7.5 (+1.0) | 35.8 (+4.2) |

→ LLM 注入在 VSGR 上提升 +4.2 R@20，在 PVSG 上提升 +1.0 R@20

## Limitations

- 超图随对象增多而复杂化，关键关系可能被淹没
- 大量对象和交互时关系结构复杂化，场景解释清晰性下降（论文原文）
- 依赖预训练目标检测器 Faster R-CNN，检测误差会传播到场景图中

## Reusable Claims

1. **超图比 pairwise 图更适合视频场景图**：超边连接多个节点，自然建模 multi-object 交互和时序因果关系。HyperGLM 在 PVSG/VSGR SGG 任务上 R@20 7.5%/35.8%，超越 CYCLO (5.8%/29.4%)
2. **过程图（Procedural Graph）有效建模关系时序演化**：通过关系转换概率显式建模因果链，在 SGA 任务上达到 Action Genome R@10=38.8（vs SceneSayerSDE 37.3）
3. **将超图注入 LLM 进一步增强推理**：HyperGLM vs pure HyperGraph 在 VSGR SGG R@20 上 +4.2（35.8 vs 31.6），在 VQA/RR 上达到 45.4%/47.2% Accuracy
4. **VSGR 数据集是大规模多任务基准**：1.9M 帧、3 视角、5 任务，支持 LLM 在多模态视频场景理解上的综合评估

## Connections

- **CYCLO [35]** / **HIG [34]**：同组工作（第一作者相同），均为视频场景图方向。CYCLO 关注航拍视频的循环图建模，HIG 是层级交错图方法。HyperGLM 在它们基础上引入超图和 LLM
- **SceneSayer [36]**：SGA 最强的 baseline，使用 NeuralODE/SDE 建模连续时间动态。HyperGLM 用过程图显式建模离散时序转换，SGA 上超越 SceneSayerSDE
- **PVSG [52]**：Panoptic Video SGG 基准数据集。HyperGLM 在其上 R@20=7.5 超越 CYCLO 5.8
- **CAGE-SGG**：开放词汇 SGG 方向，HyperGLM 聚焦有监督 VidSGG。两者互补

## Open Questions

1. **超大规模场景的可扩展性**：论文指出超图在对象增多时关系可能被淹没，有无自适应剪枝或层级超图方案？
2. **VSGR 数据集 vs Action Genome 的差异**：VSGR 上各方法得分显著低于 Action Genome（如 HyperGLM R@10 30.2 vs 38.8），两者复杂性差异需进一步分析
3. **超图随机游走中超边数量选择的普适性**：最优 60 超边是否对数据集/场景规模鲁棒？
4. **是否可扩展到开放词汇设置？** 当前为封闭类别预测，与 CAGE-SGG 等 OV 方法结合潜力

## Provenance

- **原始 PDF**：`raw/sources/2025-CVPR-HyperGLM-HyperGraph-for-Video-Scene-Graph-Generation.pdf`
- **提取文本**：`raw/sources/2025-CVPR-HyperGLM-HyperGraph-for-Video-Scene-Graph-Generation.txt`
- **提取来源**：PyMuPDF，11 页，51,923 字符
- **证据等级**：full-paper — 全文提取，方法、实验、结果完整
