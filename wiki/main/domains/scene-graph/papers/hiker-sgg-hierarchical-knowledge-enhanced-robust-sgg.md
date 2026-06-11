---
title: "HiKER-SGG: Hierarchical Knowledge Enhanced Robust Scene Graph Generation"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - scene-graph-generation
  - robust-SGG
  - knowledge-graph
  - hierarchical-reasoning
  - image-corruption
  - zero-shot-robustness
  - CVPR-2024
raw_sources:
  - ../../../sources/scene-graph/2024-CVPR-HiKER-SGG-Hierarchical-Knowledge-Enhanced-Robust-SGG.pdf
  - ../../../sources/scene-graph/2024-CVPR-HiKER-SGG-Hierarchical-Knowledge-Enhanced-Robust-SGG.txt
related_pages:
  - fast-contextual-scene-graph-generation.md
  - scalable-theory-driven-regularization-scene-graph-generation.md
evidence_level: full-paper
paper:
  title: "HiKER-SGG: Hierarchical Knowledge Enhanced Robust Scene Graph Generation"
  authors:
    - Ce Zhang
    - Simon Stepputtis
    - Joseph Campbell
    - Katia Sycara
    - Yaqi Xie
  year: 2024
  venue: "IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2024"
  arxiv: null
  doi: null
  code: "https://github.com/zhangce01/HiKER-SGG"
  project: null
classification:
  label: "Hierarchical Knowledge Enhanced Robust SGG"
  task:
    - Scene Graph Generation (SGG)
    - Predicate Classification (PredCls)
    - Scene Graph Classification (SGCls)
    - Robust SGG under real-world corruptions
  method_family:
    - Hierarchical knowledge graph
    - External knowledge base retrieval
    - Message passing on hierarchical graph
    - Adaptive refinement (AR)
    - Hierarchical predicate/entity prediction head
  modality:
    - Image
  learning_paradigm: supervised
  long_tail: addressed (via hierarchical decomposition of predicate/entity classes)
summary: >
  HiKER-SGG 提出了一种层级知识增强的鲁棒场景图生成框架，专门应对真实世界中的图像退化（如雾、烟、雪、阳光眩光、水滴等）。
  核心思想是构建层级知识图谱（hierarchical knowledge graph），将粗粒度的类别推断逐步细化为细粒度预测，
  从而在 zero-shot 场景下对受损图像保持鲁棒性。同时，本文引入了 Corrupted Visual Genome (VG-C) 基准，
  包含 20 种程序化生成的图像退化类型，用于标准化 SGG 鲁棒性评估。
---

## 背景与动机

现有 SGG 方法普遍假设输入图像是"干净"的，而真实世界中图像常受到各种退化影响（阳光眩光、灰尘、水滴、雨、雪等）。
当模型在这些退化图像上测试时，性能大幅下降。受人类利用先验领域知识识别受损物体能力的启发，
HiKER-SGG 利用外部知识库构建层级知识图谱，在粗→细的推理过程中提升鲁棒性。

## 方法

### 总体架构

HiKER-SGG 的整体流程包含三个主要阶段：

1. **初始场景图生成**：使用 Faster-RCNN 检测器从输入图像中提取初始场景图（物体候选框 + 关系初始预测）
2. **层级知识图谱构建**：从外部知识库构建层级知识图谱，包含**谓词层级（predicate hierarchy）**和**实体层级（entity hierarchy）**
3. **层级图推理**：在层级知识图谱与初始场景图之间建立 bridging connections，执行消息传递（message passing），逐步从粗粒度细化到细粒度预测

### 核心技术组件

- **层级知识图谱（Hierarchical Knowledge Graph）**：包含两级节点——粗类别（superclass，如 "animal"）和细类别（subclass，如 "cat"）。谓词层级和实体层级分别构建。
- **消息传递机制**：在层级图谱上进行 t=3 步的消息传播，使信息在粗→细节点间流动
- **自适应细化（Adaptive Refinement, AR）**：根据预测置信度自适应地决定是否进行层级细化
- **层级预测头**：将传统的单一分类器分解为多个层级分类器，每个层级只处理更小的类别空间

### VG-C 基准

- 基于 Visual Genome 数据集，引入 **20 种图像退化**
- 前 15 种来自 Hendrycks et al. 的 ImageNet-C 标准退化：高斯噪声、shot 噪声、impulse 噪声、defocus blur、glass blur、motion blur、zoom blur、snow、frost、fog、brightness、contrast、elastic transform、pixelate、JPEG compression
- 新增 5 种真实世界退化：**sun glare（阳光眩光）、water-drop（水滴）、wildfire smoke（野火烟雾）、rain（雨）、dust（灰尘）**

## 实验结果

### Clean Visual Genome 上的 PredCls 任务

| 方法 | Venue | PredCls mR@20 (UC/C) | PredCls mR@50 (UC/C) | PredCls mR@100 (UC/C) |
|------|-------|----------------------|----------------------|-----------------------|
| IMP+ | CVPR'17 | - / - | 20.3 / 9.8 | 28.9 / 10.5 |
| Neural Motifs | CVPR'18 | - / 10.8 | 24.8 / 14.0 | 37.3 / 15.3 |
| GB-Net | ECCV'20 | 23.8 / 15.3 | 41.1 / 19.3 | 55.4 / 20.9 |
| EB-Net+EOA | WACV'23 | 39.8 / 30.8 | 54.9 / 36.7 | 66.3 / 39.2 |
| **HiKER-SGG (Ours)** | — | **42.1 / 33.4** | **57.9 / 39.3** | **69.2 / 41.2** |

### Clean Visual Genome 上的 SGCls 任务

| 方法 | SGCls mR@20 (UC/C) | SGCls mR@50 (UC/C) | SGCls mR@100 (UC/C) |
|------|---------------------|---------------------|----------------------|
| IMP+ | - / - | 12.1 / 9.8 | 16.9 / 10.5 |
| Neural Motifs | - / 6.3 | 13.5 / 7.7 | 19.6 / 8.2 |
| GB-Net | 13.1 / 7.9 | 21.4 / 9.6 | 29.1 / 10.2 |
| EB-Net+EOA | 19.6 / 14.9 | 26.7 / 17.3 | 32.5 / 18.3 |
| **HiKER-SGG (Ours)** | **22.6 / 18.2** | **30.0 / 20.3** | **36.7 / 21.4** |

### VG-C（Corrupted）上的 PredCls 任务——平均 mR

| 方法 | mR@20 (UC) Avg | mR@50 (UC) Avg | mR@100 (UC) Avg |
|------|----------------|----------------|-----------------|
| GB-Net | 17.3 (-27.3%) | 31.0 (-24.6%) | 44.0 (-20.6%) |
| EB-Net | 30.9 (-22.4%) | 45.2 (-17.7%) | 56.7 (-14.5%) |
| **HiKER-SGG** | **34.6 (-17.8%)** | **49.5 (-14.5%)** | **61.4 (-11.3%)** |

在 VG-C 所有 20 种退化类型上，HiKER-SGG 在所有六项指标上平均提升约 **4%**。且相对于干净图像的性能下降幅度最小（如 mR@100 UC 仅下降 11.3%，而 EB-Net 下降 14.5%）。

### 关键零样本鲁棒性结果

在 impulse noise 情况下（约束条件 C）：
- HiKER-SGG mR@20: **24.8%**（相较于干净图像下降 8.6%）
- EB-Net mR@20: 20.4%（相较干净图像下降 10.4%）

### 消融实验

| PH | EH | AR | mR@20 (UC/C) | mR@50 (UC/C) | mR@100 (UC/C) |
|----|----|----|--------------|--------------|---------------|
| — | — | — | 39.8 / 30.8 | 54.9 / 36.7 | 66.3 / 39.2 |
| ✓ | — | — | 40.4 / 31.4 | 55.7 / 37.2 | 67.1 / 39.8 |
| M | — | — | 41.6 / 32.9 | 57.3 / 37.5 | 68.1 / 39.6 |
| M | M | — | 41.4 / 33.1 | 57.6 / 37.9 | 68.2 / 39.7 |
| M | M | ✓ | 41.8 / 33.2 | 57.7 / 38.1 | 68.7 / 40.0 |
| D | D | — | 41.7 / 33.2 | 57.7 / 38.8 | 69.0 / 40.4 |
| **D** | **D** | **✓** | **42.1 / 33.4** | **57.9 / 39.3** | **69.2 / 41.2** |

- PH: predicate hierarchical head, EH: entity hierarchical head, M: manually configured, D: discovered by hierarchical clustering, AR: adaptive refinement
- 仅谓词层级即可提升 mR@k 约 1.0%，增加实体层级再提升 0.5%
- 用聚类自动发现的层级结构优于人工配置（提升 0.4%~0.7%）
- 自适应细化（AR）额外贡献 0.2%~0.8%

### 效率对比

| 方法 | 训练时间 | 参数量 |
|------|---------|--------|
| KERN | 179.1 min | 405.2M |
| GB-Net | 84.6 min | 444.6M |
| EB-Net | 89.7 min | 448.8M |
| **HiKER-SGG** | 101.3 min | 455.9M |

HiKER-SGG 仅增加约 7M 参数，训练时间增加约 12 分钟/epoch，相比于同类知识图谱方法相当。

## 核心创新

1. **首次提出 Robust SGG 任务**：在真实世界图像退化场景下的场景图生成
2. **VG-C 基准**：包含 20 种退化类型的标准化鲁棒性评估平台
3. **层级知识增强框架**：利用外部知识库构建层级知识图谱，通过从粗到细的推理提升鲁棒性
4. **零样本鲁棒性**：只使用干净图像训练，在退化图像上零样本测试即能达到显著优于基线的方法
5. **消融分析**：系统地量化了谓词层级、实体层级、自适应细化、手动 vs 自动层级发现等各组件的贡献

## 局限性（待验证）

- 仅使用 VG 数据集（150 objects / 50 predicates），尚未验证在大规模数据集上的扩展性
- 退化图像通过程序化生成，与真实退化场景的分布差异未充分分析
- 参数量相比 GB-Net / EB-Net 略增（455.9M vs ~445M）
- 与最先进的非知识图谱方法（如 PE-Net+SIL）在干净图像上的对比未充分展开

## 相关链接

- 代码：[https://github.com/zhangce01/HiKER-SGG](https://github.com/zhangce01/HiKER-SGG)
- GitHub 星标（待补充）
