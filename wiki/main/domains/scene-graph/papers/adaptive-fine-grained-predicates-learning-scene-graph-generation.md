---
title: "Adaptive Fine-Grained Predicates Learning for Scene Graph Generation"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags: [sgg, fine-grained, predicate-correlation, adaptive-learning, long-tail]
paper:
  title: "Adaptive Fine-Grained Predicates Learning for Scene Graph Generation"
  authors: ["Xinyu Lyu", "Lianli Gao", "Pengpeng Zeng", "Heng Tao Shen", "Jingkuan Song"]
  year: 2023
  venue: "IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI)"
  arxiv: "2207.04602"
  doi: "10.1109/TPAMI.2023.3298356"
  code: null
classification:
  label: "Fine-grained predicate learning for SGG"
  task: ["Scene Graph Generation", "Predicate Classification", "Scene Graph Classification", "Scene Graph Detection"]
  method_family: ["Adaptive Fine-Grained Learning", "Predicate Correlation Modeling", "Adaptive Re-weighting"]
  modality: ["image", "text"]
  datasets: ["Visual Genome (VG-SGG)", "GQA-SGG"]
  metrics: ["mR@K", "R@K", "Group Mean Recall (Head/Body/Tail)", "DP@K (Discriminatory Power)"]
evidence_level: full-paper
raw_sources:
  - ../../../sources/scene-graph/2023-TPAMI-adaptive-fine-grained-predicates-learning-scene-graph-generation.pdf
  - ../../../sources/scene-graph/2023-TPAMI-adaptive-fine-grained-predicates-learning-scene-graph-generation.txt
---

## Citation

X. Lyu, L. Gao, P. Zeng, H. T. Shen and J. Song, "Adaptive Fine-Grained Predicates Learning for Scene Graph Generation," in IEEE Transactions on Pattern Analysis and Machine Intelligence, vol. 45, no. 11, pp. 13921-13937, Nov. 2023, doi: 10.1109/TPAMI.2023.3298356.

arXiv preprint: [2207.04602](https://arxiv.org/abs/2207.04602)

## One-Sentence Contribution

提出自适应细粒度谓词学习框架 FGPL-A，通过动态建模谓词间相关性并自适应调整区分过程，解决 SGG 中难区分谓词（如 "on/standing on/walking on"）的判别问题。

## Problem Setting

- **任务**：Scene Graph Generation (SGG)，检测图像中实例及其关系，表示为 \<subject-predicate-object\> 三元组。
- **核心挑战**：谓词分布呈长尾，通用 SGG 模型偏向头部谓词，重平衡策略偏向尾部谓词，两者都无法妥善处理**难区分谓词**（hard-to-distinguish predicates）——语义高度重叠的谓词对（如 "on/standing on/walking on"、"holding/carrying"、"watching/playing"）。
- **问题根源**：难区分谓词的相关性随上下文（subject-object 对）和模型学习状态动态变化，现有方法使用静态预定义相关性或仅依赖分布先验，无法自适应调整区分过程。

## Method

### 框架概述 FGPL-A

FGPL-A 是一个 model-agnostic 的即插即用框架，包含三个核心组件：

1. **Adaptive Predicate Lattice (PL-A)**：动态维护谓词间两两相关性图。
   - 初始化：从预训练 SGG 模型在 SGG 数据集上的有偏预测中构建 Predicate Lattice (PL)，捕获基于上下文（subject-object 对）的谓词相关性。
   - 迭代精炼：提出 **Batch-Refinement (BR)** 机制，在每个 mini-batch 中通过模型当前预测更新相关性：
     - **Category Refining Momentum (CRM)**：类别级动量更新，聚合批次内分类混淆统计。
     - **Entity Refining Momentum (ERM)**：实体级动量更新，考虑具体 entity 上下文的变化。
   - 关键参数：动量系数 τ=0.99。

2. **Adaptive Category Discriminating Loss (CDL-A)**：
   - 基于 PL-A 中的谓词相关性，自适应识别难区分谓词对（相关性 > 阈值 ξ=0.9）。
   - 渐进式设置细粒度学习目标，随模型学习动态调整优化过程。
   - 包含 Predicate Correlation (PC) 和 Re-weighting Factor (RF) 两个子组件。

3. **Adaptive Entity Discriminating Loss (EDL-A)**：
   - 基于 specific entity context，自适应选择难区分谓词进行正则化。
   - 包含 Predicate Correlation (PC) 和 Balancing Factor (BF) 两个子组件。
   - 调整 entity 层面的区分过程，防止模型在难区分谓词上过拟合或欠拟合。

### FGPL 与 FGPL-A 的区别

- **FGPL**（基础版，CVPR 2022）：使用静态预定义的 Predicate Lattice，CDL 和 EDL 在整个训练过程中固定不变。
- **FGPL-A**（自适应版，TPAMI 2023）：引入 PL-A + Batch-Refinement，CDL-A 和 EDL-A 随模型学习状态动态调整。

## Experiments

### 数据集

| 数据集 | 图像数 (train/test/val) | 物体类别 | 谓词类别 | 备注 |
|--------|----------------------|---------|---------|------|
| VG-SGG | 75k/30k/5k | 150 | 50 | 标准 SGG 基准，70-30 划分 |
| GQA-SGG | 75k/10k/5k | 1704 | 311 | 更大规模、更复杂场景 |
| VG+MS-COCO (Sentence-to-Graph) | 36k/1k/5k | — | — | 41k 重叠图像 |
| MS-COCO (Image Captioning) | 113k/5k/5k | — | — | 标准 caption 划分 |

### Baseline 方法

Transformer (NeurIPS 2017)、Motif (CVPR 2018)、VCTree (CVPR 2019)，以及对比方法：CogTree、EQL、BASGG、Reweight*、HML、IETrans、EBM、SG、PUM、NARE、PCPL、DLFE、TDE、NICE、PPDL、RTPB、GCL 等。

### 训练设置

- **检测器**：预训练 Faster R-CNN（权重冻结）
- **SGG 模型**：Cross-Entropy Loss + SGD 优化器，lr=0.01，batch size=16
- **FGPL 超参**：α=1.5, β=2.0, ξ=0.9, |Vi|=5, δ=0.5, λ=0.1
- **FGPL-A 额外超参**：τ=0.99 (CRM 动量), θ=0.1 (CDL-A)
- **硬件**：4× NVIDIA GeForce RTX 3090, PyTorch 1.9.0, Ubuntu 20.04

### 评估协议

- **三个子任务**：PredCls（预训练 + 冻结检测器）、SGCls（给定 GT bbox 预测物体+关系）、SGDet（从零检测物体+关系）
- **指标**：Recall@K (R@K)、mean Recall@K (mR@K)、Group Mean Recall（Head/Body/Tail 分组）、DP@K (Discriminatory Power，自己提出)
- **下游任务**：Sentence-to-Graph Retrieval (R@K)、Image Captioning (Bleu-4, Meteor, Cider, Spice)

## Results

### VG-SGG PredCls mR@100 主要结果

| 模型 | mR@100 | 相比 baseline 提升 |
|------|--------|-------------------|
| Transformer (baseline) | 17.5 | — |
| Transformer + FGPL-A | **42.4** | **+24.9 (↑142.3%)** |
| VCTree (baseline) | 16.1 | — |
| VCTree + FGPL-A | **44.3** | **+28.2 (↑175.2%)** |
| Motif (baseline) | 15.8 | — |
| Motif + FGPL-A | **40.7** | **+24.9 (↑157.6%)** |

### GQA-SGG 结果（PredCls mR@100/R@100）

| 模型 | mR@100 | R@100 |
|------|--------|-------|
| Transformer | 4.5 | 58.7 |
| Transformer + FGPL-A | **7.9** | 58.7 |
| Motif | 4.6 | 58.6 |
| Motif + FGPL-A | **7.7** | 57.7 |

### Group Mean Recall（PredCls, VG-SGG）

| 模型 | Head (17) | Body (17) | Tail (16) | Mean |
|------|----------|----------|----------|------|
| Transformer | 38.8 | 9.6 | 3.1 | 17.2 |
| Transformer + Re-weight | 39.8 | 34.2 | 28.8 | 34.3 |
| Transformer + FGPL | 42.2 | 37.8 | 40.7 | 40.2 |
| Transformer + FGPL-A | **42.2** | **42.7** | **42.4** | **42.4** |

> FGPL-A 在 Head/Body/Tail 三组上表现几乎一致（42.2 vs 42.7 vs 42.4），证明其实现了高度平衡的谓词区分。

### Discriminatory Power (DP@K) 对比（PredCls, VG-SGG）

| 模型 | DP@5 | DP@10 | DP@20 | Mean |
|------|------|-------|-------|------|
| Transformer | 15.6 | 17.4 | 18.5 | 17.2 |
| Transformer + Re-weight | 33.3 | 36.1 | 38.1 | 35.8 |
| Transformer + FGPL | 37.9 | 40.3 | 42.1 | 40.1 |
| Transformer + FGPL-A | **38.6** | **41.1** | **42.9** | **40.3** |
| VCTree | 14.1 | 15.7 | 17.3 | 15.7 |
| VCTree + FGPL-A | **36.6** | **39.3** | **41.1** | **39.0** |
| Motif | 15.4 | 17.1 | 18.2 | 16.9 |
| Motif + FGPL-A | **37.1** | **39.6** | **41.5** | **39.4** |

### 下游任务 — Sentence-to-Graph Retrieval (R@100, Gallery 1000)

| 模型 | R@100 | 提升 |
|------|-------|------|
| Transformer | 35.9 | — |
| Transformer + FGPL-A | **51.8** | +15.9 |
| VCTree | 45.9 | — |
| VCTree + FGPL-A | **52.1** | +6.2 |
| Motif | 39.0 | — |
| Motif + FGPL-A | **54.9** | +15.9 |

### 下游任务 — Image Captioning

| 模型 | Bleu-4 | Meteor | Cider | Spice |
|------|--------|--------|-------|-------|
| Baseline | 35.3 | 27.6 | 111.8 | 20.6 |
| + Transformer (SGG) | 35.3 | 27.6 | 111.9 | 20.7 |
| + Transformer + FGPL-A | 35.3 | **27.8** | **112.2** | **21.1** |

### 消融实验关键发现

1. **CDL 组件**：PC (Predicate Correlation) + RF (Re-weight Factor) 均有效。CDL (PC+RF) 在 Transformer 上 mR@100 从 17.5 → 40.3，DP@10 从 17.4 → 40.3。
2. **EDL 组件**：PC 和 BF (Balancing Factor) 均必要。EDL (PC+BF) mR@100 24.4，移除任一组件均明显下降。
3. **Batch-Refinement**：CRM 和 ERM 联合使用达到最佳效果（mR@100 42.4, DP@10 41.1），缺任意一个均下降。
4. **阈值 ξ**：最优为 0.9，过大/过小均降低性能。
5. **动量 τ**：最优为 0.99（Mean mR/R@100 = 36.3/47.3）。

## Limitations

1. 头部谓词性能略有下降：如 "on"、"wearing"、"holding" 等头部谓词的 Recall 因被分类为更细粒度（如 "standing on"）而有小幅降低——这在细粒度分类中不可避免。
2. 超参数较多（α, β, ξ, δ, λ, τ, θ），调参成本较高。
3. GQA-SGG 上绝对性能仍较低（mR@100 ~8%），谓词类别从 50→311 后任务难度剧增。
4. PL-A 的初始化依赖预训练 SGG 模型的有偏预测，若预训练质量差可能影响初始相关性质量。

## Reusable Claims

1. **难区分谓词问题是独立于长尾问题的新挑战**：通用 SGG 模型偏向头部、重平衡策略偏向尾部，两者都无法处理语义重叠的谓词对。需要 pairwise predicate correlation 建模。
2. **谓词相关性是动态的**：随上下文（subject-object 对）和模型学习状态变化，需要在线更新而非静态预定义。
3. **自适应 Batch-Refinement 有效**：利用每个 mini-batch 的模型预测反馈来精炼相关性图，比静态 PL 提升约 2-4% mR@100。
4. **Group Mean Recall 比单一 mR@K 信息量更大**：FGPL-A 在 Head/Body/Tail 三组上几乎一致（~42%），远优于 Re-weight 方法（Head 40% vs Tail 29%）。

## Connections

- **与长尾 SGG 方法的关系**：FGPL-A 是对重平衡方法（Re-weight, TDE, GCL）的补充而非替代，它从"难区分性"而非"频率"角度处理谓词偏差。
- **与 FGPL (CVPR 2022)**：本文为相同作者的扩展期刊版，引入自适应机制（PL-A → BR → CDL-A/EDL-A），基础版使用静态 Predicate Lattice。
- **后续相关工作**：DRM (CVPR 2024) 进一步引入双粒度（谓词+三元组）建模，在 VG150 PredCls mR@100 达到 49.6。
- **受启发于**：Fine-Grained Image Classification 中的难区分物体分类思路。

## Open Questions

1. 头部谓词性能下降的 trade-off 能否通过更精细的损失设计消除？
2. 在 GQA-SGG（311 谓词类别）上性能下降明显，大规模谓词空间下的自适应相关性建模是否可扩展？
3. PL-A 的初始化质量对最终性能影响多大？能否不依赖预训练模型的偏置预测？
4. DP@K 指标是否有更广泛的应用场景，或可替代/补充现有 mR@K？

## Provenance

- **原始 PDF**：raw/sources/2023-TPAMI-adaptive-fine-grained-predicates-learning-scene-graph-generation.pdf（从 arXiv 下载，原始 inbound PDF 内容错误）
- **全文提取**：raw/sources/2023-TPAMI-adaptive-fine-grained-predicates-learning-scene-graph-generation.txt (104,551 chars, 17 pages)
- **arXiv**：[2207.04602](https://arxiv.org/abs/2207.04602)（2022年7月首次提交，TPAMI 2023出版）
- **DOI**：10.1109/TPAMI.2023.3298356
- **证据等级**：full-paper（全文精读）
