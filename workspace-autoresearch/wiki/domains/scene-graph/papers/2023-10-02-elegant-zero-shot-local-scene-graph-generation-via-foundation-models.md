---
title: "ELEGANT: Less is More — Toward Zero-Shot Local Scene Graph Generation via Foundation Models"
type: paper
domain: scene-graph
status: active
created: 2026-06-10
updated: 2026-06-10
tags:
  - scene-graph-generation
  - zero-shot
  - local-scene-graph
  - foundation-models
  - ELEGANT
  - co-calibration
  - ECLIPSE
  - arXiv-2023
raw_sources:
  - ../../../raw/sources/2023-10-02-less-is-more-zero-shot-local-scene-graph-generation-via-foundation-models.pdf
  - ../../../raw/sources/2023-10-02-less-is-more-zero-shot-local-scene-graph-generation-via-foundation-models.txt
related_pages:
  - visual-distant-supervision-scene-graph-generation.md
  - 2023-09-07-T-CAR-zero-shot-scene-graph-generation-triplet-calibration-reduction.md
evidence_level: full-paper
paper:
  title: "Less is More: Toward Zero-Shot Local Scene Graph Generation via Foundation Models"
  abbreviated: "ELEGANT"
  authors:
    - Shu Zhao
    - Huijuan Xu
  affiliations:
    - Pennsylvania State University
  year: 2023
  venue: arXiv preprint arXiv:2310.01356, Oct 2023 (Under Review)
  doi: null
  arxiv: "2310.01356"
  code: null
  url: null
classification:
  label: "Zero-Shot Local Scene Graph Generation via Foundation Model Collaboration"
  task:
    - Local Scene Graph Generation (LSGG)
    - Zero-Shot Scene Graph Generation
  method_family:
    - Foundation Model Collaboration
    - Co-Calibration (CoCa)
    - Open-Vocabulary Object Detection
    - LLM Commonsense Reasoning
    - VQA-Based Verification
  modality: Image
  datasets:
    - Visual Genome (VG)
    - GQA
  metrics:
    - ECLIPSE (Entity-level CLIPScore)
    - Recall@K (R@K)
    - Mean Recall@K (mR@K)
---

## Citation

```
Shu Zhao and Huijuan Xu. "Less is More: Toward Zero-Shot Local Scene Graph Generation via Foundation Models." 
arXiv preprint arXiv:2310.01356, 2023.
```

## One-Sentence Contribution

提出新任务 **Local Scene Graph Generation**（局部场景图生成）及其零样本框架 **ELEGANT**，利用基础模型协作（GroundedSAM + GPT-3.5 + BLIP2）实现无需标注的局部场景图生成，并引入开放词汇评估指标 **ECLIPSE** 突破闭集指标限制。

## Problem Setting

传统的场景图生成（SGG）生成图像中所有实体及其关系的全局场景图，存在两大问题：
1. **累积错误**：无关实体的噪声关系引入下游任务误差
2. **与人类认知不符**：人类认知遵循选择性视觉感知，聚焦任务相关区域

本文提出 **Local Scene Graph Generation（局部场景图生成）**——给定一个 subject，只提取与该 subject 相关的 objects 及其 relationships。例如对于指令"obtain the white cup"，只需生成 (cup, mounted on, shelf)，忽略无关实体。这与人类注意力分配机制（Folk et al., 1992）一致。

此外，现有零样本 SGG 方法依赖知识库或预定义标签空间，无法处理开放词汇场景。

## Method

### ELEGANT 框架

ELEGANT（zEro-shot Local scEne GrAph geNeraTion）由三个核心模块和 Co-Calibration 策略组成：

#### 1. 感知模块（Observer）
- **模型**：GroundedSAM（SAM + Grounding DINO 的组合）
- **功能**：开集目标检测与分割，识别与 subject 相关的 objects
- 输入 subject 后，GroundedSAM 检测图像中所有开放词汇对象作为候选 objects
- 注：SAM 本身是 class-agnostic 的，GroundedSAM 为其注入语义标签能力

#### 2. 推理模块（Thinker）
- **模型**：GPT-3.5-turbo（LLM）
- **功能**：利用 LLM 的常识推理能力为 (subject, object) 配对推断关系
- 通过 prompt 让 LLM 作为常识推理器，生成三元组候选
- 支持 open-vocabulary（开放词汇）和 closed-set（闭集）两种 prompt 模式
- 最终选用 GPT-3.5-Turbo，消融实验显示 OPT 系列因推理能力有限表现较差，LLaMA2/Vicuna 表现中等

#### 3. 验证模块（Verifier）
- **模型**：BLIP2（VQA 模型，可选 OPT/FlanT5 变体）
- **功能**：验证 thinker 提出的关系三元组是否与图像内容一致
- 将验证转化为结构化的 "is the {subject} {relationship} the {object}?" 的 yes/no 问题
- 最终选用 BLIP2 OPT 6.7B，优于 FlanT5 变体

#### 4. Co-Calibration 策略（CoCa）
- **动机**：LLM 不能直接接收视觉信息可能导致偏差，VQA 模型可能误解 LLM 的常识知识
- **机制**：
  1. 当 verifier 否定一个三元组时，要求 verifier 提供 rationale（推理理由）
  2. 将 rationale 提交给 thinker（LLM），询问"是否可以从 verifier 的 rationale 中推断出原三元组？"
  3. 如果 LLM 确认可以推断，则保留该三元组；否则丢弃
- **效果**：CoCa 恢复 5,012 个被 verifier 误判为负样本的三元组，R@10 从 23.64 提升至 30.27

### ECLIPSE 指标

**Entity-level CLIPScore（ECLIPSE）** 是本文提出的开放词汇评估指标：

1. 对每个三元组 (s, r_i, o_i)，根据 subject 和 object 的边界框生成掩码图像 I_i
2. 将三元组改写为 "The {s} is {r_i} the {o_i}"
3. 计算 CLIPScore(I_i, text)
4. 引入基于 log barrier function 的惩罚函数 P(|G|)，对过短或过长的预测施加惩罚（对过短预测惩罚更大）

$$
\text{ECLIPSE}(G) = P(|G|) \cdot \frac{1}{|G|} \sum_{i=1}^{|G|} \text{CLIPScore}(I_i, C_i)
$$

惩罚函数参数：µ = m* - 1（m* 为数据集的平均预测长度），α 控制惩罚强度（默认 0.01）。

## Experiments

### 数据集
- **Visual Genome**：26,443 张测试图像
- **GQA**：8,208 张测试图像（split 来自 Li et al. 2023b）
- 闭集评估沿用 VisualDS（20 个关系类别）和 RECODE（24 个关系类别）的标准

### Baseline 方法
- **VisualDS** (Yao et al., 2021, ICCV)：从知识库 Conceptual Captions 挖掘三元组，CLIP 验证
- **RECODE** (Li et al., 2023b, NeurIPS)：LLM 生成关系描述模板，CLIP 验证

### 评估设置
- **开放词汇评估**：ECLIPSE 指标
- **闭集评估**：Recall@K (R@K)、Mean Recall@K (mR@K)
- 对于闭集设置，使用 ground truth 目标检测结果进行公平比较

## Results

### 开放词汇评估（Visual Genome 测试集）

| Observer | Thinker | Verifier | ECLIPSE |
|----------|---------|----------|:-------:|
| Faster RCNN | GPT-3.5-Turbo | BLIP2 OPT 6.7B | 19.31 |
| GroundedSAM | OPT 2.7B | BLIP2 OPT 6.7B | 0.09 |
| GroundedSAM | OPT 6.7B | BLIP2 OPT 6.7B | 0.16 |
| GroundedSAM | LLaMA2 7B | BLIP2 OPT 6.7B | 19.01 |
| GroundedSAM | Vicuna 7B | BLIP2 OPT 6.7B | 20.41 |
| GroundedSAM | GPT-3.5-Turbo | BLIP2 FlanT5 XL | 20.97 |
| GroundedSAM | GPT-3.5-Turbo | BLIP2 FlanT5 XXL | 21.20 |
| GroundedSAM | GPT-3.5-Turbo | BLIP2 OPT 2.7B | 21.50 |
| **GroundedSAM** | **GPT-3.5-Turbo** | **BLIP2 OPT 6.7B** | **21.54** |

### 闭集评估（Visual Genome 测试集）

**与 VisualDS 比较（20 个关系类别）：**

| Method | R@10 | R@20 | R@50 | mR@10 | mR@20 | mR@50 |
|--------|:----:|:----:|:----:|:-----:|:-----:|:-----:|
| VisualDS | 27.72 | 33.22 | 38.21 | 16.32 | 20.49 | 24.94 |
| **ELEGANT** | **30.27** | **36.80** | **41.04** | **21.21** | **26.11** | **29.78** |

**与 RECODE 比较（24 个关系类别）：**

| Method | R@10 | R@20 | R@50 | mR@10 | mR@20 | mR@50 |
|--------|:----:|:----:|:----:|:-----:|:-----:|:-----:|
| RECODE | - | 10.60 | 18.30 | - | 10.70 | 18.70 |
| **ELEGANT** | **28.14** | **35.18** | **38.87** | **39.51** | **16.54** | **21.39** |

> 注：上表为 ELEGANT 对比 RECODE 的原始数据。mR@10 值为 39.51，但在 mR@20/mR@50 上低于 R@K，可能因为 mR 计算方式或类别统计差异。R@K 上 ELEGANT 全面超越 RECODE。

### CoCa 策略消融实验（Visual Genome 测试集）

| Method | R@10 | R@20 | mR@10 | mR@20 | E@0.1 | E@0.01 | E@0.001 | #Triplets |
|--------|:----:|:----:|:-----:|:-----:|:-----:|:------:|:-------:|:---------:|
| ELEGANT | 30.27 | 36.80 | 21.21 | 26.11 | 17.63 | 20.39 | 20.78 | 12,120 |
| - CoCa | 23.64 | 31.96 | 18.78 | 25.89 | 14.86 | 16.51 | 16.73 | 7,108 |

CoCa 策略恢复 5,012 个三元组（从 7,108 增加到 12,120），R@10 提升 28.0%。

### 下游任务：VQA（GQA testdev，1,000 samples）

| Method | Scene Graph Type | Accuracy |
|--------|:----------------:|:--------:|
| Baseline (BLIP2 FlanT5 XL) | — | 50.4 |
| Ours (Vicuna) | global | 51.9 |
| Ours (Vicuna) | **local** | **55.4** |
| Ours (GPT-3.5) | global | 54.2 |
| Ours (GPT-3.5) | **local** | **58.3** |

局部场景图在 VQA 上均优于全局场景图（+3.5~4.1%），且较基线提升 7.9%。

### 预测多样性分析

- **实体类别数量**：ELEGANT 591 vs VisualDS 150 vs RECODE 150（约 4x）
- **关系类别数量**：ELEGANT 1,813 vs VisualDS 20 vs RECODE 24（约 25x vs 闭集方法）
- **三元组类别数量**：ELEGANT 16,973 vs VisualDS 2,522（约 7x）

## Limitations

1. **推理耗时**：依赖多个基础模型级联调用（GroundedSAM + GPT-3.5 + BLIP2），推理时间长
   - 可作为伪标签生成器用于监督式 SGG 训练
2. **仅基于 IoU>0 配对**：仅当 subject 和 object 的 IoU 大于 0 时才推断关系，可能遗漏空间上不重叠但语义相关的配对
3. **未利用分割掩码**：GroundedSAM 可以生成分割掩码但本文仅使用边界框
4. **评估局限**：ECLIPSE 依赖 CLIP 模型，可能无法捕捉细粒度关系差异
5. **GPT-3.5 依赖**：核心推理能力依赖商业 API，成本、延迟和可复现性受限

## Reusable Claims

1. **局部场景图优于全局场景图**：在 VQA 下游任务中，local SG（58.3%）> global SG（54.2%）> 无 SG（50.4%），证实局部结构化信息更有利于推理。
2. **基础模型协作可实现零样本 SGG**：无需任何标注数据，通过观察-推理-验证三级流水线即可生成合理的场景图，ELEGANT 在闭集上超越 VisualDS 和 RECODE。
3. **Co-Calibration 跨模型知识校准有效**：让 LLM 作为"教师"诊断 VQA 模型的错误 rationale，可显著提升质量（R@10 +6.63）。
4. **开放词汇评估的必要性**：ELEGANT 发现 1,813 种关系类别（闭集方法仅 ~20-24 种），传统闭集指标无法评估这种丰富性。
5. **LLM 的常识推理是零样本 SGG 的关键**：GPT-3.5-Turbo 远超 OPT 系列，说明指令微调 LLM 的常识推理能力对关系推断至关重要。
6. **GroundedSAM 的开放词汇感知拓宽实体类别**：实体类别数 591 vs 150（闭集），提供更多样化的三元组候选。

## Connections

- **与 VisualDS (Yao et al., 2021, ICCV)**：两者均为零样本 SGG 方法。VisualDS 从知识库挖掘关系候选 + CLIP 验证；ELEGANT 用 LLM 推理关系 + BLIP2 验证 + CoCa 校准。ELEGANT 在 R@10 上提升 9.2%（30.27 vs 27.72）。
- **与 RECODE (Li et al., 2023b, NeurIPS)**：RECODE 用 LLM 为每个关系类别生成详细描述作为模板，再通过 CLIP 匹配；ELEGANT 直接推理关系候选，更高效且可扩展。R@20 上 ELEGANT 35.18 vs RECODE 10.60。
- **与 T-CAR (Li et al., 2023, TOMM)**：T-CAR 是监督式零样本 SGG，在训练集中挖掘 unseen triplets；ELEGANT 是完全零样本（不需要任何标注数据），两者解决不同设定下的零样本问题。
- **与 BLIP2 (Li et al., 2023, ICML)**：ELEGANT 使用 BLIP2 作为 verifier，验证 LLM 生成的关系三元组。
- **与 GroundedSAM (Liu et al., 2023)**：作为 observer 模块提供开放词汇检测能力。
- **与 CLIPScore (Hessel et al., 2021, EMNLP)**：ECLIPSE 基于 CLIPScore 改进，增加长度惩罚函数以适配场景图评估。
- **与 PSG (Yang et al., 2022, ECCV)**：作者展望可扩展 ELEGANT 到 zero-shot panoptic SGG。

## Open Questions

1. ELEGANT 的 CoCa 策略是否适用于更多基础模型组合（如开源 VLM 替代 GPT-3.5）？
2. 对于空间上不重叠但语义相关的物体对（IoU=0），如何扩展配对策略？
3. ECLIPSE 的长度惩罚函数中 α 参数如何自适应不同数据集？
4. ELEGANT 在视频场景图（VSGG）或 3D 场景图上是否也能实现零样本局部场景图生成？
5. 如何降低 ELEGANT 的多模型级联推理成本？
6. ELEGANT 生成的局部场景图对其他下游任务（如机器人操作、导航）的效果如何？

## Provenance

- 论文 PDF: `raw/sources/2023-10-02-less-is-more-zero-shot-local-scene-graph-generation-via-foundation-models.pdf`
- 提取文本: `raw/sources/2023-10-02-less-is-more-zero-shot-local-scene-graph-generation-via-foundation-models.txt`
- ArXiv: https://arxiv.org/abs/2310.01356
