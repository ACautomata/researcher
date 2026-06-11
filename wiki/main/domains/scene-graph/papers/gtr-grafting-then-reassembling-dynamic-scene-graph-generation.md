---
title: "GTR: A Grafting-Then-Reassembling Framework for Dynamic Scene Graph Generation"
type: paper
domain: scene-graph
status: active
created: 2026-06-09
updated: 2026-06-09
tags:
  - dynamic-scene-graph
  - spatio-temporal
  - two-stage
  - action-genome
source_pages: []
raw_sources:
  - ../../../sources/scene-graph/2023-08-gtr-grafting-then-reassembling-dynamic-sgg.txt
  - ../../../sources/scene-graph/2023-08-gtr-grafting-then-reassembling-dynamic-sgg.pdf
related_pages: []
paper:
  title: "GTR: A Grafting-Then-Reassembling Framework for Dynamic Scene Graph Generation"
  authors:
    - Jiafeng Liang
    - Yuxin Wang
    - Zekun Wang
    - Ming Liu
    - Ruiji Fu
    - Zhongyuan Wang
    - Bing Qin
  year: 2023
  venue: IJCAI 2023 (Proceedings of the 32nd International Joint Conference on Artificial Intelligence)
  arxiv: null
  doi: null
  code: null
  project: null
classification:
  label: dynamic-scene-graph-generation
  task:
    - Dynamic Scene Graph Generation
    - Video Scene Graph Generation
    - Spatio-temporal Relationship Detection
  method_family: Two-stage Decoupling
  modality: Video
  datasets:
    - Action Genome (AG)
  metrics:
    - Recall@K (K=10, 20, 50)
evidence_level: full-paper
---

## Citation

Jiafeng Liang, Yuxin Wang, Zekun Wang, Ming Liu, Ruiji Fu, Zhongyuan Wang, Bing Qin. "GTR: A Grafting-Then-Reassembling Framework for Dynamic Scene Graph Generation." *Proceedings of the Thirty-Second International Joint Conference on Artificial Intelligence (IJCAI-23)*, pp. 1177–1185, 2023.

## One-Sentence Contribution

GTR 提出两阶段解耦框架，通过"嫁接"静态场景图生成模型生成帧内关系 + 时序依赖模型（TDM）显式重组为动态场景图，解决了动态场景图中时空上下文信息纠缠的问题，仅用60%视频数据即可超越SOTA。

## Problem Setting

**动态场景图生成**任务：给定视频 $V = \{F_1, F_2, ..., F_t\}$，目标是解析视频内容为一组场景图 $G_{vid} = \{G^{vid}_1, G^{vid}_2, ..., G^{vid}_t\}$，其中每帧的场景图 $G^{vid}_t = \{B_t, E_t, R_t\}$ 包含边界框、实体和关系谓词。

**现有方法的困境**：先前工作（STTran、AP-Net）使用单阶段Transformer隐式建模时空交互，导致两个问题：（1）空间和时间上下文信息纠缠无法分开提取；（2）需要大量视频训练数据，标注成本高。

**GTR 的出发点**：显式解耦——先用静态SGG模型提取帧内关系，再基于时序依赖将静态关系重组成动态场景图。利用视频中连续关系常按顺序出现（如 holding→drinking from）的正向归纳偏置来纠正单帧关系预测错误。

## Method

GTR 包含两个阶段：**嫁接阶段（Grafting Stage）** 和 **重组阶段（Reassembling Stage）**。

### 嫁接阶段（Grafting Stage）

1. 将预训练的静态SGG模型（RelTR）作为初始化，将视频每一帧视为独立图像进行微调
2. 微调后对每帧生成 top-k 候选静态关系谓词
3. 通过这种方式，将图像预训练模型从图像任务扩展到视频任务，利用其广泛预训练知识

### 重组阶段（Reassembling Stage）

核心组件是**时序依赖模型（Temporal Dependency Model, TDM）**，包含两个子模块：

**时序注意力模块（Temporal Attention Module）**：
- 对帧间相同实体对的跨帧依赖关系建模
- 设计**掩码策略（Mask Strategy）**：仅允许相同实体对在不同帧之间计算注意力，不同实体对的注意力分数被掩码掉
- 公式：$S^{frm}_p = \text{softmax}(Q^{frm}(K^{frm})^T / \sqrt{d_k})$，经掩码后得到 $H^{frm}_p$

**上下文注意力模块（Context Attention Module）**：
- 基于时序依赖，将静态关系谓词重新组装为动态场景图
- 将当前帧实体对作为目标（target），所有帧的静态关系谓词作为候选（candidate）
- 将匹配表示根据关系类型分解为三种掩码分支：注意力关系（attention）、空间关系（spatial）、接触关系（contacting）

**噪声过滤器（Noise Filter, NFT）**：
- 计算实体对在不同帧的视觉特征余弦相似度
- 相似度超过阈值（设为0.9）时保留候选关系谓词，否则过滤
- 提升静态关系谓词的可用性

### 训练损失

对于每帧 $F_t$，优化目标包括实体分类和关系谓词分类的交叉熵损失：
$$\hat{\theta} = \arg\min_{\theta} \sum_{p_n=1}^{n_p} \sum_{m=1}^{n_r} L_{match}(r^*_{p_n,m}, r_\theta(p_n,m)) + \sum_{l=1}^{n_o} L_{match}(o^*_l, o_\theta(l))$$

## Experiments

### 数据集
- **Action Genome (AG)**：17M 人类-物体关系实例，35 个物体类别，25 个关系谓词类别
- 关系分为三种类型：attention relationships、spatial relationships、contact relationships
- 视频中定期选择帧进行标注

### Baseline 方法
VRD、Motif Freq、MSDN、VCTREE、RelDN、GPS-Net、STTran、AP-Net（共8个对比方法）

### 评估协议
- 三种评测模式：**Predicate Classification (PREDcls)**（给定真值框和实体类别）、**Scene Graph Classification (SGcls)**（给定真值框）、**Scene Graph Detection (SGdet)**（从图像开始）
- 指标：Recall@K (K=10, 20, 50)
- IoU 阈值 0.5

### 实现细节
- **Backbone**：Faster R-CNN + ResNet-101
- **视觉特征维度**：512；语义特征：300
- **MLP**：3层全连接网络，隐层维度512
- **嫁接阶段**：基于RelTR，微调20 epochs，batch size 8，分类器学习率不变，其他层学习率×0.9
- **重组阶段**：SGD优化器，15 epochs，batch size 1，初始lr=1e-5，5 epoch后降至5e-6，10 epoch后降至1e-6
- **NFT阈值**：0.9
- **训练数据量**：仅使用60%视频数据

## Results

### 主要结果（Table 1）

| 方法 | PREDcls R@10 | PREDcls R@20 | PREDcls R@50 | SGcls R@10 | SGcls R@20 | SGcls R@50 | SGdet R@10 | SGdet R@20 | SGdet R@50 | Mean |
|------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| VRD | 51.7 | 54.7 | 54.7 | 32.4 | 33.3 | 33.3 | 19.2 | 24.5 | 26.0 | 36.6 |
| Motif Freq | 62.4 | 65.1 | 65.1 | 40.8 | 41.9 | 41.9 | 23.7 | 31.4 | 33.3 | 45.1 |
| MSDN | 65.5 | 68.5 | 68.5 | 43.9 | 45.1 | 45.1 | 24.1 | 32.4 | 34.5 | 47.5 |
| VCTREE | 66.0 | 69.3 | 69.3 | 44.1 | 45.3 | 45.3 | 24.4 | 32.6 | 34.7 | 46.9 |
| RelDN | 66.3 | 69.5 | 69.5 | 44.3 | 45.4 | 45.4 | 24.5 | 32.8 | 34.9 | 48.1 |
| GPS-Net | 66.8 | 69.9 | 69.9 | 45.3 | 46.5 | 46.5 | 24.7 | 33.1 | 35.1 | 48.6 |
| STTran | 68.6 | 71.8 | 71.8 | 46.4 | 47.5 | 47.5 | 25.2 | 34.1 | 37.0 | 50.0 |
| AP-Net | 69.4 | 73.8 | 73.8 | 47.2 | 48.9 | 48.9 | 26.3 | 36.1 | 38.3 | 51.4 |
| GTR (w/o RS) | 68.3 | 71.9 | 71.9 | 46.1 | 46.8 | 46.8 | 25.0 | 34.1 | 37.2 | 49.8 |
| **GTR（完整）** | **71.2** | **74.5** | **74.5** | **48.7** | **49.7** | **49.7** | **27.9** | **37.0** | **39.9** | **52.6** |

- GTR 在所有指标上超越之前SOTA（AP-Net），PREDcls R@10 提升 1.8%（69.4→71.2），SGcls R@10 提升 1.5%（47.2→48.7），SGdet R@10 提升 1.6%（26.3→27.9）
- 去除重组阶段后（GTR w/o RS），性能大幅下降（PREDcls R@10 从 71.2 降至 68.3），验证了时序建模是成功的关键

### 消融实验（Table 2，SGdet 指标）

| NFT | Mask Strategy | TDM | SGdet R@20 | SGdet R@50 |
|:---:|:---:|:---:|:---:|:---:|
| ✔ | ✔ | ✔ | **37.0** | **39.9** |
| ✘ | ✔ | ✔ | 36.1 | 39.0 |
| ✘ | ✘ | ✔ | 35.5 | 38.5 |
| ✘ | ✘ | ✘ | 34.1 | 37.2 |

- 去除NFT后性能下降（R@20: 37.0→36.1），验证噪声过滤器有效提升可用关系谓词质量
- 去除掩码策略后进一步下降（R@20: 36.1→35.5）
- 完全去除TDM后性能大幅下降（R@20: 35.5→34.1）

### 上下文/时序注意力消融（Table 3）

| Context Attention | Temporal Attention | SGdet R@20 | SGdet R@50 |
|:---:|:---:|:---:|:---:|
| ✔ | ✔ | **37.0** | **39.9** |
| ✘ | ✔ | 35.1 | 37.9 |
| ✔ | ✘ | 34.7 | 37.5 |

两个模块都至关重要，缺一不可。

### 连续动作区分能力（Table 4）
- 对比STTran，GTR在区分视觉相似连续动作（holding→drinking from、holding→eating）时精确度更高
- holding→drinking from: GTR 25/30 vs STTran 21/30
- holding→eating: GTR 25/30 vs STTran 25/30

### 视频数据量影响
- GTR使用50%数据即可在SGdet上超越之前SOTA（AP-Net使用100%数据）
- 使用60%数据时在所有三个评测模式上均超越SOTA
- 训练数据量低于40%时实体和关系类别无法完全覆盖

### 候选关系谓词数量影响
- 最佳候选数量 K=30
- K=40时由于捕获冗余关系谓词，框架性能下降

## Limitations

1. **仅使用 Action Genome 数据集评估**：论文未在其他视频场景图数据集（如VidVRD、ImageNet-VidVRD）上验证泛化能力
2. **静态SGG模型依赖**：嫁接阶段使用RelTR作为静态SGG模型，GTR的性能上限受限于所选静态SGG模型的能力
3. **候选关系谓词数需要手动调节**：最佳K=30需要实验确定，且K过大反而有害
4. **50%训练数据是下限**：40%以下数据无法覆盖所有实体/关系类别，限制了在极少量标注数据场景下的应用
5. **未与其他动态SGG方法在开放式设定下比较**：如开放词汇或零样本设定
6. **代码和预训练模型未开源**：论文报告中未提供代码链接，复现困难

## Reusable Claims

1. **时空解耦策略有效**：将静态关系生成和时序关系重组解耦为两个阶段，相比于单阶段隐式建模（STTran等）在数据效率和性能上更优。证据：GTR用60%数据超越AP-Net的100%数据结果。
2. **帧间掩码注意力**：仅允许相同实体对的跨帧注意力计算是一种有效获取细粒度时序依赖的手段，消融实验验证了其必要性（R@20下降0.6）。
3. **视频中的正向归纳偏置**：连续视觉关系常按顺序出现（如 holding→drinking from），可利用这一规律通过时序上下文纠正单帧误判。
4. **噪声过滤器有效**：基于视觉相似性的候选谓词过滤（阈值0.9）可以提升关系谓词的可利用率（R@20提升0.9）。

## Connections

- **STTran [Cong et al., 2021]**：GTR解决的核心问题（时空上下文纠缠）正是STTran的不足。STTran使用单阶段Transformer同时编码时空信息，GTR通过两阶段显式解耦。
- **AP-Net [Li et al., 2022]**：同样使用Transformer预训练范式提升动态SGG，但与GTR的显式解耦路线不同。GTR在AG数据集上超越AP-Net。
- **RelTR [Cong et al., 2022]**：GTR的嫁接阶段直接基于RelTR进行微调，利用其静态SGG能力。
- **TEMPURA（CVPR 2023）** 和 **PVSG（CVPR 2023）**：同为2023年动态视频场景图工作，但TEMPURA侧重视频中无偏场景图生成，PVSG侧重全景视频场景图生成，而GTR侧重时空上下文解耦。时间维度上三者可互补。
- **HiKER-SGG（CVPR 2024）**：同样借鉴层级知识增强，但侧重于开放场景鲁棒性而非时序解耦。

## Open Questions

1. GTR的两阶段设计在其他数据集（如VidVRD、PVSG、OpenPVSG）上是否同样有效？
2. 嫁接阶段的静态SGG模型替换为更强模型（如HiKER-SGG、DSGG）是否能进一步提升性能？
3. 掩码策略是否是最优的细粒度时序依赖建模方式？能否学习出软掩码而非硬掩码？
4. GTR的归纳偏置（连续关系按序出现）是否在所有视频领域都成立？例如在高动态、无规律交互场景下是否会失效？
5. 能否将GTR扩展到开放词汇或零样本设定？

## Provenance

- **Evidence level**: full-paper（基于完整PDF全文提取和分析）
- **Source**: ../../../sources/scene-graph/2023-08-gtr-grafting-then-reassembling-dynamic-sgg.txt（45474字符全文提取）
- **Venue verification**: 论文发表于 IJCAI 2023，pp. 1177–1185
- **Note**: 传入文件名标注为"Generative Compositional Augmentations for Scene Graph Generation"，但实际PDF内容为"GTR: A Grafting-Then-Reassembling Framework for Dynamic Scene Graph Generation"，系下载时文件名混淆
