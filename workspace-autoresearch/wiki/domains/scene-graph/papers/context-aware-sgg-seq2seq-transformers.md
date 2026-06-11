---
title: "Context-Aware Scene Graph Generation With Seq2Seq Transformers"
type: paper
domain: scene-graph
status: active
created: 2026-06-10
updated: 2026-06-10
tags:
  - scene-graph-generation
  - transformer
  - seq2seq
  - reinforcement-learning
  - ICCV-2021
  - autoregressive-decoding
source_pages: []
raw_sources:
  - raw/sources/2021-10-01-context-aware-scene-graph-generation-with-seq2seq-transformers.pdf
related_pages:
  - domains/scene-graph/papers/neural-motifs-scene-graph-global-context.md
  - domains/scene-graph/papers/vctree-learning-to-compose-dynamic-tree-structures.md
  - domains/scene-graph/papers/sgtr-end-to-end-scene-graph-generation-with-transformer.md
  - domains/scene-graph/papers/reltr-relation-transformer-scene-graph-generation.md
paper:
  title: "Context-Aware Scene Graph Generation With Seq2Seq Transformers"
  authors:
    - Yichao Lu
    - Himanshu Rai
    - Jason Chang
    - Boris Knyazev
    - Guangwei Yu
    - Shashank Shekhar
    - Graham W. Taylor
    - Maksims Volkovs
  year: 2021
  venue: ICCV 2021
  code: https://github.com/layer6ai-labs/SGG-Seq2Seq
classification:
  label: scene-graph-generation
  task:
    - scene graph generation
    - visual relationship detection
  method_family:
    - seq2seq transformer
    - autoregressive decoding
    - reinforcement learning
  modality: image
  datasets:
    - Visual Genome (VG)
    - Visual Relationship Detection (VRD)
  metrics:
    - Recall@K
    - mRecall@K
evidence_level: full-paper
---

## Citation

Lu, Y., Rai, H., Chang, J., Knyazev, B., Yu, G., Shekhar, S., Taylor, G. W., & Volkovs, M. (2021). Context-Aware Scene Graph Generation With Seq2Seq Transformers. *ICCV 2021*.

## One-Sentence Contribution

将场景图生成建模为序列到序列的自回归预测问题，利用 Transformer encoder-decoder 架构和策略梯度强化学习直接优化 recall/mRecall 指标，在 VG 和 VRD 上取得 SOTA。

## Problem Setting

**Scene Graph Generation (SGG)**: 给定图像，检测物体并预测物体之间的视觉关系（subject-predicate-object 三元组）。

**关键观察**：大多数现有 SGG 方法假设关系三元组之间相互独立，并行预测所有关系。作者通过分析 Visual Genome 中三元组共现统计发现，三元组之间存在强条件依赖——给定已预测的三元组可显著提升后续预测的准确性。

**形式化**：将 SGG 重写为条件概率链式分解：
p(Y₁:ₘ) = ∏ₘ p(yₘ | y₁:ₘ₋₁)

## Method

### 整体架构

采用 **Transformer encoder-decoder** 架构。整体流程：

1. **Object Detector (Faster-RCNN)** → 检测 N 个物体的 bounding box 和表示 X = {x₁, ..., xₙ}
2. **Transformer Encoder**（B=4 blocks）→ 对物体特征进行上下文编码，得到 Xᴮ
3. **Transformer Decoder**（K=2 blocks）→ 自回归预测关系三元组

### Encoder

- 标准 Transformer encoder，B=4 block
- 每个 block: MSA + FFN + residual
- 输入：物体特征（spatial + semantic + visual features, 参考 RelDN [64]）
- 输出：包含全局上下文信息的物体嵌入 Xᴮ

### Decoder

- 自回归式预测关系三元组
- 每个时间步输入已预测的 m 个三元组序列 Ŷ₁:ₘ
- 将每个三元组 (subject embedding, predicate embedding, object embedding) 拼接→FC 投影→D 维表示
- 经过 K=2 个 decoder block（self-attention + cross-attention with Xᴮ）
- 输出 Yᴷ，其中最后一个位置编码 Yᴷ[m] 与所有可能的剩余 subject-object pair 拼接后预测关系

**关键设计**：Cross-attention 将已预测的 triplet 表示与所有物体特征关联，使模型能"看到"全局上下文并动态调整后续预测。

### 训练策略

**Teacher Forcing**：训练时提供 ground truth 历史，对每个 triplet 最大化 p(yₘ₊₁|Xᴮ, Y₁:ₘ)。随机打乱 triplet 顺序（每个 batch 重新 shuffle）。包含负样本（L 个无关系物体对）。

**Reinforcement Learning（核心贡献）**：

- 直接优化非可微的目标指标（recall / mRecall）
- 奖励函数：R = α·recall + (1-α)·mRecall，α∈[0,1] 控制 trade-off
- 使用 **self-critical policy gradient** + **Monte Carlo search**（T=16 个 rollout samples）
- 在第 2 阶段交替使用 teacher forcing 和 RL 训练

### 推理

- 自回归解码，每次选取概率最高的 triplet 作为输出
- 支持 block decoding（多步同时解码）以加速推理

## Experiments

### 数据集

| 数据集 | 划分来源 | 任务 | 评估指标 |
|--------|---------|------|---------|
| Visual Genome (VG) | [51] | SGDET, SGCLS, PRDCLS | Recall@K, mRecall@K (K=20,50,100) |
| Visual Relationship Detection (VRD) | [58] | RelDetect, PhraseDetect | Recall@50, 100 |

### Baseline 方法

**VG**: Associative Embedding, Message Passing, Graph R-CNN, Message Passing+, Frequency+Overlap, MotifNet-LeftRight, RelDN, VCTree, HetH, GB-Net, MOTIFS+TDE(GATE), VTransE+TDE(GATE), VCTree+TDE(SUM)
**VRD**: ViP-CNN, VRL, CAI, KL-Distill, ZoomNet, CAI+SCA-M, HetH, RelDN

### 训练设置

- Optimizer: Adam (β₁=0.9, β₂=0.999)
- Batch size: 4096
- Learning rate: 1e-3 (linear warmup 1K steps → cosine decay)
- Architecture: 4 encoder blocks, 2 decoder blocks, embedding dim 128, 4 attention heads
- Epochs: 500 (VRD) / 2000 (VG)
- RL playout samples: T=16
- 第 1 阶段：teacher forcing 训练；第 2 阶段：alternating TF + RL

### 消融实验变体

| 变体 | 说明 |
|------|------|
| Seq2Seq - encoder only | 移除 decoder，仅用 encoder + FFN 分类 |
| Seq2Seq - teacher forcing | 仅使用 teacher forcing 训练 |
| Seq2Seq - scheduled sampling | teacher forcing + scheduled sampling |

## Results

### VRD 结果

**Relationship Detection (free k)**:

| 方法 | R@50 | R@100 |
|------|------|-------|
| RelDN [64] | 25.2 | 28.6 |
| HetH [49] | 22.4 | 24.8 |
| **Seq2Seq-RL (ours)** | **26.1** | **30.2** |
| Seq2Seq - encoder only | 24.4 | 27.9 |
| Seq2Seq - teacher forcing | 27.1 | 29.0 |
| Seq2Seq - scheduled sampling | 27.5 | 29.8 |

**Phrase Detection (free k)**:

| 方法 | R@50 | R@100 |
|------|------|-------|
| RelDN [64] | 34.4 | 36.4 |
| HetH [49] | 35.4 | 37.3 |
| **Seq2Seq-RL (ours)** | **36.8** | **46.2** |

### VG Recall 结果（with graph constraint）

**SGDET**:

| 方法 | R@20 | R@50 | R@100 |
|------|------|------|-------|
| RelDN [64] | 21.1 | 28.3 | 32.7 |
| VCTree [44] | 22.0 | 27.9 | 31.3 |
| MotifNet [60] | 21.4 | 27.2 | 30.3 |
| **Seq2Seq-RL (ours)** | **22.1** | **30.9** | **34.4** |

**SGCLS**:

| 方法 | R@20 | R@50 | R@100 |
|------|------|------|-------|
| GB-Net [59] | — | 38.0 | 38.8 |
| VCTree [44] | 35.2 | 38.1 | 38.8 |
| **Seq2Seq-RL (ours)** | **34.5** | **38.3** | **39.0** |

**PRDCLS**:

| 方法 | R@20 | R@50 | R@100 |
|------|------|------|-------|
| GB-Net [59] | — | 66.6 | 68.2 |
| VCTree [44] | 60.1 | 66.4 | 68.1 |
| **Seq2Seq-RL (ours)** | **60.3** | **66.4** | **68.5** |

### VG mRecall 结果

| 方法 | PRDCLS@50 | PRDCLS@100 | SGCLS@50 | SGCLS@100 | SGDET@50 | SGDET@100 |
|------|-----------|------------|----------|-----------|----------|-----------|
| MOTIFS+TDE(GATE) [43] | 24.9 | 28.3 | 13.9 | 15.2 | 8.5 | 9.9 |
| VCTree+TDE(SUM) [43] | 25.4 | 28.7 | 12.2 | 14.0 | 9.3 | 11.1 |
| **Seq2Seq-RL (ours)** | **26.1** | **30.5** | **14.7** | **16.2** | **9.6** | **12.1** |

**关键差距**：Seq2Seq-RL 在 mRecall@100 上比 MOTIFS+TDE 提升 +2.2 (PRDCLS), +1.0 (SGCLS), +2.2 (SGDET)。

### 消融实验发现

- **Encoder only** vs full model: 全任务一致退化，证明 conditional sequential decoding 有效
- **Teacher forcing only** vs RL: 替换 ground truth 为自预测 + 优化目标指标显著提升性能
- **Scheduled sampling** vs RL: 部分缩小差距但无法完全消除
- **训练稳定性**: 10 次不同 seed 训练 SGDET 的 std = 0.13，表明极稳定

### α（Recall vs mRecall trade-off）

通过对 α 在 [0,1] 范围扫描，验证 recall 和 mRecall 逆向相关（与已有文献一致）。RL 奖励函数可灵活控制两个指标的平衡。

## Limitations

- 依赖预训练 object detector（Faster-RCNN）
- Relation detection 模块仍受限于预定义 predicate 集合
- Block decoding 加速推理时会降低准确性（减少 sequential conditioning 效果）
- RL 训练需要多次 Monte Carlo rollout（T=16），增加训练计算量

## Reusable Claims

1. **SGG 中三元组之间存在强条件依赖**: 条件预测（co-occurrence analysis）可显著提升预测准确性，验证了自回归建模的有效性。
2. **RL 直接优化指标优于 teacher forcing**: Self-critical policy gradient + Monte Carlo search 可以直接优化非可微的 recall/mRecall，消除训练-推理 gap。
3. **Recall 和 mRecall 是逆向相关的**: α 扫描实验验证了这一 trade-off，RL 奖励函数可灵活调节。

## Connections

- **Neural Motifs [60]**: 也用 LSTM 编码全局上下文，但预测时独立进行。本工作核心改进是用 Transformer decoder 做条件自回归预测。
- **VCTree [44]**: 动态树结构建模上下文，本工作用 Transformer 的 self-attention 取代。
- **SGTR [CVPR 2022]**: 后续工作将 Transformer 应用于 end-to-end SGG，本工作是其前驱之一。
- **RelTR [2023]**: Relation Transformer，也是本方法同一路线。

## Open Questions

- 如何扩展到开集（open-vocabulary）predicate 集合？
- Block decoding 的性能退化能否通过更好的预测顺序策略缓解？
- RL reward 能否设计更复杂的多目标奖励以同时优化多个指标？
- 本方法的自回归缓慢问题如何在大规模场景中解决？

## Provenance

- **Raw source**: `raw/sources/2021-10-01-context-aware-scene-graph-generation-with-seq2seq-transformers.pdf`
- **Extraction**: pdfminer 提取全文 54,518 字符
- **Analysis method**: 全文精读 + 实验结果逐表记录
- **Evidence level**: full-paper — 捕获了方法细节、消融实验、所有主要结果表和定性分析
- **Missing**: 补充材料（supplementary）未获取；定性可视化（Figure 6）的更多示例未逐张记录
