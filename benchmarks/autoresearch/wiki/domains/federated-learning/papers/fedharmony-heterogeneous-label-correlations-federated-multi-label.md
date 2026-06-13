---
title: FedHarmony: Harmonizing Heterogeneous Label Correlations in Federated Multi-Label Learning
type: paper
domain: federated-learning
status: active
created: 2026-05-05
updated: 2026-05-05-evidence-upgrade
tags:
  - federated-learning
  - multi-label-learning
  - label-correlation
  - heterogeneity
paper:
  title: "FedHarmony: Harmonizing Heterogeneous Label Correlations in Federated Multi-Label Learning"
  authors:
    - Zhiqiang Kou
    - Junxiang Wu
    - Wenke Huang
    - Wenwen He
    - Ming-Kun Xie
    - Changwei Wang
    - Yuheng Jia
    - Di Jiang
    - Yang Liu
    - Xin Geng
    - Qiang Yang
  year: 2026
  venue: arXiv
  arxiv: "2604.28024v1"
  doi: ""
  code: ""
  project: ""
classification:
  label: federated-learning
  task:
    - federated multi-label learning
  method_family:
    - label correlation learning
    - federated learning
  modality:
    - multi-label data
  datasets:
    - FLAIR
    - MS-COCO
    - PASCAL VOC2007
  metrics:
    - mAP
    - O-mAP
    - CP/CR/CF1
    - OP/OR/OF1
evidence_level: full-paper
raw_sources:
  - raw/sources/2026-04-30-fedharmony-heterogeneous-label-correlations.pdf
source_pages:
  - wiki/domains/federated-learning/concepts/federated-learning.md
---

# FedHarmony: Harmonizing Heterogeneous Label Correlations in Federated Multi-Label Learning

## Citation

Kou et al., "FedHarmony: Harmonizing Heterogeneous Label Correlations in Federated Multi-Label Learning," arXiv:2604.28024v1, Apr 2026.

## One-Sentence Contribution

提出 consensus correlation 机制——利用其他客户端的标签相关性共识作为全局教师信号，纠正联邦多标签学习中因客户端异质性导致的 label correlation drift。

## Problem Setting

联邦多标签学习（FedMLL）的核心挑战：因客户端特定的标签空间和共现模式的差异，本地学到的标签相关性必然偏离全局结构——称为 **label correlation drift**。现有方法（FedAvg 变体）按数据量加权平均，忽略标签相关性的质量差异。

## Method

FedHarmony 两大核心机制：

1. **Consensus Correlation**：从其他客户端的标签相关性中提取共识模式，作为全局教师信号来纠正各客户端有偏的局部估计。
2. **Quality-weighted Aggregation**：聚合时不仅按数据量，还按相关性质量评估和加权每个客户端。
3. **Accelerated Optimization**：开发加速优化算法，理论证明在不牺牲精度下实现更快收敛。

## Experiments

**数据集（3 个多标签基准）**

- **FLAIR**：实例分割标注，细粒度标签（16 类别，1,628 细粒度标签），自然存在数量和标签分布偏斜。按 Dirichlet 分布诱导非 IID 分区。
- **MS-COCO (COCO-80)**：约 330K 图像，80 个目标类别，标准多标签公式。按三类异构轴（Dirichlet 浓度、客户端数、变换集）诱导非 IID。
- **PASCAL VOC2007**：20 类别，9,963 张图像。同上诱导非 IID。

**训练配置**

- 统一 ViT-B/16 backbone + C-way sigmoid 分类头。
- Adam 优化器，学习率 1e-4，batch size 16。
- 本地训练每轮 5 epochs，总通信轮次 T=50。
- 非均匀客户端采样（采样概率与本地数据量成正比，应对数量偏斜）。
- 8 张 NVIDIA RTX 4090 GPU，PyTorch 实现。

**Baselines (8 个)**

三类方法：(i) 优化驱动聚合——FedAvg、FedProx、FedNova；(ii) 曲率/几何感知——FedCurv、SphereFed；(iii) 任务/特征感知——FedLGT（联邦多标签分类）、FedRDN（联邦特征增强）。所有方法使用相同 backbone、优化器、客户端分区和通信预算以确保公平。

**评估指标（8 个）**

mAP、O-mAP (overall mAP)、CP (class-wise precision)、CR (class-wise recall)、CF1、OP (overall precision)、OR (overall recall)、OF1 (overall F1)。

## Results

**主实验 (Table 1)**

FedHarmony 在所有三个数据集和全部 8 个指标上取得最优：

- **FLAIR**：mAP 51.0%，比最强基线 FedProx (39.6%) 提升 **+11.4 mAP**；OF1 75.1 vs. FedProx 65.8；O-mAP 84.0。
- **COCO-80**：mAP 71.4%，比 FedNova (64.5%) 提升 +6.9 mAP；OF1 72.7；在所有 8 个指标上全面领先。
- **VOC2007**：mAP 86.9%，比 FedRDN (78.3%) 提升 +8.6 mAP；OF1 83.4。

**定性分析 (Fig. 3)**

FedAvg 常产生伪标签（如 COCO 马图像上预测 "bird"）或遗漏语义，FedHarmony 产出更一致、语义准确的标签集，恢复缺失的 equipment/material/structure 标签。

**训练时间 (Table 2)**

Block-Optimized (B-OPT) 变体显著加速收敛：
- FLAIR Round 1：B-OPT 3:59 vs. NB-OPT 5:14；Round 10：40:22 vs. 56:19（节省 ~28%）。
- VOC2007 Round 10：9:29 vs. 13:51（节省 ~32%）。

## Limitations

- 共识计算假设客户端间有足够的标签重叠（cross-client label overlap），label spaces 完全不相交时可能退化。
- 计算 consensus correlation 的通信和计算开销未量化。

## Reusable Claims

- 声明：联邦多标签学习中，按数据量简单加权平均客户端更新会忽略标签相关性质量的差异。
  证据：FedHarmony 在 FLAIR 上的 co-occurrence matrix 可视化展示显著跨客户端差异。
  范围：federated multi-label learning。
  置信度：medium。

- 声明：跨客户端的 consensus label correlation 可以有效作为纠正局部估计偏差的教师信号。
  证据：FedHarmony 实验验证 consensus correlation 的有效性。
  范围：有跨客户端标签重叠的 FedMLL 场景。
  置信度：medium。

## Connections

- [FL Heterogeneity and Optimization](../topics/fl-heterogeneity-and-optimization.md)：本论文属于聚合层异质性优化——label correlation consensus 作为标签空间的聚合信号。
- [Federated Learning](../concepts/federated-learning.md)：本论文解决 FL 中的 multi-label 特有问题。
- [FedHD](fedhd-federated-distillation-whole-slide-image.md)：也是联邦学习 + 跨客户端知识迁移，但使用蒸馏而非 correlation harmonization。

## Open Questions

- 标签空间中几乎没有重叠的 extreme heterogeneity 场景如何处理？
- Consensus correlation 能否与 personalization 结合（per-client residual correlation on top of consensus）？

## Provenance

- 摄入时间：2026-05-05。
- 原始来源：[raw/sources/2026-04-30-fedharmony-heterogeneous-label-correlations.pdf](../../../raw/sources/2026-04-30-fedharmony-heterogeneous-label-correlations.pdf)。
- 证据等级：full-paper（完整实验数据从 PDF 提取，包含 Table 1 全部 8 方法 × 3 数据集 × 8 指标定量结果和训练时间比较）。
