---
title: QPredSGG: Hybrid Quantum Predicate Learning for Long-Tailed Scene Graph Generation
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags: [scene-graph, quantum-ml, hybrid-quantum, long-tail, predicate-classification]
paper:
  title: QPredSGG: Hybrid Quantum Predicate Learning for Long-Tailed Scene Graph Generation
  authors:
    - Prerana Ramkumar
    - Nouhaila Innan
    - Muhammad Shafique
  year: 2026
  venue: arXiv (quant-ph)
  arxiv: 2606.04689v1
  project: https://github.com/preranarramkumar/QPredSGG_Public
classification:
  label: Hybrid Quantum Predicate Classifier for SGG
  task:
    - Scene Graph Generation (PredCls)
  method_family:
    - Hybrid Quantum-Classical Neural Network
    - Parameterized Quantum Circuit (PQC)
  modality: Image
  datasets:
    - Visual Genome (VG-150, 151 obj / 51 rel classes)
  metrics:
    - R@50, R@100
    - mR@50, mR@100
    - Expressibility (KL divergence from Haar)
    - Von Neumann Entropy
evidence_level: full-paper
raw_sources:
  - ../../../sources/scene-graph/2026-06-09-qpredsgg-hybrid-quantum-predicate-learning-sgg.pdf
  - ../../../sources/scene-graph/2026-06-09-qpredsgg-hybrid-quantum-predicate-learning-sgg.txt
---

## Citation

Prerana Ramkumar, Nouhaila Innan, Muhammad Shafique. "QPredSGG: Hybrid Quantum Predicate Learning for Long-Tailed Scene Graph Generation." arXiv:2606.04689v1, June 2026.

## One-Sentence Contribution

首次将混合量子-经典架构引入场景图生成（SGG）谓词分类，用量子谓词头（QP-Head）替代 CFEN 中的经典 MLP 谓词头，在仅使用 96 个可训练量子参数的情况下实现 mR@100 57.25%（vs CFEN 基线 41.1%）。

## Problem Setting

场景图生成中的谓词分类面临严重的长尾分布问题：Visual Genome 数据集中少量高频谓词（如"on"、"of"、"in"）占绝大多数标注，而细粒度语义谓词出现极少。现有 SGG 方法依赖大参数量的经典决策模块进行分类。本文探索的核心问题：**能否用一个紧凑的 NISQ 量子电路作为谓词决策模块，在极强维度压缩下维持甚至提升长尾关系识别？**

关键设置：
- **任务**：Predicate Classification (PredCls) — 给定 ground-truth 物体标签和 bbox，预测三元组谓词
- **数据集**：Visual Genome VG-150（151 物体类别、51 谓词类别，含背景类）
- **主干**：CFEN（Causal Features Enhancement Network），基于 BiTreeLSTM 提取 4096 维 pair embedding
- **比较基线**：经典 CFEN MLP 谓词头（2048 维）、Motifs、VCTree-TDE

## Method

### 整体架构

四阶段实验管线（Fig. 2）：
1. 建立 VG-150 数据集和 CFEN 经典基线
2. 用 QP-Head 替换经典谓词头，定义架构搜索空间
3. 使用 Weighted Cross-Entropy (WCE) 训练
4. 在语义指标、量子质量、计算开销三个维度比较

### QP-Head 架构

```
CFEN Backbone → BiTreeLSTM → hij ∈ ℝ⁴⁰⁹⁶
    ↓
Classical Projection → 4096D → 16D (for 4-qubit) or 256D (for 8-qubit)
    ↓
Encoding → Angle Embedding 或 Amplitude Embedding
    ↓
PQC → L 层 (BEL 或 SEL)
    ↓
Measurement → 期望值 → Classical Readout → 51 类 logits
```

### 架构搜索空间

| 维度 | 选项 |
|------|------|
| 量子比特数 (n) | 4, 8 |
| 编码策略 | Angle Embedding, Amplitude Embedding |
| 电路深度 (L) | 2, 4, 6 |
| 纠缠模板 | Basic Entangling Layers (BEL), Strongly Entangling Layers (SEL) |

### 关键设计

1. **Amplitude Embedding**：将归一化的 16/256 维投影特征编码到量子态的振幅中，充分利用有限 Hilbert 空间
2. **Strongly Entangling Layers (SEL)**：每个量子比特施加 RY 旋转 + CNOT 全连接纠缠
3. **Weighted Cross-Entropy (WCE)**：逆频率加权，稀有谓词权重最多为高频谓词的 46 倍
4. **量子参数极低**：4-qubit SEL 2 层仅 96 个量子参数，8-qubit SEL 4 层仅 384 个
5. **模拟训练**：PennyLane `default.qubit` 模拟器，`diff_method="backprop"`

## Experiments

### 实验设置

| 参数 | 值 |
|------|-----|
| 数据集 | VG-150, 151 obj / 51 rel |
| Backbone 特征维度 | 1024 |
| 融合方式 | Summation |
| DM Loss 权重 (λDM) | 0.4 |
| Batch size | 128 |
| 训练轮次 | 56 |
| 学习率 | 0.001 |
| Weight decay | 0.0001 |
| 优化器 | SGD (momentum 0.9) |
| 随机种子 | 1337 |
| 硬件 | Kaggle GPU 环境 |
| 仿真器 | PennyLane default.qubit |
| 物理 QPU | ibm_fez (IBM Heron r2, 156 qubits) |

### 实验配置

| ID | 模型 | Loss | Qubits | 编码 | 纠缠 | 层数 | 量子参数 |
|----|------|------|--------|------|------|------|---------|
| C1 | CFEN MLP | CE | - | - | - | - | 0 |
| C2 | CFEN MLP | WCE | - | - | - | - | 0 |
| Q1 | QP-Head | WCE | 4 | Angle | BEL | 2 | - |
| Q2 | QP-Head | WCE | 4 | Angle | SEL | 2 | - |
| Q3 | QP-Head | WCE | 4 | Amplitude | SEL | 2 | 96 |
| Q4a | QP-Head | WCE | 8 | Amplitude | SEL | 2 | 192 |
| Q4b | QP-Head | WCE | 8 | Amplitude | SEL | 4 | 384 |
| Q4c | QP-Head | WCE | 8 | Amplitude | SEL | 6 | 576 |

**注**：表 II 中 Q1、Q2 的量子参数未明确列出，只有 Q3（96）明确标注。Q1 和 Q2 由于 Angle Embedding 的参数化方式不同，预计参数模式也不同。

### 评估指标

- **R@K** (Global Recall, K=50,100)：Top-K 预测中命中 ground-truth 的比例
- **mR@K** (Mean Recall, K=50,100)：各类 recall 的均匀平均
- **Expressibility (E)**：PQC 输出 fidelity 分布与 Haar random 的 KL 散度（越低越好）
- **Von Neumann Entropy (SA)**：子系统约化密度矩阵的熵（越高表示纠缠越强）

## Results

### 1. 类平衡训练效应

| 配置 | Loss | R@50 | mR@50 | mR@100 | 观察 |
|------|------|------|-------|--------|------|
| 4-q QP (Angle+BEL) | CE | 0.7460 (Ep.19) | 0.1748 | - | CE 高频主导 |
| 4-q QP (Angle+BEL) | WCE | 0.7614 | 0.2647 (Ep.24) | 0.4054 | WCE 提升 mR@50 +8.99pp |

WCE 在不牺牲全局 recall 的前提下显著提升了长尾谓词识别。

### 2. 4-Qubit QP-Head 搜索（表 III）

| 配置 | Best R@50 | Best mR@100 | 观察 |
|------|-----------|-------------|------|
| Angle + BEL | 0.7960 (Ep.48) | 0.4980 (Ep.52) | 参考设置 |
| Angle + SEL | 0.8050 (Ep.48) | 0.4929 (Ep.52) | 更高全局 recall |
| **Amplitude + SEL** | **0.8458 (Ep.36)** | **0.5725 (Ep.52)** | **最佳 4-qubit** |

Amplitude Embedding 更充分地利用了 4-qubit 的 16 维状态空间。该配置的 Von Neumann 熵 SA=0.9817，KL 散度 E=0.0354。

### 3. 8-Qubit 深度消融（表 IV）

| 层数 | 量子参数 | KL 散度 (E, ↓) | 熵 (SA) | CUDA 推理时间 | aten::mul 调用 |
|------|---------|---------------|---------|--------------|---------------|
| 2 | 192 | 0.1116 | 2.4606 | 214.59 ms | 752 |
| 4 | 384 | 0.0432 | 2.3142 | 341.01 ms | 1,456 |
| 6 | 576 | 0.0293 | 2.2690 | 474.67 ms | 2,160 |

深度增加提高 expressibility，但增加计算开销。4 层作为平衡配置。

8-qubit 4 层配置（Q4b）：R@50 **83.73**，R@100 **92.41**，mR@50 **40.45**，mR@100 **55.38**。

### 4. 参数效率（表 V）

| 配置 | 总参数量 | 经典参数 | 量子参数 | 量子参数占比 |
|------|---------|---------|---------|------------|
| 4-q QP-Head | 69,516,292 | 69,516,196 | 96 | 0.0001% |
| 8-q QP-Head (4L) | 73,450,516 | 73,450,132 | 384 | 0.0005% |

量子参数占比极低，QP-Head 是极紧凑的决策模块。

### 5. 物理 QPU 验证（表 VI）

在 ibm_fez (IBM Heron r2, 156 qubits) 上测试 9 个 VG-150 验证三元组：
- **物理 batch 准确率**：66.67%（6/9 correct）
- **总延迟**：1.42s（含端到端云提交+执行+返回）
- **输出分布**：4 个不同谓词类别，未坍缩到单类
- **Shots**：1,024 / circuit

### 6. 与现有 SGG 方法比较（表 VIII, PredCls 设置）

| 方法 | Head 类型 | R@50 | R@100 | mR@50 | mR@100 | PQC 参数 |
|------|----------|------|-------|-------|--------|---------|
| Motifs [7] | Classical | - | 67.1 | - | 15.8 | - |
| VCTree-TDE [8] | Classical+TDE | - | 51.6 | - | 28.7 | - |
| CFEN [9] | Classical | - | - | - | 41.1 | ~8.5M |
| **QP-Head 4q (Amp+SEL)** | Hybrid Quantum | **84.58** | - | - | **57.25** | **96** |
| QP-Head 8q (Amp+SEL, 4L) | Hybrid Quantum | 83.73 | 92.41 | 40.45 | 55.38 | 384 |

4-qubit QP-Head 在 mR@100 上超出 CFEN 基线 16.15 个百分点（57.25% vs 41.1%）。

## Limitations

1. **比较范围受限**：最强对比证据来自内部消融（匹配 WCE 训练），与已有 SGG 方法的比较提供外部参考但非严格对照
2. **限于 PredCls**：未扩展到 Scene Graph Classification 和 Scene Graph Detection，上游检测错误的影响未知
3. **物理 QPU 验证规模极小**：仅 9 个三元组，无法评估统计显著性
4. **无噪声感知训练**：模拟器训练与物理硬件之间的 gap 未缓解
5. **高延迟**：单次物理 QPU 推理 1.42s，远高于经典推理
6. **特征压缩是经典侧完成的**：4096→16D 的投影层本身是经典可学习的，量子部分处理的是已压缩的特征

## Reusable Claims

- **Claim**: 紧凑型量子谓词头（96 量子参数）可在 PredCls 设置下以远超经典 MLP 的长尾识别能力运行。
  - **Evidence**: 4-qubit QP-Head mR@100 57.25% vs CFEN 41.1%（表 VIII）
  - **Scope**: VG-150 PredCls 设置，WCE 训练
  - **Confidence**: medium（需更多独立复现）

- **Claim**: Amplitude Embedding 在强维度压缩场景下显著优于 Angle Embedding。
  - **Evidence**: Amp+SEL mR@100 57.25% vs Angle+SEL 49.29%（表 III）
  - **Scope**: 4-qubit, 4096→16D 压缩
  - **Confidence**: high

- **Claim**: 增加量子电路深度改善 expressibility 但不改善纠缠，且引入显著运行时开销。
  - **Evidence**: 2→6 层 E 从 0.1116 降至 0.0293，但 SA 从 2.4606 降至 2.2690；推理时间从 214ms 升至 474ms（表 IV）
  - **Scope**: 8-qubit, Amplitude+SEL
  - **Confidence**: high

- **Claim**: WCE（稀有谓词权重最高 46×）在不牺牲全局 recall 的前提下显著改善长尾谓词识别。
  - **Evidence**: 同一 4-qubit 配置，CE→WCE 提升 mR@50 8.99pp，R@50 从 0.746 微升至 0.761（Fig. 4）
  - **Scope**: VG-150, 4-qubit QP-Head
  - **Confidence**: high

## Connections

- **CFEN [Zhou et al., 2025]**: QP-Head 直接替换 CFEN 的经典谓词 MLP 头，使用相同 BiTreeLSTM backbone
- **TDE [Tang et al., 2020]**: 作为长尾去偏的代表基线进行比较；TDE 的因果调整策略与 QP-Head 的 WCE 策略互补
- **Motifs [Zellers et al., 2018]**: 频率偏置的经典示例基线
- **VCTree [Tang et al., 2019]**: 基于树的上下文聚合方法
- **Expressibility [Sim et al., 2019]**: 使用其 PQC expressibility 诊断框架

## Open Questions

1. QP-Head 能否扩展到 Scene Graph Detection/SGGen 设置？上游检测误差是否劣化量子头的长尾收益？
2. 噪声感知训练或量子纠错能否缩小模拟→物理硬件的性能 gap？
3. 其他 SGG backbone（如基于 Transformer 的模型）是否同样受益于量子谓词头？
4. 更大的量子比特数（16+ qubits）能否提供可扩展的长尾优势？
5. 特征压缩（4096→16D）引入的经典参数是否是整体长尾性能的真正来源？

## Provenance

- **PDF 源文件**: `../../../sources/scene-graph/2026-06-09-qpredsgg-hybrid-quantum-predicate-learning-sgg.pdf` (1.6 MB, 11 pages)
- **提取文本**: `../../../sources/scene-graph/2026-06-09-qpredsgg-hybrid-quantum-predicate-learning-sgg.txt` (59,507 chars)
- **arXiv**: [2606.04689v1](https://arxiv.org/abs/2606.04689)
- **证据等级**: full-paper（全文精读）
- **作者单位**: American University of Sharjah + NYU Abu Dhabi (eBRAIN Lab, CQTS)
