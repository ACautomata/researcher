---
title: "SceneLLM: Implicit Language Reasoning in LLM for Dynamic Scene Graph Generation"
type: paper
domain: scene-graph
status: active
created: 2026-06-10
updated: 2026-06-10
tags: [dynamic-sgg, llm, implicit-language-reasoning, v2l-mapping, video-scene-understanding, scene-graph-generation]
paper:
  title: "SceneLLM: Implicit Language Reasoning in LLM for Dynamic Scene Graph Generation"
  authors: ["Hang Zhang", "Zhuoling Li", "Jun Liu"]
  year: 2024
  venue: arXiv preprint (May 2025 v2)
  arxiv: "2412.11026"
  doi: null
  code: null
  project: null
classification:
  label: scene-graph-generation, llm, dynamic-scene-graph
  task: [Dynamic Scene Graph Generation]
  method_family: [LLM-based Reasoning, VQ-VAE, Optimal Transport, LoRA]
  modality: [Video]
  datasets: [Action Genome (AG)]
  metrics: [Recall@K (R@10, R@20, R@50)]
evidence_level: full-paper
raw_sources: [raw/sources/2024-12-SceneLLM-Implicit-Language-Reasoning-LLM-Dynamic-SGG.pdf]
related_pages: []
---

# SceneLLM: Implicit Language Reasoning in LLM for Dynamic Scene Graph Generation

> SceneLLM 首次将 LLM 作为隐式语言推理引擎用于动态场景图生成，通过 Video-to-Language (V2L) 映射将视频信号转换为类似语言的 token 序列，利用 LLaMA-13B 的隐式世界知识推理时空语义关系。

## Citation

**SceneLLM: Implicit Language Reasoning in LLM for Dynamic Scene Graph Generation**  
Hang Zhang, Zhuoling Li, Jun Liu  
arXiv:2412.11026v2 [cs.CV] (May 2025)  
[https://arxiv.org/abs/2412.11026](https://arxiv.org/abs/2412.11026)

## One-Sentence Contribution

将 LLM 作为隐式场景推理引擎，通过 V2L 映射（VQ-VAE 离散化 + SIA 空间聚合 + OT 时序对齐）产生类语言"场景句子"，输入 LLaMA-13B（LoRA 微调）进行隐式推理，再由 Transformer SGG predictor 解码为动态场景图，在 Action Genome 上取得 SOTA。

## Problem Setting

- **任务**：Dynamic Scene Graph Generation（视频级场景图生成）
- **输入**：视频帧序列 V = {Iτ}（T 帧）
- **输出**：结构化场景图序列 G = {Gτ}（每帧包含三元组 <Subject-Predicate-Object>、bounding boxes 和类别标签）
- **挑战**：
  1. 视频中目标间复杂的时空交互
  2. 数据集长尾分布导致模型推理偏差
  3. 视频信号与语言信号的模态差异（连续/离散）

## Method

### 整体框架

场景视频 → V2L Mapping → 隐式语言信号（scene sentences）→ LLaMA-13B（LoRA 微调）→ Transformer SGG Predictor → 动态场景图三元组

### Video-to-Language (V2L) Mapping Module

**Stage 1: Feature Discrete Quantization**

- 使用 Faster R-CNN 检测器提取 ROI 特征
- VQ-VAE（Encoder + Codebook C ∈ R^{512×512} + Decoder）将连续视觉特征离散化：
  - f^d_n = argmin_{c_k ∈ C} ||f̃_n - c_k||₂
- 离散化使视觉特征更接近自然语言 token 形式，便于 LLM 理解

**Stage 2: Implicit Linguistic Signal Generation**

包含两个核心组件：

#### (1) Spatial Information Aggregation (SIA)

受汉字结构启发（汉字由偏旁部首按空间结构组合而成）：
- 将视频帧类比为汉字，目标类比为偏旁部首，目标间空间关系类比为汉字空间结构
- Position Embedding：MLP 将目标边界框 (x, y, w, h) 编码为位置嵌入 P_n
- Hierarchical Clustering (HC)：基于位置嵌入的离散特征 F^d+，通过层次聚类构建目标间连接 C
- Graph Convolutional Network (GCN)：在连接图 C 上融合特征，生成帧级 token t
- 对 T 帧视频得到帧级 token 序列 {tτ}_{τ=1}^{T}

#### (2) Optimal Transport (OT) Scheme

- 帧级 token 仅包含单帧空间信息，缺乏时序一致性
- 使用 Optimal Transport 在不同帧级 token 间传输语义信息，生成具有时序信息的视频级隐式语言信号
- 从原始 codebook C 更新到 C⁺，得到最终的隐式语言信号 S_LLM

### LLM Fine-tuning with LoRA

- 使用冻结的 LLaMA-13B 作为 LLM
- 通过 LoRA（Low-Rank Adaptation）微调，保持预训练权重不变的同时使 LLM 能理解"场景句子"
- LoRA 仅更新低秩适配矩阵，参数高效

### SGG Predictor

- 基于 Transformer 的解码器，将 LLM 推理输出解码为语义三元组
- 支持三个子任务：PREDCLS、SGCLS、SGDET

### 训练流程

**第一阶段：VQ-VAE 训练**
- 300,000 次迭代，AdamW 优化器，学习率 3e-4
- 重构视觉特征

**第二阶段：SceneLLM 训练**
- 先优化 MLP、GCN 和 SGG predictor（30,000 次迭代，学习率 1e-5）
- 然后 LoRA 微调 LLM（50,000 次迭代，学习率 1e-5）
- 权重因子 α = 0.5（Eq.8 门控融合系数）

## Experiments

### 设定

| 维度 | 详情 |
|------|------|
| **数据集** | Action Genome (AG)：35 个对象类别 + 25 种谓词关系（attention/spatial/contact 三种类型） |
| **数据划分** | 7,584 训练 / 1,750 测试（同原标准划分） |
| **评估协议** | 三个子任务：PREDCLS（给定 GT box + GT object label 预测谓词）, SGCLS（给定 GT box 预测 object label + 谓词）, SGDET（检测 box + 预测 object label + 谓词） |
| **评估指标** | Recall@K (R@10, R@20, R@50)，分别在有约束（With Constraint: 每对目标最多一个谓词）和无约束（No Constraint: 每对目标允许多个谓词）设置下报告 |
| **检测器** | Transformer-based detector，COCO 预训练 → AG 微调（同 OED[49]） |
| **LLM** | LLaMA-13B（冻结，LoRA 微调） |
| **VQ-VAE** | 隐特征维度 512，codebook size 512，权重因子 λ = 0.02 |
| **时序模型** | 1 层 ConvGRU，kernel size (1,1) |
| **优化器** | AdamW |
| **第二阶段学习率** | 1e-5 |
| **LoRA 迭代** | 50,000 |
| **硬件** | Nvidia A5000 GPU |

### Baselines

M-FREQ[36]、VCTREE[50]、RelDN[35]、GPS-Net[7]、TRACE[6]、STTran[8]、APT[9]、TEMPURA[11]、TR2[2]、TD2-Net[10]、FloCoDe[51]、OED[49]、DDS[52]、STABILE[53]、DIFFVSGG[54]

## Results

### 有约束设置（With Constraint）

| 方法 | PREDCLS R@10/20/50 | SGCLS R@10/20/50 | SGDET R@10/20/50 |
|------|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| **SceneLLM (Ours)** | **74.1** / **77.8** / **77.8** | **53.7** / **55.0** / **55.0** | **34.9** / **43.3** / **49.5** |
| OED[49] | 73.0 / 76.1 / 76.1 | — / — / — | 33.5 / 40.9 / 48.9 |
| DIFFVSGG[54] | 71.9 / 74.5 / 74.5 | 52.5 / 53.7 / 53.7 | 32.8 / 39.9 / 45.5 |
| DDS[52] | — / — / — | — / — / — | 36.2 / 42.0 / 47.3 |
| FloCoDe[51] | 70.1 / 74.2 / 74.2 | 48.4 / 51.2 / 51.2 | 31.5 / 38.4 / 42.4 |

SceneLLM 在有约束设置下，PREDCLS 平均优于第二名 OED 1.5%（R@10 +1.1, R@20 +1.7, R@50 +1.7），SGDET 平均优于 OED 1.5%（R@10 +1.4, R@20 +2.4, R@50 +0.6）。

### 无约束设置（No Constraint）

| 方法 | PREDCLS R@10/20/50 | SGCLS R@10/20/50 | SGDET R@10/20/50 |
|------|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| **SceneLLM (Ours)** | **83.7** / **97.2** / **99.9** | **61.2** / **69.7** / **71.1** | **37.4** / **46.1** / **53.4** |
| OED[49] | 83.3 / 95.3 / 99.2 | — / — / — | 35.3 / 44.0 / 51.8 |
| DIFFVSGG[54] | 83.1 / 94.5 / 99.1 | 60.5 / 70.5 / 74.4 | 35.4 / 42.5 / 51.0 |
| DDS[52] | — / — / — | — / — / — | 37.3 / 43.3 / 51.5 |
| FloCoDe[51] | 82.8 / 97.2 / 99.9 | 57.4 / 66.2 / 68.8 | 32.6 / 43.9 / 51.6 |

SceneLLM 在无约束设置下 PREDCLS 平均提升 1.0%，SGDET 平均提升 1.9%。

### 消融实验

**LLM 影响（SGCLS With Constraint）**：

| 变体 | R@10 | R@20 | R@50 |
|------|------|------|------|
| w/o LLM（跳过 LLM 直接解码） | 38.9 | 40.3 | 40.3 |
| w/ T5（较小 LLM 替代 LLaMA） | 51.5 | 53.0 | 53.0 |
| **SceneLLM（w/ LLaMA）** | **53.7** | **55.0** | **55.0** |

→ LLaMA 显著优于无 LLM 设置（+14.7 R@50）和 T5 设置（+2.0 R@50），证明强大 LLM 的必要性。

**特征离散化影响（SGCLS With Constraint）**：

| 变体 | R@10 | R@20 | R@50 |
|------|------|------|------|
| w/o discretization（直接用连续特征） | 40.4 | 42.6 | 42.6 |
| **SceneLLM** | **53.7** | **55.0** | **55.0** |

→ 离散化对场景理解至关重要。

**Optimal Transport 影响（SGCLS With Constraint）**：

| 变体 | R@10 | R@20 | R@50 |
|------|------|------|------|
| w/o OT（直接输入帧级 token） | 50.9 | 52.3 | 52.3 |
| Temporal Convolution (TC) | 50.8 | 52.0 | 52.0 |
| Clustering | 50.6 | 51.2 | 51.2 |
| **SceneLLM** | **53.7** | **55.0** | **55.0** |

→ OT 方案因能维护时序一致性而最优。

**LoRA 影响（SGCLS With Constraint）**：

| 变体 | R@10 | R@20 | R@50 |
|------|------|------|------|
| w/o LoRA（全参数微调） | 47.3 | 48.4 | 48.4 |
| **SceneLLM** | **53.7** | **55.0** | **55.0** |

→ LoRA 微调比全参数微调更好，说明保持预训练知识的重要性。

**权重因子 α**：通过网格搜索得最优 α = 0.5（在有无约束下一致表现最佳，基于 R@K 指标）。

## Limitations

1. **LLM 计算开销**：使用 LLaMA-13B 作为推理引擎，推理成本高于传统 CNN/Transformer 方法，实际部署可能受限
2. **AG 数据集限制**：仅 35 类对象 + 25 类关系，在更复杂场景或开放世界设定中泛化性未知
3. **V2L 映射信息损失**：从连续视觉特征到离散 token 再到隐式语言信号的转换链条中，可能有空间-时间细节信息丢失
4. **代码未公开**：论文未提供代码链接，结果可复现性待验证
5. **视频长度限制**：隐式语言信号基于 VQ-VAE 离散化 + OT 对齐，处理长视频的扩展性未讨论
6. **与之前方法比较公平性**：使用 Transformer-based detector（同 OED），但其他 baseline 可能使用不同检测 backbone，直接比较需谨慎
7. **未在开放世界/3D 场景**验证：作者提到这是未来方向，当前仅验证 AG 一个数据集

## Reusable Claims

- **Claim**: LLM 的隐式世界知识可以用于动态场景图的时空关系推理，通过将视频信号转换为类语言格式即可激活该能力
  - Evidence: SceneLLM 在 AG 全三项任务上 SOTA，且 w/o LLM 变体性能大幅下降（-14.7 R@50）
  - Scope: Action Genome 数据集，动态 SGG 任务

- **Claim**: VQ-VAE 离散化 + OT 时序对齐的组合优于直接使用连续视觉特征或简单时序卷积
  - Evidence: 消融实验 w/o discretization (-13 R@50), w/o OT (-2.7 R@50), Clustering (-3.8 R@50), TC (-3.0 R@50)
  - Scope: AG 数据集，LoRA 微调 LLaMA 设置

- **Claim**: LoRA 参数高效微调优于全参数微调，因为保护了 LLM 预训练的隐式场景知识
  - Evidence: w/o LoRA (全微调) R@50 = 48.4 vs SceneLLM (LoRA) R@50 = 55.0, 差距 +6.6
  - Scope: LLaMA-13B, AG 数据集

## Connections

- **OED[49]**：使用相同 Transformer detector backbone，SceneLLM 添加 LLM 推理层后超越
- **LLM4SGG**（同类方向）：SceneLLM 是首个将 LLM 作为隐式推理引擎用于动态 SGG 的工作
- **DIFFVSGG[54]**：扩散驱动 SGG，SceneLLM 在 PREDCLS 和 SGCLS 上有显著优势，SGDET 略领先
- **STTran[8]/TEMPURA[11]/TR2[2]**：视频 SGG 的时空建模方法，SceneLLM 利用 LLM 提供语义推理补充
- **Chinese Character SIA**：独特的层次聚类 + GCN 空间聚合方式，连接了汉字空间结构与视觉场景空间推理

### 与相关工作的关键差异

| 维度 | 传统方法 | SceneLLM |
|------|----------|----------|
| 推理引擎 | CNN/Transformer | LLaMA-13B（隐式语义推理） |
| 视频表示 | 时空特征图 | 离散类语言 token 序列 |
| 时序建模 | 3D Conv / LSTM / Transformer | Optimal Transport 对齐 |
| 参数效率 | 全模型微调 | LoRA 高效微调 |

## Open Questions

1. SceneLLM 在使用更大 LLM（如 LLaMA-70B、GPT-4）时能否进一步提升？更大的 LLM 是否有更好的"场景理解"隐式知识？
2. OT 方案的计算复杂度与视频帧数的关系如何？能否扩展到长视频（≥100 帧）？
3. V2L 映射中，离散化 codebook 大小对性能的影响——是否有最优 m 值的理论依据？
4. 在开放世界动态场景图生成中，SceneLLM 能否泛化到未见过的对象类别或关系？
5. SceneLLM 的推理延迟 vs 传统方法差距有多大？是否能在实时或近实时场景中部署？
6. 隐式推理与显式推理（如 Chain-of-Thought 提示）在 SGG 上的对比——SceneLLM 强调"隐式"，是否有理论解释为什么隐式优于显式？

## Provenance

- **本文证据等级**：full-paper（基于完整的 arXiv PDF 全文提取和分析）
- **原始来源**：raw/sources/2024-12-SceneLLM-Implicit-Language-Reasoning-LLM-Dynamic-SGG.pdf（2.77 MB, 29 页）
- **提取文本**：raw/sources/2024-12-SceneLLM-Implicit-Language-Reasoning-LLM-Dynamic-SGG.txt（52,253 字符, 1,461 行）
- **入库日期**：2026-06-10
- **数据完整性**：全文完整提取，包含 Abstract、Introduction、Method (3 节)、Experiments (4 子节)、Conclusion、References (55 篇)。前三页为作者地址和关键词信息。
- **缺失信息**：代码链接未公开；消融实验仅报告 SGCLS 任务的 With Constraint 设置；SGDET 和 PREDCLS 的消融实验未单独报告；推理延迟/效率对比未提供。
