---
title: "APT: Towards Universal Scene Graph Generation via Plug-in Adaptive Prompt Tuning"
tags:
  - scene-graph-generation
  - universal
  - adaptive-prompt
  - ICLR-2026
  - prompt-tuning
created: 2026-06-10
source: https://openreview.net/pdf?id=IZWJhdK2o7
confidence: full-paper
code: https://github.com/CGCL-codes/APT
authors:
  - Ruikun Luo
  - Changwei Gu
  - Jing Yang
  - Yuan Gao
  - Jieming Yang
  - Song Wu
  - Hai Jin
  - Xiaoyu Xia
affiliations:
  - HUST
  - Zhengzhou University
  - RMIT
---

## Paper Info

- **Title**: APT: Towards Universal Scene Graph Generation via Plug-in Adaptive Prompt Tuning
- **Venue**: ICLR 2026（非 CVPR 2024）
- **Keywords**: Scene Graph Generation, Adaptive Prompt Tuning, Universal Plugin, Information Bottleneck

## Abstract

SGG 依赖固定、冻结的预训练语义表示，与动态、上下文敏感的视觉关系不一致。APT 通过轻量级可学习 prompt 将冻结语义特征转化为动态上下文感知表示，作为 plug-in 模块无缝集成到现有 SGG 框架。实验显示 +2.7 mR@100 on PredCls, +3.6 F@100, up to +6.0 mR@50 开放词汇 novel split，<0.5M 额外参数（<1.5% 开销），训练时间减少 7.8%–25%。

## Method

### Core Diagnosis

论文指出**冻结语义表示**（GloVe, BERT, GPT, CLIP-text）是 SGG 的根本瓶颈，超越一阶段 vs 两阶段架构之争。t-SNE 可视化（Figure 2）显示冻结 GloVe 将所有"person"实例坍缩为单点，无视视觉上下文。

### Adaptive Prompt Tuning (APT)

基于连续 prompt learning (Lester et al., 2021)，引入轻量级可学习 prompt **P**：

**˜e** = fθ( A(P(c), e_static(c), ϕ(v)) )

通过 **Information Bottleneck** 框架：prompt 学习压缩无关语义信息同时注入相关视觉上下文。

### Unified Plug-in Prompts

三种 prompt 类型：
1. **Detection Prompt (Pd)** — 检测阶段
2. **Relation Prompt (Pr)** — 关系预测阶段（两阶段）
3. **Unified Relation Prompt (Pur)** — 一阶段范式

预训练语义嵌入**冻结**，仅 prompt 参数和轻量 MLP 可学习。

### Compositional Generalization Prompter (CGP)

开放词汇环境下三个子模块：
1. **Relational Context Gating (RCG)** — 角色感知 prompt 权重
2. **Basis Prompt Synthesis (BPS)** — N 个可学习基础 prompt 的加权组合
3. **Feature Refinement & Fusion (FRF)** — 最终融合

## Experiments

### 主结果 (Table 2, VG)

| Method | PredCls mR@100 | PredCls F@100 | SGCls mR@100 | SGDet mR@100 |
|--------|:---:|:---:|:---:|:---:|
| MOTIFS → MOTIFS+APT | 16.2→**18.1** | 26.0→**28.1** | 9.3→**11.1** | 7.7→**10.3** |
| SGTR → SGTR+APT | 32.9→**35.3** | 42.8→**45.9** | 16.5→**18.7** | 12.6→**14.8** |
| EGTR → EGTR+APT | 38.2→**40.1** | 45.6→**47.7** | 18.4→**20.3** | 15.5→**16.9** |
| LLM4SGG → LLM4SGG+APT | 39.1→**42.2** | 48.6→**50.3** | 22.5→**24.8** | 17.1→**19.8** |

### 开放词汇 (Table 3, VG)

| Method | Novel mR@20/50/100 |
|--------|:---:|
| SDSGG → SDSGG+APT | 17.1/25.2/31.2 → 18.6/**26.7**/32.3 |
| OvSGTR → OvSGTR+APT | 10.9/13.5/16.2 → 11.6/14.3/17.2 |

Novel split 最高 **+6.0 mR@50**。

### 效率分析 (Table 6)

部分模型参数降低（LLM4SGG -2.1M, ST-SGG -1.2M），训练时间减少 7.8%–25%。

## Results

- **+2.7 mR@100** PredCls (跨多 baseline 一致提升)
- **<0.5M** 额外参数（<1.5%）
- **7.8%–25%** 训练时间减少
- Head/tail predicates 均提升，不牺牲 R@K

## Limitations

1. 主论文仅 VG 完整结果，OI-V6/GQA 在附录
2. Prompt 长度超参缺乏敏感性分析
3. IB 代理指标非直接优化
4. 仅 3 个数据集评估
5. 冻结嵌入无法受益于 LM 训练中改进

## Connections

- **Continuous Prompt Learning** (Lester et al., 2021) — 基础技术
- **CoOp/CoCoOp** (Zhou et al., 2022) — 视觉语言 prompt learning
- **Information Bottleneck** (Tishby et al., 2000) — 理论框架
- 作为正交插件提升 OV-SGG (SDSGG, OvSGTR) 和一阶段/两阶段方法

## Open Questions

1. 能否扩展到 SGG 之外的结构化预测任务？
2. 更大 predicate 分类体系（>500）的扩展性？
3. IB 理论保障的精确优化？
4. Prompt 空间跨模型迁移？
5. 与视觉基础模型（DINOv2, SAM）的交互？

## Provenance

- **Source**: OpenReview PDF (ICLR 2026)
- **Evidence level**: full-paper
- **Status**: active — ICLR 2026
