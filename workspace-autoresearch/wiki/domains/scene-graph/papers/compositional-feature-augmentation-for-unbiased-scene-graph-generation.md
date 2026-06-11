---
title: "Compositional Feature Augmentation for Unbiased Scene Graph Generation (CFA)"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - scene-graph-generation
  - long-tail-bias
  - feature-augmentation
  - compositional-learning
  - debiasing
  - ICCV-2023
raw_sources:
  - ../../../raw/sources/2023-ICCV-Compositional-Feature-Augmentation-for-Unbiased-SGG.pdf
  - ../../../raw/sources/2023-ICCV-Compositional-Feature-Augmentation-for-Unbiased-SGG.txt
related_pages:
  - fast-contextual-scene-graph-generation.md
evidence_level: full-paper
paper:
  title: "Compositional Feature Augmentation for Unbiased Scene Graph Generation"
  authors:
    - Lin Li
    - Guikun Chen
    - Jun Xiao
    - Yi Yang
    - Chunping Wang
    - Long Chen
  year: 2023
  venue: "IEEE/CVF International Conference on Computer Vision (ICCV), 2023"
  arxiv: "2308.06712"
  doi: null
  code: "https://github.com/HKUST-LongGroup/CFA"
  project: null
classification:
  label: "CFA — Compositional Feature Augmentation for Unbiased SGG"
  task:
    - Scene Graph Generation (SGG)
    - Predicate Classification (PredCls)
    - Scene Graph Classification (SGCls)
    - Scene Graph Generation (SGGen)
  method_family:
    - Feature augmentation
    - Intrinsic feature augmentation (Intrinsic-CFA)
    - Extrinsic feature augmentation (Extrinsic-CFA)
    - Hierarchical clustering for entity replacement
    - Mixup-based context augmentation
  modality:
    - Visual features (ROI)
    - Entity features (subject/object)
    - Context features (neighbor triplets)
    - Union box features
  datasets:
    - Visual Genome (VG)
    - GQA
  metrics:
    - Recall@K (R@K)
    - mean Recall@K (mR@K)
    - Mean (average of R@K and mR@K)
---

## Citation

Lin Li, Guikun Chen, Jun Xiao, Yi Yang, Chunping Wang, Long Chen. "Compositional Feature Augmentation for Unbiased Scene Graph Generation." *Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)*, 2023, pp. 21628-21638.

## One-Sentence Contribution

提出 Compositional Feature Augmentation (CFA) 策略，将关系三元组特征分解为内在特征（intrinsic）和外在特征（extrinsic），通过替换内在特征和混合外在特征来增强尾部谓词的特征多样性，首次从特征增强角度解决无偏 SGG 的长尾偏置问题。

## Problem Setting

场景图生成（SGG）旨在检测图像中的全部视觉关系三元组 `<sub, pred, obj>`。由于普遍存在的长尾谓词分布，SGG 模型倾向于偏向头部谓词（如 on, has）而忽略尾部谓词（如 laying on, holding）。

**现有方法的缺陷**：主流去偏策略（如重采样、损失重加权）仅改变已有训练样本的频率或贡献，但没有增加尾部谓词三元组特征的多样性。由于尾部类别的特征空间稀疏，难以推断完整的数据分布，导致学习到的决策边界对超参数敏感。

## Method

### 核心思路

将每个关系三元组特征分解为两个组件：

1. **内在特征（Intrinsic Feature）**：主体和客体的视觉、语义、空间特征
2. **外在特征（Extrinsic Feature）**：同一图像中邻居物体的上下文特征

通过增强这两个组件的多样性来扩展尾部谓词的特征空间。

### Intrinsic-CFA（内在特征增强）

- 对尾部谓词三元组，用其他"合适"的实体特征替换其主体或客体特征
- **层次聚类方法**：通过三种相似度（模式相似度、上下文相似度、语义相似度）度量实体类别间的相关性，将相关实体归入同一聚类
- 同一聚类内的实体特征可互相替换（如 dog → cat 用于 `dog-laying_on-bed` 三元组）
- 聚类数 K=15 效果最佳

### Extrinsic-CFA（外在特征增强）

- 从图像中随机选取一个上下文三元组（context triplet）
- 通过限定两个物体的类别和相对位置，选择一个合理的尾部谓词三元组作为目标
- 使用 mixup 操作将目标尾部谓词三元组的特征融合到上下文三元组中
- Mixup 参数 θ=0.5 时达到最佳权衡

### 模型无关性

CFA 是模型无关的（model-agnostic），可无缝集成到各种两阶段 SGG 框架中（Motifs、VCTree、Transformer）。

### 增强框架

两个串联的随机采样模块构成 Batch-Level 的 CFG：
1. 先采样一批图像处理部分三元组
2. 再采样一批图像做 Intrinsic-CFA
3. 最后采样一批图像做 Extrinsic-CFA

### 带组件先验的变体 CFA‡

由于尾部谓词的主客体类别高度相关，通过收集数据集的组件先验知识（component prior knowledge）进一步改进尾部性能。

## Experiments

### 数据集

- **Visual Genome (VG)**：标准 SGG benchmark，长尾谓词分布显著
- **GQA**：大规模 SGG 数据集，用于验证泛化能力

### 评估任务

1. **Predicate Classification (PredCls)**：给定 ground-truth 实体框和类别，预测谓词类别
2. **Scene Graph Classification (SGCls)**：给定 ground-truth 实体框，预测实体和谓词类别
3. **Scene Graph Generation (SGGen)**：检测所有实体及其关系

### 评估指标

- **Recall@K (R@K)**：top-K 置信预测中 ground-truth 三元组的比例（偏向头部）
- **mean Recall@K (mR@K)**：每个谓词类别分别计算 R@K 后再平均（偏向尾部）
- **Mean**：R@K 和 mR@K 的平均值（综合衡量）

### Baseline 方法

**Trade-off 方法（综合性能）**：Motifs、VCTree、Transformer、BGNN、PCPL、DLFE、BP-LSA、NICE、IETrans

**Tail-focused 方法（侧重尾部）**：TDE、CogTree、RTPB、PPDL、GCL、HML

### 实现细节

- 两阶段 SGG 框架（Motifs、VCTree、Transformer）
- Backbone：Faster R-CNN
- 在 VG 和 GQA 上进行所有实验

## Results

### VG 数据集 — Trade-off 方法（Table 1）

| Model | PredCls mR@50/100 | PredCls R@50/100 | Mean | SGCls mR@50/100 | SGCls R@50/100 | Mean | SGGen mR@50/100 | SGGen R@50/100 | Mean |
|-------|-------------------|------------------|------|-----------------|----------------|------|-----------------|----------------|------|
| Motifs (baseline) | 16.5/17.8 | 65.5/67.2 | 41.8 | 8.7/9.3 | 39.0/39.7 | 24.2 | 5.5/6.8 | 32.1/36.9 | 20.3 |
| **Motifs+CFA** | **35.7/38.2** | 54.1/56.6 | **46.2** | 17.0/18.4 | 34.9/36.1 | 26.6 | 13.2/15.5 | 27.4/31.8 | 22.0 |
| VCTree (baseline) | 17.1/18.4 | 65.9/67.5 | 42.2 | 10.8/11.5 | 45.6/46.5 | 28.6 | 7.2/8.4 | 32.0/36.2 | 20.9 |
| **VCTree+CFA** | **34.5/37.2** | 54.7/57.5 | 46.0 | 19.1/20.8 | 42.4/43.5 | **31.5** | 13.1/15.5 | 27.1/31.2 | 21.7 |
| Transformer+CFA | 30.1/33.7 | 59.2/61.5 | 46.1 | 15.7/17.2 | 36.3/37.3 | 26.6 | 12.3/14.6 | 27.7/32.1 | 21.7 |

关键发现：
- CFA 显著提升 mR@K 指标（Motifs: 16.5→35.7, +19.2 在 mR@50），超越所有 trade-off SOTA 方法
- CFA 在 Mean 指标上超越 SOTA 方法 NICE（46.2 vs 43.6，Motifs 上 PredCls）
- CFA 在提升尾部性能的同时对头部性能的牺牲最小

### VG 数据集 — Tail-focused 方法（Table 2）

| Model | PredCls mR@20/50/100 | SGCls mR@20/50/100 | SGGen mR@20/50/100 |
|-------|---------------------|-------------------|-------------------|
| **Motifs+CFA‡** | **31.5/39.9/43.0** | 17.3/20.9/22.4 | 11.2/15.3/18.1 |
| **VCTree+CFA‡** | **31.6/39.2/42.5** | 21.5/26.3/28.3 | 10.8/15.1/17.9 |
| **Transformer+CFA‡** | **31.2/38.6/41.5** | 17.2/20.9/22.7 | 10.6/15.0/17.9 |

CFA‡ 超越 SOTA tail-focused 方法 HML（Motifs+CFA‡ PredCls mR@100=43.0 vs HML 38.7）。

### GQA 数据集（Table 3）

| Model | PredCls mR@50/100 | SGCls mR@50/100 | SGGen mR@50/100 |
|-------|-------------------|-----------------|-----------------|
| Motifs | 13.9/14.7 | 7.2/7.5 | 5.5/6.6 |
| **Motifs+CFA** | **31.7/33.8** | 14.2/15.2 | 11.6/13.2 |
| VCTree | 14.4/15.3 | 6.1/6.6 | 5.8/6.0 |
| **VCTree+CFA** | **33.4/35.1** | 14.1/15.0 | 10.8/12.6 |
| Transformer | 15.2/16.1 | 7.5/7.9 | 6.9/7.8 |
| **Transformer+CFA** | **27.8/29.4** | 16.2/16.9 | 13.4/15.3 |

CFA 在 GQA 上同样大幅提升 mR@K（Motifs: PredCls mR@50 从 14.7→33.8, +19.1），验证了跨数据集泛化能力。

### 消融实验（Table 4）— 各组件贡献

| IN | EX-fg | EX-bg | PredCls mR@50/100 | R@50/100 | Mean |
|----|-------|-------|-------------------|---------|------|
| — | — | — | 16.5/17.8 | 65.6/67.2 | 41.8 |
| ✓ | — | — | 19.3/21.2 | 64.7/66.6 | 43.0 |
| — | ✓ | — | 25.6/27.8 | 63.0/64.8 | 45.3 |
| — | — | ✓ | 23.9/26.3 | 63.3/65.7 | 44.8 |
| ✓ | ✓ | — | 27.2/29.3 | 61.9/64.3 | 45.7 |
| ✓ | — | ✓ | 27.5/30.0 | 61.7/64.1 | 45.8 |
| — | ✓ | ✓ | 27.8/30.3 | 60.7/63.4 | 45.6 |
| ✓ | ✓ | ✓ | **35.7/38.2** | 54.1/56.6 | **46.2** |

关键发现：
- IN 单独使用时仅微幅提升 mR@K（+2.8~3.4），因为尾部三元组数量不足
- EX-fg 和 EX-bg 均显著提升 mR@K（17.8→30.3+），同时保持竞争性 R@K
- 三者组合获得最佳 Mean（46.2）

### 消融实验 — 聚类相似度（Table 5a）

使用全部三种相似度（模式+上下文+语义）获得最佳 Mean（46.2），仅用模式相似度效果最差。

### 消融实验 — 聚类数 K（Table 5b）

K=15 效果最佳（mR@50=35.7），K=40 和 K=150 下降。更大 K 意味着每类可替换的实体类别更多，特征多样性更丰富。

### 消融实验 — Mixup 参数 θ（Table 5c）

θ=0.5 最佳（Mean=46.2）。θ 过小或过大都会降低性能。

## Limitations

1. **仅适用于两阶段框架**：CFA 当前仅支持两阶段 SGG 框架，第一阶段（Faster R-CNN）检测提议，第二阶段分类。一阶段模型的特征增强需在图像级别应用，留作未来工作。
2. **依赖数据集组件先验**：CFA‡ 变体需要从数据集中收集组件先验知识来优化尾部性能。
3. **聚类质量依赖相似度度量**：Intrinsic-CFA 中实体替换的质量依赖于聚类/相似度度量的准确性，替换不合理的实体可能引入噪声。

## Reusable Claims

> **Claim**: 现有 re-balancing 方法（重采样、损失重加权）无法增加尾部谓词三元组特征的多样性，这是其性能瓶颈的关键原因。
> **Evidence**: CFA 通过特征增强（替换内在特征、混合外在特征）显著提升 mR@K（Motifs 上 mR@50 从 16.5 提高到 35.7），而 re-balancing baseline（如 PCPL）提升有限（24.3）。
> **Confidence**: high

> **Claim**: 将关系三元组解耦为内在和外在特征并分别增强，可以有效扩展尾部谓词的特征空间。
> **Evidence**: 消融实验显示，Intrinsic-CFA 和 Extrinsic-CFA 各自贡献显著，三者组合达到最佳性能（Mean=46.2）。
> **Confidence**: high

> **Claim**: 通过组件先验（component prior）进一步优化尾部性能，CFA‡ 在尾类独大的指标（mR@K）上超越 HML 等 tail-focused SOTA。
> **Evidence**: Motifs+CFA‡ PredCls mR@100=43.0 vs HML 38.7。
> **Confidence**: high

## Connections

- 和 [Fast Contextual Scene Graph Generation with Unbiased Context Augmentation](fast-contextual-scene-graph-generation.md) 都使用上下文增强处理长尾偏置，但 CFA 关注特征层面的解耦与增强，而非输入上下文描述。
- 与 Compositional Learning（CL）方法相关但不同：CL 在 HOI 检测中用于生成新的交互样本，CFA 首次将其系统性地应用于 SGG 去偏。
- 与 NICE [CVPR 2022]、IETrans [ECCV 2022] 等同属 model-agnostic 去偏策略竞争，CFA 在 Mean 指标上超越它们。

## Open Questions

1. 如何将 CFA 扩展到一阶段 SGG 框架（如基于 Transformer 的端到端模型）？
2. 是否可以基于开放词汇（open-vocabulary）或跨域图像生成更丰富的替换实体特征？
3. Intrinsic-CFA 中的层次聚类是否可以动态更新，以在训练过程中适应实体关联的变化？

## Provenance

- **来源**：raw/sources/2023-ICCV-Compositional-Feature-Augmentation-for-Unbiased-SGG.pdf（1.5MB，11页 PDF）
- **提取文本**：raw/sources/2023-ICCV-Compositional-Feature-Augmentation-for-Unbiased-SGG.txt（50,410 chars，1830 行）
- **证据等级**：full-paper — 全文精读，覆盖方法、实验、结果、消融
- **注**：用户备注标题为"Contextual Feature Augmentation for Scene Graph Generation (CFA)"，经核对实际论文标题为 "Compositional Feature Augmentation for Unbiased Scene Graph Generation"（ICCV 2023），代码仓库 HKUST-LongGroup/CFA。
