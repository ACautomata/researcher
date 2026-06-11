---
title: "GPT4SGG: Synthesizing Scene Graphs from Holistic and Region-specific Narratives"
tags:
  - scene-graph-generation
  - llm
  - gpt4
  - weakly-supervised
  - NeurIPS-2024
created: 2026-06-10
source: https://arxiv.org/pdf/2312.04314
confidence: full-paper
authors:
  - Zuyao Chen
  - Jinlin Wu
  - Zhen Lei
  - Zhaoxiang Zhang
  - Changwen Chen
venue: NeurIPS 2024
---

## Paper Info

- **Title**: GPT4SGG: Synthesizing Scene Graphs from Holistic and Region-specific Narratives
- **Venue**: NeurIPS 2024
- **Code**: None
- **Datasets**: COCO@GPT (~94k images, ~394k triplets), VG@GPT (~47k images, ~227k triplets)

## Abstract

反转传统语言监督 SGG 管道——先定位物体，再分解场景为区域级描述，最后用 LLM 推理关系。OvSGTR + VG@GPT 在 VG150 测试集上 R@50=25.03, mR@100=8.22（接近全监督水平 8.98）。指令微调 Llama 2-13B 达到 GPT-4 的 99.8% 性能（12.06% vs 12.09%）。

## Method

三步分治：
1. **物体定位**：检测器或手动标注获取 (class, bbox)
2. **场景分解**：全局叙述（BLIP-2）+ 区域叙述（RoI，IoU>0 的对，最多 N=20）
3. **LLM 关系推理**：GPT-4 接收物体编码（`[class].[id]:[box]`）+ 叙述 → JSON 三元组

**指令微调**：LoRA 微调 Llama 2-13B 实现自主合成。

## Experiments

### 主结果（VG150）

| 方法 | 训练数据 | R@50 | R@100 | mR@50 | mR@100 |
|------|----------|:---:|:---:|:---:|:---:|
| VS3 (Swin-L) | VG Caption | 16.00 | 19.85 | 3.80 | 4.87 |
| OvSGTR (Swin-B) | VG Caption | 22.14 | 26.20 | 5.24 | 6.25 |
| VS3 (Swin-L) | **VG@GPT** | **22.42** | **25.29** | **5.82** | **6.97** |
| OvSGTR (Swin-B) | **VG@GPT** | **25.03** | **28.84** | **7.14** | **8.22** |
| OvSGTR (全监督) | VG150 | 36.40 | 42.40 | 7.41 | 8.98 |

### LLM 对比

- GPT-4: **12.09%** recall
- Llama 2-13B (指令微调): **12.06%** (>99% of GPT-4)
- 瓶颈在检测器（AR 56.8% → recall 3.11%）

## Results

- 弱监督 mR@100 接近甚至超过全监督基线
- 分治策略有效解决定位歧义
- 低成本私有化部署可行

## Limitations

1. 未利用多模态 LLM
2. 依赖 LLM 能力
3. 仅用 Recall 不全
4. 检测器瓶颈严重

## Provenance

- **Source**: arXiv 2312.04314
- **Evidence level**: full-paper
- **Status**: NeurIPS 2024
