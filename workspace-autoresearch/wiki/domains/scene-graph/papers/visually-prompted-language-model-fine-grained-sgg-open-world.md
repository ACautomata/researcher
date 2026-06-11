---
title: Visually Prompted Language Model for Fine-Grained Scene Graph Generation in an Open World
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags: [SGG, open-world, long-tail, visual-prompt, language-model, fine-grained, zero-shot]
source_pages: []
raw_sources:
  - raw/sources/2023-ICCV-visually-prompted-language-model-fine-grained-sgg-open-world.pdf
  - raw/sources/2023-ICCV-visually-prompted-language-model-fine-grained-sgg-open-world.txt
paper:
  title: "Visually Prompted Language Model for Fine-Grained Scene Graph Generation in an Open World"
  authors:
    - Qifan Yu
    - Juncheng Li
    - Yu Wu
    - Siliang Tang
    - Wei Ji
    - Yueting Zhuang
  year: 2023
  venue: ICCV 2023
  arxiv: 
  doi:
  code: https://github.com/Yuqifan1117/CaCao
  project:
classification:
  label: CaCao / Epic
  task: [Scene Graph Generation, Open-World Predicate SGG]
  method_family: [Visually-Prompted Language Model, Cross-modal Prompt Learning, Data Enhancement]
  modality: [Image, Text]
  datasets: [VG-50, GQA-200, VG-1800]
  metrics: [mR@K, Tail-R@K, R@K, Acc@1/10]
evidence_level: full-paper
---

# Visually Prompted Language Model for Fine-Grained Scene Graph Generation in an Open World

## Citation

> Qifan Yu, Juncheng Li, Yu Wu, Siliang Tang, Wei Ji, Yueting Zhuang. "Visually Prompted Language Model for Fine-Grained Scene Graph Generation in an Open World." ICCV 2023.

## One-Sentence Contribution

提出 CaCao（Cross-modal prediCate boosting）框架，通过视觉提示语言模型生成多样化的细粒度谓词以缓解长尾分布问题，并进一步提出 Epic（Entangled cross-modal prompt）方法实现开集谓词场景图生成的零样本泛化。

## Problem Setting

- **长尾分布问题**：SGG 中尾部谓词标注数据少，训练成本高且难以区分。
- **开集谓词 SGG**：现有方法仅限于预定义谓词集合，无法泛化到未见谓词。
- **细粒度区分**：头部谓词（on, in）主导预测，导致细粒度谓词被压制。

## Method

### CaCao（Cross-modal prediCate boosting）

CaCao 是一个即插即用的框架，自动增强现有 SGG 模型以应对长尾问题，包含三个核心模块：

1. **Visually-Prefixed Prompt (VPT)**：以 ViT 作为图像编码器，提取视觉特征作为前缀视觉提示，引导语言模型。
2. **Textual Prompt (TPT)**：在 BERT 输入中加入可学习的文本提示令牌，实现文本语义对齐。
3. **Adaptive Semantic Cluster Loss (ASCL)**：自适应语义聚类损失，鼓励生成多样化的细粒度谓词。

CaCao 先通过视觉提示语言模型生成多样化的高质量谓词三元组，然后用这些增强三元组辅助 SGG 模型训练，使模型关注尾部谓词。

### Epic（Entangled Cross-Modal Prompt for Open-World Predicate SGG）

基于 CaCao 生成的丰富谓词，Epic 进一步实现开集谓词场景图生成：

- **交叉纠缠提示**：构建视觉感知提示和文本感知提示，分别注入到文本编码器和图像编码器。
- **零样本泛化**：训练的模型能泛化到训练中未见的谓词类别。

## Experiments

### 数据集与设置

- **标准 SGG**：VG-50（50 谓词类，150 对象类）
- **大规模 SGG**：GQA-200、VG-1800（谓词更多样）
- **开集谓词 SGG**：从 VG-50 中划分 70% 谓词为 base set，30% 稀有谓词为 novel set
- **评估指标**：mR@K（Mean Recall@K）、Tail-R@K（尾部 50% 谓词的 Recall@K）、base/novel R@K、Acc@1/10

### 实现细节

- 视觉提示语言模型：ViT 图像编码器 + BERT 语言模型，视觉提示长度 50，可学习文本令牌 10
- SGG 骨干：Faster R-CNN (ResNet-101-FPN) + Motif/VCTree/Transformer
- 开集设置：CLIP 作为骨干，InfoNCE 损失，双线性投影

### Baselines

- 对比方法包括：Motif、VCTree、Transformer、BGNN、PCPL、SSRCNN 及其增强变体
- 数据增强方法：IETrans、VisualDS、DLFE、FGPL
- 重平衡策略：Resample、Reweight、TDE（因果规则）

## Results

### 标准 SGG（VG-50）

**CaCao 在三个骨干上一致提升 mR@K 和 Tail-R@K：**

- **Motif+CaCao**：PredCls mR@100 38.9% → baseline Motif 16.2%（+22.7%）
- **VCTree+CaCao**：PredCls mR@100 40.8% → baseline VCTree 16.1%（+24.7%）
- **Transformer+CaCao**：PredCls mR@100 **43.7%** → baseline Transformer 17.6%（+26.1%）

CaCao 显著超越模型无关数据增强方法 IETrans（3.9%~5.8% Tail-R@20 提升，0.7%~7.1% mR@20 提升），也超越强特定模型 FGPL（3.0%~8.7% mR@20 提升）。

**细粒度谓词示例**：'flying in' 预测比例从 8%（Transformer）提升到 40%（Transformer+CaCao）。

### 大规模 SGG（VG-1800）

- **Motif+CaCao**：PredCls mR@100 10.8 → baseline Motif 2.6（+8.2）
- 在 GQA-200 上也有一致改进（e.g., SGDet mR@100 +11.9% with Motif）

### 开集谓词 SGG

- **Epic（VG+CaCao）**：novel R@100 达到 **18.3**（vs backbone w/o Epic 的 8.7）
- novel R@50 达到 13.9（vs 6.4），novel 类别改进达 **9.6%**
- base R@50/100 也提升至 28.3/31.1（vs 17.6/21.1）

### Ablation Study

| 模块 | Acc@1 | Acc@10 |
|------|-------|--------|
| Backbone | 0.08% | 0.21% |
| w/o ASCL | 0.38% | 0.74% |
| w/o TPT | 0.47% | 0.80% |
| w/o VPT | 0.25% | 0.68% |
| Full CaCao | **0.74%** | **0.92%** |

### 方法性能对比

| Method | PredCls mR@100 | SGCls mR@100 | SGDet mR@100 |
|--------|---------------|--------------|--------------|
| Motif | 16.2 | 9.3 | 7.8 |
| +IETrans | 39.1 | 22.8 | 18.0 |
| +CaCao (ours) | **38.9** | **24.4** | **20.0** |
| Transformer | 17.6 | 10.7 | 9.6 |
| +IETrans | 38.0 | 22.3 | 18.1 |
| +CaCao (ours) | **43.7** | **25.0** | **22.1** |
| VCTree | 16.1 | 12.0 | 8.3 |
| +CaCao (ours) | **40.8** | **28.7** | **19.1** |

## Limitations

- CaCao 的多阶段流程（先生成谓词再训练 SGG）可能增加训练复杂度。
- Epic 在开集设置中依赖 CaCao 生成的谓词质量，生成噪声可能影响泛化。
- 方法在 VG-1800 等极度长尾场景下 mR@K 绝对值仍较低（<15%），说明极度长尾仍有挑战。
- 未提供在更多样化的视觉 backbone（如 DINOv2）下的实验。

## Reusable Claims

1. **视觉提示语言模型**可以有效为尾部谓词生成多样化的高质量三元组，是缓解 SGG 长尾问题的有效数据增强策略。
2. **即插即用性**：CaCao 可灵活集成到多种 SGG 骨干（Motif/VCTree/Transformer/SSRCNN）中，是一种模型无关方法。
3. **交叉纠缠提示**（Epic）通过视觉和文本的互相条件提示实现开集谓词泛化，展示了从闭集到开集 SGG 的可行路径。
4. 数据增强方法（生成式）优于采样和重加权策略，特别是在大规模长尾场景中。
5. 细粒度谓词的区分能力提升可以直接改善 SGG 的整体质量，而不只是偏向头部谓词。

## Connections

- **IETrans [60]**：数据增强 SGG 方法，CaCao 与其定位类似但采用生成式方式且性能更优。
- **FGPL [39]**：细粒度谓词学习，CaCao 在某些设置下超越 FGPL 3~9%。
- **CLIP [42]**：Epic 使用 CLIP 作为开集设置的 backbone。
- **TDE [47]**：因果去偏方法，CaCao 在 mR@K 上显著超越 TDE。
- 与 [[ovsgtr-expanding-scene-graph-boundaries.md|OvSGTR]] 不同，OvSGTR 关注完全的 open-vocabulary SGG 端到端设置，CaCao+Epic 更侧重于通过数据增强和提示学习实现开集能力。
- 与 [[open-world-scene-graph-generation-using-vlm.md|OwSGG]] 相关，都涉及开集/开世界 SGG，但 CaCao+Epic 侧重于谓词层面的零样本泛化，OwSGG 更关注整体对象+关系开集。

## Open Questions

- CaCao 生成的谓词质量如何自动评估？目前依赖 SGG 下游任务间接验证。
- Epic 在 base/novel 之外能否扩展到完全未见对象的设置？
- 视觉提示长度和学习令牌数量的敏感性如何？

## Provenance

- 原始 PDF: `raw/sources/2023-ICCV-visually-prompted-language-model-fine-grained-sgg-open-world.pdf`
- 提取文本: `raw/sources/2023-ICCV-visually-prompted-language-model-fine-grained-sgg-open-world.txt`
- 证据等级: full-paper（全文提取并精读）
