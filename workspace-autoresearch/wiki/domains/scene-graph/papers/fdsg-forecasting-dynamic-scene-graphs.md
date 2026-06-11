---
title: "FDSG: Forecasting Dynamic Scene Graphs"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - scene-graph-generation
  - dynamic-scene-graph
  - scene-graph-forecasting
  - scene-graph-anticipation
  - temporal-modeling
  - neural-sde
  - video-understanding
  - arxiv-2025
raw_sources:
  - ../../../raw/sources/2025-06-09-FDSG-Forecasting-Dynamic-Scene-Graphs.pdf
  - ../../../raw/sources/2025-06-09-FDSG-Forecasting-Dynamic-Scene-Graphs.txt
related_pages:
  - panoptic-video-scene-graph-generation.md
evidence_level: full-paper
paper:
  title: "FDSG: Forecasting Dynamic Scene Graphs"
  abbreviated: "FDSG"
  authors:
    - Yi Yang
    - Yuren Cong
    - Hao Cheng
    - Bodo Rosenhahn
    - Michael Ying Yang
  affiliations:
    - Leibniz University Hannover
    - University of Twente
    - University of Bath
  year: 2025
  venue: arXiv 2025
  doi: null
  arxiv: "2506.01487"
  code: null
  url: null
classification:
  label: Dynamic Scene Graph Forecasting
  task:
    - Dynamic Scene Graph Generation (DSGG)
    - Scene Graph Anticipation (SGA)
    - Scene Graph Forecasting (SGF)
  method_family:
    - Query Decomposition
    - Neural Stochastic Differential Equations (Neural SDE)
    - Cross-Attention Temporal Aggregation
  modality: Video
  datasets:
    - Action Genome
  metrics:
    - Recall@K (R@K)
    - Mean Recall@K (mR@K)
    - Object Detection Recall
    - Average Precision (AP)
---

# FDSG: Forecasting Dynamic Scene Graphs

## Citation

Yi Yang, Yuren Cong, Hao Cheng, Bodo Rosenhahn, Michael Ying Yang. "FDSG: Forecasting Dynamic Scene Graphs." arXiv:2506.01487, 2025.

## One-Sentence Contribution

提出 FDSG 框架，首次在动态场景图中**同时预测未来帧的实体标签、边界框和关系三元组**，而非仅预测关系而假设实体静止不变。

## Problem Setting

现有方法的不足：
- **DSGG**（如 STTran、OED）：用插值策略，需目标帧和参考帧都观察到才能生成场景图，缺乏对未来帧的预测能力。
- **SGA**（如 SceneSayer）：只预测未来关系，假设实体标签和位置静止不变——这在真实动态场景（人走动、物体移动）中明显不合理。

FDSG 定义了一个新任务 **Scene Graph Forecasting (SGF)**：根据观察帧预测未观察帧的完整场景图（含实体标签、边界框、关系）。

## Method

### 整体架构（One-stage End-to-end）

基于 DINO 检测器 + 四尺度特征 + ResNet50 backbone，采用端到端 one-stage 设计，无需显式目标跟踪。使用 100 个 entity queries、256d 内容表示和 512d 三元组表示。

### 核心模块

1. **Static SGG Module (S)**：基于 OED 的 one-stage 场景图生成基线，为目标帧和参考帧生成实体检测和关系三元组。

2. **Triplet Dynamics Model (TDM)**：使用 **Neural Stochastic Differential Equations (Neural SDE)** 建模三元组动态。
   - Query Decomposition：将 triplet 表示分解为 entity content、entity location、relation content 三个分量，分别建模动态。
   - 每个分量通过独立的 Neural SDE 建模连续时间演化。
   - SDE 中的 drift 和 diffusion 网络均可学习。

3. **Location Dynamics Model (LDM)**：显式建模边界框的连续时间演化（使用 Neural SDE），使 Entity Location 预测成为可能。

4. **Temporal Aggregation Module (T)**：通过 **cross-attention** 整合观察帧的预测特征与未来帧的预测特征，增强预测质量。

5. **Forecasting Error as Auxiliary Loss**：将预测误差作为辅助损失函数，联合学习 DSGG 和 SGA 任务。

### 公式化

对于视频帧序列 $$\{I_1, ..., I_T\}$$，观察窗口为 $$\{I_1, ..., I_{T_0}\}$$，预测时间 $$\Delta T = T - T_0$$：
- Triplet 动态: $$Z_{T_0+\Delta T} = Z_{T_0} + \int_{T_0}^{T_0+\Delta T} \mu(Z_t, t) dt + \int_{T_0}^{T_0+\Delta T} \sigma(Z_t, t) dW_t$$
- 其中 $$\mu$$ 为 drift 网络，$$\sigma$$ 为 diffusion 网络，$$dW_t$$ 为 Wiener 过程（Neural SDE）。

### 训练策略

1. 预训练 SGG 基线（OED 风格，5 epoch）
2. 联合微调 Temporal Aggregation + Forecast Module（3 epoch）
3. AdamW 优化器，初始 lr=0.0001，batch size=2
4. 匹配损失权重：$$\alpha_l=1.0, \beta_l=5.0$$

## Experiments

### 数据集

**Action Genome**：234,253 帧，476,229 个边界框，35 个物体类（不含"person"），1,715,568 个实例，25 个关系类（attentional/spatial/contacting 三种类型）。支持多标签标注（135,484 个 subject-object 对有多重关系标注）。

评估策略：（1）With Constraint — 每对唯一交互；（2）No Constraint — 允许多重关系。

### Baselines

DSGG 任务：RelDN, VCTree, TRACE, GPS-Net, STTran, APT, DSG-DETR, TEMPURA, OED

SGA 任务：STTran++, DSG-DETR++, SceneSayer (ODE/SDE)

SGF 任务：SceneSayerODE+, SceneSayerSDE+（adapted baseline with bounding box regression）

### 评估协议

| 任务 | 评估内容 | IoU 阈值 |
|------|---------|---------|
| DSGG (SGDET) | 实体 labels + bbox + relationships | ≥0.5 |
| DSGG (SGCLS) | 实体 labels + predicates (gt bbox) | — |
| DSGG (PredCLS) | Predicates (gt bbox + gt labels) | — |
| SGA (AGS) | Predicates (无 bbox 评估) | ≥0 |
| SGA (PGAGS) | 实体 labels + predicates (gt bbox) | — |
| SGA (GAGS) | Predicates (gt bbox + gt labels) | — |
| SGF (SGDET) | 实体 labels + bbox + relationships | ≥0.5 |

观察比例：F = {0.3, 0.5, 0.7, 0.9}

### 消融实验

消融 4 个组件：(S) Static SGG Module, (T) Temporal Aggregation, (TDM) Triplet Dynamics Model, (LDM) Location Dynamics Model。

## Results

### DSGG — Scene Graph Detection (SGDET) (Table 2)

| Method | R@10 W/C | R@20 W/C | R@50 W/C | R@10 No C | R@20 No C | R@50 No C |
|--------|---------|---------|---------|----------|----------|----------|
| OED | 33.5 | 40.9 | 48.9 | 35.3 | 44.0 | 51.8 |
| **FDSG (ours)** | **35.3** | **42.9** | **49.8** | **37.2** | **47.2** | **56.5** |

Mean Recall (mR@K) — FDSG vs OED:
- mR@10 W/C: **22.2** vs 20.9 (+1.3)
- mR@20 W/C: **27.8** vs 26.9 (+0.9)
- mR@50 No C: **54.1** vs 49.5 (+4.6)

**FDSG 在所有 SGDET 指标上超越所有 baseline**，在 R@50 No Constraint 上比 OED 提升 +4.7。

### DSGG — SGCLS (Table 3)

FDSG SGCLS R@10 W/C = **54.8**（超越 TEMPURA 47.2），mR@50 No C = **74.0**（超越 TEMPURA 66.4）。

### DSGG — PredCLS (Table 4)

FDSG PredCLS 与 SOTA OED 可比（R@50 No C: 99.4 vs 99.2），且不需为 PredCLS 训练单独模型。

### SGA — AGS (Table 5, F=0.5)

| Method | R@10 W/C | R@20 W/C | R@50 W/C | mR@10 W/C | mR@10 No C |
|--------|---------|---------|---------|----------|-----------|
| SceneSayerSDE | 27.3 | 34.8 | 37.0 | 12.4 | 16.3 |
| **FDSG** | **28.3** | **36.5** | **45.3** | **18.1** | **23.2** |

FDSG 在 AGS 上 mR@10 相比 SceneSayerSDE 提升约 50%。尤其显著：观察比例从 0.3→0.9 时，FDSG 的 mR@10 No C 从 41.7→59.5，而 SceneSayerSDE 仅从 37.1→46.8。

### SGF (Table 8, F=0.5)

| Method | R@10 W/C | R@20 W/C | R@50 W/C | mR@10 W/C | mR@10 No C |
|--------|---------|---------|---------|----------|-----------|
| SceneSayerSDE+ | 6.4 | 7.7 | 7.9 | 3.1 | 3.9 |
| **FDSG** | **10.6** | **13.3** | **15.5** | **8.4** | **11.4** |

FDSG 在 SGF 任务上大幅超越 baseline，R@50 No C: 32.5 vs 22.8（SceneSayerSDE+ at F=0.9）。体现全三元组动态建模 vs 仅关系动态的优势。

### Entity Forecasting (Table 9, F=0.5)

SGA (IoU≥0) R@20: FDSG **83.36** vs Baseline 80.11 vs Oracle 82.75
SGF (IoU≥0.5) R@20: FDSG **43.85** vs Baseline 40.33 vs Oracle 44.01

### 消融实验 (Table 10, F=0.5)

DSGG 上，完整模型（S+T+TDM+LDM）在 mR@10 W/C = **22.2**（vs S only: 19.7, S+T: 21.5）。
SGF 上，完整模型 mR@10 W/C = **8.4**（vs 无 LDM: 7.0, 无 TDM: 1.7）。**TDM 对 SGF 贡献最大**（从 1.7→7.0→8.4）。

## Limitations

1. 在 SGF 的极低观察比例（F=0.3）下，预测绝对召回率仍然很低（R@50=16.2 No Constraint），长期预测精度有待提升。
2. 实体预测精度在 SGF（IoU≥0.5）下明显低于 SGA（IoU≥0），表明联合预测标签+位置仍具挑战。
3. 推理依赖 Neural SDE 求解器，计算成本高于简单 MLP-based 预测。
4. Action Genome 数据单一（室内日常活动），泛化到室外/驾驶等场景有待验证。

## Reusable Claims

1. **全三元组动态建模优于仅关系动态建模**：SGF 结果中 FDSG 超越 SceneSayer 超过 2×（R@50: 32.5 vs 22.8），验证了同时预测实体和关系动态的必要性。
2. **预测误差辅助损失有效**：通过将 SGA/SGF 的预测误差回传到 SGG 基线，DSGG 性能也同步受益（SGDET R@50 No C: 56.5 vs OED 51.8）。
3. **Neural SDE 适合连续时间场景图动态建模**：可同时预测不同时间跨度（ΔT 可变），无需离散化。
4. **Query Decomposition 降低多分量联合预测难度**：将 entity content/location/relation 分离建模优于联合优化。

## Connections

- 在 **视频场景图** 方向扩展了 [Panoptic Video Scene Graph Generation] 和 TEMPURA 等 DSGG 基线
- 预测范式对标 **SceneSayer** (SGA 任务)，但去掉了其"实体静止"假设
- 与 **object trajectory prediction** 存在交叉（LDM 模块本质是目标级的轨迹预测）
- One-stage 架构继承自 OED，去掉了两阶段重训练需求

## Open Questions

1. Action Genome 以外的数据集（如 VidOR, OpenPVSG）上 FDSG 泛化效果如何？
2. 更长时间跨度的预测（ΔT > 50 frames）是否仍能保持优势？
3. 能否引入语义先验（如交互模式知识库）进一步提升长尾关系的预测性能？
4. FDSG 的推理速度是否满足实时应用需求？

## Provenance

- **Evidence Level**: full-paper
- **Source**: arXiv 2506.01487v2, 2025
- **Extraction**: PyMuPDF 全文提取，16 页，68417 字符
- **Verification**: 文本完整，包含所有表格和参考文献
