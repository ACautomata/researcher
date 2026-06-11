# Towards Spatio-Temporal World Scene Graph Generation from Monocular Videos

> World Scene Graph Generation (WSGG) 的提出：从单目视频构建全局 3D 世界坐标系下的场景图，涵盖被遮挡和移出视野的物体。

## Metadata

| 字段 | 值 |
|------|-----|
| **标题** | Towards Spatio-Temporal World Scene Graph Generation from Monocular Videos |
| **作者** | Rohith Peddi, Saurabh, Shravan Shanmugam, Likhitha Pallapothula, Yu Xiang, Parag Singla, Vibhav Gogate |
| **机构** | The University of Texas at Dallas, Indian Institute of Technology Delhi |
| **发表** | arXiv:2603.13185v1, Mar 2026 |
| **代码** | [https://github.com/rohithpeddi/WorldSGG](https://github.com/rohithpeddi/WorldSGG) |
| **证据等级** | full-paper |
| **领域** | scene-graph |
| **关键词** | World Scene Graph Generation, Video Scene Graph Generation, Scene Understanding, Spatio-Temporal Reasoning, Object Permanence |

## 核心贡献

1. **ActionGenome4D 数据集**：将 Action Genome 升级为 4D 场景表示，通过 π3 前馈 3D 重建、GDINO + SAM2 检测分割流水线生成世界坐标系下的 oriented 3D bounding boxes，并为所有交互物体（包括不可见物体）提供密集关系标注。
2. **World Scene Graph Generation (WSGG) 任务形式化**：在每个时刻构建包含场景中所有交互物体（observed + unobserved）的世界场景图。
3. **三种互补方法**：
   - **PWG (Persistent World Graph)**：通过零阶特征缓存实现物体永久性
   - **MWAE (Masked World Auto-Encoder)**：将不可见物体推理重构为掩码补全 + 跨视角关联检索
   - **4DST (4D Scene Transformer)**：用可微的逐物体时序注意力替代静态缓存，融合 3D 运动和相机位姿特征
4. **VLM 基线**：基于 Graph RAG 的多种开源 VLM（InternVL 2.5、Qwen 2.5-VL）WSGG 基线

## 方法

### PWG — Persistent World Graph

实现零阶物体永久性：为每个物体维护一个最近可见帧的 DINO 特征缓存。不可见时直接复用最近可见帧的原始特征，并记录特征"陈旧度"（staleness）。特点是简单、非可微、零参数。

### MWAE — Masked World Auto-Encoder

将不可见物体的关系预测视为掩码补全任务：随机掩码部分物体快照（可见/不可见混合），训练跨视角关联检索。通过交叉注意力实现可见→不可见的特征补全。

### 4DST — 4D Scene Transformer

用 Per-Object Bidirectional Self-Attention 替换 PWG 的静态缓存：每个物体在整个视频序列上执行双向自注意力，融合 3D 位置、运动、相机位姿信息。支持端到端学习，可微。

## 数据集

ActionGenome4D 继承 Action Genome 的室内单人设定，基于 π3 重建场景点云，提供：
- 世界坐标系下 oriented 3D bounding boxes
- 所有物体的密集关系标注（含不可见物体）
- 训练集使用 VLM 伪标注生成不可见物体关系，测试集人工校正

## 实验结果

### 主要结果（Table 2: R@K 比较）

| 方法 | Backbone | PredCls (WC) R@10 | PredCls (NC) R@50 | SGDet (WC) R@50 | SGDet (NC) R@50 |
|------|----------|:---:|:---:|:---:|:---:|
| PWG | DINOv2-L | 65.07 | 99.59 | 69.63 | 56.66 |
| PWG | DINOv3-L | 65.58 | 99.76 | 70.93 | 52.57 |
| MWAE | DINOv2-L | 65.33 | 99.65 | 69.50 | 56.96 |
| MWAE | DINOv3-L | 65.57 | **99.78** | 70.90 | 52.86 |
| **4DST** | **DINOv2-L** | 64.31 | 99.67 | 70.32 | **57.00** |
| **4DST** | **DINOv3-L** | **66.11** | 99.72 | **71.95** | 52.90 |

- WC = With Constraint, NC = No Constraint
- 4DST + DINOv3-L 在 PredCls (WC) R@10 和 SGDet (WC) R@50 上最优
- No Constraint 设置下各方法 R@50 均接近 100% (99.6+)

### Mean Recall（Table 3: mR@K 比较）

| 方法 | Backbone | PredCls (WC) mR@50 | SGDet (NC) mR@50 |
|------|----------|:---:|:---:|
| PWG | DINOv2-L | 38.80 | 54.98 |
| PWG | DINOv3-L | 41.29 | 55.51 |
| MWAE | DINOv2-L | 39.47 | 55.47 |
| MWAE | DINOv3-L | 40.99 | 54.08 |
| **4DST** | **DINOv2-L** | 39.50 | 55.40 |
| **4DST** | **DINOv3-L** | **41.56** | **55.88** |

### VLM 基线（Table 4 & 5）

Graph RAG + Qwen 2.5-VL 在 PredCls 模式下达到最佳 Micro F1 = 53.3%（注意：此任务为未定位关系预测，与主流 SGG 方法不可直接比较）

## 分析

- **物体永久性收益显著**：三种方法均超过纯 frame-centric 基线，4DST 的时序注意力机制提供了最一致的提升
- **No Constraint 模式饱和**：R@50 接近 100%，因为多标签允许所有合理关系同时输出
- **mR@K 差距大**：R@K vs mR@K 差距（如 71.95 vs 41.56）反映长尾关系的学习仍是主要挑战
- **VLM 性能有限**：即使采用 Graph RAG 检索增强，Macro F1 仅 ~26%，说明纯文本/视觉语言方法在细粒度关系推理上不足

## 局限与未来工作

- ActionGenome4D 继承 Action Genome 的室内单人设定，场景多样性有限
- π3 可能产生有噪声的几何结果
- 可扩展至室外、多人、多视角场景
- 自监督预训练策略可进一步利用大规模视频数据

## 链接

- [[actiongenome4d-dataset|ActionGenome4D 数据集]]
- [[4d-panoptic-scene-graph-generation|4D Panoptic Scene Graph Generation]]（相关 4D SGG 工作）
- [[panoptic-video-scene-graph-generation|Panoptic Video Scene Graph Generation]]（视频 SGG 相关工作）
