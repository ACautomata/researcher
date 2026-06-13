---
title: "FedACT: Concurrent Federated Intelligence across Heterogeneous Data Sources"
type: paper
domain: federated-learning
status: active
created: 2026-05-05
updated: 2026-05-05-evidence-upgrade
tags:
  - federated-learning
  - multi-job-scheduling
  - resource-heterogeneity
  - concurrent-training
paper:
  title: "FedACT: Concurrent Federated Intelligence across Heterogeneous Data Sources"
  authors:
    - Md Sirajul Islam
    - Isabelle G Chapman
    - N I Md Ashafuddula
    - Xu Yuan
    - Li Chen
    - Nian-Feng Tzeng
    - Klara Nahrstedt
  year: 2026
  venue: IPDPS 2026
  arxiv: "2605.00011v1"
  doi: ""
  code: ""
  project: ""
classification:
  label: federated-learning
  task:
    - multi-job FL scheduling
  method_family:
    - device scheduling
    - resource-aware optimization
  modality:
    - image
  datasets:
    - CIFAR-10
    - MNIST
    - EMNIST-Letters
    - EMNIST-Digits
    - FashionMNIST
  metrics:
    - job completion time
    - accuracy
evidence_level: full-paper
raw_sources:
  - raw/sources/2026-03-11-fedact-concurrent-federated-intelligence.pdf
source_pages:
  - wiki/domains/federated-learning/concepts/federated-learning.md
---

# FedACT: Concurrent Federated Intelligence across Heterogeneous Data Sources

## Citation

Islam et al., "FedACT: Concurrent Federated Intelligence across Heterogeneous Data Sources," 40th IEEE International Parallel & Distributed Processing Symposium (IPDPS), 2026. arXiv:2605.00011v1.

## One-Sentence Contribution

提出资源感知多作业 FL 调度——通过 alignment scoring 量化设备-作业匹配度，结合 participation fairness 约束，同时训练多个 FL 模型时平均作业完成时间（JCT）减少 8.3×、准确率提升高达 44.5%。

## Problem Setting

真实 FL 部署中，多个模型（如语言模型和图像推荐模型）需同时在同一设备池上训练。朴素串行训练导致资源浪费。现有 multi-job FL 方法（MJFL、FedAST）忽略了设备在不同模型上的性能差异，无法实现最优的 device-job matching。

## Method

FedACT 核心机制：

1. **Alignment Scoring**：对每个 device-job 对，量化设备可用资源与作业资源需求之间的兼容性。大语言模型需要更多算力/内存的设备，小图像分类器可在低配置设备上运行。
2. **Participation Fairness**：调整 alignment score 以防止资源偏好设备的过度代表和数据偏置——被频繁选中的设备降低 score，未充分代表的设备提升 score。
3. **Dynamic Scheduling**：每轮动态更新 alignment scores，生成优先选择高对齐度设备的调度计划，在训练效率和全局模型精度间取得最优平衡。

## Experiments

**任务、数据集与模型 (Table II)**

Group A（IID 和 non-IID）：
| Job | 模型 | 参数 | 数据集（训练/测试） | 本地 epochs | Batch |
|-----|------|------|-------------------|-----------|-------|
| Job 1 | LeNet-5 | 62K | EMNIST-Digits (240K/40K) | 5 | 64 |
| Job 2 | CNN-A | 3,785K | EMNIST-Letters (124.8K/20.8K) | 5 | 10 |
| Job 3 | VGG-16 | 26,233K | CIFAR-10 (50K/10K) | 5 | 30 |

Group B（IID 和 non-IID）：
| Job | 模型 | 参数 | 数据集（训练/测试） | 本地 epochs | Batch |
|-----|------|------|-------------------|-----------|-------|
| Job 1 | AlexNet | 3,275K | MNIST (60K/10K) | 5 | 64 |
| Job 2 | CNN-B | 225K | Fashion-MNIST (60K/10K) | 5 | 10 |
| Job 3 | ResNet-18 | 598K | CIFAR-10 (50K/10K) | 5 | 30 |

复杂度排序：LeNet < CNN-A < VGG；AlexNet < CNN-B < ResNet-18。

**Non-IID 构造**

IID：从完整训练集随机分配图像到设备。Non-IID：按类别排序后分 20 子集，每个设备随机选 2 类各取 1 子集。

**部署设定**

- 100 个设备，每轮每 job 选 10% 设备参与。
- SGD 优化器，4 张 NVIDIA RTX A4000 GPU + Intel i9-10900X CPU + 64GB RAM。

**Baselines (4 个)**

Random（随机选择设备）、Greedy（最大化资源对齐 + 参与惩罚）、Genetic（启发式初始化 + 进化策略）、MJ-FL（Bayesian Optimization 设备分配）。

**评估指标**

wall-clock 训练时间（到达目标精度或完成预设轮次）、平均作业完成时间 (JCT)。

## Results

**Group A 收敛精度 (Table III)**

| Method | LeNet | CNN | VGG |
|--------|-------|-----|-----|
| Random | 0.9924 | 0.942 | 0.611 |
| Greedy | 0.990 | 0.926 | 0.52 |
| Genetic | 0.9931 | 0.928 | 0.557 |
| MJ-FL | 0.9937 | 0.935 | 0.602 |
| **FedACT** | **0.9943** | **0.942** | **0.605** |

**Group A IID 到达目标精度时间 (Table III, 单位: min)**

| Method | LeNet (0.99) | CNN (0.93) | VGG (0.55) |
|--------|-------------|-----------|-----------|
| Random | 15.13 | 58.41 | 134.3 |
| Greedy | 17.25 | 30.17 | / (失败) |
| Genetic | 6.42 | 109.68 | 229.7 |
| MJFL | 5.18 | 19.18 | 59.10 |
| **FedACT** | **3.92** | **11.52** | **43.25** |

**Group A Non-IID 时间 (Table III)**

| Method | LeNet (0.984) | CNN (0.80) | VGG (0.55) |
|--------|-------------|-----------|-----------|
| Random | 42.56 | 43.61 | 2471.4 |
| Greedy | 42.73 | 97.33 | / |
| Genetic | 31.28 | 28.08 | 1168.5 |
| MJFL | 21.87 | 20.73 | 464.7 |
| **FedACT** | **15.02** | **14.82** | **286.4** |

**Group B 收敛精度 (Table IV)**

| Method | AlexNet | CNN | ResNet |
|--------|---------|-----|--------|
| Random | 0.9937 | 0.868 | 0.786 |
| Greedy | 0.9834 | 0.868 | 0.742 |
| Genetic | 0.9938 | 0.867 | 0.753 |
| MJ-FL | 0.9939 | 0.868 | 0.784 |
| **FedACT** | **0.9942** | **0.871** | **0.796** |

**Group B IID 到达目标精度时间 (Table IV)**

| Method | AlexNet (0.9933) | CNN (0.867) | ResNet (0.74) |
|--------|-------------------|-------------|---------------|
| Random | 37.02 | 123.10 | 64.66 |
| Greedy | / (失败) | 20.28 | 21.90 |
| Genetic | 36.88 | 21.90 | 31.35 |
| MJFL | 52.68 | 40.08 | 16.65 |
| **FedACT** | **13.58** | **21.08** | **11.42** |

**Group B Non-IID 时间 (Table IV)**

| Method | AlexNet (0.976) | CNN (0.73) | ResNet (0.50) |
|--------|-----------------|-----------|--------------|
| Random | 141.50 | 46.82 | 851.7 |
| Greedy | 179.9 | / | / |
| Genetic | 60.72 | 59.62 | 623.5 |
| MJFL | 71.38 | 16.51 | 218.4 |
| **FedACT** | **48.37** | **12.83** | **166.8** |

**单作业基线 (Table V)**

相同模型在单作业 FedAvg 下的训练时间：VGG IID 140.7 min / Non-IID 2488.3 min（FedACT 下仅需 43.25/286.4 min）；ResNet Non-IID 896.7 min（FedACT 仅需 166.8 min）。

**核心总结**

- FedACT 在所有 6 个 job（3 模型 × 2 数据分布）的收敛精度持续最高。
- 平均 JCT 相比最佳 baseline 减少 **8.3×**（Group B AlexNet IID: 13.58 min vs. MJFL 52.68 min）。
- 个别 job 的准确率提升高达 **+44.5%**（较最弱 baseline）。
- Non-IID 下优势更显著：VGG Non-IID 仅需 286.4 min vs. Random 2471.4 min（**-8.6×**）。

## Limitations

- 实验限于图像分类，对 NLP/多模态 multi-job FL 的泛化性未验证。
- alignment scoring 需要预知各设备的部分资源信息（现实场景中可能无法完全获取）。
- fairness module 的权重平衡（效率 vs. 公平）需手动调节。

## Reusable Claims

- 声明：multi-job FL 中设备与作业的匹配度是比硬件通用排名更好的调度信号。
  证据：FedACT 的 alignment score 在多组实验中稳定优于 data-size-based 调度。
  范围：heterogeneous multi-job FL。
  置信度：medium。

- 声明：participation fairness 在 multi-job FL 中不仅是 fairness 需求，也是提高模型准确率的有效手段（避免数据代表性偏差）。
  证据：公平模块使 underrepresented 设备贡献更多种类数据，提升模型准确率 44.5%。
  范围：multi-job FL。
  置信度：medium。

## Connections

- [FL Heterogeneity and Optimization](../topics/fl-heterogeneity-and-optimization.md)：本论文属于系统层异质性优化——multi-job scheduling 中的 device-job matching 和 participation fairness。
- [Federated Learning](../concepts/federated-learning.md)：multi-job FL 的基础。
- 与 PALCAS 的 FedRL 思路不同——FedACT 关注"如何调度多个 FL 作业"，PALCAS 关注"如何在单个 MARL 任务中隐私协作"。

## Open Questions

- Alignment scoring 对不同类型异构（计算 vs. 数据 vs. 通信）的通用性。
- 当作业数量和设备数量持续增长时，调度算法的扩展性。
- Fairness-efficiency trade-off 的自动化调节方法。

## Provenance

- 摄入时间：2026-05-05。
- 原始来源：[raw/sources/2026-03-11-fedact-concurrent-federated-intelligence.pdf](../../../raw/sources/2026-03-11-fedact-concurrent-federated-intelligence.pdf)。
- 证据等级：full-paper（完整实验数据从 PDF 提取，包含 Tables II-V 全部定量结果和 IID/non-IID 比较）。
