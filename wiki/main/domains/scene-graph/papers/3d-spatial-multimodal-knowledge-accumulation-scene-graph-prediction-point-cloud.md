---
title: "3D Spatial Multimodal Knowledge Accumulation for Scene Graph Prediction in Point Cloud"
authors:
  - Mingtao Feng
  - Haoran Hou
  - Liang Zhang
  - Zijie Wu
  - Yulan Guo
  - Ajmal Mian
year: 2023
venue: CVPR 2023
doi: null
arxiv: null
code: "https://github.com/HHrEtvP/SMKA"
domain: scene-graph
tags: [3d-scene-graph, point-cloud, knowledge-graph, multimodal]
evidence_level: full-paper
status: active
task: 3D Scene Graph Prediction
dataset: 3DSSG
---

# 3D Spatial Multimodal Knowledge Accumulation for Scene Graph Prediction in Point Cloud

> Mingtao Feng, Haoran Hou, Liang Zhang, Zijie Wu, Yulan Guo, Ajmal Mian. CVPR 2023.
> Code: [https://github.com/HHrEtvP/SMKA](https://github.com/HHrEtvP/SMKA)

## 核心贡献

1. **首次**将3D物理空间的层级结构模式显式统一到深度网络中，以促进3D场景图预测。
2. 提出**层级符号知识构建模块**：利用外部知识库（ConceptNet）作为基线，引入3D场景的层级结构线索。
3. 提出**知识引导的视觉上下文编码模块**：构建层级视觉图，通过区域感知图网络（RaGN）学习上下文特征。
4. 提出**3D空间多模态知识积累模块**：将符号知识与视觉内容关联，规范化关系预测的语义空间。

## 问题定义

给定3D点云场景 $I$，目标是生成语义场景图 $G = \{V, R\}$，其中 $V$ 为实例对象节点，$R$ 为关系边。模型分解为：

$$P(G|I) = P(K_s|I) P(G_v|K_s, I) P(R, K_m|G_v, K_s, I)$$

其中 $K_s$ 为层级符号知识图，$G_v$ 为视觉图，$K_m$ 为3D空间多模态知识。

## 方法

### 1. 层级符号知识初始化 (Hierarchical Symbolic Knowledge Initialization)

- 利用 **ConceptNet** 作为外部知识库，过滤到3D场景相关类别（约760节点，5000条边）。
- 根据物理支撑关系将物体分为三层层级结构：
  - **第一层**：地板（无支撑）
  - **第二层**：直接由地板支撑的物体（床、桌子、沙发）
  - **第三层**：由第二层物体支撑的物体（枕头、杯子、垫子）
- 用 MLP 为每个节点预测层级 token，结合 GloVe 词向量初始化节点。
- 在层级间添加"支撑边"（support edge），表示物理支撑关系。

### 2. 知识引导的视觉上下文编码 (Knowledge-guided Visual Context Encoding)

- **视觉图构建**：用 Point Cloud Transformer 提取空间感知视觉特征 $f_v$，MLP编码边界框空间特征 $f_t$，GloVe 嵌入语义特征 $f_w$。
- 根据 $K_s$ 中的层级 token 将节点分配到对应层级。
- **区域感知图网络 (RaGN)**：节点在与自己共享同一物理支撑的区域内聚集信息，增强上下文后通过 GRU 传递消息更新隐藏状态。

### 3. 3D空间多模态知识积累 (Spatial Multimodal Knowledge Accumulation)

- **图推理网络**：在层级符号知识图 $K_s$ 上执行消息传递，输入包括：(1) $K_s$ 中节点/边的可训练嵌入，(2) 是否出现在视觉图中的0/1指示器，(3) 视觉图中对应的上下文特征。
- **知识增强的场景图预测**：将多模态知识嵌入 $b_k$ 与上下文特征 $c$ 融合，得到知识增强的上下文特征 $f$，再通过标准 GCN 解码。
- **损失函数**：$L = L_{init}^o + w_o L_{final}^o + w_r L_{final}^r$，其中 $w_o=0.75, w_r=1$。

## 实验

### 数据集
- **3DSSG** (3D Semantic Scene Graph) 数据集，160个物体类别，27个关系类别。

### 任务设置
遵循标准3D场景图预测的三个评估任务：
- **PredCls (谓词分类)**：给定GT边界框和语义标签，预测关系
- **SGCls (场景图分类)**：给定GT边界框，联合预测关系和物体类别
- **SGDet (场景图检测)**：给定原始点云，端到端检测物体+预测关系

### 评估指标
Recall@K (R@K) 和 mean Recall@K (mR@K)，K=50,100。

### 主要结果

| 任务 | 方法 | R@50 | R@100 | mR@50 | mR@100 |
|------|------|------|-------|-------|--------|
| **PredCls** | Ours | **68.32** | **69.49** | **66.54** | **66.92** |
|  | SGPN | 57.71 | 58.05 | 38.12 | 38.67 |
|  | EdgeGCN | 58.42 | 59.11 | 38.84 | 39.35 |
|  | KISG | 64.47 | 64.93 | 63.19 | 63.52 |
| **SGCls** | Ours | **31.50** | **31.64** | **30.29** | **30.56** |
|  | SGPN | 28.39 | 28.74 | 22.23 | 22.57 |
|  | EdgeGCN | 28.58 | 28.93 | 22.67 | 23.33 |
|  | KISG | 29.46 | 29.65 | 28.20 | 28.64 |
| **SGDet** | Ours | **29.41** | **29.44** | **25.35** | **25.36** |
|  | 3D+IMP | 24.54 | 24.57 | 21.71 | 21.72 |
|  | 3D+MOTIFS | 26.58 | 26.59 | 24.12 | 24.17 |
|  | 3D+VCTree | 27.58 | 27.62 | 24.92 | 24.94 |

### 关键对比
- 在 **PredCls** 任务上，比 KISG 提升 R@50 提升 **3.85%** (68.32 vs 64.47)
- 在 **SGCls** 任务上，比 KISG 提升 R@50 提升 **2.04%** (31.50 vs 29.46)
- 在 **SGCls** 任务的 mR@50 上，比 KISG 提升 **2.09%** (30.29 vs 28.20)

### 消融实验 (SGCls任务)

**层级符号知识 $K_s$：**
| 变体 | R@50 | mR@50 |
|------|------|-------|
| w/o Hierarchical Tokens | 30.47 | 28.94 |
| w/o Support Edge | 30.55 | 29.17 |
| w/o Both | 28.41 | 27.13 |
| **Ours** | **31.50** | **30.29** |

**视觉上下文编码：**
| 变体 | R@50 | mR@50 |
|------|------|-------|
| $G_v$ 替换为全连接图 $G_{fc}$ | 28.17 | 26.28 |
| w/o RaGN | 26.43 | 24.23 |
| RaGN替换为GCN | 31.03 | 29.67 |
| **Ours** | **31.50** | **30.29** |

**多模态知识 $K_m$：**
| 变体 | R@50 | mR@50 |
|------|------|-------|
| w/o $b_i^o$ and $b_{ij}^e$ | 26.27 | 22.93 |
| w/o $c_i^o$ and $c_{ij}^e$ as input | 28.14 | 25.05 |
| **Ours** | **31.50** | **30.29** |

多模态知识嵌入 $K_m$ 对 R@50 提升 **5.23%**，对 mR@50 提升 **7.36%**。

### 视觉图结构分析
| 变体 | PredCls R@50 | PredCls mR@50 | SGCls R@50 | SGCls mR@50 |
|------|-------------|--------------|-----------|------------|
| $G_r$ (随机连接) | 62.74 | 58.25 | 28.17 | 27.28 |
| $G_t$ (GT支撑关系) | 68.41 | 66.59 | 31.59 | 30.35 |
| $G_v$ (本文) | **68.32** | **66.54** | **31.50** | **30.29** |

$G_v$ 与 $G_t$ 表现相近，说明层级视觉图能有效提取3D空间的层级结构模式。

### 长尾分析
| 方法 | Head (前5) | Body (中间) | Tail (后5) |
|------|-----------|------------|-----------|
| SGPN | 39.42 | 23.64 | 13.03 |
| EdgeGCN | 39.51 | 23.85 | 13.15 |
| KISG | 40.36 | 24.56 | 13.61 |
| **Ours** | **44.23** | **26.27** | **14.73** |

在尾部关系类别上表现最佳，说明层级结构能缓解样本不平衡问题。

### 标签噪声鲁棒性
在30%噪声率条件下，本文方法比 KISG 的 R@50 提升约 **6.89%**，表现出显著更好的鲁棒性。

## 分析与评价

### 优势
- 首次将3D场景层级结构显式编码到场景图预测网络中，创新性强。
- 多模态知识积累兼顾了符号知识与视觉信息的对齐，有效解决了纯文本知识库（如KISG）的局限性。
- 对标签噪声和长尾分布具有更好的鲁棒性，实用价值高。
- 所有模块消融实验设计完整，验证了每个组件的有效性。

### 局限
- SGDet 任务性能饱和（~29.4 R@50），物体检测阶段成为瓶颈。
- 视觉图中 Window1 等边界框点云稀疏的情况会错误分类层级 token。
- 未利用物体属性（如对称性、纹理）来构建更丰富的知识图。

### 与相关工作的关系
- 与 [[kisp-knowledge-inspired-3d-scene-graph-prediction-in-point-cloud]] 最直接相关：KISG 使用文本标签提取先验知识，本文扩展为多模态知识积累。
- 与 [[sgon-scene-graph-prediction]] / [[edgegc-exploiting-edge-oriented-reasoning-for-3d-point-based-scene-graph-analysis]] 对比：本文利用3D空间层级结构超越了几何特征驱动的预测。

## 参考资料
- Paper: CVPR 2023 Open Access
- Code: [https://github.com/HHrEtvP/SMKA](https://github.com/HHrEtvP/SMKA)
- Dataset: 3DSSG [Wald et al., CVPR 2020]
- External KB: ConceptNet [Speer et al., AAAI 2017]
