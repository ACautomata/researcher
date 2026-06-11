---
title: "Grounding Everything: Emerging Localization Properties in Vision-Language Transformers"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - vlm
  - grounding
  - open-vocabulary
  - zero-shot
  - self-self-attention
  - semantic-segmentation
paper:
  title: "Grounding Everything: Emerging Localization Properties in Vision-Language Transformers"
  authors:
    - Walid Bousselham
    - Felix Petersen
    - Vittorio Ferrari
    - Hilde Kuehne
  year: 2025
  venue: CVPR 2025
  arxiv: "2312.00878"
  code: "https://github.com/WalBouss/GEM"
  project: "https://huggingface.co/spaces/WalidBouss/GEM"
classification:
  label: "zero-shot open-vocabulary object localization"
  task:
    - zero-shot semantic segmentation
    - zero-shot point prediction
  method_family: training-free vision-language grounding
  modality: image-text
  datasets:
    - PascalVOC
    - PascalContext
    - ADE20K
    - OpenImagesV7
  metrics:
    - mIoU
    - p-mIoU
evidence_level: full-paper
raw_sources:
  - ../../../sources/scene-graph/2025-CVPR-Grounding-Everything-Emerging-Localization-Properties-VLMs.pdf
  - ../../../sources/scene-graph/2025-CVPR-Grounding-Everything-Emerging-Localization-Properties-VLMs.txt
---

# Grounding Everything: Emerging Localization Properties in Vision-Language Transformers

## Citation

Walid Bousselham, Felix Petersen, Vittorio Ferrari, Hilde Kuehne. "Grounding Everything: Emerging Localization Properties in Vision-Language Transformers." CVPR 2025. arXiv:2312.00878.

## One-Sentence Contribution

文章提出 Grounding Everything Module (GEM)，通过 generalized self-self attention 在**不进行任何微调**的条件下，从预训练 VLM（CLIP 等）中提取零样本开放词汇定位能力，在语义分割和点预测上超越所有无训练方法，部分达到 SOTA。

## Problem Setting

- **背景**：CLIP 等 VLM 在分类、检索等全局任务上表现优异，但在零样本定位（对象级/像素级）上能力不足——当用文本 prompt 查询时，image patches 与 text embedding 之间呈现**反向**的 vision-language 关系（前景 patch 距离更远）。
- **已有解决方案**：MaskCLIP 去掉最后一层 MLP 解决反置问题；CLIPSurgery 通过 value-value attention 累积定位信号。但 CLIPSurgery 的工作原理未被充分解释。
- **GEM 目标**：在无标注、无微调的约束下，利用预训练 VLM 的**固有定位能力**实现开放词汇对象定位。

## Method

### 核心发现
值-值注意力（value-value attention）可以广义化为**自-自注意力（self-self attention）**——即 query-query、key-key、value-value 任意一种都能产生相似的聚类效果。相比标准 q-k attention，self-self attention 会增加相似 token 间的相似度，从而形成对应于同一物体的 token 组。

### GEM 架构

1. **Generalized Self-Self Attention Block**：对每个 self-attention 头，分别对 q、k、v 计算自注意力（q-q, k-k, v-v），对三者结果做 **ensemble**，形成完整的自-自注意力块。
2. **L2 Normalization**：对每个 projected token 做 L2 归一化，防止高范数 token 过度影响注意力。
3. **Adaptive Temperature**：引入自适应温度 $\tau = \frac{N \cdot \sqrt{d}}{\sum_i \|x_i\|_2}$，无需超参数调节即能在不同数据集上取得良好表现。
4. **Iteration**：对 self-self attention 重复多次（默认 2 次）进一步增强聚类效果。
5. **Skip Connection**：保留原始 transformer 层的残差连接。
6. **Alternative Pathway**：GEM 块作为**并行路径**与原始 ViT transformer 块交替执行，最后输出 patch tokens 与 text [CLS] embedding 点积得到定位。

### 简化的直觉

> Self-self attention = 聚类。每个 token 与自己的同构投影做注意力，使属于同一对象的 token 彼此靠拢，同时维持与语言空间的对齐。

## Experiments

### 实验设置

- **模型 backbone**：使用预训练权重的 CLIP、OpenCLIP、BLIP、MetaCLIP（ViT-B/16, ViT-B/32, ViT-L/14）
- **微调**：完全不进行微调（training-free）
- **超参数**：L2 normalization + adaptive temperature + 2 次迭代，所有数据集和 backbone 使用相同配置

### 数据集

1. **Zero-shot Semantic Segmentation**：PascalVOC（20 类）、PascalContext（59 类）、ADE20K（150 类）
2. **Zero-shot Point Prediction**：OpenImagesV7（约 6000 类）

### 评估指标

- **mIoU**：mean Intersection over Union（语义分割）
- **p-mIoU**：point-wise mIoU（点预测）
- 推理速度（fps）

### Baseline 方法

- **无训练方法**：CLIP（原始）、MaskCLIP、MaskCLIP(2)、CLIPSurgery
- **有微调方法**：SPNet、ZS3Net、OpenSeg、OVSeg、SegCLIP、GroupViT、PACL、ViL-Seg、OVSegmentor 等
- **使用标注方法**：GroundingSAM
- **GEM 变体**：GEM-CLIP、GEM-MetaCLIP、GEM-SAM-CLIP、GEM-SAM-MetaCLIP

## Results

### Table 2: Zero-shot Semantic Segmentation (mIoU)

| 方法 | Backbone | Pre-train | PascalVOC | PascalContext | ADE20K |
|------|----------|-----------|-----------|---------------|--------|
| CLIP (original) | ViT-B/16 | WIT-400M | 10.4 | 7.7 | 1.7 |
| MaskCLIP* | ViT-B/16 | WIT-400M | 28.6 | 23.8 | 10.2 |
| CLIP Surgery* | ViT-B/16 | WIT-400M | 41.2 | 30.5 | 12.9 |
| **GEM (CLIP)** | **ViT-B/16** | **WIT-400M** | **46.2** | **32.6** | **15.7** |
| **GEM (MetaCLIP)** | **ViT-B/16** | **metaclip-400M** | **46.8** | **34.5** | **17.1** |

- GEM-CLIP 在 PascalVOC 上比 CLIP Surgery 提升 **+5.0 mIoU**（46.2 vs 41.2）
- GEM-MetaCLIP 在 ADE20K 上比 GEM-CLIP 进一步提升（17.1 vs 15.7）
- 训练无关方法在更复杂的 PascalContext 和 ADE20K 上能超越部分有微调方法（除 PACL 外）

### Table 3: Zero-shot Point Prediction on OpenImagesV7 (p-mIoU)

| 方法 | Loc. annotation | Loc. FT | p-mIoU | fps |
|------|----------------|---------|--------|-----|
| CLIP | ✗ | ✗ | 27.6 | 42.10 |
| MaskCLIP* | ✗ | ✗ | 42.0 | 42.43 |
| CLIPSurgery* | ✗ | ✗ | 47.8 | 38.47 |
| **GEM-CLIP** | **✗** | **✗** | **50.9** | **37.24** |
| **GEM-MetaCLIP** | **✗** | **✗** | **51.9** | **37.24** |
| GroundingSAM | ✓ | ✓ | 53.3 | 0.59 |
| **GEM-SAM-CLIP** | **✓** | **✗** | **53.4** | **0.45** |
| **GEM-SAM-MetaCLIP** | **✓** | **✗** | **55.2** | **0.45** |

- GEM-CLIP 在纯训练无关设置下比 CLIPSurgery 提升 **+3.1 p-mIoU**（50.9 vs 47.8）
- GEM-SAM-MetaCLIP（利用 SAM mask，不微调）达到 **55.2**，超过使用标注的 GroundingSAM（53.3）
- 训练无关方法整体远超有微调方法（OVSeg 22.5, SegCLIP 32.1, GroupViT 36.5）

### Table 4: 迭代次数影响

| #Iterations | PascalVOC | PascalContext |
|-------------|-----------|---------------|
| 0 (= CLIP Surgery) | 41.2 | 30.5 |
| 1 | 45.1 | 31.5 |
| 2 | 45.5 | 32.6 |
| 3 | **46.2** | 31.9 |
| 4 | 45.6 | 31.1 |

- 更多迭代对类别较少的 PascalVOC 有提升（最优 3 次），对类别较多的 PascalContext 更少迭代更好（最优 2 次）

### Table 5: 不同 Backbone 和 Variant 的 GEM 性能

| Backbone | Model | VOC | Context | V7 |
|----------|-------|-----|---------|----|
| ViT-B/16 | CLIP | 46.2 | 32.6 | 50.9 |
| ViT-B/16 | OpenCLIP | 43.1 | 31.7 | 49.9 |
| ViT-B/16 | BLIP | 42.8 | 23.5 | 45.2 |
| ViT-B/16 | MetaCLIP | 46.8 | 34.5 | 51.9 |
| ViT-B/32 | CLIP | 40.5 | 27.0 | 46.6 |
| ViT-L/14 | CLIP | 44.6 | 28.6 | 46.3 |
| ViT-L/14 | MetaCLIP | 45.7 | 26.9 | 40.9 |

- GEM 在不同 backbone 和预训练变体上表现一致，MetaCLIP 整体最佳
- ViT-B/16 优于 ViT-B/32（更高分辨率）；ViT-L/14 没有明显优势

### 主要发现总结

1. **Self-self attention = 聚类**：这是 CLIPSurgery 成功的内在原因，GEM 将其系统化为 q-q、k-k、v-v 的全自注意力
2. **L2 normalization + adaptive temperature**：消除了跨数据集/backbone 的手动调参需求
3. **迭代强化聚类**：更多迭代适用于少类场景，少迭代适用于多类场景
4. **训练无关方法在大词汇量场景占优**：OpenImagesV7（6000 类）上训练无关方法全面超出有微调方法
5. **GEM 具有通用性**：在 CLIP、OpenCLIP、BLIP、MetaCLIP 上均可工作

## Limitations

1. **迭代次数需要根据类别数调节**：少类场景需要更多迭代，多类场景需要更少迭代，最优值不统一
2. **相比有微调方法（如 PACL）仍有差距**：在更细粒度分割上，GEM 虽超越多数有微调方法，但未全面超越 PACL
3. **依赖预训练 VLM 质量**：性能上限受 backbone 的预训练数据量和质量限制
4. **推理速度略低于 CLIPSurgery**：37.24 fps vs 38.47 fps（GEM-CLIP vs CLIPSurgery），略慢但仍远快于有微调方法
5. **本质仍为粗略定位**：方法输出的是 patch-level similarity，不是精确的 object mask

## Reusable Claims

> **Claim**: 预训练 VLM 的 self-self attention 具有内在聚类特性，可用于无训练零样本定位。
> **Evidence**: GEM 在 PascalVOC 上达 46.2 mIoU（+5.0 vs CLIP Surgery），OpenImagesV7 上达 50.9 p-mIoU。
> **Scope**: 使用 CLIP-family 预训练 VLM，编码器为 ViT，评估为语义分割 / 点预测。
> **Confidence**: high

> **Claim**: 在大词汇量（数千类）开放世界分割中，训练无关方法优于有微调方法。
> **Evidence**: OpenImagesV7 上 GEM-CLIP 50.9 p-mIoU vs OVSeg 22.5、SegCLIP 32.1、GroupViT 36.5。
> **Confidence**: high

> **Claim**: L2 normalization + adaptive temperature 消除了 self-self attention 在跨数据集/backbone 上的手动调参需求。
> **Evidence**: GEM 在 3 个分割数据集 + 多个 backbone 上使用相同配置，结果一致领先。
> **Confidence**: high

## Connections

- **CLIPSurgery [Li et al., 2023]**：GEM 的前身工作，CLIPSurgery 的 value-value attention 被 GEM 推广为全局的 self-self attention
- **MaskCLIP [Zhou et al., 2022]**：最早揭示 CLIP 的 V-L 反置问题并移除最后一层 MLP
- **PACL [Mukhoti et al., 2023]**：使用 patch 级别 loss 微调 CLIP decoder 的有监督方法，在 PascalContext 和 ADE20K 上仍有优势
- **GroundingSAM**：使用 SAM 的 mask proposal + GEM 的开放词汇分类，GEM-SAM 达到最高性能 55.2 p-mIoU
- **SGG 关联**：GEM 的定位能力可直接用于 SGG 中的 visual grounding 和 predicate region proposal，无需为每个 predicate 类别微调定位模块

## Open Questions

1. GEM 能否推广到 DINO、DINOv2 等自监督 ViT backbone？
2. 如何自适应地确定最优迭代次数（可学习的终止条件）？
3. self-self attention 的聚类效果是否在更深的 transformer（ViT-L/14, ViT-H）上保持？
4. GEM 能否作为通用 grounding 模块集成到端到端 SGG 中，替代 region proposal + predicate classification 的两阶段范式？
5. adaptive temperature 的理论解释是什么？其与 softmax 熵的关联？

## Provenance

- 论文正文来自 arXiv:2312.00878v3 (2023-12-14)
- 表中数据提取自 Section 6 (Experiments)，Table 2、3、4、5
- 作者提供代码和 HuggingFace demo
- 入库时间: 2026-06-09
