---
title: "RA-SGG: Retrieval-Augmented Scene Graph Generation Framework via Multi-Prototype Learning"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - scene-graph-generation
  - long-tailed-distribution
  - semantic-ambiguity
  - multi-label-classification
  - retrieval-augmented
  - multi-prototype-learning
  - AAAI-2025
raw_sources:
  - ../../../raw/sources/2025-AAAI-RA-SGG-Relation-Alignment-for-Robust-Scene-Graph-Generation.pdf
  - ../../../raw/sources/2025-AAAI-RA-SGG-Relation-Alignment-for-Robust-Scene-Graph-Generation.txt
related_pages:
  - prototype-based-embedding-network-scene-graph-generation.md
  - compositional-feature-augmentation-for-unbiased-scene-graph-generation.md
  - fast-contextual-scene-graph-generation.md
evidence_level: full-paper
paper:
  title: "RA-SGG: Retrieval-Augmented Scene Graph Generation Framework via Multi-Prototype Learning"
  authors:
    - Kanghoon Yoon
    - Kibum Kim
    - Jaehyeong Jeon
    - Yeonjun In
    - Donghyun Kim
    - Chanyoung Park
  year: 2025
  venue: "The 39th AAAI Conference on Artificial Intelligence (AAAI-25)"
  arxiv: null
  doi: null
  code: null
  project: null
classification:
  label: "Retrieval-Augmented SGG via Multi-Prototype Learning"
  task:
    - Scene Graph Generation (SGG)
    - Predicate Classification (PredCls)
    - Scene Graph Classification (SGCls)
    - Scene Graph Detection (SGDet)
  method_family:
    - Multi-label classification with partial annotation
    - Retrieval-augmented label augmentation
    - Memory bank construction and nearest neighbor retrieval
    - Multi-prototype learning
    - Inverse propensity score sampling (IPSS)
  modality:
    - Image
  learning_paradigm: supervised
  long_tail: addressed (via multi-label discovery + IPSS unbiased augmentation)
summary: >
  RA-SGG 将场景图生成（SGG）任务重新定义为带部分标注的多标签分类问题，
  通过检索增强的方式发现训练数据中的潜在细粒度谓词，将单标签标注扩充为多标签。
  核心思路：构建内存银行（memory bank）存储关系嵌入，对每个查询关系检索视觉语义最相似的 K 个近邻，
  从而发现与原始标签语义相近的细粒度谓词作为多标签；引入多原型学习（multi-prototype learning）
  使模型同时捕捉多种语义模式；使用逆倾向得分采样（IPSS）进行无偏数据增强。
  在 Visual Genome 和 GQA 两个基准数据集上，RA-SGG 在 F@K 指标上分别提升高达 3.6% 和 5.9%。
---
## 动机与问题

SGG 面临两个根本挑战：
1. **长尾分布（Long-tailed Problem）**：谓词类别呈严重倾斜分布，头类谓词（如 "on"）大量出现，尾类细粒度谓词（如 "walking in"）极少出现，导致模型偏向粗粒度预测。
2. **语义歧义（Semantic Ambiguity）**：谓词类别间语义边界模糊（如 "on"、"walking on"、"walking in"），模型需捕捉细微视觉线索才能区分，但尾类样本不足加剧了学习难度。

已有工作如重采样/重加权（Li et al. 2021; Lyu et al. 2022）及数据增强（IE-Trans, CFA）存在两个问题：
- 增强细粒度时牺牲了对通用谓词的识别能力（trade-off）
- 仍基于单标签分类框架，迫使不同谓词相互竞争，忽略了自然语言中多个谓词可描述同一关系的本质

## 方法

### 框架总览

RA-SGG 以 PE-Net（Zheng et al. 2023, CVPR 2023）为 backbone，包含三个关键阶段：

### 1. 内存银行构建（Memory Bank Construction）

- 基于 backbone 提取的关系嵌入（relation embedding），为每个标注的 triplet（subject, predicate, object）构建 key-value 对
- key：关系嵌入；value：主语-谓语-宾语类别的 one-hot 组合
- 存储策略：每个唯一 tripet 至多存储 100 个实例，最终内存银行约占训练集 8%

### 2. 可靠多标签实例选择（Reliable Multi-labeled Instance Selection）

- 对查询 triplet 的关系嵌入，在内存银行中检索 K 个近邻
- 若检索到的邻域中有与原始标签不同的谓语类别且占比超过阈值 τ=0.3，则认为该 triplet 包含潜在多标签
- 将该 triplet 标记为 multi-labeled，并引入邻域中高频出现的其他谓语作为补充标签

### 3. 无偏数据增强（IPSS）与多原型学习

- **IPSS**：进行无偏数据增强时使用逆倾向得分采样，基于频率估计每个谓语的出现概率，对低频谓语赋予更高的采样权重
- **多原型学习**：为每个谓语维护多个原型向量（prototypes），每个原型捕捉谓语的不同视觉子模式
  - 模型不仅预测谓语类别，还预测实例属于谓语下的哪个原型
  - loss 包含分类 loss 和原型对齐 loss
- **总损失**：L_final = L_pred + λ * L_proto + L_IPSS

## 实验

### 数据集

| 数据集 | 物体类 | 谓语类 | 用途 |
|--------|--------|--------|------|
| Visual Genome (VG) | 150 | 50 | 标准基准 |
| GQA | 200 | 100+ |大规模基准 |

### 评估协议

- **PredCls**: 给定真实框和类别，预测关系谓词
- **SGCls**: 给定真实框，预测物体类别和关系谓词
- **SGDet**: 从图像中检测物体并预测所有关系

### 评估指标

- **Recall@K (R@K)**: 前 K 个预测 triplet 中命中的比例
- **Mean Recall@K (mR@K)**: 每个谓词类别的平均召回率，用于长尾评估
- **F@K**: R@K 和 mR@K 的调和平均，综合平衡指标

### 主要结果 — Visual Genome (VG)

| 方法 | PredCls R@50/100 | PredCls mR@50/100 | PredCls F@50/100 |
|------|-----------------|-------------------|-----------------|
| VTransE (CVPR'17) | 55.7/57.9 | 14.0/15.0 | 22.4/23.8 |
| Motif (CVPR'18) | 65.3/66.8 | 16.4/17.1 | 26.2/27.2 |
| VCTree (ICCV'19) | 63.8/65.7 | 16.6/17.4 | 26.4/27.5 |
| PE-Net (CVPR'23) | 54.3/56.0 | 26.2/27.1 | 35.4/36.5 |
| **PE-Net + RA-SGG** | 48.3/50.1 | **35.4/36.8** | **40.9/42.4** |

| 方法 | SGCls R@50/100 | SGCls mR@50/100 | SGCls F@50/100 |
|------|----------------|-----------------|-----------------|
| PE-Net (CVPR'23) | 26.2/27.0 | 11.2/11.5 | 15.7/16.1 |
| **PE-Net + RA-SGG** | 19.9/20.8 | **16.4/17.2** | **18.0/18.8** |

| 方法 | SGDet R@50/100 | SGDet mR@50/100 | SGDet F@50/100 |
|------|----------------|-----------------|-----------------|
| PE-Net (CVPR'23) | 19.5/22.9 | 10.3/11.9 | 13.5/15.7 |
| **PE-Net + RA-SGG** | 16.3/19.0 | **12.9/15.0** | **14.4/16.8** |

**关键发现**：RA-SGG 在降低 R@K 的情况下显著提升 mR@K 和 F@K，说明多标签发现策略在不牺牲通用谓词理解的前提下有效提升了细粒度谓词识别能力。

### 主要结果 — GQA

| 任务 | 对比基线和指标 | 关键数据 |
|------|---------------|---------|
| PredCls | PE-Net vs RA-SGG F@K | 提升高达 **5.9%** |
| - | class-wise 对比 | RA-SGG 在绝大多数谓语类别上超过 PE-Net，尤其是细粒度谓词 |

### 消融研究

| 变体 | PredCls mR@50/100 | PredCls F@50/100 |
|------|-------------------|-----------------|
| Vanilla PE-Net | 31.5/33.8 | 42.4/45.0 |
| RA-SGG w/o select. | 33.4/36.4 | 44.0/47.0 |
| RA-SGG w/o IPSS | 32.9/35.1 | 43.6/46.0 |
| **RA-SGG** | **36.2/39.1** | **45.7/48.6** |

| 变体 | SGCls mR@50/100 | SGCls F@50/100 |
|------|-----------------|-----------------|
| Vanilla PE-Net | 17.8/18.9 | 24.5/25.8 |
| RA-SGG w/o select. | 19.6/20.9 | 26.0/27.3 |
| RA-SGG w/o IPSS | 18.6/19.8 | 25.1/26.3 |
| **RA-SGG** | **20.9/22.5** | **27.0/28.6** |

**消融结论**：
1. RA-SGG w/o select.（跳过可靠实例选择）仍优于 PE-Net，验证了检索增强方法的有效性
2. RA-SGG w/o IPSS（移除无偏采样）性能下降，说明 IPSS 对提升细粒度预测至关重要
3. RA-SGG 综合全部组件取得最佳性能

### 超参数分析

- **检索数 K**：K=20 时最优，且 K=1 时仍优于 PE-Net，表明即使仅利用最近邻也有效
- **内存银行大小**：约占训练集 8% 时性能最优，兼顾效率与效果

### 检索准确性

人工评估 100 个采样实例：**84.20%** 检索准确率。

## 分析

### 与相关方法的区别

- **与数据增强方法（IE-Trans/CFA）的区别**：这些方法将通用谓词重新标注为细粒度，牺牲了对通用谓词的理解；RA-SGG 通过多标签同时保留通用和细粒度谓词信息
- **与单标签分类的区别**：RA-SGG 将 SGG 重新定义为多标签分类，避免了谓词间的竞争性抑制

### 方法优势

1. **无 trade-off**：不牺牲通用谓词即可提升细粒度谓词识别
2. **可扩展性强**：内存银行仅占 8% 训练数据，检索高效
3. **框架无关**：可应用于多种 backbone，在本文中基于 PE-Net

### 局限性

- 依赖 backbone（PE-Net）的视觉编码质量
- 检索准确性依赖存储嵌入的质量
- 需要人工标注验证检索可靠性（84.20% 人工验证准确率）

## Claims

- **[C1]** 将 SGG 重新定义为多标签分类问题是根本性解决长尾和语义歧义的有效框架。
  - 来源：论文第 1 节、第 6 节
  - 证据等级：full-paper
- **[C2]** RA-SGG 在 VG 上 PredCls 的 F@100 达 42.4（vs PE-Net 36.5），提升 5.9 点（相对 16.2%）。
  - 来源：Table 1
  - 证据等级：full-paper
- **[C3]** IPSS 无偏采样对性能提升至关重要（消融实验中移除后 F@K 下降）。
  - 来源：Table 3 消融研究
  - 证据等级：full-paper
- **[C4]** 即使仅检索 K=1 个近邻，RA-SGG 仍优于 PE-Net，表明检索增强的有效性。
  - 来源：敏感性分析 Figure 4(a)
  - 证据等级：full-paper

## Open Questions

- **[Q1]** 如果使用更强 backbone（如 ViT 而非 Faster R-CNN），RA-SGG 的检索质量和最终性能是否会进一步提升？
- **[Q2]** 内存银行在更大规模数据集（如 Open Images）上的可扩展性如何？
- **[Q3]** 多原型数量如何自动确定？是否需要为不同谓语配置不同数量的原型？

## 关键图表

- **Figure 1**: RA-SGG 的标签增强示意图 —— 查询事例的邻域包含多种语义相近谓语
- **Figure 2**: RA-SGG 整体 pipeline —— 内存银行检索 → 可靠多标签选择 → 多原型学习
- **Figure 3**: GQA 上类级别比较 —— RA-SGG 在大多数谓语类别上优于 PE-Net
- **Figure 4**: 超参数敏感性分析 —— K 和内存银行大小对性能的影响
