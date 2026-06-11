---
title: "ConceptGraphs: Open-Vocabulary 3D Scene Graphs for Perception and Planning"
tags:
  - scene-graph-generation
  - 3d-scene-graph
  - open-vocabulary
  - robot-perception
arxiv: "2309.16650"
created: 2026-06-10
source: https://arxiv.org/pdf/2309.16650
confidence: full-paper
authors:
  - Qiao Gu
  - Ali Kuwajerwala
  - Sacha Morin
  - et al.
venue: RSS 2024
---

## Paper Info

开放词汇 3D 场景图。SAM+CLIP → 3D 投影 → LLaVA caption → GPT-4 关系推理。无需训练数据。

## Method

SAM mask → CLIP/DINO feat → 3D 投影关联(几何+语义)[δsim=1.1] → LLaVA caption(10 views) → GPT-4 关系(MST剪枝) → JSON → LLM 规划

## Key Results

**Scene Graph**: 节点精度 0.71, 边精度 0.91 (Replica + AMT)
**Semantic Seg**: mAcc 40.63, F-mIoU 35.95 (vs ConceptFusion 31.53/31.31)
**Object Retrieval**: LLM 否定式查询 R@1=0.80 vs CLIP 0.26
**Robot**: Jackal 导航 + Spot 抓取 + AI2Thor 定位, 成功率 77.27%

## Provenance

- **Source**: arXiv 2309.16650
- **Evidence level**: full-paper
