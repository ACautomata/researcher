---
title: "Adaptive Self-training Framework for Fine-Grained Scene Graph Generation (ST-SGG)"
type: paper
domain: scene-graph
status: active
created: 2026-06-10
updated: 2026-06-10
tags: [scene-graph-generation, self-training, fine-grained, long-tail, pseudo-labeling, ICLR-2024]
source_pages: []
raw_sources:
  - raw/sources/2024-01-adaptive-self-training-scene-graph-generation.pdf
  - raw/sources/2024-01-adaptive-self-training-scene-graph-generation.txt
related_pages:
  - domains/scene-graph/papers/neural-motifs-scene-graph-global-context.md
  - domains/scene-graph/papers/vctree-learning-to-compose-dynamic-tree-structures.md
  - domains/scene-graph/papers/2022-03-22-fine-grained-sgg-data-transfer.md
  - domains/scene-graph/papers/nice-noisy-label-correction-scene-graph-generation.md
  - domains/scene-graph/papers/unbiased-scene-graph-generation-tde-causal-modeling.md
  - domains/scene-graph/papers/unbiased-heterogeneous-scene-graph-generation-with-relation-aware-message-passing.md
paper:
  title: "Adaptive Self-training Framework for Fine-Grained Scene Graph Generation"
  authors: ["Kibum Kim", "Kanghoon Yoon", "Yeonjun In", "Jinyoung Moon", "Donghyun Kim", "Chanyoung Park"]
  year: 2024
  venue: ICLR 2024
  arxiv: "2401.09786"
  doi: null
  code: "https://github.com/rlqja1107/torch-ST-SGG"
classification:
  label: fine-grained-sgg, self-training, pseudo-labeling, CATM
  task: [Scene Graph Generation, Unbiased SGG, Fine-Grained SGG]
  method_family: Self-Training, Pseudo-Labeling, Graph Structure Learning
  modality: Image
  datasets: [Visual Genome (VG), Open Images V6 (OI-V6)]
  metrics: [Recall@K (R@K), mean Recall@K (mR@K), F@K, wmAPrel, wmAPphr, scorewtd]
evidence_level: full-paper
---

## Citation

Kibum Kim, Kanghoon Yoon, Yeonjun In, Jinyoung Moon, Donghyun Kim, Chanyoung Park. "Adaptive Self-training Framework for Fine-Grained Scene Graph Generation." ICLR 2024.

## One-Sentence Contribution

首次将自训练（self-training）引入场景图生成（SGG），提出 ST-SGG 框架，通过 Class-specific Adaptive Thresholding with Momentum (CATM) 伪标签策略和 Graph Structure Learner (GSL) 结构增强，有效利用未标注三元组来缓解长尾谓词分布问题，在 VG 和 OI-V6 上显著提升细粒度谓词性能。

## Problem Setting

**任务**：给定图像 I，SGG 模型 fθ: I → G 生成场景图 G = {(si, pi, oi)}，其中 si 和 oi 为实体（含类别标签和边界框），pi 为谓词类别（含背景类 bg）。

**两大核心挑战**：
1. **长尾谓词分布（Long-tailed Predicate Distribution）**：通用谓词（如 on、has）出现频率极高，细粒度谓词（如 walking in）极少，导致模型偏向多数类。
2. **缺失标注（Missing Annotation Problem）**：VG 数据集中 95.5% 的三元组被标注为 bg（背景类），其中大量实际包含有效的细粒度关系，错误的 bg 标注提供了错误监督信号。

**与现有方法的关键区别**：重采样（resampling）和重加权（reweighting）仅调整数据比例或损失权重，不增加数据多样性；IE-Trans（Zhang et al., 2022）虽利用未标注三元组但采用一次性伪标签（one-shot）且依赖于初始模型参数。本文提出**迭代式自训练**，每 batch 同时更新伪标签和模型参数。

## Method

提出 **ST-SGG（Self-Training for SGG）**，包含三个核心组件：

### 3.1 自训练框架形式化

给定 B 个 batch 的场景图 {G1, ..., GB}，每个 batch Gb 包含标注三元组 G_A^b 和未标注三元组 G_U^b（|G_U^b| ≫ |G_A^b|）。损失函数为三部分：

L = E[ Loss_annotated + Loss_bg + β · Loss_pseudo-labeled ]

其中 β 控制伪标签损失权重，仅当模型置信度 ˆq ≥ 阈值 τ 时对未标注三元组分配伪标签。

### 3.2 Class-specific Adaptive Thresholding with Momentum (CATM)

**核心洞察**：SGG 的伪标注面临三个独特挑战——语义歧义（相近谓词的概率不尖锐）、长尾分布（多数类伪标签远多于少数类）、bg 类主导（95.5% 的三元组为 bg，导致模型对 bg 具有高置信度）。

**CATM 由两部分组成**：

**（1）EMA 自适应阈值**：使用指数移动平均（EMA）在每次迭代时根据模型对各类的预测置信度动态调整阈值 τ_t^c：

- 若某类存在预测置信度 ≥ 前次阈值的样本 → 提升阈值
- 若某类所有预测置信度 < 前次阈值 → 降低阈值
- 若某类无样本被预测 → 保持阈值不变

使用 λinc 和 λdec 分别控制增降速率。

**（2）类别特定动量（Class-specific Momentum）**：为防止多数类占主导，为每类设置不同的 λinc^c 和 λdec^c：

- λinc^c = (N_c / N_1)^αinc：多数类阈值上升更快（减少伪标签分配）
- λdec^c = (N_(|Cp|+1-c) / N_1)^αdec：多数类阈值下降更慢（维持高阈值）

默认 αinc = αdec = 0.4。这使得尾部类被更积极地分配伪标签，缓解长尾问题。

### 3.3 Graph Structure Learner (GSL)

针对 MPNN-based SGG 模型（BGNN、HetSGG），设计 GSL 用于学习图中的相关和不相关边，仅通过相关边传播消息。GSL 通过减少对 bg 类的置信度（见 Fig. 3），提升对其他类的置信度，从而辅助 CATM 设定更合理的类特定阈值。

GSL 使用 Gumbel-Softmax（Maddison et al., 2016; Jang et al., 2016）进行离散边选择，并通过消息传播机制与主模型联合训练。

## Experiments

### 数据集

**Visual Genome (VG)**
- 108,077 张图像
- 100 个物体类，50 个谓词类（其中仅 34 类有 ≥10 个实例）
- 标注率：仅 4.5% 的三元组（约 5 个）被标注为正例，其余 95.5% 为 bg
- 标准 train/test 划分

**Open Images V6 (OI-V6)**
- 126,368 训练图像，1,813 验证图像，6,322 测试图像
- 301 个物体类，31 个谓词类
- 预处理方式遵循 Li et al. (2021) 和 Yoon et al. (2023)

### 任务

三种标准 SGG 任务：
1. **Predicate Classification (PredCls)**：给定真值定位和物体类别，预测谓词
2. **Scene Graph Classification (SGCls)**：给定真值定位，预测物体和谓词类别
3. **Scene Graph Detection (SGDet)**：端到端检测边界框、物体、谓词

OI-V6 额外评估：**wmAPrel**（加权平均精确率-关系）、**wmAPphr**（加权平均精确率-短语）、**scorewtd**（0.2×R@50 + 0.4×wmAPrel + 0.4×wmAPphr）

### Baseline 方法

**Model-Agnostic baselines**：
- Resampling (Li et al., 2021), TDE (Tang et al., 2020), DLFE (Chiou et al., 2021)
- NICE (Li et al., 2022), IE-Trans (Zhang et al., 2022), I-Trans (Zhang et al., 2022)

**SGG backbone models**：
- Motif (Zellers et al., 2018), VCTree (Tang et al., 2019)
- BGNN (Li et al., 2021), HetSGG (Yoon et al., 2023)

**SOTA debiasing methods**：
- DT2-ACBS (Desai et al., 2021), PCPL (Yan et al., 2020)
- KERN (Chen et al., 2019), PE-Net (Zheng et al., 2023)

### 训练设置

- **Backbone**：Faster R-CNN with ResNeXt-101-FPN（VG），ResNet-101-FPN（OI-V6）
- **Optimizer**：SGD
- **Initial learning rate**：0.01（VG），0.001（OI-V6）
- **Batch size**：6
- **Total iterations**：20,000
- **Hardware**：NVIDIA A6000 GPU
- **β（伪标签损失系数）**：0.5（默认，在 0.1–1.0 范围内发现不敏感）
- **αinc, αdec**：0.4（默认，在 0.0–1.0 范围内调优）
- **GSL**：使用 Gumbel-Softmax，与主模型联合训练

## Results

### VG — Model-Agnostic 基线比较（Table 1）

**Predicate Classification 任务关键结果（mR@50/100）**：

| 模型 | R@50/100 | mR@50/100 | F@50/100 |
|------|----------|-----------|----------|
| Motif (Zellers et al., 2018) | 65.3 / 67.1 | 17.8 / 19.2 | 28.0 / 29.9 |
| +ST-SGG (ours) | 63.4 / 65.4 | **22.4 / 24.1** | 33.1 / 35.2 |
| +Resam. (Li et al., 2021) | 62.3 / 64.3 | 26.1 / 28.5 | 36.8 / 39.5 |
| +Resam.+ST-SGG (ours) | 53.9 / 57.7 | **28.1 / 31.5** | 36.9 / 40.8 |
| +IE-Trans (Zhang et al., 2022) | 54.7 / 56.7 | 30.9 / 33.6 | 39.5 / 42.2 |
| +I-Trans+ST-SGG (ours) | 50.5 / 52.8 | **32.5 / 35.1** | 40.1 / 42.5 |
| VCTree (Tang et al., 2019) | 65.5 / 67.2 | 17.2 / 18.6 | 27.3 / 29.1 |
| +I-Trans+ST-SGG (ours) | 52.5 / 54.3 | **32.7 / 35.6** | 40.3 / 43.0 |
| DT2-ACBS (Desai et al., 2021) | 23.3 / 25.6 | 35.9 / 39.7 | 28.3 / 31.1 |
| PCPL (Yan et al., 2020) | 50.8 / 52.6 | 35.2 / 37.8 | 41.6 / 44.0 |
| PE-Net (Zheng et al., 2023) | 64.9 / 67.2 | 31.5 / 33.8 | 42.4 / 45.0 |

**关键发现**：
- ST-SGG 显著提升 Motif 和 VCTree 的 mR@K（Motif mR@100 从 19.2% → 24.1%，提升 4.9 点）
- 与 I-Trans 结合后效果最佳：Motif+I-Trans+ST-SGG 在 PredCls mR@100 达 35.1%（+15.9 vs 基线 Motif）
- ST-SGG 模型无关：对所有 backbone（Motif、VCTree、BGNN、HetSGG）均有效
- 结合简单 debiasing 方法（Resampling）的 ST-SGG 即可匹敌 SOTA 架构

### VG — MPNN 模型比较（Table 2）

| 模型 | mR@50/100 (PredCls) | mR@50/100 (SGCls) |
|------|---------------------|-------------------|
| BGNN+Resam. (Li et al., 2021) | 29.2 / 31.7 | 14.6 / 16.0 |
| +ST-SGG (ours) | 33.0 / 35.1 | 17.9 / 19.0 |
| +ST-SGG+GSL (ours) | **34.1 / 36.2** | **18.0 / 19.4** |
| HetSGG+Resam. (Yoon et al., 2023) | 30.0 / 32.2 | 15.8 / 17.7 |
| +ST-SGG (ours) | 32.6 / 35.2 | 18.0 / 18.9 |
| +ST-SGG+GSL (ours) | **33.6 / 35.8** | **18.2 / 19.1** |

**关键发现**：
- GSL 进一步提升了 ST-SGG 在 MPNN 模型上的性能（BGNN+ST-SGG+GSL vs BGNN+ST-SGG：PredCls mR@100 36.2% vs 35.1%）
- GSL 通过减少 bg 类置信度，使模型对其他谓词类的预测更可靠

### 消融实验（Table 3，SGCls 任务）

| Backbone | 变体 | R@50/100 | mR@50/100 | F@50/100 |
|----------|------|----------|-----------|----------|
| Motif | Vanilla | 36.1 / 37.0 | 13.7 / 14.7 | 19.9 / 21.0 |
| | ST-SGG w/o EMA | 24.6 / 27.4 | 6.0 / 7.7 | 9.6 / 12.0 |
| | ST-SGG w/o λinc, λdec | 33.0 / 34.4 | 13.5 / 14.3 | 19.2 / 20.2 |
| | ST-SGG | 33.4 / 34.9 | **16.9 / 18.0** | **22.4 / 23.8** |
| BGNN | Vanilla | 36.9 / 38.1 | 14.6 / 16.0 | 20.9 / 22.5 |
| | ST-SGG w/o EMA | 36.6 / 37.5 | 13.9 / 14.8 | 20.1 / 21.2 |
| | ST-SGG w/o λinc, λdec | 33.8 / 36.3 | 10.4 / 12.7 | 15.9 / 18.8 |
| | ST-SGG | 32.3 / 34.0 | **18.0 / 19.0** | **23.1 / 24.4** |
| | +GSL | 33.5 / 34.7 | **18.0 / 19.4** | **23.4 / 24.9** |

**关键发现**：
- 去除 EMA（固定阈值）后 Motif mR@100 从 14.7% 暴跌至 7.7%（EMA 对 SGG 至关重要）
- 去除类别特定动量后 mR@100 从 18.0% 降至 14.3%（αinc, αdec 缓解多数类偏差）
- GSL 在 BGNN 上进一步提升了 R@K（34.7 vs 34.0）和 mR@K

### OI-V6 结果（Table 8，SGDet）

| 模型 | R@50 | mR@50 | F@50 | scorewtd |
|------|------|-------|------|----------|
| Motif (Zellers et al., 2018) | 70.6 | 31.8 | 43.8 | 38.5 |
| +ST-SGG (ours) | 71.8 | 34.1 | 46.2 | 39.8 |
| +Resam. (Li et al., 2021) | 70.3 | 40.6 | 51.5 | 40.2 |
| +Resam.+ST-SGG (ours) | **71.7** | **42.7** | **53.5** | **41.4** |
| BGNN (Li et al., 2021) | 75.3 | 39.8 | 52.1 | 41.9 |
| +ST-SGG (ours) | 75.2 | **42.9** | **54.6** | 41.7 |

**关键发现**：
- OI-V6 上 mR@50 显著提升：Motif+Resam.+ST-SGG 达 42.7（+2.1 vs 无 ST-SGG）
- BGNN+ST-SGG 的 mR@50 达 42.9（+3.1 vs 无 ST-SGG）
- 对头部谓词（如 contain）保持竞争性，尾部谓词（如 ski）显著提升（见 Fig. 13）

### 定性分析

- CATM 的类特定阈值多样化，与类别频率不相关（见 Fig. 5(a)），说明精确设阈值的困难性
- 真实背景案例（如远处的摩托车和街道）：ST-SGG 正确预测为 bg，IE-Trans 错误预测为 parked on（见 Fig. 5(b)）
- 缺失标注案例（如熊和雪）：ST-SGG 正确预测为 walking in，IE-Trans 先预测 on 后重分配给 bg（见 Fig. 5(c)）
- ST-SGG 的迭代伪标签比 IE-Trans 的一次性伪标签更准确

## Limitations

1. 当前工作聚焦于利用已有的基准数据集，尚未探索利用额外的无标注数据源（如仅含边界框的定位数据集）
2. 阈值调整的超参数（αinc, αdec）需在验证集上调优，不同数据集可能设置不同
3. GSL 仅适用于 MPNN-based 模型，非 MPNN 模型（如 Motif）无法受益
4. 自训练过程可能引入确认偏差（confirmation bias），虽然 CATM 已缓解但未完全消除
5. 计算复杂度方面，ST-SGG 的迭代伪标签比 IE-Trans 高效但仍增加训练时间（Motif: 5h03m vs 2h21m）(Table 7)
6. β 值过大（>1.0）时性能下降，表明应优先确保标注数据的监督信号

## Reusable Claims

> **Claim**: 将自训练引入 SGG 任务可有效利用未标注三元组缓解长尾分布，但需专门设计伪标注策略（CA TM）以解决语义歧义和长尾问题。
> **Evidence**: 在 VG 上，Motif+ST-SGG（CA TM）mR@100 达 24.1%（+4.9 vs Motif）；而使用 FixMatch 式固定阈值的自训练（τ con）性能甚至差于无自训练基线。
> **Scope**: VG, OI-V6, PredCls/SGCls/SGDet
> **Confidence**: high

> **Claim**: EMA 自适应阈值是 ST-SGG 的关键组件：去除 EMA 后 Motif mR@100 从 14.7% 暴跌至 7.7%（SGCls）。
> **Evidence**: 消融实验 Table 3，固定阈值（w/o EMA）严重下降各个指标。
> **Scope**: VG, Motif backbone, SGCls
> **Confidence**: high

> **Claim**: 类别特定动量（Class-specific Momentum）通过差异化阈值调整速率缓解多数类伪标签偏差，是 CATM 有效性的核心。
> **Evidence**: 去除 λinc, λdec 后 Motif mR@100 从 18.0% 降至 14.3%（SGCls），且伪标签分配偏向多数类（Fig. 9）。
> **Scope**: VG, Motif/BGNN backbone, SGCls
> **Confidence**: high

> **Claim**: GSL 通过减少 MPNN 模型对 bg 类的置信度，带来额外的性能提升（BGNN+ST-SGG+GSL PredCls mR@100 36.2% vs 35.1%）.
> **Evidence**: Table 2 和 Fig. 3：GSL 降低了 bg 类置信度，提高了其他类的置信度.
> **Scope**: VG, BGNN/HetSGG，MPNN-based SGG
> **Confidence**: medium

> **Claim**: ST-SGG 的迭代式伪标签比 IE-Trans 的一次性伪标签更准确，计算也更高效。
> **Evidence**: Motif+I-Trans+ST-SGG（mR@100 35.1%）优于 Motif+IE-Trans（mR@100 33.6%），且训练时间更短（5h03m vs 6h21m）。
> **Scope**: VG, Motif backbone
> **Confidence**: medium

## Connections

- **与 IE-Trans 的关系**：IE-Trans 是唯一使用未标注三元组的先前方法，但采用一次性伪标签；ST-SGG 采用迭代式伪标签 + 类特定自适应阈值，在 PredCls mR@100 上超越 IE-Trans（35.1% vs 33.6%）且训练更高效
- **与 FixMatch [40] 的关系**：直接套用 FixMatch 的固定阈值于 SGG 失败（Motif-τ con 性能低于无自训练基线），因 SGG 的语义歧义和 bg 类主导问题
- **与 BGNN [13] 的关系**：BGNN 是主要 MPNN 基线，GSL 专为用于 BGNN 和 HetSGG
- **与 Resampling [13] 的关系**：ST-SGG 可无缝结合重采样方法（如 Resamp.+ST-SGG），组合效果更好
- **与 NICE [17] 的关系**：NICE 也处理标注噪声（缺失标注）但通过标签校正而非伪标签
- **与 PE-Net [43] 的关系**：PE-Net 是基于原型学习的 SGG 方法，ST-SGG+I-Trans 的 F@K 接近 PE-Net 但架构更简单

## Open Questions

1. ST-SGG 能否利用外部未标注数据集（如仅含定位信息的 COCO）进一步提升性能？论文在 Limitations 中提出该方向
2. CATM 的 αinc, αdec 是否可设计为自适应而非固定？不同谓词类可能需要不同的调整率
3. GSL 能否扩展到非 MPNN 的现代 SGG 架构（如 Transformer-based SGTR）？
4. ST-SGG 在开放词汇/zero-shot SGG 设置下的效果如何？伪标签是否可推广到未见过的谓词类？
5. β 的超参数敏感性不高（0.1–1.0 均稳定），但最优值在不同 backbone/数据集下是否通用？
6. ST-SGG 的时间复杂度分析显示训练增加约 2 倍（Motif: 5h vs 2.5h），更大的模型（如 BGNN）的额外成本如何？
7. 伪标签质量能否通过集成多个模型或利用视觉-语言模型（如 CLIP）进一步提高？

## Provenance

- **原始来源**：raw/sources/2024-01-adaptive-self-training-scene-graph-generation.pdf（arXiv:2401.09786v5，ICLR 2024 接收版）
- **全文提取**：raw/sources/2024-01-adaptive-self-training-scene-graph-generation.txt（98,960 字符，25 页 PDF）
- **分析类型**：全文精读（full-paper）
- **分析日期**：2026-06-10
