---
title: "Learning to Generate Language-supervised and Open-vocabulary Scene Graph using Pre-trained Visual-Semantic Space (VS³)"
type: paper
domain: scene-graph
status: active
created: 2026-06-08
updated: 2026-06-08
tags:
  - scene-graph-generation
  - language-supervised-sgg
  - open-vocabulary-sgg
  - visual-semantic-space
  - CLIP-GLIP
  - weakly-supervised-sgg
  - CVPR-2023
raw_sources:
  - ../../../sources/scene-graph/2023-CVPR-Learning-to-Generate-Language-supervised-and-Open-vocabulary-Scene-Graph-VS3.pdf
  - ../../../sources/scene-graph/2023-CVPR-Learning-to-Generate-Language-supervised-and-Open-vocabulary-Scene-Graph-VS3.txt
related_pages:
  - fast-contextual-scene-graph-generation.md
  - squat-selective-quad-attention-scene-graph-generation.md
evidence_level: full-paper
paper:
  title: "Learning to Generate Language-supervised and Open-vocabulary Scene Graph using Pre-trained Visual-Semantic Space"
  abbreviated: "VS³"
  authors:
    - Yong Zhang
    - Yingwei Pan
    - Ting Yao
    - Rui Huang
    - Tao Mei
    - Chang-Wen Chen
  affiliations:
    - The Chinese University of Hong Kong, Shenzhen
    - HiDream.ai Inc.
    - The Hong Kong Polytechnic University
  year: 2023
  venue: CVPR 2023
  doi: null
  arxiv: null
  code: https://github.com/gitzyong812/VS3_CVPR23
  url: https://openaccess.thecvf.com/content/CVPR2023/html/Zhang_Learning_To_Generate_Language-Supervised_and_Open-Vocabulary_Scene_Graph_Using_Pre-Trained_CVPR_2023_paper.html
---

# VS³: Language-supervised and Open-vocabulary Scene Graph Generation

## 核心思想

提出利用预训练的视觉-语义空间（VSS，来自 GLIP）一次性解决 SGG 两大瓶颈：
1. **昂贵的标注成本**——通过解析图像语言描述 + VSS 短语定位，廉价获取弱场景图监督
2. **封闭集限制**——通过 VSS 的开放词汇泛化能力，实现 novel object 检测和 open-vocabulary SGG

核心设计：将 GLIP 框架扩展关系识别模块，构成 VS³ 模型。训练时冻结图像/文本编码器保持 VSS 不变，仅微调跨模态融合模块和关系识别模块。

## 方法

### VS³ 模型架构（基于 GLIP）

- **文本提示（Text Prompt）**：检测文本格式 `name(c1). name(c2). ... name(c|Co|).`，将目标检测重构为短语定位
- **图像编码器**：Swin Transformer 主干（继承 GLIP）
- **文本编码器**：BERT（继承 GLIP）
- **跨模态融合模块**：实现 region-word 特征通信（继承 GLIP，可微调）
- **关系嵌入模块**：从视觉和空间两个维度构建 pair 关系表示
  - 视觉特征：`pair_visual = f_diff(o_i - o_j) + f_sum(o_i + o_j)`，两层 MLP
  - 空间特征：拼接 subject/object 的归一化框、中心坐标差/距离/角度/面积/交并比等 9 维特征
- **关系预测**：对每个 pair 预测 relateness score（Sigmoid MLP, focal loss）和 semantic label（Softmax MLP, CE loss）

### 语言监督数据获取

1. 语义图解析：用 Stanford Scene Graph Parser 将语言描述解析为 `SG_text = {O_text, R_text}`
2. 语义图定位：用预训练 GLIP 将 noun phrase 与图像区域对齐，获取 grounding boxes
3. 后处理：NMS 合并相同 label + 高 IoU 的框

### 开放词汇迁移

- 训练时文本提示包含 base categories（70% VG150 类别）
- 推理时切换为包含 novel categories（30% 额外类别）的文本提示
- 新颖类别通过与 base category 语义相似的 embedding 找到对齐区域
- 关系特征（视觉+空间）通常是 class-agnostic，不会受 novel object 影响

## 实验结果

### 全监督 SGG（VG150，SGDET 协议）

| 模型 | 主干 | R@20 | R@50 | R@100 |
|------|------|------|------|-------|
| HL-Net (SOTA) | RX-101 | 26.0 | 33.7 | 38.1 |
| **VS³** | Swin-T | **26.1** | **34.5** | **39.2** |
| **VS³** | Swin-L | **27.8** | **36.6** | **41.5** |

消融：去掉 visual 特征 R@100 从 39.2↓36.7，去掉 spatial 特征 R@100 从 39.2↓37.8，视觉特征贡献更大。

### 语言监督 SGG

| 设置 | 模型 | R@20 | R@50 | R@100 |
|------|------|------|------|-------|
| **Unlocalized graph** | Li et.al (SOTA) | 9.57 | 11.80 | 13.15 |
| | **VS³(Swin-L+FreqBias)** | **22.18** | **29.81** | **34.96** |
| **VG caption** | Li et.al (SOTA) | 8.90 | 10.93 | 12.14 |
| | **VS³(Swin-L)** | **13.01** | **17.38** | **20.54** |
| **COCO caption** | Li et.al (SOTA) | 5.42 | 6.74 | 7.62 |
| | **VS³(Swin-L)** | **6.04** | **8.15** | **9.90** |

> 在 Unlocalized graph 设置下，VS³ 语言监督结果（R@100=34.96）甚至超过了许多全监督方法。

### 开放词汇 SGG（全监督）

| 模型 | Ov-SGG PREDCLS R@50/100 | ZsO-SGG PREDCLS R@50/100 | Ov-SGG SGDET R@50/100 | ZsO-SGG SGDET R@50/100 |
|------|---------------------------|---------------------------|------------------------|--------------------------|
| SVRP (SOTA) | 47.62 / 49.94 | 45.75 / 48.39 | — | — |
| **VS³(Swin-T)** | 50.10 / 52.05 | 46.91 / 49.13 | 15.07 / 18.73 | 10.08 / 13.65 |
| **VS³(Swin-L)** | **55.88 / 58.18** | **54.44 / 57.35** | **23.13 / 28.49** | **21.51 / 27.62** |

> VS³ 首次报告了开放词汇 SGG 在 SGDET 协议下的结果（之前方法因两阶段检测器无法处理开放词汇检测而忽略 SGDET）。

### 开放词汇 + 语言监督 SGG（首个基准）

| 模型 | SG 监督 | Ov-SGG SGDET R@50/100 | ZsO-SGG SGDET R@50/100 |
|------|---------|-----------------------|------------------------|
| VS³(Swin-T) | VG caption | 7.61 / 9.60 | 4.06 / 5.58 |
| VS³(Swin-T) | COCO caption | 4.39 / 5.63 | 3.65 / 4.73 |
| VS³(Swin-L) | VG caption | **12.98 / 16.29** | **10.71 / 13.70** |
| VS³(Swin-L) | COCO caption | 6.76 / 8.45 | 6.26 / 7.89 |

> 本文首次提出语言监督 + 开放词汇 SGG 这一新设定并建立基准。

## 关键洞见

1. **预训练 VSS 的复用**：冻结视觉/文本编码器保持 VSS 不变是成功的关键；微调会退化预训练空间
2. **语言监督质量的重要性**：Unlocalized graph > VG caption > COCO caption，说明 region-level 密集描述比 image-level 描述更有效
3. **语义解析质量的影响**：Advanced SG parser 优于 Simple parser（COCO caption 下 R@100 从 7.93→8.62）
4. **多 caption 互补**：使用全部 5 个 COCO captions 比单一 caption 提升约 10%
5. **SGDET 首次可行于开放词汇**：VS³ 的一阶段检测范式避免了传统两阶段检测器的 proposal 瓶颈

## 局限

- 语言监督结果偏向简单 predicate（如 on, of），复杂关系预测仍不足
- 跨数据域（COCO→VG150）时性能显著下降（domain shift 问题）
- 需外部预训练模型（GLIP）支撑，依赖其预训练数据的质量和覆盖度

## 关联

- **基础模型：** GLIP（Grounded Language-Image Pre-training）提供 VSS 基础
- **相关任务：** 开放词汇 SGG（对比 SVRP [He et al., ECCV 2022]），语言监督 SGG（对比 Li et al. 2021, SGNLS）
- **同领域对比：** 相比 MOTIFS/VCTREE/HL-Net 等两阶段方法，VS³ 采用一阶段范式 + 预训练知识迁移，在几乎所有设置下取得 SOTA
