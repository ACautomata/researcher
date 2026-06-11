---
title: "Knowledge-Embedded Routing Network for Scene Graph Generation"
type: paper
domain: scene-graph
status: active
created: 2026-06-10
updated: 2026-06-10
tags:
  - CVPR-2019
  - foundational
  - knowledge-routing
  - commonsense-knowledge
  - long-tail
  - debiasing
raw_sources:
  - raw/sources/2019-CVPR-knowledge-embedded-routing-network-sgg.pdf
  - raw/sources/2019-CVPR-knowledge-embedded-routing-network-sgg.txt
paper:
  title: "Knowledge-Embedded Routing Network for Scene Graph Generation"
  authors:
    - Tianshui Chen
    - Weihao Yu
    - Riquan Chen
    - Liang Lin
  year: 2019
  venue: CVPR 2019
  code: https://github.com/HCPLab-SYSU/KERN
classification:
  label: Knowledge-Embedded Scene Graph Generation
  task:
    - Scene Graph Generation (SGGen)
    - Scene Graph Classification (SGCls)
    - Predicate Classification (PredCls)
  method_family: Knowledge-Embedded Graph Routing
  modality: RGB
  datasets:
    - Visual Genome (VG)
  metrics:
    - R@50 / R@100
    - mR@50 / mR@100
evidence_level: full-paper
---

## Citation

Chen, T., Yu, W., Chen, R., Lin, L. "Knowledge-Embedded Routing Network for Scene Graph Generation." CVPR, 2019. Sun Yat-Sen University & DarkMatter AI Research.

## One-Sentence Contribution

首次将统计知识显式编码为结构化知识图，通过图传播网络（KERN）将其嵌入 SGG 流程，有效利用物体对-关系共现统计来正则化关系预测语义空间，并提出了 mR@K（mean Recall@K）作为更公平的长尾评估指标。

## Problem Setting

- **目标**：利用物体对与关系之间的统计共现信息，显式地正则化关系预测的语义空间，改善长尾关系预测性能
- **挑战**：
  - 现实世界关系分布严重不均衡（长尾），高频关系（如 "on", "wearing"）占据大部分样本，低频关系性能跌落严重
  - 已有方法（如 SMN）隐式挖掘统计知识（通过 LSTM 编码全局上下文），但未将其显式表示为结构化图
  - 现有 R@K 指标偏袒高频关系，不能全面反映各个关系的预测质量
- **设定**：经典全监督 SGG，使用 VG 数据集（108,077 张图像，150 个物体类别，50 个关系类别），沿用 [30] 的 train/test split

## Method

### 架构概览

KERN 基于 Faster R-CNN 检测器 → 构建两阶段图路由网络：**Object Graph → Relationship Graph**，流程如下：

1. **Object Proposal**：Faster R-CNN（VGG16 backbone）检测物体区域
2. **Object Graph**：根据统计物体共现矩阵构建区域间图，通过 GGNN 传播节点消息学习上下文特征表示，预测每个区域的物体类别
3. **Relationship Graph**：对每对物体（oi, oj），构建关系图 —— 节点为物体和关系，边为物体-关系共现概率 —— 通过另一个 GGNN 传播消息，预测关系标签

### Knowledge Graph Construction

- **Object co-occurrence knowledge**：统计 VG 训练集中每对物体共现频率，构建 150×150 的共现矩阵，作为 object graph 的边权重
- **Relationship correlation knowledge**：对每对物体类别 (s, o)，统计该物体对下每种关系 r 的出现概率，构建 |R|×1 的概率向量作为关系图的边权重
  - 例如：对于物体对 (person, bicycle)，关系 "ride" 的概率远高于 "sit on"

### Key Components

#### Object Graph (OG)

- 节点：每个检测到的区域 bi，初始特征为 RoI feature 和 bbox 特征拼接
- 边：基于共现矩阵的边权重，两个物体类别共现频率越高，边权重越大
- GGNN：迭代 3 步，传播消息得到上下文物体特征

#### Relationship Graph (RG)

- 对每个物体对 (oi, oj) 构建一个独立的图：
  - 节点：oi, oj 和所有 K 个候选关系
  - 边：oi → rk 的权重 = 给定 oi 时关系 rk 的条件概率；oj → rk 同理
  - 节点间相互连接以探索物体与关系的交互
- 使用另一个 GGNN 迭代 3 步传播消息

### 提出的新评估指标：mR@K

- **mR@K（mean Recall@K）**：先计算每个关系的 R@K，再对所有关系取平均
- 弥补 R@K 偏袒高频关系的不足，更公平地评估所有关系的性能
- 同时报告 with constraint（每对物体最多一个关系）和 without constraint 的结果

## Experiments

### 设置

- **数据集**：Visual Genome（VG），108,077 张图像，沿用 [30] 的 train/test split，使用最频繁的 150 个物体类别和 50 个关系类别
- **Backbone**：Faster R-CNN + VGG16（ImageNet 预训练）
- **检测器训练**：SGD，batch size=18，momentum=0.9，weight decay=0.0001，初始 lr=0.001，mAP 停滞时除以 10
- **GGNN 训练**：Adam，batch size=2，momentum=(0.9, 0.999)，初始 lr=0.00001，recall 停滞时除以 10；GGNN 迭代步数 = 3
- **输入图像尺寸**：592×592，anchor scales 参考 YOLO-9000
- **冻结检测器卷基层后训练**全连接层和 GGNN
- **任务**：Predicate Classification (PredCls)、Scene Graph Classification (SGCls)、Scene Graph Generation (SGGen)

### Baseline 方法

- **IMP [30]** — Iterative Message Passing
- **IMP+ [30, 33]** — IMP 使用更好的检测器
- **AE [23]** — Associative Embedding
- **FREQ [33]** — 直接预测每对物体的最频繁关系
- **SMN [33]** — Stacked Motif Networks（当时 SOTA）

### 评估协议

- R@50 / R@100：标准 Recall@K
- mR@50 / mR@100：提出的新指标，平均每个关系的 Recall@K
- 两种设置：with constraint（每对物体一个关系）和 without constraint（允许多个关系）

## Results

### 主要结果（mR@K，Table 1）

**SGCls** 任务（最相关），**without constraint** 设置：
| 方法 | mR@50 | mR@100 |
|------|-------|--------|
| SMN [33]（SOTA） | 15.4 | 20.6 |
| **KERN (Ours)** | **19.8** | **26.2** |
| 相对提升 | +28.6% | +27.2% |

**SGGen** 任务，**without constraint** 设置：
| 方法 | mR@50 | mR@100 |
|------|-------|--------|
| SMN [33] | 9.3 | 12.9 |
| **KERN (Ours)** | **11.7** | **16.0** |
| 相对提升 | +25.8% | +24.0% |

**Mean mR**（三任务平均），without constraint：**26.5%** vs SMN 20.6%（相对提升 **28.6%**）
**Mean mR**，with constraint：**11.7%** vs SMN 9.0%（相对提升 **30.0%**）

### 主要结果（R@K，Table 2）

**Mean R**（三任务平均），without constraint：**55.4%** vs SMN 54.7%
**Mean R**，with constraint：**44.1%** vs SMN 43.7%

### 消融实验（Table 3）

- **Full model** (with constraint)：Mean mR = 11.7%, Mean R = 44.1%
- **w/o relationship correlation (w/o rk)** ：Mean mR = 7.9%, Mean R = 40.6%
- **w/o relationship & object correlation (w/o rk & ok)**：Mean mR = 7.6%, Mean R = 40.3%

消融表明：关系相关性知识（relationship correlation）对 mR 贡献最大（11.7% → 7.9%），物体共现知识（object correlation）也有辅助作用（7.9% → 7.6%）。

### 关键发现

- **长尾关系改善显著**：KERN 在低频关系上的 R@50 提升远高于高频关系（如对某些低频关系 R@50 提升超 20%）
- **mR@K vs R@K 的差距**：mR@K 提升 28.6%，而 R@K 仅提升 ~1%，说明 KERN 主要改善了低频关系预测，对高频关系基本持平
- FREQ baseline（直接取最频繁关系）在 PredCls 的 R@100 达到 37.3%，高于多数深度方法，验证了统计知识的重要作用

## Limitations

- **依赖静态统计知识**：共现矩阵和关系-物体对概率是从训练集统计得到的，没有考虑图像中的具体视觉上下文
- **独立处理每对物体**：对每个物体对分别构建关系图，计算复杂度为 O(n²)，对大场景效率有限
- **知识图固定**：统计知识在训练后固定，不能根据数据自适应更新
- **仅限固定关系集合**：只能预测预定义的 50 个关系类别，不具备零样本能力

## Reusable Claims

1. **统计共现知识显式编码优于隐式学习**：显式构建物体对-关系共现图（KERN）在 mR@K 上比隐式编码（SMN）提升 28.6%，验证了结构化知识对长尾 SGG 的有效性
2. **mR@K 是比 R@K 更全面的 SGG 评估指标**：KERN 在 R@K 上仅提升 ~1%，但在 mR@K 上提升 28.6%，表明 R@K 掩盖了低频关系性能差异
3. **FREQ baseline 的强竞争力**：单纯取最频繁关系的 FREQ baseline 超过多数深度方法，说明 SGG 中的统计偏置既是问题也是可用的正则化信号
4. **知识图路由作为模型结构先验**：将领域知识（共现统计）编码为图结构并作为传播网络的先验，是融合先验知识的有效范式

## Connections

- **前置工作**：SMN [33] 隐式编码统计知识，KERN 将其显式化并改进；FREQ [33] 展示了统计共现的强正则化作用
- **后续工作**：后续大量长尾 SGG 工作（如 TDE [2023 TPAMI]、CFA [2023]）均将 KERN 作为重要 baseline；提出的 mR@K 指标成为 SGG 长尾评估的标准指标（几乎所有后续长尾 SGG 论文都报告 mR@K）
- **同领域**：[Multi-Prototype Space Learning for Commonsense-Based SGG](2024) 继承了使用外部知识（如 WordNet）辅助关系的思路，但用多原型空间替代了固定统计图
- **相关概念**：利用外部结构化知识（WordNet 等）辅助视觉理解，与 [Visual Commonsense Driven Knowledge Refinements for SGG](visual-commonsense-knowledge-refinements-sgg.md) 共享知识驱动范式

## Open Questions

1. 统计知识如何与视觉上下文动态融合，而不是固定地作为先验？
2. KERN 的 O(n²) 复杂度在大规模场景中的优化方案是什么？
3. 知识图是否可以端到端地学习更新（meta-learning 或 continuous learning）？
4. 能否将外部知识库（如 ConceptNet、WordNet）的语义关系与统计共现结合，建立更丰富的知识图？

## Provenance

- 原始 PDF：`raw/sources/2019-CVPR-knowledge-embedded-routing-network-sgg.pdf`
- 提取文本：`raw/sources/2019-CVPR-knowledge-embedded-routing-network-sgg.txt`
- 证据等级：full-paper — 全文精读，关键结果来自论文 Table 1-3
