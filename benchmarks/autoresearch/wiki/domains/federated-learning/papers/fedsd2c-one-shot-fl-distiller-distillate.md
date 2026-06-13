---
title: One-shot Federated Learning via Synthetic Distiller-Distillate Communication
type: paper
domain: federated-learning
status: active
created: 2026-05-08
updated: 2026-05-08
tags:
  - one-shot-fl
  - dataset-distillation
  - data-heterogeneity
  - privacy-preserving
  - fourier-transform
paper:
  title: One-shot Federated Learning via Synthetic Distiller-Distillate Communication
  authors:
    - Junyuan Zhang
    - Songhua Liu
    - Xinchao Wang
  year: 2024
  venue: NeurIPS 2024
  arxiv: ""
  doi: ""
  code: "https://github.com/Carkham/FedSD2C"
  project: ""
classification:
  label: federated-learning
  task:
    - one-shot federated learning
    - data heterogeneity
  method_family:
    - dataset distillation
    - Core-Set selection
    - knowledge distillation
  modality:
    - image
  datasets:
    - Tiny-ImageNet
    - ImageNette
    - OpenImage
    - COVID-FL
  metrics:
    - accuracy
    - PSNR
    - SSIM
evidence_level: full-paper
raw_sources:
  - raw/sources/2024-12-10-one-shot-fl-synthetic-distiller-distillate-communication.pdf
related_pages:
  - wiki/domains/federated-learning/concepts/federated-learning.md
  - wiki/domains/federated-learning/topics/federated-distillation-and-unlearning.md
  - wiki/domains/federated-learning/methods/fedsd2c.md
---

## Citation

Zhang, J., Liu, S., & Wang, X. (2024). One-shot Federated Learning via Synthetic Distiller-Distillate Communication. *Advances in Neural Information Processing Systems (NeurIPS 2024)*. National University of Singapore & Beihang University.

## One-Sentence Contribution

提出 FedSD2C——一种实用的一次性联邦学习框架，通过 V-information Core-Set 选择 + Fourier 变换扰动 + 预训练 Autoencoder 蒸馏，将本地数据端到端压缩为信息丰富、隐私增强、通信高效的合成蒸馏物（distillate），替代不一致的本地模型传输，解决基于 DFKD 的一次性联邦学习中的双层信息损失和数据异质性问题。

## Problem Setting

一次性联邦学习（One-shot FL）仅需单轮通信完成协作训练，显著降低通信成本和隐私风险。但现有主流方法基于无数据知识蒸馏（DFKD）：用 GAN 生成器从客户端模型集成中生成合成数据来训练服务端模型。这引入了**双层信息损失**：

1. **训练损失（数据→模型）**：受模型容量限制，客户端模型无法完全捕获本地数据的所有信息
2. **生成损失（模型→逆向数据）**：从随机噪声生成的数据无法充分表示模型中的信息

同时，数据异质性导致客户端模型预测不一致，在知识蒸馏中产生误导性信号（label noise）。这些问题在高分辨率复杂数据集上尤为严重。

## Method

**FedSD2C 三阶段流程**：

### 1. V-information Core-Set 选择

利用本地预训练模型作为观察者（observer $V$），从两个层级最大化 Core-Set 的 $\mathcal{V}$-information：
- **Patch 级**：从每张图像的多尺度 patches 中评估信息量
- **类别级**：对每个类别选择 top-ipc 具有最高 $\mathcal{V}$-information 的图像

目标函数：$(X_s, Y_s) = \arg\max_{X,Y} I_V(X_t \to Y_t)$

### 2. Fourier 变换扰动初始化

利用 Fourier 变换的性质——相位编码高层语义、振幅编码低层细节——对 Core-Set 样本的振幅分量进行扰动：

$$\hat{A}(x) = (1-\lambda)A(x) + \lambda A(x^*)$$

将扰动后的振幅与原相位组合做逆傅里叶变换，生成**语义保持、视觉模糊**的初始化样本。参数 $\lambda$ 控制隐私-性能权衡（默认 0.8）。

### 3. 预训练 Autoencoder 蒸馏

服务器预先分发预训练 VAE (Stable Diffusion) 给各客户端。客户端在紧凑的 latent space 中优化 distillate，使 decoded 图像与原始 Core-Set 的 $\mathcal{V}$-information 对齐：

$$L_{syn} = \left\|\frac{1}{N}\sum_{j=1}^N h_i(D(z_j)) - \frac{1}{N}\sum_{j=1}^N h_i(x_j)\right\|_2$$

最终上传 latent $Z_i$ + soft labels（由本地模型预测），服务器 decoder 重建后训练全局模型。

**隐私讨论**：攻击者无法获取预训练 VAE 的 encoder，难以从 latent 重建有效模型；Fourier 扰动结合 latent space 优化比直接加噪声或 FedMix 更平衡。

## Experiments

**数据集**：

| 数据集 | 分辨率 | 类别数 | 训练样本 | $\alpha$ 设置 |
|--------|--------|--------|----------|--------------|
| ImageNette | 128×128 | 10 | 9,469 | 0.1, 0.3, 0.5 |
| Tiny-ImageNet | 64×64 | 200 | 10,000 | 0.1, 0.3, 0.5 |
| OpenImage | 256×256 | - | 9M+ | FedScale 预定义划分 |
| COVID-FL | 医学图像 | - | - | 域迁移测试 |

**异质性模拟**：Dirichlet 分布 $\alpha \in \{0.1, 0.3, 0.5\}$（$\alpha$ 越小越异质），默认 $n=10$ clients

**模型**：ConvNet (128 通道, 3 层)、ResNet-18

**Baseline**：FedAVG、F-DAFL (DAFL + one-shot setting)、DENSE (NeurIPS 2022)、Co-Boosting (2024)

**蒸馏设置**：ipc = 50 (Tiny-ImageNet/ImageNette)，ipc = 10 (OpenImage)；$\lambda = 0.8$；预训练 Autoencoder = Stable Diffusion VAE；$T_{syn} = 50$，$\eta_{syn} = 0.1$

**Ablation 维度**：
- 隐私保护技术对比（Fourier $\lambda$ 扫描、Laplace/Gaussian 噪声、FedMix）
- 通信效率扩缩（ipc ∈ {1, 20, 50, 80}）
- 预训练 Autoencoder 影响（域迁移、随机初始化替代）
- 客户端规模扩缩（n ∈ {20, 50, 100}）
- 合成迭代数 $T_{syn}$ 影响

## Results

**主结果**（Table 1, ConvNet/ResNet-18）：

| 数据集 | $\alpha$ | 最佳 Baseline (Acc) | FedSD2C (Acc) | 提升 |
|--------|---------|---------------------|--------------|------|
| ImageNette | 0.1 (ConvNet) | F-DAFL 44.95 | **50.68** | 1.13× |
| ImageNette | 0.3 (ConvNet) | Co-Boosting 56.15 | **57.89** | +1.74 |
| ImageNette | 0.1 (ResNet-18) | DENSE 38.37 | **47.52** | 1.24× |
| Tiny-ImageNet | 0.1 (ConvNet) | DENSE 11.45 | **20.73** | 1.81× |
| Tiny-ImageNet | 0.1 (ResNet-18) | Co-Boosting 10.29 | **26.83** | **2.61×** |
| Tiny-ImageNet | 0.3 (ResNet-18) | Co-Boosting 14.35 | **29.92** | 2.08× |
| Tiny-ImageNet | 0.5 (ResNet-18) | DENSE 17.24 | **31.66** | 1.84× |
| OpenImage | - (ConvNet) | Co-Boosting 13.59 | **23.00** | 1.69× |
| OpenImage | - (ResNet-18) | DENSE 14.85 | **22.69** | 1.53× |

**关键观察**：FedSD2C 在所有设置下均超越所有 baseline，在极端异质（$\alpha=0.1$）和更复杂数据集上优势最大。

**隐私-性能权衡**（Table 2, ConvNet）：

| 方法 | ImageNette Acc | PSNR↓ | SSIM↓ | Tiny-ImageNet Acc |
|------|---------------|-------|-------|-------------------|
| 无保护 | 51.87 | - | - | 22.62 |
| **FedSD2C ($\lambda=0.8$)** | **50.68** | 16.42 | 50.80 | **20.85** |
| Laplace (p=0.1) | 48.61 | 24.02 | 81.66 | 21.50 |
| Laplace (p=0.2) | 45.61 | 20.05 | 73.13 | 19.32 |
| FedMix | 41.86 | 16.88 | 58.93 | 13.86 |

FedSD2C 在相近隐私保护水平（低 PSNR/SSIM）下保持最高准确率——Fourier 扰动比随机噪声和 FedMix 更有效地平衡隐私与性能。

**通信效率**（Table 3, ResNet-18）：
- 分享模型：44MB（DENSE/Co-Boosting）
- FedSD2C ipc=50：ImageNette **0.5MB**（1.1% of model），Tiny-ImageNet **2.1MB**（4.8% of model）
- 通信带宽允许时，ipc 从 20 增至 80：ImageNette 43.10→56.13 (+13.03%)

**预训练 Autoencoder 域迁移**（Fig 3a）：COVID-FL 医学数据域下 $T_{syn}=50$ 效果不佳，增至 1000 后恢复——预训练知识影响收敛速度，但可通过增加迭代弥补

**客户端规模**（Table 4, Tiny-ImageNet, ConvNet）：n=20→50→100 时，FedSD2C 准确率波动 <1%（21.92→21.48→20.34），baseline 方法下降 3-5%

**随机初始化 vs 预训练**（Fig 3b）：随机初始化的 encoder/decoder 通过增加 $T_{syn}$ 到 800-1000 可达到预训练版本同等性能，FedSD2C 不依赖特定预训练模型

## Limitations

1. 本地蒸馏引入额外计算开销——Core-Set 选择无需训练（约 0.4s/image），但 distillate 合成需 50 迭代
2. Fourier 扰动对低分辨率数据（CIFAR）的隐私保护效果可能有限，更适合高分辨率自然图像
3. 仅在小规模客户端设置验证（默认 n=10，最大 n=100），超大规模（n>1000）cross-device 场景未测
4. 预训练 Autoencoder 需服务器与客户端离线预定义——对特定域（如医学影像）可能需要域内预训练的 Autoencoder
5. 尚未在非视觉模态（文本/表格）上验证

## Reusable Claims

- Claim: 以端到端蒸馏的合成 distillate 替代不一致的客户端模型传输，可同时缓解 DFKD 的双层信息损失和数据异质性影响。
  Evidence: [FedSD2C](fedsd2c-one-shot-fl-distiller-distillate.md), Table 1—Tiny-ImageNet ResNet-18 上 2.6× Co-Boosting。
  Scope: one-shot FL on 视觉分类（ImageNette/Tiny-ImageNet/OpenImage），ConvNet + ResNet-18。
  Confidence: high.

- Claim: Fourier 变换振幅扰动比 Laplace/Gaussian 噪声和 FedMix 更有效地平衡隐私保护与模型性能——在相近 PSNR/SSIM 下准确率最高。
  Evidence: [FedSD2C](fedsd2c-one-shot-fl-distiller-distillate.md), Table 2。
  Scope: 视觉 one-shot FL，高分辨率自然图像。
  Confidence: medium.

- Claim: 预训练 Autoencoder 的 latent space 优化相当于正则化，使 distillate 更具泛化性；其域知识影响收敛速度但非必要条件——随机初始化可通过增加迭代达到同等性能。
  Evidence: [FedSD2C](fedsd2c-one-shot-fl-distiller-distillate.md), Fig 3a-b。
  Scope: 视觉数据域。
  Confidence: medium.

- Claim: 分享合成 distillate 的通信成本远低于分享模型参数（压缩至 MB 级 vs. 44MB），且支持带宽扩缩（更高的 ipc → 更高的准确率）。
  Evidence: [FedSD2C](fedsd2c-one-shot-fl-distiller-distillate.md), Table 3。
  Scope: one-shot FL，ResNet-18 架构。
  Confidence: high.

## Connections

- [Federated Learning](../../federated-learning/concepts/federated-learning.md)：联邦学习基础概念
- [Federated Distillation and Unlearning](../../federated-learning/topics/federated-distillation-and-unlearning.md)：联邦蒸馏与遗忘主题
- [DENSE (NeurIPS 2022)](#)：最直接 baseline——基于 DFKD 的 one-shot FL；FedSD2C 在 Tiny-ImageNet 上 2.6× DENSE
- [Co-Boosting (2024)](#)：DENSE 改进版——GAN + ensemble 双向增强；FedSD2C 全面超越
- 与 `distillation` 域的交叉：FedSD2C 使用了数据集蒸馏的 Core-Set 选择思想，但应用场景是联邦学习而非压缩训练

## Open Questions

1. 对非视觉模态（文本、表格、图数据）的适用性？
2. 超大规模跨设备场景（n>1000，每设备仅少量数据）下 Core-Set 选择的最小有效 ipc？
3. distillate 合成一次、永久复用的可行性（integration with model market）？
4. 差分隐私（DP）形式化保证与 Fourier 扰动的结合？
5. 多轮 FL 中 distillate 增量更新策略？
6. 对 adversarial clients（投毒攻击）的鲁棒性？

## Provenance

- 从 PDF `raw/sources/2024-12-10-one-shot-fl-synthetic-distiller-distillate-communication.pdf`（NeurIPS 2024，23 页）全文中提取。
- 全文阅读：包含方法描述（§3.1-3.3 + Algorithm 1）、主实验（Table 1）、隐私评估（Table 2）、通信效率（Table 3）、域迁移（Fig 3a）、客户端规模（Table 4）、Ab initio 替代（Fig 3b）、会员推断攻击防御（Appendix C.2）。
- 代码：https://github.com/Carkham/FedSD2C
