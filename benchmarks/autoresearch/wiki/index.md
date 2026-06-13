# Wiki 索引

这是分层论文知识库的第一检索入口。进入具体领域页面之前，先读这里。

## 文件夹地图

- `raw/inbox/`：待摄入的新论文或源文件。摄入完成后移入 `raw/sources/`。
- `raw/sources/`：已摄入的不可变规范副本（论文 PDF、提取文本、元数据），采用 `YYYY-MM-DD-short-title.ext` 命名。
- `wiki/index.md`：知识层的规范导航文件。
- `wiki/log.md`：知识层的维护时间线。
- `wiki/domains/meta/`：wiki 方法、仓库规则和结构演化。
- `wiki/domains/distillation/`：数据集蒸馏、长尾蒸馏、多模态压缩和轨迹匹配相关研究。
- `wiki/domains/outofdistributiondetection/`：分布外检测研究。
- `wiki/domains/spectrum/`：光谱和光谱数据中心的机器学习研究。
- `wiki/domains/autonomous-driving/`：自动驾驶、联邦强化学习和变道决策研究。
- `wiki/domains/federated-learning/`：联邦学习、隐私增强、联邦蒸馏、联邦遗忘、联邦 bandits 和多作业调度研究。
- `wiki/domains/llm-reasoning/`：大语言模型推理蒸馏、Long-CoT 思维链和多 teacher 协同解码研究。
- `wiki/domains/object-detection/`：目标检测，增量目标检测和 DETR 相关研究。
- `wiki/cross-cutting/`：跨域技术索引——按技术概念/模式/方法家族找论文，而非按领域。
- 研究领域现在采用论文优先 schema：`papers/` 存放规范论文页，`methods/`、`datasets/`、`tasks/`、`metrics/`、`concepts/`、`topics/`、`comparisons/`、`analyses/` 存放可复用研究知识。研究领域里的旧 `sources/` 页面保留为 `superseded` 跳转页。

## 领域地图

- `meta`：这个论文知识库本身的结构、维护方式和仓库级综合。
- `distillation`：数据集蒸馏、多模态压缩、长尾蒸馏和轨迹匹配相关方法。
- `outofdistributiondetection`：OOD 检测方法，目前由 negative prompt 方向起步。
- `spectrum`：光谱中心和光谱数据中心的机器学习论文。
- `autonomous-driving`：自动驾驶中的联邦强化学习、变道决策和多智能体协同。
- `federated-learning`：联邦学习——分布式隐私保护机器学习，覆盖聚合优化、个性化、隐私增强、联邦蒸馏、联邦遗忘、联邦 bandits 和面向医疗/天气/ITS 的应用。
- `llm-reasoning`：LLM 推理蒸馏——Long-CoT 思维链、多 teacher 协同解码和推理数据合成。
- `object-detection`：目标检测——增量目标检测、DETR 架构和 evolving world 数据分布变化研究。
- `cross-cutting`：跨域技术索引——按技术概念/模式/方法家族找论文。

## Cross-Cutting（跨域技术索引）

- [跨域技术索引](cross-cutting/index.md)：按技术概念而非领域组织论文的二级入口。
- [受控增量整合](cross-cutting/controlled-incremental-integration.md)：CD (SE2D) × FedHD × CoRD 的共性哲学——拒绝均匀融合，先稳定再扩展。
- [遗忘机制统一理解](cross-cutting/forgetting-mechanisms.md)：UKF × FL Catastrophic Forgetting 的共通根因与差异化缓解。
- [跨模态耦合三重角色](cross-cutting/cross-modal-coupling.md)：蒸馏的效率来源 / 遗忘的主要障碍 / OOD 检测的控制手段。
- [Matching 方法家族](cross-cutting/matching-family-taxonomy.md)：Distribution / Gradient / Trajectory / Correspondence / Curriculum / Step-wise Matching 完整谱系。
- [防多数偏差](cross-cutting/fedharmony-cobra-uniform-philosophy.md)：FedHarmony × COBRA 的均匀哲学——拒绝按规模加权。

## Meta

### 分析

- [Inbox Paper Topic Classification 2026-04-25](domains/meta/analyses/inbox-paper-topic-classification-2026-04-25.md)：把当前 inbox 论文按单标签归入 `distillation`、`outofdistributiondetection` 或 `spectrum`。更新：2026-04-25。来源：6。
- [Research Paper Wiki Rearchitecture Proposal 2026-04-25](domains/meta/analyses/research-paper-wiki-rearchitecture-proposal-2026-04-25.md)：已采纳的论文优先 schema 重构方案，引入方法、数据集、指标、原子 claim 和 comparison 层。更新：2026-04-25。来源：1。
- [Wiki Needle Tests 2026-05-05](domains/meta/analyses/needle-tests-2026-05-05.md)：全 wiki 捞针测试集——35 道跨域核心知识检索题，覆盖 7 个领域的事实检索、跨论文比较、机制理解和分类判断四类题型。更新：2026-05-20。
- [LLMwiki 优化评估 2026-05-16](domains/meta/analyses/autoresearch-optimization-evaluation-2026-05-16.md)：基于 22 篇论文、3 组案例的定量+定性优化评价——证据等级分布、捞针测试执行、反模式消除、跨域知识发现。更新：2026-05-16。
- [Autoresearch 功能模块汇报 2026-05-20](domains/meta/analyses/autoresearch-function-status-report-2026-05-20.md)：按 6 大功能模块（ingest/query/compare/lint/analysis/schema）的现状汇报——每模块含案例、定量指标、定性评价、不足及汇报策略建议。更新：2026-05-20。

### 概念

- [Persistent LLM Wiki](domains/meta/concepts/persistent-llm-wiki.md)：把原始材料编译成可维护、可链接 markdown wiki 的核心模式。更新：2026-04-20。来源：1。

### 来源

- [LLM Wiki](domains/meta/sources/karpathy-llm-wiki.md)：说明 raw/wiki/schema 架构和 ingest-query-lint 工作流的基础笔记。更新：2026-04-20。来源：1。

### 主题

- [Second Brain](domains/meta/topics/second-brain.md)：本仓库作为本地优先、LLM 维护的分层论文知识库的运行综合页。更新：2026-04-25。来源：7。

### 指标

- [Accuracy (Top-1 / Top-5)](domains/meta/metrics/accuracy.md)：分类准确率——wiki 中 9+ 论文使用的跨域共享指标。更新：2026-05-24。来源：9+。

### 对比

- [Cross-Modal Coupling 的三重角色](domains/meta/comparisons/cross-modal-coupling-triple-role.md)：蒸馏 (ProCo) / 遗忘 (EASE) / OOD 检测 (LSN) 中跨模态耦合的统一分析——效率来源 vs. 主要障碍 vs. 控制手段。更新：2026-05-24。来源：3。

## Distillation

### 概念

- [Dataset Distillation](domains/distillation/concepts/dataset-distillation.md)：紧凑学习范式，已连接长尾、多模态、轨迹控制和公平蒸馏研究线。更新：2026-05-05。来源：4。

### 论文

- [Correspondence Coverage Matters for Multi-Modal Dataset Distillation](domains/distillation/papers/correspondence-coverage-matters-multimodal-dataset-distillation.md)：AAAI 2026 论文，提出 ProCo——用 retrieval-based correspondence consistency metric 聚类和 conditional neural fields 参数化实现多模态蒸馏的 correspondence coverage。证据等级：skimmed。更新：2026-05-05。来源：1。
- [Fair Dataset Distillation via Cross-Group Barycenter Alignment](domains/distillation/papers/fair-dataset-distillation-cobra.md)：ICML 2026 投稿，提出 COBRA——群体无关重心对齐消除子群体偏差放大，兼容 DC/DM/CAFE/IDC/MTT 所有主流蒸馏。证据等级：full-paper。更新：2026-05-05。来源：1。
- [Rethinking Long-tailed Dataset Distillation: A Uni-Level Framework with Unbiased Recovery and Relabeling](domains/distillation/papers/rethinking-long-tailed-dataset-distillation.md)：AAAI 2026 论文，用 statistical alignment、expert model debiasing 和 BN recalibration 处理长尾数据集蒸馏。证据等级：full-paper。更新：2026-05-05。来源：1。
- [Targeted Data Protection for Diffusion Model by Matching Training Trajectory](domains/distillation/papers/targeted-data-protection-diffusion-model-training-trajectory.md)：AAAI 2026 论文，提出 TAFAP——首个用 trajectory alignment（完整训练轨迹而非 snapshot）实现有效 targeted data protection 的 diffusion 防御方法。证据等级：skimmed。更新：2026-05-05。来源：1。
- [Continual Distillation of Teachers from Different Domains](domains/distillation/papers/continual-distillation-teachers-different-domains.md)：arXiv 2026 论文，提出 Continual Distillation (CD) 新范式——学生从不同领域教师模型序列中顺序蒸馏，发现外部数据触发 UKT/UKF 双效应，提出 SE2D 通过保留 ED logits 平衡迁移与遗忘。CIFAR20 SE2D 76.17±0.85（+9.48pp over Self-Dist on D1），Digits 87.00±0.60，Forgetting 降低 33-47%。证据等级：full-paper。更新：2026-05-24。来源：1。
- [CD²: Constrained Dataset Distillation for Few-Shot Class-Incremental Learning](domains/distillation/papers/cd2-constrained-dataset-distillation-fscil.md)：arXiv 2026 论文，首次将数据集蒸馏引入 FSCIL——用 DDM 合成压缩记忆样本 + DCM 特征保留 + 结构保留损失约束跨会话分布偏移。CIFAR-100 平均准确率 68.67%（vs. NC-FSCIL 67.50%），CUB200 平均准确率 68.78%。证据等级：full-paper。更新：2026-05-30。来源：1。

### 主题

- [Diffusion Model Data Protection](domains/distillation/topics/diffusion-model-data-protection.md)：关于 diffusion fine-tuning 中轨迹感知防御和主动重定向的主题。更新：2026-05-05。来源：1。
- [Fair Dataset Distillation](domains/distillation/topics/fair-dataset-distillation.md)：子群体公平蒸馏主题——群体不平衡×表示分离的交互偏差放大，以及 COBRA 重心对齐框架。更新：2026-05-05。来源：1。
- [Long-Tailed Dataset Distillation](domains/distillation/topics/long-tailed-dataset-distillation.md)：关于不平衡数据集蒸馏、statistical alignment 和 debiasing 的主题。更新：2026-05-05。来源：1。
- [Multi-Modal Dataset Distillation](domains/distillation/topics/multimodal-dataset-distillation.md)：关于跨模态 correspondence 覆盖和配对数据蒸馏的主题。更新：2026-05-05。来源：1。

### 方法

- [ProCo — Promote Correspondence Coverage](domains/distillation/methods/proco.md)：多模态数据集蒸馏——correspondence consistency metric 聚类 + coverage-aware 正则化 + conditional neural fields。更新：2026-05-24。来源：1。
- [COBRA — Cross-Group Barycenter Alignment](domains/distillation/methods/cobra.md)：公平数据集蒸馏——uniform-weight barycenter 替代群体比例加权聚合目标，兼容 DC/DM/CAFE/IDC/MTT。更新：2026-05-24。来源：1。
- [RLDD — Rethinking Long-tailed Dataset Distillation](domains/distillation/methods/rldd.md)：长尾数据集蒸馏统一框架——statistical alignment + BN recalibration + multi-round initialization。更新：2026-05-24。来源：1。
- [SE2D — Self External Data Distillation](domains/distillation/methods/se2d.md)：持续蒸馏的 logit 保持方法——通过外部数据 logit 正则化平衡 UKT 和 UKF。更新：2026-05-24。来源：1。

### 数据集

- [CIFAR-10 / CIFAR-10-LT / CIFAR10-S](domains/distillation/datasets/cifar-10.md)：10 类 32×32 分类基准，含长尾（LT）和有偏（S）变体。被 RLDD、COBRA、LSN 使用。更新：2026-05-24。来源：3。
- [CIFAR-100 / CIFAR-100-LT](domains/distillation/datasets/cifar-100.md)：100 类 32×32 分类基准，含长尾变体——类别数是 CIFAR-10 的 10 倍。被 RLDD、LSN 使用。更新：2026-05-24。来源：2。
- [Tiny-ImageNet / Tiny-ImageNet-LT](domains/distillation/datasets/tiny-imagenet.md)：200 类 64×64 分类基准，含长尾变体——更高分辨率蒸馏 benchmark。被 RLDD、FedSD2C、NegPrompt 使用。更新：2026-05-24。来源：3。
- [MS-COCO](domains/distillation/datasets/ms-coco.md)：大规模图像-文本配对数据集（330K+ 图像），图文检索蒸馏 benchmark。被 ProCo 使用。更新：2026-05-24。来源：1。

### 指标

- [Equalized Odds Difference (EOD)](domains/distillation/metrics/equalized-odds.md)：子群体公平性指标——衡量不同敏感群体之间的预测公平性。COBRA 核心指标。更新：2026-05-24。来源：1。
- [PSNR / SSIM](domains/distillation/metrics/psnr-ssim.md)：图像质量评估指标——在 FedSD2C 中用作隐私保护水平的逆向度量。更新：2026-05-24。来源：1。

### 对比

- [COBRA vs RLDD — 蒸馏公平性维度对比](domains/distillation/comparisons/cobra-vs-rldd.md)：类内公平（subgroup bias / COBRA）vs. 类间公平（class imbalance / RLDD）——正交互补。更新：2026-05-24。来源：2。

## Out-of-Distribution Detection

### 概念

- [Out-of-Distribution Detection](domains/outofdistributiondetection/concepts/out-of-distribution-detection.md)：检测输入是否落在训练或部署分布之外的概念，已连接 negative-prompt、class-specific 和 transferable 方法分支。更新：2026-05-05。来源：2。

### 论文

- [Learning Transferable Negative Prompts for Out-of-Distribution Detection](domains/outofdistributiondetection/papers/learning-transferable-negative-prompts-ood-detection.md)：CVPR 2024 论文，提出 NegPrompt——只用 ID 数据学习可迁移 negative prompts，支持 open-vocabulary OOD detection。证据等级：full-paper。更新：2026-05-05。来源：1。
- [Out-of-Distribution Detection with Negative Prompts](domains/outofdistributiondetection/papers/out-of-distribution-detection-with-negative-prompts.md)：ICLR 2024 论文，提出 LSN——学习 class-specific negative prompts + semantic orthogonality loss，发现 positive/negative prompt learning 的根本差异。证据等级：full-paper。更新：2026-05-05。来源：1。

### 主题

- [Negative Prompt OOD Detection](domains/outofdistributiondetection/topics/negative-prompt-ood-detection.md)：negative prompt 方法族（LSN + NegPrompt）及其 class-specific vs. transferable 设计空间主题。更新：2026-05-05。来源：2。

### 方法

- [LSN — Learn to Say No](domains/outofdistributiondetection/methods/lsn.md)：Class-specific negative prompts + semantic orthogonality loss——多样化优先。ICLR 2024。更新：2026-05-24。来源：1。
- [NegPrompt — Transferable Negative Prompts](domains/outofdistributiondetection/methods/negprompt.md)：共享可迁移 negative prompts + open-vocabulary OOD detection——通用性优先。CVPR 2024。更新：2026-05-24。来源：1。

### 指标

- [AUROC](domains/outofdistributiondetection/metrics/auroc.md)：OOD 检测的 ROC 曲线下面积——threshold-free 整体排序质量指标。LSN、NegPrompt 共同使用。更新：2026-05-24。来源：2。
- [FPR95](domains/outofdistributiondetection/metrics/fpr95.md)：95% TPR 下的假阳性率——高召回区域的实用性能指标。LSN、NegPrompt 共同使用。更新：2026-05-24。来源：2。

### 对比

- [LSN vs NegPrompt — Negative Prompt 方法对比](domains/outofdistributiondetection/comparisons/lsn-vs-negprompt.md)：Class-specific 覆盖 vs. transferable 通用性——negative prompt OOD 检测的两个互补分支。更新：2026-05-24。来源：2。

## Spectrum

### 概念

- [Spectroscopic Manifold Learning](domains/spectrum/concepts/spectroscopic-manifold-learning.md)：从高维光谱测量中学习结构的概念，已连接拓扑流形学习和反应路径发现。更新：2026-05-05。来源：1。

### 论文

- [Topological Machine Learning Unveils Hidden Reaction Pathways in Nanocrystal Synthesis](domains/spectrum/papers/topological-machine-learning-nanocrystal-synthesis.md)：JACS 2025 论文，用 transformer-augmented UMAP 拓扑流形学习从 UV-vis 光谱中推断 InAs 纳米晶合成的隐藏反应路径和亚稳态中间体。证据等级：full-paper。更新：2026-05-05。来源：1。

### 主题

- [Spectrum-Based Reaction Pathway Discovery](domains/spectrum/topics/spectrum-based-reaction-pathway-discovery.md)：用光谱和拓扑流形学习推断机制性反应轨迹的主题。更新：2026-05-05。来源：1。

## Autonomous Driving

### 概念

- [联邦强化学习与自动驾驶](domains/autonomous-driving/concepts/federated-reinforcement-learning-autonomous-driving.md)：FedRL 在自动驾驶中的分布式训练范式、应用现状与核心挑战。更新：2026-05-05。来源：1。

### 论文

- [PALCAS: A Priority-Aware Intelligent Lane Change Advisory System for Autonomous Vehicles using Federated Reinforcement Learning](domains/autonomous-driving/papers/palcas-priority-aware-lane-change-federated-rl.md)：arXiv 2026 论文，首个联邦多智能体 RL 变道决策框架，用 priority-guided reward 和 PDQN 混合动作空间统一强制性与自主性变道。证据等级：full-paper。更新：2026-05-05。来源：1。

### 任务

- [变道决策](domains/autonomous-driving/tasks/lane-change-decision-making.md)：自动驾驶中核心运动规划子任务的定义、评估设定与代表性方法。更新：2026-05-05。来源：1。

### 方法

- [PALCAS — Priority-Aware Lane Change Advisory System](domains/autonomous-driving/methods/palcas.md)：联邦多智能体 RL 变道决策——PDQN 混合动作空间 + priority-guided 多目标奖励。更新：2026-05-24。来源：1。

## Federated Learning

### 概念

- [Federated Learning](domains/federated-learning/concepts/federated-learning.md)：分布式隐私保护机器学习范式——多客户端本地训练、服务器聚合，覆盖统计异质性、系统异质性、隐私增强、个性化和联邦遗忘等子方向。更新：2026-05-05。来源：13。

### 论文

- [Privacy-Preserving FL via DP and HE for Cardiovascular Disease Risk Modeling](domains/federated-learning/papers/privacy-preserving-fl-dp-he-cardiovascular.md)：arXiv 2026 论文，在瑞典全国健康数据上系统比较 FL+DP 与 FL+HE 的隐私-效用 trade-off。证据等级：full-paper。更新：2026-05-05。来源：1。
- [FedHarmony: Harmonizing Heterogeneous Label Correlations in Federated Multi-Label Learning](domains/federated-learning/papers/fedharmony-heterogeneous-label-correlations-federated-multi-label.md)：arXiv 2026 论文，提出 consensus correlation 机制利用跨客户端标签相关性共识纠正 label correlation drift。证据等级：full-paper。更新：2026-05-05。来源：1。
- [FedACT: Concurrent Federated Intelligence across Heterogeneous Data Sources](domains/federated-learning/papers/fedact-concurrent-federated-intelligence.md)：IPDPS 2026 论文，资源感知多作业 FL 调度，alignment scoring + participation fairness，JCT 减少 8.3×、准确率提升 44.5%。证据等级：full-paper。更新：2026-05-05。来源：1。
- [AgentReputation: A Decentralized Agentic AI Reputation Framework](domains/federated-learning/papers/agentreputation-decentralized-agentic-ai-reputation.md)：arXiv 2026 框架论文，三层去中心化 AI agent 声誉架构——context-conditioned reputation cards + adaptive verification escalation。证据等级：skimmed。更新：2026-05-05。来源：1。
- [Intrusion Detection in Intelligent Transport Systems via Trust-Aware Federated Hybrid Learning](domains/federated-learning/papers/intrusion-detection-intelligent-transport-systems-fl.md)：arXiv 2026 论文，trust-aware 联邦混合入侵检测框架，结合 RF+DT+SVM 互补表征与加权聚合。证据等级：skimmed。更新：2026-05-05。来源：1。
- [Federated Weather Modeling on Sensor Data](domains/federated-learning/papers/federated-weather-modeling-sensor-data.md)：arXiv 2026 概念论文，联邦学习整合地面站、卫星和 IoT 多源传感数据的天气建模范式。证据等级：skimmed。更新：2026-05-05。来源：1。
- [FedHAW: Federated Learning with Hypergradient-based Online Update of Aggregation Weights](domains/federated-learning/papers/fedhaw-hypergradient-aggregation-weights.md)：IEEE 2026 letter，hypergradient 在线更新 FL 聚合权重，无需额外训练数据，对通信错误鲁棒。证据等级：full-paper。更新：2026-05-05。来源：1。
- [FSCLB: Scaling Federated Linear Contextual Bandits via Sketching](domains/federated-learning/papers/federated-sketch-contextual-linear-bandits-fsclb.md)：arXiv 2026 论文，双 sketch 策略 + SVD 间接行列式将联邦 bandit 计算和通信成本降低 90%+，regret 匹配 optimal。证据等级：skimmed。更新：2026-05-05。来源：1。
- [FedHD: Federated Distillation for Whole Slide Image via Gaussian-Mixture Feature Alignment](domains/federated-learning/papers/fedhd-federated-distillation-whole-slide-image.md)：ICML 2026 论文，WSI 联邦数据集蒸馏——高斯混合对齐捕捉多组分形态、one-to-one 蒸馏保留诊断多样性、课程联邦集成。证据等级：full-paper。更新：2026-05-05。来源：1。
- [FedSD2C: One-shot Federated Learning via Synthetic Distiller-Distillate Communication](domains/federated-learning/papers/fedsd2c-one-shot-fl-distiller-distillate.md)：NeurIPS 2024 论文（NUS/Beihang），提出端到端 distillate 合成替代 DFKD 的模型→数据逆向生成，消除双层信息损失，Tiny-ImageNet 上 2.6× 最佳 baseline。证据等级：full-paper。代码：GitHub。更新：2026-05-08。来源：1。
- [EASE: Federated Multimodal Unlearning via Entanglement-Aware Anchor Closure](domains/federated-learning/papers/ease-federated-multimodal-unlearning.md)：arXiv 2026 论文，识别 Anchor Principle（三残差锚），BKE+GSD+PFL 分别闭合模态锚、子空间锚和时间重锚，Flickr30K 上 forget/retain 误差分别 0.2/4.2 R@1。证据等级：skimmed。更新：2026-05-05。来源：1。
- [Meritocratic Fairness in Budgeted Combinatorial Multi-armed Bandits via Shapley Values](domains/federated-learning/papers/meritocratic-fairness-budgeted-bandits-shapley.md)：arXiv 2026 论文，提出 K-Shapley 值与 K-SVFair-FBF 算法，O(T³/⁴) fairness regret，应用于 FL 客户端选择和社交影响。证据等级：skimmed。更新：2026-05-05。来源：1。

### 主题

- [Federated Distillation and Unlearning](domains/federated-learning/topics/federated-distillation-and-unlearning.md)：联邦蒸馏与联邦遗忘的统一视角——cross-modal coupling 既是蒸馏效率的来源也是遗忘的主要障碍，覆盖 FedHD (GM alignment + curriculum federation)、EASE (Anchor Principle + BKE/GSD/PFL) 和 FedSD2C (one-shot distillate communication)。更新：2026-05-08。来源：3。
- [FL Heterogeneity and Optimization](domains/federated-learning/topics/fl-heterogeneity-and-optimization.md)：联邦学习三层异质性——聚合层 (FedHAW hypergradient, FedHarmony consensus correlation)、任务层 (FedKPer generalization-personalization)、系统层 (FedACT multi-job scheduling)——的统一分析。更新：2026-05-05。来源：4。

### 方法

- [FedHD — Federated Distillation for WSI](domains/federated-learning/methods/fedhd.md)：面向全切片图像的联邦数据集蒸馏——高斯混合对齐 + onetone 蒸馏 + 课程联邦。ICML 2026。更新：2026-05-24。来源：1。
- [FedSD2C — Synthetic Distiller-Distillate Communication](domains/federated-learning/methods/fedsd2c.md)：一次性联邦学习端到端蒸馏——V-information Core-Set + Fourier 扰动 + Autoencoder latent 优化。NeurIPS 2024。更新：2026-05-24。来源：1。

### 数据集

- [MNIST / Colored-MNIST / MNIST-M](domains/federated-learning/datasets/mnist.md)：28×28 数字分类基准，含颜色偏差（COBRA fairness）和跨域数字识别（CD Digits benchmark）变体。被 COBRA、CD 使用。更新：2026-05-24。来源：2。

### 对比

- [FedHarmony vs FedAvg — 联邦多标签聚合策略对比](domains/federated-learning/comparisons/fedharmony-vs-fedavg.md)：数据量加权 vs. consensus correlation 加权——多数偏差污染全局的两种哲学。更新：2026-05-24。来源：1。

## LLM Reasoning

### 概念

- [Long-CoT 推理蒸馏](domains/llm-reasoning/concepts/long-cot-reasoning-distillation.md)：通过逐步协同解码从大型推理模型中蒸馏长链推理能力的概念，已连接 CoRD 和多 teacher 协同范式。更新：2026-05-05。来源：1。

### 论文

- [Distilling Long-CoT Reasoning through Collaborative Step-wise Multi-Teacher Decoding](domains/llm-reasoning/papers/distilling-long-cot-reasoning-cord.md)：arXiv 2026 论文（KAIST/UNIST），提出 CoRD——基于预测困惑度的逐步多 teacher 协同解码，在 AIME24/25 上学生模型超越所有单个 teacher。证据等级：full-paper。代码：GitHub。更新：2026-05-05。来源：1。

### 方法

- [CoRD — Collaborative Reasoning Decoding](domains/llm-reasoning/methods/cord.md)：Long-CoT 推理蒸馏——逐步协同解码 + predictive perplexity 步骤选择 + beam search。学生超越 teacher。更新：2026-05-24。来源：1。

### 对比

- [CoRD vs Curation — Long-CoT 推理蒸馏范式对比](domains/llm-reasoning/comparisons/cord-vs-curation.md)：逐步协同解码 vs. post-hoc 策展——实时 teacher 交互 vs. 事后择优。更新：2026-05-24。来源：1。

## Object Detection

### 论文

- [EW-DETR: Evolving World Object Detection via Incremental Low-Rank DEtection TRansformer](domains/object-detection/papers/ew-detr-evolving-world-object-detection.md)：arXiv 2026 论文，提出 EW-DETR——首个基于 DETR 的增量目标检测框架，用低秩适配（LoRA）+ 知识蒸馏实现 evolving world 场景下的持续目标检测，在 COCO 增量序列上 AP 优于所有比较方法。证据等级：full-paper。更新：2026-05-30。来源：1。

## 实体

- [KAIST & UNIST — CoRD 团队](domains/llm-reasoning/entities/kaist-unist-cord.md): CoRD 论文的研究团队（Taewon Yun, Hwanjun Song et al.），DISL Lab，KAIST & UNIST。更新：2026-05-24。来源：1。
- [NUS & Beihang — FedSD2C 团队](domains/federated-learning/entities/nus-beihang-fedsd2c.md): FedSD2C 论文的研究团队（Junyuan Zhang, Xinchao Wang et al.），NeurIPS 2024，NUS & 北京航空航天大学。更新：2026-05-24。来源：1。
