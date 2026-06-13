---
title: "FSCLB: Scaling Federated Linear Contextual Bandits via Sketching"
type: paper
domain: federated-learning
status: active
created: 2026-05-05
updated: 2026-05-05
tags:
  - federated-learning
  - contextual-bandits
  - sketching
  - communication-efficiency
  - regret-bound
paper:
  title: "Scaling Federated Linear Contextual Bandits via Sketching"
  authors:
    - Hantao Yang
    - Hong Xie
    - Xutong Liu
    - Defu Lian
  year: 2026
  venue: arXiv
  arxiv: "2605.00500v1"
  doi: ""
  code: ""
  project: ""
classification:
  label: federated-learning
  task:
    - federated contextual linear bandits
  method_family:
    - sketching
    - contextual bandits
    - asynchronous communication
  modality:
    - vector data
  datasets:
    - synthetic
    - real-world
  metrics:
    - cumulative regret
    - computation cost
    - communication cost
evidence_level: skimmed
raw_sources:
  - raw/sources/2026-05-01-federated-sketch-contextual-linear-bandits.pdf
source_pages:
  - wiki/domains/federated-learning/concepts/federated-learning.md
---

# FSCLB: Scaling Federated Linear Contextual Bandits via Sketching

## Citation

Yang et al., "Scaling Federated Linear Contextual Bandits via Sketching," arXiv:2605.00500v1, May 2026.

## One-Sentence Contribution

提出 Federated Sketch Contextual Linear Bandits (FSCLB)——用 SVD 间接替代 O(d³) 行列式计算 + 双 sketch 策略将通信从 O(d²) 降至 O(ld)，理论 regret bound 在 sketch 尺寸超过协方差矩阵秩时退化为标准 O(√ldT) optimal bound。

## Problem Setting

联邦 contextual linear bandits 中高维数据 (d ≫ 1000) 造成：
- **计算瓶颈**：每轮每 agent 需 O(d³) 做矩阵行列式计算以决定是否通信。
- **通信瓶颈**：每轮需上传 O(d²) 参数（协方差矩阵）。

Sketching 可以降维，但 naive sketch 会破坏 local increment 导致异步通信条件失效；仅 sketch 上传不 sketch 下载仍使下载成本保持 O(d²)。

## Method

FSCLB 三个核心创新：

1. **SVD 间接行列式计算**：将局部 sketch 与服务器 sketch 合并，在 O(l × d) sketch 矩阵上执行 SVD，用奇异值间接获得行列式，复杂度从 O(d³) 降至 O(l²d)（l < d 为 sketch 尺寸）。
2. **双 Sketch 策略**：
   - 上传：交换紧凑 sketch 矩阵 + 累积奇异值，替代完整协方差矩阵，从 O(d²) 降至 O(ld)。
   - 下载：服务器合并 sketch 后进行二次 sketching，保证下载与上传 sketch 维度一致。
3. **SCFD (Spectral Compensation Frequent Directions)**：单调不减的 sketch 更新策略，既匹配异步通信触发规则（上传仅在充分局部增长后），又产生比经典 FD 更紧的 regret bound。

## Experiments

- 合成和真实世界数据集。
- 比较维度：累积 regret、计算成本、通信成本。

## Results

- 计算和通信成本降低超过 90%，仅牺牲可忽略的累积 reward。
- 理论 regret bound: O(√(d + M·l)·l·T)。当 l 超过协方差矩阵秩时，λ_l = 0，bound 简化为 O(√ldT)，匹配无 sketch 的 FedLinUCB optimal bound。

## Limitations

- l 的上界由协方差矩阵谱尾控制，对高秩数据可能需更大的 sketch 尺寸。
- 仅在 contextual linear bandits 设定下验证，未测试 kernelized/deep bandit 场景。

## Reusable Claims

- 声明：sketching 在 FL bandits 中的计算-通信-遗憾三方面可以达成几乎无损的 trade-off（>90% 开销降低，negligible regret 损失）。
  证据：FSCLB 的理论 regret bound 和合成/真实实验。
  范围：federated contextual linear bandits。
  置信度：medium。

- 声明：双 sketch 策略（上传 + 下载均压缩）是实现端到端通信降低的必要条件，单端 sketch 效果不完整。
  证据：上传 O(d²)→O(ld)，下载 O(d²)→O(ld)。
  范围：需要双向通信的 FL 系统。
  置信度：medium。

## Connections

- [Federated Learning](../concepts/federated-learning.md)：FL + bandits 交叉。
- [Meritocratic Fairness in BCMAB](meritocratic-fairness-budgeted-bandits-shapley.md)：同属 bandit 方向，维度对比——FSCLB 关注 contextual linear bandits 的 computation/communication 效率（sketching），后者关注 BCMAB 的 meritocratic fairness（K-Shapley 值）；FSCLB 的 regret O(√ldT) 为 reward optimal，后者的 O(T³/⁴) 为 fairness-aware bound，两者在 FL 客户端选择中互补。

## Open Questions

- Sketch 与 DP 的结合（sketch 本身可能提供一种隐私形式）。
- 非线性 bandit (kernel/deep) 中的 sketching 扩展。

## Provenance

- 摄入时间：2026-05-05。
- 原始来源：[raw/sources/2026-05-01-federated-sketch-contextual-linear-bandits.pdf](../../../raw/sources/2026-05-01-federated-sketch-contextual-linear-bandits.pdf)。
- 证据等级：skimmed（基于摘要和前 5 页）。
