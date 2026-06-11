---
title: "Interaction-Centric Knowledge Infusion and Transfer for Open-Vocabulary Scene Graph Generation (ACC)"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - scene-graph-generation
  - open-vocabulary-sgg
  - interaction-centric
  - interaction-driven
  - knowledge-infusion
  - knowledge-distillation
  - bidirectional-interaction-prompt
  - interaction-guided-query-selection
  - interaction-consistent-kd
  - ovsgg
  - end-to-end-sgg
  - NeurIPS-2025
  - arXiv-2025
raw_sources:
  - ../../../raw/sources/2025-arXiv-Interaction-Centric-Knowledge-Infusion-SGG.pdf
  - ../../../raw/sources/2025-arXiv-Interaction-Centric-Knowledge-Infusion-SGG.txt
related_pages:
  - ovsgtr-expanding-scene-graph-boundaries.md
  - cage-sgg-counterfactual-active-graph-evidence-open-vocabulary-sgg.md
  - language-supervised-open-vocabulary-scene-graph-vs3.md
evidence_level: full-paper
paper:
  title: "Interaction-Centric Knowledge Infusion and Transfer for Open-Vocabulary Scene Graph Generation"
  abbreviated: "ACC"
  authors:
    - Lin Li
    - Chuhan Zhang
    - Dong Zhang
    - Chong Sun
    - Chen Li
    - Long Chen
  affiliations:
    - HKUST
    - AI Chip Center for Emerging Smart Systems (ACCESS)
    - Tencent
  year: 2025
  venue: NeurIPS 2025 (39th Conference on Neural Information Processing Systems)
  arxiv: "2511.05935"
  code: https://github.com/HKUST-LongGroup/ACC
  url: https://arxiv.org/abs/2511.05935
  doi: null
classification:
  label: "Interaction-Centric Open-Vocabulary SGG"
  task:
    - Open-Vocabulary Scene Graph Generation (OVSGG)
    - Scene Graph Generation
    - Object Detection
    - Relation Recognition
  method_family:
    - Interaction-Centric Knowledge Infusion
    - Interaction-Centric Knowledge Transfer
    - Bidirectional Interaction Prompt (BIP)
    - Interaction-Guided Query Selection (IGQS)
    - Interaction-Consistent Knowledge Distillation (ICKD)
    - Grounding DINO
    - DETR-like Transformer
  modality:
    - Image
  setting:
    - OVR-SGG (novel relations)
    - OVD+R-SGG (novel objects + relations)
---

# ACC: Interaction-Centric Knowledge Infusion and Transfer for Open-Vocabulary Scene Graph Generation

> Lin Li, Chuhan Zhang, Dong Zhang, Chong Sun, Chen Li, Long Chen. NeurIPS 2025. arXiv:2511.05935.

## 核心思想

现有 OVSGG 方法采用 object-centric 范式——在知识注入和迁移阶段均未区分同一物体类别中"正在交互"和"非交互"的实例，导致：

1. **知识注入阶段**：仅依赖物体类别进行伪标注，产生大量噪声配对（如图中多个"man"和"surfboard"配对，错误匹配到"hold"关系）
2. **知识迁移阶段**：SFT 时的 bipartite graph matching 将非交互的物体 query 错误匹配到交互标注中的 target object

**ACC** 提出 interaction-centric 范式，在两个阶段显式建模交互关系：

### 方法概览

#### ① Interaction-Centric Knowledge Infusion — 双向交互提示（BIP）

使用 Grounding DINO 作为检测器，设计双向交互提示引导物体定位：

- **前向视角**：`"man hold surfboard"`（主体→关系→客体）
- **反向视角**：`"surfboard held by man"`（客体→关系→主体，利用 LLM 或 Pattern 库生成 counter-action）
- 通过 TE 注意力机制，将交互上下文注入 object tokens，区分交互/非交互物体
- 结合规则化 IoU 组合形成 triplet 伪标注

#### ② Interaction-Centric Knowledge Transfer

**a. Interaction-Guided Query Selection (IGQS) — 两阶段 query 选择**

- **Step I**：计算每个 visual token 与 object class tokens 和 relation class tokens 的最大相似度，选出 top-K 高相关 token
- **Step II**：将第一步预测的 triplet 分解为 ⟨subject, predicate⟩ 和 ⟨predicate, object⟩ 作为交互提示，编码后向 attention 机制注入交互信息；优先选择 L 个高交互相关 token，再补充 K-L 个高物体相关 token
- 效果：显著减少非交互候选，降低 bipartite graph matching 误匹配

**b. Interaction-Consistent Knowledge Distillation (ICKD)**

- **VRD（Visual-concept Retention Distillation）**：保持学生模型 edge feature 与教师模型的逐点语义一致（L1 loss on negative samples）
- **RRD（Relative-interaction Retention Distillation）**：对齐教师-学生间 triplet embedding 的结构相似性矩阵（Frobenius norm），区分交互对和背景

**总损失**：L = Lreg + Lgiou + Lobj + Lrel + β1·LVRD + β2·LRRD

## 实验结果

### VG 数据集（SGDET 协议）

#### OvR-SGG（novel relations only）

| Backbone | Method | Base+Novel R@100 | Novel(R) R@100 |
|----------|--------|:----------------:|:--------------:|
| Swin-T | VS3 (CVPR'23) | 17.30 | 0.00 |
| Swin-T | OvSGTR (ECCV'24) | 23.86 | 16.19 |
| Swin-T | RAHP (AAAI'25) | 25.74 | 19.92 |
| **Swin-T** | **ACC** | **27.40** | **21.70** |
| Swin-B | OvSGTR | 26.65 | 19.72 |
| **Swin-B** | **ACC** | **29.28** | **24.66** |

#### OvD+R-SGG（novel objects + relations）

| Backbone | Method | Joint R@100 | Novel(O) R@100 | Novel(R) R@100 |
|----------|--------|:----------:|:--------------:|:--------------:|
| Swin-T | OvSGTR | 16.37 | 17.48 | 11.18 |
| **Swin-T** | **ACC** | **21.27** | **21.10** | **19.46** |
| Swin-B | OvSGTR | 21.03 | 21.70 | 18.22 |
| **Swin-B** | **ACC** | **23.19** | **23.29** | **21.73** |

### GQA 数据集（OvD+R-SGG, Swin-T）

| Method | Joint R@100 | Novel(O) R@100 | Novel(R) R@100 |
|--------|:----------:|:--------------:|:--------------:|
| OvSGTR | 19.14 | 18.76 | 7.40 |
| **ACC** | **20.63** | **20.57** | **9.80** |

### PSG 数据集（OvR-SGG, Swin-T）

| Method | Base+Novel R@100 | Novel(R) R@100 |
|--------|:--------------:|:--------------:|
| SGTR (CVPR'22) | 18.2 | — |
| PGSG (CVPR'24) | 20.2 | — |
| OvSGTR | 19.50 | 8.08 |
| **ACC** | **21.71** | **9.70** |

### 预训练对比（COCO captions → VG 直接测试）

| Method | Backbone | R@100 |
|--------|----------|:-----:|
| OvSGTR | Swin-T | 10.90 |
| **ACC** | **Swin-T** | **13.31** |
| OvSGTR | Swin-B | 11.48 |
| **ACC** | **Swin-B** | **14.33** |

## 消融实验要点

- **BIP 有效性**（OvD+R-SGG, Swin-T）：BIP 带来 Joint R@100 +1.73%, Novel(O) +1.45%, Novel(R) +1.63%
- **IGQS**：Step I + Step II 联合使用最佳，单一 step 也有提升
- **ICKD**：VRD (+2.83% R@100), RRD (+2.83% R@100)，两者组合最佳
- **Verb Parser 鲁棒性**：Llama2 7B、Qwen2.5-0.5B、Pattern 库均有效，说明 BIP 对解析器选择不敏感
- **β1=0.1, β2=0.5** 为最佳超参组合

### HICO-DET 扩展实验

| Method | Base+Novel R@100 | Novel(R) R@100 |
|--------|:--------------:|:--------------:|
| OvSGTR | 39.04 | 31.84 |
| **ACC** | **40.19** | **34.38** |

## 分析与讨论

- **核心范式转变**：从 object-centric → interaction-centric，是所有组件设计的统一线索
- **计算开销**：Step I 几乎无额外开销（基础矩阵运算）；Step II 增加约 65% 推理时间（单次前向+二次 query 选择），但性能增益可选
- **局限**：主要依赖于 Grounding DINO 作为底层检测器；Step II 增加额外前向开销

## 代码与资源

- 代码仓库：[https://github.com/HKUST-LongGroup/ACC](https://github.com/HKUST-LongGroup/ACC)
- 第一作者 Lin Li 主页（HKUST Long Group）：lllidy@ust.hk

## 关联论文

- [OvSGTR: Fully Open-Vocabulary SGG](ovsgtr-expanding-scene-graph-boundaries.md) — ACC 的直接 baseline 和对比方法
- [CAGE-SGG: Counterfactual Active Graph Evidence for Open-Vocabulary SGG](cage-sgg-counterfactual-active-graph-evidence-open-vocabulary-sgg.md) — 另一个 OVSGG 方法
- [VS³: Language-supervised and Open-vocabulary SGG](language-supervised-open-vocabulary-scene-graph-vs3.md) — 早期 OVSGG 工作
