---
title: NegPrompt — Transferable Negative Prompts
type: method
domain: outofdistributiondetection
status: active
created: 2026-05-24
updated: 2026-05-24
tags:
  - out-of-distribution-detection
  - negative-prompts
  - transferable
  - open-vocabulary
source_pages:
  - wiki/domains/outofdistributiondetection/papers/learning-transferable-negative-prompts-ood-detection.md
related_pages:
  - wiki/domains/outofdistributiondetection/concepts/out-of-distribution-detection.md
  - wiki/domains/outofdistributiondetection/topics/negative-prompt-ood-detection.md
  - wiki/domains/outofdistributiondetection/methods/lsn.md
---

# NegPrompt — 可迁移 Negative Prompts 的 OOD 检测

## 定义

NegPrompt 只用 ID 数据学习一组可迁移 negative prompts（而非 class-specific），实现 open-vocabulary OOD detection。每个 negative prompt 表示某一类别标签的 "negative connotation"，不绑定具体类别标签，因而能迁移到训练时未见的新 ID 类别。核心创新是 L_NIS 损失——用均匀分布替代 OOD 数据驱动 negative prompts 学习，无需任何外部 outlier data。

## 核心机制

1. **两阶段训练**（一阶段联合训练会严重破坏 positive prompts，FPR95 从 25.86% 飙至 90.07%）：
   - 第一阶段：用 CoOp 学习 positive prompts → 冻结。
   - 第二阶段：学习共享 negative prompts（每类 2 个）。
2. **三损失函数**：
   - $L_{NIS}$（Negative-Image Separation）：将 ID 图像概率均匀分布在所有 negative prompts 上，迫使 negative text features 推离 ID 图像——受 Outlier Exposure 启发但无需实际 outlier。
   - $L_{NPD}$（Negative-Positive Distance）：约束 negative 不要太远离 positive，防止学到 trivial prompts（既远离 ID 又远离 OOD）。
   - $L_{NND}$（Negative-Negative Distance）：最大化同一类内 negative prompts 之间距离，确保多样性。
3. **可迁移性**：Negative prompts 不绑定类别标签——学的是 "generic negative semantics templates"，可与任意类别名组合。训练时仅用 10% ID 类别的图像，inference 时与全部 ID 类别（含未见类别）组合。

## 假设

- Negative prompts 可以通过仅 ID 数据学习（均匀分布假设替代 OOD 样本）。
- Generic negative semantics（不绑定具体类别）可以泛化到训练未见 ID 类。
- 两阶段训练对于防止 positive prompts 被破坏是必需的。

## 证据

- CVPR 2024, Li et al.，full-paper，有代码 (github.com/mala-lab/negprompt)。
- ImageNet-1K 常规 OOD：FPR95 23.01%，AUROC 94.81%（MCM: 42.74%/90.76%，CLIPN: 31.10%/93.10%，LoCoOp: 28.66%/93.52%）。
- 4 个 ImageNet-1K hard OOD splits：平均 AUROC 97.96%，FPR95 8.18%。
- Open-vocabulary（10% ID 类训练）：AUROC 96.46%，FPR95 13.36%——仅下降约 1.5%（CoOp 下降 >3%，LoCoOp >6%）。
- ID 分类：72.1%（full ID），与 CoOp 相同，不损害 ID 分类。
- T-SNE 可视化：negative text features 在 latent space 中位于 ID 数据外围，形成有效的"围栏"。
- Ablation：移除 L_NND → FPR95 升至 10.73%；每个类 2 个 negative prompts 最优。

## 变体

无独立变体。NegPrompt 使用 CLIP-B/16 (OpenCLIP) 作为 backbone，每类 2 个 negative prompts。

## 优势与局限

**优势**：
- 首个在 open-vocabulary 设定下工作的 prompt-learning OOD 检测方法。
- L_NIS 用均匀分布替代 OOD 数据——优雅解决无 OOD 数据问题。
- 可迁移性与 class-specific 方法（LSN）形成互补。
- 不损害 ID 分类准确率。

**局限**：
- 依赖 CLIP 特征质量，对 CLIP 表示弱的类别效果可能不佳。
- Negative prompts 数量需在计算成本和精度间权衡。
- Open-vocabulary 仍使用全部 ID 类别标签名称（只是不用其训练图像）。
- 与 LSN 的直接比较因评估设置不完全相同而需谨慎（ID 类数量差异等）。
- 均匀分布假设在 ID 类别极端（10 vs. 10000 类）时的行为未充分验证。

## 关联

- [Out-of-Distribution Detection](../concepts/out-of-distribution-detection.md)：上位概念。
- [Negative Prompt OOD Detection](../topics/negative-prompt-ood-detection.md)：方法族主题页。
- [LSN](lsn.md)：互补分支——NegPrompt 强调可迁移性（shared prompts），LSN 强调 class-specific 覆盖（per-class prompts）。

## 开放问题

- 当目标 ID 域与训练 ID 域语义差异极大时，可迁移性上限在哪？
- 能否将 NegPrompt 的 shared transferable negative prompts 与 LSN 的 class-specific negative prompts 结合？
- 均匀分布假设（L_NIS）在 ID 类别数极端（10 vs. 10000）时的行为？
- 如何在保持可迁移性的同时增加 negative prompts 数量进一步提升检测精度？
