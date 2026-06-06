# VPT 实验深化提取

## 0. 文档定位

- **输入材料**：`materials/vpt_full.md`（VPT 论文全文，arXiv 2203.12119，35页）
- **当前阶段**：S2 实验深化提取
- **包含**：实验目标、实验设置、主结果、消融实验、参数分析、效率代价、鲁棒性泛化性、实验现象、证据充分性
- **不包含**：完整问题挖掘、最终结论、方法改进方案（留待 S3/S4/S5）

---

## 1. 实验目标与作者想验证的核心结论

### 核心结论 1：VPT-Deep 在全量微调之外胜出 Full Fine-Tuning

- **对应实验**：Table 1（ViT-B/16 上 24 个下游任务）
- **证据**：VPT-Deep 在 20/24 个任务上超过 Full，同时仅使用不到 1% 的可训练参数。参数量为 Full 的 1.18×（多任务总存储）vs Full 的 24.02×

### 核心结论 2：VPT 是所有参数高效微调方法中的最优方案

- **对应实验**：Table 1（VPT vs Linear / Partial / Mlp / Sidetune / Bias / Adapter）
- **证据**：VPT-Deep 在 4 个任务组（FGVC、VTAB-Natural、Specialized、Structured）的所有分组中均超越所有其他参数高效方法（b、c 组）

### 核心结论 3：VPT 在小数据场景下尤其有效

- **对应实验**：Figure 3（FGVC 数据规模消融，10%~80% 训练数据）
- **证据**：VPT-Deep 在所有数据规模下均超越 Full，而 Linear 和 Adapter 仅在低数据区域占优

### 核心结论 4：VPT 的优势在不同模型规模下保持

- **对应实验**：Figure 4（ViT-B/L/H 三种规模）
- **证据**：VPT-Deep 在 Natural 和 Structured 组显著超越 Full，在 Specialized 组性能相当

### 核心结论 5：VPT 可迁移至层次化 Transformer 架构（Swin）

- **对应实验**：Table 2（Swin-B + VTAB-1k）
- **证据**：VPT-Deep/Shallow 在所有三组 VTAB 任务上优于其他参数高效方法

### 核心结论 6：Prompt 深度与性能正相关，早期层 Prompt 更重要

- **对应实验**：Figure 7（prompt depth 消融）、Figure 14
- **证据**：插入更多 Transformer 层的 Prompt 效果越好；从底层到顶层插入优于从顶层到底层

### 核心结论 7：预训练目标对 VPT 效果有显著影响

- **对应实验**：Table 4（MAE、MoCo v3 自监督预训练）
- **证据**：在 MAE 和 MoCo v3 上 VPT 不再保持最优，表现不如 Partial-1 等方法

---

## 2. 实验设置总览

### 数据集

#### 细粒度视觉分类（FGVC）— 5 个数据集

| 数据集 | 类别数 | 训练集 | 验证集 | 测试集 | 来源 |
|--------|--------|--------|--------|--------|------|
| CUB-200-2011 | 200 | 5,394* | 600* | 5,794 | Wah et al., 2011 |
| NABirds | 555 | 21,536* | 2,393* | 24,633 | Van Horn et al., 2015 |
| Oxford Flowers | 102 | 1,020 | 1,020 | 6,149 | Nilsback & Zisserman, 2008 |
| Stanford Dogs | 120 | 10,800* | 1,200* | 8,580 | Khosla et al., 2011 |
| Stanford Cars | 196 | 7,329* | 815* | 8,041 | Gebru et al., 2017 |

*仅公开 train/test 的数据集，将训练集随机分为 90%/10% 作为 train/val

#### VTAB-1k — 19 个分类任务（每组 1000 训练样本，800/200 用于超参选择/评估）

| 分组 | 数据集 | 类别数 | 训练集(最终) | 验证集 | 测试集 | 来源 |
|------|--------|--------|-------------|--------|--------|------|
| Natural (7) | CIFAR-100 | 100 | 1,000 | 200 | 10,000 | Krizhevsky et al., 2009 |
| | Caltech101 | 102 | 1,000 | 200 | 6,084 | Li et al., 2006 |
| | DTD | 47 | 1,000 | 200 | 1,880 | Cimpoi et al., 2014 |
| | Flowers102 | 102 | 1,000 | 200 | 6,149 | Nilsback & Zisserman, 2008 |
| | Pets | 37 | 1,000 | 200 | 3,669 | Parkhi et al., 2012 |
| | SVHN | 10 | 1,000 | 200 | 26,032 | Netzer et al., 2011 |
| | Sun397 | 397 | 1,000 | 200 | 21,750 | Xiao et al., 2010 |
| Specialized (4) | Patch Camelyon | 2 | 1,000 | 200 | 32,768 | Veeling et al., 2018 |
| | EuroSAT | 10 | 1,000 | 200 | 5,400 | Helber et al., 2019 |
| | Resisc45 | 45 | 1,000 | 200 | 6,300 | Cheng et al., 2017 |
| | Retinopathy | 5 | 1,000 | 200 | 42,670 | Kaggle, 2015 |
| Structured (8) | Clevr/count | 8 | 1,000 | 200 | 15,000 | Johnson et al., 2017 |
| | Clevr/distance | 6 | 1,000 | 200 | 15,000 | Johnson et al., 2017 |
| | DMLab | 6 | 1,000 | 200 | 22,735 | Beattie et al., 2016 |
| | KITTI/distance | 4 | 1,000 | 200 | 711 | Geiger et al., 2013 |
| | dSprites/location | 16 | 1,000 | 200 | 73,728 | Matthey et al., 2017 |
| | dSprites/orientation | 16 | 1,000 | 200 | 73,728 | Matthey et al., 2017 |
| | SmallNORB/azimuth | 18 | 1,000 | 200 | 12,150 | LeCun et al., 2004 |
| | SmallNORB/elevation | 9 | 1,000 | 200 | 12,150 | LeCun et al., 2004 |

来源：Table 7，Appendix D

#### 语义分割

| 数据集 | 描述 | 训练集 | 验证集 | 来源 |
|--------|------|--------|--------|------|
| ADE20K | 场景解析（150 类别） | 20,210 | 2,000 | Zhou et al., 2019 |

来源：Section A.2

### 预训练 Backbone

| Backbone | 预训练目标 | 预训练数据 | 参数量(M) | 特征维度 d | 来源 |
|----------|-----------|-----------|-----------|----------|------|
| ViT-B/16 | 监督 | ImageNet-21k | 85 | 768 | Dosovitskiy et al., 2020 |
| ViT-L/16 | 监督 | ImageNet-21k | 307 | 1024 | Dosovitskiy et al., 2020 |
| ViT-H/14 | 监督 | ImageNet-21k | 630 | 1280 | Dosovitskiy et al., 2020 |
| ViT-B/16 | MAE (自监督) | ImageNet-1k | 85 | 768 | He et al., 2022 |
| ViT-B/16 | MoCo v3 (自监督) | ImageNet-1k | 85 | 768 | Chen* et al., 2021 |
| Swin-B | 监督 | ImageNet-21k | 88 | 1024 | Liu et al., 2021 |
| ConvNeXt-B | 监督 | ImageNet-21k | 88 | 1024 | Liu et al., 2022 |
| ResNet-50 | 监督 | ImageNet-1k | 23 | 2048 | He et al., 2016 |

来源：Table 8，Section 4.1

### Baseline 方法

| 方法 | 类型 | 调优范围 | 额外参数 | 说明 |
|------|------|---------|---------|------|
| Full | 全量微调 | 全部 backbone + head | 否 | 存储 24.02× 总参数量 |
| Linear | Head-only | 仅线性分类头 | 否 | backbone 冻结为特征提取器 |
| Partial-k | Head + 部分 backbone | 最后 k 层 + head | 否 | 文中 Partial-1 |
| Mlp-k | Head-only | MLP 头 | 是(k层MLP) | 文中 Mlp-2,3,5,9 |
| Sidetune | 附加网络 | side network + head | 是 | 线性插值预训练+side 特征 |
| Bias (BitFit) | Backbone 子集 | 仅偏置项 + head | 否 | 更新 backbone 所有 bias |
| Adapter | 附加模块 | adapter + head | 是 | 每层插入 MLP (reduction rate r) |
| VPT-shallow | 输入空间 | 第 1 层 prompt + head | 是(p 个 prompt) | p ∈ {1,5,10,50,100,200} |
| VPT-deep | 输入空间 | 所有层 prompt + head | 是(p 个/层) | p ∈ {1,5,10,50,100,200} |

来源：Section 4.1

### 训练配置

| 配置项 | Full / Partial / Bias / Adapter | Linear / Sidetune / Mlp / VPT |
|--------|-------------------------------|-------------------------------|
| 优化器 | AdamW | SGD |
| SGD momentum | — | 0.9 |
| base lr 搜索范围 | {0.001, 0.0001, 0.0005, 0.005} | {50., 25., 10., 5., 2.5, 1., 0.5, 0.25, 0.1, 0.05} |
| Weight decay 搜索范围 | {0.01, 0.001, 0.0001, 0.0} |
| 学习率调整 | cosine decay | cosine decay |
| Warmup epochs | 10 | 10 |
| 总 epoch | 100 (ViT-B, Swin-B), 50 (ViT-L/H) | 同等 |
| 图片分辨率 | 224×224（默认），384×384（附加） | 同等 |
| 数据增强 | ImageNet 标准化 + 随机裁剪 224×224 + 随机水平翻转（FGVC）/ 仅 resize 至 224×224（VTAB-1k） | 同等 |

来源：Table 6，Section A.1

**线性缩放规则**：lr = base_lr × batch_size / 256

**Batch size**（按 Linear / Partial / {Full, Bias, Adapter} / VPT(p<100) / VPT(p≥100)）：

| Backbone | Batch Size |
|----------|-----------|
| ViT-B/16 | 2048 / 1280 / 128 / 128 / 64 |
| ViT-L/16 | 2048 / 640 / 64 / 64 / 32 |
| ViT-H/14 | 1024 / 240 / 28 / 28 / 14 |

来源：Table 8

### 外部实现细节

- **框架**：PyTorch，NVIDIA A100-40GB GPU
- **VPT Prompt 初始化**：xavier uniform 初始化
- **VPT Dropout**：VPT-Deep 上应用 dropout=0.1
- **Prompt 长度搜索**：ViT 上 p∈{1,5,10,50,100,200}，Swin 上 p∈{1,5,10,50}，ConvNet 上 p∈{1,3,5,7,9,11}
- **Adapter 缩减率搜索**：r∈{8,64,256}
- **VPT-shallow 特殊学习率**：6/24 任务上从 {1000.0, 500.0, 250.0, 100.0} 搜索较大 base_lr

来源：Section A.1

---

## 3. 主结果提取

### 3.1 ViT-B/16 监督预训练（ImageNet-21k）— 24 个下游任务（Table 1）

#### FGVC 平均（5 个任务）

| 方法 | 平均准确率 | vs Full 胜场数 |
|------|-----------|---------------|
| Full | 88.54 | — |
| Linear | 79.32 | 0 |
| Partial-1 | 82.63 | 0 |
| Mlp-3 | 79.80 | 0 |
| Sidetune | 78.35 | 0 |
| Bias | 88.41 | 3 |
| Adapter | 85.66 | 2 |
| **VPT-shallow** | 84.62 | 1 |
| **VPT-deep** | **89.11** | **4** |

来源：Table 1，Page 7

#### VTAB-Natural 平均（7 个任务）

| 方法 | 平均准确率 | vs Full 胜场数 |
|------|-----------|---------------|
| Full | 75.88 | — |
| Linear | 68.93 | 1 |
| Partial-1 | 69.44 | 2 |
| Mlp-3 | 67.80 | 2 |
| Sidetune | 58.21 | 0 |
| Bias | 73.30 | 3 |
| Adapter | 70.39 | 4 |
| **VPT-shallow** | 76.81 | 4 |
| **VPT-deep** | **78.48** | **6** |

来源：Table 1，Page 7

#### VTAB-Specialized 平均（4 个任务）

| 方法 | 平均准确率 | vs Full 胜场数 |
|------|-----------|---------------|
| Full | 83.36 | — |
| Linear | 77.16 | 1 |
| Partial-1 | 78.53 | 0 |
| Mlp-3 | 72.83 | 0 |
| Sidetune | 68.12 | 0 |
| Bias | 78.25 | 0 |
| Adapter | 77.11 | 0 |
| **VPT-shallow** | 79.66 | 0 |
| **VPT-deep** | **82.43** | **2** |

来源：Table 1，Page 7

#### VTAB-Structured 平均（8 个任务）

| 方法 | 平均准确率 | vs Full 胜场数 |
|------|-----------|---------------|
| Full | 47.64 | — |
| Linear | 26.84 | 0 |
| Partial-1 | 34.17 | 0 |
| Mlp-3 | 30.62 | 0 |
| Sidetune | 23.41 | 0 |
| Bias | 44.09 | 2 |
| Adapter | 33.43 | 0 |
| **VPT-shallow** | 46.98 | 4 |
| **VPT-deep** | **54.98** | **8** |

来源：Table 1，Page 7

**关键数字**：
- VPT-Deep 在 20/24 个任务上超越 Full（胜率 83.3%），参数量仅为 Full 的 1.18× vs 24.02×
- VPT-Deep 在 VTAB-Structured 组上 8/8 任务全胜，平均提升 **+7.34**（54.98 vs 47.64）
- VPT-Deep 在所有 4 个任务组中均优于其他所有参数高效方法
- VPT-Deep 可训练参数不足 backbone 的 1%（FGVC 平均 0.98%，VTAB 平均 1.14%）

来源：Table 1，Figure 1(c)，Page 7

### 3.2 VTAB-1k 逐任务结果（Table 13，ViT-B/16 监督预训练）

#### Natural 组逐任务

| 任务 | VPT-Deep | VPT-Shallow | Full | 最佳参数高效 |
|------|---------|------------|------|-------------|
| CIFAR-100 | **78.8** | 77.7 | 68.9 | VPT-Deep |
| Caltech101 | **90.8** | 86.9 | 87.7 | VPT-Deep |
| DTD | **65.8** | 62.6 | 64.3 | VPT-Deep |
| Flowers102 | **98.0** | 97.5 | 97.2 | VPT-Deep |
| Pets | **88.3** | 87.3 | 86.9 | VPT-Deep |
| SVHN | 78.1 | 74.5 | **87.4** | VPT-Deep(Bias 59.9) |
| Sun397 | **49.6** | 51.2(Full优于shallow) | 38.8 | VPT-Deep |
| **Mean** | **78.48 (6)** | 76.81 (4) | 75.88 | — |

来源：Table 13，Page 29

#### Specialized 组逐任务

| 任务 | VPT-Deep | VPT-Shallow | Full | 最佳参数高效 |
|------|---------|------------|------|-------------|
| Patch Camelyon | **81.8** | 78.2 | 79.7 | VPT-Deep |
| EuroSAT | **96.1** | 92.0 | 95.7 | VPT-Deep |
| Resisc45 | 83.4 | 75.6 | **84.2** | VPT-Deep(Bias 72.9) |
| Retinopathy | 68.4 | 72.9 | **73.9** | VPT-Shallow |
| **Mean** | **82.43 (2)** | 79.66 (0) | 83.36 | — |

来源：Table 13，Page 29

#### Structured 组逐任务

| 任务 | VPT-Deep | VPT-Shallow | Full | 最佳参数高效 |
|------|---------|------------|------|-------------|
| Clevr/count | **68.5** | 50.5 | 56.3 | VPT-Deep |
| Clevr/distance | **60.0** | 58.6 | 58.6 | VPT-Deep |
| DMLab | **46.5** | 40.5 | 41.7 | VPT-Deep |
| KITTI/distance | **72.8** | 67.1 | 65.5 | VPT-Deep |
| dSprites/location | **73.6** | 68.7 | 57.5 | VPT-Deep |
| dSprites/orientation | **47.9** | 36.1 | 46.7 | VPT-Deep |
| SmallNORB/azimuth | **32.9** | 20.2 | 25.7 | VPT-Deep |
| SmallNORB/elevation | **37.8** | 34.1 | 29.1 | VPT-Deep |
| **Mean** | **54.98 (8)** | 46.98 (4) | 47.64 | — |

来源：Table 13，Page 29

### 3.3 FGVC 逐任务结果（Table 14，ViT-B/16）

| 任务 | VPT-Deep | VPT-Shallow | Full | 最佳参数高效 |
|------|---------|------------|------|-------------|
| CUB-200-2011 | **88.5** | 86.7 | 87.3 | VPT-Deep（Bias 88.4 次优） |
| NABirds | **84.2** | 78.8 | 82.7 | VPT-Deep（Bias 84.2 并列） |
| Oxford Flowers | **99.0** | 98.4 | 98.8 | VPT-Deep |
| Stanford Dogs | **90.2** | 90.7 | 89.4 | VPT-Shallow |
| Stanford Cars | 83.6 | 68.7 | **84.5** | VPT-Deep（Bias 79.4 次优） |
| **Mean** | **89.11 (4)** | 84.62 (1) | 88.54 | — |

来源：Table 14，Page 29

### 3.4 Swin-B 监督预训练（ImageNet-21k）— 19 个 VTAB-1k 任务（Table 2）

| 方法 | Natural (7) | Specialized (4) | Structured (8) | Total params |
|------|------------|----------------|----------------|-------------|
| Full | 79.10 | 86.21 | 59.65 | 19.01× |
| Linear | 73.52 (5) | 80.77 (0) | 33.52 (0) | 1.01× |
| Mlp-3 | 73.56 (5) | 75.21 (0) | 35.69 (0) | 1.47× |
| Partial-1 | 73.11 (4) | 81.70 (0) | 34.96 (0) | 3.77× |
| Bias | 74.19 (2) | 80.14 (0) | 42.42 (0) | 1.06× |
| **VPT-shallow** | **79.85 (6)** | 82.45 (0) | 37.75 (0) | 1.01× |
| **VPT-deep** | 76.78 (6) | **84.53 (0)** | **53.35 (0)** | 1.05× |

来源：Table 2，Page 9

**关键发现**：
- Swin-B 上 Full 整体最优（但参数量 19.01×），VPT 在所有参数高效方法中仍最优
- VPT-Deep 在 Structured 组大幅领先其他参数高效方法（53.35 vs 第二 42.42）
- VPT-Shallow 在 Natural 组出人意料地优于 VPT-Deep（79.85 vs 76.78）
- 论文未提供 Swin-B 上 VPT 击败 Full 的具体任务数（仅 report vs Full 的胜场数括号值）

来源：Section 4.2, Page 9

### 3.5 不同预训练目标（Table 4，ViT-B/16）

#### MAE 预训练

| 方法 | Natural (7) | Specialized (4) | Structured (8) |
|------|------------|----------------|----------------|
| Full | 59.29 | 79.68 | 53.82 |
| Linear | 18.87 (0) | 53.72 (0) | 23.70 (0) |
| Partial-1 | 58.44 (5) | 78.28 (1) | 47.64 (1) |
| Bias | 54.55 (1) | 75.68 (1) | 47.70 (0) |
| Adapter | 54.90 (3) | 75.19 (1) | 38.98 (0) |
| VPT-shallow | 39.96 (1) | 69.65 (0) | 27.50 (0) |
| **VPT-deep** | 36.02 (0) | 60.61 (1) | 26.57 (0) |

#### MoCo v3 预训练

| 方法 | Natural (7) | Specialized (4) | Structured (8) |
|------|------------|----------------|----------------|
| Full | 71.95 | 84.72 | 51.98 |
| Linear | 67.46 (4) | 81.08 (0) | 30.33 (0) |
| Partial-1 | 72.31 (5) | 84.58 (2) | 47.89 (1) |
| Bias | 72.89 (3) | 81.14 (0) | 53.43 (4) |
| Adapter | 74.19 (4) | 82.66 (1) | 47.69 (2) |
| VPT-shallow | 67.34 (3) | 82.26 (0) | 37.55 (0) |
| **VPT-deep** | 70.27 (4) | 83.04 (0) | 42.38 (0) |

来源：Table 4，Page 13

**关键发现**：
- 在 MAE 上 VPT 效果很差，VPT-deep 的 Natural 为 36.02 vs Full 59.29，甚至不如 Linear
- 在 MoCo v3 上 VPT 具有竞争力但非最优，Bias 和 Partial-1 表现更好
- 说明自监督预训练 ViT 与监督预训练 ViT 在 VPT 行为上存在根本性差异

### 3.6 语义分割：ADE20K（Table 3，SETR-PUP on ViT-L/16）

| 方法 | mIoU-SS | mIoU-MS | Tunable params (M) |
|------|---------|---------|-------------------|
| Full (SETR) | 48.31 | 50.07 | 318.31 |
| Head Only | 35.12 | 37.46 | 13.18 |
| Bias | 43.40 | 45.33 | 13.46 |
| VPT-deep | 42.11 | 44.06 | 13.43 |
| VPT+Bias | 44.04 | 45.63 | 15.79 |
| ResNet-101 Full (DeepLab v3+) | 45.47 | 46.27 | 63.0 |

来源：Table 3，Page 13

**关键发现**：
- VPT 在分割任务上无法接近 Full（42.11 vs 48.31），但以远少参数量（13.43M vs 318.31M）接近 ResNet-101 全量微调（45.47）
- VPT+Bias 组合（44.04）略优于 VPT 单独（42.11），但仍然显著低于 Full

### 3.7 VPT 在 ConvNet 上（Table 5）

#### ConvNeXt-B（ImageNet-21k 监督预训练）

| 方法 | Natural (7) | Specialized (4) | Structured (8) |
|------|------------|----------------|----------------|
| Full | 77.97 | 83.71 | 60.41 |
| Linear | 74.48 (5) | 81.50 (0) | 34.76 (1) |
| Partial-1 | 73.76 (4) | 81.64 (0) | 39.55 (0) |
| Bias | 69.07 (2) | 72.81 (0) | 25.29 (0) |
| **VPT** | **78.48 (6)** | **83.00 (1)** | 44.64 (1) |

来源：Table 5，Page 14

#### ResNet-50（ImageNet-1k 监督预训练）

| 方法 | Natural (7) | Specialized (4) | Structured (8) |
|------|------------|----------------|----------------|
| Full | 59.72 | 76.66 | 54.08 |
| Linear | 63.75 (6) | 77.60 (3) | 30.96 (0) |
| Partial-1 | 64.34 (6) | 78.64 (2) | 45.78 (1) |
| Bias | 63.51 (6) | 77.22 (2) | 33.39 (0) |
| **VPT** | 66.25 (6) | 77.32 (2) | 37.52 (0) |

来源：Table 5，Page 14

**关键发现**：
- ConvNeXt-B 上 VPT 在 Natural 组 6/7 任务超越 Full，Structured 组显著落后于 Full（44.64 vs 60.41）
- ResNet-50 上 VPT 无明显优势，无方法在所有 19 个任务上成为明确优胜者

---

## 4. 消融实验提取

### 消融 1：Prompt 位置（Figure 5）

- **消融内容**：Prompt 插入方式的 4 种变体对比
- **测试变体**：
  - **Prepend（默认）**：在每层输入的 patch embedding 序列前拼接 prompt
  - **Add**：将 prompt 逐元素加到 patch embedding 上（不改变序列长度）
  - **Prepend-pixel**：在 Embed 层之前的像素空间直接拼接 prompt patch
  - **Concat-channel**：在输入图像的通道维度拼接额外通道
- **揭示结果**：
  - Prepend（默认）在几乎所有情况下最优
  - Add 在某些情况下（VTAB-Natural/Shallow 下 74.0）具有竞争力，但总体不如 Prepend
  - Prepend-pixel 性能下降显著（Natural 组相比默认下降 6.9%）
  - Concat-channel 性能最差，Natural 组准确率下降最高达 30 分
  - 结论：在 latent 输入空间学习 task-dependent signal 比在像素空间更容易
- **来源**：Figure 5，Page 10

### 消融 2：Prompt 长度（Figure 6）

- **消融内容**：VPT-Deep 的 prompt 数量 p 的影响
- **测试变体**：p ∈ {1, 5, 10, 50, 100, 200}
- **揭示结果**：
  - 最优 prompt 长度因任务而异
  - 即便 p=1（仅 1 个 prompt），VPT-Deep 仍显著优于 Adapter 和 MLP 基线
  - p=1 的 VPT-Deep 在 VTAB-Structured 和 Natural 上仍优于或接近 Full
- **来源**：Figure 6，Page 11

### 消融 3：Prompt 深度（Figure 7，Figure 14）

- **消融内容**：插入 prompt 的 Transformer 层范围
- **测试变体**：1→12（全部12层），12→1（反向），9→12（仅3层，从9到12），12→9（反向），6→12（从6到12），12→6（反向），3→12（从3到12），12→3（反向），1→1（仅第1层）等
- **揭示结果**：
  - VPT 性能与 prompt 深度正相关——插入越多层效果越好
  - 从底层（靠近输入）到顶层插入优于从顶层到底层插入，说明早期 Transformer 层的 prompt 比后期层更重要
  - 不同 prompt 深度对 prompt 长度具有不同的敏感性
- **来源**：Figure 7，Figure 14，Page 11

### 消融 4：最终输出方式（Figure 8）

- **消融内容**：VPT-Deep 的最终输出特征聚合方式
- **测试变体**：
  - **CLS（默认）**：使用 [CLS] 标记的最终层嵌入 xN
  - **Image-pool**：对图像 patch 输出 EN 做平均池化
  - **Prompt-pool**：对 prompt 输出 ZN 做平均池化
  - **Global-pool**：对 [CLS]、prompt、image 所有 token 做全局平均池化
- **揭示结果**：
  - CLS（默认）和 Image-pool 结果基本一致（如 Specialized 82.4 vs 82.3）
  - Prompt-pool 和 Global-pool 准确率下降可达 8 分（如 Natural: 70.2 vs 78.5）
  - 说明下游分类任务主要依赖 image patch 特征，prompt 特征仅起辅助作用
- **来源**：Figure 8，Page 12

### 消融 5：输入序列长度 vs 可学习参数（Figure 11）

- **消融内容**：VPT 的性能提升究竟来自更长的输入序列还是可学习参数本身
- **测试变体**：
  - **Prompt-Learned（默认）**：prompt 在微调阶段更新
  - **Prompt-Fixed**：prompt 冻结不更新
  - **[CLS]-Learned**：仅训练 [CLS] token
  - **Learned p=1**：仅 1 个可学习 prompt
- **揭示结果**：
  - Prompt-Learned >> Prompt-Fixed ≈ Linear
  - [CLS]-Learned ≈ Learned p=1
  - 证实 VPT 性能主要来自可学习的 prompt 嵌入，而非更长的序列长度
- **来源**：Figure 11，Page 19

### 消融 6：Prompt 共享策略（Figure 12）

- **消融内容**：不同层间 prompt 是否共享参数
- **测试变体**：
  - **Default**：每层独立 prompt
  - **Shared-intra**：同一层内 prompt 共享
  - **Shared-inter**：不同层间 prompt 共享（仅需一组 prompt 参数复用至所有层）
  - **Shared-all**：所有层和所有 prompt 共享同一参数
- **揭示结果**：
  - Shared-intra 与 Default p=1 相当或略优
  - Shared-inter 以相近参数量略微优于 Default（总参数 1.14× vs 1.13×），且其平均最优 prompt 长度略大（64.58 vs 60.94）
  - Shared-all 性能下降但仍优于 Linear probing
- **来源**：Figure 12，Page 20

### 消融 7：Prompt 初始化策略（Figure 13）

- **消融内容**：随机初始化 vs 基于类别原型初始化
- **测试变体**：
  - **Random（默认）**：xavier uniform 随机初始化
  - **CLS**：利用数据集各类别最终 [CLS] 嵌入的类均值初始化
  - **·-fixed**：初始化后冻结不更新
- **揭示结果**：
  - Random（默认）在几乎所有情况下最优
  - CLS 在 Natural 和 Specialized 组具有竞争力
  - 冻结 prompt（fixed variants）性能显著下降
  - 论文指出这与 NLP prompt tuning 中的 sophisticated initialization 需求不同
- **来源**：Figure 13，Page 21

### 消融 8：VPT + Bias 组合（Table 9）

- **消融内容**：同时更新 prompt 和 backbone bias
- **测试变体**：VPT-shallow+Bias, VPT-deep+Bias
- **揭示结果**：
  - VPT-shallow+Bias 在 Natural 和 Specialized 组上提升（Natural: 76.81→79.78 +2.97），但 Structured 下降（46.98→45.89 -1.09）
  - VPT-deep+Bias 在所有三组均下降（Natural: 78.48→77.64; Specialized: 82.43→82.22; Structured: 54.98→53.87）
  - 结论：VPT 与 Bias 并非互补方法
- **来源**：Table 9，Page 22

### 消融 9：Prompt Ensembling（Figure 15）

- **消融内容**：5 个不同随机种子的 prompt 集成
- **揭示结果**：
  - Ensembled VPT-deep 超越平均单次运行和最佳单次运行
  - 在 VTAB-Structured 上，Ensemble 比 Average 提升 4.7（57.8 vs 54.9，差值+2.1~+4.7）
  - Ensembled Full 提升 4.3，Ensembled Bias 提升 3.3
  - VPT 在集成场景下具有存储优势：仅需存储多个 prompt 向量而非多份 backbone 参数
- **来源**：Figure 15，Page 22

### 消融 10：不同图片分辨率（Table 11）

- **消融内容**：224×224 vs 384×384 分辨率
- **测试变体**：
  - 384 resolution 微调：所有方法
  - 224 resolution 但增大 prompt（p=380）使等效序列长度达 384×384
- **揭示结果**：
  - VPT-deep 384 在 15/19 任务上超越 Full
  - 224 高 p（p=380）的 VPT-deep 在 224 下性能不如 384 VPT-deep，但以相同序列长度和更少参数匹配或超越 384 Full
  - 提高分辨率对 Full 无改善（Natural: 72.57 vs 75.88），对 VPT-Deep 略有提升（Natural: 79.37 vs 78.48）
- **来源**：Table 11，Page 24

---

## 5. 参数敏感性与稳定性分析

### Prompt 长度敏感性（Figure 6）

- 最优 prompt 长度因任务组和具体任务而异：
  - VTAB-Natural 上最佳 p 约 1~100（平均值约 12.4）
  - VTAB-Specialized 上最佳 p 约 1~100（平均值约 52.8）
  - VTAB-Structured 上最佳 p 约 10~200（平均值约 107.5）
  - FGVC 上最佳 p 约 5~200（平均值约 73）
- 即便 p=1，VPT-Deep 仍显著优于 Adapter 和 MLP 基线
- 论文未提供 p 对单个任务敏感性的完整分析（仅分组平均）

来源：Figure 6，Table 13（prompt length 列），Page 29

### Prompt 深度敏感性（Figure 7，Figure 14）

- prompt 深度（插入层数）与准确率正相关
- 底层到顶层插入 > 顶层到底层插入
- 不同深度对 prompt 长度的敏感性不同：9→12 组（仅 3 层）在不同 prompt 长度下的波动最大
- 论文未提供每个深度的标准差

来源：Figure 7，Figure 14

### 超参数敏感性（Figure 17）

- 实验在 KITTI/Distance（VTAB-Specialized）验证集上进行
- **Linear probing**：对 weight decay 更敏感
- **VPT**：同时受 learning rate 和 weight decay 影响
  - 较大 prompt 长度对 learning rate 选择更不敏感
- 其他方法的超参敏感性用灰色标出

来源：Figure 17，Page 24

### 图像分辨率影响（Table 11）

- 提高输入分辨率（224→384）对 Full 无益反有害（Natural: 75.88→72.57）
- 提高分辨率对 VPT-deep 略有促进（Natural: 78.48→79.37）
- 224 分辨率下增大 p（p=380）可模拟 384 分辨率的效果

来源：Table 11，Page 24

### 模型规模敏感性（Figure 4）

| Backbone | 参数量(M) | VPT-deep Natural | VPT-deep Specialized | VPT-deep Structured |
|----------|----------|-----------------|---------------------|-------------------|
| ViT-B/16 | 85 | 78.48 | 82.43 | 54.98 |
| ViT-L/16 | 307 | 论文未提供逐数字 | 论文未提供逐数字 | 论文未提供逐数字 |
| ViT-H/14 | 630 | 论文未提供逐数字 | 论文未提供逐数字 | 论文未提供逐数字 |

来源：Figure 4，Page 8

**论文未提供**：Figure 4 上各方法随模型规模变化的具体数字（只有图中的可视化趋势），仅声明 VPT-deep 在 Natural 和 Structured 上显著超越 Full，Specialized 上等价。

### 统计显著性检验（Table 10，Figure 16）

**Wilcoxon signed-rank test（配对，单侧，19 个 VTAB 任务，每任务 5 次平均）**：

| 比较对象（VPT-deep vs） | 是否显著优于 | p-value |
|------------------------|------------|---------|
| Full | ✓ | 1.2e-03 |
| Linear | ✓ | 2.7e-05 |
| Mlp-3 | ✓ | 1.9e-06 |
| Partial-1 | ✓ | 1.9e-05 |
| Sidetune | ✓ | 1.9e-06 |
| Bias | ✓ | 1.9e-06 |
| Adapter | ✓ | 3.8e-06 |
| VPT-shallow | ✓ | 2.7e-05 |

**Welch's t-test（非配对，单侧，每任务 5 次运行）**：
- VPT-deep 在 127/152 个（19任务×8方法）对比中显著优于基线（p<0.05）
- VPT-deep vs Full：11/19 任务显著优于

来源：Table 10，Figure 16，Pages 22-23

---

## 6. 效率、复杂度与资源代价

### 推理和训练开销（Table 12，Figure 18，ViT-B/16，A100 GPU，batch size 64）

| 方法 | 可训练参数占比 | 训练延迟(ms/img) | 训练显存(GB) | 推理延迟(ms/img) | 推理显存(GB) |
|------|--------------|-----------------|-------------|-----------------|-------------|
| Full | 100% | 358.7 | 11.7 | 69.7 | 0.87 |
| Linear | 0.09% | 148.9 | 0.9 | 64.4 | 0.87 |
| Partial-1 | 8.35% | 193.2 | 1.4 | 66.1 | 0.87 |
| Sidetune | 10.09% | 164.6 | 1.2 | 66.9 | 0.91 |
| Bias | 0.21% | 296.9 | 10.1 | 65.6 | 0.87 |
| Adapter (r=8) | 2.12% | 293.4 | 9.9 | 68.2 | 0.87 |
| VPT-shallow (p=1) | 0.09% | 205.9 | 10.3 | 68.1 | 0.88 |
| VPT-deep (p=1) | 0.10% | 213.6 | 10.3 | 69.4 | 0.88 |
| VPT-shallow (p=200) | 0.27% | 350.6 | 25.8 | 138.8 | 1.84 |
| VPT-deep (p=200) | 2.19% | 360.1 | 25.8 | 140.8 | 1.85 |

来源：Table 12，Page 25

### 存储代价

| 方法 | 全部 24 个任务总参数倍数（× backbone） |
|------|--------------------------------------|
| Full | 24.02×（每任务独立存储完整 backbone） |
| Linear | 1.02× |
| VPT-shallow | 1.04× |
| VPT-deep | 1.18× |
| Bias | 1.05× |
| Adapter | 1.23× |

来源：Table 1，Page 7

**关键对比**：
- VPT-deep（1.18×）仅需存储所有层 prompt 嵌入 + 线性分类头
- 相比 Full（24.02×）减少约 20 倍的多任务存储
- p=1 时 VPT-deep 可训练参数仅 0.10%；p=200 时 2.19%

### VPT-prefix 推理加速（Figure 19）

- VPT-prefix 等价实现在推理时将 prompt 参数直接 prepend 到 Self-Attention 的 key/value
- 在 p 较大时显著降低推理延迟和显存
- 论文未提供 VPT-prefix 的准确率是否完全一致（仅称"does not lead to accuracy improvement on VTAB datasets"）

来源：Figure 19，Page 26

### 训练配置细节

| 维度 | 值 | 来源 |
|------|---|------|
| 框架 | PyTorch | Section A.1 |
| GPU | NVIDIA A100-40GB | Section A.1 |
| 优化器选择 | Full/Partial/Bias/Adapter: AdamW; Linear/Sidetune/Mlp/VPT: SGD | Table 6 |
| 学习率搜索 | Full等: {0.001, 0.0001, 0.0005, 0.005}; VPT等: {50, 25, 10, 5, 2.5, 1, 0.5, 0.25, 0.1, 0.05} | Table 6 |
| 总 epoch | 100（ViT-B, Swin-B），50（ViT-L/H） | Table 6 |
| 热身 epoch | 10 | Table 6 |
| Prompt 长度搜索 | ViT: {1,5,10,50,100,200}; Swin: {1,5,10,50}; ConvNet: {1,3,5,7,9,11} | Section A.1 |
| Adapter 缩减率 | {8, 64, 256} | Section A.1 |
| VPT 初始化 | xavier uniform | Section A.1 |
| VPT dropout | 0.1（仅 VPT-deep） | Section A.1 |

### 论文未提供

- 单次完整训练的实际墙钟时间
- 不同 backbone 下 VPT 的具体 FLOPs 对比
- VPT-deep 与 VPT-shallow 的端到端训练时间对比（仅给了 latency per img）
- 多 GPU 分布式训练配置细节
- SGD + VPT 的 momentum 具体值（仅写 0.9，未说明是否 Nesterov）
- ConvNet 上 VPT 的 prompt 像素数 p=5 时对应多少额外参数

---

## 7. 鲁棒性、泛化性与补充实验

### 多领域泛化

VPT 在 5 大类、24 个分类任务及 1 个分割任务上测试：

| 领域 | 具体任务数 | 代表性数据集 |
|------|----------|-------------|
| 细粒度视觉分类 | 5 | CUB, NABirds, Flowers, Dogs, Cars |
| 自然图像分类 | 7 | CIFAR-100, Caltech101, DTD, 等 |
| 专业图像分类 | 4 | 医学(Patch Camelyon, Retinopathy), 卫星(EuroSAT, Resisc45) |
| 结构化理解 | 8 | 物体计数(Clevr), 距离估计(DMLab, KITTI), 定位(dSprites), 姿态(SmallNORB) |
| 语义分割 | 1 | ADE20K |

VPT-Deep 在分类任务 20/24 个任务上超越 Full，分割任务上差距较大（42.11 vs 48.31）。

### 不同架构泛化

| 架构 | 适用性 | 表现 |
|------|--------|------|
| ViT (Base/Large/Huge) | 原生支持（以 [CLS] 为 head 输入） | 最佳——在 ViT 上超越 Full |
| Swin (Base) | 需适配（无 [CLS]，使用全局池化；prompt 仅作用在局部窗口内） | 优于其他参数高效方法，但不如 Full |
| ConvNeXt (Base) | 需适配（像素级 prompt 填充） | 在更大 ConvNet 上有效，8/19 任务超越 Full |
| ResNet-50 | 需适配（像素级 prompt 填充） | 优势不明显，无明确优胜者 |

### 不同预训练目标泛化

| 预训练目标 | VPT 在参数高效方法中的排名 | 与 Full 的关系 |
|-----------|------------------------|---------------|
| 监督 ImageNet-21k | 最优 | 20/24 任务超越 |
| MAE (自监督) | 接近最差 | 远不及 Full |
| MoCo v3 (自监督) | 中等 | 具有竞争力但非最优 |

来源：Table 4，Page 13

**关键观察**：VPT 在监督预训练下表现极佳，在自监督预训练（尤其是 MAE）下效果急剧下降。论文将此归因为监督和自监督 ViT 的"根本性差异"。

### 附加分析实验

#### 输入序列扩展效应（Figure 11）
- 冻结 prompt（Prompt-Fixed）与 Linear probing 性能相当
- 可学习 prompt（Prompt-Learned）带来显著提升
- 说明 VPT 的优势来自可学习 prompt，而非序列长度增加

#### Prompt 共享效应（Figure 12）
- 跨层共享（Shared-inter）略微优于默认独立 prompt
- 全共享（Shared-all）性能下降但高于 Linear

#### Prompt 初始化效应（Figure 13）
- 随机初始化通常优于基于 [CLS] 原型初始化
- 冻结 prompt 使所有初始化策略失效
- 与 NLP prompt tuning 中 initialization 至关重要的结论相反

#### VPT vs Adversarial Reprogramming（Section C）
- VPT 较 Adversarial Reprogramming (AR) 参数量减少 20 倍（13k vs 264k）
- VPT 可应用于多种架构（ViT, Swin），AR 主要用于 ConvNet
- VPT 更新 prompt + 分类头，AR 使用预训练分类头

#### 视觉 prompt vs 文本 prompt（Section C）
- VPT 在 20/24 任务上超越 Full 微调——NLP prompt tuning 通常只能匹配但不超过 Full
- VPT 随机初始化效果优于精心初始化——NLP 则受益于 sophisticated 初始化
- VPT 中早期层 prompt 更重要——NLP 中存在不同观察
- 说明视觉 prompt 与文本 prompt 可能有根本性差异

### 论文未提供

- 每个 VTAB 任务的多次运行标准差（仅 report mean of three runs for VTAB）
- 不同随机种子下的 prompt 稳定性分析（除 ensembling 实验外）
- 不同 backbone 初始化（而非固定预训练 checkpoint）的影响
- VPT 在更大数据集（如 ImageNet 全量）上的表现
- VPT 在检测、视频理解等非分类任务上的结果（仅验证了分割）
- Swin-B 上 VPT 超越 Full 的具体任务数（论文仅给出 vs Full 的胜场数但无 Full 对比）
- Figure 4（模型规模消融）的具体数值

---

## 8. 值得关注的实验现象

### 现象 1：VPT-Deep 在 Structured 组优势极为显著

VPT-Deep 在 VTAB-Structured 组（8 个任务）上以 54.98 平均准确率超越 Full（47.64），提升高达 **+7.34**，且 8/8 任务全胜。Structured 任务（计数、距离、定位、姿态）需要几何理解能力，VPT 的 prompt 机制可能更好地保留了预训练 backbone 的几何推理能力，而全量微调可能破坏了这种能力。

**来源**：Table 1，Page 7

### 现象 2：预训练目标对 VPT 效果影响巨大

监督预训练（ImageNet-21k）下的 VPT 表现最佳，但切换到 MAE 自监督预训练后，VPT-Deep 的 Natural 准确率从 78.48 骤降至 36.02，甚至不如 Linear probing（18.87）。这是一个剧烈的反转——同样方法在不同预训练目标下从最优变为接近最差。论文未能解释这种现象的根因。

**来源**：Table 4，Page 13

### 现象 3：Swin 上 VPT-Shallow 在 Natural 组优于 VPT-Deep

与 ViT 的规律（Deep > Shallow）相反，在 Swin-B 的 Natural 组上，VPT-Shallow（79.85）优于 VPT-Deep（76.78），且 VPT-Shallow 甚至与 Full（79.10）持平。这可能与 Swin 的局部窗口注意力机制有关——深层 prompt 在局部窗口间的传播受限。

**来源**：Table 2，Page 9

### 现象 4：VPT 与 NLP Prompt Tuning 行为截然不同

几个反直觉的差异：（1）VPT 超越 Full，NLP prompt tuning 通常仅匹配；（2）随机初始化最优，NLP 需要复杂初始化；（3）早期层 prompt 更重要。这些差异暗示视觉 Transformer 和语言 Transformer 的参数高效微调机制存在根本性区别。

**来源**：Section C，Page 26

### 现象 5：VPT 与 Bias 并非互补方法

VPT-deep+Bias 在 3 组 VTAB 任务上均降低 VPT-deep 的性能（而非提升），说明 prompt 和 bias 调优共享了相似的优化空间。这提示在不同的参数高效方法之间做组合时可能存在负交互。

**来源**：Table 9，Page 22

### 现象 6：Input Embedding 空间比 Pixel 空间更适合 Prompt

在 latent embedding 空间做 Prepend 显著优于像素空间做 Prepend-pixel 或 Concat-channel。Concat-channel 最差（Natural 上准确率比默认低 30 分），说明直接修改像素输入对经过预训练的 ViT Embedding 层造成了很大干扰。

**来源**：Figure 5，Page 10

### 现象 7：VPT 在小模型（ResNet-50）上优势消失

在 ResNet-50（23M 参数）上，VPT 在 VTAB 各组的性能相比其他方法无明显优势（Natural 66.25 略高于 Linear 63.75 但相近；Structured 37.52 远低于 Full 54.08）。VPT 的收益与 backbone 规模正相关。

**来源**：Table 5，Page 14

### 现象 8：Prompt Ensembling 高效且有效

VPT 的集成不仅存储开销低（仅需存储多个 prompt 向量），而且 ensemble 增益在所有方法中较大（Structured 组 ensemble gain 4.7，高于 Full 的 4.3 和 Bias 的 3.3）。

**来源**：Figure 15，Page 22

---

## 9. 证据充分性整理

### 支撑较充分的结论

| 结论 | 证据 | 充分性 |
|------|------|--------|
| VPT-Deep > 所有参数高效方法 | Table 1（4/4 任务组全部胜出）、Table 2（Swin 上 3/3 组最优） | **充分** |
| VPT-Deep 在大多数任务上 > Full | Table 1（20/24 任务）、Figure 3（跨数据规模一致）、Figure 4（跨模型规模一致） | **充分** |
| Prompt 深度与性能正相关 | Figure 7—多种 depth 变体系统消融，性能单调递增 | **充分** |
| VPT 优势来自可学习参数而非序列长度 | Figure 11—Prompt-Fixed vs Prompt-Learned 对比 | **充分** |
| VPT 统计显著优于基线 | Table 10（Wilcoxon 检验 p<0.05 对所有方法）、Figure 16（Welch t 检验 127/152 显著） | **充分** |

### 支撑有限的结论

| 结论 | 局限 |
|------|------|
| VPT 在 ConvNet 上有效 | 仅在 ConvNeXt-B 和 ResNet-50 上验证，ResNet-50 上优势不明确 |
| VPT 在分割任务上有效 | 仅测试 ADE20K + SETR-PUP 一个组合，且 VPT（42.11）远不及 Full（48.31） |
| VPT 跨架构泛化 | 仅测试 ViT 和 Swin 两类 Transformer 架构，Swin 上不如 Full，且 Natural 组 Shallow > Deep 破坏规律 |
| VPT 跨预训练目标泛化 | MAE/MoCo v3 上 VPT 不再是最好方法，泛化性严重受限 |
| Prompt 长度的最优策略 | 仅给出分组平均趋势，未提供每任务的 p 敏感性分析（p 变化 ±1 标准差的影响） |
| VPT vs 全量微调的理论解释 | 论文仅提供实验观测，无理论分析为何 VPT 能超越 Full |
| VPT 在小 backbone 上的有效性 | ResNet-50（23M）上无明确优势，推测 VPT 收益与模型规模相关但未系统性验证 |

### 论文未提供的实验信息

- 每个 VTAB/FGVC 任务的多运行标准差（仅 report mean，Figure 1(c) 除外标注了标准差）
- 不同预训练 checkpoint（而非固定 checkpoint）的影响
- VPT 在检测、视频理解等任务上的结果
- Prompt 长度的交叉任务共享最优解分析
- 单次完整训练耗时的 wall-clock 时间
- 在不同 backbone 上 VPT prompt 的可视化/可解释性分析
- VPT 收敛速度与 Full 的对比
- 无监督/自监督预训练下 VPT 失效原因的分析/诊断实验
- VPT 在更大规模数据集（如 ImageNet 全量 1.2M）上的微调结果
- VPT-Deep 不同层的 prompt 嵌入的相似性/差异性分析

---

## 10. 对后续问题发现最有价值的实验信息

### 可复现的实验设定

- VPT 代码开源：github.com/kmnp/vpt
- 所有 ViT/Swin 预训练 checkpoint 使用标准库（timm/torchvision）
- FGVC 和 VTAB-1k 均为公开 benchmark，数据可获取
- 训练配置（超参搜索范围、优化器、epoch 等）在 Table 6 和 Section A.1 中完整给出
- 所有逐任务结果在 Table 13/14 中完整给出，支持细粒度比较

### 值得验证的问题

1. **MAE/MoCo v3 上 VPT 失效的原因**：预训练目标改变时，VPT 从最优变为接近最差。这是否与 ViT 的特征表示结构、注意力模式的差异有关？是否可设计通用的 prompt 初始化策略解决？
2. **VPT 超越 Full 的理论解释**：为何输入空间添加不到 1% 的可学习参数能超越全量微调？是否存在某种"特征保护"机制使预训练知识更好地保留？
3. **Prompt 长度与任务复杂度的关系**：Structured 任务倾向于需要更多 prompt（平均 107.5），Natural 任务较少（平均 12.4）。是否可利用任务属性预估最优 prompt 长度？
4. **VPT 在更大数据集上的表现**：VTAB-1k 仅 1k 训练样本，FGVC 数据量也不大。在 ImageNet 全量（1.2M）上 VPT 还能超越 Full 吗？
5. **Prompt 集成的实用价值**：Prompt ensemble 在几乎无额外存储成本下获得确定性的提升（~2-5%），是否可成为实际部署的标准方案？
6. **Swin 上 VPT-Shallow > VPT-Deep 的原因**：是否与局部窗口注意力的特性有关？深层 prompt 在层间传播受限？
7. **VPT 对 backbone 扰动的影响**：不同类型的 prompt 是否在 backbone 中引入了不同的注意力偏移？可否通过 prompt 可视化解释其工作机制？

### 最值得优先验证的 3 个问题

1. **MAE/MoCo v3 上 VPT 失效的根因分析**（影响最大——如果 VPT 依赖监督预训练，其应用范围将严重受限；关系到 self-supervised ViT fine-tuning 的基础理解）
2. **VPT 在更大数据规模上的表现**（FGVC 和 VTAB-1k 数据量较小，实验规模扩大后是否还保持优势？）
3. **VPT 超越 Full 的理论解释**（缺乏理论支撑使方法看起来像经验发现——理解机制有助于设计更好的变体和迁移到新架构）

---

## 11. 一段简短总结

VPT（Visual Prompt Tuning）在 24 个分类任务（FGVC 5 + VTAB-1k 19）和 1 个分割任务（ADE20K）上系统验证了输入空间 prompt 微调的有效性。核心实验发现：(1) VPT-Deep 在 20/24 任务（83.3%）上超越全量微调，仅使用不到 1% 的可训练参数；(2) 在所有参数高效微调方法中，VPT-Deep 在所有任务组上均为最优；(3) VPT 在小数据场景下优势尤为显著，且优势在不同 backbone 规模（ViT-B/L/H）和架构（ViT/Swin/ConvNeXt）上存在但程度不一；(4) 统计检验（Wilcoxon p<0.05, Welch 127/152 显著）证实 VPT 的改进不是随机波动。证据最充分的结论为 VPT-Deep > 所有参数高效方法（4/4 任务组一致）和 VPT-Deep > Full 在大多数任务上（20/24）。但 VPT 在 MAE/MoCo v3 自监督预训练下失效、Swin 架构上无法超越 Full、分割任务上差距显著的局限也明确指出了方法的边界条件。代码和配置完全开源，便于复现和进一步验证。
