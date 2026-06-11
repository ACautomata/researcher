---
title: "MA3DSG: Multi-Agent 3D Scene Graph Generation for Large-Scale Indoor Environments"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - 3d-scene-graph-generation
  - multi-agent-system
  - graph-alignment
  - large-scale-indoor
  - scalability
  - benchmark
  - arXiv-2026
raw_sources:
  - ../../../raw/sources/2026-02-04-MA3DSG-Multi-Agent-3D-Scene-Graph-Generation.pdf
  - ../../../raw/sources/2026-02-04-MA3DSG-Multi-Agent-3D-Scene-Graph-Generation.txt
related_pages:
  - incremental-3d-scene-graph-prediction-from-rgb-sequences.md
  - ccl-3dsgg-clip-driven-open-vocabulary-3d-scene-graph-generation.md
  - sgaligner-3d-scene-alignment-scene-graphs.md
evidence_level: full-paper
paper:
  title: "MA3DSG: Multi-Agent 3D Scene Graph Generation for Large-Scale Indoor Environments"
  abbreviated: "MA3DSG"
  authors:
    - Yirum Kim
    - Jaewoo Kim
    - Ue-Hwan Kim
  year: 2026
  venue: "arXiv (preprint)"
  arXiv: "2602.04152"
  code: null
  paper_url: "https://arxiv.org/abs/2602.04152"
  affiliation: "Gwangju Institute of Science and Technology (GIST)"
---

# MA3DSG: Multi-Agent 3D Scene Graph Generation for Large-Scale Indoor Environments

## 概述

MA3DSG 是**首个**针对大规模室内环境的多智能体 3D 语义场景图生成（3DSGG）框架。现有 3DSGG 方法均基于 single-agent 假设，在扩展到真实世界大规模场景时面临严重的可扩展性问题——运行时间长达 4×、数据流量高达 98×。MA3DSG 提出 **training-free 的无参数图对齐算法**，使多个 agent 在无学习参数情况下协同构建统一全局场景图。同时提出 **MA3DSG-Bench** 基准，支持多种 agent 配置（1~5 agents）、领域规模（1~47 rooms）和动态条件（static / long-term）。

## 核心贡献

1. **问题形式化**：将 3DSGG 任务推广到多智能体、大规模设定，首次系统性地解决 3DSGG 的可扩展性挑战。
2. **模型设计**：MA3DSG 提出高效的图对齐算法，在无训练参数情况下实现跨 agent 场景图融合，在不同领域规模下均保持强可扩展性和快速运行时间。
3. **基准建设**：MA3DSG-Bench 将先前 single-agent、小规模 3DSGG 基准扩展到多 agent、大规模设定，包含静态度量协作感知（SCP）和长时动态协作感知（LDCP）两种场景。

## 问题定义

给定 K 个 agent，每个 agent k 有一组 RGB-D 观察序列 Sk = {s^k_r}^{R_k}_{r=1}，其中 R_k 为 agent k 访问的房间数。目标是让多个 agent 协同探索大规模环境，各自增量构建局部 3D 语义场景图，并通过图对齐算法将其融合为统一的全局场景图。

## 方法：MA3DSG

### 架构概览

MA3DSG 包含三个核心组件：

1. **多智能体探索（Multi-Agent Exploration）**：各 agent 分布式覆盖大规模空间的不同区域，通过重叠区域（overlap ratio = 0.2）共享信息。
2. **3D 语义场景图生成（3D Semantic Scene Graph Generation）**：各 agent 基于 SGFN [32] 框架增量构建局部场景图。使用 PointNet 对 3D 全局分割图（GSM）中的 segments 提取节点特征，通过 GNN 消息传递（Feature-wise Attention Network, FAN）更新节点和边特征。
3. **3D 语义场景图对齐（3D Semantic Scene Graph Alignment）**：轻量级无参数图对齐算法，将局部图融合为统一全局表示。

### 3D 语义场景图生成

#### 3D 全局分割图（3D GSM）
- 各 agent 对输入的 RGB-D 序列进行增量几何分割生成 3D GSM
- 每个 segment ui 包含点云 Pi、质心 pi、标准差 σi、AABB 边界框 bi、最大长度 li、体积 νi

#### 特征图（Feature Graph）
- **节点特征**：vi = [E(Pi), σi, ln(bi), ln(νi), ln(li)]，融合 PointNet 提取的 latent embedding E(Pi) 与空间不变属性
- **边特征**：eij = fs([Δpij, Δσij, Δbij, ln(νi/νj), ln(li/lj)])，由 3 个 MLP 构成
- **GNN 更新**：采用 FAN（Feature-wise Attention Network）进行消息传递

### 3D 语义场景图对齐

无参数的增量图对齐算法：

1. **图对齐（Graph Alignment）**：在查询图 Gq 与参考图 Gr 之间搜索交集子图。当 Gq 节点 > 6 时随机选择锚节点，通过 triplet（node-edge-node）匹配递归扩展。若交集子图超过阈值 θlen（=3），合并节点和边；否则作为新图添加。
2. **图更新（Graph Update）**：对齐后按三种方式更新：
   - **Matching Node**：质心距离 < θdis（=1.5m）且 IoU > θbbox（=0.4）且标签相同 → 合并，用并集边界框更新
   - **Conflicting Label**：空间匹配但标签不同 → 用新节点替换旧节点
   - **New Node**：空间不匹配 → 作为新节点插入

## 实验

### 数据集与设置

- **数据集**：基于 3RScan [20] 和 3DSSG [28] 重构的统一大规模测试集，统一 47 个房间场景为单一领域
- **场景图规模**：SCP: 1,588 节点 / 5,546 边；LDCP: 1,518 节点 / 5,054 边（含 478 个动态物体）
- **Agent 配置**：5 个 agent，overlap ratio = 0.2
- **阈值**：θdis = 1.5m（距离），θlen = 3（对齐长度），θbbox = 0.4（IoU）

### 基线方法

- **Single-Agent**: 3DSSG [28], SGFN [32]
- **Multi-Agent**: SGFN + SGAligner [34], SGFN + SG-PGM [52]

### 评估指标

- **准确率**：Recall@1, Precision@1, F1@1（triplet, object, predicate），同时考核空间精度（质心位置 + 3D IoU）
- **效率**：图对齐时间、场景完成总时间、per-agent 数据流量

### 结果

#### 静态协作感知（SCP, 47 rooms）

| 方法 | Triplet F1@1 | Object F1@1 | Predicate F1@1 | 流量 (MB) | 对齐 (sec) | 总时间 (min) |
|------|:----------:|:----------:|:-------------:|:---------:|:---------:|:-----------:|
| 3DSSG | 11.2 | 33.7 | 26.3 | - | - | - |
| SGFN | 14.1 | 38.6 | 28.6 | - | - | 61.8 |
| SGFN+SGAligner | 12.7 | 38.5 | 25.9 | 364.2 | 107.1 | 16.6 |
| SGFN+SG-PGM | 12.6 | 38.3 | 26.7 | 364.1 | 32.1 | 15.3 |
| **MA3DSG (Ours)** | **13.7** | 35.1 | 24.6 | **3.7** | **0.02** | **14.8** |

MA3DSG 在所有领域规模下保持与 SGFN 相当的精度（Triplet F1@1 偏差 +1.5/-1.3%），但运行速度 **2.8×~4.2× 更快**，数据流量低至 multi-agent 基线的 **1/98**。全部推理仅在 CPU 上执行。

#### 长时动态协作感知（LDCP, 47 rooms）

| 方法 | Triplet F1@1 | Object F1@1 | Predicate F1@1 | 流量 (MB) | 对齐 (sec) | 总时间 (min) |
|------|:----------:|:----------:|:-------------:|:---------:|:---------:|:-----------:|
| 3DSSG | 7.7 | 29.1 | 20.5 | - | - | - |
| SGFN | 6.6 | 32.4 | 16.7 | - | - | 166.7 |
| SGFN+SGAligner | 6.4 | 31.0 | 19.9 | 1013.2 | 350.6 | 46.8 |
| SGFN+SG-PGM | 6.0 | 30.8 | 19.0 | 1013.1 | 104.9 | 42.7 |
| **MA3DSG (Ours)** | **6.2** | **33.0** | 16.2 | **11.6** | **0.37** | **41.0** |

MA3DSG 在动态场景中同样保持竞争力——Object F1@1 接近 SGFN（偏差 +9.6/+0.3%），运行速度 **3.4×~4.1× 更快**，对齐时间仅 0.37 秒（vs. SGFN+SGAligner 350.6 秒）。

### 效率分析

- **对齐时间**：SCP 下仅 **0.02 秒**，LDCP 下仅 **0.37 秒**（多 agent 基线 SGFN+SGAligner SCP: 107.1 秒，LDCP: 350.6 秒）
- **数据流量**：MA3DSG SCP **3.7 MB** vs SGFN+SG-PGM **364.1 MB**（**98.4× 减少**）；LDCP **11.6 MB** vs **1,013.1 MB**（**87.3× 减少**）
- 仅在小规模（5 rooms）中，MA3DSG 的对齐时间优势不明显（因对齐阈值导致无参数对齐效果受限）

## 关键洞察

1. **无参数训练的健壮性**：MA3DSG 的图对齐算法无需任何学习参数，仅依赖标签匹配和空间约束，即可在 5 agent 设置下实现与 SGFN（full-pipeline 训练）相当的场景图生成精度。
2. **可扩展性**：领域规模从 5 rooms 扩展到 47 rooms 时，MA3DSG 的运行时间从 2.3 min → 14.8 min（SCP），而 SGFN 从 6.4 min → 61.8 min，增益随规模扩大而增加。
3. **通信效率的质变**：通过仅传输图结构（少量三元组）而非原始点云数据，MA3DSG 的数据流量降低两个数量级，使多 agent 协作系统在大规模部署中成为可能。
4. **局限性**：Triplet/Relation 预测精度仍有下降（尤其是 predicate F1@1 在 LDCP 下 16.2 vs SGFN 16.7）；图对齐算法在处理大规模变化时的鲁棒性有待进一步加强。

## 总结

MA3DSG 是首个多智能体 3D 语义场景图生成框架，通过无参数图对齐算法实现了大规模环境下的高效协同场景理解。其核心优势在于极低的通信开销（< 4 MB）和推理延迟（< 0.4 sec），同时保持与 SOTA single-agent 方法相当的生成精度。MA3DSG-Bench 为未来的可扩展 3DSGG 研究提供了标准化的评估框架。

## 参考文献

- [32] Wu et al., "ScenegraphFusion: Incremental 3D Scene Graph Prediction from RGB-D Sequences", CVPR 2021.
- [34] Sarkar et al., "SGAligner: 3D Scene Alignment with Scene Graphs", ICCV 2023.
- [52] SG-PGM: Partial graph matching for 3D scene graph alignment.
- [20] Wald et al., "RIO: 3D Object Instance Re-localization in Changing Indoor Environments", ICCV 2019.
- [28] Wald et al., "Learning 3D Semantic Scene Graphs from 3D Indoor Reconstructions", CVPR 2020.
