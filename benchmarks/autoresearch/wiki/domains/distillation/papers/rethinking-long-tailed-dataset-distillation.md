---
title: Rethinking Long-tailed Dataset Distillation: A Uni-Level Framework with Unbiased Recovery and Relabeling
type: paper
domain: distillation
status: stable
created: 2026-04-20
updated: 2026-05-05
tags:
  - dataset-distillation
  - long-tailed-learning
  - computer-vision
  - aaai-2026
paper:
  title: Rethinking Long-tailed Dataset Distillation: A Uni-Level Framework with Unbiased Recovery and Relabeling
  authors:
    - Xiao Cui
    - Yulei Qin
    - Xinyue Li
    - Wengang Zhou
    - Hongsheng Li
    - Houqiang Li
  year: 2026
  venue: AAAI 2026
  arxiv: "2511.18858"
  doi: ""
  code: "https://github.com/2018cx/RLDD"
  project: ""
classification:
  label: distillation
  task:
    - long-tailed dataset distillation
  method_family:
    - statistical alignment
    - unbiased recovery
    - unbiased relabeling
    - Batch Normalization recalibration
    - expert model debiasing
  modality:
    - image
  datasets:
    - CIFAR-10-LT
    - CIFAR-100-LT
    - Tiny-ImageNet-LT
    - ImageNet-LT
  metrics:
    - top-1 accuracy
evidence_level: full-paper
raw_sources:
  - raw/sources/2025-12-14-rethinking-long-tailed-dataset-distillation.pdf
related_pages:
  - wiki/domains/distillation/concepts/dataset-distillation.md
  - wiki/domains/distillation/topics/long-tailed-dataset-distillation.md
  - wiki/domains/distillation/methods/rldd.md
  - wiki/domains/distillation/comparisons/cobra-vs-rldd.md
---

# Rethinking Long-tailed Dataset Distillation: A Uni-Level Framework with Unbiased Recovery and Relabeling

## 引用

Xiao Cui, Yulei Qin, Xinyue Li, Wengang Zhou, Hongsheng Li, Houqiang Li. Rethinking Long-tailed Dataset Distillation: A Uni-Level Framework with Unbiased Recovery and Relabeling. AAAI 2026. arXiv:2511.18858. Code: https://github.com/2018cx/RLDD

## 一句话贡献

将长尾数据集蒸馏从 trajectory-matching 视角转向统计对齐（statistical alignment）视角，通过 expert model debiasing、BN statistics recalibration 和 confidence-guided multi-round initialization 三个组件联合消除模型偏置并恢复公平监督，在多个长尾 benchmark 上显著超越 SOTA。

## 问题设定

数据集蒸馏旨在从完整数据集中提取紧凑的合成数据集，使在其上训练的模型能接近在原始数据上训练的性能。现有方法在平衡数据集上表现良好，但在长尾分布下面临两个核心挑战：

1. **模型表示偏置**：不平衡的类别频率导致模型对 head class 过拟合，tail class 语义信息丢失。
2. **BN 统计扭曲**：标准指数移动平均（EMA）更新中，近期 batch 主导统计量，早期 batch 的贡献迅速衰减——在长尾场景下每个 tail class 样本的表示价值极高，这种不公平累积尤其有害。

论文指出现有 trajectory-based 方法（如 MTT、DATM、DAMED）的局限性：它们依赖 per-class expert trajectories，而 long-tailed 数据下 expert 本身就有偏，导致蒸馏数据继承并放大偏置。

## 方法

框架采用统一的 statistical alignment 视角组织三个组件，共同实现 unbiased recovery 和 soft relabeling：

### 1. Expert Model 去偏置（Model Debiasing）

训练两个 expert 模型：
- **Observer Model (R)**：用于 recovery，计算 BN 统计量作为合成图像恢复的对齐目标。
- **Teacher Model (T)**：用于 relabeling，生成 soft labels 提供语义监督。

**Robust Loss**：用于训练 R，减少 head class 优势，保留 tail class 信号。
**Debiasing Loss**：用于训练 T，通过频率加权策略在训练过程中动态调整各类别的学习强度——先聚焦 head class 建立稳定表示，随着训练推进逐步将 focus 移向 minority class。

联合损失：L = λ₁·L_robust + λ₂·L_debias

### 2. BN 统计量公平重校准（Fair BN Statistics Recalibration）

训练完成后，冻结 R 的参数，在真实数据集上执行一次完整前向传播，使用动态 momentum 逐 batch 累积类别级统计量：

μᶜˡᵗ = (1 - τᶜᵗ) · μ̂ᶜˡᵗ⁻¹ + τᶜᵗ · μ̂ᶜˡᵗ

其中动态 momentum τᶜᵗ = Bᶜᵗ / (Nᶜᵗ⁻¹ + Bᶜᵗ)，确保每个样本无论时间顺序如何都对最终统计量有相等贡献。

最后，将所有类别的统计量均匀平均得到全局 BN 统计量：μˡ = (1/C) · Σ μᶜˡᵀ

这个两阶段策略同时缓解了 intra-class bias（动态 momentum）和 inter-class bias（类间均匀平均）。

### 3. 置信度引导的多轮初始化（Confidence-guided Multi-round Initialization）

- 对每个真实图像生成多个增强（如裁剪），通过 T 评分（负交叉熵损失），存储到类别候选池。
- 每轮每张图像贡献其置信度最高且尚未使用的增强到临时选择池。
- 如果候选数超过剩余槽位，选择 top-scoring；否则全部保留。
- 重复直到每个类别达到目标 IPC。
- 对样本数少于最大类的类别，插入零初始化占位符（不参与增强和选择过程）。

### 蒸馏数据合成与评估

初始化 S_init → 通过 R 和真实数据 BN 统计量进行 statistical recovery → 通过 T 进行 soft relabeling → 得到最终蒸馏集 S。

评估阶段，学生模型使用双目标损失训练：
L_match = λ₁·L_CE(σ(xˢᵢ), yˢᵢ) + λ₂·|| ỹˢᵢ - σ(xˢᵢ) ||²₂

## 实验

### 实验设置

- **数据集**：CIFAR-10-LT、CIFAR-100-LT、Tiny-ImageNet-LT、ImageNet-LT，使用指数衰减采样策略构建（IF = μ⁻ᶜ/⁽ᶜ⁻¹⁾）。
- **IPC 设置**：1、10、20、50。
- **IF 设置**：5、10、20、50、100、256。
- **学生模型**：CIFAR 用 depth-3 ConvNet；Tiny-ImageNet/ImageNet-LT 用 depth-4 ConvNet；ImageNet-LT 额外评估 ResNet-50。
- **训练**：学生模型在蒸馏集上训练 1000 epoch，5 次重复实验，单张 RTX 3090。
- **基线**：Random、K-Center、Graph-Cut、DC、DREAM、MTT、DATM、TESLA、DAMED、SRe2L、RDED、EDC、Minimax、G-VBSM 等。

### 主要结果

**CIFAR-10-LT**（IPC=10, IF=10）：63.6%（vs. DAMED 58.1%，提升 +5.5%）。
**CIFAR-100-LT**（IPC=10, IF=10）：47.1%（vs. DAMED 31.5%，提升 +15.6%）。
**Tiny-ImageNet-LT**（IPC=10, IF=10）：37.8%（vs. DAMED 26.0%，提升 +11.8%）。
**ImageNet-LT**（IPC=10, IF=5）：24.7%（vs. DAMED 20.8%，提升 +3.9%）。

### 高不平衡设置（IF=100, 256, ResNet-50）

在 ImageNet-LT 上 IF=256 + ResNet-50 评估：48.2%（IPC=10）/ 48.9%（IPC=20），远超 DAMED 的 17.2%/17.9%。

### 极端低 IPC 设置（IPC=1）

- CIFAR-10-LT (IF=100)：44.8% vs. DAMED 24.1%（+20.7%）
- CIFAR-100-LT (IF=50)：31.8% vs. DAMED 7.8%（+24.0%）
- Tiny-ImageNet-LT (IF=100)：20.1% vs. DAMED 6.0%（+14.1%）

### 跨架构泛化

在 ConvNet-3、VGG-11、ResNet-18、AlexNet 四种架构上评估，本方法均显著优于所有基线。值得注意的是，DAMED 在 VGG-11 上下降到 29.7%，而本方法保持 64.6%。

### 类别级准确率

与 DAMED 相比，本方法在 tail class 上的准确率大幅提升，mid-frequency class 也不受影响。DAMED 因 biased expert 训练而在 tail class 上表现不佳，且频率调整损失忽略 mid-frequency 类别。

### 消融实验

在 CIFAR-100-LT (IF=50) 上：
- 无 Model Debiasing：准确率下降约 10%。
- 无 Statistics Recalibration：准确率下降约 1-2%（IPC 越高影响越大）。
- 无 Adapted Initialization：准确率下降约 1%。
- 三个组件均有正向贡献，Model Debiasing 贡献最大。

### 计算效率

- **训练时间**：本方法 expert model 训练 + 蒸馏数据合成的总时间不到 DAMED 的 1/20。
- **GPU 内存**：本方法内存使用恒定（3.1GB），与 IPC 无关；DAMED 内存随 IPC 线性增长（10.2GB → 15.8GB）。

## 结果

- 从 trajectory matching 转向 statistical alignment 是长尾蒸馏的关键 insight，避免了 biased expert trajectory 的问题。
- BN statistics recalibration 的动态 momentum 机制设计精巧：每个样本平等贡献，不受时间顺序影响。
- 在最极端条件下（IPC=1, IF=100/256）的方法鲁棒性尤其突出。
- 计算效率优势显著——训练快 20 倍且内存恒定，对大规模部署有实际意义。

## 限制

- 方法依赖 expert model 的预训练质量，极端低数据场景下 expert 质量可能下降。
- statistical alignment 假定了 BN 统计量的分布级匹配足够——对于非 BN 架构（如 Transformer）的适用性未验证。
- 未探索与 generative-model-based 蒸馏方法（如 diffusion-based）的结合可能性。
- 多领域/联邦数据集蒸馏场景下的验证仅限于讨论，缺乏实验。

## 可复用 Claims

- 声明：长尾数据集蒸馏中，biased expert trajectories 是核心瓶颈，statistical alignment 是更有效的范式。
  证据：在 CIFAR-100-LT (IF=10) 上超越最佳 trajectory-based 方法 DAMED +15.6%。
  范围：长尾图像分类蒸馏。
  置信度：high。
  张力：需要与非 trajectory 方法（如 SRe2L、RDED）的更细粒度比较。

- 声明：动态 momentum BN recalibration 确保每个样本（尤其是 tail class）对统计量贡献平等。
  证据：消融实验显示移除 recalibration 导致准确率下降 1-2%。
  范围：基于 BN 的 ConvNet 架构。
  置信度：medium。
  张力：对无 BN 架构（Transformer、LN-based）的适用性未知。

- 声明：confidence-guided multi-round initialization 在类别样本极度稀缺时保持蒸馏质量。
  证据：IPC=1 的极端设置下方法表现最强（CIFAR-100-LT: 31.8% vs. DAMED 7.8%）。
  范围：长尾图像数据集。
  置信度：high。

- 声明：statistical alignment 方法在计算效率上远超 trajectory matching。
  证据：总训练时间不到 DAMED 的 1/20，GPU 内存恒定 3.1GB。
  范围：长尾数据集蒸馏。
  置信度：high。

## 连接

- [Dataset Distillation](../concepts/dataset-distillation.md)：本文扩展的上位研究概念。
- [Long-Tailed Dataset Distillation](../topics/long-tailed-dataset-distillation.md)：不平衡蒸馏主题页。
- 方法层面的连接：statistical alignment 与 [SRe2L](https://arxiv.org/abs/2306.1) 和 [RDED](https://arxiv.org/abs/2405.0) 等 uni-level 蒸馏方法共享 recover-relabel 范式，但本文首次针对长尾分布系统性地 debias 了 expert model 和 BN 统计量。

## 开放问题

- dynamic momentum BN recalibration 是否适用于 LayerNorm 和 Transformer 架构？
- 去偏置后的 expert model 能否与 generative/diffusion-based 蒸馏方法结合？
- 多领域/联邦数据集蒸馏中，各 client 分布不同时的 statistical alignment 如何设计？
- 论文的 "uni-level" framing 与其他 uni-level 方法（SRe2L, RDED, EDC）在理论上的本质区别？
- 能否通过 optimal transport 等工具进一步改进 statistical alignment 的匹配质量？

## 来源

- [Canonical raw PDF](../../../../raw/sources/2025-12-14-rethinking-long-tailed-dataset-distillation.pdf)
- [arXiv abstract and metadata](https://arxiv.org/abs/2511.18858)
- [Code repository](https://github.com/2018cx/RLDD)
- PDF 正文已完整抽取，覆盖 introduction、method（三组件细节）、experiments（全部 10 个 tables）、ablation、efficiency comparison、conclusion 全部章节。
