---
title: "APT: Towards Universal Scene Graph Generation via Plug-in Adaptive Prompt Tuning"
type: paper
domain: scene-graph
status: active
created: 2026-06-10
updated: 2026-06-10
tags:
  - scene-graph-generation
  - universal
  - adaptive-prompt
  - prompt-tuning
  - open-vocabulary
  - ICLR-2026
source_pages: []
raw_sources:
  - raw/sources/2026-02-26-APT-adaptive-prompt-tuning-universal-SGG.pdf
  - raw/sources/2026-02-26-APT-adaptive-prompt-tuning-universal-SGG.txt
related_pages:
  - domains/scene-graph/papers/sgtr-end-to-end-scene-graph-generation-with-transformer.md
  - domains/scene-graph/papers/egtr-extracting-graph-from-transformer-scene-graph-generation.md
  - domains/scene-graph/papers/2024-01-adaptive-self-training-framework-fine-grained-sgg.md
  - domains/scene-graph/papers/llm4sgg-weakly-supervised-scene-graph-generation.md
  - domains/scene-graph/papers/sdsgg-scene-specific-description-ovsgg.md
  - domains/scene-graph/papers/ovsgtr-expanding-scene-graph-boundaries.md
  - domains/scene-graph/papers/neural-motifs-scene-graph-global-context.md
paper:
  title: "APT: Towards Universal Scene Graph Generation via Plug-in Adaptive Prompt Tuning"
  authors:
    - Ruikun Luo
    - Changwei Gu
    - Jing Yang
    - Yuan Gao
    - Jieming Yang
    - Song Wu
    - Hai Jin
    - Xiaoyu Xia
  year: 2026
  venue: ICLR 2026
  arxiv: null
  doi: null
  code: https://github.com/CGCL-codes/APT
  project: null
classification:
  label: "场景图生成 · 自适应 prompt 调优 · 通用插件"
  task:
    - Scene Graph Generation (PredCls, SGCls, SGDet)
    - Open-Vocabulary Scene Graph Generation
  method_family: Adaptive Prompt Tuning / Prompt-based Feature Modulation
  modality: Image-Text (vision-language)
  datasets:
    - Visual Genome (VG)
    - Open Images V6 (OI-V6)
    - GQA
  metrics:
    - Recall@K (R@K)
    - Mean Recall@K (mR@K)
    - F@K (harmonic mean of R@K and mR@K)
evidence_level: full-paper
---

# APT: Towards Universal Scene Graph Generation via Plug-in Adaptive Prompt Tuning

> **注意**: 用户标记为 "CVPR 2024"，经核实实际发表会议为 **ICLR 2026**。

## Citation

Ruikun Luo, Changwei Gu, Jing Yang, Yuan Gao, Jieming Yang, Song Wu, Hai Jin, Xiaoyu Xia. "APT: Towards Universal Scene Graph Generation via Plug-in Adaptive Prompt Tuning." In *Proceedings of the International Conference on Learning Representations (ICLR)*, 2026. [OpenReview](https://openreview.net/pdf?id=IZWJhdK2o7) · [Code](https://github.com/CGCL-codes/APT)

## One-Sentence Contribution

提出 APT（Adaptive Prompt Tuning），一种通用轻量级插件模块，通过可学习的连续 prompt 将冻结的静态语义特征转化为动态、上下文感知的表示，可无缝集成到任意 SGG 框架（两阶段、一阶段、开放词汇）中，仅以 <0.5M 额外参数和 7.8%-25% 训练时间减少实现全任务性能提升。

## Problem Setting

### 核心观察

论文跳出了传统的一阶段 vs. 两阶段的架构争论，指出两种范式共享一个根本瓶颈：**依赖固定的、冻结的预训练语义表示**（GloVe、BERT 等）。这些静态嵌入对视觉上下文不敏感，无法区分细粒度关系（如 "standing on" vs "walking on"），也无法捕捉主语/宾语的角色不对称性。

### 证据

1. **t-SNE 可视化**（Figure 2）：GloVe 特征空间中所有 "person" 实例坍缩为单一点；视觉特征空间中 "person" 根据关系上下文（riding、walking、holding 等）自然聚类。
2. **诊断指标**（Table 1）：从 GloVe 到 CLIP-text 的逐级改善（如 Silhouette 0.12→0.29，I(embedding;predicate) 0.42→0.57 bits）表明更强大的预训练模型编码了更丰富的子结构，但这些结构仍与 SGG 所需的精细视觉关系上下文不对齐。
3. **系统性比较**（Figure 1）：在多种 SGG 方法（SGTR、EGTR、ST-SGG 等）上，GloVe → BERT → GPT → CLIP-text 的替换仅带来有限改善，说明仅更换冻结模型不能解决语义刚性问题。

## Method

### Adaptive Prompt Tuning (APT) 框架

APT 的核心思想：为一组轻量级可学习 prompt 参数，充当"条件适配器"，根据视觉上下文和关系角色动态调制冻结的语义特征。

从信息瓶颈（Information Bottleneck）视角，APT 目标是学习最优表示 ẽ：

```
max I(ẽ; y) − βI(ẽ; e_static | v, y)
```

其中第一项使 ẽ 对预测有信息量，第二项鼓励 ẽ 在给定视觉上下文 v 和目标 y 条件下遗忘 e_static 中的冗余信息。

### 组件

#### 1. Detection Prompt (P_d)
- 在目标检测阶段使用
- 为每个目标类别 c 定义可学习向量 P_d(c)
- 通过 MLP 与冻结语义嵌入融合，生成自适应的检测表示

#### 2. Relation Prompt (P_r)
- 在关系预测阶段使用
- 为每个谓词类别 r 定义可学习向量 P_r(r)
- 对主语-宾语对 (s, o) 生成自适应的语义特征并与视觉证据融合

#### 3. Unified Relation Prompt (P_ur)
- 适用于一阶段范式（无分离的检测阶段）
- 在单个 prompt 上操作语义查询或标签嵌入

### Compositional Generalization Prompter (CGP)

专为开放词汇场景设计，包含三个子模块：

#### Relational Context Gating (RCG)
- 生成角色感知的 prompt 权重
- 对实体 s 及其视觉特征 v_s：w_s = σ(MLP_gate(Concat(v_s, e_static(s))))

#### Basis Prompt Synthesis (BPS)
- 一组可学习的基础 prompt B ∈ R^{N×L_ov×D}，作为基础关系概念库
- 最终 prompt 是基础向量的加权组合：P_cgp(s) = Σ w_s^i · B_i
- N=16 个基础

#### Feature Refinement & Fusion (FRF)
- 合成 prompt、冻结语义嵌入和投影视觉特征的最终融合
- 通过 MLP 进行非线性变换生成自适应表示

### 训练目标

除了标准分类损失 L_cls 外，引入多项正则项：
- L2 正则化 prompt 参数
- 特征差异惩罚 ∥ẽ − e_static∥²
- 基础 prompt 正交性约束
- 门控分布的熵和 KL 散度正则

## Experiments

### 数据集

| 数据集 | 实体类 | 关系类 | 训练 | 验证 | 测试 |
|--------|--------|--------|------|------|------|
| Visual Genome (VG) | 150 | 50 | 57,723 | 5,000 | 26,446 |
| Open Images V6 (OI-V6) | 288→301 | 30→31 | 126,368 | 1,813 | 5,322→6,322 |
| GQA | 200 | 100 | 52,623 | 5,000 | 8,209 |

> 注：论文主文仅报告 VG 结果，OI-V6 和 GQA 结果在附录中。

### 评估协议

- **子任务**：Predicate Classification (PredCls)、Scene Graph Classification (SGCls)、Scene Graph Detection (SGDet)
- **指标**：Recall@K (R@K)、Mean Recall@K (mR@K)、F@K（R@K 和 mR@K 的调和平均）
- **开放词汇设置**：Base split (70% 关系类) / Novel split (30% 关系类，训练时未见)

### Baseline 方法

**两阶段方法**：MOTIFS (CVPR'18)、PE-Net (CVPR'23)、DRM (CVPR'24)、RA-SGG (AAAI'25)

**一阶段方法**：SGTR (CVPR'22)、EGTR (CVPR'24)、ST-SGG (ICLR'24)、LLM4SGG (CVPR'24)、SpeaQ (CVPR'24)、HQSG (CVPR'25)

**开放词汇方法**：SDSGG (NeurIPS'24)、OvSGTR (ECCV'24)、SGTR+RAHP (AAAI'25)

### 训练设置

- 框架：PyTorch
- 硬件：4× NVIDIA A40 GPUs
- Prompt 长度：L_d = L_r = 6
- CGP 基础集：N = 16
- 使用各 baseline 官方代码和推荐的训练协议，严格控制变量

## Results

### 视觉 Genome (VG) — 标准设置

**两阶段方法代表性结果（PredCls mR@100）**：

| 方法 | 原始 | +APT | 提升 |
|------|------|------|------|
| MOTIFS | 16.2 | 18.1 | +1.9 |
| PE-Net | 19.2 | 20.5 | +1.3 |
| DRM | 19.2 | 21.9 | +2.7 |
| RA-SGG | 19.8 | 20.2 | +0.4 |

**一阶段方法代表性结果（PredCls mR@100）**：

| 方法 | 原始 | +APT | 提升 |
|------|------|------|------|
| SGTR | 32.9 | 35.3 | +2.4 |
| EGTR | 38.2 | 40.1 | +1.9 |
| LLM4SGG | 39.1 | 42.2 | +3.1 |
| ST-SGG | 31.5 | 34.6 | +3.1 |
| SpeaQ | 33.4 | 36.8 | +3.4 |
| HQSG | 34.6 | 37.3 | +2.7 |

**F@100 改善**：LLM4SGG F@100 48.6→50.3 (PredCls), EGTR F@100 45.6→47.7 (PredCls)

**每类 APrel 分析**（Figure 5）：EGTR+APT 在 head predicates 保持竞争力，在 tail predicates 显著提升，尤其对 attached_to、overlapping 等困难类。

### 开放词汇 (OV) 设置 — VG Novel Split

| 方法 | Novel mR@50 原始 | Novel mR@50 +APT | 提升 |
|------|------------------|-------------------|------|
| SDSGG | 25.2 | 26.7 | +1.5 |
| OvSGTR | 13.5 | 14.3 | +0.8 |
| SGTR+RAHP | 11.8 | 12.4 | +0.6 |

SDSGG+APT 在 Novel 分之上 Novel mR@100 达 32.3 (vs 31.2)，为 OV 设置最佳。

### 消融实验

**APT 组件消融（基于 PE-Net, VG PredCls）**：

| 配置 | mR@50 | mR@100 | F@50 | F@100 |
|------|-------|--------|------|-------|
| Vanilla PE-Net | 31.5 | 33.8 | 42.4 | 45.0 |
| +D-Prompt only | 30.4 | 32.6 | 41.0 | 43.8 |
| +R-Prompt only | 33.4 | 36.4 | 43.6 | 46.0 |
| +Full APT | 36.2 | 39.1 | 45.7 | 48.6 |

R-Prompt 是核心：单独使用即带来显著 mR 提升（+2.6 mR@100）。D-Prompt 单独使用效果有限，但两者协同时最优。

**CGP 组件消融（基于 SDSGG, VG OV split）**：

| 配置 | Base mR@50 | Novel mR@50 | Novel F@50 |
|------|-----------|-------------|------------|
| Vanilla SDSGG | 12.4 | 25.2 | 25.3 |
| +RCG | 13.1 | 26.7 | 26.1 |
| +BPS | 13.6 | 27.5 | 26.7 |
| +RCG+BPS | 14.5 | 29.0 | 27.4 |
| +Full CGP | 15.9 | **31.2** | **28.6** |

BPS 贡献最大（Novel mR@50 +3.8 vs baseline），全 CGP 达最优。

### 效率分析

| 模型 | 参数量变化 | 时间/epoch 变化 | mR@100 增益 |
|------|-----------|----------------|-------------|
| SGTR | +0.2M (0.5%) | 0% | +2.7 |
| EGTR | +0.4M (0.9%) | -7.8% | +2.7 |
| ST-SGG | -1.2M* (-2.8%) | -11.3% | +2.5 |
| LLM4SGG | -2.1M* (-4.6%) | -25.0% | +1.5 |
| SpeaQ | -0.5M (-1.2%) | -16.3% | +3.4 |
| DRM | +0.4M (0.8%) | -13.0% | +3.2 |
| PE-Net | +0.4M (0.9%) | -10.0% | +1.8 |

> *负参数变化源于 APT 可替代部分原有语义特征层，实现参数精简。

APT 总参数量始终 <0.5M（<1.5% overhead）。

### 信息瓶颈分析（Table 7）

| 指标 | APT | Frozen (GloVe) |
|------|-----|-----------------|
| PCA@90% | 23 | 26 |
| PCA@95% | 28 | 35 |
| Linear CKA | 0.877 | — |
| Discretized MI proxy | 1.96 | 1.49 |

APT 表示更紧凑（更少主成分解释相同方差），保留了更多标签相关信息。

## Limitations

1. **超参数敏感**：Prompt 长度 (L_d, L_r)、基础数量 (N)、正则化权重 (λ_*) 等超参数需调优，尤其是 β>1.0 时可能导致性能下降。
2. **仅单数据集详尽验证**：主文仅报告 VG 完整结果（受页面限制），OI-V6 和 GQA 结果在附录中；GQA 尚需进一步验证。
3. **CGP 仅用于 OV 设置**：Compositional Generalization Prompter 当前仅为 OV 设计，未验证在标准设置中是否能带来额外收益。
4. **外部知识未探索**：未探索使用外部未标注数据或无监督数据进一步增强 prompt 学习。
5. **计算开销线性增长**：多个 prompt（类级别）在类别数大时可能带来存储开销。
6. **理论论证验证有限**：信息瓶颈解释主要通过 proxy 指标验证，缺乏直接的互信息估计。

## Reusable Claims

1. **冻结语义特征是 SGG 的根本瓶颈**：论文通过 t-SNE 可视化、诊断指标和系统性对比实验，跨架构验证了静态语义嵌入对视觉关系推理的局限性。这一洞察超越了一阶段 vs. 两阶段的架构讨论。

2. **Prompt 调优可作为通用 SGG 插件**：APT 证明了轻量级 prompt（<0.5M 参数）可作为即插即用模块增强任意 SGG 框架，同时减少训练时间 7.8%-25%，在人力和资源效率方面建立新的 Pareto 前沿。

3. **R-Prompt > D-Prompt**：关系 prompt（R-Prompt）对谓词判别起决定性作用，检测 prompt（D-Prompt）贡献有限。这为未来 SGG 模块设计提供了明确的优化优先级。

4. **基础合成（BPS）是 OV 泛化的关键**：CGP 消融中 BPS 贡献了最大的 Novel 性能提升（mR@50 +3.8），表明从有限基础 prompt 组合合成新表示是实现组合泛化的有效策略。

5. **自适应 prompt 加速收敛**：多个模型上训练时间减少（最高 25%）表明自适应语义特征比固定特征更易于优化和收敛，这一副效应值得进一步研究。

## Connections

- **SGTR / EGTR / ST-SGG**: APT 以这些一阶段方法为 backbone 进行集成验证，展示了即插即用的通用性。
- **MOTIFS / PE-Net / DRM / RA-SGG**: 两阶段 backbone，APT 展示了跨架构的一致性提升。
- **SDSGG / OvSGTR / RAHP**: OV backbone，APT+CGP 提升了 Novel 类别的泛化能力。
- **LLM4SGG**: APT 在 LLM4SGG 上削减了 25% 训练时间，展示了与 LLM 增强 SGG 方法的兼容性。
- **与 prompt learning 的关联**: APT 借鉴了 continuous prompt learning (Lester et al., 2021) 和 CoOp/CoCoOp 的思路，将其创新性地适配到 SGG 的模态间结构化预测场景。

## Open Questions

1. **APT 能否扩展到更大规模的类别空间（如 >1000 类）？** 类级别 prompt 的存储和计算成本如何？
2. **信息瓶颈解释能否通过更直接的互信息估计验证？** 当前 proxy 指标的可靠性如何？
3. **D-Prompt 在部分设置中轻微负效果（Table 4）的原因？** 是否检测阶段不需要语义自适应，或需要更精细的设计？
4. **训练时间减少的具体机制**？论文推测自适应 prompt 稳定和加速了收敛，但未提供收敛曲线对比。
5. **CGP 中的基础 prompt 是否可迁移到其他视觉任务？** 学到的关系基础概念是否有跨任务泛化能力？
6. **GQA 上 100 种关系类别的性能表现如何？** 论文受页面限制未在主文报告。
7. **与全参数微调对比**：APT 的参数量效率优势明确，但是否存在性能天花板？
8. **与同期的其他通用 SGG 方法（如 OvSGTR、RAHP）对比部署复杂度**：计算效率 vs 集成难度 trade-off 如何？

## Provenance

- **原始来源**: raw/sources/2026-02-26-APT-adaptive-prompt-tuning-universal-SGG.pdf (20 pages, 1.2 MB)
- **提取文本**: raw/sources/2026-02-26-APT-adaptive-prompt-tuning-universal-SGG.txt (2,493 lines, ~75 KB)
- **证据等级**: full-paper — 全文精读，所有 claim 均有具体数字支撑
- **额外检索**: 通过 OpenReview 确认会议为 ICLR 2026，通过 GitHub 确认公开代码可用
