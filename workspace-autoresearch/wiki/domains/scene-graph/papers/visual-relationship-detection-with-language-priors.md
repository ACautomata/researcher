---
title: Visual Relationship Detection with Language Priors
type: paper
domain: scene-graph
status: active
created: 2026-06-10
updated: 2026-06-10
tags: scene-graph-generation, language-priors, ECCV-2016, foundational, visual-relationship-detection, zero-shot
source_pages: []
raw_sources:
  - raw/sources/2016-07-31-visual-relationship-detection-with-language-priors.pdf
  - raw/sources/2016-07-31-visual-relationship-detection-with-language-priors.txt
related_pages:
  - domains/scene-graph/papers/neural-motifs-scene-graph-global-context.md
  - domains/scene-graph/papers/vctree-learning-to-compose-dynamic-tree-structures.md
  - domains/scene-graph/papers/graphical-contrastive-losses-for-scene-graph-parsing.md
paper:
  title: "Visual Relationship Detection with Language Priors"
  authors:
    - Cewu Lu
    - Ranjay Krishna
    - Michael Bernstein
    - Li Fei-Fei
  year: 2016
  venue: ECCV 2016 (Oral)
  arxiv: "1608.00187"
  doi: null
  code: null
  project: null
classification:
  label: scene-graph-generation, language-priors
  task:
    - Visual Relationship Detection
    - Scene Graph Generation
    - Zero-shot Relationship Detection
    - Content-based Image Retrieval
  method_family: Language-Prior Fusion
  modality: Image
  datasets:
    - VRD (Visual Relationship Detection Dataset, 5,000 images)
    - Visual Phrases Dataset (2,769 images, 12 phrases)
  metrics:
    - Recall @ 100
    - Recall @ 50
    - mAP
evidence_level: full-paper
---

## Citation

Cewu Lu, Ranjay Krishna, Michael Bernstein, Li Fei-Fei. "Visual Relationship Detection with Language Priors." ECCV 2016 (Oral). arXiv:1608.00187.

## One-Sentence Contribution

提出分离式建模对象和谓词外观 + 语言先验（word2vec 语义投影）的方法，使得从少量样本即可检测数千种视觉关系，并支持零样本关系检测。

## Problem Setting

给定一张图像，目标是检测其中的视觉关系 ⟨object1 - predicate - object2⟩，同时将两个对象分别定位为 bounding box。核心挑战在于关系组合空间巨大（O(N²K) 种可能的 ⟨o1-p-o2⟩），且大部分关系在训练集中出现频率极低。论文将问题分解为三个子任务：
1. **Predicate Detection** — 已知对象类别和位置，预测谓词
2. **Phrase Detection** — 将整个关系作为一个区域定位并标注
3. **Relationship Detection** — 检测两个对象并同时预测其关系

## Method

### 总体框架

使用 RCNN [43] 生成对象 proposal，两种模块联合评分：

**Visual Appearance Module (V)**：对每个对象训练 VGG net（N=100 类），对每对对象的 union box 训练谓词分类 CNN（K=70 类）。关系评分公式：
```
V(R⟨i,k,j⟩, Θ|⟨O₁, O₂⟩) = Pᵢ(O₁)(zₖᵀ CNN(O₁, O₂) + sₖ)Pⱼ(O₂)
```
其中 zₖ、sₖ 为学习参数，将 CNN 特征转换为关系似然。

**Language Module (f)**：利用 word2vec 学习的关系语义投影函数：
```
f(R⟨i,k,j⟩, W) = wₖᵀ [word2vec(tᵢ), word2vec(tⱼ)] + bₖ
```
其中 wₖ、bₖ 为谓词 k 的投影参数，将对象词向量拼接后投影到关系空间。

### 训练目标

联合优化三个损失：
1. **Ranking Loss C(Θ, W)** — 最大化正确关系的 V×f 得分
2. **Likelihood Prior L(W)** — 训练集频率高的关系获得更高 f() 得分（rank loss）
3. **Distance Regularizer K(W)** — 语义相似的关系在嵌入空间中距离更近（variance minimization）

最终目标函数：
```
min{Θ,W} C(Θ, W) + λ₁L(W) + λ₂K(W)     λ₁=0.05, λ₂=0.002
```

使用随机梯度下降迭代优化，约 20-25 轮收敛。

### 测试

对所有 RCNN proposal 对，选择 V(R)f(R) 得分最高的关系作为检测结果：
```
R* = arg max_R V(R, Θ|⟨O₁, O₂⟩)f(R, W)
```

## Experiments

### 数据集

**VRD Dataset**（论文自建）
- 5,000 张图像，100 个对象类别，70 个谓词
- 37,993 个关系实例，6,672 种关系类型
- 平均每个对象类别有 24.25 个谓词
- 训练/测试：4,000 / 1,000 张图像
- 测试集中有 1,877 种未在训练集中出现的关系（用于零样本评估）

**Visual Phrases Dataset**
- 2,769 张图像，12 个可用的 ⟨o1-p-o2⟩ 短语
- 用于跨数据集验证

### Baseline 方法

- **Visual Phrases [6]**：为每种关系单独训练 DPM 检测器
- **Joint CNN [44]**：联合训练 270 路分类（100+100+70），共同预测对象和谓词
- **Ours - V only**：仅视觉外观模块
- **Ours - L only**：仅语言先验模块
- **Ours - V + naive FC**：用训练集频率替代语义投影函数 f()
- **Ours - V + L only**：视觉 + 语言似然（无语义距离正则化）
- **Ours - V + L + Reg.**：加入 L2 正则化
- **Ours - V + L + K（Full Model）**：完整模型

### 训练设置

- Backbone: VGG net [44]
- Object detector: RCNN [43]
- 超参数 λ₁=0.05, λ₂=0.002（grid search on validation set）
- 优化器：SGD，20-25 轮收敛
- word2vec [7]: 300 维预训练词向量

### 评估协议

- **Recall @ 100 / Recall @ 50**：Top-x 置信度预测中正确关系的比例
- **mAP**：补充报告（因非穷尽标注，mAP 偏悲观）

## Results

### 主要结果：Visual Relationship Detection（VRD 数据集）

| 模型 | Phrase R@100 | Phrase R@50 | Rel R@100 | Rel R@50 | Pred R@100 | Pred R@50 |
|------|-------------|-------------|-----------|---------|------------|----------|
| Visual Phrases [6] | 0.07 | 0.04 | — | — | 1.91 | 0.97 |
| Joint CNN [44] | 0.09 | 0.07 | 0.09 | 0.07 | 2.03 | 1.47 |
| Ours - V only | 2.61 | 2.24 | 1.85 | 1.58 | 7.11 | 7.11 |
| Ours - L only | 0.08 | 0.08 | 0.08 | 0.08 | 18.22 | 18.22 |
| Ours - V + naive FC | 6.39 | 6.65 | 5.47 | 5.27 | 28.87 | 28.87 |
| Ours - V + L only | 8.59 | 9.13 | 9.18 | 9.04 | 35.20 | 35.20 |
| Ours - V + L + Reg. | 8.91 | 9.60 | 9.63 | 9.71 | 36.31 | 36.31 |
| **Ours - V + L + K** | **17.03** | **16.17** | **14.70** | **13.86** | **47.87** | **47.87** |

关键发现：
- Full model 的 Phrase Det R@100（17.03）是 V+L only（8.59）的约 2 倍，证明语义距离正则化 K() 对性能有质的提升
- Visual Phrases 和 Joint CNN 因训练数据稀疏性，在 6,672 种关系上几乎失效
- Predicate Detection 约 47.87 R@100，而 Relationship Detection 仅 13.86，说明**对象检测误差的级联放大**是主要瓶颈

### 零样本关系检测

| 模型 | Phrase R@100 | Phrase R@50 | Rel R@100 | Rel R@50 | Pred R@100 | Pred R@50 |
|------|-------------|-------------|-----------|---------|------------|----------|
| Ours - V only | 1.12 | 0.95 | 0.78 | 0.67 | 3.52 | 3.52 |
| Ours - L only | 0.01 | 0.00 | 0.01 | 0.00 | 5.09 | 5.09 |
| Ours - V + L only | 2.56 | 2.43 | 2.66 | 2.27 | 6.11 | 6.11 |
| **Ours - V + L + K** | **3.75** | **3.36** | **3.52** | **3.13** | **8.45** | **8.45** |

关键发现：K() 的引入带来约 30% 的提升，说明利用语义相似关系可有效推断零样本关系。

### Visual Phrases 数据集结果

| 模型 | Phrase mAP | Phrase R@100 | Phrase R@50 |
|------|-----------|-------------|-------------|
| Visual Phrase [6] | 38.0 | 52.7 | 49.3 |
| Joint CNN | 54.1 | 75.3 | 71.5 |
| Ours - V + L + K | **59.2** | **82.7** | **78.1** |

零样本（remove "person lying on sofa" 和 "person lying on beach"）：

| 模型 | Zero-shot mAP | Zero-shot R@100 | Zero-shot R@50 |
|------|--------------|----------------|----------------|
| Ours - V + L + K | **18.5** | **11.4** | **23.9** |

### 图像检索结果

| 方法 | R@1 | R@5 | R@10 | Median Rank |
|------|-----|-----|------|-------------|
| GIST [46] | 0.00 | 5.60 | 8.70 | 68 |
| SIFT [47] | 0.70 | 6.10 | 10.3 | 54 |
| CNN [44] | 3.15 | 7.70 | 11.5 | 20 |
| Visual Phrases [6] | 8.72 | 18.12 | 28.04 | 12 |
| **Ours** | **10.82** | **30.02** | **47.00** | **4** |

### mAP 补充结果

| 模型 | Phrase mAP | Rel mAP | Pred mAP |
|------|-----------|---------|----------|
| Visual Phrases | 0.03 | — | 0.71 |
| Joint CNN | 0.05 | 0.04 | 1.02 |
| Ours - V + L + K | **2.07** | **1.52** | **29.47** |

## Limitations

1. **对象检测误差级联**：Relationship Detection R@100（14.70）比 Predicate Detection（47.87）低约 70%，主要受 RCNN 检测质量限制。
2. **仅在 100 对象 × 70 谓词范围验证**：未验证在更大规模词汇上的扩展性。
3. **语言先验依赖 word2vec 质量**：词向量无法覆盖的罕见词或领域术语可能效果差。
4. **非穷尽标注**：mAP 结果偏低，难以公平评估多关系预测。
5. **仅使用独立对象和谓词 CNN**：未建模对象-谓词之间的交互特征。

## Reusable Claims

1. **分离式建模优于联合建模**：O(N+K) 个检测器即可覆盖 O(N²K) 种关系组合，在稀疏标注场景下显著优于每关系单独训练的检测器（Phrase R@100 0.07→17.03）。
2. **语言先验提升关系检测**：word2vec 语义投影 + 语义距离正则化 K() 带来约 8% 的绝对提升（Phrase R@100: V+L only 8.59 → full model 17.03）。
3. **语义相似关系的嵌入约束对零样本学习有效**：K() 为零样本关系检测带来约 30% 相对提升。
4. **对象检测是视觉关系检测的主要瓶颈**：Relationship Det 与 Predicate Det 之间约 34% R@100 差距。
5. **关系理解对图像检索有显著帮助**：Median Rank 从 CNN 的 20 降至 4。

## Connections

- 后续改进方向：**Neural Motifs (CVPR 2018)** 用全局场景上下文改进关系预测；**VCTree (CVPR 2019)** 用动态树结构建模对象上下文。
- 关系检测的数据集规范影响了后来的 **Visual Genome** 和 **Scene Graph Generation** 系列工作。
- 语言先验的思路延伸至 **Graphical Contrastive Losses (CVPR 2019)** 等对比学习方法。
- 零样本关系检测是该领域的早期探索，后续有更多基于 compositional learning 和知识图谱的方法。

## Open Questions

- word2vec 投影在对象类别数远大于 100 时是否仍然有效？
- 如何减少对象检测误差对关系检测的级联影响（后续 R-CNN→Faster R-CNN 的改进提供部分答案）？
- 语义距离正则化 K() 的采样策略（论文使用 500K 随机对）是否最优？

## Provenance

- 原始 PDF: `raw/sources/2016-07-31-visual-relationship-detection-with-language-priors.pdf` (2.3 MB, 19 pages)
- 提取文本: `raw/sources/2016-07-31-visual-relationship-detection-with-language-priors.txt` (51,086 chars, 1,059 lines)
- Evidence: full-paper — 全文逐节阅读，所有结果表格已完整捕获
- 检查日期: 2026-06-10
