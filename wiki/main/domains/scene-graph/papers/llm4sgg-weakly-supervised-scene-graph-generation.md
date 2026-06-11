---
title: "LLM4SGG: Large Language Models for Weakly Supervised Scene Graph Generation"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - scene-graph-generation
  - weakly-supervised-learning
  - large-language-models
  - chain-of-thought
  - few-shot-learning
  - triplet-extraction
  - semantic-parsing
  - CVPR-2024
raw_sources:
  - ../../../sources/scene-graph/2024-CVPR-LLM4SGG-Large-Language-Models-for-Weakly-Supervised-SGG.pdf
  - ../../../sources/scene-graph/2024-CVPR-LLM4SGG-Large-Language-Models-for-Weakly-Supervised-SGG.txt
related_pages:
  - vs3.md
  - language-supervised-open-vocabulary-scene-graph-vs3.md
  - ssc-sgg-semi-supervised-clustering-weakly-supervised-scene-graph-generation.md
evidence_level: full-paper
paper:
  title: "LLM4SGG: Large Language Models for Weakly Supervised Scene Graph Generation"
  authors:
    - Kibum Kim
    - Kanghoon Yoon
    - Jaehyeong Jeon
    - Yeonjun In
    - Jinyoung Moon
    - Donghyun Kim
    - Chanyoung Park
  year: 2024
  venue: "Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2024"
  arxiv: null
  doi: null
  code: "https://github.com/rlqja1107/torch-LLM4SGG"
  project: null
classification:
  label: "LLM4SGG — Weakly Supervised SGG via LLM-based Triplet Formation"
  task:
    - Scene Graph Generation (SGG)
    - Scene Graph Detection (SGDet)
    - Weakly-Supervised Scene Graph Generation (WSSGG)
  method_family:
    - Large Language Model prompting
    - Chain-of-Thought reasoning
    - In-context few-shot learning
    - Caption paraphrasing
    - LLM-based class alignment
---

# LLM4SGG: Large Language Models for Weakly Supervised Scene Graph Generation

**Kibum Kim, Kanghoon Yoon, Jaehyeong Jeon, Yeonjun In, Jinyoung Moon, Donghyun Kim, Chanyoung Park** — KAIST, ETRI, Korea University

> CVPR 2024. Code: [https://github.com/rlqja1107/torch-LLM4SGG](https://github.com/rlqja1107/torch-LLM4SGG)

## 核心贡献

提出 LLM4SGG，首次将大语言模型（LLM，具体为 ChatGPT）引入弱监督场景图生成（WSSGG）任务。核心洞察是现有 WSSGG 方法忽略了 **triplet 形成过程**（caption 解析和类别对齐），存在两个关键问题：

1. **Semantic Over-simplification（语义过度简化）**：基于规则的场景图解析器（如 Scene Parser）将细粒度谓词（如 *lying on*）错误地转换为粗粒度谓词（如 *on*），导致谓词分布严重长尾。50 个谓词中 12 个频率为 0。
2. **Low-Density Scene Graph（低密度场景图）**：基于 WordNet 的类别对齐导致大量 triplet 被丢弃。COCO Caption 经 Parser+KB 处理后仅剩 154K triplets/64K 图像（2.4 个/图），远低于 VG 全监督的 7.1 个/图。

### 方法

将 triplet 形成过程分解为两个 Chain-of-Thought 链：

- **Chain-1（替代 Step 2）**：LLM 从原始 caption 和 LLM 生成的 paraphrase caption 中提取 triplet，paraphrase 增加语义多样性 → triplet 数从 154K 提升至 243K。
- **Chain-2（替代 Step 3）**：LLM 将 triplet 中的 entity/predicate 对齐到目标数据预定义词汇表（Visual Genome 的 150 entities / 50 predicates）→ triplet 数从 243K 进一步提升至 327K。
- **总计**：LLM4SGG 从 COCO Caption 64K 图像中生成 **344K triplets**（5.4 个/图），对比 Parser+KB 的 154K（2.4 个/图）。

各组件通过 in-context few-shot learning 引导，无需 fine-tune LLM。

### 关键特点

- 与 grounding 方法（SGNLS, VS3）**即插即用**，无需修改原算法
- **一次性预处理**，并非每次训练都需要调用 LLM
- **数据高效**：仅用 7.8% 训练图像即可超越基线

## Experiments

### 数据集

- **训练**：COCO Caption（64K）、Conceptual Captions（145K）、Visual Genome Caption（57K）
- **评测**：Visual Genome（150 entities, 50 predicates, SGDet task）、GQA（200 entities, 100 predicates）
- **评价指标**：R@K, mR@K, F@K（R@K 与 mR@K 的调和平均）

### 主要结果（Table 2 — Visual Genome, SGDet）

| 方法 | 训练数据 | R@50 | R@100 | mR@50 | mR@100 | F@50 | F@100 |
|------|---------|------|-------|-------|--------|------|-------|
| LSWS (CVPR'21) | COCO Caption | 3.29 | 3.69 | 3.27 | 3.66 | 3.28 | 3.67 |
| SGNLS (ICCV'21) | COCO Caption | 3.80 | 4.46 | 2.51 | 2.78 | 3.02 | 3.43 |
| **SGNLS + LLM4SGG** | COCO Caption | **5.09** | **5.97** | **4.08** | **4.49** | **4.53** | **5.13** |
| VS3 (CVPR'23) | COCO Caption | 6.60 | 8.01 | 2.88 | 3.25 | 4.01 | 4.62 |
| **VS3 + LLM4SGG** | COCO Caption | **8.91** | **10.43** | **7.11** | **8.18** | **7.91** | **9.17** |
| VS3 (CVPR'23) | CC Caption | 6.69 | 8.20 | 1.73 | 2.04 | 2.75 | 3.27 |
| **VS3 + LLM4SGG** | CC Caption | **9.47** | **10.69** | **5.40** | **6.09** | **6.88** | **7.76** |
| VS3 (CVPR'23) | VG Caption | 14.54 | 18.48 | 2.80 | 3.79 | 4.70 | 6.29 |
| **VS3 + LLM4SGG** | VG Caption | **18.40** | **22.28** | **6.26** | **7.60** | **9.34** | **11.33** |
| VS3 + Reweighting | COCO Caption | 4.25 | 5.04 | 5.17 | 5.99 | 4.67 | 5.47 |
| **VS3 + Rwt + LLM4SGG** | COCO Caption | **5.10** | **6.34** | **8.42** | **9.90** | **6.35** | **7.73** |

> **关键观察**：LLM4SGG 对 mR@K 提升最为显著（VS3 + LLM4SGG 在 mR@100 从 3.25 → 8.18，提升 +4.93），验证了在缓解长尾问题上的有效性。VS3+Rwt+LLM4SGG 可达 mR@100 = 9.90，说明 LLM 生成细粒度谓词对重加权策略有协同增益。

### GQA 结果（Table 4）

| 方法 | R@50 | R@100 | mR@50 | mR@100 | F@50 | F@100 |
|------|------|-------|-------|--------|------|-------|
| VS3 | 5.90 | 6.97 | 1.60 | 1.81 | 2.52 | 2.87 |
| **VS3 + LLM4SGG** | **8.88** | **10.38** | **5.33** | **6.51** | **6.66** | **8.00** |

> GQA 数据集包含 100 个谓词（VG 的 2 倍），传统 WSSGG 方法有 44/100 个谓词频率为 0。LLM4SGG 在 mR@50 从 1.60 → 5.33（+3.73×），展示了对复杂谓词场景的强大效果。

### 消融实验（Table 3，VS3，VG）

| 行 | Paraphrased Caption | LLM Parsing | LLM Alignment | # Triplet | R@50/100 | mR@50/100 | F@50/100 |
|----|-------|------|------|----------|----------|-----------|----------|
| (a) | — | — | — | 154K | 6.60 / 8.01 | 2.88 / 3.25 | 4.01 / 4.62 |
| (b) | ✓ | — | — | 243K | 9.46 / 11.22 | 3.43 / 3.92 | 5.03 / 5.81 |
| (c) | ✓ | ✓ | — | 256K | 8.42 / 9.85 | 5.99 / 6.95 | 7.00 / 8.15 |
| (d) | ✓ | — | ✓ | 327K | 11.76 / 13.38 | 3.50 / 4.05 | 5.39 / 6.22 |
| (e) | ✓ | ✓ | ✓ | 344K | 8.91 / 10.43 | 7.11 / 8.18 | 7.91 / 9.17 |

> **消融关键发现**：LLM-based alignment（行d）对提升 R@K 最关键（11.76/13.38），LLM-based parsing（行c）对提升 mR@K 最关键（5.99/6.95）。两者结合（行e）在 F@K 上最优，显示语义简化缓解和密度提升的互补性。

### 数据高效性分析（Figure 4）

- 仅用 **5K 图像（7.8%）** 训练 VS3+LLM4SGG 即可超越用 64K 训练的 VS3
- 证明了 LLM 生成的高质量 triplet 在大幅减少训练数据时仍有效

## 方法细节

### 训练流程

1. **Step 1**：准备图像及其 caption
2. **Step 2-1**（LLM Chain-1）：LLM 从原始 caption 提取 triplet
3. **Step 2-2**（LLM Chain-1）：LLM 先 paraphrase caption，再从 paraphrase 提取 triplet
4. **Step 3**（LLM Chain-2）：LLM 将 entity/predicate 对齐到目标数据词汇表；无法对齐的标记为 None 并丢弃
5. **Step 4**：用 SGNLS 或 VS3 将未定位 triplet grounding 到图像区域
6. 用定位后的 pseudo-label triplet 训练全监督 SGG 模型

### Prompt 设计

- Task description + In-context few-shot examples + Actual question
- Chain-1 示例如：caption "Four clocks sitting on a floor next to a woman's feet" → paraphrase "Four clocks placed on the floor beside a woman's feet" → triplets `<clocks, placed on, floor>`, `<clocks, beside, feet>`
- Chain-2 对齐示例：entity 对齐用层次化关系（pigeon → bird），predicate 对齐用时态/位置关系（lies on → lying on, next to → near）

### 重要技术点

- 使用 ChatGPT（GPT-3.5 级别）作为 LLM backbone
- 使用 COCO Caption 中的实例作为 in-context examples
- 未对 prompt design 进行系统搜索（作为未来工作）
- 由于 LLM 是黑盒商业模型，依赖其存在潜在的局限性和成本问题

## 与相关工作的关系

- **VS3 (CVPR'23)**：LLM4SGG 直接应用于 VS3 的 grounding 流程，VS3 成功 grounding 全部 344K triplets（SGNLS 仅 grounding 71%），两者协同性最佳
- **SGNLS (ICCV'21)**：同样可直接增强，但 grounding 率较低（71%）
- **SSC-SGG (AAAI'25)**：同样是弱监督 SGG，但 SSC-SGG 采用半监督聚类范式，LLM4SGG 则聚焦 triplet 形成阶段
- **TSG Bench (2025)**：后续工作系统评测 LLM 理解/生成场景图的能力，LLM4SGG 是开创性实践

## 关键结论

1. WSSGG 中 triplet 形成阶段（Step 2 和 Step 3）的改进比 grounding 阶段（Step 4）的改进更重要
2. LLM 的语义理解和推理能力可以同时缓解语义过度简化和低密度场景图问题
3. LLM4SGG 生成的 triplet 数量从 154K→344K（+123%），且质量更高（细粒度谓词更丰富）
4. 对 mR@K 的提升远大于对 R@K 的提升，说明长尾问题得到实质性缓解
5. 数据高效性好，7.8% 数据即可超越 100% 数据训练的基线

## 局限性

- 依赖商业黑盒 LLM（ChatGPT），存在成本和访问限制
- 替换为更小的开源语言模型（如 LLaMA）的效果需要进一步验证（Appendix F 有初步讨论）
- prompt design 未做系统搜索
- LLM 的一次性预处理成本：对所有 caption 调用 LLM 可能需要较多 API 调用
