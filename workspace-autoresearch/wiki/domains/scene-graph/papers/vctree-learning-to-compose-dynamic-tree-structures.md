---
title: "Learning to Compose Dynamic Tree Structures for Visual Contexts"
authors: "Kaihua Tang, Hanwang Zhang, Baoyuan Wu, Wenhan Luo, Wei Liu"
venue: "CVPR 2019"
year: 2019
doi: "10.1109/CVPR.2019.00673"
arxiv: "1906.07106"
code: "https://github.com/KaihuaTang/VCTree"
url: "https://openaccess.thecvf.com/content_CVPR_2019/papers/Tang_Learning_to_Compose_Dynamic_Tree_Structures_for_Visual_Contexts_CVPR_2019_paper.pdf"
tags: [scene-graph-generation, tree-structure, visual-context, CVPR-2019, foundational]
domain: scene-graph
evidence_level: full-paper
task: Scene Graph Generation (SGG), Visual Question Answering (VQA)
backbone: Faster-RCNN + VGG
---
<!-- 论文原始信息：https://openaccess.thecvf.com/content_CVPR_2019/papers/Tang_Learning_to_Compose_Dynamic_Tree_Structures_for_Visual_Contexts_CVPR_2019_paper.pdf -->

## 摘要

提出 VCTREE（Visual Context Tree），一种动态二叉树结构用于编码图像中物体间的视觉上下文。核心思想：物体间的关系天然具有层级性（如"衣服"和"裤子"通常同属"人"）和平行性，链式结构和全连接图都不能有效刻画这种结构。VCTREE 通过可学习的得分矩阵构造每张图像独有的动态二叉最大生成树，利用双向 TreeLSTM 编码上下文，再解码到具体下游任务。采用混合学习策略：端任务监督学习 + 树结构强化学习（自评判 REINFORCE）。

## 核心贡献

1. **动态树结构**：提出 VCTREE，从得分矩阵构造二叉最大生成树，结构因图像和任务而异，比固定链/全连接图更灵活
2. **双向 TreeLSTM**：在二叉树上执行双向（自底向上 + 自顶向下）TreeLSTM 消息传递，同时捕捉层级关系和并行关系
3. **混合学习策略**：树结构选择用 REINFORCE（自评判基线），下游端任务用标准监督学习
4. **双任务验证**：在 SGG（Visual Genome）和 VQA（VQA2.0）上验证有效性

## 方法框架

![VCTree Framework](../../../raw/assets/vctree-framework.png)

### 四个步骤

1. **特征提取**：Faster-RCNN 检测 proposals，提取 RoIAlign 视觉特征 $v_i \in \mathbb{R}^{2048}$ 和空间特征 $b_i \in \mathbb{R}^8$
2. **VCTREE 构建**：学习得分矩阵 $S \in \mathbb{R}^{n \times n}$ 表示物体对之间的 task-dependent 有效性，通过最大生成树（MST）算法构造二叉最大生成树，再转为左孩子右兄弟（LCRS）二叉表示
3. **上下文编码**：双向 TreeLSTM（Bi-TreeLSTM）在二叉树上编码视觉上下文
4. **任务解码**：根据具体任务（SGG / VQA）解码上下文

### 关键设计

- **得分函数**：$S_{ij} = f(x_i, x_j) + g(x_i, x_j)$，其中 $f$ 学习物体间固有相关性（用预训练分类器），$g$ 是任务特定的可学习偏置
- **左孩子右兄弟（LCRS）表示**：将多叉树（n-ary tree）转为等价二叉树，左分支（红色）表示层级关系，右分支（蓝色）表示平行关系
- **Bi-TreeLSTM**：两个 pass——bottom-up（叶子→根）和 top-down（根→叶子），每个节点聚合子节点/父节点信息更新隐藏状态
- **混合学习**：REINFORCE 以结构奖励 $r = A(VCTREE) - A(Chain)$ 训练得分矩阵，其中 $A$ 是下游任务验证指标

## 实验结果

### Scene Graph Generation (Visual Genome)

数据集：VG 经典划分（top-150 object, top-50 predicate，70%/30% train/test，5000 val）

| 协议 | 模型 | R@20 | R@50 | R@100 | mR@100 |
|------|------|------|------|-------|--------|
| **SGGen** | VCTREE-HL | **22.0** | **27.9** | **31.3** | **8.0** |
| SGGen | VCTREE-SL | 21.7 | 27.7 | 31.1 | - |
| SGGen | MOTIFS⋄ | 21.4 | 27.2 | 30.3 | 6.6 |
| SGGen | FREQ⋄ | 20.1 | 26.2 | 30.1 | 7.1 |
| SGGen | IMP⋄ | 14.6 | 20.7 | 24.5 | - |
| **SGCls** | VCTREE-HL | **35.2** | **38.1** | **38.8** | **10.8** |
| SGCls | MOTIFS⋄ | 32.9 | 35.8 | 36.5 | 8.2 |
| **PredCls** | VCTREE-HL | **60.1** | **66.4** | **68.1** | **19.4** |
| PredCls | MOTIFS⋄ | 58.5 | 65.2 | 67.1 | 15.3 |

*⋄ 表示使用相同 Faster-RCNN 检测器。VCTREE-HL 为混合学习（hybrid learning），VCTREE-SL 为纯监督学习。SGGen=Scene Graph Generation, SGCls=Scene Graph Classification, PredCls=Predicate Classification。*

**消融分析**：对比 Chain / Overlap / Multi-Branch 三种树形结构变体，VCTREE 的二叉动态树全面优于链式结构（Chain R@20 21.2 → VCTREE-HL 22.0 for SGGen）。

### Visual Question Answering (VQA2.0)

| 数据集 | 模型 | Yes/No | Number | Other | All |
|--------|------|--------|--------|-------|-----|
| **test-dev** | **VCTREE-HL** | **84.28** | **47.78** | **59.11** | **68.19** |
| test-dev | Graph | 83.53 | 47.09 | 58.6 | 67.56 |
| test-dev | Chain | 82.74 | 47.31 | 58.93 | 67.42 |
| test-dev | Count [59] | 83.14 | 51.62 | 58.97 | 68.09 |
| test-dev | DA-NTN [3] | 84.29 | 47.14 | 57.92 | 67.56 |
| **test-standard** | **VCTREE-HL** | **84.55** | **47.36** | **59.34** | **68.49** |
| test-standard | Count [59] | 83.56 | 51.39 | 59.11 | 68.41 |

VCTREE-HL 在 VQA2.0 test-dev 达到 **68.19%** 总体准确率，test-standard 达到 **68.49%**，超过 DA-NTN、Count 等强 baseline。

## 分析

- **动态 vs 固定结构**：VCTREE 动态树显著优于 Chain 和全连接 Graph，验证了"树的动态性"的重要性
- **混合学习的必要性**：VCTREE-HL（混合学习）一致优于 VCTREE-SL（纯监督），证明 REINFORCE 优化的树结构更有效
- **类别平衡**：mR@K 指标上 VCTREE 显著优于 MOTIFS（mR@100 8.0 vs 6.6 for SGGen），说明树结构有助于缓解长尾 predicate 偏差
- **可解释性**：统计左右分支展示了树结构学习到的层级/平行关系模式，如 "street" 节点的左分支（层级）主要是 Car、Man、Tree；右分支（平行）主要是 Sidewalk、Street、Sign

## 讨论

- 计算成本：MST 构造和 Bi-TreeLSTM 比链式 LSTM 开销更大，但显著低于全连接 CRF-RNN
- 局限性：树结构仍为有向无环结构，无法处理环状关系（如"A 在 B 上面"同时"B 在 A 下面"这类矛盾关系）
- 未来方向：作者建议扩展到动态森林（dynamic forest）结构

## 引用

```bibtex
@inproceedings{tang2019vctree,
  title={Learning to Compose Dynamic Tree Structures for Visual Contexts},
  author={Tang, Kaihua and Zhang, Hanwang and Wu, Baoyuan and Luo, Wenhan and Liu, Wei},
  booktitle={Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
  year={2019}
}
```
