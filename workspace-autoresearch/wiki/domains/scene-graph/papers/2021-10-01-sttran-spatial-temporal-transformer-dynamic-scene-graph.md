# STTran: Spatial-Temporal Transformer for Dynamic Scene Graph Generation

> 空间-时间 Transformer 用于动态场景图生成。视频动态场景图的经典工作，首次将 Transformer 架构应用于视频场景图生成中的空间编码和时间解码。

## 元数据

| 字段 | 值 |
|------|-----|
| **标题** | Spatial-Temporal Transformer for Dynamic Scene Graph Generation |
| **作者** | Yuren Cong, Wentong Liao, Hanno Ackermann, Bodo Rosenhahn, Michael Ying Yang (Leibniz University Hannover / University of Twente) |
| **发表** | ICCV 2021 |
| **DOI** | — |
| **代码** | [https://github.com/yrcong/STTran](https://github.com/yrcong/STTran) |
| **证据等级** | full-paper |
| **原始来源** | [raw/sources/2021-10-01-sttran.pdf](/.raw/sources/2021-10-01-sttran.pdf) |
| **入库日期** | 2026-06-10 |

## 摘要

Dynamic Scene Graph Generation 旨在从视频中生成场景图。相比图像级场景图生成更富挑战性，因为对象间的动态关系和帧间时间依赖需要更丰富的语义解释。本文提出 **STTran**（Spatial-Temporal Transformer），包含两个核心模块：(1) **Spatial Encoder**：对输入帧提取空间上下文并推理帧内视觉关系；(2) **Temporal Decoder**：以 Spatial Encoder 的输出为输入，捕获帧间时间依赖并推断动态关系。STTran 可灵活接受变长视频输入而无需裁剪。在 Action Genome 数据集上取得 SOTA 结果。

## 核心贡献

1. **Spatial-Temporal Transformer 架构**：将 Transformer 的 encoder-decoder 结构赋予具体任务——encoder 关注空间上下文，decoder 捕获时间依赖，首次有效解决视频场景图的时序建模问题
2. **Multi-label 关系分类**：引入 multi-label margin loss，替代传统 single-label 分类，更贴合真实世界中一对对象可存在多重关系的语义多样性
3. **Semi Constraint 图生成策略**：提出介于 With Constraint 和 No Constraint 之间的策略，允许 subject-object pair 有多重谓词（当置信度高于阈值时），生成更接近 ground truth 的场景图
4. **Frame Encoding 学习**：提出可学习的 frame encoding 替代正弦位置编码，更好地注入时序位置信息

## 方法

### 总体框架

输入视频帧 → Faster R-CNN (ResNet-101) 目标检测 → 关系特征提取（视觉外观 + 空间信息 + 语义嵌入）→ **Spatial Encoder**（帧内自注意力）→ **Temporal Decoder**（帧间自注意力 + 可学习 frame encoding）→ 线性分类器预测关系类型（attention/spatial/contact）→ 动态场景图

### 关系特征表示

对第 t 帧中第 k 个关系（subject i, object j），特征向量 x_t^k 拼接了：
- 视觉外观：W_s v_t^i, W_o v_t^j（通过线性层降维至 512 维）
- 联合框特征：通过 RoIAlign 提取的 union box 特征图 u_t^ij ∈ R^(256×7×7)，经线性投影
- 空间特征：f_box(b_t^i, b_t^j) 编码边界框几何关系
- 语义嵌入：s_t^i, s_t^j ∈ R^200 来自目标类别嵌入

### Spatial Encoder

- 输入为单帧的关系特征 X_t = {x_t^1, ..., x_t^K(t)}
- 标准 Transformer 自注意力层堆叠（N=1 层）
- 无需额外位置编码——帧内关系天然并行，空间信息已编码在关系特征中
- 输出为空间上下文化的关系表示

### Frame Encoding

- 可学习的 frame embedding 向量 E_f = [e_1, ..., e_n]，e ∈ R^1936
- 仅用于 Temporal Decoder 的 Q 和 K 注入时序位置
- 滑动窗口大小 η 固定，视频长度不影响 encoding 长度
- 与正弦编码相比性能更好（见表 5 消融实验）

### Temporal Decoder

- 采用滑动窗口（size η=2, stride=1）在空间上下文化的表示序列 [X_1, ..., X_T] 上滑动
- 输入批次 Z_i = [X_i, ..., X_{i+η-1}]
- 标准自注意力层堆叠（N=3 层），Q=K=Z_i+E_f, V=Z_i
- 相同帧的关系共享同一 frame encoding
- 出现在多个窗口中的帧选择最早的表示
- 不使用 masked multi-head attention（与原始 Transformer decoder 不同）

### 损失函数

**Multi-label Margin Loss**：
- L_p(r, P^+, P^-) = Σ_{p∈P+} Σ_{q∈P-} max(0, 1-φ(r,p)+φ(r,q))
- P^+: 标注中包含的谓词；P^-: 未标注的谓词
- 支持一对对象同时存在多重关系（如 <person-holding-bottle> 和 <person-drinking from-bottle>）
- 总损失：L_total = L_p + L_0（L_0 为目标分类交叉熵损失）

### 图生成策略

**Semi Constraint**（本文提出）：
- 允许 subject-object pair 有多重谓词，但保留严格的置信度筛选
- 谓词置信度 > 阈值（默认 0.9）方视为正例
- 介于 With Constraint（至多一个谓词）和 No Constraint（允许多重猜测）之间
- 测试时关系三元组置信度：s_rel = s_sub · s_p · s_obj

## 实验

### 设定

| 维度 | 详情 |
|------|------|
| **数据集** | Action Genome (AG) — 234,253 帧，476,229 个边界框（35 类对象），1,715,568 个关系实例（25 类谓词） |
| **关系类型** | attention（是否在看）、spatial（空间关系）、contact（接触方式） |
| **骨干网络** | Faster R-CNN (ResNet-101) — 24.6 mAP @ 0.5 IoU |
| **优化器** | AdamW, lr=1e-5, batch_size=1, gradient clipping max_norm=5 |
| **架构参数** | η=2, stride=1, Spatial Encoder: 1 层, Temporal Decoder: 3 层, 8 heads, d_model=1936, dropout=0.1 |
| **评估任务** | PredCLS / SGCLS / SGDET |
| **评估指标** | Recall@K (K=10, 20, 50) 在 With Constraint / Semi Constraint / No Constraint 下 |

### 主要结果（Action Genome）

#### With Constraint

| 方法 | PredCLS R@10/20/50 | SGCLS R@10/20/50 | SGDET R@10/20/50 |
|------|:------------------:|:----------------:|:----------------:|
| VRD (2016) | 51.7 / 54.7 / 54.7 | 32.4 / 33.3 / 33.3 | 19.2 / 24.5 / 26.0 |
| Motif Freq (2018) | 62.4 / 65.1 / 65.1 | 40.8 / 41.9 / 41.9 | 23.7 / 31.4 / 33.3 |
| MSDN (2017) | 65.5 / 68.5 / 68.5 | 43.9 / 45.1 / 45.1 | 24.1 / 32.4 / 34.5 |
| VCTREE (2019) | 66.0 / 69.3 / 69.3 | 44.1 / 45.3 / 45.3 | 24.4 / 32.6 / 34.7 |
| RelDN (2019) | 66.3 / 69.5 / 69.5 | 44.3 / 45.4 / 45.4 | 24.5 / 32.8 / 34.9 |
| GPS-Net (2020) | 66.8 / 69.9 / 69.9 | 45.3 / 46.5 / 46.5 | 24.7 / 33.1 / 35.1 |
| **STTran (本文)** | **68.6 / 71.8 / 71.8** | **46.4 / 47.5 / 47.5** | **25.2 / 34.1 / 37.0** |

#### Semi Constraint

| 方法 | PredCLS R@10/20/50 | SGCLS R@10/20/50 | SGDET R@10/20/50 |
|------|:------------------:|:----------------:|:----------------:|
| VRD | 55.5 / 64.9 / 65.2 | 36.2 / 39.7 / 40.1 | 19.0 / 27.1 / 32.4 |
| Motif Freq | 65.7 / 74.1 / 74.5 | 45.5 / 49.3 / 49.5 | 22.9 / 33.7 / 39.0 |
| MSDN | 69.6 / 78.9 / 79.9 | 48.3 / 54.1 / 54.5 | 23.2 / 34.2 / 41.5 |
| VCTREE | 70.1 / 78.2 / 79.6 | 49.0 / 53.7 / 54.0 | 23.7 / 34.8 / 40.4 |
| RelDN | 70.7 / 78.8 / 80.3 | 49.4 / 53.9 / 54.1 | 24.1 / 35.0 / 40.7 |
| GPS-Net | 71.3 / 81.2 / 82.0 | 50.2 / 55.0 / 55.2 | 24.5 / 35.3 / 41.9 |
| **STTran** | **73.2 / 83.1 / 84.0** | **51.2 / 56.5 / 56.8** | **24.6 / 35.9 / 44.0** |

#### No Constraint

| 方法 | PredCLS R@10/20/50 | SGCLS R@10/20/50 | SGDET R@10/20/50 |
|------|:------------------:|:----------------:|:----------------:|
| RelDN | 75.7 / 93.0 / 99.0 | 52.9 / 62.4 / 65.1 | 24.1 / 35.4 / 46.8 |
| GPS-Net | 76.0 / 93.6 / 99.5 | 53.6 / 63.3 / 66.0 | 24.4 / 35.7 / 47.3 |
| **STTran** | **77.9 / 94.2** / 99.1 | **54.0 / 63.7 / 66.4** | **24.6 / 36.2 / 48.8** |

> STTran 在所有三项任务的所有约束策略下全面超越全部 baselines。No Constraint 下 PredCLS-R@50 低于 Motif Freq (99.6 vs 99.1)，但作者指出在 K=50 时由于猜测机会过多结果不可靠。

### 时序依赖分析

- **LSTM 嫁接实验**：在 Motif Freq / MSDN / RelDN / GPS-Net 的最终分类器前嫁接 LSTM 处理时序序列，所有基线均有提升（GPS-Net: 69.9→70.4），但均低于 STTran (71.8)，说明时序依赖有效且 STTran 更优
- **时序打乱实验**：将 1/3 训练集视频打乱时序，PredCLS-R@20 从 71.8 降至 70.6；反转则降至 71.0。验证 STTran 确实捕获了有意义的时间依赖，而非仅来自更强的特征表示

### 消融实验

| Spatial Encoder | Temporal Decoder | Frame Encoding | PredCLS-R@20 (With) | SGDET-R@20 (With) | PredCLS-R@20 (Semi) | SGDET-R@20 (Semi) |
|:---------------:|:----------------:|:--------------:|:-------------------:|:------------------:|:-------------------:|:------------------:|
| ✓ | — | — | 69.6 | 32.9 | 78.7 | 35.1 |
| — | ✓ | — | 71.0 | 33.7 | 82.2 | 35.5 |
| ✓ | ✓ | — | 71.3 | 33.8 | 82.7 | 35.6 |
| ✓ | ✓ | sinusoidal | 71.3 | 33.9 | 82.8 | 35.7 |
| ✓ | ✓ | learned | **71.8** | **34.1** | **83.1** | **35.9** |

关键发现：
- **Spatial Encoder 单独**（即纯图像级方法）：PredCLS-R@20=69.6，接近于 RelDN (69.5)，表明作为图像级 SGG 方法竞争力相当
- **Temporal Decoder 单独**（也处理帧内空间上下文？）：PredCLS-R@20=71.0，显著提升，说明时间信息是关键增益
- **两者联合**：PredCLS-R@20=71.3，进一步小幅提升
- **Learned frame encoding** 优于 sinusoidal（PredCLS-R@20: 71.8 vs 71.3）

### 定性结果

- Fig. 4 展示：Spatial Encoder 将第二帧的 <person-eating-food> 误判为 <person-touching-food>，而完整 STTran 借助时间信息正确推理为 eating
- Fig. 5 展示三个约束策略下的场景图质量差异，Semi Constraint 最接近 ground truth

## 方法对比

| 维度 | STTran | GPS-Net | RelDN | Motif Freq |
|------|--------|---------|-------|------------|
| **时序建模** | Transformer Decoder（滑动窗口） | 无 | 无 | 无 |
| **空间建模** | Transformer Encoder（自注意力） | GCN 传播 | 对比学习 | 全局上下文统计 |
| **关系分类** | Multi-label margin loss | Single-label | Single-label | Single-label |
| **图策略** | With / Semi / No Constraint | With / No | With / No | With / No |
| **PredCLS-R@20 (WC)** | **71.8** | 69.9 | 69.5 | 65.1 |

## 对应关系

- **动态场景图生成 (Dynamic SGG)** → 核心任务，从视频中生成随时间演变的结构化表示
- **Action Genome (AG)** → 实验评估基准数据集
- **Spatial Encoder** → 等价于图像级 SGG 方法
- **Temporal Decoder** → 视频特有模块，捕获帧间关系变化
- **Multi-label margin loss** → 支持一对对象存在多重关系

## 适用任务

- 视频场景图生成 (Dynamic/Video SGG)
- 视频理解与动作分解
- 时序关系推理

## 优缺点

**优点**：
- 首次将 Transformer 架构有效应用于视频动态场景图生成，Encoder-Decoder 结构设计合理
- 在 Action Genome 所有评估协议下全面超越当时 SOTA
- Semi Constraint 策略创新，在多标签场景中更实用
- 代码开源，推动该领域后续研究（大量后继工作以 STTran 为 baseline）
- 消融实验充分，各部分贡献明确

**缺点**：
- 滑动窗口 η=2 很小，无法捕获长程时间依赖（后续 TEMPURA 等工作改进）
- 依赖 Faster R-CNN 检测结果，SGDET 性能受检测器上限限制
- 仅在 Action Genome 单数据集上评估
- 使用 batch_size=1，训练效率较低
- 未考虑长尾分布问题——PredCLS 下 R@K 较高但未报告 mR@K（即未针对性处理谓词长尾问题）

## 后续工作影响

STTran 是 Video/Dynamic SGG 的奠基性工作，后续大量方法以其为 baseline 进行改进：
- **TEMPURA (ECCV 2022)**：改进时序建模，引入双流编码
- **STTran-TPI**：加入 temporal prompt 机制
- **GTR (IJCAI 2023)**：Grafting-Then-Reassembling 框架
- **FReMuRe (2026)**：频率引导的多层次推理，解决长尾问题
- **TRACE, TD2-Net, FloCoDe**：时空建模方向的后续发展

## 开放问题

- 是否可以使用更长的滑动窗口（η > 2）来获取更远帧的信息？
- STTran 能否从更先进的目标检测器（如 DETR）中获益？
- 在多数据集上验证泛化能力？
