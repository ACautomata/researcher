---
title: "GTR: A Grafting-Then-Reassembling Framework for Dynamic Scene Graph Generation"
authors: "Jiafeng Liang, Yuxin Wang, Zekun Wang, Ming Liu, Ruiji Fu, Zhongyuan Wang, Bing Qin"
year: 2023
venue: "IJCAI 2023"
arxiv: null
doi: "https://doi.org/10.24963/ijcai.2023/131"
code: null
domain: scene-graph
task: "Dynamic Scene Graph Generation"
evidence_level: full-paper
aliases:
  - GTR
  - Grafting-Then-Reassembling
status: active
---

# GTR: A Grafting-Then-Reassembling Framework for Dynamic Scene Graph Generation

**Venue:** IJCAI 2023
**Authors:** Jiafeng Liang (HIT), Yuxin Wang (HIT), Zekun Wang (HIT), Ming Liu (HIT & Peng Cheng Lab), Ruiji Fu (Kuaishou), Zhongyuan Wang (Kuaishou), Bing Qin (HIT)
**DOI:** [10.24963/ijcai.2023/131](https://doi.org/10.24963/ijcai.2023/131)

## 摘要

动态场景图生成旨在基于视频中的时空上下文信息识别帧间的视觉关系（subject-predicate-object）。现有方法隐式地同时建模时空交互，导致时空上下文信息纠缠。本文提出 **GTR**（Grafting-Then-Reassembling）框架，通过两个独立阶段显式提取帧内空间信息和帧间时序信息，以解耦时空上下文信息。首先嫁接一个静态场景图生成模型以生成帧内静态视觉关系，然后使用时序依赖模型提取跨帧时序依赖，最后将静态视觉关系显式重组为动态场景图。

## 核心方法

### 两阶段框架

1. **Grafting Stage（嫁接阶段）**：嫁接预训练的静态 SGG 模型，为每一帧生成静态关系三元组，无需视频级别的重新训练
2. **Reassembling Stage（重组阶段）**：
   - **Noise Filter (NFT)**：过滤嫁接阶段产生的冗余静态关系
   - **Mask Strategy**：在时序注意力模块中捕获细粒度时序依赖
   - **Temporal Dependency Model (TDM)**：由 Context Attention 和 Temporal Attention 组成，提取跨帧时序依赖并重组为动态场景图

### 关键创新

- 显式解耦时空上下文信息，避免隐式建模导致的纠缠
- 嫁接静态 SGG 模型，仅需少量视频数据微调，降低标注和训练成本
- 通过重组阶段建模时序上下文信息，显著提升动态场景图质量

## 实验结果

### Action Genome 数据集

| 任务 | 指标 | GTR | 先前最佳（AP-Net） | 提升 |
|------|------|-----|-------------------|------|
| PredCls | R@10 | **71.2** | 69.4 | +1.8 |
| PredCls | R@20 | **74.5** | 73.8 | +0.7 |
| PredCls | R@50 | **74.5** | 73.8 | +0.7 |
| SGCls | R@10 | **48.7** | 47.2 | +1.5 |
| SGCls | R@20 | **49.7** | 48.9 | +0.8 |
| SGCls | R@50 | **49.7** | 48.9 | +0.8 |
| SGDet | R@10 | **27.9** | 26.3 | +1.6 |
| SGDet | R@20 | **37.0** | 36.1 | +0.9 |
| SGDet | R@50 | **39.9** | 38.3 | +1.6 |
| **Mean** | | **52.6** | 51.4 | +1.2 |

### 低数据训练性能

- 使用 **60%** 视频数据训练，PredCls R@10 达 **71.2%**，超越先前最佳结果（使用 100% 数据训练的 AP-Net 69.4%）
- 表明 GTR 嫁接静态模型的设计显著降低了对视频数据量的需求

### 消融实验

| 设置 | SGDet R@20 | SGDet R@50 |
|------|-----------|-----------|
| Full GTR | **39.9** | **37.0** |
| w/o NFT | 37.0 | 39.0 |
| w/o Mask Strategy | 36.1 | 39.0 |
| w/o TDM | 35.1 | 37.9 |
| w/o Context Attention | 37.5 | — |
| w/o Temporal Attention | 34.7 | — |

### 与 STTran 的连续动作区分对比

GTR 在区分视觉相似的连续动作（如"holding→drinking from"、"holding→eating"）上显著优于 STTran，体现了更精确的时空交互建模能力。

## 方法对比

| 方法 | 范式 | 时空建模 | 视频数据需求 |
|------|------|---------|------------|
| STTran (Cong et al., 2021) | One-stage Transformer | 隐式 | 高 |
| AP-Net (?) | One-stage | 隐式 | 高 |
| **GTR (Ours)** | **Two-stage（嫁接+重组）** | **显式解耦** | **低（60% 数据达 SOTA）** |

## 分析

1. **显式解耦优势**：两阶段分离帧内空间信息和帧间时序信息，避免了端到端隐式建模中信息的纠缠
2. **低数据需求**：嫁接阶段复用了静态 SGG 模型的先验知识，仅需少量视频数据进行时序建模，大幅降低视频标注成本
3. **重组阶段关键性**：消融实验表明去除重组阶段性能显著下降，验证了时序建模是动态 SGG 的核心

## 局限与展望

- 依赖于嫁接的静态 SGG 模型质量
- 在更大规模或更多样化的视频数据集上的泛化能力未验证
- 可扩展至其他视频理解任务（如视频问答、视觉推理）

## 参考链接

- [IJCAI 2023 Proceedings](https://www.ijcai.org/proceedings/2023/131)
- [PDF (IJCAI)](https://www.ijcai.org/proceedings/2023/0131.pdf)
