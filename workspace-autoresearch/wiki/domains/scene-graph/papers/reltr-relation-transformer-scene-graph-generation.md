---
title: "RelTR: Relation Transformer for Scene Graph Generation"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - scene-graph-generation
  - one-stage
  - transformer
  - end-to-end
  - set-prediction
  - visual-relationship-detection
  - tpami-2023
raw_sources:
  - ../../../raw/sources/2023-TPAMI-RelTR-Relation-Transformer-for-Scene-Graph-Generation.pdf
  - ../../../raw/sources/2023-TPAMI-RelTR-Relation-Transformer-for-Scene-Graph-Generation.txt
related_pages:
  - oed-one-stage-end-to-end-dynamic-scene-graph-generation.md
  - is-ggt-iterative-scene-graph-generation-with-generative-transformers.md
  - sgtr-end-to-end-scene-graph-generation-with-transformer.md
evidence_level: full-paper
paper:
  title: "RelTR: Relation Transformer for Scene Graph Generation"
  abbreviated: "RelTR"
  authors:
    - Yuren Cong
    - Michael Ying Yang
    - Bodo Rosenhahn
  affiliations:
    - Leibniz University Hannover
    - University of Twente
  year: 2023
  venue: IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI) 2023
  doi: null
  arxiv: "2204.10862"
  code: "https://github.com/yrcong/RelTR"
  url: null
classification:
  label: One-stage End-to-End Scene Graph Generation
  task:
    - Scene Graph Generation (SGG)
    - Visual Relationship Detection (VRD)
  method_family:
    - Set Prediction (DETR-based)
    - Encoder-Decoder Transformer
    - Coupled Subject-Object Queries
  modality: Image
  datasets:
    - Visual Genome
    - Open Images V6
    - VRD
  metrics:
    - Recall@K (R@K)
    - mean Recall@K (mR@K)
    - zero-shot Recall@K (zsR@K)
    - no-graph constraint Recall@K (ng-R@K)
    - weighted mean AP (wmAP_rel, wmAP_phr)
    - FPS (inference speed)
---

# RelTR: Relation Transformer for Scene Graph Generation

## Citation

Yuren Cong, Michael Ying Yang, Bodo Rosenhahn. "RelTR: Relation Transformer for Scene Graph Generation." IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI), 2023. arXiv:2204.10862.

## One-Sentence Contribution

提出首个**纯视觉单阶段端到端**场景图生成模型 RelTR，将 SGG 重构为集合预测问题，利用 coupled subject/object queries 和多种注意力机制直接推断稀疏场景图，无需组合实体对和枚举所有谓词。

## Problem Setting

场景图生成（SGG）的目标是从图像中检测 entities 和它们之间的 relationships，以 ⟨subject, predicate, object⟩ 三元组表示。传统方法采用**两阶段流水线**：

1. **Object Detection** → 用预训练检测器（如 Faster R-CNN）产生 n 个 entity proposals
2. **Relation Classification** → 对所有 O(n²) 个 subject-object 对分类谓词

**两阶段流水线的固有问题**：
- 需要大量训练参数
- 必须在 O(n²) 候选对中预测关系，其中大部分不相关
- 易基于 proposal 置信度而非真正关系兴趣来选择三元组
- 语义/先验知识的引入使方法偏置，难以泛化

RelTR 将 SGG 视为从图像直接到三元组集合的端到端预测问题，在推断过程中仅通过注意力机制关注感兴趣的关系，不需要两阶段 pipeline。

## Method

### 整体架构

RelTR 基于 Transformer 的 encoder-decoder 架构，借鉴 DETR [18] 的设计范式：

1. **Feature Encoder**：ResNet-50 backbone + Transformer encoder，推理视觉特征上下文
2. **Entity Decoder**：用 N_e 个 entity queries 预测 entity 的类别和 bounding box（可选，可独立用于 ablation）
3. **Triplet Decoder**：用 N_t 个 **coupled subject/object queries** 直接预测 ⟨subject, predicate, object⟩ 三元组

### Triplet Decoder

Triplet decoder 是核心创新，包含三种注意力模块：

#### Coupled Self-Attention (CSA)
耦合自注意力：N_t 个 coupled queries 在 self-attention 中进行信息交互。每个 coupled query 编码一个 subject+object+predicate 的组合信息，通过 attention 建模 queries 间的全局竞争关系，避免多个查询预测相同的关系。

#### Decoupled Visual Attention (DVA)
解耦视觉交叉注意力：每个 coupled query 分别编码 subject 和 object 两套独立的 QKV 投影，从 encoder 输出的视觉特征图中分别关注 subject 和 object 对应的视觉区域。这一设计使单条 query 能同时定位两个不同的实体区域。

#### Decoupled Entity Attention (DEA)
解耦实体交叉注意力：类似于 DVA，但查询不是从原始视觉特征而是从 entity decoder 输出的上层 entity 表示中获取信息。相比 DVA 的细粒度视觉特征，DEA 使用粗粒度 entity 表示，计算开销更小但精度略低。

#### Mask Head
可选模块，为 attention heatmap 添加空间引导，进一步提升预测质量。

### 引入 Auxiliary Loss

参照 DETR [18] 和 Deformable DETR [70]，在 triplet decoder 的每一层后加入 auxiliary 预测损失，以增强训练时的梯度流动。

### Set Prediction Loss

使用基于匈牙利算法的二分匹配策略：

1. 对 N_t 个预测三元组和 M_t 个 GT 三元组（可能 N_t > M_t）计算匹配代价矩阵
2. 匹配代价 = subject box GIoU + subject box L1 + object box GIoU + object box L1 + subject class CE + object class CE + predicate class CE
3. **IoU-based assignment strategy**：在匹配代价中引入 subject 和 object 的 IoU 阈值 T，只有当预测框与 GT 框的 IoU ≥ T 时才认为可匹配。这避免模型学习到无意义的"最佳匹配"（预测系在杆上，GT 是人在跑）。默认 T = 0.7。
4. 非匹配的预测被标记为 ∅（no relation），不参与 predicate 损失计算

### Training

- 端到端训练，不做预训练检测器分离
- 默认 6 encoder layers + 6 triplet decoder layers
- 8 heads multi-head attention, d_model = 256
- N_e = 100 (entity queries), N_t = 200 (coupled queries)
- AdamW 优化器，weight decay = 10⁻⁴
- Transformer 学习率 10⁻⁴，ResNet-50 backbone 学习率 10⁻⁵
- 150 epochs（VG 和 OI），学习率 100 epoch 时乘以 0.1
- 8 RTX 2080 Ti GPUs, batch size 2 per GPU

## Experiments

### 数据集

**Visual Genome (VG)** [19]：108K 图像，150 entity 类，50 predicate 类。70%/30% train/test 划分，从训练集取 5K 作验证。长尾分组：head（>10K 实例）、body（0.5K–10K）、tail（<0.5K）。

**Open Images V6** [20]：126K 训练图像，5.3K 测试图像，1.8K 验证图像。288 entity 类，30 predicate 类。

**Visual Relationship Detection (VRD)** [2]：4K 训练图像，1K 测试图像。

### 评估指标

**Visual Genome**：R@K、mR@K、zsR@K（zero-shot）、ng-R@K（no-graph constraint）、ng-zsR@K，按 PredCLS / SGCLS / SGDET 三种设置评估。

**Open Images V6**：R@50、wmAP_rel（relationship detection）、wmAP_phr（phrase detection），综合得分 score_wtd = 0.2×R@50 + 0.4×wmAP_rel + 0.4×wmAP_phr。

**VRD**：R@50 和 R@100（relationship detection 和 phrase detection）。

### 实现细节

- Backbone: ResNet-50
- AdamW 优化器、batch size 2 per GPU × 8 GPUs、150 epochs（VG/OI）
- VG 和 OI 从头训练，VRD 用 VG 预训练权重微调（100 epochs）
- 默认 N_t = 200, N_e = 100, IoU threshold T = 0.7
- Auxiliary losses 用于 triplet decoder 每层

## Results

### Visual Genome — SGDET (Table 1)

| Method | R@20 | R@50 | R@100 | mR@20 | mR@50 | mR@100 | #Params | FPS |
|--------|:----:|:----:|:-----:|:-----:|:-----:|:------:|:-------:|:---:|
| Motifs [9] | 21.4 | 27.2 | 29.7 | 5.7 | 8.2 | 9.3 | 173.9M | 3.5 |
| VCTree [35] | 22.0 | 27.9 | 30.0 | 5.0 | 6.9 | 7.8 | 180.8M | 2.4 |
| FCSGG (one-stage) [63] | 16.1 | 22.5 | 24.6 | 3.6 | 4.6 | 6.3 | 91.4M | 4.6 |
| SGTR (one-stage) [64] | 19.3 | 23.3 | 26.1 | 9.0 | 11.9 | 13.6 | 67.4M | 14.6 |
| **RelTR (ours)** | **21.2** | **27.5** | **30.7** | **8.2** | **10.8** | **12.6** | **63.7M** | **16.6** |

- RelTR 在 one-stage 方法中全面最优：R@50 比 FCSGG 高 5.1 点，比 SGTR 高 4.2 点
- mR@50 = 10.8，高于 FCSGG（4.6）和 Motifs（8.2），展现更好的长尾性能
- 参数最少（63.7M），推理最快（16.6 FPS），约是 BGNN 的 7 倍

### Visual Genome — SGDET 无偏对比 (Table 2)

| Method | R@20 | R@50 | mR@20 | mR@50 | zsR@50 | zsR@100 | Avg |
|--------|:----:|:----:|:-----:|:-----:|:-----:|:-------:|:---:|
| Motifs-TDE [75] | 12.4 | 16.9 | 8.6 | 9.7 | 2.3 | 2.9 | 8.1 |
| VCTree-TDE [75] | 14.0 | 19.4 | 8.6 | 9.3 | 2.6 | 3.2 | 9.2 |
| VCTree (BA-SGG) [44] | 15.8 | 21.7 | 9.2 | 13.5 | — | — | — |
| VCTree-TDE (EMB) [42] | 14.7 | 20.6 | 8.6 | 9.7 | 1.6 | 2.7 | 9.4 |
| Motifs [9] | 21.4 | 27.2 | 3.3 | 5.7 | 0.1 | 0.2 | 9.8 |
| VCTree [35] | 22.0 | 27.9 | 2.5 | 5.0 | 0.8 | 1.5 | 10.6 |
| **RelTR (ours)** | **21.2** | **27.5** | **6.8** | **10.8** | **1.8** | **2.4** | **11.8** |

- RelTR 在六列平均分上以 11.8 领先，体现了 balanced performance
- 无偏方法（TDE、BA-SGG、EMB）提升 mR 和 zsR 但以 R 大幅下降为代价；RelTR 作为纯视觉方法在三项指标上平衡良好

### Visual Genome — No-Graph Constraint (Table 3)

| Method | ng-R@50 | ng-R@100 | ng-zsR@50 | ng-zsR@100 |
|--------|:------:|:-------:|:--------:|:---------:|
| Motifs [9] | 30.5 | 35.8 | — | — |
| RelDN [61] | 30.4 | 36.7 | — | — |
| KERN [10] | 30.9 | 35.8 | — | — |
| FCSGG [63] | 23.5 | 29.2 | — | — |
| **RelTR** | **30.7** | **35.2** | **2.6** | **3.4** |

ng-R@50 = 30.7，接近最优（KERN 30.9）。ng-zsR@K 高于 Pixels2Graphs（1.4/2.3）。

### Visual Genome — 长尾分组 mR@100 (Table 4)

| Method | Head(>10K) | Body(0.5–10K) | Tail(<0.5K) | All |
|--------|:---------:|:------------:|:----------:|:---:|
| GPS-NET [51] | 30.8 | 9.8 | 3.9 | 8.5 |
| VCTree-TDE [75] | 24.7 | 11.1 | 1.8 | 12.2 |
| BGNN [50] | 34.0 | 12.6 | 6.0 | 12.9 |
| **RelTR** | **30.6** | **14.4** | **5.0** | **14.4** |

- Body 组最优（14.4），Tail 组第二（5.0），全类别平均最优（14.4）
- Head 组低于 BGNN（30.6 vs 34.0），因为 RelTR 不使用语义先验知识

### Open Images V6 (Table 5)

| Method | R@50 | wmAP_rel | wmAP_phr | score_wtd | FPS |
|--------|:----:|:--------:|:--------:|:---------:|:---:|
| VCTree [35] | **75.34** | 34.31 | 33.21 | 41.97 | 1.9 |
| BGNN [50] | 74.98 | 34.15 | 33.51 | 41.69 | 2.9 |
| SGTR [64] | 59.91 | **38.73** | **36.98** | 42.28 | 3.8 |
| **RelTR (ours)** | 71.66 | 37.46 | 34.19 | **42.99** | **16.3** |

- 综合得分 score_wtd = 42.99，超越所有对比方法
- 推理速度 16.3 FPS，分别是 BGNN 和 SGTR 的约 6 倍和 4 倍
- R@50 低于 VCTree（71.66 vs 75.34），但 wmAP_rel 更高（37.46 vs 34.31），表明 RelTR 在 top-ranked predictions 上质量更好

### VRD (Table 6)

| Method | Rel Det R@50 | Rel Det R@100 | Phr Det R@50 | Phr Det R@100 |
|--------|:-----------:|:------------:|:-----------:|:------------:|
| RelDN [61] | 25.3 | 28.6 | 31.3 | 36.4 |
| GPS-Net [51] | 27.8 | 31.7 | 33.8 | 39.2 |
| **RelTR (ours)** | **29.2** | **32.2** | **34.5** | **39.8** |

- 在 relationship detection 和 phrase detection 两项指标上均超越所有对比方法
- RelTR 用 VG 预训练权重微调，而其他方法使用预训练 entity detector

### Long-tailed Techniques Compatibility (Table 7)

在 RelTR 上实现两种长尾技术：
- **Bi-level Resampling (RS)**：mR@50 从 10.8 提升至 13.9，但 R@50 从 27.5 降至 24.1
- **Logit Adjustment (LA)**：mR@50 提升至 14.2，R@50 仅下降至 25.9（更平衡的 trade-off）

Tail 组 mR@100：RelTR 5.0 → +RS 10.5 → +LA 10.2，提升显著。

### Ablation — 层数影响 (Table 8)

- 从 0→6 encoder layers：R@50 从 23.3 升至 27.5（+4.2），参数从 55.8M→63.7M
- 从 3→6 triplet decoder layers：R@50 从 25.9 升至 27.5（+1.6）
- decoder 增至 9 层性能微降（R@50 从 27.5 降至 27.1），可能过拟合

### Ablation — 模块有效性 (Table 9)

| Setting | R@50 | mR@50 | #Params | FPS |
|---------|:----:|:-----:|:-------:|:---:|
| Baseline (no triplet decoder) | 18.3 | 3.5 | 41.5M | 22.0 |
| Only CSA | 0.3 | 0.0 | 43.6M | 22.1 |
| Only DVA | 20.9 | 5.0 | 57.8M | 19.6 |
| Only DEA | 19.1 | 4.8 | 57.8M | 20.3 |
| CSA + DVA | 26.6 | 6.4 | 59.3M | 17.7 |
| CSA + DEA | 22.2 | 5.9 | 59.3M | 19.4 |
| Full (CSA+DVA+DEA) | **27.5** | **10.8** | 63.7M | 16.1 |

- CSA 本身不能检测关系（无视觉交叉注意力）
- DVA 比 DEA 更有效（R@50: 20.9 vs 19.1），因为 DVA 直接操作细粒度视觉特征
- DEA 帮助模型预测更高质量的 subject/object，使 R@50 提升 0.6
- Mask head 贡献有限（假设空间特征已隐式编码在 DVA 生成的视觉特征中）
- 完整组合相较 baseline（无 triplet decoder）R@50 提升 9.2 点

### Ablation — IoU Threshold T (Figure 9)

- T = 1（相当于禁用 IoU 分配策略）时性能最差
- T = 0.7 时最优（R@50 ≈ 27.5, mR@50 ≈ 10.8）
- 从 0.7 升至 1 时性能逐步下降

### Query Number Analysis (Figure 10)

- N_t = 200 时最优
- N_t 过少（≤100）或过多（≥250）时性能下降
- 参数随 N_t 线性增长，FPS 线性下降，但性能非线性变化

### Subject/Object Query 分布分析 (Figure 11-12)

- 不同 coupled queries 学习到不同的空间和类别模式
- 高频谓词 has 的 query 分布平滑（所有 queries 都能预测）
- Body 和 Tail 组的谓词（如 wears, mounted on）有专门的 queries 擅长检测（21% 的 wears 由 Query 115 预测）

## Limitations

1. **SGCLS/PredCLS 评估受限**：由于 RelTR 是单阶段方法，在 PredCLS/SGCLS 设置下不能直接使用输入 GT boxes/labels，需要将 GT 信息分配给匹配的 triplet proposals，特征提取不如两阶段方法精确
2. **R@K 略低于强两阶段 baseline**：如 BGNN 在 R@50 上 27.5 vs 31.0（但 mR@50 更高 10.8 vs 8.2），部分由于不使用语义先验知识
3. **Tail 类性能有限**：不使用先验知识时 Tail 组 mR@100 仅 5.0，通过 logit adjustment 可提升至 10.2
4. **仅在三个静态图像数据集评估**：扩展到视频场景图（动态 SGG）有待验证

## Reusable Claims

1. **SGG 可建模为集合预测问题**：将 SGG 从两阶段（检测→关系分类）转为端到端集合预测，避免 O(n²) 枚举和独立优化带来的次优解。这是 RelTR 的最高层次贡献。
2. **无语义先验的纯视觉 SGG 可行**：在不使用语义/统计先验知识的条件下，纯视觉模型可在 mR@K 和 zsR@K 上达到竞争性能，并保持 better balanced 的三项指标。
3. **Coupled subject/object queries 实现单 query 双实体定位**：一条 query 通过解耦的 QKV 投影同时关注 subject 和 object 两个不同区域，避免为每个 subject-object 对使用两条独立 query。
4. **IoU-based assignment strategy 提升匹配质量**：设定 IoU 阈值 T 避免无意义的匹配（预测系在杆上匹配 GT 人在跑），T = 0.7 最优。
5. **CSA 解决重复预测问题**：耦合自注意力通过 query 间的全局交互抑制重复/无意义的三元组预测，仅用 DVA 或 DEA 时会出现重复和 subject=object 的无效预测。
6. **Light-weight 和高推理速度**：63.7M 参数 + 16.6 FPS（VG）、16.3 FPS（OI），约是同类两阶段方法的 4–7 倍。
7. **与长尾技术兼容**：Logit Adjustment 在仅少量 R@K 损失下显著提升 mR@K（10.8→14.2）。

## Connections

- 与 [OED](oed-one-stage-end-to-end-dynamic-scene-graph-generation.md) 同为 **单阶段集合预测** SGG 方法，共享 DETR 范式。RelTR 聚焦静态图像 SGG，OED 扩展至视频动态 SGG
- 与 **SGTR**[64] 同为 transformer-based one-stage 方法，但 RelTR 使用 coupled query 直接预测三元组，SGTR 使用 graph assembling module 后处理
- 与 **FCSGG**[63] 同为 one-stage 方法，但 FCSGG 是全卷积架构（无 transformer）
- 与 **Motifs**[9]、**VCTree**[35] 等两阶段方法对比，展示 one-stage 在速度和参数效率上的优势
- 与 **BGNN**[50] 对比特别突出：RelTR 在 mR@K 上更高但 R@K 略低，且速度快约 7 倍
- 与 **TDE**[75]、**BA-SGG**[44]、**EMB**[42] 等无偏 SGG 方法对比，证明纯视觉模型可实现均衡的三项指标性能

## Open Questions

1. RelTR 能否扩展到视频动态 SGG（如 Action Genome）？[OED](oed-one-stage-end-to-end-dynamic-scene-graph-generation.md) 后来回答了这个问题，采用了不同的级联解码器设计
2. 更强的 backbone（如 Swin Transformer）下 RelTR 的性能上限？
3. Coupled queries 的显式可解释性分析（哪些 queries 对应哪些关系类型）是否可以进一步结构化？
4. 能否将语义先验知识以可解耦的方式引入 RelTR（如 adapter 或微调）以提升 R@K 而不牺牲 mR@K？
5. RelTR 的 VG PredCLS R@50 = 64.2 远低于两阶段方法的 >80+，这是单阶段方法的固有问题还是可以通过更好的特征分配策略解决？

## Provenance

- **Evidence Level**: full-paper
- **Source**: TPAMI 2023, 17 页正文（含附录）
- **Extraction**: pdfminer 全文提取，约 82K 字符
- **Verification**: 文本完整，包含所有 9 张表格和参考文献
