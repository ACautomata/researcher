---
title: "Generative Compositional Augmentations for Scene Graph Prediction"
type: paper
domain: scene-graph
status: active
created: 2026-06-10
updated: 2026-06-10
tags:
  - scene-graph-generation
  - augmentation
  - generative-adversarial-network
  - compositional-generalization
  - long-tail-bias
  - zero-shot-learning
  - ICCV-2021
raw_sources:
  - ../../../raw/sources/2020-07-11-generative-compositional-augmentations-for-scene-graph-prediction.pdf
  - ../../../raw/sources/2020-07-11-generative-compositional-augmentations-for-scene-graph-prediction.txt
related_pages:
  - neural-motifs-scene-graph-global-context.md
  - 2026-06-09-synthetic-visual-genome-2.md
evidence_level: full-paper
paper:
  title: "Generative Compositional Augmentations for Scene Graph Prediction"
  authors:
    - Boris Knyazev
    - Harm de Vries
    - Cătălina Cangea
    - Graham W. Taylor
    - Aaron Courville
    - Eugene Belilovsky
  year: 2021
  venue: "IEEE/CVF International Conference on Computer Vision (ICCV), 2021"
  arxiv: "2007.05756"
  doi: null
  code: "https://github.com/bknyaz/sgg"
  project: null
classification:
  label: "GCA-SGG — Generative Compositional Augmentations for Scene Graph Prediction"
  task:
    - Scene Graph Generation (SGG)
    - Predicate Classification (PredCls)
    - Scene Graph Classification (SGCls)
  method_family:
    - Generative adversarial augmentation
    - Graph-structured perturbation
    - Conditional GAN
  modality:
    - Visual features (RoI)
    - Scene graph triplets
  datasets:
    - Visual Genome (VG)
  metrics:
    - R@50 (PredCls)
    - R@100 (SGCls)
    - Zero-shot Recall (zsR@50/100)
    - 10-shot Recall
    - 100-shot Recall
    - All-shot Recall
    - Precision/Density/Recall/Coverage (feature quality)
---

## Citation

Knyazev, B., de Vries, H., Cangea, C., Taylor, G.W., Courville, A., Belilovsky, E. "Generative Compositional Augmentations for Scene Graph Prediction." ICCV 2021. [arXiv](https://arxiv.org/abs/2007.05756) | [Code](https://github.com/bknyaz/sgg)

## One-Sentence Contribution

提出基于条件 GAN 的场景图组合增强方法，通过对场景图三元组进行结构化扰动并用 GAN 生成对应的视觉特征，来提升 SGG 模型在零样本和少样本组合上的泛化能力。

## Problem Setting

- **目标**：提升场景图生成（SGG）模型在**组合泛化（compositional generalization）** 上的表现——即识别训练中未见过的物体-关系-物体三元组组合
- **挑战**：
  - Visual Genome 中三元组分布极度长尾，训练集仅覆盖约 3% 的所有可能三元组（Fig. 1）
  - 零样本组合如 `<cup, on, surfboard>` 即使每个单独类别（cup, surfboard, on）在训练集中都常见，模型仍往往失败
  - 传统的重采样/重加权方法受限于仅调整谓词频率，无法有效生成新的组合
- **设定**：标准 SGG 设定，从图像预测场景图（物体 + 关系），特别关注 zero-shot、10-shot、100-shot 测试子集

## Method

### 架构概览

完整 pipeline（Fig. 5）：

1. **场景图扰动**（Scene Graph Perturbation）：对训练集中的真实场景图 G 进行节点替换，得到扰动图 Ĝ
2. **场景图到视觉特征生成**（Scene Graph → Visual Features）：用条件 GAN（Generator G + Discriminators D）将 Ĝ 和边界框 B 转换为视觉特征（V̂, Ê）
3. **联合训练**：主模型 F 同时学习真实特征和 GAN 生成的增强特征

### 场景图扰动（§ 3.1.1）

三种扰动策略（Fig. 4）：

- **RAND**（random）：均匀随机采样替换节点类别，简单但易产生不可能的组合
- **NEIGH**（semantic neighbors）：利用预训练 GloVe 词嵌入，从目标词向量的 top-k 近邻中采样替换类别，产生语义上合理的组合但多样性受限
- **GRAPHN**（graph-structured semantic neighbors）：**核心贡献**。利用数据集统计和图结构来采样替换：
  - 对节点 i 考虑其在图中出现的所有三元组 R̃ᵢ
  - 对每个三元组在数据集中寻找匹配同类（oc, ek, oj）或（oj, ek, oc）的三元组候选替换 oc
  - 按候选出现频次的倒数定义未归一化概率：p̂c = 1/nc
  - 引入阈值 α 过滤低出现频次的候选（nc < α 时设 p̂c = 0），控制稀有三元组的采样比例
  - 从候选采样后，再从 top-k 语义近邻中确定最终替换（包含候选本身）
  - 顺序扰动：每个节点的扰动依赖于当前图的已有替换

扰动比例 L = 20% 节点，优先扰动连接度高的 hub 节点。

假设扰动后的边界框与原始相同：B̂ = B（附录 B.3 实验验证）。

### 视觉特征生成（§ 3.1.2）

- **特征提取**：使用预训练 Faster-RCNN（VGG16 backbone）提取全局特征 H，RoIAlign 提取节点特征 V 和边特征 E
- **Generator G**：基于 SPADE [53] 架构，GCN 处理场景图 → 拼接采样到的同类视觉特征 V' 作为条件 → 布局生成 → 特征细化 → RoIAlign 提取 V̂, Ê
- **Discriminators D**：三个判别器——Dnode（节点特征）、Dedge（边特征）、Dglobal（全局特征图），均按 CGAN 方式条件在类别上
- **损失函数（式 6）**：L = LCLS + LREC − γ( LD_ADV + LG_ADV )
  - LCLS：主模型分类损失（节点 CE + 边密度归一化 CE）
  - LREC：重建/循环一致性损失（在 Ĝ 上计算）
  - LD_ADV / LG_ADV：对抗损失，按 CycleGAN 风格
  - γ = 5

### 语义合理性评估（§ 3.2）

- **BERT 评分**：将场景图转为文本序列，mask 扰动节点后计算 BERT 似然分数，作为场景图质量的量化指标
- **Hit Rate**：扰动产生的三元组与测试子集真实标注的匹配百分比

## Experiments

### 数据集与划分

- **Visual Genome (VG)** [38]：150 个最频繁物体类别，50 个谓词类别（[74] 标准划分）
- 训练集 57,723 张，测试集 26,446 张，验证集 5,000 张
- 测试子集：
  - Zero-shot：三元组在训练中出现 0 次，4,519 个场景图
  - 10-shot：出现 1-10 次，9,602 个场景图
  - 100-shot：出现 11-100 次，16,528 个场景图
  - All-shot：所有测试场景图

### 模型与基线

**主模型 F**：
- **IMP++**（改进版 Iterative Message Passing [36]）
- **NM++**（改进版 Neural Motifs [82]）

**基线方法**：
- **RESAMPLE**：基于谓词/三元组逆频率的重采样 [67]
- **REWEIGHT**：提高稀有谓词类别的 softmax 分数
- **TDE**（Total Direct Effect） [67]：因果去偏方法，仅去偏谓词

### 训练设置

- 检测器：Faster-RCNN + VGG16，预训练于 VG [82]
- GAN：Spectral Norm [50] for D，Batch Norm [30] for G
- TTUR [25]：G 学习率 1e-4，D 学习率 2e-4
- 扰动比例 L = 20%
- NEIGH top-k = 10
- GRAPHN top-k = 5，α = [2, 5, 10, 20]
- 3 个随机种子运行，报告 mean ± std

### 评估指标

- **PredCls**：Recall@50
- **SGCls**：Recall@100（不施加图约束 [36]）
- **zsR@50/100**：零样本召回率（施加图约束时单独报告，Table 2）
- **特征质量**：Precision, Density, Recall, Coverage [39, 51]

### 消融实验

- GAN（无扰动）
- GAN+RAND、GAN+NEIGH、GAN+GRAPHN（不同 α）
- 无 Global D（式 5 中移除全局项）、无 Local D、无 D_ADV、无 G_ADV、无 LREC、更小 batch size、无视觉条件 V'

## Results

### 主要 SGG 结果（Table 1，基于 IMP++）

| 方法 | PredCls ZS R@50 | SGCls ZS R@100 | SGCls 10-shot | SGCls All-shot | SGCls-mR |
|---|---|---|---|---|---|
| Baseline IMP++ | 9.27±0.10 | 28.14±0.05 | 42.78±0.32 | 48.70±0.08 | 27.78±0.10 |
| GAN+GRAPHN α=2 | **9.89±0.15** | **28.90±0.14** | **43.79±0.27** | 50.06±0.29 | 27.79±0.48 |
| GAN+GRAPHN α=5 | 9.62±0.29 | **29.18±0.33** | 43.74±0.10 | 50.14±0.21 | 27.98±0.23 |
| GAN+GRAPHN α=10 | 9.84±0.17 | 28.90±0.46 | 43.54±0.36 | **50.10±0.23** | 27.68±0.37 |
| GAN+GRAPHN α=20 | 9.65±0.15 | 28.68±0.28 | 43.64±0.20 | 49.89±0.28 | 27.42±0.36 |

- GRAPHN α=2 在零样本 PredCls 上提升 +0.62（9.27→9.89，相对提升 6.7%）
- GRAPHN α=5 在零样本 SGCls 上提升 +1.04（28.14→29.18，相对提升 3.7%）
- 所有 GRAPHN 变体在 all-shot SGCls 上提升约 +1.36~1.44（48.70→50.06~50.14）
- GAN 无扰动即显著超越 baseline，尤其在 100-shot 和 all-shot 上
- RAND 和 NEIGH 提升零样本但降低 100-shot/all-shot 表现

### 其他基线对比

| 方法 | PredCls ZS R@50 | SGCls ZS R@100 | SGCls All-shot |
|---|---|---|---|
| IMP++ | 9.27±0.10 | 28.14±0.05 | 48.70±0.08 |
| REWEIGHT | 9.58±0.14 | 28.27±0.22 | 48.13±0.10 |
| RESAMPLE-predicates | 9.13±0.06 | 27.77±0.10 | 48.23±0.10 |
| RESAMPLE-triplets | 8.94±0.16 | 27.66±0.14 | 47.77±0.10 |
| TDE | 9.21±0.21 | 27.91±0.09 | 48.35±0.08 |

- TDE、REWEIGHT 因仅去偏谓词，对 ZS 组合（如 <cup, on, surfboard> 中 'on' 本就高频）帮助有限
- GAN 方法不受此限制，因为其通过扰动场景图节点而非仅调整谓词频率

### 零样本召回（Table 2，施加图约束）

| 方法 | PredCls zsR@50 | PredCls zsR@100 | SGCls zsR@50 | SGCls zsR@100 |
|---|---|---|---|---|
| IMP++ [36] | 4.2±0.2 | 18.3±0.4 | 2.3±0.1 | 10.2±0.1 |
| IMP++ GAN+GRAPHN | 4.3±0.1 | 18.5±0.3 | 3.1±0.1 | 14.2±0.0 |
| IMP++ GAN+GRAPHN (max) | **4.4±0.1** | **19.1±0.3** | **3.2±0.1** | **14.5±0.0** |
| NM++ [36] | 2.3±0.1 | 10.2±0.1 | 1.8±0.1 | 2.5±0.1 |
| NM++ GAN+GRAPHN | 3.1±0.1 | 14.2±0.0 | 2.5±0.1 | 3.7±0.1 |
| NM++ GAN+GRAPHN (max) | **3.2±0.1** | **14.4±0.0** | **2.5±0.1** | **3.8±0.1** |
| TDE [67] (with IMP) | 3.5±0.1 | 3.5±0.1 | 1.1 | 2.2 |

关键发现：GAN+GRAPHN 对 NM++ 提升更显著（SGCls zsR@50 从 1.8 提升到 2.5，PredCls zsR@100 从 10.2 提升到 14.2，约 +4 pp）。

### 特征质量评估（Table 3）

| 分布 X | Precision | Density | Recall | Coverage | Avg |
|---|---|---|---|---|---|
| Real test | 0.74 | 1.02 | 0.75 | 0.97 | 0.87 |
| Real test-zs | 0.66 | 0.99 | 0.70 | 0.94 | 0.82 (-6%) |
| GAN Fake test | 0.55 | 0.77 | 0.42 | 0.82 | 0.64 |
| GAN Fake test-zs | 0.47 | 0.60 | 0.41 | 0.75 | **0.56 (-13%)** |

- 在 zero-shot 场景图上生成的视觉特征质量显著下降（Avg 0.64→0.56，-13%，相对）
- 特征质量与 SGG 表现相关（Figure 8）：生成的视觉特征越好，SGG 增益越大

### 消融实验发现（Figure 8）

- 移除 Global D（式 5）的模型在零样本上反而更好（可能因正则化效应），但与扰动结合不佳
- 所有消融模型在 SGG 表现和特征质量上均有相关性下降
- 无视觉特征条件 V' 的 GAN 及小 batch size 均降低表现

## Limitations

1. **边际改进**：ZS recall 提升仅约 0.6-1.0 pp（PredCls 上约 6.7% 相对提升），论文自评为"marginal, but consistent improvements"
2. **零样本场景图特征质量差**：GAN 在稀有组合上生成的视觉特征 fidelity 和 diversity 均显著下降（Avg 0.64→0.56），限制了进一步改进空间
3. **扰动假设**：假设扰动后的边界框不变，这对尺寸差异大的物体类别不准确（虽然论文实验表明该假设在实践中效果尚可）
4. **Bounding box 预测实验有限**：附录 B.3 仅初步探索了 B̂ 预测，主要结果仍使用同一边界框的假设
5. **仅 Visual Genome 单一数据集**：未在 OpenImages V6 等其他 SGG 数据集上验证
6. **训练复杂度**：GAN 需要联合训练 F、G、D 三个组件，计算开销显著高于 baseline
7. **α 选择依赖于目标指标**：不同 α 值在不同的 shot 子集上各有优势，需要根据目标指标调参

## Reusable Claims

1. **场景图三元组分布极度长尾是 SGG 组合泛化的主要障碍**：训练集仅覆盖约 3% 的可能三元组，大量合理组合未被标注
2. **仅去偏谓词不足以处理零样本组合**：TDE/REWEIGHT 等仅调整谓词频率的方法对 <cup, on, surfboard> 这类高频谓词 + 低频物体组合的零样本场景效果有限
3. **图结构感知的扰动优于随机和语义邻居扰动**：GRAPHN 通过考虑数据集统计和图结构产生更合理的稀有组合，hit rate 和 SGG 表现均更优
4. **GAN 生成的视觉特征质量与 SGG 表现正相关**：Features 质量越好（如 Figure 8），SGG 增益越大，改进生成模型有望直接提升 SGG 结果
5. **特征级别增强无需完整图像生成**：在 RoI 特征空间进行增强（而非生成完整图像）减少了计算开销，且不依赖图像级生成质量

## Connections

- **与 Neural Motifs [82] 的关系**：本文的 GAN 框架可直接与 NM++ 结合使用，在 NM++ 上零样本提升更显著（SGCls zsR@50 从 1.8 到 2.5）
- **与 TDE [67] 的关系**：TDE 仅去偏谓词层面，本文方法通过节点扰动增加组合多样性，互补性较强
- **与合成数据生成**：本文使用的 ORACLE-ZS 实验（直接使用 ZS 测试三元组构造扰动）提供了一个上界估计（10.52 PredCls ZS），显示即使理想化扰动仍有较大改进空间
- **与 CFA（ICCV 2023）**：CFA 后来在特征增强方向进一步改进了组合泛化，使用混合增强而非 GAN

## Open Questions

1. 能否通过更好的生成模型（如扩散模型）生成更高质量的特征以提升 SGG 表现？
2. 边界框预测（B̂ 随 Ĝ 变化）是否能进一步改进扰动效果？
3. 本文方法是否能在更大规模数据集（如 OpenImages V6）上获得更显著增益？
4. GRAPHN 依赖完整的场景图结构，在弱监督或无标注场景图场景中如何适用？

## Provenance

- **Raw source**: `raw/sources/2020-07-11-generative-compositional-augmentations-for-scene-graph-prediction.pdf` (arXiv original; ICCV 2021 camera ready version)
- **Extracted text**: 84,142 chars, key sections covered: Introduction, Related Work, Methods (§3), Experiments (§4), Results (§4.2), Conclusion
- **Evidence level**: full-paper
- **Verification**: All numerical results transcribed from Table 1 (p.6), Table 2 (p.7), Table 3 (p.7), and supporting text
