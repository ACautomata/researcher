---
title: "Leveraging Predicate and Triplet Learning for Scene Graph Generation"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - scene-graph-generation
  - long-tail
  - dual-granularity
  - knowledge-transfer
  - CVPR-2024
source_pages: []
raw_sources:
  - ../../../sources/scene-graph/2024-06-09-leveraging-predicate-and-triplet-learning-for-sgg.pdf
  - ../../../sources/scene-graph/2024-06-09-leveraging-predicate-and-triplet-learning-for-sgg.txt
related_pages:
  - PE-Net
paper:
  title: "Leveraging Predicate and Triplet Learning for Scene Graph Generation"
  authors: ["Jiankai Li", "Yunhong Wang", "Xiefan Guo", "Ruijie Yang", "Weixin Li"]
  year: 2024
  venue: "CVPR 2024"
  arxiv: null
  doi: null
  code: "https://github.com/jkli1998/DRM"
  project: null
classification:
  label: SGG
  task: ["Scene Graph Generation"]
  method_family: ["Dual-granularity Relation Modeling (DRM)", "Dual-granularity Knowledge Transfer (DKT)"]
  modality: ["image"]
  datasets: ["Visual Genome (VG150)", "Open Image V6", "GQA200"]
  metrics: ["Recall@K", "mean Recall@K", "wmAP"]
evidence_level: full-paper
---

# Leveraging Predicate and Triplet Learning for Scene Graph Generation

## Citation

> Jiankai Li, Yunhong Wang, Xiefan Guo, Ruijie Yang, Weixin Li. "Leveraging Predicate and Triplet Learning for Scene Graph Generation." *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*, 2024.
>
> 代码：<https://github.com/jkli1998/DRM>

## One-Sentence Contribution

提出 Dual-granularity Relation Modeling (DRM) 网络，联合粗粒度谓词级和细粒度三元组级关系建模，并通过 Dual-granularity Knowledge Transfer (DKT) 策略将头部谓词/三元组的模式多样性迁移至尾部类别，缓解 SGG 长尾问题。

## Problem Setting

- **任务**：Scene Graph Generation (SGG) —— 从图像中检测实体并预测 <subject, predicate, object> 关系三元组。
- **核心挑战**：
  1. 同一谓词在不同 subject-object 对中视觉变化巨大（如 "eating" 在 <elephant, eating, leaf> vs <man, eating, pizza> 中差异显著），直接建模谓词级表征困难。
  2. 长尾分布：尾部谓词样本和三元组类型有限，模式多样性不足。
- **观察**：同一三元组内的视觉变化相对较小，特定三元组中共享某些关系线索；头部谓词/三元组蕴含丰富的模式多样性可用于尾部。

## Method

### 整体架构

DRM 网络由两阶段构成（图3）：
1. **Stage 1：谓词与三元组线索学习** — 并行提取粗粒度谓词线索和细粒度三元组线索，受双重粒度约束正则化。
2. **Stage 2：双重粒度知识迁移与微调** — 将头部类的特征分布方差迁移至尾部，生成合成样本，微调关系分类器。

### 骨干网络

- **Proposal Network**：预训练 Faster RCNN (ResNeXt-101-RPN)，生成 N 个实体及其视觉特征、标签预测和空间特征。
- **Entity Encoder**：4 层 Hybrid Attention (HA)，含 Self-Attention 和 Cross-Attention 单元，融合语义特征到实体表征。

### 谓词线索建模 (Predicate Cue Modeling)

- 使用 2 层 Hybrid Attention 模块 `Enc_prd`，捕获跨不同 subject-object 对的谓词级线索。
- 谓词表示 `p_{i,j}` 初始化为 union feature `u_{i,j}`。
- Self-Attention 建模谓词和实体上下文；Cross-Attention 捕获实体与谓词间依赖。

### 三元组线索建模 (Triplet Cue Modeling)

- 使用 2 层 Hybrid Attention 模块 `Enc_tpt`，捕获特定 subject-object 对下的细粒度三元组线索。
- 三元组表示 `t_{i,j}` 初始化为 [subject, predicate, object] 的拼接。
- 融合视觉和语义上下文信息。

### 双重粒度约束 (Dual-Granularity Constraints)

- 对谓词表征施加谓词类别感知的监督对比学习损失 `L_p`，拉近同类谓词、推开异类谓词。
- 对三元组表征施加三元组类别感知的监督对比学习损失 `L_t`，拉近同类三元组、推开异类三元组。
- 防止两分支退化为单一粒度。

### 场景图预测

- 关系分类器使用两个全连接层集成粗粒度 `p'` 和细粒度 `t'` 线索。
- 总损失：`L = λ_e L_e + λ_r L_r + λ_p L_p + λ_t L_t`

### 双重粒度知识迁移 (Dual-granularity Knowledge Transfer, DKT)

1. **分布计算**：对每个谓词/三元组类别，假设特征服从多维高斯分布，计算均值 μ 和协方差 σ。
2. **知识迁移**：对每个尾部类别 i，基于类中心欧氏距离找到最相似头部类别 j，将头部类别的方差加权迁移至尾部：
   `σ'_i = (N_i/Q_i)·σ_i + (1-N_i/Q_i)·Σ_j α_{i,j}·σ_j`
3. **合成样本**：从校准后的分布 `N(μ_i, σ'_i)` 采样生成尾部类别合成样本。
4. **微调**：欠采样头部谓词形成平衡数据集，结合真实样本和合成样本微调关系分类器。

## Experiments

### 实验设置

| 项目 | 配置 |
|------|------|
| 数据集 | VG150（150 物体类、50 谓词类；70% 训练/30% 测试/5K 验证） |
| | Open Image V6（301 物体类、31 谓词类；126,368 训练/1,183 验证/5,322 测试） |
| | GQA200（200 物体类、100 谓词类） |
| 骨干网络 | Faster RCNN with ResNeXt-101-RPN |
| 词嵌入 | GloVe |
| 优化器 | SGD，初始学习率 1e-4，batch size 16 |
| 损失权重 | λ_r=3, λ_e=0.5, λ_t=0.1, λ_p=0.1 |
| 温度参数 | τ_p=0.2, τ_t=0.1 |
| 评估协议 | PredCls / SGCls / SGDet 三个子任务 |
| 指标 | Recall@K (R@K), mean Recall@K (mR@K), 以及 Open Image 专用指标 |
| 头尾划分 | 按样本数降序排列，前 50% 为头、后 50% 为尾 |

### Baseline 方法

- **有偏 SGG**: IMP, VTransE, MOTIFS, G-RCNN, VCTREE, GPS-Net, RU-Net, HL-Net, PE-Net, VETO
- **无偏 SGG**: TDE, CogTree, BPL-SA, VisualDS, NICE, PPDL, GCL/SHA+GCL, IETrans, INF, CFA, EICR, BGNN, SQUAT, CaCao

### 消融设置

- **谓词/三元组线索消融**：逐步加入谓词建模 (P)、三元组建模 (T)、数据增强 (A)、对比约束损失 (C)
- **DKT 消融**：仅谓词迁移 (DKT-P)、仅三元组迁移 (DKT-T)、双粒度迁移 (DKT)
- **训练方式**：Stage 1 预训练 → Stage 2 DKT + 微调

## Results

### Visual Genome (VG150) — 表 1

| 方法 | PredCls (mR@50/100) | SGCls (mR@50/100) | SGDet (mR@50/100) |
|------|---------------------|-------------------|-------------------|
| MOTIFS (有偏) | 14.6/15.8 | 8.0/8.5 | 5.5/6.8 |
| VCTREE (有偏) | 16.7/17.9 | 7.9/8.3 | 6.4/7.3 |
| PE-Net (CVPR'23, 有偏) | 23.1/25.4 | 13.1/14.8 | 8.9/11.0 |
| **DRM w/o DKT** | 23.3/25.6 | 13.5/14.6 | 9.0/11.2 |
| SHA+GCL (CVPR'22, 无偏) | 41.6/44.1 | 23.0/24.3 | 17.9/20.9 |
| CaCao (ICCV'23, 无偏) | 41.7/43.7 | 24.0/25.0 | 18.3/22.1 |
| **DRM** (无偏) | **47.1/49.6** | **27.8/29.2** | **20.4/24.1** |

**关键对比**：
- DRM 在 PredCls mR@100 上达到 **49.6**，超越 SHA+GCL (44.1) 5.5、CaCao (43.7) 5.9。
- DRM w/o DKT 在 R@100 上超过 PE-Net 2.0%（PredCls）、2.9%（SGCls）、2.0%（SGDet）。
- DRM 在 mR@100 上超越 SHA+GCL 5.5%（PredCls）、4.9%（SGCls）、3.2%（SGDet）。

### Open Image V6 — 表 2

| 方法 | R@50 | wmAP_rel | wmAP_phr | score_wtd |
|------|------|----------|----------|-----------|
| PE-Net (CVPR'23) | 76.5 | 36.6 | 37.4 | 44.9 |
| SQUAT (ICCV'23) | 75.8 | 34.9 | 35.9 | 43.5 |
| **DRM w/o DKT** | **75.9** | **40.5** | **41.4** | **47.9** |

- DRM w/o DKT 在 score_wtd 上达到 **47.9**，超越 PE-Net (44.9) 3.0 分。

### GQA200 — 表 3

| 方法 | PredCls (mR@50/100) | SGCls (mR@50/100) | SGDet (mR@50/100) |
|------|---------------------|-------------------|-------------------|
| SHA+GCL (CVPR'22, 无偏) | 41.0/42.7 | 20.6/21.3 | 17.8/20.1 |
| **DRM** (无偏) | **41.9/43.5** | **19.9/20.7** | **18.9/21.0** |

### 消融实验

**谓词/三元组线索消融 (VG150 PredCls, 表 4)**：

| P | T | A | C | R@50/100 | mR@50/100 |
|---|---|---|---|-----------|-----------|
| - | - | - | - | 56.5/60.4 | 15.5/17.4 |
| ✓ | - | - | - | 67.6/69.5 | 18.1/19.9 |
| - | ✓ | - | - | 67.6/69.8 | 20.5/22.5 |
| ✓ | ✓ | - | - | 69.3/71.3 | 20.8/22.8 |
| ✓ | ✓ | ✓ | ✓ | **70.2/72.1** | **23.3/25.6** |

- 谓词+三元组联合建模比单独使用任一粒度效果更好。
- 双重粒度约束（A+C）进一步贡献性能提升。

**DKT 消融 (表 5)**：

| 方法 | PredCls R@50/100 | PredCls mR@50/100 |
|------|------------------|-------------------|
| DRM w/o DKT | 70.2/72.1 | 23.3/25.6 |
| DKT-P | 42.4/44.2 | 45.0/47.3 |
| DKT-T | 40.4/42.2 | 46.1/48.7 |
| DKT (双粒度) | 43.9/45.8 | **47.1/49.6** |

- DKT 在 mR@K 上大幅提升（25.6 → 49.6 @ PredCls R@100），但 R@K 下降，原因是模型将原本模糊分类的头部谓词（如 "on"）正确归入更具体的尾部谓词（如 "sitting on"）。
- 双粒度迁移 (DKT) 优于仅谓词迁移 (DKT-P) 和仅三元组迁移 (DKT-T)。

## Limitations

1. **R@K 下降**：DKT 策略提升尾部性能的同时牺牲了头部 R@K，因为一些原被分类为头部类别的模糊样本被正确归入尾部。
2. **GQA200 上 SGCls 略低**：在 GQA200 的 SGCls 上，DRM 的 mR@K (19.9/20.7) 略低于 SHA+GCL (20.6/21.3)，表明在更复杂标签空间下三元组线索建模的优势有限。
3. **高斯分布假设**：DKT 假设特征服从高斯分布，可能不完全适用于某些复杂多模态类别。
4. **需要两阶段训练**：Stage 1 预训练 + Stage 2 分布计算和微调增加了训练复杂度。
5. **Open Image 仅报告 w/o DKT**：未在 Open Image 上评估 DKT 完整版本，无法验证跨数据集的有效性。

## Reusable Claims

- **Claim**: 在 SGG 中联合建模粗粒度谓词线索和细粒度三元组线索优于单独建模任一粒度。
  - **Evidence**: 表 4 消融，PredCls mR@100 从 17.4（基线）→ 19.9（仅谓词）/22.5（仅三元组）→ 25.6（联合+约束）。Scope: VG150。Confidence: high。

- **Claim**: 通过将头部谓词/三元组的特征分布方差迁移至尾部可以显著缓解 SGG 长尾问题。
  - **Evidence**: 表 1/5，DKT 将 PredCls mR@100 从 25.6 提升至 49.6。Scope: VG150。Confidence: high。

- **Claim**: 双重粒度知识迁移（谓词+三元组联合）优于单粒度迁移。
  - **Evidence**: 表 5，DKT (49.6) > DKT-P (47.3) > DKT-T (48.7) @ PredCls mR@100。Scope: VG150。Confidence: high。

- **Claim**: DKT 后 R@K 下降是由于模型将头部模糊样本正确归类到更具体的尾部谓词。
  - **Evidence**: 表 1/5 及论文 Section 4.3 的解释。Scope: VG150。Confidence: medium（作者推理，需手动验证）。

## Connections

- **PE-Net**：也使用 prototype 方式减少同类谓词内方差，但 DRM 额外建模三元组线索，粒度更细。
- **SHA+GCL**：使用混合专家 + 分组协作学习处理长尾，DRM 通过知识迁移方式不同。
- **CaCao**：使用视觉提示的语言模型，DRM 方法互补——前者侧重开放世界，后者侧重长尾平衡。
- **BGNN**：使用二部图消息传递，DRM 使用 Hybrid Attention 架构不同但目标类似。
- **GCL**：对比学习用于 SGG 长尾处理，DRM 使用监督对比学习做双粒度约束——在应用方式上不同。

## Open Questions

1. DKT 的高斯分布假设在更复杂/开放词汇 SGG 场景下是否稳健？
2. DKT 的 R@K 下降是否可以通过引入头部保护机制（如加权集成）来缓解？
3. 三元组线索建模如何推广到零样本 SGG 场景（未见过的三元组组合）？
4. Transformer-based 检测器（如 DETR）与 Hybrid Attention 结合的效果如何？
5. DKT 的头部/尾部划分阈值（50%/64 次）是否对数据集分布敏感？

## Provenance

- **提取文本**：`raw/sources/2024-06-09-leveraging-predicate-and-triplet-learning-for-sgg.txt`（1,569 行）
- **原始 PDF**：`raw/sources/2024-06-09-leveraging-predicate-and-triplet-learning-for-sgg.pdf`（6.5 MB）
- **分析范围**：全文精读，覆盖摘要、引言、方法（3.1-3.3）、实验（4.1-4.4）、结论
- **所有数字均直接来自论文表格和文本，未做额外计算**
