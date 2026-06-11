---
title: Panoptic Video Scene Graph Generation (PVSG)
type: paper
domain: scene-graph
status: active
created: 2026-06-08
updated: 2026-06-08
tags:
  - video-scene-graph
  - panoptic-segmentation
  - dataset
raw_sources:
  - raw/sources/2023-CVPR-Panoptic-Video-Scene-Graph-Generation.pdf
  - raw/sources/2023-CVPR-Panoptic-Video-Scene-Graph-Generation.txt
paper:
  title: Panoptic Video Scene Graph Generation
  authors:
    - Jingkang Yang
    - Wenxuan Peng
    - Xiangtai Li
    - Zujin Guo
    - Liangyu Chen
    - Bo Li
    - Zheng Ma
    - Kaiyang Zhou
    - Wayne Zhang
    - Chen Change Loy
    - Ziwei Liu
  year: 2023
  venue: CVPR 2023
  arxiv: null
  doi: null
  code: https://github.com/Jingkang50/OpenPVSG
  project: null
classification:
  label: PVSG
  task:
    - Panoptic Video Scene Graph Generation
    - Video Scene Graph Generation
    - Video Panoptic Segmentation
  method_family:
    - Two-Stage Framework
    - Mask2Former
    - Transformer Encoder
  modality:
    - Video
    - Panoptic Segmentation Masks
  datasets:
    - PVSG Dataset
  metrics:
    - R@K
    - mR@K
evidence_level: full-paper
---

# Panoptic Video Scene Graph Generation (PVSG)

## Citation

Jingkang Yang, Wenxuan Peng, Xiangtai Li, Zujin Guo, Liangyu Chen, Bo Li, Zheng Ma, Kaiyang Zhou, Wayne Zhang, Chen Change Loy, Ziwei Liu. "Panoptic Video Scene Graph Generation." CVPR 2023.

## One-Sentence Contribution

提出 Panoptic Video Scene Graph Generation (PVSG) 新任务，将视频场景图的节点从 bounding box 细化为像素级 panoptic segmentation mask，并贡献了一个包含 400 个视频、150K 帧的 PVSG 数据集及两阶段基线框架。

## Problem Setting

**出发点**：现有视频场景图生成（VidSGG）使用 bounding box 定位节点，存在两个关键缺陷：
1. 无法覆盖 stuff 类（水、草地等无定型区域），而这些对场景理解至关重要
2. 容易遗漏微小但重要的物体细节

**PVSG 定义**：输入视频 V ∈ R^{T×H×W×3}，输出动态场景图 G = (M, O, R)，其中：
- M = {m₁, ..., mₙ}：二进制 mask tubes，每个 tube m_i ∈ {0,1}^{T×H×W}
- O = {o₁, ..., oₙ}：对应物体类别标签
- R = {r₁, ..., rₗ}：关系集合，每个关系关联一个 subject 和一个 object，具有 predicate 类别和时间区间

**评估指标**：
- R@K 和 mR@K：triplet 召回率和平均召回率
- 成功召回条件：(1) 主/客体和 predicate 类别正确 (2) mask tube 的 volume IoU > 0.5 (3) 时间区间 IoU 记录 soft recall score
- 与 VidOR 的差异：同一 triplet 多次出现只计一次，但记录分散的时间跨度

## Method

两阶段框架：

### Stage 1: Video Panoptic Segmentation

目标：为每个物体生成视频级 panoptic segmentation mask 和对应的特征 tube。

提供两种基线：

**IPS+T（Image Panoptic Segmentation + Tracker）**：
- 使用 Mask2Former 逐帧处理，输出物体 queries
- 使用 UniTrack 跨帧关联得到 tracked video cubes
- 记录 object queries 供第二阶段使用

**VPS（Video Panoptic Segmentation）**：
- 基于 Video K-Net + Mask2Former 框架
- 使用 temporal contrastive loss 学习 association embeddings
- 训练时邻近帧一起输入学习关联，推理时 online 逐帧匹配

### Stage 2: Relation Classification

在 query tubes 的时域交叠部分配对，进行关系分类。四种方案：

1. **Vanilla**：直接 FC 层 + 多标签 BCE loss
2. **Handcrafted Window**：固定核 [1/4, 1/2, 1, 1/2, 1/4]，window size 5
3. **1D Convolution**：3 层可学习 1D Conv，kernel size 5
4. **Transformer Encoder**：3 层 Transformer block + 位置编码

## Experiments

### 数据集
- **PVSG 数据集**：400 个视频（289 third-person + 111 egocentric），平均时长 76.5 秒
  - 来源：VidOR（第三人称）、Ego4D-STA 和 Epic-Kitchens（第一人称）
  - 共 152,958 帧，标注 panoptic segmentation 和 temporal scene graphs
  - 126 个物体类别，57 个关系类别
  - 训练/测试划分：360 / 40

### 基线方法
- Stage-1 两种选择：IPS+T (Mask2Former + UniTrack) / VPS (Video K-Net + Mask2Former)
- Stage-2 四种选择：Vanilla / Handcrafted Window / 1D Convolution / Transformer Encoder
- 共 8 种组合

### 训练设置
- Backbone: ResNet-50
- 训练 epochs: 12
- 硬件: Stage-1 在 8×V100 GPU 上训练（IPS+T 约 12h，VPS 约 48h），Stage-2 在单 V100 上训练（<1h）
- Stage-2 使用多标签分类 + BCE loss

### 评估协议
- R@K 和 mR@K，K = 20, 50, 100
- Volume IoU 阈值 0.5

## Results

### 主结果（Table 2）

| Stage-1 | Stage-2 | R/mR@20 | R/mR@50 | R/mR@100 |
|---------|---------|---------|---------|----------|
| IPS+T | Vanilla | 2.35 / 1.22 | 2.71 / 1.31 | 2.94 / 1.45 |
| IPS+T | Handcrafted Window | 2.56 / 1.24 | 2.78 / 1.35 | 3.05 / 1.54 |
| IPS+T | 1D Convolution | 2.79 / 1.24 | 2.80 / 1.47 | 3.10 / 1.59 |
| **IPS+T** | **Transformer Encoder** | **4.02 / 1.75** | **4.41 / 1.86** | **4.88 / 2.03** |
| VPS | Vanilla | 0.52 / 0.24 | 0.60 / 0.24 | 0.63 / 0.24 |
| VPS | Handcrafted Window | 0.54 / 0.27 | 0.61 / 0.29 | 0.62 / 0.29 |
| VPS | 1D Convolution | 0.60 / 0.27 | 0.73 / 0.28 | 0.76 / 0.29 |
| VPS | Transformer Encoder | 0.75 / 0.36 | 0.91 / 0.39 | 0.94 / 0.40 |

**关键发现**：
- 最佳组合：IPS+T + Transformer Encoder，R@100 达到 4.88，mR@100 达到 2.03
- Transformer Encoder 在所有 Stage-1 选项下均最优，说明时域信息融合的有效性
- 1D Convolution 优于 Handcrafted Window，说明可学习参数的重要性
- IPS+T 显著优于 VPS（约 5 倍差距），原因在于 PVSG 视频更长、动态性更高（频繁大幅视角切换），VPS 模型 tracking 性能不足

### 消融/分析
- VPS 在 tracking 上存在明显不足：可视化显示 VPS 在跟踪物体时会发生 identity switch（如跟踪的小孩在后几帧切换为另一人），严重影响 PVSG 性能

## Limitations

1. **长尾分布**：真实视频中物体和关系类别呈长尾异方差分布，模型倾向于预测统计上常见的平凡关系
2. **标注噪声**：语言描述的固有不确定性（如 "playing with" 和 "chasing" 在某些场景下重叠）引入 aleatoric uncertainty
3. **VPS 挑战**：PVSG 视频包含大幅视角切换，现有 VPS 模型在 tracking 和 segmentation 上仍有明显不足
4. **整体性能偏低**：即使最佳方法 R@100 仅 4.88，说明 PVSG 任务极具挑战性

## Reusable Claims

> **Claim**: 基于图像的逐帧分割 + 追踪（IPS+T）在长视频 PVSG 任务上优于端到端视频分割模型（VPS），差距约 5 倍。
> **Evidence**: Table 2 — IPS+T+TE: R@100=4.88 vs VPS+TE: R@100=0.94
> **Scope**: PVSG 数据集，长视频（平均 77s），大幅视角切换场景
> **Confidence**: high

> **Claim**: Transformer Encoder 是 PVSG 第二阶段关系分类的最优方案，在所有 Stage-1 设置下均优于 Vanilla、Handcrafted Window 和 1D Conv。
> **Evidence**: Table 2 — IPS+T 设置下 TE 比次优的 1D Conv 提升 R@100 从 3.10→4.88（+57.4%）
> **Scope**: PVSG dataset, ResNet-50 backbone
> **Confidence**: high

## Connections

- 扩展自 [[panoptic-scene-graph-generation]]（PSG，ECCV 2022）—— 从图像级扩展到视频级
- 与 [[meta-spatio-temporal-debiasing-for-video-scene-graph-generation]]（MVSGG）同属 VidSGG 领域，但 PVSG 使用 mask 而非 bounding box
- 借鉴 [[video-k-net]] 作为视频分割基线
- PVSG 数据集使用 [[mask2former]] 和 [[AOT]] 进行标注辅助

## Open Questions

1. 如何解决 PVSG 中物体/关系类别的长尾分布？
2. 如何在长视频中实现鲁棒的 mask tracking，特别是大幅视角切换下的 identity 保持？
3. PVSG 的高标注成本（150K 帧的 panoptic 标注）能否通过弱监督或自监督方法缓解？
4. 如何在 PVSG 框架下整合常识推理以处理罕见关系和动态关系？

## Provenance

- 原始 PDF 路径：`raw/sources/2023-CVPR-Panoptic-Video-Scene-Graph-Generation.pdf`
- 全文提取文本：`raw/sources/2023-CVPR-Panoptic-Video-Scene-Graph-Generation.txt`
- 证据等级：full-paper（全文精读）
