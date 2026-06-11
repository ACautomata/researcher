---
title: "DSGG: Dense Relation Transformer for an End-to-end Scene Graph Generation"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - scene-graph-generation
  - panoptic-scene-graph-generation
  - dense-relation
  - graph-aware-query
  - end-to-end
  - transformer
  - cvpr-2024
raw_sources:
  - ../../../sources/scene-graph/2024-06-17-dsgg-dense-relation-transformer-end-to-end-scene-graph-generation.pdf
  - ../../../sources/scene-graph/2024-06-17-dsgg-dense-relation-transformer-end-to-end-scene-graph-generation.txt
related_pages:
  - reltr-relation-transformer-scene-graph-generation.md
  - is-ggt-iterative-scene-graph-generation-with-generative-transformers.md
  - sgtr-end-to-end-scene-graph-generation-with-transformer.md
  - panoptic-video-scene-graph-generation.md
  - prototype-based-embedding-network-scene-graph-generation.md
evidence_level: full-paper
paper:
  title: "DSGG: Dense Relation Transformer for an End-to-end Scene Graph Generation"
  abbreviated: "DSGG"
  authors:
    - Zeeshan Hayder
    - Xuming He
  affiliations:
    - Data61-CSIRO, Australia
    - ShanghaiTech University
  year: 2024
  venue: IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) 2024
  doi: null
  arxiv: null
  code: "https://github.com/zeeshanhayder/DSGG"
  url: null
classification:
  label: Dense Relation Transformer for End-to-end Scene Graph Generation
  task:
    - Scene Graph Generation (SGG)
    - Panoptic Scene Graph Generation (PSG)
  method_family:
    - Dense Relation Transformer
    - Graph-aware Query
    - Set Prediction (DETR-based)
    - Sub-graph Matching
    - Relation Distillation
  modality: Image
  datasets:
    - Visual Genome (VG)
    - Panoptic Scene Graph (PSG)
  metrics:
    - Recall@K (R@K)
    - mean Recall@K (mR@K)
    - Mean@K (M@K)
    - Zero-shot Recall@K (zR@K)
---

# DSGG: Dense Relation Transformer for an End-to-end Scene Graph Generation

## Citation

Zeeshan Hayder, Xuming He. "DSGG: Dense Relation Transformer for an End-to-end Scene Graph Generation." IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2024.

## One-Sentence Contribution

提出 **DSGG**（Dense Scene Graph Generation），将场景图生成建模为直接图预测问题，利用**图感知查询（graph-aware queries）**联合编码节点及其所有关系边，通过**松弛子图匹配（relaxed sub-graph matching）**和**关系蒸馏（relation distillation）**实现密集、端到端的场景图生成，显著提升了低频关系和语义重叠场景下的性能。

## Problem Setting

场景图生成（SGG）的目标是从图像中检测所有 object 及其 class labels、bounding boxes、pixel-accurate segmentation，以及 object 之间的 pairwise 语义关系。表示为图 G = (V, E)，其中节点 V 是 entities（category + bounding box + optional mask），有向边 E 是 predicates。

**核心挑战**：
1. **不完备标注（incomplete labelling）**：数据集中很多关系未被标注
2. **长尾关系分布（long-tail relationship categories）**：大部分关系实例集中在少数高频类别
3. **关系语义重叠（relational semantic overlap）**：同一对 entity 之间存在多种语义关系（如"人牵马" + "人看马"）

**现有方法的局限**：
- 现有的基于 Transformer 的方法采用**独立 object 和 predicate 查询**或**三元组查询（triplet queries）**，每个查询编码一个 ⟨subject, predicate, object⟩ 三元组
- 三元组查询方法扩展性差：要建模密集场景图需要 O(N²) 个查询，随着物体数量线性增长
- HiLo [37] 用双流网络（high-low/low-high）加伪标签处理关系不平衡，但无法全面捕获所有关系和语义重叠问题

DSGG 将 SGG 视为**直接图预测问题**：一张图像 → 一个图（包含所有节点和边），使用 |V| 个 graph-aware queries 编码每个节点及其所有出站关系边。

## Method

### 整体架构

DSGG 是**单阶段 Transformer** 网络：

1. **Backbone + Transformer Encoder**：ResNet-50 / Swin-B / Swin-L backbone → 图像特征 → 位置编码 → Transformer encoder
2. **Graph-aware Queries**：N 个 graph-aware queries Qi，每个 query 编码一个节点（object）及其所有出站关系边。N = 100
3. **Compositional Tokens**：通过 pairwise 组合 graph-aware queries 生成 S ∈ R^(N×N×P) 的 compositional tokens，再经 MLP + Sigmoid 生成密集边缘概率图
4. **Relation Distillation**：学习 predicate filter F 动态过滤 pairwise relations，用 Sigmoid attention 替代标准 Softmax 以支持多标签关系预测
5. **Relation Re-scoring**：用 object confidence 乘积对关系概率重评分：p(Ê_ij) = p(V̂_i) × p(V̂_j) × p(Ê_ij | Q_i, Q_j)
6. **Logit Adjustment**（后处理）：权重 0.15 的 logit adjustment 缓解关系标签噪声，辅以 NMS 去重

### Graph-aware Queries（核心创新）

与 triplet queries（每个查询 = 一个三元组）不同，graph-aware queries：

- 每个节点关联唯一一个 graph-aware query
- 每个 query 编码了节点属性（class、bbox、mask）及其到所有其他节点的有向边特征
- 关系预测通过 **pairwise 组合**两个 graph-aware queries 计算：p(Ê_ij | Q_i, Q_j) = MLP(Q_i ⊕ Q_j)
- 使用 Sigmoid 激活（而非 Softmax）支持多标签关系分类（同一对 entity 可以有多个关系）

### Relaxed Sub-graph Matching

将预测图 Ĝ 和 GT 图 G 的匹配形式化为二次分配（QA）问题。因 QA 是 NP-hard，提出**上界近似**将 QA 简化为线性分配形式，使用 **Hungarian 算法**高效求解。

匹配代价包含：
- Ce(V_i, V̂_σ(i))：节点级代价（类别 CE + box IoU）
- Cr(r_ij, r̂_σ(i,j))：边级代价（关系标签 CE）

### Relation Distillation

- 学习 predicate filter F = Sigmoid(Q × Q^T / √d_q)，判断每对 entity 之间是否存在**至少一个**关系（而非具体关系类型）
- 过滤后的关系概率：p(Ê_ij) = F_ij × MLP(Q_i ⊕ Q_j)
- 在训练中动态学习，不依赖训练集统计预定义的三元组候选集

### 训练目标

多任务损失：L = λ_box L_box + λ_giou L_giou + λ_ent L_ent + λ_rel L_rel

- L_rel：对所有 pairwise 边应用 focal loss
- PSG 任务额外加 L_dice + L_focal（λ = 1）
- 端到端联合训练

### Relation Re-scoring

最终 pairwise 关系概率 = p(V̂_i) × p(V̂_j) × p(Ê_ij | Q_i, Q_j)，用 object confidence 加权，无 lambda scaling。

## Experiments

### 数据集

**Visual Genome (VG)**：108,077 图像，50 个 predicate 关系类别，150 个 object 类别。遵循 [31] 的 train/val/test 划分。

**Panoptic Scene Graph (PSG)**：48,749 图像，80 个 thing 类，53 个 stuff 类，56 个 predicate 类别。2,177 张测试图像，其中 28 个 rare predicate（<500 实例）和 28 个 non-rare 关系类别。927 张测试图像存在同一对 entity 的多重关系。

### 评估指标

- **Recall@K (R@K)**：Top-K 预测三元组中正确预测的比例
- **mean Recall@K (mR@K)**：逐类别计算 Recall 后取平均（对低频类更公平）
- **Mean@K (M@K)**：R@K 和 mR@K 的平均值
- **PredCIs / SGCIs / SGDet**：标准 SGG 评估设置（predicate classification、scene graph classification、scene graph detection）
- **Zero-shot Recall**：测试未见过的关系组合

### 实现细节

- 100 个 graph-aware queries（N = 100）
- Backbone：ResNet-50、Swin-B、Swin-L
- **SGG 任务**：60 epochs，从零训练（无预训练检测器）
- **PSG 任务**：12 epochs，用 Mask2Former（COCO 预训练）初始化 backbone 后微调
- 位置编码 + 默认 encoder/decoder 层数
- 256 维 compositional tokens
- AdamW 优化器，weight decay 10⁻⁴
- 学习率：backbone 10⁻⁵、transformer 10⁻⁴、SGG head 10⁻⁴
- 4× A100 GPUs，PSG batch=1, SGG batch=4
- 后处理：logit adjustment（权重 0.15）+ NMS 去重，最终取 top-100 三元组

## Results

### Visual Genome — SGDet (Table 1)

| Method | R@50 | R@100 | mR@50 | mR@100 | M@50 | M@100 |
|--------|:----:|:-----:|:-----:|:------:|:----:|:-----:|
| Motifs [34] | 32.1 | 36.8 | 6.6 | 7.9 | 19.4 | 22.4 |
| VCTree [29] | 31.9 | 36.0 | 6.4 | 7.3 | 19.2 | 21.7 |
| BGNN [13] | 31.0 | 35.8 | 10.7 | 12.6 | 20.9 | 24.2 |
| SGTR [14] | 20.6 | 25.0 | 15.8 | 20.1 | 18.2 | 22.6 |
| SS-RCNN [30] | 23.7 | 27.3 | 18.6 | 22.5 | 21.2 | 24.9 |
| SHA-GCL [9] | 14.9 | 18.2 | 17.9 | 20.9 | 16.4 | 19.6 |
| NICE [12] | 27.8 | 31.8 | 12.2 | 14.4 | 20.0 | 23.1 |
| Relationformer [26] | 28.4 | 31.3 | 9.3 | 10.7 | 18.9 | 21.0 |
| HetSGG [33] | 30.0 | 34.6 | 12.2 | 14.4 | 21.1 | 24.5 |
| PE-Net [36] | 26.5 | 30.9 | 16.7 | 18.8 | 21.6 | 24.9 |
| **DSGG (ours)** | **26.5** | **32.9** | **20.2** | **25.5** | **23.4** | **29.2** |

- DSGG 在 mR@50/100 上全面领先（20.2/25.5），比 SS-RCNN（18.6/22.5）高 1.6/3.0 点
- DSGG 的 M@50/100（23.4/29.2）也是最优，展现 recall 和 mean recall 的最佳平衡
- DSGG 无 logit adjustment 时 mR@50/100 = 13.0/17.3，LA 大幅提升了 mR

### Visual Genome — SGDet PredCIs 和 SGCIs (Table 1)

**PredCIs**：DSGG (ours) R@50/100 = 53.9/65.1，mR@50/100 = 39.4/49.9，M@50/100 = 46.7/57.5
- mR 和 M 全面最优，mR@50 39.4 远超第二 PE-Net 38.8

**SGCIs**：DSGG (ours) R@50/100 = 33.1/38.0，mR@50/100 = 23.7/29.7，M@50/100 = 28.4/33.9
- mR 和 M 全面最优，mR@50 23.7 远超第二 PE-Net 22.2

### Panoptic Scene Graph — PSG (Table 2)

| Method | Backbone | R@20 | mR@20 | R@50 | mR@50 | R@100 | mR@100 |
|--------|:--------:|:----:|:-----:|:----:|:-----:|:-----:|:------:|
| PSGTR [32] | R50 | 28.4 | 16.6 | 34.4 | 20.8 | 36.3 | 22.1 |
| HiLo [37]† | R50 | 34.1 | 23.7 | 40.7 | 30.3 | 43.0 | 33.1 |
| **DSGG (ours)** | **R50** | **32.7** | **30.8** | **42.8** | **38.8** | **50.0** | **43.4** |
| HiLo [37]† | Swin-B | 38.5 | 28.3 | 46.2 | 35.3 | 49.6 | 39.1 |
| **DSGG (ours)** | **Swin-B** | **35.5** | **32.9** | **46.5** | **41.3** | **54.2** | **46.3** |
| HiLo [37]† | Swin-L | 40.6 | 29.7 | 48.7 | 37.6 | 51.4 | 40.9 |
| **DSGG (ours)** | **Swin-L** | **36.2** | **34.0** | **47.0** | **41.7** | **54.3** | **47.8** |

- **mR@50/100** 在所有 backbone 设置下全面最优，且优势巨大
- R50 backbone：mR@50 38.8 vs HiLo 30.3（+8.5），mR@100 43.4 vs HiLo 33.1（+10.3）
- Swin-L backbone：mR@50 41.7 vs HiLo 37.6（+4.1），mR@100 47.8 vs HiLo 40.9（+6.9）
- R@100 上 DSGG 全面超越 HiLo（50.0 vs 43.0 在 R50, 54.3 vs 51.4 在 Swin-L）
- R@20/R@50 上 HiLo 略高，但 DSGG 在 mR 上的优势表明模型在低频关系上远优于 HiLo
- †标记的 HiLo 使用额外伪标签训练，DSGG 不使用额外标签

### Ablation — 组件贡献 (Table 3, VG SGDet)

| Relation Rescoring | Relation Distillation | Logits Adj. | R@50/100 | mR@50/100 | M@50/100 |
|:------------------:|:--------------------:|:-----------:|:--------:|:---------:|:--------:|
| | | | 6.9/11.2 | 11.9/15.6 | 9.4/13.4 |
| ✓ | | | 25.9/32.6 | 12.5/15.7 | 19.2/24.2 |
| ✓ | ✓ | | 32.9/38.5 | 13.0/17.3 | 23.0/28.0 |
| ✓ | ✓ | ✓ | 26.5/32.9 | **20.2/25.5** | **23.4/29.2** |

- Relation Rescoring + Distillation 主要提升 R@K（6.9→32.9）
- Logit Adjustment 在略微降低 R@K 的条件下大幅提升 mR@K（13.0→20.2），实现最佳平衡

### 关系语义重叠子集 (Table 5, PSG)

PSG 中 927 张存在同一对 entity 多重关系的图像：

| Method | Backbone | R@20 | mR@20 | R@50 | mR@50 | R@100 | mR@100 |
|--------|:--------:|:----:|:-----:|:----:|:-----:|:-----:|:------:|
| HiLo [37] | R50 | 43.6 | 30.8 | 49.7 | 36.2 | 51.1 | 38.8 |
| **DSGG** | **R50** | **48.6** | **37.6** | **58.2** | **48.6** | **63.6** | **50.2** |
| ∆ | | +5.0 | +6.8 | +8.5 | +12.4 | +12.5 | +11.4 |
| HiLo [37] | Swin-B | 51.3 | 36.4 | 57.9 | 42.2 | 59.9 | 45.0 |
| **DSGG** | **Swin-B** | **52.7** | **41.3** | **60.9** | **49.6** | **66.7** | **54.7** |
| HiLo [37] | Swin-L | 53.1 | 36.3 | 60.7 | 46.7 | 62.6 | 49.0 |
| **DSGG** | **Swin-L** | **53.4** | **42.6** | **62.1** | **50.3** | **68.0** | **55.2** |

- 在语义重叠子集上 DSGG 大幅领先 HiLo 所有设置
- R50 backbone：mR@100 50.2 vs HiLo 38.8（+11.4）
- 证明 graph-aware queries 的多标签 Sigmoid 设计能有效解决同一对 entity 的多重关系预测

### 低频关系性能 (Table 6, PSG Rare Categories 28 classes)

| Method | Backbone | mR@20 | mR@50 | mR@100 |
|--------|:--------:|:-----:|:-----:|:------:|
| HiLo [37] | R50 | 10.4 | 17.0 | 20.3 |
| **DSGG** | **R50** | **20.9** (+10.5) | **31.0** (+14.0) | **33.7** (+13.4) |
| HiLo [37] | Swin-B | 13.1 | 20.3 | 24.6 |
| **DSGG** | **Swin-B** | **23.0** (+9.9) | **33.9** (+13.6) | **38.1** (+13.5) |
| HiLo [37] | Swin-L | 14.2 | 22.6 | 26.3 |
| **DSGG** | **Swin-L** | **23.6** (+9.4) | **30.1** (+7.5) | **36.0** (+9.7) |

- 在低频关系（<500 实例）上 DSGG 全面大幅超越 HiLo
- mR@50 提升 7.5–14.0 点，证明 graph-aware queries 和 sub-graph matching 有效缓解了长尾问题
- HiLo 专门设计了 High-Low/Low-High 双流网络处理频率差异，DSGG 不做专门设计反而表现更好

### Top-20 和 Zero-shot (Table 4, VG)

**Top-20 预测**（SGDet mR@20）：
- DSGG (ours): mR@20 = 14.2, R@20 = 18.7（与 Unbiased 13.0, PE-Net 16.3 等对比）
- 仅用 20 个 queries 时 DSGG 仍达到最优（表 4 左）

**Zero-shot Recall**（SGDet zR@50/100）：
- DSGG (ours): zR@50 = 3.5, zR@100 = 5.2
- 全面超越 VCTree+TDE (2.6/3.2)、SS-RCNN (3.1/4.5)、PE-Net (2.3/3.6)

### 模型参数

DSGG 参数更少，因为无需双流 decoder：

| Backbone | DSGG | HiLo [37] |
|----------|:----:|:--------:|
| ResNet-50 | 44.2M | 58.8M |
| Swin-B | 107.1M | 121.7M |
| Swin-L | 215.6M | 230.3M |

## Limitations

1. **R@K 在高频关系上不是最优**：在 VG 的 SGDet 上 R@50 = 26.5，不如 Motifs（32.1）和 BGNN（31.0）等使用先验知识的方法。DSGG 在 Recall 上以 mR@K 为核心优势。
2. **额外后处理依赖**：依赖 logit adjustment（权重 0.15）和 NMS 去重，增加推断复杂度
3. **训练 epoch 差异大**：SGG 任务训练 60 epochs，PSG 任务仅微调 12 epochs，PSG 可能还有进一步提升空间
4. **仅评估静态图像**：未扩展到视频场景图（如 Action Genome、VidOR）
5. **Sub-graph matching 的近似上界**：QA→线性近似的上界虽可计算，但理论上界 gap 未定量分析

## Reusable Claims

1. **Graph-aware queries 替代 triplet queries 实现密集场景图预测**：每个 query 编码一个节点及其所有关系边（而非一个三元组），以 O(|V|) 的 query 数量实现 O(|V|²) 的关系预测，消除 triplet queries 的扩展性瓶颈。
2. **Relaxed sub-graph matching 将图匹配简化为线性分配**：将 NP-hard 的二次分配问题上界近似为线性形式，可用 Hungarian 算法高效求解，支持端到端训练。
3. **多标签 Sigmoid 关系分类解决语义重叠**：标准 Softmax 只能输出单一 predicate，Sigmoid 支持同一对 entity 输出多个共存关系，在 PSG 语义重叠子集上 mR@100 领先 HiLo 11.4 点（R50）。
4. **Predicate filter（Sigmoid attention）实现动态关系蒸馏**：相比基于统计预定义三元组候选集的方法，模型自动学习哪些 entity 对之间存在关系，可捕获训练集中遗漏的关系组合。
5. **无需专门长尾设计即能处理长尾关系**：不依赖伪标签或双流网络（如 HiLo），在 PSG 低频类别（<500 实例）上 mR@50 仍超越 HiLo 7.5–14.0 点。
6. **参数效率高**：44.2M（R50）vs HiLo 58.8M，减少了约 25% 参数，原因是去掉了双流 decoder 结构。
7. **更少的 queries 即可工作**：仅用 20 个 graph-aware queries 在 VG SGDet mR@20 上达到 14.2，与 100 queries 的 Unbiased (13.0) 相当。

## Connections

- 与 [RelTR](reltr-relation-transformer-scene-graph-generation.md) 同为 **Transformer-based end-to-end** SGG 方法，但 DSGG 使用 graph-aware queries（每个 query 编码节点 + 所有边），而 RelTR 使用 coupled triplet queries（每个 query 编码一个 ⟨subject, predicate, object⟩ 三元组）
- 与 **HiLo**[37] 直接对比且超越，HiLo 是 CVPR 2023/ICCV 2023 的端到端 SGG/PSG SOTA，DSGG 在无伪标签条件下仍全面领先
- 与 **SGTR**[14] 对比，SGTR 是首个 DETR-based SGG 方法，使用 graph assembling；DSGG 直接在 transformer 输出时预测全图
- 与 **PSGTR**[32]、**PSGFormer**[32] 对比，PSGTR 是 triplet query 方法，PSGFormer 是配对方法，DSGG 将二者统一为 graph-aware 范式
- 与 **SS-RCNN**[30] 同为 single-stage 方法，但 DSGG 使用 transformer 而非 R-CNN 架构
- 与 **PE-Net**[36] 对比，PE-Net 使用 prototype embedding，DSGG 使用 graph-aware queries，DSGG 在 mR@K 上显著更高

## Open Questions

1. DSGG 能否扩展到视频场景图生成（dynamic SGG, VidOR, Action Genome）？视频场景增加时序维度后 graph-aware queries 需要如何扩展？
2. Logit adjustment 在不同 backbone 和数据集上的最优超参数（当前固定 0.15）
3. 减少 query 数量（N=100）的规律性：理论上 graph-aware queries 数量应等于 |V|，但 100 是否足够覆盖 VG 中平均物体数量？
4. 能否将 graph-aware queries 与显式场景图结构先验（如 Motifs 的统计规律）结合，以同时提升 R@K 和 mR@K？
5. Sub-graph matching 的理论上界 gap 有多大？更紧的上界是否可带来性能提升？
6. DSGG 在 PSG 任务上仅微调 12 epochs，是否有较大欠拟合空间？

## Provenance

- **Evidence Level**: full-paper
- **Source**: CVPR 2024, 10 页正文（含参考文献），51985 字符提取文本
- **Extraction**: PyMuPDF 全文提取，包含所有 6 张表格和相关图示描述
- **Verification**: 文本完整，包含所有表格数据、算法伪代码可重建
