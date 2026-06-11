---
title: "MovieGraphs: Towards Understanding Human-Centric Situations from Videos"
type: paper
domain: scene-graph
status: active
created: 2026-06-10
updated: 2026-06-10
tags:
  - video-sgg
  - dataset
  - cvpr-2018
source_pages: []
raw_sources:
  - raw/sources/2018-CVPR-MovieGraphs-Towards-Understanding-Human-Centric-Situations-from-Videos.pdf
  - raw/sources/2018-CVPR-MovieGraphs-Towards-Understanding-Human-Centric-Situations-from-Videos.txt
related_pages: []
paper:
  title: "MovieGraphs: Towards Understanding Human-Centric Situations from Videos"
  authors:
    - Paul Vicol
    - Makarand Tapaswi
    - Lluís Castrejón
    - Sanja Fidler
  year: 2018
  venue: CVPR 2018
  arxiv: "1712.06761"
  code: null
  project: "http://moviegraphs.cs.toronto.edu"
classification:
  label: "scene-graph-generation, video-sgg, dataset"
  task:
    - graph-based video retrieval
    - interaction ordering
    - reason prediction
  method_family:
    - graph-structured retrieval
    - structured prediction
  modality: video
  datasets:
    - MovieGraphs
  metrics:
    - Recall@K (R@1, R@5, R@10)
    - Median Rank
    - Acc@FullySorted
    - Longest Common Subsequence (LCS)
evidence_level: full-paper
---

## Citation

Paul Vicol, Makarand Tapaswi, Lluís Castrejón, Sanja Fidler. "MovieGraphs: Towards Understanding Human-Centric Situations from Videos." CVPR 2018. arXiv:1712.06761.

## One-Sentence Contribution

提出 MovieGraphs 数据集——从 51 部电影中标注 7637 个视频片段的图结构社会情境数据——并设计图查询视频检索、交互排序和原因预测三个任务作为视频情境理解的基准。

## Problem Setting

### 动机
要使 AI 具备社会智能，机器需要理解人的情绪、动机、人际关系等影响行为的因素。现有视频理解数据集主要关注动作分类或物体关系，缺少对 **人类中心社会情境 (human-centric situations)** 的结构化标注。

### 任务
论文定义了三个情境理解代理任务：
1. **Graph-based Video Retrieval**：以图作为查询，从数据集中检索最相关的视频片段（含视频和对话两种模态）；
2. **Interaction Ordering**：给定一对角色间的交互集合，预测它们在真实场景中发生的合理顺序；
3. **Reason Prediction**：给定场景、情境、属性、关系和交互的子图，预测交互发生的合理原因（动机）。

### 评估指标
- Retrieval: Recall@K (K=1,5,10)、Median Rank
- Interaction Ordering: Fully Sorted Accuracy、Longest Common Subsequence (LCS)
- Reason Prediction: AMT 人工评分（Very relevant / Semi-relevant / Not relevant）

## Method

### 数据集构建 (MovieGraphs Dataset)

**规模**：51 部电影 → 7637 个剪辑片段。每部电影先自动分割为场景，再人工调整边界使每个片段对应一个社会情境。

**图结构**：每片段包含 8 种节点类型——
- **Character**：角色节点，通过 IMDb 获取角色名，与视频中的 face track 关联
- **Attribute**：角色属性（年龄、性别、种族、职业、外貌、心智状态、情绪）
- **Relationship**：角色间关系（家庭/朋友/浪漫/工作），可标记开始/结束
- **Interaction**：交互（verbal/non-verbal，directed/bidirectional）
- **Summary Interaction**：多个局部交互的概括
- **Topic**：附加在交互上的主题细节
- **Reason**：交互或情绪的动机（推理型信息）
- **Timestamp**：交互或情绪状态在视频中的时间区间

此外还有 scene label（场景位置）和 situation label（情境主题）以及自然语言描述。

**标注过程**：通过 Upwork 雇佣专业标注员，每个标注员负责完整标注一部电影以保证全局一致性。标注经过交叉检查和训练阶段。

**数据集统计**：每片段平均 2.98 角色、3.07 交互、13.76 属性、3.15 关系、2.65 主题、1.74 原因；平均时长 44.28 秒；train/val/test 按 10:2:3 比例分配（无跨集电影重叠）。

### 图查询视频检索模型

**核心公式**：学习评分函数 $F_θ(M, G)$ 衡量视频片段 $M$ 与查询图 $G$ 的相似度。

**对齐变量**：引入 $z = (z_1, ..., z_N)$ 将 $N$ 个角色节点对齐到 $K$ 个 face cluster。

**评分函数**：
$$F_θ(M, G, z) = φ_{sc}(v_{sc}) + φ_{si}(v_{si}) + \sum_i[φ_{ch}(v_{ch}^i, z_i) + φ_{att}(V_{att}^i, z_i)] + \sum_{i,j}[φ_{int}(V_{int}^{ij}, z_i, z_j) + φ_{rel}(V_{rel}^{ij}, z_i, z_j)]$$

其中 $φ$ 为势函数，使用 GloVe 词向量 + 可学习线性映射将查询节点嵌入与视频特征映射到联合空间，计算余弦相似度。

**视频特征**：Hybrid1365-VGG pool5 特征（时空平均池化）、年龄/性别预测 CNN、情绪预测 CNN。

**人脸识别**：VGG-16 fine-tune + triplet loss，从 IMDb 收集角色照片用于 person identification。

**对话评分**：额外学习函数 $Q(D, G)$ 计算图与对话文本的匹配度（每对单词取最大相似度后求和）。

**学习**：max-margin ranking loss，Adam 优化器 (lr=0.0003)。负样本分三类：其他电影片段（易）、同电影不同片段（中）、同片段错误对齐（难）。

### 交互排序模型

使用 attention-based GRU decoder（单层 100 hidden），以 scene/situation/relationship/attribute 的 GloVe embedding 为 context，逐个预测交互序列。训练时 teacher-forcing，测试时用模型自己的预测。

### 原因预测模型

单层 GRU decoder（100 hidden），以 scene description 为 context 逐词生成 reason。温度 0.6 用于采样多样性。

## Experiments

### 数据集划分
- 训练集：34 部电影（5050 clips）
- 验证集：7 部电影（1060 clips）
- 测试集：10 部电影（1527 clips）

### Graph-based Retrieval 实验设置

**Baselines & 消融**：
- 文本检索基线：TF·IDF、GloVe max-sum、GloVe idf·max-sum
- 随机基线：随机检索（movie unknown / movie known）
- 组件消融：scene only / scene+situation / +attributes / +interactions+relationships / +dialog
- 人脸设置消融：predicted clustering + predicted ID / ground-truth clustering + ground-truth ID

**视频特征**：每 5 帧提取 Hybrid1365-VGG pool5，再时空平均池化得到 512-d clip 表示。

**人脸聚类**用聚类纯度评估（weighted clustering purity），**person ID** 用 track-level 准确率。

### Interaction Ordering 实验设置

给定两个角色间的交互集合（含 topic、direction），训练 attention-based GRU 按合理顺序排序。评估：Fully Sorted Accuracy、LCS。

### Reason Prediction 实验设置

在 test 集上取 100 个子图，由 10 名 AMT worker 对预测原因评分（Very relevant / Semi-relevant / Not relevant）。10 名标注员中 6 人以上意见一致视为 clear verdict。

## Results

### Face Processing
- **Weighted clustering purity**：75.8%（视频人均 9.2 个 face track，汇聚为 2.1 个 GT cluster）
- **Person ID track-level accuracy**：43.7%（vs. random chance 13.2%）

### Graph-based Retrieval (Table 3)

**Description Retrieval**（图 → 描述文本）：
| Method | R@1 | R@5 | R@10 | med-R |
|--------|-----|-----|------|-------|
| TF·IDF | 61.6 | 83.8 | 89.7 | 1 |
| GloVe max-sum | 62.1 | 81.3 | 87.2 | 1 |
| GloVe idf·max-sum | 61.3 | 81.6 | 86.9 | 1 |

**Dialog Retrieval**（图 → 对话文本）：
| Method | R@1 | R@5 | R@10 | med-R |
|--------|-----|-----|------|-------|
| TF·IDF | 31.8 | 49.8 | 57.2 | 6 |
| GloVe max-sum | 28.0 | 42.4 | 50.2 | 10 |
| GloVe idf·max-sum | 28.7 | 43.1 | 50.2 | 10 |

**Movie Clip Retrieval**（图 → 视频+对话融合）：
- Scene only (row 9): med-R 141.5 (vs. random 764)
- Scene+Situation (row 10): med-R 140
- Full graph + predicted cluster/ID (row 12): R@1 2.7, med-R 59
- Full graph + GT cluster/ID (row 14): R@1 13.0, R@5 37.4, R@10 50.4, med-R 10
- Full graph + dialog + pred cluster/ID (row 15): R@1 31.6, R@5 50.4, R@10 56.6, med-R 5
- Full graph + dialog + GT cluster/ID (row 16): **R@1 40.4, R@5 62.1, R@10 71.1, med-R 3**  — 全文最佳

### Interaction Ordering (Table 4)
- Fully Sorted Accuracy: **40.5%** (chance 27%)
- LCS: **0.74** (chance 0.67)

### Reason Prediction
- 在 100 个测试子图中，72 个 (72%) 获得 clear verdict（≥6 标注员同意）
- 其中 11 个被评价为 Very relevant，10 个 Semi-relevant
- 图 8 展示了两例结果：left example (thanks + for saving him during the war → "for his help") 被评价为 Very relevant；failure case (mocks + the food has an urgent) 被评价为 Not relevant

### TF·IDF 消融研究 (Table 6 & 7)
- 对 Description Retrieval，最具有判别力的节点类型：Character (med-R 7)、Topic (med-R 5)、Reason (med-R 26)
- 删除 {Scene, Situation, Character} 后 R@1 从 61.6 降至 51.0
- Scene 单独仅 R@1 3.1，Situation 单独仅 R@1 5.0

## Limitations

1. **Person ID 准确率低 (43.7%)**：跨年代电影中 IMDb gallery 图片与视频 face track 差异大，限制了视觉检索性能。使用 GT cluster/ID 后 med-R 从 59 提升至 10 表明视觉特征是检索瓶颈。
2. **Reason Prediction 缺乏自动评估指标**：由于原因生成任务有多样正确答案，无法用标准 captioning 指标自动评估，依赖昂贵的 AMT 人工评分。
3. **数据规模有限**：51 部电影、7637 片段，覆盖的情境类型有限。
4. **社会偏见风险**：电影角色刻板印象可能被数据集继承。
5. **未开源代码**（截至论文发表时待发布）。

## Reusable Claims

1. **图结构比自然语言更适合时间/视觉定位的情境表示**：相比文本描述，图结构能显式地关联角色、属性、关系和交互，且能赋予时间戳实现视频定位。
2. **图 → 视频检索中 face identification 是关键瓶颈**：predicted ID (43.7%) 到 GT ID 的差距导致检索 med-R 从 59 降到 10，说明高质量 face ID 能大幅改善视频情境理解。
3. **Topic 和 Reason 节点在情境检索中判别力最强**：单独 Topic 节点即可实现 med-R 5，Reason 节点 med-R 26，远优于 Scene (med-R 460) 或 Relationship (med-R 704)。
4. **视频 + 对话融合显著提升检索性能**：加入对话后 R@1 从 13.0 提升至 40.4 (GT cluster/ID)，对话模态包含大量交互和情绪线索。
5. **电影情境具有时序连贯性**：相邻片段的情境标签呈现可预测的转移模式（图 5），角色情绪随时间线平滑演化（图 2）。

## Connections

- **Image Scene Graphs (Johnson et al., CVPR 2015)**：MovieGraphs 将图像场景图扩展到了视频中的人类中心情境，节点类型从物体关系转变为人的属性、交互和动机。
- **Image Situation Recognition (Yatskar et al., CVPR 2016)**：此前的图像情境识别局限于单帧、单动作，MovieGraphs 将其扩展到多角色、多交互、带时间跨度的视频片段。
- **Video Q&A / Video Description (LSMDC)**：MovieGraphs 的图结构提供比文本描述更可查询、更可解释的情境表示。
- **Social Interaction in Video (Marín-Jiménez et al.)**：先前工作仅分类 4 种视觉交互类型，MovieGraphs 增加了主题、原因等推断属性。
- 本数据集后续被用于 **Video Scene Graph Generation (VideoSGG)** 方法的基准评估。

## Open Questions

1. 如何提升自动 Person ID 的准确率以释放视觉检索的性能潜力？
2. 原因预测能否用结构化的理由分类取代自由生成，实现自动评估？
3. 电影情境数据集中的社会偏见如何量化和缓解？
4. 这些图结构能否迁移到真实世界视频（非电影）的情境理解？
5. 从 51 部电影中学到的"常识"（如图 5 的情境转移图）能否作为可复用的先验知识注入下游任务？

## Provenance

- 论文 PDF：raw/sources/2018-CVPR-MovieGraphs-Towards-Understanding-Human-Centric-Situations-from-Videos.pdf
- 提取文本：raw/sources/2018-CVPR-MovieGraphs-Towards-Understanding-Human-Centric-Situations-from-Videos.txt
- 全文精读，含正文 8 页 + 补充材料
- 所有结果数字来自原论文第 5 节 (Table 3, 4, 6, 7) 和补充材料
- Evidence level: **full-paper**（原始 PDF 全文提取 + 关键表格消融完整可读）
