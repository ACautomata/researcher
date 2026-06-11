---
title: "PRISM-0: A Predicate-Rich Scene Graph Generation Framework with Zero-Shot Capabilities"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - zero-shot-sgg
  - open-vocabulary
  - predicate-rich
  - llm-based
  - vlm-based
  - debiasing
  - bottom-up
raw_sources:
  - ../../../sources/scene-graph/2025-PRISM-0-Predicate-Rich-SGG.pdf
  - ../../../sources/scene-graph/2025-PRISM-0-Predicate-Rich-SGG.txt
paper:
  title: "PRISM-0: A Predicate-Rich Scene Graph Generation Framework for Zero-Shot Open-Vocabulary Tasks"
  authors:
    - Abdelrahman Elskhawy
    - Mengze Li
    - Nassir Navab
    - Benjamin Busam
  year: 2025
  venue: arXiv preprint
  arxiv: null
  code: null
classification:
  label: Zero-shot Open-Vocabulary SGG
  task:
    - Scene Graph Generation (Predicate Classification)
    - Sentence-to-Graph Retrieval
  method_family: Bottom-up Zero-shot SGG
  modality: RGB
  datasets:
    - Visual Genome (VG)
    - MS-COCO Caption
  metrics:
    - R@K / mR@K
    - Average Pairwise Distance (APD)
    - DBSCAN Cluster Count
    - Silhouette Score
    - Distance Correlation (dCor)
    - User Study Ratings
evidence_level: full-paper
---

## Citation

Elskhawy, A., Li, M., Navab, N., Busam, B. "PRISM-0: A Predicate-Rich Scene Graph Generation Framework for Zero-Shot Open-Vocabulary Tasks." arXiv preprint, 2025. Technical University of Munich (TUM) & Carl Zeiss Meditec AG.

## One-Sentence Contribution

提出 PRISM-0，一个模块化、零样本开放词汇场景图生成框架，通过 VLM + LLM 的 bottom-up 流水线直接从图像生成谓词丰富、语义无偏的场景图，在 PredCls mR@K 和 S2GR 下游任务上超越弱监督方法，同时与 S2GR 监督方法竞争。

## Problem Setting

- **目标**：直接从输入图像生成开放词汇、语义丰富的场景图，无需任何数据集特定训练，克服 VG 标注偏置（长尾谓词分布、稀疏图）
- **挑战**：
  - VG 前 50 个谓词占据大部分样本，特定谓词严重不足
  - GT 标注常包含琐碎关系（如 "leg of dog"），忽略高层语义（如 "dog chasing frisbee"）
  - 现有零样本方法（ELEGANT）依赖重叠 bbox 假设；弱监督方法（CaCao, PGSG）继承源标注偏置
- **设定**：全零样本（zero-shot），不接触 VG 谓词标签，与弱监督（基于 base-split 训练）对比

## Method

### 架构概览

Bottom-up 零样本 SGG 流水线：**Node Prediction → Geometry Filter → Caption Generation → Triplet Extraction → Relation Validation**

### Node Prediction Module

- 使用 **Florence-2 (large-ft)** 检测物体，输出节点 v_i（bounding box b_i + 标签 o_i）
- 使用 SDPA（scaled dot-product attention），无后处理

### Depth Estimation & Geometry Filter (GF)

- **Depth-Anything-V2 (base)** 估计深度图 D
- GF 计算公式（式 1）：λ₁(x/y) + λ₂|d_i − d_j| < τ
  - x = 2D bbox 中心距离，y = 图像对角长度
  - d_i, d_j = 归一化中位深度
  - λ₁=0.5, λ₂=1, τ=0.45
- 过滤空间上不合理的物体对，保留非重叠交互（如 "person talking to person"）

### Caption Generation Module

- 对保留的物体对生成图像裁剪，红/黄框标注目标物体
- 使用 **LLaVA-OneVision**（batch_size=15, max_tokens=50, beam=1）生成结构化关系描述
- 差异化裁剪引导 VLM 聚焦局部交互，解决全图 captioning 遗漏细节的问题

### Triplet Extraction Module

- 使用 **LLaMA 3.2 (3B)**（batch_size=16, 256-token limit）进行两步提取
  1. CoT 重述模糊描述（"two men engaged in conversation" → "a man is talking to a man"）
  2. 精确提取三元组 [subject, predicate, object]
- DBSCAN 聚类去重：eps_final=0.241, min_samples=5

### Relation Validation Module

- 对每个候选三元组用 VLM 进行 VQA 询问（"Is there a relation [subject, predicate, object]?"）
- 以归一化 "yes" 概率作为置信度，排序保留最可能的三元组
- 保留低置信度 → 全面图；丢弃 → 精确图

## Experiments

### 实验设置

**Predicate Classification (PredCls)**：在 VG 测试集上评估，使用 LLM 将 PRISM-0 开放词汇谓词映射 VG 闭集标签以减少词汇不匹配。对比方法采用弱监督设定（训练于 VG base-predicate split，测试于 base + novel）。

**Relation Diversity**：将谓词嵌入 SentenceBERT 向量空间，计算 APD（平均 pairwise 余弦距离）和 DBSCAN 聚类数。与 DRM（含/不含 DKT）和 PGSG 对比，所有开放词汇预测先映射到闭集再测量。

**Bias Analysis**：使用距离相关（distance correlation, dCor）量化谓词频率与 per-class recall 的依赖关系。dCor=0 表示与频率独立。置换检验计算 p 值。

**Sentence-to-Graph Retrieval (S2GR)**：使用 VG-COCO 重叠的 51k 图像（35k/1k/5k train/val/test），将 MS-COCO caption 解析为文本图查询，检索场景图表示。对比 MTDE（Motif-based TDE）、PGSG、CaCao、LLM4SGG。

**User Study**：75 参与者 × 40 随机图像，五点评估：Overall Situation, Object Names, Scene Completeness, Relation Correctness, Capture of Main Relations。配对 t 检验显著性。

**Ablation**：S2GR Gallery 1K 设置下消融 Geometric Filter 和 LLM 大小（3B→1B）。

## Results

### Predicate Classification on VG（Table 1）

| Method | Training | mR@50 | mR@100 | R@50 | R@100 |
|--------|:--------:|:-----:|:------:|:----:|:-----:|
| CaCao | w (weak) | 10.3 | 12.6 | - | - |
| SVRP | w | 8.3 | 10.8 | 33.5 | 35.9 |
| PGSG | w | 10.8 | 13.9 | 26.9 | 33.9 |
| **PRISM-0** | zs (zero-shot) | **12.04** | **14.98** | 22.58 | 25.11 |

> PRISM-0 在 mR@50/100 上超越所有弱监督 baseline，尽管 R@50/100 稍低——原因是 PRISM-0 生成更具体的尾部谓词（如 "person-riding-bike" vs. VG GT "person-on-bike"），在闭集评估中产生假负例。

### Relation Diversity（Table 2）

| Method | APD | DBSCAN Clusters | Noise (%) | Silhouette |
|--------|:---:|:---------------:|:---------:|:----------:|
| DRM w/o DKT | 0.76 | 52 | 23.3 | 0.038 |
| DRM | 0.78 | 75 | 30.6 | 0.231 |
| PGSG | 0.80 | 54 | 16.2 | 0.128 |
| **PRISM-0** | 0.77 | 62 | 29.8 | 0.225 |

> 尽管零样本且无谓词训练或显式去偏，PRISM-0 的语义多样性匹配甚至超越去偏方法 DRM，且显著优于 PGSG（DBSCAN 簇数 62 vs 54，SG 质量 0.225 vs 0.128）。

### Dataset Bias Analysis（Table 3）

| Method | dCor | p-value |
|--------|:---:|:-------:|
| DRM | 0.65 | 0.001 |
| PGSG | 0.47 | 0.007 |
| **PRISM-0** | **0.18** | **0.95** |

> DRM 和 PGSG 均表现出强/中等偏置依赖性（p<0.01），而 PRISM-0 本质上与 VG 谓词频率独立（dCor=0.18, p=0.95），说明零样本方法可天然避免频率偏置。

### Sentence-to-Graph Retrieval（Table 4）

| Model | ZS | Gallery 1K R@20 | Gallery 1K R@100 | Gallery 1K Med | Gallery 5K R@20 | Gallery 5K R@100 | Gallery 5K Med |
|-------|:--:|:---------------:|:----------------:|:--------------:|:---------------:|:----------------:|:--------------:|
| MTDE | ✗ | 17.0 | 53.6 | 91 | 5.2 | 18.9 | 425 |
| PGSG | ✗ | 48.4 | 75.3 | 97 | 27.1 | 54.3 | 313 |
| CaCao | ✗ | 52.0 | 77.3 | 85 | 33.4 | 60.9 | 322 |
| LLM4SGG | ✗ | 56.9 | 82.9 | 64 | 34.0 | 64.8 | 211 |
| **PRISM-0** | ✓ | **56.9** | 80.2 | 71 | 32.6 | 64.0 | 223 |

> PRISM-0 在完全零样本设置下超越所有弱监督方法（MTDE, PGSG, CaCao），与 LLM4SGG 在 R@20（1K）持平。LLM4SGG 利用 MS-COCO GT 字幕训练监督 SGG 模型，因此其输出与 GT caption 解析的查询更契合。

### Ablation（Table 5, S2GR Gallery 1K）

| Model Change | R@20 | R@100 | Med |
|-------------|:----:|:-----:|:---:|
| Ours (Full Pipeline) | **56.9** | **80.2** | **71** |
| LLM (3B → 1B) | 50.8 | 72.4 | 126 |
| w/o Geometric Filter | 29.8 | 61.1 | 239 |

> Geometric Filter 是最关键组件，移除后 R@20 从 56.9 降至 29.8（-47.6%），Med rank 从 71 飙升至 239。将 LLM 从 3B 缩小到 1B 导致约 10% R@20 下降。

### Inference Time（Table 6）

| Variant | Avg. time (sec/image) |
|---------|:--------------------:|
| w/o GF | 90.0 |
| w/ GF | 67.5 |

> Geometric Filter 减少约 25% 推理时间。

### User Study（Fig. 4）

PRISM-0 在全部五项指标上均一致优于 VG 标注（p < 0.05），特别在场景完整性（Scene Completeness）、整体情境（Overall Situation）和主关系捕获（Capture of Main Relations）上差异最大。

## Limitations

1. **依赖下游模块精度**：流水线整体效果高度依赖节点预测模块（Florence-2）的检测准确率，物体检测失败时会级联影响整个 SGG
2. **计算开销大**：bottom-up 内省所有物体对 + 多模型调用（Florence-2, Depth-Anything-V2, LLaVA-OneVision, LLaMA 3.2, VQA VLM）导致每图平均 67.5s（有 GF），不适合实时或资源受限场景
3. **复杂交互仍存难度**：即使有 GF 和 Validation Module，复杂或模糊的物体关系仍然是挑战
4. **闭集评估不公平**：现有 PredCls 基准使用 VG 偏置标注作为 GT，PRISM-0 生成的更具体、更丰富的谓词被视为假负例，导致 Recall 被系统性低估
5. **无统一零样本 SGG 评估协议**：不同方法（本文 vs CaCao/PGSG vs CAPSGG）的训练暴露和评估设置不一致，难以意义明确比较

## Reusable Claims

- **零样本 SGG 可达竞争性结果**：通过 VLM + LLM bottom-up pipeline，完全不经训练即可在 PredCls mR@K 上超越弱监督方法，在 S2GR 上超越多种监督方法
- **底层方法天然抗偏置**：零样本 pipeline 不接触任何标注数据，dCor=0.18（p=0.95）证明其本质上不受 VG 长尾分布影响，超越复杂的去偏技术
- **Geometry Filter 是关键**：结合 2D 距离 + 深度差异的空间过滤不仅提升效率（-25% 推理时间），更对 S2GR 下游任务有决定性贡献（移除后 R@20 从 56.9 降至 29.8）
- **非重叠 bbox 交互不可忽略**：传统方法只考虑重叠 bbox 对，PRISM-0 的 GF 在过滤不可信对的同时保留了重要的非重叠交互（如 "person talking to person"）
- **两步 CoT 提取优于直接提取**：先 paraphrase 再提取三元组的策略提升关系抽取精度，尤其在涉及复杂或隐含关系时
- **VQA 验证优于 CLIP 评分**：对比一般图像-文本对齐度量（如 CLIP-Score），直接 VQA 查询对细微关系有更好辨别力

## Connections

- 直接对比基线：**CaCao**, **SVRP**, **PGSG**（弱监督 PredCls），**MTDE**, **PGSG**, **CaCao**, **LLM4SGG**（S2GR），**DRM**（去偏基线）
- 零样本 SGG 方向相关：**ELEGANT**, **ConceptGraphs**（零样本/3D 零样本，均依赖重叠 bbox），**CAPSGG**（胶囊零样本，但需要训练 + 闭集词汇）
- 弱监督 SGG：**CaCao**, **LLM4SGG**, **PGSG**（依赖 caption 伪标签，继承标注偏置）
- 去偏 SGG：**DRM**（双粒度知识迁移去偏，S2GR 中有对比）
- 使用的 foundation model: **Florence-2**, **Depth-Anything-V2**, **LLaVA-OneVision**, **LLaMA 3.2**, **SentenceBERT**
- 下游任务连接：S2GR（展示了零样本 SGG 在下游检索任务中的实用性）
- 同类别方法（VLM+LLM for SGG）：**SDSGG**（NeurIPS 2024）也用 LLM，但为弱监督 + caption 依赖，而 PRISM-0 是零样本 + bottom-up
- 本 wiki 对比方法：**OwSGG** 也是 zero-shot SGG 但使用端到端 VLM 推理而非模块化流水线

## Open Questions

- PRISM-0 能否扩展到实时或近实时场景（当前 67.5s/图）？知识蒸馏或缓存机制能否降低计算开销？
- 如何建立统一、公平的零样本 SGG 评估协议，消除开放词汇 → 闭集映射的信息损失？
- 使用更强的 VLM（如 GPT-4o）或 LLM（如 LLaMA 3.1 70B）是否会进一步提升 S2GR 性能？
- Geometric Filter 的 λ₁, λ₂, τ 参数对场景类型（室内 vs 室外、密集 vs 稀疏）的敏感性如何？是否需要场景自适应调参？
- 如何将 PRISM-0 用于 3D SGG 或视频 SGG（VSGG）的零样本推理？
- 端到端 VLM（如 OwSGG 的 LLaVA-Next / Qwen2-VL）与模块化流水线（如 PRISM-0）在零样本 SGG 上孰优孰劣？

## Provenance

- Source file: `raw/sources/2025-PRISM-0-Predicate-Rich-SGG.pdf`
- Extracted text: `raw/sources/2025-PRISM-0-Predicate-Rich-SGG.txt`
- Evidence level: full-paper（全文精读，所有表格数据和实验结果均已捕获）
- Analyzed by: autoresearch subagent, 2026-06-09
