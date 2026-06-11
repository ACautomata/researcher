# Fixed External Cameras as Common Prior Maps for Active 3D Scene Graph Generation

## Metadata

- **Title (EN):** Fixed External Cameras as Common Prior Maps for Active 3D Scene Graph Generation
- **Authors:** Giorgia Modi, Davide Buoso, Giuseppe Averta, Daniele De Martini
- **Affiliations:** University of Oxford (MRG), Politecnico di Torino (VANDAL)
- **Venue:** arXiv preprint, May 2026
- **arXiv ID:** [2605.18184](https://arxiv.org/abs/2605.18184v1) [cs.RO]
- **Evidence Level:** full-paper
- **Status:** active
- **Code:** Not publicly available (not mentioned)
- **Domain:** scene-graph
- **Tags:** `3d-scene-graph`, `active-perception`, `common-prior-maps`, `rgb-only`, `external-cameras`

## 论文简介

本文提出一个仅依赖 RGB 图像的框架，用于主动、增量式 3D 场景图（3DSG）生成。核心创新在于将固定外部 RGB 摄像头（如建筑物中已部署的监控摄像头）的观测视为 **Common Prior Maps (CPMs)**——即在机器人运动开始之前提供环境和局语义几何先验的宽视角场景信息。该框架通过 RGB-only 前馈 3D 重建模型（MapAnything）统一处理所有摄像头输入（车载和外部），无需深度传感器或硬件修改。构建的场景图进一步被主动语义探索模块（ASP）利用，通过最大化信息增益选择下一个最佳视角（NBV），逐步完善初始先验。

## 核心贡献

1. **RGB-only 3DSG 管线**：完全舍弃深度传感器，仅用 RGB 图像实现 3D 场景图生成，通过 MapAnything [8] 进行前馈度量和姿态估计。
2. **外部摄像头作为 CPM**：首次将固定外部摄像头观测作为结构化的语义几何先验融入 3DSG 管线，所有摄像头（车载/外部）在统一的 RGB-only 框架中同等对待。
3. **主动语义探索循环**：将 ASP [18] 嵌入探索循环，以当前场景图的结构化状态驱动 NBV 选择，用 LLM（gemini-2.5-pro）进行场景补全推理。
4. **确定性几何关系边**：替代 ConceptGraphs 的专有 LLM 关系推断，使用固定优先级的几何规则（on top of / supported by / under / over / inside / next to）生成可复现的场景图边。

## Method

### 系统架构

系统以增量感知-行动循环运行（Figure 1）：

1. **t=0（初始化）**：一个或多个固定外部摄像头的 RGB 观测经 RGB-only 3DSG 管线处理，初始化点云和场景图，提供语义几何结构。
2. **t>0（探索循环）**：机器人从当前位置获取 RGB 图像，同管线处理以更新点云 $P_t$ 和场景图 $G_t$。ASP 模块基于当前图选择 NBV $v_{t+1}$，机器人移动至此视角获取新观测，循环迭代。

### RGB-Only 3DSG 生成

- **深度和姿态估计**：使用 MapAnything [8] 从 RGB 图像集合中预测每视图像素射线方向、深度图（up-to-scale）、相机姿态（以第一帧为参照系）和全局度量缩放因子 $m \in \mathbb{R}$。
- **场景图构建**：基于 ConceptGraphs [12] 管线：SAM [21] 提取类无关实例掩码 → CLIP [22] 编码语义描述 → 掩码投影到 3D → 多视图关联合并为 3D 对象节点。关系边通过确定性几何规则生成，基于有向 3D 边界框的垂直/水平/包含关系，每个有序对最多一条边。

### Active Semantic Perception (ASP)

ASP [18] 以当前场景图为结构化状态，由 LLM（gemini-2.5-pro）推理未观测场景的可能补全。信息增益定义为：

$$I(Y_{k+1}; G_k \mid x) = H(Y_{k+1} \mid x) - H(Y_{k+1} \mid x, G_k)$$

其中 $H(\cdot)$ 为香农熵。选择最大化信息增益的视点作为 NBV。

## 实验与结果

### 数据集
- **Replica** [24]：7 个场景（room0-2, office0-3），用于静态管线验证
- **ReplicaCAD** [26]：6 个公寓场景，用于主动探索评估
- **ReplicaCAD 变体**：90 个场景，包括复杂公寓（~123 对象）和简单家具房间（~25 大对象），用于静态 CPM 评估

### 实验 1：静态 RGB-Only 3DSG 管线验证

对比 ConceptGraphs（CG，使用深度+姿态）与 RGB-only 变体（CG-RGB，使用 MapAnything 预测）在 Replica 7 场景上的节点质量：

| 方法 | Precision ↑ | Recall ↑ | F1-score ↑ |
|------|------------|---------|------------|
| CG | 0.686 ± 0.05 | 0.401 ± 0.10 | 0.499 ± 0.08 |
| CG-RGB (ours) | 0.615 ± 0.07 | 0.436 ± 0.12 | **0.500 ± 0.08** |

**关键发现**：RGB-only 变体达到几乎相同的 F1 分数（0.500 vs 0.499），Recall 甚至从 0.401 提高到 0.436，但因 MapAnything 的噪声深度导致 Precision 略有下降（0.686 → 0.615）。

### 实验 2：CPM 初始化下的主动探索

在 Habitat 模拟器 [25] 上使用 ReplicaCAD 公寓场景，gemini-2.5-pro 作为 LLM，10 个起始位置 × 30 步探索：

| 设置 | 初始节点数 | 初始 Recall | 第30步节点数 | 第30步 Recall |
|------|-----------|-----------|-------------|--------------|
| ASP (only onboard) | ~23 | ~0.15 | ~98 | ~0.47 |
| ASP + CPM (1 external cam) | ~40 | ~0.26 | ~107 | ~0.56 |

**关键结果**：单外部相机将初始 Recall 提高 **+79%**（0.15→0.26），初始节点数增加 **+74%**（23→40），优势在 30 步探索中持续保持。

### 实验 3：外部摄像头基础设施作为独立 CPM

270 组实验，覆盖 90 个 ReplicaCAD 场景，仅使用 1-3 个外部固定摄像头（无移动机器人）：

| 场景类型 | #Cam | Precision ↑ | Recall ↑ | F1-score ↑ |
|---------|------|------------|---------|------------|
| 公寓（复杂） | 1 | 0.770 ± 0.054 | 0.198 ± 0.030 | 0.315 ± 0.041 |
| 公寓（复杂） | 2 | 0.741 ± 0.036 | 0.232 ± 0.030 | 0.353 ± 0.036 |
| 公寓（复杂） | 3 | 0.698 ± 0.031 | 0.301 ± 0.029 | 0.421 ± 0.030 |
| 家具房间（简单） | 1 | 0.566 ± 0.087 | 0.398 ± 0.071 | 0.465 ± 0.073 |
| 家具房间（简单） | 2 | 0.540 ± 0.077 | 0.487 ± 0.071 | 0.510 ± 0.067 |
| 家具房间（简单） | 3 | 0.486 ± 0.060 | 0.555 ± 0.065 | 0.516 ± 0.055 |

**关键发现**：3 个静态外部摄像头在公寓场景 Recall 达 0.301，家具房间达 0.555。Precision 随相机数增加略降（重叠重复片段），但整体 F1 持续提升。表明固定 RGB 摄像头可独立作为高质量的 CPM。

## 局限与展望

- 实验仅在仿真环境（Replica、ReplicaCAD、Habitat）中验证，未涉及真实场景
- 关系边生成仅使用确定性几何规则，未评估空间关系质量
- MapAnything 的噪声深度估计导致 Precision 下降
- 依赖 ConceptGraphs 的 SAM+CLIP 流程，受限于基础模型的开集检测能力
- 未验证外部摄像头与车载摄像头之间的外参标定对系统的影响

## 关联论文

- [ConceptGraphs: Open-Vocabulary 3D Scene Graphs for Perception and Planning](zing-3d-zero-shot-incremental-3d-scene-graphs.md) — 基础管线
- [Active Semantic Perception (ASP)](tempura-unbiased-video-scene-graph-generation.md) — 场景图驱动的主动感知框架
- [MapAnything: Universal Feed-Forward Metric 3D Reconstruction](ccl-3dsgg-clip-driven-open-vocabulary-3d-scene-graph-generation.md) — RGB-only 3D 重建
- [Hi-Dyna Graph: Hierarchical Dynamic Scene Graph for Robotic Autonomy](2025-05-30-hidynagraph.md) — 机器人场景图相关
- [SGR3: Model Scene Graph Retrieval and Reasoning Model for 3D](sgr3-model-scene-graph-retrieval-reasoning-model-3d.md) — 3D 场景图推理

## Related Work

- **3D Scene Graphs**: Hydra [10], SceneGraphFusion [11], ConceptGraphs [12]
- **Active Perception**: Frontier-based [14], density-based [15], semantic scene completion [16], 3DGS-based [17], ASP [18]
- **External Sensing in Robotics**: Visual servoing [19], VLM-guided navigation [20]
