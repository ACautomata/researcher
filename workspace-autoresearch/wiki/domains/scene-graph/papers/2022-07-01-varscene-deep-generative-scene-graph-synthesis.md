---
title: "VARSCENE: A Deep Generative Model for Realistic Scene Graph Synthesis"
type: paper
domain: scene-graph
status: active
created: 2026-06-10
updated: 2026-06-10
tags:
  - scene-graph-generation
  - generative-model
  - variational-autoencoder
  - MMD
  - ICML-2022
source_pages: []
raw_sources:
  - raw/sources/2022-07-01-varscene-scene-graph-synthesis.pdf
  - raw/sources/2022-07-01-varscene-scene-graph-synthesis.txt
related_pages: []
paper:
  title: "VARSCENE: A Deep Generative Model for Realistic Scene Graph Synthesis"
  authors:
    - Tathagat Verma
    - Abir De
    - Yateesh Agrawal
    - Vishwa Vinay
    - Soumen Chakrabarti
  year: 2022
  venue: ICML 2022
  doi: null
  code: https://cse.iitb.ac.in/~abir/codes/varscene.zip
  project: null
classification:
  label: scene-graph-generation, generative
  task:
    - Unconditional scene graph generation
    - Conditional scene graph generation
  method_family: Variational Autoencoder
  modality: Scene graphs (text-based, no images)
  datasets:
    - Visual Genome (VG)
    - Small-sized Visual Genome (SVG)
    - Visual Relationship Detection (VRD)
  metrics:
    - Star-Sim
    - Edge-Sim
    - Node-Sim
    - SP-Kernel
    - WL-Kernel
    - NSPD-Kernel
    - FID
    - Inception Score
    - Precision
    - Recall
evidence_level: full-paper
---

# VARSCENE: A Deep Generative Model for Realistic Scene Graph Synthesis

## Citation

> Tathagat Verma, Abir De, Yateesh Agrawal, Vishwa Vinay, Soumen Chakrabarti. "VARSCENE: A Deep Generative Model for Realistic Scene Graph Synthesis." ICML 2022. PMLR 162.

## One-Sentence Contribution

提出基于变分自编码器（VAE）的场景图生成模型 VARSCENE，通过将场景图分解为星图（star graphs）并以 MMD（最大均值差异）为目标优化生成分布，解决了现有图生成模型（面向分子图）在场景图大规模词表和高语义复杂度下的失效问题。

## Problem Setting

- **输入**：一批真实场景图（只包含图和节点/边类型，不含图像 modal）
- **输出**：能从学习到的分布中采样新的、语义合理的场景图
- **两种生成模式**：
  - 无条件生成：从先验分布采样 latent code Z
  - 条件生成：给定一个具体场景图 G，通过 encoder 获取 Z 再从 decoder 采样
- **核心挑战**：
  1. 场景图含大量对象类型（Visual Genome 有 16,943 种对象、8,411 种关系），远超分子图的原子类型（<15）和键类型（<10）
  2. 场景图语义隐式且复杂，不如分子图有明确的化合价规则、键位约束
  3. 仅使用 ELBO 优化的 VAE 可能无法最好地匹配真实分布

## Method

### 核心直觉

将场景图视为星图（star graph）的集合，以星为生成单元。先用 VAE 训练基础 decoder，再以 MMD 为训练目标重新优化 decoder，使其生成分布与真实分布更接近。

### Star 概念

- **Star**：由一个 hub node 表示的 object type + 该节点所有 incident edges 的 relation types 构成
- Star 的定义**不包含** neighbor node 的 identity/type，只包含中心节点的 object type 和所有 incident edge 的 relation type
- 两个不同的节点（node ID 不同）可能有相同的 star representation
- **Neighbor-star**：通过一条边连接的两个 star，定义为 N(s) 包含 (s', γ(s, s'))
- Star vocabulary S(D) 是数据集中所有 star 的集合

### 模型架构

#### 1. Prior: p0(Z)
Z = {z0, ..., zΔmax}，Δmax ~ Poisson(λ)，p0 为标准正态分布 N(0, I)

#### 2. Encoder: qφ(Z | G, T, R)
- 通过 GNN (Gilmer et al. 2017) 计算 node embeddings xu 和 edge embeddings xe, 深度 K=2, embedding dim=64
- 构建 star embeddings hs = F^S_φ(x_root(s), {x_(root(s),v) | v ∈ nbr(root(s))})
- 从 star embedding 得到 latent ζs ~ N(μ_φ(hs), σ²_φ(hs))
- 选一个 pivot star s0，将所有 star 按到 s0 的距离 Δ 分组
- 聚合每个 Δ 的 star 得到 Z = {z0, ..., zΔmax}（Δ 对应星星距离 pivot 的跳数）

#### 3. Base Decoder: pθ({si}, {γij} | Z)
- 生成方式：以 pivot star s0 为起点，按距离 Δ=1,2,... 增量生成
- 每一步 Δ 中，从 S(D) 中采样新 star sj 连接到一个现有 star si，或从已有 star 中选择连接
- Masking function MASK(s, s', r) 确保生成语义可行：仅在数据集中出现过 (s', r) ∈ N(s) 的组合才允许连接
- 第一项：从 S(D)\G_Δ 中采样新 star 并连接（softmax 概率）
- 第二项：从 G_Δ 中已有 star 连接
- pθ 通过 ELBO 训练

#### 4. MMD-Optimized Decoder: pMMD_θ
- 用预训练 decoder pbθ 参数初始化
- 优化目标：min_θ EZ[MMD(D, D(Z)) + ρ · KL(pMMD_θ || pbθ)]
  - D：训练集图集合
  - D(Z)：以 latent Z 生成的图集合
  - 图特征 ν(G) = [νs(G)] 表示 G 中每个 star s 的出现频次
  - RBF kernel k(G,G') = exp(-||ν(G)-ν(G')||²/2)
- ρ=1000 控制 MMD 与 KL 正则的权衡
- 使用 REINFORCE/log-derivative trick 求解梯度
- MMD 优化在 validation set Ddev 上训练

### 关键设计
- BERT 嵌入（paraphrase-MiniLM-L6-v2, dim=384）编码 object types 和 relation types
- MASK 机制确保生成的 scene graph 语义合理
- Star-based 生成避免了 node-by-node 生成对大规模词汇表的处理困难

## Experiments

### 数据集

| Dataset | |D| | Folds (tr:dev:te) | E[|V|] | E[|E|] | |T| | |R| |
|---------|-----|-------------------|--------|--------|------|-----|
| Visual Genome (VG) | 110,000 | 81:9:9 | 3.23 | 2.31 | 16,943 | 8,411 |
| Small-sized VG (SVG) | 124,854 | 55:12:32 | 5.31 | 4.87 | 150 | 50 |
| Visual Relationship Detection (VRD) | 7,721 | 74:12:12 | 4.29 | 3.78 | 100 | 70 |

### Baselines
1. **DeepGMG** (Li et al. 2018b) — 分子图生成
2. **MolGAN** (De Cao & Kipf 2018) — 分子图生成
3. **GraphRNN** (You et al. 2018) — 领域通用图生成
4. **GraphGen** (Goyal et al. 2020) — 领域通用图生成
5. **SceneGen** (Garg et al. 2021) — 首次提出无条件场景图生成

### 评估指标

**图分布匹配指标**（在 test set 上计算生成的图与真实图的相似度）：
- **Star-Sim**：star 分布余弦相似度
- **Edge-Sim**：edge bigram 分布余弦相似度
- **Node-Sim**：node bigram 分布余弦相似度
- **SP-Kernel**：Shortest path kernel
- **WL-Kernel**：Weisfeiler-Lehman kernel
- **NSPD-Kernel**：Neighborhood subgraph pairwise distance kernel

**图像质量指标**（对 SVG，用 sg2im 将场景图转图像）：
- Fréchet Inception Distance (FID) ↓
- Inception Score (IS) ↑
- Precision ↑ 和 Recall ↑

### 训练设置
- **VARSCENE**：pθ 训练 1000 epochs, pMMD_θ 训练 1000 epochs, batch size=1024, lr=1e-4 (pθ) / 1e-3 (pMMD_θ), Adam, weight decay=1e-5
- **参数数量**：221,249（不随数据集变化，是所有方法中最少的）
- **硬件**：Intel Xeon, 1TB RAM, TITAN RTX (24GB) / TITAN X Pascal (12GB)
- 先用 Dtr 训练 qφ 和 pθ → 用 Ddev 训练 pMMD_θ → 在 Dtest 评估

### 消融实验
- pMMD_θ vs pθ（MMD 优化 vs ELBO 基座）
- 不同优化目标替代 MMD（Star-Sim/Edge-Sim/Node-Sim等代替MMD）
- SceneGen 的隔离节点问题（通过引入 NULL relation type 揭穿）

## Results

### RQ1: 与 Baseline 对比（表 2）

**Visual Genome (VG)**：

| Model | Star-Sim | Edge-Sim | Node-Sim | SP-K | WL-K | NSPD-K |
|-------|----------|----------|----------|------|------|--------|
| DeepGMG | 0.69 | 0.46 | 0.15 | 0.01 | 0.09 | 0.01 |
| MolGAN | 0.00 | 0.00 | 0.00 | 0.00 | 0.04 | 0.01 |
| GraphGen | 0.66 | 0.37 | 0.11 | 0.00 | 0.03 | 0.01 |
| GraphRNN | 0.63 | 0.00 | 0.03 | 0.00 | 0.03 | 0.01 |
| SceneGen | 0.73 | 0.50 | 0.32 | 0.02 | 0.08 | 0.01 |
| **VARSCENE_unc** | 0.59 | 0.45 | 0.40 | **0.22** | **0.11** | 0.01 |
| **VARSCENE_cond** | **0.86** | **0.52** | **0.62** | 0.08 | 0.07 | 0.01 |

**Small-sized VG (SVG)**：

| Model | Star-Sim | Edge-Sim | Node-Sim | SP-K | WL-K | NSPD-K |
|-------|----------|----------|----------|------|------|--------|
| DeepGMG | 0.80 | 0.64 | 0.49 | 0.10 | 0.35 | 0.05 |
| MolGAN | 0.00 | 0.00 | 0.00 | 0.04 | 0.40 | 0.08 |
| GraphGen | 0.52 | 0.64 | 0.37 | 0.05 | 0.21 | 0.04 |
| GraphRNN | 0.25 | 0.07 | 0.09 | 0.38 | 0.59 | 0.07 |
| SceneGen | 0.86 | **0.88** | **0.93** | 0.68 | 0.54 | 0.06 |
| **VARSCENE_unc** | **0.92** | 0.70 | 0.83 | **1.00** | **0.65** | 0.06 |
| **VARSCENE_cond** | 0.91 | 0.69 | 0.81 | 0.96 | 0.64 | 0.06 |

**Visual Relationship Detection (VRD)**：

| Model | Star-Sim | Edge-Sim | Node-Sim | SP-K | WL-K | NSPD-K |
|-------|----------|----------|----------|------|------|--------|
| DeepGMG | 0.74 | 0.73 | 0.60 | 0.99 | 1.41 | 0.20 |
| MolGAN | 0.00 | 0.00 | 0.00 | 0.01 | 0.97 | 0.21 |
| GraphGen | 0.64 | 0.75 | 0.64 | 0.31 | 0.79 | 0.17 |
| GraphRNN | 0.54 | 0.29 | 0.71 | 0.21 | 0.76 | 0.18 |
| SceneGen | 0.81 | **0.94** | **0.95** | 0.60 | 1.12 | 0.21 |
| **VARSCENE_unc** | **0.91** | 0.93 | 0.94 | 1.03 | 1.56 | **0.23** |
| **VARSCENE_cond** | **0.91** | 0.93 | 0.93 | **1.45** | **1.92** | 0.22 |

**关键发现**：
- VARSCENE 在 VG 上全面优于所有 baseline（大词表场景下优势最明显）
- SceneGen 在 SVG/VRD 上 Edge-Sim/Node-Sim 表现好，但原因在于它生成了大量隔离节点（孤立的节点），bigram 相似度无法惩罚这种问题
- 引入 NULL relation type 后（表3），SceneGen 在 VG 上 Edge-Sim 从 0.50 降至 0.09，Node-Sim 从 0.32 降至 0.11，表现远差于 VARSCENE_cond（Edge 0.53, Node 0.62）
- MolGAN 在所有数据集上失效（接近零分），反映分子图专用方法不适用于场景图
- DeepGMG 在部分 kernel 指标上表现尚可

### RQ2: MMD 优化的效果（表 4）

| Dataset | Metric | pθ (ELBO) | pMMD_θ |
|---------|--------|-----------|---------|
| VG | Star-Sim | 0.5867 | **0.8660** |
| VG | Edge-Sim | 0.2588 | **0.5268** |
| SVG | Star-Sim | 0.7120 | **0.9182** |
| SVG | Edge-Sim | 0.4195 | **0.6964** |
| VRD | Star-Sim | 0.8988 | **0.9140** |
| VRD | Edge-Sim | 0.9339 | **0.9372** |

MMD 优化在小数据集和大数据集上都带来显著增益，尤其在 VG 上 Star-Sim 从 0.59 提升至 0.87。

### RQ3: 图像质量（表 5，SVG 上通过 sg2im）

| Model | FID ↓ | IS ↑ | Precision ↑ | Recall ↑ |
|-------|-------|------|-------------|----------|
| DeepGMG | 9.83 | 4.36 | 0.9891 | 0.9800 |
| MolGAN | 240.38 | 1.17 | 0.0137 | 0.0986 |
| GraphGen | 13.28 | 4.28 | 0.9780 | 0.9607 |
| GraphRNN | 18.82 | 4.66 | 0.9432 | 0.9707 |
| SceneGen | 19.26 | 4.03 | 0.9230 | 0.9513 |
| **VARSCENE_unc** | 6.86 | **5.15** | 0.9894 | 0.9872 |
| **VARSCENE_cond** | **6.02** | 5.02 | **0.9894** | **0.9874** |

VARSCENE 的 FID（6.02/6.86）远优於所有 baseline，IS、Precision、Recall 也全面领先。

## Limitations

1. 生成基于 star vocabulary，star 的数量是预设的最大值 Δmax（受限于训练数据中的 star 集合），新场景的 star 类型组合受数据覆盖约束
2. MASK 机制限制了生成图只包含训练数据中出现过的 (s, r, s') 三元组组合，新颖组合的泛化能力有限
3. 代码链接为 zip 下载（非 GitHub 开源仓库），复现门槛相对较高
4. 仅在 3 个数据集上评估，其中 VG 的大词表版本选用了 90K 子集（原始 800K+ 图的采样）
5. 图像质量评估仅在 SVG（150 categories）上进行，未验证 VG 大词表层级上的图像生成效果
6. 模型依赖 BERT 嵌入，对象/关系名称的质量直接影响生成效果
7. pMMD_θ 的训练是在 validation set 上优化 MMD，训练效率较高（1000 epochs），但对 validation set 的依赖性意味着需要足够的验证数据

## Reusable Claims

> **Claim**: 场景图生成任务中，基于 star graph 分解的 VAE + MMD 优化显著优于 node-by-node/edge-by-edge 的图生成方法
> **Evidence**: 表2中 VARSCENE 在 VG（大词汇表）上 Star-Sim 0.86 vs SceneGen 0.73, SP-K 0.22 vs SceneGen 0.02
> **Scope**: 数据集 VG/SVG/VRD，各种规模的词表
> **Confidence**: high

> **Claim**: MMD 优化作为 VAE 后训练步骤（而非直接端到端优化），在场景图生成任务上优于纯 ELBO 优化
> **Evidence**: 表4，VG 上 Star-Sim: pθ=0.59 vs pMMD_θ=0.87
> **Scope**: 所有三个数据集
> **Confidence**: high

> **Claim**: SceneGen 在 SVG/VRD 上的看似优势源于它生成大量隔离节点的缺陷，非真实分布拟合优势
> **Evidence**: 表3，引入 NULL relation 后 SceneGen Edge-Sim 从 0.50 降至 0.09
> **Scope**: SceneGen 模型在所有三个数据集上
> **Confidence**: high

## Connections

- **SceneGen (Garg et al. 2021)**：首个无条件场景图生成器，但未做 MMD 优化且存在隔离节点问题
- **GraphVAE / GraphRNN / MolGAN / GraphGen**：面向分子图或通用图，在场景图上表现不足
- **sg2im (Johnson et al. 2018)**：将场景图转图像的生成模型，VARSCENE 生成的场景图可通过 sg2im 进一步生成图像
- **MMD 在生成模型中的应用**：与 GAN 不同，VARSCENE 用 MMD 而非对抗训练优化生成分布，类似 GMMN/MC-GAN 思路
- **Star decomposition**：将场景图分解为 star 集合，类似 subgraph-based 图表示，在 scene graph extraction 中也有类似分解思想

## Open Questions

1. 能否使用更灵活的 MASK 机制（如基于语义相似度而非严格共现）来生成新奇的 (s, r, s') 组合？
2. 在场景图生成任务中，MMD 优化 + 扩散模型的组合是否能进一步提升生成质量？
3. 场景图生成作为 scene synthesis 的前置步骤，逆过程（scene graph → image）的联合训练能否提升两端生成质量？
4. 如何处理场景图中的 long-tail relation types（现有 MASK 基于共现，对低频关系不利）？
5. 知识图谱（如 Wikidata、ConceptNet）能否作为 "realism prior" 辅助场景图生成中的语义合理性检验？

## Provenance

- **原始 PDF**: `raw/sources/2022-07-01-varscene-scene-graph-synthesis.pdf` (ICML 2022 Proceedings 官方版本)
- **全文提取**: `raw/sources/2022-07-01-varscene-scene-graph-synthesis.txt` (PyMuPDF 提取, 78K chars, 16 pages)
- **分析依据**: 全文精读，所有实验数据来自原论文 Section 5 和 Appendix D 的表 2-8
- **evidence_level**: full-paper（已完整阅读全文包括附录）
