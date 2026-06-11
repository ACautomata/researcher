---
title: Scalable Theory-Driven Regularization for Scene Graph Generation
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - SGG
  - neurosymbolic
  - regularization
  - knowledge-injection
  - negative-constraints
source_pages: []
raw_sources:
  - ../../../sources/scene-graph/2023-AAAI-Scalable-Theory-Driven-Regularization-SGG.pdf
  - ../../../sources/scene-graph/2023-AAAI-Scalable-Theory-Driven-Regularization-SGG.txt
paper:
  title: "Scalable Theory-Driven Regularization for Scene Graph Generation"
  authors:
    - Davide Buffelli
    - Efthymia Tsamoura
  year: 2023
  venue: AAAI
  arxiv: "2209.02749"
  code: "https://github.com/tsamoura/ngp"
classification:
  label: NGP
  task:
    - Scene Graph Generation (Predicate Classification)
    - Scene Graph Generation (Scene Graph Classification)
  method_family: Neuro-Symbolic Regularization
  modality: Image
  datasets:
    - Visual Genome (VG)
    - Open Images v6 (OIv6)
  metrics:
    - Mean Recall@K (mR@20/50/100)
    - Zero-shot Recall@K (zsR@20/50/100)
evidence_level: full-paper
---

# Scalable Theory-Driven Regularization for Scene Graph Generation

## Citation

Davide Buffelli and Efthymia Tsamoura. "Scalable Theory-Driven Regularization for Scene Graph Generation." *Proceedings of the AAAI Conference on Artificial Intelligence (AAAI)*, 2023.

## One-Sentence Contribution

提出 NGP（Neural-Guided Projection），一种模型无关的符号正则化技术，通过逻辑损失函数将负完整性约束注入 SGG 神经网络，支持百万级约束规模且无推理时开销。

## Problem Setting

SGG 任务要求从图像中识别所有 `predicate(subject, object)` 事实。现有方法利用常识知识的两种途径各有缺陷：
1. **次符号化方法**（如 GLAT、LENSR）：需要额外的神经网络架构，增加训练/推理开销；
2. **符号化方法**（如 LTNs）：无法扩展到大规模背景知识。

NGP 通过提供"模型**不应**预测什么"（负完整性约束 IC）的监督信号，区别于传统提供"应预测什么"的正向示例方法。

## Method

### 核心思想

- 使用一阶逻辑中的**负原子完整性约束**（negative atomic ICs）表示背景知识
- 构造逻辑损失函数 `L_s(φ, w_θ)` 衡量模型预测 `w_θ` 违反 IC φ 的程度
- 训练目标：最小化 `β₁ · L_n(ground truth, w_θ) + β₂ · L_s(T, w_θ)`

### 支持的语义和损失函数

- **概率逻辑**：语义损失（Semantic Loss, SL）（Xu et al. 2018），基于加权模型计数
- **模糊逻辑**：DL2 损失（Fischer et al. 2019），支持 Lukasiewicz t-norm
- 损失函数需要满足：(i) 逻辑一致性时为 0；(ii) 几乎处处可微

### Neural-Guided Projection（NGP）

为解决大规模理论下的计算瓶颈，对每张训练图像 Iⁱ 选择 ρ 个**最大非满足约束**（maximally non-satisfied ICs）T^{i*}_ρ：

- **Greedy 策略**（Algorithm 2）：对预测置信度 `w(p)·w(s)·w(o)` 最高的 ρ 个 `p(s,o)` 三元组，取其在理论 T 中对应的负 IC
- 训练时只为 T^{i*}_ρ 计算损失，而非整个理论 T

### 优势

- 模型无关（支持 IMP、MOTIFS、VCTree）
- 推理时**零开销**（不访问背景知识）
- 支持与非偏技术（TDE）正交叠加

### 理论构建

构建了两个负 IC 理论：
- **CNet¬**：基于 ConceptNet 稀疏子图的补集（~500k ICs）
- **VG¬**：基于 VG 训练事实的补集（~1M ICs）

## Experiments

### 数据集和划分

| 数据集 | 划分协议 | 特点 |
|--------|----------|------|
| Visual Genome (VG) | Tang et al. 2020 划分 | 高度偏差，90% 事实集中在少数谓词 |
| Open Images v6 (OIv6) | Li et al. 2021 划分 | 标注质量更高，偏差更小 |

### Baseline 模型

- IMP (Xu et al. 2017) — 基于迭代消息传递
- MOTIFS (Zellers et al. 2018) — 基于神经模式挖掘
- VCTree (Tang et al. 2019) — 基于动态树结构

### 对比的正则化和架构方法

- **TDE** (Tang et al. 2020) — 推理时去偏（正交于 NGP）
- **GLAT** (Zareian et al. 2020) — 推理时基于训练事实模式修正
- **LENSR** (Xie et al. 2019) — 训练时嵌入符号知识到流形
- **LTNs** (Donadello et al. 2017) — 符号化训练时正则化（因规模限制未报告）
- **ITR** — 自建推理时对照：选择不违反任何 IC 的最高置信度预测
- **KBFN** (Gu et al. 2019) — 运行时同时访问 ConceptNet 的神经符号架构
- **BGNN** (Li et al. 2021) — 置信感知二分图神经网络

### 超参数设置

- ρ = 3（约束采样数）
- β₁、β₂ 通过 (Kendall, Gal, and Cipolla 2018) 自动计算
- 使用完整理论训练（LTNs 在同一资源下需 ~4000 小时/epoch）

### 评估协议

- 两项任务：Predicate Classification（已知 bbox+标签预测关系）、Scene Graph Classification（仅已知 bbox 预测）
- 指标：mR@K（去偏 recall）、zsR@K（零样本 recall）
- 限制标注实验：移除 10%~75% ground-truth facts（保留对应图像，NGP 可用 L_s 监督）

## Results

### 主表结果（CNet¬ 理论，VG 数据集）

**IMP 的相对提升最显著：**
| 任务 | 设置 | Baseline mR@100 | NGP(SL) mR@100 | 相对提升 |
|------|------|-----------------|----------------|----------|
| Predicate Cls | IMP | 12.23 | 15.30 | **+25%** |
| Scene Graph Cls | IMP | 6.74 | 8.92 | **+33%** |
| Predicate Cls | MOTIFS | 17.35 | 17.76 | +3% |
| Scene Graph Cls | MOTIFS | 8.85 | 8.42 | - |
| Predicate Cls | VCTree | 18.11 | 18.92 | +4.5% |
| Scene Graph Cls | VCTree | 12.12 | 12.35 | +6.4% |

**NGP(SL) 优于对比方法**（IMP 上最明显）：
- mR@100: NGP(SL) 15.30 vs. ITR 12.23 vs. LENSR 14.22
- mR@50: NGP(SL) 14.22 vs. ITR 11.44 vs. LENSR 13.16

### NGP + TDE 叠加效果（CNet¬，Predicate Cls）

| 模型 | 设置 | mR@20 | mR@50 | mR@100 |
|------|------|-------|-------|--------|
| VCTree | Baseline | 13.07 | 16.75 | 18.11 |
| VCTree | TDE | 19.40 | 25.94 | 29.48 |
| VCTree | NGP + TDE | **23.91** | **30.78** | **34.19** |
| MOTIFS | TDE | 17.18 | 23.95 | 27.66 |
| MOTIFS | NGP + TDE | **17.99** | **24.50** | **28.16** |

NGP + TDE 提升超过单独应用之和（非加性叠加）。

### NGP + TDE vs. GLAT + TDE（VG¬，VCTree）

| 设置 | Pred Cls mR@100 | Sg Cls mR@100 |
|------|----------------|---------------|
| TDE | 29.48 | 16.73 |
| NGP + TDE | **34.53** | **17.66** |
| GLAT + TDE | 23.14 | 3.60 |

GLAT 与 TDE 叠加后 mR 反而下降（GLAT + TDE 在 Scene Graph Cls 上 mR@100 降至 3.60，远低于 TDE 单独的 16.73）。

### 限制标注实验（OIv6，MOTIFS）

| 标注减少 | 设置 | Pred Cls mR@100 | Sg Cls mR@100 |
|---------|------|----------------|---------------|
| 0% | Baseline | 46.10 | 28.90 |
| 0% | NGP(SL) | **48.65** | 26.07 |
| 50% | Baseline | 43.12 | 25.81 |
| 50% | NGP(SL) | **46.41** | 26.21 |
| 75% | Baseline | 42.16 | 23.27 |
| 75% | NGP(SL) | **44.90** | 25.23 |

**50% 标注减少下 TDE 的 mR@100 从 32.07 降至 32.08↓，而 NGP 提供正向监督。**

### 限制标注实验（VG，IMP，Predicate Cls）

- 50% 标注减少，IMP zsR@100：从 3.06%（无 NGP）提升至 **18.99%**（+520%）
- 50% 标注减少，IMP mR@100：从 5.36% 提升至 11.28%（+110%）

### 对低频谓词的提升（VCTree + TDE + NGP）

- `belonging to` 谓词 R@100 相对提升 **+23,142%**
- `on back of` 谓词 R@100 相对提升 **+24,943%**
- 论文图 3 展示了 28 个最不频繁谓词的 recall 全面改善

### 正则化 vs. 专用架构

正则化 VCTree（NGP + TDE + ITR）**Predicate Cls mR@100 = 34.19**，远高于 KBFN 的 18.43（+86%）和 BGNN 的 3.63（+90%）。

## Limitations

1. **MOTIFS 对正则化敏感**：对 VG¬ 和模糊逻辑（DL2）采用时 recall 下降
2. **仅支持负原子约束**：不支持和/或/蕴含等更丰富的一阶逻辑公式
3. **理论质量依赖外部知识库**：ConceptNet/VG 补集包含噪声，未人工检查
4. **超参数 ρ 需要调优**：固定 ρ=3 对其他场景未必最优
5. **LTNs 可扩展性差**：作为对比方法在同一资源下需 ~4000 小时/epoch

## Reusable Claims

1. **负约束正则化能有效提升 SGG 性能**：通过定义模型"不应预测"的知识实现弱监督（evidence: Tables 1-5）
2. **NGP 的贪心约束选择策略有效**：选择最大化违反的 ρ 个约束比随机/全部约束更高效（evidence: Algorithm 2, Section "Neural-Guided Projection"）
3. **正则化 + 去偏正交叠加**：NGP + TDE 提升超过单独效果之和（evidence: Tables 3-4）
4. **符号正则化在弱监督下最有效**：标注越少，NGP 增益越大（evidence: Table 5, Figure 2）
5. **正则化标准模型优于专用神经符号架构**：VCTree + TDE + NGP 显著超过 KBFN、BGNN（evidence: Figure 4）

## Connections

- **TDE**（Tang et al. 2020）：NGP 可与 TDE 正交叠加，效果非加性
- **GLAT**（Zareian et al. 2020）：GLAT 无法有效结合去偏技术（与 TDE 叠加后 mR 下降）
- **LENSR**（Xie et al. 2019）：在 Scene Graph Classification 上完全失效（mR@K 降至 ~0.01），因其流形映射对高不确定性预测不稳定
- **KBFN**（Gu et al. 2019）：ngp 训练时+推理时无开销，KBFN 则在两个阶段都访问知识库
- **ConceptNet**: 作为背景知识源，NGP 取其稀疏子图补集

## Open Questions

1. 是否支持更丰富公式类型（非仅负原子约束）以捕获更细粒度常识？
2. ρ 值是否需要自适应调整（非固定 3）？
3. 理论噪声对 NGP 性能的鲁棒性边界在哪？论文明确未人工检查理论质量。
4. NGP 运用于其他视觉任务（如 VQA、检测）的表现？
5. 与 DeepProbLog、NeuroLog 等可微概率逻辑编程框架的集成？

## Provenance

- 来源：提取自 `/home/node/.openclaw/workspace-autoresearch/raw/sources/2023-AAAI-Scalable-Theory-Driven-Regularization-SGG.txt`
- PDF 路径：`raw/sources/2023-AAAI-Scalable-Theory-Driven-Regularization-SGG.pdf`
- 精读全文，覆盖引言、方法（含 Algorithm 1-2）、实验（Table 1-5）、消融、限制、相关工作
- Evidence level: **full-paper**
