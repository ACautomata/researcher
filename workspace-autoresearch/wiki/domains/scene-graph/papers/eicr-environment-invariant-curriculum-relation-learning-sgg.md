---
title: "Environment Invariant Curriculum Relation Learning for Fine-Grained Scene Graph Generation (EICR)"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - scene-graph-generation
  - long-tail-bias
  - context-imbalance
  - curriculum-learning
  - invariant-risk-minimization
  - debiasing
  - ICCV-2023
raw_sources:
  - ../../../raw/sources/2023-ICCV-Environment-Invariant-Curriculum-Relation-Learning-for-Scene-Graph-Generation.pdf
  - ../../../raw/sources/2023-ICCV-Environment-Invariant-Curriculum-Relation-Learning-for-Scene-Graph-Generation.txt
related_pages:
  - compositional-feature-augmentation-for-unbiased-scene-graph-generation.md
evidence_level: full-paper
paper:
  title: "Environment Invariant Curriculum Relation Learning for Fine-Grained Scene Graph Generation"
  authors:
    - Yukuan Min
    - Aming Wu
    - Cheng Deng
  year: 2023
  venue: "IEEE/CVF International Conference on Computer Vision (ICCV), 2023"
  arxiv: null
  doi: null
  code: "https://github.com/myukzzz/EICR"
  project: null
classification:
  label: "EICR — Environment Invariant Curriculum Relation Learning for Fine-Grained SGG"
  task:
    - Scene Graph Generation (SGG)
    - Predicate Classification (PredCls)
    - Scene Graph Classification (SGCls)
    - Scene Graph Detection (SGDet)
  method_family:
    - Invariant Risk Minimization (IRM)
    - Environment-invariant learning
    - Curriculum learning
    - Resampling and reweighting
  modality:
    - Visual features (ROI)
    - Semantic embeddings (GloVe)
    - Union box features
  datasets:
    - Visual Genome (VG)
    - GQA
  metrics:
    - Recall@K (R@K)
    - mean Recall@K (mR@K)
    - F@K (harmonic mean of R@K and mR@K)
    - mT@K (mean Recall for triplets with different context)
---

## Citation

Yukuan Min, Aming Wu, Cheng Deng. "Environment Invariant Curriculum Relation Learning for Fine-Grained Scene Graph Generation." *Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)*, 2023, pp. 13296-13304.

## One-Sentence Contribution

提出 EICR 框架，首次在 SGG 中同时识别并处理**谓词类别不均衡（class imbalance）**和**主客体语境不均衡（context imbalance）**，通过环境不变学习（Environment-Invariant Learning）消除语境偏置 + 课程学习策略（Class-Balanced Curriculum Learning）消除谓词类别偏置，以即插即用方式嵌入现有 SGG 模型。

## Problem Setting

场景图生成（SGG）旨在检测图像中全部视觉关系三元组 `<sub, pred, obj>`。现有数据集存在两种不均衡：

1. **类不均衡（Class Imbalance）**：谓词类别服从长尾分布，模型偏向头部谓词（如 on, has）而忽略尾部谓词——已有大量工作处理。
2. **语境不均衡（Context Imbalance）**（本文新提出）：不同主客体对 `<sub, obj>` 的分布频率差异巨大。例如 "(man, shirt)" 频繁与 "wearing" 搭配，而 "(man, boots)" 极少出现。模型容易学到 `主客体→谓词` 的虚假相关（spurious correlation），导致罕见的 `<sub, obj>` 对预测错误。

**现有方法的缺陷**：多数方法只处理类不均衡（重采样、重加权、因果推理），忽视语境不均衡。从贝叶斯角度，SGG 关系分类可分解为：

$$P(r=c|z_c,z_e) \propto \underbrace{P(r=c)}_{\text{class imbalance}} \cdot \underbrace{P(z_e|r=c,z_c)}_{\text{context imbalance}}$$

## Method

### 核心架构

EICR 包含两个核心模块，以流水线方式工作：

1. **环境不变学习（Environment-Invariant Learning, EIL）** → 消除语境偏置
2. **类均衡课程学习（Class-Balanced Curriculum Learning）** → 消除类别偏置

### 环境不变学习（EIL）

基于 Invariant Risk Minimization (IRM) [Arjovsky+ 2019]，构造三种具有不同谓词类别分布的学习环境（learning environments）：

| 环境 | 构造方式 | 作用 |
|------|----------|------|
| **Normal 环境** | 保持原始数据中谓词类别的原始分布 | 保留头部类别的通用模式 |
| **Balanced 环境** | 基于中位数频率的重采样（对高于中位数的类下采样），使各类别样本量趋于均衡 | 消除主客体数量差异 |
| **Over-Balanced 环境** | 在 Balanced 环境基础上额外施加重加权（loss 中权重 $w_i=1/n_i$），使采样的概率与类别大小负相关 | 强制模型关注尾部类别 |

目标函数（IRM）：

$$\min_g \sum_{e \in \mathcal{E}} R^e(I, r; f(\cdot), g(\cdot)) \quad \text{s.t.} \quad g \in \arg\min_g R^e \text{ for all } e \in \mathcal{E}$$

实践中使用梯度范数惩罚项：

$$\min_{\Phi} \sum_{e \in \mathcal{E}} R^e(\Phi) + \lambda \cdot \|\nabla_{w|w=1.0} R^e(w \cdot \Phi)\|^2$$

通过约束关系分类器在不同语境分布下同样最优，消除语境偏置。

### 类均衡课程学习

在 EIL 消除语境偏置后，使用课程学习策略处理类不均衡。通过权衡因子 $\lambda$ 调节 Normal 环境和 Over-Balanced 环境之间的学习权重：

$$\lambda = \begin{cases}
\lambda_{max} & \text{if } t \leq T \\
\max(H(t), \lambda_{min}) & \text{if } T < t \leq 2T \\
\lambda_{min} & \text{if } t > 2T
\end{cases}$$

其中 $H(t) = \frac{2T-t}{T}(\lambda_{max}-\lambda_{min})$ 随时间线性递减。

**三个学习阶段**：

1. **阶段 1** ($t \le T$)：$\lambda=\lambda_{max}$，主要关注 Normal 环境，学习头部类别的通用模式
2. **阶段 2** ($T < t \le 2T$)：$\lambda$ 逐渐从 $\lambda_{max}$ 递减到 $\lambda_{min}$，学习焦点从 Normal 环境转移到 Over-Balanced 环境，逐步学习细粒度的尾部谓词
3. **阶段 3** ($t > 2T$)：$\lambda=\lambda_{min}$，避免对头部模式的过拟合

联合损失：

$$\mathcal{R}_{hybrid} = \lambda \cdot \mathcal{R}_{norm} + (1-\lambda) \cdot \mathcal{R}_{over} + \mathcal{R}_{balanced}$$

### 实现细节

- Backbone：预训练 Faster-RCNN (ResNeXt-101-FPN)
- 词嵌入：GloVe
- 优化器：Adam，momentum=0.9，初始 lr=0.001
- Batch size：4
- 训练步数：120,000 steps，T=30,000
- $\lambda_{max}=0.9$，$\lambda_{min}=0.1$
- 硬件：单卡 RTX 2080 Ti

## Experiments

### 数据集

- **Visual Genome (VG)**：标准 SGG benchmark，150 个高频物体类别 + 50 个谓语类别
- **GQA**：大规模视觉语言数据集，GQA200 设 200 物体类 + 100 谓语类
- 两者均按 70% 训练 / 30% 测试划分

### 评估任务

1. **Predicate Classification (PredCls)**：给定 GT 框和标签，预测谓词
2. **Scene Graph Classification (SGCls)**：给定 GT 框，预测标签和谓词
3. **Scene Graph Detection (SGDet)**：检测所有实体及其关系

### 评估指标

- **Recall@K (R@K)**：top-K 预测中 GT 三元组的比例（偏向头部）
- **mean Recall@K (mR@K)**：各类别 R@K 的平均值（偏向尾部）
- **F@K**：R@K 和 mR@K 的调和平均（综合衡量）
- **mT@K**：不同语境（不同 `<sub,obj>` 组合）的均值召回率（专门衡量语境均衡）

### Baseline 方法

**模型无关方法（Plug-and-Play）**：TDE、PCPL、EBM、NICE、IETrans、CogTree、GCL

**专用 SGG 模型**：IMP、GPS-Net、BGNN、DT2-ACBS、SHA-GCL、Motifs、VCTree、Transformer

## Results

### VG 数据集 — PredCls 任务（Table 1 节选）

| Model | R@50/100 | mR@50/100 | F@50/100 |
|-------|----------|-----------|----------|
| Motifs (baseline) | 65.2/67.0 | 14.8/16.1 | 24.1/26.0 |
| Motifs + TDE | 46.2/51.4 | 25.5/29.1 | 32.9/37.2 |
| Motifs + NICE | 55.1/57.1 | 29.9/32.3 | 38.8/41.3 |
| Motifs + IETrans | 48.6/50.5 | 35.8/39.1 | 41.2/44.1 |
| **Motifs + EICR** | 55.3/57.4 | **34.9/37.0** | **42.8/45.0** |
| VCTree (baseline) | 65.4/67.2 | 16.7/18.2 | 26.6/28.6 |
| VCTree + TDE | 47.2/51.6 | 25.4/28.7 | 33.0/36.9 |
| VCTree + NICE | 55.0/56.9 | 30.7/33.0 | 39.4/41.8 |
| VCTree + IETrans | 48.0/49.9 | 37.0/39.7 | 41.8/44.2 |
| **VCTree + EICR** | 56.0/57.9 | **35.6/37.9** | **43.6/45.8** |
| Transformer (baseline) | 63.6/65.7 | 19.7/19.6 | 27.9/30.2 |
| Transformer + IETrans | 49.0/50.8 | 35.0/38.0 | 40.8/43.5 |
| **Transformer + EICR** | 52.8/54.7 | **36.9/39.1** | **43.5/45.6** |

### VG 数据集 — SGCls 和 SGDet（Table 1 节选）

**SGCls**:
| Model | R@50/100 | mR@50/100 | F@50/100 |
|-------|----------|-----------|----------|
| **VCTree + EICR** | 39.4/40.5 | **26.2/27.4** | **32.8/33.9** |
| **Transformer + EICR** | 31.4/32.4 | **21.6/22.4** | **25.6/26.5** |

**SGDet**:
| Model | R@50/100 | mR@50/100 | F@50/100 |
|-------|----------|-----------|----------|
| **VCTree + EICR** | 26.0/30.1 | **15.2/17.5** | **19.2/22.1** |
| **Transformer + EICR** | 23.7/27.7 | **17.3/19.7** | **20.0/23.0** |

**核心提升**：应用 EICR 后，VCTree 在三个任务上的 mR@50/100 平均提升超过 **14%**，F@50/100 平均提升超过 **12%**。

### GQA 数据集（Table 2）

| Model | PredCls mR@50/100 | SGCls mR@50/100 | SGDet mR@50/100 |
|-------|-------------------|-----------------|-----------------|
| Motifs + GCL | 36.7/38.1 | 17.3/18.1 | 16.8/18.8 |
| **Motifs + EICR** | **36.3/38.0** | **17.2/18.2** | **16.0/18.0** |
| VCTree + GCL | 35.4/36.7 | 17.3/18.0 | 15.6/17.8 |
| **VCTree + EICR** | **35.9/37.4** | **17.8/18.6** | **14.7/16.3** |

在 GQA 上 EICR 与 SOTA 的 GCL 方法性能相当或略优，验证了跨数据集泛化能力。

### 语境均衡效果（Table 9） — mT@50/100

| Model | PredCls mT@50/100 | SGCls mT@50/100 | SGDet mT@50/100 |
|-------|-------------------|-----------------|-----------------|
| Motifs | 7.9/8.8 | 3.1/3.4 | 2.0/2.4 |
| **Motifs + EICR** | **17.8/19.2** | **8.3/8.9** | **5.8/6.6** |
| VCTree | 8.4/9.3 | 4.3/4.8 | 1.7/2.1 |
| **VCTree + EICR** | **18.3/19.7** | **11.6/12.4** | **5.8/6.7** |
| Transformer | 9.6/10.6 | 3.3/3.7 | 2.4/2.9 |
| **Transformer + EICR** | **18.8/20.3** | **8.9/9.4** | **6.7/7.6** |

mT@K 指标直接衡量不同主客体语境的召回率均衡程度，EICR 在所有基线上实现显著提升（2-3x），证明语境不均衡确实得到缓解。

### 消融实验（Table 5）— 课程学习策略

| Setting | SGCls R@50/100 | mR@50/100 | F@50/100 |
|---------|---------------|-----------|----------|
| w/o-Curriculum Schedule | 39.3/40.1 | 15.4/16.1 | 22.1/23.0 |
| w/o-Norm Schedule | 39.2/40.0 | 14.8/15.8 | 21.5/22.7 |
| w/o-Over Schedule | 35.6/36.4 | 18.1/19.1 | 24.0/25.1 |
| **w-Curriculum Schedule** | **34.5/35.4** | **20.8/21.8** | **25.9/27.0** |

课程学习策略在 mR@50 上提升超过 5 点（15.4→20.8），F@50 提升近 4 点（22.1→25.9），验证了阶段式聚焦尾部的重要效果。

### 与其他去偏策略的对比（Table 8）

| Method | PredCls R@50/100 | mR@50/100 | F@50/100 |
|--------|-----------------|-----------|----------|
| BBN (resampling) | 56.0/57.7 | 19.4/21.3 | 28.8/31.1 |
| Reweight | 54.7/56.5 | 17.3/18.6 | 26.3/28.0 |
| **EICR** | 55.3/57.4 | **34.9/37.0** | **42.8/45.0** |

EICR 的 mR@50 (34.9) 远超纯重采样策略 BBN (19.4) 和权重调整 Reweight (17.3)，证明语境偏置的消除为尾部性能带来质的飞跃。

### IRM 项的影响（Table 6）

| Setting | PredCls R@50/100 | mR@50/100 | F@50/100 |
|---------|-----------------|-----------|----------|
| w/o IRM term | 52.4/54.4 | 35.4/37.4 | 42.2/44.3 |
| **w/ IRM term** | **55.3/57.4** | 34.9/37.0 | **42.8/45.0** |

IRM 正则项提升 R@50 (52.4→55.3) 和 F@50 (42.2→42.8)，主要贡献是对头部类性能的恢复。

### $\lambda_{max}$ 参数分析（Table 7）

| $\lambda_{max}$ | SGCls R@50/100 | mR@50/100 | F@50/100 |
|:---------------:|---------------|-----------|----------|
| w/o $\lambda_{max}$ | 39.3/40.1 | 15.4/16.1 | 22.1/23.0 |
| 0.7 | 37.1/38.0 | 18.0/19.0 | 24.3/25.2 |
| 0.8 | 36.2/37.1 | 19.1/20.0 | 25.0/26.0 |
| **0.9** | **34.5/35.4** | **20.8/21.8** | **25.9/27.0** |
| 0.99 | 27.6/28.7 | 20.9/21.9 | 23.8/24.8 |

$\lambda_{max}=0.9$ 实现最佳 F@K 权衡。$\lambda_{max}$ 越大，模型越关注尾部（mR 更高），但过度关注尾部（0.99）会导致 R 大幅下降。

## Analysis

### 创新点

1. **首次提出语境不均衡（Context Imbalance）**：不同于已有的类不均衡，分析了主客体对与谓词之间的虚假相关关系，并给出形式化定义
2. **环境不变学习 + 课程学习的两阶段去偏策略**：先用 IRM 消除语境偏置，再通过课程学习消除类别偏置
3. **即插即用**：可嵌入 Motifs、VCTree、Transformer 等不同架构的 SGG 模型

### 与同期方法的关系

| 维度 | EICR (本文) | NICE (ICCV'23) | IETrans (CVPR'22) | CFA (ICCV'23) |
|------|------------|----------------|-------------------|---------------|
| 处理语境不均衡 | ✅ 显式处理 | ❌ | ❌ | ❌ |
| 处理类不均衡 | ✅ 课程学习 | ✅ OOD检测 | ✅ 标签迁移 | ✅ 特征增强 |
| 即插即用 | ✅ | ✅ | ✅ | ✅ |
| 特征多样性增强 | ❌ | ❌ | ❌ | ✅ |

EICR 与 CFA 是同年 ICCV 的互补性工作：EICR 侧重**数据层面的不均衡消除**（通过构造环境和课程学习），CFA 侧重**特征层面的多样性增强**（通过特征替换和 mixup）。

### 局限

- 在 GQA 上的增益不如 VG 显著（GQA 的语境多样性更高，环境构造的区分度相对降低）
- 三个环境的构造需要额外的超参数调优（T, $\lambda_{max}$ 等）
- 在 PredCls 的 R@K 上，EICR 对比基线有时有所下降（通常在尾部提升大的同时头部有轻微衰退）

## Related Pages in This Wiki

- [Compositional Feature Augmentation for Unbiased Scene Graph Generation (CFA)](compositional-feature-augmentation-for-unbiased-scene-graph-generation.md) — 同届 ICCV 互补性去偏方法
