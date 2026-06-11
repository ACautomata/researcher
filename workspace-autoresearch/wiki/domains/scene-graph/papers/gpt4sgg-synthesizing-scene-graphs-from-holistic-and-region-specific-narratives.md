---
title: "GPT4SGG: Synthesizing Scene Graphs from Holistic and Region-specific Narratives"
type: paper
domain: scene-graph
status: active
created: 2026-06-10
updated: 2026-06-10
tags:
  - scene-graph-generation
  - llm
  - gpt4
  - language-supervised-sgg
  - weakly-supervised-sgg
  - neurips-2024
source_pages: []
raw_sources:
  - raw/sources/2023-12-07-GPT4SGG-Synthesizing-Scene-Graphs-from-Holistic-and-Region-specific-Narratives.pdf
  - raw/sources/2023-12-07-GPT4SGG-Synthesizing-Scene-Graphs-from-Holistic-and-Region-specific-Narratives.txt
related_pages: []
paper:
  title: "GPT4SGG: Synthesizing Scene Graphs from Holistic and Region-specific Narratives"
  authors:
    - Zuyao Chen
    - Jinlin Wu
    - Zhen Lei
    - Zhaoxiang Zhang
    - Changwen Chen
  year: 2024
  venue: NeurIPS 2024
  arxiv: "2312.04314"
  doi: null
  code: null
  project: null
classification:
  label: language-supervised-sgg
  task:
    - Scene Graph Generation
    - Language-supervised Scene Graph Generation
    - Weakly-supervised Scene Graph Generation
  method_family:
    - LLM-based Scene Graph Synthesis
    - Divide-and-Conquer Scene Decomposition
  modality:
    - Image
    - Text
  datasets:
    - VG150
    - COCO Captions
    - COCO@GPT
    - VG@GPT
    - VG@Poly
  metrics:
    - Recall@K (R@20/50/100)
    - mean Recall@K (mR@20/50/100)
evidence_level: full-paper
---

## Citation

Zuyao Chen, Jinlin Wu, Zhen Lei, Zhaoxiang Zhang, Changwen Chen. "GPT4SGG: Synthesizing Scene Graphs from Holistic and Region-specific Narratives." NeurIPS 2024. arXiv:2312.04314.

## One-Sentence Contribution

提出分治策略（divide-and-conquer），将复杂场景分解为区域级描述 + 全局描述，利用 LLM（GPT-4）推理关系并合成场景图，有效解决语言监督 SGG 中 grounding 歧义性、caption 稀疏偏置和解析器低效三大难题。

## Problem Setting

**任务：** 语言监督场景图生成（Language-supervised SGG / Weakly-supervised SGG），即在无人工关系标注的情况下，仅凭图像-文本对（image-caption pairs）训练 SGG 模型。

**三大挑战：**
1. **Inaccurate Scene Parser（解析器不准确）**：传统语言解析器（如 scene parser [22]）难以从自然语言描述中提取有意义的 relation triplet，尤其对非规范化描述（如 conjunctions "with", "in" 代替具体关系）。
2. **Ambiguity in Grounding（Grounding 歧义性）**：不分区域的 caption 描述中的 object 无法唯一对应到具体的 visual instance，当同一类别出现多个实例时（如一张图一男一女两条领带），visual-language alignment 存在歧义。
3. **Sparse & Biased Caption（稀疏偏置）**：Caption 数据通常稀疏且偏置，仅反映图像内容的局部观测，覆盖不全。

## Method

### 整体框架（Fig. 3）

GPT4SGG 采用分治策略，将复杂场景分解为简单区域，流程分三阶段：

#### 1. Object Grounding（目标定位）
使用人工标注或目标检测器（如 Grounding DINO）获取图像中每个目标的类别和 bounding box。每个目标用 `[category].[number]: [box]` 唯一编码，解决多实例的 grounding 歧义。

#### 2. Holistic & Region-specific Narratives Generation（场景分解与描述生成）
- **Holistic Narrative**：用 BLIP-2 对全图生成全局描述。
- **Region-specific Narratives**：
  - 将所有检测到的目标两两组对。
  - 过滤 IoU > 0 的 pair（假设有重叠的区域更可能有关系）。
  - 对每个选中的 RoI（Union of the pair）区域用 BLIP-2 生成局部描述。
  - 设定最大 RoI 数量 N（实验中 N=20），控制 prompt token 消耗。

#### 3. Relation Reasoning with LLM（LLM 关系推理）
构造精心设计的 prompt（Tab. 1/6），将 localized objects、holistic narrative 和 region-specific narratives 输入 LLM，要求：
- 逐图像处理
- 推断空间关系与交互
- 保持逻辑一致性（如一条领带只能由一个人穿戴）
- 输出为 JSON 格式的 triplet 列表

LLM 利用 spatial proximity（bounding box overlap）和描述一致性来正确关联对象。实验中使用 GPT-4 Turbo 生成数据，以后可微调 Llama 2 替代。

#### 4. Training SGG Models
将 LLM 生成的 scene graph 映射到封闭集类别后，训练标准 SGG 模型（VS3、OvSGTR）。

#### 5. Instruction Tuning Private LLM
使用 LoRA 微调 Llama 2-13B，用 GPT-4 生成的 instruction-following data 训练，使其具备 SGG 合成能力。

## Experiments

### 数据集

| 数据集 | 来源 | 图像数 | Triplet 数 | 目标类别 | 谓词类别 |
|--------|------|--------|------------|----------|----------|
| VG150 [37] | 人工标注 | 108,777 | ~257k | 150 | 50 |
| COCO@Parser [22] | COCO Captions + 解析器 | ~117k | ~181k | ~44k phrases | ~2.5k |
| COCO@GPT | COCO + GPT4SGG | ~94k | ~394k | 80 | ~4.7k |
| VG@GPT | VG150 + GPT4SGG | ~47k | ~227k | 150 | ~2.4k |
| VG@Poly | VG150 多实例子集 | ~27k | 151k | 150 | — |

### Baselines 和 Training Setup

- **SGG 模型**：
  - VS3 (Swin-L) [41]：开放词汇 SGG，用 GLIP-L 做 grounding
  - OvSGTR (Swin-B) [5]：对象和关系开放词汇 SGG，用 Grounding-DINO 做 grounding
- **训练设置**：遵循各自的官方实现进行训练（具体超参数未报告）
- **评估协议**：SGDET (SGGen)；Recall@K (R@20/50/100) + mean Recall@K (mR@20/50/100)
- **硬件/优化器/学习率/Batch size/Epoch**：未在论文中报告具体训练超参数
- **Captioning 模型**：BLIP-2 / opt-2.7b（主要）；对比 GIT-Base
- **LLM**：GPT-4 Turbo（主要数据生成）；对比 GPT-3.5-turbo、Llama 2-13B
- **N（最大 RoIs）**：20（权衡 recall 与 prompt token）

## Results

### Main Results：VG150 Test Set (Tab. 3)

**GPT4SGG (VG@GPT, ~46k images) 对比 VG Caption (~73k images)：**

| 模型 | 训练数据 | R@20 | R@50 | R@100 | mR@20 | mR@50 | mR@100 |
|------|----------|------|------|-------|-------|-------|--------|
| OvSGTR [5] + GPT4SGG | VG@GPT | **20.12** | **25.03** | **28.84** | **5.68** | **7.14** | **8.22** |
| OvSGTR [5] | VG Caption | 16.36 | 22.14 | 26.20 | 3.80 | 5.24 | 6.25 |
| VS3 [41] + GPT4SGG | VG@GPT | 17.77 | 22.42 | 25.29 | 4.24 | 5.82 | 6.97 |
| VS3 [41] | VG Caption | 11.31 | 16.00 | 19.85 | 2.39 | 3.80 | 4.87 |

**GPT4SGG (COCO@GPT, ~94k images) 对比 COCO Caption + Parser (~117k)：**

| 模型 | R@20 | R@50 | R@100 | mR@20 | mR@50 | mR@100 |
|------|------|------|-------|-------|-------|--------|
| OvSGTR + COCO@GPT | **7.65** | **10.10** | **11.73** | **2.92** | **3.84** | **4.69** |
| OvSGTR + COCO@Parser | 6.85 | 9.33 | 11.47 | 1.28 | 1.79 | 2.18 |
| VS3 + COCO@GPT | 5.07 | 7.40 | 9.50 | 1.30 | 1.93 | 2.42 |
| VS3 + COCO@Parser | 5.26 | 6.70 | 7.91 | 1.97 | 2.38 | 2.70 |

**全监督 baseline（VG150 ~76k images）：**

| 模型 | R@20 | R@50 | R@100 | mR@20 | mR@50 | mR@100 |
|------|------|------|-------|-------|-------|--------|
| OvSGTR ✧ | 27.80 | 36.40 | 42.40 | 5.24 | 7.41 | 8.98 |
| VS3 ✧ | 27.34 | 36.04 | 40.88 | 4.43 | 6.45 | 7.81 |

**关键发现：**
- OvSGTR + VG@GPT（46k 图像，无人工标注）的 mR@100 达到 8.22，接近甚至超过全监督 OvSGTR 的 8.98
- VG@GPT 对 mR@K 提升显著，说明有效缓解了长尾偏置
- COCO 上的增益不如 VG150 显著，因为 COCO 只有 80 类（仅 66 类可匹配 VG150），且 COCO 与 VG150 的数据分布差异大

### Ambiguity Ablation：VG@Poly (Tab. 4)

| 模型 | 监督 | R@20 | R@50 | R@100 | mR@20 | mR@50 | mR@100 |
|------|------|------|------|-------|-------|-------|--------|
| OvSGTR + Annotation | 157k | 27.46 | 35.98 | 41.37 | 5.04 | 6.78 | 7.97 |
| OvSGTR + Parser+GLIP | 386k | 15.63 | 20.58 | 24.20 | 3.33 | 4.48 | 5.38 |
| OvSGTR + GPT4SGG | **151k** | **19.19** | **23.96** | **27.51** | **5.32** | **6.77** | **7.80** |
| VS3 + GPT4SGG | 151k | 17.74 | 22.27 | 25.17 | 4.07 | 5.38 | 6.48 |

**关键发现：**
- GPT4SGG 在 VG@Poly（仅 27k 图像，151k triplets）的 mR@K 表现接近甚至优于全监督（Row 3 vs Row 1）
- 相比之下，Parser+GLIP 基线（386k triplets）的 mR 明显更低，说明 grounding 歧义未解决
- VG@Poly 的节点和边密度更高（27k 图 365k bbox + 151k triplet vs. 46k 图 549k bbox + 225k triplet）

### 与人工标注对比 (Fig. 4)

GPT4SGG 生成的 scene graph 与 VG150 ground truth 的 recall 率：
- w. WordNet synsets 匹配：11.70%
- w. GPT-4 lookup table：12.09%

低 recall 不意味着低质量——T4SGG 可能生成了正确但不同偏好的关系（如 "supporting" vs. "on/above"）。

### LLM 对比（VG150 Val Set，4,808 张图）

| LLM | Recall | Valid Responses |
|-----|--------|-----------------|
| GPT-3.5-turbo | 7.78% | 4,537 / 4,808 |
| Llama 2-13B (无 finetune) | 8.02% | 3,876 / 4,808 |
| **GPT-4 turbo** | **12.09%** | **4,760 / 4,808** |
| Llama 2-13B (instruction-tuned) | 12.06% | — |

微调后的 Llama 2-13B 性能与 GPT-4 相当（12.06% vs 12.09%），提供低成本私有方案。

### Captioning 模型影响 (Fig. 5)

| Captioning 模型 | LLM | Recall |
|-----------------|-----|--------|
| BLIP-2 / opt-2.7b | GPT-3.5 | **7.80%** |
| GIT-Base | GPT-3.5 | 7.27% |

增加 RoI 最大数量可提升 recall，但需权衡 prompt token 消耗。N=20 为选择的平衡点。

### Object Detection 影响

使用 Grounding DINO (Swin-B) 替代人工标注：
- Recall 大幅降至 3.11%（vs. 基线 7.80%）
- 主要原因：检测器在 VG150 上 Average Recall 仅 56.8%（IoU 0.5）

## Limitations

1. **未使用多模态 LLM**：未利用 GPT-4V 直接处理图像输入。
2. **LLM 能力瓶颈**：整体性能受限于所用 LLM 的关系推理能力。
3. **评估不全面**：仅用 recall 一个维度无法全面评价 scene graph 质量，人工标注存在偏置，GPT4SGG 可能生成正确但偏好不同的关系。
4. **检测器依赖性**：自动检测器性能不足时（AR@0.5=56.8%），整体 pipeline 显著退化（3.11% vs 7.80%）。
5. **计算开销**：对每张图需要多次 captioning（BLIP-2）+ LLM 推理，数据生成成本较高。

## Reusable Claims

- **Claim 1**: LLM（GPT-4）利用 spatial proximity（bbox 重叠）和场景描述可解决同一类别多实例的 grounding 歧义问题。
  - Evidence: Tab. 4，GPT4SGG 在 VG@Poly 的 mR 与全监督方法接近甚至持平。
  - Scope: VG@Poly 子集（含多实例图像）。Confidence: high。

- **Claim 2**: GPT4SGG 生成的数据训练 SGG 模型，在 mR@K 上接近甚至超越全监督标注数据。
  - Evidence: OvSGTR + VG@GPT 的 mR@100 = 8.22，与全监督 OvSGTR 的 8.98 接近；Tab. 4 中甚至 151k GPT4SGG triplets 的 mR 超越全监督。
  - Scope: VG150 数据集。Confidence: medium（因全监督仍有小幅优势）。

- **Claim 3**: 传统 scene parser 生成的 caption-derived triplet 存在严重的 bias（偏 conjunctions），而 GPT4SGG 生成的关系类型更丰富（~4.7k vs ~2.5k 谓词类别）。
  - Evidence: COCO@GPT 含 ~4.7k 谓词 vs COCO@Parser 的 ~2.5k；COCO@Parser 偏 conjunction words。
  - Scope: COCO 数据集。Confidence: high。

- **Claim 4**: Instruction-tuning Llama 2-13B 可达到与 GPT-4 相当的 scene graph 合成能力（12.06% vs 12.09% recall）。
  - Evidence: 消融实验 Section 4.4。Confidence: medium（仅在 recall 指标，未比较生成图的多样性与质量）。

## Connections

- **LLM4SGG [12]**：并行工作，同样用 LLM 从 caption 中提取 triplet，但遵循的是传统 pipeline（先解析再 grounding），未解决 grounding 歧义。
- **VS3 [41]**：开放词汇 SGG，GPT4SGG 主要比较的模型之一。
- **OvSGTR [5]**：开放词汇 SGG，GPT4SGG 主要比较的模型之一。
- **Scene Parser [22]**：传统场景图解析器，GPT4SGG 意图替代的组件。
- **BLIP-2 [15]**：用于生成 holistic 和 region-specific narratives 的 captioning 模型。
- **Grounding DINO [21]**：用于 object grounding 的检测器（消融实验）。
- **Llama 2 [33]**：被 instruction-tuned 以替代 GPT-4 进行 scene graph 合成的开源 LLM。
- **LLaVA [20]** / **Mini GPT-4 [43]**：视觉指令微调相关工作。

## Open Questions

1. 如果使用 GPT-4V 直接处理图像（而非通过 BLIP-2 的文本中间表示），是否会进一步提升 scene graph 质量？
2. 能否利用 VG@GPT 或 COCO@GPT 的大规模开源 LLM（如 Llama 3）和更大规模检测数据集（Open Images, LVIS）构建真正的全规模 SGG 预训练数据集？
3. 当前评估仅用 recall，如何设计更好的 scene graph 评估指标以衡量生成图的完整性和准确性？
4. GPT4SGG 对密集场景的细粒度关系（如 Occlusion 场景）效果如何？文中没有专门评估。

## Provenance

- Raw source: `raw/sources/2023-12-07-GPT4SGG-Synthesizing-Scene-Graphs-from-Holistic-and-Region-specific-Narratives.pdf` (verified PDF)
- Extracted text: `raw/sources/2023-12-07-GPT4SGG-Synthesizing-Scene-Graphs-from-Holistic-and-Region-specific-Narratives.txt` (1462 lines, 57345 chars)
- Evidence level: full-paper — 全文 PDF 已提取并精读，覆盖引言、方法、实验、消融、限制和结论全部章节。
