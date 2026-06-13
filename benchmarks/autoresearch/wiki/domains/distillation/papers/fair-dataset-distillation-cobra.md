---
title: Fair Dataset Distillation via Cross-Group Barycenter Alignment
type: paper
domain: distillation
status: active
created: 2026-05-05
updated: 2026-05-05
tags:
  - dataset-distillation
  - fairness
  - barycenter-alignment
  - group-imbalance
paper:
  title: Fair Dataset Distillation via Cross-Group Barycenter Alignment
  authors:
    - Mohammad Hossein Moslemi
    - Nima Hosseini Dashtbayaz
    - Zhimin Mei
    - Boyu Wang
    - Bissan Ghaddar
  year: 2026
  venue: ICML 2026 (submission)
  arxiv: "2605.00185"
  doi: ""
  code: ""
  project: ""
classification:
  label: distillation
  task:
    - dataset distillation
    - fair representation learning
  method_family:
    - distribution matching
    - barycenter alignment
    - trajectory matching
  modality:
    - image
  datasets:
    - CIFAR10-S
    - Colored-MNIST
    - Colored-FashionMNIST
    - UTKFace
    - BFFHQ
  metrics:
    - equalized odds difference
    - accuracy
evidence_level: full-paper
raw_sources:
  - raw/sources/2026-05-04-fair-dataset-distillation-cobra.pdf
related_pages:
  - wiki/domains/distillation/concepts/dataset-distillation.md
  - wiki/domains/distillation/papers/rethinking-long-tailed-dataset-distillation.md
  - wiki/domains/distillation/papers/correspondence-coverage-matters-multimodal-dataset-distillation.md
  - wiki/domains/distillation/methods/cobra.md
  - wiki/domains/distillation/comparisons/cobra-vs-rldd.md
---

## Citation

Moslemi, M. H., Dashtbayaz, N. H., Mei, Z., Wang, B., & Ghaddar, B. (2026). Fair Dataset Distillation via Cross-Group Barycenter Alignment. *arXiv preprint arXiv:2605.00185*. ICML 2026 submission.

## One-Sentence Contribution

提出 COBRA（Cross-grOup BaRycenter Alignment），通过计算群体不平衡无关的表示重心（barycenter）并将蒸馏目标对齐到该重心，从根本上解决数据集蒸馏中的子群体公平性偏差放大问题——兼容 DC、DM、CAFE、IDC 及 MTT 等所有主流蒸馏方法。

## Problem Setting

数据集蒸馏（DD）将大规模训练集压缩为小型合成数据集，但蒸馏过程会放大原始数据中的子群体偏差（subgroup bias）。现有观点认为这种偏差源自群体不平衡（多数群体样本主导聚合表示）或子群体表示差异，但本文证明偏差放大**源于二者的交互作用**，单一维度解释不充分。

蒸馏过程中的聚合目标（如 class-conditional mean embedding 或 mean gradient）被多数群体主导，导致合成数据主要捕获多数群体模式，少数群体信息被系统性丢失。仅仅做 uniform sampling 或 reweighting 无法完全解决，因为不同群体的表示空间几何结构差异（representational separation）依然会导致某些群体被系统性地偏离。

形式化：令 $\Phi_{a|y}$ 为群体 $a$ 在类别 $y$ 上的表示统计量，传统蒸馏目标 $m_y^{van} = \sum_a \pi_{a|y} \Phi_{a|y}$ 被群体比例 $\pi_{a|y}$ 主导。当群体表示存在几何分离时，残差 $\Delta_{a|y} = \Phi_{a|y} - m_y^{van}$ 在少数群体上显著更大，导致 Equalized Odds Difference (EOD) 恶化。

## Method

**COBRA 框架**：

1. **跨群体重心计算**：对于每个类别 $y$，计算 uniform-weight barycenter（重心）$m_y^* \in \arg\min_m \frac{1}{|A|}\sum_{a \in A} d(\Phi_{a|y}, m)$，其中 $d$ 为选定的差异度量（默认 squared Mahalanobis distance）。该重心与群体大小无关，在表示空间中与各子群体保持相似距离。

2. **重心对齐蒸馏**：将合成数据优化目标从匹配群体比例加权的聚合表示 $m_y^{van}$ 切换为匹配群体无关重心 $m_y^*$。对于 squared Q-norm，$m_y^* = \frac{1}{|A|}\sum_{a \in A} \Phi_{a|y}$，即各子群体统计量的均匀均值。

3. **理论保证**：推导了偏差放大的上界，证明该上界由群体不平衡与表示分离的交互项控制；COBRA 通过缩小最差情况子群体残差来收紧该上界（Theorem 4.1）。

4. **兼容性**：可与 DC（gradient matching）、DM（distribution matching）、CAFE（feature alignment）、IDC（informativeness-based）以及 MTT（trajectory matching）无缝集成。在 MTT 中，COBRA 修改 trajectory target 为 group-balanced barycentric trajectory target。

5. **差异度量选择**：默认使用 squared Q-norm（闭式解为均匀均值），也可选用 $\ell_1$、$\ell_2$、$\ell_\infty$、cosine、Huber，以 L-BFGS 优化。

## Experiments

**数据集**（7 个有偏基准，所有测试集 group-balanced）：

| 数据集 | 类别数 | 敏感属性 | 训练集 | SKEW | IPC=10 压缩比 |
|--------|--------|----------|--------|------|--------------|
| C-MNIST (FG) | 10 | 前景颜色 | 60,000 | 0.90 | 0.17% |
| C-MNIST (BG) | 10 | 背景颜色 | 60,000 | 0.90 | 0.17% |
| C-FMNIST (FG) | 10 | 物体颜色 | 60,000 | 0.90 | 0.17% |
| C-FMNIST (BG) | 10 | 背景颜色 | 60,000 | 0.90 | 0.17% |
| CIFAR10-S | 10 | 灰度/彩色 | 50,000 | 0.90 | 0.20% |
| UTKFace | 3 (年龄) | 种族 | 20,813 | 0.53/0.35/0.63 | 0.14% |
| BFFHQ | 2 (年龄) | 性别 | 19,200 | 0.995/0.995 | 0.10% |

**Baseline 方法**：Vanilla DD、FairDD（NeurIPS 2025）、RF (Fair Extractor)、DF (Loss Reweighting)、MF (Fair Downstream)

**蒸馏框架**：DC (gradient matching)、DM (distribution matching)、CAFE、IDC，IPC ∈ {10, 50, 100}

**训练设置**：
- 蒸馏模型：ConvNet（3 层卷积，128 通道）
- 评估模型：ConvNet、AlexNet、VGG11、ResNet18（跨架构泛化测试）
- 指标：Accuracy (Acc ↑)、Equalized Odds Difference (EOD ↓)、EODM (max)、EODA (mean)
- 每组实验 10 次独立运行，报告 mean ± std

**Ablation**：
- 重心差异度量：$\ell_1$、$\ell_2$、$\ell_\infty$、cosine、Huber
- 最差残差上界验证
- 低 IPC 鲁棒性（IPC ∈ {1, 3, 5}）
- 群体标签噪声（0% ~ 50%）
- 部分群体标签可用（5% ~ 75%）
- MTT 轨迹蒸馏兼容性
- 标准公平干预对比（RF/DF/MF）
- 语义保持表示分离隔离实验

## Results

**公平性核心结果**（Table 1, DM framework, IPC=10, EOD ↓, 同时报 Acc）：

| 数据集 | Vanilla DM (EOD/Acc) | FairDD (EOD/Acc) | COBRA (EOD/Acc) | EOD 降幅 |
|--------|---------------------|-------------------|-----------------|---------|
| CIFAR10-S | 56.25/37.2 | 25.63/44.9 | **20.18/44.5** | -36.07 |
| C-MNIST (FG) | 100.00/26.2 | 7.26/94.0 | **6.71/94.1** | -93.29 |
| C-MNIST (BG) | 100.00/20.3 | 7.51/94.7 | **7.04/94.5** | -92.96 |
| C-FMNIST (FG) | 99.20/33.9 | 17.25/76.6 | **15.93/77.1** | -83.27 |
| C-FMNIST (BG) | 99.50/22.1 | 24.05/70.9 | **21.48/70.6** | -78.02 |
| UTKFace | 35.53/55.9 | 22.78/67.5 | **20.78/70.7** | -14.75 |
| BFFHQ | 44.80/65.1 | 14.10/66.0 | **15.73/69.5** | -29.07 |

**跨架构泛化**（Table 3）：COBRA 在 AlexNet、VGG11、ResNet18 上均保持最低 EOD + 最高或接近最高 Acc。

**MTT 兼容性**（Table 17, IPC=10）：
- BFFHQ：EOD 32.96% → 9.12%（-23.84%），但 Acc 61.64 → 51.86%（-9.78）
- CIFAR10-S：EOD 39.40% → 30.38%（-9.02%），Acc 26.36 → 36.32%（+9.96）

**群体标签噪声鲁棒性**（Table 15, DM IPC=10）：
- C-MNIST (BG)：50% 噪声下 EOD 仅从 12.99 升至 17.92，远低于 Vanilla 的 100.0
- CIFAR10-S：50% 噪声下 EOD 37.03 vs. Vanilla 56.25
- BFFHQ：50% 噪声下 EOD 38.48 vs. Vanilla 44.80

**部分标签可用**（Table 16）：仅 5% 群体标签时，C-MNIST (FG) EOD 54.68 vs. Vanilla 100.0；CIFAR10-S EOD 52.93 vs. 56.25。

**计算开销**（Table 14）：
- 两组设置（BFFHQ/CIFAR10-S）：DC 1.39-1.59× 延迟，1.20-1.36× 内存；DM 1.30-1.59× 延迟，~1× 内存
- 十组设置（C-MNIST/C-FMNIST）：DC 3.74-4.29× 延迟，1.19× 内存；DM 3.02-3.21× 延迟，<1× 内存

**Ablation 关键发现**：
- 重心差异度量选择影响非均匀（Table 4）：无单一最佳度量，但 COBRA (squared Q-norm) 综合最稳健
- 最差残差上界验证（Table 5）：COBRA 在所有设置中实现最低最差类残差，确认理论
- 低 IPC 鲁棒（Table 10）：IPC=1 的 CIFAR10-S 上 EOD 4.9 vs. Vanilla 17.2；BFFHQ IPC=3 上 EOD 7.8 vs. Vanilla 30.4
- 标准公平干预对比（Table 18）：COBRA 在 6 组中的 4 组取得最低 EOD，其余 2 组仍保持 competitive + 更高 Acc

## Limitations

1. 依赖群体标签——尽管对标签噪声和部分缺失有鲁棒性，完全无标签场景无法使用
2. BFFHQ 的 DF (Loss Reweighting) 在 DM 下 EOD 略低于 COBRA（14.10 vs. 15.73），表明在特定数据集上直接 reweighting 可能更有效
3. MTT 集成在 BFFHQ 上以显著精度下降换取公平性提升，trade-off 需要根据应用场景评估
4. 十组极端合成设置下 DC 运行时 4.29× 减速；但在实际场景（两组）仅 1.3-1.6×
5. 仅在视觉分类 bias（颜色/纹理/人口统计关联）上验证，对其他模态（文本/表格/图）的泛化性未知

## Reusable Claims

- Claim: 数据集蒸馏中的偏差放大来自群体不平衡与子群体表示分离的**交互作用**，而非任一单一因素。
  Evidence: [Fair Dataset Distillation via COBRA](fair-dataset-distillation-cobra.md), Section 5.2 + Fig 2.
  Scope: 有偏视觉分类数据集（CIFAR10-S, Colored-MNIST）。
  Confidence: high.

- Claim: 蒸馏目标从群体比例加权聚合切换到 uniform-weight 重心（barycenter）可以有效降低 EOD，同时不损害甚至提升准确率。
  Evidence: [Fair Dataset Distillation via COBRA](fair-dataset-distillation-cobra.md), Table 1—7 个数据集上全面验证。
  Scope: DC/DM/CAFE/IDC/MTT 五类蒸馏框架，7 个有偏视觉数据集。
  Confidence: high.

- Claim: 仅靠蒸馏前（fair extractor）或蒸馏后（fair downstream）公平干预不足以消除偏差放大，蒸馏聚合目标本身必须公平化。
  Evidence: [Fair Dataset Distillation via COBRA](fair-dataset-distillation-cobra.md), Table 18—RF 和 MF 与 COBRA 的系统对比。
  Scope: DC/DM on CIFAR10-S, C-MNIST (BG), BFFHQ。
  Confidence: high.

- Claim: squared Q-norm barycenter 有闭式解（均匀均值），计算高效；替代差异度量选择是 dataset-specific hyperparameter。
  Evidence: [Fair Dataset Distillation via COBRA](fair-dataset-distillation-cobra.md), Table 4 + Proposition C.1.
  Scope: 视觉数据集蒸馏的 representation matching 目标。
  Confidence: medium.

## Connections

- [Dataset Distillation](../concepts/dataset-distillation.md)：COBRA 为数据集蒸馏增加公平性维度
- [Rethinking Long-tailed Dataset Distillation](rethinking-long-tailed-dataset-distillation.md)：长尾蒸馏处理的是类别不平衡，COBRA 处理的是子群体偏差——二者是互补的公平性维度
- FairDD (NeurIPS 2025)：最直接的 baseline，COBRA 在几乎所有设置中超越 FairDD
- [Targeted Data Protection for Diffusion Model](targeted-data-protection-diffusion-model-training-trajectory.md)：COBRA-MTT 作为 MTT 兼容变体，与 trajectory matching 家族连接

## Open Questions

1. 对非视觉模态（文本/表格/图/GNN）的泛化性？
2. 如何与 generative/diffusion-based 数据集蒸馏方法（如 DiM、DDPM）结合？
3. 当 sensitive attribute 未知或为连续变量时，如何在不依赖群体标签的情况下实现类似 barycenter alignment？
4. Multiple intersecting sensitive attributes（如 race × gender）的扩展？
5. 联邦数据集蒸馏场景下的公平性——各客户端群体分布不同的情形？
6. 更大规模数据集（ImageNet-1K）上的可扩展性验证？

## Provenance

- 从 PDF `raw/sources/2026-05-04-fair-dataset-distillation-cobra.pdf`（arXiv 2605.00185v1，27 页）全文中提取。
- 全文阅读，包括主实验（Table 1）、ablation（Table 4-5、Table 15-16）、跨架构泛化（Table 3）、MTT 扩展（Table 17）、标准公平干预对比（Table 18）、语义保持隔离实验（Table 19）、计算开销（Table 13-14）、附录理论证明（Proposition C.1、Theorem C.2）。
