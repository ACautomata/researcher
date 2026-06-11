---
pageType: source
id: source.burnresu-2026
type: paper
title: "BurnResu: A Multi-Task Temporal Prediction Framework for Early Burn Resuscitation"
url: null
doi: null
authors: Xinyu Liu, Jingyuan Lang, Xiaoguang Lin, Haisheng Li, Ranran Sun, Xueliang Zhao, Qihan Wu, Zhiqiang Yuan, Ning Li, Gaoxing Luo
year: 2026
venue: "Expert Systems with Applications (submitted, ESWA-D-26-21224)"
tags: [burn-resuscitation, multi-task-learning, temporal-modeling, clinical-decision-support, deep-learning]
updatedAt: 2026-06-05
---

## Abstract

Burn shock is a leading cause of early mortality in patients with severe burns, and fluid resuscitation requires balancing the competing risks of hypoperfusion and fluid overload. BurnResu is a hierarchical temporal deep learning framework that jointly predicts fluid type and infusion rate for the first 72 hours after injury. Using retrospective data from 364 patients with severe burns, the model integrates baseline characteristics, hourly vital signs, and fluid-administration histories in a rolling prediction paradigm.

## Key Results

- Fluid-type classification: macro-AUC 0.816, macro-F1 0.696
- Infusion-rate estimation: MAE 27.44 mL/h, R² 0.820, RMSE 60.04 mL/h
- Outperforms ML baselines (GBR AUC 0.763), DL baselines (Transformer AUC 0.804), and traditional CDSS (Salinas MAE 76.8)

## Related Pages

- Paper analysis: `domains/healthcare-ai/papers/burnresu-multi-task-temporal-prediction-for-early-burn-resuscitation.md`

## Raw Files

- PDF: `sources/2026-BurnResu-Multi-Task-Temporal-Prediction-Framework-for-Early-Burn-Resuscitation.pdf`
- Extracted text: `sources/2026-BurnResu-Multi-Task-Temporal-Prediction-Framework-for-Early-Burn-Resuscitation.txt`

## Related
<!-- openclaw:wiki:related:start -->
- No related pages yet.
<!-- openclaw:wiki:related:end -->
