---
title: Privacy-Preserving Federated Learning via Differential Privacy and Homomorphic Encryption for Cardiovascular Disease Risk Modeling
type: paper
domain: federated-learning
status: active
created: 2026-05-05
updated: 2026-05-05-evidence-upgrade
tags:
  - federated-learning
  - differential-privacy
  - homomorphic-encryption
  - healthcare
  - cardiovascular
paper:
  title: Privacy-Preserving Federated Learning via Differential Privacy and Homomorphic Encryption for Cardiovascular Disease Risk Modeling
  authors:
    - Gaurang Sharma
    - Juha Pajula
    - Aada Illikainen
    - Markus Rautell
    - Noora Lipsonen
    - Petri Alhainen
    - Mika Hilvo
  year: 2026
  venue: arXiv
  arxiv: "2604.27598v1"
  doi: ""
  code: ""
  project: ""
classification:
  label: federated-learning
  task:
    - cardiovascular risk prediction
  method_family:
    - federated learning
    - differential privacy
    - homomorphic encryption
  modality:
    - tabular health data
  datasets:
    - Swedish national healthcare registry
  metrics:
    - AUROC
    - computational overhead
evidence_level: full-paper
raw_sources:
  - raw/sources/2026-04-30-privacy-preserving-fl-dp-he-cardiovascular.pdf
source_pages:
  - wiki/domains/federated-learning/concepts/federated-learning.md
---

# Privacy-Preserving Federated Learning via Differential Privacy and Homomorphic Encryption for Cardiovascular Disease Risk Modeling

## Citation

Sharma et al., "Privacy-Preserving Federated Learning via Differential Privacy and Homomorphic Encryption for Cardiovascular Disease Risk Modeling," arXiv:2604.27598v1, Apr 2026.

## One-Sentence Contribution

在真实多机构瑞典全国健康数据上，系统比较了 FL+DP 与 FL+HE 两种隐私增强方案的隐私-效用 trade-off，为碎片化医疗系统中的隐私保护 FL 部署提供了实用指南。

## Problem Setting

FL 减少数据集中化，但共享参数仍可能泄露敏感信息。DP 和 HE 可增强 FL 隐私保证，但它们在真实医疗环境中的比较性能和部署影响尚不清晰。需要回答：
- FL_DP 与 FL_HE 在不同模型（LR vs. NN）下的效用代价？
- 隐私保护程度与计算开销之间的权衡？

## Method

三种设置的对比评估：
- **FL_DP**：每个数据源头对本地模型更新进行梯度裁剪后加入校准噪声（DP-SGD 范式）。
- **FL_HE**：对模型参数应用同态加密，服务器在加密状态执行聚合运算。
- **Baselines**：标准 FL（FedAvg）和集中式机器学习（cML）。

LR 和 NN 两个学习者，使用瑞典全国健康数据评估心血管疾病风险预测。

## Experiments

**数据集与部署**

- 瑞典全国健康数据，四家机构：Södermanland、Östergötland、Uppsala（Solita 托管，Google Cloud e2-medium 实例）、Stockholm（Mediconsult 托管，Azure B2als v2 实例）。
- 任务：心血管疾病风险预测。
- 模型：Logistic Regression (LR，11 个可训练参数) 和 Neural Network (NN，66 个可训练参数)。
- 部署平台：SeH Platform（Docker 容器化，ShinyProxy Web 界面，Microsoft Entra ID 认证，mTLS 安全通信）。

**训练配置**

- 本地训练每轮 20 epochs，共 250 全局通信轮次。
- 学习率 0.01，batch size：Stockholm 100,000，其余客户端 20,000。
- 先仿真验证 → 再真实多机构生产部署。

**DP 配置**

- NN: Fraction=0.9, ε=5, NoiseVar=2.5, δ=10⁻¹, γ=5×10⁻⁴。
- LR: Fraction=0.99, ε=10⁴, NoiseVar=10², δ=10⁻³, γ=10⁻⁸。
- 稀疏向量技术 (SVT) 实现：clip bound τ → Laplace 噪声阈值选择参数 → 仅保留超过阈值的参数。

**HE 配置**

- CKKS 同态加密方案，多项式度 8192，系数模数 [60, 40, 40]，缩放因子 2⁴⁰。
- 服务器端加密聚合：先累加 → 单次密文-明文乘法归一化（避免密文除法）。

**Baselines**

- FedAvg（无隐私）、集中式机器学习 (cML，10 折交叉验证)。

## Results

**计算性能**

- **NN FedAvg**：37,771s (10h 29m 31s)
- **NN FedAvg_DP**：62,721s (17h 25m 21s) —— DP 增加 ~66% 时间开销
- **NN FedAvg_HE**：63,713s (17h 41m 53s) —— HE 比 DP 多 992s (16m 32s)
- **LR FedAvg**：1,181s；LR_DP：1,154s；LR_HE：1,117s（LR 下三者差异可忽略）
- 本地训练占总运行时间的绝大部分：LR 192.5s vs. NN 35,527.5s (9.87h)
- **cML**：LR 2.52s，NN 7.13s（集中式避免所有通信/同步/隐私开销）

**通信开销**

- NN 加密模型更新约 5.4 MB；加密 ~0.013s，解密 ~0.007s。
- LR 加密更新仅 1.8 KB；加密/解密各约 0.005s。
- 服务器端处理每个客户端更新 <0.12s，验证与注册 ~0.21s/客户端，聚合在最终更新到达后 ~0.20s 触发。

**隐私-效用权衡**

- **NN+DP**：放松 DP 约束（更高 ε、更低噪声）→ 收敛平滑、性能退化最小。严格约束 → 训练不稳定、预测性能下降。
- **LR+DP**：比 NN 对 DP 噪声更敏感——即使低噪声水平，LR 也出现性能退化。原因是 LR 仅 11 个参数，缺乏 NN 的参数冗余来吸收噪声。
- **NN+HE**：CKKS 的固定精度算术带来可忽略的数值偏差，模型效用基本保留。
- **cML AUC**：0.67（10 折交叉验证）——联邦方法达到与 cML 相当的性能，除 LR_DP 外。

**收敛行为**

- NN FedAvg/FedAvg_HE：约 20 轮内收敛；NN FedAvg_DP：~50 轮才收敛（噪声延迟收敛）。
- LR 因大批量而全程稳定（除 LR_DP 外）。FedAvg_HE 收敛最快，FedAvg 次之，FedAvg_DP 最慢。

## Limitations

- 仅覆盖心血管疾病预测场景，其他疾病/任务的泛化性未知。
- HE 的加密开销在更大模型上可能成为瓶颈。
- DP 隐私预算 (ε) 与效用关系的详细刻画未在摘要中呈现。

## Reusable Claims

- 声明：FL_HE 可在不牺牲预测性能的情况下达到与集中式学习相当的准确率，代价是加密计算开销。
  证据：全文表数据（skimmed），瑞典健康数据上的 AUROC 比较。
  范围：医疗场景 FL 隐私保护。
  置信度：medium。

- 声明：FL_DP 对线性模型（LR）的影响大于神经网络，因为 NN 的参数冗余能更好地吸收 DP 噪声。
  证据：LR vs. NN 在不同 DP 噪声水平下的性能对比。
  范围：tabular health prediction。
  置信度：medium。

## Connections

- [ITS Intrusion Detection](intrusion-detection-intelligent-transport-systems-fl.md)：同属 FL 安全/隐私方向——本文关注如何用 DP/HE 保护 FL 免受隐私泄露，ITS 论文关注如何用 FL 保护边缘节点免受网络攻击。两者是 FL 安全的不同面：隐私保护 vs. 威胁检测。
- [Federated Learning](../concepts/federated-learning.md)：本论文属于 FL 隐私保护子方向。
- 与 [FedKPer](fedkper-generalization-personalization-medical-fl.md) 同属 medical FL 应用，但关注隐私而非 personalized-generalization trade-off。

## Open Questions

- DP 和 HE 的组合（hybrid PETs）是否优于单独使用？
- 更大规模 FL（更多机构、更大模型）下的加密/DP 扩展性。
- 跨法规环境（如 GDPR vs. HIPAA）的合规性分析。

## Provenance

- 摄入时间：2026-05-05。
- 原始来源：[raw/sources/2026-04-30-privacy-preserving-fl-dp-he-cardiovascular.pdf](../../../raw/sources/2026-04-30-privacy-preserving-fl-dp-he-cardiovascular.pdf)。
- 证据等级：full-paper（完整实验数据从 PDF 提取，包含 NN/LR 运行时间、DP 参数、CKKS 配置和收敛分析）。
