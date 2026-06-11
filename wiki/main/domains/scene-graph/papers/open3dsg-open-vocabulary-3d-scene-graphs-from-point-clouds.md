---
title: "Open3DSG: Open-Vocabulary 3D Scene Graphs from Point Clouds with Queryable Objects and Open-Set Relationships"
authors: "Sebastian Koch, Narunas Vaskevicius, Mirco Colosi, Pedro Hermosilla, Timo Ropinski"
year: 2024
venue: "CVPR 2024"
arxiv: null
doi: null
code: "kochsebastian.com/open3dsg"
project: "kochsebastian.com/open3dsg"
domain: scene-graph
tags: [open-vocabulary, 3D-scene-graph, point-cloud, zero-shot, LLM, VLM-distillation]
evidence_level: full-paper
status: active
raw_sources:
  - ../../../sources/scene-graph/2024-CVPR-Open3DSG-Open-Vocabulary-3D-Scene-Graphs-from-Point-Clouds.pdf
  - ../../../sources/scene-graph/2024-CVPR-Open3DSG-Open-Vocabulary-3D-Scene-Graphs-from-Point-Clouds.txt
aliases: [Open3DSG, Open-Vocabulary 3D Scene Graphs]
---

## Provenance

- **来源文件**: `sources/scene-graph/2024-CVPR-Open3DSG-Open-Vocabulary-3D-Scene-Graphs-from-Point-Clouds.pdf`
- **提取文本**: `sources/scene-graph/2024-CVPR-Open3DSG-Open-Vocabulary-3D-Scene-Graphs-from-Point-Clouds.txt`

# Open3DSG: Open-Vocabulary 3D Scene Graphs from Point Clouds with Queryable Objects and Open-Set Relationships

**Sebastian Koch** (Bosch Center for AI / University of Ulm), **Narunas Vaskevicius** (Bosch), **Mirco Colosi** (Bosch Corporate Research), **Pedro Hermosilla** (TU Vienna), **Timo Ropinski** (University of Ulm)

**CVPR 2024**

## Summary

Open3DSG 是首个从 **3D 点云**直接进行**开放词汇 3D 场景图预测**的方法。核心思路：将 3D 场景图预测骨干网络的输出特征与 2D 视觉语言基础模型的特征空间对齐，实现零样本开放词汇场景图生成。关键区别：不仅预测开放词汇物体类别，还可预测**开放集关系**（不限预定义标签集）。

## Contributions

1. **首个 3D 点云开放词汇场景图方法**：从点云直接预测 open-vocabulary 3D scene graphs
2. **可查询交互式表示**：推理时可灵活查询任意物体类、提示关系
3. **开放集关系预测**：通过 LLM（InstructBLIP）生成不限于预定义标签的关系描述
4. **VLM→3D GNN 知识蒸馏**：将 2D VLM (OpenSeg + InstructBLIP) 特征蒸馏至 3D GNN

## Method

### 框架概览

两阶段推理流程：

1. **物体查询**：通过 CLIP 文本编码器编码开放词汇查询，与蒸馏后的 3D 节点特征计算余弦相似度
2. **关系预测**：将蒸馏的边特征 + 预测的物体类别作为上下文，送入 InstructBLIP（Qformer → LLM）生成关系描述

### 训练阶段

1. **场景图构建** (Sec 3.1)：从点云 + 类无关实例分割 → 每个实例提取 PointNet 特征 → GNN 消息传递
2. **2D 特征提取** (Sec 3.2)：
   - **物体特征**：OpenSeg 像素级语言对齐嵌入，多视图平均池化
   - **关系特征**：InstructBLIP 图像编码器提取关系区域特征，多尺度 + 多视图融合
3. **图蒸馏** (Sec 3.3)：余弦相似度损失对齐 2D VLM 特征与 3D GNN 特征
4. **2D-3D 特征融合**：推理时如果有 2D 图像可用，对 2D 和 3D 特征做平均池化融合

### 关键技术选择

- 使用 **OpenSeg** 而非 CLIP 作为物体特征提取器（像素级 vs 全局特征）
- 使用 **InstructBLIP**（BLIP 架构 + Qformer + LLM）而非 CLIP 进行关系预测（CLIP-like 模型缺乏组合理解）
- 使用 **BERT** 将 LLM 生成的关系映射到闭集标签进行评估

## Experiments

### 数据集

- **训练**：ScanNet（提供高质量点云和较大 FOV 的 2D 帧）
- **评估**：3DSSG（唯一提供 3D 场景图标签的数据集，27 关系类，160 物体类）

### 闭集评估 (Tab 1, 3DSSG)

| 方法 | Obj R@5 | Obj R@10 | Pred R@3 | Pred R@5 | Rel R@50 | Rel R@100 |
|------|---------|----------|---------|---------|---------|----------|
| 3DSSG (fully-sup) | 0.68 | 0.78 | 0.89 | 0.93 | 0.40 | 0.66 |
| SGRec3D (fully-sup) | 0.80 | 0.87 | 0.97 | 0.99 | 0.89 | 0.91 |
| **Open3DSG (zero-shot)** | **0.57** | **0.68** | **0.63** | **0.70** | **0.64** | **0.66** |

对比基准：CLIP naive (Rel R@50=0.02)、OpenSeg+CLIP (0.05)、Caption-based (0.30)。

### 长尾类评估 (Tab 2)

| 方法 | Obj R@5 Head | Obj R@5 Body | Obj R@5 Tail | Pred R@3 Head | Pred R@3 Body | Pred R@3 Tail |
|------|-------------|-------------|-------------|--------------|--------------|--------------|
| SGRec3D | 0.92 | 0.78 | 0.24 | 0.97 | 0.96 | 0.65 |
| **Open3DSG** | **0.60** | **0.50** | **0.42** | **0.38** | **0.29** | **0.57** |

核心优势：在尾部类和尾部关系上显著优于全监督方法，零样本方法不受训练分布偏置影响。

### 消融研究 (Tab 3)

| 设置 | Obj R@5 | Obj mR@5 | Pred R@3 | Pred mR@3 |
|------|---------|---------|---------|----------|
| 2D only | 0.37 | 0.37 | 0.67 | 0.19 |
| 3D only | 0.46 | 0.25 | 0.60 | 0.33 |
| **2D-3D ensemble** | **0.57** | **0.45** | **0.63** | **0.37** |
| +GT Objects | 1.00 | 1.00 | 0.64 | 0.38 |
| +Supervised Rels | 0.59 | 0.46 | 0.76 | 0.44 |

- 2D-3D 融合优于各自单独的方案
- GT 物体标签对比自动查询影响很小 → 关系预测对物体预测错误鲁棒
- 少量监督微调（~100 标签/类）可进一步提升关系预测

## Key Insights

1. **CLIP 不适合关系预测**：Tab 1 中 OpenSeg+CLIP 关系 Recall 仅 0.05-0.08，验证了 CLIP-like 模型的组合理解短板
2. **LLM 生成式关系预测更有效**：即使零样本，Open3DSG 关系 R@100=0.66，接近首个监督方法 3DSSG (0.66)
3. **零样本天然抗长尾**：Tail 类物体 R@5=0.42，远超 SGRec3D (0.24) 和 VL-SAT (0.31)
4. **2D-3D 特征互补**：2D 对小型物体好，3D 对大型/形状特征显著物体好

## Limitations

1. 开放集关系预测仍有挑战，QLM 生成的关系未必精确
2. 闭集指标无法充分体现开放词汇方法的潜力
3. 需 3DSSG 数据集用于量化评估（图像 FOV 小，影响 2D 特征质量）

## Related Papers

- [[ccl-3dsgg-clip-driven-open-vocabulary-3d-scene-graph-generation|CCL-3DSGG]] — CLIP-Driven Open-Vocabulary 3D Scene Graph Generation
- [[conceptgraphs-open-vocabulary-3d-scene-graphs-for-perception-and-planning|ConceptGraphs]] — 并发工作，使用 2D VLM 和 captioning 模型预测场景图
- [[lang3dsg-language-based-contrastive-pre-training-for-3d-scene-graph-prediction|Lang3DSG]] — 同一作者的对比预训练方法
- [[sgrec3d-self-supervised-3d-scene-graph-learning|SGRec3D]] — 同一作者的自监督方法
- [[fungraph-functionality-aware-3d-scene-graphs|FunGraph]] — 3D 场景图的功能性扩展
- [[3d-spatial-multimodal-knowledge-accumulation-scene-graph-prediction-point-cloud|SMKA]] — 3D 点云场景图预测
