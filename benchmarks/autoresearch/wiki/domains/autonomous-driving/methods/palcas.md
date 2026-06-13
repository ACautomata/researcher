---
title: PALCAS — Priority-Aware Lane Change Advisory System
type: method
domain: autonomous-driving
status: active
created: 2026-05-24
updated: 2026-05-24
tags:
  - federated-reinforcement-learning
  - lane-change-decision
  - multi-agent-rl
  - pdqn
source_pages:
  - wiki/domains/autonomous-driving/papers/palcas-priority-aware-lane-change-federated-rl.md
related_pages:
  - wiki/domains/autonomous-driving/concepts/federated-reinforcement-learning-autonomous-driving.md
  - wiki/domains/autonomous-driving/tasks/lane-change-decision-making.md
---

# PALCAS — 优先级感知联邦强化学习变道决策

## 定义

PALCAS 是首个将联邦多智能体强化学习（Fed-MARL）引入优先级感知自动驾驶变道决策的框架。通过 PDQN 混合动作空间同时处理离散变道决策 + 连续纵向控制，多目标优先级引导奖励函数统一强制性和自主性变道行为，在 SUMO + Eclipse MOSAIC 仿真环境中实现 93.33% 合流成功率和 2.45% 碰撞率（60% CAV 渗透率）。

## 核心机制

1. **Fed-MARL 系统架构**：
   - 长距离多车道高速公路划分为多个路段，每个路侧单元（RSU）管理一个路段。
   - 每个 RSU 作为 Fed-MARL 的一个 agent，控制覆盖区域内所有 CAV。
   - RSU 间通过 I2I 通信共享全局交通信息，每 2500 步 FedAvg 聚合。
2. **PDQN 混合动作空间**：
   - 离散动作：左变道（a₀）、右变道（a₁）、保持巡航（a₃）。
   - 连续参数：加速度值（a₂ ∈ [a_min, a_max]）。
   - 参数网络 μ 输出连续参数，Q 网络评估所有离散动作。
3. **优先级引导多目标奖励函数**：
   - $R = \alpha \cdot r_e + \beta \cdot r_s + \gamma \cdot r_c + \delta \cdot r_{lc} + \varepsilon \cdot r_d$
   - $r_e$（效率）：接近 v_max 的自车效率 + 集群平均速度接近目标。
   - $r_s$（安全）：基于 RSS（Responsibility-Sensitive Safety）模型的纵向和横向安全距离。
   - $r_c$（舒适）：惩罚超过舒适阈值（1.47 m/s²）的加速度。
   - $r_{lc}$（优先级变道）：目的地紧急度项 u_t + 集群导向 staging 惩罚 + 动态权重 w_t。
   - $r_d$（死锁）：防止匝道车辆在加速车道末端停滞。
4. **混合状态表示**：自车状态 + 周围车辆状态（D 个邻近车辆）+ 集群级状态（平均速度、各车道密度）+ 全局状态（I2I 跨集群聚合）。

## 假设

- 所有 CAV 完全协作（非对抗性）。
- RSU 覆盖范围连续且无间隙。
- I2I 通信延迟可忽略（对实时决策无显著影响）。
- 高速公路拓扑为单一五车道、三集群场景。

## 证据

- arXiv:2604.27118, Ibork et al., 2026，full-paper。
- 仿真平台：SUMO（微观交通）+ Eclipse MOSAIC（V2X 通信）。
- 60% CAV 渗透率下：
  - 平均速度 30.03 m/s（Baseline-1 29.12, Baseline-2 28.10），+3.12% 和 +6.86%。
  - 碰撞率 2.45%（Baseline-1 降低 19.67%，Baseline-2 降低 75.5%）。
  - 合流成功率（MSR）93.33%（Baseline-1 40.34%，Baseline-2 43.93%）。
  - 目的地成功率（DSR）93.97%。
- 驾驶舒适度：加速度保持在 [-1, 1] m/s² 舒适范围（baseline [-4.5, 2.6]）。
- CAV 渗透率 5%-60% 下均最优，且随渗透率增加单调提升。
- PDQN 网络：[256, 512, 256] 隐藏层，Huber Loss，AdamW。

## 变体

- **Baseline-1**：集中式单智能体（观测整个高速公路），MSR 仅 40.34%。
- **Baseline-2**：无联邦学习的独立训练（无知识共享），MSR 仅 43.93%。
- PALCAS 权重配置：$\alpha=0.5, \beta=0.4, \gamma=0.1, \delta=0.05, \varepsilon=0.05$（敏感性未充分消融）。

## 优势与局限

**优势**：
- 首个联合处理强制性和自主性变道行为的联邦多智能体 RL 系统。
- 联邦知识共享 + I2I 通信实现大规模协同变道决策。
- 优先级引导奖励在动态交通条件下有效平衡个体紧急度和全局效率。
- PDQN 成功处理混合动作空间（离散变道 + 连续控制）。
- 安全性显著——RSS 安全约束嵌入 RL 奖励有效降低碰撞率。

**局限**：
- 仅在高仿真环境（SUMO + MOSAIC）验证，无真实世界数据。
- 单一高速公路拓扑（五车道、三集群），其他道路几何泛化性未知。
- 未与现有非联邦 MARL 变道方法（如 QCOMBO）直接比较。
- 联邦学习通信开销和延迟对实时决策的影响未深入分析。
- 假设所有 CAV 完全协作，未考虑对抗性或非协作车辆。
- 奖励权重（α=0.5, β=0.4, γ=0.1, δ=0.05, ε=0.05）的敏感性未充分消融。

## 关联

- [联邦强化学习与自动驾驶](../concepts/federated-reinforcement-learning-autonomous-driving.md)：上位概念。
- [变道决策任务](../tasks/lane-change-decision-making.md)：解决的核心任务。
- 与 distillation 域无直接交叉，但联邦学习范式未来可能与联邦数据集蒸馏产生连接。
- PDQN 混合动作空间设计可迁移到其他需要离散+连续联合决策的自动驾驶子任务。

## 开放问题

- 真实 CAV 硬件平台上的部署可行性和实时性？
- 联邦学习通信延迟对变道决策（需毫秒级响应）的实际影响？
- Priority-guided reward 权重对不同道路拓扑的敏感性？
- 扩展到混合交通（CAV + 人类驾驶车辆）中的人类行为建模？
- 与现有非联邦 MARL 变道方法的直接性能比较？
- 联邦学习框架下各 agent 的局部数据异质性如何影响收敛？
