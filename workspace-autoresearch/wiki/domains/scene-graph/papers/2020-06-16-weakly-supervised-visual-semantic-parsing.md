---
title: "Weakly Supervised Visual Semantic Parsing"
type: paper
domain: scene-graph
status: active
created: 2026-06-10
updated: 2026-06-10
tags:
  - scene-graph-generation
  - weakly-supervised
  - visual-semantic-parsing
  - message-passing
  - graph-alignment
  - CVPR-2020
source_pages: []
raw_sources:
  - raw/sources/2020-06-16-weakly-supervised-visual-semantic-parsing.pdf
  - raw/sources/2020-06-16-weakly-supervised-visual-semantic-parsing.txt
related_pages: []
paper:
  title: "Weakly Supervised Visual Semantic Parsing"
  authors: "Alireza Zareian, Svebor Karaman, and Shih-Fu Chang"
  year: 2020
  venue: "CVPR 2020"
  arxiv: ""
  doi: ""
  code: "https://github.com/alirezazareian/vspnet"
  project: ""
classification:
  label: "vspnet"
  task:
    - scene-graph-generation
    - visual-semantic-parsing
    - visual-relationship-detection
  method_family:
    - message-passing-network
    - graph-alignment
    - bipartite-attention
  modality: image
  datasets:
    - Visual Genome
    - V-COCO
  metrics:
    - R@50
    - R@100
    - SGGEN
    - SGCLS
    - PREDCLS
    - PHRDET
    - inference-time
evidence_level: full-paper
---

# Weakly Supervised Visual Semantic Parsing

## Citation

Zareian, A., Karaman, S., & Chang, S.-F. (2020). Weakly Supervised Visual Semantic Parsing. *CVPR 2020*.

## One-Sentence Contribution

提出 VSPNET，通过将谓词建模为节点（而非边）、设计基于注意力机制的双向消息传递框架以及首个基于图对齐的弱监督学习算法，实现了无需边界框标注的可扩展场景图生成，同时大幅降低了计算复杂度（**sub-quadratic**）。

## Problem Setting

### 传统 SGG 的两个核心局限

1. **计算效率低下**：所有现有方法需穷举处理所有对象提议对（O(n²)），其中 n 通常为 300，而 VG 中 <99% 的图拥有少于 20 个谓词
2. **标注成本过高**：需要数百万手动标注的边界框标注，弱监督 SGG 几乎未被研究

### VSP 形式化

提出 **Visual Semantic Parsing (VSP)**，是 SGG 的泛化形式：

- 谓词被表示为节点（而非边），实体和谓词在相同语义空间
- 边表示语义角色（如 subject, object, instrument）
- 图定义为 G_VSP = (N_e, N_p, E)，其中：
  - N_e (实体节点)：class c ∈ C_e + bounding box b
  - N_p (谓词节点)：class c ∈ C_p
  - E (边)：N_p × N_e → C_r（语义角色集合）

VSP 可以自然地表示**高阶交互**（如 "a girl eating cake with fork" 有三个实体连接到同一个谓词节点），这是传统 SGG 无法表达的。

## Method

### VSPNET 架构

整体框架包含两个核心模块：

#### 1. 动态基于角色的注意力双向消息传递

- **初始化**：实体节点 H_e^(0) 由 Faster R-CNN 提议的 RoI 特征和边界框坐标初始化；谓词节点 H_p^(0) 为可训练矩阵（测试时固定）
- **多角色注意力**：每个语义角色 r 对应一个注意力头，计算注意力矩阵 Ã_r^(t) ∈ ℝ^(np × ne)

  `Ã_r^(t)[k,i] = ⟨f_r^p(H_p^(t)[k]), f_r^e(H_e^(t)[i])⟩`

  双重 softmax 归一化（沿角色和实体两个维度），引入 p_∅ 常数以允许无连接

- **三阶段消息聚合网络**：
  1. **发送头 (send head)**：源节点 → 消息向量
  2. **池化头 (pool head)**：按角色聚合，权重为注意力分数
  3. **接收头 (receive head)**：聚合后的消息 → 目标节点更新

- **节点更新**：使用 GRU 更新节点状态（de=dp=1024），迭代 u=3 次
- **最终离散化**：最近邻搜索确定类别标签；阈值 + 非极大值抑制确定边

#### 2. 弱监督图对齐算法

- **问题定义**：给定输出图 G_O 和目标图 G_T（无位置标注），寻找对齐 I = (I_e, I_p)，最小化损失函数：

  `L(G_O, G_T, I) = L_E + L_P + λL_R`（λ=10）

  - L_E：实体嵌入 MSE + 实体对齐
  - L_P：谓词嵌入 MSE + 谓词对齐  
  - L_R：注意力矩阵的二值交叉熵损失

- **交替优化**（类 EM 算法）：
  - 外优化：Adam 优化模型参数 φ
  - 内优化：迭代式坐标下降
    1. 给定 I_e → 通过 Kuhn-Munkres 求解最优 I_p（最大二分图匹配）
    2. 给定 I_p → 最优 I_e
    3. 重复 v=3 次直到收敛

- **扩展到全监督**：添加边界框 IoU 损失项到 L_E，仅影响对齐不影响梯度

### 总体损失函数

```
L(G_O, G_T, I) = L_E + L_P + λL_R
```

其中 L_E 和 L_P 是嵌入空间的 MSE 损失，L_R 是注意力分数的二值交叉熵。

## Experiments

### 数据集

| 数据集 | 用途 | 图像数 | 标注 |
|--------|------|--------|------|
| Visual Genome (VG) [17] | 主实验 | 108,077 | 物体、关系、边界框 |
| VG [40] 预处理版 | 与 SGG 基线对比 | 同上 | 150 实体类 + 50 谓词类 |
| VG [50] 预处理版 | 与弱监督基线对比 | 同上 | 200 实体类 + 100 谓词类 |
| V-COCO [10] | VSP 高阶交互可视化 | - | 人类动作 + 物体/工具 |

### 基线方法

**弱监督基线**（来自 [50]）：
- VtransE-MIL
- PPR-FCN

**全监督基线**（来自 [40] 和 [50]）：
- IMP [40]、MSDN [20]、MotifNet [48]、Assoc. Emb. [27]、Graph R-CNN [41]
- VtransE [49]、S-PPR-FCN [50]

### 训练设置

- **提议网络**：Faster R-CNN（在 Open Images 上预训练，固定权重，不微调）
- **GRU 状态维度**：de=dp=1024
- **全连接网络**：所有消息传递头为两层 1024-D，Leaky ReLU 激活
- **嵌入预测头**：单层 1024→300
- **词嵌入**：GloVe（微调）
- **超参数**：λ=10（损失平衡系数），u=3（MP 迭代数），v=3（对齐迭代数）
- **谓词节点数**：np=100
- **优化器**：Adam
- **硬件**：NVIDIA TITAN X

### 评估协议

- **SGGEN**：检测 subject-predicate-object 三元组，边界框 IoU ≥ 0.5
- **SGCLS**：测试时提供真实边界框，评估关系分类
- **PREDCLS**：测试时提供真实边界框和物体类别，评估谓词分类
- **PHRDET**：预测三元组的联合边界框，IoU ≥ 0.5
- **召回率**：R@50 和 R@100
- **推理时间**：秒/图像（200 proposals，VGG backbone，NVIDIA TITAN X）

### 消融实验

VSPNET 的消融变体：
1. **w/o iterative alignment**：用启发式方法（最小化 LE 和 LP 分别对齐）替代对齐算法
2. **w/ fewer alignment steps**：v 从 3 减至 1
3. **w/o three-stage MP**：将三阶段消息聚合替换为平均池化
4. **w/o role-driven MP**：移除角色注意力，改为均匀分布注意力
5. **w/ fewer MP steps**：u 从 3 减至 1

## Results

### 主要结果（VG [50] 预处理，Table 1）

| 方法 | 监督 | SGGEN R@50 | SGGEN R@100 | PHRDET R@50 | PHRDET R@100 |
|------|------|:----------:|:-----------:|:-----------:|:------------:|
| VtransE-MIL [50] | Weak | 0.7 | 0.9 | 1.5 | 2.0 |
| PPR-FCN [50] | Weak | 1.5 | 1.9 | 2.4 | 3.2 |
| **VSPNET (Ours)** | **Weak** | **3.1** | **3.5** | **17.6** | **20.4** |
| VtransE [50] | Full | 5.5 | 6.0 | 9.5 | 10.4 |
| S-PPR-FCN [50] | Full | 6.0 | 6.9 | 10.6 | 11.1 |
| **VSPNET (Ours)** | **Full** | **8.9** | **9.9** | **24.0** | **27.8** |

**弱监督下**：SGGEN 性能比 SOTA 高 **2 倍以上**，PHRDET 高 **6 倍以上**。弱监督 VSPNET 的 PHRDET 甚至超过所有全监督基线。

### 主要结果（VG [40] 预处理，Table 2）

| 方法 | 监督 | SGGEN R@100 | SGCLS R@100 | PREDCLS R@100 | 推理时间(s) |
|------|:----:|:-----------:|:-----------:|:-------------:|:-----------:|
| IMP [40] | Full | 3.4 | 24.4 | 53.1 | 1.64 |
| MSDN [20] | Full | 10.5 | 21.8 | 66.4 | 3.56 |
| MotifNet [48] | Full | 9.1 | 27.2 | 48.8 | 2.07 |
| Assoc. Emb. [27] | Full | 11.3 | 30.0 | 76.2 | 1.19 |
| Graph R-CNN [41] | Full | 13.7 | 31.6 | 59.1 | 0.83 |
| **VSPNET (Ours)** | **Full** | **14.2** | **34.1** | **73.7** | **0.11** |
| **VSPNET (Ours)** | **Weak** | **5.4** | **32.7** | **62.4** | **0.11** |

**全监督下**：VSPNET 在 SGGEN 和 SGCLS 上超越所有 SOTA 方法（Assoc. Emb. 在 PREDCLS 上略高 2.5 个百分点），推理速度 **快 7.5 倍**（0.11s vs Graph R-CNN 0.83s），比 Factorizable Net 快 **5 倍**（0.55s）。

**弱监督下**：SGCLS R@100 32.7%，接近全监督 VSPNET（34.1%），超越所有全监督基线（最高 Assoc. Emb. 30.0%），表明"只要有准确的 proposals，弱监督模型可以达到与全监督方法相当的表现"。

### 消融实验结果（Table 1 内嵌）

| 变体 | SGGEN R@50 | SGGEN R@100 | PHRDET R@50 | PHRDET R@100 |
|------|:----------:|:-----------:|:-----------:|:------------:|
| w/o iterative alignment | 1.3 | 1.6 | 8.0 | 10.2 |
| w/ fewer alignment steps (v=1) | 1.8 | 2.0 | 9.9 | 11.9 |
| w/o three-stage MP | 2.4 | 2.8 | 16.7 | 19.8 |
| w/o role-driven MP | 2.5 | 2.9 | 15.7 | 18.7 |
| w/ fewer MP steps (u=1) | 2.5 | 2.8 | 15.5 | 18.3 |
| **VSPNET (full, Ours)** | **3.1** | **3.5** | **17.6** | **20.4** |

关键发现：
- 迭代对齐算法带来了 **2 倍以上** 性能提升（3.1 vs 1.3 SGGEN R@50）
- 三阶段消息聚合优于平均池化（3.1 vs 2.4）
- 角色驱动注意力贡献独立有效（3.1 vs 2.5）
- 减少对齐步数或 MP 步数均导致显著下降

### V-COCO 可视化

VSPNET 成功生成包含高阶交互的 VSP 图，如 "person cutting cake with knife"（3 实体连接同一谓词），这是任何 SGG 方法无法做到的。

## Limitations

1. **提议质量瓶颈**：VSPNET 依赖外部 Faster R-CNN（Open Images 预训练），不需自己训练检测器，但 WS 设置下 proposal 质量直接影响性能
2. **SGGEN 召回率偏低**：弱监督下 SGGEN R@50 仅 3.1-4.7%，主要受限于物体定位精度
3. **VG-150 弱监督性能未探索**：实验主要报告了 FS 在 VG-150 的结果，WS 在 VG-150 的主指标待补充
4. **VG vs V-COCO 间的gap**：V-COCO 可视化仅展示了 VSP 的表达能力，未提供定量指标
5. **谓词节点数固定**：np=100 的设定需事先确定，可能不适用于场景动态变化的应用

## Reusable Claims

1. **将谓词建模为节点可实现 sub-quadratic 推理**：VSP 形式化将 SGG 的 O(n²) 复杂度降低至 O(np·ne)，np ≪ ne（论文中 np=100 vs ne=300），推理时间仅 0.11s/图像
2. **角色驱动注意力在场景图生成中有效**：多角色注意力头为每个语义角色独立建模，三阶段消息聚合优于平均池化（+0.7 SGGEN R@50）
3. **图对齐可替代目标检测作为弱监督场景图生成的训练信号**：无需边界框标注，通过嵌入空间的对齐即可实现有竞争力的关系识别（SGCLS R@100 32.7%，超越全监督基线）
4. **交替坐标下降可近似求解图对齐**：Kuhn-Munkres 算法 + 交替优化避免了全局搜索的指数复杂度，与 Adam 配合可实现端到端弱监督训练
5. **VSP 形式化支持高阶交互**：可表示一个谓词连接多个实体的场景（如工具、多个物体），传统 SGG 无法表达

## Connections

- **vs PPR-FCN [50]**：VSPNET 在 PHRDET 弱监督上达到 17.6 R@50 vs PPR-FCN 2.4（7.3 倍提升），核心差异在于全局图对齐 vs 独立关系实例建模
- **vs Graph R-CNN [41]**：两者都试图降低全连接图的复杂度，但 VSPNET 的 VSP 形式化从根本上避免了 O(n²)（0.11s vs 0.83s）
- **vs Assoc. Emb. [27]**：同样不依赖成对提议处理，但 VSPNET 通过消息传递集成上下文信息，在 SGGEN 上领先（14.2 vs 11.3 R@100）
- **vs Factorizable Net [19]**：VSPNET 更快（0.11s vs 0.55s），但未在同一 Table 2 中直接比较召回率
- **与同一会议论文**：CVPR 2020 其他 SGG 工作的对比有待补充
- **后续工作参考**：基于弱监督场景图的方法（如 LLM4SGG、SSC-SGG）均参考了本工作的图对齐范式

## Open Questions

1. 能否将 VSP 与 DETR-like 端到端检测结合，消除对固定 Faster R-CNN 提议的依赖？
2. VSP 形式化在开放词汇场景下的扩展性如何？固定 GloVe 嵌入可能限制新类别
3. 弱监督 VSPNET 在 VG-150 上的 SGCLS/SGGEN 指标是否能超越所有全监督基线？
4. 高阶交互（如 3+ 实体连接同一谓词）的定量评估指标尚未建立
5. 动态预测 np（谓词节点数）而非固定 100 是否能进一步提升性能？

## Provenance

- **Evidence Level**: full-paper（基于全文精读）
- **Source Files**: `raw/sources/2020-06-16-weakly-supervised-visual-semantic-parsing.pdf` (1.28 MB), `raw/sources/2020-06-16-weakly-supervised-visual-semantic-parsing.txt` (47,475 chars)
- **Last Updated**: 2026-06-10
