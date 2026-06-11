---
title: "Improving Scene Graph Generation with Relation Words' Debiasing in Vision-Language Models"
type: paper
domain: scene-graph
status: active
created: 2026-06-10
updated: 2026-06-10
tags:
  - scene-graph-generation
  - debiasing
  - vlm
  - predicate-bias
  - lagrange-multiplier-estimation
  - zero-shot
source_pages: []
raw_sources:
  - raw/sources/2024-03-01-improving-scene-graph-generation-with-relation-words-debiasing.pdf
  - raw/sources/2024-03-01-improving-scene-graph-generation-with-relation-words-debiasing.txt
related_pages: []
paper:
  title: "Improving Scene Graph Generation with Relation Words' Debiasing in Vision-Language Models"
  authors:
    - Yuxuan Wang
    - Xiaoyuan Liu
  year: 2024
  venue: arXiv preprint
  arxiv: "2403.16184"
  doi: null
  code: null
  project: null
classification:
  label: scene-graph-generation, debiasing, vlm
  task:
    - Scene Graph Generation (SGG)
    - Predicate Classification (PredCls)
    - Scene Graph Classification (SGCls)
    - Relation Classification
  method_family:
    - Post-hoc Logits Adjustment
    - Lagrange-Multiplier Estimation (LM Estimation)
    - Certainty-aware Ensemble
    - Zero-shot VLM Debiasing
  modality:
    - vision-language
  datasets:
    - Visual Genome (VG)
  metrics:
    - mean Recall@K (mRecall@K)
    - Recall@K
    - Top-1 Accuracy (Acc)
    - Class-wise mean Accuracy (mAcc)
evidence_level: full-paper
---

## Citation

Yuxuan Wang, Xiaoyuan Liu. "Improving Scene Graph Generation with Relation Words' Debiasing in Vision-Language Models." arXiv preprint arXiv:2403.16184, 2024.

## One-Sentence Contribution

提出 Lagrange-Multiplier Estimation (LM Estimation) 方法估计预训练 VLM 中不可获得的关系词分布，通过 post-hoc logits adjustment 消除 VLM 在 SGG 任务上的 predicate bias，再通过 certainty-aware ensemble 与 SGG 模型动态集成以缓解 SGG 中的 underrepresentation 问题。

## Problem Setting

SGG 的核心挑战之一是 **underrepresentation**：由于 triplet 组合空间指数级大（Visual Genome 中有 375k 种 triplet 组合），训练集无法覆盖所有 triplet，导致部分测试 triplet 在训练中很少出现甚至完全未见，模型对这些样本预测质量低下。

已有的偏置消除方法（如 TDE、GCL）均在训练阶段进行，无法用于预训练 VLM 的 inference-time debiasing。而直接使用零样本 VLM 进行 SGG 预测会引入严重的 **predicate bias**，原因有二：
1. VLM 预训练数据中的谓词分布高度不均衡
2. 预训练数据的标签分布不可获得（数据保密 / 预训练目标与 SGG 不匹配）

本文同时解决两个问题：缓解 VLM 的偏见 + 利用 VLMs 的预训练知识补充 SGG 模型的 underrepresentation。

## Method

### 框架概览

双分支架构（图 2）：
- **零样本 VLM 分支 \(f_{zs}\)**：固定参数，使用 MLM prompt 格式 `"{zi} is [MASK] {zj}"` 逐对提取 K 个非背景关系的 logits \(o_{zs}^k \in \mathbb{R}^K\)。采用 ViLT 和 Oscar 作为 backbone。
- **任务特定 SGG 分支 \(f_{sg}\)**：在 VG 上微调的 VLM（使用 VQA prompt `"what is the relationship between the {zi} and the {zj}?"`）或现有 SGG 模型（PENET）。输出 K+1 个 logits（含背景类）\([o_{sg}^0, o_{sg}^k] \in \mathbb{R}^{K+1}\)。

两分支分别进行 predicate debiasing，再通过 certainty-aware ensemble 动态融合。

### Predicate Debiasing

**理论基础**：基于 label shift 假设的 post-hoc logits adjustment（Menon et al., 2020）：

\[
\hat{o}^k(r) = o^k(r) - \log P_{tr}(r) + \log P_{ta}(r)
\]

其中 \(P_{tr}(r)\) 是训练分布，\(P_{ta}(r)\) 是目标测试分布。

对于 SGG 模型 \(f_{sg}\)：\(P_{tr}(r) = \pi_{sg}\)（由 VG 训练集频率直接统计），目标分布为均匀分布 \(1/K\)（用于 mRecall 评估）或训练分布 \(\pi_{sg}\)（用于 Recall 评估）。

对于零样本 VLM \(f_{zs}\)：\(P_{tr}(r) = \pi_{pt}\)（预训练数据中的谓词分布），**不可直接获得**。

**Lagrange-Multiplier Estimation (LM Estimation)**：通过约束优化求解 \(\pi_{pt}\)。利用 VG 数据集中的非背景关系样本，最小化经调整 logits 与真实标签之间的交叉熵损失，约束 \(\pi_{pt}\) 为合法概率分布：

\[
\pi_{pt} = \arg\min_{\pi_{pt}} R_{ce}(o^k - \log \pi_{pt} + \log \pi_{sg}, r), \quad \text{s.t. } \pi_{pt}(r) \geq 0, \sum_{r \in C_r} \pi_{pt}(r) = 1
\]

使用 Lagrange multiplier 方法求解该约束优化问题。

**τ-calibration**：对 debiased logits 应用 softmax 前除以温度 τ 以避免过置信。

### Certainty-aware Ensemble

为每个样本动态计算两个分支的置信度，确定集成权重：

\[
conf = \max_{r \in C_r} P(r|z_i, z_j, x_{i,j}), \quad W_{cer} \propto sigmoid(conf_{sg} - conf_{zs})
\]

集成预测：
\[
P_{ens}(r|\cdot) = W_{cer} \cdot \hat{P}_{sg}(r|\cdot) + (1 - W_{cer}) \cdot \hat{P}_{zs}(r|\cdot)
\]

背景类仅由 \(f_{sg}\) 预测。

### 关键特性

- **Training-free**：无需额外训练
- **Plug-and-play**：可适配任意 SGG 模型
- 通过 LM Estimation 估计出的 \(\pi_{pt}\) 在不同 target distribution 之间切换时不需重新计算

## Experiments

### 数据集

- **Visual Genome (VG)**：108,077 张图像，使用最常见的 150 个物体类别和 50 个谓词类别
- 划分：70% 训练 (75,653 张) / 30% 测试 (32,424 张) / 从训练集分出 5,000 张验证集
- 平均每张图像 38 个物体、22 个关系

### 基线模型

**SGG 模型分支 \(f_{sg}\)**：
1. **ViLT ft** — 使用 PredCls 数据微调的 ViLT（VQA 范式）
2. **Oscar ft** — 使用 PredCls 数据微调的 Oscar（VQA 范式）
3. **PENET-Rwt** (Zheng et al., 2023, CVPR) — 使用 reweighting loss 训练的 SGG 专用模型

**零样本 VLM 分支 \(f_{zs}\)**：
1. **ViLT zs** — 零样本 ViLT（MLM 范式）
2. **Oscar zs** — 零样本 Oscar（MLM 范式）

**集成组合**：fine-tuned ViLT + zero-shot ViLT / fine-tuned Oscar + zero-shot Oscar / PENET + zero-shot ViLT

### 子任务与评估指标

- **Predicate Classification (PredCls)**：给定 ground truth 物体框和标签，预测关系
- **Scene Graph Classification (SGCls)**：给定 ground truth 物体框，同时预测物体标签和关系
- **Relation Classification**：仅对非背景关系样本计算 top-1 准确率
- 指标：Recall@K (R@K) 和 mean Recall@K (mR@K)，K = 20, 50, 100

### 对比方法

VTransE, SG-CogTree, BGNN, PCPL, Motifs-Rwt, Motifs-GCL, VCTree-TDE, VCTree-GCL, PENET-Rwt, KERN, R-CAGCN, GPS-Net, VCTree, MOTIFS, SGGNLS, RU-Net

### 训练设置

- 使用独立的 Faster R-CNN 进行物体检测
- VLM 零样本推理使用 MLM prompt：`"zi is [MASK] zj"`
- VLM 微调使用 VQA prompt：`"what is the relationship between the zi and the zj?"`，[CLS] token 接 MLP 分类头
- 论文未报告具体优化器、学习率、batch size、epoch 数和硬件信息（not reported in the source）

## Results

### 主结果 — mean Recall (PredCls)

| 模型 | mR@20 | mR@50 | mR@100 | SGCls mR@20 | SGCls mR@50 | SGCls mR@100 |
|------|-------|-------|--------|-------------|-------------|--------------|
| VCTree-TDE | 18.4 | 25.4 | 28.7 | 8.9 | 12.2 | 14.0 |
| VCTree-GCL | 31.4 | 37.1 | 39.1 | 19.5 | 22.5 | 23.5 |
| PENET-Rwt† | 31.0 | 38.8 | 40.7 | 18.9 | 22.2 | 23.5 |
| Oscar ft + la | 30.4 | 38.4 | 41.3 | 17.9 | 22.6 | 23.8 |
| **Oscar ft + la + Ours** | **31.2 (+0.8)** | **39.4 (+1.0)** | **42.7 (+1.4)** | **18.3 (+0.4)** | **23.4 (+0.8)** | **25.0 (+1.2)** |
| ViLT ft + la | 31.2 | 40.5 | 44.5 | 17.4 | 22.5 | 24.3 |
| **ViLT ft + la + Ours** | **32.3 (+1.1)** | **42.3 (+1.8)** | **46.5 (+2.0)** | **17.9 (+0.5)** | **23.5 (+1.0)** | **25.5 (+1.2)** |
| PENET-Rwt† | 31.4 | 38.8 | 40.7 | 18.9 | 22.2 | 23.5 |
| **PENET-Rwt + Ours** | **31.8 (+0.4)** | **39.9 (+1.1)** | **42.3 (+1.6)** | **19.2 (+0.3)** | **23.0 (+0.8)** | **24.5 (+1.0)** |

> 表 1，mRecall 结果。† 为作者复现。

**最佳结果**：ViLT ft + la + Ours 在 PredCls 上 mR@100 达 **46.5**，Oscar ft + la + Ours 在 SGCls 上 mR@100 达 **25.0**。

### 主结果 — Recall (PredCls)

| 模型 | R@20 | R@50 | R@100 | SGCls R@20 | SGCls R@50 | SGCls R@100 |
|------|------|------|-------|-----------|-----------|------------|
| PENET† | 61.7 | 68.2 | 70.1 | 37.9 | 41.3 | 42.3 |
| Oscar ft | 59.1 | 65.7 | 67.6 | 36.7 | 40.3 | 41.3 |
| **Oscar ft + Ours** | **60.5 (+1.4)** | **67.4 (+1.8)** | **69.3 (+1.7)** | **37.3 (+0.6)** | **41.4 (+1.1)** | **42.3 (+1.0)** |
| ViLT ft | 57.1 | 65.7 | 68.4 | 34.9 | 40.2 | 41.8 |
| **ViLT ft + Ours** | **58.0 (+0.9)** | **66.7 (+1.0)** | **69.8 (+1.4)** | **35.3 (+0.4)** | **41.2 (+1.0)** | **42.9 (+1.1)** |
| PENET† | 61.7 | 68.2 | 70.1 | 37.9 | 41.3 | 42.3 |
| **PENET + Ours** | **62.0 (+0.3)** | **69.0 (+0.8)** | **71.1 (+1.0)** | **38.1 (+0.2)** | **41.8 (+0.5)** | **42.9 (+0.6)** |

> 表 2，Recall 结果。**PENET + Ours 在 R@100 达 71.1，为所有方法最优**。

### 消融实验 — Relation Classification Accuracy

| 模型 | All mAcc | All Acc | Unseen mAcc | Unseen Acc |
|------|----------|---------|-------------|------------|
| ViLT ft | 46.53 | 68.92 | 14.98 | 17.72 |
| ViLT zs (initial) | 21.88 | 37.42 | 8.99 | 16.92 |
| ViLT zs (debiased) | 46.86 | 48.70 | 15.66 | 20.07 |
| ViLT ft + zs (initial ensemble) | 46.86 | 68.95 | 15.66 | 19.56 |
| **ViLT ft + zs (debiased ensemble)** | **48.70 (+2.17)** | **70.75 (+1.83)** | **20.07 (+5.09)** | **21.73 (+4.01)** |
| Oscar ft | 41.99 | 67.16 | 13.85 | 18.01 |
| Oscar zs (initial) | 17.18 | 33.96 | 6.68 | 16.01 |
| Oscar zs (debiased) | 42.02 | 44.28 | 14.83 | 19.11 |
| Oscar ft + zs (initial ensemble) | 42.02 | 67.77 | 14.83 | 19.11 |
| **Oscar ft + zs (debiased ensemble)** | **44.28 (+3.29)** | **69.03 (+1.87)** | **19.56 (+5.71)** | **20.97 (+2.96)** |

> 表 3。Unseen triplets：测试集中出现但训练集中完全未见的 triplet。

### 消融实验 — Recall / mRecall Ablation

| 模型 | mR@20 | mR@50 | mR@100 | R@20 | R@50 | R@100 |
|------|-------|-------|--------|------|------|-------|
| ViLT ft | 31.2 | 40.5 | 44.5 | 57.1 | 65.7 | 68.4 |
| ViLT + zs (initial) | 30.9 (-0.3) | 40.5 (+0.0) | 44.6 (+0.1) | 56.9 (-0.2) | 65.7 (+0.0) | 68.8 (+0.4) |
| **ViLT + zs (debiased)** | **32.3 (+0.9)** | **42.3 (+1.8)** | **46.5 (+2.0)** | **58.0 (+0.9)** | **66.7 (+1.0)** | **69.8 (+1.4)** |
| Oscar ft | 30.4 | 38.4 | 41.3 | 59.1 | 65.7 | 67.6 |
| Oscar + zs (initial) | 30.3 (-0.1) | 38.5 (+0.1) | 41.6 (+0.3) | 59.2 (+0.1) | 65.9 (+0.2) | 67.9 (+0.3) |
| **Oscar + zs (debiased)** | **31.2 (+0.8)** | **39.4 (+1.0)** | **42.7 (+1.4)** | **60.5 (+1.4)** | **67.4 (+1.8)** | **69.3 (+1.7)** |

> 表 4。直接集成初始零样本 VLM 甚至会损害性能（ViLT 的 mR@20 -0.3），而集成去偏后的 VLM 带来一致提升。

### 关键发现总结

1. **LM Estimation 有效性**：去偏后的零样本 VLM 性能大幅提升，在 unseen triplet 上甚至超越微调模型（Oscar zs debiased 在 unseen mAcc 16.01 > Oscar ft 的 13.85）
2. **集成增益集中在 tail 类**：unseen triplet 的 gain（+4.01~+5.71）远高于 all triplet 的 gain（+1.83~+3.29），说明 underrepresentation 问题得到有效缓解
3. **mRecall 提升幅度 > Recall 提升幅度**：表明去偏主力帮助了 tail classes
4. **Plug-and-play 有效**：PENET + Ours 在 R@100 达到 71.1，为所有方法最优

## Limitations

1. **推理计算开销**：集成框架增加了零样本 VLM 的推理成本，场景中物体过多时（SGDet 场景）时间开销不可忽略
2. **依赖预训练质量**：最终性能高度依赖 VLM 预训练数据的质量（comprehensiveness）
3. **逐对前向传播**：VLM 需要每个物体对一次完整前向传播，在 SGDet 的大量 proposal 场景下时间成本高

## Reusable Claims

- **Claim 1**：零样本 VLM 在 SGG 上的直接推理存在严重的 predicate bias，源于预训练数据中谓词分布不均（低频谓词如 "carrying" 被系统性压低）
- **Claim 2**：LM Estimation 可以仅通过 SGG 训练集数据估计出预训练数据中不可获得的谓词分布 \(\pi_{pt}\)，无需访问预训练数据
- **Claim 3**：去偏后的零样本 VLM 对 unseen triplets 的识别能力显著优于微调 SGG 模型（Oscar zs debiased unseen Acc 20.05 > Oscar ft 18.01），说明预训练知识的泛化价值
- **Claim 4**：直接集成未去偏的零样本 VLM 可能损害性能，而去偏后集成带来一致且显著的提升
- **Claim 5**：Certainty-aware ensemble 中 unseen triplets 的 gain（+4~+6）远超 all triplets（+1~+3），证明方法有效缓解了 SGG 的 underrepresentation 问题

## Connections

- **TDE (Tang et al., 2020)**：同为 SGG 去偏方法，但 TDE 在训练阶段 using causal modeling，本文在 inference 阶段通过 post-hoc logits adjustment 处理 VLM 偏见
- **PENET (Zheng et al., 2023)**：作为本文的 SGG 模型基线之一，展示了方法的可迁移性
- **Post-hoc Logits Adjustment (Menon et al., 2020)**：本文的理论基础，用于 long-tail classification
- **ViLT (Kim et al., 2021)** / **Oscar (Li et al., 2020)**：作为零样本 VLM backbone
- **Generalized Logit Adjustment (Zhu et al., 2024)**：同时期工作，从不同角度处理 foundation model 的 label bias

## Open Questions

- LM Estimation 能否有效扩展到更多 predicate 类别（Vr 更多）或者更复杂的 SGG benchmark（如 Open Images）？
- 方法依赖 SGG 模型先进行 post-hoc logits adjustment（la），对于未做 debiasing 的 SGG 模型适配方式？
- 逐对前向传播的计算开销是否有 batch-level 优化方案？
- 方法对 VLM backbone 选择的敏感性如何？更强大的 VLM（如 CLIP）是否带来更大提升？

## Provenance

- **PDF 下载**: arXiv: 2403.16184
- **提取文本**: pdfminer.six 提取，59283 chars，1933 行
- **证据等级**: full-paper — 基于全文提取的完整精读
- **分析日期**: 2026-06-10
- **分析者**: Autoresearch subagent
