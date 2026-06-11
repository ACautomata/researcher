---
title: Hi-Dyna Graph: Hierarchical Dynamic Scene Graph for Robotic Autonomy in Human-Centric Environments
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - dynamic-scene-graph
  - hierarchical-scene-graph
  - robotic-manipulation
  - autonomous-navigation
  - llm-reasoning
  - open-vocabulary
  - downstream-application
raw_sources:
  - ../../../sources/scene-graph/2025-05-30-hidynagraph.pdf
  - ../../../sources/scene-graph/2025-06-09-hidynagraph.txt
paper:
  title: Hi-Dyna Graph: Hierarchical Dynamic Scene Graph for Robotic Autonomy in Human-Centric Environments
  authors:
    - Jiawei Hou
    - Xiangyang Xue
    - Taiping Zeng
  year: 2025
  venue: arXiv preprint (under review)
  arxiv: "2506.00083"
  code: "https://anonymous.4open.science/r/Hi-Dyna-Graph-B326"
classification:
  label: Hierarchical Dynamic Scene Graph
  task:
    - Scene Graph Generation
    - Robotic Manipulation
    - Autonomous Navigation
    - Dynamic Scene Understanding
  method_family: Hierarchical Scene Graph
  modality: RGB-D
  datasets:
    - OpenPVSG
    - Ego4D
    - Epic-Kitchens
    - VIDOR
    - Custom campus-building dataset
  metrics:
    - R/mR@20/50/100
    - Vertices Accuracy (V. Acc.)
    - Edges Accuracy (E. Acc.)
evidence_level: full-paper
---

## Citation

Hou, J., Xue, X., Zeng, T. "Hi-Dyna Graph: Hierarchical Dynamic Scene Graph for Robotic Autonomy in Human-Centric Environments." arXiv:2506.00083, May 2025. [arXiv](https://arxiv.org/abs/2506.00083) | [Code (anonymous)](https://anonymous.4open.science/r/Hi-Dyna-Graph-B326)

## One-Sentence Contribution

提出 Hi-Dyna Graph，一种将持久全局拓扑图（房间连通性、大型家具）与局部动态语义子图（物体位置关系、人-物交互）结合的分层动态场景图架构，通过 LLM 驱动推理实现机器人在人中心动态场景中的自主导航和操作。

## Problem Setting

- **目标**：在持续变化的人中心环境中，让机器人能高效管理多模态场景信息、推理进行中的活动、自主生成和执行任务
- **挑战**：
  - 现有拓扑图（如 ConceptGraph, Topo-Field）假设静态场景，无法建模瞬态物体关系（如炊具被移动）
  - 稠密神经表示（NeRF, 3D Gaussian Splatting）密集计算开销大，下游任务查询效率低
  - 视频场景图生成方法（PSG4D）缺乏全局空间上下文和长期历史状态追踪，被动观察而非主动感知
- **设定**：从带位姿的 RGB-D 输入构建全局静态拓扑图 + 从环境/第一人称视频构建局部动态子图，通过 LLM 推理统一图理解指导机器人规划

## Method

### 架构概览

Hi-Dyna Graph 的形式化定义为 **G = {Gs, Gd}**：
- **Gs = (Vs, Es)**：全局静态图，从带位姿 RGB-D 图像构建
- **Gd = (Vd, Ed)**：局部动态图，从视频流逐步构建

### 全局静态图 Gs

1. 对带位姿的 RGB-D 图像序列编码视觉语言嵌入（视觉 CLIP 特征），根据深度和位姿提升到 3D 空间
2. 通过查询嵌入点云获取区域（room-level）和宏对象（大型家具），形成图顶点 Vs = (Vr, Vo)
3. 应用静态对象过滤：体积阈值（2m³）和语义过滤筛选罕见移动的元素
4. HOV-SG 的分层聚类 + Topo-Field 的拓扑图结构作为构建基础

### 局部动态图 Gd

1. 从视频流中预测二进制对象 mask 管（UniTrack 跨帧关联）
2. 获取对象标签和相互关系：Pr(Vd, Ed | Ft) = Pr(Mt, Ot, Rt | Ft)
3. 采用 FC-CLIP 框架（ConvNeXt-Large CLIP backbone，LAION-2B 预训练，无需微调）进行开放词汇分割
4. Spatial-Temporal Transformer 编码器进行关系预测
5. 关系先验：人更可能是 subject，大型家具更可能是 object

### 混合架构

- 通过语义和空间约束将动态子图锚定到全局拓扑
- 10 秒滑动窗口提取最新视频序列，增量更新动态子图
- 体积过滤（vthr=2m³）从动态流中分离静态对象

### LLM 推理

- 统一场景图作为结构化知识库，通过 prompt 模板输入 LLM
- prompt 内容：场景知识（全局布局 + 局域关系）、技能原语（导航、取放）、指令
- LLM 作为 reasoner 解释统一图、推理潜在任务触发（如未洗的盘子→启动清理）、生成可执行指令
- 计划随图演变实时调整

## Experiments

### 实验设置

**Relation Prediction**（OpenPVSG 数据集）：
- 基线方法：3DSGG, PSG4D
- 分割：FC-CLIP（ConvNeXt-Large CLIP backbone），不微调
- 跟踪：UniTrack
- 关系预测：候选对过滤 + Spatial-Temporal Transformer 编码器
- 评估：in-vocabulary 和 open-vocabulary 设置下的 R/mR@20/50/100

**动态组件评估**：
- 对比方法：ConceptGraph*, HOV-SG, Topo-Field
- 评估时间点：0 min, 10 min, 20 min, 30 min
- 每 1 分钟评估一次，Hi-Dyna 使用 10 秒滑动窗口更新
- 基线从全部图像序列从头重建
- 指标：Vertices Accuracy (V. Acc.), Edges Accuracy (E. Acc.)

**消融实验**：
1. 静态对象过滤：体积/语义消融，对比 HOV-SG, Topo-Field，体积阈值 2m³
2. 动态图生成：消融 backbone（ViT vs CNN-CLIP）和关系对先验策略
- 评估数据集：单楼层校园建筑（约 3029.4m²），覆盖多种功能区域（实验室、咖啡厅、展厅等）
- 多时间段采集，覆盖不同人类活动变化

**真实机器人部署**：
- 平台：SLAMTEC Hermes 移动底座 + SIASUN GCR5-910 机械臂（或 Franka Panda）+ RealSense D435i + NVIDIA RTX 4090（图构建）/ Intel i9-10885H + GTX 1650ti（机器人控制）
- 场景：校园咖啡厅助理，跨房间完成咖啡取送
- 环境相机 5Hz 记录，10s 滑动窗口

## Results

### Relation Prediction（Table 1, OpenPVSG）

| Method | In-vocab R@20 | In-vocab R@50 | In-vocab R@100 | Open-vocab R@20 | Open-vocab R@50 | Open-vocab R@100 |
|--------|:---:|:---:|:---:|:---:|:---:|:---:|
| 3DSGG | 3.37 | 3.56 | 4.52 | 3.42 | 3.98 | 4.97 |
| PSG4D | 6.15 | 6.58 | 6.83 | 6.61 | 7.02 | 7.11 |
| Ours (full) | **8.40** | **9.75** | **10.56** | **11.52** | **11.91** | **12.24** |

Open-vocabulary 设置下，Hi-Dyna Graph 大幅领先 PSG4D（R@50: 11.91 vs 7.02），优势尤为突出。

### 动态图结构（Table 2, 多时间步）

在 30 分钟跨度内，Hi-Dyna 的滑动窗口增量更新取得了与从头重建静态方法相当的图质量：
- V. Acc. 维持在 0.71-0.76（Topo-Field 静态为 0.69-0.77）
- E. Acc. 维持在 0.90-0.95（Topo-Field 静态为 0.93-0.96）
- 这表明滑动窗口更新策略在大幅节省计算的同时保持了图结构质量

### 静态过滤消融（Fig. 5）

- 提出的静态对象过滤策略在不同时间步保持稳定的顶点精度，退化最小
- 人类活动对 HOV-SG 和 Topo-Field 的影响显著更大，多次活跃事件导致精度大幅下降
- 该方法有效识别并优先保持稳定场景成分（功能区域、固定家具）

### 消融——动态图生成（Table 1, 消融行）

- "w/o CNN-CLIP"（使用 ViT backbone）：In-vocab R@50 从 9.75 降至 8.69
- "w/o relation pair prior"：Open-vocab R@20 从 11.52 降至 9.64，Open-vocab R@50 从 11.91 降至 9.82

### 真实机器人演示

机器人作为咖啡厅助理自主完成：接收咖啡订单→导航到咖啡厅→等待咖啡制作→取拿咖啡→导航到实验室→放置咖啡。全程自主，无需手动干预。

## Limitations

1. **延迟**：滑动窗口更新存在固有延迟，在快速演变场景中可能受限
2. **关系预测绝对性能低**：R@50 < 12%，即使在最佳设置下。复杂场景的关系识别仍有显著提升空间
3. **预训练依赖**：需要离线场景图构建（全局静态图）预处理阶段，尚未实现完全实时
4. **泛化性有限**：单一机器人平台 + 特定场景（咖啡厅助理）验证；无差分定位环境的适配性、其他机器人平台的迁移性有待验证
5. **底层模块级联误差**：动态场景图质量依赖底层分割（FC-CLIP）、跟踪（UniTrack）和关系预测模块的精度

## Reusable Claims

- **分层动态场景图优于纯静态图**：按时空属性将场景分离为静态和动态成分，在保持导航级效率的同时获得可更新的语义细节，30 分钟动态更新与从头重建的准确率相当（V. Acc. ~0.71-0.76）
- **滑动窗口增量更新有效**：10s 滑动窗口策略避免了全图重建，在 30 分钟内维持与静态从头构建相当的图质量
- **LLM 作为图推理器可行**：结构化场景图输入 LLM，可以实现基于环境变化的自主任务触发和执行指令生成
- **静态对象过滤提高鲁棒性**：基于体积（vthr=2m³）和语义的过滤策略有效减少人类活动对静态图构建的干扰
- **关系先验**："人作为 subject，大型家具作为 object"的静态场景先验对开放词汇关系预测有改进

## Connections

- 建立于 **PVSG (Panoptic Video Scene Graph)** [Yang et al., CVPR 2023] 框架和 OpenPVSG 评测
- 直接对比方法：**3DSGG**, **PSG4D**（关系预测），**ConceptGraph\***, **HOV-SG**, **Topo-Field**（场景图结构）
- 前期工作：第一作者之前的 **Topo-Field** [Hou et al., RA-L 2025] 是全局静态图的构建基础之一
- 分割框架：**FC-CLIP** [Yu et al., NeurIPS 2023]
- LLM 推理定位：类似 VLMap 等结合拓扑图+LLM 的工作
- 同作者相关工作：**ELA-ZSON** [Hou et al., arXiv 2025]——面向零样本导航的层次规划
- SGG 下游应用方向：展示了从视频场景图生成到机器人操作和导航的完整落地链路

## Open Questions

- 动态场景图如何扩展到更大规模（整栋建筑多层）和更长时间跨度（数小时/天）？
- 关系预测 Recall 较低（<12%），如何通过更丰富的时序建模或外部知识提升 open-vocabulary 关系识别？
- 实现完全实时动态场景图构建（消除离线预处理阶段）需要哪些效率优化？
- 该架构在双手机械臂、四足机器人等不同形态机器人上的适配性和迁移性如何？
- LLM 推理的延迟和可靠性如何影响端到端任务执行的成功率？
- 场景图的表示能否与 skill-level 控制（如机器人操作的主策略）更加紧密结合？

## Provenance

- Source file: `sources/scene-graph/2025-05-30-hidynagraph.pdf`
- Extracted text: `sources/scene-graph/2025-06-09-hidynagraph.txt`
- Evidence level: full-paper（全文精读，实验设置、表格数据和消融结果均已捕获）
- Analyzed by: autoresearch subagent, 2026-06-09
