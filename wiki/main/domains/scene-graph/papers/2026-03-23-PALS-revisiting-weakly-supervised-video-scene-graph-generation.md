---
title: "PALS: Revisiting Weakly-Supervised Video SGG via Pair Affinity Learning"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags: [weakly-supervised, video-sgg, pair-affinity, arXiv-2026]
raw_sources:
  - ../../../sources/scene-graph/2026-arXiv-Revisiting-Weakly-Supervised-Video-SGG.pdf
  - ../../../sources/scene-graph/2026-arXiv-Revisiting-Weakly-Supervised-Video-SGG.txt
evidence_level: full-paper
---

# PALS: Revisiting Weakly-Supervised Video Scene Graph Generation via Pair Affinity Learning

> 通过**可学习的 pair affinity** 抑制非交互对象对，在弱监督视频场景图生成（WS-VSGG）中大幅缩小与全监督的差距

## 摘要

Weakly-supervised video scene graph generation (WS-VSGG) 旨在无需边界框标注、仅依赖稀疏时间标注的条件下解析视频内容为结构化关系三元组。现有工作直接使用 off-the-shelf 目标检测器，存在一个根本性疏忽：**全监督检测器隐式过滤了非交互对象**，而 off-the-shelf 检测器无差别检测所有可见对象，导致关系模型被噪声对淹没。

本文提出 **PALS** (Pair Affinity Learning and Scoring) + **PAM** (Pair Affinity Modulation) + **RAM** (Relation-Aware Matching)，构建了一个模型无关的 WS-VSGG 框架。核心是学习一个可训练的 pair affinity 分数，估计 subject-object 对之间交互的可能性，将其融入推理排序和上下文推理。在 Action Genome 上取得 WS-VSGG SOTA，达到全监督上限 R@10 的 **88.3%**（With Constraint）和 **94.3%**（No Constraint）。

## 核心贡献

1. **Pair Affinity Learning and Scoring (PALS)** — 可学习的 pair affinity 估计交互概率，在推理时用于重排序，抑制非交互对
2. **Pair Affinity Modulation (PAM)** — 将 pair affinity 积分到 Transformer 注意力中，通过门控机制抑制非交互对的上下文干扰
3. **Relation-Aware Matching (RAM)** — 利用 vision-language grounding（GroundingDINO）解析伪标签生成中的类级歧义，提供更干净的 pair affinity 学习监督信号

## 方法

### 问题设定

WS-VSGG 设置：仅在视频中间帧提供未定位的三元组标注 ⟨subject, predicate, object⟩（PLA [1]）。检测阶段使用预训练 off-the-shelf 检测器（如 VinVL），关系模型需要在无 GT 框的条件下将检测到的 proposals 与关系三元组匹配。

**关键观察**：全监督检测器的检测数量（5.01 dets/frame）远少于 WS-VSGG 使用的 off-the-shelf 检测器（15.15 dets/frame），多出的检测多数为非交互对象。现有 WS-VSGG 方法未处理这种分布偏移。

### PALS — Pair Affinity Learning and Scoring

- 在关系特征提取器之上添加轻量级 pair affinity head（FFN → sigmoid），为每个 subject-object 对输出 $a_{ij} \in [0,1]$
- 训练信号：匹配到的对为正样本（$y_{ij}=1$），匹配失败的对为负样本（$y_{ij}=0$）
- 损失函数：$\mathcal{L}_{PA} = -\frac{1}{|B|} \sum_{(i,j) \in B} \left[ y_{ij} \log a_{ij} + (1 - y_{ij}) \log(1 - a_{ij}) \right]$
- 使用 **class-balanced BCE** 处理严重的正负样本不平衡（约 1:10）
- 推理时：将 pair affinity 分数作为乘性权重 $R^{(s,o)} = a_{so} \cdot R^{(s,o)}_{pred}$ 融入排序

### PAM — Pair Affinity Modulation

- 在 relation decoder 的交叉注意力中，利用 pair affinity $a_{so}$ 调制 attention logits
- 对 head $h$ 的 attention logits：$\tilde{A}^{(h)}_{ql} = A^{(h)}_{ql} - m \cdot \mathbb{1}[a_{so}(q,l) < \tau_{PAM}]$
- 非交互对的 attention 被减去一个 margin $m$，抑制其参与上下文推理
- 门控受 hinge-based ranking loss 约束：$\mathcal{L}_{PAM} = \sum_{(a,b^+,b^-)} \max(0, G_L^{(a,b^-)} - G_L^{(a,b^+)} + m)$

### RAM — Relation-Aware Matching

- **问题**：PLA 的类级匹配基于"detected object class = triplet object class"，但同一类可能有多个实例（multi-instance ambiguity）
- **方法**：使用 vision-language 模型（GroundingDINO）对检测框进行 grounding score 评估，优先选择与关系描述（如"cup/glass/bottle that the person is holding"）匹配的框
- **流程**：VL 模型定位 → 按 grounding score 排序 → 取 top-1（多实例）或加权匹配 → 可靠性过滤（$\tau_r, \tau_{gs}$）
- **效果**：RAM + GDINO 将匹配精度提升 **+80.6%**（PLA baseline：0.402 → 0.726），F1 提升 +22.4%

### 完整框架

1. Off-the-shelf 检测器生成 proposals
2. **RAM** 预处理：用 VL grounding 细化伪标签匹配
3. 关系特征提取器 + **PALS** head 学习 pair affinity
4. **PAM** 在 relation decoder 注意力中抑制非交互对
5. 推理时 **PALS** 分数用于重排序

## 实验

### 数据集与设置

- **数据集**：Action Genome (AG) — SGDet 协议
- **检测器**：VinVL（off-the-shelf）
- **VL 模型**：GroundingDINO（默认）
- **骨干网络**：STTran [2], DSG-DETR [3]
- **弱监督基线**：PLA [1], TRKT [33]
- **评价指标**：Recall@K (K ∈ {10, 20, 50})，With Constraint (WC) 和 No Constraint (NC) 两种协议
- **超参数**：lr=1e-5, epochs=5, batch_size=1 (video-level), τ_r=0.3, τ_gs=0.2

### 主要结果（SGDet on AG）

| Backbone | Supervision | Method | WC R@10 | WC R@20 | WC R@50 | NC R@10 | NC R@20 | NC R@50 |
|----------|-------------|--------|---------|---------|---------|---------|---------|---------|
| STTran | Weak | PLA [1] | 15.39 | 21.44 | 26.24 | 15.83 | 22.83 | 31.74 |
| STTran | Weak | **PLA + Ours** | **22.24** | **26.48** | **28.00** | **23.20** | **30.24** | **37.47** |
| STTran | Full | Vanilla | 25.20 | 34.10 | 37.00 | 24.60 | 36.20 | 48.80 |
| DSG-DETR | Weak | PLA | 15.47 | 21.33 | 25.86 | 15.66 | 22.71 | 31.90 |
| DSG-DETR | Weak | **PLA + Ours** | **21.88** | **25.92** | **27.41** | **23.13** | **30.34** | **37.51** |
| DSG-DETR | Full | Vanilla | 30.30 | 34.80 | 36.10 | 32.10 | 40.90 | 48.30 |

- **最佳配置**：PLA + Ours on STTran，WC R@10=22.24, NC R@10=23.20
- **全监督对比**：达到全监督上限 R@10 的 **88.3%** (WC) 和 **94.3%** (NC)
- **平均提升**：+5.47 R@10 (WC), +6.43 R@10 (NC)

### 消融实验

| 配置 | RAM | PALS | PAM | WC R@10 | WC R@50 | NC R@10 | NC R@50 |
|------|:---:|:----:|:---:|:-------:|:-------:|:-------:|:-------:|
| (a) Baseline | | | | 15.39 | 26.24 | 15.83 | 31.74 |
| (b) +PALS | | ✓ | | 19.79 | 26.34 | 21.03 | 33.63 |
| (c) +PALS+PAM | | ✓ | ✓ | 20.22 | 26.83 | 21.63 | 34.73 |
| (d) +RAM | ✓ | | | 15.90 | 26.63 | 16.46 | 32.36 |
| (e) +RAM+PALS | ✓ | ✓ | | 22.14 | 27.07 | 23.12 | 36.35 |
| (f) **Full** | ✓ | ✓ | ✓ | **22.24** | **28.00** | **23.20** | **37.47** |

- PALS 贡献最大个体增益（+4.40 WC R@10）
- RAM 单独效果有限，但与 PALS 协同后大幅放大（(d)→(e): +6.24 WC R@10）
- PAM 提供一致提升，在高 K 值下改善更显著
- 三者协同：每个组件在另两者存在时发挥更大作用

### RAM 伪标签质量

| Detector | VL Model | Precision | Recall | F1 |
|----------|----------|:---------:|:------:|:--:|
| PLA | —（原始） | 0.402 | 0.442 | 0.421 |
| PLA | GLIP | 0.589 (+46.6%) | 0.366 (-17.2%) | 0.451 (+7.2%) |
| PLA | GroundingDINO | **0.726 (+80.6%)** | 0.400 (-9.7%) | **0.515 (+22.4%)** |
| TRKT | —（原始） | 0.319 | 0.479 | 0.383 |
| TRKT | GLIP | 0.458 (+43.6%) | 0.374 (-22%) | 0.412 (+7.5%) |
| TRKT | GroundingDINO | 0.560 (+75%) | 0.399 (-17%) | 0.466 (+22%) |

### 计算开销

| Model | Params (M) | FLOPs (G) | Latency (ms/video) |
|-------|:----------:|:---------:|:------------------:|
| STTran | 103.67 | 138.91 | 20.95 |
| STTran + Ours | 104.99 (+1.27%) | 138.92 (+0.01%) | 20.95 (+0%) |
| DSG-DETR | 103.67 | 140.05 | 18.09 |
| DSG-DETR + Ours | 104.99 (+1.27%) | 140.10 (+0.04%) | 18.10 (+0.05%) |

### 其他实验

- **NL-VSGG 泛化**：在更弱的自然语言监督设置下（NL-VSGG [10]），方法同样有效，在 STTran 上 WC R@10 从 9.48 提升到 13.42
- **VL 模型选择**：仅需具备**显式区域-文本对齐**能力的 VL 模型（GroundingDINO, GLIP, MDETR）可用；BLIP、SigLIP2 等全局对齐模型无效
- **非交互对比例分析**：PAM 在非交互对比例高的视频子集上增益最大（WC R@10: +4.28 vs +0.38）

## 讨论

### 意义

- **核心 insight**：WS-VSGG 的根本瓶颈是 off-the-shelf 检测器产生的非交互对象对，而非关系建模能力本身
- **与全监督的差距大幅缩小**：仅用单帧未定位标注就达到全监督 88.3% / 94.3%，是 WS-VSGG 的重要里程碑
- **计算开销极低**：仅 +1.27% 参数，几乎零 FLOPs/latency 开销
- **模型无关**：兼容多种检测器-关系模型组合，可即插即用

### 局限

- 输入侧依赖 off-the-shelf 检测器质量（VinVL），Better detector 可能进一步提升结果
- RAM 需要额外的 VL 模型推理，虽只用于训练预处理
- TRKT + Ours 因 TRKT 本身匹配精度低（F1=0.466 vs PLA 0.515）而表现弱于 PLA + Ours

## 与我库中其他论文的关联

- **[SSC-SGG](ssc-sgg-semi-supervised-clustering-weakly-supervised-scene-graph-generation.md)** — 也是弱监督 SGG 方法，但聚焦在图/超图层面的半监督聚类，PALS 从 pair-level 过滤出发，可互补
- **[TEMPURA](tempura-unbiased-video-scene-graph-generation.md)** — 无需检测器的视频 SGG，使用生成式 attention map，PALS 对不同检测器分布偏移的处理思路可借鉴到类似无检测设置
- **[FReMuRe](2026-06-09-fremure-frequency-guided-multi-level-reasoning-video-sgg.md)** — 视频 SGG 的长尾去偏，与 PALS 的 pair affinity 视角正交

## 参考资料

- PLA [1]: Predicted Label Approximation for Weakly Supervised Video Scene Graph Generation
- STTran [2]: Scene Graph Transformer for Video
- DSG-DETR [3]: Dynamic Scene Graph Generation with Detection Transformer
- TRKT [33]: Temporal Relation Knowledge Transfer for WS-VSGG
- GroundingDINO [16]: Grounding DINO: Marrying DINO with Grounded Pre-Training
- NL-VSGG [10]: Weakly Supervised Video Scene Graph Generation with Natural Language Supervision
