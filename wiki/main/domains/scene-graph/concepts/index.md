# SGG Key Concepts

> 场景图生成研究的核心概念体系。

## 定义

### Scene Graph
有向图 $G=(O,R)$，其中 $O$ 为对象节点（含边界框和类别标签），$R$ 为关系边（subject-predicate-object 三元组）。场景图是图像的结构化表示，编码了视觉内容中的实体、属性和关系。

### Scene Graph Generation (SGG)
给定图像 $I$，预测 $(O,R)$。通常分解为：对象检测 → 关系分类。三个标准子任务：

| 子任务 | 输入 | 输出 |
|--------|------|------|
| **Predicate Classification (PredCls)** | GT 框 + GT 标签 | 关系谓词 |
| **Scene Graph Classification (SGCls)** | GT 框 | 对象类别 + 关系 |
| **Scene Graph Detection (SGDet)** | 原始图像 | 框 + 类别 + 关系 |

### Panoptic Scene Graph (PSG)
用 panoptic segmentation mask 替代边界框的扩展。每个对象是像素级片段，支持细粒度关系推理。

---

## 核心挑战

### Long-Tail Bias
谓词类别遵循长尾分布：head 谓词（"on"、"has"）占训练样本大多数，tail 谓词（"eating"、"holding"）极少。模型倾向预测常见谓词而非视觉内容匹配的谓词。

**关键论文**: [[eicr-environment-invariant-curriculum-relation-learning-sgg|EICR]], [[compositional-feature-augmentation-for-unbiased-scene-graph-generation|CFA]], [[unbiased-scene-graph-generation-tde-causal-modeling|TDE]], [[sbgg-fine-grained-sgg-sample-level-bias-prediction|SBG]]

### Context Imbalance
不同 subject-object 对出现频率差异巨大。如 "(人，衬衫)" 常配对 "穿着"，但 "(人，靴子)" 几乎不出现。模型学到实体交互与谓词之间的伪相关。

**关键论文**: [[eicr-environment-invariant-curriculum-relation-learning-sgg|EICR]], [[fast-contextual-scene-graph-generation|Fast Contextual SGG]]

### Task Gap (PredCls → SGCls → SGDet)
SGDet 最困难：需要从原始图像同时检测对象和关系，对象检测错误会级联到关系预测中。SGTR、RelTR 等端到端方法尝试缓解这一级联问题。

### Open-Vocabulary Gap
训练时未见过的谓词/对象类别。需要利用语言模型或 VLMs 的零样本泛化能力。

---

## 方法论概念

### 关系建模

| 方法 | 核心思想 | 代表论文 |
|------|---------|---------|
| Message Passing | 对象间信息传递聚合上下文特征 | [[squat-selective-quad-attention-scene-graph-generation|SQuAT]] |
| Transformer Attention | 自注意力/交叉注意力联合建模对象-关系交互 | [[reltr-relation-transformer-scene-graph-generation|RelTR]], [[sgtr-end-to-end-scene-graph-generation-transformer|SGTR]] |
| Set Prediction | 将 SGG 视为集合预测问题，DETR 风格 | [[dsgg-dense-relation-transformer-end-to-end-scene-graph-generation|DSGG]], [[sgtr-end-to-end-scene-graph-generation-transformer|SGTR]] |
| Hybrid Assignment | 一阶段 + 多分支指派 | [[hydra-sgg-hybrid-relation-assignment-one-stage|Hydra-SGG]] |

### 去偏方法

| 类别 | 思想 | 代表论文 |
|------|------|---------|
| Causal Inference | 因果干预消除频率混淆 | [[unbiased-scene-graph-generation-tde-causal-modeling|TDE]], [[reverse-causal-framework-sgg|RcSGG]] |
| Counterfactual | 反事实推理对比真实-反事实结果 | [[cage-sgg-counterfactual-active-graph-evidence-open-vocabulary-sgg|CAGE-SGG]], [[camodule-causal-adjustment-module-debiasing-scene-graph-generation|CAModule]] |
| Curriculum Learning | 从易到难渐进去偏 | [[eicr-environment-invariant-curriculum-relation-learning-sgg|EICR]], [[cafe-curricular-shape-aware-panoptic-scene-graph-generation|CAFE]] |
| Salience Estimation | 估计谓词显著性筛选正确关系 | [[salience-sgg-unbiased-scene-graph-generation-via-salience-estimation|Salience-SGG]] |

### 开放词汇学习
利用 CLIP/VLM 嵌入空间或语言驱动的原型向量，泛化到训练时未见过的谓词和对象。

**核心策略**:
- **CLIP 对齐**: [[ccl-3dsgg-clip-driven-open-vocabulary-3d-scene-graph-generation|CCL-3DSGG]], [[language-supervised-open-vocabulary-scene-graph-vs3|VS3]]
- **LLM/VLM 引导**: [[sdsgg-scene-specific-description-ovsgg|SDSGG]], [[openpsg-open-set-panoptic-scene-graph-mllm|OpenPSG]]
- **知识注入**: [[acc-interaction-centric-knowledge-infusion-sgg|Interaction-Centric Knowledge Infusion]], [[relic-sgg-relation-lattice-completion-open-vocabulary-sgg|ReLIC-SGG]]

### 一体化/端到端 SGG
一次性预测所有对象和关系，避免级联误差：

- [[sgtr-end-to-end-scene-graph-generation-transformer|SGTR]] (CVPR 2022) — 端到端 Transformer
- [[dsgg-dense-relation-transformer-end-to-end-scene-graph-generation|DSGG]] (CVPR 2023) — 密集关系 Transformer
- [[reltr-relation-transformer-scene-graph-generation|RelTR]] (CVPR 2022) — 关系 Transformer

### 交互级关系建模
从细粒度级别建模对象间交互，而非简单的视觉特征拼接：

- **Superpixel Interaction Learning**: [[superpixel-interaction-learning-scene-graph-generation|Superpixel Interaction Learning]]
- **Pair Proposal Network**: [[pair-net-panoptic-scene-graph-generation|Pair-Net]]

---

## 关键论文参考
