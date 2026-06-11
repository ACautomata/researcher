---
title: "Visual Distant Supervision for Scene Graph Generation"
type: paper
domain: scene-graph
status: active
created: 2026-06-10
updated: 2026-06-10
tags:
  - scene-graph-generation
  - weakly-supervised
  - distant-supervision
  - knowledge-base
  - ICCV-2021
  - denoising
  - EM-optimization
raw_sources:
  - ../../../raw/sources/2021-10-01-visual-distant-supervision-scene-graph-generation.pdf
  - ../../../raw/sources/2021-10-01-visual-distant-supervision-scene-graph-generation.txt
related_pages:
  - linguistic-structures-weak-supervision-visual-scene-graph-generation.md
  - 2020-06-16-weakly-supervised-visual-semantic-parsing.md
  - ppr-fcn-weakly-supervised-scene-graph-generation.md
evidence_level: full-paper
paper:
  title: "Visual Distant Supervision for Scene Graph Generation"
  authors:
    - Yuan Yao
    - Ao Zhang
    - Xu Han
    - Mengdi Li
    - Cornelius Weber
    - Zhiyuan Liu
    - Stefan Wermter
    - Maosong Sun
  year: 2021
  venue: "Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV), 2021"
  arxiv: 2103.15365
  doi: null
  code: "https://github.com/thunlp/VisualDS"
  project: null
classification:
  label: "VisualDS — 视觉远距离监督的场景图生成"
  task:
    - Scene Graph Generation (SGGen)
    - Weakly-Supervised Scene Graph Generation (WSSGG)
    - Distantly-Supervised Scene Graph Generation
  method_family:
    - Commonsense Knowledge Base Construction
    - KB-Image Alignment
    - EM-based Denoising Framework
    - External Semantic Signals (CLIP) for Relation Scoring
  modality:
    - Image
    - Text (captions)
  datasets:
    - Visual Genome (VG)
    - Conceptual Captions
  metrics:
    - Recall@50 (R@50)
    - Recall@100 (R@100)
    - macro-Recall@50 (mR@50)
    - macro-Recall@100 (mR@100)
    - Precision@K (human evaluation)
---

## Citation

Yao, Y., Zhang, A., Han, X., Li, M., Weber, C., Liu, Z., Wermter, S., & Sun, M. (2021). Visual Distant Supervision for Scene Graph Generation. *Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)*, 15816–15826.

## One-Sentence Contribution

提出视觉远距离监督（Visual Distant Supervision），通过将常识知识库与图像对齐自动生成大规模标注数据，实现无需人工标注的场景图模型训练，并配套 EM 迭代去噪框架处理标签噪声。

## Problem Setting

- **任务**：场景图生成（Scene Graph Generation），从图像中识别物体及其关系。
- **核心挑战**：传统 SGG 依赖大规模人工标注，标注工作量大且存在长尾分布（>98% 的 top-3000 关系类别缺乏足够标注实例）。
- **现有方案局限**：
  - 弱监督方法（caption 解析）受 reporting bias 影响，只能覆盖少数显著关系
  - 半监督方法（Few seed instances）仍需要与关系数线性增长的人工标注
  - 两者都无法系统性地缓解长尾问题
- **本文方案**：完全不使用人工标注数据，通过常识知识库和图像的自动对齐提供远程监督信号。

## Method

### 1. 知识库构建

- 从 **Conceptual Captions**（330 万图像描述）中提取关系三元组
- 使用基于规则的文本解析器进行提取
- 结果知识库：**18,618** 种物体类别、**63,232** 种关系类别、**1,876,659** 个不同关系三元组
- 每对物体平均有 1.94 个关系候选

### 2. 知识库与图像对齐

- 使用 Visual Genome 的物体标注（边界框和类别），也可用通用物体检测器
- 对每对物体，从知识库中检索所有关系标签作为候选
- **重叠约束**：仅当 subject 和 object 边界框有重叠区域时才分配远程标签
- 对齐后的远程标签覆盖 Visual Genome 中 70.3% 的关系标签

### 3. EM 去噪框架（蒸馏监督设置）

将远程标注数据中的真实关系标签视为隐变量，迭代估计概率关系标签并消除噪声：

**E 步（估计）**：
- **初始迭代（t=1）**：使用 CLIP 作为外部语义信号，测量文本关系三元组与对应视觉物体对的语义相关性
  - 视觉输入：物体对边界框覆盖区域遮罩后的图像
  - 文本输入：三元组拼接文本片段
  - 归一化得到关系概率分布 e
  - 初始化 r¹ = e
- **非初始迭代（t>1）**：场景图模型内部预测与外部语义信号的凸组合
  - rᵗ = ω·f(s,o;θᵗ⁻¹) + (1-ω)·e
  - 丢弃 top-k% NA 关系 logit 的噪声物体对

**M 步（最大化）**：
- 通过最大化熵加权似然函数优化模型参数 θ
- 对远程标签中的 positive 关系用 log f，negative 关系用 log(1-f)

### 4. 半监督框架

整合远程标注数据 DS 与人工标注数据 DL：

- **E 步**：由微调后的模型估计 DS 的远程标签（无外部语义信号，因为人工标注提供更强去噪信号）
- **M1 步**：在 DS 上从头预训练模型
- **M2 步**：在 DL 上微调模型

### 5. 实验设置

- **数据集**：Visual Genome，采用 Chen et al. [5] 的精炼关系方案（20 个关系类别）
- **Backbone**：ResNeXt-101-FPN + Neural Motif 架构
- **评估协议**：三模式（PredCls / SGCls / SGDet），微召回率（R@K, mR@K, K=50,100）

## Experiments

### 数据集

| 数据集 | 用途 | 规模 |
|--------|------|------|
| Conceptual Captions | 知识库构建（文本提取） | 330 万图文对 |
| Visual Genome (VG) | 远程监督对齐 + 评估 | 标准划分（Chen et al. [5] 精炼方案，20 关系类别） |
| Visual Genome (VG) | 附录实验 | 50 关系类别 |

### Baseline 方法

| 类别 | 方法 | 说明 |
|------|------|------|
| 频率基线 | Freq [54] | 预测物体对间最频繁关系 |
| | Freq-Overlap [54] | 添加重叠约束 |
| 小样本基线 | Decision Tree [33] | 每类 10 个人工 seed 实例 |
| 半监督 | Label Propagation [62] | 基于社区传播 seed 标签 |
| | Limited Labels [5] | SOTA 半监督 SGG（soft labels） |
| 弱监督 | Weak Supervision† | 基于 caption 解析的关系标签 |
| 全监督 | Neural Motif [54] | ResNeXt-101-FPN backbone |
| 去噪基线 | Cleanness Loss [23] | 启发式降权高损失标签 |

### 训练设置

- **Backbone 架构**：ResNeXt-101-FPN + Neural Motif
- **所有神经模型**基于相同架构以实现公平比较
- **去噪框架**：ω 为加权超参数，NA 丢弃比例 k 在附录中说明
- **硬件**：not reported in main text
- **Epochs / Learning rate / Batch size**：not reported in main text（参见附录）

### 消融实验

| 变体 | 组件 |
|------|------|
| Raw Label | 仅原始远程关系标签 |
| Raw Label + EXT | 添加 CLIP 外部语义信号（仅用于初步评分，不迭代训练） |
| Motif | 基于 Neural Motif 在原始远程标签上训练 |
| Motif + DNS | 添加 EM 去噪框架 |
| Motif + DNS + EXT | 去噪 + 外部语义信号（CLIP） |
| Motif + Pretrain | 预训练 → 人工数据微调 |
| Motif + DNS (SS) | 半监督去噪框架 |
| DNS iterations | 迭代 1 vs 迭代 2 去噪效果 |

## Results

### 主要结果（Table 1）—— Visual Genome 20 关系类别

**Predicate Classification（PredCls）**：

| 方法 | R@50 | R@100 | mR@50 | mR@100 |
|------|------|-------|-------|--------|
| Weak Supervision† | 44.96 | 47.19 | 24.58 | 27.14 |
| Limited Labels [5] | 49.68 | 50.73 | 37.43 | 38.91 |
| **DS: Motif + DNS + EXT (Ours)** | **53.40** | **56.54** | **37.68** | **41.98** |
| FS: Motif [54] | 67.93 | 70.20 | 52.65 | 55.41 |
| **SS: Motif + DNS (Ours)** | **76.28** | **77.98** | **60.20** | **63.61** |

**Mean（12 项指标平均）**：
- DS Motif + DNS + EXT: **29.76**（超越半监督 Limited Labels 27.23 和弱监督 20.76）
- FS Motif: 38.09
- SS Motif + DNS: **44.31**（超越 FS Motif 6.22）

**Key findings**：
- SS 模型在 PredCls R@50 上超过 FS Motif 8.3（76.28 vs 67.93）
- SS 模型在 PredCls mR@50 上超过 FS Motif 7.8（60.20 vs 52.65）
- DS 模型超越弱监督和半监督基线（无需任何人工标注）
- SS 模型通过简单的预训练+微调（Motif + Pretrain）即可超过 FS 模型（Mean 42.67 vs 38.09）

### 去噪框架效果（Table 2）

**DS 设置 PredCls**：
- Motif (不迭代): R@50=50.23, mR@50=33.99
- Motif + DNS (iter2): R@50=51.54, mR@50=36.93
- Motif + DNS + EXT (iter2): R@50=53.40, mR@50=37.68

**SS 设置 PredCls**：
- Motif + DNS (iter1): R@50=73.50, mR@50=61.40
- Motif + DNS (iter2): R@50=76.28, mR@50=60.20

Key findings：DNS 在 DS 和 SS 设置中一致提升性能；EXT（CLIP）进一步改善 DS 结果且加速收敛；SS 框架在第一次迭代即已达接近最优性能。

### 理想知识库分析（Table 3）

| 方法 | R@50 | R@100 | mR@50 | mR@100 |
|------|------|-------|-------|--------|
| DS Raw Label | 35.62 (+5.01) | 39.78 (+6.30) | 34.83 (+13.85) | 39.45 (+16.20) |
| DS Motif + DNS + EXT | 55.54 (+2.14) | 58.99 (+2.45) | 50.87 (+13.19) | 55.69 (+13.71) |
| FS Motif | 67.93 | 70.02 | 52.65 | 55.41 |

使用理想 KB 后，DS 模型宏召回大幅提升，mR@50 从 37.68→50.87（+13.19）。

### 人工评估精度（Table 4）

| 方法 | P@10 | P@20 | mP@10 | mP@20 |
|------|------|------|-------|-------|
| DS Raw Labels | 12.07 | 10.85 | 11.41 | 12.04 |
| DS Motif + DNS + EXT | 31.93 | 25.29 | 24.79 | 20.79 |
| FS Motif | 42.22 | 31.09 | 39.60 | 29.22 |
| **SS Motif + DNS** | **50.58** | **38.68** | **47.49** | **38.52** |

SS 模型在精度上全面超越 FS 模型，P@10 高 8.36（50.58 vs 42.22）。

## Limitations

1. **去噪局限于孤立的物体对**：每个物体对的标签独立去噪，未考虑场景图整体的结构一致性
2. **知识库不完整**：依赖从 caption 中提取的常识知识库，relation/object 名称与图像标注存在匹配偏差
3. **远程监督可能引入额外偏置**：对场景图模型可能产生未知的系统性偏置，文中未深入分析
4. **需要物体边界框**：当前使用 Visual Genome 的物体标注，在开放域图像中需依赖物体检测器
5. **CLIP 作为外部信号**：CLIP 虽未使用人工标注的关系数据，但可能在 image-caption 预训练中隐式编码了关系知识

## Reusable Claims

> **Claim**: 视觉远程监督可以在不依赖任何人工标注的情况下训练场景图模型，在 PredCls 上实现 R@50 53.40%，超越弱监督基线（44.96%）和半监督基线（49.68%）。
> **Evidence**: Table 1, PredCls 列
> **Confidence**: high

> **Claim**: 远程监督预训练后微调人工数据（半监督设置）可在 PredCls R@50 上超出全监督 Motif 8.3 个点（76.28 vs 67.93）。
> **Evidence**: Table 1, SS vs FS 行
> **Confidence**: high

> **Claim**: EM 迭代去噪框架在 DS 和 SS 设置中一致提升性能，结合外部语义信号（CLIP）可加速收敛。
> **Evidence**: Table 2, DNS 迭代结果
> **Confidence**: high

> **Claim**: 远程监督生成的标签在 Visual Genome 中覆盖 70.3% 的人工标注关系，且可以标注人工遗漏的合理关系（如 (wave, covering, beach)）。
> **Evidence**: Section 4, Figure 1
> **Confidence**: high

> **Claim**: 理想知识库（从训练集标注构建）可使 DS 模型 mR@50 从 37.68 提升至 50.87（+13.19），接近全监督水平。
> **Evidence**: Table 3
> **Confidence**: high

> **Claim**: 远程监督在长尾关系处理上显著优于弱监督方法，SS 模型 mR@50 达 60.20 vs FS Motif 52.65。
> **Evidence**: Table 1, mR@50 列
> **Confidence**: high

## Connections

- 与 **Textual Distant Supervision**（NLP 关系抽取领域，Mintz et al. 2009）共享核心思想：知识库与数据对齐生成标注，但本文解决的是实例级视觉关系检测而非全局实体关系
- 与 **Weakly Supervised Visual Semantic Parsing (VSPNet)**（Zareian et al. CVPR 2020）同属弱/远程监督 SGG 阵营，但 VSPNet 使用 image-level labels，本文使用知识库
- 与 **Limited Labels**（Chen et al. CVPR 2019）半监督 SGG 直接对比，本文在 DS 设置下即超越其半监督结果
- 与 **PPR-FCN**（Zhang et al. CVPR 2017）caption 弱监督方法对比，本文通过知识库系统性覆盖而非只关注 caption 中显著关系
- 与 **Neural Motif**（Zellers et al. CVPR 2018）全监督基线直接对比，本文 SS 设置显著超越全监督结果

## Open Questions

1. **场景图整体一致性**：如何将场景图的结构约束（如图一致性、语义合理性）整合进去噪框架？
2. **偏置分析**：远程监督引入的额外偏置是什么？是否偏向常识性关系而忽视罕见但有意义的视觉关系？
3. **开放域泛化**：在无 Visual Genome 物体标注的开放域图像上，整套流程（检测器+KB对齐+去噪）的端到端性能如何？
4. **知识库更新**：如何持续更新知识库以覆盖新物体和新关系，避免远程监督信号过时？
5. **去噪方法扩展**：更复杂的去噪策略（如注意力机制、图级约束）能否进一步提升远程监督的有效性？

## Provenance

- **Full paper source**: openaccess.thecvf.com (ICCV 2021)
- **arXiv**: 2103.15365
- **Code**: https://github.com/thunlp/VisualDS
- **Extraction**: PyMuPDF, 53,865 chars / 1,483 lines / 11 pages
- **Evidence level**: full-paper（全文精读，捕获了所有表格数据和关键方法论）
- **Label**: scene-graph-generation, weakly-supervised, ICCV-2021
- **Date**: 2026-06-10
