---
title: CIFAR-10 / CIFAR-10-LT / CIFAR10-S
type: dataset
domain: distillation
status: active
created: 2026-05-24
updated: 2026-05-24
tags:
  - image-classification
  - benchmark
  - long-tailed
  - fairness
source_pages:
  - wiki/domains/distillation/papers/rethinking-long-tailed-dataset-distillation.md
  - wiki/domains/distillation/papers/fair-dataset-distillation-cobra.md
  - wiki/domains/outofdistributiondetection/papers/out-of-distribution-detection-with-negative-prompts.md
related_pages:
  - wiki/domains/distillation/methods/rldd.md
  - wiki/domains/distillation/methods/cobra.md
  - wiki/domains/outofdistributiondetection/methods/lsn.md
---

# CIFAR-10

## 描述

CIFAR-10 是 10 类 32×32 彩色自然图像分类基准数据集，共 60,000 张图像（50,000 训练 / 10,000 测试）。在 wiki 中以三种变体出现：

- **CIFAR-10（标准平衡版）**：每类 5,000 训练 / 1,000 测试。
- **CIFAR-10-LT（长尾版）**：通过指数衰减采样策略构建（IF = $\mu^{-c/(C-1)}$），IF ∈ {5, 10, 20, 50, 100, 256}。RLDD 核心 benchmark。
- **CIFAR10-S（有偏版）**：引入灰度/彩色作为敏感属性（skew=0.90），COBRA 公平性 benchmark。训练集 50,000，测试集 group-balanced。

## 使用场景

- 数据集蒸馏（DD）：标准 benchmark，IPC ∈ {1, 10, 20, 50}。
- 长尾数据集蒸馏：RLDD 的 CIFAR-10-LT 变体。
- 公平数据集蒸馏：COBRA 的 CIFAR10-S 变体。
- OOD 检测：LSN 在小规模数据集部分使用。

## 划分与协议

| 变体 | 训练/测试 | 不平衡参数 | 论文 |
|------|----------|-----------|------|
| CIFAR-10 | 50K/10K (平衡) | — | LSN (小规模 OOD) |
| CIFAR-10-LT | 指数衰减采样 | IF=5~256 | RLDD |
| CIFAR10-S | 50K (skew=0.90) | 测试 group-balanced | COBRA |

## 已知问题

- CIFAR-10-LT 的指数衰减采样策略可能放大特定类别的随机噪声（tail class 样本极少时）。
- CIFAR10-S 的灰度/彩色敏感属性过于简化——真实偏差更复杂。
- 32×32 低分辨率限制了对高分辨率蒸馏方法的评估能力。

## 使用者

- **RLDD**：CIFAR-10-LT (IF=10, IPC=10) 上 63.6%（vs. DAMED 58.1%，+5.5%）。
- **COBRA**：CIFAR10-S (DM IPC=10) 上 EOD 20.18 vs. Vanilla 56.25；IPC=1 时 EOD 4.9 vs. 17.2。
- **LSN**：小规模 OOD 检测（CIFAR-10 作 ID，CIFAR+10/+50 作 OOD）。

## 关联

- [CIFAR-100](cifar-100.md)：100 类版本，更多类别、更复杂的长尾蒸馏 benchmark。
- [Tiny-ImageNet](tiny-imagenet.md)：更高分辨率（64×64）、200 类的蒸馏 benchmark。
- [RLDD](../methods/rldd.md)：CIFAR-10-LT 为核心 benchmark。
- [COBRA](../methods/cobra.md)：CIFAR10-S 为公平性 benchmark。

## 开放问题

- 更真实的 bias 注入方式（如 contextual bias、spurious correlation）能否更好地评估公平蒸馏？
- 更高分辨率变体对蒸馏方法 ranking 的影响？
