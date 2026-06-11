---
title: "Scene Graph Prediction with Limited Labels"
type: paper
domain: scene-graph
status: active
created: 2026-06-10
updated: 2026-06-10
tags:
  - scene-graph-generation
  - few-shot
  - semi-supervised-learning
  - visual-relationship-detection
  - generative-model
  - data-programming
  - ICCV-2019
raw_sources:
  - ../../../raw/sources/2019-ICCV-scene-graph-prediction-with-limited-labels.pdf
  - ../../../raw/sources/2019-ICCV-scene-graph-prediction-with-limited-labels.txt
related_pages:
  - neural-motifs-scene-graph-global-context.md
  - visual-relationship-detection-with-language-priors.md
evidence_level: full-paper
paper:
  title: "Scene Graph Prediction with Limited Labels"
  abbreviated: "Semi-supervised SGG"
  authors:
    - Vincent S. Chen
    - Paroma Varma
    - Ranjay Krishna
    - Michael Bernstein
    - Christopher Ré
    - Li Fei-Fei
  affiliations:
    - Stanford University
  year: 2019
  venue: ICCV 2019
  doi: null
  arxiv: null
  url: "https://openaccess.thecvf.com/content_ICCV_2019/papers/Chen_Scene_Graph_Prediction_With_Limited_Labels_ICCV_2019_paper.pdf"
  code: null
classification:
  label: "Scene Graph Prediction with Limited Labels"
  task:
    - Scene Graph Generation (SGG)
    - Visual Relationship Detection (VRD)
    - Semi-supervised Visual Relationship Annotation
  method_family: Semi-supervised Generative Model with Image-agnostic Heuristics
  modality: Image
  datasets:
    - Visual Genome (108K images)
    - VRD (Visual Relationship Detection)
  metrics:
    - Recall@20/50/100 (PREDCLS, SGCLS, SGDET)
    - Precision / Recall / F1 (VRD labeling)
    - Accuracy
---

## Citation

Chen, V. S., Varma, P., Krishna, R., Bernstein, M., Ré, C., & Fei-Fei, L. (2019). Scene Graph Prediction with Limited Labels. *ICCV 2019*.

## One-Sentence Contribution

首次提出一个半监督方法，利用 image-agnostic features（类别和空间特征）和因子图生成式模型，从极少标注样本（n=10）自动生成概率关系标签来训练场景图模型，在 PREDCLS 任务上超出 transfer learning baseline 5.16 recall@100。

## Problem Setting

- **背景**：Visual Genome 等视觉知识库中存在大量稀疏、不完整的关系标注——超过 98% 的关系类别没有足够的标签实例。现有 SGG 模型只能训练在有数千标签的几十种关系上。
- **挑战**：人工标注昂贵，且文本知识库补全方法（基于句法/词汇模式）不适用于视觉关系（视觉关系依赖于图像具体内容，是 image-dependent 的）。
- **设定**：每个关系只给 n=10 个标注样本，大量未标注图像可用。目标是自动为未标注图像生成高质量关系标签，并训练下游场景图模型。

## Method

### 整体框架

![Figure 1] 半监督方法：有限标签 + 未标注图像 → 生成式模型 → 概率训练标签 → 训练下游 SGG 模型。

### 1. Image-agnostic Features（图像无关特征）

定义两类不从像素值推导的特征：

- **Categorical features**：关系涉及的对象类别及其共现信息，例如 "eat" 常涉及较小物体被消耗，"look" 常涉及 phone/laptop/window。
- **Spatial features**：目标对的相对空间位置，例如 "above"/"below"/"ride" 涉及垂直位置和尺寸比例关系。

### 2. Heuristic Functions（启发函数）

在 image-agnostic features 上学习简单的规则（决策树等），每个启发函数对未标注数据输出关系标签的噪声预测。

### 3. Generative Model（生成式模型）

用因子图（factor graph）对启发函数输出进行聚合：

- 对每个启发函数学习权重参数，反映其精度
- 通过最大化观测到的启发函数输出的边际似然来估计参数
- 为每个对象对 (o, o') 计算概率标签 πφ(Y | Λ(o, o'))

### 4. Noise-aware Loss（噪声感知损失函数）

将概率标签用于训练场景图模型，修改交叉熵损失为噪声感知经验风险最小化：

```
Lθ = E_{Y∼π}[log(1 + exp(-θ^T V^T Y))]
```

其中 θ 为学习参数，π 为生成模型输出的分布，Y 为真实标签，V 为 SGG 模型提取的特征。

## Experiments

### 数据集

- **VRD**：小规模但完全标注的数据集，用于评估标注生成质量（Section 5.1）
- **Visual Genome**：108K 图像的大规模视觉知识库，标注不完整，用于评估下游 SGG 模型性能（Section 5.2）

### 关系预处理

将同义词合并、超集消除，最终保留 20 个 unique predicates（原 50 个常用 predicate 存在同义词/超集问题）。

### Baseline 方法

- **ORACLE**：用全部 Visual Genome 数据训练（108× 更多标注数据），作为上界
- **BASELINE [n=10]**：只使用 n=10 个标注样本训练
- **FREQ**：基于对象计数的频率基线
- **FREQ+OVERLAP**：增加 bbox 重叠的频率基线
- **TRANSFER LEARNING**：predict task: 用高频关系 pretrain + n=10 样本 finetune
- **DECISION TREE**：基于 image-agnostic features 的单个决策树
- **LABEL PROPAGATION**：标签传播半监督方法

### 消融实验变体

- **OURS (DEEP)**：仅使用 ResNet50 deep features
- **OURS (SPAT.)**：仅使用 spatial features
- **OURS (CATEG.)**：仅使用 categorical features
- **OURS (CATEG. + SPAT. + DEEP)**：三者结合
- **OURS (CATEG. + SPAT. + WORDVEC)**：categorical + spatial + word vectors
- **OURS (MAJORITY VOTE)**：categorical + spatial 特征但用简单多数投票替代生成模型
- **OURS (CATEG. + SPAT.)**：本文最佳完整方法

### 评估任务

三个标准 SGG 评估模式（按难度递减）：
1. **SGDET** (Scene Graph Detection)：输入图像 → 预测 bbox + 物体类别 + 关系
2. **SGCLS** (Scene Graph Classification)：输入 GT bbox → 预测物体类别 + 关系
3. **PREDCLS** (Predicate Classification)：输入 GT bbox + GT 物体类别 → 预测关系

## Results

### Table 1: VRD 标注生成质量（n=10）

| Model | Prec. | Recall | F1 | Acc. |
|---|---|---|---|---|
| RANDOM | 5.00 | 5.00 | 5.00 | 5.00 |
| DECISION TREE | 46.79 | 35.32 | 40.25 | 36.92 |
| LABEL PROPAGATION | 76.48 | 32.71 | 45.82 | 12.85 |
| OURS (MAJORITY VOTE) | 55.01 | 57.26 | 56.11 | 40.04 |
| **OURS (CATEG. + SPAT.)** | **54.83** | **60.79** | **57.66** | **50.31** |

- OURS (CATEG. + SPAT.) 在 F1 上超过 LABEL PROPAGATION 17.41 点、DECISION TREE 13.88 点、MAJORITY VOTE 1.55 点

### Table 2: Visual Genome SGG 任务结果（n=10 per predicate）

| Model | SGDET R@20/50/100 | SGCLS R@20/50/100 | PREDCLS R@20/50/100 |
|---|---|---|---|
| BASELINE [n=10] | 0.00/0.00/0.00 | 0.04/0.04/0.04 | 3.17/5.30/6.61 |
| FREQ | 9.01/11.01/11.64 | 11.10/11.08/10.92 | 20.98/20.98/20.80 |
| FREQ+OVERLAP | 10.16/10.84/10.86 | 9.90/9.91/9.91 | 20.39/20.90/22.21 |
| TRANSFER LEARNING | 11.99/14.40/16.48 | 17.10/17.91/18.16 | 39.69/41.65/42.37 |
| DECISION TREE | 11.11/12.58/13.23 | 14.02/14.51/14.57 | 31.75/33.02/33.35 |
| LABEL PROPAGATION | 6.48/6.74/6.83 | 9.67/9.91/9.97 | 24.28/25.17/25.41 |
| OURS (DEEP) | 2.97/3.20/3.33 | 10.44/10.77/10.84 | 23.16/23.93/24.17 |
| OURS (SPAT.) | 3.26/3.20/2.91 | 10.98/11.28/11.37 | 26.23/27.10/27.26 |
| OURS (CATEG.) | 7.57/7.92/8.04 | 20.83/21.44/21.57 | 43.49/44.93/45.50 |
| OURS (CATEG.+SPAT.+DEEP) | 7.33/7.70/7.79 | 17.03/17.35/17.39 | 38.90/39.87/40.02 |
| OURS (CATEG.+SPAT.+WORDVEC) | 8.43/9.04/9.27 | 20.39/20.90/21.21 | 45.15/46.82/47.32 |
| OURS (MAJORITY VOTE) | 16.86/18.31/18.57 | 18.96/19.57/19.66 | 44.18/45.99/46.63 |
| **OURS (CATEG. + SPAT.)** | **17.67/18.69/19.28** | **20.91/21.34/21.44** | **45.49/47.04/47.53** |
| ORACLE [108× more data] | 24.42/29.67/30.15 | 30.15/30.89/31.09 | 69.23/71.40/72.15 |

**关键发现：**
- OURS (CATEG. + SPAT.) 在 PREDCLS R@100 上以 47.53 超过 TRANSFER LEARNING (42.37)，提升 5.16 点
- 在 SGDET R@100 上达到 ORACLE 的 19.28 vs 30.15，差距 8.65 点（ORACLE 用了 108× 更多标注数据）
- 超过 DECISION TREE 和 LABEL PROPAGATION 分别 13.83 和 22.12 PREDCLS R@100

### 标注数量影响
- 标注样本越少（n=10），OURS 相对 TRANSFER LEARNING 优势越大
- 未标注样本越多，OURS 性能越接近 ORACLE

### 消融分析
- **CATEG. + SPAT. + DEEP 组合伤害性能**：比 OURS (CATEG. + SPAT.) 低 7.51 PREDCLS R@100，原因是 deep features 过拟合
- **CATEG. features 最关键**：单独 CATEG. 达 45.50 PREDCLS R@100，而 SPAT. 仅 27.26
- **生成模型 > 多数投票**：生成模型比简单多数投票高出 0.71 SGDET R@100

### 关系复杂度指标
- 提出 spatial + categorical subtypes 定义复杂度，指标与 OURS 超出 transfer learning 程度的相关性 R²=0.778
- 当关系较多 subtypes（高复杂度）时，OURS 显著优于 TRANSFER LEARNING
- 为关系复杂度与半监督方法适用性之间提供了量化分析

## Limitations

1. **Image-agnostic features 表达能力有限**：对于需要图像内容细粒度理解的关系（如复杂的动作关系），image-agnostic features 不足以区分
2. **同义词和超集问题**：方法无法区分同义 predicate（如 laying on vs. lying on）和超集（如 above 是 riding 的超集），需要人工预处理合并
3. **Deep features 反而有害**：加入 ResNet50 deep features 会降低性能（过拟合），方法依赖于手工设计的 image-agnostic features
4. **分类数有限**：评估仅覆盖 20 个合并后的 predicates，在原始 50 个 predicates 上的扩展性有待验证
5. **假设对象检测已解决**：方法依赖于 image-agnostic features（物体类别和空间位置），自身不改进对象检测

## Reusable Claims

1. **半监督标注生成可有效解决 SGG 长尾问题**：仅 n=10 即可训练出可用的 SGG 模型，大幅降低标注成本
2. **Categorical features > Spatial features > Deep features**：在少标注场景下，类别特征是预测关系的最强信号，加入 deep features 反而有害
3. **生成式模型聚合优于多数投票**：因子图生成模型通过学习启发函数权重，比简单多数投票聚合更优
4. **关系复杂度可作为方法选择指南**：关系复杂度（subtypes 数量）与半监督方法相对 transfer learning 的优势高度相关（R²=0.778），预测了何时半监督优于迁移学习
5. **噪声感知损失有效**：修改标准交叉熵损失以接受概率标签对半监督训练有效

## Connections

- 与 [[neural-motifs-scene-graph-global-context.md]] 关联：本文使用 Neural Motifs [Zellers et al., 2017] 作为下游 SGG 模型的 backbone
- 与 [[visual-relationship-detection-with-language-priors.md]] 关联：同为处理少标注关系检测问题，本文侧重半监督而非语言先验
- 数据编程方法（Data Programming）由 Ratner et al. [2016] 提出，本文将其引入视觉关系领域
- 后续相关工作：弱监督 SGG（如 [[linguistic-structures-weak-supervision-visual-scene-graph-generation.md]]）在类似方向推进

## Open Questions

1. 如何将 image-specific features（如视觉语义）与 image-agnostic features 结合而不引入过拟合？
2. 对于同义词和超集关系的自动分辨需要额外什么机制？
3. 该方法在更大规模（如完整 50 个 predicates）上的表现如何？
4. 与现代 VLM（如 CLIP）结合的潜力如何？是否能用 VLM 特征做更复杂的 image-agnostic 规则？

## Provenance

- **来源**：ICCV 2019 论文全文精读
- **提取自**：`raw/sources/2019-ICCV-scene-graph-prediction-with-limited-labels.pdf`
- **提取日期**：2026-06-10
- **证据等级**：full-paper
