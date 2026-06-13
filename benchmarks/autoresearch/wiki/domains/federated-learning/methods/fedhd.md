---
title: FedHD — Federated Distillation for WSI
type: method
domain: federated-learning
status: active
created: 2026-05-24
updated: 2026-05-24
tags:
  - federated-learning
  - dataset-distillation
  - whole-slide-image
  - gaussian-mixture
  - curriculum-learning
source_pages:
  - wiki/domains/federated-learning/papers/fedhd-federated-distillation-whole-slide-image.md
related_pages:
  - wiki/domains/federated-learning/concepts/federated-learning.md
  - wiki/domains/federated-learning/topics/federated-distillation-and-unlearning.md
  - wiki/domains/distillation/concepts/dataset-distillation.md
---

# FedHD — 面向全切片图像的联邦数据集蒸馏

## 定义

FedHD 是首个面向全切片图像（WSI）的联邦数据集蒸馏框架，通过高斯混合特征对齐替代均值匹配以捕捉 WSI 的多组分形态学分布，onetone 蒸馏策略保留诊断多样性，课程联邦策略逐步融合跨机构合成特征。

## 核心机制

1. **Gaussian-Mixture Feature Alignment (GMA)**：将 WSI 的 patch feature space 建模为高斯混合（M=16 组件），对真实和合成数据在对齐均值和每个组件的协方差，同时捕捉 intra-slide heterogeneity。均值匹配因 WSI patch feature 的多组分性质而失效。
2. **One-to-One Feature Distillation (O2O)**：为每张真实 slide 生成一个合成 counterpart（而非压缩多张 slide 为几个样本），直接在 patch embedding 上操作（与 MIL pipeline 天然对齐），保留 slide 级诊断多样性。
3. **Curriculum Federation Strategy (CBF)**：阶段 1——各客户端用真实数据优化 MIL 模型至稳定收敛；阶段 2——逐步引入其他客户端的合成数据作为辅助监督，缓解 domain shift 并增强泛化。
4. **Optional Interpretation Module**：从合成 embedding 重建 pseudo-patches，增强透明度。

## 假设

- WSI patch features 服从多组分分布（而非单峰分布），需要多组分对齐。
- 在小规模 WSI 数据集中，保留 slide 级诊断多样性比最大压缩更重要。
- 课程式引入跨机构合成数据可以缓解 domain shift。
- 联邦场景中客户端使用异构特征提取器和异构 MIL 架构。

## 证据

- ICML 2026, Jing et al., arXiv:2605.00578v1，full-paper。
- 异构设定：ResNet50 + UNI + PhikonV2 + GPFM（4 特征提取器），CLAM + TransMIL + ACMIL（3 MIL 模型），每个客户端随机选取一对。
- CAMELYON16：Avg Acc 91.2% / MCC 80.6（FedWSIDD 88.7%/75.3，+2.5% Acc +5.3 MCC）。
- CAMELYON17：Avg Acc 82.7% / MCC 62.3（FedWSIDD 77.2%/52.0，+5.5% Acc +10.3 MCC）。
- TCGA-IDH：Avg Acc 84.8% / MCC 57.0（FedWSIDD 80.5%/47.0，+4.3% Acc +10.0 MCC）。
- Ablation：FDD +6.2%, GMA +9.9%, O2O +9.0%, CBF +8.8% 的独立贡献。
- 隐私：LiRA MIA AUC 全面低于 FedWSIDD（TCGA-IDH: 54.7 vs. 60.1）。
- 通信效率：特征级蒸馏 39 MB/轮（O2O ~1.19 GB），训练 1 小时 vs. 图像级 10-12 小时。

## 变体

- **FedHD w/o GMA**：均值匹配替代高斯混合对齐。
- **FedHD w/o O2O**：最大压缩策略替代 onetone 蒸馏。
- **FedHD w/o CBF**：直接融合合成数据替代课程联邦。

## 优势与局限

**优势**：
- 首个面向 WSI 的联邦数据集蒸馏框架，填补了病理图像 FL + DD 交叉空白。
- 高斯混合对齐通用性强——可处理异构特征提取器和 MIL 架构。
- 课程联邦策略有效缓解跨机构 domain shift。
- 特征级蒸馏带来显著通信和训练效率提升（特征 vs. 图像级：1 小时 vs. 10-12 小时）。
- 隐私保护优于 SOTA（MIA AUC 更低）。

**局限**：
- Gaussian-mixture 组件数 K 需预定义（对未知数据分布超参数敏感）。
- O2O 蒸馏使合成集大小随 slide 数线性增长。
- 跨机构合成数据的可解释性受限于 embedding-to-patch 重建的保真度。
- 仅验证 3 个 WSI 数据集（CAMELYON16/17、TCGA-IDH），泛化性待扩展。

## 关联

- [Federated Learning](../concepts/federated-learning.md)：上位概念。
- [Federated Distillation and Unlearning](../topics/federated-distillation-and-unlearning.md)：主题页，与 EASE 统一分析蒸馏和遗忘。
- [Dataset Distillation](../../distillation/concepts/dataset-distillation.md)：FedHD 是 DD 在联邦 WSI 设定中的扩展。
- [ProCo](../../distillation/methods/proco.md)：GM alignment 与 ProCo 的 correspondence coverage 共享"分布级匹配优于均值匹配"哲学。
- [CoRD](../../llm-reasoning/methods/cord.md)：共享"受控增量整合"——FedHD 用 curriculum federation 逐步融合，CoRD 用 step-wise decoding 逐步构建。

## 开放问题

- Gaussian-mixture component count 的自动选择方法？
- 与其他 FedDD 方法（FedDM、FedDGM）在 WSI 场景的直接比较？
- 跨癌种（TCGA pan-cancer）的泛化性？
