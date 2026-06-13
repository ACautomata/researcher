---
title: Negative Prompt OOD Detection
type: topic
domain: outofdistributiondetection
status: active
created: 2026-04-25
updated: 2026-05-05
tags:
  - out-of-distribution-detection
  - negative-prompts
  - clip
  - prompt-learning
source_pages:
  - wiki/domains/outofdistributiondetection/papers/out-of-distribution-detection-with-negative-prompts.md
  - wiki/domains/outofdistributiondetection/papers/learning-transferable-negative-prompts-ood-detection.md
raw_sources:
  - raw/sources/2024-01-16-out-of-distribution-detection-with-negative-prompts.pdf
  - raw/sources/2024-05-31-learning-transferable-negative-prompts-ood-detection.pdf
---

# Negative Prompt OOD Detection

## 当前论点

CLIP-style OOD detection 中引入 learned negative prompts 是超越仅用 positive similarity 的关键方向。两个代表性分支——LSN（class-specific, ICLR 2024）和 NegPrompt（transferable, CVPR 2024）——以互补设计验证了同一核心命题：handwritten negative prompts 不够用，learned negative prompts 能显著提升 OOD 检测，且 positive 和 negative prompt learning 存在根本性差异。

## 范围

- 基于 CLIP/VLM 的 OOD 检测。
- Positive + negative prompt 的联合学习范式。
- Negative prompt 的 class-specific vs. transferable 设计空间。
- 从 ID-only 数据出发的 OOD 检测（无需 outlier data）。
- Open-vocabulary OOD detection。

## 关键线索

- Handwritten negative prompts（"not a photo of a [class]"）对 OOD 检测高度欠指定——negative features 太多样，无法用单一字符串覆盖。
- Positive 和 negative prompt learning 存在根本差异：positive 由 class name 携带语义（可跨类共享一个 prompt），negative 必须由 learned prompts 自身表达（必须 class-specific 或学 generic negative templates）。
- LSN 为每个 ID 类学习 K=3 个独立 negative prompts + semantic orthogonality loss 确保多样性；NegPrompt 学习可跨类迁移的 shared negative templates（实验每类 2 个）。
- 两阶段训练（先 freeze positive 后学 negative）是两个方法共同的稳定性要求——一阶段联合训练会严重破坏 positive prompts。
- 两个方法都用 ID-only 训练：LSN 通过 complementary label 思路（除真实标签外均为 negative），NegPrompt 通过均匀分布假设（将 ID 图像概率均匀分配在所有 negative prompts 上）。
- 在 ImageNet-100/1K 上：LSN 将 MCM baseline FPR95 从 32.58→8.56%（ImageNet-100），从 43.55→30.22%（ImageNet-1K）。
- NegPrompt 将 CoOp baseline FPR95 从 51.68→23.01%（ImageNet-1K），且 open-vocabulary（10% ID 训练）仅下降 ~1.5% AUC。

## 原子 Claims

- 声明：Handwritten negative prompts 对 OOD 检测无效，因为无法覆盖多样且类别相关的 negative features。
  证据：LSN 实验明确在手写 negation 上验证并得出此结论；NegPrompt 的 motivation 也基于同一观察。
  范围：CLIP-style OOD detection。
  置信度：high（两个独立团队得出相同结论）。

- 声明：Positive prompt learning 中跨类共享 prompt 足够，negative prompt learning 必须 class-specific 或学 generic transferable templates。
  证据：LSN Table 5——negative class-shared 使 FPR95 从 21.94 飙至 81.27（几乎失效）；positive class-shared 几乎无影响。
  范围：CLIP prompt learning for OOD detection。
  置信度：high。

- 声明：两阶段训练（先 positive 后 negative）是 negative prompt learning 的稳定性必要条件。
  证据：NegPrompt Table 5——一阶段训练 FPR95 90.07%（vs. 两阶段 25.86%）。
  范围：prompt-learning OOD detection with positive + negative prompts。
  置信度：high。

- 声明：Negative prompts 可实现 open-vocabulary transfer——仅用部分 ID 类训练即可泛化到未见 ID 类。
  证据：NegPrompt open-vocabulary 实验——10% ID 训练，AUC 仅下降 ~1.5%（CoOp/LoCoOp 下降 >3-6%）。
  范围：open-vocabulary OOD detection。
  置信度：high。

- 声明：Semantic orthogonality/diversity loss 对确保 negative prompts 覆盖多样的 "not this" 语义至关重要。
  证据：LSN 消融——移除 L_reg 后 FPR95 从 8.56→10.73；NegPrompt 消融——移除 L_NND 后 FPR95 从 8.56→10.73。
  范围：multi-prompt negative learning。
  置信度：medium。

## 证据

- [Out-of-Distribution Detection with Negative Prompts (LSN)](../papers/out-of-distribution-detection-with-negative-prompts.md)：ICLR 2024，class-specific negative prompts，full-paper。
- [Learning Transferable Negative Prompts (NegPrompt)](../papers/learning-transferable-negative-prompts-ood-detection.md)：CVPR 2024，transferable negative prompts，full-paper。
- [Out-of-Distribution Detection](../concepts/out-of-distribution-detection.md)：上位概念。

## 张力

- LSN vs. NegPrompt 的设计分歧——class-specific 覆盖 vs. transferable 通用——尚未在同一 benchmark 和 protocol 下直接比较。
- NegPrompt 的 "可迁移性" 实际指 shared negative templates 与任意 class name 的组合能力，而非 zero-shot OOD detection（仍需知道 ID 类别标签名称）。
- 两个方法都假设 CLIP feature space 质量——CLIP 表示力弱的类别效果可能受限。

## 开放问题

- LSN 的 class-specific 和 NegPrompt 的 shared transferable negative prompts 能否在同一框架中结合？
- Negative prompts 能否增强其他 OOD detection paradigm（如 gradient-based、feature-based、energy-based）？
- 在更大 scale（如 10K+ ID 类）下，negative prompts 的数量和质量如何 scale？
- 是否有必要在训练中引入少量 surrogate OOD 数据来 further boost？
- 在实际 OOD detection 部署场景中，推理延迟翻倍是否可接受？
