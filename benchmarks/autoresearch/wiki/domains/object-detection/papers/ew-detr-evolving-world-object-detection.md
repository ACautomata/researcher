---
title: EW-DETR: Evolving World Object Detection via Incremental Low-Rank DEtection TRansformer
type: paper
domain: object-detection
status: active
created: 2026-05-30
updated: 2026-05-30
tags:
  - open-world-object-detection
  - incremental-learning
  - domain-adaptation
  - detr
  - lora
  - exemplar-free
  - unknown-detection
paper:
  title: "EW-DETR: Evolving World Object Detection via Incremental Low-Rank DEtection TRansformer"
  authors:
    - Munish Monga
    - Vishal Chudasama
    - Pankaj Wasnik
    - C.V. Jawahar
  year: 2026
  venue: arXiv:2602.20985
  arxiv: "2602.20985"
  doi: ""
  code: ""
  project: ""
classification:
  label: object-detection
  task:
    - incremental object detection
    - open-world object detection
    - unknown detection
    - domain-incremental object detection
  method_family:
    - DETR-based
    - LoRA
    - exemplar-free incremental learning
  modality:
    - image
  datasets:
    - Pascal VOC
    - Clipart
    - Watercolor
    - Comic
    - BDD-100k
    - FoggyCityscapes
    - Adverse-Weather
  metrics:
    - mAP
    - mAP@0.5
    - U-Recall
    - WI (Wilderness Impact)
    - A-OSE (Absolute Open-Set Error)
    - FOGS (Forgetting-Openness-Generalisation Score)
    - FSS (Forgetting Sub-Score)
    - OSS (Openness Sub-Score)
    - GSS (Generalisation Sub-Score)
evidence_level: full-paper
raw_sources:
  - raw/sources/2026-02-20-ew-detr-evolving-world-object-detection-fulltext.txt
related_pages: []
---

## Citation

Munish Monga, Vishal Chudasama, Pankaj Wasnik, C.V. Jawahar. "EW-DETR: Evolving World Object Detection via Incremental Low-Rank DEtection TRansformer." arXiv:2602.20985v2, 2026.

## One-Sentence Contribution

提出 Evolving World Object Detection (EWOD) 新范式，将增量学习、域自适应、未知目标检测三者统一在 exemplar-free 约束下，并设计 EW-DETR 框架——通过 Incremental LoRA Adapters、Query-Norm Objectness Adapter 和 Entropy-Aware Unknown Mixing 三个模块在 DETR 检测器上实现该范式，同时在 Pascal Series 和 Diverse Weather 两个 benchmark 上引入 FOGS 综合评估指标，EW-DETR (RF-DETR) 平均 FOGS 达到 52.33，相对次优方法 ORTH (FOGS 33.28) 提升 57.24%。

## Problem Setting

EWOD 定义了一个 T 步任务序列，每步任务 t 提供来自新域 D_t 的数据集 X_t，并引入一组互不相交的新类别 K_t。训练时仅标注当前任务的已知类 K_t，先前学过的类别 K_{1:t-1} 和真正的未知类 U_t 在训练集中没有标注。评估时检测器需要同时：(1) 在所有见过的域 {D_1, ..., D_t} 中检测所有已知类 K_{1:t}；(2) 将未见过的目标检测为 "unknown"；(3) 在后续任务中逐步学习之前标记为 unknown 的类别；(4) 以上全部在不存储任何历史数据（exemplar-free）的条件下完成。

该范式将三个已有研究线耦合在一起：Open-World Object Detection (OWOD) 关注增量类学习和未知检测但假设单一静态域且依赖 exemplar replay；Class-Incremental Object Detection (CIOD) 处理新类但依赖 replay 和知识蒸馏；Domain-Incremental Object Detection (DIOD) 处理域迁移但在闭集标签空间下运行；DuIOD 同时处理类和域增量但仍为闭集（无显式 unknown 建模）。EWOD 首次要求检测器在无回放条件下同时应对类增量、域迁变和开放集识别。

## Method

EW-DETR 基于 DETR 系列检测器（Deformable DETR、RF-DETR），在冻结 backbone 和 transformer encoder-decoder 权重的前提下，通过三个模块解决 EWOD：

**1. Incremental LoRA Adapters（增量低秩适配器）**

针对 transformer encoder 和 decoder 的所有线性层，为每层维护两个低秩适配器（rank r=16）：

- Aggregate LoRA Adapter (ΔW^{t-1}_{agg})：不可训练的缓冲区，积累任务 T_1 至 T_{t-1} 的压缩知识。
- Task-Specific LoRA Adapter (ΔW^t_{task})：仅当前任务可训练的参数，捕捉任务特定的类/域迁移。

每步训练仅更新 Task-Specific Adapter 和检测头。任务结束后，通过 data-aware merging 合并两个 adapter：

- 合并系数 β_t 根据当前任务样本数 N_t 与历史累积样本数 N_{1:t-1} 的比率动态计算（β_t = β_max - (β_max - β_min) * N_t/N_{1:t-1}，β_min=0.2, β_max=0.8），样本较少的任务获得更大权重以避免被数据丰富的任务淹没。
- 合并后的矩阵通过截断 SVD 投影回 rank r 并存储为新的 Aggregate LoRA Adapter。
- Task-Specific Adapter 重置为零，准备下一任务。

该设计使可训练参数量相比标准 Deformable DETR 方法减少 98.1%（EW-DETR D-DETR: 0.46M；EW-DETR RF-DETR: 1.8M）。

**2. Query-Norm Objectness Adapter（查询归一化目标性适配器）**

利用 DETR decoder 的 class-agnostic query 特征来估计 objectness 并暴露 unknown 目标，无需任何辅助监督或额外损失。

- 对最后一层 decoder 特征 h_i 先 LayerNorm 再 l2 归一化，得到方向向量 h_norm（对域特定的协变量偏移不敏感）。
- 分类特征 h_cls = (1-α_mix) * h_i + α_mix * h_norm，α_mix 为可学习混合系数。
- 将标量范数 ||h_i||_2 通过 objectness head f_obj 后进行温度缩放 z_obj = f_obj(||h_i||_2) / (τ + ε)。

其核心假设经实验验证：匹配到真实框的 query 的 l2 范数始终高于未匹配的背景 query（T1 中 12.309 vs 12.129，T2 中 12.305 vs 12.125），提供跨任务的持久 class-agnostic objectness 信号。

**3. Entropy-Aware Unknown Mixing（熵感知未知混合）**

将分类不确定性和 objectness 结合为校准后的 unknown 分数。

- 基于 objectness 的 unknown 概率：p_unk_obj = σ(z_obj) * (1-p_known_max)^γ，其中 p_known_max 为已知类的最大置信度，γ 为可学习的温度参数。
- 基于分类器的 unknown 概率：p_unk_cls = σ(z_unk + b_obj)。
- 最终 unknown 概率通过可学习混合权重 α 融合：p_unk_final = α * p_unk_cls + (1-α) * p_unk_obj。
- 同时对已知类 logit 施加与 objectness-driven unknown score 成比例的软抑制，避免高不确定性、高 objectness 的 query 被 softmax 强制归入已知类。

所有参数通过标准检测损失端到端训练，无需显式 unknown 监督。

## Experiments

**数据集**

1. Pascal Series（两阶段）：
   - Pascal VOC [1:10] → Clipart [11:18]：T1 10 类（8909 张训练图像，16181 标注），T2 8 类（165 张训练图像，270 标注）。测试集 T1: 6041 张，T2: 7774 张。
   - Pascal VOC [1:10] → Watercolor [11:14]：T1 同上，T2 4 类（1072 张训练图像，1661 标注）。
   - Pascal VOC [1:10] → Comic [11:14]：T1 同上，T2 4 类（1150 张训练图像，3214 标注）。
   - dog 和 person 两类在所有任务中不参与训练，作为固定的 unknown 先验池。

2. Diverse Weather Series（多阶段，5 种天气条件，7 个共同目标类别，源自 BDD-100k、FoggyCityscapes 和 Adverse-Weather）：
   - 三阶段：Daytime Sunny [1:2] → Night Sunny [3:4] → Night Rainy [5:6]
     - T1: 4709 张图像，6772 标注
     - T2: 18459 张图像，169460 标注
     - T3: 471 张图像，1341 标注
   - 三阶段：Daytime Sunny [1:2] → Daytime Foggy [3:4] → Dusk Rainy [5:6]
   - 两阶段变体：Day→Night、Day→Night Rainy、Day→Day Foggy、Day→Dusk Rainy
   - truck 类在所有任务中不参与训练，作为固定的 unknown 先验池。

**Baseline 方法（全部在 EWOD 协议下重新实现）**

- ORE-EBUI [17] (CVPR 2021) — Faster RCNN 底层
- OW-DETR [11] (CVPR 2022) — Deformable DETR 底层
- PROB [48] (CVPR 2023) — Deformable DETR 底层
- CAT [23] (CVPR 2023) — Deformable DETR 底层
- ORTH [36] (CVPR 2024) — RandBox 底层
- DuET [26] (ICCV 2025) — Deformable DETR 底层（额外加入 EBUI 处理 unknown）
- OWOBJ [45] (CVPR 2025) — Deformable DETR 底层
- EW-DETR D-DETR (Deformable DETR 底层) 和 EW-DETR RF-DETR (RF-DETR-N 底层)

**训练设置**

- Backbone：DINO 预训练 ResNet-50（D-DETR 变体），DINOv2-S（RF-DETR 变体）
- 优化器：AdamW
- 学习率：1e-4（初始）
- Weight decay：1e-4
- Batch size：16
- 每任务训练 100 epochs
- 硬件：单卡 NVIDIA H100 80GB
- LoRA rank r = 16
- 合并系数边界 (β_min, β_max) = (0.2, 0.8)
- 所有方法使用单一 encoder-decoder 层（标准六层下 Deformable DETR 方法在 EWOD 中 mAP 崩溃至接近零）

**评估协议**

每步任务 t 评估时：检测器需检测所有已学类别 K_1 ∪ ... ∪ K_t（跨越所有见过的域 D_1 ∪ ... ∪ D_t）并将未见目标识别为 "unknown"。unknown 类别（dog、person 或 truck）在所有任务训练中完全保留，确保评估中 unknown 先验池固定且不泄露。

**评估指标**

- mAP@0.5：标准目标检测精度
- U-Recall：unknown 召回率
- WI (Wilderness Impact)：unknown 存在时对已知类精度的冲击
- A-OSE (Absolute Open-Set Error)：unknown 被误分为已知类的绝对计数
- FOGS (Forgetting-Openness-Generalisation Score)：综合分数 = (FSS + OSS + GSS) / 3
  - FSS (Forgetting Sub-Score)：衡量对以前学过类别的保留能力
  - OSS (Openness Sub-Score)：结合 U-Recall、(1-WI) 和归一化 A-OSE
  - GSS (Generalisation Sub-Score)：衡量当前任务类别跨所有已见域的泛化能力

**消融设置**

在 Pascal VOC [1:10] → Clipart [11:18] 上对 RF-DETR 底层的每个模块进行逐模块消融：
- Baseline (仅 RF-DETR)
- + Task-Specific LoRA only (简单 PEFT，无聚合)
- + Dual LoRA (无 merging/SVD)
- + Incremental LoRA (含 SVD merging)
- + QNorm-Obj only
- + Incremental LoRA + QNorm-Obj
- + Incremental LoRA + QNorm-Obj + EUMix (完整 EW-DETR)

## Results

**主要结果（Pascal Series: VOC [1:10] → Clipart [11:18]，Table 1）**

EW-DETR RF-DETR 在 FOGS 上达到 61.08，在所有方法中最高。次优方法 ORTH 的 FOGS 为 29.78，gap = 31.30。EW-DETR RF-DETR 的各子分数：FSS 96.19（最佳），OSS 78.62（最佳），GSS 8.42。

完整对比 EW-DETR RF-DETR vs. 最强 baseline (ORTH)：
- EW-DETR RF-DETR: FSS 96.19, OSS 78.62, GSS 8.42, FOGS 61.08
- ORTH: FSS 5.83, OSS 51.06, GSS 32.44, FOGS 29.78
- PROB (最高 OSS 但无保留): FSS 0, OSS 67.58, GSS 0.27, FOGS 22.62
- DuET (exemplar-free 但闭集): FSS 41.05, OSS 35.49, GSS 1.46, FOGS 26.00

**跨 benchmark 平均结果（Figure S4）**

在所有 9 个 EWOD 实验配置上平均：

- EW-DETR RF-DETR: 平均 FOGS 52.33（FSS 75.69, OSS 67.3, GSS 14.02）
- 次优 ORTH: 平均 FOGS 33.28（FSS 2.86, OSS 59.08, GSS 37.91）
- PROB: 平均 FOGS 24.73（FSS 0.61, OSS 66.67, GSS 6.92）
- 所有 replay 依赖的 OWOD 方法（ORE、OW-DETR、CAT、OWOBJ）FSS 接近零

EW-DETR RF-DETR 相对 ORTH 的 FOGS 提升为 57.24%。

**Pascal Series 两阶段变体（Table 2）**

- VOC → Watercolor: EW-DETR RF-DETR FOGS 65.88 (FSS 98.96, OSS 58.17, GSS 40.5)
- VOC → Comic: EW-DETR RF-DETR FOGS 62.7 (FSS 98.51, OSS 56.68, GSS 32.91)

**Diverse Weather 多阶段（Table 2）**

- Daytime Sunny → Night Sunny → Night Rainy: EW-DETR RF-DETR FOGS 55.25 (FSS 73.63, OSS 73.43, GSS 18.68)
- Daytime Sunny → Daytime Foggy → Dusk Rainy: EW-DETR RF-DETR FOGS 55.56 (FSS 82.80, OSS 65.75, GSS 18.13)

**Diverse Weather 两阶段（Table 3）**

EW-DETR RF-DETR 在四个域迁移上的 FOGS 范围 47.27-52.76。最高配置 Day→Night Rainy: FOGS 52.76。

**消融结果（Table 4，Pascal Series VOC→Clipart）**

- Baseline (RF-DETR): FSS 7.52, OSS 30.93, GSS 30.8672, FOGS 30.8672 (not reported in the source — GSS and FOGS values are identical in source text likely due to OCR artifact)
- + Incremental LoRA Adapters: FSS 从 7.52 升至 98.11，T2 Prev. Known mAP 从 5.81 恢复至 74.85；但 T2 Curr. Known mAP 从 51.49 降至 0.07（稳定性代价）；可训练参数减少 94.2%
- + QNorm-Obj: FSS 保持 97.78，GSS 提升（来自 T2 Curr. Known mAP 回升），未知检测有所改善
- + EUMix（完整 EW-DETR）: FSS 96.19, OSS 78.62, GSS 8.42, FOGS 61.08

**消融关键 delta：**
- Incremental LoRA 的 FSS delta：98.11 - 7.52 = +90.59
- EUMix 的 OSS delta（相对于 LoRA+QNorm-Obj）：78.62 - 42.04 = +36.58

**超参数消融**

- LoRA rank r：FOGS 在 r=16 处峰值 61.08；r 增大导致 GSS 下降（过拟合）；FSS 在 r=4-64 范围内稳定（94.95-97.86）
- 合并边界 (β_min, β_max)：固定 β=0.5 导致 GSS 崩溃至 0.02、FOGS 降至 54.04；(0.2, 0.8) 达到最优平衡 FOGS 61.08

**未知检测详细指标（Table S6）**

EW-DETR RF-DETR:
- T1: U-Recall 77.35, WI 0.012, A-OSE 12773
- T2: U-Recall 78.23, WI 0.0038, A-OSE 2251
- WI 在两个任务中均为所有方法最低，表明 unknown 存在时对已知类精度的影响最小

**计算效率（Table S4）**

- EW-DETR RF-DETR: 1.8M 可训练参数，32.22 GFLOPs，57.38ms 推理，0.32GB 显存
- EW-DETR D-DETR: 0.46M 可训练参数，171.23 GFLOPs，131.92ms 推理，1.55GB 显存
- 对比 ORE: 32.96M 参数，1665.03 GFLOPs；ORTH: 105.9M 参数，2073.57 GFLOPs

## Limitations

1. 域泛化子分数 GSS 相对较低（EW-DETR RF-DETR 平均 GSS 14.02，而 ORTH 达到 37.91），表明在 exemplar-free 约束下的跨域迁移仍是 EWOD 中最薄弱的维度。
2. 当新任务具有极少样本时（如 Diverse Weather T3 Night Rainy 仅 471 张训练图像），GSS 波动较大——随机任务排列实验显示 GSS 标准差为 4.81。
3. 方法要求 DETR 系列检测器作为底层架构，不支持 Faster R-CNN 等其他检测架构。
4. 论文中部分结果依赖于单一 encoder-decoder 层配置（标准六层在 EWOD 下崩溃），可能限制模型表达能力。
5. 论文未提供公开代码链接（not reported in the source）。

## Reusable Claims

- Claim: 在 exemplar-free 约束下同时处理类增量、域迁变和未知检测，FOGS 可作为综合评估指标，EW-DETR RF-DETR 在所有 9 个实验配置上平均 FOGS 52.33。
  Evidence: Figure S4，跨所有 Pascal Series 和 Diverse Weather benchmark 的平均结果。
  Scope: DETR 系列检测器，Pascal Series 和 Diverse Weather 协议，exemplar-free 设定。
  Confidence: high.

- Claim: Incremental LoRA Adapters（双 adapter + data-aware merging + 截断 SVD）能在无回放条件下有效缓解灾难性遗忘，FSS 从 7.52 提升至 98.11。
  Evidence: Table 4 消融，"Incremental LoRA Adapters" 行，Pascal VOC→Clipart 基准。
  Scope: DETR 架构，rank r=16，(β_min, β_max)=(0.2, 0.8)。
  Confidence: high.

- Claim: data-aware merging 优于固定系数合并，固定 β=0.5 导致 GSS 崩溃至 0.02、FOGS 降至 54.04。
  Evidence: Figure S5b，hyperparameter sensitivity analysis。
  Scope: Diverse Weather 数据集。
  Confidence: medium（单一 benchmark 验证）。

- Claim: decoder query 的 l2 范数提供跨任务的稳定 class-agnostic objectness 信号，matched query norm > unmatched query norm，ROC-AUC 约 0.585-0.587。
  Evidence: Figure S2，histogram of query norms。
  Scope: DETR 架构 decoder queries。
  Confidence: medium（仅一个 benchmark 上的观测，ROC-AUC 接近随机水平 0.5 仅略高）。

- Claim: 所有标准 OWOD 方法（ORE、OW-DETR、CAT、OWOBJ）在 exemplar-free 条件下 FSS 接近零，严重依赖 exemplar replay。
  Evidence: Figure S4，"all OWOD methods exhibit near-zero forgetting scores"。
  Scope: EWOD 协议下的重新实现。
  Confidence: high.

## Connections

- 与 [Open-World Object Detection](OWOD) 的关系：EWOD 将 OWOD 从单一静态域、依赖 exemplar replay 的设定扩展为多域、exemplar-free 设定。EW-DETR 是首个无需存储历史数据即可在 OWOD 场景下运行的 DETR 框架。ORE (CVPR 2021)、OW-DETR (CVPR 2022)、PROB (CVPR 2023)、CAT (CVPR 2023)、ORTH (CVPR 2024)、OWOBJ (CVPR 2025) 是该线上的代表性工作。
- 与 [DuET / DuIOD](dual-incremental-object-detection) 的关系：DuET (ICCV 2025) 首次提出类和域双重增量目标检测，但保持闭集假设（无 unknown 建模）。EW-DETR 由同一作者组提出，在 DuET 基础上加入开放集能力。
- 与 [Incremental LoRA / Continual LoRA](continual-lora) 的关系：EW-DETR 的 Incremental LoRA Adapters 设计借鉴了 continual learning 中 LoRA 的用法（如 CL-LoRA、SD-LoRA），但引入 data-aware merging 来应对 EWOD 特有的任务间严重数据不平衡。
- 与 [DETR-based Object Detection] 的关系：方法基于 Deformable DETR 和 RF-DETR，利用了 DETR decoder queries 的 class-agnostic 特性。RF-DETR 变体凭借其高效的神经架构搜索设计，仅需 32.22 GFLOPs 即可在 EWOD 中运行。

（注：以上连接的 target 页面在 wiki 中尚不存在，为后续 ingest 和交叉链接提供方向。）

## Open Questions

1. 在 GSS 维度的 significant improvement 路径是什么？当前的 data-aware merging 和 QNorm-Obj 对域泛化的贡献有限（平均 GSS 14.02），是否存在专门针对跨域特征的补充模块？
2. EW-DETR 的方法设计是否适用于非 DETR 架构（如 YOLO 系列、Faster R-CNN 系列）？Query-Norm 和 EUMix 模块强依赖 DETR decoder queries 的 class-agnostic 特性。
3. 当 unknown 类别的语义分布与已知类接近时（例如新类型的 vehicle vs. 已见过的 car），objectness-based unknown detection 是否会失效？
4. FOGS 的三个子分数（FSS/OSS/GSS）之间的 trade-off 关系如何？是否可能存在一个 Pareto 前沿供实际部署选择？
5. 论文未讨论 unknown detection 的阈值选择——在真实部署中如何确定 unknown 的决策阈值？

## Provenance

- 原始来源：arXiv:2602.20985v2（2026-02-20 提交，2026-04-02 修订）
- 全文提取：`raw/sources/2026-02-20-ew-detr-evolving-world-object-detection-fulltext.txt`（PyMuPDF 提取，含完整正文 18 页及附录 A-H）
- 证据等级：full-paper（全文 18 页 + 补充材料，包含所有表格、消融、附录）
- 元数据完整性：arXiv ID 已记录，DOI 和代码链接在原文中未提供
- 本页面基于全文提取，未经独立复现
