# SGG 研究 Idea Cards — 2026-06-10

> 基于 wiki（126 篇论文）、历史讨论记录和项目约束生成。
> 聚焦：生成式 SGG 的长尾偏差诊断 + 对分类与生成双范式有效的特征级增强。
> 已被拒方向的避免：逐一说明差异化。

---

## IDEA-01: 生成式 SGG 长尾偏差诊断报告

### 核心假设
FlowSG、DiScGraph、Diff-VRD 等生成式 SGG 方法虽然在不同指标上超越分类方法，但它们的 **Head/Body/Tail 分解性能不明**。生成式框架（迭代去噪/流匹配）可能天然缓解或继承了与分类方法同样程度的长尾偏差。

### 锚定来源
- **FlowSG**（wiki页面）：无 H/B/T breakdown，仅有一个模糊说法"marginal initialization 在长尾谓词识别上优势明显"但无量化证据
- **DiScGraph**（wiki页面）：侧重无条件 SG 生成和 SG→Image，未报告 H/B/T 分解的 SGG 指标
- **Diff-VRD**（wiki页面）：侧重开集多样性（T2I Retrieval 超越 GT），未分析其在闭集 SGG 上的 H/B/T 表现
- **IS-GGT**（wiki页面）：宣称"无去偏机制但有竞争力"，但零样本优势不等于长尾优势

### 拟解决痛点
**具体痛点：** 生成式 SGG（Flow Matching / Discrete Diffusion / Continuous Diffusion）在长尾谓词上的表现目前完全未知。现有全部去偏工作（TDE→CFA→RcSGG→CAModule→SBG）均基于分类范式，不清楚生成式 SGG 是否继承了相同偏差，或者部分缓解了偏差。

### 为什么现在值得做
- FlowSG（arXiv 2026.04）刚发布，是首个系统性将流匹配引入 SGG 的工作
- DiScGraph（arXiv 2026.05）刚发布，把离散扩散引入 SGG  
- 两个方法互为补充但均没有长尾分析
- 用户正处在"要不要在生成式方向上做文章"的决策点——诊断是第一步
- 即使不做新方法，一篇诊断报告论文（如 SGG community 的"Demystifying Long-Tail in Generative SGG"）就能填补空白

### 拟解决机制
H/B/T 分解实验协议：
1. 按 VG/PSG 的谓词频率分三档：Head（top-20%）、Body（mid-60%）、Tail（bottom-20%）
2. 对 FlowSG、DiScGraph、Diff-VRD 逐一报告每个区间的 R@K、mR@K、zR@K
3. 对比经典分类去偏方法（RcSGG、CFA、SBG）在相同协议下的对应数字
4. 额外分析：生成式方法的"边际初始化"（FlowSG 的 marginal initialization）是否对不同 frequeny 区间有差异化影响

### 最小验证实验
| 项目 | 内容 |
|------|------|
| 数据集 | VG150（SGDET）、PSG（SGDET） |
| 基线 | FlowSG、DiScGraph、Diff-VRD、RcSGG（分类 SOTA）、CFA（分类增强 SOTA） |
| 指标 | H/B/T 的 R@50/100、mR@50/100、zR@50/100 |
| 工具 | 现有开源检测器 + 论文提供的推理代码即可完成，无需重新训练 |

### 预期指标变化
不是一个干预实验，而是一个诊断实验。预期发现可能是：
- **假设 A**：生成式 SGG 的 H/B/T gap 小于分类方法（说明迭代去噪天然缓解偏差）
- **假设 B**：生成式 SGG 的 H/B/T gap 等于或大于分类方法（说明偏差嵌入在数据/特征空间，不因范式改变）
- **假设 C**：不同生成式方法（流匹配 vs 离散扩散 vs 连续扩散）对偏差的敏感性不同

### 主要风险
- **低风险**：实验只需推理现有模型，无需训练
- **结果可能不显著（所有方法 H/B/T 模式相同）** → 本身也是重要发现
- **FlowSG 没有开源代码**（论文未提供 code），需要作者复现或邮件请求
- **DiScGraph 部分代码可能未发布**

### 与被拒方向的差异
与所有被拒方向无重叠。这是**诊断工作**，不是方法提出。用户之前被拒的方向都是方法论，诊断报告是独立的、安全的、高影响力的启动点。

---

## IDEA-02: 生成式 SGG 的 Token 级自适应去噪动力学（Token-Wise Adaptive Denoising Dynamics）

### 核心假设
生成式 SGG（FlowSG 的流匹配 / DiScGraph 的离散扩散）对所有 predicate tokens 使用**统一的去噪调度**（相同的 ODE/CTMC 步数、速率矩阵、调度函数）。不同频率的 predicate 在去噪过程中应被不同对待——tail predicate 需要更长的去噪时间、更大的注意力权重或不同的速率参数，因为它们的特征空间更稀疏。

### 锚定来源
- **FlowSG**（wiki页面）：局限中提到"推理开销：多步 ODE 积分仍增加推理成本"，但没有说**不同步数用于不同谓词**
- **DiScGraph**（wiki页面）：使用统一的随机+掩码加噪策略和统一的速率矩阵，没有 predicate 级差异化
- **CFA**（wiki页面）：证明 tail predicate 的特征空间稀疏是核心问题（通过特征增强缓解）
- **RcSGG**（wiki页面）：通过特征空间干预（ARE）纠正偏差——但 ARE 是训练时的 batch 重采样，而非推理时的自适应调度

### 拟解决痛点
**具体痛点：** 所有生成式 SGG 方法对所有谓词使用相同的去噪调度（相同步数、速率常数、加噪策略），浪费了 head predicate 的计算资源，但 tail predicate 又因去噪不足而表现不佳。分类方法可以通过 logit adjustment（TDE/RcSGG）在输出层面纠正偏差，但生成式方法没有对应的推理时偏差纠正机制。

### 为什么现在值得做
- 这是生成式 SGG 独有的机会——分类方法无法做"自适应步数/速率"，因为它们是一次性预测
- FlowSG 的 ODE 积分和 DiScGraph 的 CTMC 都是可分解的（每个 token 可在不同步数后退出）
- 用户已有的 OpenSGG 框架熟悉两阶段范式，但可以低成本接入 FlowSG/DiScGraph 推理代码来做修改

### 拟解决机制
**Token-Wise Adaptive Denoising**：

在 FlowSG 推理时：
1. 对每个 relation token，维护一个**信心/不确定性度量**（去噪过程中的预测熵或 logit margin）
2. 设定一个置信度阈值 τ：当 token 的 max logit 置信度 ≥ τ 且在过去 s 步中稳定，则**提前退出**该 token 的 ODE 积分
3. Head predicate token 通常在早期步即达到高置信度→提前退出→节省计算
4. Tail predicate token 可能一直低置信度→分配更多步数→微调特征空间

在 DiScGraph 推理时：
1. 对每个 predicate token（关系语义 R⁺），使用 predicate 频率作为条件变量调整 CTMC 速率矩阵
2. Tail predicate 的转移速率降低（更慢退化为 mask/噪声），让模型有更多机会修正

两种策略都**不需要重新训练模型**，仅修改推理调度。

### 最小验证实验
| 项目 | 内容 |
|------|------|
| 数据集 | VG150、PSG |
| 基线 | FlowSG（原始推理）、DiScGraph（原始推理） |
| 实现 | 修改 FlowSG 推理：对每步预测添加 entropy-based early exit；修改 DiScGraph 推理：频率条件速率 |
| 指标 | mR@50/100（主要）、R@50/100、平均步数/推理时间 |
| 目标 | 在相同或更少平均步数下，tail predicate 的 recall 提升 |

### 预期指标变化
- **FlowSG**：tail predicate mR@50 提升 1-3 点（estimated），平均步数减少 20-40%
- **DiScGraph**：tail predicate Rare-K-TV 改善 5-10%，R-MMD 改善
- 如果 tail 预设在推理时就分配更多步数，整体推理时间可能持平或略增，但 tail 性能显著改善

### 主要风险
- **中等风险**：tail predicate 的低置信度可能不是"证据不足"而是"数据噪声"——更多的去噪步数可能只是让模型过拟合到错误的模式
- 提前退出需要额外的阈值 τ 调参
- 自适应调度破坏了统一退出的并行性，可能引入额外延迟

### 与被拒方向的差异
- 与 **Tokenization/Hierarchy**（被拒）：那个是生成 token 序列替代分类器；这个是**调整已生成的去噪调度**，不改变 tokenization 方式
- 与 **Calibration-aware debiasing**（被拒）：那个展示校准恶化"不是真问题"；这个的核心是**去噪动力学中的计算资源分配**，不是校准
- 与 **VLM Distillation**（被拒）：不依赖任何 VLM，全部在 FlowSG/DiScGraph 框架内完成

---

## IDEA-03: VQ-Codebook 去偏（VQ-Codebook Debiasing for Generative SGG）

### 核心假设
FlowSG 使用的 VQ-VAE 代码本（64×512）是在全体数据上训练的，导致代码本中 head predicate 对应的 entry 更加密集、区分度更好，而 tail predicate 的 entry 稀疏、区分度差。如果对代码本进行**谓词感知的后处理或重平衡**，可以提升生成式 SGG 的 tail 性能。

### 锚定来源
- **FlowSG**（wiki页面）：使用 64×512 的 VQ-VAE 代码本量化外观和关系；消融显示 32×256 远不如 64×512；代码本设计对性能至关重要，但**没有谓词级的代码本分析**
- **DiScGraph**（wiki页面）：不使用 VQ-VAE，而是直接在离散空间建模——但离散分类变量同样面临类别不平衡问题
- **CFA**（wiki页面，ICCV 2023）：证明 tail 三元组的特征空间在分类方法中稀疏——在 VQ-VAE 空间中同样应该稀疏

### 拟解决痛点
**具体痛点：** VQ-VAE 代码本在构建时是频率无关的（对所有训练样本统一量化），但在 SGG 的长尾数据中，head predicate 的视觉特征在代码本中占据主导：更多 entry 被 head 激活、entry 之间的决策边界更清晰。Tail predicate 的条目嵌入空间稀疏，导致生成式去噪网络（图 Transformer）难以区分不同的 tail predicate。

### 为什么现在值得做
- FlowSG 是首个在 SGG 中使用 VQ-VAE + 流匹配的工作，代码本分析完全空白
- VQ-VAE 代码本操作在视觉生成领域是成熟技术（codebook reset、EMA update、entropy penalty），但在 SGG 中未被探索
- 与分类范式的"特征增强"（CFA）有本质区别：代码本操作是离散空间的嵌入级操作，不是分类器级的 logit 调整

### 拟解决机制
**Predicate-Aware Codebook Regularization**：

1. **Analyze**: 统计每个 predicate 对代码本 entry 的激活频率、激活熵、entry 间距离
2. **Rebalance**: 对 tail predicate 对应的 entry 施加：
   - **Codebook entropy regularization**：提高 tail entry 的选择概率（类似带权重的 codebook loss）
   - **Codebook perturbation**: 用 head predicate entry 的方向性采样来增广 tail entry 的相邻空间
   - **Frequency-normalized codebook update**: EMA 更新时按谓词频率归一化，避免 head 主导 codebook
3. **Evaluate**: 重训练 FlowSG 的 VQ-VAE（保持图去噪器不变，仅更新代码本），比较 H/B/T 指标变化

### 最小验证实验
| 项目 | 内容 |
|------|------|
| 数据集 | VG150、PSG |
| 基线 | FlowSG 原始 VQ-VAE (64×512) |
| 实现 | 修改 FlowSG VQ-VAE 训练：加入 frequency-normalized codebook update、entropy regularization |
| 指标 | 代码本使用率（codebook usage）、势能（perplexity）、H/B/T 的 R@50/mR@50 |
| 分析 | 代码本 entry 之间的质心距离，tail vs head entry 的聚类质量 |

### 预期指标变化
- Tail mR@50 提升 2-4 点（若代码本重平衡有效）
- 代码本 perplexity 从原始 ≈30-40% 提升到 60-80%（更好的 entry 使用率）
- 代码本 entry 间的类间距离均匀化效果

### 主要风险
- **中-高风险**：需要重新训练 FlowSG 的 VQ-VAE，计算成本约 1-2 天 on 4×A100
- 代码本操作可能导致 head predicate 性能下降（类似所有去偏方法的固有权衡）
- FlowSG 的代码本训练已经是最优配置（64×512，消融最强），额外约束可能适得其反

### 与被拒方向的差异
- 与 **Foundation model feature space reshaping**（被拒但"有意思"）：那个是拉伸 CLIP/DINOv2 连续特征空间中的 tail 区域；这个是**离散代码本**的去偏操作，离散空间的 entry 重排是可以度量和控制的过程，不是"有意思但未发展"——它有明确的实验协议和评估指标

---

## IDEA-04: 频率条件流匹配（Frequency-Conditioned Flow for Balanced Generative SGG）

### 核心假设
FlowSG 的流匹配过程中，去噪网络 $v_\theta$ 接收图像条件但**不感知当前正在生成的 predicate 的频率信息**。如果把 predicate 频率（或频率分桶：H/B/T）作为条件变量注入去噪网络，网络可以学到对不同频率的 predicate 采取不同的去噪策略。

### 锚定来源
- **FlowSG**（wiki页面）：消融显示"Marginal 初始化在所有策略中最优……在长尾谓词识别上优势明显"——说明初始化策略对 tail 有影响，暗示有条件化空间
- **FlowSG**（wiki页面）：边缘精炼模式（概率 0.2）：仅生成边保持节点固定——有控制逻辑但无频率引导
- **RcSGG**（wiki页面）：指出评估频率与真实频率的差异是偏差根源，当训练 batch 内类别平衡时可获得贝叶斯最优分类器
- **DiScGraph**（wiki页面）：使用混合随机+掩码加噪策略，但没有 frequency-gating

### 拟解决痛点
**具体痛点：** 去噪网络没有关于"当前正在生成高/中/低频谓词"的信号。对于 tail predicate（训练中很少见），网络倾向于恢复到 head predicate（频繁出现在训练数据中）。频率条件可以给网络提供一个"提示"：现在是一个低频情境，不要退化为高频预测。

### 为什么现在值得做
- 条件流匹配（conditional flow matching）是成熟技术（CFM 论文本就支持类别条件），迁移到 SGG 几乎没有技术障碍
- FlowSG 已有条件机制（图像条件），再加一个频率条件只是增加一条 embedding
- 这是**生成式范式独有的**去偏策略——分类方法无法在"去噪过程"中注入条件，只能在输出层调整

### 拟解决机制
**Frequency-Conditioned Flow Matching**：

1. 将 VG/PSG 的 50/56 个谓词统计频率，计算每个 predicate 的 log-frequency 或 frequency bucket embedding
2. 在 FlowSG 的图去噪器（Graph Transformer）中，增加一个 frequency embedding：拼接到节点/边的 token embedding 中，或通过 adaptive layer norm 注入
3. 训练时：每个 predicate token 的真实频率 embedding 已知
4. 推理时：有三种可能的条件方案：
   - **Uniform**: 所有 predicate 用相同的"median frequency"条件
   - **Predicate-agnostic marginal**: 用数据集整体频率分布作为条件（FlowSG 已用的 marginal initialization）
   - **Adaptive**: 模型自预测每个 predicate 的"预期频率"并从条件中采样

### 最小验证实验
| 项目 | 内容 |
|------|------|
| 数据集 | VG150、PSG |
| 基线 | FlowSG（原始） |
| 实现 | 在 FlowSG 的图 Transformer 中增加 frequency embedding → 重新训练 |
| 指标 | H/B/T 的 mR@50/100（主要）、R@50/100 |
| 消融 | 不同频率条件方案（bucket vs continuous，train-time vs inference-only） |

### 预期指标变化
- mR@50 提升 2-5 点（尤其是在 Tail 区间）
- 预期 R@50 轻微下降（0-3 点）
- 如果效果好的话，FlowSG 的 marginal initialization 优势可以被更精确地替代

### 主要风险
- **高风险**：需要重新训练 FlowSG（500K iterations on 4×A100 ≈ 3-5 天）
- 频率条件如果太强可能导致模型退化为"按频率猜测"而不是真正的视觉推理
- FlowSG 本身的代码未开源，实现成本高

### 与被拒方向的差异
- 与 **Compositional Sparsity**（collapsed）：那个是用"组合覆盖率"替代频率作为独立维度，事实证明共线性。这个是用**频率作为条件变量**注入生成过程，不挑战频率维度本身，只改变策略
- 与 **VLM Distillation**（被拒无歧义关系）：不依赖 VLM 作为 teacher，模型完全在 SGG 范式内

---

## IDEA-05: 生成式 SGG 的不确定性引导步数分配（Uncertainty-Guided Step Allocation for Generative SGG）

### 核心假设
生成式 SGG 所有 predicate 使用 **固定 ODE/CTMC 步数**。但不同 predicate 的不确定性不同：head predicate 早期即收敛，tail predicate 始终振荡。如果根据**每步的预测不确定性**动态分配步数（为高不确定性区域分配更多步数），可以提升 tail 性能而不增加全局开销。

### 锚定来源
- **FlowSG**（wiki页面）"去噪器的提前退出策略（early-exit）" 明确在未来工作中列出，但没有提及这是否可以用于去偏
- **DiScGraph**（wiki页面）局限："离散采样器质量受限，需采样细化策略"
- **SBG**（wiki页面，ECCV 2024）：sample-level 偏置预测——证明每个样本的偏置不同，需要细粒度校正
- **CAModule**（wiki页面，2025）：triplet 级 logit adjustment——证明同一关系类别下不同 triplet 的准确率差异极大（0%-100%）

### 拟解决痛点
**具体痛点：** 固定步数对所有谓词一视同仁，但 tail predicate 需要更多迭代才能去噪到正确的语义空间。分类方法（SBG、CAModule）针对每个样本做 bias prediction，但生成式方法没有对应的"样本级步数分配"机制。

### 为什么现在值得做
- 与 IDEA-02 互补但更简洁：不需要修改去噪网络或 VQ-VAE，**仅修改推理时的 ODE/CTMC 采样策略**
- FlowSG 自己将 early-exit 列为未来工作，但他们的动机是效率，我们加上了**去偏**动机
- 扩散社区的 adaptive step scheduling 有成熟方法（DDIM、DPM-Solver），但从未被用于 SGG

### 拟解决机制
**Uncertainty-Guided Step Allocation**：

1. 定义 predicate 级的不确定性度量 $u_{ij}^{(t)}$ = 每个 predicate 在当前步预测 logits 的**归一化熵**或**max-probability 的倒数**
2. 在去噪过程的每步后，计算所有 predicate token 的 $u^{(t)}$
3. 对每个 predicate token，如果 $u^{(t)}$ 大于阈值 $τ$（预测不确定），则继续去噪
4. 如果 $u^{(t)}$ 连续 s 步小于 $τ_{low}$（高度确定），则自动停止该 token 的去噪（freeze 其状态）
5. 全局最大步数上限设为 T_max（可以小于原始总步数，因为 head 提前退出节省的步数分配给 tail）

### 最小验证实验
| 项目 | 内容 |
|------|------|
| 数据集 | VG150、PSG |
| 基线 | FlowSG 原始推理（50 步 DDIM）、DiScGraph 原始推理 |
| 实现 | 在推理循环中加入 per-token 不确定性检查→决策 freeze/continue |
| 指标 | mR@50/100、平均步数、Tail mR@100 / 步数效率比 |
| 超参 | τ, τ_low, s, T_max 的灵敏度分析 |

### 预期指标变化
- Tail mR@50 提升 1-3 点
- 平均步数减少 15-30%（head 提前退出）
- 推理时间基本不变（head 节省的步数被 tail 消耗）

### 主要风险
- **低-中风险**：不改变训练，只改推理。如果效果不佳可快速放弃
- 不确定性估计可能不准——尾类可能早期就表现出高伪置信度（模型把 tail 预测为 head 并 high confidence）
- 动态退出破坏了 batch 并行性，在 GPU 上可能慢于预期

### 与被拒方向的差异
- 与 **Calibration-aware debiasing**（被拒）：那个研究去偏如何损害校准；这个用**不确定性作为控制信号**调整生成过程，不损害甚至改善校准。且这是生成式独有的机制，不是对分类器的校准检查

---

## IDEA-06: 范式桥接——生成式 SGG 为分类式 SGG 合成无偏数据（Generative SGG as Unbiased Data Synthesizer）

### 核心假设
FlowSG/DiScGraph 等生成式 SGG 模型可以从随机噪声生成场景图。如果控制生成条件（prompt 特定的三数组组成），可以有目的地**合成大量 tail-heavy 的场景图**。这些合成数据可以作为增强数据训练分类 SGG 模型（RcSGG/CFA/SBG），打破"tail 类别数据不足"的瓶颈。

### 锚定来源
- **FlowSG**（wiki页面）：无条件 SG 生成能力强（PSG SGDet R@50=46.3），且支持条件生成（图像条件）
- **DiScGraph**（wiki页面）：无条件 SG 生成超越 DiGress/DiffuseSG 的所有指标；支持 reward-tilted 采样控制生成方向
- **CFA**（wiki页面，ICCV 2023）：tail 类别性能瓶颈是特征空间稀疏，数据增广可以缓解
- **Diff-VRD**（wiki页面）：在 T2I Retrieval 上生成的关系超越了 GT 标注的关系——证明生成式方法可以产生未标注但合理的关系

### 拟解决痛点
**具体痛点：** 所有去偏方法（RcSGG、CFA、SBG、CAModule）都在原始数据进行操作（重采样/重加权/校正），但**不产生新的数据**。长尾问题的根本原因是 tail 类别的训练样本本身就少。没有样本，任何损失的技巧都有上限。

### 为什么现在值得做
- 生成式 SGG 2026 年才有了实用性能（FlowSG、DiScGraph 在 SG任务上达到可比 SOTA）
- 这是两个 SGG 范式（生成 vs 分类）的首次协同——不仅有意义，而且优雅
- FlowSG 和 DiScGraph 都支持条件生成，可以定向合成 tail-heavy 场景图
- 概念简单但实现路径新颖：用生成模型增强分类模型的训练数据

### 拟解决机制
**Generative SGG → Classification SGG Data Augmentation Pipeline**：

1. 从训练集的统计中提取 tail predicate 的"原型"三元组模式（<subject, predicate, object> 组合分布）
2. 使用控制参数（predicate 类型、subject-object 对选择）生成合成场景图：
   - **FlowSG 模式**：用 Frequency-bucket 条件（见 IDEA-04）引导生成更多 tail triplet 的场景图
   - **DiScGraph 模式**：使用 reward-tilted 采样（DiScGraph 已有 CLIP reward），target reward = tail predicate 的比例
3. 将生成的 SG 转换为分类 SGG 的 supervised data：
   - 选择合成图的检测器特征作为伪 GT 特征
   - 或直接用合成的 SG 三元组作为训练标注
4. 在原始数据 + 合成 tail-heavy 数据上训练分类 SGG 模型（RcSGG/CFA baseline）
5. 评估分类范式上的 H/B/T 改善

### 最小验证实验
| 项目 | 内容 |
|------|------|
| 数据集 | VG150（原始） |
| 生成器 | FlowSG（预训练） |
| 分类基线 | Motifs+RcSGG、VCTree+CFA |
| 数据增广策略 | 原始数据 + 10%、30%、50% 合成数据 |
| 指标 | 分类方法的 mR@50/100、R@50/100、Mean（A@K） |
| 控制实验 | 同等量的合成 head-heavy 数据→验证差异来自 tail bias 控制 |

### 预期指标变化
- 分类方法的 tail mR@50 提升 3-6 点
- 可能 R@50 提升 1-2 点（合成数据增加了总数居量）
- 如果合成数据质量高（多样性好），可能超越所有仅基于原始数据的去偏方法

### 主要风险
- **中风险**：合成数据可能有模式坍塌——如果生成器自己就继承了长尾偏差，它合不成 tail-heavy 数据。需要验证生成器在受控条件下的 tail 生成能力
- FlowSG 无开源代码是最主要的实现障碍
- 合成数据与真实数据之间的 domain gap

### 与被拒方向的差异
- 与 **VLM Distillation**（被拒）：那个用 VLM teacher 蒸馏知识到尾模型，是"大模型教小模型"；这个是**用生成式 SGG（同领域）为分类式 SGG 提供数据**，不依赖任何外部 VLM，范式内循环
- 与 **Paradigm shift to generative SGG**（被拒）：不是要取代分类方法，而是让两种范式协同工作
- 与 **Tokenization/Hierarchy**（被拒）：不生成 token 序列替代分类器，而是用生成模型创建分类模型的训练数据

---

## IDEA-07: 约束感知的去偏流匹配——用反事实图约束引导生成（Counterfactual Graph Constraints for Unbiased Flow Matching）

### 核心假设
FlowSG 的流匹配过程生成的场景图整体质量高，但在**稀有组合**（如 "dog-building on"）上的表现差。原因为生成过程中图像条件的偏置引导了常见组合（如 "man-on-beach"）。如果在去噪过程的每步加入一个**反事实图约束**（counterfactual graph constraint）——提示模型不按常见组合推测——可以强制模型关注视觉证据而非统计先验。

### 锚定来源
- **FlowSG**（wiki页面）：图像条件是主要输入方式——但图像条件本身携带偏置（常见组合的图像多）
- **CAGE-SGG**（wiki方法列表中）：反事实图证据（Counterfactual Active Graph Evidence）用于 OV-SGG 验证——首次将反事实图引入 SGG 但用于 OV 场景
- **RcSGG**（wiki页面）：反向因果结构 X→R←Y，发现虚假相关的根源是 feature space 的组织方式——在生成式场景中，虚假相关体现在流匹配的每一步
- **TDE**（wiki页面）：Total Direct Effect 从分类输出中减去间接效应——在生成式 SGG 中，"间接效应"对应统计先验驱动的生成轨迹

### 拟解决痛点
**具体痛点：** FlowSG 的去噪过程每一步都条件于图像和当前带噪图。图像特征偏向了常见组合（因为大多数训练图像包含常见组合），导致生成结果整体偏向 head。TDE 可以在分类后调整输出，但生成式 SGG 的偏置是**嵌入在整个生成轨迹中**，不是一次性的 logit。

### 为什么现在值得做
- 反事实推理（CAGE-SGG，2025）已经在 OV-SGG 验证中证明了有效性
- 反事实图约束从未被用于生成式 SGG 的**去噪过程**中
- 这是 CAGE-SGG vs FlowSG 的自然交汇点——CAGE 在 OV 空间做反事实验证，FlowSG 在生成空间做去噪
- 与分类方法的反事实（TDE）不同：TDE 反事实在**输出层**做，我们反事实在**每步去噪**中做

### 拟解决机制
**Counterfactual Flow Matching**：

1. 在 FlowSG 的每步去噪中，网络输出两个预测：
   - **Factual path**: 正常图像条件 → 正常预测（$p_{fact}$）
   - **Counterfactual path**: 用"混淆图像"（常见组合被替换为稀有组合的图像）替代图像条件 → 反事实预测（$p_{CF}$）
2. 最终 logits = $p_{fact} - \alpha \cdot p_{CF}$（类似 TDE 的减法逻辑，但在每步去做）
3. 或者在训练时加入反事实正则项：鼓励网络在常见组合下**不依赖于图像条件**做出预测（类似反事实数据增广）
4. 反事实无法做到完美——用一个**简化方案**：在去噪过程中随机 mask 部分 head predicate 的图像特征，强制网络利用其他线索

### 最小验证实验
| 项目 | 内容 |
|------|------|
| 数据集 | VG150 |
| 基线 | FlowSG（原始） |
| 简化实现 | 训练时：对 head predicate 的图像条件以概率 p 加入 dropout/masking；推理时：正常推理 |
| 指标 | H/B/T 的 mR@50/100、R@50/100 |
| 消融 | mask 概率 p 的影响、仅在训练 vs 训练+推理都做 |

### 预期指标变化
- 预期 tail mR@50 提升 3-6 点
- 如果 mask 策略选择得当，head R@50 的下降可控制在 2 点以内

### 主要风险
- **高风险**：需要修改 FlowSG 训练流程（图像条件 masking），且可能损害整体生成质量
- 反事实路径难以计算：FlowSG 的图像条件通过交叉注意力注入，masking 不是完美的反事实
- 与 TDE 的类似性可能受到 reviewer 质疑——需要清晰区分"输出层反事实" vs "生成轨迹反事实"

### 与被拒方向的差异
- 与所有被拒方向均不同。这是**生成式去偏**，不是输出层调整、tokenization、或是范式转换。

---

## IDEA-08: 混合范式——用分类启发式检测器初始化生成式去噪过程

### 核心假设
FlowSG 使用高斯噪声初始化边界框、完全 masked 的关系类型。但一个**轻量级分类 SGG 模型**可以提供一个比高斯噪声更好的初始图状态。这个初始图即使很粗糙，也能为生成式去噪提供更好的起点，特别是对于 tail predicate——它们在高斯噪声中难以区分。

### 锚定来源
- **FlowSG**（wiki页面）：初始化方案中比较了四种（Uniform、Absorbing、Masking、Marginal），其中 Marginal 对 tail 最有利。但所有方案都是统计先验，不包括分类模型输出
- **FlowSG**（wiki页面）"未来工作：与检测器端到端联合训练"——说明作者对更好的初始化持开放态度
- **IS-GGT**（wiki页面，CVPR 2023）：图采样阶段用生成式 transformer 选择约 20% 边缘后再分类——证明两阶段可以优势互补
- **SGG-R/3**（wiki页面，2026）：三阶段结构化推理（类别→实例→关系）——证明顺序推理优于单次预测

### 拟解决痛点
**具体痛点：** 生成式 SGG 从完全随机的初始状态开始去噪。对于 tail predicate，在随机噪声中与 head predicate 难以区分（因为所有 predicate 从相同的均匀/边际分布开始）。一个更好的初始化有助于 tail predicate 在早期就进入正确的语义区域。

### 为什么现在值得做
- 混合策略在扩散图像生成中是成熟的（latent diffusion、SDEdit），在 SGG 中未探索
- 用户已有 OpenSGG 框架（包含 Motifs/VCTree/Transformer backbones），可以零成本产生分类初始图
- 分类方法推理快（ms 级），生成式去噪慢（多步 ODE），混合后可以通过精细的搜索策略平衡效率与质量

### 拟解决机制
**Classification → Generation Initialization Pipeline**：

1. 用轻量级分类 SGG（如 Motifs/VCTree）对图像生成**初始场景图** $G_0$
2. 将 $G_0$ 编码为 FlowSG 可消费的格式：转换为 VQ-VAE 代码 + 边界框噪声
3. 以 $G_0$ 而非纯噪声开始 FlowSG 的去噪过程，进行少量精炼步（5-10 步而非 50 步）
4. 关键创新：
   - 对分类初始图中置信度高的 predicate（已得到视觉证据支持），给予更少的去噪步数
   - 对置信度低的 predicate（分类器可能误判），给予更多去噪步数
   - 或反过来：用分类器的**不确定度**来选择哪些 predicate 需要精炼

### 最小验证实验
| 项目 | 内容 |
|------|------|
| 数据集 | VG150 |
| 分类基线 | Motifs（OpenSGG 已实现） |
| 生成基线 | FlowSG（如可获取） |
| 接口 | 将 Motifs 输出转换为 VQ-VAE 初始状态 |
| 指标 | FlowSG 完整推理 vs 分类+FlowSG 精炼的 H/B/T mR@50 |
| 控制 | 仅精炼 top-K 个最低置信度 predicate |

### 预期指标变化
- 用分类初始化后，FlowSG 的 tail mR@50 可能提升 1-3 点（因为分类器提供了不是完全随机的起点）
- 总推理时间可能减少 30-50%（因为只需要 5-10 步去噪而非 50 步）
- head predicate 的性能可能保持不变或轻微下降

### 主要风险
- **高风险**：需要 FlowSG 的代码（未开源）才能实现接口
- 分类初始化可能把偏置"传染"给生成式 SGG——如果分类器已经偏到 head，初始图被污染
- 接口设计复杂：分类模型的输出空间（bounding box + predicate logits）需要映射到 FlowSG 的状态空间（VQVAE tokens + 边界框噪声）

### 与被拒方向的差异
- 与 **Paradigm shift to generative SGG**（被拒）：不是要替换分类范式，而是让两个范式**协同工作**
- 与 **VLM Distillation**（被拒）：不使用 VLM，仅使用用户已有的 SGG 框架
- 与所有其他被拒方向无冗余

---

## 汇总对比表

| ID | 标题 | 范式 | 需要训练？ | 预期 Tail mR@50 提升 | 最大风险 | 独特卖点 |
|----|------