---
title: "Learning to Generate Scene Graph from Natural Language Supervision"
type: paper
domain: scene-graph
status: active
created: 2026-06-10
updated: 2026-06-10
tags: [scene-graph-generation, weakly-supervised, language-supervision, transformer, ICCV-2021]
source_pages: []
raw_sources: [raw/sources/2021-09-06-learning-to-generate-scene-graph-from-natural-language-supervision.pdf]
related_pages: []
evidence_level: full-paper
paper:
  title: "Learning to Generate Scene Graph from Natural Language Supervision"
  authors: ["Yiwu Zhong", "Jing Shi", "Jianwei Yang", "Chenliang Xu", "Yin Li"]
  year: 2021
  venue: "ICCV 2021"
  arxiv: "2109.02227"
  code: "https://github.com/YiwuZhong/SGG_from_NLS"
  project: null
classification:
  label: "scene-graph-generation"
  task: ["Scene Graph Generation"]
  method_family: ["Language-Supervised SGG", "Triplet Transformer"]
  modality: ["image", "text"]
  datasets: ["Visual Genome", "COCO Caption", "Conceptual Caption"]
  metrics: ["Recall@K", "mean Recall@K"]
---

# Learning to Generate Scene Graph from Natural Language Supervision

## Citation

Zhong, Y., Shi, J., Yang, J., Xu, C., & Li, Y. (2021). Learning to Generate Scene Graph from Natural Language Supervision. *ICCV 2021*. arXiv:2109.02227.

## One-Sentence Contribution

首次提出从 image-sentence pairs 学习 localized scene graph 生成的方法（language supervised SGG），通过 object detector 输出的标签与 caption 解析的 triplets 匹配构建 pseudo labels，结合 Transformer-based Triplet Transformer 模型进行训练。

## Problem Setting

- **输入**：一张图像 + 其检测到的 object regions（由预训练 object detector 提供）
- **输出**：localized scene graph，每个节点是一个带 bounding box 和类别标签的物体，每条边是一个 predicate（关系）
- **监督**：仅 image-sentence pairs（图像 + 对应的句子描述），无需任何人工标注的 bounding box、object 类别或关系标签
- **关键挑战**：候选 image regions 与 caption 中解析出的概念（nouns, predicates）之间存在缺失的对应关系

### 与已有场景图生成设置的对比

| 设置 | Object Boxes | Object & Predicate 标签 |
|------|-------------|------------------------|
| Fully Supervised [53] | ✓ | ✓ |
| Weakly Supervised [61] | ✓ | ✗（仅有 unlocalized scene graph） |
| Language Supervised (Ours) | ✓（来自 detector） | ✗（来自 caption 解析） |

## Method

### 核心思路

1. **Pseudo Label 生成**：使用 rule-based 语言解析器 [21] 从 caption 中提取 SPO triplets；通过 WordNet 匹配检测到的 object categories 与 triplet 中的 subject/object，为 region pair 构建 pseudo label
2. **Triplet Transformer**：基于 Vision-Language Transformer 设计，以 region pair 及其上下文区域为输入，预测 subject、predicate、object 标签
3. **训练信号**：仅使用 pseudo labels 进行 multi-class cross-entropy 训练

### Triplet Transformer 结构

- **Visual Embedder**：对每个 region 的 visual features (ROI pooling, 1536-D) + positional features (7-D) 进行编码，加入 type embedding（subject / object / context）
- **Textual Embedder**：对 subject 和 object 的 GloVe (300-D) word embeddings + predicate 的 [MASK] token 进行编码
- **Transformer Encoder**：2 层 self-attention，12 heads，hidden size 768（基于 UNITER [9] 实现），对所有 visual 和 textual tokens 进行 message passing
- **Classification Heads**：从 encoder 输出融合 visual 和 textual features，通过 2 层 MLP + softmax 分别预测 subject、predicate、object 类别

### 关键设计

- **Weighted Loss**：用于缓解 training set（image captions）与 target set（scene graphs）之间的分布差异。权重 = token 在 caption 中的频率 / token 在 target scene graph 中的估计频率
- **Weighted loss 对 "wearing" 提升 22.1 R@100**
- **Label Assignment**：greedy matching 基于 WordNet synsets、lemmas 和 hypernyms
- **Region Pair 过滤**：过滤掉不重叠或距离太远的 region pairs

### 扩展到其他监督设置

- **Weakly Supervised**：将 caption triplets 替换为 unlocalized scene graph 中的 triplets
- **Fully Supervised**：将 pseudo labels 替换为 ground-truth scene graph labels

## Experiments

### 数据集

- **Visual Genome (VG)** [24]：标准 split [53]，150 objects / 50 predicates，75K train / 32K test images。包含 human-annotated 图像 caption 和 localized scene graphs
- **COCO Caption (COCO)** [6]：123K images，每张 5 个人工标注 caption。筛选后使用 106K images（剔除 VG test 中存在的图像）
- **Conceptual Caption (CC)** [41]：3.3M image-caption pairs，自动从 web 收集

### 数据预处理（closed-set setting）

- VG：148 objects / 52 predicates → 673K triplets / 75K images
- COCO：143 objects / 56 predicates → 154K triplets / 64K images
- CC：148 objects / 64 predicates → 159K triplets / 145K images
- CC + COCO 联合：313K triplets / 210K images

### 评估协议

- **主要指标**：Scene Graph Detection (SGDet) 的 Recall@K (R@K) 和 mean Recall@K (mR@K)
- **SGDet 正确条件**：predicted triplet 标签与 ground-truth 匹配 + subject/object boxes IoU ≥ 0.5
- **Graph constraint**：每对 subject-object 只有一个 predicate prediction
- 代码基于 Tang et al. [46] 的 benchmark 实现

### 实现细节

- **Object Detector**：Faster R-CNN [37] 预训练在 OpenImages [25]（601 categories），保持 top 36 objects/image
- **Region features**：1536-D ROI features
- **Object tags embeddings**：GloVe 300-D
- **Transformer**：UNITER [9] 实现，2 层 self-attention，12 heads，hidden size 768
- **Optimizer**：SGD，batch size 32（images），16 sampled triplets/image，LR 0.0032
- **Loss weights**：λs=λo=0.5, λp=1.0

### Baselines

- **VSPNet** [61]：weakly supervised SGG，从 unlocalized scene graphs 学习
- **VSPNet†**：VSPNet 加上 detector 的 box predictions（与本文相同输入）
- **Ours+Weak**：本文模型用 unlocalized scene graphs 训练
- **Ours+MotifNet**：本文将 pseudo label assignment 应用于 MotifNet [63]
- **Ours+Full**：本文模型用 ground-truth scene graph labels 全监督训练（upper bound）
- **LSWS** [58]：concurrent work，同样使用 image-sentence pairs 但通过 iterative visual grounding 学习

## Results

### 语言监督 SGG — 主要结果（SGDet）

| Method | Supervision | Source | #Images | R@50 | R@100 |
|--------|-------------|--------|---------|------|-------|
| Ours+Full | Localized SG | VG | 58K | 13.8 | 15.3 |
| VSPNet [61] | Unlocalized SG | VG | 58K | 4.7 | 5.4 |
| VSPNet† | Unlocalized SG | VG | 58K | 6.7 | 7.4 |
| **Ours+Weak** | Unlocalized SG | VG | 58K | **10.0** | **11.5** |
| Ours+MotifNet | Image Caption | CC+COCO | 210K | 5.6 | 6.7 |
| **Ours** | Image Caption | CC+COCO | 210K | **5.9** | **7.0** |

**核心发现**：本文仅用 image-sentence pairs 训练的模型（Ours, R@100=7.0）显著超过 VSPNet（R@100=5.4，使用 human-annotated unlocalized scene graphs 训练），**相对提升约 30%**。

### 与 LSWS [58] 对比

| Method | Supervision | Dataset | R@50 | R@100 |
|--------|-------------|---------|------|-------|
| LSWS | Unlocalized SG | VG | 7.3 | 8.7 |
| **Ours** | Unlocalized SG | VG | **10.0** | **11.5** |
| LSWS | Image Caption | VG | 3.9 | 4.0 |
| **Ours** | Image Caption | VG | **9.2** | **10.3** |
| LSWS | Image Caption | COCO | 3.3 | 3.7 |
| **Ours** | Image Caption | COCO | **5.8** | **6.7** |

在 image caption 监督设置下，本文相对 LSWS 提升至少 75%。

### 消融实验

**1. Image Description 来源与 Weighted Loss 的影响**

| CC | COCO | VG | Weighted Loss | #Triplets | R@50 | R@100 |
|----|------|----|-------------|-----------|------|-------|
| ✓ | | | | 159K | 3.4 | 4.1 |
| | ✓ | | | 154K | 3.8 | 4.5 |
| ✓ | | | ✓ | 159K | 5.3 | 6.4 |
| | ✓ | | ✓ | 154K | 5.8 | 6.7 |
| ✓ | ✓ | | ✓ | 313K | 5.9 | 7.0 |
| | | ✓ | - | 673K | 9.2 | 10.3 |

- Weighted loss 提升效果显著：CC 上 R@100 从 4.1 提升至 6.4
- 同一数据集上 CC 和 COCO 性能接近，表明 caption quality 影响较小
- VG 上训练性能最好（10.3 R@100），因为 test 也在 VG 上

**2. Label Assignment 方案**

| Model | Detector | Assignment | R@50 | R@100 |
|-------|----------|-----------|------|-------|
| VSPNet [61] | OpenImages | Iterative Alignment | 4.7 | 5.4 |
| VSPNet† | OpenImages | Iterative Alignment | 6.7 | 7.4 |
| MotifNet | OpenImages | Detection Tags (Ours) | 9.3 | 10.7 |
| **Ours** | OpenImages | Detection Tags (Ours) | **10.0** | **11.5** |
| Ours | Objects365 | Detection Tags (Ours) | 6.1 | 6.4 |

本文的 label assignment scheme 显著优于 VSPNet 的 iterative alignment：
- MotifNet + 本文 assignment 达到 10.7 R@100 vs VSPNet† 7.4 R@100
- Objects365 detector 性能差（6.4 vs 11.5 R@100），原因：仅 94/150 VG objects 可匹配（vs OpenImages 123/150）

**3. Visual vs. Textual 输入贡献**

| Visual Input | Text Input | Detection mAP | R@50 | R@100 |
|-------------|-----------|---------------|------|-------|
| ✓ | ✓ | 10.7 | 10.0 | 11.5 |
| ✓ | | 10.6 | 3.9 | 4.7 |
| | ✓ | 6.9 | 6.2 | 7.7 |

- Visual input 关键用于 object detection（mAP 10.6 vs 6.9）
- Textual input 关键用于 predicate prediction（R@100 7.7 vs 4.7）
- 二者互补

### 全监督 SGG 结果

| Model | SGDet R@100 | SGCls R@100 | PredCls R@100 | mSGDet R@100 | mSGCls R@100 | mPredCls R@100 |
|-------|------------|------------|--------------|-------------|-------------|---------------|
| IMP [53] | 31.2 | 38.5 | 63.1 | 5.3 | 6.5 | 11.8 |
| VTransE [64] | 34.3 | 39.4 | 67.6 | 6.0 | 8.7 | 15.8 |
| VCTree [47] | 36.2 | 41.4 | 68.1 | 6.9 | 7.9 | 16.1 |
| MotifNet [63] | 36.9 | 39.9 | 67.9 | 6.8 | 8.5 | 15.8 |
| **Ours** | **36.3** | **40.8** | **67.4** | **8.7** | **11.1** | **19.5** |

- 全监督下 Recall 与 SOTA 持平（36.3 vs 36.9 R@100 SGDet）
- **Mean Recall 显著高于所有 baseline**：mSGDet 8.7 vs 6.9（VCTree），mPredCls 19.5 vs 16.1
- 表明本文模型在 tail categories 上表现更好

### Open-set SGG 结果

| Setting | #Objects | #Predicates | #Triplets | #Images | R@50 | R@100 |
|---------|---------|------------|-----------|---------|------|-------|
| Closed-set | 143 | 56 | 154K | 64K | 3.8 | 4.5 |
| Open-set | 4273 | 677 | 758K | 105K | 4.1 | 4.8 |

- Open-set 设置使用 COCO Caption 训练，在 VG 上评估
- Open-set 略优于 closed-set（4.8 vs 4.5 R@100），因为能从更多概念中学习
- **本文提供 open-set SGG 的首个结果**

## Limitations

1. **强依赖 object detector 的覆盖范围**：性能受限于 detector 能识别的 object categories（OpenImages 601 classes）
2. **Pseudo label 分配时的歧义**：当存在多个同类物体实例时，无法确定 caption 中 triplet 对应哪个实例
3. **Performance gap 仍大**：语言监督（7.0 R@100）vs 弱监督（11.5 R@100）vs 全监督（15.3 R@100），仍有很大改进空间

## Reusable Claims

- **Claim**: Image captions alone can serve as sufficient supervisory signal for localized scene graph generation, achieving 7.0 R@100 on VG SGDet.
  - Evidence: Table 2, Section 4.1
  - Scope: VG dataset, OpenImages detector, closed-set setting, CC+COCO captions
  - Confidence: high

- **Claim**: The proposed detection-tags-based label assignment scheme significantly outperforms iterative alignment (VSPNet) for weakly supervised SGG.
  - Evidence: Table 5: MotifNet + our assignment 10.7 R@100 vs VSPNet† 7.4 R@100
  - Scope: Weakly supervised setting, VG dataset
  - Confidence: high

- **Claim**: Visual and textual inputs play complementary roles — visual features dominate object detection, textual features dominate predicate prediction.
  - Evidence: Table 6: removing visual → mAP 10.6→6.9 (object drop), removing textual → R@100 11.5→7.7 (predicate drop)
  - Scope: Weakly supervised setting
  - Confidence: high

- **Claim**: The Triplet Transformer achieves SOTA mean recall in fully supervised SGG, indicating better coverage of tail predicates.
  - Evidence: Table 7: mSGDet 8.7 vs 6.9 (VCTree), mPredCls 19.5 vs 16.1 (VCTree)
  - Scope: Fully supervised setting, VG dataset
  - Confidence: high

## Connections

- 本文与 **LSWS [58]** 是 concurrent works，都探索从 image-sentence pairs 学习 SGG。本文通过 object detector + detection tags matching 显著优于 LSWS 的 iterative visual grounding 方法（COCO 上 6.7 vs 3.7 R@100）
- 与 **VSPNet [61]** 相比，本文 setting 更弱（caption vs unlocalized SG）但效果更好（7.0 vs 5.4 R@100）
- 本文的 **Shi et al. [43]** 是同一团队的另一篇 weak supervision SGG 工作（ICCV 2021）
- 模型设计受 **UNITER [9]** vision-language pre-training 启发
- 在 language supervised SGG 方向后续工作有：**VS3 (CVPR 2023)**, **LLM4SGG (CVPR 2024)**，以及 **SSC-SGG (AAAI 2025)**
- 本文提供了 **open-set SGG 的首个结果**，为后续 open-vocabulary SGG 工作（如 OV-SGG, FDtM）奠定基础

## Open Questions

1. 如何将 object detector 升级为 open-vocabulary detector 以进一步提升性能？
2. 当图像中有多个同类物体时，如何利用上下文信息消除 pseudo label 分配中的歧义？
3. language supervised SGG 的 performance gap（7.0 vs 15.3 R@100 full supervision）如何缩小？
4. 从 image-sentence pairs 学到的 scene graph 能否有效用于下游任务（如 VQA、image retrieval）？

## Provenance

- Raw source: `raw/sources/2021-09-06-learning-to-generate-scene-graph-from-natural-language-supervision.pdf`
- Full text: `raw/sources/2021-09-06-learning-to-generate-scene-graph-from-natural-language-supervision.txt`
- Evidence level: full-paper（全文 16 页，包含所有方法细节、实验结果、消融研究和附录）
