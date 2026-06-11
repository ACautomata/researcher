---
title: "FACTUAL: A Benchmark for Faithful and Consistent Textual Scene Graph Parsing"
tags:
  - scene-graph-generation
  - textual-scene-graph
  - benchmark
arxiv: "2305.17497"
created: 2026-06-10
source: https://arxiv.org/pdf/2305.17497
confidence: full-paper
authors:
  - Zhuang Li
  - Yuyang Chai
  - Terry Yue Zhuo
  - et al.
venue: arXiv May 2023
code: https://github.com/zhuang-li/FACTUAL
---

## Paper Info

文本场景图解析 benchmark。FACTUAL-MR 中间表示 + FACTUAL 数据集 (40,369 样本) + SoftSPICE 度量。

## Method

FACTUAL-MR: `{Object,Attribute}` / `{Quant, Subj, Verb, Prep, Quant, Obj}`
SoftSPICE: Sentence-BERT 嵌入余弦相似度替代精确匹配

## Key Results

**Parsing**: FACTUAL-T5(pre) SPICE=92.91 (vs CDP-T5 73.56), Precision 93%, Completeness 92%
**Caption Eval**: SoftSPICE(img)+RefCLIPScore τc=57.37 (Flicker8K SOTA)
**Zero-shot Retrieval**: FACTUAL-T5 R@1=79.39 (Local, Random)

## Provenance

- **Source**: arXiv 2305.17497
- **Evidence level**: full-paper
