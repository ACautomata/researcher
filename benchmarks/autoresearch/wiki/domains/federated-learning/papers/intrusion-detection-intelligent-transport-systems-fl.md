---
title: A Comparative Analysis of Machine Learning Models for Intrusion Detection in Intelligent Transport Systems
type: paper
domain: federated-learning
status: active
created: 2026-05-05
updated: 2026-05-05
tags:
  - federated-learning
  - intrusion-detection
  - intelligent-transportation
  - edge-computing
  - trust-aware-aggregation
paper:
  title: "A Comparative Analysis of Machine Learning Models for Intrusion Detection in Intelligent Transport Systems"
  authors:
    - Zawad Yalmie Sazid
    - Robert Abbas
    - Sasa Maric
  year: 2026
  venue: arXiv
  arxiv: "2605.00279v1"
  doi: ""
  code: ""
  project: ""
classification:
  label: federated-learning
  task:
    - intrusion detection
  method_family:
    - federated learning
    - hybrid deep learning
    - random forest
    - SVM
  modality:
    - network traffic data
  datasets:
    - intrusion detection datasets
  metrics:
    - detection accuracy
    - privacy preservation
evidence_level: skimmed
raw_sources:
  - raw/sources/2026-04-30-intrusion-detection-its-fl.pdf
source_pages:
  - wiki/domains/federated-learning/concepts/federated-learning.md
---

# Intrusion Detection in Intelligent Transport Systems via Trust-Aware Federated Hybrid Learning

## Citation

Sazid et al., "A Comparative Analysis of Machine Learning Models for Intrusion Detection in Intelligent Transport Systems," arXiv:2605.00279v1, Apr 2026.

## One-Sentence Contribution

提出 trust-aware 联邦混合入侵检测框架——在边缘端用 Random Forest + Decision Tree + Linear SVM 学习互补流量表征，服务器端按数据量和可靠性双重加权聚合，解决边缘 ITS 环境中分布式安全检测的隐私-检测质量 trade-off。

## Problem Setting

边缘计算虽通过将处理移到靠近数据源来解决延迟和带宽约束，但扩大了网络攻击面（分布式、异构、资源受限的边缘节点）。传统签名 IDS 对加密流量和演变攻击模式无能为力。集中式 ML 需要原始数据汇聚，与隐私、带宽和弹性需求冲突。

## Method

**Trust-aware Federated Hybrid Intrusion Detection Framework**：

1. **Local Hybrid Detector**：在每个边缘节点部署 Random Forest（局部特征模式提取）+ Decision Tree（规则学习）+ Linear SVM（跨特征依赖建模）三个互补模型的混合方案。
2. **Federated Learning**：边缘节点不共享原始流量数据，仅共享模型更新。
3. **Trust-aware Aggregation**：服务器按 data volume 和 reliability 双重加权聚合——不可靠客户端的更新权重被降低。
4. 提出 4 个研究问题和 4 个实践目标（去噪表示学习、局部特征模式、跨特征依赖建模、联邦协作）。

## Experiments

- 使用真实入侵检测数据集。
- 在基线结果后转向完整联邦实现评估。

## Results

- 论文呈现了 baseline achieved results（摘要未提供定量数字），但呈现了混合检测器的基线性能和联邦框架架构。

## Limitations

- 实验部分可能是不完整/早期结果——摘要提到 "baseline achieved results" 和 "preliminary achieved results"。
- 联邦训练在非 IID 安全数据上的性能退化未分析。
- Trust 分数的精确定义和更新机制未在摘要中详述。

## Reusable Claims

- 声明：边缘 ITS 的安全检测受益于混合模型——RF（统计模式）+ DT（规则）+ SVM（判别边界），三者互补表征比单一模型更强。
  证据：hybrid detector baseline 设计。
  范围：ITS 边缘入侵检测。
  置信度：low（待完整实验验证）。

## Connections

- [Privacy-Preserving FL via DP/HE](privacy-preserving-fl-dp-he-cardiovascular.md)：同属 FL 安全/隐私方向——本文通过 FL 检测边缘网络攻击，对方通过 DP/HE 保护 FL 模型隐私。FL 既是安全方案的一部分（本文），也是需要保护的目标（对方）。
- [Federated Learning](../concepts/federated-learning.md)：ITS 领域的 FL 应用。
- 与 PALCAS 同属自动驾驶/ITS 相关，但关注安全检测而非决策规划。

## Open Questions

- 完整的联邦训练实验和定量比较结果。
- Trust-aware aggregation 对 adversarial client 注入的防御力。
- 在真实 5G V2X 边缘环境中的延迟和计算可行性。

## Provenance

- 摄入时间：2026-05-05。
- 原始来源：[raw/sources/2026-04-30-intrusion-detection-its-fl.pdf](../../../raw/sources/2026-04-30-intrusion-detection-its-fl.pdf)。
- 证据等级：skimmed（基于摘要和前几页）。
