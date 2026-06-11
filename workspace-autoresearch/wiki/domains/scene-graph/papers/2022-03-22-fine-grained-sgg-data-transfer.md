---
title: "Fine-Grained Scene Graph Generation with Data Transfer (IETrans)"
type: paper
domain: scene-graph
status: active
created: 2026-06-10
updated: 2026-06-10
tags: [scene-graph-generation, fine-grained, data-transfer, long-tail, semantic-ambiguity, ECCV-2022]
source_pages: []
raw_sources:
  - raw/sources/2022-03-22-fine-grained-sgg-data-transfer.pdf
  - raw/sources/2022-03-22-fine-grained-sgg-data-transfer.txt
related_pages:
  - domains/scene-graph/papers/neural-motifs-scene-graph-global-context.md
  - domains/scene-graph/papers/vctree-learning-to-compose-dynamic-tree-structures.md
  - domains/scene-graph/papers/unbiased-scene-graph-generation-tde-causal-modeling.md
  - domains/scene-graph/papers/visual-distant-supervision-scene-graph-generation.md
  - domains/scene-graph/papers/sbg-fine-grained-sgg-sample-level-bias-prediction.md
  - domains/scene-graph/papers/eicr-environment-invariant-curriculum-relation-learning-sgg.md
paper:
  title: "Fine-Grained Scene Graph Generation with Data Transfer"
  authors: ["Ao Zhang", "Yuan Yao", "Qianyu Chen", "Wei Ji", "Zhiyuan Liu", "Maosong Sun", "Tat-Seng Chua"]
  year: 2022
  venue: ECCV 2022
  arxiv: "2203.11654"
  doi: null
  code: "https://github.com/waxnkw/IETrans-SGG.pytorch"
classification:
  label: fine-grained-sgg, data-transfer, IETrans
  task: [Scene Graph Generation, Unbiased SGG, Fine-Grained SGG, Large-Scale SGG]
  method_family: Data Augmentation, Data Transfer, Plug-and-Play
  modality: Image
  datasets: [Visual Genome (VG-50), Visual Genome (VG-1800)]
  metrics: [Recall@K (R@K), mean Recall@K (mR@K), F@K, Accuracy (Acc), mean Accuracy (mAcc), F-Acc, Non-Zero]
evidence_level: full-paper
---

## Citation

Ao Zhang, Yuan Yao, Qianyu Chen, Wei Ji, Zhiyuan Liu, Maosong Sun, Tat-Seng Chua. "Fine-Grained Scene Graph Generation with Data Transfer." ECCV 2022.

## One-Sentence Contribution

提出 IETrans（Internal and External Data Transfer）框架，通过自动增强数据集来同时缓解 SGG 中的长尾分布和语义歧义问题，在 VG-50 上使 Motif 模型 mR@100 翻倍，并在新提出的 VG-1800（1807 类谓词）大规模基准上显著超越所有基线。

## Problem Setting

**任务**：给定图像 I，生成场景图 G = {O, E}，其中 O = {(bᵢ, cᵢ)} 为物体集合（含边界框和类别），E = {(sᵢ, p(sᵢ,oᵢ), oᵢ)} 为关系三元组集合。

**两大核心问题**：
1. **长尾分布（Long-tail Problem）**：Visual Genome 中 top-5 谓词类有超过 10 万样本，而 90%+ 的谓词类样本不到 10 个。
2. **语义歧义（Semantic Ambiguity）**：同一对实体可同时被标注为通用谓词（如 on）和信息型谓词（如 riding），标注者偏好通用类，导致单标签优化冲突。

**核心洞察**：问题可通过增强数据集本身来缓解——提供更多尾部类训练样本，并提供不同类间一致标注。之前的重采样、重加权、后处理方法都是 predicated-level 调整，而关系本质上是 triplet-level的。

## Method

提出 **IETrans**（Internal and External Data Transfer）框架，两部分正交可合并，以 plug-and-play 方式应用于任意 SGG 基线模型。

### Internal Data Transfer（内部迁移）

将通用谓词标注迁移为信息型谓词标注。分为三步：

1. **Confusion Pair Discovery（混淆对发现）**：用预训练基线的预测混淆矩阵，找出三元组类别 (cₛ, p, cₒ) 中被混淆的谓词类作为候选迁移源 Pc。
2. **Transfer Pair Judgement（迁移对判定）**：根据吸引因子（Attraction Factor）筛选真正的通用谓词。吸引因子定义为：
   A(cₛ, p, cₒ) = N(cₛ, p, cₒ) / Σ_{cᵢ, cⱼ∈C} 𝕀(cᵢ, p, cⱼ) · N(cᵢ, p, cⱼ)
   分母为该谓词覆盖的三元组类型数，分母越大（A 越小）→ p 越可能是通用谓词。当 A(cₛ, pᵢ, cₒ) < A(cₛ, p, cₒ) 时，从 pᵢ 迁移到 p。
3. **Triplet Transfer（三元组迁移）**：收集被选为源的三元组实例，按目标谓词预测分数降序排列，取 top kI% 迁移。

### External Data Transfer（外部迁移）

对 NA（未标注/假阴性）样本进行重新标注：

1. **NA Relabeling**：仅考虑边界框有重叠的物体对，候选目标谓词限于训练集中存在的三元组类型。取最高预测分数（除 NA 外）的谓词类。
2. **NA Triplet Transfer**：按 NA 分数升序排列（越低越可能是漏标正样本），取 top kE% 迁移。

### Integration

两部分在数据上不冲突，可直接合并。使用增强数据集重新从头训练模型。

## Experiments

### 数据集

**VG-50**[31]（标准基准）
- 50 个谓词类，150 个物体类
- 广泛用于 SGG 评估

**VG-1800**（本文新提出）
- 1,807 个谓词类，70,098 个物体类
- 手动清理拼写错误和不合理关系
- 所有 1,807 类在训练集和测试集均出现，测试集每类 ≥5 样本
- 旨在提供更可靠的大规模 SGG 评估

### 任务

三种标准 SGG 任务：
1. **Predicate Classification (PREDCLS)**：给定真值定位和物体类别，预测谓词
2. **Scene Graph Classification (SGCLS)**：给定真值定位，预测物体和谓词类别
3. **Scene Graph Detection (SGDET)**：端到端检测边界框、物体、谓词

### 评估指标

- **Recall@K (R@K)**：标准召回率
- **mean Recall@K (mR@K)**：各类召回率均值（关注尾部性能）
- **F@K**：本文提出的 R@K 和 mR@K 的调和平均，用于整体评估
- 大规模 SGG：**Acc**（准确率）、**mAcc**（各类平均准确率）、**F-Acc**（调和平均）、**Non-Zero**（至少一个正确预测的谓词类数）

### Baseline 方法

**Model-Agnostic baselines**（可 plug-and-play 应用）：
- Resampling [13], TDE [23], CogTree [37], EBM [22], DeC [9], DLFE [5], RelMix [1]

**Specific models**：
- KERN [4], GBNet [38], BGNN [13], DT2-ACBS [6], PCPL [32]

**Baseline SGG models**（IETrans 应用的目标模型）：
- Motif [39], VCTree [24], GPS-Net [18], Transformer [23]

### 训练设置

- **Backbone**：预训练 Faster R-CNN 带 ResNeXt-101-FPN
- **Detector**：参数固定以降低计算成本
- **Batch size**：12
- **Learning rate**：0.12（Transformer 除外）
- **Optimizer**：SGD
- **Internal transfer**：kI = 70%（VG-50）
- **External transfer**：kE = 100%（所有 NA 样本重新标注；VG-50 中 top-15 高频谓词类不做外部迁移）
- **Inference**：应用原始数据集的频率偏置项

## Results

### VG-50 — 可迁移性与总体性能

**Table 1 关键结果**（Predicate Classification 任务）：

| 模型 | R@50 | R@100 | mR@50 | mR@100 | F@50 | F@100 |
|------|------|-------|-------|--------|------|-------|
| Motif [39] | 64.0 | 66.0 | 15.2 | 16.2 | 24.6 | 26.0 |
| Motif+IETrans (ours) | 54.7 | 56.7 | 30.9 | 33.6 | 39.5 | 42.2 |
| Motif+IETrans+Rwt (ours) | 48.6 | 50.5 | **35.8** | **39.1** | **41.2** | **44.1** |
| VCTree [24] | 64.5 | 66.5 | 16.3 | 17.7 | 26.0 | 28.0 |
| VCTree+IETrans (ours) | 53.0 | 55.0 | 30.3 | 33.9 | 38.6 | 41.9 |
| VCTree+IETrans+Rwt (ours) | 48.0 | 49.9 | **37.0** | **39.7** | **41.8** | **44.2** |
| GPS-Net [18] | 65.1 | 66.9 | 15.0 | 16.0 | 24.4 | 25.8 |
| GPS-Net+IETrans (ours) | 52.3 | 54.3 | 31.0 | 34.5 | 38.9 | **42.2** |
| Transformer [23] | 63.6 | 65.7 | 17.9 | 19.6 | 27.9 | 30.2 |
| Transformer+IETrans (ours) | 51.8 | 53.8 | 30.8 | 34.7 | 38.6 | **42.2** |

**关键发现**：
- IETrans 在所有 4 种不同架构（CNN、TreeLSTM、Self-Attention）基线上均能显著提升 mR@K（Motif 上 mR@100 从 16.2% 翻倍至 33.6%）
- IETrans 在所有 model-agnostic 方法中 R@K 和 mR@K 均最优（除 DeC 的 mR@K）
- 加 reweighting 后 IETrans+Rwt 进一步超越 DeC 在 mR@K 上的表现
- VCTree+IETrans+Rwt 在 PREDCLS 上取得最佳 F@50/100（41.8/44.2）
- Motif+IETrans+Rwt 在 SGCLS 和 SGDET 上取得最佳 F@50/100
- GPS-Net+IETrans 使 mR@50/100 翻倍，F@50/100 提升超 9 个点

### VG-1800 — 大规模 SGG

**Table 2 关键结果**（Predicate Classification）：

| 模型 | Top-1 Acc | Top-1 mAcc | Top-1 F-Acc | Top-1 Non-Zero | Top-10 Acc | Top-10 mAcc | Top-10 F-Acc | Top-10 Non-Zero |
|------|-----------|------------|-------------|----------------|------------|-------------|--------------|-----------------|
| Motif [39] | 59.63 | 0.61 | 1.21 | 47 | 89.44 | 4.37 | 8.33 | 139 |
| BGNN [13] | 61.55 | 0.59 | 1.16 | 37 | 90.07 | 3.91 | 7.50 | 139 |
| RelMix [1] | 60.16 | 0.81 | 1.60 | 65 | 89.91 | 5.17 | 9.78 | 177 |
| TDE [23] | 60.00 | 0.62 | 1.23 | 45 | 89.92 | 4.65 | 8.84 | 152 |
| IETrans (kI=10%) (ours) | 56.66 | 1.89 | 3.66 | 202 | 89.71 | 13.06 | 22.80 | 530 |
| IETrans (kI=90%) (ours) | 27.40 | **4.70** | **8.02** | **467** | 83.50 | **19.12** | **31.12** | **865** |

**关键发现**：
- IETrans 在 VG-1800 上 mAcc 大幅领先：kI=10% 时 top-10 mAcc 13.06% vs. RelMix 5.17%
- kI=90% 时 F-Acc 8.02（top-1）和 31.12（top-10），分别是第二高基线 RelMix 的 5 倍+和 3 倍+
- IETrans (kI=90%) 在 top-1 上能正确预测 467 个谓词类，而所有其他基线 < 70 类
- Focal Loss 在大规模设置下基本失效（mAcc 0.26%），说明简单尾部加权重无效

### 消融实验

- **内部迁移（InTrans） vs. 外部迁移（ExTrans）**：
  - 单独 ExTrans 几乎无法提升 mAcc（语义歧义问题抑制尾部类）
  - 单独 InTrans 显著提升 mAcc 但略降 Acc
  - 两者合并（IETrans）取得最佳权衡，mAcc 和 Acc 均大幅提升

- **kI 影响（内部迁移比例）**：
  - 随着 kI 增加，top-10 F-Acc 先升后降（在 kI=80% 达峰）
  - 大部分通用谓词可转为信息型，但部分无法被正确转换

- **kE 影响（外部迁移比例）**：
  - 前 90% 数据提升缓慢，最后 10%（模型最确信为真负例的数据）提升显著
  - 说明模型容易将尾部类误判为负样本，而这部分数据对改善信息型预测至关重要

### 定性分析

- IETrans 在 VG-50 上生成的关系更准确（如 "(foot, belonging to, bear)" 优于 Motif 的 "(foot, of, bear)"）
- VG-1800 上准确率下降，反映大规模数据迁移的挑战性

## Limitations

1. 在 VG-1800 上数据迁移的精确度不如 VG-50，部分迁移结果不合理
2. 外部迁移限于有边界框重叠的物体对，且迁移目标限于已有三元组类型（不考虑 zero-shot 谓词）
3. 吸引因子仅基于训练集内信息，未利用外部知识库（如 WordNet、VerbNet）
4. 依赖预训练基线模型的预测质量来发现混淆对，可能引入传播误差
5. kI 和 kE 需要在验证集上调参，不同设置下 Acc/mAcc 权衡差异大

## Reusable Claims

> **Claim**: 数据集增强（data transfer）比 predicated-level 调整更适合处理 SGG 的长尾和语义歧义问题，因为关系本质是 triplet-level 的。
> **Evidence**: VG-50 上 IETrans 使所有 4 种基线模型的 mR@K 翻倍，F@K 提升 9+ 点。VG-1800 上 Non-Zero 达 467 vs. 基线 < 70。
> **Scope**: VG-50, VG-1800, PREDCLS/SGCLS/SGDET 任务
> **Confidence**: high

> **Claim**: 通用谓词比信息型谓词覆盖更多类型的三元组（更高的吸引因子分母），这是识别通用谓词的有效特征。
> **Evidence**: 基于此观察设计的吸引因子成功筛选了有效的通用→信息型迁移对，消融实验验证了内部迁移的必要性。
> **Scope**: VG 数据集、Motif/VCTree/GPS-Net/Transformer 基线
> **Confidence**: medium

> **Claim**: 被模型误判为 NA（负例）的样本中包含了大量尾部类正样本，重新标注这些数据对提升信息型预测至关重要。
> **Evidence**: 外部迁移消融实验：按 NA 分数排序，最后 10%（模型最确信为负例）的数据迁移后提升最显著。
> **Scope**: VG 数据集
> **Confidence**: medium

## Connections

- **与 Motif [39] 的关系**：Motif 是主要应用基线，IETrans 使其 mR@100 从 16.2% 翻倍至 33.6%
- **与 TDE [23] 的关系**：TDE 是后处理去偏方法，IETrans 是数据增强方法，二者可结合（IETrans+Rwt 进一步超越 TDE）
- **与 Visual Distant Supervision (VDS) [35] 的关系**：外部迁移受 VDS 启发，但 VDS 受语义歧义限制，IETrans 通过内部迁移解决此问题
- **与 RelMix [1] 的关系**：RelMix 是专为大规模 SGG 设计的特征混叠方法，IETrans 在 VG-1800 上 F-Acc 超出 RelMix 3 倍+
- **与 CogTree [37] 的关系**：CogTree 利用谓词间语义关系设计损失函数，IETrans 采用 triplet-level 数据迁移而非 predicate-level 调整
- **与 EICR 的关系**：同样是处理细粒度 SGG 的方法，EICR 关注环境不变性，IETrans 关注数据增强
- **与 SBG 的关系**：SBG 也是处理细粒度 SGG 样本级偏置的方法

## Open Questions

1. 如何将 IETrans 扩展到其他视觉识别任务（如图像分类、语义分割）？
2. 是否可以利用外部知识库（如 VerbNet）进一步提升吸引因子和迁移对的判定质量？
3. 外部迁移能否扩展至 zero-shot 谓词（训练集中不存在的新三元组类型）？
4. 如何自动确定最优的 kI/kE 而不需要人工验证集调参？
5. IETrans 在 VG-1800 上部分迁移结果不合理的根本原因是什么？如何改进？
6. IETrans 与更现代的 SGG 模型（如基于 DETR/Transformer 的 SGTR、RelTR）结合的效果如何？

## Provenance

- **原始来源**：raw/sources/2022-03-22-fine-grained-sgg-data-transfer.pdf（arXiv:2203.11654v2，ACL 2022 ECCV 接收版）
- **全文提取**：raw/sources/2022-03-22-fine-grained-sgg-data-transfer.txt（69347 字符，26 页 PDF）
- **分析类型**：全文精读（full-paper）
- **分析日期**：2026-06-10
