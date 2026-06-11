# SGG Metrics — Evaluation & Benchmarks

> 场景图生成领域的主要评价指标、评估协议和基准。

## 核心指标

### Recall@K (R@K)
标准召回率：Top-K 预测中正确预测的比例。对常见关系（head）敏感。

### Mean Recall@K (mR@K)
类别平均召回率：先按谓词类别分别计算 Recall，再取平均。缓解 head predicate 主导问题，反映长尾预测能力。

### F@K (或 F1@K)
R@K 和 mR@K 的调和平均：$F_K = 2 \cdot \frac{R_K \cdot mR_K}{R_K + mR_K}$

### no-graph Constraint (ng-R@K / ng-mR@K)
排除图像中未形成关系图的情况。更严格。

### Pair Recall
专用于 Panoptic SGG 的指标：评估 subject-object 配对正确率。

## 评估任务

SGG 通常在三个难度递增的任务上评估：

| 任务 | 缩写 | 输入 | 预测 |
|------|------|------|------|
| Predicate Classification | **PredCls** | GT 框 + GT 类别 | 关系谓词 |
| Scene Graph Classification | **SGCls** | GT 框 | 类别 + 关系 |
| Scene Graph Detection | **SGDet** | 原始图像 | 框 + 类别 + 关系 |

### PSGG 增加的评估

- **SGGen**: SGDet 的 panoptic 版本（含 mask 评估）
- **mNgR@K**: mask no-graph constrained mR@K

## 评估协议

### MultiMPO（原始 PSG 协议）
- 允许重复 mask 映射和同一 subject-object 对的多个 predicate 分布
- **缺陷**: 可被利用来虚增指标

### SingleMPO（修正协议）
- 强制每个 GT 对象对应单个 mask
- 每个 subject-object 对对应单一 predicate 分布
- 消除不公平优势，一阶段方法在 SingleMPO 下 mR@50 最多下降 19.3

## 相关论文

- [[fair-ranking-new-model-panoptic-sgg|A Fair Ranking and New Model for Panoptic Scene Graph Generation — SingleMPO 协议]]
- [[relclipscore-reference-free-metrics-visual-relation-detection|RelCLIPScore: Reference-Free Metric for VRD]]
- [[2025-05-29-tsg-bench-llm-meets-scene-graph|TSG Bench: LLM 理解场景图的能力评估]]

## 什么是好的 SGG 指标？

一个好的 SGG 评估指标应该：
1. **分类平衡**: 不被频繁关系主导（mR@K 优于 R@K）
2. **关系完整性**: 同时评估配对和关系（Pair Recall + R@K）
3. **无评估漏洞**: 防止重复预测虚增指标（SingleMPO 协议）
