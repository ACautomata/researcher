---
title: "TextPSG: Panoptic Scene Graph Generation from Textual Descriptions"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - scene-graph-generation
  - panoptic-scene-graph
  - weakly-supervised-sgg
  - caption-to-psg
  - text-supervision
  - open-vocabulary
  - iccv-2023
raw_sources:
  - ../../../sources/scene-graph/2023-ICCV-TextPSG-Panoptic-Scene-Graph-Generation-from-Textual-Descriptions.pdf
  - ../../../sources/scene-graph/2023-ICCV-TextPSG-Panoptic-Scene-Graph-Generation-from-Textual-Descriptions.txt
related_pages:
  - panoptic-video-scene-graph-generation.md
  - language-supervised-open-vocabulary-scene-graph-vs3.md
  - prototype-based-embedding-network-scene-graph-generation.md
evidence_level: full-paper
paper:
  title: "TextPSG: Panoptic Scene Graph Generation from Textual Descriptions"
  abbreviated: "TextPSG"
  authors:
    - Chengyang Zhao
    - Yikang Shen
    - Zhenfang Chen
    - Mingyu Ding
    - Chuang Gan
  affiliations:
    - Peking University
    - MIT-IBM Watson AI Lab
    - UC Berkeley
    - UMass Amherst
  year: 2023
  venue: ICCV 2023
  doi: null
  arxiv: null
  code: null
  url: https://vis-www.cs.umass.edu/TextPSG
---

# TextPSG: Panoptic Scene Graph Generation from Textual Descriptions

## 核心思想

提出新问题 **Caption-to-PSG**（Panoptic Scene Graph Generation from Purely Textual Descriptions），首次尝试仅从图像-文本对（image-caption pairs）中学习生成 mask 级全景场景图，无需位置先验、无需显式的区域-实体链接、无需预定义概念集。

核心思路：利用大量免费的 Web 图像-文本数据作为监督信号，通过模块化框架 TextPSG 将自然语言描述中的实体与图像区域对齐，逐步学习物体定位、语义理解和关系预测。

## 方法

### 框架总览：四个模块

TextPSG 包含四个核心模块，按流水线顺序执行：

1. **Region Grouper（区域分组器）**：将图像像素分组为不同 segment。基于 GroupViT（[48]），通过分组 Transformer 架构从文本监督中学习语义分割。设置 K=2 个分组阶段，第一阶段产生 H1=64 个 segment，第二阶段产生 H2=8 个 segment。

2. **Entity Grounder（实体接地器）**：将视觉 segment 与文本实体对齐。核心组件 TfmT（Text-former-for-Matching）基于 Transformer 编码器，学习同一图像中文本实体与 segment 之间的匹配分数。包含两个关键机制：
   - **Hard Negative Sampling**：通过强化负样本跨图像挖掘（text-to-image retrieval）和段内匹配（query-to-target within same image）来提升判别能力
   - **Segment Permutation**：缓解视觉和文本之间的标记顺序差异（permutation variance）

3. **Segment Merger（段合并器）**：学习合并相似 segment。利用基于图割（graph cut）的显式段合并策略，将来自第一分组阶段的 H1=64 个 segment 合并为更少的语义一致区域。合并决策基于实体 grounder 提供的相似度分数，同时保持空间连通性约束。

4. **Label Generator（标签生成器）**：为合并后的 segment 生成物体语义标签和关系谓词标签。基于预训练的 BLIP 解码器（冻结），通过自回归方式生成文本标签。关键创新是 **PET（Prefix Embedding Tuning）**——一组可学习的 prefix embedding，插入到 BLIP 解码器的交叉注意力层之前，使模型能够利用 BLIP 的预训练常识而无需微调解码器本身。

### 推理流程

1. 输入图像 → Region Grouper → 获得 H1=64 个初始 segment
2. Entity Grounder 为每个 segment 生成与文本实体匹配的分数
3. Segment Merger 基于图割合并相似 segment → 获得 N 个最终 segment
4. Label Generator 为每个最终 segment 生成物体语义标签
5. 对每一对 segment（subject-object），Label Generator 生成关系谓词标签
6. 输出：mask 级全景场景图（panoptic scene graph）

### 训练策略

- Region Grouper 使用 GroupViT 的预训练权重
- Entity Grounder 的 TfmT 使用预训练文本编码器
- Label Generator 使用预训练 BLIP 解码器（冻结），仅训练 PET prefix embeddings
- 训练数据：COCO Caption 数据集（118,287 张图像，每张 5 个人工标注标题）

## 实验

### 数据集

- **训练**：COCO Caption 数据集（118,287 张图像，2017 split）
- **评估**：Panoptic Scene Graph 数据集（PSG, [49]），合并后包含 127 个物体语义和 56 个关系谓词

### 评估指标

- **PhrDet（Visual Phrase Detection）**：检测 subject-predicate-object 整体短语，union location IoU > 0.5
- **SGDet（Scene Graph Detection）**：分别检测 subject 和 object，各自 IoU > 0.5
- **NXR@K**：No-Graph-Constraint Recall@K，允许每对 subject-object 最多预测 X 个关系

### 主要结果

| 方法 | 方式 | PhrDet N5R100 | SGDet N5R100 |
|------|------|:------:|:------:|
| Random（bbox） | bbox | 0.03 | 0.07 |
| Prior（bbox） | bbox | 0.07 | 0.07 |
| MIL（bbox） | bbox | 2.61 | 1.97 |
| SGCLIP（bbox） | bbox | 3.71 | 2.70 |
| SGGNLS-o（bbox, w/ detector） | bbox | 7.93 | 5.02 |
| **Ours（mask）** | mask | 10.51 | 4.18 |
| **Ours（bbox）** | bbox | **14.37** | **5.48** |

**关键发现**：
- TextPSG 显著超越所有同约束（无位置先验、无预定义概念集）的基线方法（PhrDet N5R100 14.37 vs. SGCLIP 3.71）
- 即使与使用预训练检测器提供位置先验的 SGGNLS-o 相比，TextPSG 在 PhrDet（14.37 vs. 7.93）和 SGDet（5.48 vs. 5.02）上均表现更好
- mask 模式（严格要求 mask 级匹配）也优于所有 bbox 基线的 mask 性能

### OOD 鲁棒性

| 集合 | 方法 | PhrDet N5R100 | SGDet N5R100 |
|------|------|:------:|:------:|
| ID | SGGNLS-c | 18.48 | 11.86 |
| ID | SGGNLS-o | 13.64 | 8.47 |
| ID | Ours（bbox） | 14.82 | 5.36 |
| **OOD** | SGGNLS-c | **0.00** | **0.00** |
| **OOD** | SGGNLS-o | **0.06** | **0.00** |
| **OOD** | **Ours（bbox）** | **11.69** | **5.72** |

**关键发现**：SGGNLS-c 和 SGGNLS-o 在 OOD 场景下性能几乎归零（依赖预训练检测器的概念覆盖），而 TextPSG 在 ID 和 OOD 上保持相近性能，展示出极强的 OOD 鲁棒性。

### 消融实验

1. **Segment Merger 消融**（Tab. 3）：图割合并 + 第一阶段 64 segment → 最优（N5R100 PhrDet 14.37 vs. 不加图割 11.39）
2. **Label Generator 消融**（Tab. 4）：生成式（generation）优于分类式（classification）；PET 设计非常关键（BLIP w/ PET 14.28 vs. BLIP w/o PET 2.58 N5R100 PhrDet）
3. **TSSS 应用**（Tab. 5）：TextPSG 的 entity grounder + segment merger 提升了 GroupViT 的语义分割性能（mIoU 26.87% vs. GroupViT 24.72%，+2.15%）

### 局限性

论文自身总结了三个主要限制：
1. **实例分割转换不完善**：将语义分割中每个连通分量视为独立实例，重叠/遮挡时失效
2. **小物体定位困难**：分辨率和分组策略的限制
3. **关系预测不够充分**：标签生成器有时过度依赖物体语义，忽略实际图像内容
4. **Caption 粒度不足**：caption 数据中常以复数形式合并同类物体，限制了实例区分

## 与我库其他论文关联

- **对比**：[[panoptic-video-scene-graph-generation.md]] 将 PSG 扩展到视频域，TextPSG 关注静态图像的 caption-to-PSG 问题
- **对比**：[[language-supervised-open-vocabulary-scene-graph-vs3.md]] 使用语言监督进行开放词汇 SGG，但依赖检测器提供位置先验，TextPSG 不依赖任何位置先验
- **启发**：TextPSG 证明了纯文本监督对场景图生成的可行性，为弱监督 SGG 提供了新的范式
