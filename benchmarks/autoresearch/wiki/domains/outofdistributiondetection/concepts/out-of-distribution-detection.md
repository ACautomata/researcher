---
title: Out-of-Distribution Detection
type: concept
domain: outofdistributiondetection
status: active
created: 2026-04-25
updated: 2026-05-05
tags:
  - out-of-distribution-detection
  - open-world-recognition
  - prompt-learning
source_pages:
  - wiki/domains/outofdistributiondetection/papers/out-of-distribution-detection-with-negative-prompts.md
  - wiki/domains/outofdistributiondetection/papers/learning-transferable-negative-prompts-ood-detection.md
raw_sources:
  - raw/sources/2024-01-16-out-of-distribution-detection-with-negative-prompts.pdf
  - raw/sources/2024-05-31-learning-transferable-negative-prompts-ood-detection.pdf
---

# Out-of-Distribution Detection

## 定义

Out-of-distribution (OOD) detection 是识别输入是否不属于训练分布或预期部署分布的问题。在开放世界视觉识别中，目标是在保持 ID 分类能力的同时标记陌生或异常样本。

## 当前理解

- CLIP 风格 vision-language models (VLMs) 让 prompt design 成为 OOD detection 的强大工具。
- Positive prompts 描述已知类别特征，但 OOD 样本可能与已知类别共享部分特征，仅靠 positive similarity 难以区分。
- Negative prompts 引入显式 dissimilarity signal：建模给定类别 "不是什么"，用此信号划定 ID/OOD 边界。
- 当前两篇 full-paper 论文代表两个互补的 negative-prompt 设计方向：
  - **LSN (ICLR 2024)**：class-specific negative prompts（每类 K=3 个）+ semantic orthogonality loss，覆盖类特定 negative features。
  - **NegPrompt (CVPR 2024)**：shared transferable negative templates（每类 2 个）+ 三个损失函数（NIS/NPD/NND），支持 open-vocabulary transfer。
- Positive 和 negative prompt learning 存在根本性差异——positive 靠 class name 携带语义，negative 靠 learned prompts 自身。
- 两个方法都通过 ID-only 训练实现有效 OOD 检测：LSN 将 ImageNet-100 FPR95 从 32.58→8.56%，NegPrompt 将 ImageNet-1K FPR95 从 51.68→23.01%。

## 证据

- [Out-of-Distribution Detection with Negative Prompts (LSN)](../papers/out-of-distribution-detection-with-negative-prompts.md)：full-paper，class-specific negative prompts，ICLR 2024。
- [Learning Transferable Negative Prompts for Out-of-Distribution Detection (NegPrompt)](../papers/learning-transferable-negative-prompts-ood-detection.md)：full-paper，transferable negative prompts，CVPR 2024。

## 连接

- [Negative Prompt OOD Detection](../topics/negative-prompt-ood-detection.md)：本 wiki 中 prompt-based OOD 方法的主题页。
- [Inbox Paper Topic Classification](../../meta/analyses/inbox-paper-topic-classification-2026-04-25.md)：当前 inbox pass 的分类记录。

## 开放问题

- Negative prompts 什么时候优于 energy-based、gradient-based 或 distance-based OOD scores？
- Learned negative prompts 在 domain shift、label expansion 和 open-vocabulary inference 下是否稳定？
- Negative prompts 检测的是真正 distribution shift、semantic novelty，还是主要检测 class-boundary ambiguity？
- 能否将 class-specific（LSN）和 transferable（NegPrompt）negative prompts 的优势整合进单一框架？
