---
title: "GaussianGraph: 3D Gaussian-based Scene Graph Generation for Open-world Scene Understanding"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - 3d-gaussian-splatting
  - scene-graph-generation
  - open-world-scene-understanding
  - object-grounding
  - semantic-segmentation
  - adaptive-clustering
  - spatial-consistency
  - arXiv-2025
raw_sources:
  - ../../../raw/sources/2025-03-GaussianGraph-3D-Gaussian-Scene-Graph.pdf
  - ../../../raw/sources/2025-03-GaussianGraph-3D-Gaussian-Scene-Graph.txt
related_pages:
  - 3d-spatial-multimodal-knowledge-accumulation-scene-graph-prediction-point-cloud.md
  - incremental-3d-scene-graph-prediction-from-rgb-sequences.md
evidence_level: full-paper
paper:
  title: "GaussianGraph: 3D Gaussian-based Scene Graph Generation for Open-world Scene Understanding"
  abbreviated: "GaussianGraph"
  authors:
    - Xihan Wang
    - Dianyi Yang
    - Yu Gao
    - Yufeng Yue
    - Yi Yang
    - Mengyin Fu
  year: 2025
  venue: "arXiv (preprint)"
  arXiv: "2503.04034"
  code: "https://wangxihan-bit.github.io/GaussianGraph"
  paper_url: "https://arxiv.org/abs/2503.04034"
  affiliation: "Beijing Institute of Technology"
---

# GaussianGraph: 3D Gaussian-based Scene Graph Generation for Open-world Scene Understanding

## 概述

GaussianGraph 是一个结合 3D Gaussian Splatting (3DGS) 与场景图生成的框架，用于开放世界 3D 场景理解。现有 3DGS 语义理解方法（如 LangSplat、OpenGaussian、LEGaussian）主要聚焦于将压缩的 CLIP 特征嵌入到 3D Gaussians 中，存在物体分割精度低、缺乏空间推理能力两大瓶颈。GaussianGraph 通过引入自适应语义聚类（"Control-Follow" 聚类策略）和 3D 场景图生成来解决这些问题。

## 方法

### 核心架构

GaussianGraph 由三个核心组件构成：

1. **2D 特征提取（2D Feature Extraction）**：利用 SAM2 获取 2D 分割掩码，通过 LLaVA-1.6 提取图像标注（captions）和关系三元组（relation triples），OpenCLIP ViT-B/16 提取 CLIP 特征。

2. **"Control-Follow" 自适应聚类策略**：核心创新之一。传统方法直接对高斯分布进行特征压缩或固定聚类，GaussianGraph 提出自适应选择聚类数量（依据场景尺度和特征分布动态调整），避免特征压缩。使用 Farthest Point Sampling (FPS) 或 Fast Point Feature Histogram (FPFH) 采样控制点，再基于 MeanShift 算法进行聚类。FPFH 采样因更好地利用物体边缘几何信息，效果优于 FPS。

3. **3D 场景图构建与修正模块（3D Scene Graph & 3D Correction Modules）**：
   - 将渲染图像输入 VLM（BLIP-2 或 LLaVA）提取物体属性和空间关系
   - 将 2D 信息关联到 3D Gaussian 簇，构建节点（属性）和边（关系）的场景图
   - **3D 修正模块**：通过空间一致性验证（spatial consistency verification）过滤不可靠的关系三元组，包含四个子模块（论文图 2 标注的四个子模块），解决 VLM 直接生成 3D 关系时的不准确问题

### 关键技术细节

- 实现基于 OpenCLIP ViT-B/16、LLaVA-1.6、SAM2 L 模型
- 下游任务使用 LLama-3-8B 或 GPT-4o 进行目标推理
- 训练硬件：NVIDIA RTX-3090
- 对象对构建阈值 θ≈0.8，场景图构建 μ=0.9

## 实验结果

### 开放词汇语义分割（LERF 数据集）

在 LERF 4 个场景（ramen、teatime、waldo kitchen、figurines）上的结果，直接解码高斯 CLIP 特征以反映真实的 3D 理解能力：

| 方法 | Acc@0.25 Mean | Acc@0.5 Mean | mIoU Mean |
|------|:------------:|:-----------:|:--------:|
| LangSplat [7] | 13.19 | 10.92 | 12.25 |
| LEGaussian [9] | 29.30 | 23.82 | 16.21 |
| OpenGaussian [8] | 59.81 | 52.05 | 41.78 |
| **GaussianGraph (Ours)** | **64.07** | **54.22** | **47.53** |

以 figurines 场景具体数据为例：
- GaussianGraph: mIoU=62.00%, Acc@0.25=81.24%, Acc@0.5=75.61%
- OpenGaussian: mIoU=57.50%, Acc@0.25=78.57%, Acc@0.5=71.43%
- **GaussianGraph mIoU 比 SOTA (OpenGaussian) 高 4-10%**

### 语义分割（Replica & ScanNet 数据集）

| 方法 | Replica mIoU↑ | Replica mAcc↑ | ScanNet mIoU↑ | ScanNet mAcc↑ |
|------|:-----------:|:------------:|:------------:|:------------:|
| **PointCloud-based** | | | | |
| ConceptFusion [33] | 10.07 | 16.15 | 9.72 | 15.41 |
| ConceptGraph [13] | 20.72 | 31.54 | 16.42 | 27.60 |
| HOV-SG [14] | 23.16 | 29.85 | 22.43 | 43.81 |
| **3DGS-based** | | | | |
| LangSplat [7] | 4.72 | 9.12 | 3.28 | 8.95 |
| LEGaussian [9] | 4.80 | 11.59 | 3.51 | 10.04 |
| OpenGaussian [8] | 26.39 | 44.28 | 24.73 | 41.54 |
| **GaussianGraph (Ours)** | **31.18** | **49.14** | **31.09** | **48.91** |

GaussianGraph 在所有指标上超越 PointCloud-based 和 3DGS-based 方法，在 ScanNet 上 mIoU=31.09 较 OpenGaussian 24.73 提升显著。

### 目标定位（Grounding）

在 Sr3D+ 和 Nr3D 数据集上评估场景图的推理能力：

**Sr3D+**：
| 方法 | Easy A@0.1 | Easy A@0.25 | Hard A@0.1 | Hard A@0.25 | Overall A@0.1 | Overall A@0.25 |
|------|:---------:|:----------:|:---------:|:----------:|:------------:|:-------------:|
| LangSplat | 4.7 | 1.5 | 2.1 | 1.1 | 4.5 | 2.3 |
| OpenGaussian | 7.3 | 5.1 | 3.6 | 1.9 | 7.0 | 4.9 |
| ConceptGraph | 13.0 | 6.8 | 16.0 | 1.3 | 13.3 | 6.2 |
| OpenFusion | 14.0 | 2.4 | 1.3 | 1.3 | 12.6 | 2.4 |
| **GaussianGraph** | **19.1** | **7.7** | **16.3** | **5.6** | **18.2** | **7.4** |

**Nr3D**：
| 方法 | Easy A@0.1 | Easy A@0.25 | Hard A@0.1 | Hard A@0.25 | Overall A@0.1 | Overall A@0.25 |
|------|:---------:|:----------:|:---------:|:----------:|:------------:|:-------------:|
| LangSplat | 8.5 | 1.7 | 3.4 | 1.2 | 7.4 | 1.5 |
| OpenGaussian | 10.1 | 5.9 | 7.4 | 3.1 | 9.5 | 4.7 |
| ConceptGraph | 18.7 | 9.2 | 9.1 | 2.0 | 16.0 | 7.2 |
| OpenFusion | 12.9 | 1.4 | 5.1 | 1.5 | 10.7 | 1.4 |
| **GaussianGraph** | **20.7** | **12.1** | **10.9** | **6.3** | **17.2** | **8.6** |

GaussianGraph 在 Sr3D+ 上 Overall A@0.1=18.2（比 ConceptGraph 13.3 高 4.9），在 Nr3D 上 Overall A@0.1=17.2（比 ConceptGraph 16.0 高 1.2）。

### 消融实验

**"Control-Follow" 聚类策略（LERF）**：FPFH 采样 + Control-Follow 聚类在 Acc@0.5 Mean=54.22, mIoU Mean=47.53，相比 FPS 采样 + Control-Follow（Acc@0.5 Mean=49.80, mIoU Mean=41.77）和直接使用 OpenGaussian 聚类（提升 4-10%），说明边缘几何信息对分割精度的贡献。

**3D 修正模块（LERF）**：使用 LLaVA 作为 VLM 时，3D 修正模块使功能查询 mR@1 从 49.72 提升到 52.81，位置查询 mR@1 从 40.73 提升到 44.96，验证了空间一致性验证的有效性。

## 方法对比分析

### 与 3DGS 语义方法的差异

| 方面 | LangSplat / OpenGaussian / LEGaussian | GaussianGraph |
|------|--------------------------------------|--------------|
| 聚类策略 | 固定/压缩 CLIP 特征 | "Control-Follow" 自适应聚类，避免压缩 |
| 表示能力 | 仅语义特征 | 语义特征 + 物体属性 + 空间关系 |
| 推理能力 | 无 | 场景图驱动的空间推理 |
| 关系提取 | 不处理 | 2D VLM → 3D 修正 → 场景图 |

### 与 3D 场景图方法的差异

| 方面 | ConceptGraph / HOV-SG | GaussianGraph |
|------|----------------------|--------------|
| 基础表示 | Point Cloud | 3D Gaussian |
| 参数规模 | 大，生成视觉描述耗时长 | 相对轻量 |
| 关系修正 | 无 | 3D 空间一致性验证过滤错误关系 |
| 运行效率 | 较低 | 较优（基于 3DGS 渲染效率和聚类优化） |

## 结论

GaussianGraph 的核心贡献在于：
1. **"Control-Follow" 自适应聚类**：避免 CLIP 特征压缩，动态适配场景尺度和特征分布，显著提升分割精度
2. **3D 场景图构建**：将 2D VLM 提取的属性和关系关联到 3DGS 表示
3. **3D 修正模块**：通过空间物理约束过滤 VLM 生成的不准确关系三元组

在 LERF、Replica、ScanNet 三个数据集上的语义分割和目标定位任务中全面超越现有 SOTA 方法（包括 PointCloud-based 和 3DGS-based）。开放词汇语义分割 mIoU 比 OpenGaussian 高 4-10%，目标定位 A@0.1 在 Sr3D+ 和 Nr3D 分别达到 18.2 和 17.2。

未来工作方向：实时更新场景图、多机器人协作在线构建。

## References

- 3DGS: Kerbl et al., "3D Gaussian Splatting for Real-Time Radiance Field Rendering", ACM TOG 2023
- LangSplat: Qin et al., CVPR 2024
- OpenGaussian: Wu et al., arXiv:2406.02058
- ConceptGraph: Gu et al., ICRA 2024
- HOV-SG: Werby et al., ICRA 2024 Workshop
