---
title: "Scene Graph Generation With Hierarchical Context"
authors:
  - Guanghui Ren
  - Lejian Ren
  - Yue Liao
  - Si Liu
  - Bo Li
  - Jizhong Han
  - Shuicheng Yan
year: 2021
venue: IEEE Transactions on Neural Networks and Learning Systems (TNNLS)
doi: "10.1109/TNNLS.2020.2979270"
arxiv: null
code: null
domain: scene-graph
tags: [scene-graph, hierarchical-context, contextual-reasoning, predicate-classification]
evidence_level: abstract-only
status: active
task: Scene Graph Generation (Predicate Classification)
dataset: Visual Genome (VG)
---

# Scene Graph Generation With Hierarchical Context

> Guanghui Ren, Lejian Ren, Yue Liao, Si Liu, Bo Li, Jizhong Han, Shuicheng Yan. IEEE TNNLS, vol. 32, no. 2, Feb. 2021.
> DOI: [10.1109/TNNLS.2020.2979270](https://doi.org/10.1109/TNNLS.2020.2979270)

> **⚠️ 说明**：该论文由 inbound 批量入库触发，原始文件路径失效无法提取全文。以下信息基于 CrossRef / Semantic Scholar 元数据和摘要构建（evidence_level: abstract-only）。

## 核心贡献

1. 分析影响场景图关系检测的关键因素：空间相关性、对象的关注区域、关系的全局线索。
2. 提出**层次上下文网络 (Hierarchical Context Network, HCNet)**，从 pair、object、graph 三个层级集成上下文信息。
3. HCNet 包含三种上下文模块：
   - **Interaction Context**（交互上下文）：捕获对象对之间的空间交互信息
   - **Depression Context**（抑郁上下文/焦点上下文）：聚焦对象的重点区域信息
   - **Global Context**（全局上下文）：整合关系相关的全局线索
4. 通过多层级上下文融合增强谓词表示，消除矛盾关系。

## 方法概述

HCNet 以三个层级集成上下文信息增强谓词表示：

1. **Pair Level（交互上下文）**：建模两个物体之间的空间相关性和相对几何关系，捕获交互模式。
2. **Object Level（抑郁上下文）**：聚焦于每个对象中与当前关系最相关的区域，抑制无关信息。
3. **Graph Level（全局上下文）**：整合整个场景的全局语义线索，为关系预测提供场景层面的指导。

三种上下文通过融合机制联合作用于谓词分类，从不同粒度增强关系表示。

## 实验结果

> 以下信息基于摘要，具体数值待补全。

- **数据集**：Visual Genome (VG)
- **任务**：Scene Graph Generation (Predicate Classification)
- **对比基线**：与当时的 SOTA 方法相比，HCNet 在关系预测和矛盾消除方面表现更优（具体指标数值待全文确认）。

## 关键分析

- 论文指出空间相关性（spatial correlations）、对象聚焦区域（focused regions of objects）、全局线索（global hints）是关系检测中影响最大的三个因素。
- 三个层级的上下文互为补充：pair 层提供局部交互信号，object 层提供单实体焦点信号，graph 层提供全局语义约束。

## 待确认

- [ ] 具体的 Recall@K / Mean Recall@K 数值
- [ ] 与 MOTIFS、VCTree、RelDN 等方法的定量对比
- [ ] 消融实验中对各上下文模块的贡献分析
- [ ] 代码是否开源

## Related Pages

- [[scene-graph-generation-with-hierarchical-context|HCNet]]
