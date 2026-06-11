---
title: "THYME: Temporal Hierarchical-Cyclic Interactivity Modeling for Video Scene Graphs in Aerial Footage"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - video-scene-graph
  - hierarchical-graph
  - cyclic-attention
  - aerial-footage
  - dataset
raw_sources:
  - ../../../sources/scene-graph/2025-arXiv-THYME-Temporal-Hierarchical-Cyclic-Interactivity-for-Dynamic-SGG.pdf
  - ../../../sources/scene-graph/2025-arXiv-THYME-Temporal-Hierarchical-Cyclic-Interactivity-for-Dynamic-SGG.txt
paper:
  title: "THYME: Temporal Hierarchical-Cyclic Interactivity Modeling for Video Scene Graphs in Aerial Footage"
  authors:
    - Trong-Thuan Nguyen
    - Pha Nguyen
    - Jackson Cothren
    - Alper Yilmaz
    - Minh-Triet Tran
    - Khoa Luu
  year: 2025
  venue: arXiv preprint
  arxiv: "2507.09200"
  doi: null
  code: null
  project: null
classification:
  label: THYME
  task:
    - Video Scene Graph Generation (VidSGG)
    - Dynamic Scene Graph Generation
  method_family:
    - Hierarchical Feature Aggregation
    - Cyclic Temporal Attention
    - Graph Transformer
  modality:
    - Video
    - Aerial Footage
    - Ground-view Video
  datasets:
    - ASPIRe
    - AeroEye-v1.0 (New)
  metrics:
    - R@20
    - R@50
    - R@100
    - mR@20
    - mR@50
    - mR@100
evidence_level: full-paper
---

# THYME: Temporal Hierarchical-Cyclic Interactivity Modeling for Video Scene Graphs

## Citation

Trong-Thuan Nguyen, Pha Nguyen, Jackson Cothren, Alper Yilmaz, Minh-Triet Tran, Khoa Luu. "THYME: Temporal Hierarchical-Cyclic Interactivity Modeling for Video Scene Graphs in Aerial Footage." arXiv:2507.09200, 2025.

## One-Sentence Contribution

提出 THYME 方法，将 **层级特征聚合**（hierarchical feature aggregation）与 **循环时序注意力**（cyclic temporal attention）结合，以同时捕获多尺度空间细节和长程时序依赖，并贡献带五种交互类型标注的航拍数据集 AeroEye-v1.0。

## Problem Setting

**出发点**：现有 VidSGG 方法可分为两类：
1. **帧级方法**（SGTR, RelTR, EGTR, DSGG）：每帧独立推理，产生帧间关系不一致（predicate flickering），难以检测短暂/细微交互
2. **视频级方法**（HIG, CYCLO, PVSG, TRACE, DSG-DETR）：整合时序上下文，但容易忽视快速变化的交互动态，在航拍/倾斜视角下细粒度空间精度下降

**核心挑战**：同时保持每帧的细粒度空间结构与帧间一致的时序关系过渡。

**评估协议**：
- Recall (R) 和 mean Recall (mR) 在 top-20、top-50、top-100 三个阈值
- 五个交互类型分别评估：Appearance（单演员属性）、Situation（单演员环境）、Position（空间关系）、Interaction（动态交互）、Relation（功能关系）
- 数据集：ASPIRe（地面视角，1.5K 视频，1.6M 帧）和 AeroEye-v1.0（航拍，2.3K 视频，261.5K 帧）

## Method

THYME 的四阶段架构（图 3）：

### Stage 1: Per-Frame Feature Extraction
- 使用 DETR 目标检测器对每帧提取 N_t 个 object query embeddings q_i^{(t)} ∈ ℝ^{d₀}
- 每帧对象实例集合定义为 V_t = {S_i^{(t)} | S_i^{(t)} ≡ q_i^{(t)}}

### Stage 2: Hierarchical Feature Aggregation
- 初始化：F^{(0)}_t(S_i^{(t)}) = q_i^{(t)}
- 在 L_h 个层级上逐层聚合邻居信息（同一帧内所有对象）
- 每层通过注意力机制计算相关性权重 a_{ij}^{(t)}，加权聚合邻居特征后经 ReLU 激活
- 参数 W^{(l)} ∈ ℝ^{d_l × d_{l-1}} 和偏置 b^{(l)} 可学习
- 越深的层级产生更丰富的多尺度特征表示

### Stage 3: Temporal Refinement via Cyclic Attention
- 对每个跨帧跟踪对象 S_i，构建时序序列 {X_{t'}(S_i)}，其中 X_{t'}(S_i) = F^{(L_h)}_{t'}(S_i)
- 通过可学习矩阵 W^Q、W^K、W^V 投影到 Q、K、V
- **关键创新**：循环注意力（Cyclic Attention, CA）使用模运算使最后一帧也可以 attend 到第一帧：
  CA_{t'}(S_i) = Σ_τ α_{t',τ}(S_i) · V_{(t'+τ) mod T'}(S_i)
- 经 Layer Normalization 和前馈网络后得到精炼特征 \hat{F}(S_i)

### Stage 4: Scene Graph Construction
- 视频场景图 G = (V, E)，节点 V = {S_i | \hat{F}(S_i) ∈ ℝ^{d_{L_h}}}
- 关系表示从 DETR decoder 的 self-attention 输出提取，经过门控机制融合各 decoder layer
- 最终通过 MLP_rel 输出每对物体的 predicate 类别得分

### Loss Function
- 采用 Focal Loss（与 HIG/CYCLO 一致）
- 总损失聚合各层级的损失：ℒ_total = Σ_{l=1}^{L_h} ℒ(F^{(l)}_t(S_i^{(t)}))

## AeroEye-v1.0 Dataset

基于 AeroEye [33] 扩展，新增五种交互类型标注，覆盖航拍、倾斜、地面三个视角：

| 属性 | 数量 |
|------|------|
| 视频数 | 2,260 |
| 总帧数 | 261,503 |
| 目标类别 | 57 |
| 关系谓词 | 687（比 AeroEye 的 384 增加近一倍） |
| 场景数 | 29 |
| Appearance 谓词 | 157 |
| Situation 谓词 | 128 |
| Position 谓词 | 135（~752K 标注） |
| Interaction 谓词 | 142（~318K 标注） |
| Relation 谓词 | 125（~178K 标注） |
| 总 bbox | >200 万 |

优于现有 VidSGG 数据集在视频数、帧数、谓词词汇量和视角多样性的综合覆盖。

## Experiments

### Implementation Details
- **Backbone**：DETR 目标检测器
- **数据集**：
  - ASPIRe：1.5K 视频，1.6M 帧，含五种交互类型，地面视角
  - AeroEye-v1.0：2.3K 视频，261.5K 帧，航拍视角
- **评估指标**：R@20/50/100, mR@20/50/100
- **Baselines**：IMP, MOTIFS, VCTree, GPSNet, STTran, TEMPURA, HIG, CYCLO

### Ablation Studies

**1. 层级数（表 II）**
- 1/4 层级 → Appearance R@20 14.12% → 全深度 16.52%
- 1/4 层级 → Situation R@20 4.33% → 全深度 5.53%
- 1/4 层级 → Position R@20 12.32% → 全深度 15.52%
- 1/4 层级 → Interaction R@20 10.87% → 全深度 13.07%
- 1/4 层级 → Relation R@20 13.03% → 全深度 16.03%
- **趋势**：3/4 深度时大部分收益已获得，之后边际递减，提示存在最优深度

**2. 时序注意力机制（表 III）— 核心消融**
| 机制 | Appearance R@20 / mR@20 |
|------|------------------------|
| Standard Attention | 15.12 / 0.65 |
| **Cyclic Attention** | **16.52 / 0.68** |

| 机制 | Situation R@20 / mR@20 |
|------|------------------------|
| Standard Attention | 4.83 / 0.59 |
| **Cyclic Attention** | **5.53 / 0.61** |

| 机制 | Position R@20 / mR@20 |
|------|------------------------|
| Standard Attention | 13.42 / 0.92 |
| **Cyclic Attention** | **15.52 / 1.05** |

| 机制 | Interaction R@20 / mR@20 |
|------|--------------------------|
| Standard Attention | 11.07 / 0.14 |
| **Cyclic Attention** | **13.07 / 0.16** |

| 机制 | Relation R@20 / mR@20 |
|------|-----------------------|
| Standard Attention | 14.03 / 0.85 |
| **Cyclic Attention** | **16.03 / 0.95** |

循环注意力带来 **1.4%–2.0% 的 R@20 提升**，在 Position 和 Interaction 上尤其显著。

**3. 时序窗口大小（表 IV）**
- 1/2 窗口 → Appearance R@20 15.32% → 全窗口 16.52%
- 全窗口在 3/4 窗口基础上收益边际但始终最优

## Results

### ASPIRe 数据集（表 V）

| Method | Position R@20 | Position mR@20 | Interaction R@20 | Interaction mR@20 | Relation R@20 | Relation mR@20 |
|--------|--------------|---------------|-----------------|------------------|--------------|---------------|
| STTran | 13.52 | 0.51 | 12.27 | 0.14 | 12.03 | 0.51 |
| TEMPURA | 13.71 | 0.85 | 12.53 | 0.17 | 15.29 | 0.84 |
| HIG | 13.02 | 0.09 | 12.02 | 0.11 | 10.26 | 0.29 |
| CYCLO | 16.32 | 0.97 | 15.27 | 0.20 | 18.34 | 0.90 |
| **THYME** | **18.52** | **1.22** | **19.52** | **0.32** | **21.02** | **1.12** |

**Appearance**：THYME 18.23 R@20 / 1.07 mR@20（HIG: 15.02/0.60）
**Situation**：THYME 6.57 R@20 / 0.26 mR@20（HIG: 5.01/0.56）

THYME 在 **所有双演员属性**（Position/Interaction/Relation）上超过 STTran、TEMPURA、HIG 和 CYCLO，尤其在 Interaction 上 R@20 领先 CYCLO 4.25%。

### AeroEye-v1.0 数据集（表 VI）

| Method | Position R@20 | Position mR@20 | Interaction R@20 | Interaction mR@20 | Relation R@20 | Relation mR@20 |
|--------|--------------|---------------|-----------------|------------------|--------------|---------------|
| STTran | 12.22 | 0.75 | 10.52 | 0.08 | 8.52 | 0.22 |
| HIG | 12.51 | 0.85 | 11.57 | 0.19 | 9.57 | 0.25 |
| TEMPURA | 13.22 | 0.82 | 11.81 | 0.12 | 11.47 | 0.33 |
| CYCLO | 13.52 | 0.75 | 12.61 | 0.14 | 14.51 | 0.83 |
| **THYME** | **15.52** | **1.05** | **13.07** | **0.16** | **16.03** | **0.95** |

**Appearance**：THYME 16.52 R@20 / 0.68 mR@20（HIG: 14.51/0.55）
**Situation**：THYME 5.53 R@20 / 0.61 mR@20（HIG: 4.53/0.57）

THYME 在 AeroEye-v1.0 的全部交互类型上超越所有 baseline。双演员属性上 R@20 超过次优方法（CYCLO）**2–3%**。

## Limitations（待验证）

基于论文内容归纳的可能局限：
1. 推理速度未报告，层级聚合+循环注意力对计算开销的影响未知
2. 在极低帧率或严重遮挡场景下的鲁棒性未专门讨论（定性分析提到了 CYCLO 失败案例但未量化 THYME 的改进）
3. 代码未公开，结果独立可复现性待验证
4. Temporal window 消融显示 3/4→全窗口收益边际，但最优窗口数可能数据集相关，未讨论泛化性

## Reusable Claims

- **层级聚合 + 循环注意力 = 有效组合**：单独的层级聚合（HIG）或循环注意力（CYCLO）都不能同时解决多尺度空间和长程时序问题，二者结合提供互补收益
- **循环注意力优于标准自注意力**：在 AeroEye-v1.0 上所有五项交互类型一致提升 1.4–2.0% R@20
- **航拍场景的独特挑战**：高目标密度、不同尺度、复杂空间关系，需要更丰富的谓词词汇（687 vs. AeroEye 的 384）
- AeroEye-v1.0 是目前唯一标注全部五种交互类型的航拍 VidSGG 数据集

## Connections

- **HIG [32]**：THYME 的层级聚合继承自 HIG，但 HIG 缺乏时序精炼
- **CYCLO [33]**：THYME 的循环注意力继承自 CYCLO，但 CYCLO 缺乏层级聚合
- **PVSG [52]**：均做视频场景图，但 PVSG 侧重 panoptic 分割，THYME 侧重层级+循环时序建模
- **STTran / TEMPURA**：STTran 用 spatio-temporal transformer，TEMPURA 在其基础上加去偏置，两者在双演员属性上落后 THYME
- **DSGG [12]**、**RelTR [5]**、**EGTR [16]**：帧级方法，THYME 通过时序精炼解决帧间不一致
- **AeroEye [33]**：AeroEye-v1.0 的前身，THYME 新增 appearance/situation/interaction/relation 四种交互类型标注

## Open Questions

- THYME 的层级数 L_h 如何最优选择（存在边际递减阈值）？
- 循环注意力在非航拍场景（如电视剧、体育比赛长镜头）中是否同样有效？
- THYME 能否扩展到 streaming / online 设置（当前是离线批处理）？
- 是否可以通过多模态融合（音频、文本）进一步提升 AeroEye-v1.0 上的结果？

## Provenance

- 来源：arXiv:2507.09200，2025 年 7 月
- 提取方式：PyMuPDF 全文提取至 raw/sources/ 文本文件
- 分析时间：2026-06-09
- 分析状态：全文精读，所有表格数字已捕获
