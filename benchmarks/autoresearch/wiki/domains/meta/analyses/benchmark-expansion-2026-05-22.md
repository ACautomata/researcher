---
title: Benchmark LLM Expansion — 15 New QA Pairs
type: analysis
domain: meta
status: active
created: 2026-05-22
updated: 2026-05-22
tags:
  - qa
  - benchmark
  - llm-expansion
source_pages:
  - wiki/domains/meta/analyses/needle-tests-2026-05-05.md
---

# Benchmark LLM Expansion

## Method（InstructGPT 范式）

以 needle-tests.md 中的人工构建 35 题作为 Seed QA，使用 LLM（OpenClaw agent）参考论文全文页生成新 QA pair。生成准则：

1. 覆盖现有 Seed QA 尚未充分触及的论文 / 技术细节
2. 保持与现有 QA 一致的格式（问题 + 期望答案 + 验证页面）
3. 优先关注新 ingest 论文（Continual Distillation）和已有论文的深层技术细节
4. 增加量化对比类问题和实用边界类问题
5. 每道题必须可仅从 wiki 内容检索验证（不依赖外部 LLM 知识）

---

## Distillation（新增 4 题）

### N1: UKT-UKF trade-off — Continual Distillation 的核心矛盾

问题：Continual Distillation (CD) 范式中 UKT 和 UKF 分别指什么？为什么说 CD 的核心是平衡这二者？

期望答案：UKT（Unseen Knowledge Transfer）——外部数据（教师未知的数据）能让学生获取教师已知但学生未见领域的知识，这是传统蒸馏未开发的机制。UKF（Unseen Knowledge Forgetting）——顺序蒸馏中后续教师的学习会覆盖先前教师传递的未见领域知识，类似持续学习中的灾难性遗忘。核心矛盾：外部数据同时触发 UKT 和 UKF——同一个外部数据批次既能带来新领域知识（UKT）也加速旧领域知识遗忘（UKF），CD 需要找到最优平衡点。

验证页面：[Continual Distillation of Teachers from Different Domains](../../distillation/papers/continual-distillation-teachers-different-domains.md)

### N2: 方法理解 — SE2D 如何平衡 UKT 和 UKF

问题：CD 论文提出的 SE2D 方法如何同时提升 UKT 和降低 UKF？

期望答案：SE2D（Self-Ensembling with External Data Distillation）通过保留外部数据在学生模型上的 logits（self-ensembling logit preservation）来同时实现两个目标——保留的 logits 编码了先前教师的"响应模式"，在后续教师蒸馏中通过惩罚 logits 偏离来维持先前教师的知识（降低 UKF）；同时外部数据的 logits 天然携带了教师在该数据上的知识信号，logit preservation 使得这些信号在顺序蒸馏中持续可用（提升 UKT）。本质是"保留 logits = 保留（教师输入→输出）响应映射"。

验证页面：[Continual Distillation of Teachers from Different Domains](../../distillation/papers/continual-distillation-teachers-different-domains.md)

### N3: 量化对比 — COBRA 在低 IPC 下的公平性鲁棒性

问题：COBRA 在 IPC=1（每类仅 1 张合成图片）的极端压缩率下公平性表现如何？这说明什么？

期望答案：CIFAR10-S 上 COBRA 的 EOD 为 4.9（Vanilla 17.2），BFFHQ IPC=3 上 EOD 7.8（Vanilla 30.4）。说明在极端低数据压缩场景下，COBRA 的 barycenter alignment 对公平性的改善反而更为显著——因为样本越少，Vanilla 方法越容易被多数群体主导，barycenter 的"保护"效应越突出。

验证页面：[COBRA](../../distillation/papers/fair-dataset-distillation-cobra.md)

### N4: 跨域连接 — Continual Distillation 与数据集蒸馏的本质区别

问题：Continual Distillation (CD) 和 Dataset Distillation (DD) 都叫"蒸馏"，核心区别是什么？

期望答案：CD 是**模型级蒸馏**——从教师模型序列向学生模型迁移知识，目标是训练更好的学生模型，输出是模型权重。DD 是**数据级压缩**——将大规模数据集压缩为小型合成数据集，目标是替代原始训练集，输出是合成图片/数据。CD 的蒸馏对象是"教师模型的知识"（经过训练的模型参数蕴含的信息），DD 的蒸馏对象是"数据的知识"（训练集蕴含的统计信息）。两者在损失函数上也有本质不同：CD 使用 KL divergence 对齐教师/学生输出的 logits，DD 使用 gradient matching / distribution matching 对齐合成/真实数据产生的训练信号。

验证页面：[Continual Distillation of Different Domains](../../distillation/papers/continual-distillation-teachers-different-domains.md)、[Dataset Distillation](../../distillation/concepts/dataset-distillation.md)

---

## Federated Learning（新增 5 题）

### N5: 事实检索 — FedHD 的三个核心组件

问题：FedHD（ICML 2026）的联邦 WSI 蒸馏框架包含哪三个核心组件？

期望答案：(1) **Gaussian-Mixture Feature Alignment**——高斯混合建模捕捉 WSI 的多组分形态多样性，通过 GM 对齐实现特征级联邦蒸馏；(2) **One-to-One Distillation**——保留 WSI 诊断多样性所需的细粒度特征差异，避免聚合平滑导致的诊断信息丢失；(3) **Curriculum Federation**——先通过真实数据建立联合特征基线再逐步引入合成蒸馏数据，实现受控增量整合。

验证页面：[FedHD](../../federated-learning/papers/fedhd-federated-distillation-whole-slide-image.md)

### N6: 方法迁移 — FedKPer 的 selective alignment

问题：FedKPer 提出的 selective alignment with global model 如何改进 generalization-personalization trade-off？它引入的第三评估维度是什么？

期望答案：传统 FL 认为 generalization 和 personalization 是对立的（全局模型好则本地适配差，反之亦然）。FedKPer 证明通过选择性对齐——仅对齐损失中受益于全局信息的部分参数，保留对本地数据敏感的私有参数——可以在改进两者的同时保持 retention。它引入的第三评估维度是 **forgetting**——统计异质 FL 中遗忘是一个严重但被忽视的行为，不应只考虑泛化与个性化的 trade-off，还需要跟踪学生对学过的知识记住了多少。

验证页面：[FedKPer](../../federated-learning/papers/fedkper-generalization-personalization-medical-fl.md)、[FL Heterogeneity and Optimization](../../federated-learning/topics/fl-heterogeneity-and-optimization.md)

### N7: 量化对比 — FedACT 的 participation fairness 效果

问题：FedACT 引入 participation fairness 约束后，对模型准确率的量化影响是什么？这个结果说明了什么深层问题？

期望答案：FedACT 在 4×A4000 GPU 测试环境下实现 JCT 减少 8.3×，**准确率提升高达 44.5%**。这个提升幅度远超单纯"调度优化"的典型收益，说明 multi-job FL 中 fair scheduling 不只是公平问题——未被充分代表的设备贡献了更丰富多样的数据，通过提升它们的参与度实际上显著提高了模型质量。参与公平性不仅是伦理需求，也是提升模型性能的重要手段。

验证页面：[FedACT](../../federated-learning/papers/fedact-concurrent-federated-intelligence.md)

### N8: 机制理解 — FSCLB 的双 sketch 策略

问题：FSCLB 使用双重 sketch 策略从哪两个维度降低联邦 bandit 的计算和通信成本？quantization 的加性噪声如何处理？

期望答案：维度一：**特征 sketch**（count sketch 压缩高维上下文向量，降低客户端计算复杂度维度 ~d 的投影）；维度二：**梯度 sketch**（压缩服务器端梯度更新消息的维度，降低通信开销 ~O(d) → ~O(k log d) where k << d）。对于 count sketch 引入的 quantization 加性噪声，FSCLB 通过 SVD 间接行列式计算——在 sketched 空间中进行 SVD 分解，提取 top-k 奇异值和向量用于后续的悲观估计，该过程对 sketch 噪声具有天然鲁棒性。总体达到 90%+ 的计算和通信成本降低，同时 regret 匹配 optimal。

验证页面：[FSCLB](../../federated-learning/papers/federated-sketch-contextual-linear-bandits-fsclb.md)

### N9: 跨论文比较 — FedHarmony consensus correlation 与 COBRA barycenter alignment 的哲学共性

问题：FedHarmony 的 consensus correlation 和 COBRA 的 barycenter alignment 在"聚合"策略上的哲学共性是什么？实现手段有何不同？

期望答案：共性：两者都拒绝简单的"群体比例加权"——FedHarmony 拒绝按数据量加权客户端模型更新（认为数据规模不代表标签相关性质量），COBRA 拒绝按群体比例加权蒸馏目标（认为多数群体主导会导致少数群体被偏离）。不同点：(1) 场景不同——FedHarmony 在 FL 客户端模型聚合层，COBRA 在集中式蒸馏目标层；(2) 替代方案不同——FedHarmony 用 cross-client 共识标签相关性作为教师信号纠正局部偏差，COBRA 用 uniform-weight barycenter（子群体均匀平均）替代比例加权 target。共同哲学是：**群体规模不应决定聚合影响力，共识/平衡比规模更重要**。

验证页面：[FedHarmony](../../federated-learning/papers/fedharmony-heterogeneous-label-correlations-federated-multi-label.md)、[COBRA](../../distillation/papers/fair-dataset-distillation-cobra.md)、[FL Heterogeneity and Optimization](../../federated-learning/topics/fl-heterogeneity-and-optimization.md)

---

## Cross-Domain（新增 3 题）

### N10: 跨域连接 — "受控增量整合"哲学在三个域中如何体现？

问题：当前 wiki 中"受控增量整合"（先建立稳定基线再逐步引入异构信号）在至少三个域中分别以什么形式出现？

期望答案：(1) **FedHD (Federated Learning)**——Curriculum Federation：先用真实 WSI 数据建立联合特征基线，再逐步引入合成蒸馏数据；(2) **CoRD (LLM Reasoning)**——Step-wise Collaborative Decoding：先用学生模型当前状态评估候选步骤，再逐步整合多 teacher 信号（而非一次性融合全部 teacher 输出）；(3) **CD (Distillation)**——SE2D 的 self-ensembling：先保留前序教师的 logits 作为稳定基线，再逐步吸收新教师的知识。共性哲学：不信任一次性均匀混合，坚持"先建立基线，再可控地整合新信号"。

验证页面：[FedHD](../../federated-learning/papers/fedhd-federated-distillation-whole-slide-image.md)、[CoRD](../../llm-reasoning/papers/distilling-long-cot-reasoning-cord.md)、[Continual Distillation of Teachers from Different Domains](../../distillation/papers/continual-distillation-teachers-different-domains.md)

### N11: 三域交叉 — UKF 与 FL 中 forgetting 的统一理解

问题：CD 的 UKF（Unseen Knowledge Forgetting）与 FedKPer 关注的 FL forgetting 是同一个问题吗？它们的异同是什么？

期望答案：共享"顺序学习导致先前知识遗忘"的核心机制，但场景和应对策略不同。CD 的 UKF 发生在**单机顺序蒸馏**中——学生模型从不同领域的教师序列中学习，遗忘的是先前教师传递的未见领域知识，应对策略是 SE2D 的 logit preservation；FedKPer 关注的 forgetting 发生在**分布式联邦学习**中——客户端在本地更新时遗忘全局信息，应对策略是 selective alignment（仅对齐受益于全局信息的部分参数）。相同本质 = "新知识覆盖旧知识"；不同场景 = 蒸馏管道中的教师切换 vs. 联邦训练中的本地-全局交替。

验证页面：[Continual Distillation of Teachers from Different Domains](../../distillation/papers/continual-distillation-teachers-different-domains.md)、[FedKPer](../../federated-learning/papers/fedkper-generalization-personalization-medical-fl.md)、[FL Heterogeneity and Optimization](../../federated-learning/topics/fl-heterogeneity-and-optimization.md)

### N12: 跨域识别 — 当前 wiki 中基于 matching 的方法家族图谱

问题：当前 wiki 中存在哪些不同的 "matching" 范式？分别属于哪些论文和域？

期望答案：(1) **Trajectory Matching**——TAFAP（diffusion data protection，distillation 域）用 full training trajectory alignment 实现持久防御；MTT（COBRA 兼容的 trajectory matching，distillation 域）在 trajectory 层面做蒸馏；(2) **Gradient Matching**——DC（dataset distillation，distillation 域）对齐合成图片和真实图片产生的梯度；(3) **Distribution Matching**——DM（dataset distillation，distillation 域）对齐合成和真实数据的分布统计量；(4) **Feature Alignment / Distribution Matching**——FedHD（federated learning 域）用 GM alignment 对齐联邦客户端特征分布；(5) **Device-Job Resource Matching**——FedACT（federated learning 域）用 alignment scoring 匹配设备算力与作业需求。这些 matching 范式散布在蒸馏和 FL 两个域，尚无统一的 comparison 页进行系统梳理。

验证页面：[TAFAP](../../distillation/papers/targeted-data-protection-diffusion-model-training-trajectory.md)、[COBRA](../../distillation/papers/fair-dataset-distillation-cobra.md)、[FedHD](../../federated-learning/papers/fedhd-federated-distillation-whole-slide-image.md)、[FedACT](../../federated-learning/papers/fedact-concurrent-federated-intelligence.md)

---

## Meta & Practical（新增 3 题）

### N13: 证据等级 — Continual Distillation 的证据等级及其影响

问题：CD（Continual Distillation）论文当前的 evidence_level 是什么？这一等级意味着对其实验结论的信任度应该如何把握？

期望答案：CD 当前 evidence_level 为 **skimmed**——仅阅读了题目、摘要、方法标题和关键结论，未深入验证实验设置和量化结果。这意味着：(1) CD 的核心概念（UKT/UKF/SE2D logit preservation）可信，但定量结果（特定数据集上的准确率数值、与其他方法的对比）可能需要验证；(2) SE2D 方法的实现细节和消融实验尚未确认；(3) CD 的贡献定性描述可靠，但与 SOTA 的定量比较需要在 full-paper 阅读后核实。建议在引用 CD 的实验数据时标注"skimmed"级别。

验证页面：[Continual Distillation of Teachers from Different Domains](../../distillation/papers/continual-distillation-teachers-different-domains.md)

### N14: 反模式 — 当前 wiki 的方法独立化进度

问题：根据 AGENTS.md 的 schema，当前 wiki 中 Method、Dataset、Metric 独立页的创建情况如何？这造成了什么问题？

期望答案：Method、Dataset、Metric 页模板完备但 **0 个已创建**——所有方法和数据集信息内嵌在 paper 页中，无法被多篇论文共享引用。造成的问题包括：(1) 跨论文比较需要逐篇查阅 paper 页，无法从统一的方法入口检索；(2) 方法变体（如不同的 trajectory matching 实现——TAFAP vs. MTT）没有独立的方法页来追踪演化；(3) 新增 paper 时，如果其使用了已有方法，需要在多个 paper 页间手动维护一致性，违反了 DRY（Don't Repeat Yourself）原则。这是当前 wiki 最突出的反模式之一。

验证页面：[AGENTS.md](../../../AGENTS.md)、[Needle Tests Q35](needle-tests-2026-05-05.md)

### N15: 维护建议 — 基于当前测试结果的 wiki 改进优先级

问题：结合当前 35 题捞针测试的执行结果（32/35 完全通过，3 题部分通过），wiki 内容改进的优先级应该如何排序？

期望答案：P0（立即修复）：(1) LSN 论文页补充 Table 5 的定量细节（prompt 数 8 vs 2，训练 epoch 25 vs 5）；(2) PALCAS 论文页补充绝对碰撞率 2.45%（@60% CAV）；(3) 更新 Q14 的期望答案以匹配当前 14 篇 full-paper 状态。P1（短期改进）：基于 Q35 的反模式清单，创建首批比较页（LSN vs. NegPrompt 优先）和首批方法页（Trajectory Matching 优先）。P2（长期工程）：消除 6 篇孤儿论文（见 Q33），补齐 method/dataset/metric 独立页体系。优先级原则：测试题本身指示了知识密度最大的缺口——如果一个 QA 的期望答案无法直接从 wiki 检索得到，对应的 wiki 页面就需要补充。

验证页面：[Needle Tests Execution Report](needle-tests-2026-05-05.md)
