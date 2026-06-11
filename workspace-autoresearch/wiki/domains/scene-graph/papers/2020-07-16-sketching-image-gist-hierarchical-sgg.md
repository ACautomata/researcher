---
title: "Sketching Image Gist: Human-Mimetic Hierarchical Scene Graph Generation"
authors:
  - Wenbin Wang
  - Ruiping Wang
  - Shiguang Shan
  - Xilin Chen
venue: ECCV 2020
arxiv: "2007.08760"
code: "https://github.com/Kenneth-Wong/het-eccv20"
doi: ""
tags:
  - scene-graph-generation
  - hierarchical
  - ECCV-2020
  - key-relation
  - human-mimetic
year: 2020
evidence_level: full-paper
domain: scene-graph
date_captured: 2026-06-10
---

# Sketching Image Gist: Human-Mimetic Hierarchical Scene Graph Generation

**Wenbin Wang, Ruiping Wang, Shiguang Shan, Xilin Chen** — ECCV 2020

## 一句话总结

提出**类人层次场景图生成**框架，构建层次化实体树（HET）模拟人类场景解析的感知优先级，并设计 Relation Ranking Module（RRM）从视觉显著性和物体大小中学习关系优先级排序，使得生成的场景图能优先捕捉"图像要点"（image gist）——即人类最想传达的主要事件和关键关系。

## 核心动机

1. **现有 SGG 方法缺乏重要性感知**：所有关系被平等对待，导致 top 关系常常是跨图像通用的琐碎关系（如 `⟨woman, has, head⟩`），而非图像特有的关键关系。
2. **人类场景解析具有层次性**：人类描述场景时先描述主要事件（如"一个骑自行车的人"），再描述细节（如"戴着头盔"）。这种感知优先级形成天然层次结构。
3. **视觉显著 ≠ 语义重要**：人类注视的对象（视觉显著）不一定构成图像要点（image gist），95% 的描述对象会被注视，但只有 48% 的注视对象会被描述。

## 方法

### 1. Hierarchical Entity Tree (HET)

构建多分支树结构，模拟人类场景解析的感知层级：

- **构造规则**：按物体大小降序排列，通过交并比（IoU）判断父子关系
- **父节点选择**：Intersection-first Strategy (IFS) — 选择对子节点包含比例最大的候选
- **阈值 T=0.9**：大阈值减少错误层次连接，即使导致更多节点直接连到根节点
- 虚拟根节点 `o0` 代表整张图像

### 2. Hybrid-LSTM

双编码器架构，编码 HET 中的两种上下文：

- **Bi-TreeLSTM**：编码层次上下文（父-子、子-父双向传递）
- **Bi-LSTM**：编码兄弟节点上下文（同一父节点下的多子节点）
- 输入：视觉特征 vi + 语义嵌入 zi（GloVe 初始化）
- **实体上下文编码**：预测实体信息
- **关系上下文编码**：推理关系

### 3. Relation Ranking Module (RRM)

从客观特征学习人类主观关系重要性评估：

- **Saliency Map (SM)**：DSS 预测像素级视觉显著性图
- **Area Map (AM)**：像素级面积图，每个位置赋值为覆盖该位置的最小物体归一化面积
- 两者通过自适应平均池化对齐，与 Faster-RCNN conv5 特征图做 Hadamard 乘积
- **排名得分预测**：每个 triplet 的 visual + geometric 特征 → BiLSTM → 排名得分 t_{ij}
- **最终排名置信度**：φ_{ij} = s_i · s_j · s_{ij} · t_{ij}

### 4. VG-KR 数据集

扩展 VG 以获取关键关系标注：

- 从 MSCOCO caption 中通过 Stanford Scene Graph Parser 提取关系三元组 → 关键关系集合
- 与 VG 关联，过滤后得到 VG-KR：26,992 张图像，200 物体类别，80 谓词类别
- 90%+ 图像少于 5 个关键关系
- 语义丰富的动词（throwing, brushing, sniffing）更可能成为关键关系

## 实验与结果

### Scene Graph Generation (VG150)

| 方法 | PREDCLS R@20/50/100 | SGCLS R@20/50/100 | SGGEN R@20/50/100 |
|---|---|---|---|
| MOTIFS [51] | 58.5 / 65.2 / 67.1 | 32.9 / 35.8 / 36.5 | 21.4 / 27.2 / 30.3 |
| VCTree-SL [38] | 59.8 / 66.2 / 67.9 | 35.0 / 37.9 / 38.6 | 21.7 / 27.7 / 31.1 |
| **HetH (Ours)** | **59.8 / 66.3 / 68.1** | 33.8 / 36.6 / 37.3 | 21.6 / 27.5 / 30.9 |

### Scene Graph Generation (VG200)

| 方法 | PREDCLS R@20/50/100 | SGCLS R@20/50/100 | SGGEN R@20/50/100 |
|---|---|---|---|
| MOTIFS | 52.5 / 59.0 / 61.0 | 24.5 / 26.7 / 27.4 | 15.2 / 19.9 / 22.8 |
| VCTree-SL | 51.9 / 58.4 / 60.3 | 24.2 / 26.5 / 27.1 | 14.7 / 19.5 / 22.5 |
| **HetH** | **53.6 / 60.1 / 61.8** | **25.0 / 27.2 / 27.8** | **15.7 / 20.4 / 23.4** |

### Key Relation Prediction (VG-KR, Triplet Match)

| 方法 | PREDCLS kR@1/5 | SGCLS kR@1/5 |
|---|---|---|
| VCTree-SL | 11.4 / 30.2 | 5.7 / 14.2 |
| MOTIFS | 11.3 / 30.0 | 5.9 / 14.5 |
| HetH | 11.6 / 30.4 | 6.1 / 15.1 |
| MOTIFS-RRM | 16.7 / 33.8 | 8.6 / 16.4 |
| **HetH-RRM** | **17.5 / 35.0** | **9.2 / 17.1** |

### Key Relation Prediction (VG-KR, Tuple Match)

| 方法 | PREDCLS kR@1/5 | SGCLS kR@1/5 |
|---|---|---|
| HetH-RRM | **28.9 / 59.1** | **14.6 / 27.3** |

### VRD

| 方法 | RELDET R@50 (k=1) | RELDET R@100 (k=1) | PHRDET R@50 (k=1) | PHRDET R@100 (k=1) |
|---|---|---|---|---|
| HetH | 22.42 | 24.88 | 30.69 | 35.59 |

### Image Captioning 下游任务

输入不同数量的 top 关系进行 captioning（VG-KR 数据集）：

| 输入关系数 | 方法 | B@4 | CIDEr | SPICE |
|---|---|---|---|---|
| 5 | HetH-Freq | 28.0 | 84.4 | 17.2 |
| 5 | HetH | 30.5 | 92.6 | 18.5 |
| 5 | **HetH-RRM** | **31.5** | **97.5** | **19.1** |
| 2 | HetH-RRM | 30.4 | 92.2 | 18.4 |

## 关键发现

1. **层次结构优于平面结构**：HET 多分支树优于 MOTIFS 的链式结构，与 VCTree 二叉树的性能可比但更可解释
2. **数据量少时层次结构更鲁棒**：VG200 上 HetH 超越 VCTree-SL（动态调优二叉树），说明固定层次结构在数据不足时更稳定
3. **RRM 可迁移**：MOTIFS-RRM 也获得显著提升，证明 RRM 不是定制的
4. **层次深度与关系重要性负相关**：深度 (2,2) 和 (2,3) 的关系更重要，(3,3) 更次要
5. **RRM 结合 SM 和 AM 效果最佳**：单独使用 SM 或 AM 均有提升，两者结合最好

## 消融实验要点

- **IFS vs AFS**：IFS 优于 AFS（父节点选择策略）
- **Bi-TreeLSTM 弃用 → 退化到 MOTIFS**：证明层次编码的必要性
- **RRM-Base vs RRM-SM vs RRM-AM vs RRM-full**：SM 效果略优于 AM，full 版本最优

## 局限性

1. **固定层次结构**：HET 由人工规则构建（根据物体大小和 IoU），无法像 VCTree-SL 那样动态优化
2. **2D 遮挡问题**：2D 图像中的遮挡导致错误的层次连接，影响 SGCLS/SGGEN 协议下的表现
3. **EP vs SP 的 trade-off**：Structured Prediction（只预测父-子、兄弟间关系）速度快但性能略降

## 相关链接

- [arXiv](https://arxiv.org/abs/2007.08760)
- [Code](https://github.com/Kenneth-Wong/het-eccv20)
- [VCTree (CVPR 2019)](../papers/2019-06-15-VCTree-Learning-to-Compose-Dynamic-Tree-Structures-for-Visual-Contexts.md) — 层次化上下文建模的早期工作，二叉树动态学习
- [MOTIFS (CVPR 2018)](../papers/2018-CVPR-Neural-Motifs-Scene-Graph-Global-Context.md) — 序列化 LSTM 建模关系上下文
