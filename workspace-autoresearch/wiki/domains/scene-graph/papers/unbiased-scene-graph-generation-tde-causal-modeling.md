---
title: "Unbiased Scene Graph Generation from Biased Training"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - scene-graph-generation
  - causal-inference
  - debiasing
  - total-direct-effect
  - counterfactual
  - long-tail
  - TPAMI-2023
raw_sources:
  - ../../../raw/sources/2023-TPAMI-Unbiased-Scene-Graph-Generation-via-Two-Stage-Causal-Modeling.pdf
  - ../../../raw/sources/2023-TPAMI-Unbiased-Scene-Graph-Generation-via-Two-Stage-Causal-Modeling.txt
related_pages:
  - camodule-causal-adjustment-module-debiasing-scene-graph-generation.md
  - eicr-environment-invariant-curriculum-relation-learning-sgg.md
  - compositional-feature-augmentation-for-unbiased-scene-graph-generation.md
  - hilo-exploiting-high-low-frequency-for-unbiased-panoptic-scene-graph-generation.md
evidence_level: full-paper
paper:
  title: "Unbiased Scene Graph Generation from Biased Training"
  authors:
    - Kaihua Tang
    - Yulei Niu
    - Jianqiang Huang
    - Jiaxin Shi
    - Hanwang Zhang
  year: 2023
  venue: "IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI), 2023 (extension of CVPR 2020)"
  arxiv: null
  doi: null
  code: "https://github.com/KaihuaTang/Scene-Graph-Benchmark.pytorch"
  project: null
classification:
  label: "TDE — Total Direct Effect for Unbiased Scene Graph Generation"
  task:
    - Scene Graph Generation (SGG)
    - Predicate Classification (PredCls)
    - Scene Graph Classification (SGCls)
    - Scene Graph Detection (SGDet)
    - Relationship Retrieval (RR)
    - Zero-Shot Relationship Retrieval (ZSRR)
    - Sentence-to-Graph Retrieval (S2GR)
  method_family:
    - Causal Inference
    - Total Direct Effect (TDE)
    - Counterfactual Reasoning
    - Bias Decomposition
  modality:
    - Visual features (Faster R-CNN ROI)
    - GloVe word embeddings
    - Union box features
  datasets:
    - Visual Genome (VG)
  metrics:
    - Recall@K (R@K)
    - mean Recall@K (mR@K)
    - Zero-Shot Recall@K (ZSRR)
    - Median Rank (Med)
---

# Unbiased Scene Graph Generation from Biased Training

> Kaihua Tang, Yulei Niu, Jianqiang Huang, Jiaxin Shi, Hanwang Zhang. "Unbiased Scene Graph Generation from Biased Training." *IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI)*, 2023. Originally published at CVPR 2020.

## One-Sentence Contribution

提出基于因果推断的 **Total Direct Effect (TDE)** 框架，将 SGG 中的偏置分解为"好偏置"（上下文先验）和"坏偏置"（长尾数据偏置），通过反事实推理(TDE)在推理阶段消除坏偏置，实现模型无关的无偏场景图生成。

## Problem Setting

SGG 旨在从图像中检测目标并识别目标间的关系三元组 `<subject, predicate, object>`。传统 SGG 模型存在严重的训练偏置问题，将多样化关系（如 walk on / sit on / lay on beach）坍缩为高频关系（on）。去偏的核心挑战在于：

1. **好偏置（Good Bias）**：上下文先验（如 person read book 优于 person eat book）对下游任务有益，不应去除
2. **坏偏置（Bad Bias）**：长尾数据偏置（如 near 主导 behind / in front of）导致模型对尾部谓词预测能力极差
3. 传统去偏方法（重采样、重加权、Focal Loss）无法区分这两类偏置，盲目削弱所有高频类别

## Method

### 因果图（Causal Graph）

构建 SGG 的结构因果模型（SCM）：

```
X（图像）→ Z（视觉上下文）→ Y（谓词预测）
```

其中：
- **X**：输入图像
- **Z**：上下文变量（包括目标检测特征和空间配置）
- **Y**：谓词分类输出

### 两阶段因果建模

#### 阶段 1：有偏训练

标准 SGG 训练，模型学习从 X 到 Y 的全部因果路径，包括：
- **X → Y**（直接路径）：视觉语义的直接映射
- **X → Z → Y**（间接路径）：通过上下文 Z 的间接影响

有偏训练使得模型捕捉了"好偏置"和"坏偏置"的混合。

#### 阶段 2：反事实去偏（TDE 推理）

反事实推理的核心思路：**"如果模型只看到上下文而看不到目标视觉特征，它会预测什么？"**

- **Factual**（事实）：$Y_{x}(u)$ — 基于实际图像 $X=x$ 的预测
- **Counterfactual**（反事实）：$Y_{\bar{x}, z}(u)$ — 保持上下文 Z 不变但 wipes out X 的预测

**Total Direct Effect (TDE)：**

$$
TDE = Y_x(u) - Y_{\bar{x}, z}(u)
$$

TDE 等价于"好偏置"部分（直接因果效应），去除的是坏偏置部分（通过上下文的间接效应）。

### 推理时"两阶段思考"

模型在推理时"思考两次"：
1. **第一次**：正常前向推理得到 $Y_x(u)$
2. **第二次**：反事实推理，将输入特征置为 dummy（保持上下文 Z 不变），得到 $Y_{\bar{x}, z}(u)$
3. **TDE 最终分数**：$Y_x(u) - Y_{\bar{x}, z}(u)$

### 模型无关性

TDE 是即插即用的推理策略，不改变训练过程，可应用于任何 SGG 模型（MOTIFS、VCTree、VTransE 等）和任何融合函数（SUM、GATE）。

## Experiments

### 数据集

- **Visual Genome (VG)**：使用标准 VG split [65, 72, 56, 5]，包含最频繁的 150 个目标类别和 50 个谓词类别
- 训练集约 57,726 张图像，测试集 5,000 张

### Baselines

**SGG Backbones：**
- MOTIFS† [72]
- VCTree† [56]
- VTransE† [74]
- IMP+ [65, 6]
- KERN [6]

**去偏方法对比：**
- Focal Loss
- Reweight（逆频率加权）
- Resample（重采样）
- X2Y / X2Y-Tr（因果干预）
- TE（总效应）
- NIE（自然间接效应）

### 评估协议

- **Relationship Retrieval (RR)**：三个子任务（PredCls / SGCls / SGDet），评估 Recall@K 和 mean Recall@K
- **Zero-Shot Relationship Retrieval (ZSRR)**：仅评估训练中未见过的三元组
- **Sentence-to-Graph Retrieval (S2GR)**：以图像描述为查询检索场景图表示

### 消融设计

- **TDE vs TE vs NIE**：对比三种因果效应分解
- **SUM vs GATE fusion**：对比两种融合策略
- **TDE 应用于不同 backbone**：验证模型无关性

### 训练设置

基于 maskrcnn-benchmark [35]，Faster R-CNN 检测器在 VG 上微调，初始学习率 $1 \times 10^{-2}$，在第 10 和第 25 epoch 衰减 10 倍。

## Results

### Main Results — Relationship Retrieval (Table 6)

| Model | Fusion | Method | PredCls mR@20/50/100 | SGCls mR@20/50/100 | SGDet mR@20/50/100 |
|-------|--------|--------|----------------------|---------------------|--------------------|
| MOTIFS† | SUM | Baseline | 11.5 / 14.6 / 15.8 | 6.5 / 8.0 / 8.5 | 4.1 / 5.5 / 6.8 |
| MOTIFS† | SUM | **TDE** | **18.5 / 25.5 / 29.1** | **9.8 / 13.1 / 14.9** | **5.8 / 8.2 / 9.8** |
| MOTIFS† | GATE | Baseline | 12.2 / 15.5 / 16.8 | 7.2 / 9.0 / 9.5 | 5.2 / 7.2 / 8.5 |
| MOTIFS† | GATE | **TDE** | **18.5 / 24.9 / 28.3** | **11.1 / 13.9 / 15.2** | **6.6 / 8.5 / 9.9** |
| VCTree† | SUM | Baseline | 11.7 / 14.9 / 16.1 | 6.2 / 7.5 / 7.9 | 4.2 / 5.7 / 6.9 |
| VCTree† | SUM | **TDE** | **18.4 / 25.4 / 28.7** | **8.9 / 12.2 / 14.0** | **6.9 / 9.3 / 11.1** |
| VCTree† | GATE | Baseline | 12.4 / 15.4 / 16.6 | 6.3 / 7.5 / 8.0 | 4.9 / 6.6 / 7.7 |
| VCTree† | GATE | **TDE** | **17.2 / 23.3 / 26.6** | **8.9 / 11.8 / 13.4** | **6.3 / 8.6 / 10.3** |
| VTransE† | SUM | Baseline | 11.6 / 14.7 / 15.8 | 6.7 / 8.2 / 8.7 | 3.7 / 5.0 / 6.0 |
| VTransE† | SUM | **TDE** | **17.3 / 24.6 / 28.0** | **9.3 / 12.9 / 14.8** | **6.3 / 8.6 / 10.5** |

**关键结果**：MOTIFS†+SUM+TDE 在 PredCls 上 **mR@100 从 15.8 提升至 29.1（+84%）**，而传统 Recall@100 从 67.9 下降至 51.4（因细粒度分类导致）。

### Zero-Shot Relationship Retrieval (Table 2)

| Model | Fusion | Method | PredCls R@50/100 | SGCls R@50/100 | SGDet R@50/100 |
|-------|--------|--------|------------------|-----------------|----------------|
| MOTIFS† | SUM | Baseline | 10.9 / 14.5 | 2.2 / 3.0 | 0.1 / 0.2 |
| MOTIFS† | SUM | **TDE** | **14.4 / 18.2** | **3.4 / 4.5** | **2.3 / 2.9** |
| VCTree† | SUM | Baseline | 10.8 / 14.3 | 1.9 / 2.6 | 0.2 / 0.7 |
| VCTree† | SUM | **TDE** | **14.3 / 17.6** | **3.2 / 4.0** | **2.6 / 3.2** |

**关键结果**：TDE 在零样本关系检索上也存在一致改进，表明模型学到了更通用的关系表示而非记忆训练数据组合。

### 与其他去偏方法对比

在 PredCls mR@100 上：
- Baseline: 15.8
- Focal: 15.0
- Reweight: 21.9（全面提升但牺牲头部谓词）
- Resample: 20.0
- X2Y: 17.6 / X2Y-Tr: 16.0
- TE: 29.0（接近 TDE 但包含好偏置和坏偏置的混合）
- NIE: 1.4（仅坏偏置，表现极差）
- **TDE: 29.1（最优 mR@K，且头部谓词也得到保持）**

## Limitations

1. **TDE 过度强调动作类谓词**：如将 pole sign 之间的 on 误判为 holding，在某些场景下不自然
2. **传统 Recall@K 下降**：TDE 在 mR@K 上大幅提升，但 R@K 下降（从 67.9 降至 51.4 at PredCls R@100），文档明确指出这是由于更细粒度的分类而非性能退化
3. **推理成本翻倍**：TDE 需要两次前向推理（事实 + 反事实），推理时间是 baseline 的两倍
4. **仅处理谓词偏置**：未处理目标类别本身的偏置和对象对分布偏置（后续工作如 CAModule [2025] 进一步解决此问题）

## Reusable Claims

- **✅ TDE 通过反事实推理分离好/坏偏置**：在 predcls mR@100 上相比 baseline 提升 **+84%**（15.8 → 29.1），且头部谓词（如 behind, above）也得到改善
- **✅ TDE 完全模型无关**：在 MOTIFS、VCTree、VTransE 三种 backbone 上均一致改进，且与 SUM/GATE 两种融合策略兼容
- **✅ TDE 具备零样本泛化能力**：在 ZSRR 各子任务上均提升，说明去偏后的模型学到了更通用的关系概念
- **✅ 传统去偏方法（Reweight）盲目削减所有高频谓词**：Reweight 虽然提升 mR@K 但破坏了许多合理的头部谓词，TDE 没有此问题
- **✅ NIE ≠ TDE**：NIE 仅捕捉偏置路径（表现极差，mR@100=1.4），TDE 才是直接效应，验证了因果分解的正确性

## Connections

- **[CAModule](camodule-causal-adjustment-module-debiasing-scene-graph-generation.md)**：(2025) 在 TDE 的基础上进一步引入共现分布作为中介变量，实现 triplet 级别的细粒度因果调整，处理对象对分布偏置
- **[EICR](eicr-environment-invariant-curriculum-relation-learning-sgg.md)**：(ICCV 2023) 从环境不变学习角度处理语境不均衡，与 TDE 互补
- **[CFA](compositional-feature-augmentation-for-unbiased-scene-graph-generation.md)**：(2023) 通过组合式特征增强提升尾部谓词表示质量，互补于 TDE 的推理阶段去偏
- **[HiLo](hilo-exploiting-high-low-frequency-for-unbiased-panoptic-scene-graph-generation.md)**：(ICCV 2023) 分治策略处理长尾，适用全景 SGG 场景
- **KERN [6]**：与 KERN（CVPR 2019）相比，TDE 不需要额外训练 dense graph network，更简洁

## Open Questions

- TDE 的推理加倍能否通过知识蒸馏或模型剪枝优化？
- 反事实推理需要设计 dummy features，不同设计选择对最终 TDE 效果的影响尚不明确
- TDE 在更多 backbone（如 Trans-based SGG）上的表现有待验证

## Provenance

- **PDF**：raw/sources/2023-TPAMI-Unbiased-Scene-Graph-Generation-via-Two-Stage-Causal-Modeling.pdf (3.9MB, 16 pages)
- **提取文本**：raw/sources/2023-TPAMI-Unbiased-Scene-Graph-Generation-via-Two-Stage-Causal-Modeling.txt (69,571 chars)
- **证据等级**：full-paper — 全文精读，涵盖方法、实验、表格和定性分析
- **入库日期**：2026-06-09
- **入库方式**：inbound 批量入库（sub-agent）
