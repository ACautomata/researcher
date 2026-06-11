---
title: "Pair then Relation: Pair-Net for Panoptic Scene Graph Generation"
type: paper
domain: scene-graph
status: active
created: 2026-06-10
updated: 2026-06-10
tags:
  - scene-graph-generation
  - panoptic-scene-graph
  - ICCV-2023
  - pair-proposal-network
  - query-based
  - transformer
source_pages: []
raw_sources:
  - raw/sources/2023-07-PairNet-Panoptic-Scene-Graph-Generation.pdf
  - raw/sources/2023-07-PairNet-Panoptic-Scene-Graph-Generation.txt
related_pages:
  - papers/psgformer-panoptic-scene-graph.md
  - papers/sgtr-end-to-end-scene-graph-generation-with-transformer.md
  - papers/hilo-exploiting-high-low-frequency-for-unbiased-panoptic-scene-graph-generation.md
  - papers/adtrans-adaptive-data-transfer-panoptic-scene-graph-debiasing.md
  - papers/dsflash-comprehensive-panoptic-scene-graph-generation-realtime.md
paper:
  title: "Pair then Relation: Pair-Net for Panoptic Scene Graph Generation"
  authors:
    - Jinghao Wang
    - Zhengyu Wen
    - Xiangtai Li
    - Zujin Guo
    - Jingkang Yang
    - Ziwei Liu
  year: 2023
  venue: ICCV 2023 (also TPAMI extension)
  arxiv: "2307.08699"
  code: "https://github.com/king159/Pair-Net"
classification:
  label: Pair-Net
  task:
    - Panoptic Scene Graph Generation (PSG)
    - Scene Graph Generation (SGG)
  method_family:
    - Query-based Transformer
    - Pair-Proposal Network (PPN)
    - Two-stage Pair-then-Relation
  modality:
    - Image
  datasets:
    - PSG Dataset (COCO-filtered + VG)
    - VG-150
  metrics:
    - R@K (Recall at K=20/50/100)
    - mR@K (Mean Recall at K=20/50/100)
    - TT-R@K / TS-R@K / ST-R@K / SS-R@K (categorical recall)
    - Pair Recall@K
    - PQ (Panoptic Quality)
evidence_level: full-paper
---

# Pair then Relation: Pair-Net for Panoptic Scene Graph Generation

## Citation

Jinghao Wang, Zhengyu Wen, Xiangtai Li, Zujin Guo, Jingkang Yang, Ziwei Liu. "Pair then Relation: Pair-Net for Panoptic Scene Graph Generation." ICCV 2023. arXiv:2307.08699.

## One-Sentence Contribution

提出 Pair-Net，通过显式解耦 subject-object 配对和关系分类两个步骤（Pair-then-Relation），并使用 Pair Proposal Network (PPN) + Matrix Learner 学习稀疏成对关系，在 PSG 任务上实现大幅提升（mR@20 绝对提升 10.2%，R@20 绝对提升 11.6%）。

## Problem Setting

### PSG 任务定义
Panoptic Scene Graph (PSG) 是场景图生成 (SGG) 的进阶任务，要求模型同时输出 panoptic segmentation mask 和场景图三元组。与基于 bounding box 的传统 SGG 不同，PSG 额外考虑了背景 stuff 的关系。

建模为：p(S|I) = p(M, A|I) p(R|M, A, I)，其中 M 为 panoptic segmentation masks，A 为类别标签，R 为关系标签。

### 关键挑战
1. **像素级分割输出**：需要同时输出高质量分割 mask 和关系预测
2. **全关系探索**：不仅包括 thing-to-thing，还包括 stuff-to-stuff、thing-to-stuff、stuff-to-thing 关系
3. **性能瓶颈**：现有 PSG 方法平均召回率仅约 10%

## Motivation / 瓶颈分析

论文首先对 PSG 性能瓶颈进行了系统分析：

1. **分割器质量已足够**：使用 COCO 预训练的 Mask2Former 在单独物体上达到了 sub-IoU=0.79, obj-IoU=0.78, sub-Recall0.5=0.91, obj-Recall0.5=0.90（Table 1），表明分割质量已足够支撑后续配对和关系生成。

2. **Pair Recall 是关键**：不同方法在 PQ 相近的情况下，Triplet Recall 差异显著（Table 2）。Pair Recall 与 Triplet Recall 呈强正相关，且 Pair Recall 远未饱和。

3. **成对关系的稀疏性**：PSG 数据集中每张图像平均仅 5.6 个关系三元组，在全连接设定下（Nobj=100），只有约 5-6/10000 的位置为正，稀疏性极强。

## Method

### 整体架构

Pair-Net 由三个模块组成：

#### (a) Panoptic Segmentation Network
- 使用 Mask2Former 作为分割器
- 输入图像 → 输出 panoptic segmentation mask 和 object queries Qobj ∈ R^{Nobj×d}（Nobj=100, d=256）
- 损失：L_mask = λ_cls L_cls + λ_ce L_ce + λ_dice L_dice

#### (b) Pair Proposal Network (PPN) — 核心创新

PPN 旨在从 Nobj 个 object queries 中筛选出有意义的 subject-object 配对。

**三子组件**：
1. **Subject/Object Projectors**：两个独立的 MLP（3 层 FC，d=256，ReLU），将 Qobj 分别映射为 subject embedding E_sub 和 object embedding E_obj
2. **Cosine Similarity**：计算 E_sub 和 E_obj 间的余弦相似度，得到粗配对矩阵 M_rough ∈ R^{Nobj×Nobj}
3. **Matrix Learner**：对 M_rough 进行进一步过滤的轻量网络

**Matrix Learner**（关键设计）：
- 3 层 CNN，inner channel=64，kernel size=7×7，0.2M 参数
- 相比 MLP/Transformer 表现更好，CNN 能保留局部细节并过滤冗余噪声
- 输出稀疏的过滤后配对矩阵 M_filtered

**Top-K Selection**：从 M_filtered 中选择 Top-K 索引，对应选取 subject query Q_s 和 object query Q_o

**监督**：通过 Hungarian Matching 构建 ground truth 配对矩阵 M_gt ∈ {0,1}^{Nobj×Nobj}，使用正权重调整的 BCE Loss：
L_ppn = -[p·y·log σ(x) + (1-y)·log(1-σ(x))] / N_obj²
其中 p = 正位置数 / N_obj² 的倒数（动态正权重）

#### (c) Relation Fusion
- 将选中的 Q_s 和 Q_o 沿长度维度拼接为 Q_pair ∈ R^{2Nrel×d}
- 随机初始化可训练的 relation queries Q_r ∈ R^{Nrel×d}
- 6 层 DETR-style transformer decoder（self-attention + cross-attention）
- cross-attention 中第 i 个 relation query 主要关注 Q_pair 中的第 i 个 subject query 和第 i 个 object query
- 使用 Seesaw Loss 处理关系分类的长尾分布

### 损失函数
总损失 = λ_sub L_sub + λ_obj L_obj + λ_rel L_rel + λ_ppn L_ppn + λ_original L_Mask2Former
默认权重：λ_o=λ_s=4, λ_r=2, λ_ppn=5, λ_original=1

### 与之前方法的对比

| 特征 | PSGTR | PSGFormer | SGTR | **Pair-Net** |
|------|-------|-----------|------|-------------|
| SGG | ✓ | ✓ | ✓ | ✓ |
| PSG | ✓ | ✓ | ✗ | ✓ |
| End-to-end | ✓ | ✗ | ✓ | ✓ |
| 稀疏性建模 | ✗ | ✗ | ✗ | ✓ |
| Pair Loss | ✗ | ✗ | ✗ | ✓ |
| 背景关系 | ✓ | ✓ | ✗ | ✓ |

## Experiments

### 数据集
- **PSG Dataset**：从 COCO + VG 筛选，133 个 object classes（thing + stuff），56 个 relation classes，46k 训练 / 2k 测试
- **VG-150**：150 个 object classes，50 个 relation classes，62k 训练 / 26k 测试

### 评估指标
- **R@K / mR@K**（K=20/50/100）：标准 SGG 指标
- **TT/TS/ST/SS Recall@20**：按 thing/stuff 类别分组
- **Pair Recall@K**：不考虑关系正确性的配对召回

### 实现细节
- **Backbone**：ResNet-50（默认）、Swin-B（大模型消融）
- **Optimizer**：AdamW，lr=1e-4，weight decay=1e-4，batch size=8
- **Schedule**：12 epochs，lr 衰减 0.1× at epoch 5 和 10（PSGTR 需要 60 epochs）
- **Nobj**=100, **Nrel**=100, **d**=256
- **Subject/Object Projectors**：3 层 MLP，d=256，ReLU
- **Matrix Learner**：3 层 CNN，channel=64, kernel=7×7
- **Relation Fusion**：6 层 DETR-style decoder

## Results

### 主要结果（PSG Validation Set）

| Method | Backbone/Detector | mR@20 | mR@50 | mR@100 | R@20 | R@50 | R@100 |
|--------|-------------------|-------|-------|--------|------|------|-------|
| IMP | Faster R-CNN | 6.5 | 7.1 | 7.2 | 16.5 | 18.2 | 18.6 |
| MOTIFS | Faster R-CNN | 9.1 | 9.6 | 9.7 | 20.0 | 21.7 | 22.0 |
| VCTree | Faster R-CNN | 9.7 | 10.2 | 10.2 | 20.6 | 22.1 | 22.5 |
| GPS-Net | Faster R-CNN | 7.0 | 7.5 | 7.7 | 17.8 | 19.6 | 20.1 |
| PSGFormer | DETR | 14.5 | 17.4 | 18.7 | 18.0 | 19.6 | 20.1 |
| PSGTR | DETR | 16.6 | 20.8 | 22.1 | 28.4 | 34.4 | 36.3 |
| PSGFormer+ | Mask2Former | 16.6 | 19.4 | 20.3 | 18.9 | 21.5 | 22.4 |
| PSGTR+ | Mask2Former | 20.9 | 27.4 | 28.4 | 32.6 | 38.0 | 38.9 |
| HiLo | Mask2Former | 23.7 | 30.3 | 33.1 | 34.1 | 40.7 | 43.0 |
| **Pair-Net (Ours)** | **Mask2Former (RN50)** | **24.7** | **28.5** | **30.6** | **29.6** | **35.6** | **39.6** |
| **Pair-Net† (Ours)** | **Mask2Former (Swin-B)** | **25.4** | **28.2** | **29.7** | **33.3** | **39.3** | **42.4** |

**关键数值对比**：
- 相比 PSGFormer：mR@20 **+10.2** (14.5→24.7), R@20 **+11.6** (18.0→29.6)
- 相比 PSGFormer+：mR@20 **+8.1** (16.6→24.7), R@20 **+10.7** (18.9→29.6)
- 相比 HiLo：mR@20 **+1.0** (23.7→24.7)，但 R@20 低 4.5

### Categorical Recall@20

| Method | TT-R@20 | TS-R@20 | ST-R@20 | SS-R@20 |
|--------|---------|---------|---------|---------|
| PSGFormer | 17.2 | 21.7 | 14.9 | 14.7 |
| PSGFormer+ | 19.5 | 21.5 | 9.5 | 18.5 |
| **Pair-Net** | **25.7** | **31.5** | **24.2** | **34.2** |

- SS-R@20 从 18.5 提升至 34.2（**+15.7**），证明 Pair-Net 有效捕捉了 stuff-stuff 关系
- ST-R@20 从 9.5 提升至 24.2（**+14.7**），改善最大

### Pair Recall@20
- **Pair-Net: 52.7** vs PSGFormer+: 28.6（**+24.1**）
- 直接验证了 PPN 对配对质量的提升

### VG-150 结果
Pair-Net-Bbox（Deformable DETR detector, ResNet-101）：
- mR@20: 8.9, R@20: 18.8（与 SGTR 可比：8.9 / 18.8）

### 稳定性
5 次不同种子实验，mR@20 稳定性 ±0.2。

## Ablation Studies

### PPN 各组件必要性（Table 6a）

| Linear Embed | Matrix Learner | BCE Supervision | mR/R@20 | mR/R@50 |
|:------------:|:--------------:|:---------------:|:-------:|:-------:|
| ✗ | ✓ | ✓ | 0.5 / 0.4 | 1.3 / 1.2 |
| ✓ | ✗ | ✓ | 14.8 / 20.5 | 21.0 / 29.8 |
| ✓ | ✓ | ✗ | 14.6 / 22.1 | 17.8 / 27.9 |
| ✓ | ✓ | ✓ | **24.7 / 29.6** | **28.5 / 35.6** |

所有三个组件都是必要的：移除 Linear Embedding 导致模型发散；移除 BCE Supervision 丢失配对分布信息；移除 Matrix Learner 失去过滤能力。

### Matrix Learner 架构选择（Table 6b）

| Architecture | # Param | mR/R@20 | mR/R@50 |
|-------------|---------|:-------:|:-------:|
| MLP | 0.2M | 13.0 / 18.8 | 19.4 / 26.1 |
| G-Transformer | 1.4M | 17.3 / 26.1 | 23.2 / 32.6 |
| W-Transformer | 1.3M | 15.5 / 21.4 | 19.4 / 26.7 |
| **CNN-tiny** | **0.2M** | **24.7 / 29.6** | **28.5 / 35.6** |
| CNN-base | 30M | 23.3 / 33.3 | 28.2 / 39.3 |

CNN 架构表现最佳，验证了 CNN 作为高效语义滤波器保留局部细节的优势。增加参数量到 30M 未带来显著提升。

### 关系分类损失选择（Table 6c）
- Cross Entropy: 15.4 / 29.0 → Seesaw Loss: **24.7 / 29.6**（最佳）
- Focal Loss: 19.8 / 28.3

### KV 输入选择（Table 6d）
- concat pairs: **24.7 / 29.6** — 其他方案（random init / image features / random pairs）均远低于 10
- 证明 pair-level 结构信息对关系解码至关重要

### 正权重调整的 BCE Loss（Table 7b）
- 无正权重 → mR/R@20 降至 0.6 / 1.2（模型退化为全零输出）
- 有正权重 → 24.7 / 29.6

## Limitations

1. **数据集规模**：仅在中等规模数据集（PSG）上验证，未探索更大规模 SGG 数据集
2. **VG-150 泛化**：在 VG-150 上与 SGTR 性能相当但未明显超越，表明方法对 bounding-box 级别的 SGG 任务优化不足
3. **R@K 指标**：在 mR@K 上显著优于 HiLo，但在 R@K 上低于 HiLo，说明在常见关系（head classes）的识别上仍有改进空间
4. **关系分类**：长尾分布问题仅通过 Seesaw Loss 处理，可探索更复杂的去偏方法

## Reusable Claims

1. **PSG 性能瓶颈在于配对而非分割**：分割器（Mask2Former）已足够好（sub-IoU 0.79），提升配对质量比提升分割质量更有效。
2. **Pair Recall 与 Triplet Recall 强相关**：这是一个可迁移的洞察，适用于所有 PSG/SGG 方法设计。
3. **CNN 作为配对矩阵滤波器优于 Transformer**：在全连接配对矩阵的稀疏化任务上，CNN 的局部感受野比 Transformer 的全局注意力更有效。
4. **解耦配对和关系分类的两步策略**：显式先配对再分类减少了三元组重复预测（相比 PSGTR/PSGFormer 的耦合查询设计）。
5. **正权重调整的 BCE Loss**：处理极端稀疏标签（~0.056% 正类率）的关键设计。

## Connections

- **PSGFormer / PSGTR [ECCV 2022]**：本文的基线方法，Pair-Net 指出了它们未显式建模配对关系的不足
- **SGTR [CVPR 2022]**：端到端 SGG Transformer，与 PSGFormer 共享类似架构
- **HiLo [ICCV 2023]**：同步期的 PSG 方法，利用高频/低频信息去偏；Pair-Net 在 mR 上优于 HiLo 但在 R 上低于 HiLo
- **Mask2Former [CVPR 2022]**：作为分割器 backbone，提供 object queries
- **RelPN [CVPR 2021 SGG]**：之前的配对 proposal 方法，但基于 bounding box 且分三支（sub/obj/rel），Pair-Net 的 PPN 更简洁（单支 + matrix learner）
- **AdTrans / DSFlash**：后续 PSG 方法，可参考与之对比
- **DETR**：提供的 transformer decoder 结构用于 Relation Fusion 模块

## Open Questions

1. Pair-Net 在 R@K 上低于 HiLo 的原因是什么？是否因为 PPN 的 Top-K 选择过于激进？
2. Matrix Learner 的 CNN 设计是否能扩展到 3D/视频场景图生成？
3. Pair-Net 是否能与因果去偏方法（如 TDE、CaMouDle）结合以进一步提升 mR@K？
4. 正权重调整的 BCE Loss 是否适用于其他稀疏配对任务（如分子图生成、知识图谱补全）？

## Provenance

- Raw source: `raw/sources/2023-07-PairNet-Panoptic-Scene-Graph-Generation.pdf` (7.1 MB)
- Full text extracted: `raw/sources/2023-07-PairNet-Panoptic-Scene-Graph-Generation.txt` (66,939 chars)
- Evidence level: full-paper — 全文精读，包括方法细节、所有实验结果、消融研究
- Source: arXiv 2307.08699, ICCV 2023
- Code: https://github.com/king159/Pair-Net
