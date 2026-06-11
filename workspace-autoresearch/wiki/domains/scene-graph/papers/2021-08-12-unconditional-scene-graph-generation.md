---
title: "Unconditional Scene Graph Generation"
type: paper
domain: scene-graph
status: active
created: 2026-06-10
updated: 2026-06-10
tags: [scene-graph-generation, generative, ICCV-2021, auto-regressive, unconditional-generation]
raw_sources:
  - "raw/sources/2021-08-12-unconditional-scene-graph-generation.pdf"
  - "raw/sources/2021-08-12-unconditional-scene-graph-generation.txt"
paper:
  title: "Unconditional Scene Graph Generation"
  authors: ["Sarthak Garg", "Helisa Dhamo", "Azade Farshad", "Sabrina Musatian", "Nassir Navab", "Federico Tombari"]
  year: 2021
  venue: "ICCV 2021"
  arxiv: "2108.05884"
  project: "https://SceneGraphGen.github.io/"
classification:
  label: "scene-graph-generation"
  task: ["Unconditional Scene Graph Generation"]
  method_family: ["Auto-regressive Graph Generation", "Hierarchical Recurrent Architecture"]
  modality: ["Scene Graph"]
  datasets: ["Visual Genome"]
  metrics: ["MMD graph", "MMD node", "FID", "Inception Score", "Precision", "Recall", "AUROC"]
evidence_level: full-paper
---

## Citation

Sarthak Garg, Helisa Dhamo, Azade Farshad, Sabrina Musatian, Nassir Navab, Federico Tombari. "Unconditional Scene Graph Generation." ICCV 2021.

## One-Sentence Contribution

首次提出无条件场景图生成任务，开发了基于分层循环架构的自回归模型 SceneGraphGen，可直接学习带标签有向图的概率分布，并展示其在图像合成、异常检测和图补全中的应用。

## Problem Setting

给定一组场景图样本 $G_s = \{G_s^1, G_s^2, ..., G_s^n\}$（假设来自数据分布 $p_{data}(G_s)$），目标是学习一个生成模型 $p_\phi(G_s)$，使其能够生成新的场景图样本。每个场景图 $G_s = (O, E)$ 由对象节点集 $O$ 和关系边集 $E$ 组成：

- 每个对象 $o_i \in O$ 有一个对象类别 $o_i \in C$，$C = \{1, 2, ..., C\}$
- 每条边是三元组 $E \subseteq \{(o_i, r_k, o_j) | o_i, o_j \in O, o_i \neq o_j\}$，表示从 $o_i$ 到 $o_j$ 的有向边，$r_k \in R$ 为关系类别

关键挑战：场景图大小变化大、节点/边类别固有偏斜、边有向。

## Method

### SceneGraphGen 架构

整体采用自回归公式，将场景图转换为序列表示。在排列 $\pi$ 下，节点集 $O$ 变为序列 $O = (\pi(o_1), \pi(o_2), ..., \pi(o_m))$。边 $E$ 用两个上三角稀疏矩阵 $E_{to}$ 和 $E_{from}$ 表示。场景图表示为序列 $X = (O, E_{to}, E_{from})$，每个元素 $X_i$ 本身是一个序列 $X_i = (O_i, E_{to_i}, E_{from_i})$。

概率分解：

$$p_\phi(X) = p(O_1) \prod_{i=2}^n p_{\phi_1}(O_i|X_{<i}) p_{\phi_2}(E_{to_i}|O_i, X_{<i}) p_{\phi_3}(E_{from_i}|O_i, E_{to_i}, X_{<i})$$

### 三阶段生成

1. **History Encoding**：用三个专门的 GRU（gGRU^O, gGRU^{E_{from}}, gGRU^{E_{to}}）分别编码历史信息 $X_{<i}$，每个 GRU 对应一种输出类型

2. **Node Generation**：用 MLP（nMLP）取 gGRU^O 的隐藏状态，输出对象类别上的分类分布 $\theta_i^O$，遇到 EOS token 时停止生成

3. **Node-aware Edge Generation**：用两个 GRU（eGRU^{E_{to}}, eGRU^{E_{from}}）依次生成 $E_{to}$ 和 $E_{from}$。输入为四部分拼接：上一步的边 $E_{from_{i,j-1}}$ 和 $E_{to_{i,j-1}}$、当前节点 $O_i$、以及与第 $j$ 步节点 $O_j$ 的信息。eGRU^{E_{from}} 的输入还包括 eGRU^{E_{to}} 在当前步生成的 $E_{to_{i,j}}$，提供条件依赖

### 训练

- 损失函数：预测分数与真实序列的交叉熵之和，分为节点损失 $L_O$ 和边损失 $L_E$
- 训练使用 teacher forcing
- 300 epochs, batch size 256（每 epoch 256 个带放回采样的批次）
- 初始 LR 0.001，每 1710 步衰减率 0.95
- Node/edge embedding size: 64/8
- 所有 gGRU/eGRU：4 层 GRU，hidden size 128
- nMLP：2 层，ReLU 激活

### 推理

- 从先验分布（基于训练集计算）采样第一个节点
- 后续按自回归流程生成节点和边序列
- 支持计算给定样本的 NLL（负对数似然），用于异常检测

## Experiments

### 数据集

- **Visual Genome (VG)**：采用 Xu et al. [41] 的广泛使用划分，150 个对象类别，50 个关系类别
  - 训练集：58k 样本
  - 测试集：26k 样本
- 预处理：用 Unbiased causal TDE 模型 [35] 补全关系边；用 IoU 0.5 和手工分组类别去重对象；移除子对象与多个父对象的关系

### 评估指标

**图质量评估**（基于 MMD）：
- **MMD graph**：基于随机游走图核（random-walk graph kernel），比较两图的整体结构相似性
- **MMD node**：基于对象集核（object set kernel），比较对象类别及其出现次数

**图像质量评估**（用 sg2im 将生成图转图像后）：FID, Inception Score, Precision (F1/8), Recall (F8)

### Baseline

- **GraphRNN [44]**：改编版，增加节点/边类别和边方向支持
- vs. SceneGraphGen 的优势：边生成时加入节点信息、$E_{from}$ 条件依赖 $E_{to}$

### 消融实验/变体

- **节点排序方案**：BFS order, Hierarchical order（背景→对象→部位）, Random order
- 目标：评估不同排序对生成质量的影响

### 异常检测评估

- 用 NLL 对各类 corruption level 下的数据集计算 AUC-ROC
- Corruption：随机替换 x% 节点/边标签

### 实现细节

- 训练于单个 GPU（未明确说明具体型号）
- 代码未公开

## Results

### 图生成质量（Table 1, left）

| Model | Ordering | MMD node (×10⁻³) ↓ | MMD graph (×10⁻³) ↓ |
|---|---|---|---|
| GraphRNN | BFS | 2.3 | 1.3 |
| GraphRNN | Random | 0.39 | 1.2 |
| **SceneGraphGen** | **Random** | **0.37** | **0.11** |
| SceneGraphGen | Hierarchical | 1.85 | 0.63 |
| SceneGraphGen | BFS | 2.05 | 1.82 |

> SceneGraphGen (Random) 在 MMD graph 上显著优于所有变体和 baseline（0.11 vs GraphRNN Random 的 1.2），说明 node-aware 边生成和有向边建模有效。

### 图像生成质量（Table 1, right）

| Model | Ordering | FID ↓ | IS ↑ | Precision ↑ | Recall ↑ |
|---|---|---|---|---|---|
| GraphRNN | BFS | 75.8 | 4.88 | 0.680 | 0.660 |
| GraphRNN | Random | 74.5 | 4.85 | 0.679 | 0.664 |
| SceneGraphGen | BFS | 73.3 | 5.04 | 0.679 | 0.690 |
| SceneGraphGen | Hierarchical | 72.2 | 5.26 | 0.717 | 0.714 |
| **SceneGraphGen** | **Random** | **71.2** | **4.95** | **0.727** | **0.714** |
| Ground Truth | — | 73.0 | 5.22 | 0.693 | 0.707 |

> SceneGraphGen (Random) 在 Precision (0.727) 和 Recall (0.714) 上均优于 Ground Truth 图像，说明生成图的语义内容使 sg2im 生成了更可识别的对象。FID (71.2) 优于 Ground Truth 的 73.0。但 Inception Score (4.95) 低于 Hierarchical (5.26)。

### MMD 指标验证（Table 2）

| Comparison | MMD node (×10⁻³) | MMD graph (×10⁻³) |
|---|---|---|
| test vs test | 0.018 | 0.023 |
| 100% corrupt vs 100% corrupt | 0.11 | 0.0098 |
| test vs 20% corrupt | 6.0 | 3.7 |
| test vs 50% corrupt | 10 | 6.3 |
| test vs 100% corrupt | 44 | 25 |

> 随着 corruption 程度增加，MMD 值单调上升，验证了指标的有效性。

### 异常检测（Figure 6）

- 不同 corruption 水平下 NLL 分布的 AUC-ROC 作为衡量指标
- SceneGraphGen 对 corruption 水平更敏感（与 baseline GraphRNN 相比，不同 corruption 水平的 NLL 间隙更大）

### 对象统计比较

- sg2im-SGG 生成图像检测到 **50** 个对象类别 vs StyleGAN2 的 **40** 个
- sg2im-SGG 对象出现分布更接近 ground truth（平均误差 1.2 vs 1.4）

### 风格对比

- StyleGAN2 在简单场景（如风景）质量好，但在复杂场景中失败（出现多个绿色屏幕或不可区分对象）
- sg2im-SGG 图生成的图像有更扎实的语义组合

## Limitations

1. **依赖真实场景图补全的预处理**：使用 Unbiased TDE 模型 [35] 补全原始 VG 的不完整关系，引入额外依赖和潜在偏差
2. **数据预处理规则较启发式**：去重和父子关系清理使用手工规则（IoU 阈值、分组类别），不够优雅
3. **图质量评估仅靠 MMD**：MMD 能区分分布差异但缺乏细粒度语义验证（如关系合理性）
4. **图像生成依赖 sg2im**：最终图像质量受 sg2im 能力限制而非 SceneGraphGen 本身
5. **代码未公开**：不可复现
6. **仅在 VG 上验证**：未在其他场景图数据集上测试泛化性
7. **图偏斜问题**：VG 的对象/关系长尾分布的处理有限，仅通过 TDE 补全部分缓解

## Reusable Claims

- **Claim**: 自回归序列化（节点序列→边序列）能有效建模带标签有向场景图的概率分布
  - **Evidence**: MMD graph 0.11 vs GraphRNN 1.2（×10⁻³）— Table 1
  - **Scope**: Visual Genome, 150 objects, 50 relations
  - **Confidence**: high

- **Claim**: 边生成时纳入节点信息（node-aware）显著提升生成质量
  - **Evidence**: SceneGraphGen vs GraphRNN 在 MMD graph 上差距约 10 倍
  - **Confidence**: high

- **Claim**: Random ordering 优于 BFS 和 Hierarchical ordering 用于场景图生成
  - **Evidence**: MMD node 0.37 (Random) vs 1.85 (Hierarchical) vs 2.05 (BFS) — Table 1
  - **Confidence**: medium（仅 VG 数据验证）

- **Claim**: 生成的场景图作为中间表示，比直接无条件图像生成产生更语义多样的图像
  - **Evidence**: 50 vs 40 检测类别；对象分布误差 1.2 vs 1.4
  - **Confidence**: medium（受 Faster-RCNN 检测上限影响）

## Connections

- **GraphRNN [44]**：基础自回归图生成框架，SceneGraphGen 在其上增加节点/边类别和方向支持
- **sg2im [19]**：图到图像生成模型，用于 SceneGraphGen 生成图的翻译
- **Unbiased TDE [35]**：用于补全 VG 不完整关系边的前置模块
- **VG-COCO [23]**：场景图数据集，本工作的主要评估数据
- **VarScene ([2022] scene-graph-synthesis)**：后续的无条件场景图生成工作，使用层次 VAE
- **Importance-First [2023]**：另一条将图生成与注意力结合的场景图生成路线
- **IS-GGT [2023]**：生成式 Transformer 用于迭代场景图生成

## Open Questions

1. 生成图在关系层面的语义合理性如何验证？MMD 衡量分布差异而非语义正确性
2. 在大场景（10+ 节点）下的生成质量如何？自回归模型是否存在误差累积？
3. 能否扩展到视频级别的动态场景图生成？
4. 逆过程——场景图 → 文本描述 是否也能用类似框架实现？
5. 更高效的排序策略（如学习式排序）能否超越 Random ordering？

## Provenance

- 原始 PDF：`raw/sources/2021-08-12-unconditional-scene-graph-generation.pdf`
- 提取文本：`raw/sources/2021-08-12-unconditional-scene-graph-generation.txt`
- arXiv：2108.05884
- 项目页面：https://SceneGraphGen.github.io/
- Evidence level：full-paper（全文精读）
