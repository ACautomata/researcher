---
title: Tiny-ImageNet / Tiny-ImageNet-LT
type: dataset
domain: distillation
status: active
created: 2026-05-24
updated: 2026-05-24
tags:
  - image-classification
  - benchmark
  - long-tailed
  - one-shot-fl
source_pages:
  - wiki/domains/distillation/papers/rethinking-long-tailed-dataset-distillation.md
  - wiki/domains/federated-learning/papers/fedsd2c-one-shot-fl-distiller-distillate.md
  - wiki/domains/outofdistributiondetection/papers/learning-transferable-negative-prompts-ood-detection.md
related_pages:
  - wiki/domains/distillation/methods/rldd.md
  - wiki/domains/federated-learning/methods/fedsd2c.md
  - wiki/domains/distillation/datasets/cifar-100.md
---

# Tiny-ImageNet

## 描述

Tiny-ImageNet 是 ImageNet 的子集，200 类、64×64 彩色自然图像，训练集 100,000 张（每类 500），测试集 10,000 张（每类 50）。在 wiki 中以两种变体出现：

- **Tiny-ImageNet（标准版）**：FedSD2C 一次性联邦学习 benchmark（10,000 训练样本 subset）。
- **Tiny-ImageNet-LT（长尾版）**：指数衰减采样构建（IF ∈ {5, 10, 20, 50, 100}），RLDD 长尾蒸馏 benchmark（更难的长尾场景——类别数是 CIFAR-100 的 2 倍）。

## 使用场景

- 长尾数据集蒸馏：RLDD 的 Tiny-ImageNet-LT 变体——类别数更多（200）、长尾更极端。
- 一次性联邦学习：FedSD2C 的核心 benchmark，$\alpha \in \{0.1, 0.3, 0.5\}$（Dirichlet 异质性）。
- OOD 检测：NegPrompt 在 TinyImageNet（resized）上作为小规模 OOD benchmark。

## 划分与协议

| 变体 | 类别数 | 分辨率 | 训练/测试 | 论文 |
|------|--------|--------|----------|------|
| Tiny-ImageNet | 200 | 64×64 | 100K/10K | FedSD2C, NegPrompt |
| Tiny-ImageNet-LT | 200 | 64×64 | 指数衰减采样 | RLDD (IF=5~100) |

## 已知问题

- 64×64 分辨率仍低于实际应用图像——对蒸馏方法的 scaling 评估有限。
- Tiny-ImageNet-LT 在极高 IF（100+）下某些 tail class 可能只有 1-2 张图像——统计量极不稳定。
- FedSD2C 使用 subset（10,000 训练样本），与标准 Tiny-ImageNet 训练集不完全一致。

## 使用者

- **RLDD**：Tiny-ImageNet-LT (IF=10, IPC=10) 上 37.8%（vs. DAMED 26.0%，+11.8%）；IPC=1 (IF=100) 上 20.1%（vs. DAMED 6.0%，+14.1%）。
- **FedSD2C**：ResNet-18 ($\alpha=0.1$) 上 26.83%（vs. Co-Boosting 10.29%，2.61×）；通信压缩至 2.1MB（ipc=50）。
- **NegPrompt**：小规模 OOD detection（ID 类数量较少时的补充评估）。

## 关联

- [CIFAR-100](cifar-100.md)：100 类，64×64 以下——Tiny-ImageNet 类别数更多、挑战更大。
- [RLDD](../methods/rldd.md)：Tiny-ImageNet-LT 为核心 benchmark（与 CIFAR-100-LT 互补——更多类别 vs. 更高分辨率）。
- [FedSD2C](../../federated-learning/methods/fedsd2c.md)：Tiny-ImageNet 为核心 benchmark。

## 开放问题

- Tiny-ImageNet-LT 在更高分辨率变体（如 128×128）上的长尾蒸馏表现？
- FedSD2C 的通信效率在完整 100K 训练集（而非 10K subset）上的表现？
