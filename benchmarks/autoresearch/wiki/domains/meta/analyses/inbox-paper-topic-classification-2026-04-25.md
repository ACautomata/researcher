---
title: Inbox Paper Topic Classification 2026-04-25
type: analysis
domain: meta
status: stable
created: 2026-04-25
updated: 2026-04-25
tags:
  - paper-classification
  - wiki-organization
source_pages:
  - wiki/domains/distillation/papers/rethinking-long-tailed-dataset-distillation.md
  - wiki/domains/distillation/papers/correspondence-coverage-matters-multimodal-dataset-distillation.md
  - wiki/domains/distillation/papers/targeted-data-protection-diffusion-model-training-trajectory.md
  - wiki/domains/outofdistributiondetection/papers/out-of-distribution-detection-with-negative-prompts.md
  - wiki/domains/outofdistributiondetection/papers/learning-transferable-negative-prompts-ood-detection.md
  - wiki/domains/spectrum/papers/topological-machine-learning-nanocrystal-synthesis.md
raw_sources:
  - raw/sources/2025-12-14-rethinking-long-tailed-dataset-distillation.pdf
  - raw/sources/2026-03-14-correspondence-coverage-matters-multimodal-dataset-distillation.md
  - raw/sources/2026-03-14-targeted-data-protection-diffusion-model-training-trajectory.md
  - raw/sources/2024-01-16-out-of-distribution-detection-with-negative-prompts.pdf
  - raw/sources/2024-05-31-learning-transferable-negative-prompts-ood-detection.pdf
  - raw/sources/2025-11-28-topological-machine-learning-nanocrystal-synthesis.pdf
---

# Inbox Paper Topic Classification 2026-04-25

## 问题

把 `raw/inbox/` 中现有论文分别归入一个且仅一个 wiki 组织类别：`distillation`、`outofdistributiondetection` 或 `spectrum`。

## 发现

| Inbox paper | 分类 | 置信度 | 理由 |
| --- | --- | --- | --- |
| `2024_CVPR_Learning Transferable Negative Prompts for Out-of-Distribution Detection.pdf` | `outofdistributiondetection` | 高 | 标题和摘要明确把贡献定义为使用 transferable negative prompts 的 OOD detection 方法。 |
| `2024_ICLR_Out-Of-Distribution Detection With Negative Prompts.pdf` | `outofdistributiondetection` | 高 | 官方 ICLR 摘要描述了 learned positive and negative prompts 用于 OOD detection。 |
| `aaai2026rethinking.pdf` | `distillation` | 高 | 已作为 long-tailed dataset distillation 摄入。 |
| `Correspondence Coverage Matters for Multi-Modal Dataset Distillation Proceedings of the AAAI Conference on Artificial Intelligence.md` | `distillation` | 高 | 摘要明确讨论 multi-modal dataset distillation。 |
| `Lee et al. - 2025 - Topological Machine Learning Unveils Hidden Reaction Pathways in Nanocrystal Synthesis.pdf` | `spectrum` | 中高 | 论文主要数据是 UV-vis spectra，并从高维光谱数据中抽取 reaction pathways。 |
| `Targeted Data Protection for Diffusion Model by Matching Training Trajectory Proceedings of the AAAI Conference on Artificial Intelligence.md` | `distillation` | 中高 | 应用是 data protection，但在受限分类体系里，核心组织线索是受 dataset distillation 启发的 trajectory matching。 |

## 证据

- 现有 distillation paper pages 覆盖三个 `distillation` 条目。
- 两篇 negative-prompt 论文的标题和摘要都以 OOD detection 为中心。
- nanocrystal synthesis 论文归入 `spectrum`，因为 spectroscopy 是中心数据层，尽管算法方法是 topological manifold learning。

## 含义

- `wiki/domains/distillation/` 用于 dataset distillation 和 trajectory-matching-adjacent papers。
- `wiki/domains/outofdistributiondetection/` 用于 prompt-based 和其他 OOD detection papers。
- `wiki/domains/spectrum/` 用于 spectra 或 spectral measurements 是核心证据层的论文。

## 后续

- 加入更多 OOD baseline，明确 negative-prompt methods 在方法谱系中的位置。
- 加入更多 spectrum-domain papers，再考虑把 spectroscopy、frequency-domain analysis 和 spectral graph methods 拆成独立概念。
