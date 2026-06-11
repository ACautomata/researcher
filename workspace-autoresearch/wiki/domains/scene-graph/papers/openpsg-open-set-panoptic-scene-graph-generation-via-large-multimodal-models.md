---
title: OpenPSG: Open-set Panoptic Scene Graph Generation via Large Multimodal Models
type: paper
domain: scene-graph
status: active
created: 2026-06-10
updated: 2026-06-10
tags:
  - scene-graph-generation
  - panoptic-scene-graph
  - open-vocabulary
  - ECCV-2024
  - LMM
  - open-set
source_pages: []
raw_sources:
  - raw/sources/2024-07-15-openpsg-open-set-panoptic-scene-graph-generation-via-large-multimodal-models.pdf
paper:
  title: "OpenPSG: Open-set Panoptic Scene Graph Generation via Large Multimodal Models"
  authors:
    - Zijian Zhou
    - Zheng Zhu
    - Holger Caesar
    - Miaojing Shi
  year: 2024
  venue: ECCV 2024
  arxiv: 2407.11213
  code: https://github.com/franciszzj/OpenPSG
classification:
  label: OpenPSG
  task:
    - Open-set Panoptic Scene Graph Generation
    - Open-set Relation Prediction
  method_family:
    - LMM-based Relation Decoding
    - Query-based Relation Feature Extraction
  modality:
    - Image
  datasets:
    - PSG
    - VG-150
  metrics:
    - Recall@K (R@K)
    - mean Recall@K (mR@K)
evidence_level: full-paper
---

## Citation

Zhou, Z., Zhu, Z., Caesar, H., & Shi, M. (2024). OpenPSG: Open-set Panoptic Scene Graph Generation via Large Multimodal Models. *ECCV 2024*. arXiv:2407.11213.

## One-Sentence Contribution

首次提出开放集全景场景图生成（OpenPSG）任务，利用大语言模型在自回归框架中实现开放集关系预测，在封闭集和开放集设定下均达到 SOTA。

## Problem Setting

**Open-set PSG**：给定图像 I，提取开放集全景场景图 G = {O, R}，其中对象类别 c 可属于预定义基类 **C_base** 或未见新类 **C_novel**，关系 r 可属于基类 **K_base** 或新类 **K_novel**。模型仅在基类关系上训练，测试时需同时预测基类和新类关系。

**子任务**：
- **PredCls**（谓词分类）：给定对象类别和位置，预测关系
- **SGDet**（场景图检测）：同时预测对象分割、类别和关系

**评估指标**：R@K 和 mR@K（K=20, 50, 100）

## Method

OpenPSG 由三个组件构成：

### 1. Object Segmenter（对象分割器）
- 使用预训练的开放集分割模型 **OpenSeeD** 预测对象掩膜、类别和全图视觉特征 F_I
- Patchify 模块将视觉特征序列化为视觉 token，并将掩膜reshape为序列
- Pairwise 模块枚举所有 subject-object 对，生成组合类别和联合掩膜

### 2. Relation Query Transformer（RelQ-Former）
受 BLIP-2 Q-Former 启发，设计两组可学习查询（query）：
- **Pair Feature Extraction Query**（32 个查询）：通过自注意力 + 掩膜交叉注意力从全图视觉特征中提取subject-object对的交互特征，输出 F_pair(i,j)_I ∈ R^(32×D)
- **Relation Existence Estimation Query**（1 个查询）：判断对象对是否存在关系，使用 2 层 MLP + sigmoid 输出分数
- **Selector**：过滤分数低于阈值 θ=0.35 的对象对，实现 ~20× 推理加速

### 3. Multimodal Relation Decoder（RelDecoder）
基于 **BLIP-2 解码器**，设计了两种指令：

- **Generation Instruction（OpenPSG-G）**："What are the relations between c_i and c_j?"，模型自回归生成所有可能关系，[SEP] 分隔
- **Judgement Instruction（OpenPSG-J）**："Please judge between c_i and c_j whether there is a relation r_k"，模型回答 Yes/No。通过缓存 prefix 特征，对每个候选关系只需处理关系名部分，推理时间与 Generation 持平

**默认使用 OpenPSG-J**（Judgement Instruction）。

### 训练
- 总损失：L = λ·L_exist + L_LM（λ=10）
- L_exist：二分类交叉熵（关系存在预测）
- L_LM：交叉熵（语言模型预测）
- 冻结 Object Segmenter 和 Multimodal Relation Decoder，仅训练 RelQ-Former
- AdamW 优化器，lr=1e-4，weight decay=5e-2，12 epochs（第 8 epoch 降至 1e-5）
- 4×A100 GPU

## Experiments

### 数据集
- **PSG Dataset**：基于 COCO，48,749 张图像（46,563 训练 / 2,186 测试），80 thing + 53 stuff 对象类，56 关系类
- **VG-150**（Visual Genome）：150 对象类，50 关系类

### 评估协议
- 封闭集：所有关系类上训练和测试
- 开放集：按 7:3 比例划分基类:新类，仅在基类关系上训练，测试全部关系

### Baselines（PSG 子任务）
- **PredCls**：IMP, Motifs, VCTree, GPSNet
- **SGDet**：IMP, Motifs, VCTree, GPSNet, PSGTR, PSGFormer, ADTrans, PairNet, HiLo

### Baselines（VG）
- 封闭集：Motifs, VCTree
- 开放集：Cacao+Epic, OvSGTR

### 消融实验
1. **分割器对比**：OpenSeeD vs Mask2Former（OpenSeeD 的 PQ 55.1 vs 51.7，SGDet R@100 高 3.5%）
2. **特征提取方式**：RelQ-Former 注意力 vs Mask Pooling（R@100 +5.2%，mR@100 +4.7%）
3. **Selector 效果**：θ=0（不过滤）性能持平，但推理慢 20×
4. **Relation Existence Loss**：移除后 R@100 降 0.8%，mR@100 降 0.6%
5. **指令类型对比**（不同 base:novel 比例）：OpenPSG-J 始终优于 OpenPSG-G，且随 novel 比例增大优势更明显

## Results

### PSG 封闭集（Train on all relations）

| 子任务 | 指标 | OpenPSG | 之前最佳 | 提升 |
|--------|------|---------|---------|------|
| PredCls | R@100 | **79.3%** | 52.7% (VCTree) | **+26.6%** |
| PredCls | mR@100 | **63.8%** | 38.8% (ADTrans) | **+25.0%** |
| SGDet | R@100 | **52.0%** | 43.0% (HiLo) | **+9.0%** |
| SGDet | mR@100 | **50.1%** | 33.1% (HiLo) | **+17.0%** |

### PSG 开放集（Train on base, test on all, 7:3）

| 子任务 | R@20 | mR@20 | R@50 | mR@50 | R@100 | mR@100 |
|--------|------|-------|------|-------|-------|--------|
| PredCls | 45.1 | 29.1 | 55.5 | 38.7 | **61.5** | **46.0** |
| SGDet | 25.9 | 20.9 | 31.6 | 24.0 | **36.7** | **25.4** |

> 注：开放集 PredCls R@100=61.5% 甚至超过了部分先前方法在封闭集全量训练上的结果（Motifs R@100=52.4%, VCTree R@100=52.7%）。

### VG PredCls

| 场景 | R@50 | mR@50 | R@100 | mR@100 |
|------|------|-------|-------|--------|
| 封闭集 | 60.2 | 45.8 | **71.4** | **50.3** |
| 开放集 | 25.7 | 21.5 | **30.6** | **27.2** |

开放集设定下，OpenPSG 超过 OvSGTR（R@100 26.7%）和 Cacao+Epic（mR@100 21.8%），提升分别为 +3.9%（R@100）和 +5.4%（mR@100）。

### 指令类型对比（PSG PredCls 开放集）

| base:novel | OpenPSG-G R@100 | OpenPSG-G mR@100 | OpenPSG-J R@100 | OpenPSG-J mR@100 |
|-----------|-----------------|------------------|-----------------|------------------|
| 7:3 | 57.1 | 36.8 | **61.5** | **46.0** |
| 6:4 | 52.9 | 32.0 | **57.0** | **43.5** |
| 5:5 | 40.1 | 24.2 | **50.3** | **40.8** |
| 4:6 | 33.2 | 18.8 | **44.3** | **34.7** |
| 3:7 | 18.5 | 14.4 | **35.1** | **23.7** |

OpenPSG-J 在 novel 比例增大时衰减更缓（R@100 从 61.5%→35.1%，降幅 26.4%；OpenPSG-G 从 57.1%→18.5%，降幅 38.6%）。

## Limitations

1. **强依赖分割器质量**：OpenPSG 的 SGDet 性能高度依赖前段 OpenSeeD 的 panoptic segmentation 质量，分割错误会级联到关系预测
2. **计算开销**：尽管 Selector 实现了 20× 加速，但 LMM 自回归解码在多对象密集场景中仍可能成为瓶颈
3. **无真正零样本能力**：模型仍需在基类关系上训练进行 few-branch 学习，无法做到完全的 zero-shot 关系预测
4. **未探索模型蒸馏**：作者在 Conclusion 中提及计划使用蒸馏减小模型规模但未在本文中实现

## Reusable Claims

- **LMM 自回归解码适合开放集关系预测**：将关系预测转化为文本生成问题，避免了预设关系类别列表的限制
- **Judgement Instruction 优于 Generation Instruction**：将"生成所有关系"转化为"判断特定关系是否存在"，在大幅增加 novel 比例时更鲁棒
- **RelQ-Former 的交互注意力优于 Mask Pooling**：通过注意力机制聚焦对象间交互区域而非均匀掩膜池化，关系预测更准确
- **OpenPSG 的封闭集性能也大幅领先**：即使在封闭集设定下，使用 LMM 的方法也远超传统方法（+26.6% PredCls R@100），表明 LMM 在关系理解上的优势

## Connections

- [[reltr-relation-transformer-scene-graph-generation|RelTR]]、[[sgtr-end-to-end-scene-graph-generation-with-transformer|SGTR]]、[[dsgg-dense-relation-transformer-end-to-end-scene-graph-generation|DSGG]]：DETR 风格的端到端场景图生成方法
- [[ovsgtr-expanding-scene-graph-boundaries|OvSGTR]]：同样研究开放集/开放词汇 SGG，使用视觉-概念对齐
- [[pixels-to-graphs-open-vocabulary-sgg-vlm|PGSG]]：利用 VLM 进行开放词汇 SGG
- [[language-supervised-open-vocabulary-scene-graph-vs3|VS³]]：语言监督的开放词汇 SGG
- [[sdsgg-scene-specific-description-ovsgg|SDSGG]]：使用 LLM 进行场景描述的开放词汇 SGG
- [[cage-sgg-counterfactual-active-graph-evidence-open-vocabulary-sgg|CAGE-SGG]]：开放词汇 SGG，使用反事实主动图证据
- [[textpsg-panoptic-scene-graph-from-textual-descriptions|TextPSG]]：文本驱动的全景场景图生成
- [[adtrans-adaptive-data-transfer-panoptic-scene-graph-debiasing|ADTrans]]：全景场景图生成的语义原型学习
- [[hilo-exploiting-high-low-frequency-for-unbiased-panoptic-scene-graph-generation|HiLo]]：全景场景图生成的偏置缓解方法

## Open Questions

1. OpenPSG 能否与更强/更小的 LMM（如 LLaVA-NeXT, Phi-3-Vision）结合，降低计算成本？
2. 如何实现真正的 zero-shot 关系预测，而不需要任何基类关系的训练？
3. 与 [[dsflash-comprehensive-panoptic-scene-graph-generation-realtime|DSFlash]] 等实时方法相比，OpenPSG 的推理速度差距有多大？
4. 开放集关系预测能否扩展到视频/4D 场景？

## Provenance

- **raw source**: `raw/sources/2024-07-15-openpsg-open-set-panoptic-scene-graph-generation-via-large-multimodal-models.pdf`
- **extracted text**: `raw/sources/2024-07-15-openpsg-open-set-panoptic-scene-graph-generation-via-large-multimodal-models.txt`
- **evidence_level**: full-paper — 全文精读，所有数字来自论文正文和表格，提取完整
