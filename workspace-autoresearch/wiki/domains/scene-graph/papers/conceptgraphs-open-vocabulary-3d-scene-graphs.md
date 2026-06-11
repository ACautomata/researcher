---
title: "ConceptGraphs: Open-Vocabulary 3D Scene Graphs for Perception and Planning"
authors: ["Qiao Gu", "Ali Kuwajerwala", "Sacha Morin", "Krishna Murthy Jatavallabhula", "Bipasha Sen", "Aditya Agarwal", "Corban Rivera", "William Paul", "Kirsty Ellis", "Rama Chellappa", "Chuang Gan", "Celso Miguel de Melo", "Joshua B. Tenenbaum", "Antonio Torralba", "Florian Shkurti", "Liam Paull"]
venue: "CVPR 2024"
arxiv: "2309.16650"
project: "https://concept-graphs.github.io/"
code: "https://github.com/concept-graphs/concept-graphs"
year: 2024
tags: ["scene-graph-generation", "3d-scene-graph", "open-vocabulary", "CVPR-2024"]
evidence_level: "full-paper"
domain: "scene-graph"
status: "active"
---

# ConceptGraphs: Open-Vocabulary 3D Scene Graphs for Perception and Planning

## 基本信息

- **标题**: ConceptGraphs: Open-Vocabulary 3D Scene Graphs for Perception and Planning
- **作者**: Qiao Gu, Ali Kuwajerwala, Sacha Morin, Krishna Murthy Jatavallabhula 等（16 位作者，来自 University of Toronto, Université de Montréal, MIT, JHU, UMass）
- **会议**: CVPR 2024
- **arXiv**: 2309.16650 (2023 年 9 月提交)
- **项目页面**: https://concept-graphs.github.io/
- **代码**: 开源（GitHub，项目页面可访问）

## 问题定义

现有 3D 语义表示方案存在以下问题：
1. **密集特征表示**（如 ConceptFusion）为每个 3D 点分配语义特征向量，内存冗余严重，难以扩展到大型场景
2. **缺乏结构**：密集表示难以分解为对象级单元，不利于动态更新
3. **封闭词汇集**：传统 3D 场景图方法仅支持预定义类别
4. **缺乏空间关系**：现有开放词汇 3D 表示缺少实体间的语义空间关系信息

ConceptGraphs 旨在构建一种**开放词汇、对象为中心、图结构**的 3D 场景表示，同时支持感知和规划任务。

## 方法概述

ConceptGraphs 采用纯 2D 基础模型（零样本，无需训练/微调）构建 3D 场景图，流程如下：

### 1. 对象级 3D 建图 (Object-based 3D Mapping)

- **输入**: 带位姿的 RGB-D 图像序列
- **2D 分割**: 使用 **SAM** (Segment Anything) 生成类别无关的实例掩码
- **特征提取**: 每个掩码区域通过 **CLIP** 或 **DINO** 编码器提取视觉特征向量
- **3D 投影**: 将掩码区域通过深度信息投影到 3D，用 DBSCAN 去噪
- **对象关联 (Object Association)**: 对新检测对象与地图中已有对象计算加权相似度（几何相似度 + 语义余弦相似度），贪心匹配
- **对象融合 (Object Fusion)**: 匹配成功则融合点云和更新语义特征；失败则初始化新对象

### 2. 节点标注 (Node Captioning)

- 对每个对象，选取贡献最多噪声无关点的 10 个视图
- 使用 **LLaVA-7B** (LVLM) 对每个视图生成描述
- 使用 **GPT-4** 汇总 10 个视图的描述为最终节点标签（含 "invalid" 标记处理误检）

### 3. 场景图生成 (Scene Graph Generation)

- 计算所有对象对的 3D 边界框 IoU
- 通过 **最小生成树 (MST)** 剪枝，保留潜在边
- 对 MST 中的每条边，将对象描述和 3D 位置输入 **GPT-4**，输出语义关系（如 "a on b", "b in a"）
- 支持开放词汇关系类型（如 "a backpack may be stored in a closet"）

### 4. 变体: ConceptGraphs-Detector (CG-D)

- 使用 RAM (图像标注) + Grounding DINO (开放词汇检测器) 替代 SAM
- 单独处理背景对象（墙、天花板、地板）

### 5. LLM 任务规划

- 将场景图节点转为 JSON 格式文本描述（含 ID、边界框、标签、描述）
- 给定自然语言查询，由 GPT-4 定位最相关对象，传入下游任务（抓取、导航等）

## 实验结果

### 场景图构建精度 (Table I)

在 Replica 数据集上，通过 Amazon Mechanical Turk (AMT) 人工评估：

| 指标 | CG | CG-D |
|------|------|------|
| 节点精度 (Node Precision) 平均 | **0.71** | 0.61 |
| 每场景有效对象数 (Valid Objects) | 23-60 | 24-60 |
| 重复检测数 (Duplicates) | 0-5 | 0-4 |
| 边精度 (Edge Precision) 平均 | **0.88** | **0.91** |

标准 CG 变体节点精度约 70%（主要误差来自 LLaVA 的标注错误），边精度约 90%。

### 3D 语义分割 (Table II)

在 Replica 数据集上评估，与 ConceptFusion 等对比：

| 方法 | mAcc | F-mIoU |
|------|------|--------|
| ConceptFusion (zero-shot) | 24.16 | 31.31 |
| ConceptFusion + SAM | 31.53 | 38.70 |
| **ConceptGraphs (Ours)** | **40.63** | 35.95 |
| ConceptGraphs-Detector | 38.72 | 35.82 |

ConceptGraphs 在 mAcc 上显著优于 ConceptFusion（+16.47），但 F-mIoU 略低。注意内存占用远小于 ConceptFusion。

### 对象检索 (Table III)

在 Replica 和真实 Lab 场景上评估三种查询类型：

**Replica 场景 (LLM 方法)**:
| 查询类型 | R@1 | R@2 | R@3 |
|---------|-----|-----|-----|
| 描述性 (Descriptive) | 0.61 | 0.64 | 0.64 |
| 功能性 (Affordance) | 0.57 | 0.63 | 0.66 |
| **否定 (Negation)** | **0.80** | **0.89** | **0.97** |

**Lab 场景 (LLM 方法)**:
| 查询类型 | R@1 | R@2 | R@3 |
|---------|-----|-----|-----|
| 描述性 | **1.00** | – | – |
| 功能性 | **1.00** | – | – |
| 否定 | **1.00** | – | – |

CLIP 在描述性查询上表现好，但在复杂 functional/negation 查询上较差。LLM 方法整体更优。

### 真实机器人任务

1. **移动导航 (Jackal UGV)**: 响应抽象语言查询（如 "something this guy would play with" → 找到篮球），结合 LVLM 验证
2. **对象搜索**: 当目标对象被移动后，LLM 推理新位置（如 "NASA 衬衫可能在洗衣袋里"）
3. **可穿越性估计**: LLM 根据对象描述判断可推/不可推物体，结合代价地图规划路径
4. **开放词汇抓取放置 (Spot 机器人)**: 响应 "cuddly quacker" → 抓起鸭子玩具放入盒子；"something healthy to eat" → 抓起芒果
5. **定位与地图更新: 在 AI2Thor 仿真中实现 3-DoF 对象级定位和增量地图更新

## 关键洞察

1. **零样本开放词汇**: 完全利用 2D 基础模型，无需 3D 训练数据或微调
2. **对象级结构 vs 密集特征**: 比 ConceptFusion 等方案显著降低内存占用，支持动态更新
3. **LLM 赋能的语义关系**: 利用 LLM（GPT-4）推断对象间空间关系，支持开放词汇关系类型
4. **LLM 规划接口**: 场景图可转为结构化文本，直接接口到 LLM 实现复杂任务规划
5. **多功能性**: 支持分割、定位、导航、操作、地图更新等多类下游任务
6. **高引/影响力**: 成为后续 3D 开放词汇场景图工作的基准框架

## 局限性

1. **节点标注错误**: LLaVA-7B 的标注质量有限，导致约 30% 的错误率
2. **小/薄物体缺失**: 场景图偶尔遗漏小物体或薄物体
3. **重复检测**: 存在少量重复检测，在关键物体上可能影响规划
4. **计算/经济成本**: 需要多次 LVLM (LLaVA) 调用 + 商用 LLM (GPT-4) 推理，成本显著
5. **依赖 GPU**: 需要 GPU 运行 SAM/CLIP/LLaVA 等模型

## 与相关工作的关系

- **ConceptFusion**: 密集 3D 特征场，ConceptGraphs 通过对象级结构减少了内存占用并增加了可解释性
- **3D-LLM / OpenScene**: 同期工作采用不同方式做 3D 开放词汇理解
- **OGSV**: 同期工作也构建开放词汇 3D 场景图，但使用 GNN 预测关系（非 LLM）
- **CLIP 变体**: 论文的 CLIP-only 路线表现不如 LLM 路线，特别是在复杂语义查询上

## 证据等级

full-paper — 已获取完整论文 PDF，进行了全文阅读和结构化分析。
