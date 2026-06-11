---
title: "SBG: Fine-Grained Scene Graph Generation via Sample-Level Bias Prediction"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - scene-graph-generation
  - long-tailed-distribution
  - bias-correction
  - fine-grained-sgg
  - generative-adversarial-network
  - sample-level-correction
  - eccv-2024
raw_sources:
  - ../../../raw/sources/2024-ECCV-Fine-Grained-SGG-Sample-Level-Bias-Prediction.pdf
  - ../../../raw/sources/2024-ECCV-Fine-Grained-SGG-Sample-Level-Bias-Prediction.txt
related_pages:
  - hiker-sgg-hierarchical-knowledge-enhanced-robust-sgg.md
  - leveraging-predicate-and-triplet-learning-for-sgg.md
  - adaptive-fine-grained-predicates-learning-scene-graph-generation.md
  - fast-contextual-scene-graph-generation.md
evidence_level: full-paper
paper:
  title: "Fine-Grained Scene Graph Generation via Sample-Level Bias Prediction"
  abbreviated: "SBG"
  authors:
    - Yansheng Li
    - Tingzhu Wang
    - Kang Wu
    - Linlin Wang
    - Xin Guo
    - Wenbin Wang
  affiliations:
    - School of Remote Sensing and Information Engineering, Wuhan University
    - Ant Group
    - College of Computer and Information Technology, China Three Gorges University
  year: 2024
  venue: ECCV 2024
  doi: null
  arxiv: "2407.19259"
  code: "https://github.com/Zhuzi24/SBG"
  url: "https://arxiv.org/abs/2407.19259"
---

# SBG: Fine-Grained Scene Graph Generation via Sample-Level Bias Prediction

## 核心思想

现有的 SGG 去偏方法（如 DLFE, RTPB）属于 dataset-level correction：对整个数据集估计统一的正则项（如每类标签频率或阻力偏置），对所有样本使用相同的校正量。这种校正忽略了不同物体对（样本）之间的特异性。

SBG 的核心洞察：每个物体对的 union region 包含丰富的专属上下文信息，可以用来预测 **样本特定的偏置（sample-specific bias）**，从而将粗粒度关系预测修正为细粒度关系。

**关键创新**：
1. 首次探索 sample-level bias correction 用于 SGG 长尾问题
2. 设计 Bias-Oriented Generative Adversarial Network（BGAN），利用上下文信息预测样本特定的校正偏置
3. 在 VG、GQA、VG-1800 上达到 SOTA Average@K

## 方法

### Sample-Level Bias Prediction (SBP)

SBG 是一个两阶段框架：

**阶段一：构建校正偏置集（Correction Bias Set）**

用经典 SGG 模型（Motif/VCtree/Transformer）对每对物体计算原始预测 logits z，然后使用 GT 标签构建校正偏置：
- 融合 union feature f_uni 和 global bias b_glo → b_tru = φ(f_uni) + b_glo
- 检查 b_tru 是否能将原始预测校正到 GT（即 argmax(z + b_tru) = r_tru）
- 若不满足，通过差值 d 和 ε 调整 b_tru
- 所有满足条件的 b_tru 构成校正偏置集 S

**阶段二：BGAN 训练**

BGAN 由生成器 G 和判别器 D 组成：
- **G**：输入 union features f_uni、global bias b_glo、原始预测 z → 输出预测偏置 b_pre
- **D**：区分预测偏置 b_pre 与构造偏置 b_tru
- G 的损失包括对抗损失和交叉熵损失（基于校正后预测 ^z）
- D 的损失为标准 WGAN 损失

**推理阶段**：冻结 SGG 模型参数，G 为每个样本预测偏置并校正原始预测，得到细粒度关系。

### 关系全局偏置（Global Bias）

b_glo = -log(w^a / Σ_j w_j^a + ε)，其中 w 为关系类别的权重向量，a 和 ε 为超参数。

## 实验

### 设置
- **骨干网络**：Faster R-CNN + ResNeXt-101-FPN
- **数据集**：VG（150 obj / 50 rel）、GQA（160 obj / 60 rel）、VG-1800（70k obj / 1.8k rel）
- **评估指标**：R@K、mR@K、Average@K（R@K 和 mR@K 的平均值）
- **SGG 模型**：Motif、VCtree、Transformer
- **GPU**：NVIDIA 24G GeForce RTX 3090

### 主实验结果

**VG PredCls（Transformer 骨干）**：
| 指标 | R@50 | R@100 | mR@50 | mR@100 | A@50 | A@100 |
|------|------|-------|-------|--------|------|-------|
| Transformer | 65.5 | 67.3 | 18.2 | 19.7 | 41.9 | 43.5 |
| +SBG | **55.8** | **57.6** | **33.3** | **35.7** | **44.6** | **46.7** |

**VG PredCls（Motif 骨干）**：
| 指标 | R@50 | R@100 | mR@50 | mR@100 | A@50 | A@100 |
|------|------|-------|-------|--------|------|-------|
| Motif | 65.4 | 67.2 | 18.0 | 19.3 | 41.7 | 43.3 |
| +DLFE (dataset-level) | 52.4 | 54.3 | 26.7 | 28.7 | 39.6 | 41.5 |
| +RTPB (dataset-level) | 40.3 | 42.6 | 35.4 | 37.4 | 37.9 | 40.0 |
| +SBG | **55.4** | **57.3** | **32.1** | **34.4** | **43.8** | **45.9** |

**VG PredCls（VCtree 骨干）**：
| 指标 | A@50 | A@100 |
|------|------|-------|
| VCtree | 41.7 | 43.3 |
| +SBG | **44.0** | **45.9** |

**与 Dataset-Level 校正方法对比**（Figure 5）：
SBG 在 Motif/VCtree 上相对于 DLFE/RTPB 的平均提升：
- PredCls A@K: +5.6%
- SGCls A@K: +3.9%
- SGDet A@K: +3.2%

**与 RTPB 的效率对比**（Motif PredCls）：
| 方法 | A@100 | 训练时间(h) | 推理速度(s/img) | 参数量(M) |
|------|-------|------------|----------------|----------|
| DLFE | 41.5 | 22.9 | 0.1049 | 253.41 |
| RTPB | 40.1 | 12.1 | 0.1039 | 254.05 |
| SBG | **45.9** | **12.6** | 0.1062 | 254.75 |

SBG 相比 DLFE 在 A@100 提升 10.6% 的同时训练时间减少 45.0%；相比 RTPB A@100 提升 14.5% 且仅增加 4.1% 训练时间。

**GQA 结果（Transformer PredCls）**：
| 方法 | R@50/100 | mR@50/100 | A@50/100 |
|------|----------|-----------|----------|
| Transformer | 67.5/68.9 | 26.8/28.2 | 47.2/48.6 |
| +RTPB | 50.8/52.3 | 44.6/45.8 | 47.7/49.1 |
| +CFA | 50.5/52.8 | 46.1/47.2 | 48.3/50.0 |
| +SBG | **58.6/60.0** | 41.6/42.9 | **50.1/51.5** |

**VG-1800 结果（Motif PredCls）**：
| 方法 | F-Acc Top-1 | F-Acc Top-5 | F-Acc Top-10 |
|------|-------------|-------------|--------------|
| Motif | 1.21 | 5.20 | 8.33 |
| +CFA | 5.33 | 18.25 | 24.51 |
| +SBG | **13.45** | **26.74** | **34.99** |

**扩展到 One-Stage SGG（VG SGDet）**：
| 模型 | R@50/100 | mR@50/100 | A@50/100 |
|------|----------|-----------|----------|
| ISG | 30.8/35.6 | 19.5/23.4 | 25.2/29.5 |
| ISG+SBG | 29.3/33.6 | **24.1/28.2** | **26.7/30.9** |
| SGTR | 24.6/28.4 | 12.0/15.2 | 18.3/21.8 |
| SGTR+SBG | 22.3/26.3 | **18.1/20.9** | **20.2/23.6** |

**泛化到 Object Detection（COCO）**：
Faster R-CNN (R-50-FPN, 1x) + SBP：
- mAP: **37.6** (+1.2% vs 36.4)
- mAP_tail: **44.4** (+2.8% vs 41.6)

### 消融实验

**1. 区域范围**（Transformer PredCls）：使用 union region 的 A@50/100 为 44.6/46.7，使用整个图像的仅为 40.3/42.0（引入多余干扰）

**2. Global Bias 作用**：
- 同时使用 f_uni 和 b_glo：A@50/100 = 44.6/46.7（最优）
- 仅 f_uni：42.6/44.8
- 仅 b_glo：42.1/43.5
- 都不使用：41.9/43.5（即原始 Transformer baseline）

**3. 权重因子 α**（A@100 最优 @ α=0.075）

**4. 训练模式**：逐步训练（冻结 SGG → 训练 BGAN）优于联合训练

## 分析

### 优势
- 从 dataset-level 校正到 sample-level 校正的范式转变，是 SGG 去偏领域的重要演进
- 在保持 R@K 的同时显著提升 mR@K，平衡性好于其他方法
- 良好的泛化性：在三种不同 SGG 骨干（Motif/VCtree/Transformer）上均有一致提升
- 扩展到 one-stage 方法和目标检测任务表现良好
- 训练效率高：比 DLFE 节省 45% 训练时间

### 局限性
- mR@K 略低于某些方法（如 RTPB），但整体 A@K 更优
- GAN 训练稳定性需额外调参（α 需要精细调整）
- 在 GQA 上的增益相对较小（数据量较小、长尾较轻）
- 未探讨多模态或开放词汇场景

### 与 Dataset-Level 方法的关系
SBG 与 DLFE/RTPB 是互补的：DLFE 和 RTPB 在 mR 上表现突出但过度牺牲 R，SBG 在 R 和 mR 之间取得更好平衡。两者结合（sample + dataset 双层次校正）可能是值得探索的方向。

## 笔记

- **用户提供标题**为 "Fine-Grained Scene Graph Generation via Sample-Level Dual-Granularity Knowledge Distillation"，实际 arXiv 标题为 "Fine-Grained Scene Graph Generation via Sample-Level Bias Prediction"。可能为同一工作的不同版本或用户记忆偏差。
- 代码仓库：https://github.com/Zhuzi24/SBG
- 方法 SBP 在目标检测任务上也验证了有效性，说明其具有跨任务泛化能力

## 参考文献

- [DLFE: Recovering the unbiased scene graphs from the biased ones (ACM MM 2021)](https://dl.acm.org/doi/10.1145/3474085.3475339)
- [RTPB: Resistance training using prior bias (AAAI 2022)](https://arxiv.org/abs/2201.12541)
- [CFA: Compositional Feature Augmentation for Unbiased SGG (ICCV 2023)](https://arxiv.org/abs/2302.13026)
