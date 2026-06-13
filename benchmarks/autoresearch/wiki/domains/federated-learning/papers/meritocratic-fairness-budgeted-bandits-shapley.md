---
title: Meritocratic Fairness in Budgeted Combinatorial Multi-armed Bandits via Shapley Values
type: paper
domain: federated-learning
status: active
created: 2026-05-05
updated: 2026-05-05
tags:
  - bandits
  - fairness
  - shapley-value
  - federated-learning
paper:
  title: Meritocratic Fairness in Budgeted Combinatorial Multi-armed Bandits via Shapley Values
  authors:
    - Shradha Sharma
    - Swapnil Dhamal
    - Shweta Jain
  year: 2026
  venue: arXiv
  arxiv: "2605.00762v1"
  doi: ""
  code: ""
  project: ""
classification:
  label: federated-learning
  task:
    - fair bandit selection
  method_family:
    - Shapley value
    - combinatorial multi-armed bandits
    - meritocratic fairness
  modality:
    - tabular
  datasets:
    - federated learning client selection
    - social influence maximization
  metrics:
    - fairness regret
    - cumulative reward
evidence_level: skimmed
raw_sources:
  - raw/sources/2026-05-01-meritocratic-fairness-bandits-shapley.pdf
source_pages:
  - wiki/domains/federated-learning/concepts/federated-learning.md
---

# Meritocratic Fairness in Budgeted Combinatorial Multi-armed Bandits via Shapley Values

## Citation

Sharma et al., "Meritocratic Fairness in Budgeted Combinatorial Multi-armed Bandits via Shapley Values," arXiv:2605.00762v1, May 2026.

## One-Sentence Contribution

首次将 meritocratic fairness 引入 full-bandit feedback 的 budgeted combinatorial multi-armed bandits——提出 K-Shapley 值（限制最多 K 个联盟成员的 Shapley 值变体），并设计 K-SVFair-FBF 算法自适应估计 K-Shapley 值，在 O(T³/⁴) fairness regret 下实现均衡参与选择。

## Problem Setting

BCMAB-FBF (Budgeted Combinatorial Multi-Agent Bandits with Full-Bandit Feedback) 中的 fairness：

- **BCMAB**：每轮选择最多 K 个 arm 的超 arm，观察组合奖励而非个体奖励（full-bandit feedback）。
- **Fairness**：纯奖励最大化导致 winner-takes-all——高性能 arm 被反复选择，near-optimal arm 被忽略。
- **Meritocratic Fairness**：每个 arm 的选择频率应与 merit（对全局奖励的边际贡献）成比例。
- 两个核心挑战：(1) FBF 下个体 merit 不可直接观察；(2) 在未知价值函数下学习 merit 并平衡 exploration-exploitation。

应用场景：FL 客户端选择（按贡献选择客户端而非仅性能）、社交影响最大化（避免仅选少数 influencer）。

## Method

**K-Shapley Value**：
- 标准 Shapley 值假设可计算任意大小联盟的边际贡献。BCMAB 中联盟大小限制为 K，因此定义 K-Shapley 值——仅考虑大小 ≤K 的联盟。
- 证明 K-Shapley 值满足 Symmetry、Linearity、Null Player、Efficiency 四项公理（Shapley 值的所有核心属性向受限联盟的自然扩展）。

**K-SVFair-FBF** 算法：
- 在未知价值函数下自适应估计每个 arm 的 K-Shapley 值。
- 同时处理两种噪声来源：(1) bandit 反馈噪声（学习 valuation function）；(2) Monte Carlo 近似噪声（因精确 K-Shapley 计算需要指数级联盟枚举）。
- 平衡公平参与和可靠学习。

## Experiments

- 应用场景：FL 客户端选择、社交影响最大化。
- 与现有 fairness-in-bandits baselines 比较。

## Results

- 理论：K-SVFair-FBF 达到 O(T³/⁴) fairness regret bound。注意：即使无 fairness 约束，FBF 下最佳 regret 为 O(T²/³)——K-SVFair-FBF 仅以轻微额外代价实现了公平。
- 实验：在 FL 和社交影响任务中比现有公平基线更有效。

## Limitations

- O(T³/⁴) 的 regret 相比 reward-only optimal O(T²/³) 提升了 regret 阶数。
- Monte Carlo 近似质量影响实际 K-Shapley 值估计精度。
- 对非单调/非子模奖励函数的扩展性未讨论。

## Reusable Claims

- 声明：K-Shapley 值是 Shapley 值在受限联盟大小 <K 的自然扩展，保留了所有核心公理属性。
  证据：K-Shapley 值的公理推导（Symmetry、Linearity、Null Player、Efficiency）。
  范围：BCMAB 的 merit 定义。
  置信度：medium。

- 声明：meritocratic fairness 在 FL 客户端选择中可以实现公平而不牺牲过多全局模型质量。
  证据：FL 客户端选择实验中 K-SVFair-FBF 与纯奖励最大化 baselines 的比较。
  范围：FL 中的公平客户端选择。
  置信度：medium。

## Connections

- [FSCLB](federated-sketch-contextual-linear-bandits-fsclb.md)：同属 bandit 方向，维度对比——FSCLB 关注 contextual linear bandits 的计算/通信效率（sketching 降维），K-SVFair 关注 BCMAB 的 meritocratic fairness（K-Shapley 值）；FSCLB 的 regret 为 O(√ldT) optimal，K-SVFair 的 fairness regret 为 O(T³/⁴)；两者在 FL 中的应用场景互补（高效选择 vs. 公平参与）。
- [Federated Learning](../concepts/federated-learning.md)：FL 客户端选择是核心应用场景之一。

## Open Questions

- K-Shapley 值是否能够在线性/子模以外的奖励函数类中保持效率？
- Fairness regret bound 是否可进一步改进至 O(T²/³)？
- 与其他 fairness 定义（demographic parity、equal opportunity）在 bandit 上下文中的关系。

## Provenance

- 摄入时间：2026-05-05。
- 原始来源：[raw/sources/2026-05-01-meritocratic-fairness-bandits-shapley.pdf](../../../raw/sources/2026-05-01-meritocratic-fairness-bandits-shapley.pdf)。
- 证据等级：skimmed（基于摘要和前几页）。
