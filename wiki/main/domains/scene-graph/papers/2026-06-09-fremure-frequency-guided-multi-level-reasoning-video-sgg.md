---
title: "FReMuRe: Frequency-Guided Multi-Level Reasoning for SGG in Video"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags: [video-SGG, frequency-guided, long-tail, debiasing, arXiv-2026]
raw_sources:
  - ../../../sources/scene-graph/2026-06-09-frequency-guided-multi-level-reasoning-sgg.pdf
  - ../../../sources/scene-graph/2026-06-09-frequency-guided-multi-level-reasoning-sgg.txt
evidence_level: full-paper
---

## 摘要

Video Scene Graph Generation 旨在从视频中提取对象及其关系的结构化语义表示。现有方法处理长尾分布仍有局限。本文提出 **FReMuRe** (Frequency-guided Relational Multi-level Reasoning) 模型，从机制角度增强长尾关系的建模能力。核心设计包括：(1) relation-specific branches 处理梯度冲突；(2) frequency-aware dual-branch predicate embedding network (DPEG) 分别建模高/低频关系并通过门控融合提升尾类召回率；(3) 两种可互换的 relation classification heads：Bayesian Head（不确定性估计）和 GMM-Plus Head（多原型增强类别内多样性）。实验表明 FReMuRe 在 Action Genome 数据集上显著提升长尾关系召回率和推理鲁棒性。

## 核心贡献

1. **Frequency-guided tail-class debiasing**：频率感知门控机制，利用频率先验知识提升低频关系召回率
2. **Decoupled Dual-Branch Network (DPEG)**：双分支 Transformer 解耦高/低频关系的学习过程，从架构层面解决梯度冲突
3. **Replaceable relationship classification heads**：BayesianHead 建模不确定性实现鲁棒预测；GMM-Plus 通过多原型 + 可调方差增强尾类表示

## 方法

### 总体框架

Faster R-CNN + 时序一致性模块检测对象 → DPEG 双分支谓词网络处理对象对 → 全局解码器 + Bayesian Head / GMM-Plus Head 生成最终预测。

核心设计原则：**解耦学习过程**。共享特征提取器时，θ 的总梯度 ∇θL = ∇θLa + ∇θLs + ∇θLc 可能包含冲突分量（⟨∇θLa, ∇θLs⟩ < 0），削弱长尾关系学习。通过独立参数为每种关系类型解耦更新，避免破坏性干扰。

### Frequency-guided Mechanism

- 关系频率 fk = nk / Σnj，构造频率张量 f ∈ R^|R|
- **Inverse-frequency weighting**：x′ = g(f) ⊙ LN(x) + (1 - g(f)) ⊙ x
  - LN(·) 为 LayerNorm 稳定尾类特征分布
- **Learnable frequency gate**：g(f) = σ(W · log(1/f + ε) + b)
  - log(1/f) 基于自信息理论将频率转换为特征缩放因子
  - 对稀有类别放大 gate 值，结构性地抵消头类梯度主导

### Dual-Branch Predicate Embedding Generator (DPEG)

**Local branch**：两路并行
- Standard local encoding path → Hloc（高频关系特征）
- Frequency-aware Tail branch → Tloc（低频关系特征）
- 门控融合：Gloc = σ(Wloc[Hloc∥Tloc∥f] + bloc)，Zloc = Gloc ⊙ Hloc + (1 - Gloc) ⊙ Tloc
- 双分支架构（物理解耦参数）与门控机制（动态特征调整）互补

**Global branch**：引入位置编码补充目标关系的全局上下文，处理序列产生全局表示 Zglob，通过滑动窗口机制聚合，得到最终精炼嵌入 Et ∈ R^(L×d)。

### Bayesian Head

- 对每类关系预测均值 µ 和方差 σ²
- 训练时 Monte Carlo 采样：ẑ = µ + ε · √σ²，ε ∼ N(0, 1)
- 输出为平均概率预测
- 捕获两种不确定性：aleatoric（数据固有方差）和 epistemic（预测分布熵）

### GMM-Plus Head

- 每类关系由 K 个高斯分量 (µk, σ²k, πk) 组成
- 输出概率：p(y|z) = Σ πk · N(z|µk, σ²k)
- 加入频率感知正则化项，防止高斯分量退化为 Dirac 分布（σ²→0）
- 强制方差下界，确保尾样本稀少时仍保持鲁棒多模态建模

## 实验

### 设定

| 维度 | 详情 |
|------|------|
| **数据集** | Action Genome (AG)：35 个对象（不含人）+ 25 种关系（attention/spatial/contact） |
| **数据划分** | 7584 训练集 / 1750 测试集 |
| **损失函数** | attention 用 cross-entropy；spatial / contact 用 binary CE 或 multi-label margin loss |
| **训练** | 10 epochs, Adam 优化器 |
| **评估指标** | R@K, mR@K |

### 主要结果（Action Genome）

#### PREDCLS 任务

| 方法 | R@10 / mR@10 | R@20 / mR@20 | R@50 / mR@50 |
|------|:------------:|:------------:|:------------:|
| RelDN (2019) | 20.3 / 6.2 | 20.3 / 6.2 | 20.3 / 6.2 |
| TRACE (2021) | 27.5 / 15.2 | 27.5 / 15.2 | 27.5 / 15.2 |
| STTran (2021) | 68.6 / 37.8 | 71.8 / 40.1 | 71.8 / 40.2 |
| STTran-TPI (2022) | 69.7 / 37.3 | 71.6 / 40.6 | 71.6 / 40.6 |
| TEMPURA (2023) | 68.5 / 37.5 | 71.1 / 40.8 | 71.2 / 40.9 |
| **FReMuRe+Bayesian (ours)** | **69.5 / 38.9** | **72.5 / 42.9** | **72.5 / 43.1** |
| **FReMuRe+GMM-Plus (ours)** | 69.1 / 38.7 | 72.2 / **43.1** | 72.2 / 43.1 |

#### SGCLS 任务

| 方法 | R@10 / mR@10 | R@20 / mR@20 | R@50 / mR@50 |
|------|:------------:|:------------:|:------------:|
| RelDN | 11.0 / 3.4 | 11.0 / 3.4 | 11.0 / 3.4 |
| TRACE | 14.8 / 8.9 | 14.8 / 8.9 | 14.8 / 8.9 |
| STTran | 45.3 / 27.2 | 46.0 / 28.0 | 46.1 / 28.0 |
| STTran-TPI | 45.3 / 28.3 | 46.1 / 29.3 | 46.1 / 29.3 |
| TEMPURA | 45.3 / 28.4 | 46.2 / 29.5 | 46.3 / 29.5 |
| **FReMuRe+Bayesian** | 45.4 / 29.4 | 45.5 / 30.5 | 46.5 / 30.6 |
| **FReMuRe+GMM-Plus** | **45.5 / 29.4** | **46.6 / 30.6** | **46.6 / 30.6** |

#### SGDET 任务

| 方法 | R@10 / mR@10 | R@20 / mR@20 | R@50 / mR@50 |
|------|:------------:|:------------:|:------------:|
| RelDN | 9.1 / 3.3 | 9.1 / 3.3 | 9.1 / 3.3 |
| TRACE | 13.9 / 8.2 | 14.5 / 8.2 | 14.5 / 8.2 |
| STTran | 25.8 / 16.6 | 33.0 / 20.8 | 33.3 / 22.2 |
| STTran-TPI | 25.1 / 15.6 | 32.9 / 20.2 | 33.2 / 21.8 |
| TEMPURA | 25.3 / 15.5 | 33.1 / 20.4 | 35.2 / 21.9 |
| **FReMuRe+Bayesian** | 25.4 / 14.9 | 33.1 / 20.1 | 35.2 / 21.9 |
| **FReMuRe+GMM-Plus** | **25.6 / 15.1** | **33.6 / 20.7** | **36.1 / 22.5** |

#### 主要发现

- **PREDCLS**：FReMuRe+GMM-Plus 在 mR@50 达到 **43.1**，超越所有对比方法
- **SGCLS**：FReMuRe+GMM-Plus 在 R@50=**46.6** / mR@50=**30.6** 为 SOTA
- **SGDET**：FReMuRe+GMM-Plus 在 R@50=**36.1** / mR@50=**22.5** 为最优
- 长尾指标 (mR@K) 提升最显著，验证了去偏能力

### 消融实验

| 变体 | PREDCLS mR@10/20/50 | SGCLS mR@10/20/50 | SGDET mR@10/20/50 |
|------|:-------------------:|:-----------------:|:-----------------:|
| no decouple | 36.3 / 40.4 / 41.4 | 24.8 / 28.5 / 28.6 | 12.1 / 17.3 / 17.3 |
| no frequency | 36.8 / 40.9 / 41.0 | 25.1 / 29.8 / 30.2 | 12.5 / 18.1 / 19.7 |
| no dual-branch | 36.5 / 40.1 / 40.1 | 24.3 / 28.7 / 29.2 | 12.5 / 18.8 / 19.9 |
| no bayes | 37.5 / 41.2 / 41.3 | 26.5 / 30.1 / 30.6 | 13.4 / 19.6 / 20.3 |
| no gmm-plus | 36.6 / 40.7 / 40.2 | 24.4 / 29.5 / 29.9 | 12.8 / 18.7 / 19.4 |
| **ours+Bayesian** | **38.9 / 42.9 / 43.1** | **29.4 / 30.5 / 30.6** | **14.9 / 20.1 / 21.9** |
| **ours+GMM-Plus** | **38.7 / 43.1 / 43.1** | **29.4 / 30.6 / 30.6** | **15.1 / 20.7 / 22.5** |

消融关键发现：
- **Core decoupling 最关键**：去掉解耦后 SGDET mR@50 从 22.5 跌至 17.3（降幅最大）
- **DPEG 双分支架构和频率引导机制**均不可或缺，移除后 SGCLS mR@10 降至 24.3 和 25.1
- **专用分类头**提供显著增益：移除 GMM-Plus 后 SGDET mR@50 从 22.5 降至 19.4

### 定性结果

FReMuRe 正确识别 "person looking at notebook" (TEMPURA 误判为 "not looking at")；正确检测 "person standing on floor" (TEMPURA 误判为 "in front of")。验证了解耦学习缓解常见关系偏好的能力。

## 方法对比

| 维度 | FReMuRe | TEMPURA | STTran |
|------|---------|---------|--------|
| 长尾处理 | 频率门控 + 双分支解耦 | 去偏正则 | 基础时序建模 |
| 分类头 | Bayesian / GMM-Plus (可替换) | 标准分类头 | 标准分类头 |
| 梯度冲突 | 显式解耦处理 | 未处理 | 未处理 |
| PREDCLS mR@50 | **43.1** | 40.9 | 40.2 |
| SGCLS mR@50 | **30.6** | 29.5 | 28.0 |
| SGDET mR@50 | **22.5** | 21.9 | 22.2 |

## 对应关系

- **场景图生成 (SGG)** → 本论文核心任务
- **Video SGG** → 时域场景图生成
- **Action Genome (AG)** → 实验评估数据集
- **长尾去偏** → 主要技术焦点 (类比: TDE, HiLo, TEMPURA 等去偏方法)
- **概率分类头** → Bayesian Head / GMM-Plus Head

## 适用任务

- 视频场景图生成
- 长尾关系学习
- 动态交互关系推理

## 优缺点

**优点**：
- 从机制层面（梯度冲突）系统解决长尾问题，而非简单重加权
- 频率门控 + 双分支解耦 + 专用分类头三者互补，消融验证各组件有效
- Bayesian Head 提供不确定性估计，对嘈杂视频数据更鲁棒
- GMM-Plus 通过方差约束防止尾类原型退化

**缺点**：
- 仅 5 页短文，方法描述不够详细（论文仅限 ICASSP 格式）
- 未报告处理帧率/速度，与其他方法比较缺少效率维度
- 改进幅度相对温和（mR@50 提升约 2-3 点）
- 仅在 Action Genome 上评估，未在更多数据集上验证
- 未与最新的 Video SGG 方法（如 TD2-Net, FloCoDe）直接比较

## 开放问题

- FReMuRe 在更极端的尾类分布（如 Open Vocabulary 设定）上表现如何？
- GMM-Plus 的 K 选择对性能的影响？
- 与 HiLo（频率高/低频拆分的 SGG 方法）的直接对比？
