---
title: "SSC-SGG: Semi-Supervised Clustering for Weakly Supervised Scene Graph Generation"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - scene-graph-generation
  - semi-supervised-learning
  - clustering
  - pseudo-labeling
  - prototype-based
  - long-tail-bias
  - AAAI-2025
raw_sources:
  - ../../../sources/scene-graph/2025-AAAI-SSC-SGG-Semi-Supervised-Clustering-Weakly-Supervised-Scene-Graph-Generation.pdf
  - ../../../sources/scene-graph/2025-AAAI-SSC-SGG-Semi-Supervised-Clustering-Weakly-Supervised-Scene-Graph-Generation.txt
related_pages:
  - prototype-based-embedding-network-scene-graph-generation.md
  - compositional-feature-augmentation-for-unbiased-scene-graph-generation.md
evidence_level: full-paper
paper:
  title: "SSC-SGG: Semi-Supervised Clustering for Weakly Supervised Scene Graph Generation"
  authors:
    - Jiarui Yang
    - Chuan Wang
    - Jun Zhang
    - Shuyi Wu
    - Zhao Jinjing
    - Zeming Liu
    - Liang Yang
  year: 2025
  venue: "Proceedings of the AAAI Conference on Artificial Intelligence (AAAI), 2025"
  arxiv: null
  doi: null
  code: null
  project: null
classification:
  label: "SSC-SGG — Semi-Supervised Clustering for Weakly Supervised Scene Graph Generation"
  task:
    - Scene Graph Generation (SGG)
    - Predicate Classification (PredCls)
    - Scene Graph Classification (SGCls)
    - Scene Graph Detection (SGDet)
  method_family:
    - Semi-supervised learning
    - Prototype-based clustering
    - Multi-view feature augmentation
    - Dynamic pseudo-label assignment
    - Optimal transport (Sinkhorn-Knopp)
  modality:
    - Visual features (RoI)
    - Relationship features (union box)
    - Multi-view augmented features
    - Prototype embeddings (GloVe-initialized)
  datasets:
    - Visual Genome (VG150)
    - Open Image V6
  metrics:
    - Recall@K (R@K)
    - mean Recall@K (mR@K)
    - Mean@K (average of R@K and mR@K)
    - wmAP_rel
    - wmAP_phr
    - score_wtd
---

## Citation

Jiarui Yang, Chuan Wang, Jun Zhang, Shuyi Wu, Zhao Jinjing, Zeming Liu, Liang Yang. "SSC-SGG: Semi-Supervised Clustering for Weakly Supervised Scene Graph Generation." *Proceedings of the AAAI Conference on Artificial Intelligence (AAAI)*, 2025, pp. 9220-9228.

## One-Sentence Contribution

提出基于原型聚类的半监督框架 SSC-SGG，利用稀疏标注数据引导从无标注物体对中挖掘有效交互伪标签（尤其是低频谓词），通过多视图原型聚类 + 动态伪标签分配极大提升了场景图生成的综合性能。

## Problem Setting

场景图生成（SGG）旨在检测图像中全部物体及其两两关系，输出三元组 `<subject, predicate, object>`。现有 SGG 数据集（如 VG）存在两个关键问题：

1. **稀疏标注**：图像中密集物体对（如 20+ 物体可产生数百对）只标注少量关系，大量有效交互（如 wheel-mounted on-bike）未被标注，被默认当作 background 处理。
2. **长尾偏置**：谓词频率高度不均衡，高频谓词（如 on, has）训练充分，低频谓词（如 mounted on, flying in）因有效样本稀少，易在 confusion training 中被误判为高频谓词或背景。

**现有方法缺陷**：
- 直接将未标注对视为 background 会：① 混淆训练过程（阻碍高置信预测）；② 加剧偏置（低频谓词更易被高频谓词「吸收」）。
- 现有伪标签方法（IETrans, ST-SGG）基于预训练模型置信度分配标签，易受数据集偏置影响，且需要复杂人工设计。

## Method

### 整体框架

SSC-SGG 框架包含三个核心模块：

1. **Multi-View Prototype-based Clustering (MPC)** — 多视图原型聚类框架
2. **Dynamic pseudo-Label Assignment (DLA)** — 动态伪标签分配算法
3. **Swap-Joint Training** — 交换联合训练策略

#### 1. 关系增强（Relationship Augmentation）

对输入图像进行像素级增强（ColorJitter, GaussianBlur），生成多个视图。只对第一个视图进行物体检测，其余视图的物体框通过 RoI 模块对齐提取框，从而自动对齐多视图关系特征。该方法额外增加约 33% 训练时间，但推理阶段不需多视图，不影响推理速度。

#### 2. 原型聚类（Prototype-based Clustering）

**原型构建**：为每个谓词类别分配一个原型（cluster centroid），初始化为 GloVe 300D 词向量，在预训练阶段通过标注数据微调：

$$q_k = MLP(Embed(l_k))$$

**原型正则化**：使用 ℓ₂,₁ 范数最小化不同原型间的余弦相似度，使簇中心在特征空间相互远离：

$$L_p = \|Q \cdot Q^T\|_{2,1}$$

**特征聚类**：对每个视图，计算关系特征与各原型的余弦相似度，获得预测 logits：

$$r_i^k = \frac{\exp(\|p_i^T\|_2 \|q_k\|_2 / \tau)}{\sum_{k'} \exp(\|p_i^T\|_2 \|q_{k'}\|_2 / \tau)}$$

多视图之间采用 swap-prediction 模式（Caron et al. 2020），保持不同视图预测概率分布的一致性。

#### 3. 动态伪标签分配（DLA）

针对长尾分布，将伪标签分配建模为最优运输问题：

$$\arg\max_{Y \in \mathcal{U}} \text{Tr}(Y^T X) + \lambda H(Y)$$

其中约束条件 $\mathcal{U}$ 强制每个 mini-batch 中每类平均被分配 $N/C$ 次，且单样本满足概率分布。这提高对低频样本的检测灵敏度。

**动态机制**：利用历史分配信息动态调整权重约束：

$$w_k = (sh_k \cdot f_k + 1)^\sigma, \quad f_k = -\log(n_k / n_{\text{total}})$$

通过 Sinkhorn-Knopp 算法迭代求解最优分配 $Y^*$，取 top-n 置信度最高的样本作为伪标签。

#### 4. 交换联合训练

对多视图使用交叉熵损失做 swap-prediction，联合标注数据损失与原型正则化损失：

$$\mathcal{L} = \mathcal{L}_u + \mathcal{L}_l + \mathcal{L}_p$$

### 训练流程

1. **预训练阶段**（50k iterations）：仅使用 MPC 框架训练，不产生伪标签
2. **半监督训练阶段**（10k iterations）：联合伪标签与标注数据，启用 DLA

## Experiments

### 数据集

- **VG150**：108k 图像，150 个物体类，50 个谓词类别
- **Open Image V6**：602 个物体类，30 个谓词类别

### 评估任务

- **PredCls**：给定 GT 物体框和标签，预测关系
- **SGCls**：给定 GT 物体框，同时预测物体标签和关系
- **SGDet**：从零检测整个场景图

### 评估指标

- **Recall@K (R@K)**: 标准召回率
- **mean Recall@K (mR@K)**: 各类别召回率的均值，反映对低频谓词的预测能力
- **M@K**: R@K 与 mR@K 的均值，反映综合性能
- Open Image：额外使用 wmAP_rel, wmAP_phr, score_wtd

### Baseline 方法

- Motifs (Zellers et al. 2018)
- VCTree (Tang et al. 2019)
- Transformer (Vaswani et al. 2017)
- 对比方法：TDE, NICE, IETrans, CFA, ST-SGG, CogTree

### 实现细节

- Backbone：Faster R-CNN + ResNeXt-101-FPN（参数冻结）
- λ=0.05, t=3 次 Sinkhorn 迭代, σ=0.5
- 每张图像平均 top-5 伪标签
- SGD 优化器, 60k iterations, lr=1e-3 (28k/48k decay)
- Batch size=8, RTX A5000 GPU
- 预训练 50k iter + 半监督 10k iter

## Results

### VG150（Table 1）

以 Motifs 为 baseline，SSC-SGG 框架在 M@100 上平均提升 13.4%（PredCls）、24.7%（SGCls）、8.4%（SGDet）——数值为三个 baseline（Motifs/VCTree/Transformer）的均值。

**与 SOTA 对比**：
- 相比 CFA（前 SOTA）：SSC-SGG 在 M@100 上平均超出 2.7%（PredCls）、5.7%（SGCls）、0.7%（SGDet）
- 相比 IETrans（伪标签方法）：平均超出 10.2% M@100
- 相比 ST-SGG（伪标签方法）：平均超出 11.8% M@100

**以 Motifs 为 baseline 的详细结果（VG150）**：

| 任务 | 方法 | R@50/100 | mR@50/100 | M@50/100 |
|------|------|----------|-----------|----------|
| SGDet | Motifs baseline | 65.2/67.5 | 18.8/21.9 | 40.3/42.3 |
| SGDet | + MPC | 65.7/67.8 | 20.2/22.1 | 43.0/45.0 |
| SGDet | + MPC + DLA (SSC-SGG) | 59.7/62.0 | 31.5/34.0 | 45.6/48.0 |

*注：SSC-SGG 的 R@K 略低于 baseline 是因更多预测转向了低频谓词，但 M@K 显著提升，表明综合性能改善。*

### Open Image V6（Table 2）

| 模型 | 方法 | mR@50 | R@50 | wmAP_rel | wmAP_phr | score_wtd |
|------|------|-------|------|----------|----------|-----------|
| Motifs | Baseline | 33.98 | 73.08 | 32.16 | 33.39 | 40.84 |
| Motifs | + SSC-SGG | **42.48** | 75.11 | 38.13 | 39.53 | **46.21** |
| Transformer | Baseline | 32.12 | 74.78 | 33.71 | 34.59 | 42.19 |
| Transformer | + SSC-SGG | **44.26** | 74.90 | 39.27 | 39.08 | **47.02** |

SSC-SGG 在 OI V6 上的 mR@50 大幅提升（Motifs: 33.98 → 42.48; Transformer: 32.12 → 44.26），证明框架良好的泛化性。

### 消融实验（Table 3, 4, 5, 6）

**组件消融（Table 3）**：
- 仅 MPC（vs vanilla Motifs）：mR@K 平均提升 40.7%，M@K 平均提升 7.8%
- MPC + DLA（完整 SSC-SGG）：M@K 平均再提升 5.2%

**标签分配方法对比（Table 4）**：
- Static hard label → Static soft label → Dynamic soft label（SSC-SGG）性能依次提升
- DLA（dynamic soft label）在 SGDet M@100 达 48.0，显著优于 static soft label（47.2）和 static hard label（45.3）

**与其他伪标签方法公平对比（Table 5）**：
在 Motifs 框架下比较 DLA vs IETrans vs ST-SGG，DLA 在所有子任务上取得最佳综合性能。

**多视图有效性（Table 6）**：
- 纯框架（无半监督）下单视图与多视图几乎无差异
- 半监督环境下多视图带来明显增益（SGDet M@100: 单视图 47.0 → 多视图 48.0）

## Reusable Claims

1. **稀疏标注 SGG 的本质问题**：不仅在于标注稀疏性本身，更在于将未标注有效交互样本当作 background 会导致 confusion training，加剧长尾偏置。这一洞察适用于所有弱/半监督 SGG 方法的设计。

2. **原型聚类的去偏优势**：聚类关注数据内在结构而非标签置信度，天然对数据集偏置更不敏感，适合半监督 SGG 的长尾场景。

3. **最优运输批量分配优于单样本阈值**：通过最优运输实现 mini-batch 级别的全局分配，自动平衡各类别伪标签数量，避免了繁琐的阈值手工设计。

4. **动态权重防止「偏置迁移」**：静态分配仅缓解初始偏置，但训练中会出现中频谓词升级为高频、低频仍被忽略的「偏置迁移」问题；基于历史分配信息的动态权重可有效避免。

5. **无需去偏操作即可去偏**：仅从无标注数据挖掘有效低频样本（不做任何标注数据重加权/重采样），即可显著提升低频谓词预测能力且不牺牲高频性能。

## Connections

- **PE-Net ([Prototype-based Embedding Network for SGG](prototype-based-embedding-network-scene-graph-generation.md))**：同样使用原型思想，但 PE-Net 用于全监督场景下的关系推断，SSC-SGG 将原型扩展到半监督框架中做聚类分配。
- **CFA ([Compositional Feature Augmentation](compositional-feature-augmentation-for-unbiased-scene-graph-generation.md))**：从特征增强角度解偏，SSC-SGG 从数据扩充（挖掘新样本）角度解偏，两种路线互补。
- **IETrans / ST-SGG**：同为伪标签方法，但 SSC-SGG 的聚类+最优运输分配策略显著优于其基于预训练置信度的分配策略。
- 与 SwAV (Caron et al. 2020) 的 swap-prediction 机制、Sinkhorn-Knopp 算法（Cuturi 2013）等 SSL 方法有紧密技术渊源。

## Open Questions

- 伪标签的置信度质量控制：top-5 策略是否最优？能否自适应每张图的伪标签数量？
- 预训练阶段（50k iter）与半监督阶段（10k iter）的比例影响：更多半监督训练是否进一步提升？
- 本文仅在两阶段 SGG 框架上验证，能否扩展到一阶段 SGG（如 SGTR+）？
- 动态机制参数（σ, λ, t）在不同数据集/分布下的敏感性如何？

## Provenance

- **原始 PDF**：`sources/scene-graph/2025-AAAI-SSC-SGG-Semi-Supervised-Clustering-Weakly-Supervised-Scene-Graph-Generation.pdf`
- **全文提取**：`sources/scene-graph/2025-AAAI-SSC-SGG-Semi-Supervised-Clustering-Weakly-Supervised-Scene-Graph-Generation.txt` (49093 bytes)
- **作者团队**：Jiarui Yang (Fudan/IIE CAS), Chuan Wang (BJTU/IIE CAS) 等
- **入库日期**：2026-06-09
