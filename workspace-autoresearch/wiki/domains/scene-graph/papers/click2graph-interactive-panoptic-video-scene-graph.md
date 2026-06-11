---
title: Click2Graph: Interactive Panoptic Video Scene Graphs from a Single Click
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - video-scene-graph
  - panoptic-scene-graph
  - interactive-scene-graph
  - visual-prompting
  - sam2
  - interaction-discovery
  - user-guided
  - opensg
  - openpvsg
  - arxiv-2025
raw_sources:
  - raw/sources/2025-11-25-click2graph-interactive-panoptic-video-scene-graph.pdf
  - raw/sources/2025-11-25-click2graph-interactive-panoptic-video-scene-graph.txt
paper:
  title: Click2Graph: Interactive Panoptic Video Scene Graphs from a Single Click
  authors:
    - Raphael Ruschel
    - Hardikkumar Prajapati
    - Md Awsafur Rahman
    - B. S. Manjunath
  year: 2025
  venue: arXiv 2025
  arxiv: "2511.15948"
  doi: null
  code: null
  project: null
classification:
  label: Click2Graph
  task:
    - Interactive Panoptic Video Scene Graph Generation
    - User-Guided PVSG
  method_family:
    - Visual Prompting
    - Set-based Transformer
    - Promptable Segmentation (SAM2)
  modality:
    - Video (RGB)
  datasets:
    - OpenPVSG (VidOR / EPIC-Kitchens / Ego4D)
  metrics:
    - R@K (Recall@K)
    - SpIR (Spatial Interaction Recall)
    - PLR (Prompt Localization Recall)
evidence_level: full-paper
---

# Click2Graph: Interactive Panoptic Video Scene Graphs from a Single Click

## Citation

Raphael Ruschel, Hardikkumar Prajapati, Md Awsafur Rahman, B. S. Manjunath. "Click2Graph: Interactive Panoptic Video Scene Graphs from a Single Click." arXiv:2511.15948v2, Nov 2025.

## One-Sentence Contribution

首次提出**用户引导的交互式全景视频场景图生成（PVSG）框架**，从单个视觉提示（点击/框/掩码）出发，结合 SAM2 分割跟踪 + 动态交互发现模块（DIDM）+ 语义分类头（SCH），自动发现与用户指定目标交互的物体并预测关系三元组，实现可控、可解释的视频场景理解。

## Problem Setting

**出发点**：现有 VSGG/PVSG 系统是封闭的全自动流水线——模型一旦错误检测或分类，用户无法干预；可提示分割模型（SAM/SAM2）提供精确用户交互但缺乏语义和关系推理。两者之间存在根本性割裂。

**核心挑战**：
1. 如何从单一点击出发，自动发现与指定主体交互的物体（而非全图所有物体）？
2. 如何在用户引导下实现像素级精确、时序一致且关系完整的全景场景图生成？
3. 如何将 promptable segmentation 的几何输出提升为结构化语义推理？

**任务定义**：给定视频 V = {I₁, ..., I_T} 和用户提示 P_i（点/框/掩码）指定目标主体，输出交互 tracklets 集合：ATᵢ = {⟨sᵢ, oᵢⱼ, rᵢⱼ, SM, OM, t_start, t_end⟩}，包含主体掩码、交互物体掩码及关系标签的时序序列。

## Method

### Architecture Overview

Click2Graph 基于 **SAM2.1-Large** 作为 promptable video segmentation 骨干（冻结 224M 参数），引入两个轻量模块（约 5M 可训练参数）：

1. **Dynamic Interaction Discovery Module (DIDM)** — 主体条件化的物体提示生成
2. **Semantic Classification Head (SCH)** — 主体/物体/谓词联合分类

整体架构见 Figure 2。

### Dynamic Interaction Discovery Module (DIDM)

轻量级基于集合的 Transformer 模块，将单用户提示转换为一组空间精确的物体提示：

1. 接收 SAM2 backbone 编码的图像特征
2. 为目标主体生成专用主体特征 token（结合可学习主体嵌入 + 主体分割掩码特征）
3. 将主体 token 与 N_q=3 个可学习物体查询嵌入拼接，通过 Transformer decoder 对图像特征做 cross-attention
4. 将精炼后的物体 token 映射为归一化 (x, y) 坐标，作为 SAM2 的 prompt 位置

N_q=3 经验设置足以覆盖典型交互物体数量（OpenPVSG 中主体通常与 ≤2 个物体交互）。

### Semantic Classification Head (SCH)

弥补几何输出（掩码）与结构化场景图之间的语义鸿沟：

1. 在掩码区域内空间聚合 SAM2 encoder 视觉特征
2. MLP 分别预测主体类标签 sᵢ 和物体类标签 oᵢⱼ
3. 拼接 SAM2 Mask Decoder 中主体和物体的 obj_ptr query token，通过独立 MLP 预测关系谓词 rᵢⱼ

### Training Objective

多任务组合损失：

**L_total = L_mask + L_L2 + L_sub + L_obj + L_rel**

- L_mask = L_BCE + L_IoU + L_Dice（掩码损失，含主体和发现物体）
- L_L2 = ∥p̂ − p*∥²₂（DIDM 预测点定位损失）
- L_sub / L_obj / L_rel：交叉熵分类损失
- Hungarian Matching（DETR 风格）对齐预测与 GT 交互集

### 其他设计细节

- **距离加权 GT 点采样**：对物体掩码做距离变换，按距边界距离分配采样概率，避免边界模糊点作为 DIDM 训练目标
- **训练**：AdamW，DIDM cosine annealing (5×10⁻⁵→1×10⁻⁵)，SCH lr=5×10⁻⁴，400 epochs，8-frame clips，1024×1024 分辨率
- **推理**：~10 FPS on A100 (40GB)，~7GB 内存占用

## Dataset: OpenPVSG

来自 Yang et al. [32] 的 OpenPVSG 基准：

- **规模**：400 视频，~150K 帧 (5 FPS)
- **来源**：VidOR (289) + EPIC-Kitchens (55) + Ego4D (56)，覆盖第三人称与第一人称视角
- **标注**：126 物体类别（panoptic masks）、57 关系谓词（空间/接触/交互类型）
- **特点**：丰富的视觉/时序多样性、细粒度语义空间、像素级全景标注

## Experiments & Results

### 评估指标

1. **Recall@K (R@K)**：全三元组正确性（标签匹配 + 掩码 IoU ≥ 0.5），top-K 排序
2. **Spatial Interaction Recall (SpIR)**：仅评估空间定位质量（IoU ≥ 0.5），忽略分类标签
3. **Prompt Localization Recall (PLR)**：DIDM 预测点是否落在 GT 物体掩码内

每次实验重复 25 次（不同随机采样初始点击点），报告均值 ± 标准差。

### 端到端性能（Table 2）

| Method | Recall@3 | Recall@20 |
|--------|----------|-----------|
| PVSG + IPS+T [32, 4, 29] | — | 3.88 |
| PVSG + VPS [32, 4, 15] | — | 0.42 |
| MACL [22] + IPS+T | — | 4.51 |
| MACL [22] + VPS | — | 0.84 |
| **Click2Graph (Ours)** | **2.23** | — |

> Click2Graph 每帧仅生成 N_q=3 个预测（而非~100），在交互约束设置下达到 R@3=**2.23**，与自动化全帧方法具有可比性。

### 不同提示类型的鲁棒性（Table 3）

| 数据集 | Prompt | R@3 | SpIR | PLR |
|--------|--------|-----|------|-----|
| EPIC-K. | Mask | 1.78 | 24.22 | 30.67 |
| | Point | 1.14±0.38 | 23.04±1.08 | 32.06±0.81 |
| | BBox | 2.08±0.06 | 25.02±0.09 | 31.96±0.09 |
| Ego4D | Mask | 0.73 | 17.22 | 38.37 |
| | Point | 0.56±0.04 | 16.21±1.04 | 39.87±0.38 |
| | BBox | 0.72±0.06 | 17.49±0.32 | 38.97±0.11 |
| VidOR | Mask | 3.33 | 18.77 | 30.82 |
| | Point | 2.72±0.25 | 15.37±0.55 | 28.86±0.34 |
| | BBox | 3.18±0.10 | 17.59±0.36 | 30.13±0.23 |

> 三种提示类型（点/框/掩码）均产生稳定结果，方差低，验证了系统对低精度用户交互的鲁棒性。

### DIDM 消融实验（Table 4）

| 数据集 | 策略 | R@3 | SpIR | PLR |
|--------|------|-----|------|-----|
| EPIC K. | Heuristic | 0.62 | 5.14 | 10.60 |
| | **DIDM (ours)** | **2.08** | **25.02** | **32.06** |
| Ego4D | Heuristic | 0.28 | 4.26 | 9.30 |
| | **DIDM (ours)** | **0.73** | **17.49** | **39.87** |
| VidOR | Heuristic | 0.62 | 4.66 | 10.19 |
| | **DIDM (ours)** | **3.33** | **18.77** | **30.82** |

> 替代 DIDM 为全局物体概率热力图启发式采样导致 PLR、SpIR 和 R@K 全部显著下降，验证了主体条件化提示生成对交互发现的关键性。

### 定性分析

- 正确案例：系统能恢复多个交互物体并生成连贯三元组（adult-box-holding, ball-grass-on）
- 时序鲁棒性：主体短暂遮挡或镜头移动后仍保持一致性预测
- 典型失败模式：谓词语义粒度混淆（on vs. sitting）、视觉相似物体混淆（gift vs. box, floor vs. ground）

### 关键发现

1. **PLR 最高**：DIDM 可靠生成在物体掩码内的提示点
2. **SpIR 次之**：SAM2 在 DIDM 引导下产生精确全景掩码
3. **R@K 最困难**：细粒度语义分类是主要瓶颈，区分视觉相似类别（child vs. baby, box vs. bag, floor vs. ground）以及 OpenPVSG 的长尾分布是主要错误来源

## Limitations & Future Work

**当前局限**：
- 用户实时干预局限于分割纠正，不能直接修改推理时的预测标签
- 标签修正尚未反馈到模型

**未来方向**：
- 集成轻量级反馈机制，用户标签修正动态更新可学习类别嵌入
- 集成语言模型增强谓词推理能力
- 多主体提示策略处理复杂多智能体交互
- 利用交互式监督改进长尾谓词学习

## References (Selected)

- SAM2: Ravi et al., "SAM 2: Segment Anything in Images and Videos," arXiv:2408.00714, 2024.
- OpenPVSG: Yang et al., "Panoptic Video Scene Graph Generation," CVPR 2023.
- PVSG: Yang et al., "Panoptic Video Scene Graph Generation," CVPR 2023.
- STTran: Cong et al., "Spatial-temporal transformer for dynamic scene graph generation," ICCV 2021.
- DDS: Iftekhar et al., "DDS: Decoupled dynamic scene-graph generation network," WACV 2025.
