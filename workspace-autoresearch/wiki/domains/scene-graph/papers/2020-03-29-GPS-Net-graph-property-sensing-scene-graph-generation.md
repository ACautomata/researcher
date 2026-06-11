---
title: "GPS-Net: Graph Property Sensing Network for Scene Graph Generation"
type: paper
domain: scene-graph
status: active
created: 2026-06-10
updated: 2026-06-10
tags:
  - CVPR-2020
  - message-passing
  - direction-aware
  - node-priority
  - long-tail
  - debiasing
raw_sources:
  - raw/sources/2020-03-29-GPS-Net-graph-property-sensing-scene-graph-generation.pdf
  - raw/sources/2020-03-29-GPS-Net-graph-property-sensing-scene-graph-generation.txt
paper:
  title: "GPS-Net: Graph Property Sensing Network for Scene Graph Generation"
  authors:
    - Xin Lin
    - Changxing Ding
    - Jinquan Zeng
    - Dacheng Tao
  year: 2020
  venue: CVPR 2020 (Oral)
  arxiv: "2003.12962"
  code: https://github.com/taksau/GPS-Net
classification:
  label: Graph Property Sensing Network for SGG
  task:
    - Scene Graph Detection (SGDET)
    - Scene Graph Classification (SGCLS)
    - Predicate Classification (PREDCLS)
  method_family: Direction-aware Message Passing + Node Priority Loss + Adaptive Frequency Softening
  modality: RGB
  datasets:
    - Visual Genome (VG)
    - OpenImages (OI)
    - Visual Relationship Detection (VRD)
  metrics:
    - R@20 / R@50 / R@100
    - mR@100
    - wmAPrel / wmAPphr / scorewtd
evidence_level: full-paper
---

## Citation

Lin, X., Ding, C., Zeng, J., Tao, D. "GPS-Net: Graph Property Sensing Network for Scene Graph Generation." CVPR 2020 (Oral). South China University of Technology & UBTECH Sydney AI Centre, University of Sydney.

## One-Sentence Contribution

提出 GPS-Net，系统性地利用场景图的三个固有属性（边方向信息、节点优先级差异、关系长尾分布）进行场景图生成，通过方向感知消息传递（DMP）、节点优先级敏感损失（NPS-loss）和自适应推理模块（ARM）在 VG、OI、VRD 三个数据集上取得 SOTA 性能。

## Problem Setting

- **目标**：在场景图生成（SGG）中，充分利用场景图的三个未被充分探索的关键属性：（1）有向边的方向信息；（2）各节点在图中的优先级差异（节点参与三元组的数量）；（3）关系的长尾分布问题
- **挑战**：
  - 现有消息传递模块（如 GCMP, S-GCMP）使用一阶线性模型（concatenation + dot product），缺乏对边方向信息的感知，且无法生成节点特定的上下文特征
  - 节点在图中的参与度差异巨大（如 man 参与 4 个三元组 vs. leg 仅 2 个），但已有方法通常对所有节点一视同仁
  - 关系频率分布严重长尾，直接使用频率先验会劣化低频关系预测
- **设定**：经典全监督 SGG, 使用 Faster R-CNN（VGG-16/ResNeXt-101-FPN）得到目标提案，沿用 [7] 和 [6] 的数据预处理和评估协议

## Method

### 架构总览

GPS-Net 包含三大贡献模块：

1. **Direction-aware Message Passing (DMP)** — 利用边方向信息和三元线性模型生成节点特定上下文
2. **Node Priority Sensitive Loss (NPS-loss)** — 通过节点优先级调整 focal loss 的聚焦参数
3. **Adaptive Reasoning Module (ARM)** — 频率软化 + 基于视觉外观的自适应偏置调整

### DMP: Direction-aware Message Passing

DMP 的核心改进来自对 GCMP 和 S-GCMP 的分析：

- **GCMP（Global Context MP）**：使用一阶线性模型 `exp(w^T[x_i, x_j])`，但拼接操作容易被 w 忽略，实际生成对所有节点相同的上下文（论文引用 [21] 证实此问题）
- **S-GCMP（Simplified GCMP）**：简化为 `exp(w_e^T x_j)`，仍然没有方向信息和节点特异性
- **DMP** 的关键创新：
  1. **三元线性模型**：基于 Tucker 分解，将节点特征 `x_i`、`x_j` 和 union box 特征 `u_ij` 通过 Hadamard 积耦合：
     ```
     e_ij = w_e^T (W_s x_i ⊙ W_o x_j ⊙ W_u u_ij)
     ```
     其中 ⊙ 表示 Hadamard 积。
  2. **方向感知**：同时计算前向（i→j）和后向（j→i）的上下文系数，堆叠为二元素向量 `[α_ij, α_ji]^T`
  3. **Kronecker 积融合**：用 Kronecker 积将方向向量与邻居特征融合
  4. **Transformer 层**：两个全连接层后接 LN 和 ReLU，精炼上下文信息

### NPS-loss: Node Priority Sensitive Loss

基于 focal loss 的设计，但聚焦参数 γ 根据节点优先级动态调整：

- **节点优先级**：`θ_i = ‖t_i‖ / ‖T‖`，其中 t_i 是包含节点 i 的三元组数，T 是总三元组数
- **非线性映射**：`γ(θ_i) = min(2, -(1 - θ_i)^µ log(θ_i))`，其中 µ 为控制因子（经验最优 µ=4）
  - 此设计确保低优先级节点 γ 变化快，高优先级节点 γ 变化慢
  - 比线性映射更合理，避免夸大中低优先级差异
- **损失形式**：`L_nps(p_i) = -(1 - p_i)^γ(θ_i) log(p_i)`
- 与 CMAT [11] 的非可微局部敏感损失相比，NPS-loss 完全可微且凸，易于优化和部署

### ARM: Adaptive Reasoning Module

两步处理关系长尾分布：

1. **Frequency Softening**：对原始频率分布 `p_{i→j}` 使用 log-softmax 软化，缓解长尾问题
2. **Bias Adaptation**：使用 sigmoid 注意力 `d = sigmoid(W_p u_ij)` 为每个节点对自适应调整频率先验，最终预测：
   ```
   p_ij = softmax(W_r(z_i ∗ z_j ∗ u_ij) + d ⊙ p̃_{i→j})
   ```
   其中 ∗ 是融合函数（ReLU(W_x x + W_y y) - ReLU(W_x x - W_y y)）

### 关系预测

测试时：`r_ij = argmax_{r∈R}(p_ij(r))`

## Experiments

### 数据集

| 数据集 | 训练集 | 测试集 | 物体类别 | 关系类别 | 平均三元组/图 |
|--------|--------|--------|----------|----------|---------------|
| VG | 70% (5K 验证子集) | 30% | 150 | 50 | 6.2 |
| OI | 53,953 | 3,234 | — | — | — |
| VRD | VG16-based split | — | — | — | — |

### Baseline 方法

- **One-stage**：IMP [5], FREQ [7], MOTIFS [7], Graph-RCNN [22], KERN [23], VCTREE-SL [2], CMAT-XE [11], RelDN [6]
- **Two-stage**：GPI [24], VCTREE-HL [2], CMAT [11]

### 训练设置

- **Backbone**：VG/VRD → VGG-16；OI → ResNeXt-101-FPN
- **优化器**：SGD with momentum
- **学习率**：10^(-3)
- **Batch size**：6
- **冻结策略**：冻结 ROIAlign 之前的层
- **采样**：背景对 : 关系对 = 3:1
- **NMS**：per-class NMS, IoU=0.3, top-64 proposals
- **SGDET**：仅预测重叠框之间的关系

### 评估协议

- **VG**：R@20/50/100 和 mR@100（三个协议：SGDET, SGCLS, PREDCLS）
- **OI**：R@50, wmAPrel, wmAPphr, scorewtd = 0.2×R@50 + 0.4×wmAPrel + 0.4×wmAPphr
- **VRD**：R@50/100 for Predicate Detection / Phrase Detection / Relation Detection

### 消融实验

在 Table 5 和 Table 6 中系统消融了三个模块：

1. **模块消融（Table 5）**：基线（MOTIFNET-NOCONTEXT + GPS-Net 的特征构建策略）→ +DMP → +NPS → +ARM，各模块均提升性能
2. **DMP 堆叠操作（Table 6 left）**：使用 stacking（双向 α_ij 和 α_ji）比不使用在各指标上一致提升
3. **MP 模块比较（Table 6 middle）**：DMP 显著优于 GCMP 和 S-GCMP
4. **NPS-loss 设计（Table 6 right）**：µ=4 最优；NPS-loss 优于 focal loss（固定 γ）

## Results

### VG 结果（Table 1）

| 任务 | 指标 | GPS-Net († backbone) | 最佳 baseline | 差距 |
|------|------|---------------------|---------------|------|
| **SGDET** | R@20 | 22.6 | KERN 21.1 | +1.5 |
| | R@50 | 28.9 | KERN 27.1 | +1.8 |
| | R@100 | 33.2 | RelDN 32.7 | +0.5 |
| **SGCLS** | R@20 | 41.8 | CMAT 36.1 | +5.7 |
| | R@50 | 42.3 | CMAT 39.2 | +3.1 |
| | R@100 | 42.3 | CMAT 40.1 | +2.2 |
| **PREDCLS** | R@20 | 67.6 | CMAT 66.9 | +0.7 |
| | R@50 | 69.7 | CMAT 68.4 | +1.3 |
| | R@100 | 69.7 | CMAT 68.8 | +0.9 |

与 KERN 相比 GPS-Net(†) 在三个协议上的 R@50/100 均值提升 1.8%；与两阶段模型 CMAT 相比提升 0.5%（平均）。

使用 RelDN 的 backbone（‡），GPS-Net SGCLS R@100 提升 5.5%（42.3 vs 36.8）。

### VG mR@100 结果（Table 2）

| 方法 | SGDET | SGCLS | PREDCLS |
|------|-------|-------|---------|
| IMP | 6.0 | 10.5 | 4.8 |
| FREQ | 8.5 | 16.0 | 7.1 |
| MOTIFS | 8.2 | 15.3 | 6.6 |
| KERN | 10.0 | 19.2 | 7.3 |
| VCTREE-HL | 10.8 | 19.4 | 8.0 |
| **GPS-Net** | **12.6** | **22.8** | **9.8** |

GPS-Net 在 mR@100 上显著优于所有方法，尤其在 SGCLS 上比 KERN 提升 3.6%，验证了其对长尾关系的处理能力。

### OI 结果（Table 3）

| 方法 | R@50 | wmAPrel | wmAPphr | scorewtd |
|------|------|---------|---------|----------|
| RelDN L0 | 74.67 | 34.63 | 37.89 | 43.94 |
| RelDN | 74.94 | 35.54 | 38.52 | 44.61 |
| **GPS-Net** | **77.27** | **38.78** | **40.15** | **47.03** |

GPS-Net 的 scorewtd 比 RelDN 提升 2.4%。在 "wears" 关系上 APrel 差距最大（+24.5%），"hits" 差距 +20.6%。

### VRD 结果（Table 4）

| 方法 | Relation R@50 | Relation R@100 |
|------|--------------|---------------|
| CAI+SCA-M | 22.4 | 25.2 |
| MF-URLN | 26.8 | 31.5 |
| RelDN† (COCO) | 28.6 | 31.3 |
| **GPS-Net† (COCO)** | **31.7** | **33.8** |
| **GPS-Net∗ (ImageNet)** | **24.3** | **28.9** |

### 消融实验关键数值

- **DMP vs GCMP vs S-GCMP**（Table 6 middle, SGCLS R@100）：DMP 40.1 > S-GCMP 38.4 > GCMP 37.9
- **DMP stacking 对比**（Table 6 left, SGCLS R@50）：with stack 39.2 vs without 38.8
- **NPS-loss vs Focal Loss**（Table 6 right, SGCLS R@100）：NPS(µ=4) 40.1 vs Focal 39.8
- **µ 对比**：µ=4 在 SGCLS R@100 达 40.1，µ=3 为 39.9，µ=5 为 39.9

## Limitations

- DMP 使用三层线性变换（Ws, Wo, Wu）增加了参数量和计算开销
- NPS-loss 的 µ 需要在验证集上调优，不同数据集可能最优 µ 不同
- ARM 中频率先验的有效性依赖于训练集的统计分布，对未见物体对组合泛化能力有限
- 与后续 Transformer-based SGG（如 RelTR, SGTR）相比计算效率不够高
- 仅在标准全监督设定下评估，未探索 few-shot 或 zero-shot 泛化

## Reusable Claims

1. **消息传递中的方向编码**：使用三元线性模型（Tucker 分解）同时编码源节点、目标节点和 union box 特征，可生成节点特定的上下文信息 — 比 GCMP/S-GCMP 的一阶线性模型更优
2. **节点优先级可微损失**：NPS-loss 证明了节点优先级可以以完全可微的方式编码到目标检测损失中，替代 CMAT 的策略梯度方法
3. **频率软化有效性**：log-softmax 软化频率分布 + 视觉自适应偏置调整可以同时提升 Recall 和 Mean Recall
4. **三个属性协同**：边方向、节点优先级、长尾分布三个属性的联合建模比单独任一个属性带来的增益更大

## Connections

- **之前工作**：
  - 继承了 Neural Motifs [7] 的 Faster R-CNN + VGG-16 设定和频率先验基线
  - 针对 CMAT [11] 的非可微局部敏感损失提出可微替代 NPS-loss
  - 针对 GCMP/S-GCMP [21] 的节点通用上下文问题提出 DMP
- **同期/后续工作**：
  - VCTREE [2] 同 CVPR 2019，使用动态树结构建模图的方向性；GPS-Net 在方向建模上采用了不同思路（三元线性 vs 树结构）
  - RelDN [6] 同 CVPR 2019 使用对比损失；GPS-Net 使用相同 backbone 在 OI 上超越 RelDN scorewtd 2.4%
  - PE-Net (CVPR 2023) 继承了原型学习和消息传递方向
  - HiKER-SGG (CVPR 2024) 继承了知识增强和长尾处理的思路
- **相关领域**：图注意力网络 [8], Tucker 分解融合 (MUTAN [12]), 非局部网络分析 (GCNet [21])

## Open Questions

1. DMP 的三元线性模型是否可以扩展到多模态输入（如 CLIP 视觉特征 + 文本特征）？
2. NPS-loss 中的 γ 映射函数是否可以从固定形式（基于 θ）进化为可学习参数？
3. ARM 的视觉自适应机制是否可以扩展到 zero-shot 或 open-world SGG 设定？
4. 在 MOTIFS/VCTREE 等经典方法上替换 DMP/NPS-loss 是否能带来类似增益？

## Provenance

- **原始来源**：raw/sources/2020-03-29-GPS-Net-graph-property-sensing-scene-graph-generation.pdf
- **全文提取**：raw/sources/2020-03-29-GPS-Net-graph-property-sensing-scene-graph-generation.txt
- **分析依据**：全文精读（完整提取 ~2000 行）
- **arXiv ID**：2003.12962 (submitted 29 Mar 2020)
- **代码仓库**：https://github.com/taksau/GPS-Net
- **会议**：CVPR 2020 Oral
