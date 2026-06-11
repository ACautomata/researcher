---
title: "Vision Relation Transformer for Unbiased Scene Graph Generation"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - scene-graph-generation
  - unbiased-sgg
  - transformer
  - local-level-encoding
  - multi-expert-learning
  - depth-modality
source_pages: []
raw_sources:
  - ../../../sources/scene-graph/2023-ICCV-Vision-Relation-Transformer-Unbiased-SGG.pdf
  - ../../../sources/scene-graph/2023-ICCV-Vision-Relation-Transformer-Unbiased-SGG.txt
paper:
  title: "Vision Relation Transformer for Unbiased Scene Graph Generation"
  authors:
    - Gopika Sudhakaran
    - Devendra Singh Dhami
    - Kristian Kersting
    - Stefan Roth
  year: 2023
  venue: ICCV 2023
  arxiv: "2308.09472"
  doi: null
  code: "https://github.com/visinf/veto"
  project: null
classification:
  label: "VETO + MEET"
  task:
    - Scene Graph Generation (SGG)
    - Unbiased Scene Graph Generation
  method_family:
    - Transformer-based Relation Encoder
    - Mutually Exclusive Expert Learning
  modality:
    - RGB
    - Depth (optional)
  datasets:
    - Visual Genome (VG150)
    - GQA (GQA200)
  metrics:
    - Recall@k (R@k)
    - mean Recall@k (mR@k)
    - Average of Recall and mean Recall (A@k)
evidence_level: full-paper
---

## Citation

> Gopika Sudhakaran, Devendra Singh Dhami, Kristian Kersting, Stefan Roth. "Vision Relation Transformer for Unbiased Scene Graph Generation." *Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)*, 2023. arXiv: 2308.09472. Code: [https://github.com/visinf/veto](https://github.com/visinf/veto).

## One-Sentence Contribution

提出 VETO（Vision rElation TransfOrmer）局部级实体关系编码器 + MEET（Mutually Exclusive ExperT）多专家去偏学习策略，在 VG 和 GQA 上实现 PredCls 任务 A@100 相对提升 47% (VG) 和 48% (GQA) 的同时，参数量仅为 SOTA 模型的约 1/10（20M 参数）。

## Problem Setting

SGG 任务：给定输入图像 I，检测实体 E = {ei}，为每对 (ei, ej) 预测关系谓词 pi→j，构建场景图 G = {(ei, pi→j, ej)}。

核心挑战：
1. **局部信息丢失**：传统 SGG 使用全局级 entity patches 进行关系编码，丢失了关系判别关键的局部级实体线索（如"wearing"需要关注"hat"和"head"的局部区域）
2. **偏置预测**：谓词长尾分布导致现有去偏方法仅能改善 head 或 tail 单方面性能，无法同时提升
3. **参数膨胀**：全局级 entity projections 导致模型参数过大

## Method

### VETO: Vision rElation TransfOrmer

VETO 是一种局部级实体关系编码器，包含三个核心模块：

1. **Cross-Relation Patch Generation (CRPG)**：将主体和客体的 RGB 特征 r 和几何特征 g 分别池化为 p×p 块，通道拼接后进行空间分块（patch size k），生成局部级 entity patches 序列。替换传统全局级全连接投影（Eq. 2），保留局部视觉线索。

2. **Cross-Modality Patch Fusion (CMPF)**：将 RGB patches 和 depth patches 进行低维投影后融合，减少 token 序列长度（从 2(p/k)² 到 (p/k)²）的同时增强跨模态依赖。

3. **Transformer-based Relation Encoder**：由 L 层 encoder 组成（含 MSA、MLP、LayerNorm），输入为 CMPF 输出的 local-level patches + learnable class token + 1D position embedding + 额外的 location 和 semantic tokens（Eq. 8-9），输出经线性投影到谓词类别数进行分类。

### MEET: Mutually Exclusive ExperT Learning

MEET 是一种多专家去偏学习策略：

1. 将谓词按频率降序排序并均分为 G 组
2. 每组分配一个互斥分类器专家 Eg，只负责该组的谓词分类
3. 训练时调整 in-distribution / out-of-distribution 采样频率，防止 OOD 样本淹没专家
4. 引入 OOD pseudo-label 处理 eval 阶段专家遇到的分类空间外样本
5. eval 时置信度低于 0.01 的预测直接丢弃（out-of-distribution 感知）

### 整体架构流程

RGB Feature Extractor → Proposal Network (Faster R-CNN) → Local-level Patch Generator (CRPG + CMPF) → Transformer Relation Encoder → MEET Multi-Expert Decoder → Relation Prediction

Depth feature extractor（可选）并行提取 depth maps，通过 CRPG 和 CMPF 整合。

### 与 Conventional SGG 对比

| 方面 | Conventional SGG | VETO |
|------|-------------------|------|
| Entity patch 类型 | Global-level（全连接投影） | Local-level（空间分块） |
| 信息保留 | 丢失局部线索 | 保留局部特征 |
| 参数量 | 大（全连接层密集） | 小（轻量级投影） |
| 去偏策略 | 单一分类器 + re-weighting | 互斥多专家（MEET） |

## Experiments

### 数据集

- **Visual Genome (VG150)**：150 个物体类别，50 个谓词类别。使用标准 split 与 prior work [3, 19, 22, 29–31, 40, 46, 49] 一致。
- **GQA (GQA200)**：采用 Dong et al. [7] 的 GQA200 split。

Depth maps 使用 Yin et al. [45] 的单目深度估计器生成。

### 评估协议

三个标准 SGG 子任务：
- **PredCls**：给定 gt boxes + gt labels，预测关系
- **SGCls**：给定 gt boxes，预测物体类别和关系
- **SGDet**：从零检测物体并预测关系

评估指标：Recall@k (R@k)、mean Recall@k (mR@k)、及两者平均值 A@k（k = 50, 100）。

### Baseline 方法

- IMP [7,29], KERN† [3], GB-Net+Rwt† [48], DT2-ACBS [6], PCPL† [41], GPS-Net [7,22], SG-CogTree [46], BGNN [19]
- VTransE [30,51], Motifs [30,49], VCTree [30,31], SHA [7]（含各种去偏变体：Rwt, TDE, PCPL, CogTree, DLFE, EMB, GCL, IETrans+Rwt, MEET）

### 实现细节

- Backbone：ResNeXt-101-FPN（冻结）+ Faster R-CNN 检测器（冻结）
- VETO：6 层 relation encoder，每层 6 个 attention heads，embedding size 576，patch size 2，pooled entity resolution 8
- 优化器：Adam，batch size 12，初始学习率 1.2×10⁻³
- 学习率调度：linear warmup 3K steps → decay with max decay step 3, patience 2，共训练 125K iterations
- 硬件：Nvidia A100 GPU
- VETO 总参数量：20M

### 消融实验

消融组件（在 VG SGCls 上评估）：
- L: Local-level Entity Patch Generation
- CR: Cross-Relation Patch Generation
- CM: Cross-Modality Patch Fusion
- D: Depth

| L | CR | CM | D | R@50/100 | mR@50/100 | A@50/100 |
|---|---|---|---|----------|-----------|----------|
| ✗ | ✗ | ✗ | ✗ | 32.0/33.5 | 7.6/8.3 | 19.8/20.9 |
| ✗ | ✗ | ✗ | ✓ | 33.2/34.5 | 7.0/7.6 | 20.1/21.1 |
| ✓ | ✗ | ✗ | ✗ | 34.8/36.2 | 14.1/15.1 | 24.5/25.7 |
| ✓ | ✗ | ✗ | ✓ | 35.1/36.4 | 13.0/14.1 | 24.1/25.3 |
| ✓ | ✗ | ✓ | ✓ | 35.1/36.3 | 14.4/15.4 | 24.8/25.9 |
| ✓ | ✓ | ✗ | ✗ | 35.4/36.6 | 15.2/16.1 | 25.3/26.4 |
| ✓ | ✓ | ✓ | ✓ | 35.1/36.3 | 16.1/17.1 | 25.6/26.7 |

关键发现：引入 local-level patch generation 后 A@k 提升约 23%；完整组件配置相对无 local-level patches 的 baseline 提升约 28%。

## Results

### VG (Table 1)

| 模型 | PredCls R@50/100 | PredCls mR@50/100 | PredCls A@50/100 | SGCls A@100 | SGDet A@100 |
|------|------------------|--------------------|--------------------|-------------|--------------|
| VETO (ours) | 64.2/66.3 | 22.8/24.7 | 43.5/45.5 | 24.4 | 20.5 |
| VETO + Rwt | 61.9/63.9 | 33.1/35.1 | 47.5/49.5 | 26.7 | 21.1 |
| **VETO + MEET** | **74.0/78.9** | **42.0/52.4** | **58.0/65.7** | **35.7** | **23.9** |
| Motifs + IETrans + Rwt [50] (prev best) | - | - | ~44.7(A@100) | - | - |
| SHA + GCL [7] | - | - | A@100 ~39 | - | - |

### GQA (Table 2)

| 模型 | PredCls R@50/100 | PredCls mR@50/100 | PredCls A@50/100 | SGCls A@100 | SGDet A@100 |
|------|------------------|--------------------|--------------------|-------------|--------------|
| VETO (ours) | 64.5/66.0 | 21.2/22.1 | 42.9/44.0 | 20.3 | - |
| **VETO + MEET** | **73.9/78.3** | **43.3/50.5** | **58.6/64.4** | **29.9** | - |

### 关键提升

- **VETO + MEET 在 PredCls A@100 上超越 Motifs + IETrans + Rwt [50] 47%（VG）/ 48%（GQA）**
- **首次在 PredCls 任务上同时达到 R@k 和 mR@k 的 SOTA**（此前方法只能优化其一）
- SGCls 上 mR@100 也达到 SOTA
- SGDet 上 VG 结果与 baseline 可比（略低，但 GQA 上全部三个任务均 SOTA）
- 参数量仅 20M，约为 GB-Net 的 1/20，其他 SGG 模型的 1/10

### 深度图影响

- VETO 在高质量 depth map (Yin et al.) 上相比低质量 depth map (VG-Depth.v1) 提升约 7%
- VETO 的 mR@k 相比 Depth-VRD [27] 提升超过 40%（VG-Depth.v1）和 50%（VG-Depth.v2）

### 谓词级分析

与 SHA + GCL [7] 相比，VETO + MEET 在所有频段（head, body, tail）均有提升，其中局部线索重要的谓词提升显著：attached to (781%)、part of (441%)。

### SGDet 敏感性分析

使用更弱的物体检测器时（mAP 下降 13% 和 32%），VETO 的 A@k 下降（3.5-4.2% 和 27-28%）略高于 Motifs，说明 VETO 对检测器质量更敏感。

## Limitations

1. **SGDet 性能**：在 VG 上的 SGDet 任务中，VETO + MEET 的 A@100 (23.9) 低于某些 baseline（如 VTransE + GCL 在 VG SGDet 上更高），说明检测噪声对局部级编码器影响更大。
2. **检测器敏感度**：敏感性分析（Table 6）显示 VETO 在检测器退化时性能下降比 Motifs 更快。
3. **深度图依赖**：虽然 depth 是可选的，但完全体模型依赖 monocular depth estimation 质量，在深度预测不准确时额外收益有限。
4. **MEET 组数选择**：未明确讨论谓词分组数 G 的敏感度分析和选择依据。

## Reusable Claims

> **Claim**: 局部级 entity patch 生成相比全局级投影可提升 SGG mR@k 约 23% A@k（VG SGCls），同时减少模型参数 10 倍以上。
> **Scope**: VG150, ResNeXt-101-FPN backbone
> **Evidence**: Table 3, Fig. 4
> **Confidence**: high

> **Claim**: 互斥专家学习（MEET）相比共享专家蒸馏（GCL）可在维持甚至提升 mR@k 的同时显著提升 R@k，实现 head/tail 平衡。
> **Scope**: VG150, GQA200, 多种 backbone（VTransE, Motifs, VCTree, SHA, VETO）
> **Evidence**: Tables 1, 2
> **Confidence**: high

> **Claim**: VETO + MEET 在 PredCls A@100 上超越 Motifs + IETrans + Rwt 47%（VG）和 48%（GQA）。
> **Scope**: VG150 PredCls, GQA200 PredCls
> **Evidence**: Section 5.2 (Q1)
> **Confidence**: high

> **Claim**: 高质量 depth map 可额外带来约 7% mR@k 提升，但设计不良的 depth fusion 机制可能适得其反（mR@k 下降）。
> **Scope**: VG150, ResNeXt-101-FPN
> **Evidence**: Tables 3, 4, 5
> **Confidence**: medium（仅比较两种 depth map 质量）

## Connections

- **RelTR** ([reltr-relation-transformer-scene-graph-generation.md](reltr-relation-transformer-scene-graph-generation.md))：同样使用 Transformer 做 SGG，但 VETO 强调局部级编码而非全局 attention；VETO + MEET 关注去偏，RelTR 关注端到端检测+关系预测。
- **CFA** ([compositional-feature-augmentation-for-unbiased-scene-graph-generation.md](compositional-feature-augmentation-for-unbiased-scene-graph-generation.md))：另一篇 ICCV 2023 去偏 SGG 工作，CFA 通过特征组合增强尾部类别，VETO + MEET 通过互斥专家建模 head/tail 差异。
- **SHA + GCL**：本文主要对比的 baseline。MEET 与 GCL 的共同点是多专家设计，区别在于专家是否互斥（GCL 共享知识蒸馏 → 头类性能下降）。
- **Depth-VRD [27]**：使用 depth 的 SGG baseline，VETO 在 depth fusion 设计上优于 Depth-VRD（mR@k 提升 40-50%）。
- **RelTR/Transformer-based SGG**：VETO 是 Transformer-based SGG 方法之一，使用 MSA 替代传统 RNN/GNN 关系编码。

## Open Questions

1. **MEET 的分组策略**：按频率排序后均分的假设是否最优？是否可自适应分组或动态分组？
2. **局部级 vs. 全局级互补**：局部级编码擅长细粒度关系（wearing, riding），全局级编码擅长场景上下文关系（in, on, near），两者能否互补组合？
3. **SGDet 差距**：VETO 在 SGDet 上 VG 结果较低的根本原因是检测噪声放大了局部编码的敏感性，是否有鲁棒化方案？
4. **深度图替代方案**：是否可以用 cross-attention 或隐式 3D 推理替代显式 depth estimation？
5. **扩展到更多关系类型**：VETO 在 50 个谓词的 VG 上验证，扩展到更大关系集（如 GQA 200 类场景图）时局部编码是否保持优势？

## Provenance

- **PDF**: [../../../sources/scene-graph/2023-ICCV-Vision-Relation-Transformer-Unbiased-SGG.pdf](../../../../../../sources/scene-graph/2023-ICCV-Vision-Relation-Transformer-Unbiased-SGG.pdf) (1.8MB)
- **Extracted text**: [../../../sources/scene-graph/2023-ICCV-Vision-Relation-Transformer-Unbiased-SGG.txt](../../../../../../sources/scene-graph/2023-ICCV-Vision-Relation-Transformer-Unbiased-SGG.txt) (60,586 chars)
- **arXiv**: [2308.09472](https://arxiv.org/abs/2308.09472)
- **Code**: [https://github.com/visinf/veto](https://github.com/visinf/veto)
- **Evidence level**: full-paper — 全文精读，提取全部 Table 1-6 数据
- **Review date**: 2026-06-09
