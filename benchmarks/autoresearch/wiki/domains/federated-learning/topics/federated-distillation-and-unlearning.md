---
title: Federated Distillation and Unlearning
type: topic
domain: federated-learning
status: active
created: 2026-05-05
updated: 2026-05-08
tags:
  - federated-learning
  - dataset-distillation
  - machine-unlearning
  - multimodal
  - anchor-principle
  - one-shot-fl
source_pages:
  - wiki/domains/federated-learning/papers/fedhd-federated-distillation-whole-slide-image.md
  - wiki/domains/federated-learning/papers/ease-federated-multimodal-unlearning.md
  - wiki/domains/federated-learning/papers/fedsd2c-one-shot-fl-distiller-distillate.md
  - wiki/domains/distillation/papers/correspondence-coverage-matters-multimodal-dataset-distillation.md
raw_sources:
  - raw/sources/2026-05-01-fedhd-federated-distillation-wsi.pdf
  - raw/sources/2026-05-01-ease-federated-multimodal-unlearning.pdf
  - raw/sources/2024-12-10-one-shot-fl-synthetic-distiller-distillate-communication.pdf
related_pages:
  - wiki/domains/distillation/concepts/dataset-distillation.md
  - wiki/domains/distillation/topics/multimodal-dataset-distillation.md
---

# Federated Distillation and Unlearning

## 当前论点

联邦数据集蒸馏（FedDD）和联邦遗忘（federated unlearning）是同一个问题的两面：**如何在分布式、隐私受限的条件下控制知识的保留与删除**。FedHD 展示了如何在特征级别蒸馏跨机构的诊断知识而不共享原始数据，EASE 则揭示了在多模态联邦学习中消除知识时面临的深层纠缠——三个残差锚（Modality Anchor、Unique-Subspace Anchor、Temporal Re-anchoring）持续重建被遗忘的配对。两者的共同线索是：**跨模态/跨客户端的语义耦合既是蒸馏效率的来源，也是遗忘的主要障碍**。

## 范围

- 将数据集蒸馏迁移到联邦设定（FedHD 为 WSI 场景的代表性工作）。
- 联邦遗忘——客户端或概念从多模态联邦模型中删除的方法和理论。
- Cross-modal coupling 在蒸馏（correspondence coverage）和遗忘（anchor channels）中的作用。
- 联邦蒸馏与集中式 DD（如 ProCo、长尾 DD）的架构和技术关系。
- Curriculum-based 联邦知识融合策略。
- 一次性联邦学习（One-shot FL）：通过合成蒸馏物（distillate）在单轮通信中完成联邦训练，规避迭代 FL 的通信和隐私风险。

## 关键线索

- FedHD 识别出现有 FedDD 在 WSI 场景的两类失败：mean-matching 无法捕捉多组分 patch feature 分布、过度压缩损失 slide 级诊断多样性。
- FedHD 的 Gaussian-mixture alignment（对每个组件的均值和协方差进行匹配）是解决多组分分布蒸馏的更一般方案——可能适用于任何 patch-based MIL 数据。
- EASE 的 Anchor Principle 揭示了一个深层结构：joint embedding training 中的 bilinear coupling 使遗忘知识的消除需要双边（图像+文本）参数位移——单边切除会因为未修改的分支作为 cross-modal anchor 将梯度拉回而失败。
- 联邦训练使客户端的梯度子空间沿连续谱纠缠，forget-exclusive 方向与 retain-support 方向混合——粗粒度的全部擦除策略注定有 forget–retain trade-off。
- Temporal Re-anchoring 意味着即使在遗忘时刻闭合了所有 anchor，每轮 FL 训练的 alignment gradient 会沿移除方向重写一部分 anchor——需要持续的 Forget Lock 机制。
- FedHD 的 curriculum federation（先真实数据收敛，再逐步引入合成数据）提供了一种受控的跨域知识注入方式——可能同样适用于缓解 EASE 中的跨客户端 distribution shift。
- FedSD2C 通过端到端 distillate 合成（V-information Core-Set + Fourier 扰动 + 预训练 VAE 蒸馏）替代 DFKD 的模型→数据逆向生成，消除了双层信息损失；在高分辨率复杂数据集（Tiny-ImageNet, ImageNette, OpenImage）上以 model-sharing 4% 以下的通信成本实现 2.6× 最佳 baseline 的性能。

## 原子 Claims

- 声明：联邦数据集蒸馏在 WSI 场景中需要多组分分布对齐（Gaussian-mixture alignment），而非均值匹配。
  证据：FedHD (ICML 2026)，TCGA-IDH、CAMELYON16、CAMELYON17 上 GM alignment 持续优于 mean-matching baselines。
  范围：基于 MIL 的 WSI 联邦学习。
  置信度：medium。
  张力：需要与其他 FedDD 框架（FedDM、FedDGM）在 WSI 场景的直接比较。

- 声明：联邦多模态遗忘必须同时闭合三个残差锚——Modality Anchor、Unique-Subspace Anchor 和 Temporal Re-anchoring——单方面消除任一个都会导致遗忘失败。
  证据：EASE 的 Anchor Principle 分析和三组件消融实验。
  范围：基于 CLIP-style contrastive learning 的 FML。
  置信度：medium。
  张力：对其他多模态架构（BLIP、LLaVA-style）的锚结构尚不清楚。

- 声明：Bilateral knowledge excision（图像+文本分支同时位移）是闭合 Modality Anchor 的必要条件——单分支切除会因 bilinear similarity 的交叉梯度而被逆转。
  证据：EASE 的 BKE 设计，单分支切除的 forget 端性能显著退化。
  范围：contrastive multimodal models。
  置信度：medium。

- 声明：Curriculum federation（先本地收敛再逐步引入外部合成数据）是一种通用的联邦知识融合策略，可同时适用于蒸馏和遗忘后恢复。
  证据：FedHD 的 curriculum strategy 验证了受控引入的优越性。
  范围：任何涉及跨客户端合成数据共享的联邦设定。
  置信度：low（仅在 FedHD 设定下验证，尚未在遗忘后恢复场景测试）。

- 声明：One-to-one 蒸馏（每 slide 一个 counterpart）在小规模、高 intra-class 多样性的数据集中优于传统最大压缩策略。
  证据：FedHD vs. 传统压缩 FedDD。
  范围：WSI / 小样本医学影像。
  置信度：medium。

- 声明：端到端合成蒸馏物通信——从原始数据直接蒸馏而非从模型逆向生成——在 one-shot FL 中可消除 DFKD 的双层信息损失，对抗数据异质性。
  证据：FedSD2C (NeurIPS 2024)，Tiny-ImageNet ResNet-18 上 2.6× Co-Boosting，OpenImage 上 1.5× DENSE。
  范围：视觉分类 one-shot FL，ConvNet + ResNet-18。
  置信度：high。
  张力：仅限视觉域验证；Fourier 扰动对低分辨率数据效果有限。

## 证据

- [FedHD: Federated Distillation for WSI](../papers/fedhd-federated-distillation-whole-slide-image.md)：ICML 2026，GM alignment + one-to-one distillation + curriculum federation，skimmed。
- [EASE: Federated Multimodal Unlearning](../papers/ease-federated-multimodal-unlearning.md)：arXiv 2026，Anchor Principle + BKE + GSD + PFL，skimmed。
- [Dataset Distillation](../../distillation/concepts/dataset-distillation.md)：集中式 DD 的上位概念。
- [Multi-Modal Dataset Distillation](../../distillation/topics/multimodal-dataset-distillation.md)：ProCo 的 correspondence coverage 与 EASE 的 modality anchor 互补视角。
- [FedSD2C](../papers/fedsd2c-one-shot-fl-distiller-distillate.md)：NeurIPS 2024，end-to-end distillate synthesis for one-shot FL，full-paper。

## 张力

- 蒸馏追求最大化信息保留，遗忘追求完全消除——两者在联邦设定中是否有共同的最优操作（如 subspace projection 作为双用途工具）？
- FedHD 的 curriculum federation 和 EASE 的 Forget Lock + projection 都涉及"受控的知识迁移/阻止"——两者的数学形式是否有深层对应？
- 当前证据均来自 skimmed 级别——FedHD 的 ablation（K 的选择、one-to-one vs. 压缩比、curriculum schedule）和 EASE 的完整消融（仅 BKE、仅 GSD、仅 PFL 的 forget–retain 表现）需要 full-paper 验证。

## 开放问题

- 联邦蒸馏和联邦遗忘是否可以统一为一个"知识生命周期管理"框架——蒸馏注入知识、遗忘删除知识、同一套 subspace/alignment 工具服务于两者？
- EASE 的 Anchor Principle 对 FedHD 式的联邦蒸馏是否有对偶意义——蒸馏是否因同样的 anchor 机制而在跨客户端间更有效（anchor 促进知识转移而非阻止删除）？
- Gaussian-mixture 的组件数量自动选择——能否从数据中学习 K 而非手工指定？
- 联邦遗忘的法律合规性——GDPR right to be forgotten 的具体要求与 EASE 达到的 forget-retain 误差 (0.2/4.2 R@1) 之间的差距。
