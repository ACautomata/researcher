---
title: "Ensemble Predicate Decoding for Unbiased Scene Graph Generation"
type: paper
domain: scene-graph
status: active
created: 2026-06-10
updated: 2026-06-10
tags:
  - scene-graph-generation
  - debiasing
  - ensemble
  - predicate-decoding
raw_sources:
  - raw/sources/2024-08-25-ensemble-predicate-decoding-unbiased-sgg.pdf
evidence_level: full-paper
paper:
  title: "Ensemble Predicate Decoding for Unbiased Scene Graph Generation"
  authors:
    - Jiasong Feng
    - Lichun Wang
    - Hongbo Xu
    - Kai Xu
    - Baocai Yin
  year: 2024
  venue: arXiv preprint
  arxiv: "2408.14187"
  code: null
classification:
  label: scene-graph-generation, debiasing, ensemble
  task:
    - Predicate Classification (PredCls)
    - Scene Graph Classification (SGCls)
    - Scene Graph Detection (SGDet)
  method_family: Ensemble Decoding
  modality: Image
  datasets:
    - Visual Genome (VG)
  metrics:
    - R@K
    - mR@K
    - Mean
---

# Ensemble Predicate Decoding for Unbiased Scene Graph Generation

## Citation

> Jiasong Feng, Lichun Wang, Hongbo Xu, Kai Xu, Baocai Yin. "Ensemble Predicate Decoding for Unbiased Scene Graph Generation." arXiv preprint arXiv:2408.14187, 2024.

## One-Sentence Contribution

提出 **Ensemble Predicate Decoding (EPD)**，通过训练三个解码器（主解码器在全量数据、两个辅助解码器分别在低频谓词子集上训练）的集成策略，在提升低频谓词预测能力的同时保持头部谓词性能，实现模型无关（model-agnostic）的无偏 Scene Graph Generation。

## Problem Setting

SGG 中存在两个互相耦合的困难：

1. **谓词长尾分布**：训练数据中高频谓词（如 on，429,891 样本）与低频谓词（如 standing on，8,768 样本）样本量差距达 50 倍。
2. **语义重叠加剧偏置**：语义相近的谓词（如 standing on 与 on）在学习到的表示中高度相似，且样本量差异巨大。现有单分类器的判别容量有限，多分类器方案（如 GCL）虽扩展了判别容量，但未针对语义相似谓词的区分做专门设计。

## Method

### 整体架构

EPD 是一个模型无关（model-agnostic）的模块，可插入现有 SGG backbone（如 Motifs、VCTree）。在谓词编码后，使用三个独立的解码器进行集成预测。

### 三个解码器的训练设置

根据谓词频率将训练样本划分为三组：

- **N1**: head 谓词样本
- **N2**: body 谓词样本
- **N3**: tail 谓词样本

三个解码器的训练数据配置：

| 解码器 | 训练子集 | 角色 |
|--------|----------|------|
| 主解码器 **M_d** | N = N1 ∪ N2 ∪ N3（全量） | 覆盖所有谓词 |
| 辅助解码器 1 **AD1** | N2 ∪ N3（body + tail） | 关注中低频谓词 |
| 辅助解码器 2 **AD2** | N3（仅 tail） | 专注极低频谓词 |

### 解码器结构

每个解码器由两个线性层（参数共享，`F_p_d`）和独立 BN 层（`B_md`, `B_ad1`, `B_ad2`）组成。共享线性层确保初始特征一致性，独立 BN 层适应不同子任务分布。

### 聚合预测

$$
z_{\text{sum}} = \lambda_{md} z_{md} + \lambda_{ad1} z_{ad1} + \lambda_{ad2} z_{ad2}
$$

权重约束：$\lambda_{md} > \lambda_{ad2} > \lambda_{ad1}$，最优设置 $(\lambda_{md}, \lambda_{ad1}, \lambda_{ad2}) = (0.5, 0.2, 0.3)$。

### 损失函数

总损失包含四项：

$$
\mathcal{L}_{all} = (1-\gamma)(\mathcal{L}_{md} + \alpha \mathcal{L}_{ad1} + \beta \mathcal{L}_{ad2}) + \gamma \mathcal{L}_{agg}
$$

- $\mathcal{L}_{md}$: 主解码器在 N 上的交叉熵
- $\mathcal{L}_{ad1}$: 辅助解码器 1 在 N2 ∪ N3 上的交叉熵
- $\mathcal{L}_{ad2}$: 辅助解码器 2 在 N3 上的交叉熵
- $\mathcal{L}_{agg}$: 聚合预测在全量 N 上的交叉熵
- 超参数：$\alpha=8, \beta=10, \gamma=0.01$（最优）

## Experiments

### 数据集

**Visual Genome (VG)**: 108,077 张图像，使用通常的设置（150 个最频繁对象类别 + 50 个谓词类别）。划分：训练集（按标准 SGG 协议），验证集 5,000 样本。

### 评估协议

三个任务：PredCls（给定 GT 框和标签预测关系）、SGCls（给定 GT 框预测对象+关系）、SGDet（端到端检测+关系预测）

指标：R@K（Recall at K）、mR@K（Mean Recall at K，对每个类别取平均后求平均，反映类别级性能）、Mean（R@K 和 mR@K 的平均值，提供综合评估）

### 实现细节

- 框架：PyTorch
- GPU：NVIDIA GeForce RTX 3090（单卡）
- Batch size：12
- 目标检测器：Faster R-CNN with ResXNet-101-FPN（训练时冻结）
- 优化器：SGD，lr=0.0025
- 验证集：5,000 样本

### Baseline 方法

**模型相关方法（model-specific）**: BGNN、PCPL、HetSGG
**模型无关方法（model-agnostic）**: PPDL、TDE、LS-KD、DKBL、Inf（Probabilistic Debiasing）、GCL

### 分区设置

最优分区：N1=5 类别, N2=10 类别, N3=35 类别（相对均匀划分的 16:17:17，此设置将语义相近对如 standing on 和 on 分到不同子集）

## Results

### 主要结果（Table 1）

**Motifs 作为 baseline 时（model-agnostic 对比）**：

| 方法 | PredCls R@50/100 | PredCls mR@50/100 | PredCls Mean | SGCls R@50/100 | SGCls mR@50/100 | SGCls Mean | SGDet R@50/100 | SGDet mR@50/100 | SGDet Mean |
|------|------------------|--------------------|--------------|-----------------|-------------------|-------------|----------------|------------------|------------|
| Motifs†（baseline） | 65.3/67.2 | 14.9/16.3 | 40.9 | 38.9/39.8 | 8.3/8.8 | 23.9 | 32.1/36.8 | 6.6/7.9 | 20.8 |
| Motifs+GCL | 42.7/44.4 | 36.1/38.2 | 40.4 | 26.1/27.1 | 20.8/21.8 | 24.0 | 18.4/22.0 | 16.8/19.3 | 19.1 |
| **Motifs+EPD（ours）** | 54.1/56.0 | **36.3/38.8** | **46.3** | 30.8/31.9 | **21.2/22.4** | **26.5** | 29.5/31.5 | **17.3/19.0** | **24.3** |

关键对比：
- **mR@50**: Motifs+EPD (36.3) vs Motifs (14.9) → **+21.4**。vs Motifs+GCL (36.1) → **+0.2**（略超）
- **Mean**: Motifs+EPD (46.3) vs Motifs+GCL (40.4) → **+5.9**（显著优势，说明 EPD 在提升尾部谓词的同时更少牺牲头部谓词性能）

**VCTree 作为 baseline 时**：

| 方法 | PredCls R@50/100 | PredCls mR@50/100 | PredCls Mean | SGCls R@50/100 | SGCls mR@50/100 | SGCls Mean | SGDet R@50/100 | SGDet mR@50/100 | SGDet Mean |
|------|------------------|--------------------|--------------|-----------------|-------------------|-------------|----------------|------------------|------------|
| VCTree† | 65.9/67.5 | 17.2/18.5 | 42.2 | 45.3/46.2 | 10.6/11.3 | 28.3 | 31.9/36.2 | 7.1/8.3 | 20.8 |
| VCTree+GCL | 40.7/42.7 | 37.1/39.1 | 39.9 | 27.7/28.7 | 22.5/23.5 | 25.6 | 17.4/20.7 | 15.2/17.5 | 17.7 |
| VCTree+Inf | 59.5/61.0 | 28.1/30.7 | 44.8 | 40.7/41.6 | 17.3/19.4 | 31.7 | 27.7/30.1 | 10.4/11.9 | 20.0 |
| VCTree+DKBL | 60.1/61.8 | 28.7/31.3 | 45.4 | 38.8/39.7 | 21.2/22.6 | 30.5 | 26.9/30.7 | 11.8/14.2 | 20.9 |
| **VCTree+EPD（ours）** | 55.4/58.7 | 32.0/35.2 | 45.3 | 33.1/35.4 | **22.9/25.0** | 29.1 | 21.7/25.4 | 13.8/16.3 | 19.3 |

关键对比：
- **mR@50 (PredCls)**: VCTree+EPD (32.0) vs VCTree+GCL (37.1) → -5.1（GCL 在 VCTree 上 mR 更高）；但 Mean 45.3 vs 39.9 → +5.4
- **mR@50 (SGCls)**: VCTree+EPD (22.9) vs 其他去偏方法中最佳；但 Mean (29.1) 低于 Inf (31.7) 和 DKBL (30.5)

### 消融实验

**消融 1：单解码器 vs 多解码器（Table 2，PredCls）**

| 设置 | R@50/100 | mR@50/100 | Mean |
|------|----------|------------|------|
| baseline (Motifs) | 65.3/67.2 | 14.9/16.3 | 40.9 |
| 单解码器 + L'_all | 48.1/50.6 | 28.5/30.3 | 39.4 |
| **多解码器 + L'_all (EPD)** | 54.1/56.0 | **36.3/38.8** | **46.3** |

单解码器（纯 re-weighting 等价）→ mR@50 从 14.9 升至 28.5 (+13.6)，Mean 下降 1.5。多解码器 → mR@50 升至 36.3 (+21.4 vs baseline，+7.8 vs 单解码器)，Mean 升至 46.3 (+5.4 vs baseline)。验证多解码器结构比纯 re-weighting 更有效。

**消融 2：解码器组件（Table 3，PredCls）**

| F_p_d 共享 | BN 层 | R@50/100 | mR@50/100 | Mean |
|-----------|-------|----------|------------|------|
| 共享 | 有 | **54.1/56.0** | **36.3/38.8** | **46.3** |
| 独立 | 有 | 49.9/52.0 | 35.0/37.3 | 43.5 |
| 共享 | 无 | 47.7/50.0 | 30.3/32.0 | 40.0 |
| 独立 | 无 | 51.1/52.9 | 30.9/32.8 | 41.9 |

**结论**：共享 F_p_d（保持初始特征一致）+ 独立 BN（适应不同子任务分布）是最优组合。

**消融 3：训练数据配置（Table 4，PredCls）**

| M_d | AD1 | AD2 | R@50/100 | mR@50/100 | Mean |
|-----|-----|-----|----------|------------|------|
| N1 | N2 | N3 | 59.9/61.5 | 22.0/24.1 | 41.9 |
| N | N2 | N3 | 52.2/54.1 | 34.8/37.2 | 44.6 |
| N | N2∪N3 | N3 | **54.1/56.0** | **36.3/38.8** | **46.3** |

**结论**：训练子集有交集（intersecting subsets）时性能最优，交集中的低频谓词获得更多注意力。

**消融 4：分区基数（Table 5，PredCls）**

| N1 : N2 : N3（类别数） | R@50/100 | mR@50/100 | Mean |
|----------------------|----------|------------|------|
| 16:17:17（均匀） | 57.4/59.2 | 33.3/35.8 | 46.4 |
| 10:10:30 | 54.9/56.7 | 35.2/37.6 | 46.1 |
| **5:10:35** | **54.1/56.0** | **36.3/38.8** | **46.3** |
| 5:15:30 | 52.5/54.5 | 35.8/38.1 | 45.2 |

N1 包含更少类别时 mR@K 更高。最优设置 5:10:35。

**消融 5：损失权重（Table 6/7，PredCls）**

最优：α=8, β=10, γ=0.01 → mR@100=38.8（全类别平均），其中 Head=53.8, Body=30.4, Tail=37.7。

**消融 6：聚合权重（Table 8，PredCls）**

最优：λ_md=0.5, λ_ad1=0.2, λ_ad2=0.3 → Mean=46.3。另一个设置 (0.4, 0.2, 0.4) 给出最高 mR@100=40.9 但 Mean=43.5。

### 可视化结果

对于 tail 谓词三元组 ⟨bird, standing on, banana⟩，主解码器预测 on（错误），加入 AD1 后变为 holding，再加入 AD2 后变为正确的 standing on。验证辅助解码器逐步精炼预测。

对于 head 谓词 ⟨man, has, hair⟩ 和 body 谓词 ⟨dog, walking on, beach⟩，加入辅助解码器后预测保持正确，说明 EPD 不损害高频谓词预测。

## Limitations

1. **仅 VG 单数据集验证**：方法仅在 Visual Genome 上评估，未在 GQA、VRD 等其他 SGG 基准上测试，泛化性待验证。
2. **VCTree 上表现不如某些方法**：在 VCTree 为 baseline 时，EPD 的 Mean 在 SGCls (29.1) 和 SGDet (19.3) 上低于 Inf 和 DKBL，论文归因于这些方法使用了 triplet prior。
3. **超参数调优成本**：引入三个损失权重（α, β, γ）和三个聚合权重（λ_md, λ_ad1, λ_ad2）+ 分区基数，超参数空间较大。
4. **解码器数量固定**：论文仅用了 1 主+2 辅的结构，未探讨更多解码器或自适应解码器数的变体。
5. **计算开销**：三个解码器在训练和推理时增加额外计算量（约 3× 解码器参数）。
6. **长尾划分的粒度**：仅按 head/body/tail 三分，未探索更细粒度的分组策略。

## Reusable Claims

- **Claim**: 多解码器集成 + 差异化训练子集能比纯 weight re-weighting 更有效地提升低频谓词性能（mR@50 +21.4 vs baseline, +7.8 vs 单解码器 re-weighting）。
  - **Evidence**: Table 2，PredCls 任务
  - **Confidence**: High

- **Claim**: 共享线性层参数 + 独立 BN 层是多解码器结构的最优组合。
  - **Evidence**: Table 3，共享 F_p_d + BN 比独立 F_p_d + BN 的 Mean 高 2.8
  - **Confidence**: Medium（仅在一个 backbone 上验证）

- **Claim**: 训练子集有交集（intersecting subsets）比无交集（disjoint subsets）效果更好，体现实例在多个解码器中同时训练有利于低频谓词学习。
  - **Evidence**: Table 4，intersecting 比 disjoint 的 mR@50 高 14.3
  - **Confidence**: High

## Connections

- **GCL** (Dong et al., CVPR 2022): 同样使用多分类器，但 EPD 通过按频率划分训练子集的解码器结构 + 语义相似谓词分离，实现了更高的 Mean 指标（46.3 vs 40.4 with Motifs）。
- **PPDL** (Li et al., CVPR 2022): 基于预测概率分布的重加权策略。
- **TDE** (Tang et al., CVPR 2020): 因果推断去偏方法。EPD 的 Mean (46.3 PredCls) 远超 Motifs+TDE (38.0)。
- **Inf (Probabilistic Debiasing)** (Biswas & Ji, CVPR 2023): 概率去偏。EPD 在 Motifs+PredCls 上 Mean 46.3 vs Inf 40.3。
- **DKBL** (Chen et al., ICME 2023): 语义粒度控制器。在 PredCls 上 VCTree+DKBL Mean 45.4 vs VCTree+EPD 45.3（接近）。
- **HiLo** (另一去偏方法): 高频-低频分离策略的思想类似但实现不同。

## Open Questions

1. EPD 能否在更大范围模型（如 Transformer-based SGG: SGTR, RelTR）上保持一致提升？
2. 解码器数量能否自适应？（较难的谓词对可能需要更多辅助解码器）
3. N1/N2/N3 的划分能否基于语义相似度聚类而非固定频率阈值？
4. 在含更多谓词（如 OpenPSG 的 open-vocabulary 设置）时 EPD 的扩展性如何？
5. 代码未公开，实验可复现性待验证。

## Provenance

- **Raw source**: `raw/sources/2024-08-25-ensemble-predicate-decoding-unbiased-sgg.pdf`
- **Extracted text**: `raw/sources/2024-08-25-ensemble-predicate-decoding-unbiased-sgg.txt`
- **Evidence level**: full-paper（基于完整 PDF 全文提取和精读）
- **Analysis date**: 2026-06-10
