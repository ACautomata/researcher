---
title: Graphical Contrastive Losses for Scene Graph Parsing
type: paper
domain: scene-graph
status: active
created: 2026-06-10
updated: 2026-06-10
tags: scene-graph-generation, contrastive-learning, CVPR-2019
source_pages: []
raw_sources:
  - raw/sources/2019-CVPR-graphical-contrastive-losses-for-scene-graph-parsing.pdf
  - raw/sources/2019-CVPR-graphical-contrastive-losses-for-scene-graph-parsing.txt
related_pages: []
paper:
  title: "Graphical Contrastive Losses for Scene Graph Parsing"
  authors:
    - Ji Zhang
    - Kevin J. Shih
    - Ahmed Elgammal
    - Andrew Tao
    - Bryan Catanzaro
  year: 2019
  venue: CVPR 2019
  arxiv: null
  doi: null
  code: null
  project: null
classification:
  label: scene-graph-generation, contrastive-learning
  task:
    - Scene Graph Generation
    - Visual Relationship Detection
  method_family: Contrastive Learning
  modality: Image
  datasets:
    - OpenImages
    - Visual Genome
    - VRD
  metrics:
    - Recall@50 (R@50)
    - Recall@100 (R@100)
    - wmAPrel
    - wmAPphr
    - scorewtd
evidence_level: full-paper
---

## Citation

Ji Zhang, Kevin J. Shih, Ahmed Elgammal, Andrew Tao, Bryan Catanzaro. "Graphical Contrastive Losses for Scene Graph Parsing." CVPR 2019.

## One-Sentence Contribution

将对比学习引入场景图解析，提出三种图结构感知的对比损失函数（Graphical Contrastive Losses）来显式解决场景图生成中两类常见错误：Entity Instance Confusion（实体实例混淆）和 Proximal Relationship Ambiguity（邻近关系歧义）。

## Problem Setting

场景图解析（Scene Graph Parsing）的目标是从图像中推断出包含定位实体类别和谓词边的视觉语义图，通常建模为检测图像中的 ⟨subject, predicate, object⟩ 三元组。主流方法是两阶段 pipeline：第一阶段检测实体，第二阶段对每个实体对用 softmax 分类预测谓词。

论文发现这种仅使用交叉熵损失的 pipeline 存在两类系统性错误：
- **Entity Instance Confusion**：模型将主体/客体与同类实体的错误实例关联（如从多个酒杯中错误判断哪一只正被握着）
- **Proximal Relationship Ambiguity**：当多个 subject-predicate-object 三元组在近距离内共享相同谓词时，模型错误配对（如多人的乐器交互中张冠李戴）

这两类错误的根本原因在于谓词预测的空间细节细微且难以通过标准 softmax 分类捕捉。

## Method

### Graphical Contrastive Losses

基于 margin-based triplet loss 的形式，在标准交叉熵损失 L₀ 之上增加三个对比损失项：

**1. Class Agnostic Loss (L₁)**：忽略类别信息，最大化最低分正样本对与最高分负样本对的 affnity margin。定义 affinity 项 Φ(s, o) = 1 - p(pred = ∅|s, o)（即 s 和 o 之间有关系的概率）。对每个主体和客体分别计算 margin。

**2. Entity Class Aware Loss (L₂)**：解决 Entity Instance Confusion。在 L₁ 的基础上将正/负样本集按实体类别 c 分组，最大化同类实例之间的 margin。迫使模型区分视觉上相似的同类实体中哪一个是真正存在关系的。

**3. Predicate Class Aware Loss (L₃)**：解决 Proximal Relationship Ambiguity。将 margin 按谓词类别 e 分组，迫使模型在共享相同谓词类别的实体对之间正确配对。

最终损失函数：L = L₀ + λ₁L₁ + λ₂L₂ + λ₃L₃，其中超参数 λ₁=1.0, λ₂=0.5, λ₃=0.1 通过交叉验证确定。

Margin 阈值 α₁=α₂=α₃=m，实验中 m=0.2 最佳（affinity 范围为 0~1）。

### RelDN 架构

为验证损失函数的有效性设计的 Relationship Detection Network：

1. **两阶段 pipeline**：先检测实体 proposals，再对候选关系区域做细粒度谓词分类
2. **独立谓词 CNN 分支**（conv_body_rel）：与实体检测器 CNN（conv_body_det）结构相同但权重独立训练，侧重交互区域特征
3. **三个特征模块**：
   - **语义模块（Semantic）**：基于 subject-object 类别共现频率的统计先验（p(pred|s, o)）
   - **空间模块（Spatial）**：编码主体/客体/谓词边界框的相对位置（delta 特征 + 归一化坐标）
   - **视觉模块（Visual）**：从实体检测 CNN 和谓词 CNN 分别提取 ROI 特征，拼接后通过 MLP 预测谓词类 logits；包含两个 skip-connection（subject-only 和 object-only 特征直连谓词 logits）
4. **模块融合**：三路 logits 逐元素相加后 softmax：p_pred = softmax(f_vis + f_spt + f_sem)

### 训练细节

- 实体检测器 CNN 独立训练后冻结，谓词 CNN 用实体检测器权重初始化后端到端微调
- 训练时：L₀ 采样 512 对（128 正例），对比损失采样 128 个正例主体并为其采样最近的正/负对比对
- 测试时：取实体检测器 top-100 输出，穷举所有实体对并计算 pdet(s)·ppred(pred)·pdet(o) 排序
- Backbone：OpenImages 使用 ResNeXt-101-FPN，VG 和 VRD 使用 VGG-16

## Experiments

### 数据集

| 数据集 | 训练集 | 验证集 | 备注 |
|--------|--------|--------|------|
| OpenImages | 53,953（全量）/ 4,500（mini） | 3,234（全量）/ 1,000（mini） | mini 子集用于超参搜索 |
| Visual Genome | 按 [35] 划分 | 按 [35] 划分 | 三种评估：SGDET / SGCLS / PRDCLS |
| VRD | 按标准划分 | 按标准划分 | R@50 和 R@100 |

### 评估指标

- **OpenImages**：Recall@50 (R@50), mAPrel（三元组级别的 mAP），mAPphr（短语级别 mAP），加权综合 score = 0.2×R@50 + 0.4×mAPrel + 0.4×mAPphr。由于谓词类别极度不平衡（64.48% 为 "at"，仅 0.03% 为 "under"），论文使用加权 mAP（wmAP）替代 mAP 进行消融。
- **VG**：按 Neural Motifs [35] 的标准，SGDET/SGCLS/PRDCLS 下的 R@20/50/100
- **VRD**：按 [33] 标准，R@50 和 R@100（k=1, 10, 70 和 free k）

### 训练设置

- OpenImages：全量训练 2 天；超参搜索在 mini 子集（4,500 train / 1,000 val）
- 采样策略：每 loss 独立采样正负样本，受各自约束
- Margin 阈值 m=0.2（通过消融实验确定最佳值，见表 4）

### 消融实验

1. **损失组合消融**（表 1）：L₀+L₁+L₂+L₃ 全量组合一致优于 L₀ alone。关键改进：plays（+5.0 APrel）、interacts with（+3.7）、holds（+1.3）。任何子集组合均不如全量组合。
2. **困难子集验证**（表 2）：精心筛选 100 张存在两类错误的图像，"holds" 的 APrel 提升最大（+4.1）
3. **模块消融**（表 3）：语义模块 alone 不可用；视觉模块加 skip-connection 后提升显著（plays +3.1, wears +2.0）；空间模块在空间关系（inside of +2.4）上贡献最大
4. **Margin 阈值消融**（表 4）：m=0.2 为最优（scorewtd 44.61），m=0.1 接近（44.51），m=0.5/1.0 明显下降

## Results

### OpenImages Challenge（表 7）

| 模型 | Public | Private | Overall |
|------|--------|---------|---------|
| 冠军 Seiji | 0.332 | 0.285 | 0.299 |
| RelDN*（同 Seiji 检测器） | 0.327 | 0.299 | 0.308 |
| **RelDN（本论文）** | **0.320** | **0.332** | **0.328** |

- RelDN 在 Private 集上超越冠军模型 4.7%（16.5% 相对提升）
- 即使使用与冠军相同的检测器，仍在 Private 集上领先 1.4%

### Visual Genome（表 5）

| 方法 | SGDET R@50 | SGDET R@100 | SGCLS R@50 | SGCLS R@100 | PRDCLS R@50 | PRDCLS R@100 |
|------|-----------|------------|-----------|------------|-----------|------------|
| MotifNet-LeftRight | 27.2 | 30.3 | 35.8 | 36.5 | 65.2 | 67.1 |
| **RelDN** | **28.3** | **32.7** | **36.8** | **36.8** | **68.4** | **68.4** |

- SGDET R@100 超越 MotifNet-LeftRight 2.4%，PRDCLS R@50 超越 12.7%
- 注意：RelDN 实体检测器 mAP@50 更高（25.5 vs. 20.0），但 baseline Frequency+Overlap 更低，说明关系改进主要来自模型设计

### VRD（表 6）

| 方法 | Relationship Detection R@50 (free) | Phrase Detection R@50 (free) |
|------|-----------------------------------|------------------------------|
| KL Distillation [33] | 22.68 | 22.68 |
| Zoom-Net [30] | 21.37 | 21.37 |
| RelDN (COCO pretrain) | **28.15** | **28.15** |

- COCO 预训练下显著优于所有 baselines
- ImageNet 预训练下竞争力相当（21.52 R@50 free）

## Limitations

1. 对比损失引入额外超参数（λ₁, λ₂, λ₃, m），需交叉验证确定
2. 在 open-world 场景下的适用性未探讨
3. 负样本采样策略可能受限于 batch size
4. 仅验证了两阶段 pipeline，未考虑端到端联合训练

## Reusable Claims

- **Contrastive loss 可以有效解决 SGG 中两类常见错误**：通过对比正负样本对的 affinity margin，模型被迫学习判别性细节特征，而非仅靠 softmax 分类
- **Entity Class Aware loss 和 Predicate Class Aware loss 是有互补效果的**：分别针对实体混淆和关系歧义两类不同错误源，联合使用效果最优
- **独立的谓词 CNN 分支有助于聚焦交互区域**：可视化表明谓词 CNN 的特征图更集中于能推断关系的细微区域
- **RelDN 三模块融合设计有效**：语义先验 + 空间几何 + 视觉特征三者互补；visual skip-connection（独立 S/O 特征直连）对以人或物体外观主导的关系有帮助

## Connections

- 与 Associative Embedding [Newell & Deng, NIPS 2017] 最相关，后者在 VG 场景图上使用 push-pull contrastive loss 训练实体 embedding；本文提出不同的 hard negative 集合来定位特定错误类型
- 将对比学习的思路引入 SGG，启发了后续结合对比学习的场景图生成工作
- RelDN 的语义模块受 Neural Motifs [Zellers et al., CVPR 2018] 的频率 baseline 启发
- 与视觉关系检测中 Visual Translation Embedding [Zhang et al., CVPR 2017]、ViP-CNN [Li et al., CVPR 2017]、Zoom-Net [Yin et al., ECCV 2018] 等方法在同一框架下对比

## Open Questions

1. 对比损失在 one-stage / 端到端 SGG 框架中的效果如何？
2. 是否可以通过动态 hard negative 挖掘进一步提高性能？
3. 当前三类损失的权重 λ 是固定值，自适应权重方案是否可能更好？
4. 在 zero-shot / open-vocabulary SGG 设置下，该对比损失是否仍然有效？

## Provenance

- PDF 来源：CVF Open Access (https://openaccess.thecvf.com/content_CVPR_2019/papers/Zhang_Graphical_Contrastive_Losses_for_Scene_Graph_Parsing_CVPR_2019_paper.pdf)
- 全文提取方式：pymupdf，9 页，41K+ 字符
- Evidence level：full-paper（完整 PDF，全文阅读，所有关键章节和数值均可查）
