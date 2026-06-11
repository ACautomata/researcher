# DSFlash: Comprehensive Panoptic Scene Graph Generation in Realtime

> 低延迟实时全景场景图生成，56 FPS 且生成全面场景图（全实例全关系）

## 元数据

| 字段 | 值 |
|------|-----|
| **标题** | DSFlash: Comprehensive Panoptic Scene Graph Generation in Realtime |
| **作者** | Julian Lorenz, Vladyslav Kovganko, Elias Kohout, Mrunmai Phatak, Daniel Kienzle, Rainer Lienhart (University of Augsburg) |
| **发表** | arXiv 2026 (v1: 2026-03-11) |
| **arXiv** | [2603.10538](https://arxiv.org/abs/2603.10538) |
| **DOI** | — |
| **代码** | 论文接受后发布 |
| **证据等级** | full-paper |
| **原始来源** | [raw/sources/2026-06-09-dsflash-comprehensive-panoptic-scene-graph-generation.pdf](/.raw/sources/2026-06-09-dsflash-comprehensive-panoptic-scene-graph-generation.pdf) |
| **入库日期** | 2026-06-09 |

## 摘要

Scene Graph Generation (SGG) 旨在从图像中提取详细的图结构表示，这对下游任务（如具身智能体的推理）具有重要价值。然而，在实际部署中（尤其是资源受限的边缘设备），现有方法在速度和资源效率上存在严重不足。本文提出 DSFlash，一个低延迟全景场景图生成模型，在标准 RTX 3090 GPU 上可达到 56 FPS，同时不牺牲性能。与仅处理显著关系的先前方法不同，DSFlash 计算全面场景图（所有实例 + 所有实例间关系），提供更丰富的上下文信息。此外，DSFlash 训练资源需求低，可在单张九年前的 GTX 1080 GPU 上 24 小时内完成训练。

## 核心贡献

1. **DSFlash**：首个低延迟全景场景图生成模型，同时达到 SOTA 性能（mR@50=30.9）
2. **双向关系预测器**：通过门控机制（gated mechanism）将一次前向传播同时预测两个方向的关系，将模型头的前向传播次数减半
3. **基于掩码的动态 patch 剪枝**：丢弃与 subject/object 均无重叠的 patch token，按需减少处理 token 数量
4. **融合骨干网络**：直接从分割模型提取特征张量，避免额外的骨干网络前向传播
5. **低分辨率分割掩码**：跳过破坏性双线性插值，直接使用 EoMT 的低分辨率 logits 进行 patch 重叠计算
6. **Token Merging (ToMe-SD)**：在骨干注意力层中合并相似 token 后还原，降低老 GPU 的延迟

## 方法

DSFlash 采用**两阶段架构**：

### 第一阶段：实例分割

- 使用 **EoMT**（Encoder-only Mask Transformer）作为分割骨干网络
- EoMT 基于 ViT，将分割直接集成到编码器的注意力机制中，比 Mask2Former 快 4×
- 提取 blocks 2/5/8/11（S/B 变体）或 5/11/17/23（L 变体）的 patch tokens
- 骨干网络保持冻结，可独立预训练分割模型

### 第二阶段：关系预测

- 将 40×40 特征张量通过 ViT patch embedding 转换为 13×13 patch tokens
- **Mask Embedding**（来自 DSFormer）：对于每个 subject-object 对，根据 patch 与被分割掩码的重叠比例，加权加入 learnable tokens（subject token / object token / background token）
- **Model Neck**：一组 transformer block 处理 enriched patch tokens
- **门控双向关系预测头**（Sec. 3.3）：
  - 输入 x 通过门控 MLP 拆分为 t→ 和 t← 两个中间张量
  - 共享的 MLP 头同时输出前向 (S0→S1) 和反向 (S1→S0) 关系预测
  - 训练时额外使用 feature consistency loss，交换掩码顺序做两次前传监督对称性

### Mask-based Dynamic Patch Pruning（Sec. 3.4）

- 检测与 subject/object 均无重叠的 patch tokens
- 进入 model neck 前丢弃这些 tokens，降低计算量
- 训练时未启用剪枝，推理时直接使用（模型仍可适应）

### Token Merging（Sec. 3.5）

- 在 EoMT 骨干的每个注意力层前使用 **ToMe-SD** 合并相似 token
- 注意力层后立即还原，保持分割能力不受影响

## 实验

### 数据集

- **PSG Dataset**（49k images，56 predicate classes，80 thing + 53 stuff categories）
- 评估协议：**Scene Graph Detection (SGDet)**，使用 **mR@50** 作为主要指标
- 遵循 SingleMPO 协议，防止多重掩码/多重关系预测带来的虚假 SOTA

### 主要结果（PSG Dataset, SGDet, Table 1）

| Method | Backbone | mR@50 ↑ | Latency ↓ | #Params |
|--------|----------|---------|-----------|---------|
| MotifNet-R50 | R50 | 9.56 | 100ms | 109M |
| MotifNet-MD | MaskDINO | 16.32 | 504ms | 332M |
| VCTree-R50 | R50 | 10.14 | 116ms | 105M |
| VCTree-MD | MaskDINO | 17.58 | 520ms | 327M |
| HiLo-R50 | R50 | 16.34 | 277ms | 59M |
| HiLo-L | Swin-L | 19.08 | 427ms | 230M |
| REACT | YOLOv8 | 19.00 | 19ms | 43M |
| DSFormer | MaskDINO+RN50 | 30.70 | 458ms | 330M |
| **DSFlash-L** | **EoMT-L** | **30.90** | **50ms** | 340M |
| **DSFlash-B\*** | **EoMT-B** | **28.50** | **23ms** | 116M |
| **DSFlash-S\*** | **EoMT-S** | **25.05** | **18ms (56 FPS)** | **40M** |

> \* 表示使用低分辨率分割掩码。

**关键结果**：
- DSFlash-L mR@50=30.90，超越 DSFormer 的 30.70，同时延迟从 458ms 降至 50ms（快 9×）
- DSFlash-S\* 以 **18ms 延迟**（56 FPS）达到 mR@50=25.05，且仅 40M 参数，是最小最快的模型
- 对比 REACT（唯一此前注重延迟的 SGG 方法），DSFlash-S\* 在 mR@50 上大幅领先（25.05 vs 19.00），延迟几乎相同（18ms vs 19ms）

### 消融实验（Table 2 — 各优化影响）

| Method | mR@50 ↑ | Latency (ms) ↓ | RPS ↑ |
|--------|---------|----------------|-------|
| DSFormer Baseline | 30.7 | 445 | 435 |
| + Unified Backbone (EoMT) | 25.0 | 41 (-91%) | 5,745 |
| + Efficient Mask Embedding | 25.0 | 37 (-10%) | 7,132 |
| + Gated Bidirectional Pred. | 28.8 | 29 (-22%) | 11,491 |
| + No Seg. Upscaling | 28.5 | 23 (-21%) | 12,928 |
| + EoMT-3S backbone | 25.1 | 18 (-22%) | 17,897 |
| + EoMT-3L backbone | 30.9 | 50 (+72%) | 5,996 |

**关键消融发现**：
- 统一骨干（EoMT 替代 MaskDINO+RN50）将延迟降低 91%，但 mR@50 下降 5.7（因分割质量降低）
- 双向预测提升 mR@50 从 25.0 到 28.8（+3.8），且降低延迟 22%
- 低分辨率分割掩码进一步降低延迟 21%，仅 mR@50 下降 0.3
- 采用 EoMT-3L 骨干恢复并超过 DSFormer 的 mR@50

### Patch Pruning & Token Merging（Table 3 — 不同 GPU）

| Prune | ToMe | H100 | RTX 3090 | GTX 1080 | mR@50 |
|-------|------|------|----------|----------|-------|
| × | 0% | 19ms | 29ms | 230ms | 28.80 |
| ✓ | 0% | 20ms | 29ms | 205ms | 26.67 |
| ✓ | 30% | 20ms | 30ms | **173ms** | 26.51 |

**关键发现**：
- 高端 GPU（H100, RTX 3090）上 batch_size=1 时剪枝无延迟收益（GPU 可并行处理所有 token）
- 低端 GPU（GTX 1080）上延迟从 230ms 降至 173ms（-25%），但 mR@50 下降 2.29
- Token Merging 和 Patch Pruning 的延迟改善可叠加（优化不同部件）

### 骨干消融（Fig. 5 — 分割质量与 SGG 性能相关性）

- mR@50 与分割模型的 panoptic quality (PQ) 强相关（correlation=0.99）
- mR@inf（给定分割掩码的理论最佳 mR@k）直接约束了最终的 mR@50
- 使用更强的分割骨干可预期 SGG 性能直接提升

### PredCls 结果（Table 4）

| Method | PredCls mR@50 | SGDet mR@50 |
|--------|--------------|-------------|
| DSFlash-S | 39.27 | 26.62 |
| DSFlash-B | 41.30 | 28.80 |
| DSFlash-L | 41.69 | 30.90 |

### 训练细节

- 优化器：AdamW，lr=1e-5，weight decay=0.02
- Scheduler：cosine annealing with linear warmup
- 梯度裁剪：max norm=1.0
- Epochs：20
- 数据增强：DeiT III 风格（random flip, color jitter, grayscale/solarization/Gaussian blur）
- 每 5 个 GT relation 采样 1 个负样本
- 可在单张 GTX 1080 上 <24 小时完成训练

## 讨论

### 与相关工作的关系

- **DSFormer**：DSFlash 的直接 baseline。DSFlash 借用了 mask embedding 思想，但将双骨干替换为统一骨干，增加双向预测、动态剪枝等优化，实现 mR@50 小幅超越（30.9 vs 30.7）同时将延迟从 458ms 降至 50ms
- **REACT**：此前唯一注重低延迟的 SGG 方法，但仅覆盖边界框级 SGG，PSGG 覆盖有限。DSFlash 在 PSGG 上 mR@50 大幅领先（25.05 vs 19.00），延迟几乎相同
- **HiLo**：无偏 PSG 方法，DSFlash 在 mR@50 上显著超越（30.9 vs 19.08 HiLo-L）
- **EoMT**：DSFlash 的分割骨干。其轻量设计（仅 encoder，无需 decoder/pixel decoder）是 DSFlash 低延迟的关键

### 局限性

- 分割骨干训练开销独立，未端到端联合优化
- 动态 patch pruning 在高端 GPU 上的延迟收益有限（batch=1 时 GPU 并行能力抵消剪枝收益）
- 低分辨率分割掩码导致空间精度下降，对小物体关系判断可能不准确
- 结论中提及双向预测存在 subject/object 混淆问题（Fig. 14 失败案例）

## 链接

- Predecessor: [DSFormer (ECCV 2024)]() — SOTA PSG model，DSFlash 的 baseline
- 同类论文：[REACT (2025)]() — 实时 SGG，边界框级
- 同类论文：[HiLo (ICCV 2023)](hilo-exploiting-high-low-frequency-for-unbiased-panoptic-scene-graph-generation.md) — 无偏 PSG
- 同类论文：[PSGTR/PSGFormer (ECCV 2022)](https://github.com/franciszzj/HiLo) — PSG 奠基工作
- Downstream: 具身智能体的场景理解、实时视频流推理
