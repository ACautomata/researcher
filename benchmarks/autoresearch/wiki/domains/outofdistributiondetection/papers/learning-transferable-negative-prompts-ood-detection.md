---
title: Learning Transferable Negative Prompts for Out-of-Distribution Detection
type: paper
domain: outofdistributiondetection
status: stable
created: 2026-04-25
updated: 2026-05-05
tags:
  - out-of-distribution-detection
  - negative-prompts
  - open-vocabulary-learning
  - cvpr-2024
paper:
  title: Learning Transferable Negative Prompts for Out-of-Distribution Detection
  authors:
    - Tianqi Li
    - Guansong Pang
    - Xiao Bai
    - Wenjun Miao
    - Jin Zheng
  year: 2024
  venue: CVPR 2024
  arxiv: ""
  doi: ""
  code: "https://github.com/mala-lab/negprompt"
  project: ""
classification:
  label: outofdistributiondetection
  task:
    - out-of-distribution detection
    - open-vocabulary recognition
  method_family:
    - transferable negative prompts
    - NegPrompt
    - ID-only prompt learning
  modality:
    - image
    - vision-language (CLIP)
  datasets:
    - ImageNet-1K (ID)
    - Texture
    - iNaturalist
    - Places
    - SUN
    - ImageNet hard OOD splits
    - TinyImageNet
  metrics:
    - AUROC
    - FPR95
    - ID classification accuracy
evidence_level: full-paper
raw_sources:
  - raw/sources/2024-05-31-learning-transferable-negative-prompts-ood-detection.pdf
related_pages:
  - wiki/domains/outofdistributiondetection/concepts/out-of-distribution-detection.md
  - wiki/domains/outofdistributiondetection/topics/negative-prompt-ood-detection.md
  - wiki/domains/outofdistributiondetection/methods/negprompt.md
  - wiki/domains/outofdistributiondetection/comparisons/lsn-vs-negprompt.md
---

# Learning Transferable Negative Prompts for Out-of-Distribution Detection

## 引用

Tianqi Li, Guansong Pang, Xiao Bai, Wenjun Miao, Jin Zheng. Learning Transferable Negative Prompts for Out-of-Distribution Detection. CVPR 2024. Code: https://github.com/mala-lab/negprompt

## 一句话贡献

提出 NegPrompt——只用 ID 数据学习一组可迁移 negative prompts 的 OOD 检测方法。每个 negative prompt 表示某一类别标签的 negative connotation（即 "不是某类" 的语义），用于划定 ID 与 OOD 图像的边界。关键创新在于 negative prompts 不绑定具体类别标签，因而能迁移到训练时未见的新类别，实现 open-vocabulary OOD detection。

## 问题设定

### 现有 Prompt Learning OOD 检测的局限
- 已有 prompt learning 方法在 OOD 检测中展现一定能力，但训练中缺乏 OOD 图像导致 ID 类别与 OOD 图像之间的 mismatch，产生高假阳性率。
- 当前方法假设训练时可用所有 ID 类别样本，在 open-vocabulary 场景（inference 出现训练时未见的新 ID 类别）下失效。

### 核心挑战
- **缺乏 OOD 数据**：训练时无法接触 OOD 样本，如何学习有效的 OOD 判别边界？
- **可迁移性**：如何让 negative prompts 能泛化到训练时未见的 ID 类别标签？
- **多样性**：单个类别的 "不是某物" 语义是高度多样的——如何用少量 prompts 覆盖？

## 方法

NegPrompt 基于 CLIP（CLIP-B/16, OpenCLIP 预训练），分两阶段训练：

### 第一阶段：学习 Positive Prompts
- 使用 CoOp 方法在 ID 数据上学习 positive prompts。
- 获得准确的 ID 类别语义表示后冻结。

### 第二阶段：学习 Negative Prompts
学习一组共享的 negative prompts（实验中每个 ID 类 2 个），通过三个损失函数驱动：

**1. Negative-Image Separation Loss (L_NIS)**
- 核心创新：受 Outlier Exposure 启发但无需实际 outlier 数据。
- 将 ID 图像的概率分布在所有 negative prompts 上均匀分布，迫使 negative text features 推离 ID 图像。
- L_NIS = E_x~ID[H(u; F(x))]，其中 u 是均匀分布，F(x) 是 negative prompts 上的 softmax 概率。

**2. Negative-Positive Distance Loss (L_NPD)**
- 约束 negative text features 不要离 positive text features 太远。
- 防止学到 trivial 的 negative prompts（既远离 ID 又远离 OOD）。
- L_NPD = -1/(k*p) · Σ Σ sim(T^{f,neg}_{i,j}, T^{f,pos}_j)

**3. Negative-Negative Distance Loss (L_NND)**
- 最大化同一类别内不同 negative prompts 之间的距离。
- 确保学到多样、不重叠的 negative prompts，覆盖多样的 "not this class" 语义。
- L_NND = 1/(k*p*(p-1)) · Σ Σ Σ_{l≠i} sim(T^{f,neg}_{i,j}, T^{f,neg}_{l,j})

**总损失**：L_NegativePrompts = L_NIS + β·L_NPD + γ·L_NND（β=0.1, γ=0.05）

### Open-Vocabulary 能力
- Negative prompts 不绑定具体类别标签——它们学的是 "generic negative semantics templates"，可与任意类别名组合。
- 训练时只用 10% ID 类别的图像，inference 时与全部 ID 类别（含未见类别）组合使用。
- 这使得 NegPrompt 成为首个可在 open-vocabulary 设定中工作的 prompt-learning OOD 检测方法。

### Inference
使用扩展的 MCM scoring：S(x) = max(p(y=i|x))，其中 softmax 分母同时包含 positive 和 negative 相似度。ID 图像匹配 positive → 高 softmax 分数（低 OOD 分数）；OOD 图像匹配 negative → 低 softmax 分数（高 OOD 分数）。

## 实验

### 实验设置
- **ID 数据集**：ImageNet-1K（1000 类），每类 16-shot 训练。
- **OOD 数据集**：Texture、iNaturalist、Places、SUN（常规 OOD）；4 个 ImageNet-1K splits（hard OOD）。
- **Split-1**：所有 dog 类为 ID，非动物类为 OOD。
- **Split-2**：一半 hunting dog 类为 ID，其他四足动物为 OOD。
- **Split-3**：常见类别混合 ID 和 OOD。
- **Split-4**：前 100 类 ID，后 900 类 OOD。
- **基线**：MCM、CLIPN（zero-shot）；MSP、MaxLogit、Energy、ReAct、ODIN（CLIP-adapted post-hoc）；CoOp、LoCoOp（prompt learning）。
- **评估指标**：FPR95↓、AUROC↑、ID ACC。

### 主要结果

**常规 OOD 检测（ImageNet-1K full ID）**：

| 方法 | Avg FPR95↓ | Avg AUROC↑ |
|------|-----------|------------|
| MCM | 42.74 | 90.76 |
| CLIPN | 31.10 | 93.10 |
| CoOp | 51.68 | 91.78 |
| LoCoOp | 28.66 | 93.52 |
| **NegPrompt** | **23.01** | **94.81** |

- 相比最佳 zero-shot 方法 CLIPN：AUROC +1.7%，FPR95 -8%。
- 相比 CoOp：FPR95 降低约 28%（51.68→23.01）。
- 相比 LoCoOp：FPR95 降低约 5%。

**Hard OOD 检测**：
- 在 4 个 ImageNet-1K splits 上，NegPrompt 平均 AUROC 97.96%，FPR95 8.18%。
- Open-vocabulary 设置下（仅 10% ID 类训练）：AUROC 96.46%，FPR95 13.36%。

**Open-Vocabulary OOD Detection**：
- 仅用 10% ID 类训练 → 性能仍超过大多数使用全部 ID 类训练的方法。
- CoOp 在 open-vocabulary 设置下 AUC 下降 >3%，LoCoOp 下降 >6%，NegPrompt 仅下降约 1.5%。
- 证明了 negative prompts 的可迁移性。

**ID 分类准确率**：
- NegPrompt (full ID): 72.1%（与 CoOp 相同，不损害 ID 分类）。
- NegPrompt (10% ID): 71.9%（略微下降）。
- LoCoOp 降至 71.7%（其 OOD 检测能力以牺牲 ID 分类为代价）。

### 分析

**为什么 NegPrompt 有效？**
- 在 4 个 OOD 数据集上计算 ID/OOD 图像与 positive/negative prompts 的相似度。
- 结果：ID 图像与 positive prompts 相似度最高，OOD 图像与 negative prompts 相似度最高。
- T-SNE 可视化显示 negative text features 在 latent space 中位于 ID 数据外围，OOD 图像散布其间——形成有效的 "围栏"。

**Ablation 实验**：
- **Backbone**：ViT-based 优于 CNN-based（ResNet），ViT-B-16 最佳。
- **Negative prompts 数量**：1→2 个持续提升，更多可进一步提升但成本增长。
- **训练过程**：两阶段训练（先 positive 后 negative）必须保留——同时训练会严重破坏 positive prompts 学习。
- 移除 negative prompts：FPR95 从 8.56% 升至 14.86%。
- 移除 semantic orthogonality loss (L_NND)：FPR95 升至 10.73%。

## 结果

- NegPrompt 是首个实现在 open-vocabulary 设定下工作的 prompt-learning OOD 检测方法。
- L_NIS 的核心技巧——用均匀分布替代 OOD 数据驱动 negative prompts 学习——优雅地解决了无 OOD 数据问题。
- 可迁移性是 NegPrompt 区别于 class-specific negative prompt 方法（如 LSN/ICLR 2024）的关键特征。
- 两阶段训练对于稳定性至关重要。

## 限制

- NegPrompt 依赖 CLIP 的特征质量，对于 CLIP 本身表示能力较弱的类别效果可能不佳。
- Negative prompts 数量需要在计算成本和检测精度间权衡。
- Open-vocabulary 设置下仍使用全部 ID 类别的标签名称（只是不用其训练图像）——纯 zero-shot ID label 的设定更严苛。
- 与 LSN 的直接比较因评估设置不完全相同（ImageNet-100 vs. ImageNet-1K ID 类数量差异）而需谨慎。

## 可复用 Claims

- 声明：Negative prompts 可以只用 ID 数据学习，无需任何外部 outlier data。
  证据：L_NIS 利用均匀分布假设替代 OOD 样本，NegPrompt 在 ImageNet-1K 上 FPR95 23.01%。
  范围：CLIP-style OOD detection，常规和 hard OOD 场景。
  置信度：high。
  张力：均匀分布假设在 ID 类别数量极大或极小时的适用性可能需要进一步验证。

- 声明：Transferability 是 negative prompt 学习的重要设计维度——不绑定类别的 generic negative semantics 可以泛化到训练未见类别。
  证据：仅用 10% ID 类训练，open-vocabulary 下 FPR95 仅上升 ~3%（CoOp 和 LoCoOp 上升显著更多）。
  范围：open-vocabulary OOD detection。
  置信度：high。
  张力：需要更大规模的 open-vocabulary 测试（如含全新语义域的 ID 类）。

- 声明：L_NPD（限制 negative-positive 距离）对防止学到 trivial negative prompts 至关重要。
  证据：消融实验中 L_NPD 移除会导致 negative prompts 远离 ID 和 OOD 图像，失去判别能力。
  范围：CLIP-style negative prompt learning。
  置信度：medium。
  张力：optimal distance constraint 的强度仍需进一步分析。

- 声明：两阶段训练（先 positive 后 negative）对 prompt-learning OOD 检测的稳定性是必需的。
  证据：一阶段联合训练导致 positive prompts 学习被严重破坏，FPR95 从 25.86% 飙升至 90.07%。
  范围：prompt-learning-based OOD detection 中涉及 positive 和 negative prompts 的方法。
  置信度：high。

## 连接

- [Out-of-Distribution Detection](../concepts/out-of-distribution-detection.md)：上位概念页。
- [Negative Prompt OOD Detection](../topics/negative-prompt-ood-detection.md)：negative prompt 方法族主题页。
- NegPrompt 与 LSN（ICLR 2024）构成 negative-prompt OOD 检测的两个代表性分支：NegPrompt 强调可迁移性（shared prompts），LSN 强调 class-specific 覆盖（per-class prompts）。

## 开放问题

- Negative prompts 的可迁移性上限在哪——当目标 ID 域与训练 ID 域语义差很远时？
- 能否将 NegPrompt 的 shared transferable negative prompts 与 LSN 的 class-specific negative prompts 结合？
- 均匀分布假设（L_NIS）在 ID 类别数极端（如 10 vs. 10000）时的行为？
- 如何在保持可迁移性的同时增加 negative prompts 数量来进一步提升检测精度？

## 来源

- [Canonical raw PDF](../../../../raw/sources/2024-05-31-learning-transferable-negative-prompts-ood-detection.pdf)
- [Code repository](https://github.com/mala-lab/negprompt)
- PDF 正文已完整抽取，覆盖 introduction、method（三损失函数 + open-vocabulary 机制）、experiments（全部表格 + 可视化 + ablation）、conclusion 全部章节。
