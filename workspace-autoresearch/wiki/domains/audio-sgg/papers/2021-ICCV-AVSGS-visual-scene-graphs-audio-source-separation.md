---
title: "Visual Scene Graphs for Audio Source Separation"
type: paper
domain: audio-sgg
status: active
created: 2026-06-10
updated: 2026-06-10
tags:
  - audio-sgg
  - ICCV-2021
  - audio-visual-source-separation
  - scene-graph
  - self-supervised
raw_sources:
  - raw/sources/2021-ICCV-Visual-Scene-Graphs-for-Audio-Source-Separation.pdf
  - raw/sources/2021-ICCV-Visual-Scene-Graphs-for-Audio-Source-Separation.txt
paper:
  title: "Visual Scene Graphs for Audio Source Separation"
  authors:
    - Moitreya Chatterjee
    - Jonathan Le Roux
    - Narendra Ahuja
    - Anoop Cherian
  year: 2021
  venue: ICCV 2021
  arxiv: https://arxiv.org/abs/2109.02227
  code: null
  project: null
classification:
  label: Audio Visual Scene Graph Segmenter (AVSGS)
  task:
    - Visually-guided Audio Source Separation
  method_family: Scene-Graph-Conditioned U-Net Source Separation
  modality: Audio-Visual (Video + Audio)
  datasets:
    - MUSIC
    - ASIW (Audio Separation in the Wild)
  metrics:
    - SDR (Signal-to-Distortion Ratio) [dB]
    - SIR (Signal-to-Interference Ratio) [dB]
    - SAR (Signal-to-Artifact Ratio) [dB]
evidence_level: full-paper
---

## Citation

Chatterjee, M., Le Roux, J., Ahuja, N., Cherian, A. "Visual Scene Graphs for Audio Source Separation." ICCV, 2021. University of Illinois at Urbana-Champaign & Mitsubishi Electric Research Laboratories (MERL).

## One-Sentence Contribution

首次将场景图表示用于视觉引导的音频源分离任务，提出 AVSGS 模型，通过自回归生成互正交的视觉子图嵌入来条件化 U-Net 音频分离器，实现了基于场景上下文的音源分离，并提出了自然场景音源分离数据集 ASIW。

## Problem Setting

- **目标**：给定一段视频及对应的混合音频信号 x(t) = Σᵢ sᵢ(t)，使用视频中的视觉信息将混合音频解耦为各个音源 sᵢ(t)
- **挑战**：
  - 视觉嵌入与音频对应关系是一对多的，同一物体可能产生多种不同声音（如手机铃响 vs 手机落地）
  - 自然场景中的声音常来自于物体间的复杂交互（如人在冲马桶），而非单个物体的特征声音
  - 需要算法可扩展至新的声音类型及其视觉关联，不依赖人工标注的对应关系
  - 已有的方法（如 Sound of Pixels、Co-Separation）局限于音乐乐器等具有特征声音的物体，或仅使用单物体视觉编码，缺乏场景上下文建模
- **设定**：自监督学习范式，通过 mix-and-separate 策略构造训练数据，不需要单独的 ground-truth 音源信号

## Method

### AVSGS 模型架构

AVSGS 由以下组件构成：

1. **Object Detector**：使用 Faster-RCNN（Visual Genome 1600 类 + Open Images 乐器检测）提取视频关键帧中的物体检测结果（类别、边界框、特征向量、置信度）

2. **Visual Scene Graph Construction**：
   - 对每个视频，从标注（标题/类别标签）中识别 principal objects（声源主体）
   - 对每个 principal object pᵢ，选取最置信的关键帧；在该帧中，选择与 pᵢ 边界框 IoU > γ 的物体作为 context nodes
   - 顶点集 V = ∪ᵢ(pᵢ ∪ Vpᵢ)，在 V 上建立全连接图（边集 E = V × V）
   - 节点特征使用 FRCNN 提取的 2048 维特征向量
   - 由于涉及多帧的多种物体，构建的图是时空性的

3. **Visual Embedding of Sounding Interactions**：
   - 多头图注意力网络（GATConv）对节点进行注意力加权
   - 边卷积网络（EdgeConv）捕捉节点间的交互特征
   - 全局最大池化 + 平均池化拼接得到整图嵌入 ζ
   - GRU 自回归生成 N+1 个（N 个源 + 1 个背景）互正交子图嵌入 yᵢ

4. **Mutual Orthogonality Regularization**：
   - 损失函数 ℒ_ortho = Σ_{i≠j} (yᵢᵀ yⱼ)²
   - 强制不同子图嵌入相互正交，避免 GRU 重复生成相同嵌入

5. **Audio Separator Network (ASN)**：
   - U-Net 风格编码器-解码器架构
   - 子图嵌入 yᵢ 经复制匹配空间分辨率后，在 bottleneck 层与音频特征拼接
   - 输出时频掩码 ˆMᵢ ∈ [0,1]^{Ω×T}，与混合频谱 X 逐元素相乘得到分离音源谱 ˆSᵢ
   - iSTFT 恢复时域信号

### 训练策略

- **Mix-and-Separate**：混合两个视频的音频构造训练样本 x_m(t) = x₁(t) + x₂(t)
- **Consistency Loss (ℒ_cons)**：对分离音频进行分类，使用排列不变训练（PIT）匹配分离结果与 principal object 类别标签
- **Co-separation Loss (ℒ_co-sep)**：确保所有分离掩码之和接近理想二值掩码（IBM），鼓励完整恢复
- **总损失**：ℒ = λ₁ℒ_cons + λ₂ℒ_co-sep + λ₃ℒ_ortho，λ₁=1, λ₂=0.05, λ₃=1

## Experiments

### 数据集

| 数据集 | 类型 | 训练 | 验证 | 测试 | 特点 |
|--------|------|------|------|------|------|
| MUSIC | 音乐乐器演奏 | 6,300 clips | 132 | 158 | 11 种乐器，独奏与二重奏 |
| ASIW | 自然场景音频（来源于 AudioCaps） | 10,540 | 147 | 322 | 14 类 principal objects，306 个听觉词，非音乐自然声音 |

ASIW 数据集的 principal objects 类别：Baby, Bell, Birds, Camera, Clock, Dogs, Toilet, Horse, Man/Woman, Sheep/Goat, Telephone, Trains, Vehicle/Car/Truck, Water + background。

### 基线方法

- **Sound of Pixel (SofP)** [ECCV 2018]：早期基于深度学习的视觉引导音源分离方法
- **Minus-Plus Net (MP Net)** [ICCV 2019]：递归移除最高能量音源
- **Co-Separation** [ICCV 2019]：引入物体级分离损失，但仅使用单物体视觉条件
- **Sound of Motion (SofM)** [ICCV 2019]：整合像素级运动轨迹与外观特征
- **Music Gesture (MG)** [CVPR 2020]：整合场景外观与人体姿态特征（仅用于 MUSIC）

### 评估指标

SDR（Signal-to-Distortion Ratio）、SIR（Signal-to-Interference Ratio）、SAR（Signal-to-Artifact Ratio），单位 dB，值越高越好。

### 实现细节

- **框架**：PyTorch
- **音频预处理**：11 kHz 采样率，STFT 窗口 1022，hop length 256，~6s 输入 → 512×256 频谱，log-frequency 采样 → 256×256
- **检测器**：FRCNN 特征 2048 维，最多 2 个 principal object/视频，最多 20 个 context nodes
- **IoU 阈值**：γ=0.1
- **图注意力头数**：4
- **嵌入维度**：512
- **GRU**：单层单向，512 隐藏维度
- **优化器**：Adam，weight decay 1e-4，β₁=0.9，β₂=0.999
- **学习率**：初始 1e-4，每 15,000 步衰减 0.1
- **FRCNN 权重冻结**：训练过程中不更新
- **硬件**：未明确说明

## Results

### 主要结果（Table 1）

| 方法 | MUSIC SDR↑ | MUSIC SIR↑ | MUSIC SAR↑ | ASIW SDR↑ | ASIW SIR↑ | ASIW SAR↑ |
|------|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|
| Sound of Pixel (SofP) | 6.1 | 10.9 | 10.6 | 6.2 | 8.1 | 10.6 |
| Minus-Plus Net (MP Net) | 7.0 | 14.4 | 10.2 | 3.0 | 7.7 | 9.4 |
| Sound of Motion (SofM) | 8.2 | 14.6 | 13.2 | 6.7 | 9.4 | 11.1 |
| Co-Separation | 7.4 | 13.8 | 10.6 | 6.6 | 12.9 | 12.6 |
| Music Gesture (MG) | 10.1 | 15.7 | 12.9 | - | - | - |
| **AVSGS (Ours)** | **11.4** | **17.3** | **13.5** | **8.8** | **14.1** | **13.0** |

**关键差距**：AVSGS 在 MUSIC 上 SDR 超过最强非姿态基线 SofM 达 **3.2 dB**，SIR 提升 **2.7 dB**；在 ASIW 上 SDR 超过 Co-Separation 达 **2.2 dB**，SIR 提升 **1.2 dB**。SDR 和 SIR 显著提升且不以 SAR 下降为代价（SAR 均最优或持平）。

### 消融实验（Table 3，ASIW 数据集）

| 变体 | SDR↑ | SIR↑ | SAR↑ | 消融含义 |
|------|:----:|:----:|:----:|---------|
| Full AVSGS | **8.8** | **14.1** | **13.0** | 基线 |
| - No Orthogonality (λ₃=0) | 7.4 | 13.3 | 11.6 | 移除正交性约束后 SDR -1.4 |
| - No Multi-label (λ₁=0) | 6.4 | 11.2 | 11.7 | 移除一致性损失后 SDR -2.4 |
| - No Co-sep (λ₂=0) | 1.1 | 1.3 | 13.8 | **移除共分离损失后严重退化**，SDR 骤降 7.7 |
| - N=3（3 principal objects） | 8.4 | 13.5 | 12.2 | 增加物体数影响不大 |
| - No Skip Connection | 2.8 | 4.6 | 11.3 | 移除 U-Net 跳跃连接后 SDR -6.0 |
| - No GATConv | 6.5 | 11.6 | 11.8 | 移除图注意力后 SDR -2.3 |
| - No EdgeConv | 6.2 | 10.1 | 13.2 | 移除边卷积后 SDR -2.6 |
| - No GRU | 6.5 | 12.3 | 10.6 | 移除自回归 GRU 后 SDR -2.3 |

**消融关键发现**：
- Co-separation loss 是最关键的损失项（去除后 SDR 从 8.8 跌至 1.1）
- 图结构组件（GATConv + EdgeConv）同等重要，各自贡献约 2-2.6 dB
- Skip connection 对 ASN 影响极大（去除后 SDR 跌至 2.8）
- GRU 自回归机制贡献约 2.3 dB
- 正交性约束贡献约 1.4 dB

### 上下文节点数量分析（Figure 4）

- 在测试时增加 context nodes 数量，性能单调提升
- 使用多帧构建时空图的性能优于单帧图
- 证明了场景上下文丰富度对分离性能的正面影响

### 定性结果（Figure 3）

- AVSGS 在 ASIW 和 MUSIC 上的分离频谱图质量均优于 Co-Separation 和 SofM
- AVSGS 能正确选择有意义的上下文区域/物体来引导音频分离

## Limitations

1. **Principal object 依赖注释/元数据**：场景图构建需要从视频元数据（标题/类别标签）中确定 principal objects，而非完全自动化检测
2. **物体检测器限制**：依赖 Faster-RCNN 在 Visual Genome 和 Open Images 上的检测结果，覆盖范围有限
3. **运动信息未显式建模**：没有显式编码运动信息（但通过多帧时空图隐式包含），作者表明未来工作将显式融入运动
4. **场景图全连接假设**：假设图是全连接的，虽然避免了边缘选择启发式，但可能包含噪声连接
5. **GPU 硬件未说明**：训练硬件和时间未报告，影响可复现性

## Reusable Claims

> **Claim 1**: 场景图表示（含物体及交互关系）作为视觉条件，优于仅使用单物体外观或全帧特征进行音频源分离。
> **Evidence**: 表 1 中 AVSGS（场景图条件）在 MUSIC/ASIW 上分别以 SDR 11.4/8.8 超越所有基线（单物体条件 Co-Separation 7.4/6.6，运动+外观 SofM 8.2/6.7）。
> **Scope**: MUSIC（音乐乐器）和 ASIW（自然声音）两个数据集。
> **Confidence**: high

> **Claim 2**: 互正交子图嵌入正则化是音频分离的有效约束，去除后 SDR 下降 1.4 dB。
> **Evidence**: 表 3 消融，移除正交损失后 SDR 从 8.8 降至 7.4。
> **Scope**: ASIW 数据集。
> **Confidence**: medium

> **Claim 3**: Co-separation loss 在自监督训练中最为关键，去除后模型几乎崩溃（SDR 8.8 → 1.1）。
> **Evidence**: 表 3 消融（λ₂=0）。
> **Scope**: ASIW 数据集，mix-and-separate 训练范式。
> **Confidence**: high

## Connections

- **场景图起源**：本文使用的场景图概念源于 [Johnson et al., CVPR 2015] Image Retrieval Using Scene Graphs，将其从静态图像检索扩展至音频-视觉联合任务
- **与 SGG 的关系**：本文不直接生成场景图（SGG），而是使用预定义的场景图结构（利用 FRCNN 检测和视频元数据）作为音频分离的条件表示
- **与 Co-Separation [Gao & Grauman, ICCV 2019]** 的关系：AVSGS 在 Co-Separation 的 mix-and-separate + consistency loss 框架基础上，增加了场景图（替代单物体）和 GRU 自回归子图生成
- **与 Sound of Motion [Zhao et al., ICCV 2019]** 的关系：SofM 使用多帧运动信息，AVSGS 通过时空图隐式包含帧间关联
- **与 ASIW / AudioCaps** 的关系：ASIW 基于 AudioCaps 构建，提供了比 MUSIC 更具挑战性的自然场景音源分离基准

## Open Questions

1. Principal object 检测能否完全自动化（无需视频元数据/标题）？
2. 显式融入运动信息（如 Optical Flow）能否进一步提升性能？
3. 时域音源分离架构（而非频谱掩码）是否更适合场景条件化？
4. 场景图结构能否反向用于音频事件分类或声音事件检测？
5. AVSGS 能否扩展到开放集场景（未知 principal objects）？

## Provenance

- **提取源**：raw/sources/2021-ICCV-Visual-Scene-Graphs-for-Audio-Source-Separation.txt（51,422 chars, 10 pages）
- **提取方法**：PyMuPDF (fitz) PDF→文本提取
- **分析状态**：full-paper — 全文精读，含方法细节、完整实验设置、消融实验、数值结果表
- **关键章节覆盖**：Abstract, 1-Introduction, 2-Related Works, 3-Proposed Method（含 3.1-3.3）, 4-Experiments（含 4.1-4.5）, 5-Conclusions, References
