---
title: "VL-KnG: Persistent Spatiotemporal Knowledge Graphs from Egocentric Video"
tags:
  - scene-graph-generation
  - egocentric-video
  - spatiotemporal
  - embodied-qa
created: 2026-06-10
source: https://arxiv.org/pdf/2510.01483
confidence: full-paper
authors:
  - Mohamad Al Mdfaa
  - Svetlana Lukina
  - et al.
venue: arXiv v2 Mar 2026
---

## Paper Info

- **Title**: VL-KnG: Persistent Spatiotemporal Knowledge Graphs from Egocentric Video for Embodied Scene Understanding
- **Venue**: arXiv Mar 2026
- **Method**: Training-free, STOA + GER, Neo4j + SigLIP2

## Abstract

无需训练的持久时空知识图谱框架。STOA (LLM 语义关联) + GER (GraphRAG + SigLIP2 混合检索)。WalkieKnowledge 基准。查询延迟 ~0.8s，与视频长度无关。

## Method

**STOA**: LLM 语义相似度跨块关联物体身份（替代视觉跟踪）
**GER**: 图子图检索 + SigLIP2 视觉 grounding 混合

## Experiments

### WalkieKnowledge

| 方法 | Retr.@1 | Latency |
|------|:---:|:---:|
| VL-KnG (GER-G) | **65.80%** | **~0.8s** |
| Qwen 3.5+ | 66.32% | ~24s |
| Gemini 2.5 Pro | 68.91% | ~49s |

### OpenEQA

VL-KnG: LLM-Match 55.2 (vs Gemini 3 Flash 76.8, 但延迟低 13x)

### Robot Deployment

成功率 77.27% (vs RoboHop 27.27%)

## Results

- 训练自由，恒定时间查询
- 低成本硬件 (RTX 2060) 可运行
- GER 视觉 grounding 提升 12.6pp 检索

## Limitations

1. 细粒度空间推理受限（无 3D 几何）
2. 依赖 VLM 检测质量
3. 假设相对静态场景

## Provenance

- **Source**: arXiv 2510.01483
- **Evidence level**: full-paper
