# Not All Relations are Equal: Mining Informative Labels for Scene Graph Generation

> 挖掘信息量大的关系标签用于场景图生成，提出显式/隐式关系二分法与缺失隐式标签插补框架

## 元数据

| 字段 | 值 |
|------|-----|
| **标题** | Not All Relations are Equal: Mining Informative Labels for Scene Graph Generation |
| **作者** | Arushi Goel, Basura Fernando, Frank Keller, Hakan Bilen (爱丁堡大学信息学院 / A*STAR CFAR, IHPC) |
| **发表** | CVPR 2022 |
| **arXiv** | [2111.13517](https://arxiv.org/abs/2111.13517) |
| **DOI** | — |
| **代码** | [https://groups.inf.ed.ac.uk/vico/research/NARE](https://groups.inf.ed.ac.uk/vico/research/NARE) |
| **证据等级** | full-paper |
| **原始来源** | [raw/sources/2022-06-20-not-all-relations-are-equal-mining-informative-labels-for-sgg.pdf](/.raw/sources/2022-06-20-not-all-relations-are-equal-mining-informative-labels-for-sgg.pdf) / [raw/sources/2022-06-20-not-all-relations-are-equal-mining-informative-labels-for-sgg.txt](/.raw/sources/2022-06-20-not-all-relations-are-equal-mining-informative-labels-for-sgg.txt) |
| **分类标签** | scene-graph-generation, informative-labels, relation-label-imputation |
| **任务** | Scene Graph Generation (SGG), Predicate Classification, Zero-Shot SGG |
| **方法族** | label imputation, semi-supervised learning, manifold mixup |
| **数据集** | Visual Genome (VG) |
| **指标** | mean Recall@K (mR@20/50/100), zero-shot Recall (zsR@20/50) |
| **入库日期** | 2026-06-10 |

## 摘要

Scene Graph Generation (SGG) 旨在捕获物体对之间的多种交互。现有 SGG 方法在全部关系上训练时，由于训练数据中的各种偏差（长尾分布、标注偏好等），未能学到视觉和文本相关的复杂推理。学习琐碎的关系（如 spatial "on"）而非信息量大的关系（如 "parked on"）阻碍了复杂推理和泛化能力。本文提出一个模型无关的 SGG 训练框架，利用关系标签的**信息量（informativeness）**来提升性能。核心思路是：将关系标签划分为 **explicit（显式/空间）** 和 **implicit（隐式/语义）** 两类，通过交替式标签插补（label imputation）为仅标注显式关系的样本补全缺失的隐式标签，并使用 Manifold Mixup 防止确认偏差。该方法可即插即用于主流 SGG 模型，在 Visual Genome 上显著提升 mR@K 和零样本召回率。

## 核心贡献

1. **首次提出标签信息量（label informativeness）概念**：识别 SGG 中显式关系 vs. 隐式关系的信息量差异，发现隐式关系训练可泛化到显式关系，反之则不能
2. **模型无关的交替式标签插补框架**：先用隐式关系子集训练模型，再交替插补显式关系对的隐式标签并联合训练
3. **Manifold Mixup 正则化**：在特征空间做 Mixup 防止模型对自身插补标签的确认偏差
4. **显著 SOTA 提升**：在 VG 上 mR@K 多个设置 +4∼6% 绝对提升，零样本设置也有改进

## 问题设置

SGG 任务定义为：给定图像 I，预测场景图 S = (E, R)，其中 E 为检测到的物体集合（含边界框和类别），R 为关系三元组集合 (s, p, o)。标准 SGG pipeline 分解为：
- P(S|I) = P(B|I) · P(Y|B,I) · P(R|B,Y,I)

关键问题：Visual Genome 数据集每对 subject-object 只标注一个 positive 关系标签，但许多物体对同时拥有显式（spatial）和隐式（semantic）关系（如 "man on beach" vs. "man standing on beach"）。由于标注者偏好，许多有价值的隐式关系被遗漏。

## 方法

### 3.1 关系分类：显式 vs. 隐式

将 Visual Genome 的 50 个关系分为：
- **Explicit（显式，13 个）**：above, across, against, along, at, behind, between, in, in front of, near, on, over, under
- **Implicit（隐式，37 个）**：其余关系，如 carrying, eating, holding, riding, sitting on, walking on 等

显式关系可从空间坐标轻松推断；隐式关系需要复杂的视觉-文本推理。

### 3.2 两阶段训练框架

**阶段一：隐式关系预训练**
- 仅用标注了隐式关系的样本训练关系分类器 f_θ，使用标准交叉熵损失 L_CE
- 直观理解：隐式预训练鼓励模型关注语义推理而非空间捷径

**阶段二：交替式标签插补与训练**
对每个 minibatch：
1. **标签插补（Label Imputation）**：对仅标注显式关系的样本 (s,o)，用当前模型 f_θ 的隐式分类 head 预测最高分隐式标签 p̄，并与原始显式标签 p 平均得到软标签 p̂ = (p + p̄) / 2
2. **损失计算**：
   - 隐式关系样本：交叉熵 L_CE(f_θ(x), p)
   - 显式关系样本（含插补标签）：KL 散度 L_KL(f_θ(x), p̂)
3. **Manifold Mixup 正则化**：在特征空间随机混合样本 (x, x') 及其标签 (p, p')：x̃ = λx + (1-λ)x', p̃ = λp + (1-λ)p'，λ ∼ Beta(α,α)
4. **联合更新**：用 Eq.(2) 的总损失更新 θ

### 关键设计选择

- **为什么用 KL 散度而非 CE**：插补标签 p̂ 是软标签（含显式和隐式各 0.5 概率），KL 散度鼓励模型预测高熵、平滑的输出，减少过拟合
- **为什么需要 Mixup**：防止确认偏差（confirmation bias）——模型过度相信自身错误插补
- **为什么先单独训练隐式关系**：让模型先学会对隐式关系产生自信预测，后续插补时不会被显式关系"干扰"

## 实验设置

### 数据集
- **Visual Genome (VG)**：108K 图像，150 个物体类别，50 个关系类别
- 划分遵循 [56] 标准协议

### 评估设置
- **PredCls（谓词分类）**：给定 GT 物体框和类别，预测关系
- **SGCls（场景图分类）**：给定 GT 物体框，预测物体类别和关系
- **SGDet（场景图检测）**：完全端到端，预测物体框、类别和关系
- **指标**：mean Recall@K（mR@20/50/100），每个关系类别独立计算 Recall 后平均
- **零样本**：zsR@K 评估未见过的三元组

### Baselines & Backbones
- **IMP** [56]：视觉-only 模型
- **Motifs** [65]：含 BiLSTM 全局上下文
- **VCTree** [50]：二叉树结构上下文
- **VCTree-EBM** [47]：能量损失
- **VCTree-TDE / Motif-TDE-Sum** [49]：反事实推理

### 实现细节
- **检测器**：预训练 Faster R-CNN + ResNeXt-101-FPN，mAP@0.5IoU = 28%
- **优化器**：SGD，batch size=12，lr=10^{-2}，momentum=0.9
- **阶段一**：30,000 次迭代（仅隐式关系）
- **阶段二**：20,000 次迭代（全部标签 + 插补标签 + Mixup）
- **Mixup α**：4

## 实验结果

### 主表：Scene Graph Generation Performance (mR@K)

| 模型 | 方法 | PredCls mR@20/50/100 | SGCls mR@20/50/100 | SGDet mR@20/50/100 |
|------|------|---------------------|---------------------|---------------------|
| **IMP** | Baseline | 8.9 / 11.0 / 11.8 | 5.4 / 6.4 / 6.7 | 2.2 / 3.3 / 4.1 |
| | **Ours** | **12.3 / 14.6 / 15.3** | **7.1 / 8.0 / 8.3** | **6.9 / 7.8 / 8.1** |
| **Motif-TDE-Sum** | Baseline | 17.9 / 24.8 / 28.7 | 9.8 / 13.2 / 15.1 | 6.6 / 8.9 / 11.0 |
| | **Ours** | **21.3 / 27.1 / 29.7** | **11.3 / 14.3 / 15.7** | **8.4 / 10.4 / 11.8** |
| **VCTree** | Baseline | 13.1 / 16.5 / 17.8 | 8.5 / 10.5 / 11.2 | 5.3 / 7.2 / 8.4 |
| | **Ours** | **18.0 / 21.7 / 23.1** | **11.9 / 14.1 / 15.2** | **7.1 / 8.2 / 8.7** |
| **VCTree-EBM** | Baseline | 14.2 / 18.2 / 19.7 | 10.4 / 12.5 / 13.4 | 5.7 / 7.7 / 9.1 |
| | **Ours** | **21.0 / 24.9 / 26.5** | **14.0 / 16.2 / 17.1** | **7.8 / 10.1 / 11.8** |
| **VCTree-TDE** | Baseline | 16.3 / 22.9 / 26.3 | 11.9 / 15.8 / 18.0 | 6.6 / 9.0 / 10.8 |
| | **Ours** | **22.2 / 28.1 / 30.6** | **17.8 / 22.0 / 23.6** | **8.4 / 10.3 / 11.5** |

**关键解读**：
- VCTree-TDE + Ours 在 PredCls mR@20 上绝对提升 **+5.9**（16.3→22.2）
- VCTree-EBM + Ours 在 PredCls mR@20 上绝对提升 **+6.8**（14.2→21.0）
- IMP + Ours 在 SGDet mR@20 上绝对提升 **+4.7**（2.2→6.9），显示即使视觉-only 模型也从标签插补中获益

### 零样本召回率 (zsR@K)

| 模型 | 方法 | PredCls zsR@20/50 | SGCls zsR@20/50 | SGDet zsR@20/50 |
|------|------|------------------|------------------|------------------|
| Motif-TDE-Sum | Baseline | 8.28 / 14.31 | 1.91 / 2.95 | 1.54 / 2.33 |
| | **Ours** | **9.33 / 14.43** | **1.87 / 2.99** | **2.06 / 3.05** |
| VCTree-TDE | Baseline | 8.98 / 14.52 | 3.16 / 4.97 | 1.47 / 2.3 |
| | **Ours** | **9.11 / 13.52** | **4.26 / 6.20** | **2.24 / 3.25** |

### 消融实验

**Table 3：标签插补策略对比（Motif-TDE-Sum, PredCls mR@20/50）**

| 训练标签 | 插补方式 | 插补目标 | mR@20/50 |
|----------|---------|---------|----------|
| All | - | - | 17.85 / 24.75 |
| Explicit | - | - | 14.06 / 20.34 |
| Random | - | - | 16.99 / 23.33 |
| Implicit | - | - | 18.24 / 24.93 |
| **Implicit + Ours** | Top1-Implicit | Explicit | **21.26 / 27.14** |

**Table 4：各组件贡献（Motif-TDE-Sum, PredCls mR@20/50）**

| Mixup | 标签类型 | 标签精炼 | mR@20/50 |
|-------|---------|---------|----------|
| ✗ | ✗ | ✗ | 17.85 / 24.75 (Baseline) |
| ✓ | ✗ | ✗ | 17.43 / 24.20 |
| ✗ | Hard | ✗ | 18.26 / 24.23 |
| ✓ | ✗ | ✓ | 18.90 / 25.32 |
| ✗ | Hard | ✓ | 20.81 / 26.78 |
| ✓ | Hard | ✗ | 19.90 / 26.35 |
| ✓ | Soft | ✓ | 20.76 / 27.10 |
| ✓ | Hard | ✓ | **21.26 / 27.14** |

**关键消融发现**：
- Mixup 单独在 baseline 上无增益（17.85→17.43），但配合插补有显著增益
- 仅标签精炼（无 Mixup）已提升至 20.81/26.78
- 全部组件 + Hard imputation 最佳

**Table 5：显式/隐式关系分别评估（Motif-TDE-Sum, PredCls mR@50/100）**

| 训练数据 \ 测试 | Explicit mR@50/100 | Implicit mR@50/100 |
|---------------|-------------------|-------------------|
| All Relations | 24.47 / 28.79 | 24.96 / 28.74 |
| Explicit only | 22.89 / 25.34 | **0.08 / 0.09** |
| Implicit only | 20.10 / 22.89 | 24.34 / 26.03 |
| **Ours (final)** | **24.83 / 27.80** | **27.99 / 30.38** |

**关键发现**：仅用显式关系训练 → 隐式测试上 Recall 几乎为零（0.08%）！显式关系不传递有意义的语义信息。而仅用隐式关系训练 → 隐式测试 24.34% + 显式测试 20.10%，具备强泛化能力。

## 局限性

1. **样本量少的类别表现有限**：对训练样本极少的关系，插补质量不可靠
2. **依赖预定义隐式/显式划分**：50 个关系的分类标准基于 [10] 的启发式，可能不是最优划分
3. **VG 的已知偏差**：基准数据集本身存在标注偏差，框架无法完全消除
4. **计算开销**：两阶段训练 + 交替插补比标准训练成本更高

## 可复用 Claim

> **Claim 1**: 隐式（语义性）关系信息量显著高于显式（空间性）关系；仅用隐式关系训练的模型可泛化到显式关系（仅降 2%），反之则几乎完全失效（隐式 Recall 降至 0.08%）。
> **Evidence**: Table 5, PredCls mR@50: Explicit-only on Implicit test = 0.08% vs. Implicit-only on Explicit test = 20.10%
> **Confidence**: high

> **Claim 2**: 为显式关系样本插补缺失隐式标签 + 联合训练（含 Mixup 正则化）可在多种 SGG backbone 上获得一致提升，PredCls mR@20 提升幅度达 +4.7∼+6.8。
> **Evidence**: Table 1, 全部 5 种 backbone 均提升
> **Confidence**: high

> **Claim 3**: Manifold Mixup 仅在配合标签插补时有效（mR@20: 17.85→17.43 w/o imputation vs. 19.90→21.26 w/ imputation），单独使用无增益。
> **Evidence**: Table 4, row 2 vs. row 7
> **Confidence**: high

> **Claim 4**: 采用硬标签（hard imputation, one-hot）略优于软标签（soft imputation, probability vector）——mR@50: 27.14 vs. 27.10。
> **Evidence**: Table 4, row 7 vs. row 8
> **Confidence**: medium（差距极小）

## 关联

- **TDE [49]**：本文方法可正交结合 TDE 反事实推理（VCTree-TDE + Ours 为最优组合），说明标签插补补充数据信息，TDE 去除推理偏差，二者互补
- **EBM [47]**：同样正交结合，VCTree-EBM + Ours 提升显著
- **Wang et al. [54]**：最接近的方法，但本文仅插补隐式标签而非全部标签，更高效且效果更好
- **Collell et al. [10]**：启发本文的显式/隐式关系划分来源
- **Manifold Mixup [53]**：本文使用的正则化策略，原始提出用于半监督学习

## 开放问题

1. 隐式/显式关系划分的最优方式是什么？是否可自适应学习而非固定划分？
2. 如何将标签信息量概念扩展到更多关系（如 Visual Genome 未覆盖的细粒度关系）？
3. 本文方法在更大规模 SGG 数据集（如 GQA、OpenImages）上的表现？
4. 标签插补质量的下限是多少？何时插补会造成负面影响？
5. 是否可以将标签信息量度量引入主动学习，优先标注信息量最大的样本？

## 来源追溯

- 提取文本：`raw/sources/2022-06-20-not-all-relations-are-equal-mining-informative-labels-for-sgg.txt`（16 页，67K 字符）
- 原始 PDF：`raw/sources/2022-06-20-not-all-relations-are-equal-mining-informative-labels-for-sgg.pdf`（arXiv 下载，2.5 MB）
- 代码和项目页：https://groups.inf.ed.ac.uk/vico/research/NARE
