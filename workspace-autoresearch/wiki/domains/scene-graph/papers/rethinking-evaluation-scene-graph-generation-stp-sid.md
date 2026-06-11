---
title: "Rethinking the Evaluation of Scene Graph Generation: STP and SID Metrics"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - scene-graph-generation
  - evaluation-metrics
  - semantic-triplet-precision
  - semantic-information-depth
  - MLLM-evaluation
  - incomplete-annotations
  - PRCV-2026
raw_sources:
  - ../../../raw/sources/2026-06-09-rethinking-evaluation-scene-graph-generation.txt
related_pages:
  - compositional-feature-augmentation-for-unbiased-scene-graph-generation.md
  - dsgg-dense-relation-transformer-end-to-end-sgg.md
evidence_level: skimmed
paper:
  title: "Rethinking the Evaluation of Scene Graph Generation"
  authors:
    - Jingyi Wang
    - Hanwei Gao
    - Zhidong Deng
  year: 2026
  venue: "Pattern Recognition and Computer Vision (PRCV), 2026, Lecture Notes in Computer Science, Springer"
  doi: "10.1007/978-981-95-5679-3_28"
  arxiv: null
  code: null
  project: null
classification:
  label: "STP/SID — 重新思考 SGG 评估指标，解决 Recall 偏置和标注不全问题"
  task:
    - Scene Graph Generation Evaluation
    - Predicate Classification (PredCls)
    - Scene Graph Detection (SgDet)
  method_family:
    - Evaluation metrics
    - MLLM-based triplet verification (STP)
    - WordNet-based semantic depth (SID)
  modality:
    - Visual features (images)
    - Bounding box coordinates
    - Textual triplet descriptions
    - WordNet lexical hierarchy
  datasets:
    - Visual Genome (VG)
  metrics:
    - Semantic Triplet Precision@K (STP@K)
    - Semantic Information Depth@K (SID@K)
    - Recall@K (R@K)
    - mean Recall@K (mR@K)
---

## Citation

Jingyi Wang, Hanwei Gao, Zhidong Deng. "Rethinking the Evaluation of Scene Graph Generation." *Pattern Recognition and Computer Vision (PRCV)*, 2026, LNCS, Springer. DOI: 10.1007/978-981-95-5679-3_28.

## One-Sentence Contribution

指出 Recall-based 指标无法评估未标注三元组的质量和谓词语义信息量，提出 Semantic Triplet Precision（STP，用 MLLM 验证三元组视觉正确性）和 Semantic Information Depth（SID，用 WordNet 深度量化谓词语义丰富度）两个补充指标。

## Problem Setting

场景图生成（SGG）模型传统上使用 Recall@K（R@K）和 mean Recall@K（mR@K）进行评估。这些指标存在两个关键缺陷：

1. **忽略未标注三元组**：Recall 只计算预测三元组与 ground-truth 注释的匹配程度。由于 SGG 数据集注释严重不完整（标注者偏见），一个视觉上完全正确但未出现在 GT 中的三元组会被 Recall 惩罚，导致对模型质量的误判。
2. **不区分谓词语义信息**：所有匹配的谓词在 Recall 计算中权重相同，但有些谓词（如 on）仅有空间关系信息，而其他谓词（如 riding）蕴含丰富的语义信息。R@K 和 mR@K 无法区分场景图的"信息密度"。

## Method

### STP: Semantic Triplet Precision（语义三元组精度）

**核心思路**：使用预训练多模态大模型（MLLM）评估每个预测三元组在视觉上是否正确，而非仅依赖 GT 注释匹配。

**计算流程**：
1. 从场景图中提取 <subject-predicate-object> 三元组
2. 转换为文本问答格式："Is the <subject> [bbox_s] <predicate> the <object> [bbox_o]?"
3. 将问题文本和图像输入预训练 MLLM（选用 Ferret-7B）
4. 根据 MLLM 输出判断三元组正确性
5. 计算 precision：
   $$\text{STP} = \frac{1}{|T^{pred}|} \sum_{(s,p,o)\in T^{pred}} \mathbf{1}(s,p,o)$$

其中 $\mathbf{1}(\cdot)$ 是指示函数，三元组符合视觉内容时输出 1，否则输出 0。

**选择 Ferret 的原因**：Ferret 具有卓越的视觉指代理解能力（visual referring comprehension），能够理解通过 bounding box 标注的实体位置。实验表明 Ferret (7B) 显著优于 Gemini-1.5-Flash 和 Qwen2.5-VL-32B。

### SID: Semantic Information Depth（语义信息深度）

**核心思路**：通过谓词在 WordNet 中的语义深度量化语义信息量，深度越大的谓词携带更丰富的语义信息。

**计算流程**：
1. 从预测场景图中提取所有谓词
2. 使用 WordNet 计算每个谓词的语义深度（从词节点到根节点的最短路径长度）
3. 计算平均 depth（归一化到最大 depth）：

$$\text{SID} = \frac{1}{|T^{pred}|} \sum_{(s,p,o)\in T^{pred}} \frac{\text{Depth}(p)}{\max_{p' \in P} \text{Depth}(p')}$$

其中 $P$ 是数据集中所有谓词的集合。

**示例**：riding 的语义深度为 2，on 的语义深度为 1。riding 传达更丰富的语义信息，也更难仅从视觉特征推断。

### 评估框架

同时使用四种指标进行全面评估：R@K（传统 Recall）、mR@K（均衡 Recall）、STP@K（三元组精度）、SID@K（语义深度）。对所有 K 值，选取 Top-K 预测三元组进行计算，类似传统 R@K 评估协议。

## Experiments

### 数据集

- **Visual Genome (VG)**：108,077 张标注图像，标准 SGG benchmark。训练集 70%，测试集 30%。

### 评估任务

1. **Predicate Classification (PredCls)**：给定 ground-truth 实体框和类别，预测谓词类别
2. **Scene Graph Detection (SgDet)**：检测所有实体并预测其关系

### MLLM 配置

- STP 计算使用 Ferret (7B) — 具有 bounding box 感知能力的多模态大模型
- 对比 MLLM：Gemini-1.5-Flash、Qwen2.5-VL-32B

### 评估指标

- R@10 和 mR@10（传统指标）
- **STP@10** 和 **SID@10**（新提出指标）
- **Mean**：四种指标（R@10, mR@10, STP@10, SID@10）的平均值

### 评估方法

共评估 16 个 SGG 模型：
- 经典模型：IMP, Motif, VCTree, BGNN
- 近期模型：HL-Net, RU-Net, IETrans, NICE (Motif/VCTree 变体), PENet, CFA, SQUAT, DRM
- LLM/MLLM-based：LLM4SGG, Qwen2.5-VL-32B, Gemini-1.5-Flash

## Results

### PredCls 任务主要结果（Table 1）

关键发现：
- **PENet** 在 PredCls 和 SgDet 任务上均表现最强（综合 Mean 最高）
- **DRM** 的平均 Recall（R/mR）显著提升，但其 STP 低于早期模型（如 HL-Net, VCTree），表明 DRM 的谓词分类能力并未实质增强
- **早期模型（BGNN, VCTree, Motif）**在 STP 指标上表现出色，尽管它们的平均 Recall 较低
- 对于 **SID** 指标，近期模型表现更好，因为它们生成更丰富的语义信息

关键结论：R@K/mR@K 的趋势与 STP/SID 的趋势**不一致**。Recall-based 指标单独使用不足以全面评估 SGG 模型。

### MLLM 对比结果（Table 3）

| MLLM | 标注三元组准确率 |
|------|-----------------|
| **Ferret (7B)** | **显著最优** |
| Gemini-1.5-Flash | 次于 Ferret |
| Qwen2.5-VL-32B | 次于 Ferret |

Ferret (7B) 尽管参数量最小，但依靠其卓越的视觉指代理解能力显著优于 Gemini-1.5-Flash 和 Qwen2.5-VL-32B。

### 模型置信度与 STP 关系（Fig. 5）

以 Motif 为基模型，分析预测三元组的置信度分数与 STP@20 的关系：
- 置信度 0.1：STP@20 ≈ 0.87
- 置信度 1.0：STP@20 ≈ 0.99
- **趋势**：置信度越高，三元组精度越高（单调递增关系）

这说明模型的置信度评分机制与预测精度保持一致。在实际应用中，可以基于置信度分数筛选高精度三元组，而非仅依赖匹配 GT 注释的三元组。

### 可视化案例（Fig. 6 & Fig. 7）

**Fig. 6 — 高 Recall 低 STP 案例**：
- 在划船场景中，IMP 的 Recall 高于 Motif（覆盖更多 GT 三元组），但 STP 低于 Motif（IMP 的谓词分类能力较弱）
- 揭示了 Recall 仅衡量"覆盖了多少 GT"，不衡量"预测的质量"

**Fig. 7 — 高 Recall 低 SID 案例**：
- 雪地场景中，Motif 的 Recall 高于 CFA，但 CFA 的场景图含有更丰富的语义信息（如 "covered in" vs "on"）
- CFA 的混合特征策略增强了谓词语义丰富度

## Limitations

1. **MLLM 计算成本**：STP 需要调用 MLLM 评估每个三元组，计算开销大，不适合大规模验证。
2. **MLLM 评估偏置**：STP 的准确性依赖于 MLLM 的判断能力，可能存在模型特定的偏置。
3. **WordNet 深度局限性**：SID 仅基于 WordNet 词汇深度，可能无法完全捕获领域特定的语义信息量。
4. **缺乏综合性指标**：STP 和 SID 是 Recall 的补充而非替代，四种指标（R, mR, STP, SID）的权衡需要人工分析。
5. **代码未公开**：未见公开代码或 benchmark 框架。

## Reusable Claims

> **Claim**: Recall-based 指标（R@K, mR@K）无法检测 SGG 模型对未标注三元组的预测质量和谓词语义信息量。
> **Evidence**: DRM 的 mean Recall 显著高于早期模型，但其 STP 低于 HL-Net 和 VCTree，说明 Recall 指标对未标注三元组的评估完全盲视。
> **Confidence**: high

> **Claim**: STP 通过 MLLM 验证可以评估未标注三元组的视觉正确性，从而克服 SGG 数据集标注不全的问题。
> **Evidence**: Ferret (7B) 在 VG 标注三元组上显著优于 Gemini-1.5-Flash 和 Qwen2.5-VL-32B。置信度 0.1→1.0 时 STP@20 从 0.87→0.99。
> **Confidence**: medium（依赖 MLLM 验证，非独立客观指标）

> **Claim**: SID 通过 WordNet 语义深度可以区分场景图中不同谓词的语义信息量，早期模型（BGNN/VCTree/Motif）的谓词预测偏向简单谓词（低 SID）。
> **Evidence**: 早期模型在 PredCls 上 STP 高但 SID 低，近期模型（CFA, PENet）SID 更高。
> **Confidence**: medium

> **Claim**: 模型对预测三元组的置信度与三元组实际精度（STP）正相关（单调递增）。
> **Evidence**: Motif 模型上，置信度从 0.1 增长到 1.0，STP@20 从 0.87 增长到 0.99（Fig. 5）。
> **Confidence**: high

## Connections

- 和 [A Review and Efficient Implementation of Scene Graph Generation Metrics (CVPR 2024W)](https://openaccess.thecvf.com/content/CVPR2024W/SG2RL/html/Lorenz_A_Review_and_Efficient_Implementation_of_Scene_Graph_Generation_Metrics_CVPRW_2024_paper.html) 同为 SGG 评估方法学工作，但本篇侧重提出新指标（STP/SID），后者侧重高效实现现有指标。
- 与 CFA 的 Compositional Feature Augmentation（通过增强特征丰富语义信息）互补，CFA 侧重生成更丰富的场景图，STP/SID 侧重评估其质量和信息量。
- Dense Scene Graph 相关方法（如 DSGG）生成了远超 GT 注释量的三元组，传统 Recall 无法公平评估，STP 部分弥补了这一缺口。

## Open Questions

1. STP 使用 Ferret（MLLM）做三元组验证，不同 MLLM 的判断标准差异如何影响评估结果？
2. 是否可以设计一个无需 MLLM 调用的近似 STP 指标（如基于实体/谓词共现统计）以降低计算成本？
3. WordNet 深度是否可以在 SGG 特定谓词集上微调，以更好地反映领域知识？
4. 自适应场景图生成和评估指标（根据下游任务需求动态调整）是否有更系统化的方案？

## Provenance

- **原始 PDF**：未找到 — 指定路径 (/home/node/.openclaw/media/inbound/2024_CVPR_Evaluation_of_Scene_Graph_Generation_Across_Multiple_---f8042d7f-5623-4609-84c4-61f7df2e5aac.pdf) 不存在
- **信息源**：Springer 网页（DOI: 10.1007/978-981-95-5679-3_28）— 覆盖全文 Method, Experiments, Results 章节
- **实际标题**：Rethinking the Evaluation of Scene Graph Generation（与指定标题略有差异）
- **实际发表**：PRCV 2026（非 CVPR 2024）
- **证据等级**：skimmed — 基于 Springer 全文章节页阅读，覆盖方法、实验设置、主要结果和可视化
- **缺失**：完整表格数据（Table 1-3 以图片形式呈现，无法提取精确数值），详细消融实验（可能存在于补充材料）
