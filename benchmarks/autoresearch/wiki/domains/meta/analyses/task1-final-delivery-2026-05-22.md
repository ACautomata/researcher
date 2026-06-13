---
title: 任务一最终交付 — Benchmark 构建与自测
type: delivery
domain: meta
status: active
created: 2026-05-22
tags:
  - task1
  - benchmark
  - seed-qa
  - self-test
  - delivery
source_pages:
  - wiki/domains/meta/analyses/needle-tests-2026-05-05.md
  - wiki/domains/meta/analyses/benchmark-expansion-2026-05-22.md
  - wiki/domains/meta/analyses/complete-benchmark-2026-05-22.md
  - wiki/domains/meta/analyses/self-test-report-2026-05-22.md
---

# 任务一：Benchmark 构建与自测 — 最终交付

> 项目：llmwiki Agent 开发
> 任务依据：2026-05-20 会议纪要，每人完成自己 agent 领域的四项任务
> 交付日期：2026-05-22

---

## 目录

1. [任务说明](#1-任务说明)
2. [交付物概览](#2-交付物概览)
3. [交付物一：Seed QA（人工构建，35 题）](#3-交付物一seed-qa人工构建35-题)
4. [交付物二：完整 Benchmark（50 题）](#4-交付物二完整-benchmark50-题)
5. [交付物三：自测报告](#5-交付物三自测报告)
6. [执行总结与改进建议](#6-执行总结与改进建议)

---

## 1. 任务说明

### 1.1 任务目标

给 llmwiki agent 构建一套系统性测试题（Benchmark），执行自测，输出测试结论。

### 1.2 要求步骤

| 步骤 | 内容 | 状态 |
|------|------|------|
| (1) 人工构建 QA（Seed） | 每条包含：输入材料、提问、标准答案 | ✅ 已完成（35 题） |
| (2) LLM 扩充 | 以 Seed QA 为参考，参考 InstructGPT 范式，让 LLM 自动生成更多 QA | ✅ 已完成（+15 题 → 50 题） |
| (3) 跑自测 | 通过 Claude Code 逐条在干净 session 喂给 agent，对比标准答案 | ✅ 已完成（Seed 35 题；Expansion 15 题待执行） |
| (4) 写自测报告 | 提交 PR 时汇报测试情况 | ✅ 已完成 |

### 1.3 交付物清单

| 编号 | 交付物 | 来源文件 | 说明 |
|------|--------|---------|------|
| **A** | Seed QA（35 题） | `needle-tests-2026-05-05.md` | 人工构建，覆盖 7 领域 × 4 题型 |
| **B** | 完整 Benchmark（50 题） | `complete-benchmark-2026-05-22.md` + `benchmark-expansion-2026-05-22.md` | Seed 35 + LLM 扩充 15 |
| **C** | 自测报告 | `self-test-report-2026-05-22.md` | Seed 执行结果（32✅ / 3⚠️）+ Expansion 执行计划 |

---

## 2. 交付物概览

### 2.1 总体结构

```
llmwiki Agent Benchmark（50 QA pairs）
│
├── Seed QA（人工构建）35 题
│   ├── Distillation               Q1-Q3     (3 题)
│   ├── OOD Detection              Q4-Q5     (2 题)
│   ├── Spectrum                   Q6-Q7     (2 题)
│   ├── Autonomous Driving         Q8-Q9     (2 题)
│   ├── Federated Learning         Q10-Q12   (3 题)
│   ├── LLM Reasoning              Q16-Q19   (4 题)
│   ├── FL Deep                    Q20-Q24   (5 题)
│   ├── Distillation Deep          Q25-Q28   (4 题)
│   ├── Cross-Domain               Q13-Q15, Q29-Q31 (6 题)
│   └── Meta                       Q32-Q35   (4 题)
│
├── Expansion QA（LLM 扩充）15 题
│   ├── Distillation               N1-N4     (4 题)
│   ├── Federated Learning         N5-N9     (5 题)
│   ├── Cross-Domain               N10-N12   (3 题)
│   └── Meta & Practical           N13-N15   (3 题)
│
└── 覆盖
    ├── 领域：7 个（Distillation / OOD / Spectrum / Autonomous Driving / FL / LLM Reasoning / Meta）
    ├── 论文：~22 篇（跨所有领域）
    ├── 题型：6 种（事实检索 / 跨论文比较 / 机制理解 / 边界判断量化 / 跨域连接 / 结构反模式）
    └── 证据等级覆盖：seed → expansion → meta-analysis
```

### 2.2 题型分布

| 题型 | 数量 | 占比 | 说明 |
|------|------|------|------|
| 事实检索 | 15 | 30% | 从 wiki 直接检索事实性答案 |
| 机制理解 | 12 | 24% | 理解论文方法的核心机制 |
| 跨论文比较 | 10 | 20% | 比较两篇或多篇论文的方法差异 |
| 边界判断/量化 | 5 | 10% | 理解方法局限性和量化表现 |
| 跨域连接 | 5 | 10% | 识别跨领域的技术概念关联 |
| 结构/反模式 | 3 | 6% | 评估 wiki 自身结构完整性 |

### 2.3 自测结果概要

```
Seed QA 35 题执行结果
├── ✅ 完全通过  32 题 (91.4%)
├── ⚠️ 部分通过   3 题  (8.6%)
└── ❌ 不通过     0 题  (0.0%)

可回答率：100% | 完全通过率：91.4%
```

---

## 3. 交付物一：Seed QA（人工构建，35 题）

> 完整文件：[needle-tests-2026-05-05.md](./needle-tests-2026-05-05.md)

### 3.1 构建方法

- **构建人**：人工（领域专家 + 论文阅读）
- **覆盖策略**：从 wiki 现有论文中按领域分组，每个领域覆盖 4 种题型
- **构建准则**：每条 QA 必须可仅从 wiki 内容检索验证，不依赖外部 LLM 知识

### 3.2 完整题列表

#### Distillation（3 题）

| ID | 题型 | 问题 | 答案核心 | 验证页面 |
|----|------|------|---------|---------|
| Q1 | 事实检索 | ProCo 用什么 metric 衡量跨模态 correspondence？ | Retrieval-based correspondence consistency metric | [ProCo](../../distillation/papers/correspondence-coverage-matters-multimodal-dataset-distillation.md) |
| Q2 | 跨论文比较 | 长尾蒸馏和 ProCo 的核心方法差异？ | 长尾用 statistial alignment 解决 class imbalance；ProCo 用 correspondence coverage 解决跨模态覆盖 | [RLDD](../../distillation/papers/rethinking-long-tailed-dataset-distillation.md)、[ProCo](../../distillation/papers/correspondence-coverage-matters-multimodal-dataset-distillation.md) |
| Q3 | 机制理解 | TAFAP trajectory 为何优于 snapshot？ | Snapshot 被后续训练步稀释，trajectory 控制完整优化动态 | [TAFAP](../../distillation/papers/targeted-data-protection-diffusion-model-training-trajectory.md) |

#### OOD Detection（2 题）

| ID | 题型 | 问题 | 答案核心 | 验证页面 |
|----|------|------|---------|---------|
| Q4 | 跨论文比较 | LSN vs NegPrompt 核心差异？ | LSN class-specific + 不可迁移；NegPrompt transferable + 跨分布泛化 | [LSN](../../outofdistributiondetection/papers/out-of-distribution-detection-with-negative-prompts.md)、[NegPrompt](../../outofdistributiondetection/papers/learning-transferable-negative-prompts-ood-detection.md) |
| Q5 | 机制理解 | Positive vs negative prompt learning 差异？ | Positive 需更多 prompt (8 vs 2) 和更长训练 (25 vs 5) | [LSN](../../outofdistributiondetection/papers/out-of-distribution-detection-with-negative-prompts.md) |

#### Spectrum（2 题）

| ID | 题型 | 问题 | 答案核心 | 验证页面 |
|----|------|------|---------|---------|
| Q6 | 方法链 | 从 UV-vis 到反应路径的完整 pipeline？ | 5 步：Transformer 增强 → UMAP 降维 → 拓扑流形 → Beer-Lambert 量化 → 中间体识别 | [TopoML](../../spectrum/papers/topological-machine-learning-nanocrystal-synthesis.md) |
| Q7 | 边界判断 | 拓扑流形学习的局限性？ | 4 项：需独立验证、泛化未测、因果差距、定性限制 | [Spectrum Topic](../../spectrum/topics/spectrum-based-reaction-pathway-discovery.md) |

#### Autonomous Driving（2 题）

| ID | 题型 | 问题 | 答案核心 | 验证页面 |
|----|------|------|---------|---------|
| Q8 | 方法创新 | PALCAS 为什么用 PDQN 混合动作空间？ | 同时处理离散变道决策 + 连续纵向控制 | [PALCAS](../../autonomous-driving/papers/palcas-priority-aware-lane-change-federated-rl.md) |
| Q9 | 场景约束 | PALCAS 的安全模型？ | RSS 模型；60% CAV 碰撞率 2.45%，MSR 93.33% | [PALCAS](../../autonomous-driving/papers/palcas-priority-aware-lane-change-federated-rl.md) |

#### Federated Learning（3 题）

| ID | 题型 | 问题 | 答案核心 | 验证页面 |
|----|------|------|---------|---------|
| Q10 | 架构理解 | EASE 三个残差锚及闭合机制？ | Modality Anchor (BKE) + Subspace Anchor (GSD) + Temporal Re-anchoring (PFL) | [EASE](../../federated-learning/papers/ease-federated-multimodal-unlearning.md) |
| Q11 | 跨域连接 | FedHD 与 distillation 域的技术连接？ | Dataset Distillation 概念页 + 多模态蒸馏 + 长尾 DD 共享分布匹配哲学 | [FedHD](../../federated-learning/papers/fedhd-federated-distillation-whole-slide-image.md) |
| Q12 | 分类判断 | AgentReputation 属于 FL 吗？ | 不是 FL；去中心化 AI agent 声誉框架，标记为 decentralized-ai | [AgentReputation](../../federated-learning/papers/agentreputation-decentralized-agentic-ai-reputation.md) |

#### LLM Reasoning（4 题）

| ID | 题型 | 问题 | 答案核心 | 验证页面 |
|----|------|------|---------|---------|
| Q16 | 事实检索 | CoRD 的步骤选择准则及优势？ | Predictive perplexity，优于 PRM (需训练) 和 Binary Judgment (过粗) | [CoRD](../../llm-reasoning/papers/distilling-long-cot-reasoning-cord.md) |
| Q17 | 机制理解 | 逐步协同解码优于策展式的两个根本局限？ | (1) 无 teacher 交互 → 实时融合；(2) 缺乏动态探索 → beam search 中途调整 | [CoRD](../../llm-reasoning/papers/distilling-long-cot-reasoning-cord.md) |
| Q18 | 跨域区分 | Long-CoT 推理蒸馏 vs 数据集蒸馏的根本区别？ | 模型级蒸馏 (训练学生模型) vs 数据级压缩 (合成训练集) | [Long-CoT 概念](../../llm-reasoning/concepts/long-cot-reasoning-distillation.md)、[Dataset Distillation](../../distillation/concepts/dataset-distillation.md) |
| Q19 | 跨域连接 | CoRD 的多 teacher 协同 vs FedHD 的 curriculum federation 共性？ | 共性：拒绝均匀融合，受控增量整合。区别：推理时 vs 训练时 | [CoRD](../../llm-reasoning/papers/distilling-long-cot-reasoning-cord.md)、[FedHD](../../federated-learning/papers/fedhd-federated-distillation-whole-slide-image.md) |

#### FL Deep（5 题）

| ID | 题型 | 问题 | 答案核心 | 验证页面 |
|----|------|------|---------|---------|
| Q20 | 机制理解 | FedSD2C 双层信息损失？ | 训练损（数据→模型）+ 生成损（模型→逆向数据）；V-information Core-Set + Fourier + Autoencoder 端到端消除 | [FedSD2C](../../federated-learning/papers/fedsd2c-one-shot-fl-distiller-distillate.md) |
| Q21 | 方法迁移 | FedHAW hypergradient 核心洞察？ | 在线提取聚合优化信号，无需 proxy 数据；vs FedLAW: 无额外数据 + 实时追踪 + 鲁棒 | [FedHAW](../../federated-learning/papers/fedhaw-hypergradient-aggregation-weights.md) |
| Q22 | 跨论文比较 | FedHarmony vs FedAvg 在多标签中的差异？ | FedAvg 按数据量加权 → 标签偏差大时污染全局；FedHarmony 用 consensus correlation 替代 | [FedHarmony](../../federated-learning/papers/fedharmony-heterogeneous-label-correlations-federated-multi-label.md) |
| Q23 | 系统设计 | FedACT alignment scoring 超越硬件排名的因素？ | 设备-作业兼容性 + participation fairness（防过度代表/提数据多样性） | [FedACT](../../federated-learning/papers/fedact-concurrent-federated-intelligence.md) |
| Q24 | 量化对比 | FedACT 硬件配置和关键数字？ | 4×A4000 + i9-10900X + 64GB；JCT 8.3× 减少；Acc +44.5% | [FedACT](../../federated-learning/papers/fedact-concurrent-federated-intelligence.md) |

#### Distillation Deep（4 题）

| ID | 题型 | 问题 | 答案核心 | 验证页面 |
|----|------|------|---------|---------|
| Q25 | 事实检索 | COBRA 的跨群体重心计算？ | Uniform-weight barycenter，squared Mahalanobis 闭式解；避免群体比例加权的多数主导偏差 | [COBRA](../../distillation/papers/fair-dataset-distillation-cobra.md) |
| Q26 | 跨论文比较 | COBRA vs RLDD 公平性维度差异？ | RLDD：类间不公平 (class imbalance)；COBRA：类内不公平 (subgroup bias)；正交互补 | [RLDD](../../distillation/papers/rethinking-long-tailed-dataset-distillation.md)、[COBRA](../../distillation/papers/fair-dataset-distillation-cobra.md) |
| Q27 | 机制理解 | COBRA 为何与所有主流蒸馏方法兼容？ | "只改 target、不改 loss"——替换聚合表示目标为 barycentric target，其余流程不变 | [COBRA](../../distillation/papers/fair-dataset-distillation-cobra.md) |
| Q28 | 消融分析 | RLDD 三组件贡献？ | Stat Align -10% / BN Recalib -2% / Multi-Round Init -1% | [RLDD](../../distillation/papers/rethinking-long-tailed-dataset-distillation.md) |

#### Cross-Domain（6 题）

| ID | 题型 | 问题 | 答案核心 | 验证页面 |
|----|------|------|---------|---------|
| Q13 | 跨域综合 | 联邦蒸馏跨越哪几个域？ | 3 域：FL (FedHD/EASE) + Distillation (DD/ProCo/TAFAP) + AD (PALCAS) | [FL Topic](../../federated-learning/topics/federated-distillation-and-unlearning.md) |
| Q14 | 证据等级 | 当前 wiki 中 full-paper 论文有哪些？ | 见 3.3 节专项说明 | [index.md](../../index.md) |
| Q15 | 孤儿检测 | 哪些论文未被 topic 页索引？ | 6 篇：privacy-preserving-fl-dp-he, agentreputation, intrusion-detection-its, federated-weather-modeling, fsclb, meritocratic-fairness | [index.md](../../index.md) |
| Q29 | 跨域连接 | FedSD2C vs ProCo 压缩哲学异同？ | 同：追求信息量最大保留；异：目标（通信包 vs 合成集）+ 手段 + 场景 | [FedSD2C](../../federated-learning/papers/fedsd2c-one-shot-fl-distiller-distillate.md)、[ProCo](../../distillation/papers/correspondence-coverage-matters-multimodal-dataset-distillation.md) |
| Q30 | 跨域连接 | TAFAP trajectory alignment vs CoRD step-wise decoding 哲学共性？ | "过程包含快照丢失的信息"——优化轨迹 vs 推理链中的中间决策 | [TAFAP](../../distillation/papers/targeted-data-protection-diffusion-model-training-trajectory.md)、[CoRD](../../llm-reasoning/papers/distilling-long-cot-reasoning-cord.md) |
| Q31 | 三域交叉 | Cross-modal coupling 三重角色？ | 蒸馏：效率来源 (ProCo)；遗忘：主要障碍 (EASE)；OOD 检测：控制手段 (LSN) | [ProCo](../../distillation/papers/correspondence-coverage-matters-multimodal-dataset-distillation.md)、[EASE](../../federated-learning/papers/ease-federated-multimodal-unlearning.md)、[LSN](../../outofdistributiondetection/papers/out-of-distribution-detection-with-negative-prompts.md) |

#### Meta（4 题）

| ID | 题型 | 问题 | 答案核心 | 验证页面 |
|----|------|------|---------|---------|
| Q32 | 结构完整性 | 缺少哪些正式 comparison 页？ | LSN/NegPrompt、COBRA/RLDD、FedHD/FedSD2C 等至少 3 对 | [index.md](../../index.md) |
| Q33 | 孤儿检测 | 6 篇孤儿论文如何重组？ | FL Privacy and Security 新 topic + Federated Bandits 新 topic + decentralized-ai 迁移 | [index.md](../../index.md) |
| Q34 | 优先级 | 哪些 skimmed 论文优先升级？ | EASE > ProCo > TAFAP（依跨域引用度排序） | [index.md](../../index.md) |
| Q35 | 反模式 | Wiki 存在哪些结构问题？ | 4 项：0 comparison / 0 method 独立页 / 6 orphan / 捞针未全量 | [AGENTS.md](../../../AGENTS.md) |

### 3.3 专项：证据等级状态（对应 Q14）

| 等级 | 数量 | 论文 |
|------|------|------|
| **full-paper** | 14 篇 | Long-tailed Dataset Distillation, LSN (ICLR 2024), NegPrompt (CVPR 2024), Topological ML (JACS 2025), PALCAS, Rethinking Long-tailed Distillation, 以及其他升级后 full-paper |
| **skimmed** | 8 篇 | ProCo, TAFAP, EASE, AgentReputation, intrusion-detection-its, federated-weather-modeling, FSCLB, meritocratic-fairness |
| **abstract-only** | 0 篇 | 已全部升级 |

---

## 4. 交付物二：完整 Benchmark（50 题）

> 完整文件：[complete-benchmark-2026-05-22.md](./complete-benchmark-2026-05-22.md) + [benchmark-expansion-2026-05-22.md](./benchmark-expansion-2026-05-22.md)

### 4.1 LLM 扩充方法

以 Seed QA（人工构建 35 题）作为参考，遵循 InstructGPT 范式的思路，由 LLM（OpenClaw agent）基于论文全文页生成新 QA pair。生成准则：

1. **覆盖缺口**：覆盖 Seed QA 尚未充分触及的新 ingest 论文和技术细节
2. **格式一致**：保持问题 + 期望答案 + 验证页面的统一格式
3. **深层技术**：优先关注新 ingest 论文（Continual Distillation）和已有论文的深层机制
4. **量化补充**：增加量化对比类问题和实用边界类问题
5. **可检索**：每道题必须可仅从 wiki 内容检索验证

### 4.2 Expansion QA 列表（15 题）

#### Distillation（4 题）

| ID | 题型 | 问题 | 答案核心 | 验证页面 |
|----|------|------|---------|---------|
| N1 | 机制理解 | Continual Distillation 中 UKT 和 UKF 分别指什么？核心矛盾？ | UKT = 外部数据带来未见领域知识；UKF = 后续教师覆盖先前知识；外部数据同时触发两者 | [CD Paper](../../distillation/papers/continual-distillation-teachers-different-domains.md) |
| N2 | 方法理解 | SE2D 如何平衡 UKT 和 UKF？ | Logit preservation：保留的 logits 编码教师响应模式 → 降低 UKF（惩罚偏离）+ 提升 UKT（持续可用） | [CD Paper](../../distillation/papers/continual-distillation-teachers-different-domains.md) |
| N3 | 量化对比 | COBRA IPC=1 下公平性表现？ | EOD 4.9 vs Vanilla 17.2；样本越少 barycenter 保护效应越突出 | [COBRA](../../distillation/papers/fair-dataset-distillation-cobra.md) |
| N4 | 跨域连接 | CD vs DD 核心区别？ | CD = 模型级蒸馏（KL divergence）；DD = 数据级压缩（gradient/distribution matching） | [CD Paper](../../distillation/papers/continual-distillation-teachers-different-domains.md)、[DD 概念](../../distillation/concepts/dataset-distillation.md) |

#### Federated Learning（5 题）

| ID | 题型 | 问题 | 答案核心 | 验证页面 |
|----|------|------|---------|---------|
| N5 | 事实检索 | FedHD 三个核心组件？ | GM Feature Alignment + One-to-One Distillation + Curriculum Federation | [FedHD](../../federated-learning/papers/fedhd-federated-distillation-whole-slide-image.md) |
| N6 | 方法迁移 | FedKPer selective alignment 如何改进 trade-off？第三维度？ | 部分参数对齐改进 gen+pers；引入 forgetting 作为第三评估维度 | [FedKPer](../../federated-learning/papers/fedkper-generalization-personalization-medical-fl.md) |
| N7 | 量化对比 | FedACT participation fairness 的量化效果？ | JCT 8.3× + Acc 44.5%；fair scheduling 不只是伦理需求也是性能手段 | [FedACT](../../federated-learning/papers/fedact-concurrent-federated-intelligence.md) |
| N8 | 机制理解 | FSCLB 双 sketch 策略？ | 特征 sketch (count sketch) + 梯度 sketch；SVD 间接行列式处理加性噪声 | [FSCLB](../../federated-learning/papers/federated-sketch-contextual-linear-bandits-fsclb.md) |
| N9 | 跨论文比较 | FedHarmony 共识 vs COBRA barycenter 哲学共性？ | 共性：拒绝比例加权；不同：场景 + 替代方案；哲学：规模不决定影响力 | [FedHarmony](../../federated-learning/papers/fedharmony-heterogeneous-label-correlations-federated-multi-label.md)、[COBRA](../../distillation/papers/fair-dataset-distillation-cobra.md) |

#### Cross-Domain（3 题）

| ID | 题型 | 问题 | 答案核心 | 验证页面 |
|----|------|------|---------|---------|
| N10 | 跨域连接 | "受控增量整合"在三域中的体现？ | FedHD 课程联邦 + CoRD 逐步解码 + CD SE2D logit preservation | [FedHD](../../federated-learning/papers/fedhd-federated-distillation-whole-slide-image.md)、[CoRD](../../llm-reasoning/papers/distilling-long-cot-reasoning-cord.md)、[CD](../../distillation/papers/continual-distillation-teachers-different-domains.md) |
| N11 | 三域交叉 | UKF 与 FL forgetting 是同一问题吗？ | 共享"新知识覆盖旧知识"；场景不同（蒸馏管道 vs 联邦训练） | [CD](../../distillation/papers/continual-distillation-teachers-different-domains.md)、[FedKPer](../../federated-learning/papers/fedkper-generalization-personalization-medical-fl.md) |
| N12 | 跨域识别 | Wiki 中基于 matching 的方法家族图谱？ | 6 种：Trajectory/Gradient/Distribution/Feature/Device-Job/Resource Matching | [TAFAP](../../distillation/papers/targeted-data-protection-diffusion-model-training-trajectory.md)、[COBRA](../../distillation/papers/fair-dataset-distillation-cobra.md)、[FedHD](../../federated-learning/papers/fedhd-federated-distillation-whole-slide-image.md)、[FedACT](../../federated-learning/papers/fedact-concurrent-federated-intelligence.md) |

#### Meta & Practical（3 题）

| ID | 题型 | 问题 | 答案核心 | 验证页面 |
|----|------|------|---------|---------|
| N13 | 证据等级 | CD 的 evidence_level 及信任度把握？ | Skimmed：概念可信，定量数据需验证；引用时标注级别 | [CD Paper](../../distillation/papers/continual-distillation-teachers-different-domains.md) |
| N14 | 反模式 | Method/Dataset/Metric 独立页创建情况？ | 0 个已创建 → 违反 DRY 原则：无法共享引用、无法追踪演化、手动维护不一致 | [AGENTS.md](../../../AGENTS.md) |
| N15 | 维护建议 | 基于测试结果的改进优先级？ | P0：修复 Q5/Q9/Q14 缺失；P1：创建 comparison 页；P2：消除 orphan + method 独立页 | [Needle Tests](needle-tests-2026-05-05.md) |

### 4.3 Benchmark 使用说明

```bash
# 运行方式
# 1. 对每条 QA 在干净 session 中执行
# 2. 读取 AGENTS.md + wiki/index.md 完成上下文加载
# 3. 提问
# 4. 对比"期望答案"逐点判定：

✅ 完全通过 = 核心结论正确，关键细节齐全
⚠️ 部分通过 = 核心结论正确但关键细节缺失
❌ 不通过   = 核心结论错误 / 无法从 wiki 检索

# 更新策略
# - 每次 major ingest 后随机选 5-8 题执行捞针
# - 新增论文 → 新增对应 QA
# - 发现知识缺口 → 转化为新测试题
# - 期望答案随 wiki 演化同步更新
```

---

## 5. 交付物三：自测报告

> 完整文件：[self-test-report-2026-05-22.md](./self-test-report-2026-05-22.md)

### 5.1 测试方法论

- **测试对象**：llmwiki agent（在 AGENTS.md 上下文下运行的 Claude Code）
- **测试方式**：每条 Q 在干净 session 中提给 agent，agent 基于 wiki 内容检索回答
- **判定标准**：
  - ✅ 完全通过：核心结论正确，关键细节齐全
  - ⚠️ 部分通过：核心结论正确但关键细节缺失
  - ❌ 不通过：核心结论错误或无法从 wiki 检索
- **测试输入格式**：

```markdown
## 问题
[提问内容]

## 背景
[相关 wiki 路径 / 可选上下文]

请基于 wiki 内容回答上述问题。
```

### 5.2 Seed QA 执行结果

#### 总览

| 指标 | 数值 |
|------|------|
| 总题数 | 35 |
| ✅ 完全通过 | 32 (91.4%) |
| ⚠️ 部分通过 | 3 (8.6%) |
| ❌ 不通过 | 0 (0.0%) |
| 可回答率 | 100% |
| 完全通过率 | 91.4% |

#### 逐题结果表

| 题号 | 领域 | 题型 | 结果 | 说明 |
|------|------|------|:----:|------|
| Q1 | Distillation | 事实检索 | ✅ | ProCo 的 retrieval-based 指标已明确记录 |
| Q2 | Distillation | 跨论文比较 | ✅ | RLDD vs ProCo 差异清晰 |
| Q3 | Distillation | 机制理解 | ✅ | TAFAP trajectory vs snapshot 完整 |
| Q4 | OOD Detection | 跨论文比较 | ✅ | LSN vs NegPrompt 差异明确 |
| Q5 | OOD Detection | 机制理解 | ⚠️ | 缺定量细节：prompt 数 (8 vs 2)、epoch (25 vs 5) |
| Q6 | Spectrum | 方法链 | ✅ | 5 步 pipeline 完整 |
| Q7 | Spectrum | 边界判断 | ✅ | 4 项局限均有记录 |
| Q8 | Autonomous Driving | 方法创新 | ✅ | PDQN 混合动作空间明确 |
| Q9 | Autonomous Driving | 场景约束 | ⚠️ | 缺绝对碰撞率 2.45% |
| Q10 | Federated Learning | 架构理解 | ✅ | EASE 三锚完整 |
| Q11 | Federated Learning | 跨域连接 | ✅ | FedHD↔distillation 连接存在 |
| Q12 | Federated Learning | 分类判断 | ✅ | AgentReputation 标记已记录 |
| Q13 | Cross-Domain | 跨域比较 | ✅ | 跨 3 域连接完整 |
| Q14 | Cross-Domain | 证据等级 | ⚠️ | 期望答案过时（14 篇 vs 6 篇） |
| Q15 | Cross-Domain | 孤儿检测 | ✅ | 6 篇 orphan 可验证 |
| Q16 | LLM Reasoning | 事实检索 | ✅ | predictive perplexity 完整 |
| Q17 | LLM Reasoning | 机制理解 | ✅ | 策展式两局限完整 |
| Q18 | LLM Reasoning | 跨域区分 | ✅ | 模型级 vs 数据级蒸馏区分明确 |
| Q19 | LLM Reasoning | 跨域连接 | ✅ | CoRD + FedHD 哲学共性可合成 |
| Q20 | FL Deep | 机制理解 | ✅ | FedSD2C 双层信息损失完整 |
| Q21 | FL Deep | 方法迁移 | ✅ | FedHAW hypergradient 洞察明确 |
| Q22 | FL Deep | 跨论文比较 | ✅ | FedHarmony vs FedAvg 差异完整 |
| Q23 | FL Deep | 系统设计 | ✅ | FedACT alignment scoring 完整 |
| Q24 | FL Deep | 量化对比 | ✅ | 硬件 / JCT 8.3× / Acc +44.5% 验证 |
| Q25 | Distillation Deep | 事实检索 | ✅ | COBRA barycenter 完整 |
| Q26 | Distillation Deep | 跨论文比较 | ✅ | COBRA vs RLDD 互补明确 |
| Q27 | Distillation Deep | 机制理解 | ✅ | COBRA"只改 target 不改 loss" 明确 |
| Q28 | Distillation Deep | 消融分析 | ✅ | RLDD 三组件贡献验证 |
| Q29 | Cross-Domain | 跨域连接 | ✅ | FedSD2C vs ProCo 哲学可从页面合成 |
| Q30 | Cross-Domain | 跨域连接 | ✅ | TAFAP ↔ CoRD 共享哲学可验证 |
| Q31 | Cross-Domain | 三域交叉 | ✅ | cross-modal coupling 三重角色可合成 |
| Q32 | Meta | 结构完整性 | ✅ | comparison 缺口可验证 |
| Q33 | Meta | 孤儿检测 | ✅ | 6 篇 orphan + 重组方案可检索 |
| Q34 | Meta | 优先级 | ✅ | 升级优先级可从引用度推理 |
| Q35 | Meta | 反模式 | ✅ | 4 项结构问题可验证 |

### 5.3 3 题部分通过的改进建议

| 题号 | 缺失内容 | 改进动作 | 优先级 |
|:----:|---------|---------|:------:|
| Q5 | LSN Table 5：prompt 数 (8 vs 2)、epoch (25 vs 5) | 在 LSN 论文页补充具体数字 | P0 |
| Q9 | PALCAS 绝对碰撞率 (2.45% at 60% CAV) | 在 PALCAS 论文页实验结果中补充 | P0 |
| Q14 | 期望答案过时（14 篇而非 6 篇 full-paper） | 更新期望答案或改为动态描述 | P0 |

### 5.4 Expansion QA 执行计划

Expansion QA（15 题）的期望答案和验证页面已在 `benchmark-expansion-2026-05-22.md` 中准备完毕，但尚未通过 Claude Code 在干净 session 中实际执行。计划如下：

| ID | 领域 | 题型 | 验证页面 |
|:--:|------|------|---------|
| N1 | Distillation | 机制理解 | CD paper |
| N2 | Distillation | 方法理解 | CD paper |
| N3 | Distillation | 量化对比 | COBRA paper |
| N4 | Distillation | 跨域连接 | CD + DD concept |
| N5 | FL | 事实检索 | FedHD paper |
| N6 | FL | 方法迁移 | FedKPer + FL topic |
| N7 | FL | 量化对比 | FedACT paper |
| N8 | FL | 机制理解 | FSCLB paper |
| N9 | Cross-Domain | 跨论文比较 | FedHarmony + COBRA |
| N10 | Cross-Domain | 跨域连接 | FedHD + CoRD + CD |
| N11 | Cross-Domain | 三域交叉 | CD + FedKPer |
| N12 | Cross-Domain | 跨域识别 | TAFAP + COBRA + FedHD + FedACT |
| N13 | Meta | 证据等级 | CD paper |
| N14 | Meta | 反模式 | AGENTS.md + Needle Tests |
| N15 | Meta | 维护建议 | Needle Tests execution report |

### 5.5 与历史执行的对比

| 指标 | 5/5（初始 15 题） | 5/20（Seed 35 题） | 5/22（Expansion +15 → 50 题） |
|------|:-----------------:|:------------------:|:-----------------------------:|
| 题目数 | 15 | 35 | **50** |
| 已执行 | 0 | 35 | 35 / 50 |
| 可回答率 | — | 100% | 100%（Seed） |
| 完全通过率 | — | 91.4% | 91.4%（Seed） |
| 新覆盖域 | — | +LLM Reasoning, +Meta | +CD, +FedHD, +FSCLB, +Cross-Domain Practical |

---

## 6. 执行总结与改进建议

### 6.1 覆盖率分析

```
领域覆盖（基于论文数 vs. 题数）：
Distillation:        5 篇论文 →  7 题 (14%)    ⚠️ 相对不足
OOD Detection:       2 篇论文 →  2 题  (4%)
Spectrum:            1 篇论文 →  2 题  (4%)
Autonomous Driving:  1 篇论文 →  2 题  (4%)
Federated Learning: 12 篇论文 → 13 题 (26%)    ✅ 覆盖充分
LLM Reasoning:       1 篇论文 →  4 题  (8%)
Meta / Cross-Domain:   —      → 20 题 (40%)    ✅
```

### 6.2 质量评估

**优势：**
- ✅ 可回答率 100% — 无题目的答案完全"查不到"
- ✅ 完全通过率 91.4% — 多数期望答案可直接从 wiki 检索
- ✅ 题型丰富 — 6 种题型覆盖从事实检索到反模式分析
- ✅ 跨域连接题目质量高 — 体现 wiki 的知识关联优势

**不足：**
- ⚠️ 按论文数的覆盖率不均衡（FL 12 篇 vs Spectrum 1 篇）
- ⚠️ 3 题部分通过全部是"定量细节缺失" — wiki 定性描述强，但具体数字需补充
- ⚠️ 跨域题目依赖 agent 的合成推理能力（非纯检索）

### 6.3 改进路线图

```
P0（立即修复）
├── LSN 论文页 → 补充 prompt 数 (8 vs 2) 和 epoch (25 vs 5)
├── PALCAS 论文页 → 补充绝对碰撞率 2.45%
└── Q14 期望答案 → 更新为当前 14 篇 full-paper 状态

P1（短期改进）
├── 创建首批 comparison 页（LSN vs NegPrompt 优先）
├── 执行 Expansion QA 的 15 题测试
└── 为 Q5 / Q9 缺失的定量细节补充 wiki 内容

P2（长期工程）
├── 创建首批 method/dataset/metric 独立页
├── 消除 6 篇孤儿论文（重组 topic 页）
├── 每次 major ingest 后执行 5-8 题捞针
├── 新增论文后同步创建 1-2 道对应 QA
└── 季度性更新期望答案以匹配 wiki 演化
```

### 6.4 文件索引

| 交付物 | 文件路径 | 文件大小 | 状态 |
|--------|---------|:--------:|:----:|
| 任务说明 | `D:\llmwiki\任务说明.docx` | 21.7 KB | — |
| Seed QA（35 题） | `D:\llmwiki\wiki\domains\meta\analyses\needle-tests-2026-05-05.md` | 37.7 KB | ✅ |
| Benchmark LLM 扩充（15 题） | `D:\llmwiki\wiki\domains\meta\analyses\benchmark-expansion-2026-05-22.md` | 16.0 KB | ✅ |
| 完整 Benchmark 总览（50 题） | `D:\llmwiki\wiki\domains\meta\analyses\complete-benchmark-2026-05-22.md` | 4.6 KB | ✅ |
| 自测报告 | `D:\llmwiki\wiki\domains\meta\analyses\self-test-report-2026-05-22.md` | 10.8 KB | ✅ |
| **本交付文档（最终汇总）** | `D:\llmwiki\wiki\domains\meta\analyses\task1-final-delivery-2026-05-22.md` | 本文件 | ✅ New |

---

> **编写说明**：本文档整合了任务一所需的三项交付物——Seed QA（35 题人工构建）、完整 Benchmark（50 题，含 LLM 扩充 15 题）、自测报告（32✅ / 3⚠️ / 0❌）。各子文件保持独立，本文件作为统一入口和最终交付汇总。
