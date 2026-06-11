---
title: "Scene Graph Generation from Objects, Phrases and Region Captions (MSDN)"
type: paper
domain: scene-graph
status: active
created: 2026-06-10
updated: 2026-06-10
tags: [scene-graph-generation, foundational, ICCV-2017, multi-task-learning, msdn, object-detection, region-captioning]
source_pages: []
raw_sources:
  - raw/sources/2017-ICCV-scene-graph-generation-from-objects-phrases-region-captions.txt
  - raw/sources/2017-ICCV-scene-graph-generation-from-objects-phrases-region-captions.pdf
paper:
  title: "Scene Graph Generation from Objects, Phrases and Region Captions"
  authors:
    - Yikang Li
    - Wanli Ouyang
    - Bolei Zhou
    - Kun Wang
    - Xiaogang Wang
  year: 2017
  venue: "ICCV 2017"
  arxiv: "1707.09700"
  code: "https://github.com/yikang-li/MSDN"
classification:
  label: "Multi-level Scene Description Network (MSDN)"
  task: [scene-graph-generation, object-detection, region-captioning]
  method_family: [multi-task-learning, message-passing, dynamic-graph]
  modality: image
  datasets: [Visual Genome]
  metrics: [Recall@K, mAP, Meteor]
evidence_level: full-paper
---

## Citation

> Y. Li, W. Ouyang, B. Zhou, K. Wang, X. Wang. "Scene Graph Generation from Objects, Phrases and Region Captions." ICCV 2017.

```
@inproceedings{li2017scene,
  title={Scene graph generation from objects, phrases and region captions},
  author={Li, Yikang and Ouyang, Wanli and Zhou, Bolei and Wang, Kun and Wang, Xiaogang},
  booktitle={Proceedings of the IEEE International Conference on Computer Vision (ICCV)},
  year={2017}
}
```

## One-Sentence Contribution

提出 Multi-level Scene Description Network (MSDN)，通过动态图构建和消息传递机制，联合学习对象检测、场景图生成和区域描述三个不同语义层次的任务，首次在 Visual Genome 上系统定义和评估 SGG 任务，为该领域的奠基性工作。

## Problem Setting

SGG 任务定义为：给定一张图像，检测其中的所有物体并预测每一对物体之间的二元关系（predicate），从而构建一个有向图（场景图）。该任务被分解为三个子任务（沿袭自 Xu et al. [40]）：

- **Predicate Recognition (PredCls)**：给定 ground truth 物体框，仅预测物体间的关系类别
- **Phrase Recognition (PhrCls)**：给定 ground truth 物体框，预测物体类别和关系类别
- **Scene Graph Generation (SGGen)**：同时进行物体检测和关系识别，是完整的 SGG 任务

MSDN 在此基础上联合了第三个任务——区域描述（Region Captioning），利用三种不同语义层次（对象级、短语级、区域描述级）的互补信息。

## Method

### 整体架构 (MSDN)

基于 Faster R-CNN 的 region-based 检测 pipeline，搭配 VGG-16 backbone。模型包含三个并行分支：

1. **对象分支 (Object Branch)**：对 proposal 进行对象分类和框回归
2. **短语分支 (Phrase Branch)**：对物体对的 predicate 进行分类
3. **区域描述分支 (Caption Branch)**：用 LSTM 语言模型生成自由形式的句子

四个核心模块：

### 1. Region Proposal（区域提议）
- **Object proposals**：通过 RPN 生成
- **Phrase proposals**：将 N 个 object proposals 全连接成 N(N-1) 对有向的物体对
- **Caption proposals**：通过另一个 RPN 生成（anchor 由 k-means 聚类 ground truth 框获得）

### 2. Dynamic Graph Construction（动态图构建）
图结构动态依赖于具体图像的 ROIs：
- **短语-对象连接**：自然的 subject-predicate-object 三元组结构，两条有向边
- **短语-区域描述连接**：基于空间关系，当区域描述框覆盖短语框超过 0.7 的阈值时添加无向边
- 区域描述和对象之间不直接连接，通过短语层次间接连接

### 3. Feature Refining（特征精炼）
采用 **Merge-and-Refine** 范式，通过门控函数对来自不同连接的节点特征进行加权融合：

- **对象节点精炼**：接收来自 subject-predicate 和 predicate-object 两类连接的短语特征，通过门控函数 $\sigma_{\langle o,p\rangle}$（128 个模板）加权平均后，经 FC 层做模态变换后再加回原对象特征
- **短语节点精炼**：接收来自 subject 对象、object 对象和连接的区域描述节点的特征
- **区域描述节点精炼**：接收来自连接的短语节点的特征
- 精炼过程可重复迭代（最优为 2 次迭代）

特征更新公式（对象为例）：
$$x^{(o)}_{i,t+1} = x^{(o)}_{i,t} + F^{(p\to s)}(\tilde{x}^{(p\to s)}_i) + F^{(p\to o)}(\tilde{x}^{(p\to o)}_i)$$

### 4. Scene Graph Generation
使用矩阵表示场景图：对角线元素 $(i,i)$ 表示第 i 个对象，非对角线元素 $(i,j)$ 表示对象 i 与 j 之间的 predicate。当物体被识别为非 background、关系被识别为非 irrelevant 时，在场景图中建立连接。

## Experiments

### Dataset
- **Visual Genome** 数据集
- 预处理后：95,998 张图像，top-150 对象类别，top-50 谓词类别
- 对象框短边 < 16px 的移除，区域描述短边 < 32px 的移除
- 词表：top-10,000 高频词
- **Split**：70,998 训练 / 25,000 测试

### Baselines
- **LP (Language Prior)** [Lu et al., ECCV 2016]：先检测物体，再使用视觉特征和词嵌入预测 predicate
- **ISGG (Iterative SGG)** [Xu et al., arXiv 2017]：使用基于 GRU 的迭代消息传递进行 SGG

### Training Setup
- **Backbone**：VGG-16，ImageNet 预训练
- **FC 层**：1024 神经元（从原 4096 缩减）
- **Optimizer**：SGD + gradient clipping（语言模型部分使用 Adam，无 weight decay）
- **Learning rate**：base 0.01，VGG 卷积层初始固定，第一次 decay 后按 0.1 倍学习率训练
- **Mini-batch**：每 batch 一张图；NMS 后保留最多 2000 个 box；采样 256 object proposals、128 caption proposals、512 phrase proposals（25% 正例）
- **NMS 阈值**：训练时 object 0.7、caption 0.75；测试时 object 0.35、caption 0.45
- **Loss**：交叉熵（分类）+ smooth L1（回归），三项等权重相加
- **迭代次数**：特征精炼默认 2 次迭代

### Metrics
- 主要指标：**Recall@K** (R@50, R@100)，用于 SGG 三个子任务
- 原因：SGG 的关系标注不完备，mAP 会错误惩罚正类缺失标注的预测
- Object Detection：mAP + Top-1 / Top-5 accuracy (with GT boxes)
- Region Captioning：AP [Johnson et al. Densecap] + Meteor

## Results

### 主结果（Table 2）

| Task | LP [31] | ISGG [40] | **MSDN (Ours)** |
|------|---------|-----------|-----------------|
| **PredCls** R@50 | 26.67 | 58.17 | **67.03** |
| **PredCls** R@100 | 33.32 | 62.74 | **71.01** |
| **PhrCls** R@50 | 10.11 | 18.77 | **24.34** |
| **PhrCls** R@100 | 12.64 | 20.23 | **26.50** |
| **SGGen** R@50 | 0.08 | 7.09 | **10.72** |
| **SGGen** R@100 | 0.14 | 9.91 | **14.22** |

- SGGen 上相比 ISGG 提升 3.63%~4.31%（对应 R@100 从 9.91→14.22)
- PredCls 上提升 8.86%~8.27%（R@50 从 58.17→67.03）
- PhrCls 上提升 5.57%~6.27%（R@50 从 18.77→24.34）

### 消融实验（Table 1）

| ID | 消息传递 | Caption分支 | Caption监督 | 迭代次数 | SGGen R@50 | SGGen R@100 |
|:--:|:--------:|:-----------:|:----------:|:--------:|:--------:|:---------:|
| 1 | ✗ | ✗ | ✗ | 0 | 2.39 | 3.82 |
| 2 | ✓ | ✗ | ✗ | 1 | 7.73 | 10.51 |
| 3 | ✓ | ✓ | ✗ | 1 | 8.20 | 11.35 |
| 4 | ✓ | ✓ | ✓ | 1 | 10.23 | 13.89 |
| **5** | ✓ | ✓ | ✓ | **2** | **10.72** | **14.22** |
| 6 | ✓ | ✓ | ✓ | 3 | 10.01 | 13.62 |

关键发现：
- **消息传递**带来最大提升：SGGen R@50 从 2.39→7.73（+5.34%），验证了跨层次特征精炼的有效性
- **Caption 监督**进一步贡献 2.03%~2.64% 提升（ID3→4），说明区域描述能提供额外的互补信息
- **2 次迭代最优**，3 次迭代会导致训练困难、性能下降 0.21%~0.27%

### Object Detection 结果（Table 3 上）
- Faster R-CNN：mAP 6.72%
- Baseline-3-bran.：mAP 6.70%
- **MSDN (Ours)**：**mAP 7.43%**（+0.71% over FRCNN）
- Top-1 Acc：53.57% → **61.12%**（+7.55% with GT boxes）

### Region Captioning 结果（Table 3 下）
- Baseline (Densecap-like)：AP 4.41%
- Baseline-3-bran.：AP 4.28%
- **MSDN (Ours)**：**AP 5.39%**（+0.98% over baseline）

## Limitations

1. **短语数量过大**：N 个对象产生 N(N-1) 个短语 proposal，导致计算开销大且正样本稀疏（仅采样 512 个/sample，25% 正例）
2. **VGG-16 backbone**已过时，性能受限于相对浅层的特征提取能力
3. **仅覆盖 top-50 predicates**，对长尾、细粒度关系处理不足
4. **区域描述和对象之间没有直接连接**，通过短语间接连接可能丢失信息
5. **区域描述覆盖阈值 0.7 为经验设定**，缺乏自适应机制
6. **3 次迭代退化**：更深层的消息传递反而导致训练不稳定

## Reusable Claims

- **跨语义层次联合学习有效**：对象级、短语级、区域描述级三个层次的互补信息可以互相提升（SGG +3.63~4.31%，检测 mAP +0.71%，描述 AP +0.98%）
- **动态图构建**优于固定图结构：图拓扑依赖于具体图像的内容，而非预先定义的全连接图
- **门控消息传递**：使用 128 个门控模板对来自不同来源的特征进行加权融合，比简单平均更有效
- **残差式特征更新**（$x_{t+1} = x_t + \Delta$）比 GRU 式（ISGG）更容易训练

## Connections

- **前驱工作**：Visual Relationship Detection with Language Priors (LP) [Lu et al., ECCV 2016]；Scene Graph Generation by Iterative Message Passing (ISGG) [Xu et al., arXiv 2017]
- **后续影响**：MSDN 定义的 SGG 子任务（PredCls / PhrCls / SGGen）和评估协议（Recall@K）成为该领域的标准评价框架
- **同任务方法**：与后续 VTransE、MotifNet、Graph R-CNN、RelTR 等方法构成 SGG 方法谱系
- **关联方法论文**：ViP-CNN [Li et al., CVPR 2017]（同一组作者的前序工作，使用视觉短语引导 CNN）

## Open Questions

- 如何在不枚举所有 N(N-1) 对短语的情况下高效进行 SGG？
- 区域描述信息对 SGG 的增益是否具有领域普适性，还是主要来自 Visual Genome 的特殊标注分布？
- 动态图构建的阈值（0.7）是否可以学习得到？
- 消息传递的迭代次数如何自适应确定？

## Provenance

- **PDF 来源**：arXiv (1707.09700)
- **提取文本**：raw/sources/2017-ICCV-scene-graph-generation-from-objects-phrases-region-captions.txt（45,398 chars，10 pages）
- **提取方法**：PyMuPDF (fitz) 全文提取
- **证据等级**：full-paper — 完整精读全文，方法细节（动态图构建、门控函数、特征精炼公式）、实验结果（Table 1-3 完整结果数字）均已提取
