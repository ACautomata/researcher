---
title: REACT++ — Efficient Cross-Attention for Real-Time Scene Graph Generation
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags: [real-time-sgg, decoupled-two-stage, cross-attention, yolo, efficient-inference]
paper:
  title: REACT++ — Efficient Cross-Attention for Real-Time Scene Graph Generation
  authors: [Maëlic Neau, Zoe Falomir]
  year: 2026
  venue: arXiv 2026
  arxiv: 2603.06386
  code: https://github.com/Maelic/SGG-Benchmark
classification:
  label: Real-Time Scene Graph Generation
  task: [Scene Graph Generation, Object Detection, Relation Prediction]
  method_family: Decoupled Two-Stage + Cross-Attention Prototype Learning
  modality: RGB Image
  datasets: [PSG, IndoorVG, VG150]
  metrics: [Recall@K, meanRecall@K, F1@K, mAP@50, Latency]
evidence_level: full-paper
raw_sources:
  - raw/sources/2026-01-01-REACT-Efficient-Cross-Attention-Real-Time-SGG.pdf
related_pages:
  - domains/scene-graph/papers/prototype-based-embedding-network-scene-graph-generation.md
  - domains/scene-graph/papers/reltr-relation-transformer-scene-graph-generation.md
---

# REACT++: Efficient Cross-Attention for Real-Time Scene Graph Generation

## Citation

Maëlic Neau, Zoe Falomir. "REACT++: Efficient Cross-Attention for Real-Time Scene Graph Generation." arXiv:2603.06386v1, Mar 2026.

## One-Sentence Contribution

REACT++ 在 Decoupled Two-Stage（DTS）框架下，通过 DAMP 高效特征提取、AIFI 全局上下文建模和 CARPE 非对称交叉注意力关系头，在 PSG 数据集上实现 **19.4ms** 推理延迟（含 DCS）的同时保持 mAP **53.1**，是首个在 PSG 上 F1@K 超过 **30**（YOLO12m 骨干）的实时 SGG 模型。

## Problem Setting

SGG 任务需同时优化 Object Detection（OD）精度、Relation Prediction（RelPred）精度和推理延迟三方面。现有方法往往侧重其中之一：

- Two-Stage 方法（Motifs、VCTree、PE-Net）使用 Faster-RCNN 骨干，OD 精度有限且延迟高（>100ms）
- One-Stage 方法（EGTR、RelTr）延迟较低，但 RelPred 和 OD 精度显著低于 Two-Stage
- 此前 REACT（BMVC 2025）通过 DTS + YOLO 实现了 2.7× 加速和 +58% mAP，但关系头存在三个瓶颈：
  1. ROI Align 特征提取慢且参数量大
  2. 未利用全局场景信息
  3. 原型空间中 subject/object 交互是对称的，无法编码关系方向性

## Method

REACT++ 在 REACT 的 Decoupled Two-Stage（DTS）架构上引入三个新组件：

### 1. DAMP — Detection-Anchored Multi-Scale Pooling

**动机**：替代 ROI Align 的慢速特征提取。YOLO 的 one-stage 检测头在特定特征图上解码 bounding box 和类别；ROI Align 需在多个尺度重新采样，带来额外延迟。

**做法**：
- DA（Detector-Anchored）：直接根据 YOLO 检测峰值索引 ιᵢ 在特征图上 gather 单向量——几乎零开销
- DAP（DA with Pooling）：在 DA 基础上对 Gaussian 权重邻域（r=1，9 个特征）做池化
- DAM（DA with Multi-Scale）：将索引对齐到其他 FPN 层（P3+P4+P5），每对象提取 3 个向量
- **DAMP**（完整版）：DAM + Gaussian 邻域池化

**优势**：平均延迟降低 **9.3ms（32%）**；F1@K 从 ROI Align 的 8.0 提升至 **23.8**（IndoorVG，10 epoch）。

### 2. AIFI — Attention-based Intra-scale Feature Interaction

**动机**：全局场景上下文（如"厨房"、"海滩"）有助于推断上下文相关的谓词（如 eating、drinking、swimming）。

**做法**：受 RT-DETR 启发，引入轻量级 AIFI block，从 YOLO backbone 顶端特征图（P5）提取紧凑的场景表征，通过 cross-attention 补充 subject/object 表示。

**效果**：+0.42 F1@K（1.8%），但增加 **2.82ms** 延迟和 **1.97M** 参数。

### 3. CARPE — Cross-Attention Rotary Prototype Embedding

REACT++ 的核心创新，包含四个改进：

1. **SwiGLU MLP**：替换 REACT 中的三组独立线性投影（ReLU + LayerNorm），共享 subject/object 权重，参数减半
2. **Visual-Semantic Fusion via Cross-Attention**：替换 REACT 的双门控标量融合。Query=视觉特征，Key/Value=完整谓词原型库 {cᵒₖ}，模型根据关系选择融合哪些语义原型
3. **Geometry RoPE**：替换 REACT 的 Conv 空间编码（256 通道）。9 维规范化 box encoding → 两个两层网络 f₁、f₂ → sin/cos 编码 → 每 head 一个标量 → 加到 attention logits。编码空间偏置同时节省参数
4. **EMA Prototype Bank**：为谓词原型维护指数移动平均（EMA）影子缓冲区（m=0.999）。对罕见类，EMA 原型替代梯度更新权重，缓解梯度消失

### 4. DCS — Dynamic Candidate Selection（推理优化）

在推理时动态选择最优 proposal 数量。训练时最多 θ=100 个 proposals，推理时从 0 均匀采样，选择梯度 |f'(x)| < ε 的最小 x。REACT++ + DCS 在 PSG 上以 47 个 proposals 达到 F1@K=23.89（接近 100 proposals 的 23.85），延迟从 25.9ms 降至 **19.4ms**（-25%）。

### 架构总览

```
YOLOV8m → DAMP (特征提取) → AIFI (全局上下文) → CARPE (关系头) → DCS (推理裁剪)
  ↑—— 两个阶段解耦，YOLO 仅用于 OD 和特征提取，关系头独立训练 ——→
```

## Experiments

### 数据集

| 数据集 | 图像数 | 对象类 | 谓词类 | 特点 |
|--------|--------|--------|--------|------|
| PSG | ~49K | 80（panoptic） | 56 | 高质量全景标注，无模糊类 |
| IndoorVG | ~6K | 80 | 56 | 室内场景，高质量标注 |
| VG150 | ~108K | 150 | 50 | 经典基准，但有噪声和模糊类 |

### Baselines

- **Two-Stage (Faster-RCNN)**：Neural-Motifs [13]、VCTree [14]、Transformer [27]、GPS-Net [26]、PE-NET [15]
- **Decoupled Two-Stage (YOLO)**：REACT [19]、PE-NET-DTS、GPS-NET-DTS、Motifs-DTS、VCTree-DTS、Transformer-DTS
- **One-Stage**：RelTR [17]、EGTR [18]、SGTR [16]

### 训练设置

- **YOLOV8m OD**：100 epoch, batch size 16, image size 640×640
- **关系头**：20 epoch, batch size 8, SGD optimizer (REACT++) / AdamW (REACT), lr=1e-4, CosineAnnealing scheduler, gradient accumulation 4
- **硬件**：Intel i9-11950H @ 2.60GHz × 16, NVIDIA RTX 3080 Laptop 16GB VRAM
- **延迟基准**：batch size 1, 200 validation images, 20 warmup steps

### 评估协议

- Recall@K（R@K）和 meanRecall@K（mR@K），K=[20,50,100]
- F1@K = 2×R@K×mR@K/(R@K+mR@K) —— head/tail 预测的综合指标
- mAP@50 用于 OD 精度评估

## Results

### PSG 数据集（Table 2，关键行）

| 方法 | 骨干 | mR@20/50/100 | R@20/50/100 | F1@K | mAP50 | Lat. (ms) | Params |
|------|------|:---:|:---:|:---:|:---:|:---:|:---:|
| **REACT++ (DCS)** † | YOLOV8m | 22.2/24.9/27.1 | 29.1/34.2/37.5 | **28.4** | **53.1** | **19.4** | **35.8M** |
| **REACT++** | YOLOV8m | 22.2/24.9/27.1 | 29.1/34.2/37.5 | 28.4 | 53.1 | 25.9 | 35.8M |
| REACT [19] | YOLOV8m | 18.3/20.1/20.9 | 27.6/30.9/32.3 | 23.9 | 53.1 | 32.5 | 43.3M |
| PE-NET [15] | ResNeXt-101 | 10.7/11.7/12.0 | 16.8/18.7/19.5 | 14.1 | 35.5 | 390.4 | 426.5M |
| EGTR [18] | DETR | 12.0/14.5/16.6 | 24.9/30.3/33.8 | 19.4 | 33.6 | 78.3 | 42.5M |

† DCS: Dynamic Candidate Selection，推理时动态裁剪 proposals

**关键结论**：
- REACT++ vs REACT：mR@K 提升 **+20%**（20.8→24.9 avg），R@K 提升 **+17.9%**（30.3→37.5），延迟降低 **-20%**（32.5→25.9ms），参数量减少 **-17%**（43.3M→35.8M）
- DCS 进一步将延迟降至 **19.4ms**——首个低于 20ms 的 SGG 模型
- DTS 贡献：mAP +54.37% vs TS (Faster-RCNN)；mAP +120% vs OS (EGTR/RelTR)

### IndoorVG 数据集（Table 3a）

| 方法 | mR@K | R@K | F1@K | mAP50 |
|------|:---:|:---:|:---:|:---:|
| **REACT++** (DTS) | **20.7** | 28.1 | **23.9** | **37.2** |
| REACT (DTS) | 18.0 | **30.9** | 22.8 | 37.2 |
| PE-NET (DTS) | 16.0 | 29.4 | 20.7 | 37.2 |
| PE-NET (TS) | 13.8 | 27.1 | 18.1 | 25.2 |
| EGTR (OS) | 7.1 | 10.6 | 8.5 | 14.7 |

**关键结论**：DTS 带来的 mAP 改善 +43.4%，F1@K +38.76%（对比同模型的非 DTS 版本）。REACT++ 与 REACT 在 mAP 上持平（37.2），但 mR@K 显著提升（20.7 vs 18.0，+15%）。

### VG150 数据集（Table 3b）

| 方法 | mR@K | R@K | F1@K | mAP50 |
|------|:---:|:---:|:---:|:---:|
| **REACT++** (DTS) | 13.2 | 28.9 | 18.2 | **31.8** |
| REACT (DTS) | 12.9 | 27.4 | 17.6 | 31.8 |
| SQUAT [51] | **15.3** | 26.7 | **19.4** | - |
| PE-NET (TS) | 13.3 | 32.6 | 18.9 | 29.2 |

**关键结论**：VG150 上 REACT++ 提升有限，原因是 VG150 的边界框标注噪声和模糊类（如 people/men）混淆了 YOLO 检测器。REACT++ 参数少因此对噪声更敏感。

### 缩放性实验（Table C3：YOLO12 变体）

| 模型 | mR@20/50/100 | R@20/50/100 | F1@K | mAP50 | Lat. (ms) | Params |
|------|:---:|:---:|:---:|:---:|:---:|:---:|
| YOLOV8m | 22.2/24.9/27.0 | 29.1/34.2/37.5 | 28.5 | 51.1 | 25.9 | 35.9M |
| YOLO12m | **23.5/26.4/28.3** | **30.9/36.1/39.3** | **30.0** | 53.5 | 28.0 | 30.3M |
| YOLO12l | 23.6/26.1/27.9 | 29.5/34.9/37.8 | 29.4 | **56.6** | 33.3 | 36.5M |

**关键结论**：YOLO12m + REACT++ 是首个在 PSG 上 F1@K 突破 30 的模型。YOLO12 的 Area Attention 机制改善了特征表示，有助于细粒度谓词区分。

### 消融实验

**DAMP vs. ROI Align**（IndoorVG，10 epoch）：

| 提取器 | mR@K | R@K | F1@K | Lat. (ms) |
|--------|:---:|:---:|:---:|:---:|
| ROI Align（基线） | 4.9 | 21.1 | 8.0 | 29.2 |
| DA（直接索引） | 18.2 | 27.4 | 21.9 | 19.5 |
| DAP（+ Gaussian 邻域） | 19.4 | 27.9 | 22.9 | 19.6 |
| DAM（+ 多尺度） | 19.1 | 27.0 | 22.4 | 19.6 |
| **DAMP**（完整） | **20.7** | **28.1** | **23.8** | 20.8 |

- 延迟差距：**9.3ms（32%）**；F1@K 提升从 8.0→23.8（+197%）

**AIFI 全局上下文**（Table 4）：

| 方法 | R@K | mR@K | F1@K | ΔF1 | Params | Lat. |
|------|:---:|:---:|:---:|:---:|:---:|:---:|
| 有 AIFI | 28.13 | 20.70 | 23.85 | - | 9.82M | 20.76ms |
| 无 AIFI | 27.84 | 20.23 | 23.43 | -0.42 | 7.85M | 17.94ms |

AIFI 带来 +0.42 F1@K（+1.8%），主要在 tail 类（mR@K +0.47）。

**DCS 策略**：最优 proposals 数 **47**，F1@K=23.89（接近 100 proposals 的 23.85），延迟降幅约 **25.9→19.4ms**。

## Limitations

1. **VG150 噪声敏感**：相比 REACT，REACT++ 参数量更少，对标注噪声更敏感。在 VG150 上未超越近期 TS 方法（SQUAT、PE-NET）
2. **AIFI 带来延迟开销**：全局上下文虽提升 tail 性能，但增加约 2.8ms 延迟（+16%），对极低延迟场景有影响
3. **YOLO 骨干依赖**：DAMP 算法依赖于 YOLO 的 detection-peak 索引设计，不可直接迁移至 Faster-RCNN 等非 one-stage 检测器
4. **仅限 RGB**：未探索多模态（RGB-D、点云）或视频序列场景
5. **无去偏策略**：评估时未使用 re-weighting 或 causal intervention 等去偏方法，谓词长尾问题仍存在

## Reusable Claims

1. **ROI Align 是 Two-Stage SGG 的性能瓶颈**：替换为直接索引池化（DAMP）后延迟降低 32%、F1@K 从 8.0 提升至 23.8
2. **Decoupled Two-Stage（DTS）是实时 SGG 的有效范式**：YOLO 做 OD + 独立关系头，在 PSG 上 mAP 达 53.1（+120% vs OS 方法）
3. **非对称 cross-attention 优于对称 prototype 学习**：CARPE 中 subject/object 各自对应的 cross-attention 层正确建模了关系的方向性，mR@K 提升 20%
4. **几何 RoPE 可替代繁重的 Conv 空间编码**：无额外 Conv block 开销，节省参数的同时提供空间偏置
5. **推理时动态裁剪 proposals（DCS）几乎无损**：从 100 降为 47 个 proposals 时 F1@K 仅降 0.04（0.16%），延迟降低 25%

## Connections

- **REACT [19]**（BMVC 2025）：REACT++ 的直接前身，首次提出 DTS + YOLO 范式。REACT++ 在 REACT 基础上改进关系头，速度 +20%、精度 +10%、参数 -17%
- **PE-NET [15]**（CVPR 2023）：SGG 中 prototype learning 的代表工作。REACT++ 对其分析发现 ROI Align、对称原型和重复分类等瓶颈
- **RT-DETR [20]**：AIFI 模块受 RT-DETR 的 encoder 架构启发，用于高效的全局上下文提取
- **EGTR [18]**（CVPR 2024）：最佳 One-Stage SGG。REACT++ 在 mAP 上超过 EGTR 58%（53.1 vs 33.6），但这是 DTS 框架的贡献而非特定关系头

## Open Questions

1. REACT++ 在 VG150 上未超越 SQUAT，说明噪声标注下的鲁棒性仍待提升——能否引入去偏/去噪策略？
2. DCS 的最优 proposal 数是否跨数据集稳定？论文仅在 IndoorVG/PSG 上验证，未测试 VG150
3. YOLO 骨干更换为更大/更新的版本（如 YOLOv12m）后 F1@K 超过 30——更大规模的骨干是否会继续提升 RelPred 精度直至饱和？
4. REACT++ 的 CARPE 关系头是否可迁移至其他检测器（如 DETR-family）做实时 SGG？

## Provenance

- **PDF 来源**：arXiv:2603.06386v1, 6 Mar 2026
- **提取方式**：pymupdf 全文提取，63,709 chars, 26 pages
- **证据等级**：full-paper —— 全文精读，方法细节（4.1-4.4）、实验（5.1-5.4）、消融（6.1-6.4）、附录全部覆盖
- **关键表格和数字已捕获**：Table 2, 3, 4, B2, C3；所有 main metric 和消融差异均有记录
