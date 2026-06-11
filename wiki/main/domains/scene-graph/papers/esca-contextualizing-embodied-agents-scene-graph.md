---
title: "ESCA: Contextualizing Embodied Agents via Scene-Graph Generation"
tags:
  - scene-graph-generation
  - embodied-agents
  - sgclip
  - NeurIPS-2025
arxiv: "2510.15963"
created: 2026-06-10
source: https://arxiv.org/pdf/2510.15963
confidence: full-paper
authors:
  - Jiani Huang
  - Amish Sethi
  - Matthew Kuo
  - et al.
venue: NeurIPS 2025
---

## Paper Info

SGClip + 选择性场景图接地增强 MLLM 体现代理。体现代理 69% 失败源于感知错误，ESCA 降至 30%。

## Key Results

| 环境 | MLLM | Base | +ESCA |
|------|:---:|:---:|:---:|
| EB-Nav | InternVL-2.5 | ~40 | **51.66** |
| EB-Mani | GPT-4o | 23.47 | **34.44** |
| EB-Habitat | Qwen2.5-VL | 33.33 | **56.33** |

SGClip 零样本 OpenPVSG/Action Genome/VidVRD 一致超越 CLIP。

## Provenance

- **Source**: arXiv 2510.15963
- **Evidence level**: full-paper
