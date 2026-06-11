---
title: "MOSA: Motion-Guided Semantic Alignment for Dynamic Scene Graph Generation"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - dynamic-scene-graph
  - motion-guidance
  - semantic-alignment
  - action-semantic-matching
  - long-tail-relationships
  - action-genome
  - video-scene-graph
  - arxiv-2026
raw_sources:
  - raw/sources/2026-arXiv-MOSA-Motion-Guided-Semantic-Alignment-for-Dynamic-SGG.pdf
  - raw/sources/2026-arXiv-MOSA-Motion-Guided-Semantic-Alignment-for-Dynamic-SGG.txt
paper:
  title: "MOSA: Motion-Guided Semantic Alignment for Dynamic Scene Graph Generation"
  authors:
    - Xuejiao Wang
    - Bohao Zhang
    - Changbo Wang
    - Gaoqi He
  year: 2026
  venue: arXiv 2026
  arxiv: null
  doi: null
  code: null
  project: null
  affiliations:
    - School of Computer Science and Technology, East China Normal University
    - School of Data Science and Engineering, East China Normal University
classification:
  label: MoSA
  task:
    - Dynamic Scene Graph Generation
    - Video Scene Graph Generation
  method_family:
    - Motion Feature Extraction
    - Motion-guided Interaction Module
    - Action Semantic Matching
    - Category-weighted Loss
    - Spatial-Temporal Transformer
  modality:
    - Video (RGB)
  datasets:
    - Action Genome
  metrics:
    - R@K
    - mR@K
evidence_level: full-paper
---

# MOSA: Motion-Guided Semantic Alignment for Dynamic Scene Graph Generation

## Citation

Xuejiao Wang, Bohao Zhang, Changbo Wang, Gaoqi He. "MOSA: Motion-Guided Semantic Alignment for Dynamic Scene Graph Generation." arXiv 2026.

## 摘要

本文提出 MoSA（Motion-Guided Semantic Alignment）框架，用于动态场景图生成（DSGG）。核心思想是通过显式建模物体对的运动属性（距离、速度、运动持续性、方向一致性）来增强关系特征，再通过跨模态语义对齐（CLIP文本嵌入）引入语言先验，最后用类别加权损失缓解长尾分布问题。

## 核心方法

### 1. Motion Feature Extractor (MFE)

对每个物体对 (oi, oj)，基于边界框坐标计算四种运动属性：

- **相对距离 dt**: 物体中心点之间的欧氏距离
- **接近速度 vt**: dt 的时间变化率，反映物体靠近或远离的趋势
- **滑动窗口平均 IoU (IoUt)**: K 帧内的平均交并比，评估位置稳定性
- **运动方向一致性 (CosSimt)**: 两物体位移方向向量的余弦相似度

四种属性拼接后经 MLP 生成高维运动特征。

### 2. Motion-guided Interaction Module (MIM)

以运动特征为 Query，空间特征为 Key/Value，通过注意力机制融合运动信息与空间特征，生成具备动态感知能力的关系统一特征。

### 3. Action Semantic Matching (ASM)

- 对所有谓词类别构造文本描述：`"a photo of a person {predicate phrase} a {object category}"`
- CLIP 文本编码器提取语义嵌入矩阵 Z ∈ R^{Nr×D}
- 视觉关系特征与文本嵌入点积匹配，得到跨模态相似度分数

### 4. 类别加权损失 (Category-Weighted Loss)

权重 αr = (1/ log nr) / Σ(1/ log nk)，降低高频类权重，提升低频类关注度。采用 Focal Loss 形式。

## 实验

### 数据集
- **Action Genome (AG)**: 在 Predicate Classification (PREDCLS)、Scene Graph Classification (SGCLS)、Scene Graph Detection (SGDET) 三项任务上评估
- **指标**: Recall@K (R@{10/20/50}) 和 mean Recall@K (mR@{10/20/50})
- **实现**: Faster R-CNN (ResNet101) + CLIP ViT-B/32，Adam lr=1×10⁻⁵

### 主要结果（Table 1 - Recall@K）

| Task | Setting | R@10 | R@20 | R@50 |
|------|---------|------|------|------|
| PREDCLS | With Constraint | 70.6 | 73.5 | 73.5 |
| PREDCLS | No Constraint | 27.6 | 39.2 | 50.1 |
| SGCLS | With Constraint | 26.7 | 35.5 | 38.3 |
| SGCLS | No Constraint | 57.2 | 64.7 | 66.8 |
| SGDET | With Constraint | 48.1 | 49.1 | 49.1 |
| SGDET | No Constraint | 82.8 | 96.5 | 99.9 |

- **PREDCLS (With Constraint)**: R@10=70.6%, R@50=73.5%，超越 SOTA 模型 TD2-Net（70.1%/73.1%）
- **SGDET (No Constraint)**: R@10=82.8%, R@50=99.9%，全面领先基线

### 长尾性能（Table 2 - mR@K）

| Task | Setting | mR@10 | mR@20 | mR@50 |
|------|---------|-------|-------|-------|
| PREDCLS | With Constraint | 44.3 | 47.7 | 47.8 |
| PREDCLS | No Constraint | 59.9 | 84.8 | 98.9 |
| SGCLS | With Constraint | 33.0 | 34.2 | 34.2 |
| SGCLS | No Constraint | 45.2 | 59.3 | 65.0 |
| SGDET | With Constraint | 17.6 | 23.3 | 25.2 |
| SGDET | No Constraint | 19.9 | 30.6 | 45.1 |

- **SGDET mR@50 (With Constraint)**: 25.2%，比 TD2-Net (22.3%) 提升 2.9%
- **SGDET mR@50 (No Constraint)**: 45.1%，比 TD2-Net (42.1%) 提升 3.0%
- 验证类别加权损失对长尾关系的有效性

### 消融实验（Table 3）

| Exp | 模块 | PREDCLS R@{10/20/50} | SGCLS R@{10/20/50} | SGDET R@{10/20/50} |
|-----|------|----------------------|---------------------|--------------------|
| 1 | w/o MFE | 68.9/71.9/71.9 | 25.9/34.5/37.3 | 46.8/47.6/47.6 |
| 2 | w/o MIM | 70.3/73.1/73.1 | 26.5/35.2/38.0 | 47.9/48.9/48.9 |
| 3 | w/o ASM | 69.9/72.6/72.7 | 26.3/35.1/37.8 | 47.7/48.6/48.6 |
| 4 | MoSA (完整) | 70.6/73.5/73.5 | 26.7/35.5/38.3 | 48.1/49.1/49.1 |

- MFE 去除造成最大性能下降（PREDCLS R@10 从 70.6% 降至 68.9%）
- ASM 去除后 PREDCLS R@10 下降 0.7%，SGDET R@50 下降 0.5%
- 每个模块均有正向贡献

### 定性分析

与 STTran 对比：STTran 将 `<person, sandwich>` 预测为 "holding"，MoSA 正确识别为 "eating"，展示了对细粒度动作关系的理解能力。

## 与相关工作的比较

- **[STTran]**: 仅使用空间-时间 Transformer，缺乏明确运动建模，混淆 "drink from" 和 "touch"
- **[TD2-Net]**: 当前 SOTA，MoSA 在 PREDCLS R@10 上从 70.1% 提升至 70.6%
- MoSA 的核心差异化：显式多维运动属性建模 + 跨模态语义对齐

## 主要贡献

1. **MoSA 架构**: 首次将显式运动属性建模（MFE）+ 运动引导交互（MIM）引入 DSGG
2. **ASM 模块**: 通过 CLIP 跨模态对齐引入语言先验，缓解语义相似关系混淆
3. **类别加权损失**: 缓解长尾分布问题，mR@50 在 SGDET 上提升 2.9-3.0%
4. **SOTA 性能**: 在 Action Genome 数据集 PREDCLS/SGCLS/SGDET 三项任务上取得最优或竞争性结果

## 局限性

- 运动属性计算依赖边界框精度，对检测误差敏感
- <person-object> 配对策略可能忽略非人物交互
- 仅在 Action Genome 单一数据集验证，未在 Charades/VID 等多元基准测试

## 关联页面

- [[salient-temporal-encoding-dynamic-sgg.md]] — 同期动态 SGG 工作
- [[gtr-grafting-then-reassembling-dynamic-scene-graph-generation.md]] — 动态 SGG 框架
- [[td2-net-toward-denoising-debiasing-video-scene-graph-generation.md]] — 去噪去偏 DSGG
