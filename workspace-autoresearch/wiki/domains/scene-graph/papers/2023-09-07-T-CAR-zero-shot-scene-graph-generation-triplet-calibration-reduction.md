---
title: "T-CAR: Zero-Shot Scene Graph Generation via Triplet Calibration and Reduction"
type: paper
domain: scene-graph
status: active
created: 2026-06-10
updated: 2026-06-10
tags:
  - scene-graph-generation
  - zero-shot
  - triplet-calibration
  - unseen-space-reduction
  - compositional-zero-shot-learning
  - TOMM-2023
  - triplet-granularity
raw_sources:
  - ../../../raw/sources/2023-09-07-T-CAR-zero-shot-scene-graph-generation-triplet-calibration-reduction.pdf
  - ../../../raw/sources/2023-09-07-T-CAR-zero-shot-scene-graph-generation-triplet-calibration-reduction.txt
related_pages:
  - cage-sgg-counterfactual-active-graph-evidence-open-vocabulary-sgg.md
  - 2025-PRISM-0-predicate-rich-zero-shot-sgg.md
  - compositional-feature-augmentation-for-unbiased-scene-graph-generation.md
evidence_level: full-paper
paper:
  title: "Zero-Shot Scene Graph Generation via Triplet Calibration and Reduction"
  abbreviated: "T-CAR"
  authors:
    - Jiankai Li
    - Yunhong Wang
    - Weixin Li
  affiliations:
    - Beihang University
    - Shanghai Artificial Intelligence Laboratory
  year: 2023
  venue: ACM Transactions on Multimedia Computing, Communications, and Applications (TOMM) 2023. (arXiv: 2309.03542, also on arXiv Sep 2023)
  doi: "10.1145/3604284"
  arxiv: "2309.03542"
  code: "https://github.com/jkli1998/T-CAR"
  url: null
classification:
  label: "Compositional Zero-Shot SGG via Triplet Calibration and Unseen Space Reduction"
  task:
    - Scene Graph Generation (SGG)
    - Zero-Shot Scene Graph Generation
    - Compositional Zero-Shot Learning
  method_family:
    - Triplet Calibration Loss (TCL)
    - Unseen Space Reduction Loss (USRL)
    - Contextual Encoding Network (CEN)
    - Positive-Unlabeled Learning (nnPU)
  modality: Image
  datasets:
    - Visual Genome (VG150)
  metrics:
    - Zero-Shot Recall@K (zR@K)
    - Recall@K (R@K)
---

## Citation

```
Jiankai Li, Yunhong Wang, and Weixin Li. "Zero-Shot Scene Graph Generation via Triplet Calibration and Reduction." 
ACM Transactions on Multimedia Computing, Communications, and Applications (TOMM), 2023.
arXiv: 2309.03542. DOI: 10.1145/3604284.
```

## One-Sentence Contribution

提出 Triplet Calibration and Reduction (T-CAR) 框架，通过 triplet 粒度的校准损失（TCL）挖掘未标注训练样本中的 unseen triplets，结合 unseen space reduction loss（USRL）缩小包含大量不合理组合的 unseen 空间，并用 contextual encoding network（CEN）显式建模 subject-object 相对空间关系以提升零样本 SGG 的泛化能力。

## Problem Setting

零样本场景图生成（Zero-Shot SGG）的目标是从训练集中学习三元组 `<subject-predicate-object>`，并在测试时推断 unseen 组合。现有的 SGG 方法面临两个关键问题：

1. **Seen Triplet Bias**：主导 triplets 导致模型对 diverse triplets 的判别能力差，倾向于预测高频 triplets；
2. **Giant Unseen Space**：unseen 空间远大于 seen 空间（VG150 上 unseen 空间约为 seen 空间的 37 倍），其中大部分组合在现实中不存在（如 `<seat-eating-dog>`）。

## Method

### 总体框架

T-CAR 包含三个核心模块：

1. **Contextual Encoding Network (CEN)**：移除语言先验（linguistic priors），显式编码 subject 和 object 之间的相对空间特征；
2. **Triplet Calibration Loss (TCL)**：对 seen triplets 根据频率施加不同 margin 校准，同时挖掘训练集中的 unseen triplets；
3. **Unseen Space Reduction Loss (USRL)**：基于 triplets 中 subject/predicate/object 的可替换性（interchangeability），将 unseen 空间缩小到合理范围。

### Contextual Encoding Network (CEN)

- **Entity Encoder**：4 层 Transformer，不使用 linguistic features 初始化，仅用视觉+空间特征
- **Fusion Layer**：融合 subject 和 object 的 refine entity representations，加上 union box 视觉特征和相对空间特征
- **Relation Encoder**：2 层 Transformer 建模 relation context
- **相对空间特征**：由归一化联合框位置 b_ul、相对尺寸 b_sl、相对位置 b_rl 三部分组成

### Triplet Calibration Loss (TCL)

- **Unseen Triplet Calibration**：对训练集中标注为 background 但可能为 unseen triplet 的样本，施加反向校准损失，抵抗交叉熵对 unseen 样本的抑制
- **Seen Triplet Calibration**：对 seen triplets 根据频率施加动态 margin α：高频 triplet 受到更大约束，低频 triplet 受到较小约束
  - α_{s,c,o} = log(n_max / n_{s,c,o}) × normalization factor
- 最终损失：L = L^{m,α}_{ce} + λ L^{m,α}_{cal}

### Unseen Space Reduction Loss (USRL)

- 利用 subject/predicate/object 的可替换性（如 `<dog-walking on-street>` 可根据已知 seen triplets 推理合理性）
- 对 triplet 的三种配对（sbj↔(pred,obj)、(sbj,obj)↔pred、(sbj,pred)↔obj）分别判断合理性
- 形式化为 Positive-Unlabeled Learning (PU Learning) 问题，采用 nnPU loss 训练
- 最佳 reduction rate: 85%（此时 unseen 空间缩小到原来的 15%）

## Experiments

### 数据集
- **Visual Genome (VG150)**：150 个 object 类别，50 个 relation 类别
  - 训练集中约 29,283 个 seen triplets，约 5,000 个 unseen triplets（测试集），潜在组合约 1,125,000 种

### Baseline 方法
- **VGG-16 backbone**：IMP, Motifs, IMP++, GRAPHN
- **ResNeXt-101-FPN backbone**：IMP, VTransE, Motifs, Motifs+Freq, IMP++, TDE, UVTransE, EBM, BGNN, SSR(Base/Large), NARE

### 评估指标
- **Recall@K (R@K)**：Top-K 预测中包含 ground-truth triplets 的比例
- **Zero-Shot Recall@K (zR@K)**：Top-K 预测中包含 unseen ground-truth triplets 的比例
- 任务：PredCls, SGCls, SGDet
- 测试协议：不使用 Object Overlap 限制，不使用 Validation Set，移除 Frequency Bias

### 训练设置
- Backbone: VGG-16 或 ResNeXt-101-FPN (Faster R-CNN)
- 优化器：SGD，初始 lr=10⁻³，10k 次迭代后 decay 10 倍，共 16k 次迭代
- Batch size: 14
- 语言嵌入：GloVe 200 维
- USRL 缩减率：85%
- λ = 0.01, π = 0.03
- 硬件：2× NVIDIA GeForce RTX 2080Ti
- 后处理：relational-NMS
- 框架：PyTorch

## Results

### 主要结果（with graph constraint）

| Backbone | Method | PredCls zR@100 | SGCls zR@100 | SGDet zR@100 |
|----------|--------|:---:|:---:|:---:|
| VGG-16 | GRAPHN | 22.4 | 4.5 | 1.1 |
| VGG-16 | **T-CAR (ours)** | **32.8** | **8.7** | **4.2** |
| X-101-FPN | Motifs | 20.5 | 5.0 | 2.7 |
| X-101-FPN | IMP++ | 22.4 | 5.0 | 0.9 |
| X-101-FPN | TDE | 16.4 | 3.5 | 2.6 |
| X-101-FPN | EBM | 20.0 | 6.2 | 3.0 |
| X-101-FPN | SSR(Large) | - | - | 4.2 |
| X-101-FPN | **T-CAR (ours)** | **34.9** | **10.6** | **6.0** |

T-CAR 在 PredCls/SGCls/SGDet 的 zR@100 上分别提升 **12.5% / 4.4% / 1.8%**（相比现有 SOTA）。

### 主要结果（without graph constraint）

| Backbone | Method | PredCls zR@100 | SGCls zR@100 | SGDet zR@100 |
|----------|--------|:---:|:---:|:---:|
| X-101-FPN | Motifs | 39.7 | 11.2 | 4.5 |
| X-101-FPN | EBM | 38.3 | 13.9 | 4.4 |
| X-101-FPN | **T-CAR (ours)** | **50.8** | **16.7** | **8.7** |

### 消融实验结果

**组件消融（zR@100, X-101-FPN, SGCls/PredCls）：**
| CEN | TCL | USRL | SGCls | PredCls |
|:---:|:---:|:---:|:---:|:---:|
| ✗ | ✗ | ✗ | 3.9 | 16.6 |
| ✓ | ✗ | ✗ | 6.4 | 24.3 |
| ✗ | ✓ | ✗ | 7.3 | 26.7 |
| ✓ | ✓ | ✗ | 9.8 | 34.1 |
| ✓ | ✗ | ✓ | 7.9 | 27.6 |
| ✓ | ✓ | ✓ | **10.6** | **34.9** |

**TCL Margin 消融（SGCls zR@100）：** MU + MCE 同时启用达到最佳 10.6（vs. 禁用时 10.0）

**USRL Reduction Rate（SGCls zR@100）：** 最佳 reduction rate 为 85%（zR@100 = 10.6），超过 85% 后性能下降（100% reduction 时仅 6.1）

**USRL 方法与 BiLSTM 对比：** 本文方法 AUC 93.0% vs BiLSTM 91.0%，F1 7.9 vs 6.1

**λ 消融（SGCls zR@100）：** λ=0.01 时最佳（10.6），λ=1.0 时下降到 5.8

**特征初始化消融：** 去除相对位置编码（w/o P）后 SGCls zR@100 从 10.6 降至 9.9；加入语言特征（w L）性能介于之间（10.0）

### 每个 predicate 类别改进

T-CAR 在 head/body/tail 谓词类别上全面超越 IMP++（Fig. 4, Fig. 5），尤其在低频谓词上提升显著（如 "walking on" +26.6%, "laying on" +17.6%, "eating" +13.1%）。

## Limitations

1. **整体 recall 仍有下降**：T-CAR 的 seen sample Recall 相比 Motifs 有所下降（R@100 PredCls: 63.0 vs 66.9），说明零样本性能提升部分以 seen 性能为代价。
2. **USRL 的 reduction rate 需要调节**：85% 的缩减率在 VG150 上最优，但在不同的数据集上可能需要重新调参。
3. **仅在 VG 上验证**：未在 Open Images 等其他数据集上评估，泛化性待验证。
4. **GloVe 词嵌入依赖**：USRL 使用 GloVe 语言嵌入判断 triplet 合理性，可能无法捕捉细粒度的语义差异。

## Reusable Claims

1. **Triplet 粒度优于 predicate 粒度**：解决零样本 SGG 问题应在 triplet 层面而非 predicate 层面，T-CAR 显著优于 predicate-granularity debiasing 方法（TDE）。
2. **移除语言先验可降低 seen bias**：CEN 中移除 linguistic features 后，unseen 性能不降反升（T-CAR w L vs T-CAR 的 SGCls zR@100: 10.0 vs 10.6）。
3. **相对空间编码有助于提升 unseen 泛化**：显式建模 subject/object 相对位置对于提升零样本 SGG 有效。
4. **Unseen space reduction 是必要的**：直接在全 unseen 空间搜索会引入大量不合理的噪音，PU Learning 方案可以有效缩小搜索空间。
5. **训练集中存在大量未标注的 unseen triplets**：对这些未被标注的 unseen triplets 施加校准而非直接抑制，显著改善零样本 recall。
6. **Frequency Bias 严重损害零样本性能**：删除 Motifs 中的 Frequency Bias 后，zR@100 PredCls 从 4.8 提升至 20.5（Tab. 1 中 Motifs+Freq vs Motifs）。

## Connections

- **与 TDE [CVPR 2020]**：TDE 通过反事实因果推理做 predicate-granularity debiasing，T-CAR 则在 triplet 粒度上校准，二者粒度不同，T-CAR 更适合零样本 SGG。
- **与 GRAPHN [2020]**：GRAPHN 用 GAN 生成 unseen triplets 的视觉特征，T-CAR 则直接挖掘训练集中的 unseen triplets，不需要生成模型。
- **与 SSR [NeurIPS 2022]**：SSR 直接预测 triplets（跳过 predicate 分类范式），T-CAR 在标准两阶段范式下实现了更好的零样本性能。
- **与 BGNN [2022]**：BGNN 专注于 unbiased predicate prediction 而非零样本，在 zR 上远低于 SGG baselines，说明 unbiased SGG 和 zero-shot SGG 是不同的问题。
- **与 EBM [NeurIPS 2022]**：EBM 用能量损失改进 compositional generalization，T-CAR 在 triplet 粒度上更精细。

## Open Questions

1. 如何在不降低 seen recall 的前提下提升 zero-shot recall？当前存在 trade-off。
2. USRL 的 PU Learning 方案在 VG 以外（如 Open Images）是否有效？
3. CEN 中移除语言先验的决策在 fine-grained 类别下是否仍适用（如区分 "riding" vs "driving"）？
4. 是否可以将 T-CAR 的方法扩展到 open-vocabulary SGG 或视频 SGG 场景？

## Provenance

- 论文 PDF: `raw/sources/2023-09-07-T-CAR-zero-shot-scene-graph-generation-triplet-calibration-reduction.pdf`
- 提取文本: `raw/sources/2023-09-07-T-CAR-zero-shot-scene-graph-generation-triplet-calibration-reduction.txt`
- 代码仓库: https://github.com/jkli1998/T-CAR
- ArXiv: https://arxiv.org/abs/2309.03542
- DOI: 10.1145/3604284
