# Reading Notes

> 阅读笔记索引。按主题分组，便于系统性学习。

## 入门前必读

### 基础 — Predicate Classification + SGG 定义

1. [[unbiased-scene-graph-generation-tde-causal-modeling|Unbiased SGG from Biased Training (TDE)]] — 理解 SGG 偏置问题的起点
2. [[reltr-relation-transformer-scene-graph-generation|RelTR]] — 最简洁的 SGG Transformer 实现
3. [[importance-first-human-interest-scene-graph|Importance First]] — SGG"应该预测哪些关系"的思考

### Panoptic SGG 入门

1. [[hilo-exploiting-high-low-frequency-for-unbiased-panoptic-scene-graph-generation|HiLo]] — Panoptic SGG 第一代方法
2. [[pair-net-panoptic-scene-graph-generation|Pair-Net]] — Pair Proposal 新范式
3. [[fair-ranking-new-model-panoptic-sgg|Fair Ranking PSG]] — PSG 评估方法论的转折点

### 去偏 SGG

1. TDE → EICR → CFA → Salience-SGG — 去偏路线图
2. CAModule → RcSGG → CAGE-SGG — 因果路线（最新）

### 开放词汇 SGG

1. VS3 → ReLIC-SGG → Interaction-Centric — OV 基础
2. OvSGTR → Pixels-to-Graphs — 统一 OV 框架

### 视频 / 3D SGG

1. TEMPURA → OED → THYME → DIFFVSGG → MOSA — 视频 SGG 演进
2. Open3DSG → CCL-3DSGG → ZING-3D → GaussianGraph — 3D SGG 演进

### LLM + SGG

1. SDSGG → LLM4SGG → GPT4SGG — LLM 辅助 SGG
2. OpenPSG → VLM-SGG — MLLM 开放集 SGG
3. TSG Bench — LLM 场景图理解评估
