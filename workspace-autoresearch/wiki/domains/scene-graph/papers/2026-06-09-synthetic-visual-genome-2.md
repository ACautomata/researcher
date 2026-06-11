---
title: "Synthetic Visual Genome 2: Extracting Large-Scale Spatio-Temporal Scene Graphs from Videos"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - video-scene-graph-generation
  - synthetic-dataset
  - panoptic-segmentation
  - trajectory-tracking
  - gpt-5
  - vlm
  - arxiv-2026
  - large-scale-dataset
  - spatio-temporal-scene-graph
raw_sources:
  - ../../../raw/sources/2026-06-09-synthetic-visual-genome-2.pdf
  - ../../../raw/sources/2026-06-09-synthetic-visual-genome-2.txt
related_pages:
  - panoptic-video-scene-graph-generation.md
  - hyperglm-hypergraph-for-video-scene-graph-generation-and-anticipation.md
  - motion-aware-contrastive-learning-temporal-panoptic-sgg.md
  - oed-one-stage-end-to-end-dynamic-scene-graph-generation.md
  - click2graph-interactive-panoptic-video-scene-graph.md
  - fremure-frequency-guided-multi-level-reasoning-video-sgg.md
evidence_level: full-paper
paper:
  title: "Synthetic Visual Genome 2: Extracting Large-Scale Spatio-Temporal Scene Graphs from Videos"
  abbreviated: "SVG2"
  authors:
    - Ziqi Gao
    - Jieyu Zhang
    - Wisdom Oluchi Ikezogwo
    - Jae Sung Park
    - Tario G. You
    - Daniel Ogbu
    - Chenhao Zheng
    - Weikai Huang
    - Yinuo Yang
    - Winson Han
    - Quan Kong
    - Rajat Saini
    - Ranjay Krishna
  affiliations:
    - Allen Institute for AI
    - University of Washington
    - Woven by Toyota
    - Microsoft
  year: 2026
  venue: arXiv preprint (arXiv:2602.23543v3)
  doi: null
  arxiv: "2602.23543"
  code: "https://uwgzq.github.io/papers/SVG2/"
  url: null
classification:
  label: "Synthetic Visual Genome 2"
  task:
    - Video Scene Graph Generation (VSGG)
    - Panoptic Video Scene Graph Generation
    - Video Question Answering (VQA)
  method_family: Trajectory-Grounded VLM with Dual Resampler
  modality: Video
  datasets:
    - SVG2 (636K videos)
    - SVG2test (100 expert-annotated videos)
    - PVSG
    - VidOR
    - VIPSeg
    - AGQA 2.0
    - Perception Test
  metrics:
    - Triplet Recall
    - Relation Recall
    - Object Accuracy
    - Attribute Recall
    - VQA Accuracy
---

# Synthetic Visual Genome 2 (SVG2): Extracting Large-Scale Spatio-Temporal Scene Graphs from Videos

## Citation

Ziqi Gao, Jieyu Zhang, Wisdom Oluchi Ikezogwo, Jae Sung Park, Tario G. You, Daniel Ogbu, Chenhao Zheng, Weikai Huang, Yinuo Yang, Winson Han, Quan Kong, Rajat Saini, Ranjay Krishna. "Synthetic Visual Genome 2: Extracting Large-Scale Spatio-Temporal Scene Graphs from Videos." arXiv:2602.23543v3, 2026.

## One-Sentence Contribution

提出 SVG2——目前最大规模的视频场景图数据集（636K 视频、6.6M 物体、52M 属性、6.7M 关系），并配套设计了 TraSeR——一种基于轨迹对齐 token 排列和双重重采样器的视频场景图生成 VLM。

## Method Overview

### SVG2 数据集合成管线

全自动三阶段管线，结合 SAM2 + DAM + GPT 系列模型：

**Phase 1: Panoptic 轨迹生成**
- SAM2 多尺度网格提示（32×32, 16×16, 4×4）生成逐帧 panoptic mask
- **在线-离线双阶段跟踪机制**：
  - 在线阶段：SAM2 predictor 前向传播，持续监控未跟踪区域；当被检测比率 ≥ 10% 时触发断点，为新出现物体分配新 ID
  - 离线阶段：利用在线阶段收集的完整物体入口信息，重置跟踪状态，从每个物体真实起始帧重新初始化，单次连续传播生成完整轨迹
  - 不对称重叠匹配策略（公式 12-13）防止身份切换
- 轻量后过滤：去除冗余/重复轨迹，形态学清理

**Phase 2: 物体描述与结构化解析**
- DAM-3B-Video 为每个物体轨迹生成细粒度文本描述（选 top-8 最大可见区域帧）
- GPT-4.1-nano 解析出物体名称和属性列表
- SAM3 验证步骤：用 SAM3 实例轨迹匹配原始轨迹，保留被支持的标签

**Phase 3: 物体间关系提取**
- 1 FPS 采样，提供 GPT-5 帧、物体 ID、名称、bbox
- **双通道策略**：空间关系和非空间关系分开提取，避免空间关系主导
- 定义 7 类关系：spatial, motion, functional, stateful, social, attentional, event-level

### TraSeR 模型架构

基于 Qwen2.5-VL-3B 的轨迹对齐视频场景图生成模型：

**1. 轨迹对齐 Token 排列**
- 计算 ViT token 与物体 mask 的重叠覆盖率（公式 1），超过阈值 τ_eff=0.5 的 token 分配给对应物体
- 按时间排序形成每个物体的有序 token 轨迹
- 引入 [TRJ] 分隔 token

**2. 双重重采样器模块**
- **物体轨迹重采样器**（Object-trajectory Resampler）：3 层 Perceiver-Resampler，32 learnable queries，聚合整条轨迹的全局语义
- **时间窗口重采样器**（Temporal-window Resampler）：将视频分成 4s 窗口，3 层 Perceiver-Resampler，32 queries，保留局部运动和时间动态
- 两者输出拼接：global summary + window summaries（含时间戳嵌入）

**3. 训练细节**
- 训练数据：SVG2 + 学术数据集（LV-VIS, OVIS, VIPSeg, VidOR, VidVRD）
- 8×H100 GPU，batch size=1，gradient accumulation=2
- ViT 冻结，训练 projector + resamplers + language model
- 学习率：projector 5×10⁻⁵, resamplers 1×10⁻⁴, LM 2×10⁻⁵
- 1 epoch（37K steps）

## Key Results

### 数据集规模对比

| 维度 | SVG2 (Ours) | PVSG | VidOR | SVG1 |
|------|-------------|------|-------|------|
| #Videos | **636K** | 338 | 7.0K | 0 |
| #Objects | **6.6M** | 6.3K | 34.6K | — |
| #Attributes | **52M** | — | — | — |
| #Relations | **6.7M** | 3.6K | 0.3M | — |
| 标注类型 | **密集逐帧** | 稀疏抽样 | 密集 | — |

### 人工验证准确率

| 标注类别 | 准确率 |
|---------|-------|
| 物体 (Object) | **93.8%** |
| 属性 (Attribute) | **88.3%** |
| 关系 (Relation) | **85.4%** |

关系错误中约 86% 来自遮挡/拥挤场景下的谓词错误，14% 来自时间范围错误。

### 场景图生成结果（核心 Table 2）

在 lenient semantic + temporal IoU=0.5 条件下，**TraSeR (3B)** 对比最强开源基线及 GPT-5：

| 模型 | PVSG Trip | VidOR Trip | SVG2test Trip | PVSG Rel | VidOR Rel | SVG2test Rel | VIPSeg Obj | PVSG Obj | VidOR Obj | SVG2test Obj | SVG2test Attr |
|------|-----------|-----------|--------------|---------|---------|-------------|-----------|---------|---------|-------------|--------------|
| GPT-5 | 16.6 | 19.7 | 17.9 | 18.3 | 21.7 | 19.4 | 68.1 | 54.2 | 88.5 | 65.5 | 24.1 |
| **TraSeR** (Ours) | **16.1** | **22.9** | **16.7** | **16.9** | **25.0** | **18.7** | **86.5** | **72.7** | **91.4** | **79.0** | **27.1** |
| 提升 | — | +3.2 | — | — | +3.3 | — | **+18.4** | **+18.5** | +2.9 | **+13.5** | +3.0 |

关键提升总结：
- **关系检测**：比最强开源模型（GLM-4.1-9B-Thinking, Qwen3-VL-4B 等）提升 **+15~20%**
- **物体预测**：比开源基线提升 **+30~40%**，比 GPT-5 提升 **+13%**
- **属性预测**：比开源 SOTA 提升 **+15%**
- **泛化性**：在 PVSG（复杂长视频）上优势最显著

### VQA 应用（Table 5）

| 输入 | AGQA 2.0 | Perception Test |
|------|----------|----------------|
| Video only | 25.9 | 66.8 |
| Video + Qwen2.5-VL's VSG | 24.8 | 68.6 |
| Video + **TraSeR's VSG** | **26.3** | **71.4** |

- AGQA 2.0：**+0.4%** absolute gain
- Perception Test：**+4.6%** absolute gain
- 盲视频评估（仅文本场景图）：TraSeR **13.22%**（比 Qwen2.5-VL +6.5%）

### 跟踪性能

在 IoU=0.5 下跟踪 AR：VIPSeg **0.754**, PVSG **0.686**, VidOR **0.623**

### 消融实验

- 物体轨迹重采样器 vs 时间窗口重采样器互补：前者提升物体识别，后者提升关系预测
- 在线+离线跟踪 vs 仅在线：mask coverage 从 0.435 提升到 **0.486**
- 数据规模：随着训练数据从 25%→50%→75%→100%，TraSeR 性能**持续提升**（VidOR 从 22.3→27.1）

## Structured Claims

| Claim | Evidence | Source |
|-------|----------|--------|
| SVG2 是最大视频场景图数据集（636K 视频） | Table 1, Sec 3.2 | 全文 |
| 人工验证准确率：Object 93.8%, Attr 88.3%, Rel 85.4% | Sec 3.1, p.6 | 全文 |
| TraSeR 关系检测 +15~20% 优于开源 | Sec 5.1, Table 2 | 全文 |
| TraSeR 物体预测优于 GPT-5 +13% | Table 2, SVG2test Obj 79.0 vs GPT-5 65.5 | 全文 |
| VQA 使用 TraSeR 场景图提升 +4.6%（Perception Test） | Table 5, Sec 5.2 | 全文 |

## Key Insights

1. **规模驱动**：从 338 (PVSG) 到 636K (SVG2) 的数量级提升带来质的突破，使视频场景图研究从封闭集走向开放词汇
2. **自动化管线可复现**：SAM2+DAM+GPT-5 的组合流水线可灵活扩展到更多视频源
3. **在线+离线双阶段跟踪**是关键工程创新：解决了 SAM2 无法自主发现新物体的核心限制
4. **双重重采样器设计**有效分离了全局物体语义和局部时间动态，是 TraSeR 性能的核心来源
5. **场景图作为中间表示**：在 VQA 中提升 +4.6%，证明结构化场景图对高层视觉推理仍有独特价值

## Open Questions

- SVG2 由合成数据驱动，与真实场景的 domain gap 如何量化？
- TraSeR 的 3B 模型在更大尺度（7B/14B）上能否持续提升？
- 关系分类中 86% 的遮挡/拥挤场景错误是否有专门解决方案？
- 7 类关系之间的不平衡如何处理？

## Source

- arXiv: [2602.23543](https://arxiv.org/abs/2602.23543)
- Code & Dataset: [https://uwgzq.github.io/papers/SVG2/](https://uwgzq.github.io/papers/SVG2/)
