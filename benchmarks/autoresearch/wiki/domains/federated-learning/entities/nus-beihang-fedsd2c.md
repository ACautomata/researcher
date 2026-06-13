---
title: NUS & Beihang — FedSD2C 团队
type: entity
domain: federated-learning
status: active
created: 2026-05-24
updated: 2026-05-24
tags:
  - research-group
  - federated-learning
  - dataset-distillation
  - one-shot-fl
source_pages:
  - wiki/domains/federated-learning/papers/fedsd2c-one-shot-fl-distiller-distillate.md
related_pages:
  - wiki/domains/federated-learning/methods/fedsd2c.md
  - wiki/domains/federated-learning/topics/federated-distillation-and-unlearning.md
---

# NUS & Beihang — FedSD2C 团队

## 描述

新加坡国立大学（NUS）与北京航空航天大学（Beihang University）的联合研究团队，由 Xinchao Wang 主导。在 wiki 中因 FedSD2C（一次性联邦学习 via 合成蒸馏物通信）论文出现。

## 当前理解

- **团队组成**：Junyuan Zhang, Songhua Liu, Xinchao Wang（通讯作者）。
- **所属机构**：National University of Singapore (NUS) & Beihang University（北京航空航天大学）。
- **代码仓库**：github.com/Carkham/FedSD2C。
- **研究兴趣**：一次性联邦学习、数据集蒸馏、隐私保护机器学习、通信高效 FL。
- **发表**：NeurIPS 2024。

## 证据

- FedSD2C (NeurIPS 2024)：提出 V-information Core-Set 选择 + Fourier 扰动 + 预训练 Autoencoder 蒸馏的端到端一次性联邦学习框架。
- 在 Tiny-ImageNet ResNet-18 ($\alpha=0.1$) 上 2.61× Co-Boosting（26.83% vs. 10.29%）。
- 通信压缩：ipc=50 时 ImageNette 0.5MB（模型传输 44MB 的 1.1%）。
- 与 DENSE (NeurIPS 2022) 和 Co-Boosting (2024) 同一系列——NUS 团队在 one-shot FL 方向持续产出。

## 关联

- [FedSD2C](../methods/fedsd2c.md)：该团队在 wiki 中的核心方法贡献。
- [Federated Distillation and Unlearning](../topics/federated-distillation-and-unlearning.md)：所属研究领域。
- DENSE (NeurIPS 2022)、Co-Boosting (2024)：同系列相关工作，构成 one-shot FL 的技术演进线。
- 与 distillation 域的 RLDD 共享 Core-Set 选择 + statistical alignment 思想。

## 开放问题

- 团队在超大规模 cross-device FL（n>1000）上的后续扩展工作？
- 与 NUS 的 Xinchao Wang 组内其他数据集蒸馏工作的关系（如 DENSE 和 Co-Boosting 的后续演进）？
- 差分隐私形式化保证的集成进展？
