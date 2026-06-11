---
title: "INOVA: Interaction-Aware Open Vocabulary Scene Graph Generation"
tags:
  - scene-graph-generation
  - open-vocabulary
  - interaction-aware
  - VLM
created: 2026-06-10
source: https://arxiv.org/pdf/2502.03856
confidence: full-paper
authors:
  - Lin Li
  - Chuhan Zhang
  - Dong Zhang
  - Chong Sun
  - Chen Li
  - Long Chen
venue: arXiv 2025
---

## Paper Info

- **Title**: Taking A Closer Look at Interacting Objects: Interaction-Aware Open Vocabulary Scene Graph Generation
- **Venue**: arXiv Feb 2025
- **Code**: None
- **Dataset**: VG150, GQA200

## Abstract

现有 OV-SGG 忽视"交互对象"与"非交互对象"的区别。INOVA 通过 ITG（双向交互提示 grounding）+ IQS（交互引导查询选择）+ RRD（交互一致性知识蒸馏）三个组件解决。Swin-B 上 Novel Rel R@100 24.66%，超越 OvSGTR +4.94%。

## Method

### 交互感知目标生成 (ITG)

Grounding DINO 预训练阶段，设计双向交互提示：
- **正向**: `<subject, predicate, object>` → "man hold surfboard"
- **反向**: 交换主宾语（LLM 生成反动作）→ "surfboard held by man"

### 交互引导查询选择 (IQS)

两步：
1. 计算视觉 token 与对象/关系语义的相关性，选 Top-K
2. 计算交互相关性，选 Top-L 交互 token，余 K-L 按对象相关性补齐

### 交互一致性知识蒸馏 (RRD)

视觉概念保持 (VRD) + 相对交互保持 (RRD, Frobenius norm)。

## Experiments

### OvR-SGG (VG150)

| 方法 | Novel R@100 |
|------|:---:|
| OvSGTR (Swin-B) | 19.72 |
| **INOVA (Swin-B)** | **24.66** |

### OvD+R-SGG (VG150)

| 方法 | Novel Rel R@100 |
|------|:---:|
| OvSGTR (Swin-T) | 11.18 |
| **INOVA (Swin-T)** | **19.46** |
| OvSGTR (Swin-B) | 18.22 |
| **INOVA (Swin-B)** | **21.73** |

### 消融

ITG: +3.94%, IQS: +3.00%, RRD: +2.83% (R@100)

## Results

- **Swin-B**: Novel Rel R@100 24.66 (+4.94 over OvSGTR)
- **Swin-T**: 19.46 (+8.28 over OvSGTR)
- 预训练直接测试也显著超越基线

## Limitations

1. 三组件增益递减
2. 双向提示依赖 LLM 预处理
3. 未在 MLLM-based 方法验证

## Connections

- [[OvSGTR]] — 主要基线和 VRD 蒸馏来源
- [[RAHP]] — 关系层次化提示 OVSGG
- [[VS3]] — 语言监督 OVSGG

## Provenance

- **Source**: arXiv 2502.03856
- **Evidence level**: full-paper
