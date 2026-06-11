---
title: "Panoptic Scene Graph Generation with Semantics-Prototype Learning (ADTrans)"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - scene-graph-generation
  - panoptic-scene-graph
  - debiasing
  - data-transfer
  - prototype-learning
  - contrastive-learning
  - predicate-bias
  - AAAI-2024
raw_sources:
  - ../../../raw/sources/2024-02-01-panoptic-scene-graph-generation-with-semantics-prototype-learning.pdf
  - ../../../raw/sources/2024-02-01-panoptic-scene-graph-generation-with-semantics-prototype-learning.txt
related_pages:
  - compositional-feature-augmentation-for-unbiased-scene-graph-generation.md
  - camodule-causal-adjustment-module-debiasing-scene-graph-generation.md
  - hiker-sgg-hierarchical-knowledge-enhanced-robust-sgg.md
evidence_level: full-paper
paper:
  title: "Panoptic Scene Graph Generation with Semantics-Prototype Learning"
  authors:
    - Li Li
    - Wei Ji
    - Yiming Wu
    - Mengze Li
    - You Qin
    - Lina Wei
    - Roger Zimmermann
  year: 2024
  venue: "Proceedings of the AAAI Conference on Artificial Intelligence (AAAI), 2024"
  arxiv: "2307.15567"
  doi: null
  code: "https://github.com/lili0415/PSG-biased-annotation"
  project: null
classification:
  label: "ADTrans — Adaptive Data Transfer for PSG Debiasing"
  task:
    - Panoptic Scene Graph Generation (PSG)
    - Predicate Classification (PredCls)
    - Scene Graph Classification (SGCls)
    - Scene Graph Generation (SGDet/SGDET)
  method_family:
    - Adaptive data transfer
    - Prototype-based predicate representation learning
    - Robust contrastive training (RCT)
    - Invariant representation exploration
    - Multistage data filtration
    - Dynamic prototype updating
  modality:
    - Visual features (panoptic segmentation)
    - Textual features (BERT sentence embeddings)
    - Confusion matrix (visual prior knowledge)
  datasets:
    - PSG (Panoptic Scene Graph)
    - Visual Genome (VG)
  metrics:
    - Recall@K (R@K)
    - mean Recall@K (mR@K)
    - Percentile Recall (PR@K)
    - F@K (harmonic mean of R@K and mR@K)
---

# ADTrans: Adaptive Data Transfer for Panoptic Scene Graph Generation Debiasing

## 概述

ADTrans (Adaptive Data Transfer) 是一个针对 PSG 和 SGG 任务中**标注偏差（biased annotation）**问题的数据集增强框架。核心思路：不对模型结构做改变，而是通过数据端的高质量转换来消除标注不一致性。

## 动机

PSG 数据集存在严重的标注偏差问题：
1. **语言偏好差异**：不同标注者对同一物体对的 predicate 标注不统一（如"on" vs."standing on"）
2. **语义重叠**：predicate 之间存在层级关系和语义重叠（如 superclass "on" 与 subclass "standing on"）
3. **标注惰性**：标注者倾向使用通用 predicate（如"on"、"beside"）而非信息量更具体的 predicate

这导致模型无法学到从视觉到语义的一致映射，最终性能受限。

## 方法

### 框架总览：ADTrans

ADTrans 包含三个核心阶段：

#### 1. 目标识别（Target Identifying）
- **不可区分三元组（Indistinguishable Triplets）**：使用预训练模型（如 VCTree）在原训练集上预测，找出模型预测与 ground truth 不一致的样本
- **潜在正样本（Potentially Positive Samples）**：找出被标注者遗漏的 NA（未标注 predicate）样本

#### 2. 关系表示提取（Relation Representation Extraction）
- **鲁棒对比训练（Robust Contrastive Training, RCT）**：将三元组转换为句子（如"<person, standing on, snow>"→"The person is standing on the snow"），使用 BERT + Angular Margin InfoNCE Loss 训练文本编码器
- **视觉域对齐**：利用预训练模型的混淆矩阵 C ∈ R^Q×Q，对视觉上相似的 predicate 对设置较小的对比权重，对齐视觉-文本语义空间
- **不变表示探索（Invariant Representation Exploration）**：通过最小化同类样本损失值的方差，鼓励模型学到对不同偏置分布都鲁棒的不变特征

#### 3. 语义原型学习（Semantics-Prototype Learning）
- **动态原型更新**：构建原型空间 P_type ∈ R^L×Q，根据表示的不变程度动态更新每个 predicate 类的原型向量
- **多阶段数据过滤**：利用样本与原型之间的分布偏移 + 损失方差，每轮训练筛除 top D% 的偏置样本。对于少于 100 个样本的 predicate 类不再剔除

#### 4. 数据转换与重采样（Data Transfer & Resampling）
- **不可区分三元组**：用原型相似度矩阵作为自适应转换比例，代替 IETrans 的硬转换
- **潜在正样本**：定义影响因子 E(·) = √(−log(NAscore)) × c(subject, object) × c(predicate)，按影响因子排序后选取 top Kg%
- **重采样**：对低频率 triplet 进行过采样，repeat factor = max(1, t × c(subject, object) × c(predicate))

## 实验结果

### PSG 数据集 — SGDet 任务

| 方法 | R@20 | R@50 | R@100 | mR@20 | mR@50 | mR@100 | PR@20 | PR@50 | PR@100 |
|------|------|------|-------|-------|-------|--------|-------|-------|--------|
| **Two-Stage** | | | | | | | | | |
| IMP | 16.5 | 18.2 | 18.6 | 6.52 | 7.05 | 7.23 | 12.9 | 13.7 | 13.9 |
| IMP + IETrans | 14.5 | 15.9 | 16.4 | 10.2 | 11.0 | 11.3 | 14.5 | 15.4 | 15.7 |
| IMP + **ADTrans** | **15.0** | **16.5** | **17.0** | **12.5** | **13.5** | **14.0** | **16.0** | **17.1** | **17.5** |
| VCTree | 20.6 | 22.1 | 22.5 | 9.70 | 10.2 | 10.2 | 16.0 | 16.8 | 16.9 |
| VCTree + IETrans | 17.5 | 18.9 | 19.3 | 17.1 | 18.0 | 18.1 | 19.6 | 20.5 | 20.7 |
| VCTree + **ADTrans** | **17.9** | **19.5** | **19.9** | **18.0** | **18.9** | **19.0** | **20.2** | **21.2** | **21.4** |
| MOTIFS | 20.0 | 21.7 | 22.0 | 9.10 | 9.57 | 9.69 | 15.5 | 16.3 | 16.5 |
| MOTIFS + IETrans | 16.7 | 18.3 | 18.8 | 15.3 | 16.5 | 16.7 | 18.2 | 19.4 | 19.7 |
| MOTIFS + **ADTrans** | **17.1** | **18.6** | **19.0** | **17.1** | **18.0** | **18.5** | **19.4** | **20.4** | **20.8** |
| GPSnet | 17.8 | 19.6 | 20.1 | 7.03 | 7.49 | 7.67 | 13.6 | 14.4 | 14.7 |
| GPSnet + IETrans | 14.6 | 16.0 | 16.7 | 11.5 | 12.3 | 12.4 | 15.3 | 16.2 | 16.5 |
| GPSnet + **ADTrans** | **17.8** | **19.2** | **19.5** | **16.5** | **17.5** | **17.6** | **19.3** | **20.3** | **20.5** |
| **One-Stage** | | | | | | | | | |
| PSGTR | 28.4 | 34.4 | 36.3 | 16.6 | 20.8 | 22.1 | 21.9 | 26.3 | 27.6 |
| PSGTR + IETrans | 25.3 | 28.8 | 29.2 | 23.1 | 27.2 | 27.5 | 24.9 | 28.4 | 28.7 |
| PSGTR + **ADTrans** | **26.0** | **29.6** | **30.0** | **26.4** | **29.7** | **30.0** | **27.1** | **30.2** | **30.5** |

**关键结果**：PSGTR + ADTrans 在 PSG 数据集 SGDet 任务上，mR@100 从 **22.1** 提升至 **30.0**（+35.7%），PR@100 从 27.6 提升至 30.5。

### VG 数据集 — PredCLS 任务

| 方法 | mR@20 | mR@50 | mR@100 | F@20 | F@50 | F@100 |
|------|-------|-------|--------|------|------|-------|
| MOTIFS | 11.7 | 15.2 | 16.2 | 19.5 | 24.5 | 26.0 |
| MOTIFS + **ADTrans** | **29.0** | **36.2** | **38.8** | **36.1** | **41.7** | **43.5** |
| VCTree | 14.0 | 16.3 | 17.7 | 22.7 | 26.0 | 28.0 |
| VCTree + **ADTrans** | **30.0** | **32.9** | **35.5** | **37.2** | **40.5** | **42.5** |
| GPSnet | 13.2 | 15.0 | 16.0 | 21.7 | 24.4 | 25.8 |
| GPSnet + **ADTrans** | **27.3** | **32.0** | **34.7** | **34.8** | **40.2** | **42.1** |

**关键结果**：MOTIFS + ADTrans 在 VG PredCLS 上 mR@100 从 **16.2** → **38.8**（+139.5%），F@100 从 26.0 → 43.5。

### VG 数据集 — SGCLS 任务

| 方法 | mR@20 | mR@50 | mR@100 | F@20 | F@50 | F@100 |
|------|-------|-------|--------|------|------|-------|
| MOTIFS | 6.0 | 8.0 | 8.5 | 10.1 | 13.1 | 13.8 |
| MOTIFS + **ADTrans** | **14.8** | **17.0** | **17.8** | **20.2** | **22.5** | **23.7** |
| VCTree | 6.3 | 7.5 | 8.0 | 10.7 | 12.5 | 13.3 |
| VCTree + **ADTrans** | **16.0** | **19.0** | **19.8** | **20.3** | **23.7** | **24.5** |
| GPSnet | 10.0 | 11.8 | 12.6 | 15.7 | 17.9 | 18.9 |
| GPSnet + **ADTrans** | **15.5** | **18.2** | **18.8** | **19.9** | **22.5** | **23.7** |

### VG 数据集 — SGDET 任务

| 方法 | mR@20 | mR@50 | mR@100 | F@20 | F@50 | F@100 |
|------|-------|-------|--------|------|------|-------|
| MOTIFS | 4.8 | 6.2 | 7.1 | 8.0 | 10.3 | 11.8 |
| MOTIFS + **ADTrans** | **10.6** | **15.5** | **18.1** | **13.4** | **18.9** | **22.0** |
| VCTree | 5.2 | 6.7 | 7.9 | 8.7 | 11.0 | 13.0 |
| VCTree + **ADTrans** | **9.7** | **12.5** | **16.9** | **12.2** | **16.3** | **20.3** |
| GPSnet | 5.2 | 5.9 | 7.1 | 8.6 | 9.9 | 11.8 |
| GPSnet + **ADTrans** | **12.3** | **15.8** | **19.2** | **15.1** | **18.6** | **21.9** |

### 消融实验

| 配置 | R/mR@20 | R/mR@50 | R/mR@100 |
|------|---------|---------|----------|
| PSGTR baseline | 28.4 / 16.6 | 34.4 / 20.8 | 36.3 / 22.1 |
| + 不可区分三元组转换 | 26.2 / 24.9 | 30.3 / 28.2 | 30.7 / 29.2 |
| + 潜在正样本转换 | 25.5 / 25.6 | 29.2 / 29.1 | 29.7 / 29.6 |
| + 重采样（完整 ADTrans） | 26.0 / 26.4 | 29.6 / 29.7 | 30.0 / 30.0 |

**关键消融发现**：
- 不可区分三元组转换提供最大增益（mR@100: 22.1 → 29.2）
- 潜在正样本转换进一步改善（mR@100: 29.2 → 29.6）
- 重采样微调（mR@100: 29.6 → 30.0）

## 关键发现

1. **数据层面的去偏比模型层面的去偏更有效**：ADTrans 直接在标注层面解决偏差，避免模型结构复杂化
2. **自适应转换优于硬转换**：相比 IETrans 的硬阈值转换，ADTrans 的原型相似度自适应转换更精确，减少正样本误转
3. **少量偏注数据破坏性极大**：消融实验显示简单移除不可区分三元组（而非转换）就可大幅提升 baseline（mR@100: 22.1 → 25.3），说明偏注样本对模型训练的负面影响
4. **视觉-文本对齐**：利用混淆矩阵将语言模型与视觉领域对齐，避免纯文本相似度带来的误对齐
5. **跨数据集泛化**：ADTrans 在 PSG 和 VG 两个数据集上均有显著提升，在更具挑战的 VG 数据集上表现更突出

## 局限性

- 需要额外预训练模型（VCTree）来生成混淆矩阵和目标识别
- 多阶段过滤可能剔除少数真正难样本
- 框架复杂度较高，训练需要多个阶段
- 代码已开源（GitHub），但未与 HuggingFace 集成

## 参考资料

- arXiv: [2307.15567](https://arxiv.org/abs/2307.15567)
- 代码: [lili0415/PSG-biased-annotation](https://github.com/lili0415/PSG-biased-annotation)
- 相关论文: IETrans (Zhang et al., ECCV 2022)
