---
title: "Diff-VRD: Generalized Visual Relation Detection with Diffusion Models"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - visual-relation-detection
  - diffusion-models
  - generalized-vrd
  - hoi-detection
  - scene-graph-generation
  - generative-vrd
  - tcsvt-2024
raw_sources:
  - ../../../sources/scene-graph/2025-06-09-generalized-visual-relation-detection-with-diffusion-models.pdf
  - ../../../sources/scene-graph/2025-06-09-generalized-visual-relation-detection-with-diffusion-models.txt
related_pages:
  - reltr-relation-transformer-scene-graph-generation.md
  - is-ggt-iterative-scene-graph-generation-with-generative-transformers.md
  - hiker-sgg-hierarchical-knowledge-enhanced-robust-sgg.md
  - dsgg-dense-relation-transformer-end-to-end-scene-graph-generation.md
  - ietrans-scene-graph-generation.md
evidence_level: full-paper
paper:
  title: "Generalized Visual Relation Detection with Diffusion Models"
  abbreviated: "Diff-VRD"
  authors:
    - Kaifeng Gao
    - Siqi Chen
    - Hanwang Zhang
    - Jun Xiao
    - Yueting Zhuang
    - Qianru Sun
  year: 2024
  venue: "IEEE Transactions on Circuits and Systems for Video Technology (TCSVT)"
  arxiv: "2504.12100"
  doi: ~
  code: ~
classification:
  label: "Diff-VRD"
  task:
    - Generalized Visual Relation Detection (VRD)
    - Human-Object Interaction (HOI) Detection
    - Scene Graph Generation (SGG)
  method_family: "Diffusion-based Generative Model"
  modality: Image
  datasets:
    - HICO-DET
    - V-COCO
    - Visual Genome (VG)
  metrics:
    - Recall@K (R@K)
    - mean Recall@K (mR@K)
    - Text-to-Image (T2I) Retrieval Recall@K
    - SPICE Precision-Recall Curve
---

# Generalized Visual Relation Detection with Diffusion Models

## Citation

Kaifeng Gao, Siqi Chen, Hanwang Zhang, Jun Xiao, Yueting Zhuang, and Qianru Sun. "Generalized Visual Relation Detection with Diffusion Models." IEEE TCSVT, 2024. arXiv:2504.12100.

## One-Sentence Contribution

将视觉关系建模为连续嵌入（而非离散分类），通过扩散模型实现**超越预定义类别标签**的广义视觉关系检测（Diff-VRD），并引入 T2I Retrieval 和 SPICE PR Curve 两个代理指标以评估生成的关系多样性。

## Problem Setting

**现有 VRD 的局限**：所有现有 VRD 模型都受限于预定义关系类别，忽略了视觉关系的语义模糊性——同一视觉交互可从不同视角用多个谓词描述（如 "ride" 在体育视角也可描述为 "race"，在空间位置视角描述为 "sit on"）。

**Diff-VRD 定位**：将 VRD 重构为条件生成问题，在连续嵌入空间中生成关系，再通过 rounding 和 matching 阶段映射到词汇。模型可以生成训练数据集中未标注的合理关系。

**广义 VRD 评估挑战**：传统 mAP 无法衡量超出标注范畴的关系预测。为此引入两个代理任务：
- **T2I Retrieval**：将检测到的三元组拼接成描述，用 VLM 做零样本文到图检索
- **SPICE PR Curve**：借鉴图像描述评估，对排序的三元组计算 PR 曲线

## Method

### 整体架构

![架构：Embedding 步骤 → 扩散-去噪过程 → Rounding 步骤 → Matching 步骤](...)

分成三个阶段：

1. **Embedding 步骤**（`q_ϕ(x0|v)`）：将离散关系词 `v` 投影到连续潜在嵌入 `x0`，类似 VAE 编码器
2. **扩散-去噪过程**（`p_θ(x0|xt, t, y)`）：基于 Transformer Decoder 的扩散模型，以 CLIP 提取的主体-客体视觉和文本嵌入 `y` 为条件信号，通过交叉注意力注入
3. **Rounding 步骤**（`p_θ(v|x0)`）：将去噪后的嵌入 `x0` 通过语义相似度匹配到词汇表 `V` 中的关系词
4. **Matching 步骤**：将生成的关系序列通过匈牙利算法分配给检测到的主体-客体对

### 关键设计

- **条件信号注入**：使用 CLIP 提取每个主体-客体对的视觉和文本嵌入，拼接后通过编码器 `τ_θ` 和交叉注意力注入扩散模型
- **词汇表构建**：构建包含 4858 个关系词/短语的大词汇表 `V`（从图像描述中收集视觉可表达的动词+场景图解析的谓词），覆盖全部标注数据集的关系类别
- **训练目标**：`L_simple + λL_match`，其中 `L_simple` 为简化的扩散损失，`L_match` 为辅助匹配损失（BCE），通过匈牙利算法建立生成关系与主体-客体对的对应关系
- **推理**：采用 DDIM scheduler，50 步去噪步骤

### 作为增强模块

Diff-VRD 还可应用于现有 VRD 模型之上：将检测到的关系投影为嵌入 → 进行 T' 步去噪 → 生成新的关系。在 SGG 模型 IETrans 上验证。

## Experiments

### 数据集

| 数据集 | 用途 | 训练/测试规模 | 标注 |
|--------|------|-------------|------|
| HICO-DET | HOI 检测 | 37,633 训练 / 9,546 测试 | 117 互动类别，80 对象类别 |
| V-COCO | HOI 检测 | 2,533 训练 / 2,867 验证 / 4,946 测试 | 26 互动类别，80 对象类别 |
| Visual Genome (VG) | SGG | 70% 训练 / 30% 测试 | 150 对象类别，50 谓词类别 |

### 评估协议

- **HOI Detection**：Recall@K（R@K），因生成的关系可能超出标注，mAP 不适用
- **SGG**：PredCls / SGCls / SGGen 的 R@K 和 mR@K
- **T2I Retrieval**：用 X-VLM 或 CLIP 做零样本检索，Recall@1/5/10
- **SPICE PR Curve**：对预测三元组计算 SPICE 得分的 PR 曲线

### Baseline 方法

#### HOI Detection
- 闭集方法：EoID, CDN, UPT, GEN-VLKT
- 开集方法（适配大词汇表 V）：GEN-VLKT (Cr/V), THID (Cr/V), CMMP
- CLIP baseline（直接基于 CLIP 相似度分类）

#### SGG
- VCTree, Motif, TDE, CogTree, IETrans

### 训练设置

- **骨干**：CLIP 编码器（视觉+文本），Transformer Decoder
- **解码器配置**：6 层，8 头注意力，512 隐藏维度，FFN 2048
- **训练**：4×2080Ti GPU，batch size 128，lr 1e-4，40,000 步
- **扩散步骤**：T=2000（训练），50 步 DDIM（推理）
- **序列长度**：L=32
- **损失权重**：λ=1.0, κ=0.05

### 消融实验

1. **Matching 监督**：匹配监督改善 HOI Detection（R@5: 16.14% → 21.83%），但降低 T2I 检索（R@1: 11.37% → 8.67%），因监督引导模型偏向领域内关系
2. **序列长度 L**：更大 L 提升性能（R@5: L=16→21.38%, L=32→21.83%, L=48→22.60%），但增加计算开销
3. **K 值（增强模式）**：增大每对生成的关系数 K，提升多样性但降低传统 SGG 指标

## Results

### HOI Detection on HICO-DET

**闭集设定（Training/Testing 同为 Cr，即 117 类标注谓词）：**
| 方法 | R@5 | R@10 | R@15 |
|------|-----|------|------|
| EoID | 47.08 | 57.91 | 62.51 |
| CDN | 48.84 | 59.03 | 63.63 |
| UPT | 52.30 | 64.35 | 69.71 |
| GEN-VLKT | 53.28 | 64.35 | 69.14 |
| Diff-VRD† (V/Cr) | 25.23 | - | - |

**开集设定（Training V / Testing V，即 4858 类大词汇表）：**
| 方法 | R@5 | R@10 | R@15 |
|------|-----|------|------|
| GEN-VLKT (Cr/V) | 0.71 | 1.22 | 1.59 |
| THID (Cr/V) | 1.99 | 3.32 | 4.36 |
| CLIP (V/V) | 1.21 | 2.72 | 3.08 |
| **Diff-VRD (V/V)** | **17.28** | **21.52** | **23.49** |

> Diff-VRD 在开集设定下大幅超越开集 baseline（R@5: 17.28% vs. 1.99% THID, +768%）

### T2I Retrieval on HICO-DET

**与 SOTA HOI 方法对比（用 CLIP 做检索模型，除另有说明）：**
| 方法 | R@1 | R@5 | R@10 |
|------|-----|-----|------|
| GEN-VLKT (Cr/V) | 8.96 | 28.13 | 41.32 |
| THID (Cr/V) | 7.91 | 23.79 | 35.69 |
| CMMP (Cr/V) | 6.66 | 20.87 | 30.36 |
| CLIP (V/V) | 16.00 | 41.32 | 57.67 |
| **Diff-VRD (V/V, CLIP)** | 11.13 | 32.00 | 45.07 |
| **Diff-VRD (V/V, X-VLM)** | **15.12** | **39.03** | **53.63** |

### T2I Retrieval on HICO-DET and V-COCO（一致对象检测）

| 方法 | HICO-DET R@1 | HICO-DET R@5 | HICO-DET R@10 | V-COCO R@1 | V-COCO R@5 | V-COCO R@10 |
|------|:---:|:---:|:---:|:---:|:---:|:---:|
| GT (ground truth) | 7.97 | 24.97 | 37.86 | 8.60 | 26.27 | 37.71 |
| GT-Object | 4.51 | 16.82 | 27.43 | 7.70 | 24.34 | 34.31 |
| UPT* | 7.20 | 22.03 | 33.76 | 7.36 | 22.87 | 35.33 |
| **Diff-VRD*** | **11.13** | **32.00** | **45.07** | **10.07** | **28.42** | **44.05** |

> Diff-VRD 在相同对象检测结果下大幅超越 UPT（HICO-DET R@1: 11.13% vs. 7.20%, +54.6%），甚至超越了 GT 标注的检索结果（7.97%），说明模型预测了大量合理但未标注的关系。

### SGG on VG — Diff-VRD 作为 IETrans 增强

**PredCls：**
| 方法 | R@50 | R@100 | mR@50 | mR@100 |
|------|:----:|:-----:|:-----:|:------:|
| VCTree | 64.5 | 66.5 | 16.3 | 17.7 |
| Motif | 64.0 | 66.0 | 15.2 | 16.2 |
| TDE† | 46.2 | 51.4 | 25.5 | 29.1 |
| CogTree† | 35.6 | 36.8 | 26.4 | 29.0 |
| IETrans† | 48.6 | 50.5 | 35.8 | 39.1 |
| **IETrans† + Diff-VRD** | 47.9 | 52.0 | 33.0 | 38.0 |

**SGCls：**
| 方法 | R@50 | R@100 | mR@50 | mR@100 |
|------|:----:|:-----:|:-----:|:------:|
| VCTree | 39.3 | 40.2 | 8.9 | 9.5 |
| Motif | 38.0 | 38.9 | 8.7 | 9.3 |
| TDE† | 27.7 | 29.9 | 13.1 | 14.9 |
| CogTree† | 21.6 | 22.2 | 14.9 | 16.1 |
| IETrans† | 29.4 | 30.2 | 21.5 | 22.8 |
| **IETrans† + Diff-VRD** | 29.5 | 31.5 | 20.0 | 22.7 |

**SGGen：**
| 方法 | R@50 | R@100 | mR@50 | mR@100 |
|------|:----:|:-----:|:-----:|:------:|
| VCTree | 30.2 | 34.6 | 6.7 | 8.0 |
| Motif | 31.0 | 35.1 | 6.7 | 7.7 |
| TDE† | 16.9 | 20.3 | 8.2 | 9.8 |
| CogTree† | 20.0 | 22.1 | 10.4 | 11.8 |
| IETrans† | 23.5 | 27.2 | 15.5 | 18.0 |
| **IETrans† + Diff-VRD** | 21.0 | 25.5 | 13.3 | 16.8 |

**T2I Retrieval on VG（增强模式）：**
| 方法 | R@1 | R@5 | R@10 |
|------|:---:|:---:|:----:|
| CLIP | 9.20 | 21.35 | 28.64 |
| IETrans | 12.12 | 28.49 | 37.73 |
| **IETrans + Diff-VRD** | **17.72** | **36.71** | **46.52** |

> 在 T2I Retrieval 上，IETrans+Diff-VRD 提升显著（R@1: 12.12% → 17.72%, +46.2%），证明了 Diff-VRD 作为增强模块生成更丰富关系描述的能力。

### 关系多样性

在 HICO-DET 测试集上的 diversity 评估（以 SPICE 解析的关系为 ground truth）：
- Diff-VRD 正确识别的 ground-truth 关系数量远超 UPT、GEN-VLKT 和 CLIP baseline
- CLIP 虽然预测类别最多（86,884 种 predicate-object 组合），但精度极低

## Limitations

1. **纯视觉判断问题**：在某些情况下，模型基于纯视觉信息而非交互信息做出预测（如 "person booze wine glass"），原因是条件特征仅关注对象视觉特征而忽略上下文
2. **闭集 SGG 指标下降**：作为增强模块时，因 Diff-VRD 为每对生成多个谓词（非单一 ground truth 标注），传统 SGG 的 recall/mR 指标下降
3. **大词汇表训练下的闭集评估不足**：用大词汇表 V 训练但用窄词汇表 Cr 测试时，模型性能显著下降（因学习到的语义歧义信息被丢失）

## Reusable Claims

> **Claim**: 将 VRD 从离散分类重构为连续空间中的条件生成问题，可以实现超越预定义类别的广义视觉关系检测。
> **Evidence**: Diff-VRD 在 V/V 设定下 R@5=17.28%（HICO-DET），T2I Retrieval 超越 GT 标注（R@1: 11.13% vs. 7.97%）。
> **Scope**: HOI Detection + SGG，HICO-DET / V-COCO / VG
> **Confidence**: high

> **Claim**: 扩散模型的生成能力可有效增强现有 SGG 模型的关系多样性，T2I Retrieval 是评估这种多样性的有效指标。
> **Evidence**: IETrans+Diff-VRD 将 VG T2I Retrieval R@1 从 12.12% 提升至 17.72%（+46.2%）。
> **Scope**: SGG 增强
> **Confidence**: high

> **Claim**: 匹配监督会提升传统 VRD 指标但损害关系多样性，两者存在 trade-off。
> **Evidence**: 添加匹配监督后 HOI R@5 从 16.14% 升至 21.83%，但 T2I R@1 从 11.37% 降至 8.67%。
> **Scope**: HICO-DET
> **Confidence**: medium

## Connections

- 与 RelTR、DSGG 等 DETR-based SGG 方法相比，Diff-VRD 首次将扩散模型引入关系检测领域
- 与 IS-GGT（生成式 Transformer）共享"生成式"范式，但使用扩散过程而非自回归生成
- 与 SG-Adapter（文本到图像的场景图引导生成）互补：Diff-VRD 提取关系，SG-Adapter 消费关系
- 匹配阶段借鉴了 DETR 的匈牙利匹配思想
- 嵌入-去噪-取整流程类似 Bit Diffusion，但面向视觉关系而非图像生成

## Open Questions

1. 条件特征仅使用对象级别特征，忽略上下文信息——改进条件特征设计能否提升细粒度关系辨别能力？
2. 词汇表 V 的构建（4858 个词/短语）是否最优？更大或更小的词汇表如何影响性能与多样性？
3. SPICE PR Curve 评估的标准化：如何建立广义 VRD 评估的统一协议？
4. Diff-VRD 的推理速度（50 步 DDIM）能否通过蒸馏或更少采样步数加速？

## Provenance

- **原始文件**：raw/sources/2025-06-09-generalized-visual-relation-detection-with-diffusion-models.pdf (8.1 MB, 15 pages)
- **提取文本**：raw/sources/2025-06-09-generalized-visual-relation-detection-with-diffusion-models.txt (77,593 chars, 2,101 lines)
- **arXiv**: 2504.12100v1 (2025-04-16)
- **发表**：IEEE Transactions on Circuits and Systems for Video Technology (TCSVT), 2024
- **evidence_level**: full-paper
