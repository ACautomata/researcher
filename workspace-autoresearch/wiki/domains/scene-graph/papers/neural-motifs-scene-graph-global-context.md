---
title: "Neural Motifs: Scene Graph Parsing with Global Context"
type: paper
domain: scene-graph
status: active
created: 2026-06-10
updated: 2026-06-10
tags:
  - scene-graph-generation
  - foundational
  - motif-patterns
  - global-context
  - biLSTM
  - CVPR-2018
raw_sources:
  - ../../../raw/sources/2018-CVPR-Neural-Motifs-Scene-Graph-Global-Context.pdf
  - ../../../raw/sources/2018-CVPR-Neural-Motifs-Scene-Graph-Global-Context.txt
related_pages:
  - message-passing-scene-graph-generation.md
  - reltr-relation-transformer-scene-graph-generation.md
  - unbiased-scene-graph-generation-tde-causal-modeling.md
  - eicr-environment-invariant-curriculum-relation-learning-sgg.md
  - camodule-causal-adjustment-module-debiasing-scene-graph-generation.md
evidence_level: full-paper
paper:
  title: "Neural Motifs: Scene Graph Parsing with Global Context"
  authors:
    - Rowan Zellers
    - Mark Yatskar
    - Sam Thomson
    - Yejin Choi
  year: 2018
  venue: CVPR 2018
  doi: "10.1109/CVPR.2018.00591"
  arxiv: "1711.06640"
  code: "https://github.com/rowanz/neural-motifs"
  citations: 2300+
  project: "https://rowanzellers.com/neuralmotifs"
---

# Neural Motifs: Scene Graph Parsing with Global Context

## 概述

SGG（Scene Graph Generation）领域的奠基论文之一，引用 2300+。核心洞察：**场景图中的关系标签高度依赖于物体类别标签（而非反之）**，这种非对称依赖使得利用全局上下文进行结构化预测成为关键。论文提出的 FREQ baseline 和 MOTIFNET 成为此后几乎所有 SGG 方法的对比基准。

## 核心洞察：Motif 模式

通过 Visual Genome 数据集的统计分析发现：

1. **物体标签高度预测关系标签**：给定物体对类别，关系的分布高度偏斜。例如 `person-wearing-shirt` 在训练集中出现频率远高于其他关系。反之则不成立（关系标签对物体标签的预测力弱）。
2. **子图级别的重复模式**：超过 50% 的场景图包含至少两条关系的 motif（重复出现的子图结构）。
3. **长尾分布**：Visual Genome 中关系类别呈长尾分布，常见关系（wear、has、on、in）主导训练数据。

## 方法架构

### MOTIFNET（Stacked Motif Network）

MOTIFNET 将场景图解析分解为阶段性预测过程，每阶段利用前序阶段的全局上下文：

1. **Bounding Box 预测**：Faster-RCNN（在 VG 上 fine-tune）生成 RoI 候选框
2. **双向 LSTM 全局上下文编码**：对所有 RoI 视觉特征经过 biLSTM 编码全局上下文
3. **物体标签预测 LSTM**：从左到右（按 biLSTM 编码顺序）逐物体预测标签，每个预测条件于之前的标签和全局上下文
4. **边预测 biLSTM**：对所有物体对编码全局上下文化的表示，使用低秩外积（low-rank outer product）融合 head、tail 和图像特征
5. **端到端训练**

### FREQ Baseline

一个惊人简单但有效的 baseline：给定检测到的物体类别，**直接使用训练集统计的频率分布**预测物体对之间的关系，完全不看图像内容。FREQ+OVERLAP 版本额外要求两框要有 IoU 重叠。

## 实验结果

### 主要结果（Table 6，Visual Genome，@K）

| 模型 | PredCls R@20/50/100 | SGCls R@20/50/100 | SGDet R@20/50/100 | Mean R@50/100 |
|------|---------------------|-------------------|-------------------|---------------|
| VRD (Lu et al. 2016) | -/27.9/35.0 | -/11.8/14.1 | -/0.3/0.5 | 14.9 |
| MESSAGE PASSING (Xu et al. 2017) | -/44.8/53.0 | -/21.7/24.4 | -/3.4/4.2 | 25.3 |
| MESSAGE PASSING+ | **52.7/59.3/61.3** | **31.7/34.6/35.4** | 14.6/20.7/24.5 | 39.3 |
| ASSOC EMBED (Newell & Deng 2017) | 47.9/54.1/55.4 | 18.2/21.8/22.6 | 6.5/8.1/8.2 | 28.3 |
| FREQ | 49.4/59.9/64.1 | 27.7/32.4/34.0 | 17.7/23.5/27.6 | 40.2 |
| **FREQ+OVERLAP** | **53.6/60.6/62.2** | 29.3/32.3/32.9 | 20.1/26.2/30.1 | **40.7** |
| **MOTIFNET** | **58.5/65.2/67.1** | **32.9/35.8/36.5** | **21.4/27.2/30.3** | **43.6** |

> **注**：Mean = (PredCls @50 + PredCls @100 + SGCls @50 + SGCls @100 + SGDet @50 + SGDet @100) / 6。

### 关键观察

- **FREQ+OVERLAP 超越 prior SOTA（MESSAGE PASSING+）**：mean Recall 提升 1.4 个点（+3.6% relative），主要在 PredCls (+6.5) 和 SGDet (+5.5) 上显著
- **MOTIFNET 进一步超越 FREQ+OVERLAP**：mean Recall 再提升 2.9 个点（+7.1% relative），所有设定一致提升
- **MOTIFNET vs MESSAGE PASSING+**：全量提升 4.3 mean 点（+10.9% relative）

### 消融实验

| 变体 | 说明 | Mean R@50/100 |
|------|------|--------------|
| MOTIFNET-NOCONTEXT | 去除边预测时的全局上下文 | 42.4 |
| MOTIFNET-CONFIDENCE | 按检测置信度排序替代 biLSTM 顺序 | 43.5 |
| MOTIFNET-SIZE | 按框面积排序替代 biLSTM 顺序 | 43.3 |
| MOTIFNET-RANDOM | 随机排序替代 biLSTM 顺序 | 43.5 |
| MOTIFNET (full) | 完整模型 | 43.6 |

消融结果显示：
- 去掉上下文（NOCONTEXT）descent 最大（-1.2 mean），确认全局上下文价值
- 排序方式影响极小（<0.3），说明 MOTIFNET 对 RoI 顺序鲁棒
- R@20 上上下文收益最大，说明主要改善关系排序而非分类

## 方法比较与影响

### 与 SGG 任务设定的关系

论文首次系统定义了三个评估设定并沿用至今：
- **PredCls（谓词分类）**：给定 GT box + GT object label，预测关系
- **SGCls（场景图分类）**：给定 GT box，预测 object label + 关系
- **SGDet（场景图检测）**：从零预测 box + object label + 关系

### 后续方法对比（影响）

作为 SGG 领域奠基性工作，MOTIFNET 是几乎所有后续方法的直接对比基准：

| 后续方法 | 与 MOTIFNET 对比要点 |
|----------|---------------------|
| G-RCNN / RelTR (Transformer 架构) | 用 Transformer 替代 biLSTM 进行全图上下文编码 |
| EICR (2020) | 发现 MOTIFNET 在长尾关系上偏置，提出课程学习去偏 |
| TDE/CAModule (因果 SGG) | 指出 MOTIFNET 依赖统计 co-occurrence 导致上下文偏差，用因果干预去偏 |
| Contextual SGG (2023+) | 在 MOTIFNET pipeline 上添加更丰富的视觉上下文编码 |

## 局限与后续问题

1. **依赖于 VG 预设的 150 类物体 / 50 类关系**：限制了开放世界泛化能力
2. **biLSTM 的顺序性**：物体排列顺序影响关系预测精度（虽实验显示鲁棒）
3. **FREQ baseline 的惊人表现**：说明 VG 数据集的统计偏置极大，模型可能"偷懒"利用 co-occurrence 而非真正理解视觉语义
4. **检测失败级联**：Faster-RCNN 漏检直接导致关系预测失败
5. **评估指标 R@K 的局限**：未考虑关系质量排序，后续工作提出 mR@K 等指标

## 参考资料

- 原始论文：Zellers et al., "Neural Motifs: Scene Graph Parsing with Global Context", CVPR 2018
- 代码：https://github.com/rowanz/neural-motifs
- 项目页：https://rowanzellers.com/neuralmotifs
