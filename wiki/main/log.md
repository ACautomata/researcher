# Wiki Change Log

## 2026-06-08

- **新建领域** `scene-graph` — 场景图生成与预测，包含 papers/, methods/, datasets/ 等子目录
- **入库 5 篇 SGG 论文** (CVPR/AAAI 2023):
  1. 3D Spatial Multimodal Knowledge Accumulation for Scene Graph Prediction in Point Cloud
  2. Fast Contextual Scene Graph Generation with Unbiased Context Augmentation
  3. Scalable Theory-Driven Regularization of Scene Graph Generation Models
  4. Unbiased Heterogeneous Scene Graph Generation with Relation-Aware Message Passing Neural Network
  5. Incremental 3D Semantic Scene Graph Prediction from RGB Sequences
- **来源文件**: sources/scene-graph/ 目录

## 2026-06-09 — SG-Adapter (ICCV 2025)

- **论文**: Scene Graph Guided Generation: Enable Accurate Relations Generation in Text-to-Image Models via Textural Rectification
- **文件**: `domains/scene-graph/papers/sg-adapter-scene-graph-guided-generation.md`
- **来源**: `sources/scene-graph/2025-ICCV-SG-Adapter-scene-graph-guided-generation.{pdf,txt}`
- **证据等级**: full-paper
- **关键结果**: SG-IoU=0.623 (vs SD 0.157), Relation Accuracy=77.6%, FID=26.2

## 2026-06-09 — CFA / Compositional Feature Augmentation (ICCV 2023)

- **论文**: Compositional Feature Augmentation for Unbiased Scene Graph Generation
- **文件**: `domains/scene-graph/papers/compositional-feature-augmentation-for-unbiased-scene-graph-generation.md`
- **来源**: `sources/scene-graph/2023-ICCV-Compositional-Feature-Augmentation-for-Unbiased-SGG.{pdf,txt}`
- **证据等级**: full-paper
- **关键结果**: VG PredCls CF+Motiifs mR@50=35.7 (baseline 16.5), Tail PredCls mR@100=43.0

## 2026-06-09 — CAGE-SGG (arXiv 2026)

...

[43 more entries of similar pattern omitted for brevity. All 90 papers were ingested on 2026-06-09.]

## 2026-06-10 — Wiki 结构重构

- **全局 index.md 更新**: 从旧版（仅 5 篇）升级为完整组织索引，覆盖全部 90 篇 SGG 论文
- **目录索引创建**: 为 domains/scene-graph/ 下 10 个子目录创建 index.md：
  - `methods/index.md` — 11 个方法家族分类（causal, generative, transformer, knowledge-enhanced 等）
  - `tasks/index.md` — 8 个任务类型分类（open-vocabulary, panoptic, video, 3D, unbiased 等）
  - `metrics/index.md` — 评价指标定义 + 相关论文
  - `datasets/index.md` — 常用数据集说明 + 相关论文
  - `concepts/index.md` — 关键概念定义（long-tail bias, context imbalance, counterfactual 等）
  - `comparisons/index.md` — Debiasing 方法对比表 + Causal 方法对比表
  - `analyses/index.md` — 研究空白分析框架
  - `topics/index.md` — 前沿主题梳理（Generative SGG, VLM/LLM, Causal SGG, 3D SGG）
  - `reading-notes/index.md`, `entities/index.md` — 骨架页
- **domains/scene-graph/index.md 更新**: 添加维度浏览链接表
- **变更说明**: 现在 90 篇论文可通过方法家族、任务类型、对比表格等多种维度检索，不再是平铺文件堆

## 2026-06-10 — Batch 9: 6 papers ingested (新流程: sub-agent→/tmp→main搬运)

- APT: Adaptive Prompt Tuning (ICLR 2026) — 通用 SGG plug-in
- UniQ: Unified Decoder (ACM MM 2024) — 高效 one-stage SGG
- CAFE: Curricular Shape-aware Features (arXiv 2024) — 全景 SGG 课程学习
- GPT4SGG: LLM-synthesized SGG (NeurIPS 2024) — GPT-4 分治策略
- INOVA: Interaction-Aware Open Vocab SGG (arXiv 2025) — 交互对象聚焦
- LLaVA-SpaceSGG: 3D Spatial MLLM SGG (arXiv 2024) — 空间关系增强

**流程改进**：发现 sub-agent 沙箱文件系统隔离，主机文件不落地。
改为 sub-agent 写 /tmp -> main agent 读取 -> write 工具写入 wiki。

## 2026-06-10 — Batch 10: 6 LLM/foundation-model papers ingested

- EM-Grounding (Hallucinate, Ground, Repeat) — arXiv Jun 2025, LLM+EM 弱监督 VRD
- PC-SGG (Conformal Prediction) — arXiv Mar 2025, 首次 CP+UQ for SGG
- CooK (Co-occurrence + TF-l-IDF) — ICML 2024, 共现知识长尾缓解
- SkySenseGPT — arXiv Jul 2024, 遥感关系理解指令微调
- SceneLLM — arXiv May 2025, LLM 隐式推理动态 SGG
- ELEGANT (Less is More) — arXiv Oct 2023, 零样本局部 SGG via 基础模型

**流程稳定**: sub-agent→/tmp→main write→wiki，每批 6 篇并行。

## 2026-06-10 — Batch 11: 6 core SGG papers (125 batch #1/21)

- CoPa-SG — arXiv Jun 2025, 密集场景图+参数化关系 (Univ. Augsburg)
- HOIverse — arXiv Jun 2025, 合成 HOI+SGG 数据集
- Relation-R1 — AAAI 2026, CoT+GRPO 全景 SGG (HKUST)
- LASER — ICLR 2025, 神经符号弱监督 STSG (UPenn)
- VL-KnG — arXiv Mar 2026, 持久时空知识图谱 from egocentric video
- ASMP — NeurIPS 2022, 2.5D 场景图音源分离 (UIUC/MERL)

## 2026-06-10 — Batch 12: 6 core SGG papers

- SVG (Synthetic Visual Genome) — arXiv Jun 2025, 146K图像/5.6M关系, ROBIN-3B
- HIERCOM — WACV 2025, 分层关系头+常识验证 (UPenn)
- MSG (Multiview Scene Graph) — NeurIPS 2024, 无位姿RGB→place+object拓扑图
- SPADE — arXiv Jul 2025, DDIM inversion+RGT开放词汇全景SGG
- ConceptGraphs — RSS 2024, 开放词汇3D场景图 (MIT, UdeM)
- FACTUAL — arXiv May 2023, 文本场景图解析benchmark + SoftSPICE

## 2026-06-10 — Batch 13: 6 core SGG papers

- VLPrompt — arXiv 2024, LLM 视觉语言提示 PSG (Tokyo/Airbus)
- Pair-Net — IEEE TPAMI 2024, Pair Proposal Network PSG (NTU)
- Fair Ranking PSGG — arXiv 2024, SingleMPO协议+DSFormer (Augsburg)
- ESCA — NeurIPS 2025, SGClip场景图增强体现代理 (UPenn/UCF)
- Scene-Graph ViT — arXiv 2024, 纯编码器开放词汇 VRD (Google DeepMind)
- CYCLO — NeurIPS 2024, 循环注意力航拍 VidSGG (Arkansas)

- REACT — arXiv 2024, 实时效率SGG
- Hydra-SGG — ICLR 2025, 混合关系指派
- OvSGTR — arXiv 2024, 全开放词汇SGG (VLPrompt同一组)
- EGTR — CVPR 2024, Transformer图提取 (注意: 原链接2401.02724指向不同论文, 正确ID 2404.02072)
- SGTR — CVPR 2022, 端到端Transformer SGG
- OpenPSG — ECCV 2024, 开放集全景SGG
