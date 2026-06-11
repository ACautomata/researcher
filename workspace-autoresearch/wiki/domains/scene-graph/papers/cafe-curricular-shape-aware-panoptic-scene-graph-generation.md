---
title: "From Easy to Hard: Learning Curricular Shape-aware Features for Robust Panoptic Scene Graph Generation (CAFE)"
type: paper
domain: scene-graph
status: active
created: 2026-06-10
updated: 2026-06-10
tags:
  - scene-graph-generation
  - panoptic-scene-graph
  - curriculum-learning
  - shape-aware-features
  - robust-learning
  - zero-shot
source_pages: []
raw_sources:
  - raw/sources/2024-07-12-curricular-shape-aware-panoptic-sgg.pdf
  - raw/sources/2024-07-12-curricular-shape-aware-panoptic-sgg.txt
related_pages:
  - papers/pair-net-panoptic-scene-graph-generation.md
  - papers/hilo-exploiting-high-low-frequency-for-unbiased-panoptic-scene-graph-generation.md
  - papers/neural-motifs-scene-graph-global-context.md
  - papers/vctree-learning-to-compose-dynamic-tree-structures.md
  - papers/adtrans-adaptive-data-transfer-panoptic-scene-graph-debiasing.md
  - papers/EICR-environment-invariant-curriculum-relation-learning-sgg.md
paper:
  title: "From Easy to Hard: Learning Curricular Shape-aware Features for Robust Panoptic Scene Graph Generation"
  authors:
    - Hanrong Shi
    - Lin Li
    - Jun Xiao
    - Yueting Zhuang
    - Long Chen
  year: 2024
  venue: arXiv (submitted to journal)
  arxiv: "2407.09191"
  code: ~
  project: ~
classification:
  label: CAFE
  task:
    - Panoptic Scene Graph Generation (PSG)
    - Robust PSG
    - Zero-shot PSG
  method_family:
    - Curriculum Learning
    - Shape-aware Feature Learning
    - Two-stage PSG
    - Knowledge Distillation
  modality:
    - Image
    - Panoptic Segmentation
  datasets:
    - PSG (48,749 images, 133 object classes, 56 relation classes)
  metrics:
    - Recall@K (R@20/50/100)
    - mean Recall@K (mR@20/50/100)
    - Mean (average of all R@K and mR@K)
    - Zero-shot Recall@K (zR@K)
    - PQ (Panoptic Quality)
evidence_level: full-paper
---

# From Easy to Hard: Learning Curricular Shape-aware Features for Robust Panoptic Scene Graph Generation (CAFE)

## Citation

Hanrong Shi, Lin Li, Jun Xiao, Yueting Zhuang, Long Chen. "From Easy to Hard: Learning Curricular Shape-aware Features for Robust Panoptic Scene Graph Generation." arXiv:2407.09191, 2024. (submitted to journal)

## One-Sentence Contribution

CAFE 提出模型无关的课程学习策略，将形状感知特征（mask features 和 boundary features）以 easy-to-hard 方式渐进集成到两阶段 PSG 框架中，显著提升鲁棒 PSG 和零样本 PSG 的性能。

## Problem Setting

Panoptic Scene Graph Generation (PSG) 旨在基于全景分割 mask 生成全面的图结构场景表示。与基于 bbox 的传统 SGG 相比，PSG 可提供更精确的物体定位并涵盖背景区域关系。

**关键问题**：现有 PSG 方法完全依赖 bbox 导出的空间特征，忽略了 mask 中蕴含的形状感知特征（shape-aware features），导致细粒度关系预测中的语义混淆（如 walking on vs. running on）。

**任务形式**：PSG 建模分布 P(G|I) = P(M, O, R|I)，其中 G 为场景图（节点为物体 oi + mask mi，边为关系 rij）。

## Method

CAFE 基于两阶段 PSG 范式（mask 生成 → 物体分类 → 关系分类），包含两个核心组件：

### 1. Shape-aware Feature Preparation

提出两类形状感知特征，使用 **Zernike moments** 提取紧凑表示（256 维）：

- **Mask Features (f^m_i ∈ R²⁵⁶)**：从物体 mask 中提取轮廓形状信息（binary erosion + Zernike moments）
- **Boundary Features (f^d_ij ∈ R²⁵⁶)**：从 subject-object 的掩码交集中提取交互区域信息

三阶段特征复杂度递增：
- **Stage-1**：仅 bbox features (RoIAlign)
- **Stage-2**：bbox + mask features
- **Stage-3**：bbox + mask + boundary features

对于 Transformer backbone，提出三种融合策略：Joint Fusion、Divided Fusion、Entangled Attention（Entangled Attention 效果最佳）。

### 2. Curricular Feature Training

**Cognition-based Predicate Grouping**（两步法）：
1. 按谓词实例数降序排列，均分三组 R1/R2/R3
2. 基于混淆矩阵做语义相似度调整（阈值 μ=0.8），将易混淆谓词分配到不同组
3. 结果：不平衡比从 6,777 降至最高 28

**三分类器架构**：
- 每个阶段有其独立的关系分类器 Cls^(k)_rel
- 分类空间逐步扩展：Cls^(1) 只识别 R1，Cls^(2) 识别 R1∪R2，Cls^(3) 识别所有谓词

**Predicate Sampling**：
- 图像级过采样（tail predicate images）
- 中位数重采样（公式 ϕ^k = λϕ^k₁ + (1−λ)ϕ^k₂，λ=0.5）

**训练目标**：
- Cross-Entropy Loss（分类）+ KL-divergence Loss（知识蒸馏，Top-Down 模式）
- 总损失：L_total = L_ce + α·L_kl（α=1.0）

**推理**：仅使用最后一个分类器 Cls^(3)_rel。

## Experiments

### 数据集和设置
- **数据集**：PSG 数据集，48,749 张图像，133 个物体类（80 thing + 53 stuff），56 个关系类
- **任务**：PredCls（给定 GT 物体和位置预测关系）和 SGDet（检测+关系预测）

### 评估指标
- **Robust PSG**：R@20/50/100（偏向 head 谓词）、mR@20/50/100（偏向 tail 谓词）、Mean（综合）
- **Zero-shot PSG**：zR@20/50/100、Average
- **SGDet** 额外报告 PQ

### 实现细节
- **Mask 生成**：PredCls 用 Panoptic FPN（ResNet-50-FPN），SGDet 用 Panoptic Segformer（COCO pretrained）
- **Object 模块**：与 baseline 对齐（Motifs 用 bi-LSTM）
- **Relation 模块**：CAFE 框架
- **优化器**：SGD，batch size=16，lr=0.002，12 epochs
- **超参数**：α=1.0, λ=0.5, μ=0.8
- **硬件**：NVIDIA 2080ti GPUs

### Baselines
- **Two-stage 模型无关方法**：Motifs, VCTree, Transformer + BGNN, GCL, BAI, IETrans, ADTrans, DWIL, RCpsg
- **Two-stage 模型特定方法**：IMP, GPSNet, C-SGG
- **One-stage 方法**：PSGTR, PSGFormer, CATQ, Pair-Net, HiLo

## Results

### Robust PSG — PredCls（Table 1）

| 模型 | R@20 | R@50 | R@100 | mR@20 | mR@50 | mR@100 | Mean |
|------|------|------|-------|-------|-------|--------|------|
| Motifs | 44.9 | 50.4 | 52.4 | 20.2 | 22.1 | 22.9 | 35.5 |
| Motifs+CAFE | 39.2 | 45.3 | 47.2 | **33.2** | **36.2** | **36.9** | **39.7** |
| VCTree | 45.3 | 50.8 | 52.7 | 20.5 | 22.6 | 23.3 | 35.9 |
| VCTree+CAFE | 40.4 | 46.0 | 48.1 | **34.6** | **36.8** | **37.6** | **40.6** |
| Transformer | 36.4 | 42.2 | 44.5 | 13.2 | 15.2 | 15.9 | 27.9 |
| Transformer+CAFE | 43.3 | 48.8 | 50.9 | **30.9** | **32.8** | **33.5** | **40.0** |

关键发现：CAFE 在 Mean 指标上超越 SOTA 模型特定方法 C-SGG（38.0→40.6，基于 VCTree）。在 head 谓词上有轻微牺牲，但对 tail 谓词实现大幅提升（从 0.3% 升至 16.8% R@100，Table 3）。

### Robust PSG — SGDet（Table 2）

| 模型 | R@20 | R@50 | R@100 | mR@20 | mR@50 | mR@100 | Mean | PQ |
|------|------|------|-------|-------|-------|--------|------|-----|
| VCTree | 20.6 | 22.1 | 22.5 | 9.7 | 10.2 | 10.2 | 15.9 | 40.2 |
| VCTree+CAFE | **26.9** | **29.8** | **30.6** | **27.8** | **29.1** | **29.4** | **28.9** | **54.9** |
| Transformer | 19.6 | 21.1 | 21.6 | 8.7 | 9.1 | 9.2 | 14.9 | 40.2 |
| Transformer+CAFE | **24.6** | **27.6** | **28.7** | **25.0** | **26.6** | **26.9** | **26.6** | **54.9** |

关键发现：CAFE 在 SGDet 中大幅超越所有两阶段 SOTA（如 DWIL 18.4 Mean → CAFE 28.9 Mean，基于 VCTree）。PQ 指标 54.9 超越多数 one-stage 方法（如 PSGFormer 36.8, HiLo 55.4）。

### Head/Body/Tail 分解（Table 3）
- Motifs+CAFE 在 Head R@100: 50.9（Motifs 基线 56.3），Body: **45.7**（Motifs 13.1），Tail: **16.8**（Motifs 0.3）
- 平均：37.8 vs 23.2（Motifs 基线）

### Zero-shot PSG — PredCls（Table 4）

| 模型 | zR@20 | zR@50 | zR@100 | Average |
|------|-------|-------|--------|---------|
| Motifs | 25.6 | 37.2 | 42.3 | 35.0 |
| Motifs+CAFE | **31.4** (+5.8) | **42.2** (+5.0) | **44.1** (+1.8) | **39.2** (+4.2) |
| Transformer | 20.5 | 42.3 | 50.0 | 37.6 |
| Transformer+CAFE | **38.9** (+18.4) | **47.7** (+5.4) | **51.6** (+1.6) | **46.1** (+8.5) |

### 消融实验

**Shape-aware Features 有效性（Table 5）**：
- bbox only: Mean 35.9 → +bbox+mask+boundary: Mean 39.7
- 逐步增加特征复杂度带来渐进性能提升

**Feature Fusion 策略（Table 6）**：
- Entangled Attention 最优：Mean 40.0（vs Concatenation 35.2）
- 训练代价 2.38s/image，推理代价 0.204s/image

**Curriculum Learning（Table 7）**：
- 使用课程学习后 mR@100 提升 6.5~7.9 个百分点
- Mean 提升 3.2~4.6 个百分点

**Predicate Grouping 策略（Table 8）**：
- Cognition-based Mean 39.7 > Average 38.5 > Random 37.7

**Sampling 策略（Table 9）**：
- 同时使用过采样 + 中位数重采样取得最佳 Mean 39.7
- 无采样时 Mean 37.1（R@K 高但 mR@K 低）

**λ 消融（Table 10）**：
- λ=0.5 最优（Mean 39.7）；极端值 λ=0 导致 mR@K 高但 R@K 低（Mean 35.8）

**Knowledge Transfer Mode（Table 11）**：
- Top-Down Mean 39.7 > Bi-Direction 39.2 > Neighbor 38.3

## Limitations

1. CAFE 当前仅适用于两阶段框架（因为 shape-aware features 源自全景分割器产生的 mask）
2. 受计算资源限制，未验证在 one-stage 方法（如 PSGTR，需 8×V100）上的适用性
3. 知识蒸馏虽在训练阶段增加额外开销，但推理阶段无额外代价

## Reusable Claims

- **Claim**: 在 PSG 中引入形状感知特征（mask + boundary features）能够弥补仅依赖 bbox 空间特征导致的语义混淆
- **Claim**: 课程学习策略（easy-to-hard 的谓词分组 + 渐进特征复杂度）在 PSG 任务中比随机/均分分组显著更优，mR@100 提升 7.9 个百分点
- **Claim**: CAFE 在零样本 PSG 场景中因学习到更鲁棒的视觉关系特征而展现出强泛化能力，Average 指标较 Transformer 基线提升 8.5 个百分点
- **Claim**: 中位数重采样与图像级过采样的结合在 PSG 不平衡数据集上比单一采样策略更优（Mean 39.7 vs 38.4/38.0）

## Connections

- 与 [EICR](papers/eicr-environment-invariant-curriculum-relation-learning-sgg.md) 同为课程学习在 SGG/PSG 中的应用，但 EICR 侧重环境不变性，CAFE 侧重形状感知特征的渐进集成
- 与 [HiLo](papers/hilo-exploiting-high-low-frequency-for-unbiased-panoptic-scene-graph-generation.md) 同为 PSG 去偏方法，HiLo 关注频率学特征分离，CAFE 关注形状感知特征
- 基于 Motifs/VCTree/Transformer 等经典 SGG backbone，与 [BGNN](papers/2023-CVPR-Fast-Contextual-Scene-Graph-Generation.md)、[GCL](papers/2022-CVPR-stacked-hybrid-attention-group-collaborative-learning-sgg.md) 等同属模型无关方法
- Zero-shot PSG 能力与 [T-CAR](papers/2023-09-07-T-CAR-zero-shot-scene-graph-generation-triplet-calibration-reduction.md) 和 [OvSGTR](papers/ovsgtr-expanding-scene-graph-boundaries.md) 相关

## Open Questions

- CAFE 能否扩展到 one-stage PSG 方法（如 PSGTR/PSGFormer）？
- Zernike moments 之外的形状特征提取方法能否带来进一步提升？
- 在更大规模/多样化 PSG 数据集（如 OpenPSG）上的表现？
- 课程学习的三个阶段划分是否最优？可否自适应确定分组数和特征复杂度？

## Provenance

- Raw source: raw/sources/2024-07-12-curricular-shape-aware-panoptic-sgg.pdf (2.98 MB)
- Full text: raw/sources/2024-07-12-curricular-shape-aware-panoptic-sgg.txt (84,431 chars)
- Evidence level: full-paper（基于完整 PDF 全文分析）
