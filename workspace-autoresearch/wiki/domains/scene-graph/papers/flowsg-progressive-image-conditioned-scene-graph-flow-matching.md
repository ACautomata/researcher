---
title: "FlowSG: Progressive Image-Conditioned Scene Graph Generation with Flow Matching"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - scene-graph-generation
  - flow-matching
  - generative-model
  - hybrid-discrete-continuous
  - VQ-VAE
  - diffusion
  - open-vocabulary
  - panoptic-scene-graph
  - arXiv-2026
  - graph-transformer
raw_sources:
  - ../../../raw/sources/2026-06-09-FlowS-Can-We-Build-Scene-Graphs-Not-Classify-Them.pdf
  - ../../../raw/sources/2026-06-09-FlowS-Can-We-Build-Scene-Graphs-Not-Classify-Them.txt
related_pages:
  - is-ggt-iterative-scene-graph-generation-with-generative-transformers.md
evidence_level: full-paper
paper:
  title: "FlowSG: Progressive Image-Conditioned Scene Graph Generation with Flow Matching"
  authors:
    - Xin Hu
    - Ke Qin
    - Wen Yin
    - Yuan-Fang Li
    - Ming Li
    - Tao He
  year: 2026
  venue: arXiv preprint arXiv:2604.18623, 2026
  arxiv: "2604.18623"
  doi: null
  code: null
classification:
  task:
    - Scene Graph Generation (SGG)
    - Panoptic Scene Graph Generation (PSG)
    - Open-Vocabulary SGG
  method_family:
    - Flow Matching (CFM + DFM)
    - Hybrid Discrete-Continuous Generation
    - Graph Transformer with Relation-Modulated Attention
    - VQ-VAE Tokenization
  modality:
    - RGB Image (2D)
  dataset:
    - Visual Genome
    - PSG (Panoptic Scene Graph)
  backbone:
    - CLIP ViT-B/16 (frozen)
    - Pre-trained Object Detector (frozen)
---

# FlowSG: Progressive Image-Conditioned Scene Graph Generation with Flow Matching

## 概述

FlowSG 提出了一种**基于流匹配（Flow Matching）的渐进式场景图生成**方法，将 SGG 从一次性分类（one-shot classification）重新定义为**混合离散-连续状态空间上的连续时间运输**问题。核心思路是从带噪图出发，通过约束感知的渐进式精炼（progressive refinement）联合合成节点（物体）和边（谓词），实现语义与几何的协同生成。

论文标题的关键问题："Can We Build Scene Graphs, Not Classify Them?"——倡导从确定性分类转向生成式构建。

## 动机与挑战

- 现有 SGG/PSG 方法（两阶段/一阶段）本质上是**一次性预测**而非**生成**：
  1. 关系分配在单次前向中决定，缺乏迭代纠错机制
  2. 语义与几何特征被作为静态输入而非联合演化状态
  3. 全局图约束（如空间传递性）难以在独立打分的关系上施加
- 现有方法在产生全局一致的场景图方面存在本质局限
- 流匹配（Flow Matching）在图生成领域已展示出高质量的迭代去噪能力，但多数工作是无条件或弱条件的

## 方法

### 整体架构

FlowSG 的整体流程：
1. **场景图离散化（Tokenization）**：使用 VQ-VAE 将物体外观特征和关系谓词量化为紧凑的、语言对齐的 token
2. **混合流匹配（Hybrid Flow Matching）**：联合使用连续流匹配（CFM）处理边界框和离散流（DFM via CTMC）处理分类 token
3. **图去噪器（Graph Denoiser）**：基于 DiT 风格的图 Transformer，包含关系调制自注意力（ReSA）和流程感知消息聚合（FMA）

### 1. 场景图 Tokenization（Section 4.1）

**物体离散化**：
- 用 CLIP 图像编码器提取裁剪区域的视觉特征 $u_i$
- 训练 VQ-VAE 编码器将 $u_i$ 量化为代码本 H_obj 中的最近邻条目 $a^*_i$
- 每个节点 token 包含：外观码 $a^*_i$、类别标签 $c^*_i$、边界框 $b^*_i$

**关系离散化**：
- 用 CLIP 文本编码器将谓词短语映射到语言嵌入空间
- 训练 VQ-VAE 将关系短语量化为紧凑代码 $p_{ij} \in [K_r]$
- 语言空间编码提供语义平滑，支持开集解码（推理时通过最近邻回退到 CLIP 空间）

### 2. 混合流匹配（Section 4.2）

**状态空间**：
- 每个节点存有离散物体标签+外观码和连续边界框参数
- 每个边存有离散谓词标签
- 离散状态用包含 [MASK] 状态的单纯形上的概率质量函数建模

**初始化**：
- 物体类别源自检测器（未被 mask），作为指导先验
- 关系类型和外观码完全 masked
- 边界框从标准高斯噪声初始化

**连续流匹配（CFM）用于边界框**：
- 线性插值路径：$g_t = (1-\kappa_t)g_0 + \kappa_t g_1$
- 目标速度：$u^*_g = dot\kappa_t(g_1 - g_0)$
- 训练网络 $v_\theta$ 匹配目标速度场（L2 损失）

**离散流（DFM via CTMC）用于语义**：
- 两点条件路径：$p_t(s|s_0,s_1) = (1-\kappa_t)\delta_{s_0}(s) + \kappa_t\delta_{s_1}(s)$
- 训练网络预测干净后验分布（时间条件交叉熵损失）
- 推理时组装速率矩阵进行 CTMC 演化

**混合图因子化**：
- 所有槽（节点/边）并行演化，每个局部更新以全局带噪图和图像特征为条件
- 通过条件独立性实现高效步骤分解

### 3. 图去噪器架构（Section 4.3）

基于 DiT 风格的图 Transformer，包含三个核心模块：

**全局图像条件集成（Cross-attention）**：
- 用冻结的 CLIP ViT-B/16 提取图像特征
- 通过交叉注意力将视觉信息注入图 Transformer

**关系调制自注意力（ReSA）**：
- 在注意力计算中以 FiLM [45] 方式注入谓词语义
- 选择性放大关系一致的邻居，抑制虚假连接

**流程感知消息聚合（FMA）**：
- 维护一个邻域矩（均值、方差、偏度、峰度）的存储库
- 根据时间 t 和节点度计算自适应权重
- 早期去噪步（高噪声）偏向保守的稳健统计量，后期步（低噪声）转向更锐利的高阶矩

### 训练目标

总损失：$\mathcal{L} = \mathcal{L}_{CFM} + \lambda\mathcal{L}_{DFM}$
- $\mathcal{L}_{CFM}$：边界框的 CFM 速度匹配 L2 损失
- $\mathcal{L}_{DFM}$：离散语义的交叉熵损失（分解到节点和边缘）

### 实现细节

- 5 个 Transformer 模块，8 头自注意力，hidden=512，dropout=0.1
- 冻结 CLIP ViT-B/16 图像编码器
- 目标/关系代码本：64 entries × 512 维
- 4 个有序槽（ordered slots）量化外观/关系
- 随机边缘精炼模式（概率 0.2）：仅生成边，保持节点固定
- 优化器：AdamW，500K 迭代，batch=128，lr=1e-4，weight decay=0.02
- 训练硬件：4× NVIDIA A100 GPU

## 实验结果

### 闭集（Closed-Set）结果

#### PSG Dataset（双阶段方法）

| 方法 | SGDet R@50 | SGDet mR@50 | SGDet R@100 | SGDet mR@100 | PredCls R@50 | PredCls mR@50 | PredCls R@100 | PredCls mR@100 |
|------|:---------:|:----------:|:----------:|:-----------:|:-----------:|:------------:|:------------:|:-------------:|
| IMP [59] | 18.2 | 7.1 | 18.6 | 7.2 | 36.8 | 10.9 | 38.9 | 11.6 |
| MOTIF [69] | 21.7 | 9.6 | 22.0 | 9.7 | 50.4 | 22.1 | 52.4 | 22.9 |
| VCTree [54] | 22.1 | 10.2 | 22.5 | 10.2 | 50.8 | 22.6 | 52.7 | 23.3 |
| ADtrans [29] | 29.6 | 29.7 | 30.0 | 30.0 | — | 36.2 | — | 38.8 |
| PairNet [57] | 35.6 | 28.5 | 39.6 | 30.6 | — | — | — | — |
| SPADE† [21] | 43.8 | 38.9 | 49.3 | 46.5 | 64.2 | 49.1 | 69.3 | 54.8 |
| USG-Par† [58] | 44.6 | 40.9 | 51.3 | 42.7 | 67.2 | 51.1 | 72.3 | 57.8 |
| **FlowSG** | **46.3** | **42.7** | **53.3** | **48.3** | **69.4** | **54.9** | **74.3** | **61.3** |

**关键指标**：FlowSG 在 PSG 闭集 SGDet 上 R@50 达 **46.3%**，mR@50 达 **42.7%**，以约 +1~2 点超越此前 SOTA USG-Par。

#### VG Dataset（双阶段方法，SGDet）

| 方法 | R@50 | mR@50 | R@100 | mR@100 |
|------|:----:|:-----:|:-----:|:------:|
| MOTIF [69] | 32.5 | 6.6 | 36.8 | 7.9 |
| VCTree [54] | 31.9 | 6.4 | 36.0 | 7.3 |
| PE-Net [71] | 26.5 | 16.7 | 30.9 | 18.8 |
| OpenPSG† [72] | 32.7 | 13.5 | 38.0 | 18.3 |
| DSGG [15] | 32.9 | 13.0 | 38.5 | 17.3 |
| CAPSGG [22] | 18.3 | — | 22.8 | — |
| **FlowSG** | **36.5** | **18.4** | **42.4** | **21.6** |

**关键指标**：VG 闭集 SGDet 上 R@100 达 **42.4%**（+3~4 点），mR@100 达 **21.6%**。

#### VG Dataset（单阶段方法）

| 方法 | R@50 | mR@50 | R@100 | mR@100 |
|------|:----:|:-----:|:-----:|:------:|
| SGTR [34] | 24.6 | 12.0 | 28.4 | 15.2 |
| EGTR [23] | 30.2 | 5.5 | 34.3 | 7.9 |
| SpeaQ [26] | 32.9 | 11.8 | 36.0 | 14.1 |
| OvSGTR† [4] | 33.8 | 7.2 | 37.3 | 8.8 |
| Hydra-SGG [3] | 28.6 | 15.9 | 33.4 | 19.4 |
| HRTrans [9] | 34.1 | 16.0 | 38.3 | 20.5 |
| **FlowSG** | **36.5** | **18.4** | **42.4** | **21.6** |

**关键指标**：FlowSG 在单阶段对比中也取得最佳，约 +2 点提升。

### 开集（Open-Vocabulary）结果

| 数据集 | 方法 | R@50 | mR@50 | R@100 | mR@100 |
|:------:|------|:----:|:-----:|:-----:|:------:|
| PSG | PGSG [35] | 15.5 | 10.1 | 17.7 | 11.5 |
| | OvSGTR∗ [4] | 19.3 | 12.4 | 22.8 | 14.0 |
| | OpenPSG [72] | 21.2 | 19.8 | 25.1 | 21.4 |
| | VL-IRM∗ [42] | 25.1 | 18.2 | 29.3 | 22.5 |
| | **FlowSG** | **26.7** | **22.3** | **31.8** | **24.2** |
| VG | VS3 [70] | 15.6 | 6.7 | 17.2 | 7.4 |
| | PGSG [35] | 15.8 | 5.2 | 19.1 | 7.3 |
| | OvSGTR∗ [4] | 15.1 | 5.3 | 19.3 | 7.5 |
| | VL-IRM∗ [42] | 14.1 | 8.4 | 20.4 | 12.7 |
| | **FlowSG** | **16.9** | **9.7** | **22.5** | **14.1** |

**关键指标**：开集设置下，PSG 上 mR@50 达 **22.3%**（超 VL-IRM 约 +4 点），VG 上 R@100 达 **22.5%**（+2 点）。

### 消融实验

#### Graph Transformer 组件（PSG SGDet）

| 变体 | R@50 | mR@50 | R@100 | mR@100 |
|------|:----:|:-----:|:-----:|:------:|
| w/o FMA | 40.5 | 37.1 | 47.2 | 39.7 |
| w/o EdgeMA | 43.1 | 38.5 | 49.8 | 44.2 |
| w/o NodeMA | 42.8 | 38.9 | 49.6 | 42.5 |
| w/o Cross-attn | 39.2 | 34.3 | 45.3 | 36.9 |
| **FlowSG (full)** | **46.3** | **42.7** | **53.3** | **48.3** |

- **FMA 贡献最大**：去除后 R@50 下降 5.8 点，mR@50 下降 5.6 点
- **Cross-attention 最关键**：去除后 R@50 下降 7.1 点，mR@100 下降 11.4 点
- 边缘级和节点级聚合互补：各自去除均导致 3-6 点下降

#### Tokenization 设计（PSG）

| 配置 | R@50 | mR@50 | R@100 | mR@100 |
|------|:----:|:-----:|:-----:|:------:|
| 32×256 | 32.7 | 28.5 | 39.5 | 31.2 |
| 64×256 | 43.3 | 41.1 | 52.1 | 46.6 |
| **64×512 (Ours)** | **46.3** | **42.7** | **53.3** | **48.3** |
| M=3 槽 | 44.1 | 38.8 | 50.8 | 45.5 |
| M=5 槽 | 35.6 | 31.4 | 42.3 | 47.0 |
| **M=4 (Ours)** | **46.3** | **42.7** | **53.3** | **48.3** |

#### 采样策略
- **Marginal 初始化**在所有策略中最优，基于数据集先验的初始化方案在长尾谓词识别上优势明显
- 四种策略排序：Marginal > Absorbing > Masking > Uniform

## 关键洞察

1. **新范式**：首次将 SGG 重新定义为混合离散-连续空间上的渐进式生成，而非一次性分类
2. **生成式协同**：连续流匹配（几何）与离散流（语义）通过共享图编码器紧密耦合，实现语义-几何共生成
3. **渐进式精炼**：多步 ODE 积分带来粗到细的结构修正，可视化显示从粗粒关系到精确谓词的改进轨迹
4. **开集泛化**：语言对齐的 VQ-VAE 代码本支持开集推理，CLIP 嵌入空间提供语义平滑
5. **推理效率**：流匹配支持少步 ODE 求解（相比传统扩散过程所需步数更少）

## 局限与未来工作

- **推理开销**：相比严格的一次性模型，多步 ODE 积分仍增加推理成本
- **未来方向**：
  - 与检测器端到端联合训练
  - 模型压缩与步数自适应求解器
  - 去噪器的提前退出策略（early-exit）

## 对比与关联

- **与 IS-GGT（CVPR 2023）比较**：两者都挑战"SGG 即分类"的传统范式
  - IS-GGT 通过生成式图采样选择约 20% 边缘，再分类谓词
  - FlowSG 通过流匹配在完整状态空间上渐进式生成，支持语义与几何耦合
  - FlowSG 的混合离散-连续建模比 IS-GGT 的纯分类路由表达力更强
  - 两者都强调迭代/渐进式结构，但 FlowSG 的流匹配框架更统一
- **与扩散类 SGG（如 Diff-VRD）比较**：
  - Diff-VRD 用去噪扩散概率模型生成关系特征
  - FlowSG 用流匹配替代扩散，支持更少步推理和更好训练稳定性
  - FlowSG 同时处理离散语义和连续几何，Diff-VRD 仅关注关系特征
- **与 USG-Par [58] 比较**：FlowSG 在所有指标上超 USG-Par 约 3 点，验证了生成式框架的优越性
