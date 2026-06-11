---
title: "Linguistic Structures as Weak Supervision for Visual Scene Graph Generation"
type: paper
domain: scene-graph
status: active
created: 2026-06-10
updated: 2026-06-10
tags:
  - scene-graph-generation
  - weakly-supervised-learning
  - caption-supervision
  - linguistic-structures
  - phrasal-context
  - sequential-context
  - CVPR-2021
  - foundational
raw_sources:
  - ../../../raw/sources/2021-CVPR-linguistic-structures-as-weak-supervision-for-visual-scene-graph-generation.pdf
  - ../../../raw/sources/2021-CVPR-linguistic-structures-as-weak-supervision-for-visual-scene-graph-generation.txt
related_pages:
  - vspnet-scene-graph-generation-image-level-supervision.md
  - ppr-fcn-weakly-supervised-scene-graph-generation.md
  - llm4sgg-weakly-supervised-scene-graph-generation.md
  - ssc-sgg-semi-supervised-clustering-weakly-supervised-scene-graph-generation.md
  - graphical-contrastive-losses-for-scene-graph-parsing.md
evidence_level: full-paper
paper:
  title: "Linguistic Structures as Weak Supervision for Visual Scene Graph Generation"
  authors:
    - Keren Ye
    - Adriana Kovashka
  year: 2021
  venue: "Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2021"
  arxiv: null
  doi: null
  code: "https://github.com/yekeren/WSSGG"
  project: null
classification:
  label: "WSSGG — Caption-supervised Scene Graph Generation via Linguistic Structure Parsing"
  task:
    - Scene Graph Generation (SGGen)
    - Weakly-Supervised Scene Graph Generation (WSSGG)
    - Visual Relation Detection (VRD)
  method_family:
    - Caption-to-text-graph parsing
    - Graph Neural Network for phrasal context
    - Iterative grounding refinement (WSOD)
    - Sequential pattern RNN for commonsense reranking
  modality:
    - Image
    - Text (captions)
  datasets:
    - Visual Genome (VG)
    - COCO Captions
  metrics:
    - Recall@50 (R@50)
    - Recall@100 (R@100)
---

## Citation

> Keren Ye, Adriana Kovashka. "Linguistic Structures as Weak Supervision for Visual Scene Graph Generation." *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*, 2021.

## One-Sentence Contribution

提出利用图片描述（caption）中的**语言结构**作为弱监督信号，通过文本图解析、短语上下文 GNN 编码和序列模式 RNN 后处理，无需人工三元组标注即可训练场景图生成模型。

## Problem Setting

传统 SGG 方法依赖密集人工标注的 subject-predicate-object 三元组（带/不带 bbox），但场景图是整体性的（holistic）表示，而训练标注是局部的（local triplets），存在不一致性。本文提出用**图片描述（caption）**作为更易获取的弱监督源：

- Caption 提供**全局上下文**，可关联多个三元组
- Caption 可自动从互联网大规模获取，比人工标注三元组更具扩展性
- 挑战：caption 中的名词与三元组中标注的实体之间的对齐是弱对齐（weak alignment）

提出两种设置：
1. **Cap-Graph**：从 caption 中解析文本图作为监督
2. **GT-Graph**：从 ground-truth 场景图标注中构建文本图（忽略 bbox），作为上限基准

## Method

整体流程（Fig. 2）：从 caption 解析文本图 → GNN 编码短语上下文 → 文本实体与视觉区域注意力对齐 → 迭代精炼（WSOD 技术）→ 序列模式 RNN 后处理。

### 3.1 Phrasal Context 建模（+PHRASAL）

- 输入：caption 经语言 parser [41] 解析为文本图 $G_L = (E, R)$
  - $E = [e_1, ..., e_{n_e}]^T$：实体节点（ce 类）
  - $R = [(r_1, s_1, o_1), ..., (r_{n_r}, s_{n_r}, o_{n_r})]^T$：关系边（cr 类）
- 使用 TF-GraphNets 实现消息传递（Algorithm 1）：
  - 更新关系边表示：$r'_i = \phi_r(r_i, e_{s_i}, e_{o_i})$
  - 带权聚合到实体节点：$e'_i = \sum \alpha_j r'_j$
- 输出：上下文化的实体嵌入 $\psi(E; G_L) \in \mathbb{R}^{n_e \times d}$

### 3.2 文本-视觉关联（Grounding）

- 通过注意力机制将文本实体 $e_i$ 关联到视觉区域 $v_j$
- 注意力矩阵 $A^{(0)} \in \mathbb{R}^{n_e \times n_v}$，$g^{(0)}_i = \arg\max_j A^{(0)}[i, j]$
- 通过图像级实体分类交叉熵损失 $L_{grd}$ 训练注意力

### 3.3 初始场景图生成

- 从 grounding 结果解析伪标签 $Y_{det}, Y_{relsub}, Y_{relobj}$
- 学习从视觉特征直接预测实体检测 $P_{det}$ 和关系检测 $P_{rel}$（无 caption 辅助）
- 测试时 top-K 后处理（Eq. 6）：通过 NMS 搜索最优 5-tuple 集合最大化 log 概率

### 3.4 迭代精炼（+ITERATIVE）

- 借鉴 WSOD 技术 [45]，交替优化：
  - $P_{det}^{(t)}$：纯视觉预测
  - $Y_{det}^{(t+1)}$：融合 caption 实体信息的增强标签
- 默认迭代次数 $n_t = 3$

### 3.5 序列上下文建模（+SEQUENTIAL）

- LSTM 编码 subject→object→predicate 的序列模式
- 输入：GloVe 词嵌入 + 视觉 region 特征
- 训练：从 caption 文本图提取高质量三元组 $D_{gt}$ 作为监督
- 测试时 beam search（beam size=5）重新标注并重排 5-tuple
- 核心作用：剔除违反常识的预测（如 "plate-on-pizza" → "plate-under-pizza"）

### 总损失

$$L = L_{grd} + \beta\left(\sum_{t=0}^{n_t} L_{det}^{(t)} + L_{relsub} + L_{relobj}\right) + L_{cssub} + L_{csobj} + L_{cspred}$$

其中 $\beta = 0.5$ 用于平衡 grounding 和 detection 任务。

## Experiments

### 数据集

| 数据集 | 使用情况 | 划分 |
|--------|---------|------|
| Visual Genome (VG) | 108,077 张图片，5.4M region descriptions，3.8M objects，2.3M relations | Zareian et al. 划分：99,646 张（73,791/25,855 train/test），ce=200, cr=100；Xu et al. 划分：75,651/32,422 train/test，ce=150, cr=50 |
| COCO Captions 2017 | 118,287 张训练图片（去除 VG test 重复后 VG split 对应 106,401/102,786 张） | 仅用于 Cap-Graph 训练 |

### 学习任务三设置

1. **VG-GT-Graph**：从 VG ground-truth 场景图构建文本图（IoU>0.5 连接实体），隔离 caption 噪声和 parser 影响，用于公平对比
2. **VG-Cap-Graph**：从 VG region descriptions 解析文本图
3. **COCO-Cap-Graph**：从 COCO 图片级 caption 解析文本图

### 评估指标

- **Recall@50 / Recall@100**：预测的 top-50/100 三元组中，成功检索到的 ground-truth 三元组的比例。三标签正确且 subject/object bbox IoU ≥ 0.5 视为正确。

### Baseline 方法

**弱监督方法**（Zareian et al. 划分）：
- VtransE-MIL [56]
- PPR-FCN-single [57]
- PPR-FCN [57]
- VSPNet [54]

**全监督方法**（Xu et al. 划分）：
- IMP [48], MotifNet [55], Associative Embedding [34], MSDN [24], Graph R-CNN [49], VSPNet (Full) [54]

**消融变体**：
- **BASIC**：无短语上下文（$\psi(E, G_L) = H_{ent}^{(0)}$）
- **+PHRASAL**：使用短语上下文实体嵌入（Sec 3.1）
- **+ITERATIVE**：迭代精炼 grounding（$n_t=3$，Sec 3.4）
- **+SEQUENTIAL**：序列模式 RNN 后处理（Sec 3.5）

### 训练超参

- nv=20 proposals/image，dcnn=1536，Faster-RCNN（InceptionResnet backbone，OpenImage 预训练）
- Language parser：Bllip parser [41] via [47]'s implementation
- GloVe 300-dim embedding，frozen
- Batch size=32，lr=1e-5，Adam optimizer，TensorFlow distributed
- Weight decay=1e-6，random normal init (mean=0.0, stdev=0.01)
- LSTM：100 hidden units，dropout=0.2
- NMS：score threshold=0.01，IoU=0.4，max 4 instances/entity class
- Beam size=5

## Results

### VG-GT-Graph 设置

**Zareian et al. 划分（弱监督对比）**：

| Method | R@50 | R@100 |
|--------|------|-------|
| VtransE-MIL [56] | 0.71 | 0.90 |
| PPR-FCN-single [57] | 1.08 | 1.63 |
| PPR-FCN [57] | 1.52 | 1.90 |
| VSPNet [54] | 3.10 | 3.50 |
| **BASIC** | 2.20 | 2.88 |
| **+PHRASAL** | 2.77 | 3.62 |
| **+ITERATIVE** | 3.26 | 4.15 |
| **+SEQUENTIAL (Ours)** | **4.92** | **5.84** |

- 最终模型 R@50 **4.92**，比 VSPNet 提升 **59%**（4.92 vs 3.10）
- +PHRASAL 提升 BASIC 26%（2.77 vs 2.20）
- +ITERATIVE 提升 +PHRASAL 18%（3.26 vs 2.77）
- +SEQUENTIAL 提升 +ITERATIVE 51%（4.92 vs 3.26）

**Xu et al. 划分（全监督对比）**：

| Method | R@50 | R@100 |
|--------|------|-------|
| IMP [48] | 3.44 | 4.24 |
| MotifNet [55] | 6.90 | 9.10 |
| Associative Embedding [34] | 9.70 | 11.30 |
| MSDN [24] | 10.72 | 14.22 |
| Graph R-CNN [49] | 11.40 | 13.70 |
| VSPNet (Full) [54] | 12.60 | 14.20 |
| **BASIC** | 3.82 | 4.96 |
| **+PHRASAL** | 4.04 | 5.21 |
| **+ITERATIVE** | 6.06 | 7.60 |
| **+SEQUENTIAL (Ours)** | **7.30** | **8.73** |

- 仅使用图像级标注的弱监督方法，R@50 **7.30** 超越 IMP（3.44）和 MotifNet（6.90）
- +PHRASAL 提升 BASIC 6%（4.04 vs 3.82）
- +ITERATIVE 提升 +PHRASAL 50%（6.06 vs 4.04）
- +SEQUENTIAL 提升 +ITERATIVE 20%（7.30 vs 6.06）

### VG-Cap-Graph / COCO-Cap-Graph 设置

**VG-Cap-Graph**：

| Method | 评估：Zareian 划分 | 评估：Xu 划分 |
|--------|-------------------|--------------|
| | R@50 | R@100 | R@50 | R@100 |
| BASIC | 0.81 | 0.91 | 0.99 | 1.09 |
| +PHRASAL | 0.90 | 1.04 | 1.39 | 1.69 |
| +ITERATIVE | 1.11 | 1.32 | 1.79 | 2.22 |
| +SEQUENTIAL | **1.83** | **1.94** | **3.85** | **4.04** |

**COCO-Cap-Graph**：

| Method | 评估：Zareian 划分 | 评估：Xu 划分 |
|--------|-------------------|--------------|
| | R@50 | R@100 | R@50 | R@100 |
| BASIC | 1.20 | 1.51 | 2.09 | 2.63 |
| +PHRASAL | 1.17 | 1.47 | 1.65 | 2.16 |
| +ITERATIVE | 1.41 | 1.75 | 2.41 | 3.02 |
| +SEQUENTIAL | **1.95** | **2.23** | **3.28** | **3.69** |

- VG-Cap-Graph Xu 划分 R@50 **3.85**，接近全监督 IMP（3.44）
- COCO-Cap-Graph 下 +PHRASAL 轻微下降，归因于 COCO caption 与 VG GT 三元组分布差异大（Fig. 3 展示关系频率差异）
- Fig. 3 显示 "has"、"near" 在 caption 中很少出现但在 GT 场景图中常见；"of"、"with"、"at" 在 caption 中频繁但很少标注为关系

### 定性结果

- Fig. 4：+PHRASAL 帮助 grounding 避免卡在局部区域（如头部）或错误关注整图
- Fig. 5：+SEQUENTIAL 纠正违反常识的预测，"plate-on-pizza"（logprob=-1.32）被纠正为 "plate-under-pizza"（logprob=-1.91）；"person-wear-person"（logprob=-2.25）被纠正为 "person-wear-shirt"（-2.56）

## Limitations

1. **分布偏移**：caption 中使用的动词和介词分布与场景图标注的关系分布存在显著差异（Fig. 3），导致 Cap-Graph 设置下性能上限受限
2. **依赖 parser 质量**：Cap-Graph 设置完全依赖语言 parser [41] 从 caption 中提取结构化文本图的能力
3. **caption 覆盖度**：caption 可能未穷尽描述图片中的所有实体和关系，导致漏标注
4. **关系频率长尾**：某些关系（如 "has"、"near"）在 caption 中极少出现，模型难以学习预测
5. **与全监督方法仍有差距**：虽超越早期全监督方法（IMP、MotifNet），但与强全监督方法（Graph R-CNN R@50 11.40、MSDN 10.72）差距明显

## Reusable Claims

1. **Caption 的语言结构可替代三元组标注作为弱监督**：通过文本图解析 + 多阶段精炼，caption 监督可以有效训练 SGG 模型，且可扩展到 COCO 这种只有图片级 caption 的数据集
2. **短语上下文（phrasal context）改善语言-视觉 grounding**：使用 GNN 在文本图上传播上下文关系，比独立词嵌入更精确地定位图像中的实体
3. **序列模式建模可纠正违反常识的三元组**：显式建模 subject→object→predicate 的 N-gram 语言模式，有效修剪不合理的预测
4. **迭代 WSOD 精炼提升 grounding 鲁棒性**：交替使用 caption 引导的注意力标签和纯视觉预测，缓解 caption 噪声和注意力漂移
5. **Caption 与场景图标注之间存在系统性的分布偏移**："has"、"near" 等关系在 caption 中低频但在 GT 中高频，是弱监督 SGG 的核心挑战

## Connections

- 与 **VSPNet [54]** 最直接相关：VSPNet 也使用图像级三元组标注的弱监督，但未利用 caption 中的语言结构；本文在 VSPNet 的基础上增加了文本图感知
- 与 **PPR-FCN [57]** 同为弱监督 SGG 早期工作，但本文首次将 caption 语言结构引入弱监督 SGG
- 后续工作 **LLM4SGG (CVPR 2024)** 使用大语言模型进行三元组提取和序列推理，部分继承了本文的 caption-as-supervision 范式
- **SSC-SGG (AAAI 2025)** 使用半监督聚类改进弱监督 SGG，可视为对本文弱监督范式的延续
- 本文的 GT-Graph vs Cap-Graph 双重实验设置成为后续弱监督 SGG 的标准评估范式

## Open Questions

1. 如何缩小 caption 关系分布与场景图标注分布之间的差距？能否通过合成数据或数据增强弥合？
2. 是否可以引入 AMR（Abstract Meaning Representation）等更丰富的语言结构替代本文使用的依存解析图？
3. 弱监督 SGG 的上限是多少？在完全接入 LLM（如 GPT-4/VLM 联合推理）后，弱监督能否接近全监督？
4. 多模态大模型（如 CLIP）能否替代本文的独立 Faster-RCNN + 文本图解析两阶段流程？

## Provenance

- **Raw PDF**: `raw/sources/2021-CVPR-linguistic-structures-as-weak-supervision-for-visual-scene-graph-generation.pdf` (3.4 MB)
- **Extracted text**: `raw/sources/2021-CVPR-linguistic-structures-as-weak-supervision-for-visual-scene-graph-generation.txt` (55,837 chars, 1,461 lines)
- **Evidence level**: `full-paper` — 全文 PDF 精读，涵盖 Abstract、Intro、Related Work、Method (Sec 3.1-3.5)、Experiments (Sec 4)、Results (Tab. 2, 3, Fig. 3-6) 和 Conclusion
- **URL**: https://openaccess.thecvf.com/content/CVPR2021/papers/Ye_Linguistic_Structures_As_Weak_Supervision_for_Visual_Scene_Graph_Generation_CVPR_2021_paper.pdf
- **Code**: https://github.com/yekeren/WSSGG
