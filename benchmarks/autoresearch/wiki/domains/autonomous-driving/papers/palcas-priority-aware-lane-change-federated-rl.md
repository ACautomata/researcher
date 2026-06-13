---
title: PALCAS: A Priority-Aware Intelligent Lane Change Advisory System for Autonomous Vehicles using Federated Reinforcement Learning
type: paper
domain: autonomous-driving
status: stable
created: 2026-05-05
updated: 2026-05-05
tags:
  - federated-reinforcement-learning
  - lane-change-decision
  - multi-agent-rl
  - autonomous-vehicles
  - v2x-communication
paper:
  title: "PALCAS: A Priority-Aware Intelligent Lane Change Advisory System for Autonomous Vehicles using Federated Reinforcement Learning"
  authors:
    - Yassine Ibork
    - Nhat Ha Nguyen
    - Myounggyu Won
    - Lokesh Das
  year: 2026
  venue: arXiv preprint (cs.RO)
  arxiv: "2604.27118"
  doi: ""
  code: ""
  project: ""
classification:
  label: autonomous-driving
  task:
    - lane-change decision making
    - multi-agent coordination
  method_family:
    - federated reinforcement learning
    - parameterized deep Q-network
    - multi-agent RL
  modality:
    - traffic simulation
  datasets:
    - SUMO simulated highway
  metrics:
    - collision rate
    - destination success rate
    - merging success rate
    - average speed
    - acceleration comfort
evidence_level: full-paper
raw_sources:
  - raw/sources/2026-04-29-palcas-priority-aware-lane-change-federated-rl.pdf
related_pages:
  - wiki/domains/autonomous-driving/concepts/federated-reinforcement-learning-autonomous-driving.md
  - wiki/domains/autonomous-driving/tasks/lane-change-decision-making.md
  - wiki/domains/autonomous-driving/methods/palcas.md
---

# PALCAS: A Priority-Aware Intelligent Lane Change Advisory System for Autonomous Vehicles using Federated Reinforcement Learning

## 引用

Yassine Ibork, Nhat Ha Nguyen, Myounggyu Won, Lokesh Das. PALCAS: A Priority-Aware Intelligent Lane Change Advisory System for Autonomous Vehicles using Federated Reinforcement Learning. arXiv:2604.27118, April 2026.

## 一句话贡献

首次将联邦多智能体强化学习（Fed-MARL）引入优先级感知的自动驾驶变道决策，通过新颖的 priority-guided reward 设计同时处理强制性和自主性变道行为，在 SUMO + Eclipse MOSAIC 仿真环境中显著提升交通效率、安全性和舒适度。

## 问题设定

城市高速公路变道决策是一个具有挑战性的任务，需要协调车辆的横向和纵向运动控制以响应动态变化的交通模式。现有方法存在以下不足：

- **单智能体系统**：只关注自车效率与安全的平衡，缺乏多车协同。
- **集中式多智能体系统**：存在数据安全隐患和高计算开销。
- **联邦学习在自动驾驶中的应用**：当前 FedRL 研究主要限于低层碰撞避免，尚未探索集成式多智能体变道决策。

论文将优先级感知变道问题建模为去中心化部分可观测马尔可夫决策过程（Dec-POMDP），动作空间为混合空间（离散变道 + 连续纵向控制）。

## 方法

PALCAS 的核心架构包含以下关键设计：

### 系统架构
- 长距离多车道高速公路被划分为多个路段，每个路段由一个路侧单元（RSU）管理。
- 每个 RSU 作为 Fed-MARL 框架中的一个 agent，控制其覆盖区域内所有联网自动驾驶车辆（CAV）。
- RSU 之间通过 I2I（Infrastructure-to-Infrastructure）通信共享全局交通信息。
- 使用 FedAvg 进行全局模型聚合，每 2500 步同步一次。

### 状态空间
混合状态表示，融合四个层次的信息：
1. **自车状态**：横向/纵向位置、速度、加速度、当前车道、距出口距离。
2. **周围车辆状态**：D 个邻近车辆的相对距离、速度、加速度、车道索引、距出口距离。
3. **集群级状态**：RSU 覆盖区域内的平均速度和各车道交通密度。
4. **全局状态**：通过 I2I 通信共享的跨集群聚合交通统计。

### 动作空间
混合动作空间，PDQN（Parameterized Deep Q-Network）同时处理：
- 离散动作：左变道（a₀）、右变道（a₁）、保持巡航（a₃）
- 连续参数：加速度值（a₂ ∈ [a_min, a_max]）

### 奖励函数
多目标奖励函数 R = α·r_e + β·r_s + γ·r_c + δ·r_lc + ε·r_d：

1. **效率奖励 (r_e)**：加权组合自车效率（接近 v_max）和集群效率（集群平均速度接近目标）。
2. **安全奖励 (r_s)**：基于 RSS（Responsibility-Sensitive Safety）模型，同时评估纵向和横向安全距离。
3. **舒适奖励 (r_c)**：惩罚超过舒适阈值（1.47 m/s²）的加速度。
4. **优先级引导变道奖励 (r_lc)**：
   - 目的地紧急度项 u_t：当车辆接近出口但不在出口车道时施加负奖励，使用 feasibility factor p_t 衡量安全变道的可行性。
   - 集群导向 staging 惩罚 p_stage：惩罚过早占用出口车道的行为。
   - 动态权重 w_t：综合考虑出口距离和剩余变道次数。
5. **死锁惩罚 (r_d)**：防止匝道车辆在加速车道末端停滞。

### 学习算法
- 使用 PDQN 处理混合动作空间：参数网络 μ 输出连续参数，Q 网络评估所有离散动作。
- 联邦学习：每个 RSU 独立训练本地 PDQN，定期通过 FedAvg 聚合。
- 网络结构：[256, 512, 256] 隐藏层，Huber Loss，AdamW 优化器。

## 实验

### 实验设置
- **仿真平台**：SUMO（微观交通仿真）+ Eclipse MOSAIC（V2X 通信仿真）
- **场景**：2.4km 五车道城市高速公路，含多个进出匝道，分为 3 个 RSU 管理的集群
- **交通流**：主线 3200 veh/h/lane，匝道 600 veh/h/lane，60% CAV 渗透率
- **对比基线**：
  - Baseline-1：集中式单智能体（观测整个高速公路）
  - Baseline-2：无联邦学习的独立训练（无知识共享）
- **评估指标**：碰撞率（CR）、目的地成功率（DSR）、合流成功率（MSR）、舒适度、效率（平均速度）

### 主要结果

**交通效率**：PALCAS 平均速度 30.03 m/s，分别比 Baseline-1（29.12）和 Baseline-2（28.10）高 3.12% 和 6.86%。时空图显示 PALCAS 有效缓解了进出匝道车辆引起的间歇性拥堵。

**交通安全**：在 60% CAV 渗透率下，PALCAS 碰撞率比 Baseline-1 降低 19.67%，比 Baseline-2 降低 75.5%。随着 CAV 比例增加，PALCAS 碰撞率单调递减。

**驾驶舒适度**：PALCAS 加速度轨迹平滑，保持在 [-1, 1] m/s² 的舒适范围内，而基线方法加速度波动范围达到 [-4.5, 2.6] m/s²。

**成功率**：PALCAS 在 60% PR 下达到 93.97% DSR 和 93.33% MSR。相比之下，Baseline-1 的 MSR 仅 40.34%（集中式系统在高 CAV 密度下协调能力受限），Baseline-2 的 MSR 为 43.93%（缺乏全局知识共享）。

**CAV 渗透率影响**：PALCAS 在各渗透率（5%-60%）下均表现最优，且随渗透率增加性能持续提升。

## 结果

- PALCAS 是首个联合处理强制性和自主性变道行为的联邦多智能体 RL 系统。
- 联邦知识共享和 I2I 通信是实现大规模协同变道决策的关键。
- 优先级引导的奖励设计在动态交通条件下有效平衡了个体紧急度和全局效率。
- PDQN 成功处理了离散变道决策和连续纵向控制的混合动作空间。

## 限制

- 仅在高仿真环境（SUMO + MOSAIC）中验证，缺乏真实世界部署数据。
- 实验限定在单一高速公路拓扑（五车道、三集群），对其他道路几何的泛化性未知。
- 未与现有的非联邦学习多智能体变道方法进行直接比较。
- 联邦学习通信开销和延迟对实时决策的影响未深入分析。
- 假设所有 CAV 完全协作，未考虑对抗性或非协作车辆。

## 可复用 Claims

- 声明：联邦多智能体 RL 框架在变道决策中优于集中式和独立训练方法。
  证据：PALCAS 在 60% PR 下速度提升 3-7%，碰撞减少 19-75%。
  范围：高速公路变道场景，SUMO 仿真。
  置信度：medium。
  张力：缺乏与 SOTA 非联邦 MARL 变道方法的直接比较。

- 声明：优先级引导的奖励函数可以有效统一强制性和自主性变道行为。
  证据：MSR 从 40.34%（Baseline-1）提升到 93.33%（PALCAS）。
  范围：含进出匝道的高速公路场景。
  置信度：medium。
  张力：奖励权重（α=0.5, β=0.4, γ=0.1, δ=0.05, ε=0.05）的敏感性未充分消融。

- 声明：PDQN 混合动作空间适用于自动驾驶的横向+纵向联合控制。
  证据：PALCAS 在效率和安全性上均优于离散动作基线。
  范围：高速公路变道场景。
  置信度：medium。

- 声明：RSS 模型的安全约束嵌入 RL 奖励能有效降低碰撞率。
  证据：PALCAS 碰撞率在 60% PR 下仅 2.45%。
  范围：SUMO 仿真中的 CAV 变道。
  置信度：medium。

## 连接

- [联邦强化学习与自动驾驶](../concepts/federated-reinforcement-learning-autonomous-driving.md)：本文所属的上位概念。
- [变道决策任务](../tasks/lane-change-decision-making.md)：本文解决的核心任务。
- 与 distillation、OOD detection、spectrum 领域的方法无直接交叉，联邦学习范式在未来可能与数据集蒸馏（如联邦数据集蒸馏）产生连接。

## 开放问题

- PALCAS 在真实 CAV 硬件平台上的部署可行性和实时性如何？
- 联邦学习的通信延迟对变道决策（需毫秒级响应）的实际影响？
- priority-guided reward 的权重对不同道路拓扑的敏感性？
- 能否扩展到混合交通（CAV + 人类驾驶车辆）中的人类行为建模？
- 与现有非联邦 MARL 变道方法（如 QCOMBO）的直接性能比较？
- 联邦学习框架下各 agent 的局部数据异质性（不同交通密度、拓扑）如何影响收敛？

## 来源

- [Canonical raw PDF](../../../../raw/sources/2026-04-29-palcas-priority-aware-lane-change-federated-rl.pdf)
- [arXiv abstract](https://arxiv.org/abs/2604.27118)
- 完整 PDF 正文已抽取，覆盖 introduction、method、simulation results、conclusion 全部章节。
