---
title: "Fast Contextual Scene Graph Generation with Unbiased Context Augmentation"
type: paper
domain: scene-graph
status: active
created: 2026-06-08
updated: 2026-06-08
tags:
  - scene-graph-generation
  - long-tail-bias
  - context-augmentation
  - real-time-inference
  - visual-relationship-detection
  - CVPR-2023
raw_sources:
  - ../../../raw/sources/2023-CVPR-Fast-Contextual-Scene-Graph-Generation.pdf
  - ../../../raw/sources/2023-CVPR-Fast-Contextual-Scene-Graph-Generation.txt
related_pages:
  - 3d-spatial-multimodal-knowledge-accumulation-scene-graph-prediction-point-cloud.md
evidence_level: full-paper
paper:
  title: "Fast Contextual Scene Graph Generation with Unbiased Context Augmentation"
  authors:
    - Tianlei Jin
    - Fangtai Guo
    - Wen Wang
    - Wei Song
    - Zonghao Mu
    - Shiqiang Zhu
    - Qiwei Meng
    - Xiangming Xi
  year: 2023
  venue: "IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2023"
  arxiv: null
  doi: null
  code: null
  project: null
classification:
  label: "Context-Augmented Scene Graph Generation"
  task:
    - Scene Graph Generation (SGG)
    - Predicate Classification (PredCls)
    - Scene Graph Generation (SGGen)
  method_family:
    - Context Knowledge Network (CKN)
    - Context augmentation
    - Vision Differentiation Network (VDN)
    - ReLuL1 loss
    - Contextual Mask (Rmask)
  modality:
    - Bounding box locations
    - Object categories
    - Visual features (for CV-SGG only)
  datasets:
    - Visual Genome (VG)
    - Panoptic Scene Graph (PSG)
  metrics:
    - Recall@K (R@K)
    - mean Recall@K (mR@K)
    - Mean@K
    - F@K (harmonic mean of R@K and mR@K)
---

## Citation

Tianlei Jin, Fangtai Guo, Wen Wang, Wei Song, Zonghao Mu, Shiqiang Zhu, Qiwei Meng, Xiangming Xi. "Fast Contextual Scene Graph Generation with Unbiased Context Augmentation." *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*, 2023.

## One-Sentence Contribution

提出了一种基于上下文描述（仅用物体类别和位置，不使用视觉特征）的快速场景图生成方法，并通过上下文增强（context augmentation）解决长尾偏置问题，首次实现实时 SGG。

## Problem Setting

场景图生成 (SGG) 的两个核心障碍：
1. **长尾偏置**：数据集中常见谓词（如 on, has）样本远多于尾部谓词（如 playing, across），导致模型倾向于预测常见谓词。
2. **推理速度慢**：分析每对物体间的谓词是二次时间复杂问题，传统方法难以实现实时推理。

现有方法要么改善长尾偏置但降低常见谓词召回率，要么提高速度但牺牲性能。作者试图同时解决这两个问题。

## Method

### 核心观察

- 人类可以仅根据上下文描述（类别+位置）推测物体间的可能关系，无需视觉外观信息。
- 物体大小和位置的轻微偏移基本不影响谓词判断（例如 man 和 glasses 间的 wearing 关系不会因眼镜大小变化而改变）。

### C-SGG (Contextual SGG)

**输入**：仅上下文描述（物体类别 + 归一化边界框位置）

**上下文增强 (Context Augmentation)**：
- 对边界框位置添加随机扰动 ε（设 ε ≤ 0.05）
- 物体类别用 GloVe 转为 50 维词向量
- 位置向量为边界框坐标及其中心点，重复 5 倍得到 30 维
- 最终上下文描述向量 `D = [o_j1, b_j1, o_j2, b_j2, b_j1 - b_j2]`，共 190 维

**Context Knowledge Network (CKN)**：
- 3 层全连接网络 + sigmoid 输出层
- 输出维度 = 数据集谓词数量
- 损失：BCE + 置信度损失

### CV-SGG (Context Guided Visual SGG)

- 基于 C-SGG 的输出生成 Rmask，仅对 C-SGG 预测的高可能谓词（top-Nmask）进行视觉分析
- VDN 用 ResNet 提取视觉特征 + 全连接层 + sigmoid
- ReLuL1 loss：boost 真实谓词概率，suppress 高假阳性谓词
- 最终融合：`R = (α·Rc + (1-α)·Rv) × Rmask`

### 优势

- C-SGG 完全无需视觉特征提取，每对物体仅需 0.2M FLOPs
- 上下文增强可为每个谓词生成多样化的训练样本，实现无偏训练
- CV-SGG 通过 Rmask 引导视觉注意力仅关注可能谓词，大幅降低计算量

## Experiments

### 数据集

**VG (Visual Genome)**：
- ~108K 图像，70% 训练 / 30% 测试
- 150 个物体类别，50 个谓词类别
- 训练集 342,363 对物体上下文描述
- 严重不平衡：on 有 101,843 样本，playing 仅 121 样本

**PSG (Panoptic Scene Graph)**：
- 46,697 训练图像，1,989 验证/测试图像（来自 COCO）
- 133 个物体类别（thing + stuff），56 个谓词类别
- 训练集 261,666 对物体上下文描述
- on 有 52,974 样本，falling off 仅 7 样本

### 任务与指标

- **PredCls**（谓词分类）：给定 ground-truth 物体/位置，预测谓词
- **SGGen**（场景图生成）：仅给定图像，生成完整场景图
- 指标：R@K, mR@K, Mean@K = (R@K + mR@K)/2, F@K = 2×R@K×mR@K/(R@K+mR@K)
  - R@K 侧重常见谓词召回，mR@K 侧重尾部谓词召回，Mean@K 和 F@K 衡量均衡性

### 训练设置

**C-SGG**：
- 硬件：1× RTX2070 SUPER，batch size 256
- 训练时间：2000 epoch，约 8 小时
- 初始学习率 0.04，训练中下降
- GPU 显存仅 1.8G（无需视觉信息）
- 交替类别平衡采样 [DT2-ACBS]

**CV-SGG**：
- VDN 输入：224×224×5（subject mask + image + object mask）
- Nmask = 10（C-SGG 输出中真实谓词在 top-10 概率为 98%）
- boost factor η = 0.1，经验因子 α = 0.7
- 硬件：1× RTX3090Ti，batch size 64
- 训练时间：100 epoch，约 60 小时
- 初始学习率 0.002，训练中下降

### Baselines

- PredCls：IMP, FREQ, G-RCNN, KERN, GB-Net, BGNN, DT2-ACBS, PCPL, FCSGG, SGTR, SS-RCNN, Motifs ± (TDE, CogTree, DLFE, BPL-SA, NICE, IETrans), VCTree ± (TDE, CogTree, DLFE, BPL-SA, NICE, IETrans)
- SGGen：同 PredCls 列表 + PSGTR, PSGFormer
- 推理速度：IMP, VCTree, Motifs, FCSGG, PSGFormer, PSGTR

### 消融实验

1. **上下文增强因子 ε**：VG PredCls 测试 ε=0, 0.01, 0.05, 0.1
2. **ReLuL1 与 boost factor η**：η=0.05, 0.1, 0.2 对比 BCE loss
3. **经验因子 α**：α=0, 0.1, 0.3, 0.5, 0.7, 0.9
4. **Contextual Mask Nmask**：Nmask=0, 3, 5, 10, 20

## Results

### VG 数据集 PredCls 任务（Table 1）

| Method | R@50/100 | mR@50/100 | **Mean@50/100** | **F@50/100** |
|--------|---------|-----------|----------------|-------------|
| C-SGG (Ours) | 55.2/59.2 | **44.1/47.6** | **44.1/47.6** | **41.2/44.7** |
| CV-SGG (Ours) | **58.2/62.4** | 44.1/47.6 | **45.4/49.3** | **45.8/49.3** |
| IETrans + VCTree | 55.0/56.9 | 37.0/39.7 | 42.5/44.8 | 42.2/44.8 |
| NICE + VCTree | 55.0/56.9 | 30.7/33.0 | 42.9/45.0 | 42.5/44.8 |

- CV-SGG 在 Mean@50 和 F@50 上达到 SOTA（45.4 和 45.8）
- C-SGG 不使用任何视觉信息即达到 Mean@50=44.1，高于所有不带视觉增强的方法
- 相比 IETrans+VCTree (Mean@50=42.5)，CV-SGG 提升 2.9

### VG 数据集 SGGen 任务（Table 1）

| Method | R@50/100 | mR@50/100 | **Mean@50/100** | **F@50/100** |
|--------|---------|-----------|----------------|-------------|
| C-SGG (Ours) | 32.6/36.2 | 20.8/23.8 | 26.7/30.5 | 19.0/21.9 |
| CV-SGG (Ours) | **41.8/45.8** | 21.2/24.5 | **27.8/32.0** | **19.2/22.2** |
| IETrans + VCTree | 41.2/44.1 | 19.5/22.6 | 23.5/27.2 | 18.7/21.7 |
| BGNN | 40.2/42.8 | 20.9/24.2 | 31.0/35.8 | 15.9/18.6 |

- CV-SGG 在 Mean@100=32.0 和 F@100=22.2 上为 SOTA
- CV-SGG 的 R@100=45.8，大幅领先（BGNN 42.8）

### PSG 数据集（Table 2）

| Method | PredCls Mean@20/100 | SGGen Mean@20/100 |
|--------|-------------------|------------------|
| C-SGG (Ours) | **34.5/41.5** | **24.0/29.0** |
| CV-SGG (Ours) | 34.0/41.5 | **25.3/29.8** |
| VCTree | 32.9/38.0 | 20.6/22.5 |
| MOTIFS | 32.6/37.7 | 20.0/22.0 |

- C-SGG 在 PSG PredCls Mean@100=41.5，远超 VCTree（38.0）和 Motifs（37.7）
- CV-SGG 在 SGGen Mean@100=29.8，为 SOTA

### 推理速度对比（Table 3）

| Method | #Param | FPS |
|--------|--------|-----|
| Yolov5l + **C-SGG** | 45+0.2M | **33.5** |
| Yolov5l + CV-SGG | 45+10M | 6.4 |
| FCSGG-W48-5S-FPN×2 | 83.0M | 5.89 |
| Motifs | 349.8M | 4.00 |
| IMP | 293.9M | 4.05 |
| PSGFormer | 50.4M | 4.52 |

- C-SGG 为唯一 FPS>30 的 SGG 方法，首次实现实时 SGG
- 每对物体仅 0.2M FLOPs（10000 对仅 2 GFLOPs）
- CV-SGG 通过仅处理 top-100 物体对，FPS=6.4，仍超过大多数方法

### 消融实验关键发现

1. **上下文增强**（Table 4）：ε=0.05 最优，PredCls Mean@50=44.1；不增强（ε=0）时仅 Mean@50=40.0；无位置信息时更低（Mean@50=31.2）
2. **ReLuL1 loss**（Table 5）：η=0.1 最优，R@50=58.2 & mR@50=35.1；BCE loss 时 R@50=60.2 但 mR@50 仅 23.1（说明 ReLuL1 有效平衡常见/尾部谓词）
3. **经验因子 α**（Table 6，PSG SGGen）：α=0.7 为最佳平衡点，Mean@20=25.8
4. **Contextual Mask**（Table 7，PSG SGGen）：Nmask=10 最佳，无 mask 时 mR@20=16.5，加入 mask 后 mR@20=22.8（+6.3）

## Limitations

1. **复杂谓词区分困难**：由于显著弱化视觉信息，难以区分 against 和 belong to 等复杂谓词
2. **缺乏全局场景感知**：仅使用局部上下文描述（物体对），忽略全局场景信息
3. **依赖外部检测**：两阶段方法依赖于独立的对象检测器，SGG 性能受制于检测质量

## Reusable Claims

1. **Claim**: 物体外观特征对谓词判断不重要，上下文（类别+位置）足以推断可能谓词
   **Evidence**: C-SGG 完全不使用视觉特征，在 VG PredCls 上 Mean@50=44.1，超越多数使用视觉特征的方法
   **Scope**: VG 和 PSG 数据集上的场景图生成
   **Confidence**: high

2. **Claim**: 轻微位置扰动不改变物体间关系，可用于数据增强
   **Evidence**: 添加 ε≤0.05 的随机位置扰动，Mean@50 从 40.0 提升至 44.1（Table 4）
   **Scope**: 边界框级别的上下文描述
   **Confidence**: high

3. **Claim**: 上下文引导可显著提升尾部谓词召回率
   **Evidence**: C-SGG mR@50=44.1 vs Motifs+TDE mR@50=25.5（VG PredCls）
   **Scope**: VG/PSG 数据集
   **Confidence**: high

4. **Claim**: C-SGG 首次实现实时 SGG
   **Evidence**: 33.5 FPS (yolov5l + C-SGG)，每对 0.2M FLOPs（Table 3）
   **Scope**: RTX2070 SUPER GPU
   **Confidence**: high

## Connections

- 与 [[3d-spatial-multimodal-knowledge-accumulation-scene-graph-prediction-point-cloud.md|3D Spatial Multimodal Knowledge Accumulation]] 同属场景图生成领域，但面向不同模态（2D 图像 vs 3D 点云）
- 与 [[../../autonomous-driving/]] 潜在关联：场景图可用于自动驾驶场景理解（但当前无直接交叉）
- SGG 下游任务：VQA, visual grounding, visual-language navigation

## Open Questions

1. 上下文增强上限如何？增加 ε 到更大值时性能下降（ε=0.1 时 Mean@50 降至 41.4），但最优 ε 是否与数据集相关？
2. 如何将全局场景上下文融入 C-SGG 同时保持实时性？
3. CV-SGG 的高 FPS（6.4）是否可通过优化 VDN backbone 进一步提升？

## Provenance

- 原始 PDF：`raw/sources/2023-CVPR-Fast-Contextual-Scene-Graph-Generation.pdf`
- 提取文本：`raw/sources/2023-CVPR-Fast-Contextual-Scene-Graph-Generation.txt`（47,475 chars, 1,513 lines）
- 提取方式：pdfminer.six
- 确认内容：包含完整 abstract, introduction, method, experiments, results, conclusion, references
- 证据等级：full-paper（全文精读，确认所有实验结果和数字）
