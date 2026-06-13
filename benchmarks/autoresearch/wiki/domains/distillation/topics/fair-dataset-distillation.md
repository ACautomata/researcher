---
title: Fair Dataset Distillation
type: topic
domain: distillation
status: active
created: 2026-05-05
updated: 2026-05-05
tags:
  - fairness
  - dataset-distillation
  - subgroup-bias
  - barycenter-alignment
source_pages:
  - wiki/domains/distillation/papers/fair-dataset-distillation-cobra.md
related_pages:
  - wiki/domains/distillation/concepts/dataset-distillation.md
  - wiki/domains/distillation/papers/rethinking-long-tailed-dataset-distillation.md
---

# Fair Dataset Distillation

## Current Thesis

数据集蒸馏中的公平性问题不能简单地通过纠正群体不平衡（uniform sampling/reweighting）来解决——偏差放大源于**群体不平衡与子群体表示分离的交互作用**。有效的公平干预必须在蒸馏聚合目标层面修改，将群体比例加权的聚合替换为群体无关的重心（barycenter）对齐，使合成数据与各子群体保持相似距离。COBRA 是当前唯一从理论和实验上系统证明这一点的框架。

## Scope

- 数据集蒸馏中的子群体公平性（demographic/subgroup fairness），以 Equalized Odds Difference (EOD) 为主要指标
- 覆盖有偏视觉分类场景：spurious correlation（C-MNIST/C-FMNIST 颜色关联）、人口统计偏差（UTKFace 种族、BFFHQ 性别）
- 蒸馏方法族覆盖：DC (gradient matching)、DM (distribution matching)、CAFE (feature alignment)、IDC、MTT (trajectory matching)
- 公平干预位置：蒸馏前（fair extractor）、蒸馏中（COBRA/reweighting）、蒸馏后（fair downstream）

## Key Threads

1. **偏差放大的根本原因**：群体不平衡 × 表示分离的交互 → 合成数据系统性偏向多数群体 → EOD 恶化
2. **公平干预位置**：蒸馏前（RF）和蒸馏后（MF）均不足以充分消除偏差——蒸馏目标本身必须公平化
3. **重心对齐**：uniform-weight barycenter 作为与群体大小无关的聚合目标，在表示空间中对各子群体等距
4. **方法无关性**：COBRA 仅修改蒸馏的 target 构建，不改变优化循环，因此可兼容所有现有蒸馏方法
5. **对标签质量的鲁棒性**：对群体标签噪声（up to 50%）和部分标签可用（低至 5%）具有一定鲁棒性

## Atomic Claims

- Claim: 数据集蒸馏在群体不平衡和表示分离同时存在时，会放大原始数据中的子群体偏差。
  Evidence: [COBRA](../papers/fair-dataset-distillation-cobra.md), Fig 2 + Table 1—Vanilla DM EOD 显著高于 FULL baseline。
  Scope: 7 个有偏视觉分类数据集，DC/DM/CAFE/IDC 四种蒸馏方法。
  Confidence: high.
  Tensions: 无已知矛盾证据。

- Claim: uniform-weight barycenter alignment 可同时降低 EOD 并维持或提升准确率。
  Evidence: [COBRA](../papers/fair-dataset-distillation-cobra.md), Table 1—7 数据集上 EOD 全面下降，Acc 同步提升。
  Scope: DC/DM/CAFE/IDC on 视觉分类。
  Confidence: high.
  Tensions: MTT 集成在 BFFHQ 上以显著 Acc 下降换取 EOD 改善（Table 17）；且 BFFHQ DM 下 Loss Reweighting (DF) EOD 14.10 略低于 COBRA 15.73。

- Claim: 重心差异度量选择是 dataset-specific hyperparameter，无单一最佳选择。
  Evidence: [COBRA](../papers/fair-dataset-distillation-cobra.md), Table 4—不同数据集的最佳 d 不同。
  Scope: ℓ₁、ℓ₂、ℓ∞、cosine、Huber、squared Q-norm on 7 个数据集。
  Confidence: medium.

## Evidence

- COBRA 在 CIFAR10-S DM IPC=10 上 EOD 从 56.25% 降至 20.18%，Acc 同步提升 7.3%（37.2 → 44.5%）。来源：[COBRA](../papers/fair-dataset-distillation-cobra.md), Table 1。
- 仅靠 RF (Fair Extractor) 或 MF (Fair Downstream) 不能替代 COBRA——RF 在 C-MNIST (BG) DM 下 EOD 仍为 100.0%，MF 同样 100.0%。来源：[COBRA](../papers/fair-dataset-distillation-cobra.md), Table 18。
- COBRA-MTT 在 BFFHQ IPC=10 上 EOD 32.96% → 9.12%，但 Acc 61.64 → 51.86%。来源：[COBRA](../papers/fair-dataset-distillation-cobra.md), Table 17。
- 语义保持隔离实验：FULL baseline Acc 恒定 ~72%/EOD ~51% 不受 GAP 影响，而 Vanilla DD EOD 随 GAP 增大升至 68.2%，COBRA 仅为 29.33%。来源：[COBRA](../papers/fair-dataset-distillation-cobra.md), Table 19。

## Tensions

- COBRA 在 BFFHQ DM IPC=10 上 EOD 15.73 vs. Loss Reweighting (DF) 14.10——DF 在公平性上略优，但 COBRA Acc 更高（69.5 vs. 66.0）
- MTT 集成 BFFHQ 上 Acc 显著下降（-9.78%），带来最大 EOD 改善（-23.84%）——存在 fairness-accuracy trade-off
- COBRA 依赖群体标签，虽然对噪声有一定鲁棒性，但完全无标签场景不可用

## Open Questions

1. 对非视觉模态（文本/表格/图）的泛化性？
2. 多个相交敏感属性（race × gender）的扩展？
3. 联邦数据集蒸馏中的公平性——各客户端群体分布不同的情形？
4. 与 generative/diffusion-based 蒸馏方法（DiM、DDPM）的结合？
5. 如何在公平蒸馏中形式化地量化 fairness-accuracy-efficiency 三元 trade-off？
6. 当群体标签完全不可用时，是否能从数据分布中无监督地推断出需要公平化的群体结构？
