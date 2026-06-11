---
title: "Unsupervised Vision-Language Parsing: Seamlessly Bridging Visual Scene Graphs with Language Structures via Dependency Relationships"
type: paper
domain: scene-graph
status: active
created: 2026-06-10
updated: 2026-06-10
tags:
  - scene-graph-generation
  - unsupervised
  - CVPR-2022
  - vision-language-parsing
  - dependency-parsing
  - contrastive-learning
  - graph-autoencoder
paper:
  title: "Unsupervised Vision-Language Parsing: Seamlessly Bridging Visual Scene Graphs with Language Structures via Dependency Relationships"
  authors:
    - Chao Lou
    - Wenjuan Han
    - Yuhuan Lin
    - Zilong Zheng
  year: 2022
  venue: CVPR 2022
  arxiv: 2203.14260
  code: https://github.com/LouChao98/VLGAE
  project: https://github.com/bigai-research/VLGAE
classification:
  label: VLGAE
  task:
    - vision-language-parsing
    - language-dependency-parsing
    - weakly-supervised-phrase-grounding
  method_family: graph-autoencoder
  modality: vision-language
  datasets:
    - VLParse
    - MSCOCO
    - Visual Genome
  metrics:
    - UDA (Undirected Dependency Accuracy)
    - DDA (Directed Dependency Accuracy)
    - Zero-AA (Zero-Order Alignment Accuracy)
    - First-AA (First-Order Alignment Accuracy)
    - Second-AA (Second-Order Alignment Accuracy)
evidence_level: full-paper
raw_sources:
  - raw/sources/2022-CVPR-Unsupervised-Vision-Language-Parsing.pdf
  - raw/sources/2022-CVPR-Unsupervised-Vision-Language-Parsing.txt
related_pages: []
---

## Citation

> Chao Lou, Wenjuan Han, Yuhuan Lin, Zilong Zheng. "Unsupervised Vision-Language Parsing: Seamlessly Bridging Visual Scene Graphs with Language Structures via Dependency Relationships." *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*, 2022, pp. 15607-15616.

## One-Sentence Contribution

首次形式化定义并解决无监督视觉-语言联合解析任务（VLParse），提出基于对比学习的VLGAE框架，无缝桥接场景图（SG）和语言依存树（DT），并构建半自动化标注数据集。

## Problem Setting

- **输入**：图像 I 及其对应的自然语言描述句子 w（N 个单词）
- **输出**：联合视觉-语言结构（Joint VL Structure），包含视觉场景图（SG）、语言依存树（DT）及两者之间的层次对齐
- **约束**：完全无监督，仅使用图像-描述配对，没有任何 DT、SG 或短语-区域对应标注
- **任务衍生**：由于缺少联合结构标注，通过两个衍生任务评估模型：
  1. **语言依存结构归纳**（Language Structure Induction）
  2. **弱监督短语定位**（Weakly-supervised Visual Phrase Grounding）

## Method

### Joint VL Structure 定义

联合视觉-语言结构由三部分组成：
1. **Scene Graph (SG)**：包含 OBJECT、ATTRIBUTE、RELATIONSHIP 三类节点
2. **Dependency Tree (DT)**：包含父节点、子节点和依存关系，额外添加节点类型标签
3. **层次对齐（Alignment）**：
   - **Zero-order Alignment**：DT 中每个节点 wi 对齐到 SG 中一个节点 vi
   - **First-order Alignment**：DT 中的三元组 (wi, wj, wiÑj) 对齐到 SG 中相似语义的三元组 (vi, vj, viÑj)
   - **Second-order Alignment**：三个节点之间的依存关系对齐

### VLGAE（Vision-Language Graph Autoencoder）

三个核心模块：

**1. Feature Extraction（特征提取）**
- 视觉特征：Faster R-CNN 提取 top-50 目标候选框（RoI-Align + Global Average Pooling），OBJECT 节点特征来自 RoI，ATTRIBUTE 特征通过 MLP(vo_i) 生成，RELATIONSHIP 特征通过随机初始化网络生成
- 语言特征：预训练词嵌入 + 随机初始化的 POS 标签嵌入拼接，依存关系通过 Biaffine Scorer 计算

**2. Structure Construction（结构构建）**
- **Encoder**：通过注意力机制融合文本特征和视觉信息，生成联合上下文编码 c，再经过平均池化得到全局表征 s
- **Decoder**：基于全局表征 s，使用 inside algorithm（O(n³) 动态规划）递归构建 VL 结构，计算所有可能解析树的后验概率 p(pt|s)
- 训练优化：通过 EM 过程最大化条件对数似然 L_mle

**3. Cross-modality Matching（跨模态匹配）**
- 计算每个语言上下文 c 和视觉节点 v 之间的点积相似度 sim(v, c)
- 使用解码器后验概率 p(c|s) 增强匹配分数：sim+(I, c) = sim(I, c) × p(c|s)
- 对比损失（Contrastive Loss）：配对图像作为正例，batch 内其他图像作为负例
- 总损失：L_tot = (1-λ)·L_mle + λ·L_cl

### 推理

- 解析树：在 PT(s) 中搜索条件概率最高的 pt*
- 图像区域定位：使用增强相似度 sim+(v, c) 选择最佳匹配区域

## VLParse Dataset

**数据集构建流程**：
1. 基于 MSCOCO 训练集（82,783 张图像）作为训练数据
2. 从 MSCOCO dev+test 与 Visual Genome 的交集中选取 850 张图像，每张图对应 5 条描述（共 4,250 条描述）
3. **自动规则对齐**（Automatic Rule-based Alignment）：
   - DT Rewriting：类型分类（OBJECT/ATTRIBUTE/RELATIONSHIP）+ 父节点识别（共设计了 52 条规则）
   - DT-SG Alignment：计算 SG 节点与单词父节点的相似度，选择 top-k 作为对齐结果
4. **人工精炼**（Crowd-Sourcing Human Refinement）：通过 AMT 雇佣标注者检查和修正对齐结果，每张图至少 2 个标注者，有分歧时第三方复核

**数据划分**：850 张图像按 1:1 分为 dev 和 test（各 425 张），剩余 dev+test 并入训练集

**数据集规模**：
| | Train | Dev | Test |
|---|---|---|---|
| # Images | 83,933 | 425 | 425 |
| # Sentences | 419,665 | 2,125 | 2,125 |
| Avg. DT Instances | - | 20 | 21 |
| Avg. SG Instances | - | 135 | 134 |

**Human Performance**：5 名标注者测试集准确率 96.15%

## Experiments

### 实验设置

- **目标检测器**：Faster R-CNN（同 MAF [39]），每图 top-50 目标候选框
- **特征提取**：RoI-Align [16] + Global Average Pooling
- **标注替代**：由于缺少真值结构，使用外部解析器生成的预测作为 ground truth（同 [32][52]）
- **报告方式**：3 次不同随机种子的平均分
- **无监督设置**：不提供 DT、SG 或短语-区域对应标注用于训练
- **评估协议**：遵循 Zhao and Titov [51/52] 的数据划分方案
- λ 参数：平衡 L_mle 和 L_cl 的超参数（论文未报告具体数值）

### 实验 1：语言依存结构归纳（Table 2）

**Baselines**：
- Left branch / Right branch / Random（随机策略）
- DMV [26]：Dependency Model with Valence
- D-NDMV [15]：Discriminative Neural Dependency Model with Valence

**Metric：UDA (Undirected Dependency Accuracy) / DDA (Directed Dependency Accuracy)**

| Method | UDA | DDA |
|--------|-----|-----|
| Left branch | 53.61 | 30.75 |
| Right branch | 53.19 | 23.01 |
| Random | 32.44 | 19.29 |
| DMV | 58.06 | 41.36 |
| D-NDMV | 70.77 | 65.88 |
| **VLGAE (ours)** | **71.43** | **67.57** |

**Key findings**：
- VLGAE 在 DDA 上超过 D-NDMV 1.69%，在 UDA 上超过 0.66%
- 视觉线索（visual cues）带来了稳定的性能提升
- 与 VC-PCFG 不同，VLGAE 的视觉增强对所有弧长都有正向作用（Figure 4）

### 实验 2：弱监督视觉短语定位（Table 3）

**Baseline**：
- Random（随机定位）
- MAF* [39]：Multimodal Alignment Framework（论文重新实现版本）

**Metrics**：Zero-AA（Zero-order Alignment Accuracy）、First-AA、Second-AA

| Method | All | Obj. | Attr. | Rel. | First | Second |
|--------|-----|------|-------|------|-------|--------|
| Random | 12.2 | 15.9 | 9.4 | 0.0 | 0.0 | 0.0 |
| MAF* | 27.7 | 38.5 | 20.7 | 0.1 | 0.0 | 0.0 |
| **VLGAE** | **28.7** | 36.1 | **21.0** | **10.2** | **3.4** | **0.2** |
| VLGAE: (gold SG) | 42.3 | 67.2 | 41.8 | 15.9 | - | - |

\* 为重新实现的结果；: 使用 gold scene graph（真值场景图）

**Key findings**：
- VLGAE Zero-AA 整体准确率 28.7%，超过 MAF (27.7%) 1.0%
- 在 RELATIONSHIP 节点定位上大幅领先（10.2% vs. 0.1%），说明多阶对齐有效
- 高阶关系（First-AA, Second-AA）仍然非常低（3.4%, 0.2%），说明长程跨模态对齐是开放挑战
- 使用真值 SG 时性能大幅提升至 42.3%，表明检测器质量是关键瓶颈

### 消融实验：弧长分析（Figure 4）

- 对比 D-NDMV 和 VLGAE 在不同弧长（arc length）上的 DDA
- VLGAE 在短弧和长弧上均优于 D-NDMV
- 这与 VC-PCFG 的发现相反：VC-PCFG 的视觉增强对短弧有效但长弧无效
- 说明 VLGAE 的依存结构对所有弧长都有益

## Results

- **Language Structure Induction**：VLGAE DDA 67.57%，UDA 71.43%，超越无监督依存解析 SOTA D-NDMV（DDA 65.88%，UDA 70.77%）
- **Visual Phrase Grounding**：VLGAE Zero-AA 28.7%，超越 MAF（27.7%）
- **Human performance**：标注准确率 96.15%（对齐任务）

## Limitations

1. **Overall performance still low**：语言结构 DDA 仅 67.57%，短语定位 Zero-AA 仅 28.7%，距离实际应用差距显著
2. **Heavy reliance on pre-trained detector**：使用 Faster R-CNN 生成目标候选框，检测质量直接影响后续对齐效果（真值 SG 时 Zero-AA 从 28.7% 提升至 42.3%）
3. **High-order alignment challenging**：First-AA 仅 3.4%，Second-AA 仅 0.2%，高阶跨模态关系几乎无法学到
4. **No joint structure evaluation**：由于缺少联合 VL 结构的标注，只能通过两个衍生任务间接评估
5. **Small annotated dataset**：VLParse 仅 850 张图像标注，虽然构造经济但规模有限

## Reusable Claims

> **Claim**: 视觉线索可以提升无监督语言依存解析的性能。
> **Evidence**: VLGAE DDA 67.57% vs. D-NDMV 65.88%（+1.69%），UDA 71.43% vs. 70.77%（+0.66%）。Section 6.2，Table 2。
> **Scope**: MSCOCO 数据集，VLParse benchmark
> **Confidence**: medium
> **Tensions**: 提升幅度有限（<2%），可能存在统计波动

> **Claim**: 对比学习框架可以同时学习 VL 结构构建和跨模态对齐。
> **Evidence**: VLGAE 在语言结构归纳（Table 2）和视觉短语定位（Table 3）两个任务上同时取得优于 baselines 的性能。
> **Scope**: 无监督/弱监督设置
> **Confidence**: medium

> **Claim**: 自动规则对齐 + 人工精炼的范式可以减少 VL 结构数据集的标注成本。
> **Evidence**: VLParse 仅对 850 张图像进行人工精炼，即可建立包含三个层次对齐关系的 VL 结构数据集。Human performance 96.15%。
> **Scope**: 视觉-语言结构标注
> **Confidence**: high

## Connections

- **VL-Grammar [17]**：最相关工作，同样构建图像和语言的联合结构，但使用 Compound PCFG 且有预定义的 segmentation parts。VLParse 在无监督设置下更具挑战性。
- **VC-PCFG [52]**：视觉增强的语法归纳，但 VLGAE 对所有弧长有效，VC-PCFG 仅对短弧有效。
- **D-NDMV [15]**：无监督依存解析 baseline，VLGAE 通过视觉线索在其基础上提升。
- **MAF [39]**：弱监督短语定位 baseline，VLGAE 使用对比学习和结构后验增强替代纯匹配策略。
- **Related to**: [Linguistic Structures as Weak Supervision for Visual Scene Graph Generation](linguistic-structures-weak-supervision-visual-scene-graph-generation.md)（也利用语言结构作为视觉场景图的弱监督信号）
- **Related to**: [Knowledge Embedded Routing Network](2019-CVPR-knowledge-embedded-routing-network-sgg.md)（场景图生成相关工作）

## Open Questions

- VLGAE 能否扩展到更大的联合结构数据集？
- 如何解决高阶关系对齐的挑战（First-AA 仅 3.4%）？
- 是否可以通过更强的视觉 backbone（如 DETR）替代 Faster R-CNN 来提升基础检测质量？
- 联合 VL 结构是否能直接用于下游任务（如 VQA、captioning）并带来收益？

## Provenance

- **Raw source**: `raw/sources/2022-CVPR-Unsupervised-Vision-Language-Parsing.pdf`（arXiv PDF，8.2MB）
- **Extracted text**: `raw/sources/2022-CVPR-Unsupervised-Vision-Language-Parsing.txt`（51,724 chars，11页）
- **evidence_level**: full-paper（全文精读）
- **分析日期**: 2026-06-10
