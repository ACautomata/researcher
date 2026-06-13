---
title: FL Heterogeneity and Optimization
type: topic
domain: federated-learning
status: active
created: 2026-05-05
updated: 2026-05-05
tags:
  - federated-learning
  - heterogeneity
  - aggregation
  - personalization
  - multi-job-scheduling
  - label-correlation
source_pages:
  - wiki/domains/federated-learning/papers/fedhaw-hypergradient-aggregation-weights.md
  - wiki/domains/federated-learning/papers/fedkper-generalization-personalization-medical-fl.md
  - wiki/domains/federated-learning/papers/fedact-concurrent-federated-intelligence.md
  - wiki/domains/federated-learning/papers/fedharmony-heterogeneous-label-correlations-federated-multi-label.md
raw_sources:
  - raw/sources/2026-05-01-fedhaw-hypergradient-aggregation-weights.pdf
  - raw/sources/2026-05-01-fedkper-medical-fl-knowledge-personalization.pdf
  - raw/sources/2026-03-11-fedact-concurrent-federated-intelligence.pdf
  - raw/sources/2026-04-30-fedharmony-heterogeneous-label-correlations.pdf
---

# FL Heterogeneity and Optimization

## 当前论点

联邦学习中的异质性（heterogeneity）不是一个单一维度的问题，而是在三个层次上独立且互动地影响 FL 性能：**(1) 聚合层——如何组合异构客户端更新（FedHAW、FedHarmony）**；**(2) 任务层——如何在全局和本地目标间取得平衡（FedKPer）**；**(3) 系统层——如何调度异构资源上的并发训练任务（FedACT）**。这三个层次的优化信号来源不同但互补——聚合层看 gradient geometry（hypergradient、label correlation consensus），任务层看 loss landscape 的 local vs. global curvature，系统层看 device-job resource alignment。当前证据倾向于表明：**数据量加权的 FedAvg 聚合在三层上都远不是最优的**。

## 范围

- FL 聚合权重的优化：从固定加权（FedAvg）到可学习加权（FedLAW）到在线自适应加权（FedHAW）。
- 统计异质性的处理：label correlation drift（FedHarmony）、generalization-personalization trade-off（FedKPer）。
- 系统异质性的调度：multi-job FL 中的 device-job matching（FedACT）。
- 跨这些子方向的共同主题：如何用更丰富的信号替代简单的 data-size-weighted averaging。

## 关键线索

- FedAvg 的 data-size-weighted aggregation 在多标签学习中忽略标签相关性质量差异——共识标签相关性作为教师信号能更好纠正局部偏差（FedHarmony）。
- Hypergradient（梯度关于聚合权重的梯度）可以在线提取 aggregation 的优化信号——无需预先准备的 proxy 数据，且对实时通信环境变化有追踪能力（FedHAW）。
- FedHAW 的核心洞察：hypergradient descent 最初是为在线学习率优化设计的，但可以直接迁移到聚合权重空间——两者都是"优化外层超参数以最小化训练过程中的损失"。
- Generalization 和 personalization 不是对立的——selective alignment with global model 可以在改进两者 trade-off 的同时保持 retention（FedKPer）。
- Multi-job FL 中的 device-job matching 是独立于单作业 FL 中 client selection 的新问题——alignment scoring 超越了简单的硬件排名，需考虑设备-作业对的兼容性（FedACT）。
- Participation fairness 在 multi-job FL 中不仅关乎公平——通过让 underrepresented 设备贡献更多样化的数据，公平调度实际上提升了模型准确率（FedACT: +44.5%）。
- Forgetting 是统计异质 FL 中严重但被忽视的行为——FedKPer 将其作为与 generalization 和 personalization 并列的第三评估维度。

## 原子 Claims

- 声明：FL 聚合权重优化存在一个 spectrum：data-size weighted (FedAvg) → learnable with proxy data (FedLAW) → online hypergradient (FedHAW)——online 端消除了对 proxy 数据的依赖且可追踪环境变化。
  证据：FedHAW 相比 FedLAW 在通信错误条件下的鲁棒性提升。
  范围：FL 聚合策略。
  置信度：medium。
  张力：FedHAW 的超梯度更新频率和计算开销 vs. FedLAW 的预学习开销的完整比较未量化。

- 声明：联邦多标签学习中的 label correlation drift 是独立于 feature distribution shift 的异质性源——仅纠正后者不足以恢复全局标签依赖结构。
  证据：FedHarmony 的 FLAIR co-occurrence matrix 可视化和 consensus correlation 有效性。
  范围：federated multi-label learning。
  置信度：medium。

- 声明：Multi-job FL 的最优调度不仅需要硬件资源匹配，还需要 participation fairness——两者共同决定全局模型的准确率和作业完成时间。
  证据：FedACT alignment scoring + fairness module，JCT -8.3× + accuracy +44.5%。
  范围：multi-job FL。
  置信度：medium。

- 声明：Forgetting 应作为 FL 评估的标准第三维度（与 generalization 和 personalization 并列），特别是在 partial client participation 的 non-IID 设定下。
  证据：FedKPer 的 forgetting metrics 设计，医疗 FL 中观察到显著的遗忘行为。
  范围：涉及多轮迭代的 FL 系统。
  置信度：low（仅在一项工作中作为核心维度提出，尚未被社区广泛采纳）。

## 证据

- [FedHAW: Hypergradient-based Online Update of Aggregation Weights](../papers/fedhaw-hypergradient-aggregation-weights.md)：IEEE letter 2026，hypergradient 迁移，skimmed。
- [FedKPer: Generalization and Personalization in Medical FL](../papers/fedkper-generalization-personalization-medical-fl.md)：ICIP 2026，knowledge personalization，skimmed。
- [FedACT: Concurrent Federated Intelligence](../papers/fedact-concurrent-federated-intelligence.md)：IPDPS 2026，multi-job scheduling，skimmed。
- [FedHarmony: Heterogeneous Label Correlations](../papers/fedharmony-heterogeneous-label-correlations-federated-multi-label.md)：arXiv 2026，consensus correlation，skimmed。

## 张力

- FedHAW 的 hypergradient 优化聚合权重 vs. FedHarmony 的 consensus correlation 加权 vs. FedKPer 的 reliability+label-diversity 加权——三种聚合策略的优劣尚未直接比较。它们可能针对不同类型的异质性（system heterogeneity vs. label heterogeneity vs. data heterogeneity）各自最优。
- 在线更新的聚合权重（FedHAW）能否与 selective alignment 的本地训练（FedKPer）结合——即双端自适应（server-side online aggregation + client-side knowledge personalization）——是一个开放且有前景的方向。
- Multi-job FL (FedACT) 中的调度问题与单作业 FL 中的 client selection 是否可以统一为一个"有限资源下最优任务-设备分配"框架？

## 开放问题

- 三种聚合策略（hypergradient、consensus correlation、reliability-weighted）的直接比较基准。
- 双层同时自适应（server-side online aggregation + client-side selective alignment）对极端 non-IID 的鲁棒性。
- Multi-job FL 向非图像任务（NLP、多模态、联邦 RL）的扩展——alignment scoring 如何适应不同的资源需求特征？
- Forgetting 指标在非医疗 FL 场景中的基线测量和标准化。
