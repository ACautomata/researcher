---
title: MNIST / Colored-MNIST / MNIST-M
type: dataset
domain: federated-learning
status: active
created: 2026-05-24
updated: 2026-05-24
tags:
  - image-classification
  - fairness
  - continual-learning
  - benchmark
source_pages:
  - wiki/domains/distillation/papers/fair-dataset-distillation-cobra.md
  - wiki/domains/distillation/papers/continual-distillation-teachers-different-domains.md
related_pages:
  - wiki/domains/distillation/methods/cobra.md
  - wiki/domains/distillation/methods/se2d.md
---

# MNIST

## 描述

MNIST 是 28×28 灰度手写数字分类基准数据集（10 类，60,000 训练 / 10,000 测试）。在 wiki 中以多个变体出现：

- **MNIST（标准版）**：CD 的 Digits benchmark 中的共享领域数据（所有教师已知）。
- **Colored-MNIST (FG/BG)**：注入颜色偏差——前景颜色 (FG) 或背景颜色 (BG) 与类别标签强相关（skew=0.90），COBRA 公平性 benchmark。
- **MNIST-M**：MNIST 数字与彩色背景 patches 混合，CD 的 Digits benchmark 中作为教师特定领域。
- **USPS、SVHN、KMNIST**：Digits benchmark 中的其他数字识别数据集（SVHN 为街景门牌号，USPS 为邮政手写数字，KMNIST 为日本 Kuzushiji 字符）。

## 使用场景

- 公平数据集蒸馏：Colored-MNIST (FG/BG) 是 COBRA 评估 bias 放大最极端的 benchmark（skew=0.90，群体表示高度分离）。
- 持续蒸馏：Digits benchmark（MNIST/MNIST-M/USPS/SVHN + KMNIST 作 ED）验证 SE2D 的跨域 UKT/UKF trade-off。

## 划分与协议

| 变体 | 训练/测试 | 敏感属性 | 论文 |
|------|----------|---------|------|
| MNIST | 60K/10K (平衡) | — | CD (Digits) |
| C-MNIST (FG) | 60K (skew=0.90) | 前景颜色 | COBRA |
| C-MNIST (BG) | 60K (skew=0.90) | 背景颜色 | COBRA |
| MNIST-M | 60K | — | CD (Digits) |

## 已知问题

- Colored-MNIST 的颜色偏差过于人工——真实世界的 bias 更复杂且多因素交织。
- MNIST 分辨率极低（28×28）——对需要高分辨率特征的方法代表性有限。
- Digits benchmark 中 MNIST-M/SVHN/USPS/KMNIST 的域间差异大于真实跨域场景，可能高估方法的跨域迁移能力。

## 使用者

- **COBRA**：C-MNIST (FG) DM IPC=10 上 EOD 6.71 vs. Vanilla 100.0（-93.29%）；C-MNIST (BG) EOD 7.04 vs. 100.0（-92.96%）。
- **CD/SE2D**：Digits benchmark 验证外部数据（KMNIST）的 UKT 效果和不同蒸馏方法的 UKF 程度。MNIST-M 上 DKD 从 54.50% 跌至 33.84%（严重 UKF）。

## 关联

- [COBRA](../methods/cobra.md)：Colored-MNIST 为核心 fairness benchmark——颜色偏差 + 群体表示高度分离构成最极端测试。
- [SE2D](../methods/se2d.md)：Digits benchmark 验证 CD 范式的 UKT-UKF trade-off。
- [CIFAR-10](../datasets/cifar-10.md)：类似 10 类分类任务但分辨率更高、场景更自然。

## 开放问题

- 更自然的 bias 注入方式（如 contextual bias + multiple attributes）对公平蒸馏评估的改进？
- Digits benchmark 是否应该引入更多中间难度域（介于完全相关和完全无关之间）来细粒度评估 UKT？
