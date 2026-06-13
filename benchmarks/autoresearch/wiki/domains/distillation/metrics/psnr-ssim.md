---
title: PSNR / SSIM — 图像质量评估
type: metric
domain: distillation
status: active
created: 2026-05-24
updated: 2026-05-24
tags:
  - image-quality
  - privacy-evaluation
  - reconstruction
source_pages:
  - wiki/domains/federated-learning/papers/fedsd2c-one-shot-fl-distiller-distillate.md
related_pages:
  - wiki/domains/federated-learning/methods/fedsd2c.md
---

# PSNR / SSIM — 峰值信噪比与结构相似性

## 定义

- **PSNR (Peak Signal-to-Noise Ratio)**：$PSNR = 10 \cdot \log_{10}(MAX_I^2 / MSE)$，单位为 dB。衡量重建图像与原始图像之间的像素级差异。越高表示越相似。
- **SSIM (Structural Similarity Index Measure)**：$SSIM(x, y) = [l(x,y)]^\alpha \cdot [c(x,y)]^\beta \cdot [s(x,y)]^\gamma$，综合考虑亮度（luminance）、对比度（contrast）、结构（structure）三个维度。值域 [0, 1]（或百分比），越高表示越相似。

在 wiki 的 FedSD2C 中，PSNR 和 SSIM 被倒置使用：**低 PSNR/SSIM = 更好的隐私保护**（合成 distillate 与原始图像差异大）。

## 解读

- **隐私评估上下文**：PSNR < 20dB + SSIM < 60% 表示合成数据在视觉上与原始数据差异显著——攻击者难以从 distillate 逆向重建可识别的原始图像。
- **权衡**：PSNR/SSIM 越低（隐私越好），通常 Acc 越低（性能越差）——Fourier 扰动的优势是在相近 PSNR/SSIM 下保持更高 Acc。
- **FedSD2C 中**：$\lambda=0.8$ 时 PSNR 16.42 / SSIM 50.80 vs. 无保护时 Acc 51.87→50.68（仅损失 1.19%）。

## 失效模式

- **与感知隐私不完全对应**：低 PSNR 的图像在人类看来可能仍可识别关键内容——PSNR 只衡量像素差异，不考虑语义级隐私。
- **不反映重构攻击能力**：攻击者可能不通过直接像素重建，而通过模型逆向（model inversion）或成员推断（membership inference）攻击——PSNR/SSIM 无法防御这些向量。
- **对低分辨率图像敏感**：32×32 图像（如 CIFAR）的 PSNR/SSIM 变化范围远小于高分辨率图像——可比性差。
- **SSIM 对结构变化的惩罚不均衡**：颜色偏移可能产生低 PSNR 但高 SSIM（结构保留），反之亦然。

## 使用者

| 论文 | 设置 | PSNR↓ | SSIM↓ | Acc |
|------|------|-------|-------|-----|
| FedSD2C | Fourier $\lambda=0.8$ (ImageNette) | 16.42 | 50.80 | 50.68 |
| FedSD2C | Laplace p=0.1 (ImageNette) | 24.02 | 81.66 | 48.61 |
| FedSD2C | FedMix (ImageNette) | 16.88 | 58.93 | 41.86 |

FedSD2C 在相近 PSNR/SSIM（隐私保护水平）下保持最高 Acc——Fourier 扰动比 Laplace 噪声和 FedMix 更有效地平衡隐私与性能。

## 关联

- [FedSD2C](../../federated-learning/methods/fedsd2c.md)：wiki 中 PSNR/SSIM 作为隐私评估 metric 的唯一使用者。
- [Accuracy](../../meta/metrics/accuracy.md)：在 FedSD2C 中与 PSNR/SSIM 构成隐私-性能 trade-off 的关键维度。

## 开放问题

- 更全面的隐私保护评估指标——结合 MIA AUC、PSNR/SSIM、语义相似度等多维度的标准化 protocol？
- PSNR/SSIM 对高分辨率（>256×256）和低分辨率（≤32×32）图像的可比性校准？
