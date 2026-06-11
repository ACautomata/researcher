---
title: "Assured Autonomy with Neuro-Symbolic Perception for Scene Graph Generation"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - neuro-symbolic
  - assured-autonomy
  - adversarial-robustness
  - sensor-fusion
  - frustum-attack
  - cross-sensor-integrity
  - foundation-model
  - pmrl-2025
raw_sources:
  - ../../../raw/sources/2025-arXiv-Assured-Autonomy-Neuro-Symbolic-SGG.pdf
  - ../../../raw/sources/2025-arXiv-Assured-Autonomy-Neuro-Symbolic-SGG.txt
related_pages:
  - r1-sgg-compile-scene-graphs-with-reinforcement-learning.md
  - hiker-sgg-hierarchical-knowledge-enhanced-robust-sgg.md
  - scalable-theory-driven-regularization-scene-graph-generation.md
evidence_level: full-paper
paper:
  title: "Assured Autonomy with Neuro-Symbolic Perception for Scene Graph Generation"
  authors:
    - R. Spencer Hallyburton
    - Miroslav Pajic
  year: 2025
  venue: "Proceedings of Machine Learning Research (PMLR) 288:1–19, 2025"
  arxiv: "2505.21322"
  code: null
  project: null
classification:
  label: "Neuro-Symbolic Perception for Assured Autonomy via SGG"
  task:
    - assured-autonomy
    - adversarial-attack-detection
    - cross-sensor-integrity
    - neuro-symbolic-perception
  method_family: neuro-symbolic-framework
  modality: multi-modal (camera + LiDAR)
  datasets:
    - CARLA
    - nuScenes
  metrics:
    - attack-displacement (m)
    - IoU-consistency
---

## Citation

> R. Spencer Hallyburton and Miroslav Pajic. "Assured Autonomy with Neuro-Symbolic Perception for Scene Graph Generation." *Proceedings of Machine Learning Research* 288:1–19, 2025. arXiv:2505.21322.

## One-Sentence Contribution

提出神经符号感知范式 **NeuSPaPer**，利用场景图生成（SGG）桥接低层传感器感知与高层符号推理，首次通过跨传感器图一致性检测实现单平台 frustum 攻击识别。

## Problem Setting

**背景**：现有 DNN 感知模型本质上是统计模式匹配器，面对改变场景语义结构的攻击（如 frustum 攻击将 3D 物体平移 40m+ 仍保持 2D 投影一致性）无法防御。传统认证鲁棒性技术（子采样、集成）对基于等变性的平移攻击无效。

**目标**：设计神经符号感知框架，通过联合检测与图生成将感知输出结构化，利用常识知识和跨模态图一致性评估实现攻击检测。

**挑战**：
1. DNN 的 **等变性漏洞**（equivariance vulnerability）：LiDAR 点云 DNN 对空间平移等变的特性使得平移攻击无法被 subsampling/ensembling 防御
2. **frustum 攻击**最优解（式 1）：攻击者在保持 2D-3D IoU ≥ ζ_min 的约束下最大化 3D 检测位移
3. 多传感器 fusion 中不对称分辨率（2D 相机 vs 3D LiDAR）造成的安全盲区

## Method

### NeuSPaPer 框架（四组件）

1. **联合感知与图生成（Joint Perception and Graph Generation）**
   - **相机模态**：使用基础模型（foundation model，如 CLIP/ViLT）从 RGB 图像直接构建场景图（subject, predicate, object triplets）
   - **LiDAR 模态**：基于规则几何函数，根据 3D 检测框计算空间关系（front of, left of, near/far, occluding 等 7 种关系）
   - 专业 SGG 模型（如 EGTR, SGTR）可用于全模态 SGG
   - 关系集：front_of, left_of, occluding, following, far_from, close_to, next_to 及各自补关系

2. **单传感器图完整性推理（Per-Sensor Graph Integrity）**
   - **知识图谱嵌入（KGEs）**：将 SGG 输出与常识知识图谱比较，验证 observed concepts 是否合理
   - **约束满足评估（CSE）**：应用领域特定逻辑约束，拒绝不合真实世界预期的图输出

3. **跨传感器图完整性推理（Cross-Sensor Graph Integrity）**
   - **暴力匹配**：图间节点匹配后比较边一致性，未匹配边评估是噪声还是攻击
   - **GNN 推断**：用图神经网络评估图一致性
   - 输出：per-node, per-edge 一致/不一致分类；可进一步假设扰动源

4. **图信息传感器融合（Graph-Informed Sensor Fusion）**
   - 图级语义信息辅助异构数据对齐（如解决跨传感器物体分配的冲突）
   - 减少模糊性（如遮挡情况下的推理）

### 攻击假设

- Frustum 攻击（式 1）：攻击者知道场景中现有物体，能操纵 3D 检测框的位置，在保持 2D 投影 IoU ≥ 阈值条件下最大化位移
- 实践约束：物体体积 [Vmin, Vmax]、维度限制、垂直位置固定、仅 yaw 可操纵

## Experiments

### 数据集

- **CARLA**：高保真自动驾驶模拟器，提供合成城市场景（多场景分析，代表性主场景含 4 检测物体：car, van, bicycle, truck）
- **nuScenes**：真实世界大规模驾驶数据集，含详细 3D 标注（2 个补充案例，Fig.7-8）

### 评估协议

- 定可行性案例研究，非传统 SGG benchmark 评估
- 比较：camera 图（foundation model 生成）vs LiDAR 图（规则生成）的跨模态一致性
- 攻击场景：frustum 攻击（3D 检测平移，保持 2D 投影一致性）
- 检测标准：跨传感器图间不一致性的可识别性

### 方法配置

- **相机图生成**：foundation model via natural language prompting ("Build a scene graph from this image")，输出 (subject, predicate, object) triplets
- **LiDAR 图生成**：classical 3D 检测器 → 规则几何关系函数
- **跨传感器完整性**：暴力子图匹配枚举，比较节点和边的一致性

## Results

### 主要结果

| 指标 | 值 |
|------|-----|
| Frustum 攻击最大位移（保持 IoU > 0.9） | **40 m+** |
| Frustum 攻击 IoU 阈值（保持单帧隐身性） | **> 0.9** |
| 跨传感器图一致性攻击检测能力 | **成功识别**（van 平移攻击场景） |
| 行人平移攻击检测（nuScenes） | **成功识别**（Fig.7） |
| van 平移攻击检测（nuScenes） | **成功识别**（Fig.8） |

### 关键发现

1. **等变性漏洞**：LiDAR DNN 的 translation equivariance 使得任何 subsampling/ensembling 认证方法都无法抵御平移攻击（Section 3.1）
2. **跨模态图不一致性可检测**：由于 foundation model 可从 2D 图像中推断 3D 空间关系（如 front_of, near），当攻击者平移 3D 物体时，相机图的 van→truck 关系与 LiDAR 图的同一关系不一致，从而暴露攻击
3. **图级推理优于检测级推理**：传统 χ2 创新检验只能评估单检测层面一致性，图级推理利用完整的物体关系结构，对改变语义结构的攻击更敏感

### 无标准 SGG 量化指标

本文为可行性/立场论文，**未报告**标准 SGG 指标（Recall@K, mR@K, mAP 等）。该论文不侧重 SGG 模型性能，而是使用 SGG 作为交叉模态安全验证的工具。

## Limitations

1. **定性验证为主**：仅展示案例研究，缺乏大规模定量评估
2. **依赖基础模型**：相机图生成使用计算密集的 foundation model，不适合实时部署
3. **LiDAR 图生成序列化**：先检测后规则建图，非端到端
4. **暴力匹配可扩展性**：跨传感器完整性使用枚举，对复杂场景计算开销大
5. **缺少概率推理**：噪声数据可能导致图不完整/不确定，当前方法缺乏鲁棒性
6. **无标准 SGG 基准评测**：未在 Action Genome, VG 等 SGG benchmark 上评测

## Reusable Claims

- **DNN 等变性漏洞是关键安全弱点**：对空间平移的等变性是内在属性，无法通过后处理认证技术消除（Section 3.1）→ 需要根本性的架构变革
- **SGG 可桥接 2D→3D 推理**：foundation model 能从 2D 图像中推断 3D 空间关系（如 front_of, behind），实现模态间的语义对齐
- **跨传感器图一致性检查有效检测语义攻击**：即使攻击保持 2D-3D 检测层面的投影一致性，图级语义关系的不一致仍可暴露攻击
- **SGG 用于安全而非生成**：本工作将 SGG 从传统的视觉关系理解/生成任务重新定位为 CPS 安全验证工具

## Connections

- **R1-SGG**（Compile SGG with RL）：同样使用结构化方法提升 SGG，但 R1-SGG 侧重图生成质量，本工作侧重 SGG 用于安全验证
- **HiKER-SGG**（Hierarchical Knowledge Enhanced Robust SGG）：都引入外部知识增强 SGG 鲁棒性，但 HiKER 侧重视觉关系识别，本工作侧重跨模态安全
- **Scalable Theory-Driven Regularization**：用形式化约束规范 SGG 输出，与本工作的 CSE 方向一致，但侧重图质量而非安全性
- **frustum attack** Hallyburton et al. (2022)：本工作的攻击场景基于该前期工作

## Open Questions

1. 大规模定量评估：在 100+ 攻击场景中，SGG 跨模态一致性的检测率（TPR）和误报率（FPR）是多少？
2. 实时性：专业 SGG 模型（如 EGTR）能否在车载平台达到实时推理？
3. GNN 推断：基于 GNN 的图一致性评估相比暴力匹配的性能和鲁棒性如何？
4. 时序图完整性：利用时序一致性（如 tracking 信息）能否进一步提升检测率？
5. 对抗攻击的适应性：若攻击者已知 SGG 安全校验，能否设计针对性逃逸攻击？
6. 概率推理：对噪声/不确定图如何进行概率化一致性评估？

## Provenance

- **证据等级**：full-paper
- **获取方式**：arXiv PDF（2505.21322）
- **分析范围**：全文精读，包括 19 页正文 + 4 个附录
- **验证状态**：定性结果已验证（逻辑自洽，无定量 benchmark），定量数据来源于原文
- **核心依赖**：frustum attack 来自 Hallyburton et al. (2022) USENIX Security；等变性分析基于 Bronstein et al. (2021)
