---
title: LSN — Learn to Say No
type: method
domain: outofdistributiondetection
status: active
created: 2026-05-24
updated: 2026-05-24
tags:
  - out-of-distribution-detection
  - negative-prompts
  - class-specific
  - clip-prompt-learning
source_pages:
  - wiki/domains/outofdistributiondetection/papers/out-of-distribution-detection-with-negative-prompts.md
related_pages:
  - wiki/domains/outofdistributiondetection/concepts/out-of-distribution-detection.md
  - wiki/domains/outofdistributiondetection/topics/negative-prompt-ood-detection.md
  - wiki/domains/outofdistributiondetection/methods/negprompt.md
---

# LSN — 学习拒绝的 Class-Specific Negative Prompts

## 定义

LSN 为 CLIP-style OOD 检测学习 class-specific negative prompts。核心发现是 handwritten negative prompts（如 "not a photo of a [class]"）高度欠指定——negative features 极其多样，无法被单一共享 prompt 覆盖。通过为每类学习 K 个独立的 negative prompts + semantic orthogonality 正则化确保多样性，LSN 在多个 OOD benchmark 上大幅超越 prompt-learning baseline。

## 核心机制

1. **Positive + Negative 双 Prompt 学习**：
   - Positive prompts (V)：跨所有类别共享（由 CoOp/CoCoOp 训练）。
   - Negative prompts (Ṽ)：每个类别学 K 个（实验中 K=3），表示该类别的 "negative semantics"。
2. **损失函数**：
   - Empirical Classification Loss $L$：学习将 ID 图像分类为其"不属于"的类别。
   - Semantic Orthogonality Loss $L_{reg} = \sum_c \sum_i \sum_{j=i+1} |\cos(t_i^c, t_j^c)|$：最大化同一类内 negative prompts 之间的角度，覆盖多样、不重叠的 negative features。
   - 总损失：$L^- = L + \lambda \cdot L_{reg}$（$\lambda=0.1$）。
3. **OOD Scoring**：$S(x) = \max_c [MCM_{pos}(x, c)] - \min_c [MCM_{neg}(x, c)]$。ID 图像在 positive 上得分高、negative 上低 → S(x) 大；OOD 相反。

## 假设

- Negative features 具有内在多样性，必须用 class-specific + multi-prompt 策略覆盖。
- Positive prompt learning 中 class name 携带主要语义（cross-class shared 足够），而 negative prompt learning 中语义必须由 learned prompts 自身表达。
- Semantic orthogonality 是确保 multi-prompt 不塌缩为单一模式的有效正则。

## 证据

- ICLR 2024, Nie et al.，full-paper，有代码 (github.com/junz-debug/lsn)。
- ImageNet-100：CoCoOp+LSN FPR95 8.56%（CoCoOp 14.86%，MCM 32.58%），AUROC 98.05%。
- ImageNet-1K：CoCoOp+LSN FPR95 30.22%（MCM 43.55%，CLIPN 31.10%）。
- Positive vs. Negative 根本差异（Table 5）：class-shared negative FPR95 从 21.94 飙至 81.27；去除 class name 对 positive 影响大但对 negative 无影响。
- Positive：8 个 prompt、25 epochs；Negative：每类 3 个 prompt、5 epochs（Table 5 消融数据——当前 paper 页缺定量数字）。
- Semantic orthogonality removal：FPR95 从 8.56 升至 10.73。
- 跨架构鲁棒：CLIP-RN50x4、CLIP-B/32、BLIP 上均有效。
- 不损害 ID 分类准确率。

## 变体

- **CoOp + LSN**：positive prompts 使用 CoOp 训练。
- **CoCoOp + LSN**：positive prompts 使用 CoCoOp 训练（条件化图像特征），性能最高。

## 优势与局限

**优势**：
- 首次系统性研究 class-specific negative prompts 在 OOD 检测中的价值。
- 发现了 positive 和 negative prompt learning 的根本差异（定性 insight 而非仅性能提升）。
- 可与 CoOp/CoCoOp 无缝集成，不损害 ID 分类。
- 跨 backbone、多 ID 类数量设置下表现一致。

**局限**：
- 强烈依赖 CLIP 的 feature quality。
- 相比 CoOp 训练和推理时间约翻倍（两组 prompts）。
- Prompt 学习参数量有限，训练样本增加时性能不继续提升。
- Class-specific 设计不可迁移到训练未见 ID 类——与 NegPrompt 的 transferability 相对。
- 未探索 open-vocabulary 能力。

## 关联

- [Out-of-Distribution Detection](../concepts/out-of-distribution-detection.md)：上位概念。
- [Negative Prompt OOD Detection](../topics/negative-prompt-ood-detection.md)：方法族主题页。
- [NegPrompt](negprompt.md)：互补分支——LSN 强调 class-specific 覆盖（更多样），NegPrompt 强调可迁移性（更通用）。
- 与 EASE 的跨模态遗忘形成对比：LSN 用 negative prompts 增强 OOD 判别边界，EASE 用 modality anchor 防止遗忘。

## 开放问题

- LSN 的 class-specific negative prompts 能否与 NegPrompt 的 shared transferable negative prompts 结合？
- 每类的最优 negative prompts 数量如何自适应确定？
- 在 open-vocabulary OOD detection 中的扩展？
- 当训练数据包含部分 OOD 信息（outlier exposure setting）时的进一步提升？
