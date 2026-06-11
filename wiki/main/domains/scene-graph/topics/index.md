# SGG Topics — Research Topics

> 场景图生成领域的主要研究专题。

## 🔬 专题索引

### 1. 去偏 SGG（Debiased SGG）
解决谓词长尾分布和上下文不平衡问题。

**相关论文**: TDE, EICR, CFA, CAModule, RcSGG, SBG, Salience-SGG, SGG-R/3, HiLo, VRT, Unbiased Heterogeneous
**方法家族**: Causal / Debiasing

### 2. 开放词汇 SGG（Open-Vocabulary SGG）
超越训练时封闭谓词集，泛化到未见过的谓词和对象。

**相关论文**: VS3, CAGE-SGG, ReLIC-SGG, OvSGTR, Pixels-to-Graphs, Scene-Graph ViT, SDSGG, FlowSG, Interaction-Centric, CCL-3DSGG, ELEGANT
**方法家族**: Open-Vocabulary / Zero-Shot

### 3. LLM/VLM 增强 SGG
利用大语言模型和视觉语言模型辅助 SGG。

**相关论文**: SDSGG, LLM4SGG, OpenPSG, VLM-SGG, GPT4SGG, Pixels-to-Graphs, SceneLLM, TSG Bench, SGG-R/3
**方法家族**: LLM & VLM Enhanced

### 4. 端到端 SGG（End-to-End SGG）
一次性预测对象和关系，避免级联误差。

**相关论文**: SGTR, RelTR, DSGG, Hydra-SGG, EGTR
**方法家族**: Transformer-Based

### 5. Panoptic SGG
用 panoptic segmentation mask 替代边界框的扩展 SGG。

**相关论文**: HiLo, Pair-Net, OpenPSG, DSFlash, Fair Ranking, AdTrans, VLPrompt
**方法家族**: Panoptic Scene Graph Generation

### 6. 视频 / 动态 SGG
处理时序场景图，包括关系预测和未来场景图预测。

**相关论文**: TEMPURA, OED, HyperGLM, THYME, DIFFVSGG, MOSA, GTR, FDSG, PSVG, SceneLLM, CYCLO, FReMuRe
**方法家族**: Video & Dynamic Scene Graph

### 7. 3D 场景图
从 3D 点云或 RGB-D 序列构建 3D 场景图。

**相关论文**: Open3DSG, CCL-3DSGG, ZING-3D, ConceptGraphs, GaussianGraph, SGR3, MA3DSG, Incremental 3D
**方法家族**: 3D Scene Graph Generation

### 8. 生成式 SGG（Generative SGG）
用扩散模型或流匹配生成场景图。

**相关论文**: Diff-VRD, DiScGraph, FlowSG, IS-GGT, SPADE
**方法家族**: Generative Models (Diffusion / Flow)

### 9. 因果 SGG（Causal SGG）
用因果推理分析和去偏 SGG。

**相关论文**: TDE, CAModule, RcSGG, CAGE-SGG
**方法家族**: Causal / Debiasing

### 10. 弱监督 / 零样本 SGG
减少标注依赖的方法。

**相关论文**: LLM4SGG, GPT4SGG, VS3, PALS, SSC-SGG, EM-Grounding
**方法家族**: Weakly & Semi-Supervised

### 11. 实时 SGG（Real-Time SGG）
追求推理速度的轻量 SGG 方法。

**相关论文**: REACT, REACT++, DSFlash, Fast Contextual, EGTR, UniQ
**方法家族**: Efficient / Real-Time

### 12. 知识增强 SGG（Knowledge-Enhanced SGG）
注入外部知识（常识、统计共现、图谱）提升 SGG。

**相关论文**: HiKER-SGG, CooK, RA-SGG, PE-Net, Multi-Prototype, Interaction-Centric, Commonsense Relations

### 13. 交互式 / 人机协同 SGG
用户参与引导的场景图生成。

**相关论文**: Click2Graph

### 14. SGG 在机器人 / 具身智能中的应用

**相关论文**: ConceptGraphs, Open3DSG, FunGraph, ZING-3D, VL-KnG, ESCA, SceneLLM

### 15. 数据集 / 基准

**相关论文**: SVG, SVG2, PSG, PVSG, HOIverse, FACTUAL, TSG Bench
