---
title: Continual Distillation of Teachers from Different Domains
type: paper
domain: distillation
status: active
created: 2026-05-20
updated: 2026-05-24
tags:
  - knowledge-distillation
  - continual-learning
  - model-distillation
  - domain-incremental
  - external-data
paper:
  title: Continual Distillation of Teachers from Different Domains
  authors:
    - Nicolas Michel
    - Maorong Wang
    - Jiangpeng He
    - Toshihiko Yamasaki
  year: 2026
  venue: arXiv preprint
  arxiv: "2605.04059"
  doi: ""
  code: "https://github.com/Nicolas1203/continual_distillation"
  project: ""
classification:
  label: distillation
  task:
    - continual distillation
    - knowledge distillation
    - domain incremental learning
  method_family:
    - SE2D
    - logit preservation
    - external data distillation
    - self-distillation
  modality:
    - image
  datasets:
    - CIFAR20
    - Digits (MNIST/MNIST-M/USPS/SVHN)
    - DomainNet
    - CUB
    - KMNIST
  metrics:
    - accuracy (domain-wise final)
    - forgetting
    - UKT rate
    - UKF rate
    - teacher entropy distribution kurtosis
evidence_level: full-paper
raw_sources:
  - raw/sources/2026-04-10-continual-distillation-teachers-different-domains.pdf
related_pages:
  - wiki/domains/distillation/concepts/dataset-distillation.md
  - wiki/domains/llm-reasoning/concepts/long-cot-reasoning-distillation.md
  - wiki/domains/distillation/methods/se2d.md
---

## Citation

Michel, N., Wang, M., He, J., & Yamasaki, T. (2026). Continual Distillation of Teachers from Different Domains. *arXiv preprint arXiv:2605.04059*. The University of Tokyo, National Institute of Informatics, Indiana University Bloomington.

## One-Sentence Contribution

提出 **Continual Distillation (CD)** 新范式——学生模型从不同领域的教师模型序列中顺序蒸馏学习，无需保留历史教师的访问权限；发现外部无标签数据同时触发 Unseen Knowledge Transfer (UKT) 和 Unseen Knowledge Forgetting (UKF)，提出 SE2D 方法通过保留外部数据 logits 来平衡二者，在 CIFAR20 上超越 Self-Distillation +1.24pp、在 Digits 上 +1.42pp。

## Problem Setting

Foundation Models 持续涌现且规模巨大（100B+ 参数，约 38GB+），存储和访问历史版本模型日益困难——API 更新后旧版本可能不可用。CD 范式将此建模为：单一学生模型从教师模型序列中顺序学习，无法回访先前教师。

**三个关键假设**：(1) 每个教师在不同领域数据上训练，但共享某个特定领域（Di）；(2) 蒸馏训练数据 DS 固定不变，DS = De ∪ Di；(3) 训练数据无标签。

**核心挑战**：
- **UKT (Unseen Knowledge Transfer)**：外部数据（ED，所有教师都未知的数据）能让学生获取教师已知但学生未见领域的知识——Table 1 显示 ID-only 蒸馏时未见领域仅 33-45%，加入 ED 后提升至 77-85%。
- **UKF (Unseen Knowledge Forgetting)**：顺序蒸馏中，后续教师的学习会覆盖先前教师传递的未见领域知识——DKD 在 Digits 上 MNIST-M 从 54.50% 跌至 33.84%（-20.66pp）。
- **UKT-UKF trade-off**：CD 的核心是找到最优的知识迁移-遗忘平衡点。

与数据集蒸馏的本质区别：CD 是**模型级蒸馏**（教师模型→学生模型），数据集蒸馏是**数据级压缩**（大规模数据集→合成小数据集）。

## Method

### 数据分解

训练数据 DS 分为两类：
- **Internal Data (ID, Di)**：所有教师都已知的共享领域数据
- **External Data (ED, De)**：所有教师都未知的外部领域数据

### SE2D (Self External Data Distillation)

受持续学习中 self-distillation 机制启发，SE2D 在蒸馏损失之外增加 logit 保持正则项：

1. **标准蒸馏损失**：KL 散度（T=10），学生模仿当前教师的软标签，在全量 DS 上计算
2. **外部数据 Logit 保持**：仅在 De 上进行 self-distillation——保存学生上一任务 checkpoint 对 ED 的预测 logits，约束当前 logits 不过度偏离
3. **联合训练**：L_SE2D = L_KD(S_t, T_t; DS) + L_KD(S_t, S_{t-1}; De)

关键设计：self-distillation **仅限 De**——在 Di 上 self-distill 主要强化已稳定知识，而在 De 上 self-distill 才能直接保护从未见领域迁移来的脆弱知识。

### Baseline 方法

| 方法 | 出处 | 核心机制 |
|------|------|---------|
| KL-divergence | Hinton 2015 | 标准 logit 蒸馏，T=10 |
| Logits Standardization (LS) | Sun et al., CVPR 2024 | 标准化师生 logits 后蒸馏 |
| Medium Difficulty Samples (MDS) | Chen et al., ICLR 2025 | 仅蒸馏中等难度样本（用教师熵估计难度） |
| Decoupled Knowledge Distillation (DKD) | Zhao et al., CVPR 2022 | 解耦目标类/非目标类蒸馏（无监督适配：以教师最大预测为目标类） |
| Self-Distillation | CL 通用策略 | 保存学生历史 checkpoint，在当前任务上同时对 Di 和 De 做 self-distill |

## Experiments

### 实验配置

**训练设置**：ViT-B/16 backbone（预训练权重初始化），Adam lr=1e-4，3 epochs，224×224，batch 64，KL 蒸馏 T=10，3 seeds。教师单独预训练 50 epochs，域内准确率 >95%。

**Benchmark 1 — CIFAR20**：CIFAR-100 的 20 个超类，每超类 5 子类组成 5 个 domain（D0-D4），每 domain 10K train / 2K test。教师序列：{(0,1), (0,2), (0,3)}，D0 为共享 ID，ED 分别用 D4（相关）、CUB（中等相关）、MNIST（无关）。

**Benchmark 2 — Digits**：MNIST（ID，共享）+ SVHN + MNIST-M + USPS 依次为教师专属 domain。KMNIST（日本平假名字符）作为相关 ED。教师用 ViT-tiny。

**Benchmark 3 — DomainNet**：6 个视觉 domain（Real, Clipart, Painting, Infograph, Sketch, Quickdraw），345 类共享，~600K 图像，domain 间不平衡。Clipart 为 ID，Sketch 为 ED。额外测试 CLIP-base（ViT-L/14）教师和多种 domain 序列。

### 评估指标

- **Domain-wise Final Accuracy**：训练序列结束后学生在各 domain 测试集上的准确率
- **Forgetting**：F_d = max_{i<t} A_d^(i) - A_d^(t)，取所有 domain 平均
- **Gain**：相比 Internal Data Only 设置的平均提升

---

## Results

### 5.1 ED 对 UKT 的触发效应（Table 1）

**现象**：仅用 ID（|De|/|DS| = 0%）蒸馏时，学生在见过 domain（D0）上达 92.10-93.95%，但未见 domain 仅 31.60-45.30%。加入 ED 后：

| |De|/|DS| | D0 (ID) | D1 (seen) | D2 (unseen) | D3 (unseen) |
|----------|---------|-----------|-------------|---------------|
| 0% | 93.95 | 31.60 | 42.20 | 35.25 |
| 33% | 92.70 | 93.15 | 68.35 | 53.80 |
| 50% | 96.35 | 77.15 | 48.95 | 48.45 |
| 66% | 94.60 | 85.20 | 51.85 | 57.15 |

**结论**：ED 是 UKT 的必要条件；|De|/|DS| 比例越大，未见 domain 性能越强。

### 5.2 UKF 现象与缓解（Tables 2-4）

#### CIFAR20 基准（Table 2，4 种 ED 场景，均值 ± 标准差）

**Internal Data Only**（教师序列 D0→D1→D2→D3，无 ED）：
所有方法在未见 domain 上表现极差。KL 平均 61.94±1.24，DKD 54.42±2.02，Self-Dist 57.82±1.51。Tbest 上限 96.5。

**Related ED (D4)**——SE2D 最优场景：

| 方法 | D0 (ID) | D1 (最早) | D2 | D3 (最近) | Avg (0-3) | Gain |
|------|---------|-----------|-----|-----------|-----------|------|
| KL | 97.05±0.09 | 48.55±1.15 | 55.08±0.70 | 84.77±0.87 | 71.36±0.70 | +9.42 |
| DKD | 96.05±0.50 | 44.13±0.98 | 51.67±0.92 | 68.55±2.60 | 65.10±1.25 | +10.68 |
| LS | 96.85±0.15 | 47.25±0.69 | 54.25±0.46 | 83.20±1.87 | 70.39±0.79 | +11.64 |
| MDS | 96.55±0.07 | 45.26±2.10 | 54.90±0.71 | 73.51±0.56 | 67.56±0.86 | +14.01 |
| Self-Dist | 97.71±0.18 | 61.23±0.83 | 64.21±0.51 | 76.58±0.94 | 74.93±0.61 | +17.11 |
| **SE2D** | **97.46±0.19** | **70.71±1.05** | **62.85±0.50** | **73.65±1.67** | **76.17±0.85** | n/a |

**关键发现**：SE2D 在 D1（最早 domain）上 70.71 vs Self-Dist 61.23（**+9.48pp**），证明 SE2D 有效缓解 UKF。Self-Dist 在最近 domain D3 上更强（76.58 vs 73.65），体现 UKT-UKF trade-off。

**CUB 作为 ED**（中等相关）：

| 方法 | D0 | D1 | D2 | D3 | Avg (0-3) | Gain |
|------|-----|-----|-----|-----|-----------|------|
| KL | 97.24±0.37 | 43.89±1.02 | 55.13±0.76 | 71.80±1.73 | 67.02±0.97 | +5.08 |
| DKD | 93.39±0.88 | 33.46±2.51 | 43.10±2.93 | 40.70±2.20 | 52.66±2.13 | **-1.76** |
| Self-Dist | 97.47±0.12 | 47.97±1.07 | 58.40±1.34 | 61.97±1.82 | 66.45±1.09 | +8.63 |
| **SE2D** | **97.74±0.10** | **53.93±0.43** | **58.02±0.45** | **64.54±1.81** | **68.56±0.70** | n/a |

CUB 相关度低于 D4，所有方法 gain 缩小。DKD 出现负 gain（-1.76），说明方法-ED 交互敏感。

**MNIST 作为 ED**（无关）：
所有方法 gain 为负——KL 59.78±8.63（-2.16），Self-Dist 54.26±9.00（-3.56），SE2D 57.25±9.29。标准差显著增大（8-15%），反映无关 ED 引入的噪声。ED 与教师 domain 差距过大时，使用 ED 反而劣于不使用。

#### Digits 基准（Table 3，2 种场景）

**Internal Data Only**：KL 73.40±1.17，DKD 70.40±1.07，Self-Dist 73.87±0.76。Tbest 98.77。

**Related ED (KMNIST)**：

| 方法 | MNIST (ID) | SVHN | MNIST-M | USPS | Avg | Gain |
|------|-----------|------|---------|------|-----|------|
| KL | 99.13±0.05 | 31.53±1.55 | 59.84±2.57 | 96.51±0.10 | 71.75±1.07 | **-1.65** |
| DKD | 98.35±0.32 | 25.21±1.62 | **33.84±4.28** | 92.87±1.63 | 62.57±1.96 | **-7.83** |
| LS | 99.13±0.08 | 32.28±0.37 | 61.47±2.15 | 96.33±0.33 | 72.30±0.73 | -1.91 |
| MDS | 99.12±0.04 | 33.03±1.79 | 60.74±0.97 | 96.13±0.05 | 62.50±0.90 | -7.71 |
| Self-Dist | 99.38±0.01 | 55.86±1.60 | 90.76±0.35 | 96.33±0.15 | 85.58±0.53 | +11.71 |
| **SE2D** | **99.33±0.04** | **61.84±2.05** | **90.44±0.18** | **96.33±0.10** | **87.00±0.60** | n/a |

**关键发现**：加入 ED 后，KL/DKD/LS/MDS 的 gain 全为负——ED 加剧了 UKF。DKD 的 MNIST-M 从 Internal Only 的 54.50% 暴跌至 33.84%（**-20.66pp**），是最严重的 UKF 案例。Self-Dist 部分缓解（gain +11.71），SE2D 进一步优化（87.00 vs 85.58，**+1.42pp**）。

#### DomainNet 基准（Table 4，2 种场景）

**Internal Data Only**：Self-Dist 47.31±0.11，KL 44.78±0.29，DKD 43.91±0.17。Tbest 64.39。

**Related ED (Sketch)**：

| 方法 | Clipart (ID) | Infograph | Painting | Quickdraw | Real | Avg | Gain |
|------|-------------|-----------|----------|-----------|------|-----|------|
| KL | 76.00±0.18 | 18.89±0.09 | 44.77±0.79 | 15.53±0.15 | 70.65±0.46 | 45.17±0.31 | +0.39 |
| Self-Dist | **80.10±0.18** | 21.53±0.09 | **48.15±0.23** | **25.28±0.19** | **68.75±0.01** | **48.76±0.07** | **+1.45** |
| SE2D | 78.05±0.11 | **21.98±0.29** | 47.76±0.44 | 23.81±0.34 | 68.43±0.14 | 48.01±0.20 | n/a |

**关键发现**：SE2D 在 DomainNet 上**落后于 Self-Distillation**（48.01 vs 48.76）。原因：(1) 教师质量低——DomainNet 域间差异大，教师对未见 domain 的监督信号弱；(2) domain 间差异过大阻碍 UKT。这揭示了 SE2D 的核心局限——需要足够强的教师和合理的 ED-domain 关联。

### 5.3 Forgetting 分析（Appendix Tables C.1-C.3）

**CIFAR20 + Related ED (D4)**：
| 方法 | Avg Forgetting ↓ |
|------|-----------------|
| KL | 17.23 |
| LS | 17.98 |
| MDS | 17.26 |
| DKD | 10.38 |
| Self-Dist | 8.32 |
| **SE2D** | **4.44** |

SE2D 遗忘率比 Self-Dist 降低 **46.6%**，比 KL 降低 **74.2%**。

**Digits + Related ED (KMNIST)**：
| 方法 | Avg Forgetting ↓ |
|------|-----------------|
| LS | 19.22 |
| KL | 19.17 |
| MDS | 19.16 |
| DKD | 15.87 |
| Self-Dist | 5.58 |
| **SE2D** | **3.73** |

SE2D 遗忘率比 Self-Dist 降低 **33.2%**，比 KL 降低 **80.5%**。

**DomainNet + Related ED (Sketch)**：
SE2D 遗忘率 14.18 vs Self-Dist 13.08——在 DomainNet 上 SE2D 的遗忘率反而更高，印证了 Table 4 的结论。

**CIFAR20 + CUB**：SE2D 遗忘率 7.21 vs Self-Dist 7.29（基本持平），但 DKD 仅 2.03——DKD 遗忘率低是因为它从一开始就没学到（accuracy 低），而非真正保留了知识。

**CIFAR20 + MNIST**：SE2D 遗忘率 4.43 vs Self-Dist 2.18——在无关 ED 上 Self-Dist 遗忘率更低，但所有方法 absolute accuracy 都很低（<60%）。

### 5.4 跨架构验证（Appendix Tables C.4-C.5）

**ViT-tiny 学生**（CIFAR20 + Related ED）：
| 方法 | Avg (0-3) |
|------|-----------|
| KL | 68.68±1.09 |
| Self-Dist | 70.76±0.68 |
| **SE2D** | **71.09±1.21** |

SE2D 在更小 backbone 上仍优于 Self-Dist（+0.33pp），且 D1 上优势更明显（62.33 vs 55.42，**+6.91pp**）。

**CLIP-base 教师**（ViT-L/14，DomainNet）：
| 方法 | Avg |
|------|-----|
| KL | 47.05±0.22 |
| Self-Dist | **47.69±0.84** |
| SE2D | 46.83±0.31 |

即使换用更强教师（Tbest 从 64.39 提升至 76.23），SE2D 仍落后于 Self-Dist，进一步证实 DomainNet 的困难根源于 domain 差异而非教师能力。

### 5.5 ED 质量代理指标（Appendix Fig B.1-B.2）

提出用**教师熵分布的峰度（kurtosis）**作为 ED 质量的代理指标：

- 在 CIFAR20 教师（训练于 D0+D1）上，D4 的熵分布集中（高峰度），CUB 次之，MNIST 最平坦（低峰度）
- **熵分布越平坦 → UKT 潜力越低**：MNIST 平坦分布 → 所有方法 gain 为负；D4 集中分布 → 高 UKT
- DomainNet 各 domain 熵分布差异极大（Fig B.2），部分解释了该数据集的困难

实际使用：用户可 (1) 按熵阈值过滤 ED 样本；(2) 用 4 阶矩（kurtosis）量化分布的"平坦度"来选择 ED。

### 5.6 额外 DomainNet 序列（Appendix Table C.6）

移除困难 domain 后：
- **Seq 1**（Quickdraw 作 ED，Infograph 忽略）：Self-Dist 61.79 vs SE2D 56.82
- **Seq 2**（Infograph 作 ED）：Self-Dist 54.72 vs SE2D 53.58（差距缩小至 1.14）
- **Seq 3**（Sketch 作 ED，Infograph+Quickdraw 忽略）：Self-Dist 70.21 vs SE2D 69.34（差距缩小至 0.87）

在简化场景下 SE2D 与 Self-Dist 的差距收窄，但始终未能超越——DomainNet 的根本挑战在于 domain 差异本身而非特定 domain 的难度。

## Results Summary

- **CIFAR20**：SE2D 76.17±0.85，超越所有 baseline，在最早 domain D1 上比 Self-Dist **+9.48pp**
- **Digits**：SE2D 87.00±0.60，比 Self-Dist **+1.42pp**；DKD 出现严重 UKF（MNIST-M -20.66pp）
- **DomainNet**：SE2D 48.01±0.20，**落后于** Self-Dist 48.76±0.07——教师质量低 + domain 差异大
- **Forgetting**：CIFAR20 上 SE2D 遗忘率 4.44 vs Self-Dist 8.32（**-46.6%**），Digits 上 3.73 vs 5.58（**-33.2%**）
- **跨架构**：ViT-tiny 上 SE2D 71.09 vs Self-Dist 70.76；CLIP-base 上仍然 DomainNet 困难
- **ED 选择**：ED 必须与教师 domain 有足够相关性（D4 > CUB > MNIST），完全无关的 ED 反而损害性能
- **ED 质量代理**：教师熵分布的 kurtosis 可有效预测 UKT 潜力

## Limitations

1. 仅验证 ViT 架构（ViT-B/16、ViT-tiny），未测试 CNN/MLP 等其他 backbone
2. ED 必须与教师训练领域有足够相关性才能有效 UKT——完全无关的 ED 增益为负
3. 教师质量显著影响 CD 效果——弱教师（如 DomainNet 某些 domain）限制了 SE2D 的上限
4. 未探索标签可用的 CD 场景（supervised CD）
5. 仅考虑 logit 级蒸馏，未探索 feature 级蒸馏在 CD 中的表现
6. 主要评估限于视觉分类任务，未涉及语言或多模态模型
7. SE2D 需要数据来源知识——学生必须区分教师的已知和未知 domain，在数据生成场景下难以实现

## Reusable Claims

- 声明：外部无标签数据（ED）是 CD 中实现 UKT 的必要条件——ID-only 蒸馏无法将知识迁移到学生未见领域。
  证据：[Table 1](continual-distillation-teachers-different-domains.md)，ID-only 下未见领域仅 31.60-45.30%，加入 ED（|De|/|DS|=66%）后提升至 44.00-85.20%。
  范围：domain-incremental CD，ViT 架构，CIFAR20。
  置信度：**high**。

- 声明：CD 中存在 UKT-UKF trade-off，类似持续学习的 stability-plasticity trade-off。
  证据：[Tables 2-4](continual-distillation-teachers-different-domains.md)，所有方法在新旧教师领域上的性能呈反相关。Self-Distillation 在旧 domain 上优于 KL 但在新 domain 上弱于 KL。
  范围：domain-incremental CD，三种 benchmark。
  置信度：**high**。

- 声明：SE2D 通过仅在 ED 上做 self-distillation 有效缓解 UKF，遗忘率比 Self-Distillation 降低 33-47%。
  证据：[Table C.1-C.2](continual-distillation-teachers-different-domains.md)，CIFAR20 forgetting 4.44 vs Self-Dist 8.32（-46.6%），Digits 3.73 vs 5.58（-33.2%）。
  范围：ED 与教师 domain 相关的 CD 场景。
  置信度：**high**（从 medium 升级——有了完整的 forgetting 定量证据）。

- 声明：ED-教师 domain 的相关性决定了 UKT 效率和 SE2D 的有效性——ED 存在明确的质量层级：相关 domain > 中等相关数据集 > 无关数据集。
  证据：[Table 2](continual-distillation-teachers-different-domains.md)，D4 作 ED → KL gain +9.42；CUB → +5.08；MNIST → -2.16。所有方法遵循此层级。
  范围：视觉分类 CD。
  置信度：**high**（从 medium 升级——三种 ED 类型覆盖了完整的相关性谱系）。

- 声明：教师熵分布的 kurtosis 可作为 ED 质量的免标签代理指标——分布越平坦 UKT 潜力越低。
  证据：[Fig B.1-B.2](continual-distillation-teachers-different-domains.md)，D4（高峰度）→ 高 UKT，MNIST（平坦）→ 负 gain。
  范围：视觉分类 CD，ViT 教师。
  置信度：medium（首次提出，仅在一个数据集上系统验证）。

- 声明：DomainNet 上 SE2D 落后于 Self-Distillation，因为域间差异过大导致 UKT 微弱、教师对未见 domain 监督信号不足。
  证据：[Table 4](continual-distillation-teachers-different-domains.md)，SE2D 48.01 vs Self-Dist 48.76；[Table C.5](continual-distillation-teachers-different-domains.md)，CLIP-base 教师下 SE2D 46.83 vs Self-Dist 47.69。
  范围：DomainNet 及类似大域间差异数据集。
  置信度：**high**（多个教师配置和序列下一致）。

- 声明：DKD 在无监督 CD 场景下表现极不稳定——UKF 最严重（Digits MNIST-M -20.66pp），且对 ED 相关性高度敏感（CUB 作 ED 时 gain 为 -1.76）。
  证据：[Tables 2-3](continual-distillation-teachers-different-domains.md)，DKD 在多个场景下 gain 为负。
  范围：无监督 CD，DKD 以教师最大预测为目标类。
  置信度：medium（DKD 原生为监督方法，无监督适配可能不是最优）。

## Connections

- [Dataset Distillation](../concepts/dataset-distillation.md)：CD 与数据集蒸馏共享"蒸馏"概念但层次不同——CD 是模型级序列蒸馏，DD 是数据级压缩。CD 中 ED 的选择问题与 DD 中合成数据的信息覆盖问题类似。
- [Long-CoT 推理蒸馏](../../llm-reasoning/concepts/long-cot-reasoning-distillation.md)：CoRD 的多 teacher 协同蒸馏与 CD 的序列 teacher 蒸馏形成对比——前者并行利用多 teacher 互补性，后者顺序处理 teacher 流。
- [Federated Distillation and Unlearning](../../federated-learning/topics/federated-distillation-and-unlearning.md)：联邦蒸馏中的知识迁移与 CD 的 UKT 面临类似挑战——如何在分布式/序列场景中保留跨源知识。
- [SE2D 方法页](../methods/se2d.md)：本文提出的核心方法，详见方法页。

## Open Questions

1. Feature 级蒸馏（而非仅 logit 级）能否更有效地缓解 UKF？
2. ED 的质量和选择策略——如何自动选择与教师领域相关的外部数据？kurtosis 阈值的跨数据集泛化性？
3. CD 能否与数据集蒸馏结合——用合成数据作为 ED 进行持续模型蒸馏？
4. 更大规模 teacher 序列（10+ teachers）下的 UKF 累积效应？
5. 跨模态 CD（视觉→语言→多模态 teacher 序列）是否可行？
6. DKD 的无监督适配是否可以改进以在 CD 中发挥作用？
7. SE2D 在教师质量普遍较低时的改进方向？（如自适应 λ 权重）
8. UKT 的安全风险——不受控的外部知识可能通过 ED 意外嵌入学生模型？

## Provenance

- Source PDF: `raw/sources/2026-04-10-continual-distillation-teachers-different-domains.pdf`
- arXiv: 2605.04059v1, submitted 2026-04-10
- 全文 17 页（含 Appendix A-D），通过 PyMuPDF 完整抽取
- 覆盖：Introduction (§1)、Related Work (§2)、Continual Distillation (§3)、Experimental Setup (§4)、Experimental Results (§5, Tables 1-4)、Conclusions (§6)、Appendix A-D (Tables C.1-C.6, 额外架构/序列/熵分析)
- 代码：https://github.com/Nicolas1203/continual_distillation
