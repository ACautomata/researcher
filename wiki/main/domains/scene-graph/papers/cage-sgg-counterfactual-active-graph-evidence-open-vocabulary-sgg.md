---
title: "CAGE-SGG: Counterfactual Active Graph Evidence for Open-Vocabulary Scene Graph Generation"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - scene-graph-generation
  - open-vocabulary-sgg
  - counterfactual
  - evidence-grounding
  - relation-verification
  - counterfactual-verification
  - visual-grounding
  - arxiv-2026
  - panoptic-sgg
raw_sources:
  - ../../../sources/scene-graph/2026-arXiv-CAGE-SGG-Counterfactual-Active-Graph-Evidence-for-Open-Vocabulary-SGG.pdf
  - ../../../sources/scene-graph/2026-arXiv-CAGE-SGG-Counterfactual-Active-Graph-Evidence-for-Open-Vocabulary-SGG.txt
related_pages:
  - language-supervised-open-vocabulary-scene-graph-vs3.md
  - prototype-based-embedding-network-scene-graph-generation.md
evidence_level: full-paper
paper:
  title: "CAGE-SGG: Counterfactual Active Graph Evidence for Open-Vocabulary Scene Graph Generation"
  abbreviated: "CAGE-SGG"
  authors:
    - Suiyang Guang
    - Chenyu Liu
    - Ruohan Zhang
    - Siyuan Chen
  affiliations:
    - Institute of Intelligent Vision and Embodied Cognition
  year: 2026
  venue: arXiv 2026
  doi: null
  arxiv: null
  code: null
  url: null
---

# CAGE-SGG: Counterfactual Active Graph Evidence for Open-Vocabulary Scene Graph Generation

## 核心思想

已有开放词汇 SGG 方法依赖视觉-语言模型的语义相似度来预测关系，容易受到语言先验和物体共现统计的影响，导致关系是"语言上合理、视觉上无依据"的幻觉。CAGE-SGG 将范式从"关系生成"（predict what relation to assign）转向"关系验证"（verify whether a candidate relation is visually grounded）。

**核心设计**：对 vision-language proposer 生成的候选关系，通过反事实验证（counterfactual intervention）检测关系分数在移除必要证据后是否下降、在保留预设干扰下是否稳定，从而判断该关系是否真实基于视觉证据。

## 方法

### 框架总览

1. **Open-Vocabulary Relation Proposer**：基于 CLIP 生成候选关系短语（top-K 候选）
2. **Relation-Type Decomposition (RTD)**：将谓词分解为软证据基（soft evidence bases）：support（支撑）、contact（接触）、containment（包含）、depth（深度）、motion（运动）、state（状态）等
3. **Relation-Conditioned Evidence Encoder (RCEE)**：提取关系特定的视觉、几何、上下文线索
4. **Counterfactual Relation Verifier (CRV)**：测试反事实干预下关系分数的变化
5. **Contradiction-Aware Predicate Learning (CAP)**：减少矛盾谓词（如同时预测 "cup on table" 和 "cup under table"）
6. **Graph-Level Preference Optimization (GPO)**：图级全局一致性优化

### 反事实验证机制

- **关系破坏型干预（relation-breaking）**：移除支撑物体（如拿掉桌子，cup on table 得分应下降）、擦除联合区域、修改几何特征
- **关系保持型干预（relation-preserving）**：保留预设无关的视角变化（如杯子的颜色改变），关系分数应保持稳定
- **评估指标**：CF-Acc（正确响应干预的比率↑）、Inv-Stab（保持稳定的比率↑）、Hallu-Rate（高置信但被反事实否决的比率↓）

### 证据基分解

谓词语义被分解为可共享的证据维度（evidence bases），如 "standing on"、"resting on"、"supported by" 共享支撑证据基。这使得未见谓词（unseen predicate）可通过共享证据基被识别，无需直接标注。

## 实验

### 数据集与设置

- **VG150**：传统封闭集 SGG 评测（150 object / 50 predicate）
- **OV-VG**：开放词汇 SGG 变体（35 seen + 15 unseen predicate）
- **PSG**：全景 SGG（mask 级关系预测）
- 主干：ResNeXt-101-FPN（Faster R-CNN 检测器）+ CLIP ViT-B/16 文本编码器（冻结）
- 训练：AdamW, lr=1e-4, batch size=12, 1×A100

### VG150 结果

| 方法 | PredCls R@50/100 | PredCls mR@50/100 | SGCls R@50/100 | SGCls mR@50/100 | SGDet R@50/100 | SGDet mR@50/100 |
|------|:-:|:-:|:-:|:-:|:-:|:-:|
| Motifs | 65.2/67.1 | 14.6/15.8 | 35.8/36.5 | 7.9/8.5 | 27.4/30.3 | 6.5/7.3 |
| VCTree | 66.4/68.1 | 16.1/17.5 | 38.1/39.2 | 8.8/9.6 | 28.7/31.9 | 7.4/8.2 |
| PE-Net | 69.8/71.6 | 23.1/25.0 | 41.7/42.9 | 14.2/15.4 | 32.4/35.5 | 12.6/13.8 |
| LLM4SGG | 70.5/72.1 | 24.0/25.8 | 42.3/43.5 | 14.8/16.1 | 33.1/36.3 | 13.2/14.4 |
| **CAGE-SGG** | **73.4/75.1** | **28.5/30.3** | **45.6/46.9** | **18.9/20.5** | **35.8/39.1** | **15.9/17.4** |

- SGDet mR@50 比 PE-Net 高 **3.3 点**（12.6→15.9），比 LLM4SGG 高 **2.7 点**
- 提升集中在 mR@K（稀有关系），R@K 增益较小，符合预期

### 开放词汇 SGG（OV-VG）

| 方法 | S-mR@50 | U-mR@50 | HM@50 |
|------|:-:|:-:|:-:|
| CLIP-ZS | 18.3 | 7.4 | 10.5 |
| OV-SGG | 22.6 | 9.8 | 13.7 |
| Pix2Graphs | 24.9 | 11.5 | 15.7 |
| OpenPSG | 25.7 | 12.1 | 16.5 |
| VL-IRM | 26.4 | 12.8 | 17.2 |
| **CAGE-SGG** | **28.9** | **17.6** | **21.9** |

- U-mR@50 **17.6**，比最佳基线 VL-IRM 12.8 高 **4.8 点**
- HM@50 **21.9**，比 VL-IRM 17.2 高 **4.7 点**
- 证据表明未见谓词受益于反事实验证中的共享证据基

### 全景 SGG（PSG）

| 方法 | PR@50 | PR@100 | PmR@50 | PmR@100 |
|------|:-:|:-:|:-:|:-:|
| PSGTR | 31.8 | 36.5 | 13.4 | 15.1 |
| OpenPSG | 36.7 | 41.2 | 17.5 | 19.4 |
| Pix2Graphs | 37.4 | 42.0 | 18.1 | 20.2 |
| **CAGE-SGG** | **40.6** | **45.3** | **21.0** | **23.4** |

- PmR@50 **21.0**，比 Pix2Graphs 18.1 高 **2.9 点**

### 反事实接地评估

| 方法 | CF-Acc↑ | Inv-Stab↑ | Hallu-Rate↓ |
|------|:-:|:-:|:-:|
| Motifs | 54.8 | 71.2 | 28.6 |
| PE-Net | 59.5 | 73.4 | 24.1 |
| Pix2Graphs | 61.7 | 75.8 | 22.5 |
| VL-IRM | 63.4 | 76.9 | 20.7 |
| **CAGE-SGG** | **74.9** | **83.5** | **12.8** |

- CF-Acc **74.9** vs VL-IRM 63.4（+11.5 点）
- Hallu-Rate **12.8%**，为所有方法最低（VL-IRM 20.7%）

### 消融研究

- 基线 proposer：U-mR@50=9.6, HM@50=13.7
- +RTD（关系类型分解）：+1.9 U-mR → 11.5
- +RCEE（关系条件证据编码）：+2.1 U-mR → 13.6
- **+CRV（反事实关系验证）：+2.9 U-mR → 16.5**，最大增益
- +CAP（矛盾感知学习）：+0.6 U-mR → 17.1
- Full（+GPO）：U-mR@50=**17.6**, HM@50=**21.9**, CF-Acc=**74.9**, Hallu-Rate=**12.8%**

### 按关系类型的增益

Geometric: 20.5 / Contact: **19.2** / Containment: **18.7** / Action: 18.4 / Functional: **16.9**（mR@50）
对比最佳基线 VL-IRM：Contact 14.6, Containment 13.1, Functional 11.5
Contact, Containment, Functional 类别增益最大，依赖具体视觉或几何证据

### 对语言先验偏置的鲁棒性

- Bias-Acc（物体对常见但关系罕见/矛盾的测试）：
  - Motifs 41.7 → CAGE-SGG **63.8**（+22.1 点）
  - Hallu-Rate 从 Motifs 34.5% 降至 **12.8%**

## 结论

- 从"关系生成"到"关系验证"的范式转换有效减少语言先验幻觉
- 反事实干预 + 证据基分解使未见谓词可通过共享视觉-几何证据被识别
- VG150 + OV-VG + PSG 三个基准上一致超越已有方法，稀有关系增益更大
- 幻觉率（Hallu-Rate）从 20.7%（VL-IRM）降至 12.8%，降幅 38%
- 反事实接地指标（CF-Acc, Inv-Stab）上的差距比标准 recall 指标更大，说明许多已有方法看似正确但实际缺乏视觉证据锚定
