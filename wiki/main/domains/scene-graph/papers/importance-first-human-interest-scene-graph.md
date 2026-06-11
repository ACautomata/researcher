---
title: "Importance First: Generating Scene Graph of Human Interest"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags: [sgg, human-interest, hierarchical, importance-ranking]
source_pages: []
raw_sources:
  - ../../../sources/scene-graph/2023-06-09-importance-first-generating-scene-graph-human-interest.pdf
  - ../../../sources/scene-graph/2023-06-09-importance-first-generating-scene-graph-human-interest.txt
paper:
  title: "Importance First: Generating Scene Graph of Human Interest"
  authors:
    - Wenbin Wang
    - Ruiping Wang
    - Shiguang Shan
    - Xilin Chen
  year: 2023
  venue: "International Journal of Computer Vision (IJCV)"
  volume: 131
  pages: "2489–2515"
  doi: "10.1007/s11263-023-01817-7"
  code: "https://github.com/Kenneth-Wong/TGIR"
  arxiv: null
classification:
  label: "Hierarchical SGG with Importance Ranking"
  task:
    - "Scene Graph Generation (SGG)"
    - "Visual Relationship Detection (VRD)"
    - "Image Captioning"
    - "Cross-Modal Retrieval"
    - "Image Generation"
  method_family: "Tree-Guided Message Passing"
  modality: visual
  datasets:
    - VRD
    - VG150 (Visual Genome)
    - VG200
    - VG-KR
  metrics:
    - Recall@K (R@K)
    - mean Recall@K (mR@K)
    - CIDEr (captioning)
evidence_level: full-paper
---

## Citation

Wenbin Wang, Ruiping Wang, Shiguang Shan, Xilin Chen. "Importance First: Generating Scene Graph of Human Interest." *International Journal of Computer Vision*, vol. 131, pp. 2489–2515, 2023. DOI: [10.1007/s11263-023-01817-7](https://doi.org/10.1007/s11263-023-01817-7). Code: [github.com/Kenneth-Wong/TGIR](https://github.com/Kenneth-Wong/TGIR).

## One-Sentence Contribution

提出 Tree-Guided Importance Ranking (TGIR) 模型，通过根据空间尺度构建的 Hierarchical Entity Tree (HET) 引导场景图生成，并引入 Relationship Ranking Module (RRM) 对关系进行重要性排序，首次将"人类兴趣优先"的感知层级结构融入场景图生成。

## Problem Setting

传统 SGG 将图像中所有对象和关系均等对待，生成扁平场景图。然而人类观察场景时存在天然的层级偏好——大物体优先、重要关系先被注意到。本文提出生成 **Scene Graph of Interest (SGoI)**，即按重要层级结构化的场景图：重要内容优先呈现，次要内容按需呈现。

## Method

### 整体框架 (TGIR)

TGIR 由三个核心模块组成：

1. **Hierarchical Entity Tree (HET)** — 层级实体树
   - 根据对象空间尺度（bounding box 大小）组织成多叉树结构
   - 大尺度对象位于高层（优先感知），小尺度对象位于低层
   - 不同层级的对象间存在从属（subordination）和并列（juxtaposition）关系
   - 树结构为启发式构建，不需额外学习

2. **Hierarchical Contextual Propagation (HCP)** — 层级上下文传播
   - **O-HCP**（Object-level HCP）：沿 HET 的拓扑结构传播对象级上下文信息
   - **R-HCP**（Relationship-level HCP）：沿 HET 结构传播关系级上下文
   - 两种变体实现：
     - **HCPL**：基于 Bi-LSTM 的序列传播
     - **HCP-B**：沿树结构的双向传播
     - **HCP-G**：基于 mGAT（modified Graph Attention Network）的图传播
   - TGIR-B 使用 Bi-LSTM 版 HCP，TGIR-G 使用 mGAT 版 HCP

3. **Relationship Ranking Module (RRM)** — 关系排序模块
   - 对所有关系进行重要性重新排序
   - 两种训练方案：
     - **D-Sup（Direct Supervision）**：使用关键关系标注直接监督训练
     - **A-Sup（Approximate Supervision）**：利用视觉显著性（visual saliency）和空间尺度（spatial scale）作为近似监督信号，无需人工标注关键关系

### 损失函数

- 基础分类损失 L_cls（标准交叉熵）
- 排序损失：用于 RRM 的 pairwise ranking loss
- 排序损失权重 λ 对 D-Sup 设为 1，对 A-Sup 设为 1000

## Experiments

### 数据集

| 数据集 | 训练/测试图像 | 对象类别 | 谓词类别 | 关键关系标注 |
|--------|-------------|---------|---------|------------|
| VRD | 4,000 / 1,000 | 100 | 70 | ❌ |
| VG150 | 75,651 / 32,422 | 150 | 50 | ❌ |
| VG200 | 32,510 / 14,052 | 200 | 80 | ❌ |
| VG-KR | 18,720 / 8,272 | 200 | 80 | ✅ (26,992 张含关键关系标注) |

VG200 和 VG-KR 为本文收集：选取同时属于 VG 和 MS-COCO 的 51,498 张图像，利用图像描述中的关系作为关键关系标注。

### 评估协议

- 三种标准协议：PREDCLS、SGCLS、SGGEN
- 指标：R@K 和 mR@K，K ∈ {20, 50, 100}
- 关键关系预测评估：PREDCLS 协议 + 三元组匹配（triplet-match）和二元组匹配（tuple-match）

### 训练设置

- Backbone：VGG16 / ResNet-101（Faster R-CNN 检测器）
- 场景图推理模块：Bi-LSTM（TGIR-B）或 mGAT（TGIR-G）
- 优化器：SGD（检测器） + Adam（推理模块）
- 学习率：检测器初始学习率 1e-2，推理模块 1e-3
- Batch size：not explicitly reported
- Epochs：not explicitly reported（提及随机采样 epoch）
- 硬件：not reported

### 消融实验

- HCP 变体对比（HCPL / HCP-B / HCP-G vs. Motif baseline）
- RRM 在不同 A-Sup 配置下的效果
- A-Sup 与 D-Sup 的对比
- 关键关系预测中不同监督方案的对比

## Results

### 消融实验 (Table 2, PREDCLS 协议)

**VG150 上消融结果 (R@20/50/100 / mR@20/50/100):**

| 模型 | R@20/50/100 | mR@20/50/100 |
|------|------------|-------------|
| Motif (Zellers et al., 2018) | 60.0 / 66.2 / 67.5 | 11.4 / 14.0 / 14.9 |
| HCPL | 58.4 / 64.6 / 66.7 | 10.9 / 13.4 / 14.2 |
| HCP-B | 60.1 / 66.3 / 67.6 | 11.7 / 14.3 / 15.1 |
| **HCP-G** | **60.2 / 66.4 / 67.7** | **12.7 / 16.1 / 17.2** |

HCP-G 在 VG150 上以 mGAT 得到最佳 mR@K（17.2 vs. Motif 14.9），表明层级结构有利于尾谓词的关系生成。

### 与 SOTA 对比 (Table 3, VG150)

**PREDCLS 协议下 TGIR 与 TYPE-I 方法对比:**

| 模型 | R@20/50/100 | mR@20/50/100 |
|------|------------|-------------|
| VCTree (Tang et al., 2019) | 60.1 / 66.4 / 68.1 | 14.0 / 17.9 / 19.4 |
| Seq2Seq (Lu et al., 2021) | 60.3 / 66.4 / 68.5 | 21.3 / 26.1 / 30.5 |
| TGIR-B | 60.1 / 66.3 / 67.6 | 11.7 / 14.3 / 15.1 |
| TGIR-G | ~60.2 / 66.4 / 67.7 | 12.7 / 16.1 / 17.2 |

在同等非核心模块条件下，TGIR 与 VCTree（二进制树）性能相当，但 TGIR 在 mR@K 上有改善。层级结构优于平层结构在上下文建模上的表现。

**SGCLS 协议下:**
- TGIR-B: R@20/50/100 = 35.2 / 38.2 / 38.8, mR@20/50/100 = 7.1 / 8.4 / 8.7
- TGIR-G: R@20/50/100 = 35.3 / 38.3 / 38.9, mR@20/50/100 = 7.6 / 9.2 / 9.7

**SGGEN 协议下:**
- TGIR-B: R@20/50/100 = 23.1 / 30.3 / 35.0, mR@20/50/100 = 4.2 / 5.5 / 6.4
- TGIR-G: R@20/50/100 = 21.3 / 29.1 / 34.8, mR@20/50/100 = 4.4 / 6.4 / 7.9

### 关键关系预测 (Table 5, VG-KR, PREDCLS 协议)

**三元组匹配 (triplet-match) R@5/10/20:**

| 模型 | R@5/10/20 | mR@5/10/20 | Tup.R@5/10/20 |
|------|----------|-----------|--------------|
| Motif+D-Sup | — | — | — |
| TGIR-B (D-Sup) | 35.8 / 42.9 / 48.0 | 8.2 / 10.5 / 12.1 | 65.9 / 80.1 / 90.6 |
| TGIR-G (D-Sup) | 36.3 / 43.5 / 49.2 | 7.1 / 9.0 / 11.0 | 64.9 / 78.7 / 90.1 |

TGIR 在二元组匹配（tuple-match）规则下相比基线高约 2%，表明 HET 提供的层级结构有助于关系重要性估计。

### 图像描述任务 (Tables 6-7, VG-KR)

**CIDEr 指标 (VG-KR, top-20 关系输入):**

| 模型 | CIDEr | R@10 |
|------|-------|------|
| TGIR-B (Freq) | 73.1 / 55.7 | — |
| TGIR-B | 74.9 / 58.4 | 8.2 / 6.9 |
| **TGIR-B (D-Sup)** | **75.0 / 58.2** | **16.6 / 15.7** |
| **TGIR-G (D-Sup)** | **81.7 / 77.2** | **18.6 / 16.9** |

D-Sup 方案在图像描述任务上显著优于基线，D-Sup 训练的 TGIR 在 top-20 关系输入时 CIDEr 达 81.7/77.2（TGIR-G）。

### 跨模态检索 (Table 8-9)

使用关键关系进行检索的性能好于使用全部关系，表明关键关系更具图像特异性，对下游任务更实用。

## Limitations

1. HET 的树结构启发式基于空间尺度，可能不适用于所有场景（如关系中对象尺度接近时的优先级判别）
2. 文中未在 VG200 上进行全量 SOTA 对比，仅用于关键关系评估
3. A-Sup 方案虽然不需标注，但排序损失权重 λ 需要手动调整（A-Sup 用 λ=1000 远大于 D-Sup 的 λ=1）
4. 视觉显著性和空间尺度作为近似监督的正向相关性统计依据不够充分
5. 未讨论 HET 结构对复杂场景（多物交错遮挡）的鲁棒性

## Reusable Claims

- **Claim**: 人类感知场景存在层级偏好，大尺度对象在场景图构建中应当优先处理。
  - **Evidence**: 论文全文，消融实验（HCP-G mR@K=17.2 vs Motif 14.9）。
  - **Scope**: SGG 任务，空间尺度作为层次代理。
  - **Confidence**: High

- **Claim**: 视觉显著性和空间尺度与关系重要性正相关，可用作近似监督信号。
  - **Evidence**: 论文 Sect.4.2.3，A-Sup 方案在关键关系预测中有效提升性能。
  - **Scope**: 依赖预计算显著性图（如 SalGAN）和对象检测器。
  - **Confidence**: Medium（未提供严格的相关性量化分析）

- **Claim**: 关键关系（含语义丰富动词如 throwing, brushing, sniffing 等）往往是长尾谓词，对下游任务贡献更大。
  - **Evidence**: 论文 Fig.10c 和 VG-KR 统计分析。
  - **Scope**: VG 数据集。
  - **Confidence**: High

## Connections

- **VCTree (Tang et al., CVPR 2019)**：也使用了树结构，但 VCTree 通过可学习的二元树构建，而本文 HET 是启发式的多叉树。TGIR 在 mR@K 上优于 VCTree。
- **Motif (Zellers et al., CVPR 2018)**：标准基线，平层 LSTM 架构。HCPL 与其结构最接近。
- **KERN (Chen et al., 2019)**：核传播方法，TGIR 使用更明确的层级结构。
- **Seq2Seq (Lu et al., 2021)**：强化学习方法，在 mR@K 上最强，但不是本文关注方向。
- **TDE (Tang et al., CVPR 2020)**：反事实去偏方法，TYPE-II 类别，本文与其对比。

## Open Questions

1. HET 如改为可学习的端到端层次结构构建而非启发式方法，性能能否进一步提升？
2. 视觉显著性和空间尺度之间的融合权重是否可以自动学习？
3. 如何将层级场景图结构[wiki 其他 SGG 页面]扩展到视频域（动态场景图）？
4. SGoI 在开放词汇设置下如何保持层级结构？

## Provenance

- **原始 PDF**: `raw/sources/2023-06-09-importance-first-generating-scene-graph-human-interest.pdf`（DOI 直接下载，4.9MB）
- **提取文本**: `raw/sources/2023-06-09-importance-first-generating-scene-graph-human-interest.txt`（105,576 chars）
- **入库时间**: 2026-06-09
- **证据等级**: full-paper（全文提取 + 精读分析）
- **注意**: 原始 inbound 路径 `/home/node/.openclaw/media/inbound/2023_IJCV_Importance_First_Generating_Scene_Graph_of_Human_I---2514383d-55e4-4c26-9db1-4ca6afebf8de.pdf` 包含的是一篇名为 "Optimal and H∞ Control of Stochastic Reaction Networks" 的不相关论文（arXiv:2111.14754），PDF 文件名与内容不匹配。已通过 Springer DOI 渠道重新下载正确版本。
