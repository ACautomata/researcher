---
title: "Salience-SGG: Enhancing Unbiased Scene Graph Generation with Iterative Salience Estimation"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - scene-graph-generation
  - unbiased-sgg
  - salience-estimation
  - iterative-decoder
  - spatial-understanding
  - attention-mechanism
  - arxiv-2026
  - one-stage-sgg
raw_sources:
  - ../../../sources/scene-graph/2026-arXiv-Salience-SGG-Enhancing-Unbiased-SGG-via-Salience-Estimation.pdf
  - ../../../sources/scene-graph/2026-arXiv-Salience-SGG-Enhancing-Unbiased-SGG-via-Salience-Estimation.txt
evidence_level: full-paper
paper:
  title: "Salience-SGG: Enhancing Unbiased Scene Graph Generation with Iterative Salience Estimation"
  abbreviated: "Salience-SGG"
  authors:
    - Runfeng Qu
    - Ole Hall
    - Pia K. Bideau
    - Julie Ouerfelli-Ethier
    - Martin Rolfs
    - Klaus Obermayer
    - Olaf Hellwich
  affiliations:
    - Technische Universität Berlin
    - Humboldt Universität zu Berlin
    - Univ. Grenoble Alpes, Inria, CNRS, Grenoble INP, LJK
    - Bernstein Center for Computational Neuroscience
    - Science of Intelligence Research Cluster of Excellence
  year: 2026
  venue: arXiv 2026 (2601.08728)
  doi: null
  arxiv: "2601.08728"
  code: "https://github.com/runfeng-q/Salience-SGG"
  url: null
related_pages:
  - cage-sgg-counterfactual-active-graph-evidence-open-vocabulary-sgg.md
  - compositionally-feature-augmentation-for-unbiased-scene-graph-generation.md
  - eicr-environment-invariant-curriculum-relation-learning-sgg.md
  - hilo-exploiting-high-low-frequency-for-unbiased-panoptic-scene-graph-generation.md
  - salience-temporal-encoding-dynamic-sgg.md
  - sdsgg-scene-specific-description-ovsgg.md
  - rethinking-evaluation-scene-graph-generation-stp-sid.md
---

# Salience-SGG: Enhancing Unbiased Scene Graph Generation with Iterative Salience Estimation

## 核心思想

已有的 Unbiased-SGG 方法通过重加权、重采样、伪标签等去偏策略提升稀有谓词上的 mR@K，但这种提升常以空间理解能力为代价——模型倾向过度依赖语义先验而忽视空间结构，导致空间上松散的对象对（spatially incoherent pairs）被误判为高置信度的稀有关系对，进而抑制空间上更显著的对象对被召回。作者将此问题称为 **salience insensitivity（显著性不敏感性）**。

**Salience-SGG** 提出 Iterative Salience Decoder (ISD)，通过语义无关的 triplet salience labels（仅基于空间重叠的二元掩码）引导 ISD 学习全局探索场景中最显著的空间结构，从而在不牺牲常见谓词性能的前提下提升无偏 SGG。

### 与现有方法的区别

- 现有二进制验证模块（如 Mg-RMPN [44]）的标签来源于标注三元组的语义（top-down），与 triplet 语义高度相关，无法充分支持模型探索显著空间结构
- Salience-SGG 的标签仅基于 subject 和 object 检测框与 GT 的空间 IoU（bottom-up），语义无关，迫使 ISD 依赖纯粹的视觉空间信息
- Salience 估计被公式化为一个迭代的消息传递过程（salience message-passing），而非一次性分类

## 方法

### 框架总览

1. **Object Detector**：Deformable DETR（ResNet-50），冻结训练，输出实体框 B、类别 C、特征 Q
2. **Predicate Decoder**：轻量 MLP，将 entity pair 特征（包含 box、GloVe 语义、query 特征）映射为 predicate logits G
3. **Iterative Salience Decoder (ISD)**：4 层 salience decoder layers，每层包含两个分支：
   - **Geometry Enhanced Self-Attention (G-ESA)**：在自注意力中加入实体框之间的 IoU，强化空间重叠实体的 salience 信息交互
   - **Predicate Enhanced Cross-Attention (P-ECA)**：在交叉注意力中加入预测谓词信息，指导 subject-object 间的 salience 消息传递
   - 迭代更新 subject 和 object salience queries → 逐步精炼 triplet salience 矩阵 M

### 关键技术点

- **Triplet Salience Label**：给定检测框 {b_i} 和 GT triplet 框 {b'_sk, b'_ok}，若 ∃k s.t. IoU(b_i, b'_sk) ≥ T 且 IoU(b_j, b'_ok) ≥ T，则 M'_ij = 1。T=0.6
- **Salience Queries 初始化**：利用 entity features Q 和类别分布 C 的线性投影产生 Q_sub⁰ 和 Q_obj⁰，不额外增加可学习向量
- **迭代精炼**：M_{l+1} = sigmoid(inverse_sigmoid(M_l) + Q_sub_{l+1} · (Q_obj_{l+1})^T / √d)，通过层次化的残差连接逐步优化 salience 估计
- **Loss**：Focal loss（L_salience）+ Seesaw loss（L_pre）+ DETR 的 entity loss（L_ent）
- **推理**：将 salience score 与 predicate score 结合用于 triplet 排序

### Salience 测量

引入 **Pairwise Localization Average Precision (pl-AP)** 衡量模型捕捉显著 subject-object 对的能力。对 top-100 检测 triplet，计算类别无关的 precision-recall，其中 true positive 定义为 subject 和 object 框与 GT 对的双重 IoU ≥ 0.5。pl-AP 与 F@100 正相关。

## 实验结果

### Visual Genome (VG) — SGDet 任务

| 方法 | 参数量 | R@100 | mR@100 | F@100 |
|------|--------|-------|--------|-------|
| Motifs [50] (CVPR2018) | 369.9M | 37.2 | 7.9 | 13.0 |
| TDE [39] (CVPR2020) | 369.9M | 20.2 | 11.0 | 14.3 |
| BGNN [26] (CVPR2021) | 341.9M | 35.8 | 12.6 | 18.6 |
| IETrans [51] (ECCV2022) | 369.9M | 27.3 | 18.2 | 21.8 |
| DRM [25] (CVPR2024) | — | 22.9 | 24.1 | 23.5 |
| Mg-RMPN [44] (ECCV2024) | — | 33.5 | 17.3 | 22.8 |
| Hydra-SGG [3] (ICLR2025) | 67.6M | 33.4 | 19.4 | 24.7 |
| **Salience-SGG (Ours)** | **77.7M** | **33.4** | **21.6** | **26.2** |

- SOTA F@100 = **26.2**（超越 Hydra-SGG 24.7 +1.5）
- SOTA mR@100 = **21.6**（同组 one-stage 最佳），mR@50=18.0
- 参数量仅 77.7M，远低于两阶段方法 300M+

### Open Images V6 (OIv6)

| 方法 | mR@50 | micro-R@50 | wmAPrel | wmAPphr | score |
|------|-------|------------|---------|---------|-------|
| Hydra-SGG [3] | — | 76.1 | 42.8 | 44.3 | 50.1 |
| **Salience-SGG (Ours)** | **48.0** | **78.1** | **45.6** | **44.9** | **51.8** |

- 全部指标 SOTA：score=**51.8**，wmAPrel=**45.6**（显著，+2.8 vs Hydra-SGG）
- 在启用去偏策略（seesaw loss）的条件下仍达到最好

### GQA-200

| 方法 | R@100 | mR@100 | F@100 |
|------|-------|--------|-------|
| DRM [25] (CVPR2024) | 21.7 | 21.0 | 21.3 |
| Hydra-SGG [3] (ICLR2025) | 26.5 | 15.9 | 19.9 |
| **Salience-SGG (Ours)** | **26.6** | **18.4** | **21.7** |

- SOTA F@100 = **21.7**，SOTA mR@100 = **18.4**

### 鲁棒性分析（表4）

控制 mR@K 相近时，Salience-SGG 的 F@K 显著高于对比方法，证明其去偏策略的鲁棒性：
- Salience-SGG (β=0.35) F@100=26.2 vs DRM F@100=23.5（mR@K 相近时）
- β=0.5 时实现 SOTA mR@50=21.4, mR@100=25.3

### ISD 兼容性（表5）

ISD 模块可直接插入已有两阶段方法：
- TDE+ISD: mR@100 11.0 → 12.4, F@100 14.3 → 16.4
- IETrans+ISD: mR@100 18.2 → 18.6, F@100 21.8 → 23.7

### 分组性能（表6）

| 模型 | Head(16) | Body(17) | Tail(17) | mR@100 |
|------|----------|----------|----------|--------|
| EGTR [17] | 24.3 | 19.4 | 13.3 | 18.9 |
| Salience-SGG (β=0.5) | 25.9 | 28.0 | 22.1 | 25.3 |
| Salience-SGG (β=0.2) | 27.4 | 22.8 | 15.0 | 21.6 |

Salience-SGG β=0.5 在 head/body/tail 三组上取得最高 mR@100，尤其 body 组 28.0（跨方法最高）。

### 消融实验（表7、8、9）

- **ISD**：完全移除 ISD 时 F@100 从 26.2 降至 21.1（-5.1），验证 salience 估计的关键作用
- **G-ESA + P-ECA**：任一缺失导致 R@K 和 mR@K 均下降，两模块互补
- **迭代精炼**：迭代 vs 非迭代 F@100 26.2 vs 25.4，表明迭代消息传递有益
- **Bottom-up vs Top-down 标签**：Bottom-up 标签（Ours）F@100=26.2 远超 top_down_gt (23.3)、top_down_entity (24.6)、top_down_triplet (24.1)，验证语义无关空间标签的有效性

## 核心贡献

1. 揭示 Unbiased-SGG 中 salience insensitivity 问题——去偏策略导致空间理解退化
2. 提出 Iterative Salience Decoder (ISD)，通过语义无关的 salience labels 引导模型恢复空间敏感性
3. G-ESA 和 P-ECA 两种增强注意力层，分别强化空间重叠和谓词引导的消息传递
4. 引入 pl-AP 指标定量评估模型捕捉显著空间结构的能力
5. 在 VG、OIv6、GQA-200 三个数据集上全面 SOTA，参数量仅为两阶段方法的 1/4-1/5

## 局限性

- 需要训练一个额外的 ISD 模块，增加计算开销（尽管参数量小）
- Salience label 的 IoU 阈值 T=0.6 需要人工设定
- pl-AP 指标仅关注 spatial 维度的显著度，未整合语义显著度
- 未在更多 backbones（如 Swin-T、ViT）上验证泛化性

## 源码

- [GitHub: runfeng-q/Salience-SGG](https://github.com/runfeng-q/Salience-SGG)

*最后更新：2026-06-09 | 证据等级：full-paper*
