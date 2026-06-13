---
title: CIFAR-100 / CIFAR-100-LT
type: dataset
domain: distillation
status: active
created: 2026-05-24
updated: 2026-05-24
tags:
  - image-classification
  - benchmark
  - long-tailed
  - ood-detection
source_pages:
  - wiki/domains/distillation/papers/rethinking-long-tailed-dataset-distillation.md
  - wiki/domains/outofdistributiondetection/papers/out-of-distribution-detection-with-negative-prompts.md
related_pages:
  - wiki/domains/distillation/methods/rldd.md
  - wiki/domains/distillation/datasets/cifar-10.md
  - wiki/domains/distillation/datasets/tiny-imagenet.md
---

# CIFAR-100

## 描述

CIFAR-100 是 100 类 32×32 彩色自然图像分类基准数据集，共 60,000 张图像（50,000 训练 / 10,000 测试），每类 500 训练 / 100 测试。此外包含 20 个超类（superclass），每个超类含 5 个细类。在 wiki 中以两种形式出现：

- **CIFAR-100（标准版）**：OOD 检测（LSN 小规模 benchmark）。
- **CIFAR-100-LT（长尾版）**：指数衰减采样（IF ∈ {5, 10, 20, 50, 100}），RLDD 核心 benchmark——类别数是 CIFAR-10 的 10 倍，长尾蒸馏挑战更大。

## 使用场景

- 长尾数据集蒸馏：RLDD 的核心 benchmark——验证在 100 类长尾设置下 statistical alignment 的 scaling 能力。
- OOD 检测：LSN 在小规模数据集（CIFAR-10/100）上的补充评估。

## 划分与协议

| 变体 | 类别数 | 训练/测试 | 不平衡参数 | 论文 |
|------|--------|----------|-----------|------|
| CIFAR-100 | 100 (20 超类) | 50K/10K | — | LSN |
| CIFAR-100-LT | 100 | 指数衰减采样 | IF=5~100 | RLDD |

RLDD 消融实验在 CIFAR-100-LT (IF=50) 上进行：三组件贡献 Stat Align -10% / BN Recalib -2% / Multi-Round Init -1%。

## 已知问题

- 32×32 低分辨率——对需要高分辨率特征的方法不友好。
- 20 超类的层次结构在长尾蒸馏中未被利用——超类信息可能辅助 tail class 的语义恢复。
- 指数衰减采样可能导致部分 tail class 在极端 IF 下样本数为 0（rounding 问题）。

## 使用者

- **RLDD**：CIFAR-100-LT (IF=10, IPC=10) 上 47.1%（vs. DAMED 31.5%，+15.6%）；IPC=1 (IF=50) 上 31.8%（vs. DAMED 7.8%，+24.0%）。
- **LSN**：小规模 OOD detection（作为 ID 数据集或 OOD 数据集的补充）。

## 关联

- [CIFAR-10](cifar-10.md)：10 类版本——更简单的 benchmark，适合方法初始验证。
- [Tiny-ImageNet](tiny-imagenet.md)：200 类、64×64——更高类别数 + 更高分辨率的 scaling 验证。
- [RLDD](../methods/rldd.md)：CIFAR-100-LT 为核心 benchmark + ablation 平台。

## 开放问题

- CIFAR-100 的 20 超类层次结构能否在长尾蒸馏中被利用（如 hierarchical statistical alignment）？
- 更高分辨率 CIFAR-100 变体对蒸馏方法 ranking 的影响？
