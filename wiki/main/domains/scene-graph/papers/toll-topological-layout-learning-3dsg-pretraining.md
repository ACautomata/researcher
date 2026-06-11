---
title: "ToLL: Topological Layout Learning with Asymmetric Cross-View Structural Distillation for 3D Scene Graph Generation Pretraining"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - 3d-scene-graph-generation
  - self-supervised-learning
  - pretraining
  - topological-layout-learning
  - generative-pretraining
  - geometric-shortcut
  - anchor-conditioned-reasoning
  - structural-multi-view-augmentation
  - self-distillation
  - 3d-point-cloud
  - graph-neural-network
  - diffusion-model
  - long-tail-robustness
  - zero-shot-generalization
  - arXiv-2026
raw_sources:
  - ../../../sources/scene-graph/2026-arXiv-ToLL-Topological-Layout-Learning-SGG.pdf
  - ../../../sources/scene-graph/2026-arXiv-ToLL-Topological-Layout-Learning-SGG.txt
related_pages:
  - cage-sgg-counterfactual-active-graph-evidence-open-vocabulary-sgg.md
  - vizor-viewpoint-invariant-zero-shot-3d-scene-graph-generation.md
evidence_level: full-paper
paper:
  title: "ToLL: Topological Layout Learning with Asymmetric Cross-View Structural Distillation for 3D Scene Graph Generation Pretraining"
  abbreviated: "ToLL"
  authors:
    - Yucheng Huang
    - Luping Ji
    - Xiangwei Jiang
    - Wen Li
    - Mao Ye
  year: 2026
  venue: "arXiv (preprint)"
  arXiv: "2603.28178"
  code: "https://github.com/UESTC-nnLab/ToLL-SGG"
  paper_url: "https://arxiv.org/abs/2603.28178"
  affiliation: "University of Electronic Science and Technology of China (UESTC)"
---

# ToLL: Topological Layout Learning with Asymmetric Cross-View Structural Distillation for 3D Scene Graph Generation Pretraining

> 通过**Anchor-Conditioned Topological Geometry Reasoning (ACTGR)** 构造信息瓶颈，避免生成式预训练中的"几何捷径"问题，并通过**Structural Multi-view Augmentation (SMA)** 增强语义鲁棒性，在 3DSSG 数据集上显著提升谓词分类和场景图生成性能

## 概述

3D 场景图（3DSG）生成对空间理解和 affordance 感知至关重要。针对数据稀缺带来的泛化问题，现有方法利用联合嵌入或生成式代理任务在无标注数据集上预训练 3DSG 表示。然而，已有生成式预训练虽然避免了联合嵌入中几何变换引起的语义破坏，却存在一个关键缺陷——**"几何捷径"（Geometric Shortcut）**：暴露稠密的物体空间位置和尺度先验会诱导模型通过插值物体位置来平凡重建场景，而非学习边编码的拓扑约束。

ToLL 通过设计 ACTGR 信息瓶颈和 SMA 交叉视图自蒸馏，强制模型仅从边缘拓扑中学习场景布局，模型在 3DSSG 数据集上全面超越 SOTA 基线。

## 方法

### 核心架构

#### 1. Anchor-Conditioned Topological Geometry Reasoning (ACTGR)

- 将物体点云归一化到规范空间，应用 Point-MAE 风格掩码
- 仅保留**一个随机锚点**的绝对空间属性（位置、形状、尺度），其余物体全局空间特征完全遮蔽
- 构造**信息瓶颈**：GNN 必须仅凭单个锚点的空间先验，通过边拓扑关系进行空间推断（"dead-reckoning"）
- 恢复整体场景布局使用**条件扩散模型**（而非自编码器），避免过平滑

#### 2. Structural Multi-view Augmentation (SMA)

- 不使用几何变换（旋转等），改用**连接性扰动**生成非对称学生视图：
  - **Edge-Guided Student View**：保留完整物体但随机丢弃边
  - **Node-Guided Student View**：随机丢弃物体节点及其相邻边
- 教师视图使用完整拓扑结构，通过 SwAV-style 自蒸馏 + EMA 更新
- 强制模型学习对空间不完整性和拓扑遮挡不变的表示

#### 3. Decoupled Geometric Layout Recovery（ToLL++ 扩展）

- 将形状、尺度、位置解耦为独立恢复分支
- 物体在规范空间中生成，防止大物体淹没小物体的梯度

### 损失函数

总损失：$\mathcal{L}_{total} = \mathcal{L}_{gen}(G_{edge}) + \lambda \sum_{v \in \{edge, node\}} \mathcal{L}_{distill}(G_v, G_{ref})$

- $\mathcal{L}_{gen}$：条件扩散模型的布局重构损失
- $\mathcal{L}_{distill}$：交叉视图自蒸馏的 SwAV 损失
- $\lambda = 0.1$：蒸馏损失权重

## 关键贡献

1. **识别并解决几何捷径问题**：首次揭示生成式 3DSG 预训练中"几何捷径"缺陷，通过 ACTGR 信息瓶颈强制拓扑学习
2. **ACTGR（Anchor-Conditioned 拓扑几何推理）**：仅保留单个锚点空间属性，迫使 GNN 通过边拓扑进行空间推断，同时增强物体级几何细节和边缘级语义
3. **SMA（结构多视图增强）**：通过连接性扰动（而非几何变换）生成非对称视图，结合自蒸馏学习对拓扑遮挡鲁棒的语义表示
4. **ToLL++ 解耦恢复**：将形状、尺度、位置解耦为独立分支，进一步提升性能
5. 在 3DSSG 基准上取得全面 SOTA，尤其在长尾谓词分类和零样本三元组泛化上表现优异

## 实验与结果

### 预训练设置

- **预训练数据**：1,513 个 ScanNet 场景，构建 7,392 个子图样本（33,949 节点、61,599 边）
- **物体采样**：剔除 <512 点物体，均匀采样至 1,024 点
- **训练**：300 epoch，AdamW 优化器，weight decay 1e-4，lr 1e-3，cosine scheduler + 5 epoch warmup
- **硬件**：4× RTX 3090 GPUs，batch size 32

### 微调设置

- **数据集**：3DSSG（160 物体类别、27 谓词类别）
- **评估协议**：
  - 全微调（完整编码器 + 低学习率）
  - MLP-only 微调（冻结编码器，仅训练 MLP 分类头）
- **评估指标**：Object A@k、Predicate mA@k、Triplet mA@k、SGCLs mR@k、PredCls R@k

### 与 SOTA 对比（3DSSG 数据集）

| 方法 | 预训练 | Object A@1 | Predicate mA@1 | Predicate mA@3 | Triplet mA@50 | Triplet mA@100 | SGCLs mR@50 | PredCls R@50 |
|------|--------|-----------|---------------|---------------|--------------|---------------|-------------|-------------|
| SGFNpt | ×（from scratch） | 56.04 | 46.69 | 71.84 | 60.05 | 70.26 | 30.8 | 62.1 |
| VL-SATpt | ×（from scratch） | 57.84 | 52.43 | 73.35 | 63.55 | 72.48 | 32.8 | 63.8 |
| SGFNpt | PointDif | 57.10 | 48.82 | 73.29 | 63.61 | 72.89 | 33.5 | 62.6 |
| VL-SATpt | PointDif | 58.54 | 52.66 | 73.33 | 64.86 | 73.66 | 34.2 | 64.8 |
| VL-SATpt | OCRL | 59.27 | 54.26 | 75.68 | 64.37 | 74.26 | 37.1 | 66.4 |
| VL-SATpt | MvIL | 58.34 | 58.43 | 79.63 | 68.57 | 76.89 | 38.2 | 68.3 |
| SGFNpt | **ToLL** | 58.68 | 54.59 | 81.36 | 66.58 | 74.32 | 36.6 | 66.3 |
| VL-SATpt | **ToLL** | 58.72 | 56.67 | 79.03 | 66.42 | 75.59 | 36.7 | 67.6 |
| SGFNpt | **ToLL++** | 60.64 | 56.19 | 80.79 | 67.85 | 76.25 | 38.3 | 69.1 |
| **VL-SATpt** | **ToLL++** | **61.43** | **57.94** | **82.06** | **68.42** | **78.42** | **40.2** | **69.4** |

#### 关键对比
- 相比 VL-SATpt（from scratch），**VL-SATpt w/ ToLL++** 提升：Predicate mA@1 **+5.51**（57.94 vs 52.43），mA@3 **+8.71**（82.06 vs 73.35），Triplet mA@50 **+4.87**（68.42 vs 63.55）
- **Object A@1**：61.43（ToLL++）vs 58.34（MvIL）、57.84（from scratch）
- **SGCLs mR@50**：40.2（ToLL++）vs 38.2（MvIL）
- 超越 MvIL、OCRL 等已有预训练框架

### 长尾鲁棒性（Predicate 分类）

| 方法 | 预训练 | Head mA@3 | Body mA@3 | Tail mA@3 |
|------|--------|-----------|-----------|----------|
| VL-SATpt | × | 95.97 | 78.75 | 54.44 |
| VL-SATpt | MvIL | 98.67 | 86.25 | 63.42 |
| **VL-SATpt** | **ToLL++** | **98.52** | **85.72** | **63.95** |

- Tail mA@3：**63.95**（ToLL++）vs 54.44（from scratch），提升 **+9.51**
- Body mA@3：**85.72**（ToLL++）vs 78.75（from scratch），提升 **+6.97**
- 长尾谓词识别能力显著优于 from-scratch 基线和竞争性预训练方法

### 零样本三元组泛化

| 方法 | 预训练 | Unseen A@50 | Unseen A@100 |
|------|--------|-------------|--------------|
| VL-SATpt | × | 32.87 | 46.32 |
| VL-SATpt | MvIL | 39.75 | 55.83 |
| **VL-SATpt** | **ToLL++** | **40.28** | **56.42** |

- Unseen A@50：**40.28**（ToLL++）vs 32.87（from scratch），提升 **+7.41**
- 超越 MvIL 的 39.75，验证了 ToLL 学到的表示具有较强的可迁移性

### 消融实验关键结果

| 设置 | Object A@1 | Predicate mA@1 | Predicate mA@3 | Triplet mA@50 | Triplet mA@100 |
|------|-----------|---------------|---------------|--------------|---------------|
| Baseline（Global Layout） | 57.62 | 47.28 | 70.20 | 60.39 | 70.85 |
| **ACTGR**（单锚点） | **58.46** | **53.87** | **75.69** | **64.92** | **73.66** |
| SMA w/ ACTGR | 58.68 | 54.59 | 81.36 | 66.58 | 74.32 |
| SMA w/o ACTGR | 55.36 | 50.07 | 72.64 | 61.94 | 71.63 |
| +PointDif Init | 58.68 | 54.59 | 81.36 | 66.58 | 74.32 |
| +Random Init | 57.94 | 52.37 | 76.62 | 63.69 | 73.87 |
| **ToLL++**（解耦） | **60.64** | **56.19** | **80.79** | **67.85** | **76.25** |

- ACTGR 相比 Global Layout Baseline：Triplet mA@50 提升 **+4.53**
- SMA w/ ACTGR 相比仅 ACTGR：Predicate mA@3 提升 **+5.67**，Triplet mA@50 提升 **+1.66**
- 单独 SMA（无 ACTGR）反而比 Baseline 更差（55.36 vs 57.62），说明 SMA 必须在 ACTGR 基础上才有效
- ToLL++ 的预测器性能：Object A@1 60.64，Predicate mA@1 56.19

### 锚点数消融

| 配置 | 锚点数 | Object A@1 | Predicate mA@1 | Triplet mA@50 |
|------|--------|-----------|---------------|--------------|
| ACTGR Only | Single (1) | **58.46** | **53.87** | **64.92** |
| | 50% | 57.83 | 46.80 | 61.30 |
| | 100% | 57.62 | 47.28 | 60.39 |
| **ToLL**（完整） | **Single (1)** | **58.68** | **54.59** | **66.58** |
| | 50% | 58.96 | 49.85 | 62.20 |
| | 100% | 58.49 | 47.76 | 60.65 |

- **单锚点**设置在所有配置下最优，验证了信息瓶颈的有效性
- 锚点增多（50%、100%）导致性能下降，确认了"几何捷径"的存在

### 生成方法对比

| 方法 | Object A@1 | Predicate mA@1 | Predicate mA@3 | Triplet mA@50 |
|------|-----------|---------------|---------------|--------------|
| ToLL w/ Diffusion | 58.68 | 54.59 | **81.36** | 66.58 |
| ToLL w/ AE | 57.19 | 55.17 | 78.62 | 65.93 |
| **ToLL++ w/ Diffusion** | **60.64** | **56.19** | 80.79 | **67.85** |
| ToLL++ w/ AE | 59.47 | 55.85 | 78.34 | 66.19 |

- 扩散模型在 Predicate mA@3 上比自编码器高 **2.74**（81.36 vs 78.62）
- ToLL++ w/ Diffusion 取得全部 SOTA

## 讨论

### 几何捷径问题

核心洞察：当模型能直接访问所有物体的绝对空间位置时，它可以简单插值坐标来重建场景，而无需学习边拓扑。ACTGR 通过仅暴露单个锚点的空间先验，创造信息瓶颈，迫使 GNN 通过谓词表示学习来恢复完整场景布局。

### 连接性扰动 vs. 几何变换

现有联合嵌入方法使用旋转等几何变换会导致谓词语义改变。SMA 使用连接性扰动（边丢弃、节点丢弃）生成非对称视图，既保留了空间语义信息，又通过自蒸馏增强了鲁棒性。

### ToLL++ 的解耦策略

将形状、尺度、位置解耦为独立恢复分支，使模型在规范空间中生成物体，防止大物体梯度主导小物体，带来一致的性能提升（Object A@1 +1.96）。

## 局限性

- 仅在 ScanNet/ScanNet++ 室内场景上验证，未在户外场景测试
- ACTGR 依赖子图连通性，对高度稀疏图可能不够鲁棒
- 预训练计算资源需求较高（4× RTX 3090，300 epoch）
- 单锚点策略在极端小图场景（≤3 节点）中锚点偏置可能影响重建质量

## 总结

ToLL 通过 ACTGR 信息瓶颈和 SMA 结构自蒸馏的组合，有效解决了生成式 3DSG 预训练中的几何捷径问题。在 3DSSG 基准上的全面实验表明：ToLL++ 在全微调和 MLP-only 冻结评估中均超越 MvIL、OCRL 等现有预训练框架，在长尾谓词分类和零样本三元组泛化方面尤其突出。

## 参考资料

- arXiv: [2603.28178](https://arxiv.org/abs/2603.28178)
- 代码: [github.com/UESTC-nnLab/ToLL-SGG](https://github.com/UESTC-nnLab/ToLL-SGG)
- 数据集: 3DSSG (ScanNet + ScanNet++)
- 相关方法: OCRL [41], MvIL [16], PointDif [40], VL-SAT [7]
