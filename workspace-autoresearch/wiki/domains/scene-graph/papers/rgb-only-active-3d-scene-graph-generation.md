---
title: RGB-only Active 3D Scene Graph Generation for Indoor Environments
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - 3D-scene-graph
  - active-perception
  - RGB-only
  - next-best-view
  - indoor-mobile-robots
paper:
  title: "RGB-only Active 3D Scene Graph Generation for Indoor Mobile Robots"
  authors:
    - Giorgia Modi
    - Davide Buoso
    - Giuseppe Averta
    - Daniele De Martini
  year: 2026
  venue: arXiv preprint
  arxiv: "2605.18197"
  code: null
  project: null
classification:
  label: Active 3D Scene Graph Generation
  task:
    - 3D scene graph generation
    - active exploration
    - next-best-view planning
  method_family:
    - ConceptGraphs-based
    - MapAnything-based
    - Active Semantic Perception (ASP)
  modality: RGB-only
  datasets:
    - Replica
    - ReplicaCAD
  metrics:
    - F1-score
    - Precision
    - Recall
    - node count
evidence_level: full-paper
raw_sources:
  - raw/sources/2026-06-09-rgb-only-active-3d-scene-graph-generation.pdf
  - raw/sources/2026-06-09-rgb-only-active-3d-scene-graph-generation.txt
related_pages:
  - domains/scene-graph/papers/conceptgraphs-open-vocabulary-3d-scene-graphs.md
  - domains/scene-graph/papers/zing-3d-zero-shot-incremental-3d-scene-graphs.md
  - domains/scene-graph/papers/incremental-3d-scene-graph-prediction-from-rgb-sequences.md
---

# RGB-only Active 3D Scene Graph Generation for Indoor Environments

## Citation

> Modi, G., Buoso, D., Averta, G., & De Martini, D. "RGB-only Active 3D Scene Graph Generation for Indoor Mobile Robots." arXiv preprint arXiv:2605.18197, 2026.

## One-Sentence Contribution

首次提出纯RGB输入的主动式3D场景图增量构建框架，通过结合前馈3D重建、开放词汇语义映射和LLM驱动的语义探索，消除对深度传感器的依赖，并实现多来源RGB视图（机载+外部固定相机）的异构融合。

## Problem Setting

- **目标**：在仅使用RGB相机的情况下，让移动机器人在探索过程中增量构建3D场景图（3DSG）
- **挑战**：
  1. 现有3DSG方法依赖RGB-D或LiDAR获取度量深度，限制了部署场景
  2. 现有管道多为被动式，沿预设轨迹采集，不会根据已构建场景图选择视点
  3. 缺少支持异构RGB输入（机载相机+外部固定相机）的统一框架
- **机器人场景**：室内移动机器人在未知环境中自主探索，需要同时构建语义和几何层次的场景表示

## Method

### 系统架构

系统运行在增量式感知-动作循环中（Fig. 1）：

1. **RGB-only 3DSG生成管道**（第三章B节）：
   - **深度和位姿估计**：使用MapAnything [11] 从单张或一组RGB图像前馈推断每视图像素射线方向、up-to-scale深度图、位姿和全局度量尺度因子，无需SLAM或光度优化
   - **开放词汇场景图构建**：使用ConceptGraphs管道：SAM提取类别无关实例掩码 → CLIP嵌入语义描述 → MapAnything深度/位姿将掩码投影至3D → 多视图关联增量合并为3D对象节点
   - **边关系**：确定性几何过程评估有序对象对的谓词（on top of / supported by、under / over、inside、next to），每对最多分配一个谓词
   - 基于基础模型（SAM、CLIP），无需预定义类别

2. **主动语义感知（ASP）**（第三章C节）：
   - 使用LLM（gemini-2.5-pro）根据当前场景图采样场景补全假设
   - 计算每个候选视点x的期望信息增益: I(Yₖ₊₁; Gₖ | x) = H(Yₖ₊₁ | x) − H(Yₖ₊₁ | x, Gₖ)
   - 场景图既是目标表示也是引导探索的认知结构
   - 几何基线：Surface Edge Explorer (SEE) [17]，基于测量密度识别前沿点

3. **多视图外部相机集成**（第三章D节）：
   - 外部固定RGB相机图像通过MapAnything以相同方式处理，无需标定
   - 提供鸟瞰全局视图，引导场景图初始化并辅助探索

### 技术细节

- 3D关系判定阈值：固定超参数，每个数据集调试一次，跨所有实验一致
- 关系谓词优先级：on top of / supported by > under/over > inside > next to

## Experiments

### 实验设置

| 项目 | 范围 |
|------|------|
| **硬件** | 无特定硬件需求；在Habitat模拟器中评估 |
| **模型** | MapAnything（深度/位姿推断）、SAM（掩码）、CLIP（语义嵌入）、gemini-2.5-pro（ASP的LLM） |
| **评估协议** | 节点质量评估使用SentenceTransformer嵌入联合语义相似度和3D定位约束匹配，无关系GT标注可用 |
| **实验配置** | 10个不同起始位置、30个探索步骤；6个ReplicaCAD公寓场景，报告公寓3的代表性结果 |

### 实验1：静态RGB-only 3DSG管道验证

**数据集**：Replica（7个场景：room0-2, office0-3）

**比较**：原始ConceptGraphs（GT深度+位姿）vs. CG-RGB（MapAnything预测深度+位姿）

**结果**（Table I）：

| 方法 | Precision ↑ | Recall ↑ | F1-score ↑ |
|------|:-----------:|:---------:|:-----------:|
| CG（GT深度） | 0.686 ± 0.05 | 0.401 ± 0.10 | 0.499 ± 0.08 |
| CG-RGB（ours） | 0.615 ± 0.07 | 0.436 ± 0.12 | **0.500 ± 0.08** |

F1-score持平。MapAnything噪声深度略微降低precision，但反直觉地提升了recall（避免过度合并邻近物体）。

### 实验2：主动探索评估

**数据集**：ReplicaCAD（6个公寓场景）

**比较**：SEE（几何基线） vs. ASP（语义驱动）

**训练设置**：30个探索步骤，10个不同起始位置。Habitat模拟器处理局部导航。

**关键结果**（Fig. 2）：
- **ASP在第30步检测到约110个对象节点**，接近GT总数124
- **SEE仅检测到约45个节点**
- **ASP recall = 0.54 vs. SEE recall = 0.22**，ASP recall是SEE的2.45倍
- 三十次"智能"移动匹配了数百帧被动轨迹的质量

### 实验3：多视图外部相机集成

**设置**：在90个ReplicaCAD场景（复杂公寓≈123对象 + 简单家具房间≈25对象）上使用1-3个固定外部相机进行270次实验。

**结果**（Table II）：

| 场景 | #Cam | Precision ↑ | Recall ↑ | F1-score ↑ |
|:----:|:----:|:-----------:|:---------:|:-----------:|
| 公寓 | 1 | 0.770 ± 0.054 | 0.198 ± 0.030 | 0.315 ± 0.041 |
| 公寓 | 2 | 0.741 ± 0.036 | 0.232 ± 0.030 | 0.353 ± 0.036 |
| 公寓 | 3 | 0.698 ± 0.031 | 0.301 ± 0.029 | 0.421 ± 0.030 |
| 家具房 | 1 | 0.566 ± 0.087 | 0.398 ± 0.071 | 0.465 ± 0.073 |
| 家具房 | 2 | 0.540 ± 0.077 | 0.487 ± 0.071 | 0.510 ± 0.067 |
| 家具房 | 3 | 0.486 ± 0.060 | 0.555 ± 0.065 | 0.516 ± 0.055 |

外部相机作为主动探索的bootstrap（Fig. 2）：
- 单次过顶外部相机将SEE起始节点从16提升至37（+125%），ASP从23提升至36（+57%）
- 初始recall：SEE从0.12→0.27（+130%），ASP从0.15→0.27（+80%）

## Results

### 核心数字发现

1. **RGB-only与深度基线精度持平**：CG-RGB F1-score 0.500 vs. CG（GT深度）0.499 —— 差异在标准差范围内
2. **语义主动探索优于几何探险**：30步后ASP检测~110节点 vs. SEE~45节点；ASP recall 0.54 vs. SEE 0.22，检测物体数2.4倍
3. **外部相机有效引导**：单帧外部视角提升初始检测125%（SEE）和57%（ASP）
4. **纯外部相机设置**：3相机在公寓场景F1=0.421，在家具房间F1=0.516
5. 相机数量增加时precision略有下降（多视图重复片段），但net F1持续改善

### 可复用Claims

> **Claim**: RGB-only管道使用MapAnything替代GT深度+位姿，在3DSG节点预测中可实现与深度方法持平的F1-score（0.500 vs. 0.499）。
> **Evidence**: Table I，Replica 7场景
> **Confidence**: High
> **Scope**: 基础模型（SAM+CLIP）场景图，MapAnything前馈3D重建

> **Claim**: 语义驱动的主动探索（ASP）比几何前沿探索（SEE）在相同步数内发现超过2倍的物体（~110 vs. ~45），recall翻倍（0.54 vs. 0.22）。
> **Evidence**: Fig. 2，ReplicaCAD公寓3场景，30步，10个起始位置
> **Confidence**: High
> **Scope**: 使用gemini-2.5-pro作为LLM，Habitat模拟器

> **Claim**: 外部固定RGB相机可作为有效的场景图初始化源，单视角即可提升初始检测57-125%。
> **Evidence**: Fig. 2外部相机增强试验
> **Confidence**: High
> **Scope**: ReplicaCAD公寓场景

## Limitations

1. **边关系的验证受限**：评估仅针对节点（因数据集缺少关系GT），边生成的质量需人工验证
2. **仅Replica/ReplicaCAD合成场景测试**：未在真实室内环境（如ScanNet、Matterport3D）验证
3. **MapAnything的泛化边界**：极端光照、低纹理、高反射表面等挑战性条件下的深度估计质量未分析
4. **ASP依赖外部LLM API**：对llm推理质量、延迟和成本有依赖
5. **关系谓词有限**：仅支持4类空间关系（on top of / supported by、under/over、inside、next to），缺少功能关系

## Connections

- **ConceptGraphs [8]**：本文的语义映射核心，本文将其扩展到RGB-only和主动探索场景
- **MapAnything [11]**：提供RGB-only的3D重建能力，替代传统RGB-D SLAM
- **Active Semantic Perception (ASP) [12]**：本文采用其语义探索框架，但原始方法假设深度输入
- **Surface Edge Explorer (SEE) [17]**：几何探索基线方法
- 与[[zing-3d-zero-shot-incremental-3d-scene-graphs.md]]类似支持增量3DSG构建，但本文强调主动视点选择而非零样本增量
- 与[[incremental-3d-scene-graph-prediction-from-rgb-sequences.md]]类似使用RGB序列，但本文使用主动而非被动

## Open Questions

1. **真实世界部署**：从Habitat模拟到真实机器人，MapAnything在真实室内场景的泛化性能？
2. **长期大规模场景图**：在更大空间（整层办公楼）中，增量构建的场景图如何保持一致性？
3. **关系的主动探索**：本文仅评估了节点检测，未来可探索针对关系推断的信息增益导向
4. **多机器人协同**：外部相机和多个机器人的RGB视图如何更高效地集成？
5. **任务驱动的探索**：探索目标是否可以由下游任务（如导航、操作）动态指定？

## Provenance

- PDF源文件：`raw/sources/2026-06-09-rgb-only-active-3d-scene-graph-generation.pdf`（1.2 MB）
- 全文提取文本：`raw/sources/2026-06-09-rgb-only-active-3d-scene-graph-generation.txt`
- 提取方法：PyMuPDF全文提取
- 证据等级：full-paper（已阅读全文）
