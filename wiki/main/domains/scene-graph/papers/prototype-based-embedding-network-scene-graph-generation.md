---
title: "Prototype-based Embedding Network for Scene Graph Generation (PE-Net)"
type: paper
domain: scene-graph
status: active
created: 2026-06-08
updated: 2026-06-08
tags:
  - scene-graph-generation
  - prototype-learning
  - embedding-network
  - relation-recognition
  - long-tail-distribution
  - prototypical-networks
  - CVPR-2023
raw_sources:
  - ../../../sources/scene-graph/2023_CVPR_PE-Net_Prototype-based_Embedding_Network_for_Scene_Graph_Generation.pdf
  - ../../../sources/scene-graph/2023_CVPR_PE-Net_Prototype-based_Embedding_Network_for_Scene_Graph_Generation.txt
related_pages:
  - fast-contextual-scene-graph-generation.md
  - squat-selective-quad-attention-scene-graph-generation.md
  - language-supervised-open-vocabulary-scene-graph-vs3.md
evidence_level: full-paper
paper:
  title: "Prototype-based Embedding Network for Scene Graph Generation"
  abbreviated: "PE-Net"
  authors:
    - Chaofan Zheng
    - Xinyu Lyu
    - Lianli Gao
    - Bo Dai
    - Jingkuan Song
  affiliations:
    - University of Electronic Science and Technology of China
  year: 2023
  venue: CVPR 2023
  doi: null
  arxiv: "2303.07096"
  code: https://github.com/VL-Group/PENET
  url: https://openaccess.thecvf.com/content/CVPR2023/html/Zheng_Prototype-Based_Embedding_Network_for_Scene_Graph_Generation_CVPR_2023_paper.html
---

# PE-Net: Prototype-based Embedding Network for Scene Graph Generation

## 核心思想

现有 SGG 方法面临两大挑战：(1) 同一谓词类别内因 subject-object 视觉外观多样导致**大类内变异**（如"man-eating-pizza" vs "giraffe-eating-leaf"）；(2) 不同谓词间的**类间相似性**（如"man-holding-plate" vs "man-eating-pizza"）。本文提出谓词的类别固有语义可以作为**类原型**（class-wise prototypes）来缓解上述挑战。

核心设计：PE-Net 在语义空间中建模实体/谓词的原型对齐（prototype-aligned）紧致且可区分的表示，通过在共同嵌入空间中建立实体对与谓词之间的匹配来实现关系识别。

## 方法

### 架构总览

PE-Net 由三个关键组件构成：

1. **实体/谓词编码**：基于 Faster R-CNN + motif 上下文编码器获取初始实体特征，然后通过语义映射投影到嵌入空间
2. **原型对齐表示（Prototype-based Modeling）**：
   - 为每个实体类别和每个谓词类别定义可学习的**原型向量**（prototype vector）
   - 将每个实例的特征对齐到对应类别的原型，学习紧致且可区分的表示
3. **实体-谓词匹配（Entity-Predicate Matching）**：
   - 将实体对的特征与谓词原型在共同嵌入空间中进行匹配
   - 匹配分数作为关系分类的依据

### Prototype-guided Learning (PL)

PL 帮助 PE-Net 高效学习实体-谓词匹配。对每个实体对 (s, o)，计算其联合表示与各谓词原型的相似度，通过对比学习方式训练：

- 正样本对：实体对特征与其真实关系原型的匹配
- 负样本对：实体对特征与无关关系原型的匹配
- 损失函数使用 InfoNCE 风格对比损失

### Prototype Regularization (PR)

PR 用于缓解谓词语义重叠导致的模糊实体-谓词匹配：

- 鼓励不同谓词类别的原型在语义空间中相互远离（增加原型间距离）
- 减少谓词原型间的语义冲突，提升分类判别力
- 通过正则化项 `L_PR = Σ_{i≠j} max(0, γ - ||p_i - p_j||^2)` 实现

### 整体损失函数

`L = L_PL + λ * L_PR`，其中 L_PL 是原型引导学习损失，L_PR 是原型正则化项。

## 实验结果

### Visual Genome（VG）数据集结果

Table 1：与 SOTA 方法对比（VG，三子任务）

| 模型 | PredCls R@50/100 | PredCls mR@50/100 | SGCls R@50/100 | SGCls mR@50/100 | SGDet R@50/100 | SGDet mR@50/100 |
|------|------------------|--------------------|----------------|------------------|----------------|------------------|
| Motifs | 65.3/67.2 | 14.9/16.3 | 38.9/39.8 | 8.3/8.8 | 32.1/36.8 | 6.6/7.9 |
| VCTree | 65.5/67.4 | 16.7/17.9 | 40.3/41.6 | 7.9/8.3 | 31.9/36.0 | 6.4/7.3 |
| RU-Net | 67.7/69.6 | —/24.2 | 42.4/43.3 | —/14.6 | 32.9/37.5 | —/10.8 |
| BGNN | 59.2/61.3 | 30.4/32.9 | 37.4/38.5 | 14.3/16.5 | 31.0/35.8 | 10.7/12.6 |
| **PE-Net(P)** | 68.2/70.1 | 23.1/25.4 | 41.3/42.3 | 13.1/14.8 | 32.4/36.9 | 8.9/11.0 |
| **PE-Net (full)** | 64.9/67.2 | **31.5/33.8** | 39.4/40.7 | **17.8/18.9** | 30.7/35.2 | **12.4/14.5** |

PE-Net(P) = 仅用 PL 训练；PE-Net = PL+PR 训练。
- PE-Net 全模型在 mR@100 上全面超过所有方法：PredCls 33.8% vs. BGNN 32.9%
- 相对 VCTree 在 mR@100 上提升：PredCls +15.9%、SGCls +10.6%、SGDet +7.2%

### 去偏（Reweight）设定

| 模型 | PredCls R@100 | PredCls mR@100 | SGCls R@100 | SGCls mR@100 | SGDet R@100 | SGDet mR@100 |
|------|---------------|----------------|-------------|---------------|-------------|--------------|
| Motifs-GCL | 44.4 | 38.2 | 27.1 | 21.8 | 22.0 | 19.3 |
| Motifs-Reweight | 55.5 | 36.1 | 33.4 | 19.1 | 28.2 | 15.4 |
| **PE-Net-Reweight** | **61.4** | **40.7** | **37.3** | **23.5** | **30.9** | **18.8** |

PE-Net-Reweight 在三个子任务上全面超越所有去偏方法，PredCls R@100=61.4（超 Motifs-GCL 17.0%）。

### 零样本（Zero-shot）Recall（VG）

| 模型 | PredCls zs-R@50/100 | SGCls zs-R@50/100 | SGDet zs-R@50/100 |
|------|---------------------|-------------------|-------------------|
| Motifs-TDE | 14.4/18.2 | 3.4/4.5 | 2.3/2.9 |
| VCTree-TDE | 14.3/17.6 | 3.2/4.0 | 2.6/3.2 |
| **PE-Net** | **17.16/20.89** | **5.37/6.53** | **2.31/3.60** |

PE-Net 零样本 Recall 全面超过 TDE（去偏）方法。

### Open Images V6 数据集

| 模型 | R@50 | wmAPrel | wmAPphr | scorewtd |
|------|------|---------|---------|----------|
| Motifs | 71.6 | 29.9 | 31.6 | 38.9 |
| G R-CNN | 74.5 | 33.2 | 34.2 | 41.8 |
| BGNN | 75.0 | 33.5 | 34.2 | 42.1 |
| RU-Net | 76.9 | **35.4** | 34.9 | 43.5 |
| **PE-Net** | **76.5** | **36.6** | **37.4** | **44.9** |

PE-Net 在 wmAPrel、wmAPphr、scorewtd 三个指标上取得最佳，超过 RU-Net。

### 表征质量分析

使用 Intra-class Variance (IV) 和 Intra-class to Inter-class Variance Ratio (IIVR) 度量：

| 模型 | IV-O ↓ | IIVR-O ↓ | IV-R ↓ | IIVR-R ↓ |
|------|--------|----------|--------|----------|
| Motifs | 9.73 | 1.93 | 1.41 | 2.72 |
| VCTree | 8.31 | 2.11 | 1.50 | 2.78 |
| **PE-Net** | **0.74** | **0.24** | **1.06** | **1.67** |

PE-Net 的 IV 和 IIVR 均大幅低于所有对比方法，证实其产生了高度紧致且可区分的实体和谓词表示。

### 消融实验

| Exp | PL | PR | PredCls mR@100 | SGCls mR@100 | SGDet mR@100 | M@100 Mean |
|-----|----|----|-----------------|---------------|-------------|------------|
| 1 | ✗ | ✗ | 20.0 | 10.5 | 9.3 | 23.1 |
| 2 | ✓ | ✗ | 25.4 | 14.8 | 11.0 | 24.0 |
| 3 | ✓ | ✓ | **33.8** | **18.9** | **14.5** | **24.9** |

- PL（Exp 2 vs 1）在各子任务上带来显著 mR@100 提升（+5.4/+4.3/+1.7）
- PR（Exp 3 vs 2）进一步大幅提升 mR（+8.4/+4.1/+3.5），说明正则化对缓解谓词语义重叠很关键
- 但 PR 导致 R@100 轻微下降（从 70.1→67.2），表明牺牲部分常见谓词精度换取长尾谓词性能

## 核心贡献

1. 提出**原型对齐的嵌入网络（PE-Net）**，在语义空间中建模紧致且可区分的实体/谓词表示用于 SGG
2. 设计**原型引导学习（PL）**，通过对比学习建立实体对与谓词原型的匹配
3. 设计**原型正则化（PR）**，增加谓词原型间距以缓解模糊匹配
4. 在 VG 和 Open Images 两个数据集上达到新 SOTA，尤其在 mR（长尾性能）上优势显著
5. 零样本泛化能力大幅超越以往方法，证明原型建模的类比推理能力

## 局限与展望

- **R@K 和 mR@K 的权衡**：PR 提升长尾谓词识别精度，但轻微降低了常见谓词的 R@K，二者之间需要更好的平衡
- 原型建模依赖于固定的谓词集合，对于 open-vocabulary SGG 可能需要扩展原型机制
- 方法当前仅在场景图生成任务上验证，可推广性未在其他关系理解任务上测试

---

## Extracted By

- **提取日期**：2026-06-08
- **提取方法**：PyMuPDF
- **文件大小**：3.3M PDF
- **来源文件**：`raw/sources/2023_CVPR_PE-Net_Prototype-based_Embedding_Network_for_Scene_Graph_Generation.pdf`
