---
title: "SGTR: End-to-end Scene Graph Generation with Transformer"
tags:
  - scene-graph-generation
  - transformer
  - end-to-end
  - CVPR-2022
arxiv: "2112.12970"
created: 2026-06-10
source: https://arxiv.org/pdf/2112.12970
confidence: full-paper
authors:
  - Yao Teng
  - Limin Wang
  - et al.
venue: CVPR 2022
code: https://github.com/.../SGTR
---

## Paper Info

SGG 形式化为二部图构建（entity nodes + predicate nodes + graph assembling）。Entity-aware predicate representation + Structural Predicate Decoder。早期 Transformer SGG。

## Key Results

| 基准 | 指标 | SGTR |
|:---|:---:|:---:|
| OpenImages V6 | mR@50 | **42.61** (+2.28 vs BGNN) |
| VG (SGDet) | mR@100 | **15.2** |
| VG +cRT (长尾) | mR@100 | **21.6** (Tail 18.1) |
| Zero-shot | zR@100 | **5.8** |

推理 0.35s/image。图组装模块最关键：移除后 mR 从 17.3→7.0。

## Provenance

- **Source**: arXiv 2112.12970
- **Evidence level**: full-paper
