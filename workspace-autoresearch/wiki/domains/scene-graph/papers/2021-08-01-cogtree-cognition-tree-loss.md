---
title: "CogTree: Cognition Tree Loss for Unbiased Scene Graph Generation"
type: paper
domain: scene-graph
status: active
created: 2026-06-10
updated: 2026-06-10
tags:
  - scene-graph-generation
  - debiasing
  - cognition-tree
  - hierarchical-classification
  - long-tail-bias
  - coarse-to-fine
  - IJCAI-2021
raw_sources:
  - ../../../raw/sources/2021-08-01-cogtree-cognition-tree-loss.pdf
  - ../../../raw/sources/2021-08-01-cogtree-cognition-tree-loss.txt
related_pages:
  - vctree-learning-to-compose-dynamic-tree-structures.md
  - neural-motifs-scene-graph-global-context.md
  - unbiased-scene-graph-generation-tde-causal-modeling.md
  - salience-sgg-unbiased-scene-graph-generation-via-salience-estimation.md
evidence_level: full-paper
paper:
  title: "CogTree: Cognition Tree Loss for Unbiased Scene Graph Generation"
  authors:
    - Jing Yu
    - Yuan Chai
    - Yujing Wang
    - Yue Hu
    - Qi Wu
  year: 2021
  venue: "Thirtieth International Joint Conference on Artificial Intelligence (IJCAI-21)"
  arxiv: null
  doi: null
  code: "https://github.com/CYVincent/Scene-Graph-Transformer-CogTree"
  project: null
classification:
  label: "CogTree — Cognition Tree Loss for Unbiased Scene Graph Generation"
  task:
    - Scene Graph Generation (SGG)
    - Predicate Classification (PredCls)
    - Scene Graph Classification (SGCls)
    - Scene Graph Detection (SGDet)
  method_family:
    - Hierarchical classification
    - Class-balanced reweighting
    - Coarse-to-fine learning
  modality:
    - Visual features (RoI)
    - Object bounding boxes
    - Spatial features
  datasets:
    - Visual Genome (VG)
  metrics:
    - mean Recall@K (mR@20/50/100)
    - Recall@K (R@20/50/100)
---

## Citation

Yu, J., Chai, Y., Wang, Y., Hu, Y., Wu, Q. "CogTree: Cognition Tree Loss for Unbiased Scene Graph Generation." IJCAI 2021, pp. 1274-1280. [Paper](https://www.ijcai.org/proceedings/2021/0176.pdf) | [Code](https://github.com/CYVincent/Scene-Graph-Transformer-CogTree)

## One-Sentence Contribution

提出基于认知层次结构的 CogTree 损失函数，利用从偏置模型预测中自动构建的认知树来组织关系类别，通过粗到细（coarse-to-fine）的分类策略实现无偏场景图生成。

## Problem Setting

- **目标**：解决 SGG 中因长尾数据分布导致的偏置预测问题——尾部关系常被错误预测为头部关系（如 `walking on` → `on`、`standing on` → `on`），相似尾部关系（如 `standing on` vs `sitting on` vs `lying on`）也难以区分
- **挑战**：
  - 关系类别分布极度长尾，少量头部关系占据绝大多数样本
  - 尾部关系的视觉相似性和稀疏训练数据导致分类混淆
  - 传统方法仅在数据分布平衡、无偏模型学习和表示解耦层面处理，忽略了偏置类别间的内在关联结构
- **关键洞察**：人脑通过前额叶皮层的层次化推理机制处理信息——先粗区分明显不同的关系，再聚焦于容易混淆的细节差异。受此启发，论文从偏置模型的预测中自动构建关系之间的认知层次结构
- **设定**：标准 SGG 设定（PredCls、SGCls、SGDet），在 Visual Genome 标准划分上评估

## Method

### 架构概览

CogTree 损失是模型无关（model-agnostic）的，可应用于各种 SGG 模型。论文对其在三个模型上进行了案例研究：MOTIFS、VCTree 以及自建的 SG-Transformer（基于 Transformer 的 SGG 模型）。

完整框架包含三部分（Figure 2）：
1. **偏置驱动的 CogTree 构建**：从预训练的偏置 SGG 模型中自动构建认知层次树
2. **Debiasing CogTree 损失**：基于树结构的粗到细去偏损失函数
3. **SGG 网络**：标准的目标分类 + 关系分类流水线

### 自动 CogTree 构建（§ 3.1）

三步构建过程：

**Step 1: Bias-Adaptive Concept Induction（偏置自适应概念归纳）**：
- 对每个真实类别 dᵢ 的样本，用偏置模型预测其标签，获得预测频率分布 Pᵢ
- 将最频繁预测的类别 dⱼ 视为该真实类别的"概念关系"
- 将所有关系归纳为 C 个概念，每个概念对应一个概念关系 cᵢ

**Step 2: Concept-Centered Subtree Building（以概念为中心的子树构建）**：
- 对每个概念构建一颗子树，根为 cᵢ，叶子为归纳到该概念的细粒度关系
- 若子树仅含根节点（如 `parked on` 作为概念但无其他关系属于它），则进一步归纳到 Pᵢ 中第二高频的概念关系

**Step 3: Cognition-Based Subtree Aggregation（认知驱动的子树聚合）**：
- 聚合 T 个子树为完整的层次 CogTree（Figure 3）
- CogTree 包含四个功能层：
  - **Root Layer (y₀)**：虚拟根节点
  - **Concept Layer (y₁)**：区分输入属于哪个概念，含 T 个虚拟节点
  - **Coarse-fine Layer (y₂)**：判断输入是否可由粗粒度或细粒度关系描述，每个 y₁ 节点分裂为两个——一个叶子节点（粗粒度概念关系）和一个虚拟节点（细粒度关系簇）
  - **Fine-grained Layer (y₃)**：区分同一概念中易混淆的细粒度关系（如 `standing on` vs `walking on`）

### Debiasing CogTree 损失（§ 3.2）

CogTree 损失包含两个互补的项：

**Ground-Truth CogTree Path (GCP)**：给定样本的真实标签，从根到对应叶子节点的路径 Lpath = {l₀, l₁, ..., lM}

**Predicted CogTree Probability (PCP)**：树中每个节点的预测概率，通过自顶向下的平均聚合计算（式 1）：
- 叶子节点：zᵢ = pₖ（该类别的 softmax 概率）
- 非叶子节点：zᵢ = (1/|C(i)|) Σⱼ∈C(ᵢ) zⱼ（子节点的平均）

**Class-Balanced Weight (CBW)**：基于 [Cui et al., 2019] 的类平衡权重（式 2）：
- 叶子节点：wᵢ = (1−β)/(1−βⁿⁱ)
- 非叶子节点：wᵢ = (1/|C(i)|) Σⱼ∈C(ᵢ) wⱼ（子节点权重的平均）

**TCB Loss（式 3）**：CogTree-based Class-Balanced 损失，在 GCP 路径上每层计算类平衡 softmax 交叉熵损失后取平均：
- LTCB = (1/|Lpath|) Σᵢ∈Lpath −wᵢ log(exp(zᵢ)/Σⱼ∈B(ᵢ) exp(zⱼ))
- 其中 B(i) 表示节点 i 的兄弟节点
- 该损失强制网络：先超越概念间噪声学习概念特定嵌入 → 再超越概念内噪声精炼关系特定嵌入

**CB Loss（式 4）**：标准类平衡 softmax 交叉熵损失（基于 [Cui et al., 2019] 的权重因子）：
- LCB = −wₖ log(exp(pₖ)/Σⱼ exp(pⱼ))

**完整 CogTree Loss（式 5）**：L = LCB + λLTCB，λ 默认设为 1

### SG-Transformer（§ 3.3）

论文自建的强基线模型，将 Transformer 架构引入 SGG：

- **Object Encoder**：N 个 Object-to-Object (O2O) Transformer 块，输入为物体嵌入 {vᵢ}ᴷ
- **Relation Encoder**：M 个 Relation-to-Object (R2O) Transformer 块，输入为关系嵌入 {rᵢⱼ}ᴷˣᴷ 和物体嵌入 {mᵢ}ᴷ
- 关系嵌入 rᵢⱼ 由三类特征组合：空间特征、联合区域特征、物体标签的词嵌入（GloVe）
- 编解码器输出经全连接层 + softmax 分类

## Experiments

### 数据集与划分

- **Visual Genome (VG)** [Krishna et al., 2017]：标准划分 [Xu et al., 2017]
- 最频繁的 150 个物体类别和 50 个谓词类别
- VG 划分仅有训练集和测试集，遵循 [Zellers et al., 2018] 从训练集中采样 5K 验证集
- 训练集 57,723 张，测试集 26,446 张

### 评估协议

三个子任务 [Zellers et al., 2018]：
- **Predicate Classification (PredCls)**：使用真实物体标签和边界框进行关系预测
- **Scene Graph Classification (SGCls)**：使用真实边界框进行物体和关系预测
- **Scene Graph Detection (SGDet)**：从零开始完整场景图预测

评估指标：
- **Recall@K (R@K)**：报告但非主要指标（因存在偏置问题）
- **mean Recall@K (mR@K)**：**主要指标**，每类独立计算 R@K 后取平均 [Chen et al., 2019; Tang et al., 2019]

### 模型与基线

**基线 SGG 模型**：
- **IMP+** [Xu et al., 2017]：迭代消息传递
- **FREQ** [Zellers et al., 2018]：频率基线
- **KERN** [Chen et al., 2019]：知识嵌入路由网络
- **MOTIFS** [Zellers et al., 2018]：LSTM 序列模型
- **VCTree** [Tang et al., 2019]：动态树结构模型
- **SG-Transformer**：论文自建的 Transformer 模型

**去偏基线**：
- **Focal Loss** [Lin et al., 2017]
- **Reweight**：基于 [Cui et al., 2019] 的类平衡重加权
- **Resample**：重采样
- **TDE** [Tang et al., 2020]：总直接效应的因果去偏方法

### 训练设置

- 检测器：预训练 Faster R-CNN (ResNeXt-101-FPN)
- 优化器：SGD，5 个 epoch
- Batch size：12
- 学习率：1.2 × 10⁻³
- CogTree 超参：λ = 1，β = 0.999
- SG-Transformer：3 个 O2O 块 + 2 个 R2O 块，12 个注意力头
- 硬件：NVIDIA Tesla V100 GPU

### 消融实验

消融研究（Table 3，基于 SG-Transformer）系统检验了以下设计选择：
1. **损失项贡献**：LTCB（单独使用）、LCB（单独使用）、LTCE（移除权重）、LCE（移除权重）
2. **树构建策略**：Fuse-subtree（混合不同概念到同一子树）、Fuse-layer（混合粗细粒度到同一层）
3. **PCP/CBW 聚合方法**：L(MAX) 和 L(SUM) vs 默认 AVERAGE
4. **平衡权重 λ**：在 [0.4, 1.6] 范围内调参（Table 4）

## Results

### 主实验结果（Table 1）

以 mR@K 为主要指标，CogTree 在所有三个子任务上的一致提升：

**MOTIFS + CogTree**（对比 MOTIFS* Baseline）：
- PredCls mR@20/50/100：**20.9/26.4/29.0** vs 11.5/14.6/15.8（绝对提升 **+9.4/+11.8/+13.2**）
- SGCls mR@20/50/100：**12.1/14.9/16.1** vs 6.5/8.0/8.5（绝对提升 **+5.6/+6.9/+7.6**）
- SGDet mR@20/50/100：**7.9/10.4/11.8** vs 4.1/5.5/6.8（绝对提升 **+3.8/+4.9/+5.0**）

**VCTree + CogTree**（对比 VCTree* Baseline）：
- PredCls mR@20/50/100：**22.0/27.6/29.7** vs 11.7/14.9/16.1（绝对提升 **+10.3/+12.7/+13.6**）
- SGCls mR@20/50/100：**15.4/18.8/19.9** vs 6.2/7.5/7.9（绝对提升 **+9.2/+11.3/+12.0**）
- SGDet mR@20/50/100：**7.8/10.4/12.1** vs 4.2/5.7/6.9（绝对提升 **+3.6/+4.7/+5.2**）

**SG-Transformer + CogTree**（对比 SG-Transformer Baseline）：
- PredCls mR@20/50/100：**22.9/28.4/31.0** vs 14.8/19.2/20.5（绝对提升 **+8.1/+9.2/+10.5**）
- SGCls mR@20/50/100：**13.0/15.7/16.7** vs 8.9/11.6/12.6（绝对提升 **+4.1/+4.1/+4.1**）
- SGDet mR@20/50/100：**7.9/11.1/12.7** vs 5.6/7.7/9.0（绝对提升 **+2.3/+3.4/+3.7**）

**与其他去偏方法对比**（基于 MOTIFS）：
- CogTree 在 mR@K 上全面超越 Focal Loss、Reweight、Resample 和 TDE
- 例如 PredCls mR@50：CogTree **26.4** vs TDE 25.5 vs Reweight 20.0 vs Focal 13.9 vs Resample 18.5
- 在最强基线 VCTree 上，CogTree 同时在 mR@K 和大部分 R@K 指标上超越 TDE

### 尾部 R@K 分析（Table 2）

尾部 45 个类别的 R@K（PredCls）：
| 方法 | R@20 | R@50 | R@100 |
|------|------|------|-------|
| MOTIFS baseline | 35.0 | 36.7 | 37.0 |
| MOTIFS+CogTree | **51.6** | **57.7** | **59.8** |
| VCTree baseline | 35.0 | 36.5 | 36.8 |
| VCTree+CogTree | **51.6** | **57.2** | **58.9** |
| SG-Transformer baseline | 38.0 | 39.6 | 39.9 |
| SG-Transformer+CogTree | **48.7** | **54.5** | **56.4** |

- R@K 绝对值提升约 +10.7~21.0 pp，表明 CogTree 在不牺牲主指标的情况下显著提升了尾部类别的预测准确性

### 消融结果（Table 3，SG-Transformer 上完整消融）

| 配置 | PredCls mR@20/50/100 | SGCls mR@20/50/100 | SGDet mR@20/50/100 |
|------|-----------------------|---------------------|--------------------|
| Full loss (L=LCB+λLTCB) | **22.89/28.38/30.97** | **12.96/15.68/16.72** | **7.92/11.05/12.70** |
| LTCB 单独 | 21.08/27.08/29.41 | 12.15/15.07/16.15 | 7.70/10.39/12.07 |
| LCB 单独 | 18.02/23.40/25.25 | 10.76/13.13/13.88 | 6.74/9.56/11.29 |
| LTCE（LTCB 移除权重） | 21.16/26.14/28.32 | 12.14/14.42/15.29 | 7.57/10.53/11.86 |
| LCE（LCB 移除权重） | 14.35/18.48/20.21 | 8.57/11.46/12.27 | 5.55/7.74/8.98 |
| Fuse-subtree | 16.20/20.17/22.12 | 8.71/10.66/11.61 | 5.36/7.19/8.28 |
| Fuse-layer | 13.77/18.87/20.77 | 8.17/10.39/11.32 | 5.86/8.02/9.05 |
| L(MAX) | 15.48/19.93/21.87 | 8.97/10.85/11.83 | 5.38/7.16/8.16 |
| L(SUM) | 11.31/15.67/17.98 | 6.58/8.82/9.86 | 1.86/3.09/3.68 |

消融关键发现：
1. **LTCB + LCB 具有互补性**：联合使用优于单独使用（PredCls mR@20 22.89 vs 21.08 或 18.02）
2. **权重策略有效**：LTCE (21.08) 和 LCE (18.02) 均低于带权版本，验证了类平衡权重的重要性
3. **树结构原则不可或缺**：违反概念分组（Fuse-subtree）或粗细层次分离（Fuse-layer）均导致显著下降
4. **AVERAGE 优于 MAX/SUM**：MAX 和 SUM 增加预测概率、降低错误分类惩罚效果

### 平衡权重 λ 分析（Table 4）

- λ = 1 在大多数指标上表现最佳
- 在 [0.7, 1.3] 范围内性能仅轻微下降
- PredCls mR@50：λ=1 的 28.38 对比 λ=0.4 的 27.20、λ=1.6 的 26.80

### 标注偏置分析（Figure 5）

论文注意到 R@K 下降伴随 mR@K 上升的现象，并分析：
- 标注者偏好简单模糊的标签（因有限理性 [Simon, 1990]），形成头部类别
- CogTree 偏好细粒度、语义丰富的尾部标签
- 将 CogTree "错误"预测为细粒度尾部关系（实为更准确的预测）实际上是正确的

### 定性分析（Figure 6）

可视化显示 CogTree 的三类改进：
1. **更细粒度**：baseline 预测 `on`/`near`，CogTree 预测 `parked on`/`in front of`
2. **准确区分相似关系**：`walking on` vs `standing on`，`in front of` vs `behind`
3. **消歧**：在复杂场景中准确识别尾部关系

## Limitations

1. **CogTree 构建依赖偏置模型质量**：若偏置模型预测质量过低，归纳的概念结构可能不准确，影响损失函数效果
2. **R@K 下降**：虽然 mR@K 大幅提升，但常规 R@K 因偏好细粒度预测而下降；论文通过尾部 R@K 分析证明了真实改进，但整体 R@K 的下降在实践中可能影响与下游任务的兼容性
3. **概念归纳的单一性**：每个关系仅属于一个概念（硬分配），但某些关系可能在多个概念间共享属性，多分配或软分配可能进一步提升性能
4. **仅 VG 单一数据集评估**：未在 OpenImages V6 或其他 SGG 基准上验证
5. **超参敏感度**：β（类平衡权重）需要调节（β=0.999），不同数据集可能需要不同的 β 设置
6. **树结构的静态性**：CogTree 一旦构建固定不变，不随训练过程动态调整

## Reusable Claims

1. **关系类别间的层次结构可以从偏置模型预测中自动归纳**：偏置模型的预测模式编码了关系之间的相似性和从属关系，无需额外的监督信号
2. **粗到细（Coarse-to-fine）的分类策略是有效的 SGG 去偏机制**：先区分概念再精炼细节，显著缓解了长尾偏置（在 VCTree 上 mR@K 提升 +10.3~13.6 pp）
3. **层次损失与类平衡重加权具有互补性**：LB + LTCB 的联合使用优于单独任一损失项
4. **CogTree 是模型无关且即插即用的**：在所有三个 SGG 模型上均取得一致提升，无需修改模型架构
5. **SGG 的 R@K 高不代表预测好**：标注偏置导致头部类别的虚高（annotators prefer simple labels），mR@K 和尾部 R@K 提供了更公平的评估视角
6. **SG-Transformer**：首次将 Transformer 架构系统应用于 SGG 关系编码，为后续 Transformer-based SGG 方法（如 RelTR、SGTR）提供参考

## Connections

- **与 VCTree [Tang et al., 2019] 的关系**：CogTree 利用 VCTree 的树结构编码器作为 SGG 模型之一，但 CogTree 的树是认知层次结构而非动态视觉结构
- **与 TDE [Tang et al., 2020] 的关系**：CogTree 和 TDE 均致力于 SGG 去偏但路径不同——TDE 通过因果干预解耦表示，CogTree 通过层次化分类渐进去偏；二者互补（CogTree 在 VCTree 上同时超越 TDE 的 mR@K 和部分 R@K）
- **与类平衡损失 [Cui et al., 2019] 的关系**：CogTree 直接继承了 CB loss 的权重方案
- **与后序 SGG 去偏工作的关系**：CogTree 的主旨（粗到细分类）后来被 HiLo（CVPR 2023）等高频/低频分解方法继承和扩展
- **与 CFA [2023] 的关系**：两者均解决长尾偏置但方法互补——CogTree 通过分类策略去偏，CFA 通过数据增强去偏

## Open Questions

1. 能否构建动态自适应的 CogTree，在训练过程中根据模型演化调整树结构？
2. 软分配（一个关系属于多个概念）能否提升树结构的表达能力？
3. CogTree 能否推广到其他长尾分类场景（如细粒度识别、关系抽取中的长尾问题）？
4. 结合概念知识（如 WordNet 或常识知识库）是否能够改进概念归纳的质量？
5. CogTree 的层次结构与后续扩散模型（如 DiffVSGG）的结合效果如何？

## Provenance

- **Raw source**: `raw/sources/2021-08-01-cogtree-cognition-tree-loss.pdf` (IJCAI 2021 proceedings)
- **Extracted text**: 38,469 chars, all sections covered (Abstract, Introduction, Related Work, Method (§3), Experiments (§4), Results (§4.1-4.4), Conclusion)
- **Evidence level**: full-paper
- **Verification**: All numerical results transcribed from Table 1 (p.1277), Table 2 (p.1277), Table 3 (p.1278), Table 4 (p.1279), and supporting text. Cross-checked: consistent with in-paper values.
