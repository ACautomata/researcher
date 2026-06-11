---
title: "CLIP-Driven Open-Vocabulary 3D Scene Graph Generation via Cross-Modality Contrastive Learning (CCL-3DSGG)"
authors:
  - Lianggangxu Chen
  - Xuejiao Wang
  - Jiale Lu
  - Shaohui Lin
  - Changbo Wang
  - Gaoqi He
year: 2024
venue: CVPR 2024
doi: null
arxiv: null
code: null
domain: scene-graph
tags: [3d-scene-graph, open-vocabulary, clip, contrastive-learning, cross-modality, point-cloud]
evidence_level: full-paper
status: active
raw_sources:
  - ../../../sources/scene-graph/2024-CVPR-CLIP-Driven-Open-Vocabulary-3D-Scene-Graph.pdf
  - ../../../sources/scene-graph/2024-CVPR-CLIP-Driven-Open-Vocabulary-3D-Scene-Graph.txt
task: 3D Scene Graph Generation
dataset: [3DSSG, ScanNet]
---

# CLIP-Driven Open-Vocabulary 3D Scene Graph Generation via Cross-Modality Contrastive Learning

> Lianggangxu Chen, Xuejiao Wang, Jiale Lu, Shaohui Lin, Changbo Wang, Gaoqi He. CVPR 2024.
> East China Normal University.

## 核心贡献

1. **首次**将 CLIP 跨模态特征引入无监督/开放词汇 3DSGG，无需手工标注即可训练 3DSG 特征提取器。
2. 提出 **Grammar Parse** 机制：将 caption 按词性（主语、宾语、谓语、形容词等）分解为词级特征，替代传统的 sentence-level 嵌入，减少语义歧义。
3. 提出 **Adjective Exchange 负样本增强**：交换不同 pair 中的形容词生成结构化负样本，增强模型细粒度语义理解。
4. 设计 **T3D loss（text-to-3D）** 和 **I3D loss（image-to-3D）** 两个跨模态对比损失，分别对齐文本-3D 和图像-3D 特征。

## 问题定义

给定 3D 点云场景，目标是开放词汇地识别场景中的物体及其关系谓词。传统 3DSGG 方法依赖大量人工标注且只能识别闭集类别。本文旨在无标注条件下实现开放词汇（包含 novel 类别）的 3D 场景图生成。

## 方法：CCL-3DSGG

### 1. 跨模态特征提取 (Cross-modality Features Extraction)

#### 文本特征 (Text Features)

**Grammar Parse**：将 caption 按词性分解为五类：
- **S** (Subject)：主要主语
- **O** (Object)：主要宾语
- **P** (Predicate)：谓语/关系
- **A** (Adjective)：外观属性
- **AS/AO**：分属主语/宾语的形容词
- **OT** (Other)：未分类词

词集表示为 $T_{pw} = \{S, O, P, A, AS, AO, OT\}$。

**Negative Text Feature Augmentation**：通过交换不同 pair $(A_i S_i, P_i, A_i O_i)$ 和 $(A_j S_j, P_j, A_j O_j)$ 中的形容词生成负样本：

$$T_{pw}^- = \text{Swap}(Pair_i, Pair_j) = \{(A_j X_i, A_i X_j)\}, X \in \{S, O\}$$

使用 CLIP 文本编码器 $T_\theta$ 提取文本特征 $F_T \in \mathbb{R}^{w \times 512}$。

#### 图像特征 (Image Features)

利用点云数据附带的 RGB 序列和相机位姿，选择同一场景中距当前 3D 扫描最近的相机视角图像作为正样本，其他视角作为负样本。通过 CLIP 视觉编码器 $I_\theta$ 提取图像特征 $F_I \in \mathbb{R}^{k \times 512}$。

#### 3D 特征

采用 PointNet + GNN 主干网络作为 3DSG 特征提取器 $P_\theta$，输出跨模态特征 $F_P \in \mathbb{R}^{n \times 512}$，其中 $n$ 为 3DSG 中 object/predicate 节点总数。

### 2. 跨模态对比学习损失 (Cross-modality Contrastive Learning Losses)

#### T3D Loss (Text-to-3D)

对齐单词级文本特征与 3DSG 特征：

$$\mathcal{L}_{T3D} = -\frac{1}{B} \sum_{i=1}^B \log \frac{\sum_{j \in \mathcal{P}(i)} \exp(\text{sim}(F_T^i, F_P^j)/\tau)}{\sum_{k \in \mathcal{N}(i)} \exp(\text{sim}(F_T^i, F_P^k)/\tau)}$$

其中 $B$ 为训练对总数，$\mathcal{P}(i)$ 为正样本集，$\mathcal{N}(i)$ 为负样本集（含 adjective exchange 增广）。

经 Grammar Parse + Adjective Exchange 后，positive 样本匹配数显著增加（从 1:1 变为 $w$:1，$w$ 为解析词数），同时负样本更丰富。

#### I3D Loss (Image-to-3D)

对齐多视角图像特征与 3DSG 特征：

$$\mathcal{L}_{I3D} = -\frac{1}{B} \sum_{i=1}^B \log \frac{\exp(\text{sim}(F_I^i, F_P^i)/\tau)}{\sum_{j=1}^B \exp(\text{sim}(F_I^i, F_P^j)/\tau)}$$

将当前场景最近视角视为正样本，其他场景所有视角视为负样本。

### 3. 无监督总损失

$$\mathcal{L}_{CCL-3DSGG}^u = \lambda_1 \mathcal{L}_{I3D} + \lambda_2 \mathcal{L}_{T3D}$$

### 4. 开放词汇推理 (Open-Vocabulary Inference)

训练完成后，固定 3DSG 特征提取器。在推理时，构造 prompt 模板（如 "a photo of {object}"）并用 CLIP 文本编码器提取 prompt 特征，计算 cosine similarity 与 3DSG 特征的相似度进行分类，无需分类头。

## 实验

### 数据集

- **3DSSG**：3,582 训练场景 / 548 测试场景，160 个物体类别，27 个谓词类别
- **ScanNet**：用于无标注场景的定性可视化评估

### 任务设置

- **PREDCLS (Predicate Classification)**：给定 GT 物体标签和边界框，预测关系
- **SGCLS (Scene Graph Classification)**：给定 GT 边界框，联合预测物体及关系

### 评估指标
**Recall@K (R@K)** 和 **mean Recall@K (mR@K)**，K=20,50,100

### 实验设置

- 主干：PointNet + GNN | 特征维度 512
- 优化器：Adam | batch size 8 | 100 epochs
- 初始学习率：0.001 | GPU：Nvidia RTX 2080Ti
- 训练时间：约 48-50 小时

### 主要结果

#### Table 1: 监督学习对比 (3DSSG)

| 方法 | SGCLS (R@20/50/100) | SGCLS (mR@20/50/100) | PREDCLS (R@20/50/100) | PREDCLS (mR@20/50/100) | Mean{R/mR} |
|------|---------------------|----------------------|----------------------|-----------------------|------------|
| SGPN (CVPR20) | 27.0/28.8/29.0 | 19.5/22.6/23.1 | 51.9/58.0/58.5 | 32.1/38.4/38.9 | 42.2/29.1 |
| SGFN (CVPR21) | 27.5/29.2/29.2 | 24.2/28.1/28.2 | 52.6/58.9/59.4 | 45.3/53.1/53.2 | 42.8/38.7 |
| EdgeGCN (CVPR21) | 28.0/29.8/29.8 | 24.5/29.1/29.2 | 54.7/60.9/61.5 | 54.3/62.1/62.2 | 44.1/43.6 |
| KISGP (NeurIPS22) | 28.5/30.0/30.1 | 24.4/28.6/28.8 | 59.3/65.0/65.3 | 56.6/63.5/63.8 | 46.4/44.3 |
| VL-SAT (CVPR23) | 32.0/33.5/33.7 | 31.0/32.6/32.7 | 67.8/79.9/80.8 | 57.8/64.2/64.3 | 54.4/47.1 |
| **CCL-3DSGG (Ours)** | **37.6/40.3/45.7** | **35.0/37.3/40.6** | **73.6/80.5/82.9** | **59.1/66.7/69.1** | **60.1/51.3** |

#### Table 2: 长尾谓词分类 + 未见三元组 (3DSSG)

| 方法 | Head mA@3 | Head mA@5 | Body mA@3 | Body mA@5 | Tail mA@3 | Tail mA@5 | Unseen A@50 | Unseen A@100 |
|------|-----------|-----------|-----------|-----------|-----------|-----------|-------------|--------------|
| SGPN | 96.66 | 99.17 | 66.19 | 85.73 | 10.18 | 28.41 | 15.78 | 29.60 |
| VL-SAT | 96.31 | 99.21 | 80.03 | 93.64 | 52.38 | 66.13 | 31.28 | 47.26 |
| **Ours** | **98.54** | **99.78** | **84.72** | **96.03** | **61.24** | **75.91** | **36.72** | **52.47** |

#### Table 3: 无监督结果 (3DSSG, mR@K)

| 方法 | SGCLS (mR@20/50/100) | PREDCLS (mR@20/50/100) |
|------|----------------------|-----------------------|
| SGPN w/o CL | -/-/- | 0.7/2.5/11.8 |
| KISGP w/o CL | 2.5/5.4/8.9 | 5.6/9.2/23.5 |
| VL-SAT w/o CL | 8.2/10.1/13.3 | 9.5/13.9/27.4 |
| **CCL-3DSGG** | **13.4/19.6/23.7** | **29.4/33.2/49.1** |

#### Table 4: 开放词汇 & Zero-shot 3DSGG (3DSSG, R@50/100)

| 方法 | OV-SGCLS | OV-PREDCLS | ZS-SGCLS | ZS-PREDCLS |
|------|----------|-------------|----------|-------------|
| KISGP | 19.3/24.8 | 38.1/44.6 | 15.7/20.1 | 32.0/38.9 |
| Chen et al. | 20.5/25.8 | 46.2/52.8 | 15.8/18.7 | 41.2/47.6 |
| VL-SAT | 23.1/29.4 | 60.3/66.9 | 21.6/28.1 | 43.5/59.4 |
| **CCL-3DSGG** | **37.1/42.3** | **64.8/71.2** | **35.5/40.6** | **49.1/65.7** |

### 关键对比

- **监督学习**（Table 1）：CCL-3DSGG 在两个子任务上全面超越 SOTA，Mean Recall **60.1**（vs. VL-SAT 54.4），Mean mR **51.3**（vs. VL-SAT 47.1）
- **无监督**（Table 3）：PREDCLS mR@20 达到 **29.4**，远超 VL-SAT 的 9.5（提升 **209%**）
- **开放词汇**（Table 4）：OV-PREDCLS R@50 **64.8**（vs. VL-SAT 60.3），SGCLS R@50 **37.1**（vs. 23.1，提升 **60.6%**）
- **Zero-shot**（Table 4）：较 VL-SAT 平均提升 **25.1%**，ZS-SGCLS R@50 **35.5**（vs. 21.6）
- **长尾谓词**（Table 2）：Tail mA@3 **61.24**（vs. VL-SAT 52.38），Unseen A@50 **36.72**（vs. 31.28）

### 消融实验 (Table 5, PREDCLS mR@K + 物体分类 A@K)

| Exp | 变体 | mR@20 | mR@50 | mR@100 | A@1 | A@5 |
|-----|------|-------|-------|--------|-----|-----|
| 1 | **Full method** | **29.4** | **33.2** | **49.1** | **49.2** | **73.1** |
| 2 | w/o Grammar Parse (sentence-level) | 6.8 | 10.7 | 26.6 | — | — |
| 3 | w/o Adjective Exchange | 25.8 | 31.8 | 47.8 | — | — |
| 4 | w/o I3D loss | 20.5 | 27.1 | 42.8 | 46.1 | 70.2 |
| 5 | w/o T3D loss | ≤EXP 2 | — | — | — | — |
| 7 | Learnable prompt | ≈ Full | — | — | — | — |
| 8 | + Object loss (L_obj) | — | — | — | **60.4** | **81.7** |
| 9 | + Predicate loss (L_pred) | **50.5** | **55.8** | **63.7** | — | — |
| 10 | w/o prompt (VL-SAT head) | 28.6 | 32.7 | 48.5 | — | — |
| 11 | Prediction head fine-tune | 40.7 | 48.1 | 53.7 | 52.6 | 74.8 |

### 消融分析

- **Grammar Parse 最关键**（EXP 2 → EXP 1）：mR@20 从 6.8 暴跌至 29.4，说明词级对齐对比 sentence-level 效果提升巨大（**+332%**）
- **Adjective Exchange 有效**（EXP 3）：mR@20 从 25.8 升至 29.4，提升 **14.0%**
- **文本主导**（EXP 4 vs EXP 5）：移除 I3D 损失仍能工作（20.5），移除 T3D 损失则彻底失效，说明文本特征是主要驱动
- **学习到的特征鲁棒**（EXP 10）：不使用 prompt 而用 VL-SAT 预测头，mR@20 仅从 29.4 略降至 28.6

## 定性结果

- 在 ScanNet 无标注数据上，CCL-3DSGG 能预测精确空间谓词（如 above, beside），而 VL-SAT 倾向预测 generic 的 close by。
- 能预测训练集不存在的谓词（如 mounted to, hanging in），展示了开放词汇泛化能力。
- 在 3DSSG 上，能区分易混淆物体（如 box 与 leaning against）和空间关系（如 in front of 与 behind）。

## 分析与评价

### 优势
- **完全无标注训练**：无需任何物体/关系手工标注，仅利用自然伴随的 caption 和多视角图像。
- **开放词汇能力强**：在 zero-shot 设置下超越已有监督方法，平均提升 VL-SAT 25.1%。
- **Grammar Parse 创新性强**：从 word-level 对齐的思路简单有效，打破了 sentence-level 对比学习的瓶颈。
- **消融实验充分**：11 个 ablation 实验系统验证了每个组件的贡献。
- **长尾友好**：在 tail 谓词和未见三元组上显著提升。

### 局限
- 依赖 caption 可用性（需与点云对应的自然语言描述）。
- 训练时间较长（48-50 小时 on RTX 2080Ti）。
- 监督模式下推理时间较高（30 秒/场景 vs. VL-SAT 24 秒），主要来自 prompt 计算。
- 未在更大规模 3D 数据集（如 ARKitScenes, Matterport3D）上验证。

### 与相关工作的关系
- 与 [[language-supervised-open-vocabulary-scene-graph-vs3]]（VS³, CVPR23）直接相关：两者均探索语言监督 SGG，但 CCL-3DSGG 扩展至 3D 领域并引入 Grammar Parse。
- 与 [[3d-spatial-multimodal-knowledge-accumulation-scene-graph-prediction-point-cloud]]（SMKA, CVPR23）相关：SMKA 使用 ConceptNet 外部知识，CCL-3DSGG 使用 CLIP 跨模态对齐。
- 与 [[pixels-to-graphs-open-vocabulary-sgg-vlm]]（PGSG, CVPR24）对比：PGSG 用 image-to-text 生成范式，CCL-3DSGG 用对比学习对齐范式。
- 与 VL-SAT [[待补全]] 直接对比：CCL-3DSGG 为 VL-SAT 的无监督/开放词汇扩展。

## Provenance

- **来源文件**: `sources/scene-graph/2024-CVPR-CLIP-Driven-Open-Vocabulary-3D-Scene-Graph.pdf`
- **提取文本**: `sources/scene-graph/2024-CVPR-CLIP-Driven-Open-Vocabulary-3D-Scene-Graph.txt`

## 参考资料
- Paper: CVPR 2024
- Dataset: 3DSSG [Wald et al., CVPR 2020], ScanNet [Dai et al., CVPR 2017]
- Base model: CLIP [Radford et al., ICML 2021], PointNet [Qi et al., CVPR 2017]
