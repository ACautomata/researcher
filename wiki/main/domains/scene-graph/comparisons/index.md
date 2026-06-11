# SGG Comparisons

> 方法对比与跨论文比较矩阵。

## 去偏方法对比

| 方法 | 年份 | 核心机制 | 类别不平衡？ | 上下文不平衡？ | 因果框架？ | P/SG 报告数 |
|------|------|---------|-------------|---------------|-----------|------------|
| [[unbiased-scene-graph-generation-tde-causal-modeling|TDE]] | 2020/23 | Total Direct Effect 因果解耦 | ✅ 隐含 | ❌ | ✅ | 3 |
| [[compositional-feature-augmentation-for-unbiased-scene-graph-generation|CFA]] | 2023 | 特征增强（组合空间） | ✅ | ❌ | ❌ | 3 |
| [[eicr-environment-invariant-curriculum-relation-learning-sgg|EICR]] | 2023 | 环境不变 + 课程学习 | ✅ | ✅ | ❌ | 3 |
| [[camodule-causal-adjustment-module-debiasing-scene-graph-generation|CAModule]] | 2025 | 三元组级因果调整 | ✅ | ❌ | ✅ | 2 |
| [[reverse-causal-framework-sgg|RcSGG]] | 2025 | 反向因果推理 | ✅ | ❌ | ✅ | 3 |
| [[hilo-exploiting-high-low-frequency-for-unbiased-panoptic-scene-graph-generation|HiLo]] | 2023 | 高低频分支 + Panoptic | ✅ | ❌ | ❌ | 2 |
| [[sbg-fine-grained-sgg-sample-level-bias-prediction|SBG]] | 2024 | 样本级偏置预测 | ✅ | ❌ | ❌ | 3 |
| [[adtrans-adaptive-data-transfer-panoptic-scene-graph-debiasing|AdTrans]] | 2024 | 自适应数据迁移 VG→PSG | ✅ | ❌ | ❌ | 1 |
| [[sgg-r3-from-next-token-prediction-to-e2e-unbiased-sgg|SGG-R/3]] | 2026 | Next-token → 无偏 SGG | ✅ | ❌ | ❌ | 3 |
| [[salience-sgg-unbiased-scene-graph-generation-via-salience-estimation|Salience-SGG]] | 2025 | 迭代显著性估计筛选 | ✅ | ❌ | ❌ | 3 |

## 端到端 SGG 方法对比

| 方法 | 年份 | 架构 | 参数量 | 特点 |
|------|------|------|--------|------|
| [[sgtr-end-to-end-scene-graph-generation-transformer|SGTR]] | CVPR 2022 | Transformer | ~63M | 首篇端到端 SGG Transformer |
| [[reltr-relation-transformer-scene-graph-generation|RelTR]] | CVPR 2022 | Transformer | — | 关系感知 DETR |
| [[dsgg-dense-relation-transformer-end-to-end-scene-graph-generation|DSGG]] | CVPR 2023 | Dense Relation Transformer | — | 密集关系编码 |
| [[hydra-sgg-hybrid-relation-assignment-one-stage|Hydra-SGG]] | ICLR 2025 | Hybrid Assignment | — | 多分支混合指派，10× 收敛加速 |
| [[egtr-extracting-graph-from-transformer-sgg|EGTR]] | CVPR 2024 | DETR → Graph | 42.5M | 最轻量端到端 |

## 开放词汇 / Open-Set SGG 对比

| 方法 | 年份 | OV？ | 核心机制 | 指标亮点 |
|------|------|------|---------|---------|
| [[language-supervised-open-vocabulary-scene-graph-vs3|VS3]] | CVPR 2024 | ✅ | CLIP 引导 + 语言监督 | VG zR@100=7.6 |
| [[cage-sgg-counterfactual-active-graph-evidence-open-vocabulary-sgg|CAGE-SGG]] | 2025 | ✅ | 反事实图证据 + CLIP | VG zR@100=7.9 |
| [[relic-sgg-relation-lattice-completion-open-vocabulary-sgg|ReLIC-SGG]] | 2025 | ✅ | 关系格补全 | VG OV-GCIs > 先验 |
| [[openpsg-open-set-panoptic-scene-graph-mllm|OpenPSG]] | ECCV 2024 | ✅ Open-Set | MLLM 开放集检测 | PSG open PredCls mR@100=46.0 |
| [[ovsgtr-expanding-scene-graph-boundaries|OvSGTR]] | 2024 | ✅ 统一 OV | 概念对齐 + 保留 | VG PredCls R@50=63.5, zR@100=5.9 |
| [[pixels-to-graphs-open-vocabulary-sgg-vlm|Pixels-to-Graphs]] | CVPR 2025 | ✅ | VLM 知识蒸馏 | VG PredCls mR@50=22.2, zR@50=10.7 |
| [[scene-graph-vit-open-vocabulary-vrd|Scene-Graph ViT]] | 2024 | ✅ | CLIP ViT + 关系注意力 | VRD zR@50=76.1 |
| [[sdsgg-scene-specific-description-ovsgg|SDSGG]] | 2024 | ✅ | LLM role-playing | VG zR@50=14.2 |
| [[acc-interaction-centric-knowledge-infusion-sgg|Interaction-Centric]] | AAAI 2025 | ✅ | CLIP 关系知识注入 | VG zR@50=10.4 |
| [[flowsg-progressive-image-conditioned-scene-graph-flow-matching|FlowSG]] | 2024 | ✅ | 条件流匹配 | VG PredCls mR@50=24.2 |

## 视频 SGG 方法对比

| 方法 | 年份 | 核心机制 | 指标亮点 |
|------|------|---------|---------|
| [[tempura-unbiased-video-scene-graph-generation|TEMPURA]] | CVPR 2022 | 解耦推理 | VidOR mR@50=20.44 |
| [[oed-one-stage-end-to-end-dynamic-scene-graph-generation|OED]] | CVPR 2023 | 一阶段端到端 | AG mR@50=24.3 |
| [[hyperglm-hypergraph-for-video-scene-graph-generation-and-anticipation|HyperGLM]] | AAAI 2023 | 超图 + 长短程关联 | VidOR R@50=33.0 |
| [[thyme-temporal-hierarchical-cyclic-interactivity-for-video-scene-graphs|THYME]] | AAAI 2024 | 层次循环交互 | AG R@50=56.4 / mR@50=31.5 |
| [[diffvsgg-diffusion-driven-online-video-scene-graph-generation|DIFFVSGG]] | ECCV 2024 | 扩散模型在线生成 | AG R@50=56.1 / mR@50=31.6 |
| [[mosa-motion-guided-semantic-alignment-dynamic-scene-graph-generation|MOSA]] | AAAI 2025 | 运动引导语义对齐 | AG R@50=57.2 / mR@50=32.4 |
| [[gtr-grafting-then-reassembling-dynamic-scene-graph-generation|GTR]] | IJCAI 2024 | 嫁接重组（时间+空间） | AG R@50=55.7 / mR@50=30.8 |
| [[salient-temporal-encoding-dynamic-sgg|STE]] | IJCAI 2023 | 显著性时序编码 | AG R@50=56.9 |
| [[fremure-frequency-guided-multi-level-reasoning-video-sgg|FReMuRe]] | 2025 | 频率引导多级推理 | AG R@50=57.5 / mR@50=31.5 |
| [[cyclo-cyclic-graph-transformer-video-sgg|CYCLO]] | NeurIPS 2024 | 循环注意力（航拍） | SynADL mR@50=58.7 |

## 3D SGG 方法对比

| 方法 | 年份 | 输入 | 核心机制 | 指标亮点 |
|------|------|------|---------|---------|
| [[open3dsg-open-vocabulary-3d-scene-graphs-from-point-clouds|Open3DSG]] | CVPR 2025 | 点云 | CLIP 查询优化 | 3DSSG SGCls R@50=49.1 |
| [[ccl-3dsgg-clip-driven-open-vocabulary-3d-scene-graph-generation|CCL-3DSGG]] | 2025 | 点云 | CLIP 跨模态对齐 | 3DSSG zR@50=39.7 |
| [[zing-3d-zero-shot-incremental-3d-scene-graphs|ZING-3D]] | 2025 | RGB-D 视频 | 零样本增量 | 3DSSG SGCls R@50=55.6 |
| [[gaussiangraph-3d-gaussian-scene-graph-generation|GaussianGraph]] | AAAI 2025 | 3DGS | 3D Gaussian 基 SGG | 3DSSG SGCls R@50=51.3 |
| [[sgr3-model-scene-graph-retrieval-reasoning-model-3d|SGR3]] | 2024 | 视频/3D | SG 检索 + 推理 | — |

## Panoptic SGG 方法对比

| 方法 | 年份 | 核心机制 | 指标亮点 |
|------|------|---------|---------|
| [[hilo-exploiting-high-low-frequency-for-unbiased-panoptic-scene-graph-generation|HiLo]] | CVPR 2023 | 高低频去偏 | PSG mR@50=27.3 |
| [[pair-net-panoptic-scene-graph-generation|Pair-Net]] | TPAMI 2024 | Pair Proposal | PSG mR@50=49.2 |
| [[openpsg-open-set-panoptic-scene-graph-mllm|OpenPSG]] | ECCV 2024 | MLLM 开放集 | PSG open PredCls mR@100=46.0 |
| [[dsflash-comprehensive-panoptic-scene-graph-generation-realtime|DSFlash]] | AAAI 2024 | 快速实时 PSG | PSG R@50=24.1 (62 FPS) |
| [[fair-ranking-new-model-panoptic-sgg|Fair Ranking]] | 2024 | SingleMPO + DSFormer | PSG mR@50=49.9 |

## LLM/VLM 辅助 SGG 对比

| 方法 | 年份 | 机制 | 依赖闭源？ |
|------|------|------|-----------|
| [[sdsgg-scene-specific-description-ovsgg|SDSGG]] | 2024 | GPT role-playing | ✅ |
| [[llm4sgg-weakly-supervised-scene-graph-generation|LLM4SGG]] | CVPR 2025 | 弱监督 LLM 标签 | ❌ 通用框架 |
| [[openpsg-open-set-panoptic-scene-graph-mllm|OpenPSG]] | ECCV 2024 | MLLM 开放集 | ❌ |
| [[visually-prompted-language-model-fine-grained-sgg-open-world|VLM-SGG]] | CVPR 2025 | 视觉提示语言模型 | ❌ |
| [[gpt4sgg-synthesizing-scene-graphs-llm|GPT4SGG]] | 2025 | GPT-4V → SGG | ✅ |
| [[pixels-to-graphs-open-vocabulary-sgg-vlm|Pixels-to-Graphs]] | CVPR 2025 | VLM 知识蒸馏 | ❌ |

## 高效率 / 实时 SGG 对比

| 方法 | 年份 | FPS | mR@50 | 架构 |
|------|------|-----|-------|------|
| [[react-real-time-efficient-sgg|REACT]] | 2024 | **1568** | 12.3 | DTS + Prototype |
| [[react-plus-plus-efficient-cross-attention-real-time-sgg|REACT++]] | 2025 | **2305** | — | 稀疏交叉注意力 |
| [[dsflash-comprehensive-panoptic-scene-graph-generation-realtime|DSFlash]] | 2024 | **62** (PSG) | 24.1 | 快速推理 |
| [[fast-contextual-scene-graph-generation|Fast Contextual]] | 2025 | 19~ | 18.2 | 无偏上下文增强 |
