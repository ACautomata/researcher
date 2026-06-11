---
title: Motion-aware Contrastive Learning for Temporal Panoptic Scene Graph Generation
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - temporal-scene-graph
  - panoptic-scene-graph
  - contrastive-learning
  - motion-awareness
  - optimal-transport
  - video-scene-graph
  - 4d-scene-graph
  - psg4d
  - opensg
  - aaai-2025
raw_sources:
  - raw/sources/2025-AAAI-Motion-aware-Contrastive-Learning-for-Temporal-Panoptic-SGG.pdf
  - raw/sources/2025-AAAI-Motion-aware-Contrastive-Learning-for-Temporal-Panoptic-SGG.txt
paper:
  title: Motion-aware Contrastive Learning for Temporal Panoptic Scene Graph Generation
  authors:
    - Thong Thanh Nguyen
    - Xiaobao Wu
    - Yi Bin
    - Cong-Duy T Nguyen
    - See-Kiong Ng
    - Anh Tuan Luu
  year: 2025
  venue: AAAI 2025
  arxiv: null
  doi: null
  code: null
  project: null
classification:
  label: MCL-TPSGG
  task:
    - Temporal Panoptic Scene Graph Generation
    - Video Scene Graph Generation
    - 4D Scene Graph Generation
  method_family:
    - Contrastive Learning
    - Mask Tube Representation Learning
    - Optimal Transport
  modality:
    - Video (RGB)
    - 4D RGB-D Video
    - 4D Point Cloud Video
  datasets:
    - OpenPVSG
    - PSG4D-GTA
    - PSG4D-HOI
  metrics:
    - R@K
    - mR@K
evidence_level: full-paper
---

# Motion-aware Contrastive Learning for Temporal Panoptic Scene Graph Generation

## Citation

Thong Thanh Nguyen, Xiaobao Wu, Yi Bin, Cong-Duy T Nguyen, See-Kiong Ng, Anh Tuan Luu. "Motion-aware Contrastive Learning for Temporal Panoptic Scene Graph Generation." AAAI 2025.

## One-Sentence Contribution

提出基于**运动感知对比学习**的框架，利用 optimal transport 度量 mask tube 间的运动相似性，通过 shuffle-based 和 triplet-based 两种对比策略推动模型学习运动敏感的特征表示，显著提升时序全景场景图生成在动态关系上的性能。

## Problem Setting

**出发点**：现有时序全景场景图生成方法（如 IPS+T、VPS、PSG4DFormer）在分割获得 mask tubes 后，通过全局池化（temporal pooling）编码 tube 特征进行分类。这种操作会**展平时序维度**，丢失表征实体间动态关系的关键运动信息，导致模型在动态关系（kicking, opening, running on）上表现显著弱于静态关系（on, sitting on, standing on）。

**核心挑战**：
1. 如何让 mask tube 的表示保留运动信息，而不是被全局池化压平？
2. 如何在不同视频的相似 triplets 之间建立运动模式的对齐？
3. 如何度量不同长度 mask tubes 之间的运动相似性？

**任务定义**：给定视频 V（RGB: R^{T×H×W×3}，RGB-D: R^{T×H×W×4}，或点云: R^{T×M×6}），输出动态场景图 G = (M, O, R)，其中 M 为 binary mask tubes，O 为实体标签，R 为关系集合。

## Method

### 整体框架

基于已有两步式 pipeline（分割 → 关系分类），在关系分类阶段引入 motion-aware contrastive learning。框架如图 3 所示。

### Step 1: Temporal Panoptic Segmentation

采用两种分割方案（与 [[panoptic-video-scene-graph-generation]](PVSG) 一致）：
- **IPS+T**：Mask2Former + UniTrack tracker，逐帧分割后关联
- **VPS**：Video K-Net，端到端视频分割+跟踪
- **4D 场景**：PSG4DFormer 基线，ResNet-101 (RGB-D) / DKNet (点云)

### Step 2: Relation Classification with Contrastive Learning

#### 基础模块
分割后产出 mask tubes → 自注意力/卷积编码得到 H_i ∈ R^{T×D} → 全局池化 + concat + MLP 分类。本文在此基础上加入对比学习分支。

#### 对比学习框架

**Anchor 构造**：对每个 groundtruth subject-relation-object triplet，将其 subject tube 表示 H_sub 和 object tube 表示 H_obj 拼接得到 anchor H_a = [H_sub, H_obj] ∈ R^{T×2D}。

**对比目标**（InfoNCE-style）：

$$L_{\text{cont}} = -\log\frac{e^{\text{sim}(H_a, H_p)}}{e^{\text{sim}(H_a, H_p)} + \sum_{z=1}^{N_n} e^{\text{sim}(H_a, H_n^z)}}$$

#### 正负样本设计

**正采样**：从**不同视频**中选取相同 subject 类别、object 类别和 relation 类别的 triplet 的 mask tube 表示。由于两个视频视觉特征不同，模型必须依赖共享的**运动模式**来对齐，而非视觉语义。

**负采样（两种策略）**：

1. **Shuffle-based Contrastive Learning**：
   - 对 anchor tube 进行时间维度随机排列（shuffle）得到负样本 H_n = π(H_a)
   - 迫使模型区分正常时序 vs 乱序版本——两者视觉语义相同，只能通过运动信息区分
   - **强运动选择策略**：对静态关系（如 on, next to），shuffle 后与原始几乎相同。通过光流边（Sobel filter on flow magnitude）计算 mask tube 的运动强度，选取超过阈值 γ 的 tube 进行 shuffle。γ=9.0（经验证选取）。

2. **Triplet-based Contrastive Learning**：
   - 从**同一视频**中选择不同 triplets 作为负样本
   - 设计多项分布，优先选择与 anchor 共享更多类别（subject/relation/object）的 triplet，构造**难负样本**
   - 同一视频视觉特征接近，迫使模型依赖运动语义来区分

#### Optimal Transport 距离度量

核心问题：如何定义两个 mask tube 表示 H_i 和 H_j 之间的相似度？

**方法**：将两个 mask tube 视为两个离散分布 μ 和 ν，通过 Sinkhorn 算法求解最优运输（optimal transport）距离。

$$\mu = \sum_{k=1}^{T_i} a_k \delta_{h_{i,k}}, \quad \nu = \sum_{l=1}^{T_j} b_l \delta_{h_{j,l}}$$

- 权重均匀分布：a = 1/T_i, b = 1/T_j
- 代价函数：cosine 距离 c(h_{i,k}, h_{j,l}) = 1 - (h_{i,k}·h_{j,l})/(‖h_{i,k}‖_2·‖h_{j,l}‖_2)
- 运输约束：T1_{T_i} ≤ a, T^T 1_{T_j} ≤ b, 总运输量 s ∈ [0, min(T_i, T_j)]
- 通过 Sinkhorn 迭代求解，Niter=1000
- 相似度：sim(H_a, H_p) = α - d_OT, α=10.0

OT 距离的优势：可处理不同长度的 mask tubes，保留时序演化轨迹信息，对比 pooling + 余弦相似度/L2 更有效。

## Experiments

### 数据集

- **OpenPVSG** (Yang et al., 2023): 400 个视频（289 third-person + 111 egocentric），126 物体类别，57 关系类别
- **PSG4D-GTA**: 67 个第三人称视频，35 物体类别，43 关系类别，平均时长 84 秒
- **PSG4D-HOI**: 2,973 个第一人称视频，46 物体类别，15 关系类别，平均时长 20 秒，室内场景

### 评估协议

- R@K 和 mR@K (K=20, 50, 100)
- vIoU 阈值：0.5（严格）和 0.1（宽松）
- 成功条件：(1) subject/object/predicate 类别正确 (2) mask tube 的 vIoU ≥ 阈值

### 实现细节

- IPS+T: Mask2Former + UniTrack，COCO 预训练，8 epochs，AdamW lr=1e-4，batch=32
- VPS: Video K-Net，COCO 预训练，同上策略
- 关系分类 fine-tune: Adam lr=1e-3，batch=32
- 4D: PSG4DFormer 基线，ResNet-101 (RGB-D) / DKNet (点云)
- 分割 fine-tune: 12 epochs (RGB-D) / 200 epochs (点云)
- 关系分类 fine-tune: 额外 100 epochs
- γ=9.0, α=10.0, Niter=1000

## Results

### 主结果 — OpenPVSG（Table 1）

**IPS+T 设置**（vIoU=0.5）：

| Method | R/mR@20 | R/mR@50 | R/mR@100 |
|--------|---------|---------|----------|
| IPS+T - Vanilla | 3.04/1.35 | 4.61/2.94 | 5.56/3.33 |
| IPS+T - Transformer | 3.88/2.81 | 5.66/4.12 | 6.18/4.44 |
| IPS+T - Convolution | 3.88/2.55 | 5.24/3.29 | 6.71/5.36 |
| **Ours - Transformer** | **3.98/2.98** | **5.97/4.20** | **7.44/5.15** |
| **Ours - Convolution** | **4.51/3.56** | **6.08/4.38** | **7.76/5.86** |

**IPS+T 设置**（vIoU=0.1）：

| Method | R/mR@20 | R/mR@50 | R/mR@100 |
|--------|---------|---------|----------|
| IPS+T - Transformer | 9.01/6.69 | 14.88/11.28 | 17.51/13.20 |
| IPS+T - Convolution | 10.06/8.98 | 14.99/12.21 | 18.13/15.47 |
| **Ours - Transformer** | **10.59/9.56** | **16.98/12.39** | **22.33/17.47** |
| **Ours - Convolution** | **11.43/9.57** | **17.30/13.13** | **22.85/17.48** |

**关键提升**（vIoU=0.5）：
- Ours - Convolution vs. IPS+T - Convolution：R/mR@50 **提高 0.84/1.09** 点
- Ours - Transformer vs. IPS+T - Transformer：R/mR@100 **提高 1.26/0.71** 点

**VPS 设置**（vIoU=0.5, R/mR@100）：Ours - Convolution 达 **1.26/1.22**，Ours - Transformer 达 **1.05/0.76**

### 主结果 — PSG4D（Table 2）

**点云视频 — PSG4D-GTA**：

| Method | R/mR@20 | R/mR@50 | R/mR@100 |
|--------|---------|---------|----------|
| PSG4DFormer | 4.33/2.10 | 4.83/2.93 | 5.22/3.13 |
| **Ours** | **5.88/3.45** | **6.31/3.70** | **7.31/4.70** |

**点云视频 — PSG4D-HOI**：

| Method | R/mR@20 | R/mR@50 | R/mR@100 |
|--------|---------|---------|----------|
| PSG4DFormer | 5.36/3.10 | 5.61/3.95 | 6.76/4.17 |
| **Ours** | **7.28/5.09** | **7.62/6.49** | **9.18/6.85** |

**RGB-D 视频 — PSG4D-GTA**：

| Method | R/mR@20 | R/mR@50 | R/mR@100 |
|--------|---------|---------|----------|
| PSG4DFormer | 6.68/3.31 | 7.17/3.85 | 7.22/4.02 |
| **Ours** | **9.07/5.52** | **9.73/6.32** | **9.73/6.32** |

**RGB-D 视频 — PSG4D-HOI**：

| Method | R/mR@20 | R/mR@50 | R/mR@100 |
|--------|---------|---------|----------|
| PSG4DFormer | 5.62/3.65 | 6.16/4.16 | 6.28/4.97 |
| **Ours** | **7.63/6.09** | **8.36/6.94** | **8.53/8.29** |

**关键提升**：
- 点云 PSG4D-HOI R/mR@50：+2.01/+2.54（vs. PSG4DFormer）
- RGB-D PSG4D-GTA R/mR@20：+2.39/+2.21（vs. PSG4DFormer）
- RGB-D PSG4D-HOI R/mR@20：+2.01/+2.44（vs. PSG4DFormer）

### 消融实验 — OpenPVSG（Table 3）

| 设置 | R/mR@20 | R/mR@50 | R/mR@100 |
|------|---------|---------|----------|
| w/o shuffle-based | 4.41/3.43 | 5.90/4.24 | 7.30/5.79 |
| w/o triplet-based | 4.44/3.50 | 6.02/4.28 | 7.36/5.83 |
| **Ours** | **4.51/3.56** | **6.08/4.38** | **7.44/5.86** |

- 两者都贡献性能，triplet-based 略优于 shuffle-based
- 推测：shuffle-based 更专注于运动语义

### 消融实验 — OT 距离（Table 4）

| Tube 关系量化 | R/mR@20 | R/mR@50 | R/mR@100 |
|--------------|---------|---------|----------|
| Pooling + Cosine | 4.44/3.40 | 6.04/4.36 | 7.36/5.84 |
| Pooling + L2 | 4.36/3.37 | 3.77/5.95 | 7.29/5.80 |
| **Optimal Transport** | **4.51/3.56** | **6.08/4.38** | **7.44/5.86** |

- OT 距离优于所有 pooling-based 方法

### 强运动阈值 γ 消融（Figure 5）

- γ=9 达到最佳 R@50（约 6.07）
- γ 过低时弱 motion tube 被 shuffle 无法区分
- γ 过高时过多 tube 被排除，限制对比学习效果

### 定性分析（Figure 2）

可视化显示本方法在动态关系（kicking, opening, running on）上正确预测，而基线倾向于预测静态关系（on, next to）。Figure 1 的统计对比证实本方法在动态关系 recall 上显著优于 IPS+T - Convolution。

## Limitations

1. **静态关系饱和**：方法主要提升动态关系，静态关系（on, next to）提升有限
2. **强运动阈值依赖**：γ=9.0 需手工调参，不同数据集/场景最优 γ 可能不同
3. **计算开销**：Optimal Transport 的 Sinkhorn 迭代（1000 步）增加训练计算量
4. **场景普适性**：OpenPVSG 和 PSG4D 数据集仍相对有限，在更多样化场景上的泛化性待验证

## Reusable Claims

> **Claim**: 通过 shuffle-based 和 triplet-based 对比学习，模型可以学习运动敏感的 mask tube 表示，显著提升动态关系（kicking, opening, running on）的识别。
> **Evidence**: Figure 1 — 动态关系 recall 显著高于 IPS+T-Conv；Table 1 — Ours-Conv vs IPS+T-Conv R@50 从 5.24→6.08 (+16%)。
> **Scope**: OpenPVSG/PSG4D 数据集，用 IPS+T/VPS 分割框架
> **Confidence**: high

> **Claim**: Optimal Transport 距离比「池化+余弦相似度」更有效地度量 mask tube 间的运动相似性，因为 OT 保留了时序轨迹演化信息。
> **Evidence**: Table 4 — OT vs Pooling+Cosine R/mR@100 7.44/5.86 vs 7.36/5.84；Table 6 — PSG4D-HOI 点云 R/mR@100 9.18/6.85 vs 8.20/6.64。
> **Scope**: mask tube 相似度度量，图 3 框架
> **Confidence**: medium（提升幅度较小但对所有设置一致）

> **Claim**: 不同视频中相同 subject-relation-object 类别的 mask tube 存在共享的运动模式，通过跨视频正样本对比学习可捕获。
> **Evidence**: Table 1 — 对比学习提升在动态关系 recall 上显著
> **Scope**: OpenPVSG, PSG4D
> **Confidence**: high

## Connections

- 建立在 [[panoptic-video-scene-graph-generation]]（PVSG）的任务框架和基线之上，从运动角度改进关系分类
- 与 [[tempura-unbiased-video-scene-graph-generation]]（TEMPURA）同为视频 SGG 中的运动/时序建模工作，但 TEMPURA 使用 bounding box 且侧重去偏
- 与 [[4d-panoptic-scene-graph-generation]]（PSG-4D）直接相关，本文在 4D 数据上也验证了有效性
- 对比学习机制借鉴 [[CLIP]] / [[MoCo]] / [[SimCLR]] 中的 InfoNCE 框架，但正负样本设计针对运动感知
- Optimal Transport 距离首次被引入场景图关系分类的 tube 相似度度量

## Open Questions

1. 能否将运动感知对比学习嵌入到端到端训练框架中（而非两阶段）？
2. OT 距离的计算成本（1000 次 Sinkhorn 迭代）能否通过蒸馏或近似方法降低？
3. 对于静态关系占主导的场景（如密集室内静态场景），运动对比学习的收益有限——是否需要结合其他线索？
4. 强运动阈值 γ 的自适应设置策略？
5. 本文方法与 TEMPURA 的视频 SGG 去偏方法是否可以互补？

## Provenance

- 原始 PDF 路径：`raw/sources/2025-AAAI-Motion-aware-Contrastive-Learning-for-Temporal-Panoptic-SGG.pdf`
- 全文提取文本：`raw/sources/2025-AAAI-Motion-aware-Contrastive-Learning-for-Temporal-Panoptic-SGG.txt`
- 证据等级：full-paper（全文精读）
