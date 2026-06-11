---
title: "IS-GGT: Iterative Scene Graph Generation with Generative Transformers"
type: paper
domain: scene-graph
status: active
created: 2026-06-08
updated: 2026-06-08
tags:
  - scene-graph-generation
  - generative-transformers
  - graph-sampling
  - iterative-generation
  - predicate-classification
  - CVPR-2023
  - transformer
raw_sources:
  - ../../../sources/scene-graph/2023-CVPR-IS-GGT-Iterative-Scene-Graph-Generation-with-Generative-Transformers.pdf
  - ../../../sources/scene-graph/2023-CVPR-IS-GGT-Iterative-Scene-Graph-Generation-with-Generative-Transformers.txt
related_pages:
  - squat-selective-quad-attention-scene-graph-generation.md
  - fast-contextual-scene-graph-generation.md
evidence_level: full-paper
paper:
  title: "IS-GGT: Iterative Scene Graph Generation with Generative Transformers"
  authors:
    - Sanjoy Kundu
    - Sathyanarayanan N. Aakur
  year: 2023
  venue: "IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2023"
  arxiv: null
  doi: null
  code: "https://saakur.github.io/Projects/IS_GGT/"
  project: "https://saakur.github.io/Projects/IS_GGT/"
classification:
  label: "Iterative Scene Graph Generation with Generative Transformers"
  task:
    - Scene Graph Generation (SGG)
    - Predicate Classification (PredCls)
    - Scene Graph Classification (SGCls)
    - Scene Graph Detection (SGDet)
  method_family:
    - Generative Graph Sampling
    - Transformer Decoder
    - Iterative Interaction Graph Generation
    - Two-Stage Architecture
  modality:
    - RGB Image (2D)
  dataset:
    - Visual Genome
  backbone:
    - Faster R-CNN (ResNet-101)
---

# IS-GGT: Iterative Scene Graph Generation with Generative Transformers

## 概述

IS-GGT 提出了一种**两阶段生成式**场景图生成方法，区别于传统的"生成即分类"（generation-by-classification）范式。核心思路是：先用**生成式 Transformer 解码器**从检测到的物体中采样可能的场景图结构（交互图），再对采样出的边缘进行谓词分类。

通过只考虑约 20% 的可能成对边缘，IS-GGT 在不使用任何去偏（unbiasing）机制的情况下，在 Visual Genome 上取得了有竞争力的性能。

## 动机与挑战

- 传统 SGG 方法从全连接图出发（所有物体对之间都有潜在关系），然后对每对进行边缘关系分类
- 全连接图有两个问题：
  1. 稠密拓扑忽略了底层语义结构，导致谓词分类质量差
  2. 成对比较数量随物体数非线性增长（N² 复杂度），推理开销巨大
- 这两个问题加剧了场景图生成中的长尾分布问题
- 现有的去偏方法（TDE、EBML、PPDL 等）依赖于底层图生成器的质量，但底层生成器本身存在上述缺陷

## 方法

### 整体架构（两阶段）

IS-GGT 包含三大组件：

1. **概念接地（Concept Grounding）**——锚定实体假设
2. **结构推理（Structural Reasoning）**——生成式图采样
3. **关系推理（Relational Reasoning）**——边缘关系分类

### 1. 概念接地（Section 3.1）

- 使用预训练 Faster R-CNN (ResNet-101) 检测物体
- 每个检测实体 vi = {li, fᵢᴺ, bbi}（标签、视觉特征、边界框）
- 物体独立表示，不预编码关系，为解耦图预测和谓词分类做准备

### 2. 迭代交互图生成（Section 3.2）——核心创新

- 将图生成建模为**邻接表的自回归解码**
- 对每个节点 vi，Transformer 解码器在给定其视觉特征 fᵢᴺ、标签 li 以及之前解码的邻接矩阵时，输出其邻接表 Âᵢᴺ
- 解码过程按物体置信度分数**固定排序**（从高到低），避免搜索空间爆炸
- 输出 N×N 邻接矩阵，通过阈值 γ 二值化后得到边缘列表 E
- 按能量 E(eij) = σ(ci × cj) 对边缘排序（ci 为检测置信度），取 top-K（K=250）

**训练损失**：
- 邻接损失 LA：预测与真实二值邻接矩阵之间的二元交叉熵
- 语义损失 LS：节点标签预测的交叉熵（辅助损失，注入语义信息）
- 总损失：LG = λ·LA + (1-λ)·LS，λ=0.75

### 3. 边缘关系预测（Section 3.3）

- 对采样出的 top-K 边缘进行谓词分类
- 使用**编码器-解码器 Transformer**，输入为：
  - 视觉特征：实体 ROI 特征 + 边界框特征（线性投影到共同空间）
  - 语义特征：GloVe 300-d 词嵌入
  - 全局上下文（Global Context）：DETR 提取的全图特征
- 使用**加权交叉熵损失**（权重为关系频率的逆归一化）处理长尾分布

### 实现细节

- Faster RCNN (ResNet-101) 预训练于 Visual Genome，冻结检测器层
- 图解码器：hidden=256, 6 层 Transformer, 50 epochs, lr=0.001
- 谓词分类器：hidden=256, 20 epochs, lr=1e-4
- 训练时间：~3 小时（2×NVIDIA Titan RTX, 64-core AMD Threadripper）
- top-K 采样边缘数：K=250

## 实验结果

### Visual Genome 主要结果（mR@K 指标，有图约束）

#### 无去偏方法对比

| 方法 | PredCls mR@50 | PredCls mR@100 | SGCls mR@50 | SGCls mR@100 | SGDet mR@50 | SGDet mR@100 | 平均 mR@50 | 平均 mR@100 |
|------|:-----------:|:-----------:|:---------:|:---------:|:---------:|:---------:|:--------:|:---------:|
| VCTree [33] | 17.9 | 19.4 | 10.1 | 10.8 | 6.9 | 8.0 | 12.7 | 11.6 |
| RelTR [9] | 21.2 | - | 11.4 | - | 8.5 | - | - | 13.7 |
| **IS-GGT (Ours)** | **26.4** | **31.9** | **15.8** | **18.9** | **9.1** | **11.3** | **17.1** | **20.7** |

- IS-GGT 在**所有三个任务**上显著优于所有无去偏方法
- 在平均 mR@100 上达到 **20.7%**，超越 RelTR 约 2.7 个点（平均 mR@50）

#### 与去偏方法对比

- IS-GGT 在平均 mR@100 上（20.7%）与 BGNN（20.7%）持平
- 超越 VCTree+CogTree（20.6%）、MOTIFS+CogTree（19.0%）、MOTIFS+TDE（17.9%）等去偏模型
- 超越统一框架 RU-Net（16.5%）达 **+3.6 个点**
- 与 SOTA 去偏方法 PPDL（23.5%）、PCPL（23.0%）相比仍有差距，但 PPDL/PCPL 考虑 >1000 个组合而 IS-GGT 仅用 ~200 个边缘

### 零样本评估（zR@K）

| 方法 | zR@20 平均 | zR@50 平均 |
|------|:--------:|:--------:|
| VCTree [33] | 0.7 | 1.9 |
| MOTIFS [41] | 0.6 | 1.7 |
| VCTree+EBML [31] | 1.1 | 2.6 |
| **IS-GGT (Ours)** | **2.5** | **4.1** |

- 零样本性能超过所有对比方法（包括去偏方法）的 **2× 以上**
- 无图约束下 zR@100 达 **21.4**，超越 FC-SGG（19.6）、VCTree+TDE（17.6）、MOTIFS+TDE（18.2）

### 图采样效果

- 仅考虑 top-100 边缘（~10% 全组合）即超越所有无去偏 SGG 模型
- top-200 边缘（~20% 全组合）超越大部分去偏模型
- 仅 250 个采样边缘时，约束图准确率（constrained graph accuracy）达 30.7%，即 >30% 真实关系边缘落在 top-250 中

### 消融实验

| 设置 | PredCls mR@100 | SGCls mR@100 | SGDet mR@100 |
|------|:------------:|:-----------:|:-----------:|
| 完整模型（GloVe + 图采样 + 全局上下文） | 30.1 | 17.5 | 11.8 |
| - 去除语义特征 | 29.2 (-0.9) | 15.2 (-2.3) | 10.0 (-1.8) |
| - 去除全局上下文 | 28.5 (-1.6) | 16.9 (-0.6) | 11.0 (-0.8) |
| - 去除边缘先验排序（Edge Prior） | N/A | 17.2 (-0.3) | 9.3 (-2.5) |
| + 使用节点采样（Node Sampling） | 28.5 (-1.6) | 17.2 (-0.3) | 8.9 (-2.9) |
| - 去除图采样 | 27.9 (-2.2) | 16.1 (-1.4) | 11.0 (-0.8) |

关键发现：
- **图采样贡献最大**：去除后 PredCls 下降 2.2、SGCls 下降 1.4
- **语义特征重要性**：去除后平均下降 1.47%
- **节点采样反而降低性能**：说明物体检测器已有全局上下文，额外解码带来噪声
- **边缘先验对 SGDet 最关键**：去除后下降 2.5 个点

## 关键洞察

1. **生成式图采样替代全连接**：首次将图生成模型引入 SGG，避免构造 N² 成对比较
2. **两阶段解耦**：结构推理（采样边缘）和关系推理（分类谓词）分离，各自专注子任务
3. **信息密度**：~20% 的边缘即可承载大部分语义关系，大幅降低推理开销
4. **零样本优势突出**：生成式采样天然泛化到未见过的关系组合（zR@100: 21.4 无图约束）
5. **无需去偏**：在加权交叉熵之外未使用任何专门去偏机制，但平均 mR@100 仍然对比大多数去偏方法有竞争力

## 局限与对比

- IS-GGT 与 SQUAT 同属 CVPR 2023，都关注**选择性边缘处理**
  - SQUAT 通过边缘选择模块（ESM）筛选有效边缘，再用四元注意力进行消息传递
  - IS-GGT 通过生成式图采样直接建模图结构，再对采样边缘分类
  - SQUAT 在 PredCls 上更优（33.4 vs 31.9），但 IS-GGT 更强调推理效率
- 在任务较难设置（SGDet）上，去偏方法 PPDL 和 PCPL 仍优于 IS-GGT
