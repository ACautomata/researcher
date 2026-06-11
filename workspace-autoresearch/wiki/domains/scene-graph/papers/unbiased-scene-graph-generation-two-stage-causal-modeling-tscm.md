---
title: "Unbiased Scene Graph Generation via Two-stage Causal Modeling"
type: paper
domain: scene-graph
status: active
created: 2026-06-10
updated: 2026-06-10
tags:
  - scene-graph-generation
  - causal-inference
  - debiasing
  - long-tail
  - semantic-confusion
  - TPAMI-2023
  - TsCM
  - sparse-mechanism-shift
raw_sources:
  - ../../../raw/sources/2023-07-11-unbiased-scene-graph-generation-via-two-stage-causal-modeling.pdf
  - ../../../raw/sources/2023-07-11-unbiased-scene-graph-generation-via-two-stage-causal-modeling.txt
related_pages:
  - unbiased-scene-graph-generation-tde-causal-modeling.md
  - camodule-causal-adjustment-module-debiasing-scene-graph-generation.md
  - eicr-environment-invariant-curriculum-relation-learning-sgg.md
  - compositional-feature-augmentation-for-unbiased-scene-graph-generation.md
evidence_level: full-paper
paper:
  title: "Unbiased Scene Graph Generation via Two-stage Causal Modeling"
  authors:
    - Shuzhou Sun
    - Shuaifeng Zhi
    - Qing Liao
    - Janne Heikkilä
    - Li Liu
  year: 2023
  venue: "IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI), 2023"
  arxiv: "2307.05276"
  doi: "10.1109/TPAMI.2023.3285009"
  code: null
  project: null
classification:
  label: "TsCM — Two-stage Causal Modeling for Unbiased Scene Graph Generation"
  task:
    - Scene Graph Generation (SGG)
    - Predicate Classification (PredCls)
    - Scene Graph Classification (SGCls)
    - Scene Graph Detection (SGDet)
  method_family:
    - Causal Inference
    - Two-stage Causal Modeling (TsCM)
    - Population Loss (P-Loss)
    - Adaptive Logit Adjustment (AL-Adjustment)
  modality:
    - Visual features (Faster R-CNN ResNeXt-101-FPN)
    - GloVe word embeddings
    - Union box features
  datasets:
    - Visual Genome VG150
  metrics:
    - mean Recall@K (mR@K)
    - Recall@K (R@K)
    - Mean of R@K and mR@K (MR@K)
---

# Unbiased Scene Graph Generation via Two-stage Causal Modeling

> Shuzhou Sun, Shuaifeng Zhi, Qing Liao, Janne Heikkilä, Li Liu. "Unbiased Scene Graph Generation via Two-stage Causal Modeling." *IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI)*, 2023.

## One-Sentence Contribution

提出 **Two-stage Causal Modeling (TsCM)** 框架，首次将 SGG 中的双重偏置（长尾分布偏置和语义混淆偏置）建模为因果图中的混杂因子，通过两阶段解耦因果干预实现无偏场景图生成，在保持头部谓词性能的同时显著提升尾部谓词预测精度。

## Problem Setting

SGG 旨在从图像中提取 `<subject, predicate, object>` 三元组。当前去偏方法主要关注长尾分布问题，但忽略了另一重要偏置来源——**语义混淆（semantic confusion）**，即语义相似的关系（如 carrying vs. holding）之间的误判。

论文实验验证（Fig. 1(c)）：MotifsNet 在尾部关系的 FP（False Predictions）中，绝大多数发生在**尾部相似关系**上（而非尾部不相似关系），证明语义混淆是一个独立于长尾分布的重要偏置源。

核心挑战：
1. **长尾分布偏置**：部分高频关系（on=34.8%, has=13.6%）主导预测，尾部关系（standing on=0.7%, carrying=0.3%）被系统性抑制
2. **语义混淆偏置**：相似语义关系之间的决策边界模糊，导致误判
3. **因果不充分性（causal-insufficient）**：SGG 数据集的嘈杂特性导致部分混杂因子不可观测，使得构建的结构因果模型（SCM）无法直接受益于稀疏机制转移（SMS）[38, 39]

## Method

### 因果图（Structural Causal Model）

论文构建含两个混杂因子的 SCM：

```
      S (语义混淆)     L (长尾分布)
       ↙               ↙
X → Z → Y (谓词预测)
```

- **X**：输入图像
- **Z**：上下文变量（目标检测特征 + 空间配置）
- **S**：语义混淆混杂因子（使相似关系在表示空间中靠近）
- **L**：长尾分布混杂因子（使头部关系主导预测）
- **Y**：谓词分类输出

由于 SGG 数据集的嘈杂性，构建的 SCM 是 **causal-insufficient**（部分混杂因子不可观测），导致变量纠缠，无法直接应用 SMS。

### 两阶段解耦干预

#### 阶段 1：因果表示学习 — Population Loss (P-Loss)

**核心洞察**：语义相似的关系在特征空间中天然具有**稀疏性**，即每个关系只与少数关系语义相近。

**Population 定义**：对每个关系类别 $c$，定义其 population $P_\alpha(c)$ 为与该关系特征距离最近的 $\alpha$ 个关系类别。

**P-Loss 公式**：

$$
\hat{\ell}(x, y) = \ell(x, y) + \lambda \sum_{c' \in P_\alpha(y)} \max(0, f_{\theta,y}(x) - f_{\theta,c'}(x) + m)
$$

其中 $\ell(x, y)$ 是标准交叉熵损失，第二项拉大相似关系之间的 logit 差距，$m$ 是 margin。

**效果**：
- 增加相似关系之间的预测差距，使决策边界更清晰
- 利用关系类别的稀疏性实现稀疏干预（只扰动语义相似的关系）
- 产生解耦的因子分解（disentangled factorization），为阶段 2 铺垫

#### 阶段 2：因果校准学习 — Adaptive Logit Adjustment (AL-Adjustment)

**前提**：阶段 1 获得解耦因子分解后，$L$（长尾混杂因子）与 $S$ 解耦，可以独立干预。

**核心操作**：
1. **Logit 增强（Logit Augmentation）**：将分类 logits 乘以背景网络的 logits $f^{\text{bg}}_{\theta^*,y}(x)$，使 logits 统一为正值且更具判别性
2. **自适应因子学习**：从数据中学习一组稀疏、独立的调整因子 $\Delta_y$，对每个类别的 logit 进行校准：

$$
\hat{f}_{\theta^*,y}(x) = \tilde{f}_{\theta^*,y}(x) + \beta \cdot \Delta_y
$$

其中 $\tilde{f}$ 是增强后的 logits，$\beta$ 控制调整强度（默认 $\beta=3$）

**效果**：
- 提升尾部关系的 logits 以抵消长尾分布偏置
- 不扰动头部关系（因为调整因子稀疏且独立）
- 将 less informative 的预测（如 `<bear, on, chair>`）调整为 high-informative 预测（如 `<bear, standing on, chair>`）

### 模型无关性

两阶段均与 backbone 无关，可应用于任何 SGG 模型（MotifsNet、VCTree、Transformer）。

## Experiments

### 数据集

- **VG150**：Visual Genome 子集，包含 150 个目标类别和 50 个关系类别
- 约 94k 张图像，按 [14] 的分割：62k 训练 / 5k 验证 / 26k 测试

### Backbones

- MotifsNet [9]（RNN-based）
- VCTree [11]（动态树结构）
- Transformer [67]（纯注意力架构）

### Baselines

分为四类：
- **Resampling**：SegG [19], TransRwt [20]
- **Reweighting**：CogTree [21], EBM-loss [15], Loss-reweight [44], FGPL [30], GCL [16], PPDL [17], LS-KD(Iter) [32]
- **Adjustment**：TDE [14], DLFE [24], Logit-reweight [44], PKO [25]
- **Hybrid**：BPL+SA [27], HML [28], RTPB [29], NICE [31], CAME [33]

### 评估协议

- 三个子任务：PredCls, SGCls, SGDet
- 三个指标：R@K, mR@K, MR@K（K=20, 50, 100）
- **MR@K** = avg(AVGmR, AVGR)，综合衡量头部-尾部性能平衡

### 训练设置

- 目标检测器：Faster R-CNN with ResNeXt-101-FPN，VG 训练集上预训练（28.14 mAP）
- 检测器冻结，仅训练关系分类器
- 优化器：SGD
- MotifsNet/VCTree：batch size=12, lr=0.01
- Transformer：batch size=16, lr=0.001
- P-Loss 超参数 $\alpha=5$（默认）
- AL-Adjustment 超参数 $\beta=3$（默认）

## Results

### Main mR@K Results

#### MotifsNet Backbone（Table 1）

| Method | PredCls mR@20/50/100 | AVGmR | SGCls mR@20/50/100 | AVGmR | SGDet mR@20/50/100 | AVGmR |
|--------|----------------------|-------|--------------------|-------|--------------------|-------|
| MotifsNet (baseline) | 12.2 / 15.5 / 16.8 | 14.8 | 7.2 / 9.0 / 9.5 | 8.6 | 5.2 / 7.2 / 8.5 | 7.0 |
| TDE (CVPR'20) | 18.5 / 25.5 / 29.1 | 24.4 | 9.8 / 13.1 / 14.9 | 12.6 | 5.8 / 8.2 / 9.8 | 7.9 |
| Loss-reweight (ICLR'21) | 26.5 / 32.9 / 35.3 | 31.6 | 13.8 / 17.4 / 19.3 | 16.8 | 9.2 / 12.8 / 16.5 | 12.8 |
| HML (ECCV'22) | 30.1 / 36.3 / 38.7 | 35.0 | 17.1 / 20.8 / 22.1 | 20.0 | 10.8 / 14.6 / 17.3 | 14.2 |
| GCL (CVPR'22) | 30.5 / 36.1 / 38.2 | 34.9 | 18.0 / 20.8 / 21.8 | 20.2 | 12.9 / 16.8 / 19.3 | 16.3 |
| **TsCM** | **31.8 / 37.8 / 40.9** | **36.8** | **18.7 / 22.4 / 23.8** | **21.6** | **13.7 / 17.4 / 19.7** | **16.9** |

#### VCTree Backbone（Table 2）

| Method | PredCls mR@20/50/100 | AVGmR | SGCls mR@20/50/100 | AVGmR | SGDet mR@20/50/100 | AVGmR |
|--------|----------------------|-------|--------------------|-------|--------------------|-------|
| VCTree (baseline) | 12.4 / 15.4 / 16.6 | 14.8 | 6.3 / 7.5 / 8.0 | 7.3 | 4.9 / 6.6 / 7.7 | 6.4 |
| TDE (CVPR'20) | 18.4 / 25.4 / 28.7 | 24.2 | 8.9 / 12.2 / 14.0 | 11.7 | 6.9 / 9.3 / 11.1 | 9.1 |
| HML (ECCV'22) | 31.0 / 36.9 / 39.2 | 35.7 | 20.5 / 25.0 / 26.8 | 24.1 | 10.1 / 13.7 / 16.3 | 13.4 |
| FGPL (CVPR'22) | 30.8 / 37.5 / 40.2 | 36.2 | 21.9 / 26.2 / 27.6 | 25.2 | 11.9 / 16.2 / 19.1 | 15.7 |
| **TsCM** | **32.3 / 38.7 / 41.5** | **37.5** | **23.4 / 26.9 / 28.9** | **26.4** | **12.5 / 16.9 / 19.3** | **16.2** |

#### Transformer Backbone（Table 3）

| Method | PredCls mR@20/50/100 | AVGmR | SGCls mR@20/50/100 | AVGmR | SGDet mR@20/50/100 | AVGmR |
|--------|----------------------|-------|--------------------|-------|--------------------|-------|
| Transformer (baseline) | 12.4 / 16.0 / 17.5 | 15.3 | 7.7 / 9.6 / 10.2 | 9.2 | 5.3 / 7.3 / 8.8 | 7.1 |
| Loss-reweight (ICLR'21) | 27.8 / 33.1 / 36.2 | 32.4 | 15.8 / 19.3 / 21.1 | 18.8 | 11.7 / 15.3 / 17.9 | 15.0 |
| HML (ECCV'22) | 30.1 / 36.3 / 38.7 | 35.0 | 17.1 / 20.8 / 22.1 | 20.0 | 10.8 / 14.6 / 17.3 | 14.2 |
| **TsCM** | **32.8 / 40.1 / 42.3** | **38.4** | **19.6 / 23.7 / 25.1** | **22.8** | **13.8 / 18.3 / 21.2** | **17.8** |

### R@K and MR@K Results（Table 4, Table 5）

**MR@K 综合表现**（MotifsNet PredCls）：
- MotifsNet baseline: 39.7
- TDE: 34.1
- Logit-reweight: 37.3
- **TsCM: 46.1**（最佳，比 baseline 高 6.4）

**关键数字**：
- MotifsNet PredCls mR@100: **40.9**（SOTA，比 baseline 16.8 提升 +143%，比最强 baseline HML 38.7 提升 +5.7%）
- MotifsNet PredCls R@100: 59.5（低于 baseline 67.9 但远高于其他去偏方法如 TDE 51.4）
- MotifsNet PredCls MR@100: **46.1**（最佳头部-尾部平衡）

### 消融研究

#### 两阶段贡献（Table 6）

| Setting | PredCls mR@20/50/100 (MotifsNet) |
|---------|----------------------------------|
| Baseline | 12.2 / 15.5 / 16.8 |
| +P-Loss only | 12.9 / 16.9 / 20.1 |
| +AL-Adjustment only | 24.4 / 30.7 / 33.3 |
| **+P-Loss + AL-Adjustment** | **31.8 / 37.8 / 40.9** |

**关键发现**：
- AL-Adjustment 单独使用即可大幅提升 mR@K（16.8→33.3 on PredCls）
- P-Loss 单独使用提升有限（16.8→20.1），但其目的是获取因果表示
- **两者联合使用效果远大于单独累加**（33.3→40.9），证明 P-Loss 的解耦作用显著增强了 AL-Adjustment 的效果
- VCTree 上，AL-Adjustment + P-Loss 较 AL-Adjustment 单独提升 8.4~8.7%

#### Logit 增强消融（Table 7）

PredCls mR@100:
- 无增强: 37.4
- $e^{f} \times 1$: 39.7
- $e^{f} \times f^{\text{bg}}$: **40.9**（最佳）

#### 损失函数对比（Table 9）：验证解耦性

仅 P-Loss（干预相似关系）能显著改变模型行为，而干预不相似关系（$\hat{\ell}^{\triangleright}$）或不相似尾部关系（$\hat{\ell}^{\triangleleft}$）影响极小，证明 P-Loss 实现的是**稀疏干预**。

### 超参数分析（Fig. 8）

- $\alpha=5$ 最优（$\alpha$ 太小遗漏相似关系，太大引入不相似关系）
- $\beta \in [1,3]$ 最优（$\beta > 3$ 导致调整因子过拟合）

## Limitations

1. **仅处理可观测偏置**：SCM 的 causal-insufficient 假设意味着仍有不可观测的混杂因子未被建模（论文在结论中明确承认此局限性）
2. **P-Loss 需要 $\alpha$ 超参数调优**：$\alpha$ 值依赖于关系类别数（VG150 为 5），更换数据集可能需要重新调优
3. **P-Loss 单独提升有限**：阶段 1 主要是为阶段 2 提供解耦表示而设计，单独使用收益较小
4. **仅 VG150 评估**：未在 OpenImages、GQA 等其他 SGG 基准上验证

## Reusable Claims

- **✅ TsCM 首次将语义混淆偏置纳入 SGG 去偏框架**：实验证明 FP on tail-similar relationships 是主要的尾部分类错误来源（Fig. 1(c)）
- **✅ P-Loss 通过稀疏干预实现因果表示学习**：仅扰动语义相似的关系类别的决策边界，不干扰不相似关系，验证了解耦性（Table 9）
- **✅ AL-Adjustment 自适应校准长尾偏置**：PredCls mR@100 从 16.8 提升至 33.3（MotifsNet），证明 logit 调节策略的有效性
- **✅ 两阶段联合效果超出单独累加**：MotifsNet PredCls mR@100 上，AL-Adjustment 单独 33.3，联合 P-Loss 达 40.9（+22.8%），验证解耦因子分解的增益
- **✅ TsCM 实现更好的头部-尾部性能平衡**：MR@K 46.1 vs. baseline 39.7 vs. Logit-reweight 37.3（Table 5），在三个 backbone 上均最优
- **✅ 模型无关性**：在 MotifsNet、VCTree、Transformer 三个 backbone 上一致提升，支持即插即用

## Connections

- **[TDE](unbiased-scene-graph-generation-tde-causal-modeling.md)**：（CVPR 2020 / TPAMI 2023）TDE 通过反事实推理分离好/坏偏置，但仅处理长尾分布。TsCM 继承了因果推理思路，额外处理了语义混淆，且在 MotifsNet PredCls mR@100 上从 29.1 提升至 40.9
- **[CAModule](camodule-causal-adjustment-module-debiasing-scene-graph-generation.md)**：（2025）在 TDE 基础上进一步引入共现分布作为中介变量。与 TsCM 互补——CAModule 处理对象对分布偏置，TsCM 处理语义混淆偏置
- **[EICR](eicr-environment-invariant-curriculum-relation-learning-sgg.md)**：（ICCV 2023）从环境不变学习角度处理语境不均衡，与 TsCM 的因果干预思路互补
- **[CFA](compositional-feature-augmentation-for-unbiased-scene-graph-generation.md)**：（2023）通过组合式特征增强提升尾部谓词表示质量，互补于 TsCM 的推理阶段校准
- **Loss-reweight [44]**：（ICLR 2021）TsCM 的 P-Loss 属于重加权方法族，但 P-Loss 仅重加权语义相似的关系，而非全局重加权
- **Logit-adjustment [44]**：（ICLR 2021）TsCM 的 AL-Adjustment 属于 logit 调整族，但调整因子是自适应学习的而非基于先验频率
- **本文引用 TDE [14] 作为调整方法对比**

## Open Questions

- TsCM 在 OpenImages、GQA 等更大规模 SGG 基准上的表现如何？$\alpha$ 超参数如何随关系类别数变化？
- 不可观测的混杂因子具体有哪些？能否通过因果发现或弱监督方法自动识别？
- P-Loss 的 $\alpha$ 选择可以自适应化（如基于关系相似度阈值而非固定数量）？
- TsCM 能否推广到其他受长尾+语义混淆双重偏置影响的任务（如细粒度分类、动作识别）？
- AL-Adjustment 的自适应因子学习是否可以在训练阶段联合优化而非推理阶段单独学习？

## Provenance

- **PDF**：raw/sources/2023-07-11-unbiased-scene-graph-generation-via-two-stage-causal-modeling.pdf (6.1MB, 17 pages)
- **提取文本**：raw/sources/2023-07-11-unbiased-scene-graph-generation-via-two-stage-causal-modeling.txt (103,916 chars, 3,692 lines)
- **证据等级**：full-paper — 全文精读，涵盖方法、实验、表格和定性分析
- **入库日期**：2026-06-10
- **入库方式**：sub-agent in-context analysis（全文提取后直接分析）
- **注意**：用户标签标注为 "CVPR-2023"，实际为 TPAMI 2023 长文
