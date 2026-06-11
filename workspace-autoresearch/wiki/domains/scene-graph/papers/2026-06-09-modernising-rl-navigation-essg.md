---
title: "Modernising Reinforcement Learning–Based Navigation for Embodied Semantic Scene Graph Generation"
date: 2026-06-09
authors:
  - Roman Küble (Organic Computing Group, University of Augsburg)
  - Marco Hüller (Organic Computing Group, University of Augsburg)
  - Mrunmai Phatak (ML and Computer Vision Group, University of Augsburg)
  - Rainer Lienhart (ML and Computer Vision Group, University of Augsburg)
  - Jörg Hähner (Organic Computing Group, University of Augsburg)
arxiv: true
venue: arXiv 2026
domain: scene-graph
evidence_level: full-paper
type: conference
tags:
  - embodied-ai
  - scene-graph
  - reinforcement-learning
  - navigation
  - organic-computing
source: raw/sources/2026-06-09-modernising-rl-navigation-scene-graphs.pdf
code: null
---

# Modernising Reinforcement Learning–Based Navigation for Embodied Semantic Scene Graph Generation

## 核心贡献

本文聚焦 Embodied Semantic Scene Graph Generation (ESSG) 任务中的 RL 导航组件，系统性地研究了三个设计维度对 SSG 完整性和导航效率的影响：

1. **算法升级**：将基线 REINFORCE 替换为 PPO（同奖励塑造设计）
2. **动作空间设计**：对比紧凑动作集（16 动作）、大原子动作集（504 动作）和分解多头发（MH，旋转/平移/停止各为一头）
3. **辅助监督**：深度输入 + 碰撞预测辅助头，以及课程学习（CL，分阶段扩展动作空间）

## 方法

### 架构

基于 ResNet18（冻结主干）+ 轻量深度 CNN + HGT 图编码器 + LSTM 策略核心（2 层 1024-d）。状态向量 1888 维，包含 RGB 特征、深度特征（可选）、LSSG/GSSG 嵌入、上一动作嵌入和停滞检测嵌入。

### 动作空间

- **SH16**：8 旋转（45° 分辨率）× 2 平移（0.0 m / 0.3 m）= 16 原子动作
- **SH504**：24 旋转（15° 分辨率）× 21 平移（0.0-2.0 m，0.1m 步长）= 504 原子动作，其中 (rot=0, len=0) 为 Stop
- **MH504**：三头分解——旋转头（24 类）× 平移头（21 类）+ 独立的 Stop 头。Move-first 语义（先平移后旋转）

### 奖励函数

复合奖励：基于节点覆盖 + 边覆盖 + 视角多样性的势能差 + 移动成功/碰撞/探索/停止事件奖励。时间衰减项 `-ρ·t`。

### 训练设置

- 模拟器：AI2-THOR，FloorPlans 1-27 训练，28-30 评估
- 每 episode 固定 40 步，支持 Stop 早期终止
- SSG 信息直接从模拟器元数据获取（理想感知，无检测噪声）
- 超参数：贝叶斯优化（Optuna），每场景 1000 个 block，5 个随机种子
- 并行 32 环境，每环境 60 步 rollout，PPO 4 epoch / REINFORCE 1 epoch
- CL：4 阶段扩展 16 → 48 → 160 → 504 动作

## 实验与结果

### 最终评估集性能（FloorPlans 28-30，mean ± std across seeds）

| 场景 | 算法+动作 | Node Recall↑ | Episodic Return↑ | Move Success Rate↑ | Path Length↑ | Episode Length |
|------|-----------|-------------|-----------------|-------------------|-------------|---------------|
| Baseline | R+SH16+IL | 0.48 ± 0.22 | 0.69 | 0.14 | 0.1 | 14.0 |
| S0 | R+SH16+IL+D | 0.50 ± 0.24 | 0.69 | 0.14 | 0.2 | 15.4 |
| S1 | R+SH16+D | 0.50 ± 0.23 | 0.69 | 0.15 | 0.2 | 16.2 |
| S2 | PPO+SH16 | 0.58 ± 0.29 | 0.84 | 0.71 | 1.6 | 21.0 |
| S3 | PPO+SH16+D | 0.58 ± 0.29 | 0.86 | 0.77 | 2.2 | 20.8 |
| S4 | PPO+SH504+D | 0.92 ± 0.14 | 0.89 | 0.42 | 7.9 | 32.7 |
| S5 | PPO+SH504+D+CL | 0.86 ± 0.19 | 0.79 | 0.30 | 4.2 | 28.3 |
| S6 | PPO+MH504 | 0.93 ± 0.14 | 1.07 | 0.56 | 10.8 | 27.7 |
| S7 | PPO+MH504+D | 0.91 ± 0.15 | 1.04 | 0.56 | 10.1 | 26.0 |
| S8 | PPO+MH504+CL | 0.93 ± 0.14 | 1.09 | 0.57 | 12.2 | 27.8 |
| S9 | PPO+MH504+D+CL | 0.93 ± 0.15 | 1.11 | 0.58 | 12.9 | 29.3 |

### 关键发现

1. **算法升级**：REINFORCE → PPO 在相同奖励下 **Node Recall 提升 21%**（0.48 → 0.58），同时 Move Success Rate 从 0.14 飙升至 0.71。IL 和深度输入均无法挽救 REINFORCE 的退化行为。

2. **动作空间分辨率**：增大动作空间（SH16 → SH504）可提升 Node Recall（0.58 → 0.92），但 Move Success Rate 下降（0.71 → 0.42），说明大原子空间更难学习。

3. **分解 vs 原子**：MH504 在相同分辨率下 **Node Recall 达 0.93**，且 Move Success Rate 显著高于 SH504（0.56 vs 0.42）。因子化策略更早收敛，学习更稳定。

4. **课程学习**：在 MH 设置下 CL 主要提升安全性（Move Success Rate 0.56→0.58），Node Recall 持平；但在 SH 设置下 CL **劣化性能**（0.92→0.86），说明 CL 对动作空间参数化敏感。

5. **深度输入**：紧凑 PPO 下深度提升安全性（Move Success Rate 0.71→0.77），但对 Node Recall 无影响；高分辨率 MH 下深度**边际影响极小**。

6. **最优配置**：S9（PPO+MH504+D+CL）Episodic Return 最高（1.11），Path Length 最大（12.9），Node Recall 0.93。

## 分析与讨论

- PPO 的改善源于更好的优化动力学（稳定梯度），而非更好的泛化（评估集也保持优势）
- 大动作空间虽提供更广覆盖，但有用行为在输出空间占比更小，需要更细的 credit assignment
- MH 通过分解决策实现动作组分的重用和重组（旋转 + 平移分别学习），避免 SH 中学习坍缩到少数高效用原子动作
- 轨迹可视化显示 MH 产生更多方向变化的分布式覆盖，SH504 倾向直线/走廊式遍历
- 深度仅在紧凑设置下大幅改善安全性，在高分辨率分解设置下影响有限

## 局限性

- SSG 信息直接从 AI2-THOR 元数据获取（理想感知），未纳入真实传感器/检测/分割噪声
- 仅评估 FloorPlans 1-30，规模有限
- 子 agent 分析由 AI 辅助生成，未通过人工复现验证

## 链接

- Source: `raw/sources/2026-06-09-modernising-rl-navigation-scene-graphs.pdf`
- Extract: `raw/sources/2026-06-09-modernising-rl-navigation-scene-graphs.txt`
- Related: [[rgb-only-active-3d-scene-graph-generation]]（同为 embodied SGG 的 RGB-only 导航探索）
