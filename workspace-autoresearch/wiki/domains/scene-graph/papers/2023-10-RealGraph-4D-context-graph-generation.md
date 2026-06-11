---
title: "RealGraph: A Multiview Dataset for 4D Real-world Context Graph Generation"
type: paper
domain: scene-graph
status: active
created: 2026-06-10
updated: 2026-06-10
tags: [4d-scene-graph, dataset, ICCV-2023, multiview, context-graph]
paper:
  title: "RealGraph: A Multiview Dataset for 4D Real-world Context Graph Generation"
  authors: [Haozhe Lin, Zequn Chen, Jinzhi Zhang, Bing Bai, Yu Wang, Ruqi Huang, Lu Fang]
  year: 2023
  venue: ICCV 2023
  arxiv: null
  project: https://github.com/THU-luvision/RealGraph
raw_sources:
  - raw/sources/2023-10-RealGraph-4D-Context-Graph.pdf
  - raw/sources/2023-10-RealGraph-4D-Context-Graph.txt
classification:
  label: scene-graph-generation
  task: [4D Context Graph Generation, 3D Scene Graph Generation, 3D Object Detection, 3D Multi-Object Tracking]
  method_family: Multi-view 3D Volume-based Multi-stage Pipeline
  modality: [Multiview RGB Video, Camera Calibration]
  datasets: [RealGraph]
  metrics: [mAP, MOTA, MOTP, IDs, R@K, mR@K, CGR@K, mCGR@K]
evidence_level: full-paper
---

## Citation

Haozhe Lin, Zequn Chen, Jinzhi Zhang, Bing Bai, Yu Wang, Ruqi Huang, Lu Fang. "RealGraph: A Multiview Dataset for 4D Real-world Context Graph Generation." ICCV 2023.

## One-Sentence Contribution

提出了首个面向 4D 真实场景的 Context Graph Generation (CGG) 任务及配套的 RealGraph 多视角视频数据集，并给出多阶段基线方法 MCGNet。

## Problem Setting

**CGG (Context Graph Generation)** 任务定义：给定校准后的多视角同步视频（4D 输入），在 4D 时空空间中恢复场景中物体的语义信息（位置坐标、轨迹、语义关系），并以时空上下文图（spatio-temporal context graph）的形式输出。

Context Graph 包含：
1. 一组 3D 边界框 B = {B₁,...,Bₙ}，每框含 (x,y,z,l,w,h,θ)
2. 一组物体标签 O = {o₁,...,oₙ}
3. 一组全局跟踪 ID I = {i₁,...,iₙ}（跨视角、跨帧一致）
4. 一组关系三元组 R = {r₁,...,rₘ}，每个为 (head, tail, predicate)

**与 3D Scene Graph 的区别**：CGG 关注动态场景中的人类日常活动，增加了时空一致性约束（temporal consistency）。

## Method

### MCGNet (Multiview-based Context Graph Generation Network)

多阶段 pipeline，包含三个核心组件：

**1. 3D 检测模块**

- 使用预训练的 2D backbone + FPN 对每张多视角图像提取特征
- 通过相机标定进行 2D→3D 反投影，构建 3D 特征体积 (HV × WV × DV)
- **Feature Fusion (FF)** 网络：3 个下采样残差块（各 3 个 3D 卷积层）+ 3 个上采样块（转置 3D 卷积 + 3D 卷积），输出 3 级特征图
- 检测头预测类别分布 pₙ、centerness cₙ 和 3D 边界框 Bₙ
- 损失：focal loss (Lcls) + cross-entropy (Lcntr) + IoU loss (Lloc)

**2. 关系预测模块**

- 使用 3D ROI align 提取物体特征 E 和上下文特征 C
- BiLSTM 在物体 proposals 间传播上下文信息
- 边缘特征 fₙ,ₘ = (cₙ⊕cₘ) ⊙ êₙ∪ₘ（head 和 tail 的上下文组合 + 联合框的体积特征）
- Softmax 输出关系概率分布
- 不需要边界框重叠即可识别关系

**3. 3D 跟踪模块**

- Kalman filter 作为运动模型
- IoU 作为关联度量 + Hungarian 算法匹配
- **Double Association (DA)**：两阈值策略（thr₁=0.25, thr₂=0.05），先用高阈值做标准关联，再用低阈值匹配未关联的检测结果，但不用低分框更新运动状态

## Dataset: RealGraph

### 数据采集

- 13 个动态场景（含人类活动）
- 每场景 8–15 台 GoPro Hero 10 相机，固定位置
- 分辨率 5312×2988，帧率 30 FPS，水平 FOV 87°
- 时长 3–20 分钟，总计 >2.4M 视频帧
- 相机同步在后期处理中手动完成

### 标注

- 语义标签标注频率为 1 FPS
- 总计：2.3M 2D 边界框、760K 2D 关系、420K 3D 边界框、130K 3D 关系
- 37 个物体类别、18 个关系类别（包括 "on", "stand on", "sit on", "use", "hold", "read", "drag", "drink", "eat", "in", "lie on", "ride", "hug" 等）
- 每个物体有跨视角和跨帧一致的全局 ID
- 关系标注限于物理接触（supportive 如 "on"、"in"，以及 human-object 动作如 "hold"、"drag"、"read"、"ride"）

### 与现有数据集对比

| 特性 | RealGraph | 3DSG | 3DSSG | KITTI | Waymo | nuScenes | HOI4D | LEMMA | BEHAVE |
|------|-----------|------|-------|-------|-------|----------|-------|-------|--------|
| 视频 | ✓ | ✗ | ✗ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 多视角 | 8–15 | ✗ | ✗ | 4 | 5 | 6 | 1 | 4 | 4 |
| 帧数 | 2.4M | - | - | 15K | 230K | 40K | 2.4M | 4.6M | 15.2K |
| 物体类别 | 37 | 80 | 187 | 8 | 4 | 23 | 16 | 14 | 20 |
| 关系类别 | 18 | 7 | 40 | - | - | - | 54 | 16 | 1 |
| 相机标定 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ |

## Experiments

### 任务与指标

- **3D Detection**: AP@0.25, mAP（IoU≥25% 为 TP）
- **3D MOT**: MOTA↑, MOTP↓(cm), IDs↓, FP↓, FN↓
- **3D SGG**: R@K, mR@K（K=20,50,100），评估三种子任务：SGDet、SGCls、PredCls；含 With/Without Constraint 两种评估方式
- **CGG**: CGR@K, mCGR@K（新增指标，CGR = 1 − (IDs + FN) / (TP + FN)，引入 ID switches 惩罚以评估时间一致性）

### 数据划分

- 13 场景：10 训练 + 3 测试（按场景划分）

### 训练设置

- **3D Det**: 空间范围 (8×8×2.4)m，体素大小 0.08m；ResNet-50 backbone；C₁=256, C₂=128；Adam 优化器 lr=2×10⁻⁴, wd=10⁻⁴；14 epochs，lr 在第 6、8 epoch 降 10 倍；NMS IoU=25%
- **3D SGG**: 使用检测模型生成的特征体积和 GT 边界框训练；边缘特征尺寸 7×7×7×128；SGD 优化器 lr=8×10⁻⁴，2 epochs 后降 10 倍
- **硬件**: 8× NVIDIA 3090 GPUs
- **跟踪**: thr₁=0.25, thr₂=0.05；最小 3D IoU 0.25 算匹配

### 消融实验

- Feature Fusion (FF) — 多尺度 3D 特征融合模块
- Double Association (DA) — 两阈值跟踪关联策略
- Half vs Full views — 使用一半 vs 全部相机视角

## Results

### 3D Detection (AP@0.25, mAP)

| FF | #views | chair | table | person | laptop | cup | box | whiteboard | mAP |
|:--:|:------:|:-----:|:-----:|:------:|:------:|:---:|:---:|:----------:|:---:|
| ✗ | half | 43.96 | 12.27 | 23.36 | 58.93 | 0.85 | 12.32 | 12.07 | 18.70 |
| ✓ | half | 53.38 | 20.32 | 38.57 | 64.49 | 2.10 | 16.28 | 19.52 | 23.33 |
| ✗ | full | 71.52 | 32.77 | 61.19 | 80.98 | 5.04 | 19.73 | 38.26 | 34.96 |
| ✓ | full | 75.14 | 33.70 | 68.44 | 80.29 | 7.16 | 22.49 | 43.29 | **38.29** |

FF 贡献 mAP +3.3 提升，尤其对小物体（cup +2.12, box +2.76）。Half views 性能显著下降，说明充分的相机覆盖对 CGG 至关重要。

### 3D MOT

| FF | DA | MOTA↑ | MOTP↓ | IDs↓ | FP↓ | FN↓ |
|:--:|:--:|:-----:|:-----:|:----:|:---:|:---:|
| ✗ | ✗ | 35.16 | 18.12 | 3379 | 8603 | 13246 |
| ✓ | ✗ | 37.06 | 16.60 | 2658 | 6859 | 9933 |
| ✗ | ✓ | 35.20 | 18.08 | 1921 | 8096 | 11853 |
| ✓ | ✓ | **37.17** | **16.54** | **1658** | 6269 | **8773** |

FF 提升检测质量，DA 降低 ID switches（1921→1658 with FF）。

### 3D SGG (No Constraint)

| Task | FF | R@20 | R@50 | R@100 | mR@20 | mR@50 | mR@100 |
|:----:|:--:|:----:|:----:|:-----:|:-----:|:-----:|:------:|
| SGDet | ✗ | 30.6 | 32.8 | 33.5 | 18.0 | 21.6 | 22.9 |
| SGDet | ✓ | 32.4 | 33.6 | 34.2 | 21.7 | 23.5 | 25.7 |
| SGCls | ✗ | 38.0 | 40.1 | 41.4 | 25.7 | 31.4 | 33.2 |
| SGCls | ✓ | 38.6 | 40.5 | 41.4 | 28.2 | 31.7 | 33.3 |
| PredCls | ✓ | 66.7 | 69.4 | 71.6 | 39.2 | 41.5 | 43.0 |

FF 在 SGDet 子任务上贡献 mR@20/50/100 分别提升 1.2/1.8/0.8。

### CGG (No Constraint)

| FF | DA | CGR@20 | CGR@50 | CGR@100 | mCGR@20 | mCGR@50 | mCGR@100 |
|:--:|:--:|:------:|:------:|:-------:|:-------:|:-------:|:--------:|
| ✗ | ✗ | 29.1 | 31.3 | 32.0 | 16.5 | 20.1 | 21.4 |
| ✓ | ✗ | 31.3 | 32.5 | 33.1 | 20.6 | 22.4 | 24.6 |
| ✗ | ✓ | 29.8 | 32.0 | 32.7 | 17.2 | 20.8 | 22.1 |
| ✓ | ✓ | **31.8** | **33.0** | **33.6** | **21.1** | **22.9** | **25.0** |

DA 平均提升 CGR 约 0.5，主要通过降低 ID switches 实现。

## Limitations

- MCGNet 为多阶段 pipeline，误差在各阶段累积，缺乏联合优化机制
- 关系预测仅考虑物体对的直接上下文，未利用时间一致性对关系进行约束（论文在 conclusion 中提出这是未来方向）
- 仅提供 1 FPS 的语义标注（原始视频 30 FPS），限制了时间粒度的分析
- 关系类别较少（18 类），且局限于物理接触类关系（supportive/containing + 动作），缺乏视角相关的空间关系（如 "in front of"、"near"）
- 数据集仅 13 个场景，规模和场景多样性有限

## Reusable Claims

> **Claim**: 多视角 3D 特征体积方法适用于 4D 场景理解，但多阶段 pipeline 的误差累积是主要瓶颈（mAP 38.29 → CGG mCGR@100 仅 25.0）
> **Evidence**: 论文 Table 2 & 5，3D Det mAP 38.29 但 CGG mCGR@100 仅 25.0（no constraint）
> **Scope**: RealGraph 数据集，MCGNet 基线方法
> **Confidence**: high

> **Claim**: 多尺度特征融合 (FF) 对多视角动态场景中的小物体检测至关重要（cup AP 从 5.04→7.16, box AP 从 19.73→22.49）
> **Evidence**: Table 2
> **Scope**: RealGraph，3D volume-based 检测
> **Confidence**: high

> **Claim**: Double Association 策略能有效降低跟踪中的 ID switches（1658 vs 3379, −51%），但对 MOTA 提升有限（37.17 vs 35.16, +2.01）
> **Evidence**: Table 3
> **Scope**: RealGraph 上的 3D MOT
> **Confidence**: high

> **Claim**: 充分且合理布局的相机覆盖是 CGG 任务成功的关键（full views mAP 38.29 vs half views mAP 23.33, −39%）
> **Evidence**: Table 2
> **Scope**: RealGraph 数据集评估
> **Confidence**: high

## Connections

- 与 STTran / TRACE / MViTv2 等视频场景图方法同属动态场景理解方向，但 RealGraph 独特地使用多视角（非单视角）视频
- 与 [[2022-CVPR-dynamic-scene-graph-anticipatory-pre-training.md]] 的区别在于后者关注未来帧预测，RealGraph 关注 4D 几何+语义的联合恢复
- 与 [[4d-panoptic-scene-graph-generation.md]] 同属 4D 场景图生成方向，但 RealGraph 使用多视角 RGB 视频而非 LiDAR + RGB-D
- 经典 3D SGG 数据集如 3DSG、3DSSG 仅提供静态场景，RealGraph 扩展到了动态场景
- 与 STCrowd、HOI4D、LEMMA、BEHAVE 等人类活动数据集的区别在于 RealGraph 提供多视角校准和 3D 语义关系

## Open Questions

- CGG 任务能否通过端到端的联合优化（而非多阶段 pipeline）取得显著提升？
- 关系预测的时间一致性约束（如关系在时间上的平滑性）能否进一步提高 CGR？
- 更广泛的关系类别（包含视角依赖的空间关系）是否会改变 CGG 任务的难度？
- RealGraph 数据集较小（13 场景），更大规模的多视角 4D 场景图数据集是否必要？

## Provenance

- PDF 来源: IEEE Xplore / CVF Open Access
- 提取方式: PyMuPDF 全文提取
- 验证: 11 页全文，包含摘要、引言、相关工���、方法、实验、结论、引用
- 提取日期: 2026-06-10
