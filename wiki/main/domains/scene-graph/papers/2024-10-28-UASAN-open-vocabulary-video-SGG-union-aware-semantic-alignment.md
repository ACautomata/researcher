---
title: "Open-Vocabulary Video Scene Graph Generation via Union-aware Semantic Alignment"
authors: "Ziyue Wu, Junyu Gao, Changsheng Xu"
year: 2024
venue: "ACM MM 2024"
doi: "10.1145/3664647.3681061"
arxiv: null
code: "https://github.com/ZiyueWu59/UASAN"
openreview: "https://openreview.net/forum?id=Bml0z3hGKG"
evidence_level: "full-paper"
domain: "scene-graph"
tags: ["open-vocabulary", "video-scene-graph", "union-region", "semantic-alignment", "VidVRD", "VidOR"]
status: "active"
aliases: ["UASAN"]
raw_sources:
  - ../../../sources/scene-graph/2024-10-28-UASAN-Open-Vocab-Video-SGG-Union-Aware-Alignment.pdf
  - ../../../sources/scene-graph/2024-10-28-UASAN-Open-Vocab-Video-SGG-Union-Aware-Alignment.txt
---

# UASAN: Open-Vocabulary Video Scene Graph Generation via Union-aware Semantic Alignment

> Ziyue Wu, Junyu Gao, Changsheng Xu — ACM MM 2024

## 核心思想

提出 **Union-Aware Semantic Alignment Network (UASAN)**，探索**视觉联合区域（union regions）** 与关系谓词（relation predicates）之间的语义对齐，以实现开放词汇视频场景图生成（Open-vocabulary VidSGG）。

关键洞察：现有的开放词汇 VidSGG 方法忽略了主体-客体轨迹对的联合区域（union region）与关系谓词之间的对应关系。UASAN 显式建模这种对齐，提升开放词汇关系预测能力。

## 方法架构

UASAN 由三个协作组件构成：

1. **Visual Refiner（视觉精炼器）**：从预训练 VLM（BLIP-2）中获取开放词汇知识，桥接不同模态，使模型能适应特定 VidSGG 任务场景。

2. **Semantic-Aware Context Encoder（语义感知上下文编码器）**：对目标轨迹、视觉联合区域和轨迹运动信息进行全面语义交互，生成语义感知的联合区域表示。

3. **Union-Relation Alignment Decoder（联合-关系对齐解码器）**：为每个联合区域生成判别性的关系 token，用于最终的关系预测。该解码器包含两个子模块：
   - **Relation Perception Decoder**：将联合区域表示解码为关系 token
   - **Semantic Aggregation**：聚合语义信息以增强对齐

## 训练策略

- 将目标轨迹分类和视觉关系预测分开训练
- 训练时仅使用 base-split 类别，在 novel-split 上评估泛化能力
- 仅微调 bridge encoder 模块，其他部分保持冻结

## 主要结果

### 开放词汇目标轨迹分类（VidVRD 数据集）

| 模型 | VidVRD-novel R@5 | VidVRD-novel R@10 | VidVRD-all R@5 | VidVRD-all R@10 |
|------|:---:|:---:|:---:|:---:|
| ALPro | 41.38 | 53.81 | 38.07 | 55.14 |
| RePro | 46.34 | 50.42 | 63.31 | 65.62 |
| BLIP-2 | 59.90 | 72.97 | 50.41 | 62.51 |
| **UASAN** | **68.70** | **70.79** | **73.51** | **76.39** |

### 常规 VidSGG 设定（VidVRD，仅 base 训练）

| 方法 | 训练数据 | RelDet mAP | RelDet R@50 | RelDet R@100 | RelTag P@1 |
|------|:---:|:---:|:---:|:---:|:---:|
| VRD-SGTC | base+novel | 18.38% | 11.21% | 13.69% | 60.00% |
| MHA | base+novel | 19.03% | 9.53% | 10.38% | 57.50% |
| IVRD | base+novel | 22.97% | 12.40% | 14.46% | 68.83% |
| BIG-C | base+novel | 17.67% | 9.63% | 11.29% | 56.00% |
| RePro | base | 21.33% | 12.92% | 15.94% | 59.00% |
| **UASAN** | **base** | **23.57%** | **15.90%** | **19.23%** | **65.50%** |

### 开放词汇 VidSGG（VidVRD Novel-Split）

| 方法 | SGDet mAP | SGDet R@50 | SGDet R@100 | PredCls mAP | PredCls R@50 | PredCls R@100 |
|------|:---:|:---:|:---:|:---:|:---:|:---:|
| ALPro | 1.05% | 3.14% | 4.62% | 4.09% | 9.42% | 10.41% |
| VidVRD-II | 3.57% | 8.59% | 12.39% | 7.35% | 18.84% | 26.44% |
| RePro | 6.10% | 13.38% | 16.52% | 12.74% | 25.12% | 33.88% |
| **UASAN** | **11.05%** | **13.88%** | **18.35%** | **17.62%** | **28.93%** | **36.53%** |

### 开放词汇 VidSGG（VidVRD All-Split）

| 方法 | SGDet mAP | SGDet R@50 | SGDet R@100 | PredCls mAP | PredCls R@50 | PredCls R@100 |
|------|:---:|:---:|:---:|:---:|:---:|:---:|
| RePro | 21.33% | 12.92% | 15.94% | — | 25.50% | 32.49% |
| **UASAN** | **23.57%** | **15.90%** | **19.23%** | **38.43%** | **30.01%** | **37.13%** |

## 消融实验

在 VidVRD Novel-Split SGDet 上的消融结果表明：
- 仅用 pair region（无 union region 和对齐）：mAP=6.76%
- 加入 union region：mAP=7.69%
- 加入语义感知上下文编码器（SACEnc）：mAP=10.09%
- 完整模型（加入对齐解码器 URADec）：mAP=11.05%

验证了 union region 建模和语义对齐策略各自的重要性。

## 关键贡献

1. 首次在开放词汇 VidSGG 中显式建模 union region 与 relation predicate 之间的语义对齐
2. 提出三组件框架（Visual Refiner + Semantic-Aware Context Encoder + Union-Relation Alignment Decoder）
3. 在 VidVRD 和 VidOR 基准上达到 SOTA，大量超越现有方法

## 与相关工作的对比

- 与 [[panoptic-video-scene-graph-generation|Panoptic Video SGG (2023)]] 等全监督方法不同，UASAN 面向开放词汇设定
- 与 [[language-supervised-open-vocabulary-scene-graph-vs3|VS³ (2023)]] 和 [[ovsgtr-expanding-scene-graph-boundaries|OvSGTR (2024)]] 等开放词汇方法相比，UASAN 专门针对**视频** SGG 任务
- 相关工作 [[repro-compositional-prompt-tuning-motion-cues-video-relation-detection|RePro]] 是 UASAN 的直接基线

## 已知局限

- VidOR 数据集上的实验结果放在了补充材料中，主文未呈现
- 关系预测依赖于预先检测到的目标轨迹，轨迹检测误差会传播
- 与全监督方法相比，在 base-split 上的性能仍有差距

## Provenance

- **来源文件**: `sources/scene-graph/2024-10-28-UASAN-Open-Vocab-Video-SGG-Union-Aware-Alignment.pdf`
- **提取文本**: `sources/scene-graph/2024-10-28-UASAN-Open-Vocab-Video-SGG-Union-Aware-Alignment.txt`

## 备注

- 原始 PDF 文件在 inbound 目录中误标记（实际内容为 SST-1M 望远镜 arXiv:2409.18639），已从 OpenReview 获取正确全文
- 代码已在 GitHub 开源
