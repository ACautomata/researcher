---
title: CD2: Constrained Dataset Distillation for Few-Shot Class-Incremental Learning
type: paper
domain: distillation
status: active
created: 2026-05-30
updated: 2026-05-30
tags:
  - dataset-distillation
  - few-shot-class-incremental-learning
  - catastrophic-forgetting
  - knowledge-distillation
  - memory-replay
paper:
  title: CD2: Constrained Dataset Distillation for Few-Shot Class-Incremental Learning
  authors:
    - Kexin Bao
    - Daichi Zhang
    - Hansong Zhang
    - Yong Li
    - Yutao Yue
    - Shiming Ge
  year: 2026
  venue: arXiv:2601.08519v1
  arxiv: "2601.08519v1"
  doi: ""
  code: ""
  project: ""
classification:
  label: distillation
  task:
    - few-shot class-incremental learning
    - dataset distillation
  method_family:
    - dataset distillation
    - knowledge distillation
    - memory replay
  modality:
    - image
  datasets:
    - CIFAR-100
    - mini-ImageNet
    - CUB-200-2011
  metrics:
    - accuracy (Top-1)
evidence_level: full-paper
raw_sources:
  - raw/sources/2026-01-15-cd2-constrained-dataset-distillation-fscil-fulltext.txt
related_pages:
  - wiki/domains/distillation/concepts/dataset-distillation.md
  - wiki/domains/distillation/datasets/cifar-100.md
---

## Citation

Kexin Bao, Daichi Zhang, Hansong Zhang, Yong Li, Yutao Yue, and Shiming Ge. CD2: Constrained Dataset Distillation for Few-Shot Class-Incremental Learning. arXiv:2601.08519v1, January 2026. Institute of Information Engineering, Chinese Academy of Sciences; School of Cyber Security, University of Chinese Academy of Sciences; Hong Kong University of Science and Technology (Guangzhou).

## One-Sentence Contribution

首次将数据集蒸馏（Dataset Distillation）引入 Few-Shot Class-Incremental Learning (FSCIL)，提出 CD2 框架：用 DDM（Dataset Distillation Module）合成高度压缩的关键知识记忆样本，用 DCM（Distillation Constraint Module）通过特征保留损失和结构保留损失约束跨会话分布偏移，在 CIFAR-100 上平均准确率达到 68.67%（超过 NC-FSCIL 的 67.50%），在 mini-ImageNet 和 CUB200 上也取得最高平均准确率。

## Problem Setting

**任务定义**：Few-Shot Class-Incremental Learning (FSCIL) 要求模型先在一个拥有充足标注样本的基类会话（base session）上学习大量类别，然后在后续增量会话中以 N-way K-shot 的方式持续学习新类别，同时保留旧类别知识。任意两个会话的标签空间互不相交。评估时，模型需要在当前会话及所有历史会话的测试集上进行分类。

**核心挑战**：灾难性遗忘（catastrophic forgetting）——模型在学习新类别时会覆盖已学知识，尤其在增量会话中每类仅有 K 个样本时更为严重。

**现有方法的问题**：主流方法冻结 backbone 并利用外部记忆（memory）保存旧知识，包括样本回放（sample replay）、原型计算（prototype computing）、生成样本和伪特征存储。但这些方法存在两个缺陷：(1) 记忆构建粗放，混合了判别性关键知识和冗余知识，稀释了关键类别相关信息；(2) 记忆中的数据与增量会话新数据之间存在分布差异，将它们同等对待会导致旧类别的协变量偏移（covariate shift）。

**本文动机**：借鉴数据集蒸馏（DD）获取高度压缩且富含信息的合成样本，同时借鉴知识蒸馏（KD）的思想约束跨会话分布偏移。

## Method

CD2 框架包含两个核心模块和一个两阶段训练流程。

### 整体架构

- **Backbone**: ResNet12（CIFAR-100 和 mini-ImageNet，无预训练）或 ResNet18（CUB200，ImageNet 预训练），增量会话中冻结。
- **分类器**: 三层 MLP 块 + 全连接分类层，增量会话中微调。
- **Memory M(t)**: 存放由 DDM 合成的数据，随会话推进逐步累积。

### 数据集蒸馏模块 (DDM: Dataset Distillation Module)

**目的**：从每一类中选择和合成最具判别性的关键知识样本，替代粗糙的样本回放或原型平均。

**具体步骤**：
1. 从当前会话数据集 D(t) 中每类随机选取 K 个样本初始化合成集 D_S(t)。
2. 冻结模型参数，仅更新合成集 D_S(t)。
3. 使用最大均值差异（Maximum Mean Discrepancy, MMD）按类别估计合成集与真实数据的分布距离，每一类单独优化：

   L_DDM = sup(D_S(t)(y_m=c) - D(t)(y_i=c)) = (1/K * sum(phi(x_m)) - 1/|D(t)(y_i=c)| * sum(phi(x_i)))^2

   其中 c 为类别标签，phi 为模型映射函数。

4. 为减少训练开销，从 D(t) 中采样子集 D_R(t) 替代完整数据集参与合成。
5. 合成完成后，将 D_S(t) 加入记忆 M(t+1) 供后续增量会话使用。

**关键特性**：
- 合成的样本能聚合同类样本的互补信息，突出关键知识，弱化冗余信息和离群点偏差。
- 因难以从合成样本逆向恢复原始数据，具有一定隐私保护性。

### 蒸馏约束模块 (DCM: Distillation Constraint Module)

**目的**：在增量会话训练时，约束记忆数据与新数据之间的分布偏移，使旧知识传递更稳定、灵活。

DCM 由两个损失函数组成：

**1. 特征保留损失 (Feature Retention Loss, L_FR)**：
- 保证记忆合成样本在前一模型和当前模型之间的输出向量一致性。
- 约束输出向量前 C 个维度（对应旧类别数）保持一致：

  L_FR = (1/|M(t)|) * sum(|v_m^(t-1) - v_m^(t)[:C]|)

  其中 v_m^(t-1) = phi_c^(t-1)(f_m), v_m^(t) = phi_c^(t)(f_m)。

- L_FR 约束位置信息，维持知识传递的连贯性和稳定性。

**2. 结构保留损失 (Structure Retention Loss, L_SR)**：
- 受 Relational Knowledge Distillation (RKD) 启发，保证记忆合成样本在特征空间中的结构关系在新旧模型间保持一致。
- 基于线性变换约束：

  L_SR = (1/|M(t)|) * sum(|P^(t-1) - P^(t)[:C]|)

  其中 P^(t) = v_m * V^T, V = {phi_c^(t)(f_m) | (x_m, y_m) in M(t)}。

- L_SR 约束结构信息，赋予模型在处理新数据时更多灵活性。

**总体 DCM 损失**：

L_DCM = alpha * L_SR + beta * L_FR

其中 alpha 自适应调节：alpha = ln((-50 / |sum_{i=0}^t C(i)|)^3 + 2)，beta = 0.1（固定）。

SR 损失和 FR 损失双约束同时满足稳定性与灵活性的需求，减少协变量偏移。

### 两阶段训练流程

**基类会话 (t=0)**：
1. 在 D(0) 上联合训练 backbone 和分类器，最小化交叉熵损失。
2. 训练完成后，用 DDM 生成合成集 D_S(0) 并放入记忆 M(1)。

**增量会话 (t>0)**：
1. 冻结 backbone，在 D(t) 和 M(t) 上微调分类器。
2. 总损失：L_i = L_gce + L_DCM = L_gce + alpha * L_SR + beta * L_FR。
3. 全局分类损失 L_gce 对当前数据 D(t) 和记忆数据 M(t) 均计算交叉熵。
4. 训练完成后，用 DDM 从 D(t) 生成合成集 D_S(t) 并加入 M(t+1)。

## Experiments

### 数据集

| 数据集 | 总类别数 | 基类数 | 增量类别数 | 增量会话数 | 增量设置 | 基类每类样本数 |
|--------|---------|-------|-----------|-----------|---------|-------------|
| CIFAR-100 | 100 | 60 | 40 | 8 | 5-way 5-shot | 500 |
| mini-ImageNet | 100 | 60 | 40 | 8 | 5-way 5-shot | 500 |
| CUB-200-2011 | 200 | 100 | 100 | 10 | 10-way 5-shot | not reported in the source |

- CIFAR-100: 32x32 图像，100 类。
- mini-ImageNet: 84x84 图像，100 类（ImageNet 子集）。
- CUB-200-2011: 鸟类细粒度分类，200 类。

### 对比方法（Baselines）

本论文与以下方法进行比较：

**类增量学习（CIL）方法（适配 FSCIL 设置）**：
- iCaRL (Rebuffi et al., 2017) — 增量分类器与表征学习
- EEIL (Castro et al., 2018) — 端到端增量学习

**FSCIL 方法**：
- SoftNet (Kang et al., 2023a) — 软子网络
- MCNet (Ji et al., 2023) — 记忆补全网络
- GKEAL (Zhuang et al., 2023) — 高斯核嵌入分析学习
- FACT (Zhou et al., 2022b) — 前向兼容 FSCIL
- C-FSCIL (Hersche et al., 2022) — 约束 FSCIL
- MICS (Kim et al., 2024) — 中点插值紧凑分离表征
- ALICE (Peng et al., 2022) — 开放集视角的 FSCIL
- CABD (Zhao et al., 2023b) — 类别感知双边蒸馏
- OrCo (Ahmed et al., 2024) — 正交与对比 FSCIL
- WaRP (Kim et al., 2023) — 权重空间旋转
- NC-FSCIL (Yang et al., 2023b) — 神经坍缩启发的特征-分类器对齐
- Revisting-FSCIL (Tang et al., 2024) — 重思 FSCIL

共 14 个 baseline 方法（2 个 CIL 适配 + 12 个 FSCIL 专用）。

### 训练配置

**架构**：
- Backbone: ResNet12（CIFAR-100, mini-ImageNet，无预训练）；ResNet18（CUB200，ImageNet 预训练）
- 分类器: 三层 MLP + 全连接层

**优化器**: SGD with momentum（momentum 具体值 not reported in the source）

**学习率**：
- 基类会话: lr = 0.25（CIFAR-100, mini-ImageNet）；0.01（CUB200）
- 增量会话: lr = 0.25（CIFAR-100, mini-ImageNet）；0.001（CUB200）
- DDM 合成: lr = 0.2

**学习率调度**: Cosine annealing

**训练轮次**：
- 基类会话: 100-200 epochs
- 增量会话: 100-300 iterations
- DDM 合成: 1000 iterations

**批大小 (batch size)**: not reported in the source

**数据增强**: random resizing, random flipping, Mixup, CutMix

**超参数**: beta = 0.1, K = 2（每类合成样本数），alpha 按公式自适应计算

**硬件**: not reported in the source

### 评估协议

- 在每次增量会话结束后，在当前会话及所有历史会话的测试集上评估 Top-1 准确率。
- 报告每个会话的准确率、所有会话的平均准确率（Average accuracy），以及 CD2 相对于其他方法的平均提升（Average improvement）。
- 评估覆盖所有 9 个会话（CIFAR-100/mini-ImageNet: 0-8）或 11 个会话（CUB200: 0-10）。

### 消融实验

在 CIFAR-100 上进行了以下消融：

1. **记忆策略对比**：原型计算 vs. DDM（以 K=2 合成样本）
2. **DCM 消融**：不使用 DCM 损失 vs. 仅 SR 损失 vs. 仅 FR 损失 vs. SR+FR 联合
3. **合成样本数 K 的影响**: K = 1, 2, 3, 4, 5
4. **t-SNE 可视化**：真实样本与合成样本的特征分布

## Results

### CIFAR-100 主结果（Table 1）

CD2 在 CIFAR-100 上的逐会话准确率：

| 会话 | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|------|---|---|---|---|---|---|---|---|---|
| CD2 (Ours) | 83.32 | 79.42 | 74.96 | 70.33 | 67.28 | 64.21 | 61.35 | 59.81 | 57.36 |

CD2 平均准确率: **68.67%**。

最强 baseline 对比：

| 方法 | 平均准确率 (%) | 与 CD2 差距 |
|------|---------------|------------|
| CD2 (Ours) | 68.67 | - |
| NC-FSCIL | 67.50 | +1.17 |
| Revisting-FSCIL | 67.02 | +1.65 |
| CABD | 66.14 | +2.53 |
| WaRP | 65.82 | +2.85 |
| MICS | 63.62 | +5.05 |
| ALICE | 63.21 | +5.46 |
| FACT | 62.24 | +6.43 |
| OrCo | 62.11 | +6.56 |
| C-FSCIL | 61.64 | +7.03 |
| GKEAL | 61.35 | +7.32 |
| MCNet | 60.40 | +8.27 |
| SoftNet | 57.57 | +11.10 |
| EEIL | 33.79 | +34.77 |
| iCaRL | 32.87 | +35.69 |

CD2 在基类会话比 NC-FSCIL 高 0.80%（83.32% vs. 82.52%），在增量会话中分别领先 2.60%-0.39%。

### mini-ImageNet 主结果（Figure 4 左）

CD2 在 mini-ImageNet 上在所有会话（0-8）中均取得最高准确率。CD2 平均准确率的具体数值未在主文本中给出，仅出现在附录中。从图中曲线位置看，CD2（Ours）在所有会话中均高于所有对比方法。文本仅以图例标注 "Average: 67.75"，not explicitly stated 这是 CD2 还是某 baseline 的平均值——鉴于正文声称 "obtain the best accuracy in all sessions on CIFAR100 and MiniImageNet"，该数值极可能对应 CD2 在 mini-ImageNet 上的平均准确率。

### CUB-200-2011 主结果（Figure 4 右）

CD2 在 CUB200 上取得了最高平均准确率 **68.78%**（not reported in the source 这是否为 CD2 数值——该数值出现在右子图旁，正文声称 "we still achieve the highest average accuracy"）。CUB200 上的准确率曲线在某些会话有波动（"appears dented"），但整体平均仍最高。逐会话数值仅收录于附录，主文本未提供。

### 消融实验结果

**记忆策略对比（Table 2）**：在均使用 SR+FR 损失的前提下：

| 记忆策略 | 首个增量会话 (%) | 末个增量会话 (%) |
|---------|----------------|-----------------|
| 原型计算 | 78.98 | 56.03 |
| DDM (CD2) | 79.42 | 57.36 |
| DDM 提升 | +0.44 | +1.33 |

DDM 相比原型计算在首个增量会话提升 0.44%，在末个增量会话提升 1.33%。

**DCM 损失消融（Table 2）**：使用 DDM 作为记忆策略：

| DCM 配置 | 首个增量会话 (%) | 末个增量会话 (%) |
|----------|----------------|-----------------|
| 无 DCM | 79.01 | 56.31 |
| 仅 L_SR | 79.24 | 56.83 |
| 仅 L_FR | 79.37 | 56.06 |
| L_SR + L_FR (CD2) | 79.42 | 57.36 |

- 仅 L_SR vs 无 DCM: 首个会话 +0.23%, 末会话 +0.52%
- 仅 L_FR vs 无 DCM: 首个会话 +0.36%, 末会话 -0.25%（仅 FR 损失在末尾反而退化）
- L_SR + L_FR vs 无 DCM: 首个会话 +0.41%, 末会话 +1.05%
- 双损失联合 vs 仅 L_SR: 末会话 +0.53%（结构损失保障灵活性，特征损失保障精度）

**合成样本数 K 的影响（Table 3）**：

| K | 基类 (%) | 首个增量 (%) | 末个增量 (%) | 平均 (%) |
|---|---------|------------|------------|---------|
| 1 | 83.32 | 78.85 | 56.67 | 67.74 |
| 2 | 83.32 | 79.42 | 57.36 | 68.67 |
| 3 | 83.32 | 79.36 | 57.13 | 68.59 |
| 4 | 83.32 | 79.45 | 56.92 | 68.23 |
| 5 | 83.32 | 79.48 | 57.41 | 68.70 |

K=1 → K=2: 平均准确率从 67.74% 提升至 68.67%（+0.93%）。K>=2 后性能变化可忽略（峰值 68.70% 在 K=5 但 K=2 时为 68.67%，差距仅 0.03%）。论文出于资源消耗考虑选择 K=2。

### 可视化结果（t-SNE）

t-SNE 可视化（Figure 5, CIFAR-100 示例）显示：
- 同类真实样本在特征空间中良好聚集，模型能捕获同类共性模式。
- 新类别（增量类）的类间距离比基类更近——学习新数据比基类数据更难。
- 合成样本（星号标记）与所属类别的真实样本在特征空间中高度聚集，表明 DDM 成功从真实数据中学习并保留了关键类别特征。

## Limitations

1. **仅适用于图像分类**：实验仅在 CIFAR-100、mini-ImageNet 和 CUB-200-2011 三个图像分类数据集上进行验证，未探索其他模态（如文本、语音）或任务（如检测、分割）。

2. **依赖冻结 backbone 范式**：CD2 在增量会话中冻结 backbone 仅微调分类器，这限制了模型对新类别表征的适应能力。若 backbone 容量不足以覆盖所有新类别，性能可能饱和。

3. **DDM 合成引入额外计算开销**：每个增量会话后需要运行 1000 次迭代的 MMD 优化来合成记忆样本，论文未量化这一开销相比基线方法的额外成本。

4. **缺少 batch size 和硬件配置**：论文未报告 batch size 和使用的 GPU 型号/数量，使得复现存在不确定性。

5. **缺少统计显著性检验**：所有结果仅报告单次运行的准确率，未提供标准差或多次运行的均值±标准差，无法判断性能差异是否统计显著。

6. **CUB200 曲线波动未解释**：在 CUB200 上准确率曲线在部分会话出现凹陷（"appears dented"），论文未分析原因。

7. **长序列增量场景未充分评估**：最多 10 个增量会话（CUB200），未测试更长序列（如 20+ 会话）下的累计遗忘效应。

8. **未与生成式回放方法深度对比**：虽然论文提及了基于 GAN 的生成方法（如 Liu et al., 2022; Agarwal et al., 2022），但主实验表中未直接包含这些方法的数值对比。

## Reusable Claims

- Claim: 数据集蒸馏（DD）可以作为 FSCIL 中构建记忆的有效替代方案，相比原型计算能保留更多判别性关键知识，末个增量会话准确率提升 1.33%（57.36% vs. 56.03%）。
  Evidence: Table 2, CIFAR-100, DDM vs. Prototype (both with SR+FR losses).
  Scope: 5-way 5-shot FSCIL, 8 个增量会话, CIFAR-100, ResNet12 backbone.
  Confidence: medium（仅一个数据集上的消融结果，缺少 mini-ImageNet 和 CUB200 上的对应消融）。

- Claim: 合成样本数 K=2 是 CIFAR-100 上性能与资源消耗的最佳平衡点，K>=2 后额外收益可忽略（K=2 平均 68.67% vs. K=5 平均 68.70%，差距仅 0.03%）。
  Evidence: Table 3, CIFAR-100.
  Scope: CIFAR-100, 5-way 5-shot FSCIL 设置.
  Confidence: medium（仅在 CIFAR-100 上验证，其他数据集上 K 的最优值可能不同）。

- Claim: 特征保留损失 (L_FR) 和结构保留损失 (L_SR) 具有互补性：L_FR 确保位置精度，L_SR 提供灵活性，联合使用比单独使用任一损失在末个会话上获得更高准确率（57.36% vs. 56.83% (仅 SR) vs. 56.06% (仅 FR)）。
  Evidence: Table 2, DCM ablation rows.
  Scope: CIFAR-100.
  Confidence: medium（单一数据集验证）。

- Claim: 使用 MMD 按类别匹配合成数据与真实数据分布能够在每类仅 K=2 个合成样本的条件下有效保留关键类别知识。
  Evidence: Table 1 (overall SOTA), Table 2 (ablation), Figure 5 (t-SNE).
  Scope: 三个图像分类 FSCIL benchmark, ResNet12/18.
  Confidence: high（三个数据集一致验证）。

## Connections

### 已存在的 wiki 页面链接

- **[Dataset Distillation](../concepts/dataset-distillation.md)**: 数据集蒸馏核心概念——CD2 首次将 DD 引入 FSCIL，DDM 模块使用 MMD 分布匹配进行合成。
- **[CIFAR-100](../datasets/cifar-100.md)**: CIFAR-100 是 CD2 三个评估数据集之一，也是主要消融实验平台（60 基类 + 40 增量类，5-way 5-shot）。
- **[COBRA -- Cross-Group Barycenter Alignment](../methods/cobra.md)**: COBRA 同样是数据集蒸馏方法（关注子群体公平性），与 CD2 都是 2026 年将 DD 技术向新维度（公平性 vs. 增量学习）扩展的工作。
- **[RLDD -- Rethinking Long-tailed Dataset Distillation](../methods/rldd.md)**: RLDD 处理长尾蒸馏中的类别不平衡，与 CD2 处理增量会话中的类别遗忘同属 DD 在非标准分类设定下的应用。
- **[Accuracy (Top-1 / Top-5)](../../../meta/metrics/accuracy.md)**: CD2 使用的核心评估指标。

### 建议建立但尚未创建的关联页面

- **FSCIL 任务页** (`wiki/domains/distillation/tasks/few-shot-class-incremental-learning.md`): FSCIL 的任务定义、标准协议、常用数据集和代表性方法。
- **mini-ImageNet 数据集页**: CD2 使用的第二个 benchmark 数据集。
- **CUB-200-2011 数据集页**: CD2 使用的细粒度分类 benchmark。

## Open Questions

1. CD2 在非图像模态（如文本、语音）或非分类任务（如检测、分割）上是否同样有效？DDM 的 MMD 分布匹配策略是否需要针对不同模态和任务做调整？

2. K=2 在 CIFAR-100 上是性能-资源最优，在 mini-ImageNet 和 CUB200 上的最优 K 是否相同？论文未提供这两个数据集上的 K 消融。

3. 若在更长序列（如 20+ 增量会话）上运行，DDM 合成的记忆样本是否会累积偏差？alpha 自适应调节策略是否能持续有效？

4. CD2 的 DDM 合成速度（每类 1000 次迭代 MMD 优化）在实际部署中是否可接受？是否可能用更高效的匹配策略（如 KIP、MTT、DM）替代 MMD 分布匹配？

5. 若允许 backbone 在增量会话中也进行部分更新（而不仅是冻结），CD2 是否能获得更好性能？如何在 backbone 可塑性（plasticity）和记忆稳定性（stability）之间取得更好的平衡？

6. 论文声称 DDM 合成样本难以逆向恢复原始数据从而具有隐私保护性——这一声明缺少定量或形式化的隐私分析（如差分隐私保证或重建攻击实验）。

7. CD2 的 DCM 与传统的 LwF（Learning without Forgetting）知识蒸馏有何本质区别？论文未与 LwF 或类似知识蒸馏基线直接对比。

## Provenance

- 原始 PDF: not yet captured in `raw/sources/`（当前仅有全文本提取文件）。
- 全文本提取: `raw/sources/2026-01-15-cd2-constrained-dataset-distillation-fscil-fulltext.txt`（8 页完整论文文本）。
- 提取方式: 由主 agent 从 PDF 提取（具体工具 not specified in provenance）。
- 证据等级: `full-paper`——基于完整的 9 页（含参考文献）论文全文提取，覆盖标题、摘要、引言、相关工作、预备知识、方法论、实验（含主表、消融表、可视化）、结论、致谢和参考文献。
- 未覆盖内容: 附录（appendix）——论文多次引用附录中的额外结果（mini-ImageNet 和 CUB200 的详细逐会话数值表、更多消融实验），但全文本提取文件中未包含附录内容。
