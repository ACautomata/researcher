---
title: LSN vs NegPrompt — Negative Prompt OOD 检测方法对比
type: comparison
domain: outofdistributiondetection
status: active
created: 2026-05-24
updated: 2026-05-24
tags:
  - negative-prompts
  - ood-detection
  - clip
  - method-comparison
source_pages:
  - wiki/domains/outofdistributiondetection/papers/out-of-distribution-detection-with-negative-prompts.md
  - wiki/domains/outofdistributiondetection/papers/learning-transferable-negative-prompts-ood-detection.md
related_pages:
  - wiki/domains/outofdistributiondetection/methods/lsn.md
  - wiki/domains/outofdistributiondetection/methods/negprompt.md
  - wiki/domains/outofdistributiondetection/topics/negative-prompt-ood-detection.md
---

# LSN vs NegPrompt — Negative Prompt OOD 检测方法对比

## 问题

LSN (ICLR 2024) 和 NegPrompt (CVPR 2024) 都使用了 negative prompt learning 进行 CLIP-style OOD 检测，它们的核心差异是什么？各自适用什么场景？

## 范围

- 方法维度：negative prompt 学习策略（class-specific vs. transferable）、损失函数设计、可迁移性。
- 实验维度：ID 数据集规模（100 vs. 1000 类）、OOD benchmark、open-vocabulary 能力。
- 不包含：计算效率对比（两方法在训练/推理成本上相近——均比 CoOp 约翻倍）。

## 对比表

| 维度 | LSN (ICLR 2024) | NegPrompt (CVPR 2024) |
|------|-----------------|----------------------|
| **Negative Prompt 策略** | Class-specific（每个 ID 类 K 个独立 prompts） | Class-shared transferable（一组 prompts 跨类共享） |
| **每类 prompt 数** | K=3（class-specific negatives）+ 1 shared positive | 2 shared negative prompts |
| **Positive Prompt** | CoOp/CoCoOp（shared） | CoOp（shared，第一阶段冻结） |
| **核心损失** | $L = L_{empirical} + \lambda L_{orthogonality}$ | $L = L_{NIS} + \beta L_{NPD} + \gamma L_{NND}$ |
| **多样性正则** | Semantic Orthogonality Loss（类内正交） | $L_{NND}$（类内距离最大化）+ $L_{NPD}$（NP 距离约束） |
| **关键洞察** | Positive 靠 class name 携带语义（shared 足够）；Negative 必须由 learned prompts 自身表达（必须 class-specific） | 用均匀分布假设替代 OOD 数据（$L_{NIS}$）；两阶段训练必需 |
| **可迁移性** | ❌ 不可迁移——负 prompts 绑定具体类 | ✅ 可迁移——仅用 10% ID 类训练可泛化到全部 |
| **Open-Vocabulary** | 不支持 | 首个支持的 prompt-learning OOD 检测方法 |
| **ID 类数量** | ImageNet-100 / ImageNet-1K | ImageNet-1K（1000 类） |
| **最佳 FPR95** | 8.56%（ImageNet-100, CoCoOp+LSN） | 23.01%（ImageNet-1K, 常规 OOD） |
| **最佳 AUROC** | 98.05%（ImageNet-100） | 94.81%（ImageNet-1K）；97.96%（Hard OOD splits） |
| **Hard OOD** | 未独立评估 | 4 个 ImageNet-1K splits: AUROC 97.96%, FPR95 8.18% |
| **训练稳定性** | 无特殊要求（CoOp positive 可同时或先后训练） | 两阶段训练必须保留（同时训练 FPR95 飙至 90.07%） |
| **ID 分类影响** | 不损害 ID 分类准确率 | 不损害 ID 分类（72.1% vs. CoOp 72.1%） |

## 发现

1. **根本哲学差异**：LSN 认为 negative features 极其多样，必须用 class-specific multi-prompt 才能覆盖——多样化优先。NegPrompt 认为 negative prompts 可以学到 generic semantics，不绑定类别实现迁移——通用性优先。
2. **不可直接排名**：两者的 ID 类数量不同（100 vs. 1000），OOD benchmark 不完全一致——FPR95/AUROC 的数值比较需要谨慎。LSN 在 100 类上的 8.56% FPR95 优于 NegPrompt 在 1000 类上的 23.01% FPR95，但 ID 类数量差异使直接比较不 fair。
3. **Positive vs. Negative 的根本差异（LSN 的发现）是跨方法的通用 insight**：NegPrompt 的两阶段训练稳定性要求也验证了这一点——negative prompts 的学习与 positive 有本质不同。
4. **可迁移性是 NegPrompt 的独特优势**：在 open-vocabulary 设定（10% ID 类训练）下 FPR95 仅上升 ~3%（CoOp >3%, LoCoOp >6%）。LSN 在 open-vocabulary 场景中可能需要为每个新类重新学习 negative prompts。
5. **结合的可能性**：NegPrompt 训练一组可迁移的 shared negative prompts 作为 base，LSN 在此基础上为关键类别（如高频类或易混淆类）增加 class-specific negative prompts——混合策略可能兼具通用性和覆盖率。

## 注意事项

- LSN 和 NegPrompt 的直接比较因评估设置不完全相同（ID 类数量差异、OOD 数据集选择差异、Backbone 和预训练权重差异）而需谨慎。
- LSN 在 ICLR 2024 发表（先于 NegPrompt 的 CVPR 2024），但两者同期独立发展——NegPrompt 的 paper 中已引用 LSN 并讨论差异。
- 表格中的 "最佳 FPR95" 来自不同 ID 类数设置，不可直接对比。

## 证据

- LSN paper: ICLR 2024, full-paper。Table 1 (ImageNet-100), Table 2 (ImageNet-1K), Table 5 (positive vs. negative prompt comparison)。
- NegPrompt paper: CVPR 2024, full-paper。Table 1 (常规 OOD), Table 2 (Hard OOD), Table 3 (open-vocabulary), Fig 4 (两阶段训练必要性)。

## 后续

- 标准化 OOD benchmark 协议——使 LSN 和 NegPrompt 可在相同 ID 类数、相同 OOD 数据集下直接比较。
- 探索 LSN + NegPrompt 的混合策略：shared transferable base + class-specific extension。
- 创建统一的 negative prompt OOD detection benchmark 对比表（含更多后续方法如 CLIPN、LoCoOp 的更新对比）。
