---
title: "SGG-R/3: From Next Token Prediction to End-to-End Unbiased Scene Graph Generation"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - scene-graph-generation
  - unbiased-sgg
  - reinforcement-learning
  - chain-of-thought
  - large-language-models
  - mllm
  - policy-optimization
  - relation-augmentation
  - arxiv-2026
raw_sources:
  - ../../../sources/scene-graph/2026-06-09-sgg-r3-from-next-token-prediction-to-e2e-unbiased-sgg.pdf
  - ../../../sources/scene-graph/2026-06-09-sgg-r3-from-next-token-prediction-to-e2e-unbiased-sgg.txt
evidence_level: full-paper
paper:
  title: "SGG-R/3: From Next Token Prediction to End-to-End Unbiased Scene Graph Generation"
  abbreviated: "SGG-R/3"
  authors:
    - Jiaye Feng
    - Qixiang Yin
    - Yuankun Liu
    - Tong Mo
    - Weiping Li
  affiliations:
    - School of Software and Microelectronics, Peking University
    - Zhongguancun Academy, Beijing
  year: 2026
  venue: arXiv 2026
  arxiv: null
  code: null
  url: null
related_pages:
  - r1-sgg-reasoning-driven-scene-graph-generation.md
  - cage-sgg-counterfactual-active-graph-evidence-open-vocabulary-sgg.md
  - compositionally-feature-augmentation-for-unbiased-scene-graph-generation.md
  - hilo-exploiting-high-low-frequency-for-unbiased-panoptic-scene-graph-generation.md
  - eicr-environment-invariant-curriculum-relation-learning-sgg.md
  - dsgg-dense-relation-transformer-end-to-end-scene-graph-generation.md
  - relic-sgg-relation-lattice-completion-open-vocabulary-sgg.md
---

# SGG-R/3: From Next Token Prediction to End-to-End Unbiased Scene Graph Generation

## 核心思想

现有的基于 MLLM 的端到端 SGG 方法受限于缺乏任务特定的结构化推理，以及稀疏长尾关系分布的挑战，导致低召回和有偏预测。SGG-R/3 提出一个结构化推理框架，将 CoT 引导的 SFT 和 RL 结合 Group Sequence Policy Optimization (GSPO)，通过三阶段渐进式推理实现端到端无偏场景图生成。

### 方法总览

1. **SFT 阶段**：使用类型感知的关系增强（Type-aware Relation Augmentation）策略，通过 MLLM 生成额外关系三元组并用 embedding 相似性过滤，缓解关系稀疏问题
2. **RL 阶段**：提出**阶段对齐奖励方案**（Stage-aligned Reward Scheme），其中核心是**双粒度关系奖励**（Dual-granularity Reward），结合细粒度（谓语级）和粗粒度（聚类级）奖励，通过频率自适应加权缓解长尾问题
3. **三阶段结构化推理**：类别检测（Category Detection）→ 实例定位（Instance Grounding）→ 多类型关系提取（Multi-type Relation Extraction），使用 `<CATEGORY>`/`<OBJECT>`/`<RELATION>` 标签标记

## Problem Setting

- **任务**：端到端 Scene Graph Generation（SGDet 协议），模型需从图像直接生成场景图，没有 ground-truth 检测框
- **评估**：Recall@K, mean Recall@K (mR@K), zero-shot Recall@K (zsR@K)，K=100，遵循 SGDET 协议（IoU≥0.5 的边界框匹配）
- **数据集**：VG150（150 对象类、50 关系类，56,224 训练/5,000 验证/14,700 测试）和 PSG（80 thing 类、53 stuff 类、56 关系类，46,563 训练/2,186 测试）

## 方法

### 三阶段结构化推理（Section 3.2）

- **Stage 1: Object Category Detection**：模型先识别图像中存在的对象类别，缩小搜索空间，避免直接边界框检测导致的误差传播
- **Stage 2: Object Instance Grounding**：基于 Stage 1 的类别集合，逐类检测和定位所有对象实例，使用 `<OBJECT>` 标签
- **Stage 3: Multi-type Relation Extraction**：提取（subject-predicate-object）关系三元组。在 VG150 中使用 spatial/possessive/interactive 三类，PSG 中使用 spatial/static-interactive/dynamic-interactive 三类。输出按 Stage 2 的 subject 实例顺序排列

所有阶段在单次推理中完成。

### 类型感知关系增强（Section 3.3）

- 基于 Qwen2.5-VL-32B 为 SFT 数据增强
- 首先生成图像描述，再基于描述和预定义谓语类型生成关系三元组
- 经规则启发式过滤（subject/object 须为 GT 实体，谓语严格属于可用类别集）
- 随后通过 Sentence-BERT embedding 余弦相似度过滤：若生成三元组的 embedding 与任一 GT 三元组 embedding 的余弦相似度 ≥ 阈值 θ，则保留
- 大幅增加训练示例并引入语义多样性

### 双粒度关系奖励（Section 3.4）

- **细粒度奖励（Fine-grained Relation Reward）**：对每个三元组计算正确性（基于 predicate 类别），使用频率自适应权重，稀有谓词被赋予更高权重
- **粗粒度奖励（Coarse-grained Relation Reward）**：将谓语通过语义聚类映射到语义簇，在簇层面评估关系多样性
- 两奖励组合缓解长尾分布

### 训练流程

1. SFT：在增强数据上微调 Qwen2.5-VL-3B，学习结构化输出格式
2. SFT→RL 初始化：SFT 模型作为 RL 的初始化
3. RL with GSPO：基于 TRL 实现，使用 vLLM 加速采样。训练于 8×NVIDIA A800 (40GB)

## 实验结果

### VG150 — SGDet 任务（Table 1）

| 方法 | 参数量 | R@100 | mR@100 | Mean | zsR@100 |
|------|--------|-------|--------|------|---------|
| DSGG | — | 38.5 | 17.3 | 27.9 | 3.9 |
| VS3 | — | 40.9 | 7.8 | 24.4 | — |
| OwSGG | 72B | 3.2 | 3.4 | 3.3 | 2.0 |
| R1-SGG | 7B | 27.6 | 10.9 | 19.3 | 4.4 |
| **SGG-R/3 (SFT)** | 3B | 17.5 | 8.2 | 12.9 | 2.4 |
| **SGG-R/3 (SFT+RL)** | 3B | **36.0** | **14.8** | **25.4** | **6.1** |

- mR@100 = **14.8**（VLM-based 方法中 SOTA），Mean = **25.4**（所有方法第二）
- zsR@100 = **6.1**（**超越所有非 VLM 方法**），R@100 = **36.0**
- SFT 阶段模型性能较低，但经过 RL 阶段后全面大幅提升

### PSG — SGDet 任务（Table 2）

| 方法 | 参数量 | R@100 | mR@100 | Mean | zsR@100 |
|------|--------|-------|--------|------|---------|
| HiLo | — | 51.4 | 40.9 | 46.2 | — |
| DSGG | — | 50.0 | 43.4 | 46.7 | — |
| R1-SGG | 7B | 43.5 | 33.2 | 38.4 | 7.7 |
| Relation-R1 | 3B | 25.9 | 21.3 | 23.6 | — |
| **SGG-R/3 (SFT)** | 3B | 33.3 | 26.1 | 29.7 | 0.0 |
| **SGG-R/3 (SFT+RL)** | 3B | **52.5** | **44.3** | **48.4** | **7.7** |

- R@100 = **52.5**（**SOTA**，超越 HiLo 51.4），mR@100 = **44.3**（SOTA，超越 DSGG 43.4）
- Mean = **48.4**（**所有方法第一**）
- zsR@100 = **7.7**（与 R1-SGG 并列最佳 VLM 方法）

### MLLM 方法比较（Table 3）

- SGG-R/3 2B SFT 模型在 VG150 上的输出故障率（Failure Rate）降低 **57.23%**
- 3B SFT+RL 模型：在 VG150 上 mR@100 提升 1.25% vs 7B 基线，PSG 上提升 4.62%
- 关系增强策略进一步降低了输出故障率

### 关系覆盖分析（Figure 4）

- 在 VG150 上，启用 RA（关系增强）后：SFT 平均关系数/图从 7.3 提升至 20.3，SFT+RL 从 59.5 提升至 65.3
- 在 PSG 上，启用 RA 后：SFT 从 9.4 提升至 20.8，SFT+RL 从 60.0 提升至 69.7
- 关系增强显著提升生成关系的覆盖率，缓解稀疏问题

### 消融结论（文中定性描述）

- SFT 虽有结构化输出能力，但受限于稀疏标注，性能低
- RL 阶段带来全面大幅提升（SFT→SFT+RL 在所有指标上跳跃式增长）
- 关系增强（RA）在所有设置下提升平均关系数量
- 等价数据量训练下，SGG-R/3 的 CoT 框架显著优于无结构化推理的基线

## 核心贡献

1. 提出三阶段结构化推理（类别→实例→多类型关系），将无序 SGG 转化为系统化顺序生成，所有阶段在单次推理完成
2. 类型感知关系增强策略（MLLM 生成 + embedding 过滤），缓解关系稀疏和长尾问题
3. 双粒度关系奖励融合细粒度谓语级和粗粒度语义簇级奖励，频率自适应加权
4. 首次将 GSPO（Group Sequence Policy Optimization）应用于 SGG 任务
5. 在 VG150 和 PSG 两个 benchmark 上端到端 SGG 达到 SOTA / 领先性能

## 局限性

- MLLM 导致的非可忽略推理延迟，限制实时应用
- 关系增强无法保证三元组完全准确，增广数据质量构成性能上限
- 当前限于闭集词汇，无法识别未见关系（future work 指向开放词汇扩展）

## 源码

- 基于 TRL 库 + vLLM，base 模型为 Qwen2.5-VL-3B
- 训练硬件：8×NVIDIA A800 (40GB)
- 代码链接：论文未提供公开代码仓库

## 对比 R1-SGG

与同团队的 R1-SGG (Qwen2-VL 7B) 相比：
- SGG-R/3 (3B) 参数更少但性能全面超越 R1-SGG (7B)
- VG150：SGG-R/3 R@100 36.0 vs R1-SGG 27.6（+8.4），mR@100 14.8 vs 10.9（+3.9），zsR@100 6.1 vs 4.4（+1.7）
- PSG：SGG-R/3 R@100 52.5 vs R1-SGG 43.5（+9.0），mR@100 44.3 vs 33.2（+11.1），zsR@100 7.7 vs 7.7（平）
- 差异在于 SGG-R/3 使用了更强的 base model (Qwen2.5-VL)、CoT SFT（结构化三阶段推理）和 RL with GSPO + 语义增强

*最后更新：2026-06-09 | 证据等级：full-paper*
