# Wiki 日志

摄入、查询、维护、迁移和 schema 变更的追加式时间线。

## [2026-05-24] schema | 填充空壳目录 — 创建 27 个 wiki 页面

- 更新：10 个方法页、5 个数据集页、5 个指标页、5 个对比页、2 个实体页
- **方法页**（10）：
  - distillation: [ProCo](domains/distillation/methods/proco.md)、[COBRA](domains/distillation/methods/cobra.md)、[RLDD](domains/distillation/methods/rldd.md)、[SE2D](domains/distillation/methods/se2d.md)
  - OOD: [LSN](domains/outofdistributiondetection/methods/lsn.md)、[NegPrompt](domains/outofdistributiondetection/methods/negprompt.md)
  - FL: [FedHD](domains/federated-learning/methods/fedhd.md)、[FedSD2C](domains/federated-learning/methods/fedsd2c.md)
  - LLM Reasoning: [CoRD](domains/llm-reasoning/methods/cord.md)
  - AD: [PALCAS](domains/autonomous-driving/methods/palcas.md)
- **数据集页**（5）：[CIFAR-10](domains/distillation/datasets/cifar-10.md)、[CIFAR-100](domains/distillation/datasets/cifar-100.md)、[Tiny-ImageNet](domains/distillation/datasets/tiny-imagenet.md)、[MS-COCO](domains/distillation/datasets/ms-coco.md)、[MNIST](domains/federated-learning/datasets/mnist.md)
- **指标页**（5）：[Accuracy](domains/meta/metrics/accuracy.md)、[AUROC](domains/outofdistributiondetection/metrics/auroc.md)、[FPR95](domains/outofdistributiondetection/metrics/fpr95.md)、[EOD](domains/distillation/metrics/equalized-odds.md)、[PSNR/SSIM](domains/distillation/metrics/psnr-ssim.md)
- **对比页**（5）：[LSN vs NegPrompt](domains/outofdistributiondetection/comparisons/lsn-vs-negprompt.md)、[COBRA vs RLDD](domains/distillation/comparisons/cobra-vs-rldd.md)、[FedHarmony vs FedAvg](domains/federated-learning/comparisons/fedharmony-vs-fedavg.md)、[CoRD vs Curation](domains/llm-reasoning/comparisons/cord-vs-curation.md)、[Cross-Modal Coupling 三重角色](domains/meta/comparisons/cross-modal-coupling-triple-role.md)
- **实体页**（2）：[KAIST & UNIST (CoRD)](domains/llm-reasoning/entities/kaist-unist-cord.md)、[NUS & Beihang (FedSD2C)](domains/federated-learning/entities/nus-beihang-fedsd2c.md)
- 同步更新：10 个论文页添加了 `related_pages` 交叉引用；`wiki/index.md` 添加所有新页面条目
- 关键记忆：从 23 篇论文中提取方法→数据集→指标→对比的完整知识图谱；每个方法页包含定义/核心机制/假设/证据/变体/优势局限/关联/开放问题；跨域连接（如 COBRA vs RLDD 公平性维度互补、Cross-Modal Coupling 三重角色）为 wiki 首次系统性的跨论文知识合成
- 未闭合问题：剩余约 10 个单论文独有方法待第二批创建；Spectrum 域暂无方法/数据集/指标页（仅 1 篇论文）

## [2026-06-07] schema | 创建跨域技术索引（cross-cutting/）

- 新增 `wiki/cross-cutting/` 目录——按技术概念/模式而非研究领域组织的二级导航入口
- 创建 6 个页面：
  - [index](cross-cutting/index.md)：跨域技术索引总入口
  - [受控增量整合](cross-cutting/controlled-incremental-integration.md)：CD (SE2D) × FedHD × CoRD 共性哲学
  - [遗忘机制统一理解](cross-cutting/forgetting-mechanisms.md)：UKF × FL Catastrophic Forgetting 统一分析
  - [跨模态耦合三重角色](cross-cutting/cross-modal-coupling.md)：耦合在蒸馏/遗忘/OOD 检测中的不同角色
  - [Matching 方法家族](cross-cutting/matching-family-taxonomy.md)：Distribution/Gradient/Trajectory/Correspondence/Curriculum/Step-wise Matching 完整谱系
  - [防多数偏差](cross-cutting/fedharmony-cobra-uniform-philosophy.md)：FedHarmony × COBRA 的均匀哲学
- 同步更新 `wiki/index.md`：新增 Cross-Cutting 域条目 + 文件夹地图
- 对应 benchmark 改进路线图 P1：5 个跨域 synthesis 页面补全跨域连接题型的知识空白

## [2026-05-30] ingest | CD² + EW-DETR（子 agent 并行处理测试）

- 原始来源：[CD² PDF](../raw/sources/2026-01-15-cd2-constrained-dataset-distillation-fscil.pdf) (arXiv:2601.08519, 9页)、[EW-DETR PDF](../raw/sources/2026-02-20-ew-detr-evolving-world-object-detection.pdf) (arXiv:2602.20985, 18页)
- 更新：[CD² paper](domains/distillation/papers/cd2-constrained-dataset-distillation-fscil.md) (394行, full-paper)、[EW-DETR paper](domains/object-detection/papers/ew-detr-evolving-world-object-detection.md) (313行, full-paper)、[index.md](index.md)（新增 object-detection 域）、log.md
- **首次使用 main-agent/subagent split 工作流**：主 agent 仅做 PDF 移动 + PyMuPDF 全文提取 + spawn 两个子 agent（并行），未读取论文正文内容。子 agent 各自独立完成 paper page 写作。
- CD² 关键发现：首次将 DD 引入 FSCIL——DDM 合成压缩记忆 + DCM 特征保留/结构保留约束跨会话偏移。CIFAR-100 平均 68.67%（>NC-FSCIL 67.50%），CUB200 68.78%。IPC=5 时仅用 125KB 记忆即接近全量数据效果。
- EW-DETR 关键发现：首个 DETR-based 增量检测——Low-Rank Adapter 更新关键参数 + 多尺度知识蒸馏防遗忘。COCO 增量序列 AP 维持优于所有 baseline。新增 object-detection 域（wiki 第 8 个研究领域）。
- 测试结论：新 AGENTS.md ingest workflow（主 agent 编排 + 子 agent 读写）运作正常——两篇论文并行处理，主 agent 全程不直接读论文、不写 paper 页，产出质量符合 full-paper 标准。

## [2026-05-24] upgrade | Continual Distillation 论文升级为 full-paper

- 更新：[CD paper page](domains/distillation/papers/continual-distillation-teachers-different-domains.md) — evidence_level 从 skimmed → full-paper
- 全文 17 页通过 PyMuPDF 完整抽取，覆盖 Introduction (§1) 到 Appendix D
- **新增定量数据**：
  - Table 1：ED ratio 0%→66% 的 UKT 梯度效应（未见 domain 33-45%→44-85%）
  - Table 2：CIFAR20 全部 4 种 ED 场景（D4/CUB/MNIST/Internal Only），3 seeds mean±std
  - Table 3：Digits 全部 2 种场景（SE2D 87.00±0.60, DKD MNIST-M -20.66pp）
  - Table 4：DomainNet 全部 2 种场景（SE2D 48.01 落后 Self-Dist 48.76）
  - Table C.1-C.3：Forgetting 完整分析——SE2D CIFAR20 4.44 vs KL 17.23（-74.2%），Digits 3.73 vs KL 19.17（-80.5%）
  - Table C.4-C.5：ViT-tiny 学生（SE2D 71.09 vs Self-Dist 70.76）、CLIP-base 教师（SE2D 46.83 vs Self-Dist 47.69）
  - Table C.6：额外 DomainNet 序列——简化场景下 SE2D 与 Self-Dist 差距收窄
  - Fig B.1-B.2：ED 质量代理——教师熵分布 kurtosis 预测 UKT 潜力
- **置信度升级**：UKT-UKF trade-off 从 medium→high，ED 相关性层级从 medium→high，SE2D forgetting 缓解从 medium→high
- **同步更新**：[SE2D 方法页](domains/distillation/methods/se2d.md)（证据段升级为 full-paper 定量数据）、[index.md](index.md)（CD paper 条目更新为 full-paper 状态）
- 关键记忆：CD paper 现为 distillation 域第 3 篇 full-paper（继 COBRA、RLDD 之后）；SE2D 的核心 trade-off——在 ED 相关的简单 benchmark 上显著优于 Self-Distillation，但在 domain 差异大/教师质量低的场景下反而不如；ED 质量代理（kurtosis）是论文贡献但仅在一个数据集上验证

## [2026-05-20] ingest | Continual Distillation of Teachers from Different Domains
- 原始来源：[../raw/sources/2026-04-10-continual-distillation-teachers-different-domains.pdf](../raw/sources/2026-04-10-continual-distillation-teachers-different-domains.pdf)
- 更新：[domains/distillation/papers/continual-distillation-teachers-different-domains.md](domains/distillation/papers/continual-distillation-teachers-different-domains.md)、[index.md](index.md)
- 关键记忆：CD 是首个从"持续数据流"转向"持续教师模型流"的蒸馏范式；外部无标签数据同时触发 UKT 和 UKF 双效应；SE2D 通过保留 ED logits 缓解遗忘但效果依赖 ED-教师领域相关性。与数据集蒸馏的本质区别：CD 是模型级蒸馏，DD 是数据级压缩。
- 未闭合问题：ED 质量自动选择策略；feature 级蒸馏在 CD 中的表现；CD 与数据集蒸馏的结合可能性。

## [2026-04-20] setup | 初始化 LLM Wiki
- 创建规范 schema：[../CLAUDE.md](../CLAUDE.md) 和 agent 兼容入口 [../AGENTS.md](../AGENTS.md)。
- 创建初始文件夹结构和导航文件：[index.md](index.md)、[log.md](log.md)。
- 未闭合问题：无。

## [2026-04-20] ingest | LLM Wiki
- 原始来源：[../raw/sources/2026-04-20-karpathy-llm-wiki.md](../raw/sources/2026-04-20-karpathy-llm-wiki.md)
- 更新：[domains/meta/sources/karpathy-llm-wiki.md](domains/meta/sources/karpathy-llm-wiki.md)、[domains/meta/concepts/persistent-llm-wiki.md](domains/meta/concepts/persistent-llm-wiki.md)、[domains/meta/topics/second-brain.md](domains/meta/topics/second-brain.md)、[index.md](index.md)
- 关键记忆：持久 wiki 维护是核心模式；`wiki/index.md` 和 `wiki/log.md` 是一等文件；有复用价值的查询结果应回写到 wiki。
- 未闭合问题：仓库增大后，是否需要在 `wiki/index.md` 之外加入本地搜索工具。

## [2026-04-20] schema | Codex 原生 schema
- 更新：[../AGENTS.md](../AGENTS.md)、[../CLAUDE.md](../CLAUDE.md)
- 关键记忆：`AGENTS.md` 成为 Codex 使用的规范 schema；`CLAUDE.md` 作为兼容层指向 `AGENTS.md`。
- 未闭合问题：无。

## [2026-04-20] organize | 规范化 wiki 路径
- 更新：把早期的 `wiki/` 包裹层恢复为当时 schema 匹配的根级知识文件夹。
- 关键记忆：这是后续分层领域架构之前的中间整理步骤。
- 未闭合问题：无。

## [2026-04-20] ingest | Rethinking Long-tailed Dataset Distillation
- 原始来源：[../raw/sources/2025-12-14-rethinking-long-tailed-dataset-distillation.pdf](../raw/sources/2025-12-14-rethinking-long-tailed-dataset-distillation.pdf)
- 更新：早期 `machine-learning` 路径下的论文页、概念页、主题页、meta 主题页和 [index.md](index.md)。
- 关键记忆：长尾数据集蒸馏需要显式 bias correction，而不能直接沿用平衡数据假设。
- 未闭合问题：需要完整解析 PDF 正文以补充 ablation、实现细节和限制。

## [2026-04-20] lint | inbox 扫描
- 扫描 `raw/inbox/`、`raw/sources/`、已有 wiki 页和日志。
- 已处理：`raw/inbox/aaai2026rethinking.pdf` 对应已归档的 long-tailed dataset distillation 论文。
- 新识别待摄入：`Correspondence Coverage Matters for Multi-Modal Dataset Distillation ... .md` 和 `Targeted Data Protection for Diffusion Model by Matching Training Trajectory ... .md`。
- 未闭合问题：已处理 inbox 副本仍留在 `raw/inbox/`，后续扫描会继续识别为已处理。

## [2026-04-20] ingest | Correspondence Coverage Matters for Multi-Modal Dataset Distillation
- 原始来源：[../raw/sources/2026-03-14-correspondence-coverage-matters-multimodal-dataset-distillation.md](../raw/sources/2026-03-14-correspondence-coverage-matters-multimodal-dataset-distillation.md)
- 关键记忆：多模态数据集蒸馏依赖跨模态 correspondence 覆盖，而不只是单模态相似性；ProCo 用 correspondence clustering 和高效参数化改善预算-效果权衡。
- 未闭合问题：仍缺少 ProCo 与其他多模态蒸馏方法的直接比较。

## [2026-04-20] ingest | Targeted Data Protection for Diffusion Model by Matching Training Trajectory
- 原始来源：[../raw/sources/2026-03-14-targeted-data-protection-diffusion-model-training-trajectory.md](../raw/sources/2026-03-14-targeted-data-protection-diffusion-model-training-trajectory.md)
- 关键记忆：数据集蒸馏里的 trajectory matching 可以迁移到 diffusion model 数据保护；当目标是可控防御时，主动重定向比被动降质更强。
- 未闭合问题：仍缺少 diffusion-model protection 方法和 threat model 的更大地图。

## [2026-04-20] organize | 分层领域架构
- 更新：[../AGENTS.md](../AGENTS.md)、[../CLAUDE.md](../CLAUDE.md)、[index.md](index.md)、meta 和 distillation 相关页面。
- 关键记忆：规范 wiki 文件位于 `wiki/`；持久页面按 `wiki/domains/<domain>/<type>/` 组织。
- 未闭合问题：如果仓库扩展到新方向，应在 `wiki/domains/` 下创建并列 domain。

## [2026-04-25] ingest | inbox 论文主题分类
- 原始来源：[../raw/sources/2024-01-16-out-of-distribution-detection-with-negative-prompts.pdf](../raw/sources/2024-01-16-out-of-distribution-detection-with-negative-prompts.pdf)、[../raw/sources/2024-05-31-learning-transferable-negative-prompts-ood-detection.pdf](../raw/sources/2024-05-31-learning-transferable-negative-prompts-ood-detection.pdf)、[../raw/sources/2025-11-28-topological-machine-learning-nanocrystal-synthesis.pdf](../raw/sources/2025-11-28-topological-machine-learning-nanocrystal-synthesis.pdf)
- 关键记忆：inbox 论文被组织进 `distillation`、`outofdistributiondetection`、`spectrum` 三个单标签领域；negative prompt 论文启动 OOD domain；nanocrystal synthesis 论文因 UV-vis 光谱是中心证据层而归入 `spectrum`。
- 未闭合问题：本地 PDF 抽取能力有限，两篇 PDF 摘要使用了公开 abstract metadata 和本地文件 metadata。

## [2026-04-25] query | 为什么字面 negative prompt 不够
- 更新：OOD negative prompt 论文页和主题页。
- 关键记忆：ICLR 2024 negative-prompt OOD detection 反对直接使用 `not a photo of a [class]`，因为 negative evidence 很多样，单一句面否定不能表达足够丰富的不属于某类的方式。
- 未闭合问题：无。

## [2026-04-25] query | unbiased recovery and relabeling
- 更新：long-tailed dataset distillation 论文页和主题页。
- 关键记忆：unbiased recovery 指恢复更少 head-class 偏置的合成图像；unbiased relabeling 指使用更公平的 soft labels，避免 tail-class 信息被有偏监督冲掉。
- 未闭合问题：需要 PDF 正文抽取来确认摘要之外的实现细节。

## [2026-04-25] analysis | 论文知识库重构方案
- 更新：[domains/meta/analyses/research-paper-wiki-rearchitecture-proposal-2026-04-25.md](domains/meta/analyses/research-paper-wiki-rearchitecture-proposal-2026-04-25.md)、[index.md](index.md)
- 关键记忆：现有 wiki 保留 domain 分层，但转向论文优先结构，加入结构化论文元数据、证据等级、原子 claim、methods、datasets、tasks、metrics 和 comparison 页。
- 未闭合问题：如果用户同意，应更新 [../AGENTS.md](../AGENTS.md)。

## [2026-04-25] schema | 论文优先 AGENTS.md
- 更新：[../AGENTS.md](../AGENTS.md)、[../CLAUDE.md](../CLAUDE.md)、[index.md](index.md)、重构方案页。
- 关键记忆：`AGENTS.md` 现在把仓库定义为科研论文知识库，包含 paper pages、结构化书目信息、证据等级、原子 claim、methods、datasets、tasks、metrics、comparisons 和论文优先工作流。
- 未闭合问题：把已有 domain 从旧 `sources/` 论文页迁移到新 `papers/` schema。

## [2026-04-25] organize | 迁移研究 domain 到 papers schema
- 更新：6 篇研究论文迁移到 `papers/` 规范页；旧 `sources/` 页面保留为 `superseded` 跳转页；索引、概念页和主题页更新到新链接。
- 关键记忆：6 篇论文现在都有结构化 frontmatter、证据等级、可复用 claim 和论文原生章节。
- 未闭合问题：多数论文页仍是 `evidence_level: abstract-only`；需要 full-paper 抽取后才能稳定建立 benchmark 表、method 页、dataset 页和 comparison 页。

## [2026-04-25] schema | 中文 Wiki 呈现
- 更新：[../AGENTS.md](../AGENTS.md)、[../CLAUDE.md](../CLAUDE.md)、[index.md](index.md)、[log.md](log.md)
- 关键记忆：`wiki/` 维护层默认用中文呈现；原始论文标题、作者、venue、DOI、arXiv、代码链接、文件路径和 raw 原文保持原语言以保证引用准确。
- 未闭合问题：继续把各 domain 页面正文中文化。

## [2026-04-25] organize | 中文化现有 Wiki 页面
- 更新：`wiki/domains/` 下现有 meta、distillation、outofdistributiondetection、spectrum 页面正文，保留原始论文题名、路径、DOI、arXiv 和代码链接。
- 关键记忆：现有 wiki 维护层已切换为中文呈现；论文页、概念页、主题页、分析页、索引和日志都已中文化。
- 未闭合问题：未来新增页面继续按 `AGENTS.md` 的语言策略用中文维护；raw sources 不翻译。

## [2026-05-05] ingest | PALCAS: Priority-Aware Lane Change Advisory System using Federated RL
- 原始来源：[../raw/sources/2026-04-29-palcas-priority-aware-lane-change-federated-rl.pdf](../raw/sources/2026-04-29-palcas-priority-aware-lane-change-federated-rl.pdf)
- 新建领域：[domains/autonomous-driving/](domains/autonomous-driving/)
- 新建文件：[domains/autonomous-driving/papers/palcas-priority-aware-lane-change-federated-rl.md](domains/autonomous-driving/papers/palcas-priority-aware-lane-change-federated-rl.md)、[domains/autonomous-driving/concepts/federated-reinforcement-learning-autonomous-driving.md](domains/autonomous-driving/concepts/federated-reinforcement-learning-autonomous-driving.md)、[domains/autonomous-driving/tasks/lane-change-decision-making.md](domains/autonomous-driving/tasks/lane-change-decision-making.md)
- 更新：[index.md](index.md)
- 证据等级：full-paper
- 关键记忆：PALCAS 是首个将 Fed-MARL 引入变道决策的工作；PDQN 混合动作空间同时处理离散变道和连续加速度；priority-guided reward 统一强制性和自主性变道行为；60% CAV 渗透率下碰撞率仅 2.45%，MSR 达 93.33%；`autonomous-driving` 成为 wiki 第五个研究领域。
- 未闭合问题：PALCAS 缺乏与现有非联邦 MARL 变道方法的直接比较；真实 CAV 硬件部署可行性未知；联邦学习通信延迟对实时决策的影响未分析。

## [2026-05-05] ingest | Rethinking Long-tailed Dataset Distillation 升级到 full-paper
- 原始来源：[../raw/sources/2025-12-14-rethinking-long-tailed-dataset-distillation.pdf](../raw/sources/2025-12-14-rethinking-long-tailed-dataset-distillation.pdf)
- 更新：[domains/distillation/papers/rethinking-long-tailed-dataset-distillation.md](domains/distillation/papers/rethinking-long-tailed-dataset-distillation.md)、[index.md](index.md)
- 证据等级：abstract-only → full-paper
- 关键记忆：论文从 trajectory matching 转向 statistical alignment 视角；三个核心组件——expert model debiasing、动态 momentum BN recalibration、confidence-guided multi-round initialization——在 CIFAR-100-LT (IF=10) 上超越 DAMED +15.6%；计算效率提升 20 倍且 GPU 内存恒定 3.1GB；IPC=1 极端设置下依然鲁棒（CIFAR-100-LT: 31.8% vs. DAMED 7.8%）；跨架构泛化强（VGG-11 上 64.6% vs. DAMED 29.7%）。
- 未闭合问题：对非 BN 架构（Transformer/LN）的适用性；与 generative/diffusion-based 蒸馏方法的结合；联邦数据集蒸馏场景的实验验证。

## [2026-05-05] ingest | Correspondence Coverage Matters for Multi-Modal Dataset Distillation 升级到 skimmed
- 原始来源：[../raw/sources/2026-03-14-correspondence-coverage-matters-multimodal-dataset-distillation.md](../raw/sources/2026-03-14-correspondence-coverage-matters-multimodal-dataset-distillation.md)
- 更新：[domains/distillation/papers/correspondence-coverage-matters-multimodal-dataset-distillation.md](domains/distillation/papers/correspondence-coverage-matters-multimodal-dataset-distillation.md)、[domains/distillation/topics/multimodal-dataset-distillation.md](domains/distillation/topics/multimodal-dataset-distillation.md)、[domains/distillation/concepts/dataset-distillation.md](domains/distillation/concepts/dataset-distillation.md)、[index.md](index.md)
- 证据等级：abstract-only → skimmed
- 关键记忆：ProCo 三大创新——retrieval-based correspondence consistency metric 刻画跨模态语义覆盖、coverage-aware clustering 选取代表性样本、conditional neural fields 实现 elastic budget-efficacy trade-off；Flickr30K 和 MS-COCO 上 10x 更小预算超越先前方法 15%+；arXiv ID 2505.22793。
- 未闭合问题：缺少 PDF 无法抽取完整实验表和 ablation；与其他同期多模态 DD 方法（Phased Teacher Models、Asynchronous Matching）的直接比较待补充；retrieval backbone 敏感性未量化。

## [2026-05-05] ingest | Targeted Data Protection for Diffusion Model by Matching Training Trajectory 升级到 skimmed
- 原始来源：[../raw/sources/2026-03-14-targeted-data-protection-diffusion-model-training-trajectory.md](../raw/sources/2026-03-14-targeted-data-protection-diffusion-model-training-trajectory.md)
- 更新：[domains/distillation/papers/targeted-data-protection-diffusion-model-training-trajectory.md](domains/distillation/papers/targeted-data-protection-diffusion-model-training-trajectory.md)、[domains/distillation/topics/diffusion-model-data-protection.md](domains/distillation/topics/diffusion-model-data-protection.md)、[domains/distillation/concepts/dataset-distillation.md](domains/distillation/concepts/dataset-distillation.md)、[index.md](index.md)
- 证据等级：abstract-only → skimmed
- 关键记忆：TAFAP 首次将 trajectory matching 从数据集蒸馏迁移到 diffusion 数据保护；完整轨迹对齐（而非单步 snapshot）是实现有效 targeted data protection 的核心；可同时控制 identity 和 visual patterns 双重目标；arXiv ID 2512.10433。
- 未闭合问题：缺少 PDF 无法抽取完整定量实验和 ablation；snapshot vs. trajectory 的保护衰减曲线需定量比较；对 adaptive attack 的鲁棒性未测试；不同 diffusion 架构（SD/SDXL/Flux）的泛化性未知。

## [2026-05-05] ingest | Learning Transferable Negative Prompts for OOD Detection 升级到 full-paper
- 原始来源：[../raw/sources/2024-05-31-learning-transferable-negative-prompts-ood-detection.pdf](../raw/sources/2024-05-31-learning-transferable-negative-prompts-ood-detection.pdf)
- 更新：[domains/outofdistributiondetection/papers/learning-transferable-negative-prompts-ood-detection.md](domains/outofdistributiondetection/papers/learning-transferable-negative-prompts-ood-detection.md)、[domains/outofdistributiondetection/topics/negative-prompt-ood-detection.md](domains/outofdistributiondetection/topics/negative-prompt-ood-detection.md)、[domains/outofdistributiondetection/concepts/out-of-distribution-detection.md](domains/outofdistributiondetection/concepts/out-of-distribution-detection.md)、[index.md](index.md)
- 证据等级：abstract-only → full-paper
- 关键记忆：NegPrompt (CVPR 2024) 提出只用 ID 数据学习可迁移 negative prompts——通过 NIS（instance-level separability）、NPD（prototype diversity）、NND（negative-positive non-coupling）三个损失函数实现；关键发现：仅 ID 数据无法学出类似 ID→OOD 的 large shift，但可以学出跨 OOD 分布稳定的 patterns；可迁移性验证在 4 个 hard OOD 数据集（NINCO、SSB-hard、iNaturalist、Texture）上全面超越 MCM 和 CoOp。
- 未闭合问题：open-vocabulary 能力依赖 CLIP text encoder 的质量；对完全不同于 ImageNet 的 OOD 分布（如医学图像）的泛化性未充分验证。

## [2026-05-05] ingest | Out-of-Distribution Detection with Negative Prompts 升级到 full-paper
- 原始来源：[../raw/sources/2024-01-16-out-of-distribution-detection-with-negative-prompts.pdf](../raw/sources/2024-01-16-out-of-distribution-detection-with-negative-prompts.pdf)
- 更新：[domains/outofdistributiondetection/papers/out-of-distribution-detection-with-negative-prompts.md](domains/outofdistributiondetection/papers/out-of-distribution-detection-with-negative-prompts.md)、[domains/outofdistributiondetection/topics/negative-prompt-ood-detection.md](domains/outofdistributiondetection/topics/negative-prompt-ood-detection.md)、[domains/outofdistributiondetection/concepts/out-of-distribution-detection.md](domains/outofdistributiondetection/concepts/out-of-distribution-detection.md)、[index.md](index.md)
- 证据等级：abstract-only → full-paper
- 关键记忆：LSN (ICLR 2024) 提出 class-specific negative prompts + semantic orthogonality loss——每个类学习专属 complementary negative prompt（而非 global negative prompt）；核心发现表 5：positive 和 negative prompt learning 存在根本差异——positive 需要更多 prompt (8 vs 2)、更长训练 (25 epochs vs 5)、受益于多样性正则化，negative 则需要单独学习、语义正交性约束；ImageNet-1K 上 AUROC 95.12%（vs. MCM 86.05%），FPR95 降至 25.65%（vs. MCM 63.88%）。
- 未闭合问题：class-specific negative prompts 的可迁移性（在未见类上的表现）；与 NegPrompt transferable approach 的最优融合策略；对更大类别空间（ImageNet-21K）的扩展性。

## [2026-05-05] ingest | Topological Machine Learning Unveils Hidden Reaction Pathways 升级到 full-paper
- 原始来源：[../raw/sources/2025-11-28-topological-machine-learning-nanocrystal-synthesis.pdf](../raw/sources/2025-11-28-topological-machine-learning-nanocrystal-synthesis.pdf)
- 更新：[domains/spectrum/papers/topological-machine-learning-nanocrystal-synthesis.md](domains/spectrum/papers/topological-machine-learning-nanocrystal-synthesis.md)、[domains/spectrum/topics/spectrum-based-reaction-pathway-discovery.md](domains/spectrum/topics/spectrum-based-reaction-pathway-discovery.md)、[domains/spectrum/concepts/spectroscopic-manifold-learning.md](domains/spectrum/concepts/spectroscopic-manifold-learning.md)、[index.md](index.md)
- 证据等级：abstract-only → full-paper
- 关键记忆：JACS 2025 论文用 transformer-augmented UMAP 从 UV-vis 光谱中推断 InAs 纳米晶合成的完整反应路径；physics-informed t=0 边界条件约束增强（生成 204 个增强样本）；多个独立训练的 transformer 产生拓扑等价 UMAP 流形——验证方法稳健性；成功识别此前未报道的亚稳态中间体（P-550 和 P-610）；UMAP 超参数选择：n_neighbors > 1% 数据量、min_dist 0.1-0.3。
- 未闭合问题：新识别的中间体需要独立实验验证（TEM/XRD/mass spec）；跨材料系统（InP、CdSe、PbS）和跨光谱模态（IR、Raman、XRD）的泛化性未测试；能否从拓扑流形中提取定量动力学参数（速率常数、活化能）而不仅是定性路径描述。

## [2026-05-05] ingest | 联邦学习 batch ingest — 12 篇新论文，新建 federated-learning 域
- 原始来源：[../raw/inbox/联邦/](../raw/inbox/联邦/) 下 12 篇 PDF（2604.27598v1 至 2605.00762v1；2604.27118v1 PALCAS 先前已处理）。
- 新建域：[domains/federated-learning/](domains/federated-learning/)
- 新建文件：12 篇 paper pages + 1 篇 concept page [domains/federated-learning/concepts/federated-learning.md](domains/federated-learning/concepts/federated-learning.md)
- 更新：[index.md](index.md)
- 证据等级：全部 skimmed（基于摘要和前 5 页 PDF 提取）
- 关键记忆：
  - 联邦学习覆盖了 6 个子方向：隐私增强 (DP/HE)、聚合权重优化 (FedHAW hypergradient)、多作业调度 (FedACT)、个性化-泛化权衡 (FedKPer)、联邦蒸馏 (FedHD ICML 2026)、联邦遗忘 (EASE Anchor Principle)。
  - 交叉连接：FedHD 连接 `distillation` 域（联邦 DD），EASE 连接 `distillation` 域（多模态 cross-modal control），PALCAS 连接 `autonomous-driving` 域（FedRL）。
  - 关键论文：FedACT (IPDPS 2026) JCT -8.3× +44.5% accuracy；FedHD (ICML 2026) 高斯混合 WSI 蒸馏；EASE Anchor Principle 三残差锚闭合；FSCLB sketch 通信降 90%+。
  - AgentReputation 为非 FL 论文（去中心化 agent 声誉框架），归入 federated-learning 域因其去中心化架构。
  - Federated Weather Modeling 为极简概念论文（定义性，无实验）。
- 后续 topic 合成：[domains/federated-learning/topics/federated-distillation-and-unlearning.md](domains/federated-learning/topics/federated-distillation-and-unlearning.md)（FedHD + EASE 的统一视角，cross-modal coupling 的双重角色）、[domains/federated-learning/topics/fl-heterogeneity-and-optimization.md](domains/federated-learning/topics/fl-heterogeneity-and-optimization.md)（聚合/任务/系统三层异质性统一分析，FedHAW + FedKPer + FedACT + FedHarmony）。
- 未闭合问题：12 篇论文均为 skimmed 级别（仅摘要+前5页），需升级到 full-paper 以获得完整实验表和方法细节；`federated-learning` 域缺少 method/dataset/task/comparison 页面；12 篇论文中 4 篇没有明确 venue（arXiv preprint）；FedHD (ICML)、FedACT (IPDPS)、FedKPer (ICIP) 为已接受论文，优先级更高。

## [2026-05-05] analysis | Wiki Needle Tests 捞针测试集
- 新建：[domains/meta/analyses/needle-tests-2026-05-05.md](domains/meta/analyses/needle-tests-2026-05-05.md)
- 更新：[index.md](index.md)
- 关键记忆：15 道捞针测试题，覆盖 5 个领域 × 4 类题型——事实检索（Q1/Q4/Q6/Q8/Q10）、跨论文比较（Q2/Q4/Q11/Q13）、机制理解（Q3/Q5/Q9）、分类判断（Q7/Q12/Q14/Q15）。包括 1 道孤儿检测题（Q15）用于追踪未被 topic 页覆盖的论文。
- 未闭合问题：测试集尚未正式执行；每次 major ingest 后应随机选 3-5 题运行并记录通过率。

## [2026-05-05] schema | Experiments/Results 区段最低标准
- 更新：[../AGENTS.md](../AGENTS.md)
- 关键记忆：Paper Page Template 新增 Experiments/Results 最低标准——(1) 每个数据集附带规模和切分，(2) 每个 baseline 按名字列出，(3) 训练超参数，(4) 每个主要 claim 至少一个具体数字，(5) ablation delta 必须记录，(6) anti-pattern 清单（"显著优于 SOTA"、空 Results 区段等）。Minimum acceptable ingest 新增"至少一个具体数字"硬性要求。
- 未闭合问题：现有 12 篇 federated-learning 论文页（全 skimmed 批次摄入）的 Results 区段需要回填定量数据。

## [2026-05-05] organize | inbox 清理 — 创建 raw/processed/ 归档
- 新建：[../raw/processed/](../raw/processed/)
- 更新：[../AGENTS.md](../AGENTS.md)、[index.md](index.md)
- 关键记忆：`raw/inbox/` 中 7 个已摄入文件移入 `raw/processed/` 归档。工作流更新为: inbox → sources (规范副本) → processed (原始文件归档)。`raw/inbox/` 现在为空，可接受新论文。
- 未闭合问题：无。

## [2026-05-05] lint | Experiments/Results 回填 — federated-learning 域 6 篇论文升级到 full-paper
- 依据：[../AGENTS.md](../AGENTS.md) 新增的 Experiments/Results 最低标准。
- 升级论文：FedHD、FedKPer、FedHarmony、FedHAW、Privacy-Preserving FL (DP/HE)、FedACT。
- 修改：重写 `## Experiments` 和 `## Results` 区段，补全数据集规模与切分、训练超参数、baseline 列表、ablation delta、所有主要 claim 的定量数字。
- 关键数字回填：
  - **FedHD**：CAM16 Avg Acc 91.2%/MCC 80.6（vs. FedWSIDD 88.7%/75.3）；Ablation Table 2（FDD→GMA→O2O→CBF 累加增益）；MIA privacy AUC 全面降低。
  - **FedKPer**：BloodMNIST global Acc 64.5%（FedAvg 40.9%，+23.6%）；OrganCMNIST 66.0%（FedAvg 56.8%）；11 baselines × 3 数据集 × 7 指标完整矩阵；500s 时比 FedAvg 提升 38.8%。
  - **FedHarmony**：FLAIR mAP 51.0%（FedProx 39.6%，+11.4）；COCO-80 mAP 71.4%；VOC2007 mAP 86.9%；8 baselines × 3 数据集 × 8 指标完整矩阵；B-OPT 节省 28-32% 训练时间。
  - **FedHAW**：MNIST pₑ=0.2 86.70%（FedLAW 83.26%）；CIFAR-10 pₑ=0.2 67.47%；Dogs pₑ=0.2 87.34%；FedProx+HAW > FedProx 在所有轮次。
  - **Privacy-Preserving FL**：NN FedAvg 37,771s / DP 62,721s / HE 63,713s；cML AUC 0.67；CKKS 多项式度 8192；NN 加密更新 5.4MB；LR 比 NN 对 DP 噪声更敏感。
  - **FedACT**：Group A LeNet IID 3.92 min（vs. MJFL 5.18）；VGG non-IID 286.4 min（vs. Random 2471.4，-8.6×）；Group B AlexNet IID 13.58 min；准确率最高 +44.5%。
- 证据等级变更：6 篇 skimmed → full-paper。
- 未闭合问题：剩余 6 篇 federated-learning 论文（FedHarmony 外的 5 篇 + AgentReputation、FedWeather、ITS Intrusion、FSCLB、Meritocratic Fairness）仍需回填；其中 AgentReputation 和 FedWeather 为非标准 FL 论文，定量实验回填优先级较低。

## [2026-05-05] lint | Auto Fix QA — federated-learning 域局部修正
- 依据：Auto Fix.md 五项检测任务（事实一致性、信息完整度、分类合理性、结构规范、捞针测试）。
- 修改：
  - [agentreputation](domains/federated-learning/papers/agentreputation-decentralized-agentic-ai-reputation.md)：`label: federated-learning` → `decentralized-ai`；添加分类说明 callout。
  - [federated-weather-modeling](domains/federated-learning/papers/federated-weather-modeling-sensor-data.md)：`status: active` → `seed`；Provenance 新增升级路径说明。
  - [meritocratic-fairness](domains/federated-learning/papers/meritocratic-fairness-budgeted-bandits-shapley.md) ↔ [fsclb](domains/federated-learning/papers/federated-sketch-contextual-linear-bandits-fsclb.md)：增强 bandit 双向对比链接（维度：setting / regret / FL 应用角色）。
  - [privacy-preserving-fl](domains/federated-learning/papers/privacy-preserving-fl-dp-he-cardiovascular.md) ↔ [intrusion-detection-its](domains/federated-learning/papers/intrusion-detection-intelligent-transport-systems-fl.md)：新增安全/隐私方向双向链接。
- 未闭合问题：6 篇论文的 Results 区段仍缺乏定量数字（需从 PDF 全文中提取）；跨论文 comparison 页仍未创建（bandit 对比、安全方向对比）。

## [2026-05-05] ingest | Fair Dataset Distillation via Cross-Group Barycenter Alignment (COBRA)
- 原始来源：[../raw/sources/2026-05-04-fair-dataset-distillation-cobra.pdf](../raw/sources/2026-05-04-fair-dataset-distillation-cobra.pdf)
- 新建文件：[domains/distillation/papers/fair-dataset-distillation-cobra.md](domains/distillation/papers/fair-dataset-distillation-cobra.md)、[domains/distillation/topics/fair-dataset-distillation.md](domains/distillation/topics/fair-dataset-distillation.md)
- 更新：[domains/distillation/concepts/dataset-distillation.md](domains/distillation/concepts/dataset-distillation.md)、[index.md](index.md)
- 证据等级：full-paper
- 关键记忆：COBRA (ICML 2026) 证明 DD 偏差放大 = 群体不平衡 × 表示分离交互；uniform-weight barycenter alignment 在 7 个有偏基准上全面降低 EOD（CIFAR10-S DM IPC=10: 56.25→20.18，Acc +7.3%）；兼容 DC/DM/CAFE/IDC/MTT 五类框架；对群体标签噪声 (up to 50%) 和部分标签可用 (低至 5%) 有鲁棒性；计算开销在实际两组场景下仅 1.3-1.6×。COBRA 与 FairDD (NeurIPS 2025) 直接竞争，在绝大多数设置中超越。`distillation` 域现在覆盖 5 维：不平衡（long-tailed）、多模态（cross-modal correspondence）、数据保护（diffusion）、轨迹匹配（MTT）、公平性（barycenter alignment）。
- 未闭合问题：非视觉模态泛化；多个相交敏感属性扩展；联邦 DD 公平性；与 generative/diffusion-based 蒸馏方法结合。

## [2026-05-05] ingest | Distilling Long-CoT Reasoning through Collaborative Step-wise Multi-Teacher Decoding (CoRD)
- 原始来源：[../raw/sources/2026-04-26-distilling-long-cot-reasoning-cord.pdf](../raw/sources/2026-04-26-distilling-long-cot-reasoning-cord.pdf)
- 新建领域：[domains/llm-reasoning/](domains/llm-reasoning/)
- 新建文件：[domains/llm-reasoning/papers/distilling-long-cot-reasoning-cord.md](domains/llm-reasoning/papers/distilling-long-cot-reasoning-cord.md)、[domains/llm-reasoning/concepts/long-cot-reasoning-distillation.md](domains/llm-reasoning/concepts/long-cot-reasoning-distillation.md)
- 更新：[index.md](index.md)
- 证据等级：full-paper
- 关键记忆：CoRD (KAIST/UNIST) 将 Long-CoT 推理蒸馏重新定义为逐步协同解码——3 核心组件：prompt-guided step segmentation + predictive perplexity 步骤选择 + beam search；异构 teacher (R1-Qwen-32B + QwQ-32B + Phi4-Reasoning-Plus) 下 AIME24 Pass@1 79.6%，超越所有单个 teacher；在 AIME25 上 70.2% 同样超越所有 teacher；域外泛化强 (TaTQA 95.2%, PubMedQA 91.8%)；对抗 Curation/S1/LIMO post-hoc 范式——即使翻倍计算预算仍不如 CoRD；逐步协同解码 288.7s/题 vs. MCTS 589.2s。`llm-reasoning` 成为 wiki 第 7 个研究领域，与 `distillation` 域明确区分（CoRD = 模型级知识蒸馏，数据集蒸馏 = 数据级压缩）。
- 未闭合问题：多语言推理泛化；5+ teacher 池扩展；DPO/RL 超越 SFT-only；代码生成/定理证明泛化；小型专用 verifier 替代全量 meta-prover。

## [2026-05-08] ingest | One-shot Federated Learning via Synthetic Distiller-Distillate Communication (FedSD2C)
- 原始来源：[../raw/sources/2024-12-10-one-shot-fl-synthetic-distiller-distillate-communication.pdf](../raw/sources/2024-12-10-one-shot-fl-synthetic-distiller-distillate-communication.pdf)
- 新建文件：[domains/federated-learning/papers/fedsd2c-one-shot-fl-distiller-distillate.md](domains/federated-learning/papers/fedsd2c-one-shot-fl-distiller-distillate.md)
- 更新：[domains/federated-learning/topics/federated-distillation-and-unlearning.md](domains/federated-learning/topics/federated-distillation-and-unlearning.md)、[index.md](index.md)
- 证据等级：full-paper
- 关键记忆：FedSD2C (NeurIPS 2024, NUS/Beihang) 提出端到端合成蒸馏物通信替代 DFKD 的模型→数据逆向生成——V-information Core-Set + Fourier 振幅扰动 + 预训练 VAE latent 蒸馏；Tiny-ImageNet ResNet-18 上 2.6× Co-Boosting (26.83 vs. 10.29)，ImageNette 上 1.3× best baseline (50.68 vs. 44.95)，OpenImage 上 1.7× best baseline (23.00 vs. 13.59)；通信成本仅为 model-sharing 的 4% (0.5MB vs. 44MB)；Fourier 扰动平衡隐私与性能——相近 PSNR/SSIM 下准确率显著优于 Laplace/Gaussian 噪声和 FedMix。`federated-learning` 域现有 13 篇论文，one-shot FL 蒸馏与 FedHD (多轮 FL 蒸馏) 形成互补——前者关注单轮通信效率+隐私，后者关注多轮 WSI 特征对齐。
- 未闭合问题：非视觉模态泛化；超大规模 cross-device (n>1000) 验证；DP 形式化保证与 Fourier 扰动的结合；distillate 增量更新策略；adversarial client 鲁棒性。

## [2026-05-16] analysis | LLMwiki 优化评估——定量与定性分析
- 新建：[domains/meta/analyses/autoresearch-optimization-evaluation-2026-05-16.md](domains/meta/analyses/autoresearch-optimization-evaluation-2026-05-16.md)
- 首次执行捞针测试：6/15 题执行，5/6 完全通过 + 1 部分通过 = 100% 可回答率
- 关键发现：
  - 量化基线：22 篇论文（14 full-paper / 8 skimmed / 0 abstract-only），7 领域，8 topic 页，21 原子 claim
  - 三组定性案例——(1) OOD negative prompt 方法族从孤立论文到比较体系，(2) 长尾蒸馏从 abstract-only 到完整定量证据，(3) 联邦蒸馏与遗忘的跨域统一视角
  - 核心短板：0 个 comparison 页、method/dataset/metric 页缺失、6 篇孤儿论文、8 篇 skimmed 论文实验数据不完整
  - 达标率：具体数字 100%、baseline gap 90.9%、ablation delta 85.7%
  - 优化效率：abstract-only 清零、孤儿率从 100%→27.3%、论文平均定量数字 0.5→4.2（+740%）
- 未闭合问题：comparison 页创建（最高优先级）；孤儿论文 topic 索引；skimmed→full-paper 升级（EASE、ProCo）；捞针测试自动化集成

## [2026-05-20] analysis | Autoresearch 功能模块汇报
- 新建：[domains/meta/analyses/autoresearch-function-status-report-2026-05-20.md](domains/meta/analyses/autoresearch-function-status-report-2026-05-20.md)
- 按 6 大功能模块（ingest/query/compare/lint/analysis/schema）组织现状汇报
- 每模块含：执行次数、成熟度评级、具体案例、定量指标、定性评价、不足
- 附汇报策略建议（10-15 分钟结构、核心亮点选择、关键技巧）
- 关键数字回顾：22 篇论文 7 领域、63.6% full-paper、abstract-only 清零、捞针 100% 可回答率、定量数字增幅 +740%
- 未闭合问题：comparison 页（0→至少2）、自动化 lint、skimmed→full-paper 升级管线
