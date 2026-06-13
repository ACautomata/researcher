---
title: "EASE: Federated Multimodal Unlearning via Entanglement-Aware Anchor Closure"
type: paper
domain: federated-learning
status: active
created: 2026-05-05
updated: 2026-05-05
tags:
  - federated-learning
  - machine-unlearning
  - multimodal
  - contrastive-learning
  - anchor-principle
  - lora
paper:
  title: "EASE: Federated Multimodal Unlearning via Entanglement-Aware Anchor Closure"
  authors:
    - Zihao Ding
    - Beining Wu
    - Jun Huang
  year: 2026
  venue: arXiv (preprint)
  arxiv: "2605.00733v1"
  doi: ""
  code: ""
  project: ""
classification:
  label: federated-learning
  task:
    - federated unlearning
  method_family:
    - subspace excision
    - multimodal contrastive unlearning
    - LoRA
  modality:
    - image-text pairs
  datasets:
    - Flickr30K
    - MS-COCO
  metrics:
    - R@1 (retrieval)
    - forget-retain trade-off
evidence_level: skimmed
raw_sources:
  - raw/sources/2026-05-01-ease-federated-multimodal-unlearning.pdf
source_pages:
  - wiki/domains/federated-learning/concepts/federated-learning.md
  - wiki/domains/distillation/concepts/dataset-distillation.md
---

# EASE: Federated Multimodal Unlearning via Entanglement-Aware Anchor Closure

## Citation

Ding et al., "EASE: Federated Multimodal Unlearning via Entanglement-Aware Anchor Closure," arXiv:2605.00733v1, May 2026.

## One-Sentence Contribution

识别联邦多模态对比学习遗忘中的 **Anchor Principle**（三个纠缠残留通道——Modality Anchor、Unique-Subspace Anchor、Temporal Re-anchoring），提出 EASE 框架在每个通道上系统闭合：Bilateral Knowledge Excision 切断跨模态重建，Gradient Subspace Decomposition 分离 forget-exclusive 方向，Projection with Forget Lock 防止联邦训练轮次间的漂移。

## Problem Setting

联邦多模态学习（FML）通过 LoRA adapter 在 frozen multimodal backbone (CLIP) 上联合训练。当某个客户端需要被遗忘（right to be forgotten）时，存在三个失败模式（anchors）：

1. **Modality Anchor**：联合嵌入训练的 bilinear coupling 纠缠了遗忘知识到两个模态——仅切除一个模态的参数，另一个模态作为交叉锚点将梯度拉回原始配对。
2. **Unique-Subspace Anchor**：联邦训练使客户端梯度子空间沿连续谱纠缠，forget-exclusive 方向与 retain-support 方向混合——现有方法将遗忘集贡献视为不可分块，导致 forget–retain trade-off。
3. **Temporal Re-anchoring**：即使遗忘时闭合前两个 anchor，每轮联邦训练中的 SGD 对齐梯度会在移除的方向上重写一部分已消除的 anchor。

## Method

EASE 三组件对三个 anchor：

1. **Bilateral Knowledge Excision (BKE)**：同时位移图像和文本分支，使 bilinear similarity 无法通过未触及的模态重建移除的配对——双边原则在单模态遗忘中没有对应物。
2. **Gradient Subspace Decomposition (GSD)**：复用 FedAvg 已传输的客户端更新，服务器通过 SVD 提取 per-client 子空间基，用成对 principal angles 量化子空间纠缠——几乎与 retain 子空间正交的方向视为 forget-exclusive anchor，与 retained clients 共享的方向保留为 retain support。
3. **Projection with Forget Lock (PFL)**：
   - 服务器端：每轮遗忘时将参数位移投影到 unique subspace 的补空间。
   - 客户端端：Forget Lock 惩罚沿已识别 unique 方向的漂移，drift 被 bound 在正则化强度的倒数。

## Experiments

- 数据集：Flickr30K、MS-COCO（CLIP-B/32 backbone）。
- 场景：client unlearning（移除某个客户端的所有 image-text pairs）。

## Results

- EASE 在 client unlearning 上达到 forget side 和 retain side 分别与 retrain reference 误差在 0.2 和 4.2 R@1 点之内。
- 一致优越于多个数据集和遗忘场景。
- 证明三个 anchor 的消除是联邦多模态遗忘的必要充分条件。

## Limitations

- 使用 frozen CLIP backbone + LoRA，对 fully fine-tuned multimodal models 未验证。
- 假设客户端间有足够的子空间重叠以识别 unique/exclusive 方向。
- Forget Lock 的超参数 (regularization strength) 对性能敏感。

## Reusable Claims

- 声明：联邦多模态遗忘需要双边（图像 + 文本）参数位移——单边切除不可行，因为 bilinear coupling 将未修改分支作为交叉通道重建遗忘配对。
  证据：EASE 的 BKE 双边设计 + Anchor Principle 分析。
  范围：FML with contrastive objectives (CLIP-style)。
  置信度：medium。

- 声明：客户端梯度子空间的 principal angle 分解可以区分 forget-exclusive 和 retain-shared 更新方向，是替换粗粒度 erase 操作的更细粒度控制手段。
  证据：GSD 通过 SVD + principal angles 识别 unique subspace。
  范围：多客户端 FL unlearning。
  置信度：medium。

## Connections

- [Federated Distillation and Unlearning](../topics/federated-distillation-and-unlearning.md)：本论文与 FedHD 的统一分析——Anchor Principle 揭示了跨模态 coupling 如何使遗忘变得困难，与蒸馏的 correspondence preservation 形成对偶。
- [Federated Learning](../concepts/federated-learning.md)：联邦多模态遗忘子方向。
- 与 `distillation` 域的 [Multi-Modal Dataset Distillation](../../distillation/topics/multimodal-dataset-distillation.md) 共享跨模态技术栈：跨模态 reconstruction channel 的闭合与控制是两者的共同议题（distillation 中的 correspondence coverage，unlearning 中的 modality anchor closure）。
- [FedHD](fedhd-federated-distillation-whole-slide-image.md)：同属 FL + 多模态/WSI 方向，FedHD 关注 distillation，EASE 关注 unlearning。

## Open Questions

- Anchor Principle 对其他 multimodal architectures（BLIP、LLaVA）的普适性。
- 多个客户端同时请求遗忘时的顺序效应和累积误差。
- 与 DP-based 遗忘（coupled approach）的互补性。

## Provenance

- 摄入时间：2026-05-05。
- 原始来源：[raw/sources/2026-05-01-ease-federated-multimodal-unlearning.pdf](../../../raw/sources/2026-05-01-ease-federated-multimodal-unlearning.pdf)。
- 证据等级：skimmed（基于摘要和首 5 页全文）。
