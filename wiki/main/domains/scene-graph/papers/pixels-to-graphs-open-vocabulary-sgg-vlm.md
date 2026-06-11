---
title: "From Pixels to Graphs: Open-Vocabulary Scene Graph Generation with Vision-Language Models (PGSG)"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - scene-graph-generation
  - open-vocabulary-sgg
  - vlm-sgg
  - sequence-generation-sgg
  - image-to-graph
  - blip
  - visual-language-model
  - CVPR-2024
raw_sources:
  - ../../../sources/scene-graph/2024-CVPR-From-Pixels-to-Graphs-Open-Vocabulary-SGG.pdf
  - ../../../sources/scene-graph/2024-CVPR-From-Pixels-to-Graphs-Open-Vocabulary-SGG.txt
related_pages:
  - language-supervised-open-vocabulary-scene-graph-vs3.md
  - ovsgtr-expanding-scene-graph-boundaries.md
  - cage-sgg-counterfactual-active-graph-evidence-open-vocabulary-sgg.md
evidence_level: full-paper
paper:
  title: "From Pixels to Graphs: Open-Vocabulary Scene Graph Generation with Vision-Language Models"
  abbreviated: "PGSG"
  authors:
    - Rongjie Li
    - Songyang Zhang
    - Dahua Lin
    - Kai Chen
    - Xuming He
  affiliations:
    - School of Information Science and Technology, ShanghaiTech University
    - Shanghai AI Laboratory
    - Shanghai Engineering Research Center of Intelligent Vision and Imaging
  year: 2024
  venue: CVPR 2024
  arxiv: null
  code: https://github.com/SHTUPLUS/Pix2Grp_CVPR2024
  url: null
  doi: null
classification:
  label: "Open-Vocabulary Predicate SGG via Image-to-Text Generation with VLM"
  task:
    - Open-Vocabulary Scene Graph Generation
    - Scene Graph Generation
    - Vision-Language Reasoning

---

## 概述

PGSG (Pixel to Graph Scene Graph) 提出一种基于**序列生成**范式的开放词汇场景图生成（open-vocabulary SGG）框架。核心思路是将 SGG 转化为**图像到文本生成**（image-to-text generation）任务，利用预训练视觉语言模型（VLM，以 BLIP 为例）直接生成描述场景结构的文本序列，再从中解析出场景图。该方法突破传统 SGG 方法依赖封闭谓词集合的限制，同时实现 SGG 与下游 VL 任务（VQA、视觉定位、图像描述）的统一框架。

## 背景与动机

- 传统 SGG 方法受限于封闭谓词集合，无法泛化到未见过的视觉关系概念
- 现有开放词汇 SGG 方法（如 CaCao、SVRP）仅支持给定实体对条件下的谓词分类（predicate classification），无法完整完成 SGDet 设定下的实体检测 + 关系预测
- VLM 已具备强大的零样本视觉语义理解能力，但如何将 VLM 用于结构化图生成的尚未被充分探索
- 现有 VLM 在 SGG 中缺乏显式关系建模，限制了其对下游 VL 推理任务的增益

## 方法

### 整体架构

PGSG 由三个核心模块构成：

1. **VLM-based 场景图序列生成器**：以图像为输入，通过 BLIP 的视觉编码器（ViT-B/16）提取视觉特征，文本解码器基于前缀指令生成格式化的场景图文本序列（包含实体标签、关系谓词、分隔符标记）
2. **实体定位模块（Entity Grounding Module）**：对生成的实体标记序列预测边界框，通过 Relation-aware Token 与图像特征交叉注意力精确定位实体。使用多层 Transformer 解码器（最优 L=6），对实体查询 Q 与图像特征 Z_v 做交叉注意力
3. **类别转换模块（Category Conversion Module）**：将 VLM 生成的开放词汇预测映射到目标数据集定义的标准类别上，通过类别加权放大匹配类别得分，支持闭集评估

### 序列格式

生成的场景图序列使用特殊标记：[ENT] 分隔实体,[REL] 标记关系,格式如 "person [ENT] riding [REL] horse [REL] ..."。使用启发式规则从序列中解析关系三元组。

### 训练

- 多任务损失：标准下一标记预测语言建模损失 L_lm + 实体定位模块边界框回归损失 L_pos
- SGG 训练后，将 VLM 参数作为初始化权重迁移到下游 VL 任务（VQA、视觉定位、图像描述）
- 无需双阶段训练（no two-stage training），VLM 直接端到端学习 SGG

### 推理

- 控制输出序列长度（256/512/768/1024 tokens）平衡性能与速度
- 序列长度 768 时推理时间 4.8 秒/图，1024 时 6.9 秒/图

## 实验

### 开放词汇 SGG 主实验

**设定**：随机选择 50% 谓词类别作为 novel class 进行开放词汇评估。在 VG、PSG、OpenImage V6 三个基准上与 CaCao、SVRP、VS3、SGTR 对比。

| 数据集 | 设定 | 指标 | PGSG | 对比最优基线 | 提升 |
|--------|------|------|------|-------------|------|
| VG | SGCls | mR@100 (base+novel) | — | SVRP | **+6.5** |
| VG | SGCls | R@100 (base+novel) | — | SVRP | **+5.7** |
| VG | SGDet | mR@100 (all) | **2.9** | SGTR | — |
| VG | SGDet | R@100 (all) | **0.9** | SGTR | — |
| PSG | SGDet | mR@100 (all) | — | SGTR+ViT | **+9.4** |
| PSG | SGDet | R@100 (all) | — | SGTR+ViT | **+14.3** |
| PSG | SGDet | novel mR@100 | — | SGTR+ViT | **+4.5** |
| OIV6 | SGDet | mR@100 (all) | — | SGTR | **+5.3** |
| OIV6 | SGDet | R@100 (all) | — | SGTR | **+4.9** |

### 闭集 + 零样本三元组 SGG

- **PSG 零样本三元组 SGDet**：zR@100 = **21.2**（PGSG-c, close-set classifier），超越 ViT SGTR 基线 **4.1**，与 ResNet-101 PSGTR 持平
- **VG 零样本三元组 SGDet**：zR@100 超越 SSRCNN **4.0**，超越 ViT SGTR **3.6**

### 消融实验

- **实体定位模块层数 L**：L=6 时性能达到饱和（PSG mR@100=17.0, R@100=28.4），L=0 时仅 10.3/20.1
- **输出序列长度**：768 tokens 达到性能-速度平衡（PSG mR@100=24.9, R@100=18.0, 推理 4.8s/图）；512 tokens 性能下降但推理仅需 2.2s
- **场景图监督 vs 仅实体监督**：场景图监督显著提升 GQA 关系类（+1.9）和属性类（+1.8）准确率，仅实体监督无实质提升
- **序列质量**：256 tokens 时 96.1% 的有效三元组比例，768 tokens 时 96.0%

### 下游 VL 任务

| 任务 | 数据集 | 指标 | 初始模型 | PGSG | 提升 |
|------|--------|------|---------|------|------|
| VQA | GQA | 总体准确率 | 62.5 (BLIP) | **64.2** | **+1.7** |
| VQA | GQA | 关系类准确率 | 54.9 | **56.8** | **+1.9** |
| VQA | GQA | 属性类准确率 | 64.5 | **66.3** | **+1.8** |
| VQA | GQA | 对象类准确率 | 86.6 | **87.9** | **+1.3** |
| VQA | GQA (BLIPv2 ZS) | 总体 | 32.3 | **33.9** | **+1.6** |
| 视觉定位 | RefCOCO val | acc | 83.1 | **86.0** | **+2.9** |
| 视觉定位 | RefCOCO testA | acc | 86.0 | **88.9** | **+2.9** |
| 视觉定位 | RefCOCO testB | acc | 77.0 | **82.4** | **+5.4** |
| 视觉定位 | RefCOCO+ val | acc | 77.1 | **79.8** | **+2.7** |
| 视觉定位 | RefCOCO+ testA | acc | 83.1 | **84.3** | **+1.2** |
| 视觉定位 | RefCOCO+ testB | acc | 69.8 | **72.3** | **+2.5** |
| 视觉定位 | RefCOCOg val | acc | 74.3 | **77.8** | **+3.5** |
| 图像描述 | COCO | CIDEr | 132.1 | 131.2 | -0.9 |
| 图像描述 | COCO | SPICE | 23.6 | **23.9** | **+0.3** |

## 局限性与不足

1. **闭集 SGG 性能欠佳**：受限于 VLM 视觉骨干（ViT-B/16, 384x384 分辨率）较传统 SGG 方法（ResNet-101 FPN, 800x1333）的低输入分辨率，在标准闭集 SGG 设定下性能与 SOTA 仍有差距
2. **标注噪声敏感**：直接用于 SGG 训练的一阶段训练方式限制了对小目标的检测能力
3. **VLM 架构局限**：仅基于 BLIP/BLIPv2 进行评估，未探索更多 VL 模型和任务

## 结论

PGSG 是首个将 VLM image-to-text generation 用于开放词汇 SGG 的完整框架，实现了从 pixels 到 scene graph 的直接生成。核心优势在于：（1）开放词汇谓词泛化能力；（2）统一 SGG 与下游 VL 任务，显式关系建模为 VL 推理带来实质性增益。对比同期工作 OvSGTR（ECCV 2024），PGSG 聚焦谓词级开放词汇（predicate open-vocabulary），而 OvSGTR 扩展到实体-关系联合开放词汇（fully open-vocabulary）。

## 关键结果汇总

- **开放词汇 SGG（PSG）**：mR@100 较 SGTR+ViT 提升 **9.4**，R@100 提升 **14.3**
- **零样本三元组 SGG（PSG）**：zR@100 = **21.2**，超越 ViT SGTR 基线 **4.1**
- **GQA VQA**：总体准确率 **64.2%**（+1.7 over BLIP baseline）
- **RefCOCO 视觉定位**：testB 提升 **5.4** 个百分点（77.0 → 82.4）
