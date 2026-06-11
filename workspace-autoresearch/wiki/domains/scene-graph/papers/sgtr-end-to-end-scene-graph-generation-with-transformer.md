---
title: "SGTR: End-to-end Scene Graph Generation with Transformer"
type: paper
domain: scene-graph
status: active
created: 2026-06-10
updated: 2026-06-10
tags:
  - scene-graph-generation
  - transformer
  - end-to-end
  - bipartite-graph
  - entity-aware
  - cvpr-2022
raw_sources:
  - ../../../raw/sources/2022-CVPR-SGTR-End-to-end-Scene-Graph-Generation-with-Transformer.pdf
  - ../../../raw/sources/2022-CVPR-SGTR-End-to-end-Scene-Graph-Generation-with-Transformer.txt
related_pages:
  - reltr-relation-transformer-scene-graph-generation.md
  - dsgg-dense-relation-transformer-end-to-end-scene-graph-generation.md
  - is-ggt-iterative-scene-graph-generation-with-generative-transformers.md
evidence_level: full-paper
paper:
  title: "SGTR: End-to-end Scene Graph Generation with Transformer"
  abbreviated: "SGTR"
  authors:
    - Rongjie Li
    - Songyang Zhang
    - Xuming He
  affiliations:
    - ShanghaiTech University
    - Shanghai Engineering Research Center of Intelligent Vision and Imaging
    - Shanghai Institute of Microsystem and Information Technology, CAS
    - University of Chinese Academy of Sciences
  year: 2022
  venue: IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) 2022
  doi: null
  arxiv: "2112.12970"
  code: "https://github.com/Scarecrow0/SGTR"
  url: null
classification:
  label: Transformer-based End-to-End Scene Graph Generation
  task:
    - Scene Graph Generation (SGG)
    - Visual Relationship Detection (VRD)
  method_family:
    - Bipartite Graph Construction
    - Encoder-Decoder Transformer
    - Set Prediction (DETR-based)
    - Entity-Aware Predicate Representation
  modality: Image
  datasets:
    - Visual Genome (VG)
    - OpenImages V6
  metrics:
    - Recall@K (R@K)
    - mean Recall@K (mR@K)
    - weighted mean AP (wmAP_rel, wmAP_phr)
    - Score-weighted metric (scorewtd)
    - Inference Time (seconds/image)
---

# SGTR: End-to-end Scene Graph Generation with Transformer

## Citation

Rongjie Li, Songyang Zhang, Xuming He. "SGTR: End-to-end Scene Graph Generation with Transformer." IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2022. arXiv:2112.12970.

## One-Sentence Contribution

提出首个将 Transformer 用于端到端场景图生成的模型 SGTR，将 SGG 重构为**二分图构造问题**，通过生成实体/谓词 proposal 集合并推断有向边来形成关系三元组，克服了两阶段方法的 O(N²) 复杂度和点式单阶段方法的非重叠假设限制。

## Problem Setting

场景图生成（SGG）的目标是从输入图像中解析出场景图 $G_{\text{scene}} = \{V_e, E_r\}$，其中 $V_e$ 为实体节点集合（含类别标签和边界框），$E_r$ 为有向边集合（表示主-谓-宾三元组中的谓词类别）。

**现有方法的主要问题**：

1. **Two-stage 方法**（如 Motifs、VCTree、BGNN）：
   - 先检测 N 个实体 proposals，然后对 O(N²) 个实体对进行谓词分类
   - O(N²) 谓词 proposal 导致计算量大且上下文建模噪声高
   - 前端检测错误的组合传播

2. **Point-based one-stage 方法**（如 FCSGG）：
   - 直接从图像特征中提取关系，减少 proposal 集
   - 但依赖交互区域不重叠的强假设，限制其在复杂场景中的应用
   - 缺乏显式实体建模，难以捕获复杂视觉关系

**本文方案**：将 SGG 建模为二分图构造问题，联合生成实体/谓词 proposal 及其潜在关联。

## Method

SGTR 由三个主要模块组成：

### 1. Backbone + Entity Node Generator
- **Backbone**: ResNet-101 提取卷积特征 + Transformer Encoder 增强，得到特征图 $Z \in \mathbb{R}^{w \times h \times d}$
- **Entity Generator**: 采用 DETR 解码器结构，从 $N_e$ 个可学习 entity queries 解码出实体位置 $B_e \in \mathbb{R}^{N_e \times 4}$、类别得分 $P_e \in \mathbb{R}^{N_e \times (C_e+1)}$ 和特征表示 $H_e \in \mathbb{R}^{N_e \times d}$

### 2. Predicate Node Generator（核心创新）
- **Predicate Encoder**: 轻量级 Transformer Encoder，提取谓词特定图像特征 $Z_p$
- **Compositional Query 初始化**：将谓词 query 分解为三个组件 $Q_{is}, Q_{io}, Q_p$（subject indicator、object indicator、predicate representation），通过 cross-attention 将实体信息融入谓词 query
- **Structural Predicate Decoder**: 三个并行的子解码器：
  - **Predicate Sub-decoder**：从图像特征 $Z_p$ 更新谓词表示
  - **Entity Indicator Sub-decoders**：从实体特征 $H_e$ 更新 subject/object indicator
  - **Predicate-Indicator Fusion**：融合三个组件的输出，校准 query 表示
  - 输出：谓词类别预测 $P_p$、subject/object 中心位置 $B_p$、entity indicator 定位和分类

### 3. Bipartite Graph Assembling
- 构建对应矩阵 $M \in \mathbb{R}^{N_r \times N_e}$，计算 entity indicator 与 entity node 之间的距离（结合定位相似度 $d_{\text{loc}}$ 和分类语义相似度 $d_{\text{cls}}$）
- 对每个谓词节点保留 Top-K 最佳匹配的实体作为 subject 和 object
- 生成最终关系三元组 $T = \{(b_s, p_s, b_o, p_o, p_p, b_p)\}$

### 学习与推理
- **Multi-task Loss**: $L = L_{\text{enc}} + L_{\text{pre}}$，包含实体生成损失和谓词生成损失（Hungarian matching + L1/GIoU + cross-entropy）
- **推理**: 生成 $K \cdot N_r$ 个关系预测，过滤自连接三元组，按 triplet score $S_t = (s_s \cdot s_o \cdot s_p)$ 排序取 Top-N

## Experiments

### 数据集
- **Visual Genome (VG)**: 标准 split，SGDet 任务，R@K / mR@K 评估，含 head/body/tail 分组分析
- **OpenImages V6**: weighted evaluation metrics（wmAP_rel, wmAP_phr, scorewtd）

### Baselines
- **Two-stage**: BGNN, RelDN, VCTree-PCPL, VCTree-DLFE, VCTree-TDE, DT2-ACBS
- **One-stage**: FCSGG, AS-Net (HOI), HOTR (HOI)
- 对 BGNN、RelDN、AS-Net、HOTR 用相同 ResNet-101 骨干重实现以公平比较

### 训练设置
- **骨干**: ResNet-101 + DETR（entity detector）
- **优化**: 先训练 entity detector，再联合训练 predicate node generator
- **Predicate encoder**: 3 层 Transformer Encoder
- **Predicate/indicator decoder**: 6 层 Transformer Decoder
- **隐藏维度**: $d=256$
- **谓词 query 数**: $N_r=150$
- **Graph assembling Top-K**: $K=40$（训练）/ $K=3$（测试）
- **硬件**: NVIDIA GeForce Titan XP GPU
- **输入尺寸**: $600 \times 1000$

### 消融实验

**Table 1: 组件消融（VG val, mR/R@50/100）**

| # | EPN | SPD | GA | mR@50 | mR@100 | R@50 | R@100 |
|---|---|---|---|---|---|---|---|
| 1 | ✓ | ✓ | ✓ | **13.9** | **17.3** | **24.2** | **28.2** |
| 2 | ✗ | ✓ | ✓ | 12.0 | 15.9 | 22.9 | 26.3 |
| 3 | ✓ | ✗ | ✓ | 11.4 | 15.1 | 21.9 | 24.9 |
| 4 | ✗ | ✗ | ✓ | 11.3 | 14.8 | 21.2 | 24.1 |
| 5 | ✓ | ✓ | ✗ | 4.6 | 7.0 | 10.6 | 13.3 |

- EPN（Entity-aware Predicate Node）提升 R@100 +1.9，mR@100 +1.4
- SPD（Structural Predicate Decoder）提升 R@100 +3.3，mR@100 +2.5 (对比 line 3 vs line 4: 同时移除 EPN+SPD → 4 vs 1)
- GA（Graph Assembling）影响最大，移除后 mR@100 从 17.3 降至 7.0（-10.3）

**Table 3: Graph Assembling 设计对比（VG val）**
- 本文方法（结合空间+语义相似度）: mR@100 = **17.3**
- AS-Net [3] 风格（仅空间距离）: mR@100 = 11.8
- HOTR [13] 风格（仅特征余弦相似）: mR@100 = 16.1

## Results

### OpenImages V6（Table 4, ResNet-101 backbone）

| Model | mR@50 | R@50 | wmAP_rel | wmAP_phr | scorewtd |
|---|---|---|---|---|---|
| BGNN† | 39.41 | 74.93 | 31.15 | 31.37 | 40.00 |
| RelDN† | 36.80 | 72.75 | 29.87 | 30.42 | 38.67 |
| HOTR† | 40.09 | 52.66 | 19.38 | 21.51 | 26.88 |
| AS-Net† | 35.16 | 55.28 | 25.93 | 27.49 | 32.42 |
| **SGTR (ours)** | **42.61** | 59.91 | **36.98** | **38.73** | **42.28** |

- mR@50 = **42.61**，超越 BGNN（39.41）+3.20
- wmAP_rel = **36.98**，超越 BGNN（31.15）+5.83
- wmAP_phr = **38.73**，超越 BGNN（31.37）+7.36
- 注：R@50 低于两阶段方法（59.91 vs BGNN 74.93），因为 DETR 检测器对小物体检测较弱

### Visual Genome SGDet（Table 5, ResNet-101 backbone）

| Model | mR@50 | mR@100 | R@50 | R@100 | Head mR | Body mR | Tail mR | Time(s) |
|---|---|---|---|---|---|---|---|---|
| BGNN† | 8.6 | 10.3 | 28.2 | 33.8 | 29.1 | 12.6 | 2.2 | 1.32 |
| RelDN† | 4.4 | 5.4 | 30.3 | 34.8 | 31.3 | 2.3 | 0.0 | 0.65 |
| AS-Net† | 6.12 | 7.2 | 18.7 | 21.1 | 19.6 | 7.7 | 2.7 | 0.33 |
| HOTR† | 9.4 | 12.0 | 23.5 | 27.7 | 26.1 | 16.2 | 3.4 | 0.25 |
| **SGTR (ours)** | **12.0** | **15.2** | 24.6 | 28.4 | 28.2 | **18.6** | **7.1** | **0.35** |
| **SGTR∗** | **15.8** | **20.1** | 20.6 | 25.0 | 21.7 | **21.6** | **17.1** | 0.35 |

- mR@100 = **15.2**，超越 HOTR（12.0）+3.2，超越 BGNN（10.3）+4.9
- 使用 resampling 后（SGTR∗）：mR@100 = **20.1**，tail category mR = **17.1**（显著提升）
- Head category mR 低于两阶段方法（28.2 vs BGNN 29.1），因 DETR 小物体检测弱
- 推理时间 **0.35 秒/图**，与 HOTR（0.25）接近，远快于两阶段方法（BGNN 1.32）

## Limitations

1. **Head category 召回率较低**：DETR 检测器在处理小物体时弱于 Faster-RCNN，而 VG 数据集中较大比例的关系涉及小物体，导致 head 类别 mR 不够高
2. **依赖 DETR 检测质量**：entity generator 的质量直接影响下游 predicate 生成和 graph assembling
3. **K 超参数敏感**：graph assembling 的 Top-K 值需要在训练和测试时分别设置，不同 K 值影响性能

## Reusable Claims

1. **SGG 的二分图建模是有效框架**：将场景图构造为二分图（实体节点+谓词节点+有向边），联合生成 proposal 和关联，平衡了两阶段和单阶段方法的优缺点
2. **Entity-aware 谓词表示提升关系质量**：将实体指示信息融入谓词 query（分解为 subject indicator + object indicator + predicate representation），使谓词表示更有结构性和判别力
3. **Graph Assembling 是关键瓶颈**：消融实验显示移除 graph assembling 后 mR@100 从 17.3 降至 7.0（-59.5%），其效果远大于移除 entity-aware 谓词设计（-1.4）
4. **One-stage Transformer 可实现更快推理**：SGTR 推理时间 0.35s/img，与单阶段 HOI 方法持平，远超两阶段方法的 0.65-1.69s/img

## Connections

- **RelTR (Cong et al., TPAMI 2023)**：将 SGG 构建为集合预测问题，使用 coupled subject/object queries，是 SGTR 之后的重要 Transformer 单阶段 SGG 工作
- **DSGG (Hayder et al., CVPR 2024)**：提出 dense relation transformer，进一步扩展端到端 Transformer SGG 到密集关系预测场景
- **IS-GGT (Iterative SG Generation with Generative Transformers)**：用生成式 Transformer 进行迭代场景图生成
- **DETR (Carion et al., ECCV 2020)**：SGTR 的 entity generator 基于 DETR 架构
- **AS-Net / HOTR**：借鉴了 HOI 领域的 dual-decoder + grouping 设计范式
- **BGNN**: SGTR 在两阶段方法中主要对比的 SOTA 基线

## Open Questions

1. SGTR 的 DETR-based entity detector 对小物体的检测弱于 Faster-RCNN，如何在不增加推理成本的前提下提升小物体关系检测？
2. Graph Assembling 的 Top-K 机制是否最优？是否有可学习/可微分的软匹配方案？
3. SGTR 的三元组独立排名（triplet score）后处理是否损失了图的全局一致性？是否可以通过图级优化来提升？

## Provenance

- **PDF**: `raw/sources/2022-CVPR-SGTR-End-to-end-Scene-Graph-Generation-with-Transformer.pdf` (4.5 MB, 16 pages)
- **Extracted Text**: `raw/sources/2022-CVPR-SGTR-End-to-end-Scene-Graph-Generation-with-Transformer.txt` (2155 lines, 72.7K chars)
- **Evidence Level**: full-paper
- **Notes**: 全文 PDF 提取，代码开源（PyTorch + DETR）
