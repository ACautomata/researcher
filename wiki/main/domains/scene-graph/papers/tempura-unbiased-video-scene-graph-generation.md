---
title: TEMPURA: Unbiased Scene Graph Generation in Videos
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - video-scene-graph
  - dynamic-scene-graph
  - unbiased-sgg
  - long-tail
  - temporal-consistency
  - memory-guided
  - uncertainty-attenuation
raw_sources:
  - ../../../sources/scene-graph/2023-CVPR-TEMPURA-Unbiased-Scene-Graph-Generation-in-Videos.pdf
  - ../../../sources/scene-graph/2023-CVPR-TEMPURA-Unbiased-Scene-Graph-Generation-in-Videos.txt
paper:
  title: Unbiased Scene Graph Generation in Videos
  short_title: TEMPURA
  authors:
    - Sayak Nag
    - Kyle Min
    - Subarna Tripathi
    - Amit K. Roy-Chowdhury
  year: 2023
  venue: CVPR 2023
  arxiv: null
  doi: null
  code: https://github.com/sayaknag/unbiasedSGG.git
  project: null
classification:
  label: TEMPURA
  task:
    - Dynamic Scene Graph Generation
    - Unbiased Video Scene Graph Generation
  method_family:
    - Spatio-temporal Transformer
    - Gaussian Mixture Model (GMM)
    - Memory-guided Training
    - Contrastive Learning
  modality:
    - Video
    - Bounding Box
  datasets:
    - Action Genome (AG)
  metrics:
    - mR@K
    - R@K
evidence_level: full-paper
paper_note: CVPR 2023，首发系统性地解决视频场景图生成中的长尾偏置问题，提出三个互补模块：序列一致性建模(OSPU)、不确定性衰减(GMM head)和记忆原型去偏(MDU)。
---

# TEMPURA: Unbiased Scene Graph Generation in Videos

## Citation

Sayak Nag, Kyle Min, Subarna Tripathi, Amit K. Roy-Chowdhury. "Unbiased Scene Graph Generation in Videos." CVPR 2023.

## One-Sentence Contribution

提出 TEMPURA（TEmporal consistency and Memory Prototype guided UnceRtainty Attenuation），通过对象级时序一致性建模、记忆原型引导的知识迁移和高斯混合模型不确定性衰减，首次系统性地解决视频场景图生成中的长尾分布偏置和标注噪声问题。

## Problem Setting

**出发点**：现有动态 SGG 方法（如 STTran、TRACE）主要关注设计复杂架构捕捉时空上下文，但忽略三个关键偏置来源：
1. **长尾分布**：Action Genome 中部分 predicate（如 "in front of / not looking at"）高频出现，而 informative 的 predicate（如 "eating / wiping"）极度稀疏（Fig 1a）
2. **标注噪声**：Action Genome 存在缺失标注、多标签映射和 triplet variability（同一物体对可能有多个正确 predicate），增加预测不确定性（Fig 2）
3. **时序波动**：运动模糊、遮挡导致 off-the-shelf 目标检测器（Faster R-CNN）在视频帧间产生不一致的物体分类（Fig 3）

**TEMPURA 架构**（Fig 4）包含四个核心组件：
- **PEG**（Predicate Embedding Generator）：基于 STTran [10] 的时空 transformer，生成关系嵌入
- **OSPU**（Object Sequence Processing Unit）：用 transformer encoder + 对比学习，对同一物体在各帧的 proposal 特征序列建模，实现时序一致的物体分类
- **GMM Head**：将 predicate 分类头设计为 Gaussian Mixture Model（GMM），通过 MDN loss 惩罚高不确定性样本，衰减标注噪声的不利影响
- **MDU**（Memory Diffusion Unit）：记忆原型库 + 基于注意力的信息扩散，从数据丰富类向数据贫乏类迁移知识，生成更均衡的 predicate 表示

## Key Results

### 与 SOTA 对比（Action Genome 数据集）

| 任务 | 设置 | 指标 | STTran | STTran-TPI | TRACE | TEMPURA (Ours) |
|------|------|------|--------|------------|-------|-----------------|
| **PredCLS** | With Constraint | mR@10 | 37.8 | 37.3 | 15.2 | **42.9** |
| **PredCLS** | With Constraint | mR@20 | 40.1 | 40.6 | 15.2 | **46.3** |
| **SGCLS** | With Constraint | mR@10 | 27.2 | 28.3 | 8.9 | **34.0** |
| **SGCLS** | With Constraint | mR@20 | 28.0 | 29.3 | 8.9 | **35.2** |
| **PredCLS** | No Constraints | mR@10 | 51.4 | — | 50.9 | **61.5** |
| **SGCLS** | No Constraints | mR@10 | 40.7 | — | 31.9 | **48.3** |
| **SGDET** | With Constraint | mR@10 | 16.5 | — | 8.4 | **18.5** |
| **SGDET** | No Constraints | mR@10 | 20.9 | — | 16.5 | **24.7** |

### 相对提升（vs. 最佳 baseline，No Constraints 设置）
- **PredCLS mR@10**: +10.1%（51.4 → 61.5）
- **SGCLS mR@10**: +7.6%（40.7 → 48.3）
- **SGDET mR@10**: +3.8%（20.9 → 24.7）

### 消融实验（Table 4）

Ablation 在 SGCLS / SGDET 的 mR@10（With Constraint）上验证各组件贡献：

| Uncertainty Att. | Memory Debiasing | Temporal Consist. | SGCLS mR@10 | SGDET mR@10 |
|:---:|:---:|:---:|:---:|:---:|
| ✗ | ✗ | ✗ | 27.2 | 16.5 |
| ✓ | ✗ | ✓ | 30.6 | 16.7 |
| ✗ | ✓ | ✓ | 31.8 | 16.8 |
| ✓ | ✓ | ✗ | 30.9 | 17.0 |
| ✓ | ✓ | ✓ | **34.0** | **18.5** |

结论：
- 三个组件均贡献正向收益，组合使用最好
- GMM 头对尾部类的噪声衰减最有效（Prevent under-fitting to TAIL classes）
- MDU 生成的嵌入更均衡，略优于仅使用不确定性衰减
- OSPU 对物体误分类的纠正在 SGDET 任务上尤其重要（Without OSPU 时 SGDET mR@10 下降 1.5 个点）

### GMM 组件数 K 实验（Table 5）

| K | PredCLS mR@10 | SGCLS mR@10 |
|:---:|:---:|:---:|
| 1 | 40.1 | 31.0 |
| 2 | 40.8 | 33.1 |
| 4 | 42.6 | **34.0** |
| 6 | **42.9** | 32.7 |
| 8 | 42.1 | 32.6 |

K=4~6 效果最佳，超过后边际收益递减且显存占用增加。

### TAIL 类性能（Fig 6）

TEMPURA 在 TAIL 类上的 mR@10 显著优于 STTran 和 TRACE，同时在 HEAD 和 BODY 类上的表现不降反升，证明其真正实现了"无偏"的场景图生成。

## Method Details

### OSPU（Object Sequence Processing Unit）
- 对于视频中每个 detected object class，收集所有帧中属于该类别的 proposal 特征序列 T = {vᵢᵗ, vᵢᵗ⁺¹, ...}
- 送入 transformer encoder（SeqEnc）进行 multi-head self-attention 建模长期时序依赖
- 结合对比学习损失（contrastive loss），拉近同一物体在相邻帧的特征、推远不同类别的特征

### GMM Head（Uncertainty Attenuation）
- 将 predicate 分类头设计为 Mixture Density Network（MDN）
- 输出 GMM 参数（mean μk, variance σk, mixing coefficient πk）
- Loss 函数：最小化负对数似然（NLL），高不确定性样本会产生较大 penalty
- 建模两类不确定性：
  - **Aleatoric uncertainty**：标注噪声、运动模糊、多标签等数据内在噪声
  - **Epistemic uncertainty**：尾部类样本不足导致的模型不确定性

### MDU（Memory Diffusion Unit）
- 维护一个记忆原型库 M = {m₁, ..., m_Cr}，每个原型压缩一个 predicate 类的抽象表示
- 渐进更新（Progressive memory computation）：每个 batch 后用指数移动平均更新原型
- 基于注意力的信息扩散（Attention-based diffusion）：评估当前 predicate 嵌入与各原型的相似度，从数据丰富的原型向当前嵌入扩散知识
- 训练损失（MDU）：使用 contrastive 变体，鼓励同类嵌入靠近原型、异类远离

## Connections & Significance

- **与图像 SGG 的关系**：TEMPURA 将图像 SGG 中成熟的去偏思路（如 re-weighting、decoupling、因果干预）扩展到视频域，但额外引入了时序一致性这一视频特有维度。
- **与 STTran [10] 的关系**：直接以 STTran 的时空 transformer 为 PEG 骨干，在其基础上叠加去偏模块。
- **与 TRACE [57] 的关系**：TRACE 使用 3D 模型 + 跟踪来处理视频，TEMPURA 用更轻量的 OSPU（transformer + contrastive）实现类似效果。
- **局限性**：
  - 仅在 Action Genome 上验证（26 个 predicate 类），更大规模视频 SGG 数据集上是否有效待验证
  - GMM 组件数 K 需手动设置（最优值在 4-6 之间）
  - MDU 的内存消耗随 predicate 类别数线性增长
- **后续影响**：后续涌现了一批视频 SGG 去偏工作（2024-2025 CVPR），TEMPURA 是该方向的早期奠基工作之一。

## References

- [STTran: Spatial-Temporal Transformer for Dynamic Scene Graph Generation (ICCV 2021)](prototype-based-embedding-network-scene-graph-generation.md) — TEMPURA 直接继承其 PEG 架构
- [TRACE: Target Adaptive Context Aggregation for Video Scene Graph Generation (ICCV 2021)] — 使用跟踪的对比方法
- PVSG: [Panoptic Video Scene Graph Generation (CVPR 2023)](panoptic-video-scene-graph-generation.md) — 同期视频 SGG 工作，focus 不同（panoptic 而非 unbiased）
