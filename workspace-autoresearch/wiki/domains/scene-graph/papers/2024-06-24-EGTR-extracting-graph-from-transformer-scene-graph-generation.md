---
title: "EGTR: Extracting Graph from Transformer for Scene Graph Generation"
type: paper
domain: scene-graph
status: active
created: 2026-06-10
updated: 2026-06-10
tags:
  - scene-graph-generation
  - transformer
  - one-stage
  - DETR
  - self-attention
  - relation-extraction
  - cvpr-2024
  - best-paper-candidate
raw_sources:
  - ../../../raw/sources/2024-04-02-EGTR-Extracting-Graph-from-Transformer-for-Scene-Graph-Generation.pdf
  - ../../../raw/sources/2024-04-02-EGTR-Extracting-Graph-from-Transformer-for-Scene-Graph-Generation.txt
related_pages:
  - sgtr-end-to-end-scene-graph-generation-with-transformer.md
  - reltr-relation-transformer-scene-graph-generation.md
  - dsgg-dense-relation-transformer-end-to-end-scene-graph-generation.md
  - is-ggt-iterative-scene-graph-generation-with-generative-transformers.md
evidence_level: full-paper
paper:
  title: "EGTR: Extracting Graph from Transformer for Scene Graph Generation"
  abbreviated: "EGTR"
  authors:
    - Jinbae Im
    - JeongYeon Nam
    - Nokyung Park
    - Hyungmin Lee
    - Seunghyun Park
  affiliations:
    - NAVER Cloud AI
    - NAVER
    - Korea University
  year: 2024
  venue: IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) 2024 (Best paper award candidate)
  doi: null
  arxiv: "2404.02072"
  code: "https://github.com/naver-ai/egtr"
  url: null
classification:
  label: Lightweight One-Stage Scene Graph Generator via DETR Self-Attention By-products
  task:
    - Scene Graph Generation (SGG)
  method_family:
    - DETR-based One-Stage SGG
    - Relation Extraction from Self-Attention By-products
    - Adaptive Smoothing (Curriculum Learning)
    - Connectivity Prediction (Auxiliary Task)
    - Gated Multi-layer Feature Aggregation
  modality: Image
  datasets:
    - Visual Genome (VG)
    - Open Images V6 (OI V6)
  metrics:
    - Recall@K (R@K)
    - mean Recall@K (mR@K)
    - AP50
    - micro-R@50
    - weighted mean AP (wmAP_rel, wmAP_phr)
    - Score (0.2×micro-R@50 + 0.4×wmAP_rel + 0.4×wmAP_phr)
    - zR@50 (zero-shot Recall)
    - FPS
    - #params

---

## 核心贡献

1. **EGTR 架构**：一种轻量级 one-stage SGG 模型，利用 DETR decoder 多层 self-attention 的 by-products（Q 和 K）直接提取关系图，无需额外的 triplet detector 或 triplet queries。仅 42.5M 参数（backbone + detector + relation head）。

2. **Adaptive Smoothing**：根据 object detection 的质量动态调整 relation label——训练初期聚焦目标检测，检测质量提升后逐渐过渡到多任务学习（连续课程学习）。

3. **Connectivity Prediction**：辅助任务，预测任意两个 object query 之间是否存在关系。训练时作为 hint loss，推理时用于过滤低置信度 triplet。

## 方法概述

### 关系提取（Relation Extractor）

- 从 DETR decoder 第 l 层 self-attention 的 query Q<sup>l</sup> 和 key K<sup>l</sup> 出发，将其视为 subject/object entity
- 对 query-key 对做 pairwise concat 得到 R<sub>a</sub><sup>l</sup> ∈ ℝ<sup>N×N×2d_model</sup>
- 同时利用最后一层 object queries Z<sup>L</sup> 做 pairwise concat 得到 R<sub>z</sub>
- 引入 **gated sum** 聚合所有层的 R<sub>a</sub><sup>l</sup> 和 R<sub>z</sub>，避免简单平均
- 3 层 MLP（ReLU）作为关系分类头，sigmoid 允许一对物体间存在多种关系

### Adaptive Smoothing

- 用 bipartite matching cost 衡量每个 object candidate 的检测不确定性 u<sub>i</sub>（sigmoid 映射）
- ground truth 关系 label 从 1 调整为 (1-u<sub>i</sub>)(1-u<sub>j</sub>)
- 训练早期检测差 → label 被抹平（接近 0）→ 模型专注检测 → 检测提升后 label 趋近 1 → 自然过渡到多任务学习

### 负例与非匹配采样

- 对 GT region、negative region、non-matching region 分别处理
- Hard negative mining：选择 top-k<sub>neg</sub>×|ℰ| 个最难负例
- Hard non-matching mining：从零填充区域选择 top-k<sub>non</sub>×|ℰ| 个困难样本

## 实验结果

### Visual Genome（SGDet, Graph-Constraint）

| 指标 | EGTR (Ours) | EGTR (LA, τ=0.5) | SSR-CNN | RelTR | SGTR |
|------|-------------|-------------------|---------|-------|------|
| #params (M) | 42.5 | 42.5 | 274.3 | 63.7 | 117.1 |
| FPS | 14.7 | 14.7 | 4.0 | 13.4 | 6.2 |
| AP50 | **30.8** | **30.8** | 23.8 | 26.4 | 25.4 |
| R@50 | 25.9 | **32.1** | — | — | — |
| mR@50 | — | — | 17.9 | — | — |
| R@100 | 25.1 | 31.1 | — | — | — |
| mR@100 | — | — | 21.4 | — | — |

> **说明**：LA = logit adjustment (SSR-CNN 提出的尾部谓词处理技术)。EGTR 的 AP50 在所有 one-stage 方法中最高（30.8），显著优于 SSR-CNN (23.8) 等 triplet detection 模型。所有 EGTR 变体共用同一检测器，AP50 一致，R@k 通过不同 LA τ 调节。

### Open Image V6

| 方法 | Score | micro-R@50 | wmAP_rel | wmAP_phr |
|------|-------|-----------|----------|----------|
| EGTR (Ours) | **48.6** | **75.0** | **42.0** | **41.9** |
| SSR-CNN | 49.4 | 76.7 | 41.5 | 43.6 |

> EGTR 在 OI V6 上取得 competitive 表现，score 48.6 vs SOTA SSR-CNN 的 49.4，但参数量仅为 SSR-CNN 的 1/6。

### Ablation 关键发现

| 配置 | R@50 | mR@50 |
|------|------|-------|
| Base（无任何技巧） | 26.6 | 5.3 |
| + adaptive smoothing | 28.3 | 6.5 |
| + connectivity loss | 29.6 | 7.0 |
| + sampling | 28.9 | 7.1 |
| **All techniques** | **30.2** | **7.9** |

- 仅用 attention by-products（Q&K）做关系源，效果与仅用最后一层 hidden states 相当
- **Q&K + Z<sup>L</sup>** 结合达到最佳性能（R@50 30.2, mR@50 7.9）
- 所有 proposed techniques 组合获得最大提升

### 零样本性能

- 无 frequency baseline 时：zR@50 = **2.1**，R@50 下降 0.2，mR@50 下降 0.6

### 检测性能分析（Tab. 6）

| 方法 | AP50 | AP50_rel | AP50_no-rel |
|------|------|---------|-----------|
| Iterative SGG† | 27.7 | — | — |
| SSR-CNN† | 23.8 | — | — |
| EGTR (Ours) | **30.8** | — | — |

> EGTR 在无关系物体上的检测（AP50_no-rel）显著优于 triplet detection 模型，证明其能检测完整场景图（含孤立物体）。

## 核心 Insight

- **Self-attention by-products 富含关系信息**：预训练 DETR 的 attention weights 可直接构成 plausible attention graph（Fig. 1c）。
- **无需额外 triplet detector**：从 query-key 对中提取关系，参数量仅 42.5M（SSR-CNN 的 1/6），速度 14.7 FPS（SSR-CNN 的 3.7 倍）。
- **检测-关系依赖建模**：adaptive smoothing 是第一篇显式建模"关系提取依赖目标检测质量"的论文。

## 局限

- 在 open-world / long-tail 场景下仍需套用 logit adjustment 等技术
- 零样本性能仍有提升空间（zR@50=2.1）
- 仅在 ResNet-50 backbone 上实验，更大 backbone 效果待验证

## 与相关方法的关系

- **SGTR/RelTR（object-triplet detection）**：EGTR 不需要额外 triplet queries，直接从检测器的 Q/K 提取关系
- **SSR-CNN（triplet detection）**：EGTR 有显式 object detector，能检测无关系物体，参数量大幅减少
- **Relationformer**：EGTR 在利用 final hidden states 外还使用了 attention by-products

## 参考文献

- Z. Liu et al., "Structured Sparse R-CNN for Scene Graph Generation" (SSR-CNN), 2023
- R. Li et al., "SGTR: End-to-end Scene Graph Generation with Transformer" (SGTR), CVPR 2022
- Y. Cong et al., "RelTR: Relation Transformer for Scene Graph Generation", 2023
- N. Carion et al., "End-to-End Object Detection with Transformers" (DETR), ECCV 2020
- X. Zhu et al., "Deformable DETR: Deformable Transformers for End-to-End Object Detection", ICLR 2021
