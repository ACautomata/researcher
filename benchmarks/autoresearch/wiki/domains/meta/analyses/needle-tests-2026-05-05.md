---
title: Wiki Needle Tests
type: analysis
domain: meta
status: active
created: 2026-05-05
updated: 2026-05-20
tags:
  - qa
  - needle-test
  - wiki-health
source_pages:
  - wiki/index.md
---

# Wiki Needle Tests

自动捞针测试集——按领域分组的核心知识检索问题。每次 lint 或 major ingest 后可重跑。当前共 35 题，覆盖 7 领域 × 4 题型。

使用方式：对每个问题，从 wiki 中检索答案，与期望答案对比。正确率低于阈值时标记对应页面需修正。

---

## Distillation

### Q1: 事实检索 — ProCo 的核心指标

问题：ProCo 用什么 metric 衡量跨模态 correspondence？

期望答案：Retrieval-based correspondence consistency metric——通过 cross-modal retrieval distributions 量化并聚类 correspondence patterns。

验证页面：[Correspondence Coverage Matters for Multi-Modal Dataset Distillation](../../distillation/papers/correspondence-coverage-matters-multimodal-dataset-distillation.md)

### Q2: 跨论文比较 — 长尾蒸馏 vs. ProCo 的方法差异

问题：长尾数据集蒸馏（AAAI 2026）和多模态蒸馏 ProCo（AAAI 2026）的核心方法差异是什么？

期望答案：长尾蒸馏用 statistical alignment（expert debiasing + dynamic momentum BN recalibration + confidence-guided multi-round initialization）解决 class imbalance；ProCo 用 correspondence coverage（retrieval-based consistency metric + conditional neural fields）解决多模态 paired semantics 的覆盖度和多样性。两者目标不同（tail-class recovery vs. cross-modal coverage），技术路线正交。

验证页面：[Rethinking Long-tailed Dataset Distillation](../../distillation/papers/rethinking-long-tailed-dataset-distillation.md)、[ProCo](../../distillation/papers/correspondence-coverage-matters-multimodal-dataset-distillation.md)

### Q3: 机制理解 — TAFAP 的 trajectory matching 为何优于 snapshot

问题：TAFAP 声称 trajectory-level defense 比 snapshot-level defense 更持久，原因是什么？

期望答案：Snapshot-based 保护随 fine-tuning 进行而衰减（被后续训练步稀释）。Full training trajectory alignment 控制完整的优化动态，保护效果不会随训练继续而消失。这与 dataset distillation 中 trajectory matching > single-step matching 的原理一致。

验证页面：[Targeted Data Protection for Diffusion Model](../../distillation/papers/targeted-data-protection-diffusion-model-training-trajectory.md)、[Diffusion Model Data Protection](../../distillation/topics/diffusion-model-data-protection.md)

---

## Out-of-Distribution Detection

### Q4: 方法区分 — LSN vs. NegPrompt 的核心差异

问题：LSN (ICLR 2024) 和 NegPrompt (CVPR 2024) 在 negative prompt 设计上的根本差异是什么？

期望答案：LSN 学习 **class-specific** negative prompts（每个类独立的 complementary negative prompt）+ semantic orthogonality loss，只用 ID 数据，不可迁移到未见类。NegPrompt 学习 **transferable** negative prompts——只用 ID 数据但能在未见 OOD 分布上泛化，通过 NIS + NPD + NND 三个损失实现跨 OOD 分布的稳定 patterns。核心 trade-off：class-specific 精度 (LSN: AUROC 95.12%) vs. 跨分布可迁移性 (NegPrompt: 在 NINCO/SSB-hard/iNaturalist/Texture 上超越 MCM 和 CoOp)。

验证页面：[LSN](../../outofdistributiondetection/papers/out-of-distribution-detection-with-negative-prompts.md)、[NegPrompt](../../outofdistributiondetection/papers/learning-transferable-negative-prompts-ood-detection.md)、[Negative Prompt OOD Detection](../../outofdistributiondetection/topics/negative-prompt-ood-detection.md)

### Q5: 核心发现 — positive vs. negative prompt learning 的根本差异

问题：LSN 论文 Table 5 揭示了 positive 和 negative prompt learning 之间存在哪些根本差异？

期望答案：(1) Positive 需要更多 prompt (8 vs 2)，negative 只需少量；(2) Positive 需要更长训练 (25 epochs vs 5)；(3) Positive 受益于多样性正则化，negative 更需要单独学习和语义正交性约束。差异根源：negative evidence 比 positive 更多样，单一否定无法覆盖所有"不是某类"的方式。

验证页面：[LSN](../../outofdistributiondetection/papers/out-of-distribution-detection-with-negative-prompts.md)

---

## Spectrum

### Q6: 方法链 — 拓扑流形学习在光谱分析中的完整 pipeline

问题：JACS 2025 拓扑机器学习论文中，从原始 UV-vis 光谱到反应路径推断的完整 pipeline 包含哪些步骤？

期望答案：(1) Transformer-augmented data augmentation（physics-informed t=0 边界条件约束，生成 204 个增强样本，多个独立训练的 transformer 生成拓扑等价流形）；(2) UMAP 降维（n_neighbors > 1% 数据量，min_dist 0.1-0.3）；(3) 拓扑流形分析——UMAP 嵌入中的分支点对应路径分叉，聚类对应反应阶段，过渡区域对应中间体形成；(4) Beer-Lambert 定律量化纳米晶浓度变化；(5) 识别出此前未报道的亚稳态中间体（P-550 和 P-610）。

验证页面：[Topological Machine Learning Nanocrystal Synthesis](../../spectrum/papers/topological-machine-learning-nanocrystal-synthesis.md)、[Spectroscopic Manifold Learning](../../spectrum/concepts/spectroscopic-manifold-learning.md)

### Q7: 边界判断 — 该方法的局限性

问题：拓扑流形学习从光谱推断反应路径的方法有哪些已知局限？

期望答案：(1) 新识别的中间体（P-550、P-610）需要独立实验验证（TEM/XRD/mass spec）；(2) 跨材料系统（InP/CdSe/PbS）和跨光谱模态（IR/Raman/XRD）的泛化性未测试；(3) 拓扑流形分析本质是探索性/可视化工具，拓扑特征与化学机制的因果对应尚未严格证明；(4) 目前只能提取定性路径描述，无法提取定量动力学参数（速率常数、活化能）。

验证页面：[Spectrum-Based Reaction Pathway Discovery](../../spectrum/topics/spectrum-based-reaction-pathway-discovery.md)

---

## Autonomous Driving

### Q8: 方法创新 — PALCAS 的混合动作空间

问题：PALCAS 为什么使用 PDQN 的混合动作空间，它同时处理哪两类控制？

期望答案：PDQN 的 parameterized action space 同时处理离散变道决策（左变道/保持/右变道）和连续纵向控制（加速度），统一了强制性和自主性变道行为。传统 DQN 只能处理离散动作，DDPG 只能处理连续动作——PDQN 是处理混合动作空间的自然选择。

验证页面：[PALCAS](../../autonomous-driving/papers/palcas-priority-aware-lane-change-federated-rl.md)

### Q9: 场景约束 — PALCAS 的安全模型

问题：PALCAS 使用什么安全模型约束变道行为？

期望答案：RSS (Responsibility-Sensitive Safety) 模型——定义安全纵向和横向距离阈值，确保变道决策即使在最坏情况下也不会导致碰撞。60% CAV 渗透率下碰撞率仅 2.45%，MSR（合并成功率）93.33%。

验证页面：[PALCAS](../../autonomous-driving/papers/palcas-priority-aware-lane-change-federated-rl.md)

---

## Federated Learning

### Q10: 架构理解 — EASE 的 Anchor Principle

问题：EASE 提出的三个残差锚分别是什么？各自用什么机制闭合？

期望答案：(1) **Modality Anchor**——通过 Bilateral Knowledge Excision (BKE) 闭合：同时位移图像+文本分支，使 bilinear similarity 无法通过未触及模态重建遗忘配对；(2) **Unique-Subspace Anchor**——通过 Gradient Subspace Decomposition (GSD) 闭合：SVD + principal angles 分解客户端梯度子空间，区分 forget-exclusive 与 retain-shared 方向；(3) **Temporal Re-anchoring**——通过 Projection with Forget Lock (PFL) 闭合：服务器端投影到 unique subspace 补空间 + 客户端端 Forget Lock 惩罚漂移。

验证页面：[EASE](../federated-learning/papers/ease-federated-multimodal-unlearning.md)、[Federated Distillation and Unlearning](../federated-learning/topics/federated-distillation-and-unlearning.md)

### Q11: 跨域连接 — FedHD 与 distillation 域的关系

问题：FedHD (ICML 2026) 与数据蒸馏域（`distillation`）的哪些页面形成直接技术连接？

期望答案：(1) [Dataset Distillation](../../distillation/concepts/dataset-distillation.md)——FedHD 将 DD 的核心思想（合成数据替代原始数据）迁移到联邦场景；(2) [Multi-Modal Dataset Distillation](../../distillation/topics/multimodal-dataset-distillation.md)——GM alignment 的"多组分语义保留"问题与 ProCo 的 correspondence coverage 是同一核心的不同表述；(3) 长尾 DD 的 statistical alignment 与 FedHD 的 GM alignment 共享"分布匹配优于点匹配"的哲学。

验证页面：[FedHD](../federated-learning/papers/fedhd-federated-distillation-whole-slide-image.md)

### Q12: 分类判断 — AgentReputation 的归属

问题：AgentReputation 是否属于联邦学习论文？为什么放在 federated-learning 域？

期望答案：不是联邦学习论文——它是去中心化 AI agent 声誉框架。放在 federated-learning 域是因为当前 wiki 无独立的 decentralized-systems 域，且其三层去中心化架构与 FL 的设计空间有交集。Frontmatter `label` 已标记为 `decentralized-ai` 并添加了分类说明。

验证页面：[AgentReputation](../federated-learning/papers/agentreputation-decentralized-agentic-ai-reputation.md)

---

## LLM Reasoning

### Q16: 事实检索 — CoRD 的步骤选择准则

问题：CoRD 用什么准则在每一步选择最优推理步骤？为什么该准则优于其他候选方案？

期望答案：使用 **predictive perplexity**（预测困惑度）作为步骤级选择准则——对每个 teacher 提出的候选推理步骤，用学生模型的预测困惑度评估其与已生成上下文的连贯性和信息增益。predictive perplexity 在步骤粒度上显著优于 PRM (Process Reward Model) 和 Binary Judgment（二元判断）——PRM 需要额外训练且依赖最终答案正确性，二元判断过于粗糙无法区分细粒度的推理质量差异。

验证页面：[CoRD](../../llm-reasoning/papers/distilling-long-cot-reasoning-cord.md)、[Long-CoT 推理蒸馏](../../llm-reasoning/concepts/long-cot-reasoning-distillation.md)

### Q17: 机制理解 — 逐步协同解码为何优于策展式蒸馏

问题：CoRD 的逐步协同解码（step-wise collaborative decoding）相比 S1/LIMO 的策展式（curation-based）推理蒸馏，在机制层面解决了哪两个根本局限？

期望答案：(1) **Teacher 间信号无交互**：策展式中各 teacher 独立生成完整推理轨迹，无法在推理过程中利用其他 teacher 的强项——CoRD 在每一步让所有 teacher 提出候选步骤，实现 teacher 互补信号的实时融合；(2) **缺乏动态探索**：策展式 post-hoc 选择只能基于最终结果，无法在推理中途调整方向——CoRD 通过 beam search 在每步探索多条路径，可以在推理过程中适时切换策略。本质差异：策展式是"独立生成→事后选择"，CoRD 是"协同生成→逐步构建"。

验证页面：[CoRD](../../llm-reasoning/papers/distilling-long-cot-reasoning-cord.md)、[Long-CoT 推理蒸馏](../../llm-reasoning/concepts/long-cot-reasoning-distillation.md)

### Q18: 跨域区分 — Long-CoT 推理蒸馏 vs. 数据集蒸馏

问题：Long-CoT 推理蒸馏（llm-reasoning 域）和数据集蒸馏（distillation 域）都叫"蒸馏"，它们的根本区别是什么？

期望答案：Long-CoT 蒸馏是**模型级知识蒸馏**（训练更好的学生模型）——目标是让学生模型在推理能力上接近 teacher LRM，输出是更好的模型权重。数据集蒸馏是**数据级压缩**（合成更小的训练集）——目标是将大规模数据集压缩为小型合成数据集，输出是更小的合成数据集。两者共享"知识迁移"的思想但层次不同：一个迁移模型能力，一个压缩数据信息。

验证页面：[Long-CoT 推理蒸馏](../../llm-reasoning/concepts/long-cot-reasoning-distillation.md)、[Dataset Distillation](../../distillation/concepts/dataset-distillation.md)

### Q19: 跨域连接 — CoRD 的多 teacher 协同与 FedHD 的 curriculum federation

问题：CoRD 的多 teacher 协同解码和 FedHD 的 curriculum federation 都涉及"多个知识源的整合"，它们的共性哲学是什么？区别在哪里？

期望答案：共性：两者都拒绝简单的"均匀融合"——CoRD 用 predictive perplexity 动态选择最优 teacher 步骤（而非平均所有 teacher 输出），FedHD 先用真实数据训练再逐步引入合成数据（而非直接混合）。区别：CoRD 在**推理时**（inference time）整合多 teacher 能力，FedHD 在**训练时**（training time）整合多数据源。共同哲学是"受控的增量整合"——先建立稳定基线，再逐步引入异构信号。

验证页面：[CoRD](../../llm-reasoning/papers/distilling-long-cot-reasoning-cord.md)、[FedHD](../../federated-learning/papers/fedhd-federated-distillation-whole-slide-image.md)

---

## Federated Learning 深度

### Q20: 机制理解 — FedSD2C 的双层信息损失

问题：FedSD2C 论文指出基于 DFKD 的一次性联邦学习存在"双层信息损失"，具体指哪两层？FedSD2C 如何消除这两层损失？

期望答案：第一层**训练损失（数据→模型）**：受模型容量限制，客户端模型无法完全捕获本地数据的所有信息；第二层**生成损失（模型→逆向数据）**：从随机噪声通过 GAN 生成的数据无法充分表示模型中的信息。FedSD2C 的解决方案：用 V-information Core-Set 选择 + Fourier 变换扰动 + 预训练 Autoencoder 蒸馏，将本地数据**端到端**压缩为 distillate——跳过中间的模型训练步骤，直接在数据层面进行信息压缩和通信，从根本上消除两层信息损失。

验证页面：[FedSD2C](../../federated-learning/papers/fedsd2c-one-shot-fl-distiller-distillate.md)

### Q21: 方法迁移 — FedHAW 的 hypergradient 核心洞察

问题：FedHAW 将 hypergradient descent 从学习率优化迁移到 FL 聚合权重更新，其核心洞察是什么？相比 FedLAW 有什么优势？

期望答案：核心洞察：hypergradient（梯度关于聚合权重的梯度）可以**在线**提取聚合的优化信号——无需预先准备的 proxy 数据。优势：FedLAW 需要额外训练数据预学习聚合权重（这些数据可能无法反映真实分布），而 FedHAW 的在线更新机制：(1) 不需要额外数据；(2) 对通信环境变化有实时追踪能力；(3) 在通信错误场景下保持鲁棒性。

验证页面：[FedHAW](../../federated-learning/papers/fedhaw-hypergradient-aggregation-weights.md)、[FL Heterogeneity and Optimization](../../federated-learning/topics/fl-heterogeneity-and-optimization.md)

### Q22: 跨论文比较 — FedHarmony vs. FedAvg 在标签相关性上的差异

问题：FedHarmony 认为 FedAvg 的 data-size-weighted aggregation 在多标签学习中存在什么根本问题？FedHarmony 用什么机制替代？

期望答案：根本问题：FedAvg 按数据量加权聚合客户端模型更新，但在多标签学习中，不同客户端可能拥有截然不同的标签相关性结构（label correlation drift）——数据量大的客户端如果标签相关性偏差大，会污染全局模型。FedHarmony 用 **consensus correlation** 机制替代：从跨客户端标签共现模式中提取共识标签相关性作为教师信号，用于纠正各客户端的局部标签相关性偏差，而非简单按数据量加权。

验证页面：[FedHarmony](../../federated-learning/papers/fedharmony-heterogeneous-label-correlations-federated-multi-label.md)、[FL Heterogeneity and Optimization](../../federated-learning/topics/fl-heterogeneity-and-optimization.md)

### Q23: 系统设计 — FedACT 的 alignment scoring

问题：FedACT 的 alignment scoring 为什么超越了简单的硬件排名？它额外考虑了哪些因素？

期望答案：alignment scoring 不仅考虑设备硬件能力（算力/内存/带宽），还量化**设备-作业对的兼容性**——大语言模型训练需要高算力设备，小图像分类器可在低配置设备运行。此外还引入 **participation fairness** 约束：被频繁选中的设备降低 score 以防止过度代表和数据偏置，未充分代表的设备提升 score 以增加数据多样性。这两个因素使 alignment scoring 超越了静态硬件排名，实现动态的设备-作业最优匹配。

验证页面：[FedACT](../../federated-learning/papers/fedact-concurrent-federated-intelligence.md)、[FL Heterogeneity and Optimization](../../federated-learning/topics/fl-heterogeneity-and-optimization.md)

### Q24: 量化对比 — FedACT 的关键数字

问题：FedACT 在什么硬件配置下测试？相比 baselines 实现了多少 JCT 减少和准确率提升？

期望答案：4 张 NVIDIA RTX A4000 GPU + Intel i9-10900X CPU + 64GB RAM，100 个设备。平均作业完成时间（JCT）减少 8.3×，准确率提升高达 44.5%。Baselines 包括 Random、Greedy、Genetic、MJ-FL。

验证页面：[FedACT](../../federated-learning/papers/fedact-concurrent-federated-intelligence.md)

---

## Distillation 深度

### Q25: 事实检索 — COBRA 的跨群体重心计算

问题：COBRA 如何计算跨群体重心（barycenter）？为什么用 uniform-weight 而非群体比例加权？

期望答案：对每个类别 y，计算 uniform-weight barycenter m* = argmin_m (1/|A|) Σ d(Φ_{a|y}, m)，默认使用 squared Mahalanobis distance（闭式解为各子群体统计量的均匀均值）。使用 uniform-weight 而非群体比例加权的原因：群体比例加权的重心（vanilla target m_y^{van} = Σ π_{a|y} Φ_{a|y}）被多数群体主导，导致少数群体表示被系统性偏离——偏差放大的理论上界由群体不平衡与表示分离的交互项控制，uniform-weight 重心通过缩小最差情况子群体残差来收紧该上界。

验证页面：[COBRA](../../distillation/papers/fair-dataset-distillation-cobra.md)、[Fair Dataset Distillation](../../distillation/topics/fair-dataset-distillation.md)

### Q26: 跨论文比较 — COBRA vs. RLDD 的公平性维度

问题：COBRA (ICML 2026) 和 RLDD (AAAI 2026) 都关注数据集蒸馏中的公平性，它们解决的公平性维度有何不同？技术上如何互补？

期望答案：RLDD 解决 **class imbalance**（长尾分布）——少数类样本不足，用 statistical alignment + dynamic momentum BN 恢复尾类信息。COBRA 解决 **subgroup bias**（子群体偏差）——在类别内部，敏感属性（如颜色、性别、种族）定义的子群体被系统性忽视，用 barycenter alignment 消除群体不平衡×表示分离的交互偏差。两者正交互补：RLDD 处理"类间"不公平（某些类样本少），COBRA 处理"类内"不公平（某些子群体被忽视）。完整的公平蒸馏需要同时处理两个维度。

验证页面：[RLDD](../../distillation/papers/rethinking-long-tailed-dataset-distillation.md)、[COBRA](../../distillation/papers/fair-dataset-distillation-cobra.md)、[Long-Tailed Dataset Distillation](../../distillation/topics/long-tailed-dataset-distillation.md)、[Fair Dataset Distillation](../../distillation/topics/fair-dataset-distillation.md)

### Q27: 机制理解 — COBRA 为何能与所有主流蒸馏方法兼容

问题：COBRA 声称兼容 DC/DM/CAFE/IDC/MTT 所有主流蒸馏方法，其兼容性的机制基础是什么？

期望答案：COBRA 不改变各蒸馏方法的核心优化目标（gradient matching / distribution matching / feature alignment / trajectory matching），只修改这些目标中使用的**聚合表示目标（target）**——从群体比例加权的 vanilla target 替换为 group-balanced barycentric target。例如在 MTT 中，COBRA 修改 trajectory target 为 barycentric trajectory target（各子群体 trajectory 的均匀平均），其余优化流程完全不变。这种"只改 target、不改 loss"的设计使其成为蒸馏方法的通用公平性插件。

验证页面：[COBRA](../../distillation/papers/fair-dataset-distillation-cobra.md)

### Q28: 消融分析 — RLDD 的三组件各自贡献

问题：RLDD（长尾数据集蒸馏）包含三个核心组件，各自的性能贡献（从消融实验）分别是多少？

期望答案：(1) Statistical Alignment（统计对齐）贡献最大——移除后 CIFAR-100-LT 上约 -10%；(2) Dynamic Momentum BN Recalibration（动态动量 BN 重校准）——移除后约 -2%；(3) Confidence-Guided Multi-Round Initialization（置信度引导多轮初始化）——移除后约 -1%。三个组件协同工作时效果最优，说明长尾蒸馏需要从表示对齐、统计重校准和初始化策略三个层面同时处理。

验证页面：[RLDD](../../distillation/papers/rethinking-long-tailed-dataset-distillation.md)

---

## 跨域综合（续）

### Q29: 跨域连接 — FedSD2C 与 ProCo 在压缩哲学上的异同

问题：FedSD2C 的 distillate 合成和 ProCo 的多模态蒸馏都涉及"压缩"，它们的压缩目标和手段有何异同？

期望答案：相同点：两者都追求在压缩过程中保留最大信息量——FedSD2C 用 V-information 最大化 Core-Set 的信息量，ProCo 用 correspondence coverage 最大化跨模态配对覆盖度。不同点：(1) 目标不同——FedSD2C 压缩为**隐私增强的通信数据包**（distillate），ProCo 压缩为**高质量合成训练集**（distilled dataset）；(2) 手段不同——FedSD2C 用 Fourier 扰动 + Autoencoder 蒸馏实现端到端压缩，ProCo 用 conditional neural fields 参数化 + retrieval-based consistency 聚类实现语义保留压缩；(3) 场景不同——联邦通信 vs. 集中式训练数据压缩。

验证页面：[FedSD2C](../../federated-learning/papers/fedsd2c-one-shot-fl-distiller-distillate.md)、[ProCo](../../distillation/papers/correspondence-coverage-matters-multimodal-dataset-distillation.md)

### Q30: 跨域连接 — TAFAP 的 trajectory alignment 与 CoRD 的 step-wise decoding

问题：TAFAP 的 trajectory alignment 和 CoRD 的 step-wise collaborative decoding 都强调"轨迹优于快照"，这一哲学在两个完全不同的领域如何体现？

期望答案：TAFAP（diffusion data protection）：snapshot-based 保护随 fine-tuning 进行而衰减——后续训练步会稀释单步保护信号。Full training trajectory alignment 控制完整的优化动态，保护效果持久。CoRD（reasoning distillation）：post-hoc curation 只看最终推理结果选择最佳轨迹——丢失了推理过程的中间探索和策略切换。Step-wise decoding 在每一步评估和选择，保留了完整的推理动态。共同哲学：**过程包含快照丢失的信息**——无论是优化轨迹中的渐进变化还是推理链中的中间决策，完整过程比单点快照更丰富和鲁棒。

验证页面：[TAFAP](../../distillation/papers/targeted-data-protection-diffusion-model-training-trajectory.md)、[CoRD](../../llm-reasoning/papers/distilling-long-cot-reasoning-cord.md)

### Q31: 三域交叉 — cross-modal coupling 的三重角色

问题：当前 wiki 中 cross-modal coupling 在蒸馏、遗忘、OOD 检测三个域中分别充当什么角色？请各自举例论文。

期望答案：(1) **蒸馏域（效率来源）**：ProCo 的 correspondence coverage——保留跨模态配对语义的覆盖度和多样性是关键压缩目标；(2) **遗忘域（主要障碍）**：EASE 的 modality anchor——图像+文本分支的 bilinear coupling 使单边切除失败，被未修改分支拉回，是遗忘的核心障碍；(3) **OOD 检测域（控制手段）**：LSN 和 NegPrompt 的 positive/negative prompt coupling——通过控制正向和负向文本提示与视觉特征的语义耦合来实现 class-specific 或 transferable 的分布外检测。同一个"跨模态耦合"概念，在三个域中分别是被追求的目标、被克服的障碍、被利用的工具。

验证页面：[ProCo](../../distillation/papers/correspondence-coverage-matters-multimodal-dataset-distillation.md)、[EASE](../../federated-learning/papers/ease-federated-multimodal-unlearning.md)、[LSN](../../outofdistributiondetection/papers/out-of-distribution-detection-with-negative-prompts.md)、[Federated Distillation and Unlearning](../../federated-learning/topics/federated-distillation-and-unlearning.md)

---

## Meta — Wiki 结构与质量

### Q32: 结构完整性 — 当前 wiki 的 comparison 页缺口

问题：当前 wiki 中存在哪些已充分记录但尚未创建正式 comparison 页的论文对？至少列出 3 对。

期望答案：(1) LSN vs. NegPrompt——class-specific vs. transferable negative prompt 设计空间，在 Negative Prompt OOD Detection topic 页和两篇论文页中已有详细对比，但无独立 comparison 页；(2) COBRA vs. RLDD——两个公平性维度（subgroup bias vs. class imbalance）的正交互补关系，在 Long-Tailed DD topic 页和 Fair DD topic 页中已有交叉引用；(3) FedHD vs. FedSD2C——联邦蒸馏的两种范式（特征级 vs. 数据级），在 Federated Distillation and Unlearning topic 页中已有统一分析。此外 TAFAP vs. MTT 的 trajectory matching 对比、ProCo vs. RLDD 的跨模态 vs. 长尾蒸馏对比也缺少独立 comparison 页。

验证页面：[index.md](../../index.md)、各 topic 页

### Q33: 孤儿检测 — 未被 topic 页覆盖的论文（更新版）

问题：截至 2026-05-20，federated-learning 域中哪些论文未被任何 topic 页索引？它们可以被如何重新组织？

期望答案：6 篇孤儿论文：privacy-preserving-fl-dp-he（心血管疾病风险建模）、agentreputation（去中心化 AI agent 声誉）、intrusion-detection-its（ITS 入侵检测）、federated-weather-modeling（天气建模）、fsclb（联邦 bandits）、meritocratic-fairness（公平 bandits）。可能的组织方案：(1) privacy-preserving-fl-dp-he 和 intrusion-detection-its 可归入新 topic "FL Privacy and Security"；(2) fsclb 和 meritocratic-fairness 可归入新 topic "Federated Bandits and Decision Making"；(3) agentreputation 当前标记为 decentralized-ai，建议长期迁移到独立的 decentralized-ai 域。

验证页面：[index.md](../../index.md)

### Q34: 证据等级升级优先级

问题：当前 8 篇 skimmed 论文中，哪些应优先升级到 full-paper？判断依据是什么？

期望答案：(1) **EASE**（最高优先）——Anchor Principle 是跨域核心概念（连接蒸馏、遗忘、多模态耦合），已在 Federated Distillation and Unlearning topic 页中有大量实质性引用，缺少定量实验数据影响跨域分析的精度；(2) **ProCo**（高优先）——correspondence coverage 概念与 FedHD 的 GM alignment、COBRA 的 barycenter alignment 形成"分布对齐方法族"的完整谱系，升级后可深化跨域连接；(3) **TAFAP**（中优先）——trajectory matching 哲学与 CoRD 的 step-wise decoding 形成跨域共鸣。其余 skimmed 论文（agentreputation、intrusion-detection-its、federated-weather-modeling、fsclb、meritocratic-fairness）为领域边界论文，升级优先级较低。

验证页面：[index.md](../../index.md)、各 paper 页的 evidence_level frontmatter

### Q35: 反模式检测 — 当前 wiki 中存在的已知结构问题

问题：根据 AGENTS.md 中定义的反模式清单，当前 wiki 中存在哪些已知的结构问题？

期望答案：(1) **0 个正式 comparison 页**——多对论文（LSN/NegPrompt、COBRA/RLDD、FedHD/FedSD2C）的跨论文比较仅存在于 topic 页中，未实例化 comparison 模板；(2) **0 个 method/dataset/metric 独立页**——Method、Dataset、Metric 页模板完备但 0 创建，所有方法和数据集信息内嵌在 paper 页中，无法被多篇论文共享引用；(3) **6 篇孤儿论文**（见 Q33）——有 paper 页但无 topic 页归属；(4) **捞针测试未全量执行**——15 题仅执行 6 题（5 题完全通过，1 题部分通过），剩余 9 题未跑。

验证页面：[AGENTS.md](../../../AGENTS.md)（workspace-autoresearch）、[index.md](../../index.md)

---

## 跨域综合

问题：当前 wiki 中，联邦蒸馏相关研究跨越了哪几个域？分别通过哪些论文连接？

期望答案：跨越 3 个域：
- `federated-learning`：FedHD（联邦 WSI 蒸馏）、EASE（联邦多模态遗忘，与蒸馏共享 cross-modal 技术栈）
- `distillation`：Dataset Distillation 概念页、Multi-Modal Dataset Distillation（ProCo 的 correspondence coverage）、Long-Tailed Dataset Distillation（统计对齐范式）、Diffusion Model Data Protection（TAFAP 的 trajectory matching）
- `autonomous-driving`：PALCAS（FedRL，联邦学习在自动驾驶中的应用）

交叉核心：cross-modal coupling 在蒸馏中是效率来源（correspondence preservation），在遗忘中是主要障碍（modality anchor），在扩散保护中是控制手段（trajectory alignment）——同一个技术概念在三个场景中充当不同角色。

验证页面：[Federated Distillation and Unlearning](../federated-learning/topics/federated-distillation-and-unlearning.md)、[index.md](../../index.md)

### Q14: 证据等级完整性

问题：当前 wiki 中 evidence_level 为 full-paper 的论文有哪些？哪些仍是 abstract-only？

期望答案：
- **full-paper**（6 篇）：Long-tailed Dataset Distillation、LSN (ICLR 2024)、NegPrompt (CVPR 2024)、Topological ML Nanocrystal Synthesis (JACS 2025)、PALCAS、Rethinking Long-tailed Distillation（升级后）。
- **skimmed**（14 篇）：ProCo、TAFAP、12 篇 federated-learning 论文。
- **abstract-only**（0 篇）：先前 5 篇 abstract-only 已在 Phase 2 全部升级。

验证页面：[index.md](../../index.md)

### Q15: 孤儿检测 — 未被任何 topic 页覆盖的论文

问题：当前 wiki 中哪些论文未被任何 topic 页索引？（即"孤儿论文"——有 paper page 但无 topic page 引用）

期望答案（2026-05-05 状态）：federated-learning 域中 6 篇——privacy-preserving-fl-dp-he、agentreputation、intrusion-detection-its、federated-weather-modeling、fsclb、meritocratic-fairness。这些论文有 cross-links 但缺少上层 topic 线程归属。

验证页面：[index.md](../../index.md)、[FL Heterogeneity and Optimization](../federated-learning/topics/fl-heterogeneity-and-optimization.md)、[Federated Distillation and Unlearning](../federated-learning/topics/federated-distillation-and-unlearning.md)

---

## 执行报告 2026-05-20

### 总览

```
35 题执行结果
├── ✅ 完全通过  32 题  ████████████████████████████████  91.4%
├── ⚠️ 部分通过   3 题  ███                                8.6%
└── ❌ 不可答     0 题                                     0.0%
```

**可回答率 100%**（无一道"查不到"），完全通过率 91.4%。

### 逐题详情

| 题号 | 领域 | 题型 | 结果 | 说明 |
|------|------|------|------|------|
| Q1 | Distillation | 事实检索 | ✅ | ProCo 的 retrieval-based correspondence consistency metric 已明确记录 |
| Q2 | Distillation | 跨论文比较 | ✅ | RLDD (statistical alignment) vs ProCo (correspondence coverage) 差异清晰 |
| Q3 | Distillation | 机制理解 | ✅ | TAFAP trajectory vs snapshot 持久性差异已完整解释 |
| Q4 | OOD | 跨论文比较 | ✅ | LSN (class-specific) vs NegPrompt (transferable) 核心差异明确 |
| Q5 | OOD | 机制理解 | ⚠️ | 核心定性发现存在（negative 必须 class-specific），但缺定量细节：prompt 数 (8 vs 2) 和 epoch (25 vs 5) 未记录 |
| Q6 | Spectrum | 方法链 | ✅ | 5 步 pipeline（transformer→UMAP→topology→Beer-Lambert→intermediates）完整 |
| Q7 | Spectrum | 边界判断 | ✅ | 4 项局限均有记录（验证需求、泛化未测、因果差距、定性限制） |
| Q8 | Autonomous Driving | 方法创新 | ✅ | PDQN 混合动作空间（离散变道+连续加速度）明确记录 |
| Q9 | Autonomous Driving | 场景约束 | ⚠️ | RSS 模型和 MSR 93.33% 已记录，但绝对碰撞率 2.45% 未在 wiki 中（仅有相对降低率） |
| Q10 | Federated Learning | 架构理解 | ✅ | EASE 三锚（Modality/Subspace/Temporal）+ BKE/GSD/PFL 机制完整 |
| Q11 | Federated Learning | 跨域连接 | ✅ | FedHD↔distillation 域的多条技术连接在 topic 页和 related_pages 中存在 |
| Q12 | Federated Learning | 分类判断 | ✅ | AgentReputation 的 decentralized-ai 归属标记和分类说明已记录 |
| Q13 | 跨域综合 | 跨域比较 | ✅ | 联邦蒸馏跨越 3 域的连接在 Federated Distillation and Unlearning topic 页完整 |
| Q14 | 跨域综合 | 证据等级 | ⚠️ | 期望答案的 "6 篇 full-paper" 已过时（5/5 状态），当前 wiki 有 14 篇 full-paper，检索可获正确值 |
| Q15 | 跨域综合 | 孤儿检测 | ✅ | 6 篇 orphan 论文可从 index.md 交叉验证 |
| Q16 | LLM Reasoning | 事实检索 | ✅ | CoRD 的 predictive perplexity 选择准则及其优于 PRM/Binary Judgment 的证据完整 |
| Q17 | LLM Reasoning | 机制理解 | ✅ | 策展式两局限（无 teacher 交互、无动态探索）在 CoRD 页明确记录 |
| Q18 | LLM Reasoning | 跨域区分 | ✅ | 模型级蒸馏 vs 数据级压缩的区分在 Long-CoT 概念页明确 |
| Q19 | LLM Reasoning | 跨域连接 | ✅ | CoRD 逐步协同 + FedHD 课程联邦的哲学共性可从各自页面检索合成 |
| Q20 | FL 深度 | 机制理解 | ✅ | FedSD2C 双层信息损失（数据→模型 / 模型→逆向数据）完整记录 |
| Q21 | FL 深度 | 方法迁移 | ✅ | FedHAW hypergradient 迁移洞察 + vs FedLAW 优势明确 |
| Q22 | FL 深度 | 跨论文比较 | ✅ | FedHarmony consensus correlation vs FedAvg data-size weighting 差异完整 |
| Q23 | FL 深度 | 系统设计 | ✅ | FedACT alignment scoring（设备-作业匹配 + participation fairness）完整 |
| Q24 | FL 深度 | 量化对比 | ✅ | 硬件配置（4×A4000, i9-10900X, 64GB）、JCT 8.3×、准确率 +44.5% 全部验证 |
| Q25 | Distillation 深度 | 事实检索 | ✅ | COBRA uniform-weight barycenter（squared Mahalanobis, 闭式解）完整记录 |
| Q26 | Distillation 深度 | 跨论文比较 | ✅ | COBRA (subgroup bias) vs RLDD (class imbalance) 正交互补关系明确 |
| Q27 | Distillation 深度 | 机制理解 | ✅ | COBRA"只改 target 不改 loss"的兼容性机制完整 |
| Q28 | Distillation 深度 | 消融分析 | ✅ | RLDD 三组件贡献（-10%/-2%/-1%）在消融实验节验证 |
| Q29 | 跨域综合续 | 跨域连接 | ✅ | FedSD2C (V-information) vs ProCo (correspondence coverage) 压缩哲学可从各自页面合成 |
| Q30 | 跨域综合续 | 跨域连接 | ✅ | TAFAP trajectory alignment ↔ CoRD step-wise decoding 共享"过程优于快照"哲学，各页面可独立验证 |
| Q31 | 跨域综合续 | 三域交叉 | ✅ | cross-modal coupling 三重角色（效率来源/遗忘障碍/检测工具）跨三域页面可合成 |
| Q32 | Meta | 结构完整性 | ✅ | comparison 缺口（LSN/NegPrompt, COBRA/RLDD, FedHD/FedSD2C）可从 index.md 验证 |
| Q33 | Meta | 孤儿检测 | ✅ | 6 篇孤儿论文 + 重组方案可从 index.md 检索 |
| Q34 | Meta | 优先级 | ✅ | 升级优先级（EASE > ProCo > TAFAP）可从 evidence_level 和跨域引用度推理 |
| Q35 | Meta | 反模式 | ✅ | 4 项结构问题（0 comparison/0 method/6 orphan/未全量捞针）可从 AGENTS.md 和 index.md 验证 |

### 3 题部分通过的改进建议

| 题号 | 缺失内容 | 改进动作 |
|------|---------|---------|
| Q5 | LSN Table 5 中 positive/negative prompt 的具体数量对比 (8 vs 2) 和训练 epoch 对比 (25 vs 5) | 在 LSN 论文页的"Positive vs. Negative Prompt Learning 的关键差异"节补充具体数字 |
| Q9 | PALCAS 的绝对碰撞率数值（2.45% at 60% CAV） | 在 PALCAS 论文页的实验结果中补充绝对碰撞率 |
| Q14 | 期望答案已过时（反映 5/5 而非 5/20 状态） | 定期更新期望答案以匹配当前 wiki 状态，或改写为"列出当前 full-paper 论文"而非硬编码列表 |

### 与上次执行对比

| 指标 | 5/5（初始） | 5/20（本次） |
|------|-----------|-----------|
| 题目数 | 15 | 35 |
| 已执行 | 0 | 35 |
| 可回答率 | — | 100% |
| 完全通过率 | — | 91.4% |
| 新覆盖域 | — | +LLM Reasoning, +Meta 结构 |

| 日期 | 执行人 | 问题数 | 通过 | 失败 | 备注 |
|------|--------|--------|------|------|------|
| 2026-05-05 | — | 15 | — | — | 初始测试集创建，尚未执行 |
| 2026-05-20 | — | 35 (+20) | — | — | 扩展：新增 LLM Reasoning (4题)、FL 深度 (5题)、Distillation 深度 (4题)、跨域综合续 (3题)、Meta 结构 (4题) |
| 2026-05-20 | Claude | 35 | 32 ✓ | 3 ⚠ | 详细结果见下方执行报告。32 题完全通过，3 题部分通过（缺失细节），0 题不可答 |

## 使用说明

1. 每次 major ingest 后随机选 3-5 题执行捞针。
2. 回答必须从 wiki 检索，不允许凭记忆或外部知识。
3. 失败项返回对应页面进行修正（事实错误）或补充（信息缺失）。
4. 本测试集随 wiki 演化更新——新论文、新 topic 或新发现的知识缺口应转化为新测试题。
