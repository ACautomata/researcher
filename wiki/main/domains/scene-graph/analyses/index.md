# SGG Analyses — Deep Analysis Index

> 深度分析与领域洞察索引。

## SGG 领域的核心难题

### 偏置问题分析

- [[unbiased-scene-graph-generation-tde-causal-modeling|TDE]] — 因果解耦分析 SGG 偏置来源
- [[eicr-environment-invariant-curriculum-relation-learning-sgg|EICR]] — 分析上下文和类别偏置的叠加效应
- [[sbgg-fine-grained-sgg-sample-level-bias-prediction|SBG]] — 样本级偏置的可预测性分析
- [[salience-sgg-unbiased-scene-graph-generation-via-salience-estimation|Salience-SGG]] — 关系显著性与偏置的关系分析
- [[fair-ranking-new-model-panoptic-sgg|Fair Ranking PSG]] — SingleMPO 协议对 PSG 评估偏置的清洗分析

### 评估方法论分析

- [[fair-ranking-new-model-panoptic-sgg|Fair Ranking PSG]] — MultiMPO vs SingleMPO 评估漏洞分析
- [[2025-05-29-tsg-bench-llm-meets-scene-graph|TSG Bench]] — LLM 理解场景图的能力边界分析
- [[relclipscore-reference-free-metrics-visual-relation-detection|RelCLIPScore]] — 参考自由的 VRD 评估指标

### 开放词汇能力分析

- [[pixels-to-graphs-open-vocabulary-sgg-vlm|Pixels-to-Graphs]] — VLM 知识蒸馏对 OV-SGG 的效果分析
- [[acc-interaction-centric-knowledge-infusion-sgg|Interaction-Centric]] — 交互级知识注入对 OV 泛化的贡献分析
- [[scene-graph-vit-open-vocabulary-vrd|Scene-Graph ViT]] — ViT 架构对开放词汇 VRD 的影响分析

## 方法对比分析

- [[hydra-sgg-hybrid-relation-assignment-one-stage|Hydra-SGG]] — 混合指派 VS 传统稠密指派
- [[pair-net-panoptic-scene-graph-generation|Pair-Net]] — Pair proposal VS 全连接的关系表示对比
- [[flowsg-progressive-image-conditioned-scene-graph-flow-matching|FlowSG]] — 流匹配 VS 扩散生成 VS Transformer 分类
- [[egtr-extracting-graph-from-transformer-sgg|EGTR]] — DETR 特征直接提取 VS 独立关系网络
- [[dsflash-comprehensive-panoptic-scene-graph-generation-realtime|DSFlash]] — 速度-精度权衡分析
