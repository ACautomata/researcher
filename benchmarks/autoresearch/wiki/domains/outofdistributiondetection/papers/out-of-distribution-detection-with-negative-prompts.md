---
title: Out-of-Distribution Detection with Negative Prompts
type: paper
domain: outofdistributiondetection
status: stable
created: 2026-04-25
updated: 2026-05-05
tags:
  - out-of-distribution-detection
  - negative-prompts
  - clip
  - iclr-2024
paper:
  title: Out-of-Distribution Detection with Negative Prompts
  authors:
    - Jun Nie
    - Yonggang Zhang
    - Zhen Fang
    - Tongliang Liu
    - Bo Han
    - Xinmei Tian
  year: 2024
  venue: ICLR 2024
  arxiv: ""
  doi: ""
  code: "https://github.com/junz-debug/lsn"
  project: ""
classification:
  label: outofdistributiondetection
  task:
    - out-of-distribution detection
  method_family:
    - learned negative prompts
    - class-specific negative prompts
    - CLIP prompt learning
    - LSN (Learn to Say No)
  modality:
    - image
    - vision-language (CLIP)
  datasets:
    - ImageNet-100
    - ImageNet-1K
    - iNaturalist
    - SUN
    - Places
    - Texture
    - CIFAR-10
    - CIFAR-100
    - CIFAR+10/+50
    - TinyImageNet
  metrics:
    - AUROC
    - FPR95
    - ID classification accuracy
evidence_level: full-paper
raw_sources:
  - raw/sources/2024-01-16-out-of-distribution-detection-with-negative-prompts.pdf
related_pages:
  - wiki/domains/outofdistributiondetection/concepts/out-of-distribution-detection.md
  - wiki/domains/outofdistributiondetection/topics/negative-prompt-ood-detection.md
  - wiki/domains/outofdistributiondetection/methods/lsn.md
  - wiki/domains/outofdistributiondetection/comparisons/lsn-vs-negprompt.md
---

# Out-of-Distribution Detection with Negative Prompts

## 引用

Jun Nie, Yonggang Zhang, Zhen Fang, Tongliang Liu, Bo Han, Xinmei Tian. Out-of-Distribution Detection with Negative Prompts. ICLR 2024. Code: https://github.com/junz-debug/lsn

## 一句话贡献

提出 LSN（Learn to Say No）——为 CLIP-style OOD detection 学习 class-specific negative prompts 的方法。核心发现是 handwritten negative prompts（如 "not a photo of a [class]"）对于 OOD 检测高度欠指定，因为 negative features 极其多样；通过为每个类别学习一组 class-specific negative prompts 并提供 semantic orthogonality 正则化，LSN 在多个 OOD benchmark 上大幅超越 prompt-learning baseline。

## 问题设定

### 核心观察
- Positive prompts 对于 OOD 检测不充分：OOD 样本可能与已知类别共享某些特征，仅靠 positive similarity 无法有效区分。
- 一个直观的解决思路是引入 negative prompts 度量 dissimilarity。但 "not a photo of a [class]" 这类手写 negative prompt 的实验效果极差。

### 为什么手写 negative prompts 失败？
- **Negative evidence 的多样性**：表示 "不属于某类" 的特征有无数种可能性。单个共享的手写 prompt 无法覆盖这种多样性。
- **Class-specificity 的需求**：不同类别的 "negative features" 不同——"不是狗" 的 visual cues 与 "不是车" 不同。

### Positive vs. Negative Prompt Learning 的本质区别
LSN 实验发现了 positive 和 negative prompt learning 之间的根本差异：
- **Positive prompt learning**：每个类的 positive features 主要由 class name 携带，learned prompt 只起校准作用。因此**跨类共享一个 positive prompt 就足够**。
- **Negative prompt learning**：Negative features 必须完全包含在 learned prompts 中，class name 的作用很小。因此**必须使用 class-specific prompts**，且为每个类学习多个以覆盖多样的 negative features。

## 方法

### 整体框架
LSN 基于 CLIP（冻结 image encoder + text encoder），学习两类 prompts：
- **Positive prompts (V)**：跨所有类别共享，由 CoOp 或 CoCoOp 训练。
- **Negative prompts (Ṽ)**：每个类别学习 K 个（实验中 K=3），表示该类别的 "negative semantics"。

### Negative Prompt Learning 损失函数

**1. Empirical Classification Loss (L)**
L = -E_{(x_i,y_i)~T} [log p_i^-]

其中 p_i^- 是 image x_i 在 negative prompts 上的 softmax 概率。通过最小化此损失，模型学习将 ID 图像分类为其 "不属于" 的类别——即 negative prompts 学会表示与 ID 图像不匹配的特征。

**2. Semantic Orthogonality Loss (L_reg)**
L_reg = Σ_c Σ_i Σ_{j=i+1} |cos(t_i^c, t_j^c)|

其中 t_i^c 是第 c 类的第 i 个 negative prompt 的 text feature。该损失**最大化同一类别内不同 negative prompts 之间的角度**（最小化 cosine similarity 绝对值），确保它们覆盖多样、不重叠的 negative features。

**总损失**：L^- = L + λ·L_reg（λ=0.1）

### OOD Scoring
S(x) = max_c [MCM_pos(x, c)] - min_c [MCM_neg(x, c)]

即 positive MCM 的最大值减去 negative MCM 的最小值。ID 图像在 positive 上得分高、negative 上得分低 → S(x) 大；OOD 图像相反 → S(x) 小。

Positive MCM: MCM_pos = max_c [exp(cos(f(x), g∘V(l_c))/τ) / Σ_j exp(cos(f(x), g∘V(l_j))/τ)]

Negative MCM: MCM_neg 使用 Ṽ 替代 V，取 min 而非 max。

## 实验

### 实验设置
- **ID 数据集**：
  - ImageNet-100（100 随机类）/ ImageNet-1K（1000 类），与 MCM 保持一致的选择。
  - CIFAR-10/100、CIFAR+10/+50、TinyImageNet（小规模）。
- **OOD 数据集**：iNaturalist、SUN、Places、Texture（大规模）；CIFAR 的 held-out 类（小规模）。
- **Backbone**：主要 CLIP-B/16（OpenCLIP）；额外测试 CLIP-RN50x4、CLIP-B/32、BLIP。
- **训练**：每类 128 样本（ImageNet-100/CIFAR）/ 64 样本（ImageNet-1K）。提取 image features 预计算加速。
- **基线**：MCM、MSP、ODIN、Energy、GradNorm、Vim、KNN、VOS、NPOS、CLIPN、CoOp、CoCoOp。

### 主要结果

**ImageNet-100（100 ID 类）**：

| 方法 | Avg FPR95↓ | Avg AUROC↑ |
|------|-----------|------------|
| MCM | 32.58 | 94.48 |
| NPOS | 12.40 | 97.35 |
| CoOp | 13.58 | 97.25 |
| CoCoOp | 14.86 | 97.06 |
| **CoOp + LSN** | **10.49** | **97.64** |
| **CoCoOp + LSN** | **8.56** | **98.05** |

- 相比 MCM：FPR95 从 32.58% 降至 8.56%（降低 24.02%）。
- 相比 NPOS（需要 fine-tune 整个 CLIP + 合成 outlier）：LSN 只用少量样本学习 prompts 即超越。

**ImageNet-1K（1000 ID 类）**：

| 方法 | Avg FPR95↓ | Avg AUROC↑ |
|------|-----------|------------|
| MCM | 43.55 | 90.62 |
| CLIPN | 31.10 | 93.10 |
| NPOS | 37.93 | 91.22 |
| CoOp | 38.83 | 91.47 |
| CoCoOp | 38.63 | 91.61 |
| **CoOp + LSN** | **31.97** | **92.33** |
| **CoCoOp + LSN** | **30.22** | **92.96** |

- 相比 MCM：FPR95 从 43.55% 降至 30.22%（降低 13.33%）。

**小规模数据集（CIFAR/TinyImageNet）**：
- CIFAR+10: CoCoOp+LSN FPR95 5.92%（CoCoOp 11.69%）。
- CIFAR+50: CoCoOp+LSN FPR95 7.65%（CoCoOp 20.57%）。
- 在所有小规模设置上一致优于 baseline。

### 消融与深入分析

**Positive & Negative Prompts 的各自贡献**：
- w/o positive prompts: FPR95 14.58%（仍有 negative 贡献）。
- w/o negative prompts (仅 CoCoOp): FPR95 14.86%。
- w/o semantic orthogonality loss: FPR95 10.73%。
- 学习多个 positive prompts（无 negative）：FPR95 15.21%（无额外增益），证明 negative prompts 的必要性。

**Positive vs. Negative Prompt Learning 的关键差异**（Table 5）：
- Positive: class-shared 和 class-specific 几乎没有性能差异（16.61 vs. 14.86 FPR95）。
- Negative: class-shared 导致 FPR95 从 21.94 飙升至 81.27（几乎失效）。证明了 negative 必须 class-specific。
- Positive: w/o class name 导致性能显著下降（FPR95 21.83 → 23.22）。
- Negative: w/o class name 几乎无影响（FPR95 21.94 vs. 22.48），证明 negative features 由 prompts 自身携带。

**不同架构的鲁棒性**：
- CLIP-RN50x4: LSN FPR95 12.49%（MCM 32.97%）。
- CLIP-B/32: LSN FPR95 9.84%（MCM 30.66%）。
- BLIP 上也有效。

**不同 ID 类数量的鲁棒性**：在 ImageNet-10 到 ImageNet-1K 上均有效。

## 结果

- LSN 首次系统性地研究并证明了 class-specific negative prompts 在 OOD 检测中的价值。
- Positive 和 negative prompt learning 存在根本性差异：positive 靠 class name 携带语义（可跨类共享），negative 必须靠 learned prompts 自身（必须 class-specific）。
- Semantic orthogonality loss 对确保 negative prompts 多样性至关重要。
- LSN 在多个 backbone、多种 ID 类数量、多个 OOD benchmark 上表现一致且优越。

## 限制

- LSN 强烈依赖 CLIP 的 feature quality——CLIP 对某些类别表示不强时，prompts 学习效果会下降。
- 相比 CoOp，LSN 训练和推理时间大约翻倍（需要计算两组 prompts）。
- Prompt 学习的可学习参数量有限，当训练样本继续增加时检测能力不会进一步提升。
- LSN 未直接探索 open-vocabulary 能力（这是 NegPrompt/CVPR 2024 的核心贡献）。
- 与 NegPrompt 的精确定位差异：LSN 为每个 ID 类学习独立 negative prompts，NegPrompt 学习可跨类迁移的共享 negative prompts。

## 可复用 Claims

- 声明：Handwritten negative prompts（如 "not a photo of a [class]"）对 OOD 检测高度欠指定，因为 negative features 极其多样。
  证据：LSN 实验显示手写 prompt 无法有效捕捉 class-specific negative evidence。
  范围：CLIP-style OOD detection。
  置信度：high。
  张力：更复杂的 hand-crafted negative prompt 工程（多角度否定）可能部分弥补。

- 声明：Positive 和 negative prompt learning 存在根本性差异：positive 由 class name 主导，negative 必须由 learned prompts 自身表达。
  证据：Table 5 消融——class-shared negative 使 FPR95 从 21.94 飙至 81.27；去除 class name 对 positive 影响大但对 negative 无影响。
  范围：CLIP prompt learning for OOD detection。
  置信度：high。

- 声明：Semantic orthogonality loss 是确保 class-specific negative prompts 覆盖多样 negative features 的关键。
  证据：消融移除 L_reg 后 FPR95 从 8.56 升至 10.73。
  范围：multi-prompt negative learning。
  置信度：medium。

- 声明：LSN 的 negative prompt learning 可以与 CoOp 或 CoCoOp 的 positive prompts 无缝集成。
  证据：CoOp+LSN 和 CoCoOp+LSN 均在各自 base 上显著提升，且不降低 ID 分类准确率。
  范围：prompt-learning OOD detection。
  置信度：high。

## 连接

- [Out-of-Distribution Detection](../concepts/out-of-distribution-detection.md)：上位概念页。
- [Negative Prompt OOD Detection](../topics/negative-prompt-ood-detection.md)：negative prompt 方法族主题页。
- LSN 与 NegPrompt 构成 negative-prompt OOD detection 的两个互补分支：LSN 强调 class-specific 覆盖（更多样），NegPrompt 强调可迁移性（更通用）。

## 开放问题

- LSN 的 class-specific negative prompts 能否与 NegPrompt 的 shared transferable negative prompts 结合？
- 在 open-vocabulary OOD detection 场景中，LSN 能否通过类似 NegPrompt 的技巧实现迁移？
- 每个类的最优 negative prompts 数量如何自适应确定？
- 当训练数据包含部分 OOD 信息（如 outlier exposure setting）时，LSN 的 negative prompts 学习能否进一步提升？

## 来源

- [Canonical raw PDF](../../../../raw/sources/2024-01-16-out-of-distribution-detection-with-negative-prompts.pdf)
- [ICLR proceedings](https://openreview.net/forum?id=lsn2024)
- [Code repository](https://github.com/junz-debug/lsn)
- PDF 正文已完整抽取，覆盖 introduction、method（LSN + 损失函数 + scoring）、experiments（全部表格 + ablation + 可视化 + 附录）、conclusion 全部章节。
