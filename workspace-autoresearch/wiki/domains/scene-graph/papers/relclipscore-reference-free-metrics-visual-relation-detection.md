---
title: "Measuring Image-Relation Alignment: Reference-Free Evaluation of VLMs and Synthetic Pre-training for Open-Vocabulary Scene Graph Generation"
alias: RelCLIPScore
authors:
  - Maëlic Neau
  - Zoe Falomir
  - Cédric Buche
  - Akihiro Sugimoto
year: 2025
venue: arXiv
arxiv: https://arxiv.org/abs/2505.09201
code: null
doi: null
domain: scene-graph
tags:
  - scene-graph-generation
  - open-vocabulary
  - metric
  - reference-free
  - synthetic-data
  - VLM
  - RelCLIPScore
  - FG-OV-SGG
evidence_level: full-paper
status: active
source: raw/sources/2025-06-09-Measuring_Image_Relation_Alignment.pdf
---

# Measuring Image-Relation Alignment: Reference-Free Metrics for Visual Relation Detection

> Neau et al. (2025), Umeå University / CNRS / IMT Atlantique / NII.
> arXiv preprint, 2025.

## 核心贡献

1. **RelCLIPScore** — 首个用于 Open-Vocabulary SGG 的无参考（reference-free）评估指标。扩展 CLIPScore 到关系三元组级别，计算 `<subject, predicate, object>` 三元组与对应 union region（subject+object bbox 并集）的 CLIP 余弦相似度，并引入基于预测关系数量的惩罚项。
2. **VLM 关系预测能力评估** — 系统评估多种 VLM（LlaVa-OneVision 7B、InternVL3-8B、Qwen2.5VL 7B、GPT4o-mini、GPT4o）在区域级关系预测上的表现，揭示其在**大小不平衡对**、**远距离物体**、**逆关系方向**等方面的局限性。
3. **FG-OV SGG 数据集** — 利用 LlaVa-OneVision 7B 通过区域特定提示（region-specific prompting）生成的 200K 张图像的合成关系标注数据集，质量优于已有弱监督数据（RLIPv2）。

## RelCLIPScore 定义

- **CLIPScore(c, t) = max(cos(c, t), 0)** — 视觉嵌入 c 与文本嵌入 t 的余弦相似度
- **Image-level RelCLIPScore** — 图像内所有关系的 CLIPScore 平均值，加入对预测关系数量的惩罚
- **Ref-RelCLIPScore** — 结合预测与 ground truth 文本相似度的变体

## 实验与结果

### VLM 与图像-文本对齐模型评估（PSG 数据集）

| 模型 | Score | Precision | θ (Matching Score) |
|------|-------|-----------|-------------------|
| NegCLIP B-32 | 24.47 | 30.18 | **66.10** |
| CLIP L-14 | 23.64 | 27.77 | 63.14 |
| SIGLIP | 17.78 | 25.23 | 62.36 |
| BLIP2 | 67.38 | 24.19 | 62.29 |

**结论**：NegCLIP B-32 在关系级图像-文本对齐上最优（θ=66.10），SIGLIP 和 BLIP2 虽然更近期但在排序候选关系上表现更差。

### VLM 区域关系预测（PSG 测试集，零样本）

| 模型 | NegCLIP Score | Precision |
|------|--------------|-----------|
| LlaVa-OneVision 7B | **24.02** | 16.07 |
| InternVL3-8B | 23.94 | 30.97 |
| Qwen2.5VL 7B | 23.88 | 14.01 |
| GPT4o-mini | 24.00 | 16.23 |
| GPT4o | 23.97 | 18.05 |

**结论**：LlaVa-OneVision 7B 综合最优（NegCLIP 24.02），超越 GPT4o 系列闭源模型。Precision 指标波动大，不适合作为 VLM 评估的主要指标。

### 消融实验

**大小不平衡对**（box ratio < 1:5 vs > 1:5）：
- InternVL3-8B: NegCLIP 23.91 (Low) vs 24.15 (High)；Precision 29.22 vs 40.86
- LlaVa-OV-7B: NegCLIP 23.89 (Low) vs 24.11 (High)；Precision 10.65 vs 23.88
- **趋势**：大小不平衡导致所有指标显著下降

**远距离物体**（IoU < 0 vs IoU ≥ 0）：
- InternVL3-8B: NegCLIP 23.01 (Non-Intersect) vs 23.78 (Intersect)；Precision 30.08 vs 36.13
- LlaVa-OV-7B: NegCLIP 22.98 vs 24.01；Precision 3.7 vs 11.67
- **趋势**：远距离物体对关系预测带来严重性能下降

### FG-OV SGG 数据集质量

| 数据来源 | NegCLIP | CLIP | SIGLIP |
|---------|---------|------|--------|
| RLIPv2 (baseline) | 22.22 | 25.41 | 18.50 |
| **FG-OV (ours)** | **25.41** | **25.97** | **20.72** |

FG-OV 在 COCO 上生成 1,121 个不同谓词（vs RLIPv2 的 388 个），谓词分布更均衡、更细粒度。

### OV-SGG 迁移学习（HICO-DET）

| 数据混合 | UC-RF | UC-NF |
|---------|-------|-------|
| RLIPv2 | 15.88 / 26.00 / 23.98 | 18.87 / 19.87 / 19.67 |
| **FG-OV (ours)** | **16.99 / 25.92 / 24.12** | 18.77 / **21.27 / 20.77** |

- UC-RF Unseen: 16.99% vs 15.88% (+7.0% 相对提升)
- 所有指标平均提升 +3.5%
- 验证了预训练数据多样性对零样本泛化的重要性

## 关键发现

1. **NegCLIP 是关系级对齐的最佳文本编码器**，CLIP L-14 次之，SIGLIP/BLIP2 的反而不适合排序候选关系
2. **LlaVa-OneVision 7B 在零样本关系预测上超越 GPT4o 系列**，且为可本地部署的开源模型
3. **VLM 的三大局限**：大小不平衡对、远距离物体、逆关系方向（特别是人-物交互）
4. **区域特定提示（region-specific prompting）优于 全局图像级 VLM 标注**，生成的 FG-OV 数据比 RLIPv2 更细粒度、更多样化

## 与现有工作的关系

- 对比 [[cage-sgg-counterfactual-active-graph-evidence-open-vocabulary-sgg]]：CAGE-SGG 侧重解偏置训练策略，本文侧重评估指标和数据质量
- 对比 [[language-supervised-open-vocabulary-scene-graph-vs3]]：VS³ 侧重语言监督训练范式，本文侧重统一的参考指标
- 对比 [[ovsgtr-expanding-scene-graph-boundaries]]：OvSGTR 提出全开放词汇检测框架，本文提供评估这些框架的指标
- 对比 [[sdsgg-scene-specific-description-ovsgg]]：SDSGG 使用 LLM 角色扮演增强数据，本文使用 VLM 区域提示生成数据

## 待验证

- RelCLIPScore 在不同 VLM 作为骨干时的稳定性
- FG-OV 数据集在更多 OV-SGG 模型（如 OvSGTR、VS³）上的迁移效果
- 区域特定提示的计算成本优化（当前需遍历所有 <subject, object> 对）
