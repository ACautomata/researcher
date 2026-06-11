# Autoresearch Wiki Log

> 追加式操作时间线。

## 2026-06-10

### Ingested: From Easy to Hard: Learning Curricular Shape-aware Features for Robust PSG (CAFE) — arXiv 2024

- **操作**：单篇入库（sub-agent）
- **论文**：[From Easy to Hard: Learning Curricular Shape-aware Features for Robust Panoptic Scene Graph Generation (CAFE)](domains/scene-graph/papers/cafe-curricular-shape-aware-panoptic-scene-graph-generation.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2024-07-12-curricular-shape-aware-panoptic-sgg.pdf (2.98 MB, arXiv:2407.09191)
- **提取**：raw/sources/2024-07-12-curricular-shape-aware-panoptic-sgg.txt (84,431 chars, 2885 lines)
- **用户备注**：课程学习的全景 SGG。
- **作者**：Hanrong Shi, Lin Li, Jun Xiao, Yueting Zhuang, Long Chen (ZJU & HKUST)
- **贡献**：
  - 首次在 PSG 中引入 shape-aware features（mask features + boundary features），弥补单纯依赖 bbox 空间特征的不足
  - 提出 Cognition-based Predicate Grouping，按谓词分布和语义相似度将 56 个谓词分三组
  - 三阶段课程学习策略（easy-to-hard），渐进集成 bbox → mask → boundary feature
  - Top-Down 知识蒸馏保留早期阶段知识
  - 模型无关，可嵌入任何两阶段 PSG 框架
  - PredCls Mean 40.6 (VCTree+CAFE) vs C-SGG SOTA 38.0
  - SGDet Mean 28.9 (VCTree+CAFE) vs DWIL SOTA 18.4

### Ingested: Visual Scene Graphs for Audio Source Separation (AVSGS) — ICCV 2021

- **操作**：单篇入库（sub-agent）
- **论文**：[Visual Scene Graphs for Audio Source Separation (AVSGS)](domains/audio-sgg/papers/2021-ICCV-AVSGS-visual-scene-graphs-audio-source-separation.md)

- **操作**：单篇入库（sub-agent）
- **论文**：[Visual Scene Graphs for Audio Source Separation (AVSGS)](domains/audio-sgg/papers/2021-ICCV-AVSGS-visual-scene-graphs-audio-source-separation.md)
- **领域**：audio-sgg（新建）
- **证据等级**：full-paper
- **来源**：raw/sources/2021-ICCV-Visual-Scene-Graphs-for-Audio-Source-Separation.pdf (6.1 MB)
- **提取**：raw/sources/2021-ICCV-Visual-Scene-Graphs-for-Audio-Source-Separation.txt (51,422 chars, 10 pages)
- **用户备注**：ICCV 2021（原记 CVPR 2015，经查为 ICCV 2021）。音频场景图的开创性工作。
- **作者**：Moitreya Chatterjee, Jonathan Le Roux, Narendra Ahuja, Anoop Cherian (UIUC & MERL)
- **贡献**：
  - 首次将场景图表示用于视觉引导音频源分离，提出 AVSGS
  - 自回归生成互正交子图嵌入条件化 U-Net 实现音源分离
  - 提出自然场景音源分离数据集 ASIW（基于 AudioCaps）
  - MUSIC SDR 11.4 vs SofM 8.2; ASIW SDR 8.8 vs Co-Sep 6.6

### Ingested: Sketching Image Gist: Human-Mimetic Hierarchical Scene Graph Generation — ECCV 2020

- **操作**：单篇入库（sub-agent）
- **论文**：[Sketching Image Gist: Human-Mimetic Hierarchical Scene Graph Generation (HetH)](domains/scene-graph/papers/2020-07-16-sketching-image-gist-hierarchical-sgg.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2020-07-16-sketching-image-gist-hierarchical-sgg.pdf (10.1 MB, arXiv:2007.08760)
- **提取**：raw/sources/2020-07-16-sketching-image-gist-hierarchical-sgg.txt (78,115 chars, 30 pages)
- **用户备注**：ECCV 2020。类人层次场景图生成。
- **作者**：Wenbin Wang, Ruiping Wang, Shiguang Shan, Xilin Chen (CAS)
- **贡献**：
  - 提出 Hierarchical Entity Tree (HET)，按物体大小和 IoU 构建层次树结构模拟人类场景解析
  - Hybrid-LSTM 编码 HET 中的层次上下文（Bi-TreeLSTM）和兄弟上下文（Bi-LSTM）
  - Relation Ranking Module (RRM) 从视觉显著性和物体大小学习关键关系排序
  - 构建 VG-KR 数据集，从 MSCOCO caption 提取关键关系标注
  - 在 VG-KR 关键关系预测上达到 PREDCLS kR@1 17.5%，VG200 超越 VCTree-SL
  - 下游 captioning 实验中，2 条 top 关系即优于 5 条频率基线

### Ingested: Importance Weighted Structure Learning for Scene Graph Generation (IWSL) — CVPR 2022

- **操作**：单篇入库（sub-agent）
- **论文**：[Importance Weighted Structure Learning for SGG](domains/scene-graph/papers/importance-weighted-structure-learning-for-sgg.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2022-05-17-importance-weighted-structure-learning-for-sgg.pdf (1.1 MB, arXiv:2205.07017)
- **提取**：raw/sources/2022-05-17-importance-weighted-structure-learning-for-sgg.txt (57,576 chars, 11 pages)
- **用户备注**：CVPR 2022。加权结构学习的 SGG。
- **作者**：Daqi Liu, Miroslaw Bober, Josef Kittler (University of Surrey)
- **贡献**：
  - 提出 Importance Weighted Structure Learning (IWSL)，用重要性加权下界 (IWLB) 替代传统 ELBO 作为变分推断目标
  - Gumbel-Softmax sampler 实现可微分 categorical 采样
  - Entropic Mirror Descent (EMD) 求解概率单纯形约束的变分推理
  - SGDet mR@50: IWSL 13.7 vs BGNN 10.7 (+28%)；IWSL+BA PredCls mR@50: 36.9 vs Transformer+BA 31.9 (+15.7%)
  - Open Images V6 mR@50: IWSL 42.18 vs BGNN 40.45
  - Body/Tail 组显著提升 (Body R@100 16.5, Tail R@100 10.7 vs BGNN 13.4/6.4)
- **Updated pages**：
  - `wiki/domains/scene-graph/papers/importance-weighted-structure-learning-for-sgg.md`（新建）
  - `wiki/index.md`（添加条目）
  - `wiki/log.md`（本条）

### Ingested: Learning to Generate Scene Graph from Natural Language Supervision — ICCV 2021

- **操作**：单篇入库（sub-agent）
- **论文**：[Learning to Generate Scene Graph from Natural Language Supervision](domains/scene-graph/papers/2021-09-06-learning-to-generate-scene-graph-from-natural-language-supervision.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2021-09-06-learning-to-generate-scene-graph-from-natural-language-supervision.pdf (1.4 MB, arXiv)
- **提取**：raw/sources/2021-09-06-learning-to-generate-scene-graph-from-natural-language-supervision.txt (71,487 chars, 16 pages)
- **用户备注**：ICCV 2021。利用自然语言监督生成场景图。
- **作者**：Yiwu Zhong, Jing Shi, Jianwei Yang, Chenliang Xu, Yin Li (UW-Madison, Rochester, Microsoft Research)
- **贡献**：
  - 首次从 image-sentence pairs 学习 localized scene graph（language supervised SGG）
  - Triplet Transformer：基于 Vision-Language Transformer 的 SPO triplet 预测模型
  - Pseudo labels：detector tags + caption parsing + WordNet matching
  - Language supervised SGG: 7.0 R@100 (vs VSPNet 5.4, +30% relative gain)
  - 首个 open-set SGG 结果: 4.8 R@100
  - 全监督下 mean recall SOTA: mSGDet 8.7 vs VCTree 6.9
- **Open loops**：object detector 覆盖范围限制；多实例歧义问题；language→full supervision gap (7.0→15.3 R@100)

### Ingested: Scene Graph Prediction with Limited Labels — ICCV 2019

- **操作**：单篇入库（sub-agent）
- **论文**：[Scene Graph Prediction with Limited Labels](domains/scene-graph/papers/2019-ICCV-scene-graph-prediction-with-limited-labels.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2019-ICCV-scene-graph-prediction-with-limited-labels.pdf (2.4 MB, OpenAccess)
- **提取**：raw/sources/2019-ICCV-scene-graph-prediction-with-limited-labels.txt (50,675 chars, 11 pages)
- **用户备注**：ICCV 2019。少标签场景图预测。
- **作者**：Vincent S. Chen, Paroma Varma, Ranjay Krishna, Michael Bernstein, Christopher Ré, Li Fei-Fei (Stanford)
- **贡献**：
  - 首次用半监督方法补全视觉知识库中缺失的关系标注
  - 提出 image-agnostic features（类别+空间）和因子图生成式模型，n=10 即可生成可用标签
  - PREDCLS R@100: 47.53，超出 TRANSFER LEARNING baseline 5.16 点
  - SGDET R@100: 19.28 vs ORACLE 30.15（ORACLE 用 108× 更多数据）
  - 引入关系复杂度指标（subtypes），R²=0.778 预测半监督 vs 迁移学习的收益

### Ingested: Unsupervised Vision-Language Parsing (VLGAE) — CVPR 2022

- **操作**：单篇入库（sub-agent）
- **论文**：[Unsupervised Vision-Language Parsing: Seamlessly Bridging Visual Scene Graphs with Language Structures via Dependency Relationships](domains/scene-graph/papers/2022-CVPR-unsupervised-vision-language-parsing.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2022-CVPR-Unsupervised-Vision-Language-Parsing.pdf (8.2 MB, arXiv)
- **提取**：raw/sources/2022-CVPR-Unsupervised-Vision-Language-Parsing.txt (51,724 chars, 11 pages)
- **用户备注**：CVPR 2022。无监督视觉-语言场景图解析方法。
- **作者**：Chao Lou, Wenjuan Han, Yuhuan Lin, Zilong Zheng (BIGAI, ShanghaiTech, Tsinghua)
- **贡献**：
  - 首次定义并解决无监督视觉-语言联合解析任务（VLParse）
  - 提出 VLGAE（对比学习图自编码器），无缝桥接场景图和语言依存树
  - 构建 VLParse 数据集（850 张图像 × 5 captions = 4,250 对，半自动标注+人工精炼）
  - 语言结构归纳：DDA 67.57% (+1.69% vs D-NDMV), UDA 71.43% (+0.66% vs D-NDMV)
  - 短语定位：Zero-AA 28.7% (+1.0% vs MAF)
- **Open loops**：总体性能仍偏低（Zero-AA 28.7%），高阶对齐极难（First-AA 3.4%, Second-AA 0.2%）

### Ingested: VARSCENE — A Deep Generative Model for Realistic Scene Graph Synthesis — ICML 2022

- **操作**：单篇入库（sub-agent）
- **论文**：[VARSCENE: A Deep Generative Model for Realistic Scene Graph Synthesis](domains/scene-graph/papers/2022-07-01-varscene-deep-generative-scene-graph-synthesis.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2022-07-01-varscene-scene-graph-synthesis.pdf (1.9 MB)
- **提取**：raw/sources/2022-07-01-varscene-scene-graph-synthesis.txt (78,764 chars)
- **用户备注**：ICML 2022。深度生成模型合成真实场景图。
- **作者**：Tathagat Verma, Abir De, Yateesh Agrawal, Vishwa Vinay, Soumen Chakrabarti (IIT Bombay & Adobe Research)
- **贡献**：
  - 提出 VAE+MMD 优化的场景图生成模型，以 star graph 分解解决大规模词汇表场景图生成
  - 在 VG（16,943 对象、8,411 关系）上 Star-Sim 0.86 vs SceneGen 0.73，SP-K 0.22 vs SceneGen 0.02
  - 图像质量 FID 6.02 (VARSCENE_cond) vs DeepGMG 9.83、SceneGen 19.26
  - MMD 后训练带来显著提升（Star-Sim 0.59→0.87 on VG）
- **Updated pages**：
  - `wiki/domains/scene-graph/papers/2022-07-01-varscene-deep-generative-scene-graph-synthesis.md`（新建）
  - `wiki/index.md`（添加条目，计数 72→73）
  - `wiki/log.md`（本条）

### Ingested: Visual Relationship Detection with Language Priors — ECCV 2016 (Oral)

- **操作**：单篇入库（sub-agent）
- **论文**：[Visual Relationship Detection with Language Priors](domains/scene-graph/papers/visual-relationship-detection-with-language-priors.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2016-07-31-visual-relationship-detection-with-language-priors.pdf (2.3 MB)
- **提取**：raw/sources/2016-07-31-visual-relationship-detection-with-language-priors.txt (51,086 chars)
- **用户备注**：ECCV 2016。SGG 早期工作，用语言先验改善视觉关系检测。
- **作者**：Cewu Lu, Ranjay Krishna, Michael Bernstein, Li Fei-Fei (Stanford)
- **贡献**：
  - 提出分离式建模对象和谓词外观 + word2vec 语言先验，从少量样本即可检测数千种关系
  - 构建 VRD 数据集（5,000 图像，37,993 关系，6,672 关系类型，24.25 谓词/对象类别）
  - Phrase Det R@100 17.03 vs Visual Phrases 0.07，Relationship Det R@100 14.70
  - 支持零样本关系检测（Predicate Det R@100 8.45 vs 随机 0.00014）
  - 图像检索 Median Rank 4 vs CNN 20
- **Updated pages**：
  - `wiki/domains/scene-graph/papers/visual-relationship-detection-with-language-priors.md`（新建）
  - `wiki/index.md`（添加条目，计数 71→72）
- **Open loops**：仅 100 对象 × 70 谓词验证；对象检测误差级联严重（Rel Det 14.70 vs Pred Det 47.87）；word2vec 依赖语言资源

### Ingested: Pair then Relation: Pair-Net for Panoptic Scene Graph Generation — ICCV 2023

- **操作**：单篇入库（sub-agent）
- **论文**：[Pair then Relation: Pair-Net for Panoptic Scene Graph Generation](domains/scene-graph/papers/pair-net-panoptic-scene-graph-generation.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2023-07-PairNet-Panoptic-Scene-Graph-Generation.pdf (7.1 MB)
- **提取**：raw/sources/2023-07-PairNet-Panoptic-Scene-Graph-Generation.txt (66,939 chars)
- **用户备注**：ICCV 2023。解耦成对处理的 PSG 方法。
- **作者**：Jinghao Wang, Zhengyu Wen, Xiangtai Li, Zujin Guo, Jingkang Yang, Ziwei Liu (NTU S-Lab)
- **贡献**：
  - 首次对 PSG 任务瓶颈进行系统分析：分割器质量已足够，pair recall 是关键制约因素
  - 提出 Pair Proposal Network (PPN) + Matrix Learner，显式建模 subject-object 配对关系
  - 使用 CNN 作为配对矩阵滤波器（0.2M 参数），性能优于 MLP/Transformer
  - mR@20 24.7% vs PSGFormer 14.5%（**+10.2 绝对提升**），R@20 29.6% vs 18.0%（**+11.6 绝对提升**）
  - Pair Recall@20 52.7 vs PSGFormer+ 28.6（+24.1），验证了配对质量的提升
  - 扩展至 VG-150 达到可比性能（mR@20 8.9, R@20 18.8）
- **Updated pages**：
  - `wiki/domains/scene-graph/papers/pair-net-panoptic-scene-graph-generation.md`（新建）
  - `wiki/index.md`（添加条目）
- **Open loops**：R@K 低于同期 HiLo；仅在 PSG 中等规模数据集验证；VG-150 泛化未显著超越 SGTR

### Ingested: Unbiased Scene Graph Generation via Two-stage Causal Modeling (TsCM) — TPAMI 2023

- **操作**：单篇入库（sub-agent）
- **论文**：[Unbiased Scene Graph Generation via Two-stage Causal Modeling (TsCM)](domains/scene-graph/papers/unbiased-scene-graph-generation-two-stage-causal-modeling-tscm.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2023-07-11-unbiased-scene-graph-generation-via-two-stage-causal-modeling.pdf (6.1 MB, 17 pages)
- **提取**：raw/sources/2023-07-11-unbiased-scene-graph-generation-via-two-stage-causal-modeling.txt (103.9K chars, 3692 lines)
- **作者**：Shuzhou Sun, Shuaifeng Zhi, Qing Liao, Janne Heikkilä, Li Liu
- **用户备注**：TPAMI 2023。两阶段因果建模的去偏 SGG 方法。注意：用户原标签为 CVPR-2023，实际为 TPAMI 2023 长文。
- **贡献**：
  - 首次将语义混淆偏置（semantic confusion）纳入 SGG 去偏框架
  - 提出 TsCM：阶段 1 用 Population Loss (P-Loss) 消除语义混淆，阶段 2 用 Adaptive Logit Adjustment (AL-Adjustment) 消除长尾分布
  - MotifsNet PredCls mR@100: 40.9 (SOTA, vs baseline 16.8)
  - MR@K 46.1 实现最佳头部-尾部平衡

### Added: STTran — Spatial-Temporal Transformer for Dynamic Scene Graph Generation (ICCV 2021)

- **操作**：单篇入库（sub-agent）
- **论文**：[STTran: Spatial-Temporal Transformer for Dynamic Scene Graph Generation](domains/scene-graph/papers/2021-10-01-sttran-spatial-temporal-transformer-dynamic-scene-graph.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2021-10-01-sttran.pdf (2.1 MB)
- **提取**：raw/sources/2021-10-01-sttran.txt (52.7K chars, 11 pages)
- **用户备注**：ICCV 2021。STTran，视频动态场景图的经典工作，空间-时间 Transformer。
- **作者**：Yuren Cong, Wentong Liao, Hanno Ackermann, Bodo Rosenhahn, Michael Ying Yang (Leibniz University Hannover / University of Twente)
- **贡献**：
  - 提出 Spatial-Temporal Transformer (STTran)，Spatial Encoder 提取帧内空间上下文，Temporal Decoder 捕获帧间时间依赖
  - 引入 Multi-label margin loss 和 Semi Constraint 图生成策略
  - 在 Action Genome 数据集上以 With Constraint 协议实现 PredCLS-R@20=71.8，SGCLS-R@20=47.5，SGDET-R@20=34.1，全面超越当时 SOTA

### Added: OpenPSG — Open-set Panoptic Scene Graph Generation via Large Multimodal Models (ECCV 2024)

- **操作**：单篇入库（sub-agent）
- **论文**：[OpenPSG: Open-set Panoptic Scene Graph Generation via Large Multimodal Models](domains/scene-graph/papers/openpsg-open-set-panoptic-scene-graph-generation-via-large-multimodal-models.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2024-07-15-openpsg-open-set-panoptic-scene-graph-generation-via-large-multimodal-models.pdf (1.6 MB)
- **提取**：raw/sources/2024-07-15-openpsg-open-set-panoptic-scene-graph-generation-via-large-multimodal-models.txt (60.9K chars, 1781 lines)
- **用户备注**：ECCV 2024。开放集全景场景图生成，利用多模态大模型。
- **作者**：Zijian Zhou, Zheng Zhu, Holger Caesar, Miaojing Shi (King's College London / GigaAI / TU Delft / Tongji University)
- **贡献**：
  - 首次定义 open-set PSG 任务，允许开放集的对象和关系预测
  - 提出 OpenPSG：三组件框架（OpenSeeD分割器 + RelQ-Former + BLIP-2 Multimodal Relation Decoder）
  - RelQ-Former 设计两组可学习查询：pair feature extraction + relation existence estimation，后者通过 selector 过滤无关对象对实现 20× 加速
  - 设计 Judgement Instruction（OpenPSG-J）优于 Generation Instruction（OpenPSG-G），在 novel 比例增大时更鲁棒
  - 封闭集 PSG PredCls: R@100=79.3%, mR@100=63.8%（+26.6%/+25.0% over best prior）
  - 开放集 PSG PredCls: R@100=61.5%, mR@100=46.0%（超先前方法封闭集结果）

### Added: Anticipatory Pre-training for Dynamic Scene Graph Generation (CVPR 2022)

- **操作**：单篇入库（sub-agent）
- **论文**：[Dynamic Scene Graph Generation via Anticipatory Pre-training](domains/scene-graph/papers/2022-CVPR-dynamic-scene-graph-anticipatory-pre-training.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2022-06-01-dynamic-scene-graph-generation-via-anticipatory-pre-training.pdf (1.24 MB)
- **提取**：raw/sources/2022-06-01-dynamic-scene-graph-generation-via-anticipatory-pre-training.txt (49.4K chars, 1400 lines)
- **用户备注**：CVPR 2022。视频动态场景图的代表方法，面向未来的预训练策略。
- **作者**：Yiming Li (ZZU), Xiaoshan Yang, Changsheng Xu (CASIA/UCAS/PCL)
- **贡献**：
  - 提出面向预训练（Anticipatory Pre-training）范式，用历史帧预测当前帧的视觉关系，显式建模时序相关性
  - 设计 Anticipatory Transformer：空间编码器 + 渐进式时序编码器（短时+长时双编码器）
  - 利用未标注帧进行预训练，缓解 Action Genome 标注稀疏问题
  - Action Genome (With Constraint): Pred Cls R@10/R@20 = 78.5/73.8, SG Gen R@20 = 38.3（超越 STTran +4.2）

### Added: SGTR — End-to-end Scene Graph Generation with Transformer (CVPR 2022)

- **操作**：单篇入库（sub-agent）
- **论文**：[SGTR: End-to-end Scene Graph Generation with Transformer](domains/scene-graph/papers/sgtr-end-to-end-scene-graph-generation-with-transformer.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2022-CVPR-SGTR-End-to-end-Scene-Graph-Generation-with-Transformer.pdf (4.5 MB)
- **提取**：raw/sources/2022-CVPR-SGTR-End-to-end-Scene-Graph-Generation-with-Transformer.txt (72.7K chars, 2155 lines)
- **用户备注**：CVPR 2022。第一个将 Transformer 用于端到端 SGG 的方法，将 SGG 建模为二分图匹配问题。高引论文。
- **作者**：Rongjie Li, Songyang Zhang, Xuming He (上海科技大学 / 中科院上海微系统所)
- **贡献**：
  - 首次将 SGG 建模为二分图构造问题，使用 Transformer 端到端生成实体与谓词 proposal 集合
  - 提出 Entity-Aware 谓词表示（Structural Predicate Decoder），将谓词 query 分解为 subject indicator + object indicator + predicate representation
  - 设计 Graph Assembling 模块，结合空间和语义相似度推断二分图连通性
  - OpenImages V6: mR@50 = 42.61, wmAPrel = 36.98（超越 BGNN +5.83）
  - Visual Genome: mR@100 = 15.2, 使用 resampling 后 mR@100 = 20.1, tail mR = 17.1

### Added: ConceptGraphs: Open-Vocabulary 3D Scene Graphs for Perception and Planning

- **操作**：单篇入库（sub-agent）
- **论文**：[ConceptGraphs: Open-Vocabulary 3D Scene Graphs for Perception and Planning](domains/scene-graph/papers/conceptgraphs-open-vocabulary-3d-scene-graphs.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2023-09-28-ConceptGraphs-Open-Vocabulary-3D-Scene-Graphs.pdf (2.5 MB)
- **提取**：raw/sources/2023-09-28-ConceptGraphs-Open-Vocabulary-3D-Scene-Graphs.txt (63 KB, 1,456 lines)
- **作者**：Qiao Gu, Ali Kuwajerwala, Sacha Morin, Krishna Murthy Jatavallabhula et al. (Toronto, Montreal, MIT, JHU, UMass)
- **贡献**：
  - 提出开放词汇 3D 场景图 ConceptGraphs，利用 SAM + CLIP + LLaVA + GPT-4 零样本构建
  - 对象级 3D 建图：SAM 做类别无关分割 + CLIP 语义特征 + 多视图关联融合
  - 节点标注：LLaVA 多视图描述 + GPT-4 汇总为最终标签
  - 场景图生成：MST 剪枝 + LLM 推断对象间开放词汇空间关系
  - LLM 规划接口：场景图转 JSON 文本，支持复杂语言查询的导航、操作等任务
- **关键结果**：
  - 场景图节点精度 CG avg 0.71，边精度 CG avg 0.88
  - 语义分割 mAcc 40.63 (vs ConceptFusion 24.16)
  - 对象检索 LLM 方法 Negation R@1 在 Lab 场景达 1.00

### Added: SceneGraphFusion: Incremental 3D Scene Graph Prediction from RGB-D Sequences (CVPR 2021)

- **操作**：单篇入库（sub-agent）
- **论文**：[SceneGraphFusion: Incremental 3D Scene Graph Prediction from RGB-D Sequences](domains/scene-graph/papers/scenegraphfusion-incremental-3d-scene-graph-prediction.md)
- **Raw source**：`raw/sources/2021-06-01-scenegraphfusion-incremental-3d-scene-graph-prediction.pdf`
- **Evidence level**：full-paper
- **Key takeaways**：
  - 首个从 RGB-D 序列增量构建 3D 场景图的方法
  - 提出 Feature-wise Attention (FAT)，在 Relationship R@1 达 0.55（vs. 3DSSG 0.38）
  - 支持 35Hz CPU 实时运行
  - 全景分割副产物在 ScanNet 上 PQ 达 36.3（超过 PanopticFusion 的 33.5）
- **Updated pages**：
  - `wiki/domains/scene-graph/papers/scenegraphfusion-incremental-3d-scene-graph-prediction.md`（新建）
  - `wiki/index.md`（添加条目）
- **Open loops**：none

### Added: Graphical Contrastive Losses for Scene Graph Parsing (CVPR 2019)

- **操作**：单篇入库（sub-agent）
- **论文**：[Graphical Contrastive Losses for Scene Graph Parsing](domains/scene-graph/papers/graphical-contrastive-losses-for-scene-graph-parsing.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2019-CVPR-graphical-contrastive-losses-for-scene-graph-parsing.pdf (1.8 MB, 9 pages)
- **提取**：raw/sources/2019-CVPR-graphical-contrastive-losses-for-scene-graph-parsing.txt (41,419 chars)
- **作者**：Ji Zhang, Kevin J. Shih, Ahmed Elgammal, Andrew Tao, Bryan Catanzaro (Rutgers / NVIDIA)
- **贡献**：
  - 首次将对比学习（Contrastive Learning）引入场景图解析
  - 提出三种 Graphical Contrastive Losses（Class Agnostic / Entity Class Aware / Predicate Class Aware）解决 Entity Instance Confusion 和 Proximal Relationship Ambiguity
  - 设计 RelDN 架构验证损失有效性（三模块融合：语义 + 视觉 + 空间）
  - OpenImages Challenge Private 集超越冠军 4.7%（score 0.332 vs 0.285）
  - VG PRDCLS R@50=68.4，SGCLS R@50=36.8，超越 MotifNet
- **Open loops**：对比损失在 one-stage / end-to-end SGG 框架中的应用；open-vocabulary 设置下的有效性

### Added: Neural Motifs: Scene Graph Parsing with Global Context (CVPR 2018)

- **操作**：单篇入库（sub-agent）
- **论文**：[Neural Motifs: Scene Graph Parsing with Global Context](domains/scene-graph/papers/neural-motifs-scene-graph-global-context.md)
- **领域**：scene-graph
- **证据等级**：full-paper

### Added: The Devil Is in the Labels: Noisy Label Correction for Robust SGG (NICE) (CVPR 2022)

- **操作**：单篇入库（sub-agent）
- **论文**：[The Devil Is in the Labels: Noisy Label Correction for Robust SGG (NICE)](domains/scene-graph/papers/nice-noisy-label-correction-scene-graph-generation.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2022-CVPR-Devil-Is-in-the-Labels-Noisy-Label-Correction-SGG.pdf (1.8 MB, 10 pages)
- **提取**：raw/sources/2022-CVPR-Devil-Is-in-the-Labels-Noisy-Label-Correction-SGG.txt (47,873 chars)
- **作者**：Lin Li, Long Chen, Yifeng Huang, Zhimeng Zhang, Songyang Zhang, Jun Xiao (ZJU / Columbia / Rochester)
- **贡献**：
  - 首次将 SGG 重新定义为 noisy label learning 问题
  - 指出 VG 数据集存在三类标签噪声：Common-prone、Synonym-random、Negative（缺失标注）
  - 提出 NICE 策略（Neg-NSD + Pos-NSD + NSC），模型无关的预处理管道
  - Motifs+NICE PredCls mR@100 提升 14.5（17.8→32.3），VCTree+NICE mR@100 提升 14.6（18.4→33.0）
- **Open loops**：聚类超参数（dc 距离阈值）的手工设置；在其他 SGG 数据集（PSG 等）上的泛化性
- **来源**：raw/sources/2018-CVPR-Neural-Motifs-Scene-Graph-Global-Context.pdf (1.3 MB)
- **提取**：raw/sources/2018-CVPR-Neural-Motifs-Scene-Graph-Global-Context.txt (46,281 chars, 1,353 lines)
- **作者**：Rowan Zellers, Mark Yatskar, Sam Thomson, Yejin Choi (UW / Allen AI / CMU)
- **贡献**：
  - 系统分析 Visual Genome 中的 Motif 模式：物体标签高度预测关系标签，>50% 场景图包含至少两条关系的 motif
  - 提出 FREQ+OVERLAP baseline：仅用训练集统计频率预测关系，超越 prior SOTA 3.6% relative
  - 提出 MOTIFNET（Stacked Motif Networks）：biLSTM 编码全局上下文 + 阶段性预测，超越 baseline 7.1% relative
  - 定义 SGG 三大评估设定（PredCls/SGCls/SGDet）成为领域标准
- **关键结果**：MOTIFNET PredCls R@50=65.2, SGCls R@50=35.8, SGDet R@50=27.2

### Added: VCTREE: Learning to Compose Dynamic Tree Structures for Visual Contexts (CVPR 2019)

- **操作**：单篇入库（sub-agent）
- **论文**：[VCTREE: Learning to Compose Dynamic Tree Structures for Visual Contexts](domains/scene-graph/papers/vctree-learning-to-compose-dynamic-tree-structures.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2019-06-15-VCTree-Learning-to-Compose-Dynamic-Tree-Structures-for-Visual-Contexts.pdf (2.1 MB, 10 pages)
- **提取**：raw/sources/2019-06-15-VCTree-Learning-to-Compose-Dynamic-Tree-Structures-for-Visual-Contexts.txt (46,156 chars)
- **用户备注**：VCTree 原始论文，CVPR 2019。提出动态树结构编码视觉上下文。经典 SGG 方法，广泛用作 baseline。
- **作者**：Kaihua Tang, Hanwang Zhang, Baoyuan Wu, Wenhan Luo, Wei Liu (NTU / Tencent AI Lab)
- **贡献**：
  - 提出 VCTREE 动态二叉树结构，编码物体间的层级和平行关系
  - 得分矩阵 + 最大生成树（MST）构造每张图像独有的二叉树
  - 双向 TreeLSTM 编码视觉上下文
  - 混合学习：监督学习 + REINFORCE（自评判基线）优化树结构
- **关键结果**：SGGen R@20=22.0, R@50=27.9, R@100=31.3; PredCls R@20=60.1, R@50=66.4, R@100=68.1; VQA2.0 test-dev 68.19%, test-standard 68.49%

### Added: Scene Graph Generation from Objects, Phrases and Region Captions (MSDN) — ICCV 2017

- **操作**：单篇入库（sub-agent）
- **论文**：[Scene Graph Generation from Objects, Phrases and Region Captions (MSDN)](domains/scene-graph/papers/msdn-scene-graph-generation-from-objects-phrases-region-captions.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2017-ICCV-scene-graph-generation-from-objects-phrases-region-captions.pdf (1.5 MB)
- **提取**：raw/sources/2017-ICCV-scene-graph-generation-from-objects-phrases-region-captions.txt (45,398 chars, 10 pages)
- **用户备注**：SGG 最早论文之一，提出基于对象检测+关系分类的经典 pipeline。首次在 Visual Genome 上定义 SGG 任务。
- **作者**：Yikang Li, Wanli Ouyang, Bolei Zhou, Kun Wang, Xiaogang Wang (CUHK / Univ. Sydney / MIT)
- **贡献**：
  - 提出 Multi-level Scene Description Network (MSDN)，联合学习对象检测、SGG 和区域描述三个语义层次任务
  - 提出动态图构建机制，根据图像内容建立对象-短语-区域描述之间的连接
  - 提出门控消息传递 + 残差式特征精炼的 Merge-and-Refine 范式
  - 定义 SGG 三个子任务（PredCls/PhrCls/SGGen）和 Recall@K 评估协议，成为领域标准
- **关键结果**：
  - SGGen R@50=10.72, R@100=14.22（超 ISGG 3.63%~4.31%）
  - PredCls R@50=67.03, R@100=71.01（超 ISGG 8.86%/8.27%）
  - 消息传递带来 SGGen +5.34% 最大提升；2 次迭代最优
  - 联合学习也提升物体检测 mAP 7.43%（vs FRCNN 6.72%）和区域描述 AP 5.39%（vs baseline 4.41%）

### Added: Learning 3D Semantic Scene Graphs from 3D Indoor Reconstructions (CVPR 2020)

- **操作**：单篇入库（sub-agent）
- **论文**：[Learning 3D Semantic Scene Graphs from 3D Indoor Reconstructions (3DSSG)](domains/scene-graph/papers/learning-3d-semantic-scene-graphs-from-3d-indoor-reconstructions.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2020-CVPR-Learning-3D-Semantic-Scene-Graphs-from-3D-Indoor-Reconstructions.pdf (9.5 MB)
- **提取**：raw/sources/2020-CVPR-Learning-3D-Semantic-Scene-Graphs-from-3D-Indoor-Reconstructions.txt (57,695 chars, 1,704 lines)
- **用户备注**：CVPR 2020 Spotlights。在 3D 室内重建上学习语义场景图的经典工作。提出了 3DSSG 数据集。
- **作者**：Johanna Wald*, Helisa Dhamo*, Nassir Navab, Federico Tombari (TUM / Google)
- **贡献**：
  - 提出 3DSSG 数据集：首个大规模真实 3D 室内场景的语义场景图数据集（1,482 scans, 48k instances, 534 classes, 40 relations, 93 attributes）
  - 提出 SGPN（Scene Graph Prediction Network）：首个从 3D 点云学习语义场景图的端到端方法（PointNet + GCN）
  - 多谓词预测策略（per-class BCE），处理 3D 场景中的关系歧义
  - 展示场景图作为跨域（2D-3D）检索中间表示的可行性
- **关键结果**：Multi Predicate Ours: Relationship R@50=0.40, R@100=0.66; Object R@5=0.68, R@10=0.78; Predicate R@3=0.89, R@5=0.93. 3D-3D 检索 Top-1=0.34, 2D-3D 检索 Top-1=0.17 (predicted graphs)

### Added: EGTR: Extracting Graph from Transformer for Scene Graph Generation (CVPR 2024)

- **操作**：单篇入库（sub-agent）
- **论文**：[EGTR: Extracting Graph from Transformer for Scene Graph Generation](domains/scene-graph/papers/2024-06-24-EGTR-extracting-graph-from-transformer-scene-graph-generation.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2024-04-02-EGTR-Extracting-Graph-from-Transformer-for-Scene-Graph-Generation.pdf
- **提取**：raw/sources/2024-04-02-EGTR-Extracting-Graph-from-Transformer-for-Scene-Graph-Generation.txt (70,721 chars)
- **用户备注**：CVPR 2024。从 DETR 类检测器中直接提取关系图。
- **标签**：scene-graph-generation, transformer, one-stage, CVPR-2024
- **作者**：Jinbae Im, JeongYeon Nam, Nokyung Park, Hyungmin Lee, Seunghyun Park (NAVER Cloud AI / Korea University)
- **贡献**：
  - 利用 DETR decoder 多层 self-attention 的 Q/K by-products 直接提取关系图，无需额外 triplet 检测器
  - 提出 Adaptive Smoothing（课程学习），根据目标检测质量动态调整关系标签
  - 提出 Connectivity Prediction 辅助任务，用于训练 hint 和推理时过滤
  - 显著优于 prior arts：VG SGDet AP50=**30.8**（vs SSR-CNN 23.8），参数量仅 **42.5M**（SSR-CNN 的 1/6），速度 **14.7 FPS**（SSR-CNN 的 3.7×）
  - Open Image V6 上取得 competitive 性能：Score=48.6（micro-R@50=75.0, wmAPrel=42.0, wmAPphr=41.9）
- **Updated pages**：
  - `wiki/domains/scene-graph/papers/2024-06-24-EGTR-extracting-graph-from-transformer-scene-graph-generation.md`（新建）
  - `wiki/index.md`（添加条目）

## 2026-06-09

### Added: ToLL: Topological Layout Learning for 3D Scene Graph Generation Pretraining (arXiv 2026)

- **操作**：单篇入库（sub-agent, inbound 批量入库）
- **论文**：[ToLL: Topological Layout Learning for 3D Scene Graph Generation Pretraining](domains/scene-graph/papers/toll-topological-layout-learning-3dsg-pretraining.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2026-arXiv-ToLL-Topological-Layout-Learning-SGG.pdf (6.7 MB, 10 pages)
- **提取**：raw/sources/2026-arXiv-ToLL-Topological-Layout-Learning-SGG.txt (52,937 chars, 1,803 lines)
- **用户备注**：inbound 批量入库，拓扑布局学习非对称关系SGG（arXiv 2026）
- **作者**：Yucheng Huang, Luping Ji, Xiangwei Jiang, Wen Li, Mao Ye (UESTC)
- **贡献**：
  - 提出 ACTGR（Anchor-Conditioned Topological Geometry Reasoning），仅保留单锚点空间属性创造信息瓶颈，迫使 GNN 通过边拓扑进行空间推断，避免几何捷径
  - 提出 SMA（Structural Multi-view Augmentation），通过连接性扰动生成非对称视图，结合 SwAV 自蒸馏学习对拓扑遮挡鲁棒的三元组表示
  - 提出 ToLL++ 解耦布局恢复，将形状/尺度/位置解耦独立预测
  - 全面超越 MvIL、OCRL 等 SOTA 预训练框架：Object A@1 61.43，Predicate mA@3 82.06，SGCLs mR@50 40.2

### Added: RGB-only Active 3D Scene Graph Generation for Indoor Environments (arXiv 2026)

- **操作**：单篇入库（sub-agent, inbound 批量入库）
- **论文**：[RGB-only Active 3D Scene Graph Generation for Indoor Environments](domains/scene-graph/papers/rgb-only-active-3d-scene-graph-generation.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2026-06-09-rgb-only-active-3d-scene-graph-generation.pdf (1.2 MB)
- **提取**：raw/sources/2026-06-09-rgb-only-active-3d-scene-graph-generation.txt (26,420 chars)
- **用户备注**：inbound 批量入库，仅RGB主动3D场景图生成（arXiv 2026）
- **作者**：Giorgia Modi, Davide Buoso, Giuseppe Averta, Daniele De Martini (Univ. Oxford / Politecnico di Torino)
- **贡献**：
  - 首次提出纯RGB输入的主动式3D场景图增量构建框架
  - 使用MapAnything前馈深度估计替代RGB-D/LiDAR，消除深度传感器依赖
  - 将ConceptGraphs扩展到RGB-only + 主动探索场景，结合ASP语义驱动力探索
  - 支持异构RGB输入（机载相机+外部固定相机）统一处理
  - Replica上F1-score 0.500 vs CG(GT深度) 0.499（持平）；ASP主动探索30步检测~110节点 vs SEE~45节点

### Added: Visual Commonsense Driven Knowledge Refinements for Scene Graph Generation (arXiv 2026)

- **操作**：单篇入库（sub-agent, inbound 批量入库）
- **论文**：[Visual Commonsense Driven Knowledge Refinements for Scene Graph Generation](domains/scene-graph/papers/visual-commonsense-knowledge-refinements-sgg.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2026-06-09-visual-commonsense-knowledge-refinements-sgg.pdf (29.2 MB, 35 pages)
- **提取**：raw/sources/2026-06-09-visual-commonsense-knowledge-refinements-sgg.txt (85,698 chars)
- **用户备注**：inbound 批量入库，视觉常识驱动知识精炼SGG（arXiv 2026）
- **作者**：Maëlic Neau, Salim Baloch, Jakob Suchan, Zoe Falomir, Mehul Bhatt (Umeå Uni. / Constructor Uni. / Örebro Uni. / CoDesign Lab EU)
- **贡献**：
  - 模型无关的常识驱动 SGG 后处理精炼框架，无需重训练
  - 从训练数据自动挖掘三类视觉常识规则（空间/功能/关系），使用 ASP 溯因推理修正 SGG 预测
  - 超类抽象机制缓解细粒度标注稀疏性，支持向开放词汇扩展
  - 新指标 Constraint Violation Rate (CVR) 量化常识一致性
- **关键结果**：
  - PSG F1@K **30.74**（+1.15 vs REACT++ 基线），VG150 F1@K **18.49**（+0.87）
  - zsR@100 在 PSG 上 **5.21**（基线 4.31，+21%），CVR 从 12.44% 降至 0.93%
  - 三种架构（Motifs / Transformer / REACT++）均获一致提升

### Added: PALS — Revisiting Weakly-Supervised Video Scene Graph Generation via Pair Affinity Learning (arXiv 2026)

- **操作**：单篇入库（sub-agent, inbound 批量入库）
- **论文**：[PALS: Revisiting Weakly-Supervised Video Scene Graph Generation via Pair Affinity Learning](domains/scene-graph/papers/2026-03-23-PALS-revisiting-weakly-supervised-video-scene-graph-generation.md)

### Added: Towards Spatio-Temporal World Scene Graph Generation from Monocular Videos (arXiv 2026)

- **操作**：单篇入库（sub-agent, inbound 批量入库）
- **论文**：[Towards Spatio-Temporal World Scene Graph Generation from Monocular Videos](domains/scene-graph/papers/towards-spatio-temporal-world-scene-graph-generation.md)
- **证据等级**：full-paper
- **摘要**：提出 ActionGenome4D 数据集和 World Scene Graph Generation (WSGG) 任务，将视频 SGG 从帧中心扩展至全局 3D 世界坐标系，支持对不可见物体的关系推理。提出 PWG、MWAE、4DST 三种方法及 VLM 基线。
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2026-arXiv-Revisiting-Weakly-Supervised-Video-SGG.pdf (1.6 MB)
- **提取**：raw/sources/2026-arXiv-Revisiting-Weakly-Supervised-Video-SGG.txt (75,861 chars)
- **用户备注**：inbound 批量入库，弱监督视频SGG再探（arXiv 2026）
- **作者**：Minseok Kang, Minhyeok Lee, Minjung Kim, Jungho Lee, Donghyeong Kim, Sungmin Woo, Inseok Jeon, Sangyoun Lee (Yonsei Univ. / LG Electronics)
- **arXiv**：[2603.21559](https://arxiv.org/abs/2603.21559)
- **方法**：PALS (Pair Affinity Learning and Scoring) — 可学习的 pair affinity 估计交互概率并用于推理重排序；PAM (Pair Affinity Modulation) — 在注意力中门控抑制非交互对；RAM (Relation-Aware Matching) — 利用 VL grounding 解析伪标签类级歧义
- **关键结果**：
  - PLA + Ours on STTran, WC R@10=**22.24**, NC R@10=**23.20**（vs 基线 15.39 / 15.83）
  - 达到全监督上限 R@10 的 **88.3%** (WC) 和 **94.3%** (NC)
  - RAM + GDINO 提升匹配精度 +**80.6%**，F1 +22.4%
  - 计算开销仅 +1.27% 参数，几乎零 FLOPs/latency

### Added: QPredSGG — Hybrid Quantum Predicate Learning for Long-Tailed Scene Graph Generation (arXiv 2026)

- **操作**：单篇入库（sub-agent, inbound 批量入库）
- **论文**：[QPredSGG: Hybrid Quantum Predicate Learning for Long-Tailed Scene Graph Generation](domains/scene-graph/papers/qpredsgg-hybrid-quantum-predicate-learning-sgg.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2026-06-09-qpredsgg-hybrid-quantum-predicate-learning-sgg.pdf (1.6 MB, 11 pages)
- **提取**：raw/sources/2026-06-09-qpredsgg-hybrid-quantum-predicate-learning-sgg.txt (59,507 chars)
- **用户备注**：inbound 批量入库，混合量子谓词学习低资源SGG（arXiv 2026）
- **作者**：Prerana Ramkumar, Nouhaila Innan, Muhammad Shafique
- **方法**：QP-Head — 用参数化量子电路（PQC）替换 CFEN 中的经典 MLP 谓词头，在 4-qubit 设置下将 4096 维 pair embedding 压缩为 16 维量子态，使用 Amplitude Embedding + Strongly Entangling Layers + Weighted Cross-Entropy 训练
- **关键结果**：
  - 4-qubit QP-Head (Amp+SEL)：mR@100 **57.25%**（vs CFEN 基线 41.1%），R@50 **84.58%**，仅 **96** 个量子参数
  - 8-qubit QP-Head (4L)：mR@100 **55.38%**，R@50 **83.73%**，R@100 **92.41%**，384 个量子参数
  - 物理 QPU (ibm_fez) 验证：9 个三元组 batch 准确率 **66.67%**，输出分布未坍缩至单类
  - 特征压缩比 4096→16 (256×)；量子参数占比 <0.001%

### Added: MA3DSG — Multi-Agent 3D Scene Graph Generation for Large-Scale Indoor Environments (arXiv 2026)

- **操作**：单篇入库（sub-agent, inbound 批量入库）
- **论文**：[MA3DSG: Multi-Agent 3D Scene Graph Generation for Large-Scale Indoor Environments](domains/scene-graph/papers/ma3dsg-multi-agent-3d-scene-graph-generation.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2026-02-04-MA3DSG-Multi-Agent-3D-Scene-Graph-Generation.pdf (2.6 MB, 8 pages)
- **提取**：raw/sources/2026-02-04-MA3DSG-Multi-Agent-3D-Scene-Graph-Generation.txt (44,543 chars, 1,519 lines)
- **用户备注**：inbound 批量入库，多智能体3D场景图生成（arXiv 2026）
- **作者**：Yirum Kim, Jaewoo Kim, Ue-Hwan Kim (GIST, Korea)
- **方法**：首个多智能体 3DSGG 框架，提出无参数图对齐算法（training-free），基于标签匹配 + 空间约束（θdis=1.5m, θbbox=0.4）融合多个 agent 的局部场景图为统一全局图。基于 SGFN 做增量场景图生成，使用 PointNet + FAN GNN 提取节点/边特征
- **关键结果**：
  - SCP（47 rooms）：Triplet F1@1 **13.7**，Object F1@1 **35.1**，总时间 **14.8 min**（vs SGFN 61.8 min，4× 更快），数据流量 **3.7 MB**（vs multi-agent 基线 364.1 MB，98.4× 更少）
  - LDCP（47 rooms）：Object F1@1 **33.0**，总时间 **41.0 min**（vs SGFN 166.7 min），对齐时间仅 **0.37 sec**（vs SGFN+SGAligner 350.6 sec）
  - 全部推理仅使用 CPU

### Added: Salience-SGG — Enhancing Unbiased Scene Graph Generation via Salience Estimation (arXiv 2026)

- **操作**：单篇入库（sub-agent, inbound 批量入库）
- **论文**：[Salience-SGG: Enhancing Unbiased Scene Graph Generation with Iterative Salience Estimation](domains/scene-graph/papers/salience-sgg-unbiased-scene-graph-generation-via-salience-estimation.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2026-arXiv-Salience-SGG-Enhancing-Unbiased-SGG-via-Salience-Estimation.pdf (5.1 MB)
- **提取**：raw/sources/2026-arXiv-Salience-SGG-Enhancing-Unbiased-SGG-via-Salience-Estimation.txt (53,161 chars, 1,812 lines)
- **用户备注**：inbound 批量入库，显著性估计增强无偏SGG（arXiv 2026）
- **作者**：Runfeng Qu, Ole Hall, Pia K. Bideau, Julie Ouerfelli-Ethier, Martin Rolfs, Klaus Obermayer, Olaf Hellwich（TU Berlin + HU Berlin + Grenoble Alpes）
- **方法**：Iterative Salience Decoder (ISD) 通过语义无关的 bottom-up salience labels（仅基于空间重叠 IoU）引导 G-ESA 和 P-ECA 增强注意力层迭代估计 triplet salience，缓解去偏策略导致的空间理解退化
- **关键结果**：
  - VG F@100 **26.2**（SOTA，+1.5 vs Hydra-SGG 24.7），mR@100 **21.6**，参数量仅 77.7M
  - OIv6 score **51.8**（SOTA，+1.7 vs Hydra-SGG 50.1），wmAPrel **45.6**（+2.8）
  - GQA-200 F@100 **21.7**（SOTA），mR@100 **18.4**
  - ISD 模块兼容 TDE、IETrans 等已有去偏方法，显著提升 F@100
  - 消融验证 bottom-up 空间标签远优于 top-down 语义标签（F@100 26.2 vs 23.3~24.6）

### Added: ReLIC-SGG — Relation Lattice Completion for Open-Vocabulary SGG (arXiv 2026)

- **操作**：单篇入库（sub-agent, inbound 批量入库）
- **论文**：[ReLIC-SGG: Relation Lattice Completion for Open-Vocabulary Scene Graph Generation](domains/scene-graph/papers/relic-sgg-relation-lattice-completion-open-vocabulary-sgg.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2026-04-ReLIC-SGG.pdf
- **提取**：raw/sources/2026-04-ReLIC-SGG.txt
- **用户备注**：inbound 批量入库，关系格补全的开放词汇SGG（arXiv 2026）
- **作者**：Amir Hosseini, Sara Farahani, Xinyi Li, Suiyang Guang（Amirkabir University of Technology）
- **关键结果**：VG150 PredCls mR@100=31.0, SGDet mR@50=16.4；OV-VG U-mR@50=18.3, HM@50=22.3；PSG PmR@50=22.0。FN-Recall=45.7（+11.5 vs VL-IRM），Redundancy=9.3（最佳）
- **贡献**：将未标注关系视为潜在变量而非负样本，通过语义关系格（similarity + entailment + contradiction）完成缺失关系补全

### Added: GTR — Grafting-Then-Reassembling Framework for Dynamic Scene Graph Generation (IJCAI 2023)

- **操作**：单篇入库（sub-agent）
- **论文**：[GTR: Grafting-Then-Reassembling Framework for Dynamic Scene Graph Generation](domains/scene-graph/papers/gtr-grafting-then-reassembling-dynamic-scene-graph-generation.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2023-08-generative-compositional-augmentations-sgg.pdf（PDF原始文件名有误，实际内容为GTR）
- **提取**：raw/sources/2023-08-generative-compositional-augmentations-sgg.txt
- **会议**：IJCAI 2023
- **关键结果**：Action Genome上PREDcls R@10=71.2%（+1.8% vs AP-Net），SGcls R@10=48.7%（+1.5%），SGdet R@10=27.9%（+1.6%），仅用60%训练数据
- **贡献**：两阶段时空解耦框架（嫁接静态SGG + 时序依赖重组），噪声过滤器
- **注意**：PDF文件名标注为"Generative Compositional Augmentations"但实际内容为GTR，系下载时文件名混淆

### Added: CAGE-SGG — Counterfactual Active Graph Evidence for Open-Vocabulary SGG (arXiv 2026)

- **操作**：单篇入库（sub-agent, inbound 批量入库）
- **论文**：[CAGE-SGG: Counterfactual Active Graph Evidence for Open-Vocabulary Scene Graph Generation](domains/scene-graph/papers/cage-sgg-counterfactual-active-graph-evidence-open-vocabulary-sgg.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2026-arXiv-CAGE-SGG-Counterfactual-Active-Graph-Evidence-for-Open-Vocabulary-SGG.pdf
- **提取**：raw/sources/2026-arXiv-CAGE-SGG-Counterfactual-Active-Graph-Evidence-for-Open-Vocabulary-SGG.txt
- **用户备注**：inbound 批量入库，反事实主动图证据的SGG（arXiv 2026）
- **关键结果**：SGDet mR@50=15.9（VG150），U-mR@50=17.6（OV-VG），PmR@50=21.0（PSG），CF-Acc=74.9，Hallu-Rate=12.8%；三个基准上一致超越 SOTA，罕见关系增益更大
- **作者**：Suiyang Guang, Chenyu Liu, Ruohan Zhang, Siyuan Chen

### Added: Rethinking the Evaluation of Scene Graph Generation (PRCV 2026)

- **操作**：单篇入库（sub-agent, inbound 批量入库）
- **论文**：[Rethinking the Evaluation of SG: STP and SID Metrics](domains/scene-graph/papers/rethinking-evaluation-scene-graph-generation-stp-sid.md)
- **领域**：scene-graph
- **证据等级**：skimmed
- **来源**：raw/sources/2026-06-09-rethinking-evaluation-scene-graph-generation.txt（Springer 网页提取）
- **用户备注**：inbound 批量入库，多指标和不完整标注下的SGG评测
- **注意**：原始 inbound PDF 文件不存在（路径中无文件）；实际论文标题为 "Rethinking the Evaluation of Scene Graph Generation"，发表于 PRCV 2026（非 CVPR 2024）。本次基于 Springer 网页全文章节内容完成入库。
- **关键结果**：STP@20 置信度 0.1→1.0 时从 0.87→0.99；Ferret (7B) 显著优于 Gemini-1.5-Flash 和 Qwen2.5-VL-32B 做三元组验证
- **作者**：Jingyi Wang, Hanwei Gao, Zhidong Deng

### Added: Importance First — Generating Scene Graph of Human Interest (IJCV 2023)

- **操作**：单篇入库（sub-agent, inbound 批量入库）
- **论文**：[Importance First: Generating Scene Graph of Human Interest (TGIR)](domains/scene-graph/papers/importance-first-human-interest-scene-graph.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2023-06-09-importance-first-generating-scene-graph-human-interest.pdf（Springer DOI 下载，4.9MB）
- **提取**：raw/sources/2023-06-09-importance-first-generating-scene-graph-human-interest.txt（105,576 chars）
- **用户备注**：inbound 批量入库，重要性优先的人-物交互 SGG（IJCV 2023）
- **注意**：原始 inbound PDF 文件内容不匹配（实际为 Stochastic Reaction Networks 论文），已通过 Springer 重新下载正确版本
- **关键结果**：TGIR-G (D-Sup) 在 VG-KR 上关键关系预测 R@20=49.2, mR@20=11.0; 图像描述 CIDEr=81.7/77.2
- **作者**：Wenbin Wang, Ruiping Wang, Shiguang Shan, Xilin Chen

### Updated: OvSGTR — From Data to Modeling (arXiv 2025 journal version)

- **操作**：更新现有论文页（sub-agent）
- **论文**：[OvSGTR: From Data to Modeling — Fully Open-Vocabulary SGG](domains/scene-graph/papers/ovsgtr-expanding-scene-graph-boundaries.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **新增来源**：raw/sources/2025-arXiv-FDtM-Fully-Open-Vocabulary-SGG.pdf (11.6MB)
- **提取**：raw/sources/2025-arXiv-FDtM-Fully-Open-Vocabulary-SGG.txt (71,576 chars, 14 pages)
- **用户备注**：inbound 批量入库，全开放词汇场景图生成（arXiv 2025）
- **更新内容**：
  - 标题从 "Expanding Scene Graph Boundaries" 更新为 "From Data to Modeling"
  - 新增三种关系感知预训练管线对比（场景解析器/LLM/Gemini-MegaSG）
  - 新增零样本 MegaSG 实验结果（PredCls R@100=48.54）
  - 更新 Closed-set/OvD-SGG/OvR-SGG/OvD+R-SGG 四场景结果，含 MegaSG 预训练
  - 原始 ECCV 2024 版本 (arXiv 2311.10988) 保留作为版本引用
  - 关键新增：OvSGTR⋆(Swin-B) Closed-set R@100=43.4, OvD+R-SGG Joint R@50=17.84

### Added: PRISM-0 — A Predicate-Rich Scene Graph Generation Framework with Zero-Shot Capabilities

- **操作**：单篇入库（sub-agent, inbound 批量入库）
- **论文**：[PRISM-0: A Predicate-Rich Scene Graph Generation Framework with Zero-Shot Capabilities](domains/scene-graph/papers/2025-PRISM-0-predicate-rich-zero-shot-sgg.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2025-PRISM-0-Predicate-Rich-SGG.pdf (1.6MB)
- **提取**：raw/sources/2025-PRISM-0-Predicate-Rich-SGG.txt (35,544 chars, 10 pages)
- **用户备注**：inbound 批量入库，谓词丰富零样本场景图生成（arXiv 2025）
- **内容**：TUM + Carl Zeiss Meditec。提出 PRISM-0，模块化零样本开放词汇 SGG 框架。Bottom-up 流水线：Florence-2（节点检测）→ Depth-Anything-V2（深度估计 + Geometry Filter）→ LLaVA-OneVision（regions captioning）→ LLaMA 3.2 3B（CoT 两步三元组提取）→ VQA 验证。全零样本，无数据集训练。在 PredCls 上 mR@100=**14.98**（超越所有弱监督基线），S2GR Gallery 1K R@20=**56.9**（超越 PGSG/MTDE/CaCao，与 LLM4SGG 持平），dCor=**0.18**（与 VG 谓词频率近乎独立，vs DRM 0.65），用户研究五维均优于 VG GT（p<0.05）。GF 移除后 S2GR R@20 下降 47.6%。

### Added: RelCLIPScore — Measuring Image-Relation Alignment

- **操作**：单篇入库（sub-agent）
- **论文**：[RelCLIPScore: Measuring Image-Relation Alignment — Reference-Free Metrics for Visual Relation Detection](domains/scene-graph/papers/relclipscore-reference-free-metrics-visual-relation-detection.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2025-06-09-Measuring_Image_Relation_Alignment.pdf (3.4MB)
- **提取**：raw/sources/2025-06-09-Measuring_Image_Relation_Alignment.txt (43,756 chars)
- **内容**：arXiv 2025。Neau et al. (Umeå University / CNRS / IMT Atlantique / NII)。提出 RelCLIPScore 无参考评估指标用于 OV-SGG，系统评估多种 VLM 的区域关系预测能力（LlaVa-OneVision 7B 最优，NegCLIP 24.02，超越 GPT4o），利用 LlaVa 区域特定提示生成 FG-OV SGG 数据集（200K 图像，1,121 谓词），在 HICO-DET UC-RF Unseen 上达 **16.99%**（vs RLIPv2 15.88%，+7.0% 相对提升）。

### Added: ACC — Interaction-Centric Knowledge Infusion and Transfer for OVSGG

- **操作**：单篇入库（sub-agent）
- **论文**：[ACC: Interaction-Centric Knowledge Infusion and Transfer for OVSGG](domains/scene-graph/papers/acc-interaction-centric-knowledge-infusion-sgg.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2025-arXiv-Interaction-Centric-Knowledge-Infusion-SGG.pdf (7.8MB)
- **提取**：raw/sources/2025-arXiv-Interaction-Centric-Knowledge-Infusion-SGG.txt (95,464 chars, 27 pages)
- **内容**：NeurIPS 2025/arXiv 2511.05935。HKUST + Tencent。提出 ACC，interaction-centric OVSGG 框架。核心贡献：(1) 双向交互提示（BIP）用于鲁棒的伪标注生成；(2) 交互引导 query 选择（IGQS）减少非交互候选误匹配；(3) 交互一致知识蒸馏（VRD+RRD）。VG OvR-SGG（Swin-B）R@100 = 29.28（SOTA），OvD+R-SGG（Swin-B）Joint R@100 = 23.19。另在 GQA、PSG、HICO-DET 上验证有效性。

### Added: DIFFVSGG — Diffusion-Driven Online Video Scene Graph Generation

- **操作**：单篇入库（sub-agent）
- **论文**：[DIFFVSGG: Diffusion-Driven Online Video Scene Graph Generation](domains/scene-graph/papers/diffvsgg-diffusion-driven-online-video-scene-graph-generation.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2025-arXiv-DIFFVSGG-Diffusion-Driven-Online-Video-Scene-Graph-Generation.pdf (1.1MB)
- **提取**：raw/sources/2025-arXiv-DIFFVSGG-Diffusion-Driven-Online-Video-Scene-Graph-Generation.txt (78,309 chars, 18 pages)
- **内容**：arXiv 2503.13957。ZJU + UTS。提出 DIFFVSGG，首个将潜在扩散模型（LDM）用于在线视频场景图生成的方法。统一物体分类、bbox 回归、关系生成于共享特征嵌入的去噪过程。在线逐帧处理，前帧结果作为后帧 LDMs 的条件输入。在 Action Genome（with constraint, ResNet-101+Faster-RCNN）上 PredCLS mR@20 达 **50.2**（vs. TEMPURA 46.3），SGCLS mR@20 达 **38.4**（vs. TEMPURA 35.2）；在 ImageNet-VidVRD 上 RelDet mAP 达 **30.15**（vs. HCM 29.68），RelTag P@1 达 **79.95**（vs. HCM 78.50）。

### Added: Click2Graph — Interactive Panoptic Video Scene Graphs from a Single Click

- **操作**：单篇入库（sub-agent）
- **论文**：[Click2Graph: Interactive Panoptic Video Scene Graphs from a Single Click](domains/scene-graph/papers/click2graph-interactive-panoptic-video-scene-graph.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2025-11-25-click2graph-interactive-panoptic-video-scene-graph.pdf (3.7MB)
- **提取**：raw/sources/2025-11-25-click2graph-interactive-panoptic-video-scene-graph.txt (38,935 chars)
- **用户备注**：inbound 批量入库，交互式全景视频场景图生成（arXiv 2025）
- **内容**：arXiv 2511.15948v2。UC Santa Barbara 提出 Click2Graph，首个用户引导的交互式 PVSG 框架。从单一点击出发，结合 SAM2.1-Large（冻结 224M）+ DIDM（动态交互发现 Transformer）+ SCH（语义分类头），自动发现与目标主体交互的物体并预测关系三元组。在 OpenPVSG 基准上评估，使用 R@K / SpIR / PLR 三个指标。
- **关键结果**：R@3=**2.23**（端到端三元组）；DIDM 在 EPIC K. 上 BBox R@3=**2.08**、SpIR=**25.02**、PLR=**32.06**；DIDM 在 VidOR 上 Mask R@3=**3.33**、SpIR=**18.77**、PLR=**30.82**；DIDM 全面超越启发式基线（Heuristic R@3 仅 0.28-0.68）

### Added: THYME — Temporal Hierarchical-Cyclic Interactivity Modeling for Video Scene Graphs

- **操作**：单篇入库（sub-agent）
- **论文**：[THYME: Temporal Hierarchical-Cyclic Interactivity Modeling for Video Scene Graphs in Aerial Footage](domains/scene-graph/papers/thyme-temporal-hierarchical-cyclic-interactivity-for-video-scene-graphs.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2025-arXiv-THYME-Temporal-Hierarchical-Cyclic-Interactivity-for-Dynamic-SGG.pdf (10.4MB)
- **提取**：raw/sources/2025-arXiv-THYME-Temporal-Hierarchical-Cyclic-Interactivity-for-Dynamic-SGG.txt (74,914 chars, 14 pages)
- **内容**：arXiv 2507.09200。Arkansas 大学 + Ohio State + VNU-HCM。提出 THYME 方法，结合层级特征聚合与循环时序注意力用于视频场景图生成。贡献 AeroEye-v1.0 航拍数据集（2,260 视频，687 关系谓词，五种交互类型）。在 ASPIRe 上 THYME 达 Relation R@20 **21.02** (vs. CYCLO 18.34)，在 AeroEye-v1.0 上 THYME 达 Relation R@20 **16.03** (vs. CYCLO 14.51)。
- **关键结果**：ASPIRe THYME Relation R@20 **21.02**；AeroEye-v1.0 THYME Appearance R@20 **16.52**、Position R@20 **15.52**、Interaction R@20 **13.07**、Relation R@20 **16.03**

### Added: Motion-aware Contrastive Learning for Temporal Panoptic Scene Graph Generation

- **操作**：单篇入库（sub-agent）
- **论文**：[Motion-aware Contrastive Learning for Temporal Panoptic Scene Graph Generation](domains/scene-graph/papers/motion-aware-contrastive-learning-temporal-panoptic-sgg.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2025-AAAI-Motion-aware-Contrastive-Learning-for-Temporal-Panoptic-SGG.pdf (1.4MB)
- **提取**：raw/sources/2025-AAAI-Motion-aware-Contrastive-Learning-for-Temporal-Panoptic-SGG.txt (41,409 chars, 9 pages)
- **内容**：AAAI 2025。NUS + NTU + 同济大学。提出运动感知对比学习框架用于时序全景场景图生成。核心创新：shuffle-based 和 triplet-based 两种负采样策略 + optimal transport 距离度量 mask tube 运动相似性。在 OpenPVSG（vIoU=0.5）上 Ours-Conv 达 R/mR@50 **6.08/4.38**（vs. IPS+T-Conv 5.24/3.29），在 PSG4D 上点云 HOI 达 R/mR@50 **7.62/6.49**（vs. PSG4DFormer 5.61/3.95）。
- **关键结果**：OpenPVSG Ours-Conv R@50 **6.08**；PSG4D-GTA 点云 R/mR@100 **7.31/4.70**；PSG4D-HOI RGB-D R/mR@20 **7.63/6.09**

### Added: SDSGG — Scene Graph Generation with Role-Playing Large Language Models

- **操作**：单篇入库（sub-agent）
- **论文**：[SDSGG: Scene Graph Generation with Role-Playing Large Language Models](domains/scene-graph/papers/sdsgg-scene-specific-description-ovsgg.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2024-12-01-Scene-Graph-Generation-Role-Playing-LLMs.pdf (2.2MB)
- **提取**：raw/sources/2024-12-01-Scene-Graph-Generation-Role-Playing-LLMs.txt (79,090 chars)
- **内容**：NeurIPS 2024。浙江大学 + 长沙理工。提出 SDSGG，基于场景特定描述（SSD）的 OVSGG 框架。核心创新：多角色协作（MPC）让 LLM 扮演不同角色生成上下文感知描述，自归一化相似度计算动态调整文本分类器权重，互视觉适配器（MVA）捕捉 subject-object 交互。在 VG novel split 上 mR@100 达 31.2（vs. CLS 23.8），GQA base 上 R@100 达 49.5（vs. CLS 7.9）。
- **关键结果**：VG base R@100 **31.6** (vs. CLS 3.9, Epic 27.2)；VG novel mR@100 **31.2** (vs. CLS 23.8)；VG semantic R@100 **34.9** (vs. RECODE⋆ 25.0)；GQA base R@100 **49.5** (vs. CLS 7.9)

### Added: CCL-3DSGG — CLIP-Driven Open-Vocabulary 3D Scene Graph Generation

- **操作**：单篇入库
- **论文**：[CCL-3DSGG: CLIP-Driven Open-Vocabulary 3D Scene Graph Generation](domains/scene-graph/papers/ccl-3dsgg-clip-driven-open-vocabulary-3d-scene-graph-generation.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2024-CVPR-CLIP-Driven-Open-Vocabulary-3D-Scene-Graph.pdf (3.4MB)
- **提取**：raw/sources/2024-CVPR-CLIP-Driven-Open-Vocabulary-3D-Scene-Graph.txt (57,336 chars)
- **内容**：CVPR 2024。华东师范大学。提出 CCL-3DSGG，首个基于 CLIP 跨模态对比学习的无监督/开放词汇 3DSGG 方法。核心创新：Grammar Parse 将 caption 分解为词级特征（S/O/P/A 等），Adjective Exchange 生成结构化负样本，T3D/I3D 双对比损失对齐文本-图像-3D 特征。在 3DSSG 上无监督 PREDCLS mR@20 达 29.4（vs. VL-SAT 9.5），开放词汇设置超越监督方法，zero-shot 设置平均提升 VL-SAT 25.1%。
- **关键结果**：监督 Mean Recall **60.1** (vs. VL-SAT 54.4)；无监督 PREDCLS mR@20 **29.4** (vs. VL-SAT 9.5, +209%)；开放词汇 OV-PREDCLS R@50 **64.8**；Zero-shot SGCLS R@50 **35.5** (vs. VL-SAT 21.6)；长尾 Tail mA@3 **61.24** (vs. VL-SAT 52.38)


### Added: RA-SGG — Retrieval-Augmented Scene Graph Generation via Multi-Prototype Learning

- **操作**：单篇入库（批量 inbound）
- **论文**：[RA-SGG: Retrieval-Augmented Scene Graph Generation via Multi-Prototype Learning](domains/scene-graph/papers/ra-sgg-retrieval-augmented-scene-graph-generation-multi-prototype-learning.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2025-AAAI-RA-SGG-Relation-Alignment-for-Robust-Scene-Graph-Generation.pdf (548KB)
- **提取**：raw/sources/2025-AAAI-RA-SGG-Relation-Alignment-for-Robust-Scene-Graph-Generation.txt (48,495 chars)
- **内容**：AAAI 2025。KAIST & Korea University。提出 RA-SGG，将 SGG 重新定义为多标签分类问题，通过内存银行检索增强发现潜在细粒度谓词，使用多原型学习和 IPSS 无偏采样。backbone 为 PE-Net (CVPR'23)。
- **关键结果**：VG PredCls F@100 **42.4** (vs PE-Net 36.5, +16.2%)；GQA F@K 提升高达 **5.9%**；检索人工标注准确率 **84.20%**

### Added: LLM4SGG — Large Language Models for Weakly Supervised SGG

- **操作**：单篇入库
- **论文**：[LLM4SGG: Large Language Models for Weakly Supervised Scene Graph Generation](domains/scene-graph/papers/llm4sgg-weakly-supervised-scene-graph-generation.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2024-CVPR-LLM4SGG-Large-Language-Models-for-Weakly-Supervised-SGG.pdf (2.2MB)
- **提取**：raw/sources/2024-CVPR-LLM4SGG-Large-Language-Models-for-Weakly-Supervised-SGG.txt (58,890 chars)
- **内容**：CVPR 2024。首次将 LLM（ChatGPT）引入弱监督场景图生成。识别 WSSGG 的语义过度简化和低密度场景图两个关键问题，通过 Chain-of-Thought 分解 triplet 提取（Chain-1）和类别对齐（Chain-2）两步。triplet 数量从 154K→344K（+123%），在 VG 上 VS3+LLM4SGG 达 R@100=10.43, mR@100=8.18, F@100=9.17；GQA 上 mR@50 从 1.60→5.33。数据高效：7.8% 数据即可超越基线。

### Added: PGSG — Open-Vocabulary Scene Graph Generation with Vision-Language Models

- **操作**：单篇入库
- **论文**：[PGSG: Open-Vocabulary SGG with Vision-Language Models](domains/scene-graph/papers/pixels-to-graphs-open-vocabulary-sgg-vlm.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2024-CVPR-From-Pixels-to-Graphs-Open-Vocabulary-SGG.pdf (2.2MB)
- **提取**：raw/sources/2024-CVPR-From-Pixels-to-Graphs-Open-Vocabulary-SGG.txt (52,127 chars)
- **内容**：CVPR 2024。首次将 VLM image-to-text generation 用于开放词汇 SGG，提出 PGSG 框架。基于 BLIP，以 image-to-graph 范式直接生成场景图文本序列，再解析为结构化图。关键模块包括实体定位模块（Entity Grounding Module）和类别转换模块（Category Conversion Module）。在 VG、PSG、OpenImage V6 上超越 CaCao、SVRP、VS3、SGTR 等基线。同时统一 SGG 与下游 VL 任务，在 GQA VQA（+1.7）、RefCOCO 视觉定位（testB +5.4）上取得增益。
- **关键结果**：PSG SGDet mR@100 较 SGTR+ViT 提升 **9.4**，R@100 提升 **14.3**；OpenImage mR@100 提升 **5.3**；GQA 总体准确率 **64.2%**（+1.7）；RefCOCO testB **82.4%**（+5.4）



### Added: TSG Bench — LLM Meets Scene Graph

- **操作**：单篇入库
- **论文**：[TSG Bench: LLM Meets Scene Graph — Can LLMs Understand and Generate Scene Graphs?](domains/scene-graph/papers/2025-05-29-tsg-bench-llm-meets-scene-graph.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2025-05-29-LLM-Meets-Scene-Graph.pdf (2.9MB, 26 pages)
- **提取**：raw/sources/2025-05-29-LLM-Meets-Scene-Graph.txt (82,976 chars)
- **内容**：arXiv 2025。提出 TSG Bench，系统评估 LLM 理解（SGDS/SGQA）和生成（SA-SGG/MA-SGG）场景图能力的基准。120 个现实场景、2,041 描述、4,298 场景图。评估 11 个主流 LLM，发现理解任务优秀但生成任务远逊人类——最佳模型 Claude-3.5-Sonnet 在 MA-SGG 上 F1=58.80 仅及人类 75.60 的 78%。动作分解是主要瓶颈。10-shot ICL 可缩小差距（Claude: 58.80→71.75）。错误类型感知引导大幅提升修正能力（Claude: F1 60.03→88.28）。
- **关键结果**：Claude-3.5-Sonnet SGDS=98.40, SGQA(EM)=90.60, SA-SGG(F1)=68.43, MA-SGG(F1)=58.80；Human: SA-SGG(F1)=82.50, MA-SGG(F1)=75.60

### Added: OwSGG — Open World Scene Graph Generation using Vision Language Models

- **操作**：单篇入库
- **论文**：[OwSGG: Open World Scene Graph Generation using Vision Language Models](domains/scene-graph/papers/open-world-scene-graph-generation-using-vlm.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2025-06-09-Open_World_Scene_Graph_Generation_using_VLM.pdf (2.9MB)
- **提取**：raw/sources/2025-06-09-Open_World_Scene_Graph_Generation_using_VLM.txt (77,040 chars)
- **内容**：arXiv 2025。首个完全训练无关（training-free）、模型无关的开放世界场景图生成框架 OwSGG。将 SGG 形式化为零样本结构化推理问题，直接利用预训练 VLM（LLaVA-Next, Qwen2-VL）生成场景图。提出严格 Open World 评估协议（novel Object AND novel Relation）。在 VG150、OIV6、PSG 上全面评估 Close Vocabulary、Zero-Shot、OVR、OvD+R、OW 五种设置。引入多模态提示 + SimCSE 嵌入对齐 + 轻量级 pair refinement。
- **关键结果**：OIV6 PredCls CloseVocab R@100 = **83.78**（超越所有训练过的基线）；PSG SGDet OVR mR@100 = **13.35**（最高）；Open World 设置下 R@100 = 2.41 (Qwen72b)，传统方法均为 0.00

### Added: TextPSG — Panoptic Scene Graph Generation from Textual Descriptions

- **操作**：单篇入库
- **论文**：[TextPSG: Panoptic Scene Graph Generation from Textual Descriptions](domains/scene-graph/papers/textpsg-panoptic-scene-graph-from-textual-descriptions.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2023-ICCV-TextPSG-Panoptic-Scene-Graph-Generation-from-Textual-Descriptions.pdf (3.7MB)
- **提取**：raw/sources/2023-ICCV-TextPSG-Panoptic-Scene-Graph-Generation-from-Textual-Descriptions.txt (57633 chars)
- **内容**：ICCV 2023。首次提出Caption-to-PSG问题——仅从图像-文本对（无位置先验、无区域-实体链接、无预定义概念集）生成mask级全景场景图。提出TextPSG框架（Region Grouper + Entity Grounder + Segment Merger + Label Generator），基于GroupViT和BLIP，通过PET（Prefix Embedding Tuning）利用预训练常识。在PSG数据集上显著超越所有基线和SGGNLS-o。
- **关键结果**：PhrDet N5R100=14.37（bbox模式，vs. SGCLIP 3.71, vs. SGGNLS-o 7.93）；SGDet N5R100=5.48（vs. SGCLIP 2.70, vs. SGGNLS-o 5.02）；OOD Set PhrDet N5R100=11.69（vs. SGGNLS-o 0.06）

### Added: R1-SGG — Compile Scene Graphs with Reinforcement Learning

- **操作**：单篇入库
- **论文**：[R1-SGG: Compile Scene Graphs with Reinforcement Learning](domains/scene-graph/papers/r1-sgg-compile-scene-graphs-with-reinforcement-learning.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2025-arXiv-R1-SGG-Compile-Scene-Graphs-with-Reinforcement-Learning.pdf (2.6MB)
- **提取**：raw/sources/2025-arXiv-R1-SGG-Compile-Scene-Graphs-with-Reinforcement-Learning.txt (55574 chars)
- **内容**：arXiv 2025。首个将GRPO强化学习应用于多模态大模型端到端场景图生成的工作。提出两阶段训练框架（SFT+RL），设计图中心奖励（Hard Recall/Soft Recall）和格式奖励，对齐标准SGDET指标。基于Qwen2-VL-2B/7B，在VG150和PSG上均超越传统SGG方法和其他M-LLM基线。
- **关键结果**：VG150上R1-SGG(7B) Recall=23.75%, mRecall=11.43%, Failure Rate=0.08%；PSG上Recall=43.48%, mRecall=33.71%, Failure Rate=0.00%。RL将Failure Rate从SFT的39.54%-72.42%降至<1%。

### Added: FunGraph — Functionality-Aware 3D Scene Graphs for Language-Prompted Scene Interaction

- **操作**：单篇入库
- **论文**：[FunGraph: Functionality-Aware 3D Scene Graphs for Language-Prompted Scene Interaction](domains/scene-graph/papers/fungraph-functionality-aware-3d-scene-graphs.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2025-06-09-FunGraph.pdf (6.2MB)
- **提取**：raw/sources/2025-06-09-FunGraph.txt (47309 bytes)
- **内容**：IROS 2025。首个在3D场景图中显式建模功能性交互元素(functional elements)和intra-object关系的框架。通过从SceneFun3D(3D)投影生成2D训练数据→训练RT-DETR→扩展ConceptGraphs pipeline，实现功能元素节点+has-part关系。可在低成本RGB-D传感器上运行。
- **关键结果**：2D检测RT-DETR(ST) mAP50:95=21.0；3D功能元素分割AP25=30.3%；Affordance Grounding AP25=33.3%（vs ConceptGraphs 0.0%，vs SceneFun3D最优 17.5%）；GPT-Context标签精炼正确率78.0%

### Added: SIL — Improving Scene Graph Generation with Superpixel-based Interaction Learning

- **操作**：单篇入库
- **论文**：[SIL: Improving Scene Graph Generation with Superpixel-based Interaction Learning](domains/scene-graph/papers/superpixel-interaction-learning-scene-graph-generation.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2023-ACM-MM-Improving-Scene-Graph-Generation-with-Superpixel-based-Interaction-Learning.pdf (5.8MB)
- **提取**：raw/sources/2023-ACM-MM-Improving-Scene-Graph-Generation-with-Superpixel-based-Interaction-Learning.txt (69028 bytes)
- **内容**：ACM MM 2023。提出Superpixel-based Interaction Learning (SIL)范式，将场景图生成中的粗粒度框级交互提升为超像素级细粒度交互。将图像视为点集，通过聚类得到超像素，建模intra-entity和cross-entity交互。即插即用模块可集成到任意SGG方法中。
- **关键结果**：VG PredCls上7个baseline平均提升+2.0% mR（最高BGNN +3.4% mR@50）；PE-Net+SIL在PredCls mR@100达35.3%（超越此前SOTA）；OI V6上PE-Net+SIL scorewtd达45.5%。

### Added: FlowSG — Progressive Image-Conditioned Scene Graph Generation with Flow Matching (arXiv 2026)

- **操作**：单篇入库（sub-agent, inbound 批量入库）
- **论文**：[FlowSG: Progressive Image-Conditioned Scene Graph Generation with Flow Matching](domains/scene-graph/papers/flowsg-progressive-image-conditioned-scene-graph-flow-matching.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2026-06-09-FlowS-Can-We-Build-Scene-Graphs-Not-Classify-Them.pdf (1.4MB)
- **提取**：raw/sources/2026-06-09-FlowS-Can-We-Build-Scene-Graphs-Not-Classify-Them.txt (52,251 bytes, 11 pages)
- **用户备注**：inbound 批量入库，流式场景图生成（arXiv 2026）
- **作者**：Xin Hu, Ke Qin, Wen Yin, Yuan-Fang Li, Ming Li, Tao He（电子科技大学 + 天府绛溪实验室 + Monash University + 广东省人工智能与数字经济实验室（深圳））
- **关键结果**：
  - PSG SGDet R@100 **53.3%** / mR@100 **48.3%**（超 SOTA USG-Par ~3 点）
  - VG SGDet R@100 **42.4%** / mR@100 **21.6%**（+3-4 点）
  - PSG 开集 mR@50 **22.3%**（超 VL-IRM ~+4 点）
  - 流匹配框架实现少步推理，语义-几何联合渐进式生成

### Added: SGR3 Model — Scene Graph Retrieval-Reasoning Model in 3D (arXiv 2026)

- **操作**：单篇入库（sub-agent, inbound 批量入库）
- **论文**：[SGR3 Model: Scene Graph Retrieval-Reasoning Model in 3D](domains/scene-graph/papers/sgr3-model-scene-graph-retrieval-reasoning-model-3d.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2026-06-09-SGR3_Egocentric_Video_Scene_Graph_Retrieval.pdf (8.1 MB, 8 pages)
- **提取**：raw/sources/2026-06-09-SGR3_Egocentric_Video_Scene_Graph_Retrieval.txt (40,375 chars)
- **用户备注**：inbound 批量入库，第一视角视频场景图检索推理模型（arXiv 2026）
- **作者**：Zirui Wang, Ruiping Liu, Yufan Chen, Junwei Zheng, Weijia Fan, Kunyu Peng, Di Wen, Jiale Wei, Jiaming Zhang, Rainer Stiefelhagen (KIT / Shenzhen University / Hunan University)
- **贡献**：
  - 训练无关的 3D 场景图生成框架，无需显式 3D 重建和相机位姿
  - ColPali 风格的 RAG 检索管线 + 加权 patch 投票机制提高检索鲁棒性
  - 系统分析了 RAG 对 MLLM 场景图生成的作用机制（复制比率 64.7%，推理过程中检索信息显式参与 token 生成）
- **关键结果**：
  - 3RScan 上 Rel New R@1 **0.125**（训练无关方法中最佳，与有监督 MonoSSG 0.131 可比）
  - Pred R@3 **0.78**，Rel Old R@1 **0.62**
  - 知识库移除后 Rel Rec 从 0.125 降至 0.061（-51%），验证 RAG 必要性

## 2026-06-08

### Added: PE-Net — Prototype-based Embedding Network for Scene Graph Generation

- **操作**：单篇入库
- **论文**：[PE-Net: Prototype-based Embedding Network for Scene Graph Generation](domains/scene-graph/papers/prototype-based-embedding-network-scene-graph-generation.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2023_CVPR_PE-Net_Prototype-based_Embedding_Network_for_Scene_Graph_Generation.pdf
- **提取**：raw/sources/2023_CVPR_PE-Net_Prototype-based_Embedding_Network_for_Scene_Graph_Generation.txt (47712 bytes)
- **内容**：CVPR 2023。提出原型对齐嵌入网络(PE-Net)，利用谓词类原型在语义空间中建模紧致可区分的表示，通过实体-谓词匹配进行关系识别。包含Prototype-guided Learning(PL)和Prototype Regularization(PR)两个核心组件。VG上PredCls mR@100=33.8%，Open Images scorewtd=44.9，零样本Recall超越TDE方法。
- **关键结果**：VG PredCls mR@100=33.8，SGCls mR@100=18.9，SGDet mR@100=14.5；PE-Net-Reweight PredCls R@100=61.4；Open Images scorewtd=44.9

### Added: VS³ — Language-supervised and Open-vocabulary Scene Graph Generation

- **操作**：单篇入库
- **论文**：[VS³: Language-supervised and Open-vocabulary Scene Graph Generation](domains/scene-graph/papers/language-supervised-open-vocabulary-scene-graph-vs3.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2023-CVPR-Learning-to-Generate-Language-supervised-and-Open-vocabulary-Scene-Graph-VS3.pdf
- **提取**：raw/sources/2023-CVPR-Learning-to-Generate-Language-supervised-and-Open-vocabulary-Scene-Graph-VS3.txt (55484 bytes)
- **内容**：CVPR 2023。利用预训练GLIP的视觉-语义空间(VSS)同时解决SGG两大瓶颈——廉价获取语言监督 + 开放词汇泛化。提出VS³模型（GLIP扩展关系识别模块），在VG150上全监督/语言监督/开放词汇SGDET均创新SOTA。语言监督Unlocalized graph R@100=34.96（超过许多全监督方法），开放词汇SGDET ZsO-SGG R@50=21.51（首次报告该协议结果）。
- **关键结果**：全监督SGDET R@100=41.5(Swin-L)；语言监督Unlocalized graph R@100=34.96；开放词汇PREDCLS R@100=58.18(Swin-L)

### Added: Panoptic Video Scene Graph Generation (PVSG)

- **操作**：单篇入库
- **论文**：[Panoptic Video Scene Graph Generation](domains/scene-graph/papers/panoptic-video-scene-graph-generation.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2023-CVPR-Panoptic-Video-Scene-Graph-Generation.pdf
- **提取**：raw/sources/2023-CVPR-Panoptic-Video-Scene-Graph-Generation.txt (45782 bytes)
- **内容**：CVPR 2023。提出PVSG新任务，将视频场景图节点从bbox细化为像素级panoptic segmentation mask。贡献PVSG数据集（400视频/150K帧/126物体类/57关系类）。提出两阶段框架：Stage-1（IPS+T或VPS）获得mask tube特征，Stage-2（4种关系分类器）预测时域关系。最佳方法(IPS+T+Transformer Encoder) R@100=4.88, mR@100=2.03。
- **关键结果**：IPS+T+Transformer Encoder R@100=4.88,mR@100=2.03；VPS+Transformer Encoder R@100=0.94,mR@100=0.40

### Added: IS-GGT — Iterative Scene Graph Generation with Generative Transformers

- **操作**：单篇入库
- **论文**：[IS-GGT: Iterative Scene Graph Generation with Generative Transformers](domains/scene-graph/papers/is-ggt-iterative-scene-graph-generation-with-generative-transformers.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2023-CVPR-IS-GGT-Iterative-Scene-Graph-Generation-with-Generative-Transformers.pdf
- **提取**：raw/sources/2023-CVPR-IS-GGT-Iterative-Scene-Graph-Generation-with-Generative-Transformers.txt (49206 bytes)
- **内容**：CVPR 2023。提出IS-GGT（Iterative Scene Graph Generation with Generative Transformers），两阶段生成式SGG方法。先用生成式Transformer解码器采样交互图（~20%边缘），再对采样边缘进行谓词分类。在Visual Genome上无去偏平均mR@100=20.7%，零样本性能2×超越对比方法。核心创新：生成式图采样替代N²全连接比较，大幅降低推理开销。
- **关键结果**：PredCls mR@100=31.9, SGCls mR@100=18.9, SGDet mR@100=11.3, 平均mR@100=20.7；零样本zR@50平均=4.1（2×以上超越对比方法）

### Added: SQUAT — Selective Quad Attention for Scene Graph Generation

- **操作**：单篇入库
- **论文**：[SQUAT: Selective Quad Attention for Scene Graph Generation](domains/scene-graph/papers/squat-selective-quad-attention-scene-graph-generation.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2023-CVPR-Devils-on-the-Edges-Selective-Quad-Attention-for-Scene-Graph-Generation-SQUAT.pdf
- **提取**：raw/sources/2023-CVPR-Devils-on-the-Edges-Selective-Quad-Attention-for-Scene-Graph-Generation-SQUAT.txt (50237 bytes)
- **内容**：CVPR 2023。提出SQUAT (Selective Quad Attention Network)，通过边缘选择模块（ESM）筛选有效物体对 + 四元注意力（N2N/N2E/E2N/E2E）实现鲁棒场景图生成。在Visual Genome和OpenImages v6上超越SOTA。核心洞见：全连接图消息传递对SGG有害，移除无效边缘是关键。
- **关键结果**：VG SGDet mR@100=16.5 vs BGNN 12.6 (+31%)，SGCls mR@100=18.8 vs BGNN 16.5 (+14%)，OI score_wtd=43.5（SOTA持平RU-Net）

### Added: Incremental 3D Semantic Scene Graph Prediction from RGB Sequences

- **操作**：单篇入库
- **论文**：[Incremental 3D Semantic Scene Graph Prediction from RGB Sequences](domains/scene-graph/papers/incremental-3d-scene-graph-prediction-from-rgb-sequences.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2023-06-01-incremental_3d_scene_graph.pdf
- **提取**：raw/sources/2023-06-01-incremental_3d_scene_graph.txt (56075 bytes)
- **内容**：CVPR 2023。首个仅依赖RGB序列的实时增量式3D语义场景图预测框架。提出置信度融合的增量实体估计IEE管道 + 基于多视图特征和gated geometric feature的GNN场景图预测网络。在3RScan上超越IMP/VGfM/3DSSG/SGFN等SOTA方法。
- **关键结果**：GT输入 Recall Rel=66.1, Obj=81.2, Pred=71.5, mRecall Obj=95.6, Pred=77.4；增量标签关联AOS=39.6%；运行时~206ms/帧

### Added: Unbiased Heterogeneous Scene Graph Generation with Relation-Aware Message Passing Neural Network

- **操作**：单篇入库
- **论文**：[Unbiased Heterogeneous Scene Graph Generation with Relation-Aware Message Passing Neural Network](domains/scene-graph/papers/unbiased-heterogeneous-scene-graph-generation-with-relation-aware-message-passing.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2023-AAAI-Unbiased-Heterogeneous-Scene-Graph-Generation-with-Relation-Aware-Message-Passing-Neural-Network.pdf
- **提取**：raw/sources/2023-AAAI-Unbiased-Heterogeneous-Scene-Graph-Generation-with-Relation-Aware-Message-Passing-Neural-Network.txt (50422 bytes)
- **内容**：AAAI 2023，提出HetSGG框架，首次将场景图生成视为异构图问题，通过关系感知消息传递网络（RMP）捕获谓词类型感知的上下文信息，包含高效基矩阵分解（b=8）。在Visual Genome和Open Images V6上超越SOTA，尤其在尾部谓词类上提升显著。
- **关键结果**：SGCls mR@100=18.7 vs BGNN*‡ 16.0（+16.9%），OI SGGen mR@50=42.7 vs BGNN‡ 40.5（+5.4%）

### Added: 3D Spatial Multimodal Knowledge Accumulation for Scene Graph Prediction in Point Cloud

- **操作**：单篇入库
- **论文**：[3D Spatial Multimodal Knowledge Accumulation for Scene Graph Prediction in Point Cloud](domains/scene-graph/papers/3d-spatial-multimodal-knowledge-accumulation-scene-graph-prediction-point-cloud.md)
- **领域**：scene-graph (新建)
- **证据等级**：full-paper
- **来源**：raw/sources/2023-06-01-3d-spatial-multimodal-knowledge-accumulation-scene-graph-prediction-point-cloud.pdf
- **提取**：raw/sources/2023-06-01-3d-spatial-multimodal-knowledge-accumulation-scene-graph-prediction-point-cloud.txt (52070 bytes)
- **内容**：CVPR 2023，提出3D空间多模态知识积累方法（SMKA）用于点云场景图预测，利用ConceptNet构建层级符号知识图+区域感知图网络+多模态知识积累，在3DSSG数据集上超越SGPN/EdgeGCN/KISG等SOTA方法
- **关键结果**：PredCls R@50=68.32, SGCls R@50=31.50, SGDet R@50=29.41，均优于现有方法

### Added: Scalable Theory-Driven Regularization of Scene Graph Generation Models (Paper Page Complete)

- **操作**：单篇入库（sub-agent，补全 paper page）
- **论文**：[Scalable Theory-Driven Regularization for Scene Graph Generation](domains/scene-graph/papers/scalable-theory-driven-regularization-scene-graph-generation.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2023-AAAI-Scalable-Theory-Driven-Regularization-SGG.pdf (1.08 MB)
- **提取**：raw/sources/2023-AAAI-Scalable-Theory-Driven-Regularization-SGG.txt (56,416 chars)
- **用户备注**：inbound 批量入库，理论驱动正则化的 SGG（AAAI 2023）
- **内容**：AAAI 2023。University of Padova + Samsung AI。提出 NGP（Neural-Guided Projection），模型无关的神经符号正则化技术，通过负完整性约束（负原子 IC）注入大规模常识知识。核心创新：(1) 使用概率或模糊逻辑损失衡量预测违反 IC 的程度；(2) Neural-Guided Projection（贪心选择 ρ=3 个最违反约束）实现百万级 IC 可扩展；(3) 模型无关，零推理开销。构建两个理论：CNet¬（基于 ConceptNet，~500K ICs）和 VG¬（基于 VG 训练数据补集，~1M ICs）。支持与去偏技术 TDE 正交叠加。
- **关键结果**：
  - IMP SGCls mR@50 6.31→8.45 (+33%, 最大相对提升)
  - IMP PredCls mR@100 12.23→15.30 (+25%)
  - VCTree + TDE + NGP PredCls mR@100 29.48→34.19 (+16%); SGCls mR@100 16.73→17.66
  - MOTIFS + TDE + NGP PredCls mR@100 27.66→28.16, zsR@100 17.11→17.80
  - VCTree + TDE + NGP vs. KBFN mR@100: 34.19 vs 18.43 (+86%); vs BGNN mR@100: 34.19 vs 3.63 (+90%)
  - 50% 标注减少下 IMP zsR@100 3.06→18.99（+520%）
  - 低频谓词 `belonging to` R@100 +23,142%, `on back of` +24,943%
  - NGP + TDE 提升非加性叠加（大于单独应用之和）

---

## 2026-06-05

### Added: BurnResu: A Multi-Task Temporal Prediction Framework for Early Burn Resuscitation

- **操作**：单篇入库
- **论文**：`healthcare-ai/papers/burnresu-multi-task-temporal-prediction-for-early-burn-resuscitation.md`
- **领域**：healthcare-ai
- **证据等级**：full-paper
- **来源**：raw/sources/2026-02-01-burnresu-multi-task-temporal-prediction-for-early-burn-resuscitation.pdf
- **内容**：本文提出 BurnResu，一个用于早期烧伤复苏的多任务时序预测框架。

---

## 2026-06-05 (earlier)

### Added: Edge-Aware Regularization for Graph Neural Networks

- **操作**：单篇入库
- **论文**：`graph-neural-networks/papers/edge-aware-regularization-for-gnns.md`
- **领域**：graph-neural-networks
- **证据等级**：abstract-only
- **来源**：N/A (arXiv 摘要)
- **内容**：边缘感知正则化方法，用于提升图神经网络的泛化能力。

## 2026-06-09

### Added: Diff-VRD — Generalized Visual Relation Detection with Diffusion Models

- **操作**：单篇入库（sub-agent）
- **论文**：[Diff-VRD: Generalized Visual Relation Detection with Diffusion Models](domains/scene-graph/papers/diff-vrd-generalized-visual-relation-detection-with-diffusion-models.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2025-06-09-generalized-visual-relation-detection-with-diffusion-models.pdf (8.1 MB, 15 pages, arXiv:2504.12100)
- **提取**：raw/sources/2025-06-09-generalized-visual-relation-detection-with-diffusion-models.txt (77,593 chars, 2,101 lines)
- **用户备注**：inbound 批量入库，扩散模型做广义视觉关系检测（arXiv 2025）
- **内容**：IEEE TCSVT 2024。浙江大学/NTU/SMU。提出 Diff-VRD，将视觉关系建模为连续嵌入，通过扩散模型实现超越预定义类别的广义 VRD。引入 T2I Retrieval 和 SPICE PR Curve 两个代理指标。构建 4858 词汇表 V。
- **关键结果**：HICO-DET（V/V）R@5=17.28%（vs. THID 1.99%）; T2I Retrieval HICO-DET R@1=11.13%（超越 GT 7.97%）, X-VLM R@1=15.12%; VG 增强 IETrans: T2I R@1=17.72%（vs. 12.12%, +46.2%）; SPICE PR Curve 全面优于 CLIP baseline 和 UPT

### Added: TEMPURA — Unbiased Scene Graph Generation in Videos

- **操作**：单篇入库
- **论文**：[TEMPURA: Unbiased Scene Graph Generation in Videos](domains/scene-graph/papers/tempura-unbiased-video-scene-graph-generation.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2023-CVPR-TEMPURA-Unbiased-Scene-Graph-Generation-in-Videos.pdf
- **提取**：raw/sources/2023-CVPR-TEMPURA-Unbiased-Scene-Graph-Generation-in-Videos.txt (54169 chars)
- **用户备注**：排队入库，无偏视频场景图生成
- **内容**：CVPR 2023。提出 TEMPURA 框架，通过 OSPU（object-level 时序一致性建模）+ GMM Head（高斯混合模型不确定性衰减）+ MDU（记忆原型引导的知识迁移），系统性地解决视频场景图生成中的长尾偏置和标注噪声问题。在 Action Genome 数据集上与 STTran 等 SOTA 对比，With Constraint 设置下 PredCLS mR@10=42.9（+5.1 vs. STTran 37.8）, SGCLS mR@10=34.0（+5.7 vs. STTran 27.2）, SGDET mR@10=18.5（+1.9 vs. STTran 16.5）。No Constraints 设置下提升更大：PredCLS mR@10=61.5（+10.1）, SGCLS mR@10=48.3（+7.6）, SGDET mR@10=24.7（+3.8）。
- **关键结果**：PredCLS mR@10=42.9（With Constraint），无约束最高 61.5；SGCLS mR@10=34.0（With Constraint），无约束 48.3；在 TAIL 类上显著优于 STTran/TRACE

---

### Added: HATS — Hazard-Aware Traffic Scene Graph Generation (arXiv 2026)

- **操作**：单篇入库（sub-agent, inbound 批量入库）
- **论文**：[HATS: Hazard-Aware Traffic Scene Graph Generation](domains/scene-graph/papers/hazard-aware-traffic-scene-graph-generation.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2026-hazard-aware-traffic-scene-graph-generation.pdf (4.3 MB)
- **提取**：raw/sources/2026-hazard-aware-traffic-scene-graph-generation.txt (47,016 chars, 1,305 lines)
- **用户备注**：inbound 批量入库，危险感知交通场景图生成（arXiv 2026）
- **作者**：Yaoqi Huang, Julie Stephany Berrio, Mao Shan, Stewart Worrall (ACFR, University of Sydney)
- **arXiv**：arXiv:2603.03584v2 (2026-05-04)
- **内容**：提出 HATS（Hazard-Aware Traffic Scene Graph Generation）框架，以自车为中心生成危险感知交通场景图。包含 PS 模块（Mask2Former 全景分割）、ERES 模块（可学习交叉注意力筛选路径相关实体）、TSGG 模块（三头预测：作用机制/方位/严重度）。辅助 KG 分支融合 NHTSA 交通事故数据构建 16,066 节点、153,488 边知识图谱，通过 KGE 提供结构化先验。在 Cityscapes 820 张标注图像上评估。
- **关键结果**：
  - KGE Object Prediction MRR=88.04%, H@10=99.77%
  - HP mAP@10=82.90%, MRR@10=96.60%, NDCG@10=89.47%
  - SGDet R@50=62.79%, mR@50=76.13%（vs. MOTIFS 29.68/9.38）
  - Entity Relevance F1=95.03%（vs. PSGTR 44.24%）, AUC=97.20%, MAE=0.047
  - Entity Prominence F1=90.89%（vs. CFHP 62.49%）, AUC=92.17%, MAE=0.103
  - Severity R@1=80.10%, Side R@1=82.40%, Mechanism R@1=73.16%

### Added: SG-Adapter — Scene Graph Guided Generation for Text-to-Image Models

- **操作**：单篇入库
- **论文**：[SG-Adapter: Scene Graph Guided Generation for Text-to-Image Models](domains/scene-graph/papers/sg-adapter-scene-graph-guided-generation.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2025-ICCV-SG-Adapter-scene-graph-guided-generation.pdf
- **提取**：raw/sources/2025-ICCV-SG-Adapter-scene-graph-guided-generation.txt (41749 chars)
- **用户备注**：排队入库，场景图指导文生图（2025 ICCV），SGG下游应用方向
- **内容**：ICCV 2025。提出 SG-Adapter，利用场景图结构化表示作为 CLIP 文本编码后处理模块，通过 Token-Triplet 注意力掩码纠正因果注意力导致的"关系泄漏"(relation leakage)问题。同时构建 MultiRels 数据集（309 张高精度多关系标注图像）和三项 GPT-4V 评估指标（SG-IoU/Entity-IoU/Relation-IoU）。在 T2I 任务上 SG-IoU=0.623（SD=0.157），Relation Accuracy=77.6%（SD=5.38%）；在 SG→Image 任务上 FID=25.1（SGDiff=36.2），SG-IoU=0.413（SGDiff=0.122）。
- **关键结果**：T2I: SG-IoU=0.623, Entity-IoU=0.812, Relation-IoU=0.753, Relation Acc=77.6%, FID=26.2；SG2I: FID=25.1, IS=57.8, SG-IoU=0.413

### Added: CFA — Compositional Feature Augmentation for Unbiased Scene Graph Generation

- **操作**：单篇入库
- **论文**：[CFA: Compositional Feature Augmentation for Unbiased Scene Graph Generation](domains/scene-graph/papers/compositional-feature-augmentation-for-unbiased-scene-graph-generation.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2023-ICCV-Compositional-Feature-Augmentation-for-Unbiased-SGG.pdf
- **提取**：raw/sources/2023-ICCV-Compositional-Feature-Augmentation-for-Unbiased-SGG.txt (50410 chars)
- **用户备注**：排队入库，上下文特征增强场景图生成（注：原标题实为 Compositional Feature Augmentation）
- **内容**：ICCV 2023。提出 CFA（Compositional Feature Augmentation）策略，将关系三元组特征分解为内在特征（intrinsic）和外在特征（extrinsic），通过 Intrinsic-CFA（替换实体特征）和 Extrinsic-CFA（Mixup 上下文特征）增强尾部谓词的特征多样性，首次从特征增强角度解决无偏 SGG 的长尾偏置。模型无关，可集成 Motifs/VCTree/Transformer。在 VG 和 GQA 上均达 SOTA。
- **关键结果**：VG PredCls: Motifs+CFA mR@50=35.7（+19.2 vs baseline 16.5），mR@100=38.2；Mean=46.2（SOTA trade-off）；GQA PredCls mR@50=31.7（+17.8 vs baseline 13.9）

---


### Added: Hi-Dyna Graph — Hierarchical Dynamic Scene Graph for Robotic Autonomy in Human-Centric Environments

- **操作**：单篇入库
- **论文**：[Hi-Dyna Graph: Hierarchical Dynamic Scene Graph for Robotic Autonomy in Human-Centric Environments](domains/scene-graph/papers/2025-05-30-hidynagraph.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2025-05-30-hidynagraph.pdf
- **提取**：raw/sources/2025-06-09-hidynagraph.txt (80040 bytes)
- **用户备注**：排队入库，分层动态场景图用于机器人自主导航操作（arXiv 2025），SGG下游应用方向
- **内容**：arXiv 2025 (2506.00083)。提出 Hi-Dyna Graph，一种层次化动态场景图架构，整合持久的全局拓扑图（房间连通性+大型家具）与局部动态语义子图（物体位置关系+人-物交互）。全局图从带位姿 RGB-D 构建，局部图从视频流（环境/第一人称）预测关系，通过语义+空间约束锚定，结合 LLM 推理实现自主任务生成与执行。在 OpenPVSG 上 open-vocabulary R@50=11.91 vs PSG4D 7.02；30 分钟动态更新维持 V. Acc. ~0.71-0.76；真实机器人咖啡厅助理部署验证端到端自主操作。
- **关键结果**：Open-vocab R@50=11.91（OpenPVSG），In-vocab R@50=9.75；30min 动态 V. Acc.=0.71-0.76, E. Acc.=0.90-0.95

### Added: FDSG — Forecasting Dynamic Scene Graphs

- **操作**：单篇入库
- **论文**：[FDSG: Forecasting Dynamic Scene Graphs](domains/scene-graph/papers/fdsg-forecasting-dynamic-scene-graphs.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2025-06-09-FDSG-Forecasting-Dynamic-Scene-Graphs.pdf (18.9MB)
- **提取**：raw/sources/2025-06-09-FDSG-Forecasting-Dynamic-Scene-Graphs.txt (68417 bytes)
- **用户备注**：排队入库，动态场景图预测（arXiv 2025）
- **内容**：arXiv 2025 (2506.01487)。提出 FDSG 框架，首次在动态场景图中同时预测未来帧的实体标签、边界框和关系三元组。核心创新包括：(1) Query Decomposition 将 triplet 分解为 entity content/location/relation 三个分量分别通过 Neural SDE 建模连续时间演化；(2) Temporal Aggregation Module 用 cross-attention 融合观察与预测信息；(3) Location Dynamics Model 显式建模边界框动态。在 Action Genome 的 DSGG/SGA/SGF 三个任务上均超越 SOTA，尤其 SGF 任务上 FDSG 的 R@50 比 SceneSayer 高出 2× 以上。
- **关键结果**：DSGG SGDET R@50 No C=56.5（vs OED 51.8）；SGA AGS F=0.5 mR@10=18.1（vs SceneSayerSDE 12.4）；SGF F=0.5 mR@10=8.4（vs SceneSayerSDE+ 3.1）

---

### Added: SSC-SGG — Semi-Supervised Clustering for Weakly Supervised Scene Graph Generation

- **操作**：单篇入库
- **论文**：[SSC-SGG: Semi-Supervised Clustering for Weakly Supervised Scene Graph Generation](domains/scene-graph/papers/ssc-sgg-semi-supervised-clustering-weakly-supervised-scene-graph-generation.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2025-AAAI-SSC-SGG-Semi-Supervised-Clustering-Weakly-Supervised-Scene-Graph-Generation.pdf
- **提取**：raw/sources/2025-AAAI-SSC-SGG-Semi-Supervised-Clustering-Weakly-Supervised-Scene-Graph-Generation.txt (49093 bytes)
- **用户备注**：排队入库，半监督聚类框架用于弱监督场景图生成（AAAI 2025）
- **内容**：AAAI 2025。提出 SSC-SGG 框架，基于原型聚类从无标注物体对中挖掘有效伪标签。核心组件：Multi-View Prototype-based Clustering (MPC) 增强特征鲁棒性；Dynamic pseudo-Label Assignment (DLA) 通过最优运输 + 历史分配权重动态调整，解决长尾偏置。在 VG150 上以 Motifs baseline 在 M@100 提升 8-25%，全面超越伪标签方法 IETrans (+10.2%) 和 ST-SGG (+11.8%)；Open Image V6 上 Motifs mR@50 33.98→42.48，Transformer 32.12→44.26。
- **关键结果**：VG150 Motifs baseline SGDet M@100=42.3→SSC-SGG=48.0；OI V6 Motifs mR@50=33.98→42.48；MPC 组件单独提升 mR@K 40.7%

---

### Added: OvSGTR — Expanding Scene Graph Boundaries: Fully Open Vocabulary SGG

- **操作**：单篇入库
- **论文**：[OvSGTR: Expanding Scene Graph Boundaries — Fully Open Vocabulary SGG](domains/scene-graph/papers/ovsgtr-expanding-scene-graph-boundaries.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2024-ECCV-Expanding-Scene-Graph-Boundaries.pdf (5.2MB)
- **提取**：raw/sources/2024-ECCV-Expanding-Scene-Graph-Boundaries.txt (45875 chars)
- **用户备注**：排队入库，全开放词汇场景图生成（ECCV 2024）
- **内容**：ECCV 2024。提出 OvSGTR 统一框架，将SGG从封闭集扩展到全开放词汇设置（同时覆盖节点和边的开放集识别）。系统性定义了四种SGG场景：Closed-set SGG / OvD-SGG / OvR-SGG / OvD+R-SGG（后两种为本文首次系统研究）。
  核心创新：(1) 视觉-概念对齐利用COCO Caption弱监督进行关系感知预训练；(2) 视觉-概念保持通过知识蒸馏缓解关系灾难性遗忘。
  基于DETR-like端到端transformer架构，冻结Swin-B/BERT-backbone，轻量关系头（2层MLP）。
- **关键结果**：Closed-set SGG R@100=42.4 (Swin-B)；OvD-SGG Novel Object R@50=59.30 (vs VS³ 46.91, +26.4%)；OvR-SGG Novel Relation R@50=16.39 (首次非零结果)；OvD+R-SGG Novel Relation R@50=14.56 (vs VS³ 0.00)。蒸馏使OvR-SGG Novel R@50从0.34提升至13.45。

---

### Added: OED — Towards One-stage End-to-End Dynamic Scene Graph Generation

- **操作**：单篇入库
- **论文**：[OED: Towards One-stage End-to-End Dynamic Scene Graph Generation](domains/scene-graph/papers/oed-one-stage-end-to-end-dynamic-scene-graph-generation.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2024-CVPR-OED-Towards-One-stage-End-to-End-Dynamic-Scene-Graph-Generation.pdf (1.3MB)
- **提取**：raw/sources/2024-CVPR-OED-Towards-One-stage-End-to-End-Dynamic-Scene-Graph-Generation.txt (47960 chars)
- **内容**：CVPR 2024。提出 OED（One-stage End-to-end Dynamic scene graph generation），首个将DSGG重构为集合预测问题的单阶段端到端框架。核心组件：(1) 级联解码器（Pair-wise Instance Decoder → Pair-wise Relation Decoder）聚合空间上下文；(2) Progressively Refined Module (PRM) 通过多步渐进式筛选参考帧pair-wise特征聚合时序上下文，无需额外跟踪器或手绘轨迹。在Action Genome的SGDET任务上全面超越多阶段SOTA方法（STTran, APT, TR², TEMPURA, DSG-DETR, TPT等）。
- **关键结果**：SGDET With Constraint R@10=33.5, R@20=40.9, R@50=48.9；No Constraint R@10=35.3, R@20=44.0, R@50=51.8。PredCLS With Constraint R@10=73.0, R@20=76.1, R@50=76.1。

---

### Added: HiKER-SGG — Hierarchical Knowledge Enhanced Robust Scene Graph Generation

- **操作**：单篇入库
- **论文**：[HiKER-SGG: Hierarchical Knowledge Enhanced Robust Scene Graph Generation](domains/scene-graph/papers/hiker-sgg-hierarchical-knowledge-enhanced-robust-sgg.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2024-CVPR-HiKER-SGG-Hierarchical-Knowledge-Enhanced-Robust-SGG.pdf (5.3MB)
- **提取**：raw/sources/2024-CVPR-HiKER-SGG-Hierarchical-Knowledge-Enhanced-Robust-SGG.txt (57921 chars)
- **用户备注**：排队入库，层级知识增强鲁棒场景图生成（CVPR 2024）
- **内容**：CVPR 2024。提出 HiKER-SGG，利用层级知识图谱从粗到细的推理增强 SGG 在真实世界图像退化下的鲁棒性。核心组件：外部知识库→层级知识图谱（谓词+实体层级）→消息传递→自适应细化。同时引入 VG-C 基准（20 种程序化退化，包括 15 种标准 + 5 种真实世界退化如阳光眩光/水滴/野火烟雾/雨/灰尘）。在干净 VG 和受损 VG-C 上均超越 SOTA 知识图谱方法（GB-Net、EB-Net+EOA），零样本鲁棒性显著（mR@100 UC 仅下降 11.3%，vs EB-Net 14.5%）。
- **关键结果**：VG Clean PredCls mR@100=69.2(UC)/41.2(C)；SGCls mR@100=36.7(UC)/21.4(C)；VG-C 平均 mR@100 UC=61.4(-11.3%)；在 GB-Net 和 EB-Net 上平均提升约 4%。

---

### Added: CAModule — A Causal Adjustment Module for Debiasing Scene Graph Generation

- **操作**：单篇入库
- **论文**：[CAModule: A Causal Adjustment Module for Debiasing Scene Graph Generation](domains/scene-graph/papers/camodule-causal-adjustment-module-debiasing-scene-graph-generation.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2025-arXiv-CAModule-Causal-Adjustment-Module-for-Debiasing-Scene-Graph-Generation.pdf (3.0MB)
- **提取**：raw/sources/2025-arXiv-CAModule-Causal-Adjustment-Module-for-Debiasing-Scene-Graph-Generation.txt (111579 chars)
- **用户备注**：排队入库，因果推理去偏场景图生成（arXiv 2025, TPAMI under review）
- **内容**：arXiv 2025 (TPAMI under review)。提出 CAModule 因果调整模块，通过 Mediator-based Causal Chain Model (MCCM) 进行 triplet 级别的 logit adjustment。分析了比关系长尾更深层的偏置根源——对象分布和对象对分布的倾斜。引入 co-occurrence distribution 作为中介变量，结合 Euclidean distance 和 cosine similarity 学习隐空间 adjustment factors。通过两个推理规则 (Rule 1/2) 支持零样本关系组合。在 VG150、GQA、Open Images V6 上与 MotifsNet/VCTree/Transformer 三个框架集成，mR@K 和 zR@K 均达 SOTA。
- **关键结果**：VG150 PredCls VCTree backbone CAModule mR@100=40.5；MotifsNet PredCls mR@20/50/100=32.5/36.7/39.3，zR@20/50/100=9.5/16.7/20.3；OI V6 mR@50=40.3，R@50=43.7；零样本 zR@K 显著超越 CAModule-P（无对象对分布优化变体），MotifsNet PredCls zR@100=16.7 vs CAModule-P=9.5

---

### Added: UASAN — Open-Vocabulary Video Scene Graph Generation via Union-aware Semantic Alignment

- **操作**：单篇入库
- **论文**：[UASAN: Open-Vocabulary Video Scene Graph Generation via Union-aware Semantic Alignment](domains/scene-graph/papers/2024-10-28-UASAN-open-vocabulary-video-SGG-union-aware-semantic-alignment.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2024-10-28-UASAN-Open-Vocab-Video-SGG-Union-Aware-Alignment.pdf (479KB)
- **提取**：raw/sources/2024-10-28-UASAN-Open-Vocab-Video-SGG-Union-Aware-Alignment.txt (65637 chars)
- **用户备注**：排队入库，开放词汇视频场景图生成（ACM MM 2024）
- **注意**：inbound PDF 实际内容为 SST-1M 望远镜论文 (arXiv:2409.18639)，与标题不匹配；已从 OpenReview 获取正确全文
- **内容**：ACM MM 2024。提出 UASAN 框架，通过显式建模视觉联合区域（union region）与关系谓词之间的语义对齐实现开放词汇视频场景图生成。三组件架构：Visual Refiner（知识迁移）+ Semantic-Aware Context Encoder（语义上下文交互）+ Union-Relation Alignment Decoder（对齐解码）。在 VidVRD 和 VidOR 上评估，仅用 base-split 训练达到 SOTA。
- **关键结果**：VidVRD Novel-Split SGDet mAP=11.05%（vs RePro 6.10%），RelDet mAP=23.57%（vs RePro 21.33%），PredCls mAP=17.62%（novel）/38.43%（all），均超越现有开放词汇方法。

---

### Added: RelTR — Relation Transformer for Scene Graph Generation

- **操作**：单篇入库
- **论文**：[RelTR: Relation Transformer for Scene Graph Generation](domains/scene-graph/papers/reltr-relation-transformer-scene-graph-generation.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2023-TPAMI-RelTR-Relation-Transformer-for-Scene-Graph-Generation.pdf (10MB)
- **提取**：raw/sources/2023-TPAMI-RelTR-Relation-Transformer-for-Scene-Graph-Generation.txt (81723 chars)
- **用户备注**：inbound 批量入库，关系Transformer用于场景图生成（TPAMI 2023，Trans部分架构）
- **内容**：TPAMI 2023。提出 RelTR，首个**纯视觉单阶段端到端**场景图生成模型，将 SGG 重构为集合预测问题。基于 Transformer encoder-decoder 架构，使用 coupled subject/object queries 和三种注意力模块（CSA/DVA/DEA）直接推断稀疏场景图，无需组合实体对和枚举所有谓词。在 Visual Genome、Open Images V6 和 VRD 三个数据集上验证。
- **关键结果**：VG SGDET: R@50=27.5, mR@50=10.8, 63.7M params, 16.6FPS；OI V6: score_wtd=42.99（SOTA）, 16.3FPS；VRD: RelDet R@50=29.2, R@100=32.2

---

### Added: PSG-4D — 4D Panoptic Scene Graph Generation

- **操作**：单篇入库
- **论文**：[4D Panoptic Scene Graph Generation (PSG-4D)](domains/scene-graph/papers/4d-panoptic-scene-graph-generation.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2023-12-01-4D_Panoptic_Scene_Graph_Generation.pdf (13.8MB)
- **提取**：raw/sources/2023-12-01-4D_Panoptic_Scene_Graph_Generation.txt (54731 chars)
- **用户备注**：inbound 批量入库，4D全景场景图生成（NeurIPS 2023）
- **内容**：NeurIPS 2023。提出 PSG-4D 新任务，将场景图从静态 3D 扩展至动态 4D（3D+时间）。构建 PSG4D 数据集（PSG4D-GTA 合成第三人称 + PSG4D-HOI 真实第一人称），共 ~3K RGB-D 视频/1M 帧。提出 PSG4DFormer 两阶段框架（4D Panoptic Segmentation + Spatial-Temporal Transformer 关系建模），支持 RGB-D 和点云输入。集成 GPT-4 部署于服务机器人展示实际应用价值。
- **关键结果**：RGB-D 输入 PSG4DFormer：PSG4D-GTA R/mR@20=6.68/3.31, R/mR@50=7.17/3.85, R/mR@100=7.22/4.02；PSG4D-HOI R/mR@20=5.62/3.65, R/mR@50=6.16/4.16, R/mR@100=6.28/4.97。深度和时序建模均被验证为关键组件。

### Added: DRM — Leveraging Predicate and Triplet Learning for Scene Graph Generation

- **操作**：单篇入库（重试）
- **论文**：[DRM: Leveraging Predicate and Triplet Learning for Scene Graph Generation](domains/scene-graph/papers/leveraging-predicate-and-triplet-learning-for-sgg.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2024-06-09-leveraging-predicate-and-triplet-learning-for-sgg.pdf (6.5 MB)
- **提取**：raw/sources/2024-06-09-leveraging-predicate-and-triplet-learning-for-sgg.txt (1,569 行)
- **内容**：CVPR 2024。提出 Dual-granularity Relation Modeling (DRM) 网络，联合谓词级和三元组级关系建模。引入 Dual-granularity Knowledge Transfer (DKT) 策略，将头部谓词/三元组方差迁移至尾部，缓解 SGG 长尾问题。基于 Faster RCNN (ResNeXt-101-RPN) + 4 层 Hybrid Attention 骨干。使用监督对比学习作双重粒度约束。在 VG150、Open Image V6、GQA200 上超越 SOTA。
- **关键结果**：VG150 PredCls mR@100 = 49.6（超越 SHA+GCL 5.5、CaCao 5.9）；Open Image score_wtd = 47.9（超越 PE-Net 3.0）；GQA200 PredCls mR@100 = 43.5

---

### Added: Open3DSG — Open-Vocabulary 3D Scene Graphs from Point Clouds with Queryable Objects and Open-Set Relationships

- **操作**：单篇入库
- **论文**：[Open3DSG: Open-Vocabulary 3D Scene Graphs from Point Clouds with Queryable Objects and Open-Set Relationships](domains/scene-graph/papers/open3dsg-open-vocabulary-3d-scene-graphs-from-point-clouds.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2024-CVPR-Open3DSG-Open-Vocabulary-3D-Scene-Graphs-from-Point-Clouds.pdf (1.2MB)
- **提取**：raw/sources/2024-CVPR-Open3DSG-Open-Vocabulary-3D-Scene-Graphs-from-Point-Clouds.txt (53,486 chars)
- **内容**：CVPR 2024。首个从3D点云直接进行开放词汇3D场景图预测的方法。将3D GNN特征与2D VLM（OpenSeg + InstructBLIP）特征空间对齐，实现零样本物体查询（通过CLIP余弦相似度）和开放集关系预测（通过InstructBLIP Qformer+LLM）。零样本在3DSSG上达到Object R@10=0.68、Predicate R@5=0.70、Relationship R@100=0.66。尾部类表现显著优于全监督方法（Obj Tail R@5=0.42 vs SGRec3D 0.24）。2D-3D融合优于单独使用任何模态。
- **关键结果**：3DSSG零样本 Obj R@5=0.57, R@10=0.68；Pred R@3=0.63, R@5=0.70；Rel R@50=0.64, R@100=0.66；Obj Tail R@5=0.42（SGRec3D 0.24）；Pred Tail R@3=0.57（SGRec3D 0.65）

### Added: Adaptive Fine-Grained Predicates Learning for Scene Graph Generation

- **操作**：单篇入库（inbound 批量入库）
- **论文**：[Adaptive Fine-Grained Predicates Learning for Scene Graph Generation](domains/scene-graph/papers/adaptive-fine-grained-predicates-learning-scene-graph-generation.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2023-TPAMI-adaptive-fine-grained-predicates-learning-scene-graph-generation.pdf (4.8 MB, 从 arXiv:2207.04602 下载)
- **提取**：raw/sources/2023-TPAMI-adaptive-fine-grained-predicates-learning-scene-graph-generation.txt (104,551 chars, 3,195 行)
- **用户备注**：inbound 批量入库，自适应细粒度谓词学习（TIP 2023）→ 实际发表于 TPAMI 2023
- **内容**：TPAMI 2023。提出 Adaptive Fine-Grained Predicates Learning (FGPL-A) 框架，通过 Adaptive Predicate Lattice (PL-A，含 Batch-Refinement 的 CRM/ERM) 动态建模谓词相关性，Adaptive Category Discriminating Loss (CDL-A) 和 Adaptive Entity Discriminating Loss (EDL-A) 自适应调节区分过程。Model-agnostic 集成于 Transformer/Motif/VCTree。在 VG-SGG 上 PredCls mR@100 达 44.3%（VCTree+FGPL-A，相比 baseline 16.1 提升 175%），Group Mean Recall Head/Body/Tail 均 ~42%。GQA-SGG PredCls mR@100 达 7.9%。Sentence-to-Graph Retrieval R@100 达 54.9%（VCTree+FGPL-A）。
- **关键结果**：VG-SGG PredCls mR@100：VCTree+FGPL-A=44.3（↑175%）, Transformer+FGPL-A=42.4（↑142%）, Motif+FGPL-A=40.7（↑158%）；Group Mean Recall Transformer+FGPL-A: Head=42.2, Body=42.7, Tail=42.4（Mean=42.4）；GQA-SGG PredCls mR@100 Transformer+FGPL-A=7.9
- **注意**：原始 inbound PDF 为无关论文（Matrix Models for the Nested Hypergeometric Tau-Functions），已从 arXiv 下载正确版本替换。

### Added: ADTrans — Panoptic Scene Graph Generation with Semantics-Prototype Learning

- **操作**：单篇入库（sub-agent）
- **论文**：[ADTrans: Panoptic Scene Graph Generation with Semantics-Prototype Learning](domains/scene-graph/papers/adtrans-adaptive-data-transfer-panoptic-scene-graph-debiasing.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2024-02-01-panoptic-scene-graph-generation-with-semantics-prototype-learning.pdf (1.3MB)
- **提取**：raw/sources/2024-02-01-panoptic-scene-graph-generation-with-semantics-prototype-learning.txt (38,872 chars)
- **用户备注**：inbound 批量入库，语义增强视角的全景场景图生成（AAAI 2024）
- **内容**：AAAI 2024。新加坡国立大学 + 悉尼大学 + 浙江大学 + 杭州城市大学。提出 ADTrans（Adaptive Data Transfer），一种针对 PSG 标注偏差的数据级去偏框架。核心创新：鲁棒对比训练（RCT）+ 动态原型学习 + 多阶段数据过滤，自适应转换不可区分三元组和潜在正样本。在 PSG 和 VG 两个数据集上显著提升所有 baseline 的性能。
- **关键结果**：PSGTR + ADTrans 在 PSG SGDet 上 mR@100 **30.0**（vs. baseline 22.1, +35.7%）；MOTIFS + ADTrans 在 VG PredCLS 上 mR@100 **38.8**（vs. baseline 16.2, +139.5%）；在 VG 四个任务（PredCls/SGCls/SGDet/SGDET）上均取得新 SOTA

### Added: Scene Graph Generation With Hierarchical Context (HCNet)

- **操作**：单篇入库（sub-agent，inbound 批量入库）
- **论文**：[Scene Graph Generation With Hierarchical Context](domains/scene-graph/papers/scene-graph-generation-with-hierarchical-context.md)
- **领域**：scene-graph
- **证据等级**：abstract-only
- **用户备注**：inbound 批量入库，层次上下文场景图生成（AAAI 2024）
- **⚠️ 说明**：原始 PDF 文件路径无效（`/home/node/.openclaw/media/inbound/2024_AAAI_Scene_Graph_Generation_with_Hierarchical_Context__---c25f0c99-8b90-427c-9e99-071999a6ebbc.pdf` 不存在）。
- **内容**：IEEE TNNLS 2021（用户标注为 AAAI 2024，实际出版于 TNNLS）。Guanghui Ren, Lejian Ren, Yue Liao, Si Liu, Bo Li, Jizhong Han, Shuicheng Yan。提出 HCNet（Hierarchical Context Network），从 pair（interaction context）、object（depression context）、graph（global context）三个层级集成上下文信息增强谓词表示。实验在 Visual Genome 上进行，优于当时 SOTA。
- **元数据来源**：CrossRef / Semantic Scholar（abstract-only，未获取到全文）

### Added: Multi-Prototype Space Learning for Commonsense-Based Scene Graph Generation

- **操作**：单篇入库（sub-agent）
- **论文**：[Multi-Prototype Space Learning for Commonsense-Based Scene Graph Generation](domains/scene-graph/papers/multi-prototype-space-learning-commonsense-sgg.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2024-AAAI-Multi-Prototype-Space-Learning-for-Commonsense-SGG.pdf (1.5MB)
- **提取**：raw/sources/2024-AAAI-Multi-Prototype-Space-Learning-for-Commonsense-SGG.txt (44,179 chars, 1,248 lines)
- **内容**：AAAI 2024。华东师范大学。提出多原型学习（MPL）框架用于常识性场景图生成（C-SGG）。核心创新：三重最优传输（TOT）匹配谓词-原型、动量更新自适应寻找多类中心、类间可分性+类内紧致性损失优化原型空间。在 VG 数据集上平均 Recall 54.2（SOTA），SGDET R@50=42.2、SGCLS R@50=49.2、PREDCLS R@50=75.1。在 Open Images V6 上也取得 SOTA（mR@50=43.98, R@50=76.34）。消融实验验证 TOT 比传统 OT 提升 +1.1~+2.2 mR，K=3 为最优原型数。
- **关键结果**：VG mean Recall **54.2** (vs. PE-Net 46.4)；SGDET R@50 **42.2**；PREDCLS R@50 **75.1**；Open Images V6 mR@50 **43.98**

### Added: ZING-3D — Zero-shot Incremental 3D Scene Graphs via Vision-Language Models

- **操作**：单篇入库（sub-agent）
- **论文**：[ZING-3D: Zero-shot Incremental 3D Scene Graphs via Vision-Language Models](domains/scene-graph/papers/zing-3d-zero-shot-incremental-3d-scene-graphs.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2025-arXiv-ZING-Zero-shot-Incremental-3D-Scene-Graphs-via-Hierarchical-Alignment.pdf (4.5MB)
- **提取**：raw/sources/2025-arXiv-ZING-Zero-shot-Incremental-3D-Scene-Graphs-via-Hierarchical-Alignment.txt (31,773 chars, 842 lines)
- **用户备注**：inbound 批量入库，零样本增量3D场景图（arXiv 2025）
- **内容**：arXiv 2025。BITS Pilani + NUS。提出 ZING-3D，零样本增量式3D场景图生成框架。使用 VLM（Gemini 2.5-Flash）从 RGB 序列生成2D场景图，Grounded-SAM2 分割后通过深度投影至3D空间，支持逐帧增量融合和任务导向剪枝。采用人工评估（非标准 SGG 指标），在 Replica 数据集上 Node Prec. **0.97**、Edge Prec. **0.96**；HM3D 上 Node Prec. **0.96**、Edge Prec. **0.98**。VLM 消融实验显示 Gemini 2.5-Flash 最优（Node Prec. **0.96**, Edge Prec. **0.94**），Flash-Lite 速度快但略低（0.93/0.93），Qwen2.5-VL-7B 最差（0.83/0.88，耗时280s）。
- **关键结果**：Replica Node Prec. **0.97**（96-98% range）；HM3D Node Prec. **0.96**（97-98% edge）；Gemini 2.5-Flash Node Prec. **0.96** Valid Obj **93%** Edge Prec. **0.94**（Table II）

### Added: Salient Temporal Encoding for Dynamic Scene Graph Generation

- **操作**：单篇入库（sub-agent，inbound 批量入库）
- **论文**：[Salient Temporal Encoding for Dynamic Scene Graph Generation (STRE)](domains/scene-graph/papers/salient-temporal-encoding-dynamic-sgg.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2025-arXiv-Salient-Temporal-Encoding-for-Dynamic-SGG.pdf (17.1 MB)
- **提取**：raw/sources/2025-arXiv-Salient-Temporal-Encoding-for-Dynamic-SGG.txt (46,300 chars, 1,486 lines)
- **用户备注**：inbound 批量入库，显著时序编码的动态场景图生成（arXiv 2025）
- **内容**：arXiv 2025。CMU 独立工作。提出 STRE（Salient Temporal Relation Encoder），通过 Saliency Attention 选择性建立稀疏帧间时序连接（仅 top-K 相关物体对），替代现有方法全连接稠密时序策略。时序关系编码为显式边。在 Action Genome 上 SGDet-R@20 达 **38.4**（vs STTran 34.1 +4.3, vs APT 36.1 +2.3）；SGDet-mR@50 **42.7**（vs TRACE 40.1 +2.6）；参数量仅 STTran 的 24%（21.7M vs 91.8M），FLOPs 仅 21%。下游 Action Recognition 在 Charades 上 mAP **45.5**（vs SGFB 44.3 +1.2, vs LFB 42.5 +3.0）。
- **关键结果**：SGDet-R@20 **38.4**；SGDet-mR@50 **42.7**；SGDet-wmAPr **17.9**；Action Recognition mAP **45.5**（ST-SGFB）

### Added: HyperGLM — HyperGraph for Video Scene Graph Generation and Anticipation

- **操作**：单篇入库（sub-agent，inbound 批量入库）
- **论文**：[HyperGLM: HyperGraph for Video Scene Graph Generation and Anticipation](domains/scene-graph/papers/hyperglm-hypergraph-for-video-scene-graph-generation-and-anticipation.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2025-CVPR-HyperGLM-HyperGraph-for-Video-Scene-Graph-Generation.pdf (8.3 MB)
- **提取**：raw/sources/2025-CVPR-HyperGLM-HyperGraph-for-Video-Scene-Graph-Generation.txt (51,923 chars, 11 pages)
- **用户备注**：inbound 批量入库，超图视频场景图生成（CVPR 2025）
- **内容**：CVPR 2025。University of Arkansas + Ohio State University。提出 HyperGLM，将统一超图（融合实体场景图和过程图）注入 Mistral-7B-Instruct。核心创新：实体场景图建模空间关系，过程图通过转移概率（式3-5）建模关系类别时序因果演化，random-walk 构造超边（Algorithm 1），经 MLP 注入 LLM。同时发布 VSGR 数据集（1.9M 帧，3,748 视频，支持 SGG/SGA/VQA/VC/RR 五任务）。
- **关键结果**：SGG-VSGR R@20 **35.8** (vs CYCLO 29.4)；SGA-VSGR R@10 **30.2** (vs SceneSayerSDE 27.5)；SGA-Action Genome R@10 **38.8** (vs SceneSayerSDE 37.3)；VQA-Accuracy **45.4** (vs Chat-UniVi 44.3)；RR-Accuracy **47.2** (vs LLaMA-VID 44.1)

### Added: Assured Autonomy with Neuro-Symbolic Perception for Scene Graph Generation



- **操作**：单篇入库（sub-agent，inbound 批量入库）

- **论文**：[Assured Autonomy with Neuro-Symbolic Perception for Scene Graph Generation](domains/scene-graph/papers/assured-autonomy-neuro-symbolic-perception-sgg.md)

- **领域**：scene-graph

- **证据等级**：full-paper

- **来源**：raw/sources/2025-arXiv-Assured-Autonomy-Neuro-Symbolic-SGG.pdf (17.0 MB)

- **提取**：raw/sources/2025-arXiv-Assured-Autonomy-Neuro-Symbolic-SGG.txt (48,373 chars, 713 lines)

- **用户备注**：inbound 批量入库，神经符号感知鲁棒 SGG（arXiv 2025）

- **内容**：PMLR 288:1-19, 2025 (arXiv:2505.21322)。Duke University。提出 NeuSPaPer（Neuro-Symbolic Paradigm for Perception），利用场景图生成桥接低层传感器感知与高层符号推理用于保证CPS安全性。框架四组件：(1) joint perception + graph generation（foundation model用于相机图，规则几何函数用于LiDAR图）；(2) per-sensor graph integrity（KGEs + CSE）；(3) cross-sensor graph integrity（暴力/ GNN图一致性比较）；(4) graph-informed sensor fusion。定可行性案例研究，在CARLA和nuScenes上通过跨传感器图不一致性检测frustum攻击。首次单平台检测此前认爲隐身性的frustum攻击（位移40m+，IoU>0.9）。

- **关键结果**：Frustum攻击最大位移 **40 m+**（保持IoU > 0.9时隐身）；跨传感器图一致性成功检测van/行人平移攻击（CARLA+nuScenes定性案例）。无标准SGG指标（position paper）。


### Added: OOTSM — Language-Driven Object-Oriented Two-Stage Method for Scene Graph Anticipation

- **操作**：单篇入库（sub-agent）
- **论文**：[OOTSM: Language-Driven Object-Oriented Two-Stage Method for Scene Graph Anticipation](domains/scene-graph/papers/language-driven-oo-two-stage-psg.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2025-arXiv-Language-Driven-OO-Two-Stage-PSG.pdf (1.5MB)
- **提取**：raw/sources/2025-arXiv-Language-Driven-OO-Two-Stage-PSG.txt (60,470 chars)
- **用户备注**：inbound 批量入库，语言驱动面向对象的两阶段 PSG（arXiv 2025）
- **注意**：PDF metadata 显示实际标题为 "Scene Graph Anticipation"（场景图预测）而非 "Panoptic Scene Graph Generation"，已按实际内容入库。
- **内容**：arXiv 2509.05661。HKUST + Qilu University of Technology。提出 OOTSM，将场景图预测形式化为语言域时序推理问题。两阶段架构：GOA（预测未来对象集合）+ OORA（预测对象关系轨迹），基于 LoRA 微调 Llama-3.2-3B Instruct。在 Action Genome 上视频 SGA 的 mR@50 达 **51.7**（F=0.9, w/ GOA），长程预测 mR@50 比 SceneSayerSDE 提升 **21.9%**。纯文本 LSGA 设置下 R@20=**73.6** 超越 GPT-4o（63.9）和 DeepSeek-V3（57.9）。

*最后更新：2026-06-09*

### Added: HiLo — Exploiting High Low Frequency Relations for Unbiased PSG

- **操作**：单篇入库（sub-agent，inbound 批量入库）
- **论文**：[HiLo: Exploiting High Low Frequency Relations for Unbiased PSG](domains/scene-graph/papers/hilo-exploiting-high-low-frequency-for-unbiased-panoptic-scene-graph-generation.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2023-ICCV-HiLo-PSG.pdf (1.5MB)
- **提取**：raw/sources/2023-ICCV-HiLo-PSG.txt (62,878 chars)
- **用户备注**：inbound 批量入库，高低频关系用于全景SGG（ICCV 2023）
- **内容**：ICCV 2023。King's College London + 同济大学 + TU Delft。提出 HiLo 框架解决 PSG 中长尾问题与关系语义重叠的耦合挑战。核心创新：(1) Relation Swapping 构建 H-L/L-H 两分支数据；(2) HiLo Prediction Alignment（Subject-Object + Relation consistency loss）；(3) HiLo Inference Fusion。首个显式无偏 PSG 方法。
- **关键结果**：PSG SGDet R50 mR@100 **33.1**（vs PSGTR 24.5, +11%）；Rare 关系 mR@100 **20.3**（vs PSGTR 6.2, +14.1）；语义重叠数据 mR@100 **38.8**（vs PSGTR 23.5, +15.3）。12 epochs 收敛（PSGTR 需 60 epochs）。

### Added: TEMPURA — Unbiased Scene Graph Generation in Videos

- **操作**：inbound 批量入库（sub-agent，发现已有页面，匹配现存文件）
- **论文**：[TEMPURA: Unbiased Scene Graph Generation in Videos](domains/scene-graph/papers/tempura-unbiased-video-scene-graph-generation.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源验证**：raw/sources/2023-CVPR-TEMPURA-Unbiased-Scene-Graph-Generation-in-Videos.pdf (3.3MB)
- **提取验证**：raw/sources/2023-CVPR-TEMPURA-Unbiased-Scene-Graph-Generation-in-Videos.txt (54,514 chars)
- **用户备注**：inbound 批量入库，视频场景图生成去偏（CVPR 2023）
- **内容**：CVPR 2023。UC Riverside + Intel。提出 TEMPURA，通过对象级时序一致性（OSPU + 对比学习）、GMM 不确定性衰减和记忆原型去偏（MDU），首次系统性解决视频 SGG 中的长尾偏置和标注噪声。在 Action Genome 上 PredCLS mR@10 达 **42.9**（+5.1% vs. best baseline, With Constraint），No Constraints 下 mR@10 **61.5**（+10.1%）。TAIL 类性能显著优于 STTran 和 TRACE。

### New: EICR — Environment Invariant Curriculum Relation Learning for Fine-Grained SGG

- **操作**：新论文入库（sub-agent）
- **论文**：[EICR: Environment Invariant Curriculum Relation Learning for Fine-Grained SGG](domains/scene-graph/papers/eicr-environment-invariant-curriculum-relation-learning-sgg.md)
- **领域**：scene-graph
- **学年**：2023
- **会议**：ICCV 2023
- **证据等级**：full-paper
- **来源验证**：raw/sources/2023-ICCV-Environment-Invariant-Curriculum-Relation-Learning-for-Scene-Graph-Generation.pdf (1.3MB)
- **提取验证**：raw/sources/2023-ICCV-Environment-Invariant-Curriculum-Relation-Learning-for-Scene-Graph-Generation.txt (53,170 chars)
- **用户备注**：inbound 批量入库，环境不变课程关系学习（ICCV 2023）
- **内容**：ICCV 2023。Xidian University。提出 EICR 框架，首次在 SGG 中同时处理谓词类别不均衡和主客体语境不均衡。使用环境不变学习（IRM）消除语境偏置 + 类均衡课程学习消除类别偏置。VCTree + EICR 在 VG 上 PredCls mR@50/100 达 **35.6/37.9**，F@50/100 **43.6/45.8**，mR@K 提升超 14%。

### Added: TDE — Unbiased Scene Graph Generation via Two-Stage Causal Modeling (TPAMI 2023)

- **操作**：单篇入库（sub-agent, inbound 批量入库）
- **论文**：[TDE: Unbiased Scene Graph Generation via Two-Stage Causal Modeling](domains/scene-graph/papers/unbiased-scene-graph-generation-tde-causal-modeling.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2023-TPAMI-Unbiased-Scene-Graph-Generation-via-Two-Stage-Causal-Modeling.pdf（3.9MB, 16 pages）
- **提取**：raw/sources/2023-TPAMI-Unbiased-Scene-Graph-Generation-via-Two-Stage-Causal-Modeling.txt（69,571 chars）
- **用户备注**：inbound 批量入库，两阶段因果建模去偏 SGG（TPAMI 2023）
- **内容**：TPAMI 2023 期刊版（扩展自 CVPR 2020）。NTU + Alibaba DAMO + 清华。提出 Total Direct Effect (TDE) 框架，通过反事实推理分离好/坏偏置实现无偏 SGG。模型无关，可应用于任何 SGG backbone。MOTIFS†+SUM+TDE 在 VG PredCls 上 mR@100 从 **15.8 提升至 29.1（+84%）**，ZSRR PredCls R@100 从 14.5 提升至 18.2。代码开源。

### Added: CaCao/Epic — Visually Prompted Language Model for Fine-Grained SGG in an Open World (ICCV 2023)

- **操作**：单篇入库（sub-agent, inbound 批量入库）
- **论文**：[Visually Prompted Language Model for Fine-Grained SGG in an Open World (CaCao/Epic)](domains/scene-graph/papers/visually-prompted-language-model-fine-grained-sgg-open-world.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2023-ICCV-visually-prompted-language-model-fine-grained-sgg-open-world.pdf (1.4MB)
- **提取**：raw/sources/2023-ICCV-visually-prompted-language-model-fine-grained-sgg-open-world.txt (65,030 chars, 1867 lines)
- **用户备注**：inbound 批量入库，视觉提示语言模型的开集细粒度SGG（ICCV 2023）
- **作者**：Qifan Yu, Juncheng Li, Yu Wu, Siliang Tang, Wei Ji, Yueting Zhuang（浙江大学 + 武汉大学 + 新加坡国立大学）
- **关键结果**：
  - Transformer+CaCao PredCls mR@100 **43.7%** v.s. baseline 17.6%（+26.1%）
  - Epic 开集设置 novel R@100 **18.3** v.s. 8.7（+9.6%）
  - CaCao Ablation Acc@1/10 **0.74/0.92** v.s. backbone 0.08/0.21

### Added: RelWitness — Open-Vocabulary 3D Scene Graph Generation with Visual-Geometric Relation Witnesses (arXiv 2026)

- **操作**：单篇入库（sub-agent, inbound 批量入库）
- **论文**：[RelWitness: Open-Vocabulary 3D Scene Graph Generation with Visual-Geometric Relation Witnesses](domains/scene-graph/papers/relwitness-open-vocabulary-3d-scene-graph-generation.md)
- **领域**：scene-graph
- **证据等级**：abstract-only ⚠️
- **来源**：raw/sources/2026-01-01-RelWitness-Open-Vocabulary-3D-Scene-Graph-Generation.pdf (3.8 MB, 14 pages)
- **提取**：raw/sources/2026-01-01-RelWitness-Open-Vocabulary-3D-Scene-Graph-Generation.txt (64,268 chars)
- **用户备注**：inbound 批量入库，开放词汇3D场景图生成RelWitness（arXiv 2026）
- **作者**：Minh Anh Nguyen, Quang Huy Tran, Bao Ngoc Le, Tuan Kiet Pham, Sui Yang Guang
- **arXiv**：2605.20823v3
- **机构**：Phenikaa University
- **方法**：提出 relation witness 概念，结合 RGB 视图、深度图、3D 几何、角色敏感文本、多视角一致性等视觉-几何线索构建见证记录；经见证质量评估后将未标注候选分为验证缺失正例、可靠负例、不确定候选；用见证引导 PU 学习训练；以见证一致解码输出场景图
- **关键结果（均为 simulated manuscript-planning numbers）**：
  - 3DSSG 闭集：R@50 **69.3%**，mR@50 **38.4%**
  - OV-3DSSG 开放词汇：U-mR@50 **25.7%**，HM@50 **29.3%**
  - 缺失关系审计：WP **78.9%**，Halluc. **12.7%**，Redun. **8.8%**
  - 文中明确标注所有数值为模拟规划值，非实际复现结果

*最后更新：2026-06-09*

### Verified: UASAN — Open-Vocabulary Video Scene Graph Generation via Union-aware Semantic Alignment (ACM MM 2024)

- **操作**：验证已有论文页（inbound 批量入库请求，sub-agent）
- **论文**：[UASAN: Open-Vocabulary Video Scene Graph Generation via Union-aware Semantic Alignment](domains/scene-graph/papers/2024-10-28-UASAN-open-vocabulary-video-SGG-union-aware-semantic-alignment.md)
- **领域**：scene-graph
- **证据等级**：full-paper（已验证）
- **用户备注**：inbound 批量入库，跨模态学习的开放词汇视频 SGG（ACM MM 2024）
- **发现问题**：inbound PDF 文件实际为 SST-1M 望远镜论文（arXiv:2409.18639），内容不匹配。论文页已存在且内容完整（70+ 具体数字），无需重新入库
- **修复**：清理误拷贝的 raw/sources 文件；修复 index.md 中的重复条目

### Added: MoSA — Motion-Guided Semantic Alignment for Dynamic Scene Graph Generation (arXiv 2026)

- **操作**：单篇入库（sub-agent）
- **论文**：[MoSA: Motion-Guided Semantic Alignment for Dynamic Scene Graph Generation](domains/scene-graph/papers/mosa-motion-guided-semantic-alignment-dynamic-scene-graph-generation.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2026-arXiv-MOSA-Motion-Guided-Semantic-Alignment-for-Dynamic-SGG.pdf (1.4 MB)
- **提取**：raw/sources/2026-arXiv-MOSA-Motion-Guided-Semantic-Alignment-for-Dynamic-SGG.txt (27,851 chars, 921 lines)
- **用户备注**：inbound 批量入库，运动引导语义对齐的动态SGG（arXiv 2026）
- **作者**：Xuejiao Wang, Bohao Zhang, Changbo Wang, Gaoqi He (华东师范大学)
- **方法**：Motion Feature Extractor (MFE) 显式建模对象间距/速度/IoU/方向一致性 → Motion-guided Interaction Module (MIM) 融合运动与空间特征 → Action Semantic Matching (ASM) CLIP跨模态对齐 → 类别加权损失缓解长尾
- **关键结果**：PREDCLS With Constraint R@10=70.6% (超越TD2-Net 70.1%)；SGDET With Constraint mR@50=25.2% (+2.9% vs TD2-Net)；消融实验验证各模块均有正向贡献

### Added: DSFlash — Comprehensive Panoptic Scene Graph Generation in Realtime (arXiv 2026)

- **操作**：单篇入库（sub-agent, inbound 批量入库）
- **论文**：[DSFlash: Comprehensive Panoptic Scene Graph Generation in Realtime](domains/scene-graph/papers/dsflash-comprehensive-panoptic-scene-graph-generation-realtime.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2026-06-09-dsflash-comprehensive-panoptic-scene-graph-generation.pdf (9.3 MB)
- **提取**：raw/sources/2026-06-09-dsflash-comprehensive-panoptic-scene-graph-generation.txt (47,486 chars, 12 pages)
- **用户备注**：inbound 批量入库，全面全景场景图生成 DSFlash（arXiv 2026）
- **作者**：Julian Lorenz, Vladyslav Kovganko, Elias Kohout, Mrunmai Phatak, Daniel Kienzle, Rainer Lienhart (University of Augsburg)
- **方法**：EoMT 统一骨干 → 低分辨率分割掩码 → 门控双向关系预测（单次前传预测正反两方向）→ 动态 patch pruning（丢弃与 subject/object 无重叠的 token）→ ToMe-SD token merging
- **关键结果**：DSFlash-L mR@50=30.90 (超越 DSFormer 30.70), 50ms 延迟 (DSFormer 458ms, 快 9×); DSFlash-S* mR@50=25.05, Latency=18ms (56 FPS), 40M 参数; 单张 GTX 1080 上 <24h 训练
- **贡献**：首个低延迟 PSGG 模型，全面场景图（全实例全关系），资源效率极高

### Added: FReMuRe — Frequency-Guided Multi-Level Reasoning for SGG in Video (arXiv 2026)

- **操作**：单篇入库（sub-agent, inbound 批量入库）
- **论文**：[FReMuRe: Frequency-Guided Multi-Level Reasoning for Scene Graph Generation in Video](domains/scene-graph/papers/2026-06-09-fremure-frequency-guided-multi-level-reasoning-video-sgg.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2026-06-09-frequency-guided-multi-level-reasoning-sgg.pdf (1.9 MB)
- **提取**：raw/sources/2026-06-09-frequency-guided-multi-level-reasoning-sgg.txt (30,778 chars, 895 lines, 5 pages)
- **用户备注**：inbound 批量入库，频率引导多层次推理SGG（arXiv 2026）
- **作者**：Chenxing Li, Yiping Duan, Xiaoming Tao (清华大学)
- **方法**：频率门控（inverse-frequency weighting + learnable gate）→ DPEG 双分支谓词网络（高频/低频并行，门控融合）→ 全局分支 + 滑动窗口聚合 → Bayesian Head（MC 采样不确定性估计）/ GMM-Plus Head（K 分量高斯混合 + 方差正则）→ 解耦学习消除梯度冲突
- **关键结果**：PREDCLS mR@50=43.1 (超越 TEMPURA 40.9)；SGCLS R@50=46.6 / mR@50=30.6 (SOTA)；SGDET R@50=36.1 / mR@50=22.5 (SOTA)；消融验证解耦策略最关键（移除后 SGDET mR@50 从 22.5 跌至 17.3）
- **贡献**：从机制层面（梯度冲突解耦）系统解决视频 SGG 长尾问题，频率门控 + 双分支架构 + 专用分类头三者互补

### Added: VIZOR — Viewpoint-Invariant Zero-Shot Scene Graph Generation for 3D Scene Reasoning (arXiv 2026)

- **操作**：单篇入库（sub-agent, inbound 批量入库）
- **论文**：[VIZOR: Viewpoint-Invariant Zero-Shot Scene Graph Generation for 3D Scene Reasoning](domains/scene-graph/papers/vizor-viewpoint-invariant-zero-shot-3d-scene-graph-generation.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2026-arXiv-VIZOR-Viewpoint-Invariant-Zero-Shot-SGG.pdf
- **提取**：raw/sources/2026-arXiv-VIZOR-Viewpoint-Invariant-Zero-Shot-SGG.txt
- **用户备注**：inbound 批量入库，视角不变零样本SGG（arXiv 2026）
- **贡献**：首个零样本视角不变3D场景图生成，训练无关，基于物体前朝向定义关系
- **关键结果**：Replica SGG Node Precision 0.88（vs CG 0.71, +17%）；Replica 开放词汇物体定位 Overall 0.78（+22% vs CG-LLM 0.56），Complex-Spatial 0.67（+39%）；Nr3D 零样本 grounding Accuracy 52.81%（+4.81% vs VLM-Grounder 48.0%）；Front-View Precision 85.71%
- **作者**：Vivek Madhavaram, Vartika Sengar, Arkadipta De, Charu Sharma（IIIT Hyderabad + Fujitsu Research India）

### Added: AlignG — Learning Context-Conditioned Predicate Semantics via Prototype Feedback (ICML 2026)

- **操作**：单篇入库（sub-agent, inbound 批量入库）
- **论文**：[AlignG: Learning Context-Conditioned Predicate Semantics via Prototype Feedback](domains/scene-graph/papers/aligng-context-conditioned-predicate-semantics-prototype-feedback.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2026-06-09-context-conditioned-predicate-semantics-sgg.pdf (3.4 MB)
- **提取**：raw/sources/2026-06-09-context-conditioned-predicate-semantics-sgg.txt (54,939 chars, 1,934 lines)
- **用户备注**：inbound 批量入库，上下文条件谓词语义SGG（arXiv 2026）
- **作者**：NamGyu Jung, Chang Choi（Gachon University）
- **方法**：AlignG 通过两阶段原型反馈机制（交叉注意力上下文化原型 + GRU 更新关系嵌入）实现图像条件化的谓词语义适配，训练损失包含对齐损失和分散损失
- **关键结果**：
  - VG-150 SGDet: F@100 **23.8**（SOTA，+1.4），mR@100 **19.7**（+2.4 vs MCL†）；PredCls mR@100 **42.6**（+8.8 vs PE-Net）
  - GQA-200 SGDet: F@100 **19.5**（+2.7），mR@100 **15.5**（+10.8 vs PE-Net）；PredCls F@100 **43.4**
  - 仅 +7.05G FLOPs 和 -0.70 FPS 推理开销
  - 消融：GRU 更新优于 concat（SGDet F@100 +0.8），与重加权互补
  - 混淆分析：解决 PE-Net 42.6% 的 lying on vs laying on 混淆

### Added: REACT++ — Efficient Cross-Attention for Real-Time Scene Graph Generation (arXiv 2026)

- **操作**：单篇入库（sub-agent, inbound 批量入库）
- **论文**：[REACT++: Efficient Cross-Attention for Real-Time Scene Graph Generation](domains/scene-graph/papers/react-plus-plus-efficient-cross-attention-real-time-sgg.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2026-01-01-REACT-Efficient-Cross-Attention-Real-Time-SGG.pdf (2.5 MB, 26 pages)
- **提取**：raw/sources/2026-01-01-REACT-Efficient-Cross-Attention-Real-Time-SGG.txt (63,709 chars)
- **用户备注**：inbound 批量入库，高效交叉注意力实时SGG（arXiv 2026）
- **作者**：Maëlic Neau, Zoe Falomir (Umeå University)
- **贡献**：
  - DAMP：Detection-Anchored Multi-Scale Pooling，替代 ROI Align，延迟降 32%，F1@K +197%
  - AIFI：基于 RT-DETR 的轻量全局上下文模块
  - CARPE：Cross-Attention Rotary Prototype Embedding，非对称 subject/object cross-attention + Geometry RoPE
  - DCS：Dynamic Candidate Selection，推理时 proposals 从 100 降至 47，延迟 -25% 近乎无损
- **关键结果**：
  - PSG：F1@K **28.4**，mAP **53.1**，Lat **19.4ms** (DCS) / **25.9ms** (full)，Params **35.8M**
  - REACT++ vs REACT：mR@K +20%，latency -20%，params -17%
  - YOLO12m + REACT++：F1@K **30.0**（首个在 PSG 上突破 30 的模型）
  - IndoorVG：F1@K **23.9**（+4.8% vs REACT 22.8），mR@K **20.7**（+15% vs REACT 18.0）

### Added: SVG2 — Synthetic Visual Genome 2 (arXiv 2026)

- **操作**：单篇入库（sub-agent, inbound 批量入库）
- **论文**：[SVG2: Synthetic Visual Genome 2 — Extracting Large-Scale Spatio-Temporal Scene Graphs from Videos](domains/scene-graph/papers/2026-06-09-synthetic-visual-genome-2.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2026-06-09-synthetic-visual-genome-2.pdf (24 MB, 41 pages)
- **提取**：raw/sources/2026-06-09-synthetic-visual-genome-2.txt (96,472 chars)
- **用户备注**：inbound 批量入库，合成视觉基因组2大规模场景图提取（arXiv 2026）
- **作者**：Ziqi Gao, Jieyu Zhang, Wisdom Oluchi Ikezogwo et al. (AI2 / UW / Woven by Toyota / Microsoft)
- **贡献**：
  - SVG2：最大视频场景图数据集，636K 视频、6.6M 物体、52M 属性、6.7M 关系
  - 全自动三阶段管线：SAM2 + DAM + GPT-5，含在线-离线双阶段跟踪机制
  - TraSeR：轨迹对齐 VLM，双重重采样器（global + temporal window）
- **关键结果**：
  - 人工验证：Object 93.8%, Attribute 88.3%, Relation 85.4%
  - TraSeR 比开源基线关系检测 +15~20%，物体预测 +30~40%
  - TraSeR 物体预测优于 GPT-5 +13%（SVG2test Obj 79.0 vs 65.5）
  - VQA 使用 TraSeR 场景图提升 +4.6%（Perception Test）

### Added: ReLaGS — Relational Language Gaussian Splatting (arXiv 2026)

- **操作**：单篇入库（sub-agent, inbound 批量入库）
- **论文**：[ReLaGS: Relational Language Gaussian Splatting](domains/scene-graph/papers/2026-03-18-relags-relational-language-gaussian-splatting.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2026-03-18-ReLaGS-Relational-Language-Gaussian-Splatting.pdf (14 MB, 20 pages)
- **提取**：raw/sources/2026-03-18-ReLaGS-Relational-Language-Gaussian-Splatting.txt (87,413 chars, 2,459 lines)
- **用户备注**：inbound 批量入库，关系语言高斯泼溅（arXiv 2026）
- **作者**：Yaxu Xie, Abdalla Arafa, Alireza Javanmardi, Christen Millerdurai, Jia Cheng Hu, Shaoxiang Wang, Alain Pagani, Didier Stricker (DFKI / RPTU Kaiserslautern / Uni. Modena)
- **贡献**：
  - 首个统一层级语义与关系推理的无需训练 Gaussian 场框架
  - Maximum Weight Pruning (MWP)：去除低贡献高斯体，提升几何精度
  - Robust Outlier-Aware Feature Aggregation (ROFA)：Z-score 过滤异常 CLIP 特征
  - 两种场景图构建：LLM-SoM 提升（高质量稀疏）和 GNN 预测（高效可扩展）
- **关键结果**：
  - 3DSSG Predicate R@3 **0.79** / R@5 **0.87**（超越 RelationField +0.3/+0.5）
  - ScanNet++ 关系引导分割 mIoU **0.56**（vs RelationField 0.53，训练无关）
  - LeRF-OVS Mean IoU **64.4%**（训练无关方法最佳）
  - 构建 < 15 分钟，渲染 > 200 fps，内存效率 7.6× 优于 RelationField

### Added: Fixed External Cameras as Common Prior Maps for Active 3DSG (arXiv 2026)

- **操作**：单篇入库（sub-agent, inbound 批量入库）
- **论文**：[Fixed External Cameras as Common Prior Maps for Active 3D Scene Graph Generation](domains/scene-graph/papers/fixed-external-cameras-common-prior-maps-active-3dsg.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2026-05-18-fixed-external-cameras-common-prior-maps-active-3dsg.pdf (1.1 MB)
- **提取**：raw/sources/2026-05-18-fixed-external-cameras-common-prior-maps-active-3dsg.txt (24,842 chars, 626 lines)
- **用户备注**：inbound 批量入库，自动驾驶场景图（arXiv 2026）
- **作者**：Giorgia Modi, Davide Buoso, Giuseppe Averta, Daniele De Martini (Oxford / PoliTo)
- **贡献**：
  - RGB-only 3DSG 管线（MapAnything 替代深度传感器）
  - 固定外部摄像头作为 Common Prior Maps (CPMs)
  - 确定性几何规则场景图边生成（替代 ConceptGraphs LLM 关系查询）
  - 主动语义探索（ASP）与 CPM 初始化结合
- **关键结果**：
  - 单外部相机提升初始 Recall **+79%**（0.15→0.26），节点数 **+74%**（23→40）
  - RGB-only 管线 F1 **0.500** vs ConceptGraphs full-depth 的 0.499（Replica 7 场景）
  - 3 个外部相机作为独立 CPM：公寓 Recall **0.301**，家具房间 Recall **0.555**（ReplicaCAD 90 场景）

### Added: Modernising RL Navigation for ESSG with Scene Graphs (arXiv 2026)

- **操作**：单篇入库（sub-agent, inbound 批量入库）
- **论文**：[Modernising RL Navigation for ESSG with Scene Graphs](domains/scene-graph/papers/2026-06-09-modernising-rl-navigation-essg.md)
- **证据等级**：full-paper
- **领域**：scene-graph
- **来源**：raw/sources/2026-06-09-modernising-rl-navigation-scene-graphs.pdf (1.9 MB)
- **提取**：raw/sources/2026-06-09-modernising-rl-navigation-scene-graphs.txt (73,413 chars)
- **用户备注**：inbound 批量入库，基于场景图 RL 导航（arXiv 2026）
- **作者**：Roman Küble, Marco Hüller, Mrunmai Phatak, Rainer Lienhart, Jörg Hähner (University of Augsburg)
- **关键结果**：
  - PPO+SH16 较 REINFORCE+SH16+IL Node Recall 提升 **21%**（0.48→0.58）
  - PPO+MH504+D+CL Node Recall **0.93**（最高），Move Success Rate 0.58，Episodic Return 1.11
  - 因子化多头发 MH504 在相同分辨率下优于单头 SH504（Node Recall 0.93 vs 0.92，Move Success Rate 0.56 vs 0.42）
  - 深度输入在紧凑 PPO 中提升安全性（Move Success Rate 0.71→0.77），在高分辨率 MH 中边际影响极小
- **贡献**：系统性地对比了 RL 算法（REINFORCE vs PPO）、动作空间参数化（SH vs MH，16 vs 504 动作）和辅助监督（深度 + CL）对 Embodied SGG 中导航组件的影响

### Added: Knowledge-Embedded Routing Network (KERN) for Scene Graph Generation (CVPR 2019)

- **操作**：单篇入库（sub-agent）
- **论文**：[Knowledge-Embedded Routing Network for Scene Graph Generation](domains/scene-graph/papers/2019-CVPR-knowledge-embedded-routing-network-sgg.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2019-CVPR-knowledge-embedded-routing-network-sgg.pdf (720 KB)
- **提取**：raw/sources/2019-CVPR-knowledge-embedded-routing-network-sgg.txt (42,569 chars, 1,526 lines)
- **用户备注**：CVPR 2019，420+ 引用。通过知识路由网络将常识知识（如 WordNet）嵌入 SGG。经典方法之一。
- **作者**：Tianshui Chen, Weihao Yu, Riquan Chen, Liang Lin (Sun Yat-Sen University / DarkMatter AI Research)
- **贡献**：
  - 首次显式将统计知识（物体对-关系共现）编码为结构化知识图，通过 GGNN 传播嵌入 SGG
  - 提出 mR@K（mean Recall@K）作为更公平的长尾 SGG 评估指标（已成为社区标准）
  - 在 Visual Genome 上显著改善长尾关系预测：SGCls mR@50 **19.8%** (vs SMN 15.4%, +28.6%)，mR@100 **26.2%** (vs SMN 20.6%, +27.2%)
  - FREQ baseline 竞争力分析验证了统计共现的强正则化作用

### Added: 3D Scene Graph: A Structure for Unified Semantics, 3D Space, and Camera (ICCV 2019)

- **操作**：单篇入库（sub-agent）
- **论文**：[3D Scene Graph: A Structure for Unified Semantics, 3D Space, and Camera](domains/scene-graph/papers/3d-scene-graph-unified-semantics-3d-space-camera.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2019-10-01-3d-scene-graph-unified-semantics-3d-space-camera.pdf (6.98 MB)
- **提取**：raw/sources/2019-10-01-3d-scene-graph-unified-semantics-3d-space-camera.txt (47,157 chars, 10 pages)
- **用户备注**：3D 场景图的开创性论文。定义了 3D 场景图的概念（对象、房间层、相机层三层结构）。在 3D 领域影响力极大。
- **作者**：Iro Armeni, Zhi-Yang He, JunYoung Gwak, Amir R. Zamir, Martin Fischer, Jitendra Malik, Silvio Savarese (Stanford / UC Berkeley)
- **贡献**：
  - 首次将 Scene Graph 范式扩展到 3D 空间，定义四层图结构（Building→Room→Object→Camera）
  - 提出 Framing + Multi-View Consistency 鲁棒化机制，实现半自动 3D 场景图构建
  - 在 Gibson 数据库上，2D AP 从 0.079 提升至 0.485（+6.1×），3D AP 从 0.222 提升至 0.409（+1.84×）

### Added: MovieGraphs: Towards Understanding Human-Centric Situations from Videos (CVPR 2018)

- **操作**：单篇入库
- **论文**：[MovieGraphs: Towards Understanding Human-Centric Situations from Videos](domains/scene-graph/papers/moviegraphs-towards-understanding-human-centric-situations-from-videos.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2018-CVPR-MovieGraphs-Towards-Understanding-Human-Centric-Situations-from-Videos.pdf (12 MB, 23 pages)
- **提取**：raw/sources/2018-CVPR-MovieGraphs-Towards-Understanding-Human-Centric-Situations-from-Videos.txt (77,278 chars)
- **用户备注**：CVPR 2018。视频场景图的数据集+方法，经典电影场景图数据。
- **作者**：Paul Vicol, Makarand Tapaswi, Lluís Castrejón, Sanja Fidler (University of Toronto / Vector Institute / MILA)
- **贡献**：
  - 提出 MovieGraphs 数据集：51 部电影 7637 片段，图结构标注角色属性/关系/交互/主题/原因，附带时间戳和 face track 关联
  - 定义三个情境理解任务：图查询视频检索、交互排序、原因预测
  - 图→描述检索 R@1 62.1%，图+视频+对话融合检索 R@1 40.4%，med-R 3
  - 开源数据集成为后续 Video SGG 研究的基础基准
- **Updated pages**：
  - `wiki/domains/scene-graph/papers/moviegraphs-towards-understanding-human-centric-situations-from-videos.md`（新建）
  - `wiki/index.md`（添加条目）
- **Open loops**：Person ID 仍是瓶颈（43.7%准确率）；原因预测缺乏自动评估指标

### Added: Linguistic Structures as Weak Supervision for Visual Scene Graph Generation (CVPR 2021)

- **操作**：单篇入库（sub-agent）
- **论文**：[Linguistic Structures as Weak Supervision for Visual Scene Graph Generation](domains/scene-graph/papers/linguistic-structures-weak-supervision-visual-scene-graph-generation.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2021-CVPR-linguistic-structures-as-weak-supervision-for-visual-scene-graph-generation.pdf (3.4 MB)
- **提取**：raw/sources/2021-CVPR-linguistic-structures-as-weak-supervision-for-visual-scene-graph-generation.txt (55,837 chars, 1,461 lines)
- **用户备注**：CVPR 2021。利用语言结构做弱监督的 SGG 方法，经典弱监督 SGG 工作。
- **作者**：Keren Ye, Adriana Kovashka (University of Pittsburgh)
- **贡献**：
  - 首次系统利用 caption 语言结构（文本图）作为 SGG 弱监督信号
  - 提出 Phrasal Context（GNN 编码短语上下文）、Iterative Grounding Refinement（WSOD 迭代精炼）、Sequential Context（RNN 序列模式后处理）三组件
  - 在 VG-GT-Graph 设置下 R@50 **4.92**，超越 VSPNet 59%；仅使用 Caption 监督（COCO-Cap-Graph）R@50 **1.95**（Zareian 划分）
  - 弱监督方法在 Xu et al. 划分 R@50 **7.30** 超越全监督 IMP（3.44）和 MotifNet（6.90）
- **Updated pages**：
  - `wiki/domains/scene-graph/papers/linguistic-structures-weak-supervision-visual-scene-graph-generation.md`（新建）
  - `wiki/index.md`（添加条目）
- **Open loops**：Caption 关系分布与场景图标注分布的系统性偏移仍未解决；弱监督 SGG 与强全监督方法仍有明显差距

---

## 2026-06-10

### ingest: T-CAR — Zero-Shot Scene Graph Generation via Triplet Calibration and Reduction (TOMM 2023)

- **操作**：单篇入库（sub-agent）
- **论文**：[T-CAR: Zero-Shot Scene Graph Generation via Triplet Calibration and Reduction](domains/scene-graph/papers/2023-09-07-T-CAR-zero-shot-scene-graph-generation-triplet-calibration-reduction.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2023-09-07-T-CAR-zero-shot-scene-graph-generation-triplet-calibration-reduction.pdf (1.57 MB)
- **提取**：raw/sources/2023-09-07-T-CAR-zero-shot-scene-graph-generation-triplet-calibration-reduction.txt (76,967 chars)
- **用户备注**：零样本场景图生成的 triplet 校准方法
- **作者**：Jiankai Li, Yunhong Wang, Weixin Li (Beihang University / Shanghai AI Lab)
- **贡献**：
  - 提出 Triplet Calibration Loss (TCL) 在 triplet 粒度上校准 seen/unseen triplets
  - 提出 Unseen Space Reduction Loss (USRL) 将 unseen 空间缩减 85%
  - 提出 Contextual Encoding Network (CEN) 显式编码相对空间关系
  - 在 VG150 上 PredCls/SGCls/SGDet zR@100 分别达 34.9/10.6/6.0，超过 SOTA
- **入库文件**：
  - `raw/sources/2023-09-07-T-CAR-zero-shot-scene-graph-generation-triplet-calibration-reduction.pdf`
  - `raw/sources/2023-09-07-T-CAR-zero-shot-scene-graph-generation-triplet-calibration-reduction.txt`
  - `wiki/domains/scene-graph/papers/2023-09-07-T-CAR-zero-shot-scene-graph-generation-triplet-calibration-reduction.md`（新建）
  - `wiki/index.md`（添加条目）

### ingest: Not All Relations are Equal (CVPR 2022)

- **论文**：Not All Relations are Equal: Mining Informative Labels for Scene Graph Generation
- **作者**：Arushi Goel, Basura Fernando, Frank Keller, Hakan Bilen（爱丁堡大学 / A*STAR）
- **贡献**：
  - 首次提出 SGG 中标签信息量（label informativeness）概念，区分显式/隐式关系
  - 提出模型无关的交替式标签插补框架，为显式关系样本补全缺失隐式标签
  - 使用 Manifold Mixup 防止确认偏差
  - 在 Visual Genome 上大幅提升 mR@K（VCTree-TDE PredCls mR@20: 16.3→22.2）
- **入库文件**：
  - `raw/sources/2022-06-20-not-all-relations-are-equal-mining-informative-labels-for-sgg.pdf`（arXiv 下载）
  - `raw/sources/2022-06-20-not-all-relations-are-equal-mining-informative-labels-for-sgg.txt`（全文提取）
  - `wiki/domains/scene-graph/papers/2022-06-20-mining-informative-labels-for-sgg.md`（新建）
  - `wiki/index.md`（添加条目，计数值 70→71）

## 2026-06-10 — Ingest: Unconditional Scene Graph Generation (ICCV 2021)

- **任务**：论文入库，用户指定的无条件场景图生成论文
- **原始来源**：arXiv PDF (2108.05884)，全文 6.1 MB
- **处理流程**：Capture → Extract (47K 字符, 1449 行) → Create paper page → Update index → Update log
- **入库文件**：
  - `raw/sources/2021-08-12-unconditional-scene-graph-generation.pdf`（原始 PDF）
  - `raw/sources/2021-08-12-unconditional-scene-graph-generation.txt`（全文提取）
  - `wiki/domains/scene-graph/papers/2021-08-12-unconditional-scene-graph-generation.md`（新建论文页，full-paper）
  - `wiki/index.md`（添加条目）

### Ingested: Weakly Supervised Visual Semantic Parsing (VSPNet) — CVPR 2020

- **操作**：单篇入库（sub-agent）
- **论文**：[Weakly Supervised Visual Semantic Parsing (VSPNet)](domains/scene-graph/papers/2020-06-16-weakly-supervised-visual-semantic-parsing.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2020-06-16-weakly-supervised-visual-semantic-parsing.pdf (1.28 MB)
- **提取**：raw/sources/2020-06-16-weakly-supervised-visual-semantic-parsing.txt (47,475 chars)
- **标签**：scene-graph-generation, weakly-supervised, CVPR-2020
- **用户备注**：CVPR 2020。弱监督视觉语义解析。
- **作者**：Alireza Zareian, Svebor Karaman, Shih-Fu Chang (Columbia University)
- **贡献**：
  - 提出 Visual Semantic Parsing (VSP) 形式化，将谓词建模为节点而非边，实现 sub-quadratic 推理
  - 提出 VSPNET，基于动态注意力双向消息传递框架联合推断节点和边
  - 提出首个基于图对齐的弱监督学习框架，无需边界框标注
  - 弱监督 SGGEN R@100 3.5% vs PPR-FCN 1.9%（+1.6），PHRDET R@100 20.4% vs 3.2%（+17.2，6 倍提升）
  - 全监督下推理时间 0.11s/图像，比所有基线快数倍（快于 Graph R-CNN 7.5x）
  - 支持高阶交互（如 3+ 实体连接同一谓词），传统 SGG 无法实现
- **Updated pages**：
  - `wiki/domains/scene-graph/papers/2020-06-16-weakly-supervised-visual-semantic-parsing.md`（新建）
  - `wiki/index.md`（添加条目）

### Ingested: Improving Scene Graph Generation with Relation Words' Debiasing in Vision-Language Models — arXiv 2024

- **操作**：单篇入库（sub-agent）
- **论文**：[Improving Scene Graph Generation with Relation Words' Debiasing in Vision-Language Models](domains/scene-graph/papers/2024-03-01-improving-sgg-with-relation-words-debiasing-vlm.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2024-03-01-improving-scene-graph-generation-with-relation-words-debiasing.pdf (2.2 MB, arXiv 2403.16184)
- **提取**：raw/sources/2024-03-01-improving-scene-graph-generation-with-relation-words-debiasing.txt (59,283 chars, 1,933 lines)
- **用户备注**：CLIP-based 的关系词去偏方法。
- **作者**：Yuxuan Wang, Xiaoyuan Liu (Nanyang Technological University)
- **贡献**：
  - 提出 Lagrange-Multiplier Estimation (LM Estimation)，通过约束优化估计预训练 VLM 中不可获得的谓词分布 πₚₜ
  - 提出 certainty-aware ensemble，动态集成去偏后的零样本 VLM 与 SGG 模型以缓解 underrepresentation
  - Training-free 方法，Plug-and-play 兼容任意 SGG 模型
  - ViLT ft + Ours PredCls mR@100 46.5（+2.0），PENET + Ours R@100 71.1（所有方法最优）
  - Unseen triplet 上的集成增益（+4.01~+5.09）远超 all triplet（+1.83~+3.29）
- **Updated pages**：
  - `wiki/domains/scene-graph/papers/2024-03-01-improving-sgg-with-relation-words-debiasing-vlm.md`（新建）
  - `wiki/index.md`（添加条目）

### Ingested: Visual Distant Supervision for Scene Graph Generation — ICCV 2021

- **操作**：单篇入库（sub-agent）
- **论文**：[Visual Distant Supervision for Scene Graph Generation](domains/scene-graph/papers/visual-distant-supervision-scene-graph-generation.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2021-10-01-visual-distant-supervision-scene-graph-generation.pdf (940 KB)
- **提取**：raw/sources/2021-10-01-visual-distant-supervision-scene-graph-generation.txt (53,865 chars)
- **标签**：scene-graph-generation, weakly-supervised, ICCV-2021
- **用户备注**：ICCV 2021。视觉远距离监督的 SGG。
- **作者**：Yuan Yao, Ao Zhang, Xu Han, Mengdi Li, Cornelius Weber, Zhiyuan Liu, Stefan Wermter, Maosong Sun (Tsinghua University / University of Hamburg)
- **贡献**：
  - 提出视觉远距离监督（Visual Distant Supervision），将常识知识库与图像对齐自动生成大规模标注数据
  - 从 Conceptual Captions 构建含 187 万关系三元组的常识知识库
  - 提出 EM 迭代去噪框架，结合 CLIP 外部语义信号和内部模型预测
  - DS 模型 PredCls R@50 53.40% 超越弱监督 44.96% 和半监督 49.68% 基线（无需任何人工标注）
  - SS 模型 PredCls R@50 76.28% 超越全监督 Motif 67.93%（+8.3），mR@50 60.20% vs 52.65%（+7.8）
  - 远程监督覆盖 VG 70.3% 人工标注关系，且有效缓解长尾问题
- **Updated pages**：
  - `wiki/domains/scene-graph/papers/visual-distant-supervision-scene-graph-generation.md`（新建）
  - `wiki/index.md`（添加条目，计数 73→74）

### Ingested: Generative Compositional Augmentations for Scene Graph Prediction — ICCV 2021

- **操作**：单篇入库（sub-agent，直接分析）
- **论文**：[Generative Compositional Augmentations for Scene Graph Prediction](domains/scene-graph/papers/2021-ICCV-generative-compositional-augmentations-for-scene-graph-prediction.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2020-07-11-generative-compositional-augmentations-for-scene-graph-prediction.pdf (65.7 MB, arXiv → ICCV 2021)
- **提取**：raw/sources/2020-07-11-generative-compositional-augmentations-for-scene-graph-prediction.txt (84,142 chars)
- **分类标签**：scene-graph-generation, augmentation, generative-adversarial-network, compositional-generalization, ICCV-2021
- **用户备注**：ICCV 2021。生成式组合增强的场景图预测。
- **作者**：Boris Knyazev, Harm de Vries, Cătălina Cangea, Graham W. Taylor, Aaron Courville, Eugene Belilovsky
- **贡献**：
  - 提出基于条件 GAN 的场景图组合增强方法，通过结构化扰动（RAND/NEIGH/GRAPHN）生成稀有三元组并用 GAN 合成对应视觉特征
  - GRAPHN（graph-structured semantic neighbors）是核心贡献，通过图结构和数据集统计采样合理的稀有组合
  - 在 Visual Genome 上获得 marginal but consistent 的零样本提升（ZS PredCls 9.27→9.89，ZS SGCls 28.14→29.18）
  - 与 NM++ 结合零样本提升更显著（SGCls zsR@50 1.8→2.5）
- **Updated pages**：
  - `wiki/domains/scene-graph/papers/2021-ICCV-generative-compositional-augmentations-for-scene-graph-prediction.md`（新建）
  - `wiki/index.md`（添加条目，计数 74→75）

### Ingested: Context-Aware Scene Graph Generation With Seq2Seq Transformers — ICCV 2021

- **操作**：单篇入库（sub-agent，直接分析，max depth reached）
- **论文**：[Context-Aware Scene Graph Generation With Seq2Seq Transformers](domains/scene-graph/papers/context-aware-sgg-seq2seq-transformers.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2021-10-01-context-aware-scene-graph-generation-with-seq2seq-transformers.pdf (1.88 MB, OpenAccess)
- **提取**：raw/sources/2021-10-01-context-aware-scene-graph-generation-with-seq2seq-transformers.txt (54,518 chars)
- **分类标签**：scene-graph-generation, transformer, seq2seq, ICCV-2021
- **用户备注**：ICCV 2021。Seq2Seq Transformers 的场景图生成。
- **作者**：Yichao Lu, Himanshu Rai, Jason Chang, Boris Knyazev, Guangwei Yu, Shashank Shekhar, Graham W. Taylor, Maksims Volkovs (Layer 6 AI / U of Guelph / Vector Institute)
- **贡献**：
  - 将 SGG 建模为 Seq2Seq 自回归预测，Transformer encoder-decoder 架构
  - Self-critical policy gradient + Monte Carlo search RL 直接优化 recall/mRecall
  - VG SGDET R@50: 30.9, R@100: 34.4；mRecall@100: PRDCLS 30.5, SGCLS 16.2, SGDET 12.1
- **Updated pages**：
  - `wiki/domains/scene-graph/papers/context-aware-sgg-seq2seq-transformers.md`（新建）
  - `wiki/index.md`（添加条目，计数 73→74）

### Ingested: GPS-Net: Graph Property Sensing Network for Scene Graph Generation — CVPR 2020 (Oral)

- **操作**：单篇入库（sub-agent，全文精读）
- **论文**：[GPS-Net](domains/scene-graph/papers/2020-03-29-GPS-Net-graph-property-sensing-scene-graph-generation.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2020-03-29-GPS-Net-graph-property-sensing-scene-graph-generation.pdf (3.77 MB)
- **提取**：raw/sources/2020-03-29-GPS-Net-graph-property-sensing-scene-graph-generation.txt (52,655 chars, 2003 lines)
- **分类标签**：scene-graph-generation, message-passing, direction-aware, node-priority, long-tail, CVPR-2020
- **用户备注**：CVPR 2020。图属性感知网络的场景图生成。
- **作者**：Xin Lin, Changxing Ding, Jinquan Zeng, Dacheng Tao
- **贡献**：
  - 提出 DMP（Direction-aware Message Passing），利用三元线性模型（Tucker 分解）编码边方向信息，生成节点特定上下文
  - 提出 NPS-loss（Node Priority Sensitive Loss），通过非线性映射函数 γ(θi)=min(2, -(1-θi)^µ log(θi)) 调整 focal loss 聚焦参数
  - 提出 ARM（Adaptive Reasoning Module），通过 log-softmax 频率软化 + 视觉自适应偏置缓解长尾分布
  - VG: SGCLS R@100 42.3 (+5.5 vs RelDN), mR@100 SGCLS 22.8 (+3.6 vs KERN)
  - OI: scorewtd 47.03 (+2.4 vs RelDN), wears APrel +24.5%
  - VRD: Relation R@100 33.8 (+2.5 vs RelDN†)
- **Updated pages**：
  - `wiki/domains/scene-graph/papers/2020-03-29-GPS-Net-graph-property-sensing-scene-graph-generation.md`（新建）
  - `wiki/index.md`（添加条目，计数 75→76）

### Ingested: Fine-Grained Scene Graph Generation with Data Transfer (IETrans) — ECCV 2022

- **操作**：单篇入库（sub-agent）
- **论文**：[Fine-Grained Scene Graph Generation with Data Transfer (IETrans)](domains/scene-graph/papers/2022-03-22-fine-grained-sgg-data-transfer.md)
- **领域**：scene-graph
- **证据等级**：full-paper
- **来源**：raw/sources/2022-03-22-fine-grained-sgg-data-transfer.pdf (3.4 MB, arXiv:2203.11654)
- **提取**：raw/sources/2022-03-22-fine-grained-sgg-data-transfer.txt (69,347 chars, 26 pages)
- **用户备注**：ECCV 2022。细粒度场景图生成的迁移方法。
- **作者**：Ao Zhang, Yuan Yao, Qianyu Chen, Wei Ji, Zhiyuan Liu, Maosong Sun, Tat-Seng Chua (NUS / Tsinghua)
- **代码**：https://github.com/waxnkw/IETrans-SGG.pytorch
- **贡献**：
  - 提出 IETrans（Internal and External Data Transfer）框架，通过自动增强数据集缓解 SGG 的长尾分布和语义歧义问题
  - Internal Transfer：根据混淆矩阵+吸引因子发现通用→信息型谓词对，triplet-level 数据迁移
  - External Transfer：重新标注 NA 样本（漏标假阴性）为有效关系三元组
  - 在 VG-50 上 Motif 模型 mR@100 翻倍（16.2→33.6），F@K 提升 9+ 点
  - 在所有 4 种基线模型（Motif、VCTree、GPS-Net、Transformer）上均显著提升
  - 提出 VG-1800 大规模基准（1,807 谓词类），IETrans 正确预测 467 类 vs 基线 < 70 类
  - VG-1800 上 Top-10 F-Acc 31.12（3× 第二高基线 RelMix 9.78）
  - Plug-and-play，可加 reweighting 策略进一步改善
- **Updated pages**：
  - `wiki/domains/scene-graph/papers/2022-03-22-fine-grained-sgg-data-transfer.md`（新建）
  - `wiki/index.md`（添加条目）
  - `wiki/log.md`（本条）

## [2026-06-10] ingest | CogTree: Cognition Tree Loss for Unbiased Scene Graph Generation
- **Raw source**: `raw/sources/2021-08-01-cogtree-cognition-tree-loss.pdf`
- **Updated pages**:
  - `wiki/domains/scene-graph/papers/2021-08-01-cogtree-cognition-tree-loss.md`（新建）
  - `wiki/index.md`（添加条目）
  - `wiki/log.md`（本条）
- **Evidence level**: full-paper
- **Key takeaways**: 提出 CogTree 损失，从偏置 SGG 模型预测中自动构建认知层次树，通过粗到细分类实现无偏 SGG。VCTree+CogTree PredCls mR@50 27.6（+12.7pp），SG-Transformer+CogTree PredCls mR@50 28.4（+9.2pp）。模型无关，即插即用于 MOTIFS/VCTree/SG-Transformer。
- **Open loops**: 树结构静态固定；仅 VG 评估；概念硬分配，软分配或可提升

## [2026-06-10] ingest | SceneLLM: Implicit Language Reasoning in LLM for Dynamic Scene Graph Generation
- **Raw source**: `raw/sources/2024-12-SceneLLM-Implicit-Language-Reasoning-LLM-Dynamic-SGG.pdf`
- **Extracted text**: `raw/sources/2024-12-SceneLLM-Implicit-Language-Reasoning-LLM-Dynamic-SGG.txt` (52,253 chars, 1,461 lines)
- **Updated pages**:
  - `wiki/domains/scene-graph/papers/2024-12-SceneLLM-Implicit-Language-Reasoning-LLM-Dynamic-SGG.md`（新建/补全）
  - `wiki/index.md`（添加条目）
  - `wiki/log.md`（本条）
- **Evidence level**: full-paper
- **Key takeaways**: 首次将 LLM（LLaMA-13B, LoRA 微调）作为隐式推理引擎用于动态场景图生成。通过 V2L 映射（VQ-VAE 离散化 + SIA 空间聚合 + OT 时序对齐）将视频信号转换为类语言 token 序列，输入 LLM 进行隐式推理。在 Action Genome 上 PREDCLS R@50 77.8（+1.7 vs OED），SGCLS R@50 55.0（+1.3 vs DIFFVSGG），SGDET R@50 49.5（+0.6 vs OED）。消融实验证实离散化和 LoRA 微调分别贡献 +13 和 +6.6 R@50。
- **Open loops**: LLM 计算开销大；仅 AG 单数据集验证；代码未公开；长视频扩展性未讨论；隐式 vs 显式推理对比未做

## [2026-06-10] ingest | Ensemble Predicate Decoding for Unbiased Scene Graph Generation
- **Raw source**: `raw/sources/2024-08-25-ensemble-predicate-decoding-unbiased-sgg.pdf`
- **Updated**:
  - `wiki/domains/scene-graph/papers/2024-08-25-ensemble-predicate-decoding-unbiased-sgg.md`
  - `wiki/index.md`（添加条目，更新计数 76→77）
  - `wiki/log.md`（本条）
- **Evidence level**: full-paper
- **Key takeaways**: 提出 EPD（Ensemble Predicate Decoding），通过三个解码器集成（主解码器在全量数据、AD1 在 body+tail 子集、AD2 仅在 tail 子集）来提升 SGG 低频谓词判别能力。在 VG PredCls 上 Motifs+EPD 达 mR@50 36.3（vs Motifs 14.9，+21.4），Mean 46.3（vs Motifs+GCL 40.4，+5.9）。核心消融：多解码器结构 vs 单解码器 re-weighting 带来 mR@50 +7.8 和 Mean +6.9 的增益。最优分区：N1=5, N2=10, N3=35（类别数）。
- **Open loops**: 仅 VG 单数据集验证；在 VCTree baseline 上 Mean 低于 Inf 和 DKBL（使用了 triplet prior）；超参数空间大（α, β, γ, λ_md, λ_ad1, λ_ad2, 分区基数）；解码器数固定 3 个未探讨自适应变体；代码未公开

## [2026-06-10] ingest | ELEGANT: Less is More — Zero-Shot Local Scene Graph Generation via Foundation Models
- **Raw source**: `raw/sources/2023-10-02-less-is-more-zero-shot-local-scene-graph-generation-via-foundation-models.pdf`
- **Extracted text**: `raw/sources/2023-10-02-less-is-more-zero-shot-local-scene-graph-generation-via-foundation-models.txt` (52,873 chars, 16 pages)
- **Updated pages**:
  - `wiki/domains/scene-graph/papers/2023-10-02-elegant-zero-shot-local-scene-graph-generation-via-foundation-models.md`（新建）
  - `wiki/index.md`（添加条目）
  - `wiki/log.md`（本条）
- **Evidence level**: full-paper
- **Key takeaways**: 提出 Local Scene Graph Generation 新任务及 ELEGANT 零样本框架（GroundedSAM + GPT-3.5-Turbo + BLIP2 OPT 6.7B），通过观察-推理-验证三级流水线和 Co-Calibration 策略实现无需标注的局部场景图生成。在 Visual Genome 闭集评估中，R@10 30.27 (vs VisualDS 27.72, +9.2%)；对 RECODE 的 R@20 35.18 vs 10.60。VQA 下游任务中局部场景图（58.3%）优于全局场景图（54.2%）和基线（50.4%）。开放词汇评估指标 ECLIPSE 发现 1,813 种关系类别（~25x 闭集方法）。
- **Open loops**: 多模型级联推理耗时；仅基于 IoU>0 配对；未利用分割掩码；ECLIPSE 依赖 CLIP 模型；GPT-3.5 依赖商业 API

## [2026-06-10] ingest | Adaptive Self-training Framework for Fine-Grained Scene Graph Generation (ST-SGG)
- **Raw source**: `raw/sources/2024-01-adaptive-self-training-scene-graph-generation.pdf` (arXiv:2401.09786v5, ICLR 2024)
- **Extracted text**: `raw/sources/2024-01-adaptive-self-training-scene-graph-generation.txt` (98,960 chars, 25 pages)
- **Updated pages**:
  - `wiki/domains/scene-graph/papers/2024-01-adaptive-self-training-framework-fine-grained-sgg.md`（新建）
  - `wiki/index.md`（添加条目）
  - `wiki/log.md`（本条）
- **Evidence level**: full-paper
- **Key takeaways**: 首次将自训练引入 SGG。提出 ST-SGG 框架，核心为 CATM（EMA 自适应阈值 + 类别特定动量），有效利用 VG 中 95.5% 的未标注三元组。Motif+I-Trans+ST-SGG 在 VG PredCls 上 mR@100 达 35.1%（+15.9 vs 基线）。GSL 进一步提升 MPNN 模型（BGNN+ST-SGG+GSL PredCls mR@100 36.2%）。OI-V6 上 Motif+Resamp.+ST-SGG mR@50 42.7（+2.1）。代码公开。
- **Open loops**: 未探索外部无标注数据源；GSL 仅限于 MPNN 模型；CA TM 超参数需调优；β>1.0 时性能下降

## [2026-06-10] ingest | EchoScene: Indoor Scene Generation via Information Echo over Scene Graph Diffusion
- **Raw source**: `raw/sources/2024-05-02-echoscene-indoor-scene-generation-via-information-echo-scene-graph-diffusion.pdf`
- **Extracted text**: `raw/sources/2024-05-02-echoscene-indoor-scene-generation-via-information-echo-scene-graph-diffusion.txt` (81,278 chars, 1,920 lines)
- **Updated pages**:
  - `wiki/domains/scene-graph/papers/echoscene-indoor-scene-generation-via-information-echo-scene-graph-diffusion.md`（新建）
  - `wiki/index.md`（添加条目）
  - `wiki/log.md`（本条）
- **Evidence level**: full-paper
- **Key takeaways**: 提出 EchoScene，基于信息回响机制的双分支（布局+形状）场景图扩散模型。每个节点分配独立去噪进程并通过信息交换单元在每步进行全局状态交换。SG-FRONT 数据集上，EchoScene 全面超越 CommonScenes：Bedroom FID 改善 15%（57.68→48.85），KID 改善 73%（6.59→1.77）。物体间一致性 CD 全面大幅下降（衣柜 0.61→0.14、餐桌 11.75→3.02）。提出扩散逆工作流操控策略，无需 GAN 判别器。消融证实 shape echoes 贡献 FID +7.14 的改善。
- **Open loops**: 仅 SG-FRONT 单数据集验证；symmetrical 关系（0.9%）导致约束准确率下降；无纹理场景需外接纹理生成器；多节点计算开销线性增长

## 2026-06-10 — Ingest: RealGraph (ICCV 2023)

- **Raw source**: `raw/sources/2023-10-RealGraph-4D-Context-Graph.pdf` (2.1 MB, 11 pages)
- **Extracted text**: `raw/sources/2023-10-RealGraph-4D-Context-Graph.txt` (53,452 chars)
- **Updated pages**:
  - `wiki/domains/scene-graph/papers/2023-10-RealGraph-4D-context-graph-generation.md`（新建，full-paper）
  - `wiki/index.md`（两个 scene-graph 节分别添加条目）
  - `wiki/log.md`（本条）
- **Evidence level**: full-paper
- **Domain**: scene-graph
- **Key takeaways**: 提出首个 4D Context Graph Generation (CGG) 任务及 RealGraph 多视角视频数据集（13 场景，8-15 相机，2.4M 帧，37 物体类，18 关系类）。基线 MCGNet 为多阶段 pipeline（3D Det→BiLSTM Rel→Kalman Tracking）。3D Det mAP 38.29，CGG mCGR@100 仅 25.0，体现多阶段误差累积的挑战。Feature Fusion 在 Det 贡献 +3.3 mAP，Double Association 降低 51% ID switches。充分相机覆盖对 CGG 至关重要（full views mAP 38.29 vs half 23.33）。
- **Open loops**: 多阶段 pipeline 缺乏联合优化；关系预测未利用时间一致性约束；数据集仅 13 场景，规模有限；关系类别局限物理接触类

## [2026-06-10] ingest | INOVA: Interaction-Aware Open Vocabulary Scene Graph Generation
- **Raw source**: `raw/sources/2025-02-06-interaction-aware-open-vocabulary-sgg.pdf` (3.7 MB, 10 pages)
- **Extracted text**: `raw/sources/2025-02-06-interaction-aware-open-vocabulary-sgg.txt` (48,872 chars, 1,391 lines)
- **Updated pages**:
  - `wiki/domains/scene-graph/papers/2025-02-06-inova-interaction-aware-open-vocabulary-sgg.md`（新建）
  - `wiki/index.md`（添加条目，scene-graph 计数 78→79）
  - `wiki/log.md`（本条）
- **Evidence level**: full-paper
- **Domain**: scene-graph
- **Key takeaways**: 提出 INOVA 交互感知 OVSGG 框架。三个组件：ITG（双向交互提示引导预训练 grounding）、IQS（交互引导查询选择减少 SFT 二部图匹配错误）、RRD（关系级知识蒸馏防止灾难性遗忘）。VG 上 OvR-SGG Novel Rel R@100 21.70（Swin-T）/24.66（Swin-B），超越 OvSGTR 4.94-5.51。OvD+R-SGG Novel Rel R@100 19.46（Swin-T）/21.73（Swin-B），超越 OvSGTR 3.51-8.28。消融证实三个组件均有贡献但存在 diminishing returns。
- **Open loops**: 三个组件集成有 diminishing returns；仅验证 SGDET 协议；依赖 Grounding DINO backbone；GQA 结果只在 appendix；交互提示对 VLM 架构的依赖程度未探讨

## [2026-06-10] ingest | GPT4SGG: Synthesizing Scene Graphs from Holistic and Region-specific Narratives
- **Raw source**: `raw/sources/2023-12-07-GPT4SGG-Synthesizing-Scene-Graphs-from-Holistic-and-Region-specific-Narratives.pdf` (7.3 MB)
- **Extracted text**: `raw/sources/2023-12-07-GPT4SGG-Synthesizing-Scene-Graphs-from-Holistic-and-Region-specific-Narratives.txt` (57,345 chars, 1,462 lines)
- **Updated pages**:
  - `wiki/domains/scene-graph/papers/gpt4sgg-synthesizing-scene-graphs-from-holistic-and-region-specific-narratives.md`（新建，260 行）
  - `wiki/index.md`（添加条目）
  - `wiki/log.md`（本条）
- **Evidence level**: full-paper
- **Domain**: scene-graph
- **Key takeaways**:
  - 提出分治框架 GPT4SGG：将复杂场景分解为 region-specific narratives + holistic narrative，用 LLM 推理合成场景图
  - 有效解决语言监督 SGG 的 grounding 歧义性、caption 稀疏偏置和解析器不准确三大难题
  - OvSGTR + VG@GPT（46k 图）R@50=25.03, mR@100=8.22，接近全监督的 42.40/8.98
  - Instruction-tuned Llama 2-13B 达到与 GPT-4 相当的合成能力（12.06% vs 12.09% recall）
- **Open loops**: 未使用多模态 LLM（GPT-4V）；仅用 recall 评估 scene graph 质量不全面；检测器性能不足时 pipeline 显著退化（AR=56.8%→recall 3.11%）

## [2026-06-10] ingest | APT: Towards Universal Scene Graph Generation via Plug-in Adaptive Prompt Tuning
- **Raw source**: `raw/sources/2026-02-26-APT-adaptive-prompt-tuning-universal-SGG.pdf` (1.2 MB, 20 pages)
- **Extracted text**: `raw/sources/2026-02-26-APT-adaptive-prompt-tuning-universal-SGG.txt` (74,468 chars, 2,493 lines)
- **Updated pages**:
  - `wiki/domains/scene-graph/papers/APT-adaptive-prompt-tuning-universal-SGG.md`（新建，290 行）
  - `wiki/index.md`（添加条目，scene-graph 计数 79→80）
  - `wiki/log.md`（本条）
- **Evidence level**: full-paper
- **Domain**: scene-graph
- **Venue**: ICLR 2026（用户标记 CVPR 2024 有误，已更正）
- **Key takeaways**: 提出 APT（Adaptive Prompt Tuning），一种通用轻量级插件模块，通过可学习 prompt 将冻结语义特征转化为上下文感知表示，可无缝集成到两阶段/一阶段/OV SGG 框架。VG PredCls 上 LLM4SGG+APT mR@100 42.2 vs 39.1 baseline (+3.1)；EGTR+APT mR@100 40.1 vs 38.2 baseline (+1.9)。OV Novel 上 SDSGG+APT mR@50 26.7 vs 25.2 (+1.5)。<0.5M 额外参数（<1.5% overhead），训练时间减少 7.8%-25%。R-Prompt 是核心（消融中 mR@100 +2.6），D-Prompt 贡献有限。CGP 中 BPS 贡献最大 OV 提升（Novel mR@50 +3.8）。信息瓶颈分析显示 APT 表示更紧凑（PCA@90% 23 vs 26）。
- **Open loops**: OI-V6 和 GQA 全部结果仅在 appendix；D-Prompt 在部分设置中轻微负效果；β>1.0 时性能下降；类级别 prompt 在大类别空间中存储开销未分析；信息瓶颈解释依赖 proxy 指标
