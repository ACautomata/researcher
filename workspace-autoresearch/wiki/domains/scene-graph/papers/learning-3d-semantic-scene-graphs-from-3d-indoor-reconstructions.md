# Learning 3D Semantic Scene Graphs from 3D Indoor Reconstructions

- **标题（中译）**：从 3D 室内重建学习 3D 语义场景图
- **作者**：Johanna Wald\*, Helisa Dhamo\*, Nassir Navab, Federico Tombari (\* equal contribution)
- **机构**：Technische Universität München, Google
- **发表**：CVPR 2020 (Spotlight)
- **arXiv**：[2004.03967](https://arxiv.org/abs/2004.03967)
- **项目主页**：[https://3dssg.github.io/](https://3dssg.github.io/)
- **代码**：未开源（项目主页提供数据集）
- **数据集**：[3DSSG](https://3dssg.github.io/)（基于 3RScan）
- **标签**：`scene-graph-generation` `3d-scene-graph` `CVPR-2020` `foundational` `3DSSG`
- **证据等级**：`full-paper`

## 摘要

场景理解不仅需要识别场景中的物体，还需理解物体之间的上下文关系。本文聚焦于场景图（scene graph）这一数据结构，将场景实体组织为图（物体为节点，关系为边），并将其作为 3D 场景理解的推理工具。本文提出了**首个从 3D 点云学习语义场景图的算法**，基于 PointNet 和 Graph Convolutional Networks (GCN) 的架构来回归场景图。同时，发布了 **3DSSG 数据集**，为 3RScan 中的 1,482 个 3D 重建（478 个自然变化的室内环境）提供半自动生成的语义场景图标注。

## 贡献

1. **3DSSG 数据集**：大规模 3D 语义场景图数据集，扩展 3RScan，包含关系、属性和类别层次。通过渲染 3D 图到 2D 可获得 363k 对图-图像对。
2. **首个学习的 3D 场景图预测方法**：SGPN（Scene Graph Prediction Network），从 3D 点云端到端生成语义场景图。
3. **跨域检索应用**：展示 3D 语义场景图在 2D-3D 场景检索（变化环境下的匹配）中的效用。

## 3DSSG 数据集

### 规模

| 指标 | 数值 |
|------|------|
| 3D 重建数 | 1,482 scans |
| 场景数 | 478 scenes |
| 实例数 | 48k |
| 类别数 | 534（层次化） |
| 关系类型 | 40 种 |
| 属性类型 | 93 种 |
| 属性标注 | ~21k 实例，共 48k 条属性 |
| 2D 场景图-图像对 | 363k 对（通过 3D→2D 渲染获得） |

对比 Armemi et al. [3]：~3k 实例、28 类、4 种关系 | 3DSSG：48k 实例、534 类（层次化）、40 种关系。

### 节点（Nodes）

- 每个节点对应一个 3D 物体实例
- 具有**层次化类别标签**：使用 WordNet 获取超义词链（如 armchair → chair → seat → furniture）
- 每个节点包含**属性 A**：静态属性（颜色、尺寸、形状、材质）、动态属性（open/closed、full/empty 等状态）、功能可供性（affordance，如 sitting）

### 关系（Relationships）

3 类共 40 种关系：

1. **支撑关系**（Support）：如 standing on, lying on → 基于物理接触和几何分析
2. **空间/邻近关系**（Proximity）：如 next to, in front of, behind → 仅在共享支撑父节点间计算
3. **比较关系**（Comparative）：如 bigger than, darker than, same as → 从属性对比派生

### 标注流程

半自动生成：自动提取几何关系（支撑、邻近）+ 人工验证 + 专家标注（属性、复杂关系）。

## 方法：SGPN（Scene Graph Prediction Network）

### 架构

给定输入点集 P 和类无关的实例分割 M：

1. **ObjPointNet**：对每个实例 i 独立提取节点特征 φ_n（从 Pi 的 PointNet 特征）
2. **RelPointNet**：对每对节点 (i,j) 提取边特征 φ_r（从联合包围盒 Bi∪Bj 的点集 + 掩码 Mij 的 PointNet 特征）
3. **GCN**：消息传递图卷积网络
   - 每层消息传递：三元组 (subject, predicate, object) 经 MLP g1 传播
   - 节点聚合：平均来自所有连接的消息
   - 残差连接：φ(l+1)_i = φ(l)_i + g2(ρ(l)_i) 缓解 Laplacian 平滑
   - 层数对应可捕获的关系阶数
4. **预测头**：两个 MLP 分别输出节点类别和谓词类别

### 损失函数

- **物体分类损失** Lobj：多分类 focal loss + 归一化逆频率加权
- **谓词分类损失** Lpred：逐类二元交叉熵（每个边可被分配多个标签 or 无标签）+ focal loss
- 总损失：L_total = λ_obj L_obj + L_pred

### 关键设计

- 保留 RelPointNet 输入的方向（禁用旋转增强）以支持左/右等方向关系
- 多谓词预测（而非单标签分类）以处理关系歧义（如 simultaneously in front of and same as）

## 实验与结果

### 实验设置

- **数据集**：3DSSG（3RScan 原始 train/test 划分）
- **基线**：重实现 [29] 的方法，适配到 3D（PointNet 特征 + 直连分类器）
- **指标**：Recall@K（triplets, object, predicate）

### 语义场景图预测结果

| 方法 | Relationship R@50 | Relationship R@100 | Object R@5 | Object R@10 | Predicate R@3 | Predicate R@5 |
|------|:---:|:---:|:---:|:---:|:---:|:---:|
| Relation Prediction Baseline | 0.39 | 0.45 | 0.66 | 0.77 | 0.62 | 0.88 |
| Single Predicate, ObjCls from PN | 0.37 | 0.43 | 0.68 | 0.78 | 0.42 | 0.58 |
| **Multi Predicate, ObjCls from PN (Ours)** | **0.40** | **0.66** | **0.68** | **0.78** | **0.89** | **0.93** |
| Multi Predicate, ObjCls from GCN | 0.30 | 0.60 | 0.60 | 0.73 | 0.79 | 0.91 |

关键发现：
- 多谓词预测显著优于单谓词（Predicate R@3: 0.89 vs 0.42）
- PointNet 特征直连 + GCN 消息传递优于纯 GCN 特征（ObjCls from PN 优于 from GCN）
- 基线在关系 R@100 仅 0.45，本文 Multi Predicate 达 0.66

### 3D-3D 场景检索（变化场景匹配）

| 图源 | Graph | Top-1 | Top-3 | Top-5 |
|------|:----:|:----:|:----:|:----:|
| GT | fS(G_3D, G_3D) | **0.96** | **1.00** | **1.00** |
| GT | fJ(G_3D, G_3D) | 0.95 | 0.96 | 0.98 |
| Baseline 预测 | fJ(G_3D, G_3D) | 0.29 | 0.50 | 0.59 |
| **Ours 预测** | **fJ(G_3D, G_3D)** | **0.34** | **0.51** | **0.56** |

### 2D-3D 场景检索

| 图源 | Graph | Top-1 | Top-3 | Top-5 |
|------|:----:|:----:|:----:|:----:|
| GT | fS(G_2D, G_3D) | **1.00** | **1.00** | **1.00** |
| GT | τS(s(N_2D), s(N_3D)) | 0.98 | 0.99 | 1.00 |
| Baseline 预测 | fS(G_2D, G_3D) | 0.10 | 0.25 | 0.32 |
| **Ours 预测** | **τS(s(N_2D), s(N_3D))** | **0.17** | **0.36** | **0.41** |

## 分析与讨论

- **多谓词建模的重要性**：3D 场景中物体对可以同时具有多种关系（空间 + 支撑 + 比较），单标签分类无法处理这种歧义
- **场景图的鲁棒性**：场景图作为中间表示对光照变化和动态场景（家具移动、物品增减）具有天然鲁棒性
- **跨域潜力**：通过渲染 3D→2D 的场景图，实现了 2D-3D 跨模态检索
- **局限**：
  - 需要类无关的实例分割作为输入（尚未端到端）
  - 预测图在检索任务上与 GT 图仍有显著差距（Top-1: 0.34 vs 0.96）
  - 仅限于室内场景，未评估泛化到室外或合成数据

## 后续工作链接

- [CCL-3DSGG: CLIP-Driven Open-Vocabulary 3D Scene Graph Generation](ccl-3dsgg-clip-driven-open-vocabulary-3d-scene-graph-generation.md) — 使用 CLIP 进行开放词汇 3D SGG
- [Open3DSG: Open-Vocabulary 3D Scene Graphs from Point Clouds](open3dsg-open-vocabulary-3d-scene-graphs-from-point-clouds.md) — 开放词汇 3D SGG 后续工作
- [ZING-3D: Zero-shot Incremental 3D Scene Graphs](zing-3d-zero-shot-incremental-3d-scene-graphs.md) — 零样本增量 3D 场景图

## 总结

本文是 3D 语义场景图领域的奠基之作：
1. **数据集贡献**：3DSSG 是首个大规模真实 3D 室内场景的语义场景图数据集（40 种关系、534 类、93 种属性），后续大量 3D SGG 工作以此为基础
2. **方法贡献**：首个从 3D 点云学习语义场景图的端到端方法（PointNet + GCN），设计了多谓词预测和层次化节点分类
3. **应用贡献**：展示了场景图作为跨域检索中间表示的可行性（2D-3D 场景检索）

## 参考文献

- Wald, J., Dhamo, H., Navab, N., & Tombari, F. (2020). Learning 3D Semantic Scene Graphs from 3D Indoor Reconstructions. In *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*, pp. 3961-3970.
