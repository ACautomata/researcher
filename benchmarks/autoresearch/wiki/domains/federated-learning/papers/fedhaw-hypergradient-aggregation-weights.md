---
title: "FedHAW: Federated Learning with Hypergradient-based Online Update of Aggregation Weights"
type: paper
domain: federated-learning
status: active
created: 2026-05-05
updated: 2026-05-05-evidence-upgrade
tags:
  - federated-learning
  - aggregation-weights
  - hypergradient
  - online-update
  - communication-errors
paper:
  title: "FedHAW: Federated Learning with Hypergradient-based Online Update of Aggregation Weights"
  authors:
    - Ayano Nakai-Kasai
    - Tadashi Wadayama
  year: 2026
  venue: IEEE (letter)
  arxiv: "2605.00458v1"
  doi: ""
  code: ""
  project: ""
classification:
  label: federated-learning
  task:
    - aggregation weight optimization
  method_family:
    - hypergradient descent
    - learnable aggregation weights
  modality:
    - image
  datasets:
    - MNIST
    - CIFAR-10
    - Stanford Dogs
  metrics:
    - test accuracy
evidence_level: full-paper
raw_sources:
  - raw/sources/2026-05-01-fedhaw-hypergradient-aggregation-weights.pdf
source_pages:
  - wiki/domains/federated-learning/concepts/federated-learning.md
---

# FedHAW: Federated Learning with Hypergradient-based Online Update of Aggregation Weights

## Citation

Nakai-Kasai & Wadayama, "Federated Learning with Hypergradient-based Online Update of Aggregation Weights," IEEE (letter), arXiv:2605.00458v1, May 2026.

## One-Sentence Contribution

将 hypergradient descent 从学习率优化迁移到 FL 聚合权重在线更新——FedHAW 无需额外训练数据和预训练步骤，在异质和通信错误场景下实现高泛化和高鲁棒性。

## Problem Setting

FedLAW 通过预准备数据在学习阶段学习聚合权重来应对异质性，但存在两个局限：(1) 需要额外训练数据预学习聚合权重，这些数据可能无法反映真实分布；(2) 额外开销显著，且环境（通信/设备）可能在训练期间变化。需要一种在线自适应更新聚合权重的方法。

## Method

FedHAW 核心：

1. **Hypergradient-based Online Update**：hypergradient 是目标函数关于聚合权重的梯度。FedHAW 在每轮 FL 训练中在线计算 hypergradient 并用于更新聚合权重。
2. **低计算开销**：hypergradient 计算开销低，无需额外训练数据。
3. **即插即用**：可与任何 FL 算法的客户端更新过程结合。

与 FedLAW 对比：
- FedLAW：需要预先准备 proxy 数据，离线学习最优聚合权重参数 (λ, τ)。
- FedHAW：在线 hypergradient 更新，零额外数据需求，实时适应环境变化。

## Experiments

**数据集**

- **MNIST**、**CIFAR-10**、**Dogs**（Stanford Dogs 细粒度分类数据集）。

**训练配置**

- 数据异质性设定：按标签分布进行 non-IID 分区。
- 通信错误设定：每轮每个客户端以概率 pₑ 随机丢失模型更新。测试 pₑ∈{0.2, 0.8}。

**Baselines**

FedAvg、FedHyper（学习率调度器）、FedLWS（逐层权重收缩）、FedLAW（离线学习聚合权重——需 proxy 数据集）。

## Results

**通信错误下的测试准确率 (Table IV)**

| Dataset | pₑ | FedAvg | FedHyper | FedLWS | FedLAW | **FedHAW** |
|---------|-----|--------|----------|--------|--------|-----------|
| MNIST | 0.2 | 80.53 | 81.13 | 80.52 | 83.26 | **86.70** |
| MNIST | 0.8 | 73.41 | 75.17 | 73.39 | 78.98 | **83.72** |
| CIFAR-10 | 0.2 | 61.30 | 58.55 | 63.44 | 68.39 | 67.47 |
| CIFAR-10 | 0.8 | 62.39 | 60.40 | 64.46 | 67.12 | 63.07 |
| Dogs | 0.2 | 83.60 | 82.02 | 83.26 | 86.14 | **87.34** |
| Dogs | 0.8 | 82.33 | 83.84 | 81.58 | 85.80 | 85.21 |

- MNIST pₑ=0.2 下 FedHAW 86.70% vs. FedLAW 83.26%（+3.44%）；pₑ=0.8 下也保持领先（83.72% vs. 78.98%）。
- CIFAR-10 pₑ=0.2 下 FedHAW 67.47% 略低于 FedLAW 68.39%，但 FedHAW 无需 proxy 数据集。
- Dogs 上 FedHAW 在两种 pₑ 下均最优。

**与 FedProx 结合 (Table V)**

FedProx+HAW 在多数轮次超越单独 FedProx：

- MNIST t1：74.30 vs. FedProx 49.24；t5：83.69 vs. 81.36。
- CIFAR-10 t1：60.44 vs. 53.56。
- Dogs t1：81.58 vs. 66.96。

**per-round 精度动态 (Fig. 2)**

在 CIFAR-10 pₑ=0.8 下，FedHAW 的每轮精度始终高于 FedAvg/FedLWS/FedHyper，错误客户端数也维持在较低水平。FedLAW 精度接近但需要 proxy 数据集每轮辅助训练——实际部署中不可行。

**核心结论**

FedHAW 在通信错误和数据异质性场景下达到或超过 FedLAW 的性能水平，且无需任何额外数据或预训练步骤。hypergradient 更新可与任意客户端优化器（如 FedProx proximal term）组合，进一步提升精度。

## Limitations

- 实验规模未在摘要中详述（客户端数量、数据集）。
- 对 extreme heterogeneity（如完全 non-overlapping label spaces）的表现未知。

## Reusable Claims

- 声明：hypergradient 可以从 FL 训练过程本身提取聚合权重的优化信号，替代离线预学习。
  证据：FedHAW hypergradient 公式与实验结果。
  范围：FL 聚合权重优化。
  置信度：medium。

- 声明：在线聚合权重更新可以适应训练过程中通信环境的变化，而离线学习的权重可能过时。
  证据：通信错误仿真实验中的鲁棒性验证。
  范围：不稳定的 FL 通信环境。
  置信度：medium。

## Connections

- [FL Heterogeneity and Optimization](../topics/fl-heterogeneity-and-optimization.md)：本论文属于聚合层异质性优化的子方向——hypergradient 提供在线聚合权重更新的信号。
- [Federated Learning](../concepts/federated-learning.md)：FL 聚合权重的在线优化方法。
- [FedKPer](fedkper-generalization-personalization-medical-fl.md)：也解决 FL 中数据异质性问题，但 FedKPer 关注通过 selective alignment 实现 medical FL 的 generalization-personalization 平衡，FedHAW 关注通过在线超梯度更新聚合权重来应对环境变化。

## Open Questions

- Hypergradient 在大规模 FL（数千客户端）中的扩展性。
- 与其他 personalized FL 方法的可结合性（如先用 hypergradient 聚合，再做本地个性化）。
- Hypergradient 更新频率（每轮 vs. 每 N 轮）对性能和通信的影响。

## Provenance

- 摄入时间：2026-05-05。
- 原始来源：[raw/sources/2026-05-01-fedhaw-hypergradient-aggregation-weights.pdf](../../../raw/sources/2026-05-01-fedhaw-hypergradient-aggregation-weights.pdf)。
- 证据等级：full-paper（完整实验数据从 PDF 提取，包含 Table IV-V 定量结果和 FedProx 组合实验）。
