---
title: Correspondence Coverage Matters for Multi-Modal Dataset Distillation
type: paper
domain: distillation
status: stable
created: 2026-04-20
updated: 2026-05-05
tags:
  - dataset-distillation
  - multimodal-learning
  - computer-vision
  - aaai-2026
paper:
  title: Correspondence Coverage Matters for Multi-Modal Dataset Distillation
  authors:
    - Zhuohang Dang
    - Minnan Luo
    - Chengyou Jia
    - Hangwei Qian
    - Xinyu Zhang
    - Xiaojun Chang
    - Ivor Tsang
  year: 2026
  venue: AAAI 2026
  arxiv: ""
  doi: "10.1609/aaai.v40i25.39207"
  code: ""
  project: ""
classification:
  label: distillation
  task:
    - multi-modal dataset distillation
    - image-text retrieval
  method_family:
    - correspondence coverage
    - ProCo
    - conditional neural fields
    - cross-modal retrieval
  modality:
    - image-text paired data
  datasets:
    - Flickr30K
    - MS-COCO
  metrics:
    - Recall@K (R@1, R@5, R@10)
    - budget-efficacy trade-off
evidence_level: skimmed
raw_sources:
  - raw/sources/2026-03-14-correspondence-coverage-matters-multimodal-dataset-distillation.md
related_pages:
  - wiki/domains/distillation/concepts/dataset-distillation.md
  - wiki/domains/distillation/topics/multimodal-dataset-distillation.md
  - wiki/domains/distillation/methods/proco.md
---

# Correspondence Coverage Matters for Multi-Modal Dataset Distillation

## 引用

Dang, Z., Luo, M., Jia, C., Qian, H., Zhang, X., Chang, X., & Tsang, I. (2026). Correspondence Coverage Matters for Multi-Modal Dataset Distillation. *Proceedings of the AAAI Conference on Artificial Intelligence*, *40*(25), 20693-20701. https://doi.org/10.1609/aaai.v40i25.39207

## 一句话贡献

提出 ProCo——首个系统性地以跨模态 correspondence coverage 为核心目标的多模态数据集蒸馏框架，通过 retrieval-based correspondence consistency metric 聚类 + conditional neural fields 参数化，在 10 倍更小蒸馏预算下超越先前方法 15% 以上。

## 问题设定

多模态数据集蒸馏（Multi-modal Dataset Distillation）将大规模图文配对数据集压缩为紧凑合成数据集，同时保留下游任务（如图文检索）的效果。核心挑战在于捕捉**跨模态 correspondence patterns**——即配对模态间共享的语义对应关系。

现有方法的两个关键缺陷：
1. **单模态策略的局限性**：现有方法依赖 intra-modal similarity（如图像-图像、文本-文本相似性），无法忠实捕捉跨模态（图像-文本）的 correspondence。
2. **过度集中（over-concentration）**：当前多模态 DD 方法倾向于冗余编码相似的 correspondence patterns，限制了蒸馏数据的泛化能力。

## 方法

ProCo（**Pro**mote **Co**rrespondence **Co**verage）包含三个核心创新：

### 1. Correspondence Consistency Metric
- 基于跨模态检索分布（cross-modal retrieval distributions）定义 correspondence consistency metric。
- 使用该 metric 对 correspondence patterns 进行聚类，揭示真实数据集的底层 correspondence 分布。
- 聚类结果为后续初始化和正则化提供代表性 pattern 指导。

### 2. Coverage-Aware Initialization & Regularization
- 从 correspondence clusters 中选择代表性 patterns 初始化蒸馏数据。
- 优化过程中引入正则化项，同时促进 correspondence 的**代表性（representativeness）**和**多样性（diversity）**。
- 这确保蒸馏数据覆盖真实数据中多样的跨模态语义关系，而非冗余重复少量 pattern。

### 3. Conditional Neural Fields 参数化
- 使用 conditional neural fields 高效参数化蒸馏数据，而非直接优化原始像素/文本 token。
- 优势：（1）更精细地捕捉跨模态 pattern；（2）在固定存储预算下允许更多蒸馏样本，进一步提升 correspondence coverage。
- 这是实现 "elastic budget-efficacy trade-off" 的关键技术。

## 实验

### 实验设置
- **数据集**：Flickr30K、MS-COCO（标准多模态 benchmark）。
- **任务**：Image-text retrieval（R@1, R@5, R@10）。
- **评估维度**：不同压缩比下的 budget-efficacy trade-off。
- 与多个单模态和多模态 DD baseline 比较。

### 主要结果
- **核心结果**：ProCo 在使用 **10 倍更小蒸馏预算**的情况下，超越先前方法 **超过 15%**。
- 在不同压缩比下均展现优越且弹性的 budget-efficacy trade-off。
- 在真实世界资源受限部署场景中展现出实用性。

## 结果

- 在多模态数据集蒸馏中，cross-modal correspondence coverage（而非 intra-modal similarity）才是核心压缩目标。
- Retrieval-based correspondence consistency metric 能有效发现并聚类多样的跨模态关系。
- Conditional neural fields 提供了比直接像素/文本优化更高效的蒸馏数据参数化方式。
- Coverage-aware regularization 是防止 over-concentration 和提升泛化能力的关键。

## 限制

- 当前证据基于 AAAI 摘要和公开元数据，尚未获取完整 PDF 正文。
- 方法对 retrieval-based correspondence consistency metric 质量的敏感性分析未知。
- Clustering、regularization 和 conditional neural field parameterization 的相对贡献（ablation）未记录。
- 方法在 image-text 之外的模态组合（如 audio-text、video-text）上的可迁移性未探索。
- 与同期提出的多模态 DD 方法（如 Phased Teacher Models、Asynchronous Matching）的直接比较缺失。

## 可复用 Claims

- 声明：在多模态数据集蒸馏中，cross-modal correspondence coverage 是核心压缩目标，intra-modal similarity 不足以替代。
  证据：ProCo 通过 correspondence-based clustering 和 diversity regularization 在 10x 更小预算下超越先前方法 15%+。
  范围：image-text paired dataset distillation。
  置信度：medium。
  张力：需要与其他多模态 DD 方法的直接比较和 ablation 验证。

- 声明：Retrieval-based correspondence consistency metric 可以有效聚类跨模态 correspondence patterns。
  证据：ProCo 方法设计的核心步骤。
  范围：paired multi-modal distillation。
  置信度：medium。
  张力：metric 对不同 retrieval 模型和距离度量的敏感性未知。

- 声明：Conditional neural fields 是实现 elastic budget-efficacy trade-off 的关键参数化手段。
  证据：相比直接像素/文本优化，允许在固定预算下容纳更多高质量蒸馏样本。
  范围：多模态数据集蒸馏的参数化策略。
  置信度：medium。
  张力：需要与其它参数化方案（如 latent diffusion、hypernetwork）的直接比较。

## 连接

- [Dataset Distillation](../concepts/dataset-distillation.md)：本文把 dataset distillation 扩展到多模态设置。
- [Multi-Modal Dataset Distillation](../topics/multimodal-dataset-distillation.md)：跨模态 correspondence coverage 主题页。
- ProCo 的 conditional neural fields 参数化思路与长尾蒸馏中的 statistical alignment 共享 "不直接优化原始数据" 的设计哲学。

## 开放问题

- ProCo 对 retrieval-based correspondence consistency metric 的质量有多敏感？
- Clustering、regularization、conditional neural field 三个组件的各自贡献（ablation）？
- 方法能否迁移到 image-text 之外的模态组合（audio-text、video-text）？
- 多模态 correspondence coverage 与单模态蒸馏中的 diversity objective 在数学上的精确关系？
- 与同期多模态 DD 方法（Phased Teacher Models、Asynchronous Matching with Dynamic Sampling, ICLR 2026）的系统比较？

## 来源

- [Canonical raw clipping](../../../../raw/sources/2026-03-14-correspondence-coverage-matters-multimodal-dataset-distillation.md)
- [AAAI proceedings page](https://ojs.aaai.org/index.php/AAAI/article/view/39207)
- [DOI](https://doi.org/10.1609/aaai.v40i25.39207)
- 升级说明：2026-05-05 基于 AAAI 摘要、公开元数据、web search 补充的方法/实验细节进行大幅充实。证据等级从 abstract-only 升级为 skimmed。完整 PDF 正文获取后应进一步升级到 full-paper。
