---
title: "SGR3 Model: Scene Graph Retrieval-Reasoning Model in 3D"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags: [3D-SGG, MLLM, RAG, training-free, egocentric-video, arXiv-2026]
raw_sources:
  - ../../../sources/scene-graph/2026-06-09-SGR3_Egocentric_Video_Scene_Graph_Retrieval.pdf
  - ../../../sources/scene-graph/2026-06-09-SGR3_Egocentric_Video_Scene_Graph_Retrieval.txt
evidence_level: full-paper
---

# SGR3 Model: Scene Graph Retrieval-Reasoning Model in 3D

> 一种基于 MLLM + RAG 的 **训练无关 3D 场景图生成** 框架，无需显式 3D 重建和摄像机位姿。通过 ColPali 风格的跨模态检索机制从外部知识库获取结构化场景图先验，指导 MLLM 输出关系三元组。

## 核心思想

传统 3D 场景图生成依赖重建→GNN 管线，需要 RGB-D 序列、精确摄像机位姿和 3D 网格。SGR3 Model 完全绕过显式 3D 重建，使用 MLLM（Qwen3-VL 32B）作为推理骨干，通过 RAG 从外部知识库检索结构相似场景的图结构，作为结构化提示引导 MLLM 生成关系三元组。

## 方法

### 整体管线

1. **知识库构建**: 从 3RScan 训练场景提取帧级子图，用 SigLip2 编码图像块为 768 维嵌入，FAISS 索引
2. **关键帧过滤**: ColQwen（Qwen 版 ColPali）计算帧间 token 级相似度，阈值 σ=0.5 过滤冗余帧，减少重复检测
3. **参考边检索**: 对窗口内关键帧进行 patch 级检索，引入加权 patch 投票机制（Eq. 3-5），抑制模糊/低信息量区域的负面影响
4. **窗口级生成**: MLLM 接收关键帧图像 + 检索到的参考边 + 当前全局场景图，一步推理输出场景图

### 关键创新

- **加权 patch 级相似度选择**（Eq. 3-5）：计算 patch 自相似性矩阵，低独特性 patch（如模糊区域）获得更低权重，提升检索鲁棒性
- **ColQwen 关键帧过滤**：token 级最大相似度聚合（late interaction），比全局嵌入更细粒度
- **图到图检索（graph-to-graph retrieval）**：传统 RAG 用场景图作下游任务外部知识，SGR3 用已完成场景图检索结构相关三元组辅助当前生成

## 实验

### 数据集
- **3RScan**: 定量评估（3D 场景图关系三元组标注）
- **ScanNet**: 定性分析（仅有物体标签，用于可视化）

### 实现细节
- 骨干 MLLM: Qwen3-VL 32B
- 硬件: 4× NVIDIA H100 (80GB)
- 帧输入: 滑动窗口 RGB 帧

### 与 SOTA 对比（Tab. I）

| 方法 | 类型 | Obj R@10 | Pred R@3 | Rel Old R@1 | Rel New R@1 |
|------|------|-----------|----------|-------------|-------------|
| VGfM | 有监督 | 0.77 | 0.36 | 0.63 | 0.06 |
| 3DSSG | 有监督 | 0.74 | 0.94 | 0.59 | 0.070 |
| SGFN | 有监督 | 0.80 | 0.82 | 0.59 | 0.074 |
| MonoSSG | 有监督 | 0.89 | 0.87 | 0.62 | 0.131 |
| VLSAT | 有监督 | 0.86 | 0.98 | 0.54 | 0.087 |
| ConceptGraph | 训练无关 | 0.75 | 0.96 | 0.55 | 0.084 |
| OpenWorld | 训练无关 | 0.46 | 0.10 | 0.27 | 0.043 |
| Only Qwen | 消融基线 | 0.78 | 0.56 | 0.57 | 0.064 |
| Abstraction | 消融基线 | 0.65 | 0.59 | 0.59 | 0.096 |
| **SGR3 Model** | **训练无关** | **0.67** | **0.78** | **0.62** | **0.125** |

**关键结果解读**：
- SGR3 在训练无关方法中大幅领先 OpenWorld（Rel New R@1: 0.125 vs 0.043），微弱领先 ConceptGraph（0.125 vs 0.084）
- 与有监督 GNN 方法可比：仅次于 MonoSSG（0.131），超过其他所有方法
- Predicate R@3: 0.78（低于 3DSSG/ConceptGraph 的 0.94/0.96，但 Rel New R@1 接近最好水平，说明改进主要在关系对选择和组合推理）

### 消融实验

**ColQwen 关键帧过滤（Tab. II）**：

| 配置 | Obj Rec | Rel Rec | 推理时间 | 冗余度 |
|------|---------|---------|---------|--------|
| 有 filter | 0.67 | 0.125 | 2.73s | 1.42 |
| 无 filter | 0.80 | 0.131 | 6.18s | 4.18 |

→ 过滤略微牺牲召回（-0.6% Rel Rec），但推理加速 2.3×，冗余度降 66%

**知识库规模（Tab. III）**：

| 规模 | Obj Rec | Rel Rec |
|------|---------|---------|
| 100% | 0.67 | 0.125 |
| 75% | 0.67 | 0.121 |
| 50% | 0.64 | 0.117 |
| 25% | 0.66 | 0.110 |
| 0% | 0.66 | 0.061 |

→ 知识库完全移除后 Rel Rec 从 0.125 降至 0.061（-51%），表明 RAG 提供了 MLLM 无法从纯视觉中可靠推断的必要关系先验

**检索粒度消融（Tab. IV）**：

| 粒度 | Obj Rec | Rel Rec | 冗余度 |
|------|---------|---------|--------|
| 加权 patch 级 | 0.67 | 0.125 | 1.42 |
| Patch 级 | 0.62 | 0.117 | 1.44 |
| 图像级 | 0.63 | 0.095 | 1.49 |

→ 加权 patch 级优于 patch 级和图像级检索

### 机制分析

- **抽象 vs. 原始三元组**: 将检索到的参考三元组抽象为高层谓词指令（Abstraction）后 Rel Rec 从 0.125 降至 0.096，表明 MLLM 更受益于具体的结构示例而非抽象规则
- **复制比率**: ρ = 64.7%（三元组级），71%（物体对级），说明 RAG 带来的性能提升主要来自显式结构信息复用，而非隐式泛化
- **注意力分析**: 生成谓词时，MLLM 的跨层注意力集中在 prompt 中的参考三元组区域，验证了检索信息直接参与生成过程

## 优缺点

### 优点
- 真正的训练无关框架，无需显式 3D 重建和传感器标定
- RAG 机制分析透彻（复制比率、抽象实验、注意力可视化）
- 加权 patch 投票机制有效处理模糊/低质量区域
- 在关系三元组预测上表现具有竞争力（Rel New R@1: 0.125）

### 不足
- 物体检测能力较弱（Obj R@10: 0.67，低于大部分方法），单纯依赖 MLLM 的检测和定位能力
- 在新版 recall 评估下（所有 GT 物体对作为分母），所有方法关系 recall 普遍偏低（最高 MonoSSG 仅 0.131），3D 场景图关系预测整体仍需突破
- 知识库依赖 3RScan 训练场景，跨域泛化能力未测试

## 关联论文

- [[RA-SGG: Retrieval-Augmented Scene Graph Generation via Multi-Prototype Learning]] — 2D SGG 的 RAG 方法，SGR3 将其扩展到 3D
- [[CCL-3DSGG: CLIP-Driven Open-Vocabulary 3D Scene Graph Generation]] — 另一个利用 VLM 的 3D SGG 方法
- [[Open3DSG: Open-Vocabulary 3D Scene Graphs from Point Clouds]] — 开源字典 3D SGG，使用 2D VLM+LLM
- [[OwSGG: Open World Scene Graph Generation using Vision Language Models]] — 同样使用 VLM 的开放世界 SGG
- [[ZING-3D: Zero-shot Incremental 3D Scene Graphs via Vision-Language Models]] — 零样本增量 3D SGG
