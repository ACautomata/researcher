---
title: "ReLIC-SGG: Relation Lattice Completion for Open-Vocabulary Scene Graph Generation"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags: [open-vocabulary, relation-completion, positive-unlabeled-learning, relation-lattice, false-negative]
source_pages: []
raw_sources:
  - raw/sources/2026-04-ReLIC-SGG.pdf
  - raw/sources/2026-04-ReLIC-SGG.txt
related_pages:
  - domains/scene-graph/papers/pixels-to-graphs-open-vocabulary-sgg-vlm.md
  - domains/scene-graph/papers/ovsgtr-expanding-scene-graph-boundaries.md
  - domains/scene-graph/papers/cage-sgg-counterfactual-active-graph-evidence-open-vocabulary-sgg.md
  - domains/scene-graph/papers/prototype-based-embedding-network-scene-graph-generation.md
paper:
  title: "ReLIC-SGG: Relation Lattice Completion for Open-Vocabulary Scene Graph Generation"
  authors: "Amir Hosseini, Sara Farahani, Xinyi Li, Suiyang Guang"
  year: 2026
  venue: "arXiv preprint"
  arxiv: "2604.22546v6"
  code: null
  project: null
  doi: null
classification:
  label: "Relation-Incompleteness-Aware Open-Vocabulary SGG"
  task:
    - open-vocabulary scene graph generation
    - panoptic scene graph generation
    - conventional scene graph generation
  method_family:
    - positive-unlabeled learning
    - relation lattice reasoning
    - latent variable modeling
    - graph-level semantic consistency
  modality:
    - image
    - text (relation phrases)
  datasets:
    - Visual Genome (VG150)
    - Panoptic Scene Graph (PSG)
  metrics:
    - Recall@K
    - mean Recall@K (mR@K)
    - Seen mean recall (S-mR)
    - Unseen mean recall (U-mR)
    - Harmonic mean (HM)
    - FN-Recall
    - Lat-Cons
    - Redundancy
evidence_level: full-paper
---

# ReLIC-SGG: Relation Lattice Completion for Open-Vocabulary Scene Graph Generation

## Citation

Amir Hosseini, Sara Farahani, Xinyi Li, Suiyang Guang. "ReLIC-SGG: Relation Lattice Completion for Open-Vocabulary Scene Graph Generation." arXiv preprint arXiv:2604.22546v6, May 2026.

## One-Sentence Contribution

将未标注关系视为潜在变量而非确定负样本，通过语义关系格（relation lattice）完成缺失正标签的补全，解决开放词汇 SGG 中的标注不完整问题。

## Problem Setting

开放词汇场景图生成（open-vocabulary SGG）的目标是超越固定谓语集合，用灵活的自然语言关系短语描述视觉场景。现有方法将标注 triplet 视为正样本、未标注的 object-pair 关系视为负样本。然而场景图标注天然不完整：同一交互可用不同粒度描述（如 on / standing on / resting on / supported by），许多有效关系未被标注。在开放词汇场景下，谓语空间大幅扩大，这一问题更加严重。因此模型可能因虚假负样本监督而抑制正确但未标注的关系预测。

## Method

ReLIC-SGG 的核心思想是将未标注关系视为潜在变量 z<sub>ij</sub><sup>r</sup> ∈ {0,1}，而非直接设为 0。框架包含四个组件：

### 1. 开放词汇关系提议（Open-Vocabulary Relation Proposal）
对每个 object pair (o<sub>i</sub>, o<sub>j</sub>)，使用 CLIP ViT-B/16 构建视觉配对表示（包含 subject 外观、object 外观、联合区域、空间几何特征），与每个关系短语的文本嵌入计算余弦相似度，保留 top-K（K=15）候选。

### 2. 语义关系格（Semantic Relation Lattice）
构建有向图 L = (R<sub>open</sub>, A)，边分为三类：
- **相似边（A<sub>sim</sub>）**：连接语义相近的谓语（如 resting on ↔ supported by）
- **蕴含边（A<sub>ent</sub>）**：细粒度→粗粒度（如 standing on → on）
- **矛盾边（A<sub>con</sub>）**：互斥谓语（如 in front of ↔ behind）

通过边权重 w(r, r′) = sim(t<sub>r</sub>, t<sub>r′</sub>) 传播置信度，抑制矛盾谓语的分数。

### 3. 潜在关系补全（Latent Relation Completion）
对每个未标注候选，计算后验概率 q<sub>ij</sub><sup>r</sup> = σ(α ˜s<sub>ij</sub><sup>r</sup> + β c<sub>ij</sub><sup>r</sup> + γ g<sub>ij</sub><sup>r</sup> − δ n<sub>ij</sub><sup>r</sup>)，融合：
- 格校准分数 ˜s<sub>ij</sub><sup>r</sup>（视觉-语言兼容性）
- 格一致性 c<sub>ij</sub><sup>r</sup>（语义相近谓语的支撑）
- 图上下文 g<sub>ij</sub><sup>r</sup>（局部场景图结构，Graph Transformer）
- 矛盾抑制 n<sub>ij</sub><sup>r</sup>

同时估计可靠负样本分数 ρ<sub>ij</sub><sup>r</sup> = (1−q<sub>ij</sub><sup>r</sup>)·σ(η n<sub>ij</sub><sup>r</sup> − µ ˜s<sub>ij</sub><sup>r</sup>)，仅在高可信时抑制。

### 4. 正-无标注图学习（Positive-Unlabeled Graph Learning）
损失函数 L = L<sub>PU</sub> + λ<sub>lat</sub> L<sub>lat</sub> + λ<sub>cmp</sub> L<sub>cmp</sub>：
- **L<sub>PU</sub>**：正样本风险 + 软目标无标注风险，不将未标注直接视为负样本
- **L<sub>lat</sub>**：图级格损失（惩罚矛盾谓词同时被接受，保持蕴含一致性）
- **L<sub>cmp</sub>**：紧凑性正则化（根据 object-pair 交互强度自适应控制关系密度）

### 训练策略
三阶段训练：1) 预热关系评分器；2) 构建语义格并初始化潜在后验；3) 联合优化所有组件。使用 stop-gradient 防止伪标签退化。

### 格引导解码（Lattice-Guided Graph Decoding）
推理时结合格校准分数和潜在补全后验：ˆs<sub>ij</sub><sup>r</sup> = ˜s<sub>ij</sub><sup>r</sup> + λ<sub>q</sub> q<sub>ij</sub><sup>r</sup>。矛盾对保留高分者，相似谓词保留最具体者。

## Experiments

### 数据集与设置
- **VG150**：Visual Genome 的 150 类物体 / 50 类谓语标准划分，报告 PredCls / SGCls / SGDet
- **开放词汇 VG 划分**：频繁谓语→seen，稀有谓语→unseen
- **PSG**：全景场景图生成
- **检测器**：Faster R-CNN + ResNeXt-101-FPN；PSG 用 Mask2Former
- **文本编码**：CLIP ViT-B/16
- **优化器**：AdamW，lr=1×10<sup>−4</sup>，batch size=12，K=15 候选/object pair

### 指标
- Recall@K (R@K) 和 mean Recall@K (mR@K)
- Seen/Unseen mean recall (S-mR, U-mR) 和 HM
- 新增：FN-Recall（缺失关系恢复率）、Lat-Cons（语义格一致性）、Redundancy（冗余度，越低越好）

### Baselines
- **VG150**：Motifs、VCTree、TDE、BGNN、PE-Net、Pix2Graphs、VL-IRM
- **开放词汇**：CLIP-ZS、OV-SGG、OvSGTR、Pix2Graphs、OpenPSG、VL-IRM
- **PSG**：PSGTR、Pair-Net、OpenPSG、SPADE

## Results

### 表1：VG150 常规 SGG（PredCls / SGCls / SGDet）

| Method | PredCls mR@50 | PredCls mR@100 | SGCls mR@50 | SGCls mR@100 | SGDet mR@50 | SGDet mR@100 |
|--------|:---:|:---:|:---:|:---:|:---:|:---:|
| Motifs | 14.6 | 15.8 | 7.9 | 8.5 | 6.5 | 7.3 |
| VCTree | 16.1 | 17.5 | 8.8 | 9.6 | 7.4 | 8.2 |
| TDE | 18.5 | 20.1 | 10.9 | 12.0 | 9.8 | 10.9 |
| BGNN | 20.2 | 22.0 | 12.3 | 13.5 | 10.7 | 11.8 |
| PE-Net | 23.1 | 25.0 | 14.2 | 15.4 | 12.6 | 13.8 |
| Pix2Graphs | 24.6 | 26.5 | 15.3 | 16.7 | 13.6 | 14.9 |
| VL-IRM | 25.4 | 27.2 | 16.0 | 17.4 | 14.2 | 15.6 |
| **ReLIC-SGG** | **29.1** | **31.0** | **19.3** | **21.1** | **16.4** | **18.2** |

ReLIC-SGG 在所有三个任务上取得最佳 mR@K。在 SGDet 上收益最大（mR@50 16.4 vs. VL-IRM 14.2，+2.2），说明关系补全在标注稀疏时尤为有效。

### 表2：开放词汇 VG

| Method | S-mR@50 | U-mR@50 | HM@50 | S-mR@100 | U-mR@100 | HM@100 |
|--------|:---:|:---:|:---:|:---:|:---:|:---:|
| CLIP-ZS | 18.3 | 7.4 | 10.5 | 19.8 | 8.2 | 11.6 |
| OV-SGG | 22.6 | 9.8 | 13.7 | 24.1 | 10.9 | 15.0 |
| OvSGTR | 23.8 | 10.6 | 14.7 | 25.2 | 11.8 | 16.0 |
| Pix2Graphs | 24.9 | 11.5 | 15.7 | 26.5 | 12.6 | 17.0 |
| OpenPSG | 25.7 | 12.1 | 16.5 | 27.3 | 13.3 | 17.9 |
| VL-IRM | 26.4 | 12.8 | 17.2 | 28.1 | 14.0 | 18.7 |
| **ReLIC-SGG** | **28.6** | **18.3** | **22.3** | **30.2** | **19.8** | **23.9** |

U-mR@50 从 VL-IRM 的 12.8 提升至 **18.3**（+5.5），HM@50 从 17.2 提升至 **22.3**（+5.1）。未见类提升显著大于见类，证实语义格可将有标注谓语的监督转移到语义相近的未见谓语。

### 表3：PSG 全景场景图生成

| Method | PR@50 | PR@100 | PmR@50 | PmR@100 |
|--------|:---:|:---:|:---:|:---:|
| PSGTR | 31.8 | 36.5 | 13.4 | 15.1 |
| Pair-Net | 34.2 | 39.0 | 15.7 | 17.6 |
| OpenPSG | 36.7 | 41.2 | 17.5 | 19.4 |
| SPADE | 38.1 | 42.8 | 18.8 | 21.0 |
| **ReLIC-SGG** | **40.8** | **45.6** | **22.0** | **24.3** |

PmR@50 22.0 vs. SPADE 18.8（+3.2），mask 级关系预测场景下关系补全同样有效。

### 表4：False-Negative-Aware 评估

| Method | FN-Recall↑ | Lat-Cons↑ | Redundancy↓ |
|--------|:---:|:---:|:---:|
| Motifs | 21.4 | 61.2 | 18.7 |
| PE-Net | 27.8 | 66.5 | 16.2 |
| Pix2Graphs | 31.6 | 69.8 | 15.4 |
| VL-IRM | 34.2 | 71.3 | 14.1 |
| **ReLIC-SGG** | **45.7** | **82.6** | **9.3** |

FN-Recall 45.7（+11.5 vs. VL-IRM），Lat-Cons 82.6（+11.3），Redundancy 9.3（−4.8）。直接证明 ReLIC-SGG 能有效恢复缺失的有效关系。

### 表5：消融实验（SGDet，开放词汇 VG）

| Variant | SRL | LRC | RNE | PUGL | LGD | S-mR@50 | U-mR@50 | HM@50 | FN-Recall | Redundancy |
|---------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Baseline | – | – | – | – | – | 24.1 | 9.6 | 13.7 | 24.8 | 18.9 |
| + SRL | ✓ | – | – | – | – | 25.4 | 12.1 | 16.4 | 29.7 | 16.5 |
| + LRC | ✓ | ✓ | – | – | – | 26.8 | 15.6 | 19.7 | 38.9 | 14.2 |
| + RNE | ✓ | ✓ | ✓ | – | – | 27.3 | 16.4 | 20.5 | 41.2 | 13.5 |
| + PUGL | ✓ | ✓ | ✓ | ✓ | – | 28.1 | 17.5 | 21.5 | 43.6 | 12.8 |
| **Full** | ✓ | ✓ | ✓ | ✓ | ✓ | **28.6** | **18.3** | **22.3** | **45.7** | **9.3** |

各组件均有正向贡献。PUGL（正-无标注图学习）和 LRC（潜在关系补全）对 U-mR 的贡献最大。LGD（格引导解码）主要降低冗余度。

### 表6：格构建方式的影响

| Lattice Type | S-mR@50 | U-mR@50 | HM@50 | Lat-Cons | Redundancy |
|--------------|:---:|:---:|:---:|:---:|:---:|
| None | 24.1 | 9.6 | 13.7 | 63.5 | 18.9 |
| Similarity only | 25.4 | 12.1 | 16.4 | 70.8 | 16.5 |
| Sim + Entailment | 27.0 | 15.7 | 19.9 | 76.1 | 14.8 |
| Sim + Contradiction | 26.5 | 14.9 | 19.0 | 78.4 | 11.6 |
| Full lattice | 28.6 | 18.3 | 22.3 | 82.6 | 9.3 |

三种边类型各有作用：相似边传播监督，蕴含边保持分层一致性，矛盾边抑制不兼容谓词。完整格优于任意子集。

### 表7：候选数 K 的敏感性

| K | S-mR@50 | U-mR@50 | HM@50 | FN-Recall | Redundancy |
|:-:|:---:|:---:|:---:|:---:|:---:|
| 5 | 26.2 | 14.6 | 18.7 | 36.5 | 7.8 |
| 10 | 27.8 | 17.2 | 21.2 | 43.1 | 8.6 |
| **15** | **28.6** | **18.3** | **22.3** | 45.7 | **9.3** |
| 20 | 28.5 | 18.1 | 22.1 | 46.0 | 11.8 |
| 30 | 28.1 | 17.6 | 21.7 | 46.3 | 15.4 |

K=15 是最优折中。K 偏小会遗漏有效细粒度候选，K 偏大会引入噪声导致 HM 下降和冗余上升。

## Limitations

1. **语义格构建的依赖**：蕴含边和矛盾边的构建需要人工规则和模板，在扩展到更多领域时可能不可扩展。
2. **计算开销**：对每个 object pair 维护 top-K 候选并进行格传播，在大规模场景中计算成本较高。
3. **评估局限**：FN-aware 评估仅验证了一部分高置信度未标注预测，未覆盖完整的缺失关系空间。
4. **格边权重的文本相似度依赖**：纯文本相似度对反义词不鲁棒（antonyms 可能在嵌入空间中靠近），需额外规则补偿。

## Reusable Claims

- **Claim**: 场景图标注存在系统性的不完整性问题，将未标注关系视为负样本会在开放词汇 SGG 中引入大量虚假负样本。
  - **Evidence**: Table 4—VL-IRM 的 FN-Recall 仅 34.2%，即约 65.8% 的缺失有效关系未被基线方法识别。
  - **Confidence**: high
- **Claim**: 语义关系格（similarity + entailment + contradiction）能有效在谓语间转移监督信号，提升未见类谓词识别。
  - **Evidence**: Table 5—添加 SRL 使 U-mR@50 从 9.6 提升至 12.1（+2.5），完整格达到 18.3（+8.7 vs. baseline）。
  - **Confidence**: high
- **Claim**: 正-无标注图学习（PUGL）是贡献最大的组件，通过避免虚假负样本惩罚提升稀有和未见关系预测。
  - **Evidence**: Table 5—PUGL 的独立贡献 U-mR@50 从 16.4 提升至 17.5（+1.1）。
  - **Confidence**: high
- **Claim**: 开放词汇 SGG 中的 U-mR（未见类召回）改进显著大于 S-mR（见类召回），说明该方法主要解决标注不完整而非过拟合问题。
  - **Evidence**: Table 2—U-mR@50 从 VL-IRM 的 12.8 升至 18.3（+5.5），S-mR@50 从 26.4 升至 28.6（+2.2）。
  - **Confidence**: high
- **Claim**: 候选数 K=15 在覆盖率和可靠性之间取得最佳平衡。
  - **Evidence**: Table 7—HM@50 在 K=15 时最高（22.3），K=30 时降至 21.7。
  - **Confidence**: medium (依赖于实验设置)

## Connections

- **Related methods**: 与 TDE [20] 的因果去偏、PE-Net [22] 的原型学习、VL-IRM [16] 的视觉-语言交互挖掘共同处理 SGG 中的标注偏差问题，但 ReLIC-SGG 首次显式建模标注不完整性。
- **Related theories**: 连接正-无标注学习（PU learning）[36,37] 和部分标签学习（partial-label learning）[38,39]，但针对结构化场景图预测做了专门设计。
- **Grounding**: 与 [[pixels-to-graphs-open-vocabulary-sgg-vlm.md|PGSG（Pix2Graphs）]] 共享 CLIP 视觉-语言对齐基础，但增加了关系不完整性的显式处理。
- **OpenPSG comparison**: 与 [[cage-sgg-counterfactual-active-graph-evidence-open-vocabulary-sgg.md|CAGE-SGG]] 同为开放词汇 SGG 方法，ReLIC-SGG 侧重于标注补全，CAGE-SGG 侧重于反事实主动证据。

## Open Questions

1. **格边构建的自动化**：能否用 LLM 自动生成蕴含/矛盾边而不依赖人工规则？
2. **与其他 SGG 偏差类型的交互**：标注不完整性与长尾分布、因果混淆之间的交互关系尚不明确。
3. **召回-精确度权衡**：FN-Recall 提升是否以引入更多假正为代价？论文中 Redundancy 指标部分回答了但不够充分。
4. **跨领域迁移**：在 COCO、VG-200 等更大规模数据集上的泛化性如何？
5. **时域/3D 场景的扩展**：论文声称框架可扩展到 video 和 3D SGG，但未提供实验验证。

## Provenance

- Raw source: `raw/sources/2026-04-ReLIC-SGG.pdf` (1.5 MB PDF, 11 pages)
- Extracted text: `raw/sources/2026-04-ReLIC-SGG.txt` (50,608 chars)
- Evidence level: **full-paper** — 全文 11 页已提取，包含完整的方法公式、实验结果表和消融分析
- arXiv: 2604.22546v6, dated May 2026
- 作者单位：Amirkabir University of Technology
