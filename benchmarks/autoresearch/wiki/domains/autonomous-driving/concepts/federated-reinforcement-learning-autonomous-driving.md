---
title: 联邦强化学习与自动驾驶
type: concept
domain: autonomous-driving
status: seed
created: 2026-05-05
updated: 2026-05-05
tags:
  - federated-learning
  - reinforcement-learning
  - autonomous-driving
  - multi-agent-systems
source_pages:
  - wiki/domains/autonomous-driving/papers/palcas-priority-aware-lane-change-federated-rl.md
raw_sources:
  - raw/sources/2026-04-29-palcas-priority-aware-lane-change-federated-rl.pdf
related_pages:
  - wiki/domains/autonomous-driving/tasks/lane-change-decision-making.md
---

# 联邦强化学习与自动驾驶

## 定义

联邦强化学习（Federated Reinforcement Learning, FedRL）将联邦学习的分布式训练范式与强化学习结合。在自动驾驶场景中，多个 agent（如 RSU、车辆或区域控制器）在本地环境中独立训练 RL 策略，定期将模型参数上传到中心服务器进行聚合（如 FedAvg），再广播回各 agent。这种范式既能保护数据隐私，又能通过知识共享提升各 agent 的泛化能力。

## 当前理解

- FedRL 在自动驾驶中的应用目前主要限于低层运动控制（如碰撞避免）和交通信号控制。
- PALCAS 是首个将 FedRL 应用于集成式多智能体变道决策的工作。
- 联邦学习在自动驾驶中的关键优势：跨区域知识泛化、数据隐私保护、去中心化容错。
- 关键挑战：通信延迟对实时决策的影响、本地数据异质性导致的收敛困难。

## 证据

- PALCAS 在 SUMO + MOSAIC 仿真中验证了 FedRL 在变道决策中的有效性（arXiv:2604.27118）。
- 现有文献中，FedRL 已用于碰撞避免（Fu et al. 2022）和交通信号控制（Lu et al. 2025），但未涉及变道决策。

## 连接

- [PALCAS](../papers/palcas-priority-aware-lane-change-federated-rl.md)：本概念的首个支撑论文。
- [变道决策任务](../tasks/lane-change-decision-making.md)：FedRL 在自动驾驶中的核心应用任务。

## 开放问题

- FedRL 的通信效率能否满足自动驾驶变道决策的实时性要求（毫秒级）？
- 如何在 FedRL 框架下处理各 RSU 覆盖区域交通密度和拓扑的异质性？
- FedRL 聚合策略（FedAvg vs. 更复杂的方法）对变道策略质量的影响？
