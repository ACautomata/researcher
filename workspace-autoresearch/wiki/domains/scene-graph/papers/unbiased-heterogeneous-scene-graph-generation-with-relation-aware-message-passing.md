---
title: "Unbiased Heterogeneous Scene Graph Generation with Relation-Aware Message Passing Neural Network"
authors:
  - Kanghoon Yoon
  - Kibum Kim
  - Jinyoung Moon
  - Chanyoung Park
year: 2023
venue: AAAI 2023
doi: null
arxiv: null
code: "https://github.com/KanghoonYoon/hetsgg-torch"
domain: scene-graph
tags: [scene-graph-generation, heterogeneous-graph, message-passing, long-tail, unbiased]
evidence_level: full-paper
status: active
task: Scene Graph Generation
dataset: Visual Genome, Open Images V6
---

# Unbiased Heterogeneous Scene Graph Generation with Relation-Aware Message Passing Neural Network

> Kanghoon Yoon*, Kibum Kim*, Jinyoung Moon, Chanyoung Park†. AAAI 2023.
> Code: [https://github.com/KanghoonYoon/hetsgg-torch](https://github.com/KanghoonYoon/hetsgg-torch)

## 核心贡献

1. **首次**将场景图生成任务重新定义为异构图（heterogeneous graph）问题，取代了传统的同构图（homogeneous graph）假设。
2. 提出 **RMP（Relation-aware Message Passing）** 层，一种关系类型感知的消息传递机制，通过可分解的基矩阵（basis matrices）高效构建类型特定的投影矩阵。
3. 提出 **HetSGG** 框架，模型无关（model-agnostic），可接入任何基于 MPNN 的 SGG 方法（如 Graph R-CNN、BGNN）。
4. 自然地缓解了长尾谓词类偏置问题：不需要额外的重加权损失或因果推断，仅通过异构图建模就能同时提升尾部谓词性能并保持头部谓词竞争力。

## 问题定义

给定图像 $I$，目标是生成场景图。本文将场景图定义为异构图 $G = \langle V, E, T_V, T_E \rangle$，其中：

- $V$ 为图像中的物体集合
- $E$ 为物体间的关系集合
- $T_V$ 为物体类型集合（Human、Animal、Product）
- $T_E$ 为关系类型集合（HH、HA、HP、AH、AA、AP、PA、PH、PP）

目标概率分解为：
$$P(G, Y|I) = P(G|I) P(Y_o|G, I) P(Y_r|Y_o, G, I)$$

若 $|T_V| = |T_E| = 1$，HetSGG 退化为同构 SGG 方法。

## 方法

### 1. 异构图构建 (Heterogeneous Graph Construction)

**初始图构建**：基于 Faster R-CNN 检测的物体，构建全连接图。节点特征 $x_u$ 由边界框位置、视觉特征和 GloVe 词向量拼接后得到；边特征 $x_{u \to v}$ 由边界框位置和提案对的联合框视觉特征提取。

**类型推断**：
- 物体类型：利用 Faster R-CNN 的类 logit $p_u \in \mathbb{R}^{|Y_o|}$，通过预定义映射函数 $\phi: Y_o \to T_V$ 聚合得到物体类型。使用 Average(·) 作为聚合函数。
- 关系类型：由关联物体类型通过笛卡尔积自动确定：$\psi(u, v) = \text{type}(u)\text{-type}(v)$。
- 使用 Faster R-CNN 时，类型推断准确率约为 **95.3%**。

### 2. 关系感知消息传递网络 (RMP)

核心思想：根据关系类型 $t \in T_E$ 分别处理每条关系。

**类型特定投影矩阵的高效构建**：
使用基矩阵分解（basis decomposition）避免参数爆炸：
$$W_t = \sum_{i=1}^{b} a_{ti} B_i$$
其中 $B_i \in \mathbb{R}^{d \times d}$ 为可训练基矩阵，$b$ 为基数量（实验中 VG 用 8，OI 用 4），$a_{ti} \in \mathbb{R}$ 为类型 $t$ 对应的可训练系数。

参数从 $O(d^2|T_E|)$ 降至 $O(d^2b + |T_E|b)$，其中 $b \ll |T_E|$。

**Step 1: Edge-wise Update（边更新）**
生成双向消息（subject→relation 和 object→relation），更新关系表示：

$$z_{u \to v}^{(l+1)} = z_{u \to v}^{(l)} + \sigma\left(\alpha(u,v)W_{\psi(u,v)}^{s2r}z_u^{(l)} + (1-\alpha(u,v))W_{\psi(u,v)}^{o2r}z_v^{(l)}\right)$$

其中 $\alpha(u,v)$ 为 attention 系数，决定主语/宾语对关系的相对重要性。

**Step 2: Node-wise Update（节点更新）**

- **Intra-relation aggregation（关系内聚合）**：对每个关系类型 $t$，聚合同类型邻居的消息：
  $$z_{u,t}^{(l+1)} = \sum_{v \in \mathcal{N}_t(u)} \alpha_{r2s}(v,t) W_{r2s}^{\psi(u,v)} z_{u \to v}^{(l+1)} + \alpha_{r2o}(v,t) W_{r2o}^{\psi(u,v)} z_{v \to u}^{(l+1)}$$

- **Inter-relation aggregation（关系间聚合）**：聚合所有关系类型的表示，得到最终的物体表示：
  $$z_u^{(l+1)} = z_u^{(l)} + \frac{1}{|T_E|} \sum_{t=1}^{|T_E|} \sigma\left(z_{u,t}^{(l+1)}\right)$$

通过堆叠多个 RMP 层可以捕获高阶交互。

### 3. 场景图预测与训练

- 物体分类：$p_u = \text{softmax}(W^{obj}z_u)$
- 关系分类：$p_{u \to v} = \text{softmax}(W^{rel}z_{u \to v} + \log \hat{p}_{u \to v})$，其中 $\hat{p}$ 为频率先验
- 损失：$\mathcal{L}_{final} = \mathcal{L}_{obj} + \mathcal{L}_{rel}$（标准交叉熵）

## 实验

### 数据集
- **Visual Genome (VG)**：150 个物体类、50 个谓词类，108K 图像（70% 训练 / 30% 测试）
- **Open Images V6 (OI)**：301 个物体类、31 个谓词类，126K 训练、1.8K 验证、6.3K 测试

### 评估设置
- 三个标准 SGG 任务：PredCls、SGCls、SGGen
- 评估指标：mR@K（均值召回）和 R@K（常规召回），K=50,100
- OI 额外报告 wmAP_rel、wmAP_phr、score_wtd = 0.2×R@50 + 0.4×wmAP_rel + 0.4×wmAP_phr
- 实现细节：ResNeXt-101-FPN + Faster R-CNN (冻结)，b=8 (VG)/b=4 (OI)，4 层 RMP

### 主要结果 — Visual Genome

| 任务 | 模型 | mR@50 | mR@100 | R@50 | R@100 |
|------|------|-------|--------|------|-------|
| **PredCls** | HetSGG‡ | 12.2 | 14.4 | 57.8 | 59.1 |
| | BGNN*‡ | 10.9 | 13.1 | 57.8 | 60.0 |
| | GPS-Net‡ | 8.1 | 9.6 | 55.2 | 57.6 |
| **SGCls** | HetSGG‡ | **17.2** | **18.7** | 37.6 | 38.7 |
| | HetSGG++‡ | 15.8 | 17.7 | 32.3 | 34.5 |
| | BGNN*‡ | 14.6 | 16.0 | 29.2 | 31.7 |
| | GPS-Net‡ | 15.9 | 16.9 | 29.2 | 31.4 |
| **SGGen** | HetSGG‡ | 30.0 | 34.6 | 9.3 | 9.6 |
| | HetSGG++‡ | 30.2 | 34.5 | 9.5 | 9.7 |
| | BGNN*‡ | 30.4 | 32.9 | 9.2 | 9.5 |

**关键提升**：在 SGCls 任务上，HetSGG‡ 的 mR@100 达到 18.7，比 BGNN*‡（16.0）提升 **16.9%**，比 GPS-Net‡（16.9）提升 **10.7%**。

### 主要结果 — Open Images V6 (SGGen)

| 模型 | mR@50 | R@50 | wmAP_rel | wmAP_phr | score_wtd |
|------|-------|------|----------|----------|-----------|
| **HetSGG‡** | 42.7 | **76.8** | **34.6** | **35.5** | **43.3** |
| HetSGG++‡ | **43.2** | 74.8 | 33.5 | 34.5 | 42.2 |
| BGNN‡ | 40.5 | 75.0 | 33.5 | 34.1 | 42.1 |
| GPS-Net | 38.9 | 74.7 | 32.8 | 33.9 | 41.6 |

HetSGG‡ 在 OI 上 mR@50 比 BGNN‡ 提升 **5.4%**（42.7 vs 40.5）。

### 头部/身体/尾部性能分析 (SGGen, VG)

| 类别分组 | HetSGG‡ | BGNN*‡ | 提升 |
|---------|---------|--------|------|
| Head | ~70 | ~69 | ~+1.4% |
| Body | ~42 | ~38 | ~+10.5% |
| Tail | ~14 | ~11 | ~+27.3% |

HetSGG 在尾部谓词类上提升最为显著（约 +27%），同时保持头部性能不降——解决了现有无偏方法中 head vs tail 的 trade-off 问题。

### 类型推断分析 (SGCls)

| 物体类型 | 模型 | 类型准确率 | mR@100 | R@100 |
|----------|------|-----------|--------|-------|
| P,H,A | HetSGG‡ | 95.3% | 18.7 | 38.7 |
| P,H,A | HetSGG‡ (GT) | 100% | 19.1 | 39.0 |
| P,H,A,L | HetSGG‡ | 90.9% | 18.2 | 38.4 |
| P,H,A,L | HetSGG‡ (GT) | 100% | **19.4** | **40.5** |

- 类型推断越准确，HetSGG 性能越好。
- 更细粒度的物体类型划分（增加 Landform）在 GT 条件下能进一步提升性能，但在推断准确率不足时反而会降低。

### 消融实验

**关系类型特定权重矩阵的影响 (SGCls)：**
| Edge | Node | mR@100 | R@100 |
|------|------|--------|-------|
| ✗ | ✗ | 15.9 | 38.6 |
| ✓ | ✗ | 16.2 | 38.7 |
| ✗ | ✓ | 17.7 | 38.7 |
| ✓ | ✓ | **18.7** | **38.7** |

edge 和 node 两处同时使用关系类型特定权重矩阵效果最佳。

**基矩阵数量分析：**
| b | $|T_E|=9$ (mR@100/R@100) | $|T_E|=16$ (mR@100/R@100) |
|---|--------------------------|--------------------------|
| 4 | 17.2 / 38.5 | 17.2 / 38.5 |
| 8 | **18.7 / 38.7** | **18.2 / 38.4** |
| 12 | 17.6 / 38.3 | 17.6 / 38.5 |
| 16 | 18.2 / 38.9 | 17.6 / 38.3 |

b=8 为最佳配置，且增加关系类型数时最优基数量不变，说明基矩阵分解具有良好的参数效率。

## 定性分析

HetSGG 生成的关系更合理：
- **避免不合理谓词**：如 BGNN 预测 ⟨hand, hold, boy⟩，但 hand（Product）不可能 hold boy（Human）；HetSGG 正确预测 of。
- **生成更丰富的关系**：如 BGNN 对树的所有关系都预测为最常见的 on，而 HetSGG 能预测 growing on 等更精确但低频的谓词。

## 分析与评价

### 优势
- 首次将异构图的视角引入 SGG，定位清晰，问题设计有洞察力。
- 通过异构图自然缓解长尾偏置，无需复杂损失函数或因果推断，简洁有力。
- RMP 层的参数效率高（基矩阵分解），可扩展到更多关系类型。
- 模型无关架构，可直接提升已有的 MPNN-based SGG 方法。
- 充分的消融和类型分析验证了方法设计的每一步。

### 局限
- 类型推断依赖 Faster R-CNN 的检测质量，95% 准确率下仍有提升空间。
- 仅定义了 Human/Animal/Product 三种物体类型（V6 扩展到 4 种），更细粒度划分的收益受限于类型推断精度。
- Open Images 上 HetSGG++ 的 R@50 低于 HetSGG（74.8 vs 76.8），说明对异构图进行更复杂的设计不一定在所有指标上占优。

### 与相关工作的关系
- 与 [[3d-spatial-multimodal-knowledge-accumulation-scene-graph-prediction-point-cloud]] 对比：本文关注 2D 场景图的异构图建模，后者关注 3D 点云场景图的层级符号知识积累。
- 与 GPS-Net (DMP) / BGNN (AMP) 直接竞争：HetSGG 的 RMP 是其一般化版本，在 DMP 的方向感知和 AMP 的置信度感知基础上增加了谓词类型感知。

## 参考资料
- Paper: AAAI 2023
- Code: [https://github.com/KanghoonYoon/hetsgg-torch](https://github.com/KanghoonYoon/hetsgg-torch)
- Dataset: Visual Genome [Krishna et al., ICCV 2017], Open Images V6 [Kuznetsova et al., IJCV 2020]
- Key references: Graph R-CNN [Yang et al., ECCV 2018], BGNN [Li et al., CVPR 2021], GPS-Net [Lin et al., CVPR 2020], TDE [Tang et al., CVPR 2020]
