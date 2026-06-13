---
title: "FedKPer: Tackling Generalization and Personalization in Medical Federated Learning via Knowledge Personalization"
type: paper
domain: federated-learning
status: active
created: 2026-05-05
updated: 2026-05-05-evidence-upgrade
tags:
  - federated-learning
  - personalized-fl
  - medical-imaging
  - generalization
  - forgetting
paper:
  title: "FedKPer: Tackling Generalization and Personalization in Medical Federated Learning via Knowledge Personalization"
  authors:
    - Zoe Fowler
    - Ghassan AlRegib
  year: 2026
  venue: IEEE ICIP 2026
  arxiv: "2605.00698v1"
  doi: ""
  code: https://github.com/olivesgatech/FedKPer
  project: https://alregib.ece.gatech.edu/
classification:
  label: federated-learning
  task:
    - medical image classification
  method_family:
    - personalized federated learning
    - knowledge personalization
  modality:
    - medical images
  datasets:
    - BloodMNIST
    - OrganCMNIST
    - OrganSMNIST
  metrics:
    - global accuracy
    - local accuracy
    - backward transfer (forgetting)
    - consistency
evidence_level: full-paper
raw_sources:
  - raw/sources/2026-05-01-fedkper-medical-fl-knowledge-personalization.pdf
source_pages:
  - wiki/domains/federated-learning/concepts/federated-learning.md
---

# FedKPer: Tackling Generalization and Personalization in Medical Federated Learning via Knowledge Personalization

## Citation

Fowler & AlRegib, "FedKPer: Tackling Generalization and Personalization in Medical Federated Learning via Knowledge Personalization," IEEE ICIP, Apr 2026. arXiv:2605.00698v1. Code: github.com/olivesgatech/FedKPer.

## One-Sentence Contribution

提出 FedKPer——在本地训练阶段引入 knowledge personalization + 在全局聚合阶段按可靠性和标签多样性加权——首次同时优化医疗 FL 的 generalization 和 personalization，不牺牲遗忘抵抗（retention）。

## Problem Setting

医疗 FL 中统计异质性导致：
- 全局模型难以泛化到未见患者群体。
- 本地模型难以适配个体医院的数据分布。
- 异质性和部分客户端参与加剧 **forgetting**：先前学到的患者模式在模型更新后被错误分类。
- 现有方法将 generalization 和 personalization 视为独立挑战，忽视两者的 trade-off 与遗忘行为的关系。

## Method

FedKPer 两阶段设计：

1. **Knowledge Personalization (Local Stage)**：
   - 在每个本地设备训练阶段选择性对齐全局模型，而非完全遵循全局方向。
   - 保留对本地分布重要的知识，同时部分吸收全局知识。
2. **Reliability and Label-Diversity Weighted Aggregation (Global Stage)**：
   - 聚合时不仅按数据量加权，还按更新的可靠性和标签多样性加权——使具有丰富标签分布的可靠客户端贡献更多。
3. **Additional Metrics for Forgetting**：设计额外指标捕捉遗忘行为（连续训练后被错误分类的先前正确样本比例）。

## Experiments

**数据集**

- **BloodMNIST**：20 个本地客户端，Dirichlet α=0.1 分区（高度异质）。
- **OrganCMNIST**：30 个本地客户端，Dirichlet α=0.1。
- **OrganSMNIST**：50 个本地客户端，Dirichlet α=0.1。
- 全局测试集保留原始整体测试集；每个客户端从本地数据 Dₖ 中划出 20% 作为本地测试集。

**训练配置**

- 标准四层 CNN（FL 文献通用架构）。
- SGD 优化器，学习率 0.01。
- 每轮采样 10% 客户端，本地训练 5 epochs，总通信轮次 100。
- 所有结果报告为 3 个随机种子的平均值。

**Baselines (11 个)**

FedAvg、FedCurv、MOON、FedProx、FedNTD、FedAS、FedALA、Ditto、FedPer、FedKD、FedBABU。

**评估指标**

- Avg Global Accuracy、Avg Global BwT（backward transfer，衡量遗忘）、Avg Global Consistency、Avg Local Accuracy、Avg Worst Client Accuracy、Avg Local Consistency、Balance（全局-本地平衡：(Ā_g + Ā_k)/2）。
- 作者提出 IPFR (Inter-Peak Forgetting Rate)、AIPFR、Consistency 等遗忘评估指标。

## Results

**主实验 (Table 1)**

FedKPer 在所有三个数据集上取得最优全局精度、最低遗忘和最强的全局-本地平衡：

- **BloodMNIST**：Avg Global Acc 64.5%（FedAvg 40.9%，+23.6%）；BwT -0.127（FedAvg -0.255）；Consistency 0.823（FedAvg 0.721）；Avg Local Acc 86.8%（最高 FedALA 89.9% 但全局仅 51.6%）；Worst Client Acc 79.6%（次优 FedBABU 79.2%）；Balance 0.757（次优 FedNTD 0.719）。
- **OrganSMNIST**：Avg Global Acc 51.7%（FedAvg 44.5%，+7.2%）；BwT -0.024（FedAvg -0.103）；Consistency 0.899（FedAvg 0.811）；Worst Client Acc 51.1%（次优 FedALA 58.4% 但全局仅 37.5%）；Balance 0.626（次优 FedNTD 0.622）。
- **OrganCMNIST**：Avg Global Acc 66.0%（FedAvg 56.8%，+9.2%）；BwT -0.013（FedAvg -0.077）；Consistency 0.924（FedAvg 0.818）；Avg Local Acc 88.9%（次优 FedNTD 86.8% 但全局仅 61.8%）；Worst Client Acc 79.7%；Balance 0.774（次优 FedNTD 0.743）。

**关键发现**

- FedKPer 是唯一在所有三个数据集上同时实现最高全局精度和最低遗忘的方法。
- FedALA 在局部精度上偶尔领先，但全局精度大幅落后（如 OrganSMNIST 全局仅 37.5%），说明仅优化个性化会牺牲泛化。

**Ablation (Fig. 4)**

- KD Only（仅知识蒸馏项 Eq.3）：主要提升本地精度。
- Agg Only（仅聚合权重 Eq.6）：主要提升全局精度。
- FedKPer（两者结合）：全局-本地 trade-off 最优。

**计算效率 (Fig. 5)**

- BloodMNIST 上同累积 wall-clock 时间比较：FedKPer 在 500s 时全局精度比 FedAvg 提升 38.8%。FedKPer 在相同时间预算下始终取得更高精度。

## Limitations

- 仅在作者设计的 medical FL 场景中验证（非真实多医院部署）。
- reliability 和 label-diversity 的量化方法可能对设置敏感。

## Reusable Claims

- 声明：医疗 FL 中 generalization 和 personalization 不是对立的——通过 selective alignment 可以在不牺牲 retention 的情况下改进两者的权衡。
  证据：FedKPer 的 generalization-personalization-retention 三维度实验。
  范围：统计异质的 medical FL。
  置信度：medium。

- 声明：forgetting 在统计异质 FL 中是严重但被忽视的行为——应在 accuracy 之外作为独立指标评估。
  证据：FedKPer 引入专门 forgetting 指标。
  范围：所有涉及 continual/iterative 更新的 FL 系统。
  置信度：medium。

## Connections

- [FL Heterogeneity and Optimization](../topics/fl-heterogeneity-and-optimization.md)：本论文属于任务层异质性优化——selective alignment 在 generalization-personalization-forgetting 三维度上取得平衡。
- [Federated Learning](../concepts/federated-learning.md)：personalized FL 子方向。
- [FedHAW](fedhaw-hypergradient-aggregation-weights.md)：都解决 FL 异质性，FedHAW 通过在线 hypergradient 更新聚合权重，FedKPer 通过 knowledge personalization 和 refined aggregation。
- [Privacy-Preserving FL](privacy-preserving-fl-dp-he-cardiovascular.md)：同属 medical FL，关注点不同（privacy vs. personalization）。

## Open Questions

- Knowledge personalization 的 selective alignment 机制在不同模型架构间是否通用。
- Forgetting 指标的定义是否应成为 FL 评估的标准部分。
- 与 model-agnostic meta-learning (MAML) based pFL 方法的比较。

## Provenance

- 摄入时间：2026-05-05。
- 原始来源：[raw/sources/2026-05-01-fedkper-medical-fl-knowledge-personalization.pdf](../../../raw/sources/2026-05-01-fedkper-medical-fl-knowledge-personalization.pdf)。
- 证据等级：full-paper（完整实验数据从 PDF 提取，包含 Table 1 全部 12 方法 × 3 数据集定量结果和 ablation）。
