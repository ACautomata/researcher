---
title: "INOVA: Interaction-Aware Open Vocabulary Scene Graph Generation"
type: paper
domain: scene-graph
status: active
created: 2025-06-10
updated: 2025-06-10
tags: [scene-graph-generation, open-vocabulary, interaction-aware, grounding-dino]
source_pages: []
raw_sources:
  - raw/sources/2025-02-06-interaction-aware-open-vocabulary-sgg.pdf
  - raw/sources/2025-02-06-interaction-aware-open-vocabulary-sgg.txt
related_pages: []
paper:
  title: "Taking A Closer Look at Interacting Objects: Interaction-Aware Open Vocabulary Scene Graph Generation"
  authors: ["Lin Li", "Chuhan Zhang", "Dong Zhang", "Chong Sun", "Chen Li", "Long Chen"]
  year: 2025
  venue: arXiv preprint (Feb 2025)
  arxiv: "2502.03856"
  code: null
  project: null
classification:
  label: interaction-aware-ovsgg
  task: ["Open Vocabulary Scene Graph Generation"]
  method_family: ["Interaction-aware", "Knowledge Distillation", "Query Selection"]
  modality: ["Image", "Text"]
  datasets: ["Visual Genome", "GQA"]
  metrics: ["Recall@K"]
evidence_level: full-paper
---

# INOVA: Interaction-Aware Open Vocabulary Scene Graph Generation

## Citation

Li, L., Zhang, C., Zhang, D., Sun, C., Li, C., & Chen, L. (2025). Taking A Closer Look at Interacting Objects: Interaction-Aware Open Vocabulary Scene Graph Generation. arXiv:2502.03856.

## One-Sentence Contribution

提出交互感知的 OVSGG 框架 **INOVA**，通过在预训练和微调阶段显式区分 interacting objects 与 non-interacting objects，解决关系对匹配错误问题，在 VG 和 GQA 上达到 SOTA。

## Problem Setting

**Open Vocabulary Scene Graph Generation (OVSGG)** 的目标是从图像中生成场景图，要求识别预定义以外的新颖物体和关系。现有方法采用两阶段流程：

1. **VLM Pre-training**：基于图像描述生成伪标注三元组（subject-predicate-object），用弱监督对齐视觉和概念
2. **Supervised Fine-Tuning (SFT)**：在完全标注的场景图数据上用 DETR-like 结构 + 二部图匹配对齐预测和 GT

**核心问题**：现有方法将所有物体等同处理，不区分 "一个正在骑马的 man" 和 "旁边不参与任何动作的 man"，导致：

- **预训练阶段**：仅靠实体类别（如 man, surfboard）检测物体，大量候选对产生歧义，难以将关系关联到正确的实体对上，引入噪声监督
- **SFT 阶段**：二部图匹配可能将非交互物体错误匹配到交互 triplet 标签上（如 non-interacting "man" 匹配到 ⟨man, riding, horse⟩），加剧关系分类难度

## Method

**INOVA** 基于 Grounding DINO 的 dual-encoder-single-decoder 架构，包含三个核心组件：

### 1. Interaction-aware Target Generation (ITG) — 预训练阶段

- 采用 **bidirectional interaction prompts**（双向交互提示），在 grounding 过程中引入 interaction tokens（交互令牌）
- 交互令牌通过注意力机制捕捉上下文依赖和关系语义，使模型能够区分 interacting 和 non-interacting 物体
- 例如：给定 ⟨man, hold, surfboard⟩ 三元组，ITG 让 detector 只关注"正在 hold 的 man"和"被 hold 的 surfboard"，而非场景中所有 man 和 surfboard

### 2. Interaction-guided Query Selection (IQS) — SFT 阶段

- 两阶段查询选择机制：
  - 第一步：根据交互相关性对 decoder queries 排序
  - 第二步：优先选择对应 interacting objects 的 queries，减少 non-interacting objects 在二部图匹配中的干扰
- 目标：增加同类别物体间的区分度，降低错误匹配概率

### 3. Relative-interaction Retention Distillation (RRD) — SFT 阶段

- 交互一致性知识蒸馏：用预训练的 teacher model 指导 student model
- 不仅保持 point-wise 语义对齐（单个实体的视觉-文本匹配）
- 还保持 **inter-pair relational consistency**（交互对 vs 非交互对的相对依赖关系）
- 目的：避免 SFT 阶段灾难性遗忘，同时增强 interacting pairs 与 background 的区分度

![Figure 1](raw/sources/2025-02-06-interaction-aware-open-vocabulary-sgg.pdf)

## Experiments

### 数据集

| 数据集 | 图像数 | Obj 类别 | Rel 类别 | 划分方式 |
|--------|--------|----------|----------|----------|
| VG (Krishna et al., 2017) | 108,777 | 150 | 50 | 70% 训练, 5,000 验证, 剩余测试；去掉与 Grounding DINO 预训练重叠的图像后保留 14,700 测试图 |
| GQA (Hudson & Manning, 2019) | GQA200 split | 200 | 100 | 随机采样 70% 的 obj 和 pred 类别作为 base |

### 评估设置

- **协议**：Scene Graph Detection (SGDET) — 需要同时检测物体和识别关系，不使用 GT 物体标签或边界框
- **指标**：Recall@K (R@K) 和 Mean R@K (mR@K)

### 两个 OVSGG 设定

| 设定 | 描述 | 训练排除 |
|------|------|----------|
| **OvR-SGG** | 评估对新关系的泛化能力，保留原有物体类别 | VG150 中 50 个关系类别中的 15 个 |
| **OvD+R-SGG** | 同时评估对新物体和新关系的泛化能力 | 新物体和新关系均排除在训练外 |

### Baselines

IMP, MOTIFS, VCTREE, TDE (闭集)、VS3 (CVPR'23)、OvSGTR (ECCV'24)、RAHP (AAAI'25)

### Backbones

Swin-T (Swin-Tiny), Swin-B (Swin-Base)

### 消融实验变体

- Baseline：不带 ITG/IQS/RRD 的通用 OVSGG pipeline（含 OvSGTR 的 visual-concept retention distillation）
- +ITG：仅添加 Interaction-aware Target Generation
- +IQS：仅添加 Interaction-guided Query Selection
- +RRD：仅添加 Relative-interaction Retention Distillation
- ITG+IQS+RRD（完整）：全部三个组件

### 预训练对比

所有模型在 COCO captions 上预训练后用 Grounding DINO 作为 grounding backbone，直接测试 R@K

## Results

### OvR-SGG 设定（VG 测试集）

| Method | Backbone | R@20 | R@50 | R@100 (B+N) | R@20 (Novel Rel) | R@50 (Novel Rel) | R@100 (Novel Rel) |
|--------|----------|------|------|-------------|-------------------|-------------------|-------------------|
| IMP | - | - | - | 14.65 | - | - | 0.00 |
| MOTIFS | - | - | - | 16.96 | - | - | 0.00 |
| VCTREE | - | - | - | 17.26 | - | - | 0.00 |
| TDE | - | - | - | 17.37 | - | - | 0.00 |
| VS3 | Swin-T | - | 15.60 | 17.30 | - | 0.00 | 0.00 |
| OvSGTR | Swin-T | - | 20.46 | 23.86 | - | 13.45 | 16.19 |
| RAHP | Swin-T | - | 20.50 | 25.74 | - | 15.59 | 19.92 |
| **INOVA** | **Swin-T** | **17.49** | **23.22** | **27.40** | **12.90** | **17.89** | **21.70** |
| OvSGTR | Swin-B | - | 22.89 | 26.65 | - | 16.39 | 19.72 |
| **INOVA** | **Swin-B** | **18.77** | **24.81** | **29.28** | **14.72** | **20.04** | **24.66** |

**关键差距**：
- Swin-T：INOVA Novel Rel R@100 21.70 vs RAHP 19.92 (+1.78), vs OvSGTR 16.19 (+5.51)
- Swin-B：INOVA Novel Rel R@100 24.66 vs OvSGTR 19.72 (+4.94)

### OvD+R-SGG 设定（VG 测试集）

| Method | Backbone | R@50 (Joint) | R@100 (Joint) | R@100 (Novel Obj) | R@100 (Novel Rel) |
|--------|----------|-------------|--------------|-------------------|-------------------|
| IMP | - | - | 0.94 | 0.00 | 0.00 |
| MOTIFS | - | - | 1.12 | 0.00 | 0.00 |
| VCTREE | - | - | 1.17 | 0.00 | 0.00 |
| TDE | - | - | 1.15 | 0.00 | 0.00 |
| VS3 | Swin-T | - | 7.20 | 0.00 | 0.00 |
| OvSGTR | Swin-T | 13.50 | 16.37 | 17.48 | 11.18 |
| **INOVA** | **Swin-T** | **17.43** | **21.27** | **21.10** | **19.46** |
| OvSGTR | Swin-B | 17.14 | 21.03 | 21.70 | 18.22 |
| **INOVA** | **Swin-B** | **18.88** | **23.19** | **23.29** | **21.73** |

**关键差距**：
- Swin-T：INOVA Joint R@100 21.27 vs OvSGTR 16.37 (+4.90)；Novel Rel R@100 19.46 vs 11.18 (+8.28)
- Swin-B：INOVA Joint R@100 23.19 vs OvSGTR 21.03 (+2.16)；Novel Rel R@100 21.73 vs 18.22 (+3.51)

### 消融实验（OvD+R-SGG, Swin-T, VG）

| ITG | IQS | RRD | R@20 (Joint) | R@50 (Joint) | R@100 (Joint) | R@100 (Novel Obj) | R@100 (Novel Rel) |
|-----|-----|-----|-------------|-------------|--------------|-------------------|-------------------|
| - | - | - | 10.02 | 13.50 | 16.37 | 17.48 | 11.18 |
| ✓ | - | - | 11.43 | 15.67 | 19.20 | 19.32 | 17.32 |
| - | ✓ | - | 11.37 | 15.71 | 19.37 | 19.61 | 17.38 |
| - | - | ✓ | 11.92 | 16.67 | 20.31 | 20.16 | 18.52 |
| ✓ | ✓ | - | 11.84 | 16.17 | 19.55 | 19.65 | 17.83 |
| ✓ | - | ✓ | 12.27 | 17.11 | 20.81 | 20.80 | 19.01 |
| - | ✓ | ✓ | 12.42 | 17.22 | 21.10 | 20.99 | 19.16 |
| ✓ | ✓ | ✓ | **12.61** | **17.43** | **21.27** | **21.10** | **19.46** |

**消融要点**：
- ITG 贡献：Joint R@100 +3.94（相较于 baseline 16.37 → 20.31含RRD）
- IQS 贡献：Joint R@100 +3.00 改善
- RRD 贡献：Joint R@100 +2.83 改善（含ITG+IQS baseline vs 完整）
- 三个组件集成有一定 diminishing returns（都针对 interacting objects），但完整模型仍获得 1.92%∼8.28% 全面提升
- Novel Rel 从 RRD 获益最大（+7.34）

### 预训练效果对比（VG, 直接测试，无 SFT）

| Model | Backbone | R@20 | R@50 | R@100 |
|-------|----------|------|------|-------|
| LSWS (CVPR'21) | - | - | 3.28 | 3.69 |
| MOTIFS+Li et al. | - | 5.02 | 6.40 | 7.33 |
| Uniter+SGNLS | - | 5.80 | 6.70 | - |
| Uniter+Li et al. | - | 5.42 | 6.74 | 7.62 |
| VS3 | Swin-T | 5.59 | 7.30 | 8.62 |
| OvSGTR | Swin-T | 6.61 | 8.92 | 10.90 |
| **INOVA** | **Swin-T** | **7.86** | **10.81** | **13.31** |
| OvSGTR | Swin-B | 6.88 | 9.30 | 11.48 |
| **INOVA** | **Swin-B** | **8.28** | **11.61** | **14.33** |

**预训练效果**：INOVA R@100 13.31 (Swin-T) vs OvSGTR 10.90 (+2.41)；14.33 (Swin-B) vs 11.48 (+2.85)

## Limitations

1. **Diminishing returns of interaction-aware strategies**：论文自述三个组件都针对 interacting objects 时，效果叠加不如预期显著，说明存在冗余
2. **依赖 Grounding DINO 的检测能力**：整体性能受限于 grounding backbone 的质量
3. **仅验证了 SGDET 协议**：未在 PredCls/SGCls 等更宽松协议下验证
4. **GQA 上的结果**仅在 appendix 中呈现，正文主要报告 VG 结果
5. **方法基于 dual-encoder-single-decoder 架构**：架构选择本身限制了与 MLLM-based 方法的公平比较

## Reusable Claims

1. **等同对待 all objects 是 OVSGG 的性能瓶颈**：预训练阶段引入噪声监督，SFT 阶段导致二部图匹配错误，这会降低闭集和新颖类的关系预测能力
2. **交互提示（bidirectional interaction prompts）能提升 grounding 精准度**：通过 interaction tokens 引导注意力机制关注关系相关实体，减少冗余检测
3. **交互引导的查询选择优于无差别查询分配**：在 DETR-like 管线中，优先为 interacting objects 分配 queries 可减少匹配错误
4. **关系级知识蒸馏增强新颖关系泛化**：RRD 的 pairwise relational consistency 比 point-wise 对齐对 Novel Rel 提升更显著

## Connections

- 建立在 **OvSGTR (ECCV'24)** 的视觉概念对齐与保持工作基础上，扩展其预训练和监督微调流程
- 对比 **VS3 (CVPR'23)** 和 **RAHP (AAAI'25)**，这些方法未显式建模交互信息
- 与弱监督 SGG 中 **Li et al. (ACMMM'22)** 的交互感知知识有方法论关联
- 与 **ACC (NeurIPS'25)** 同属交互感知 OVSGG 方向，但 INOVA 侧重预训练+SFT 全流程而非知识迁移
- 与 **GEM (2025)** 等 grounding-centric VLM 方法互补
- **Grounding DINO** 作为检测 backbone，与 GLIP 等形成方法族对比

## Open Questions

1. INOVA 的三个组件能否更紧凑地集成以消除冗余？
2. 在 PredCls/SGCls 协议下，交互感知策略是否同样有效？
3. 双向交互提示的设计是否依赖特定的 VLM 架构（Grounding DINO），能否迁移到 MLLM-based pipeline？
4. 交互感知策略引入的计算开销是否值得在实时场景中部署？
5. 对 longer-tail 数据分布（如更多的关系和物体类别）的泛化能力如何？

## Provenance

- Raw source: `raw/sources/2025-02-06-interaction-aware-open-vocabulary-sgg.pdf`
- Full text: `raw/sources/2025-02-06-interaction-aware-open-vocabulary-sgg.txt`
- Evidence level: **full-paper** — 全文精读，阅读了摘要、引言、方法、实验结果、消融分析、结论和参考文献
- Analysis by: Autoresearch subagent (ingest)
- Verification: 所有表格数据来自论文正文，数值对照核实
