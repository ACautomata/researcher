---
title: "FedHD: Federated Distillation for Whole Slide Image via Gaussian-Mixture Feature Alignment and Curriculum Integration"
type: paper
domain: federated-learning
status: active
created: 2026-05-05
updated: 2026-05-05-evidence-upgrade
tags:
  - federated-learning
  - dataset-distillation
  - whole-slide-image
  - digital-pathology
  - gaussian-mixture
  - curriculum-learning
paper:
  title: "Federated Distillation for Whole Slide Image via Gaussian-Mixture Feature Alignment and Curriculum Integration"
  authors:
    - Luru Jing
    - Cong Cong
    - Yanyuan Chen
    - Yongzhi Cao
  year: 2026
  venue: ICML 2026
  arxiv: "2605.00578v1"
  doi: ""
  code: ""
  project: ""
classification:
  label: federated-learning
  task:
    - whole slide image classification
  method_family:
    - dataset distillation
    - gaussian-mixture alignment
    - curriculum learning
  modality:
    - histopathology images
  datasets:
    - TCGA-IDH
    - CAMELYON16
    - CAMELYON17
  metrics:
    - classification accuracy
evidence_level: full-paper
raw_sources:
  - raw/sources/2026-05-01-fedhd-federated-distillation-wsi.pdf
source_pages:
  - wiki/domains/federated-learning/concepts/federated-learning.md
  - wiki/domains/distillation/concepts/dataset-distillation.md
related_pages:
  - wiki/domains/federated-learning/methods/fedhd.md
---

# FedHD: Federated Distillation for Whole Slide Image via Gaussian-Mixture Feature Alignment and Curriculum Integration

## Citation

Jing et al., "Federated Distillation for Whole Slide Image via Gaussian-Mixture Feature Alignment and Curriculum Integration," accepted at ICML 2026. arXiv:2605.00578v1.

## One-Sentence Contribution

提出 FedHD——首个面向全切片图像的联邦数据集蒸馏框架：用高斯混合对齐替代均值匹配以捕捉 WSI 的多组分形态学分布，onetone 蒸馏策略保留诊断多样性，课程联邦策略逐步融合跨机构合成特征。

## Problem Setting

真实医疗联邦学习中，不同机构使用异构特征提取器和异构 MIL 架构——导致模型参数空间不兼容，传统加权平均 FL 不适用。现有 FedDD 尝试共享合成数据集替代模型参数，但在 WSI 场景失效：
- **Mean-matching 对齐不适用**：WSI 的 patch feature 服从多组分分布而非单峰分布。
- **过度压缩**：将数千 patch 压缩为少数合成样本会丢弃细粒度诊断线索。
- **domain shift**：合成数据的直接融合可能导致跨机构分布偏移。

## Method

FedHD 三大创新：

1. **Gaussian-Mixture Feature Alignment**：将 patch feature space 建模为高斯混合，对真实和合成数据在对齐均值和每个组件的协方差——同时捕捉 intra-slide heterogeneity。
2. **One-to-One Feature Distillation**：为每张真实 slide 生成一个合成 counterpart（而非压缩多张 slide 为几个样本），保留 slide 级诊断多样性。直接在 patch embedding 上操作（与 MIL pipeline 天然对齐）。
3. **Curriculum Federation Strategy**：
   - 阶段 1：每个客户端用真实数据优化其 MIL 模型至稳定收敛。
   - 阶段 2：当本地性能饱和后，逐步引入来自其他客户端的合成数据作为辅助监督——在缓解 domain shift 的同时增强泛化。
4. **Optional Interpretation Module**：从合成 embedding 重建 pseudo-patches，增强透明度。

## Experiments

**数据集**

- **CAMELYON16**：乳腺癌二分类（正常 vs. 肿瘤），399 张 WSI，来自 RUMC (C1) 和 UMCU (C2) 两个中心。C1 训练集 169 张（99 正常/70 肿瘤）、测试集 74 张（50/24）；C2 训练集 101 张（60/41）、测试集 55 张（31/24）。使用官方训练/测试切分，5 个随机种子重复测试。
- **CAMELYON17**：乳腺癌转移四分类（neg/itc/micro/macro），5 个中心 (C1-C5) 各 20 名患者、每患者 5 张 slide。5 折交叉验证，同一患者 slide 不跨折。
- **TCGA-IDH**：胶质瘤 IDH 突变状态二分类（WT/MU），8 个中心共 1016 张 WSI。5 折交叉验证。

**训练配置**

- Patch 大小：256×256，CAMELYON16/17 在 40× 放大倍率，TCGA-IDH 在 10×。
- 单轮通信协议：每个客户端本地蒸馏 1000 次迭代 → 上传蒸馏 slide → 接收全局合成集后本地训练 50 epochs。
- 合成特征随机初始化，T=1000 patch embeddings/张，高斯混合组件 M=16，q=0.7 (GCE loss)，t₀=30（课程阈值）。
- PyTorch 实现，NVIDIA A100 GPU。

**异构设定**

- 特征提取器池：ResNet50 (ImageNet pretrained) + UNI + PhikonV2 + GPFM（3 个病理基础模型）。
- MIL 模型池：CLAM + TransMIL + ACMIL。
- 每个客户端随机选取一对特征提取器 + MIL 模型。

**Baselines**

FedHE、DESA、FedDGM、HistoFS、FedWSIDD（5 个个性化 FL 方法）。

**评估指标**

- 测试准确率 (Acc) 和 Matthews Correlation Coefficient (MCC)，报告客户端加权全局平均和各客户端独立结果。

## Results

**主实验 (Table 1)**

在异构本地模型设定下 FedHD 全面最优：

- **CAMELYON16**：Avg Acc 91.2% / MCC 80.6，比最强基线 FedWSIDD (88.7%/75.3) 提升 +2.5% Acc、+5.3 MCC。C2 客户端 (UNI+TransMIL) 上 Acc 95.8%/MCC 91.8，FedWSIDD 为 93.2%/86.8。
- **CAMELYON17**：Avg Acc 82.7% / MCC 62.3，比 FedWSIDD (77.2%/52.0) 大幅领先。C5 (GPFM+CLAM) 上 Acc 87.2%/MCC 75.8。
- **TCGA-IDH**：Avg Acc 84.8% / MCC 57.0，比 FedWSIDD (80.5%/47.0) 提升 +4.3% Acc、+10.0 MCC。C8 (PhikonV2+CLAM) 上 Acc 88.4%/MCC 46.8 vs. FedWSIDD 85.3%/34.5。
- 配对 t 检验验证大多数客户端上 FedHD 对第二名的提升具有统计显著性 (p < 0.05)。

**通信与训练效率**

- 以 TCGA-IDH C1 (313 张训练 slide) 为基准：FedWSIDD 传输合成 patch 图像约 49.2 MB/轮；FedHD 无 O2O 策略时 39 MB（10 张合成 slide × 1000 embeddings × 1024 维），O2O 启用时约 1.19 GB。
- FedHD 特征级蒸馏 1000 轮约 1 小时，而图像级蒸馏需 10-12 小时（单 A100）。

**Ablation (Table 2)**

| 配置 | CAM16 Acc/MCC | CAM17 Acc/MCC | IDH Acc/MCC |
|------|--------------|--------------|-------------|
| Baseline | 88.7/75.3 | 77.2/52.0 | 80.5/47.0 |
| +FDD | 89.7/77.6 | 78.8/54.5 | 82.1/49.8 |
| +GMA | 89.4/77.1 | 79.9/57.1 | 83.4/52.4 |
| +CBF | 90.3/78.5 | 80.7/58.5 | 83.9/55.1 |
| +FDD&O2O | 90.6/79.2 | 81.2/60.0 | 84.0/54.3 |
| +FDD&GMA&O2O | 91.2/80.3 | 81.9/61.3 | 84.6/56.6 |
| +All | 91.2/80.6 | 82.7/62.3 | 84.8/57.0 |

- FDD（特征级蒸馏）替换像素生成立即带来精度和效率增益；O2O 保留 slide 级诊断多样性；GMA 改善合成-真实特征分布对齐质量；CBF（课程联邦）进一步提升并增强可解释性。

**隐私分析 (Table 3)**

LiRA membership inference attack 结果 (Max AUC / Mean AUC)：

- CAM16: FedWSIDD 52.7/52.9 → FedHD 51.8/51.5
- CAM17: FedWSIDD 57.6/54.2 → FedHD 56.7/53.0
- IDH: FedWSIDD 60.1/56.1 → FedHD 54.7/52.3

FedHD 在所有三个数据集上均取得更低 MIA AUC，PPR 模块未引入额外隐私泄露。

## Limitations

- Gaussian-mixture 的组件数量 K 需要预定义或手动选择（对未知数据分布可能是超参数敏感）。
- One-to-one distillation 意味着合成集大小线性增长（虽然蒸馏后存储远小于原始 WSI）。
- 跨机构间合成数据的可解释性（即使有 interpretation module）仍受限于 embedding-to-patch 重建的保真度。

## Reusable Claims

- 声明：WSI 蒸馏需要多组分分布对齐——均值匹配因无法捕捉多模态 patch feature 的多组分性质而失败。
  证据：FedHD 的 GM alignment vs. mean-matching 比较实验（TCGA-IDH、CAMELYON16、CAMELYON17）。
  范围：WSI / histopathology image 数据集蒸馏。
  置信度：medium。

- 声明：onetone 蒸馏（每 slide 一个 counterpart）在小规模 WSI 数据集中优于最大压缩策略，因为保留 slide 级诊断多样性比压缩效率更重要。
  证据：FedHD vs. 传统最大压缩 FedDD 实验。
  范围：样本量小、类内差异大的 WSI 场景。
  置信度：medium。

## Connections

- [Federated Distillation and Unlearning](../topics/federated-distillation-and-unlearning.md)：本论文与 EASE 的统一分析——蒸馏和遗忘共享 cross-modal coupling 这一技术核心。
- [Dataset Distillation](../../distillation/concepts/dataset-distillation.md)：FedHD 是 DD 在联邦 WSI 设定中的扩展——从集中式 single-model DD 迁移到联邦异构模型场景。
- [Multi-Modal Dataset Distillation](../../distillation/topics/multimodal-dataset-distillation.md)：虽不是 image-text multimodal，但 FedHD 的 GM alignment 可与 ProCo 的 correspondence coverage 议题交叉（如何在压缩中保留多组分语义多样性）。
- [Federated Learning](../concepts/federated-learning.md)：架构无关的 FL 范式。

## Open Questions

- Gaussian-mixture component count 的自动选择方法。
- 与其他 FedDD 方法（FedDM、FedDGM）在 WSI 场景的直接比较。
- 跨癌种（TCGA pan-cancer）的泛化性。

## Provenance

- 摄入时间：2026-05-05。
- 原始来源：[raw/sources/2026-05-01-fedhd-federated-distillation-wsi.pdf](../../../raw/sources/2026-05-01-fedhd-federated-distillation-wsi.pdf)。
- 证据等级：full-paper（完整实验数据从 PDF 提取，包含 Table 1-3 定量结果和 ablation）。
