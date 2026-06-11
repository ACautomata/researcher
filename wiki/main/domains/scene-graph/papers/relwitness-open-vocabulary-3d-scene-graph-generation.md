---
title: "RelWitness: Open-Vocabulary 3D SGG with Visual-Geometric Relation Witnesses"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags: [3D-SGG, open-vocabulary, relation-witness, positive-unlabeled, arXiv-2026]
raw_sources:
  - ../../../sources/scene-graph/2026-01-01-RelWitness-Open-Vocabulary-3D-Scene-Graph-Generation.pdf
  - ../../../sources/scene-graph/2026-01-01-RelWitness-Open-Vocabulary-3D-Scene-Graph-Generation.txt
evidence_level: abstract-only
---

# RelWitness: Open-Vocabulary 3D Scene Graph Generation with Visual-Geometric Relation Witnesses

> **⚠️ 证据等级说明**：本文所有实验结果为 **simulated manuscript-planning numbers**（文中明确标注 "All numerical results are planning values and must be replaced by reproduced measurements before submission"）。论文提出完整方法论和实验设计，但无实际复现结果。本页记录仅反映论文声称的方法论设计和计划中的实验方案。

## 核心贡献

1. **问题重新定义**：将开放词汇 3D 场景图生成中的不完整监督问题表述为 **物理可观测性（physical observability）** 问题，引入 **relation witness（关系见证者）** 作为决定未标注关系能否成为监督信号的单元。
2. **视觉-几何见证验证器（Visual-Geometric Witness Verifier）**：结合 RGB 视图、深度线索、重建 3D 几何、角色敏感的文本、对象先验空视图（null test）和多视角一致性来构建见证记录。
3. **见证引导的正-无标记学习（Witness-Guided Positive-Unlabeled Learning）**：提出族平衡见证记忆库，存储验证后的缺失正例、可靠负例、不确定候选及其见证轨迹。
4. **见证一致图解码**（Witness-Consistent Graph Decoding）和 **RGB-D 缺失关系审计协议**（Missing-Relation Audit Protocol）。

## 动机

- 开放词汇 3D SGG 的核心困难不仅是词汇扩展，更是 **监督可靠性**：3D 场景图数据集的关系标注是选择性的，许多有效的物体对关系未被标注。
- 将所有未标注关系当作负例会抑制有用的缺失关系（missing positives）；基于语言合理性或物体共现补全标签则可能添加物理上不存在的边（hallucination）。
- 核心观测：**合理性（plausibility）≠ 可观测性（observability）**。一个合理的 "cup on table" 短语，如果杯子实际在 sink 里就是错的。

## 方法

### 问题设定

给定有 pose 的 RGB-D 序列 $S = \{(I_t, D_t, T_t)\}_{t=1}^T$，得到 3D 物体实例 $O = \{o_i\}$。对于每个有序对 $(o_i, o_j)$ 和关系短语 $r$，标注 $y^r_{ij}$ 不完整：
- $y^r_{ij}=1 \Rightarrow z^r_{ij}=1$
- $y^r_{ij}=0 \Rightarrow z^r_{ij} \in \{0, 1\}$

维护四个动态集合：$P_{obs}$（标注正例）、$P_{miss}$（验证缺失正例）、$N^{rel}$（可靠负例）、$U^{unc}$（不确定候选）。

### 关系见证库（Witness Taxonomy）

| 见证族 | 示例短语 | 正见证线索 | 常见拒绝原因 |
|--------|---------|-----------|------------|
| Support | on, standing on, resting on, supported by | 垂直顺序、底-顶接触、支持面重叠 | 可见深度间隙或主体低于客体 |
| Containment | in, inside, within, stored in | 主体范围在容器体积或货架单元内 | 主体在容器前，弱包围 |
| Proximity | near, next to, beside, adjacent to | 以物体和房间尺度归一化的度量距离小 | 大表面距离或中间有障碍物 |
| Vertical order | above, below, under, over | 一致的高度顺序和水平兼容性 | 矛盾的深度/高度关系 |
| Attachment | attached to, mounted on, hanging from | 稳定的边界接触和合理的共享表面 | 仅在一个视图中接触或表面不匹配 |
| Orientation | facing, looking at, oriented toward | 前轴指向目标，视角一致的朝向 | 对称物体或轴背离 |
| Interaction | holding, touching, leaning against | 局部 RGB/深度接触区域或类力配置 | 无局部接触或遮挡交互区域 |
| Functional/uncertain | used for, belongs to, part of task | 显式可观测代理或强任务特定线索 | 静态扫描中无视觉-几何线索 |

### 关系见证记录（Relation Witness Record）

对每个候选 $(o_i, r, o_j)$ 构建：
$$W^r_{ij} = \{S_{rgb}, S_{dep}, S_{3d}, S_{mv}, S_{role}, S_{null}, \pi_r, A_{2d}, A_{3d}, \eta_{ij}\}$$

- **RGB 见证**：选择双物体同时可见的帧，计算跨模态验证得分 $S_{rgb}$，使用可靠性加权 top-average 避免单帧偶然高分。
- **深度见证**：根据见证族选择相应线索（支持检查表面间隙、包含检查深度不连续性、前后检查深度排序）。
- **3D 几何见证**：使用表面距离 $d_{surf}$、垂直位移 $\Delta z_{ij}$、水平投影重叠 $\Omega_{ij}$、包含比例 $\delta_{in}$ 等族特定探针。
- **多视角持久性**：计算 RGB 和深度见证分数在可见帧间的一致性方差。
- **角色一致性**：对比原序和对调序的得分差异。
- **对象先验空视图**：遮蔽配对几何和交互区域后评估语言先验强度，区分共现驱动 vs. 物理可观测。

### 见证引导学习

**见证质量**：
$$Q^r_{ij} = \sigma(w_{rgb}S_{rgb} + w_{dep}S_{dep} + w_{3d}S_{3d} + w_{mv}S_{mv} + w_{role}S_{role} - w_{null}S_{null})$$

权重按关系族不同（$w = h(\pi_r)$）。

**三阶段训练**：
1. **监督预热**（Stage 1）：仅用 $P_{obs}$ 和采样背景对训练，不信任未标注关系。
2. **保守见证启动**（Stage 2）：动量为师在严格阈值下评估未标注候选，仅通过严格族阈值者加入 $P_{miss}$ 或 $N^{rel}$。
3. **联合见证引导学习**（Stage 3）：用 $P_{obs} + P_{miss} + N^{rel} + U^{unc}$ 联合训练。

**损失函数**：
$$\mathcal{L} = \mathcal{L}_{obs} + \lambda_m\mathcal{L}_{miss} + \lambda_n\mathcal{L}_{neg} + \lambda_u\mathcal{L}_{unc} + \lambda_w\mathcal{L}_{wit}$$

- $\mathcal{L}_{obs}$：标注正例的标准正监督
- $\mathcal{L}_{miss}$：见证加权正监督（权重 $Q^r_{ij}$）
- $\mathcal{L}_{neg}$：可靠负例的负监督
- $\mathcal{L}_{unc}$：不确定候选的置信度温度化（熵正则化）

### 见证一致解码

推理时按分类器置信度和见证质量联合排序：
$$\hat{s}^r_{ij} = s^r_{ij} + \lambda_Q \log(Q^r_{ij} + \epsilon)$$

仅当两个短语具有高文本相似度且共享同一见证族和轨迹时才合并（因此 "on" 和 "supported by" 可合并，但 "near" 和 "facing" 分别保留）。

## 实验设计

### 数据集
- **3DSSG/3RScan**：标准 3D 室内场景图基准，闭集和缺失标签两个设定
- **OV-3DSSG**：从 3DSSG 导出的开放词汇切分，保留稀有和组合关系短语为 unseen
- **ScanNet-OV**：从 ScanNet 相机轨迹导出的 RGB-D 开放词汇切分

### 审计协议
从所有方法的预测中按关系频率、族、seen/unseen、置信度分层采样 2,400 个候选（含 1,200 未标注预测）。标注者在看到 RGB 帧、深度图、3D 重建、mask 和短语后（不看到方法来源）标记为 supported / unsupported / ambiguous / not observable。

### 基线方法
- 3DSSG Baseline, SGFN-style 3D GNN, SceneGraphFusion, Open3DSG, ConceptGraphs-query, OpenFunGraph, FROSS
- Text Completion（基于短语相似度和分类器置信度）
- Object-Prior Completion（基于物体对统计）

### 模拟规划结果（非真实复现值）

> 以下所有数值为 **simulated manuscript-planning numbers**，未实际复现，仅供参考实验设计模式。

**闭集 3DSSG/3RScan 关系预测（表 2）**：

| 方法 | R@50 | R@100 | mR@50 | mR@100 |
|------|------|-------|-------|--------|
| RelWitness | **69.3** | **74.1** | **38.4** | **41.7** |
| Text Completion | 66.8 | 71.5 | 33.9 | 37.2 |
| Object-Prior Completion | 67.5 | 72.0 | 32.6 | 35.8 |
| OpenFunGraph | 65.5 | 70.2 | 30.4 | 34.5 |
| Open3DSG | 64.3 | 69.1 | 29.2 | 32.8 |

**开放词汇 OV-3DSSG（表 3）**：

| 方法 | S-mR@50 | U-mR@50 | HM@50 | S-mR@100 | U-mR@100 | HM@100 |
|------|---------|---------|-------|----------|----------|--------|
| **RelWitness** | **34.2** | **25.7** | **29.3** | **36.8** | **27.9** | **31.7** |
| Text Completion | 31.7 | 20.8 | 25.1 | 34.0 | 22.5 | 27.1 |
| OpenFunGraph | 30.4 | 15.6 | 20.6 | 32.7 | 17.2 | 22.5 |

**缺失关系审计（表 4）**：

| 方法 | VMR↑ | WP↑ | MVWA↑ | Halluc.↓ | Redun.↓ |
|------|------|-----|-------|---------|---------|
| **RelWitness** | **47.6** | **78.9** | **72.4** | **12.7** | **8.8** |
| Text Completion | 49.4 | 60.8 | 52.7 | 28.6 | 24.5 |
| Open3DSG | 32.8 | 63.1 | 56.2 | 23.7 | 18.4 |

**按见证族分解 U-mR@50（表 5）**：

| 族 | U-mR@50 | WP | MVWA | Halluc.↓ | Gain |
|-----|---------|-----|------|---------|------|
| Support | 29.8 | 82.4 | 76.5 | 9.8 | +7.1 |
| Containment | 27.3 | 80.1 | 73.9 | 11.2 | +6.4 |
| Orientation | 23.7 | 73.2 | 66.1 | 15.9 | +5.1 |

**消融研究（表 6）**：

| 配置 | U-mR@50 | HM | VMR | WP | MVWA | Halluc.↓ |
|------|---------|-----|-----|-----|------|---------|
| 基线 OV-3DSG | 13.1 | 17.9 | 29.7 | 61.5 | 53.2 | 25.8 |
| +RGB | 16.2 | 21.1 | 36.4 | 66.9 | 58.7 | 21.4 |
| +Depth | 18.7 | 23.3 | 40.6 | 70.8 | 63.5 | 18.1 |
| +3D geom | 21.4 | 25.7 | 43.5 | 74.2 | 67.9 | 15.6 |
| +Multi-view | 22.9 | 27.0 | 44.8 | 76.1 | 70.2 | 14.1 |
| +Null test | 23.8 | 27.7 | 45.1 | 77.8 | 71.1 | 13.2 |
| **Full** | **25.7** | **29.3** | **47.6** | **78.9** | **72.4** | **12.7** |

**跨数据集迁移 ScanNet-OV（表 11）**：

| 方法 | S-mR | U-mR | HM | WP | Halluc.↓ | Redun.↓ |
|------|------|------|-----|-----|---------|---------|
| **RelWitness** | **31.0** | **22.4** | **26.0** | **74.6** | **14.9** | **10.6** |
| OpenFunGraph | 27.4 | 13.9 | 18.4 | 62.5 | 23.7 | 17.2 |

**效率（表 14）**：
- 参数量：166M（vs Open3DSG 134M）
- 训练时间：1.6×（基线 = 1.0×）
- FPS：4.7（最慢）
- GPU 内存：19.2G

## 关键发现（规划值）

1. **Unseen 关系大幅提升**：U-mR@50 从 Text Completion 的 20.8 → **25.7**，见证族分解中 Support 系 U-mR@50 达 **29.8**。
2. **验证缺失精度高**：WP **78.9%**（vs Text Completion 60.8%），说明视觉-几何见证有效过滤语言驱动的假阳性。
3. **幻觉率低**：Halluc. **12.7%**（vs Text Completion 28.6%），得益于多模态见证的保守策略。
4. **冗余输出少**：Redun. **8.8%**（vs Text Completion 24.5%），见证一致解码有效合并语义近似的重叠短语。
5. **消融分析**：每个见证组件贡献渐进收益，3D 几何和多视角持久性影响最大。

## 失败模式分析（表 15）

| 失败类别 | 占比 | 主要影响族 | 典型影响 |
|---------|------|-----------|---------|
| 几何噪声 | 31.6% | support/attach | 假拒绝 |
| 语义粒度 | 24.8% | support/proximity | 冗余 |
| 单视角模糊 | 22.1% | orientation/interact | 不确定 |
| 不可观测短语 | 15.3% | functional | 不确定 |
| 解析器不匹配 | 6.2% | directional | 假接受/假拒绝 |

## 局限与待验证

- 所有数值为规划值，需实际复现验证
- 依赖高质量物体定位（mask 质量退化→WP 从 78.9 降至 68.2）
- 面向离线场景图构建，在线部署需蒸馏或轻量见证探针
- 功能性和交互性关系的可观测性仍有限（Fleiss κ 分别 0.47 和 0.54）

## 关联论文

- [CCL-3DSGG: CLIP-Driven Open-Vocabulary 3D Scene Graph Generation](ccl-3dsgg-clip-driven-open-vocabulary-3d-scene-graph-generation.md) — 同样面向开放词汇 3D SGG，但 RelWitness 聚焦不完整监督问题
- [ConceptGraphs](https://arxiv.org/abs/2402.03628) — 开放词汇 3D 物体中心图，RelWitness 在其基础上增加关系见证
- [Open3DSG](https://arxiv.org/abs/2402.03628) — 点云开放词汇 3D SGG，提出来即可查询物体和开放集关系
- [OpenFunGraph](https://arxiv.org/abs/2503.19199) — 功能性 3D 场景图
