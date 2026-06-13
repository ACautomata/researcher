---
title: Second Brain
type: topic
domain: meta
status: active
created: 2026-04-20
updated: 2026-04-25
tags:
  - second-brain
  - knowledge-system
  - operating-model
source_pages:
  - wiki/domains/meta/sources/karpathy-llm-wiki.md
  - wiki/domains/distillation/papers/rethinking-long-tailed-dataset-distillation.md
  - wiki/domains/distillation/papers/correspondence-coverage-matters-multimodal-dataset-distillation.md
  - wiki/domains/distillation/papers/targeted-data-protection-diffusion-model-training-trajectory.md
  - wiki/domains/outofdistributiondetection/papers/out-of-distribution-detection-with-negative-prompts.md
  - wiki/domains/outofdistributiondetection/papers/learning-transferable-negative-prompts-ood-detection.md
  - wiki/domains/spectrum/papers/topological-machine-learning-nanocrystal-synthesis.md
raw_sources:
  - raw/sources/2026-04-20-karpathy-llm-wiki.md
  - raw/sources/2025-12-14-rethinking-long-tailed-dataset-distillation.pdf
  - raw/sources/2026-03-14-correspondence-coverage-matters-multimodal-dataset-distillation.md
  - raw/sources/2026-03-14-targeted-data-protection-diffusion-model-training-trajectory.md
  - raw/sources/2024-01-16-out-of-distribution-detection-with-negative-prompts.pdf
  - raw/sources/2024-05-31-learning-transferable-negative-prompts-ood-detection.pdf
  - raw/sources/2025-11-28-topological-machine-learning-nanocrystal-synthesis.pdf
---

# Second Brain

## 当前论点

这个仓库是用户长期、本地优先的科研论文 second brain。用户负责投喂论文和提出问题；LLM 负责维护结构、总结来源、更新交叉引用，并让知识库长期保持一致。

## 范围

- 追踪用户想记住或继续发展的重要来源。
- 把来源转化为持久 paper pages、concepts、topics、comparisons 和 analyses。
- 保留 provenance，让 claim 能追溯到 raw materials。
- 让 wiki 同时服务 active exploration 和 later retrieval。

## 关键线索

- 一次 ingest 一篇论文，并立即整合到现有知识结构中。
- 用 `wiki/index.md` 作为第一导航界面。
- 把 `wiki/log.md` 作为 wiki 演化的追加式记忆。
- 有复用价值的回答应提升为 wiki 内容。
- 当前研究覆盖从 [Long-Tailed Dataset Distillation](../../distillation/topics/long-tailed-dataset-distillation.md) 起步，并扩展到 [Multi-Modal Dataset Distillation](../../distillation/topics/multimodal-dataset-distillation.md)、[Diffusion Model Data Protection](../../distillation/topics/diffusion-model-data-protection.md)、[Negative Prompt OOD Detection](../../outofdistributiondetection/topics/negative-prompt-ood-detection.md) 和 [Spectrum-Based Reaction Pathway Discovery](../../spectrum/topics/spectrum-based-reaction-pathway-discovery.md)。
- 新论文按单一主标签组织：`distillation`、`outofdistributiondetection` 或 `spectrum`。
- `wiki/` 维护层默认中文呈现；raw sources 保持原始语言和不可变状态。

## 证据

- [LLM Wiki](../sources/karpathy-llm-wiki.md)：定义整体架构和运行循环。
- [Persistent LLM Wiki](../concepts/persistent-llm-wiki.md)：命名本仓库背后的核心概念。
- [Rethinking Long-tailed Dataset Distillation](../../distillation/papers/rethinking-long-tailed-dataset-distillation.md)：第一条外部研究论文线索。
- [Correspondence Coverage Matters for Multi-Modal Dataset Distillation](../../distillation/papers/correspondence-coverage-matters-multimodal-dataset-distillation.md)：扩展到多模态压缩和 correspondence coverage。
- [Targeted Data Protection for Diffusion Model by Matching Training Trajectory](../../distillation/papers/targeted-data-protection-diffusion-model-training-trajectory.md)：展示 trajectory-matching 思想用于 diffusion-model protection。
- [Dataset Distillation](../../distillation/concepts/dataset-distillation.md)：连接长尾、多模态和轨迹启发分支的 hub concept。
- [Out-of-Distribution Detection](../../outofdistributiondetection/concepts/out-of-distribution-detection.md)：以 OOD detection 为中心的第二个研究 domain。
- [Spectroscopic Manifold Learning](../../spectrum/concepts/spectroscopic-manifold-learning.md)：以 spectral data 为中心的第三个研究 domain。

## 开放问题

- 下一步应优先深入哪个方向：distillation、OOD detection，还是 spectrum？
- 哪些 method、dataset、task、metric 应优先拆成独立页面？
- 哪些查询输出应自动成为 analysis 或 comparison 页面？
