---
title: "Dynamic Scene Graph Generation via Anticipatory Pre-training"
type: paper
domain: scene-graph
status: active
created: 2026-06-10
updated: 2026-06-10
tags: [scene-graph-generation, dynamic-scene-graph, video-sgg, anticipatory-pretraining, CVPR-2022]
source_pages: []
raw_sources:
  - raw/sources/2022-06-01-dynamic-scene-graph-generation-via-anticipatory-pre-training.pdf
  - raw/sources/2022-06-01-dynamic-scene-graph-generation-via-anticipatory-pre-training.txt
related_pages:
  - domains/scene-graph/papers/sgtr-end-to-end-scene-graph-generation-with-transformer.md
  - domains/scene-graph/papers/gtr-grafting-then-reassembling-dynamic-scene-graph-generation.md
paper:
  title: "Dynamic Scene Graph Generation via Anticipatory Pre-training"
  authors: ["Yiming Li", "Xiaoshan Yang", "Changsheng Xu"]
  year: 2022
  venue: CVPR 2022
  arxiv: null
  doi: null
  code: null
classification:
  label: dynamic-scene-graph, anticipatory-pretraining
  task: [Dynamic Scene Graph Generation]
  method_family: Anticipatory Pre-training, Transformer
  modality: Video
  datasets: [Action Genome]
  metrics: [Recall@K (R@10, R@20, R@50)]
evidence_level: full-paper
---

## Citation

Yiming Li, Xiaoshan Yang, Changsheng Xu. "Dynamic Scene Graph Generation via Anticipatory Pre-training." CVPR 2022.

## One-Sentence Contribution

提出基于 Transformer 的面向预训练（Anticipatory Pre-training）范式，通过用历史帧预测当前帧视觉关系来显式建模视频中的时序关系相关性，提升动态场景图生成性能。

## Problem Setting

**任务**：给定视频 V = {I₁, I₂, ..., I_T}，为每一帧 I_t 生成对应的场景图 G_t = {B_t, O_t, R_t}，其中 B_t 为边界框集合、O_t 为物体类别集合、R_t 为谓词集合。

**挑战**：
1. 视频中物体的运动导致物体间视觉关系动态变化，比静态图像 SGG 更复杂
2. 时序信息与空间信息在视频中高度耦合，难以显式捕获时序相关性
3. 现有数据集（如 Action Genome）仅标注关键帧，缺少连续帧标注，阻碍时序相关性的连续建模

**在线预测分解**：将 G_t 的概率分解为时序部分和空间部分：P(G_t|{I_t}) = P(G_t|{I_{t−1}}) · P(G_t|I_t)，其中时序部分 P(G_t|{I_{t−1}}) 通过面向预训练学习。

## Method

### 整体框架
1. **检测器**：Faster R-CNN（ResNet-101 backbone）
2. **空间编码器（Spatial Encoder）**：对每一帧提取帧内空间上下文信息，使用 1 层 Multi-Head Attention，将物体特征编码为上下文感知的视觉表示
3. **渐进式时序编码器（Progressive Temporal Encoder）**：包含短时编码器和长时编码器
   - **短时编码器**：基于 IoU 匹配（阈值 0.8）在相邻帧间追踪同一 subject-object pair，构建关系表示时序序列 A_ij（长度 γ=4），3 层 Multi-Head Attention
   - **长时编码器**：处理更长的关系序列 U_ij（长度 λ=10），使用聚合函数 f_θ（可学习的线性层）压缩长期关系表示，3 层 Multi-Head Attention
4. **微调阶段**：复用预训练的空间编码器和渐进式时序编码器，添加全局时序编码器融合当前帧信息

### 面向预训练 范式
- **预训练任务**：用前序帧 {I_{t−1}} 预测当前帧 I_t 的场景图（在线预测，无当前帧信息）
- **损失函数**：多标签 margin loss（因为两个物体间可能有多个正确关系）
- **多个线性分类器**：Action Genome 有 3 种关系类型（attention, spatial, contacting），使用多个分类器分别预测不同类型的视觉关系

### 预训练与微调区别
- 预训练：输入为 {I_{t−1}}，预测 I_t 的关系
- 微调：输入为 {I_{t−1}} ∪ {I_t}，结合时序上下文和当前帧空间信息预测当前帧关系

## Experiments

### 数据集
- **Action Genome**：最大的动态场景图数据集，标注视频中动作相关的 subject-object 关系
- **训练集/测试集**：使用标准划分（同 [18]）
- **额外数据**：利用未标注帧进行预训练

### Baseline 方法
- VRD [26], MotifFreq [52], MSDN [23], VCTREE [38], ReIDN [54], GPS-Net [24], STTran [7]（最相关工作，也是基于 Transformer 的动态 SGG 方法）

### 训练设置
- 框架：PyTorch
- 检测器 Backbone：Faster R-CNN + ResNet-101
- 物体语义嵌入：200 维
- 物体表示维度：840，关系表示维度：2192
- 空间编码器：1 层 Multi-Head Attention（8 head）
- 短时/长时/全局时序编码器：各 3 层 Multi-Head Attention（8 head）
- **预训练**：SGD，初始 lr=0.001，decay factor=0.9/epoch，momentum=0.9，batch size=16，短时序列长度 γ=4，长时序列长度 λ=10，每 3 帧采样 1 帧
- **微调**：SGD，初始 lr=1e-5，decay factor=0.9/epoch，momentum=0.9，batch size=16
- 硬件：not reported in the source

### 评估协议
- **度量**：Recall@K (R@10, R@20, R@50)
- **三种实验设置**：Predicate Classification (Pred Cls)、Scene Graph Classification (SG Cls)、Scene Graph Generation (SG Gen)
- **两种策略**：With Constraint（每对至多一个谓词）、No Constraint（允许多个谓词）
- 同 [7] 一样，对每个 subject-object pair 预测 3 种关系类型（attention, spatial, contacting）

### 消融实验
- 消融语义信息（w/o Semantic）
- 消融长时编码器（w/o long-term）
- 消融预训练（w/o Pre-training，直接用当前帧代替历史帧做预测）
- 是否使用未标注数据（对比 STTran* 使用相同数据量）

## Results

### 主实验结果（With Constraint 策略）

| 设置 | 方法 | Pred Cls R@10 | Pred Cls R@20 | SG Cls R@10 | SG Cls R@20 | SG Gen R@10 | SG Gen R@20 |
|------|------|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|
| With Constraint | STTran [7] | 69.4 | 71.8 | 46.4 | 47.5 | 24.6 | 34.1 |
| With Constraint | **Ours** | **78.5** | **73.8** | **47.2** | **48.9** | **25.7** | **38.3** |
| No Constraint | STTran [7] | 77.9 | 94.4 | 54.0 | 63.7 | 25.2 | 24.6 |
| No Constraint | **Ours** | **95.1** | **55.1** | **65.1** | **38.3** | **26.3** | **25.7** |

> 注：表中 Pred Cls R@50 和 SG Gen R@50 等更多数据见原论文 Table 1。No Constraint 下 Pred Cls R@50 数据不稳定，Ours 在 R@10/R@20 更可靠。

**Over STTran (With Constraint) 提升**：
- Pred Cls: R@10 +0.8%, R@20 +2.0%
- SG Cls: R@10 +0.8%, R@18 +1.4% (from 47.5→48.9)
- SG Gen: R@10 +1.1% (from 24.6→25.7), R@20 +4.2% (from 34.1→38.3)

### 消融实验结果（With Constraint）

| 设置 | Pred Cls R@20 | Pred Cls R@50 | SG Cls R@20 | SG Cls R@50 | SG Gen R@20 | SG Gen R@50 |
|------|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|
| w/o Semantic | 72.65 | 72.97 | 47.25 | 47.30 | 35.62 | 37.94 |
| w/o long-term | 72.24 | 72.98 | 47.81 | 47.15 | 35.67 | 37.71 |
| w/o Pre-training | 71.57 | 71.59 | 44.96 | 45.82 | 33.24 | 35.92 |
| **Full model** | **73.81** | **73.84** | **48.94** | **48.94** | **36.11** | **38.28** |

**关键发现**：去除预训练后性能下降最显著（Pred Cls R@50 从 73.84 降至 71.59，下降 2.25），说明预训练确实捕获了时序相关性。

### 未标注数据消融

| 方法 | Pred Cls R@20 | SG Gen R@20 |
|------|:-----:|:-----:|
| STTran [7] | 71.8 | 24.6 |
| STTran* (same data scale) | 72.0 | 24.7 |
| **Ours** | **73.8** | **25.7** |

### 超参数分析 (Figure 4)
- 短时序列长度 γ=4 时性能最佳
- 长时序列长度 λ=10 时性能趋于稳定
- 可学习的线性聚合函数优于平均池化和最大池化
- 可学习的帧编码优于 Sinusoidal 编码

## Limitations

1. **依赖 IoU 匹配追踪**：短时编码器中通过 IoU 阈值 0.8 匹配帧间 subject-object pair，在物体快速运动或遮挡严重时可能导致匹配失败或产生 placeholder
2. **计算开销**：对每对 subject-object 都构建时序序列并分别通过 Transformer 编码，当帧中物体较多时计算量大
3. **仅 Action Genome 上评估**：未见在其他视频 SGG 数据集（如 VidVRD、ImageNet Video）上的结果
4. **生成策略的非对称结果**：No Constraint 下 Pred Cls R@50 下降（95.1→55.1），论文解释为多谓词允许增加了猜测空间，但非对称性能变化需要进一步分析

## Reusable Claims

- **面向预训练范式**：将时序关系预测转化为从历史帧预判当前帧的任务，可以有效引导模型在任务层面显式学习时序相关性，优于仅在特征层面嵌入时序信息的方法
- **短+长时序双编码器**：短时编码器捕捉直接相邻帧的细粒度关系变化，长时编码器捕获更广时间范围的视觉上下文，两者互补改善动态场景图预测
- **未标注帧价值**：利用 Action Genome 的未标注帧进行预训练（不使用检测框/类别标注），可以额外提升性能
- **可学习聚合 vs 静态池化**：可学习的线性聚合函数（f_θ = W_θ(ϕ(u_{t−λ}) ⊗ ... ⊗ ϕ(u_{t−1}))）在长时序关系压缩上优于平均池化和最大池化

## Connections

- **[STTran [7]](https://openaccess.thecvf.com/content/ICCV2021/papers/Cong_Spatial-Temporal_Transformer_for_Dynamic_Scene_Graph_Generation_ICCV_2021_paper.pdf)**（ICCV 2021）：最直接相关工作，也使用 Transformer 建模时序依赖。本文差异在于提出面向预训练范式显式建模时序相关性
- **GTR**（IJCAI 2023）：后续工作，提出嫁接-重组框架改进动态 SGG
- **Teng et al. [39]**（ICCV 2021, Target Adaptive Context Aggregation）：使用 3D 卷积捕获视频 SGG 时序信息
- **Action Genome [18]**（CVPR 2020）：本方法所评估的数据集
- **BERT [9]**：预训练范式在 NLP 的成功启发了本方法将预训练+微调应用于动态 SGG

## Open Questions

1. 面向预训练范式是否能在更精细的帧级标注数据集（如 VidOR / VidVRD）上带来更大提升？
2. IoU 匹配追踪是时序建模的瓶颈，是否存在可学习的帧间物体关联方法能提升追踪鲁棒性？
3. 短时序列长度 γ=4 和长时序列长度 λ=10 为数据集特定最优，是否有自适应序列长度选择策略？
4. No Constraint 下 R@50 的异常下降原因未充分分析，是否由多标签 margin loss 设计导致？

## Provenance

- **Raw source**: raw/sources/2022-06-01-dynamic-scene-graph-generation-via-anticipatory-pre-training.pdf (1.24 MB)
- **Extracted text**: raw/sources/2022-06-01-dynamic-scene-graph-generation-via-anticipatory-pre-training.txt (49.4K chars, 1400 lines)
- **Evidence level**: full-paper（全文提取精读，覆盖 Introduction、Method、Experiments、Results 全部章节）
- **Accessed**: 2026-06-10
