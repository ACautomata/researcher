---
title: "OED: Towards One-stage End-to-End Dynamic Scene Graph Generation"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - scene-graph-generation
  - dynamic-scene-graph
  - one-stage
  - end-to-end
  - set-prediction
  - temporal-modeling
  - cvpr-2024
  - video-understanding
raw_sources:
  - ../../../raw/sources/2024-CVPR-OED-Towards-One-stage-End-to-End-Dynamic-Scene-Graph-Generation.pdf
  - ../../../raw/sources/2024-CVPR-OED-Towards-One-stage-End-to-End-Dynamic-Scene-Graph-Generation.txt
related_pages:
  - tempura-unbiased-video-scene-graph-generation.md
  - panoptic-video-scene-graph-generation.md
  - fdsg-forecasting-dynamic-scene-graphs.md
evidence_level: full-paper
paper:
  title: "OED: Towards One-stage End-to-End Dynamic Scene Graph Generation"
  abbreviated: "OED"
  authors:
    - Guan Wang
    - Zhimin Li
    - Qingchao Chen
    - Yang Liu
  affiliations:
    - Wangxuan Institute of Computer Technology, Peking University
    - Tencent Inc.
    - National Institute of Health Data Science, Peking University
  year: 2024
  venue: CVPR 2024
  doi: null
  arxiv: null
  code: "https://github.com/guanw-pku/OED"
  url: null
classification:
  label: One-stage End-to-End Dynamic Scene Graph Generation
  task:
    - Dynamic Scene Graph Generation (DSGG)
  method_family:
    - Set Prediction (DETR-based)
    - Cascaded Decoders
    - Progressively Refined Temporal Module (PRM)
  modality: Video
  datasets:
    - Action Genome
  metrics:
    - Recall@K (R@K)
---

# OED: Towards One-stage End-to-End Dynamic Scene Graph Generation

## Citation

Guan Wang, Zhimin Li, Qingchao Chen, Yang Liu. "OED: Towards One-stage End-to-End Dynamic Scene Graph Generation." CVPR 2024.

## One-Sentence Contribution

提出首个**单阶段端到端**动态场景图生成框架 OED，将 DSGG 重构为集合预测问题，通过级联解码器聚合空间上下文 + Progressively Refined Module (PRM) 实现无显式跟踪器的时序上下文聚合。

## Problem Setting

动态场景图生成 (DSGG) 的目标是从视频序列中检测视觉关系，以 ⟨subject, predicate, object⟩ 三元组表示。传统方法采用**多阶段流水线**：

1. **Object Detection** → 用预训练检测器检测实例
2. **Temporal Association** → 用跟踪器或轨迹关联帧间实例
3. **Relation Classification** → 对候选 subject-object 对进行谓词分类

**多阶段流水线的固有问题**：
- 各阶段独立优化，无法联合学习，产生次优解
- 枚举所有候选 subject-object 对引入大量负样本，训练效率低
- 额外的跟踪器无法端到端联合训练
- 3D 卷积等时序算子计算开销大

近年来 TPT [38] 提出了基于 transformer 的端到端框架，但仍采用两阶段范式（先检测+跟踪，再关系分类），依赖手绘轨迹或多阶段分离。

## Method

### 整体架构

OED 扩展 DETR [2] 至时空维度，直接以集合预测方式生成动态场景图。包含两大模块：

1. **Spatial Context Aggregation**（空间上下文聚合）
2. **Temporal Context Aggregation**（时序上下文聚合，PRM）

### 问题形式化

传统多阶段方法建模为链式分解：
- P(⟨s,p,o⟩|V) = P(p|s,o)P(s,o|D)P(D|V) 或
- P(⟨s,p,o⟩|V) = P(p|s,o)P(s,o|T)P(T|D)P(D|V)

OED 直接建模 P(⟨s,p,o⟩|Iᵢ, {I_ref})，不经过独立检测和跟踪阶段。

### Spatial Context Aggregation

1. **CNN Backbone + Transformer Encoder** → 提取每帧视觉特征 F = {f_T, f_T1, ..., f_Tn}

2. **Two Cascaded Decoders**：
   - **Pair-wise Instance Decoder**：用 N_q=100 个可学习查询 Q 捕获 pair-wise 实例相关信息。输出 Qp，作为下个解码器的 query
   - **Pair-wise Relation Decoder**：以 Qp 作为 query，聚合 pair-wise 关系特定的空间上下文。输出 Qr
   
   整体 pair-wise 特征 Qc = Concat(Qp, Qr)，维度 R^{Nq×2d_model}。级联设计的关键考量：实例特征可为谓词分类提供强先验（如 person-chair 大面积重叠 → sitting）。

### Temporal Context Aggregation — Progressively Refined Module (PRM)

PRM 以**多步渐进式筛选**方式聚合时序上下文，无需额外跟踪器或手绘轨迹：

1. 提取目标帧和参考帧的 pair-wise 特征 {Qc_T, Qc_T1,...,Qc_Tn}
2. 拼接参考帧 pair-wise 特征 Qc_ref
3. 对每个 pair-wise 特征用分类头打分：p(qc_i) = s_sub × s_obj × s_rel
4. 按分数排序，渐进筛选 Top-K 参考特征

公式化：
- Q'_i = CrossAttn(SelfAttn(Q'_{i-1}), Qc;ki_ref), i > 0
- Qc;ki_ref = Top-K(Qc_ref, ki)
- Q'_0 = Qc_T

K 值逐步减少：[80n, 50n, 30n]（n = 参考帧数），实现"更多上下文 vs 更少噪声"的权衡。

**PRM 的核心优势**：
- 长距离全局时序交互（不限于特定轨迹内的物体对）
- 渐进式筛选逐步过滤背景噪声（如 Fig.3 示意 towel 逐步被滤除）
- 无需额外跟踪器，支持端到端优化

### Training

- 使用匈牙利算法进行预测与 GT 的二分匹配
- 匹配损失组合：subject/object/predicate 分类 + subject/object 的 box 回归（L1 + GIoU）
- **Matched Predicate Loss**：仅对匹配 GT 的预测计算 predicate loss，而不将未匹配预测视为负样本——解决 Action Genome 中标注不完全的问题
- Predicate 分类使用 Focal Loss，应对类别不平衡

### Inference

- 对预测三元组按分数排序：s_sub × s_obj × s_rel
- NMS 过滤：对标签相同且 subject/object 大重叠区域的重复预测进行抑制

## Experiments

### 数据集

**Action Genome (AG)** [9]：234,253 帧场景图，从 ~10K Charades 视频中采样。35 个物体类 + 25 个谓词类（attention/spatial/contacting 三种类型）。同一对可能存在多个谓词。

### 评估指标

- Recall@K (R@K), K ∈ {10, 20, 50}
- **With Constraint** vs **No Constraints**
- **SGDET**: 场景图检测（同时检测对象和关系，IoU≥0.5）
- **PredCLS**: 谓词分类（给定 oracle 检测结果，仅分类谓词）

### 实现细节

- Backbone: ResNet-50
- Image Encoder, Pair-wise Decoder, Relation Decoder: 各 6 层 transformer
- 可学习查询数 N_q = 100
- 预训练初始化：Image Encoder + Pair-wise Decoder 在 MS-COCO 预训练，再在 AG 上微调
- PRM: 3 步渐进式交互，Top-K = [80n, 50n, 30n]
- 推理阈值：0.9
- PredCLS 初始化：用 Glove 嵌入初始化查询 + 位置嵌入

## Results

### 主要对比 — SGDET (Table 1)

| Method | R@10 W/C | R@20 W/C | R@50 W/C | R@10 No C | R@20 No C | R@50 No C |
|--------|---------|---------|---------|----------|----------|----------|
| STTran | 25.2 | 34.1 | 37.0 | 24.6 | 36.2 | 48.8 |
| APT | 26.3 | 36.1 | 38.3 | 25.7 | 37.9 | 50.1 |
| TR² | 26.8 | 35.5 | 38.3 | 27.8 | 39.2 | 50.0 |
| TEMPURA | 28.1 | 33.4 | 34.9 | 29.8 | 38.1 | 46.4 |
| DSG-DETR | 30.3 | 34.8 | 36.1 | 32.1 | 40.9 | 48.3 |
| TPT | — | — | — | 32.0 | 39.6 | 51.5 |
| **OED** | **33.5** | **40.9** | **48.9** | **35.3** | **44.0** | **51.8** |

**SGDET With Constraint**：OED 以平均 6.2% 的优势超越第二名（R@10: +3.2, R@20: +4.8, R@50: +10.6）。**SGDET No Constraint**：平均 +2.2%（R@10: +3.3, R@20: +3.1, R@50: +0.3）。

### 主要对比 — PredCLS (Table 1)

| Method | R@10 W/C | R@20 W/C | R@50 W/C | R@10 No C | R@20 No C | R@50 No C |
|--------|---------|---------|---------|----------|----------|----------|
| TR² | 70.9 | 73.8 | 73.8 | 83.1 | 96.6 | 99.9 |
| TPT | — | — | — | 85.6 | 97.4 | 99.9 |
| **OED** | **73.0** | **76.1** | **76.1** | 83.3 | 95.3 | 99.2 |

**PredCLS With Constraint**：OED 超越第二名平均 +2.1%。**No Constraint** 下略低于 TPT 和 TR²，原因为：(1) OED 作为单阶段方法无法显式利用 oracle tracking 信息；(2) TPT 使用多尺度特征，TR² 使用 CLIP 预训练模型（4M 图文对），这些额外信息带来了优势。

### 消融实验 — Spatial-Temporal Context Aggregation (Table 2)

| # | SA | TA | R@10 W/C | R@20 W/C | R@50 W/C | R@10 No C | R@20 No C | R@50 No C |
|:-:|:-:|:-:|:-------:|:-------:|:-------:|:--------:|:--------:|:--------:|
| 1 | | | 26.3 | 29.2 | 32.1 | 28.4 | 32.9 | 37.2 |
| 2 | ✓ | | 31.5 | 37.7 | 43.7 | 33.4 | 41.6 | 49.0 |
| 3 | ✓ | ✓ | 33.5 | 40.9 | 48.9 | 35.3 | 44.0 | 51.8 |

- SA（空间上下文聚合）带来大幅提升（R@50 W/C: 32.1→43.7, +11.6）
- TA（时序上下文聚合，PRM）带来进一步提升（R@50 W/C: 43.7→48.9, +5.2）

### 消融实验 — Spatial Context Designs (Table 3)

| # | CD | ML | R@10 W/C | R@20 W/C | R@50 W/C | R@10 No C | R@20 No C | R@50 No C |
|:-:|:-:|:-:|:-------:|:-------:|:-------:|:--------:|:--------:|:--------:|
| 1 | | | 26.3 | 29.2 | 32.1 | 28.4 | 32.9 | 37.2 |
| 2 | ✓ | | 27.2 | 30.3 | 33.7 | 29.2 | 34.0 | 38.4 |
| 3 | ✓ | ✓ | 31.5 | 37.7 | 43.7 | 33.4 | 41.6 | 49.0 |

- CD（Cascaded Decoders）缓解了多任务统一表示的优化困难
- ML（Matched Loss）有效缓解了 Action Genome 标注不完全问题

### 消融实验 — Temporal Context (Table 4)

| # | NPR | PR | R@10 W/C | R@20 W/C | R@50 W/C | R@10 No C | R@20 No C | R@50 No C |
|:-:|:--:|:--:|:-------:|:-------:|:-------:|:--------:|:--------:|:--------:|
| 1 | | | 31.5 | 37.7 | 43.7 | 33.4 | 41.6 | 49.0 |
| 2 | ✓ | | 32.3 | 39.7 | 47.8 | 34.0 | 42.7 | 50.6 |
| 3 | | ✓ | 33.5 | 40.9 | 48.9 | 35.3 | 44.0 | 51.8 |

- NPR（非渐进式，所有参考特征参与交互）已有效（R@50 W/C: 43.7→47.8）
- PR（渐进式筛选）进一步过滤噪声，获得增益（R@50 W/C: 47.8→48.9）

### Oracle 上限分析 (Table 5)

| # | R@10 W/C | R@20 W/C | R@50 W/C | R@10 No C | R@20 No C | R@50 No C |
|:-:|:-------:|:-------:|:-------:|:--------:|:--------:|:--------:|
| Oracle | 37.5 | 44.8 | 51.9 | 40.1 | 48.6 | 56.5 |
| Ours | 33.5 | 40.9 | 48.9 | 35.3 | 44.0 | 51.8 |

Oracle 选择（假设参考 query 精确匹配 GT）显著高于 PRM，说明参考特征选择仍有提升空间。

## Limitations

1. **PredCLS 受限**：单阶段范式无法直接利用 oracle tracking 信息，在 PredCLS No Constraint 设置下略逊于 TPT/TR² 等多阶段方法
2. **参考特征选择非最优**：Oracle vs PRM 差距（R@10 W/C: 37.5 vs 33.5）表明渐进式筛选远未达到上限
3. **仅在 Action Genome 评估**：泛化到其他视频场景图数据集（如 VidOR, OpenPVSG）有待验证
4. **ResNet-50 backbone**：未使用更强的 backbone（如 Swin Transformer），性能尚可进一步提升

## Reusable Claims

1. **DSGG 可建模为集合预测问题**：将 DSGG 从多阶段分解转为端到端集合预测，避免独立优化的次优解和枚举候选对的计算开销。这是该文的最高层次贡献。
2. **无跟踪器的时序聚合可行**：PRM 通过渐进式 Pair-wise 特征交互实现跨帧时序依赖建模，无需额外跟踪器或手绘轨迹，支持纯端到端优化。
3. **级联解码器解决多任务冲突**：Pair-wise Instance Decoder + Pair-wise Relation Decoder 级联设计优于单一解码器统一表示，关系分类可从实例检测先验中受益。
4. **Matched Predicate Loss 缓解不完全标注**：仅对匹配 GT 的预测计算 predicate loss，避免未匹配正样本被错误视为负样本。
5. **渐进式特征选择优于全连接交互**：多步骤逐渐收紧 Top-K 的策略优于一次性利用所有参考帧特征（滤除噪声关键）。

## Connections

- 在 **单阶段 DSGG** 方向上开创性工作，直接启发了后继的 [FDSG: Forecasting Dynamic Scene Graphs](fdsg-forecasting-dynamic-scene-graphs.md)（采用 OED 架构作为 SGG 基线，用 Neural SDE 扩展至预测任务）
- 与 **TPT**[38] 同为端到端方向，但 OED 实现真正的单阶段（TPT 仍为两阶段：检测+跟踪 → 关系分类）
- 与 **RelTR**[5] 等单阶段静态 SGG 共享集合预测范式，但扩展至视频时空域
- 对比 **DSG-DETR**[8]（基于 DETR 加轨迹匹配），OED 的无轨迹方案更简洁
- 实验基线覆盖了 **TEMPURA**[19]（无偏）等强 baseline，OED 在 SGDET 全面超越

## Open Questions

1. 能否将 PRM 扩展为可学习的参考帧选择策略（而非固定分数阈值排序）？
2. 更强的 backbone（如 Swin-L）下 OED 的性能上限？
3. OED 的 PredCLS No Constraint 为何显著低于 TPT（83.3 vs 85.6 R@10）？是否与 one-stage 的 query representation 的语义表达能力上限有关？
4. PRM 的 3 步渐进交互的 K 值设定是否需根据视频动态自适应调整？
5. Action Genome 以外的数据集（VidOR, OpenPVSG）上 OED 的泛化能力如何？

## Provenance

- **Evidence Level**: full-paper
- **Source**: CVPR 2024, 10 页正文
- **Extraction**: PyMuPDF 全文提取，47960 字符
- **Verification**: 文本完整，包含所有表格和参考文献
