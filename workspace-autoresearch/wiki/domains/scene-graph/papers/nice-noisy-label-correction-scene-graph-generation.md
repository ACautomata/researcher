---
title: "The Devil Is in the Labels: Noisy Label Correction for Robust Scene Graph Generation"
authors: ["Lin Li", "Long Chen", "Yifeng Huang", "Zhimeng Zhang", "Songyang Zhang", "Jun Xiao"]
year: 2022
venue: CVPR 2022
doi: null
arxiv: null
code: "https://github.com/muktilin/NICE"
tags: [scene-graph-generation, noisy-label, robust-sgg, CVPR-2022]
evidence_level: full-paper
status: active
created: 2026-06-10
---

# The Devil Is in the Labels: Noisy Label Correction for Robust Scene Graph Generation

> Lin Li, Long Chen, Yifeng Huang, Zhimeng Zhang, Songyang Zhang, Jun Xiao. CVPR 2022.

## 核心思想

SGG 标签噪声纠正的开创性工作。指出 VG 数据集的标签噪声问题，将 SGG 重新定义为 noisy label learning 问题。

**关键洞察：** 现有 SGG 方法普遍接受两个隐含假设：（1）所有人工标注的正样本同等正确；（2）所有未标注的负样本都是背景。本文论证这两个假设在 SGG 中不成立。

## 标签噪声类型

本文识别出 VG 数据集中的三种标签噪声：

1. **Common-prone（粗粒度倾向）：** 标注者倾向于选择更常见的粗粒度谓词（如 `on` 代替 `riding`），导致标注缺乏信息量。
2. **Synonym-random（同义词随机选择）：** 对于同义谓词（如 `has` vs `with`），标注者随机选择，同一视觉模式标注不一致。
3. **Negative（缺失标注）：** 大量未标注的负样本实际是存在关系的正样本被遗漏标注。

## 方法：NICE

NICE（NoIsy label CorrEction）包含三个模块：

### ① Neg-NSD（负样本噪声检测）
- 将检测缺失标注的负样本建模为 **OOD 检测问题**
- 正样本作为 in-distribution（ID）数据，未标注负样本作为 OOD 测试数据
- 检测到的缺失标注样本被赋予伪标签

### ② Pos-NSD（正样本噪声检测）
- 基于 **聚类** 的算法，将正样本按局部密度分组
- 噪声最大的簇被视为噪声正样本
- 处理 common-prone 和 synonym-random 两类噪声

### ③ NSC（噪声样本纠正）
- 使用 **加权 KNN** 为噪声正样本重新分配谓词标签
- 根据特征空间中近邻样本的标签加权投票决定新标签

**输出：** 经清理的 SGG 训练数据集。

## Experiments

### 实验设置
- **数据集：** Visual Genome (VG)
- **Backbone：** VGG-16, ResNeXt-101-FPN
- **Base SGG 模型：** Motifs, VCTree（含多种 debiasing 方法作对比）
- **任务：** PredCls, SGCls, SGGen
- **指标：** Recall@K (R@K), mean Recall@K (mR@K), Mean

### 主要结果（PredCls 任务）

| 方法 | mR@50/100 | R@50/100 | Mean | 备注 |
|------|-----------|---------|------|------|
| Motifs (baseline) | 16.5 / 17.8 | 65.5 / 67.2 | 41.8 | CVPR 2018 |
| + TDE | 24.2 / 27.9 | 45.0 / 50.6 | 36.9 | CVPR 2020 |
| + PCPL | 24.3 / 26.1 | 54.7 / 56.5 | 40.4 | MM 2020 |
| + CogTree | 26.4 / 29.0 | 35.6 / 36.8 | 32.0 | IJCAI 2021 |
| + DLFE | 26.9 / 28.8 | 52.5 / 54.2 | 40.6 | MM 2021 |
| + BPL-SA | 29.7 / 31.7 | 50.7 / 52.5 | 41.2 | ICCV 2021 |
| **+ NICE (ours)** | **29.9 / 32.3** | **55.1 / 57.2** | **43.6** | **本方法** |

### VCTree 系列结果（PredCls 任务）

| 方法 | mR@50/100 | R@50/100 | Mean |
|------|-----------|---------|------|
| VCTree | 17.1 / 18.4 | 65.9 / 67.5 | 42.2 |
| + TDE | 26.2 / 29.6 | 44.8 / 49.2 | 37.5 |
| + PCPL | 22.8 / 24.5 | 56.9 / 58.7 | 40.7 |
| + CogTree | 27.6 / 29.7 | 44.0 / 45.4 | 36.7 |
| + DLFE | 25.3 / 27.1 | 51.8 / 53.5 | 39.4 |
| + BPL-SA | 30.6 / 32.6 | 50.0 / 51.8 | 41.3 |
| **+ NICE (ours)** | **30.7 / 33.0** | **55.0 / 56.9** | **43.9** |

### 关键数值提升

- **Motifs + NICE vs. Motifs baseline：** mR@100 **↑14.5**（17.8 → 32.3）
- **VCTree + NICE vs. VCTree baseline：** mR@100 **↑14.6**（18.4 → 33.0）
- NICE 在提升 mR@K（尾部类别）的同时，能保持较高的 R@K（头部类别）性能
- 在 SGCls 和 SGGen 任务上同样有显著提升

### 消融实验

- **Neg-NSD 单独：** mR@100 从 17.8 → 25.2（+7.4），说明缺失标注的负样本纠正确实有益
- **Pos-NSD 单独：** 即使只用更少的正样本训练，mR@K 指标仍然提升
- **三者组合（完整 NICE）：** 达到最佳性能
- 聚类距离阈值 dc 对不同谓词类别需要差异化设置（head 类用小阈值，tail 类用大阈值）

## 分析

### 优势
1. **开创性视角：** 首次将 SGG 标注质量问题系统化，识别出三种具体噪声类型
2. **模型无关：** NICE 可作为预处理模块，兼容任意 SGG 架构
3. **可解释性强：** 每个模块有明确的语义含义和目标
4. **代码开源：** 推动后续研究

### 局限
1. 依赖聚类超参数（dc 距离阈值）的手工设置
2. OOD 检测阶段可能需要额外的训练数据
3. 主要在 VG 上验证，对其他 SGG 数据集（如 PSG）的泛化性需进一步验证

## 后续影响

- 启发了后续 SGG 标签质量研究
- 推动了 noisy label learning 在 SGG 领域的应用
- 被引用为 SGG 数据质量分析的基础工作

## 原始资料
- PDF: [raw/sources/2022-CVPR-Devil-Is-in-the-Labels-Noisy-Label-Correction-SGG.pdf](/raw/sources/2022-CVPR-Devil-Is-in-the-Labels-Noisy-Label-Correction-SGG.pdf)
- 提取文本: [raw/sources/2022-CVPR-Devil-Is-in-the-Labels-Noisy-Label-Correction-SGG.txt](/raw/sources/2022-CVPR-Devil-Is-in-the-Labels-Noisy-Label-Correction-SGG.txt)
- 论文链接: https://openaccess.thecvf.com/content/CVPR2022/papers/Li_The_Devil_Is_in_the_Labels_Noisy_Label_Correction_for_CVPR_2022_paper.pdf
