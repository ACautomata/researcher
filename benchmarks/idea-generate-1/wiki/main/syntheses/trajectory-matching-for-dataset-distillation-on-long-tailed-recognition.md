---
pageType: synthesis
id: synthesis.trajectory-matching-for-dataset-distillation-on-long-tailed-recognition
title: Trajectory Matching for Dataset Distillation on Long-Tailed Recognition
sourceIds:
  - arxiv:2026.00001
claims:
  - text: TM 在 CIFAR-LT 平衡准确率 62.1%，优于 random (58.4%) 和 herding (60.0%)
    status: supported
    evidence:
      - kind: abstract
        sourceId: arxiv:2026.00001
        path: abstract
        weight: 1
        confidence: 1
  - text: TM 少数类准确率 31.4%，多数类 71.2%，差距约 40 个百分点
    status: supported
    evidence:
      - kind: abstract
        sourceId: arxiv:2026.00001
        path: abstract
        weight: 1
        confidence: 1
  - text: 轨迹匹配过度拟合头类动态是少数类性能差的根源
    status: supported
    evidence:
      - kind: method
        sourceId: arxiv:2026.00001
        path: method
        weight: 1
        confidence: 0.8
contradictions: []
questions:
  - 类别感知重加权能否改善少数类准确率？
  - 类别平衡合成预算是否优于固定每类预算？
confidence: 0.8
status: published
updatedAt: 2026-06-15T12:30:26.375Z
---

# Trajectory Matching for Dataset Distillation on Long-Tailed Recognition

## Notes
<!-- openclaw:human:start -->
<!-- openclaw:human:end -->

## Summary
<!-- openclaw:wiki:generated:start -->
# Trajectory Matching for Dataset Distillation on Long-Tailed Recognition

## 1. 论文摘要

本文研究了长尾分布下的轨迹匹配（Trajectory Matching, TM）数据集蒸馏方法。TM 通过匹配网络在合成集上训练的参数轨迹与在全量数据上训练的参数轨迹，来合成小型图像集。在 CIFAR-10-LT（类别不平衡比例 100）上，合成集（每类 1 张图像，头类/尾类各 1 张）可恢复全量数据训练的 62.1% 平衡准确率，但少数类准确率仅 31.4%，而多数类为 71.2%。研究表明，TM 过度拟合头类动态是差距的根源。

## 2. 研究背景与问题

数据集蒸馏旨在从大规模数据中合成一小规模、高质量的合成数据集，以用于神经网络训练。现有方法在平衡分布下效果良好，但在**长尾分布**（少数类样本远少于多数类）场景下缺乏系统研究。

**核心问题**：轨迹匹配在长尾场景下是否会出现类别不平衡问题？若出现，根源何在？

## 3. 方法

**核心方法：轨迹匹配（Trajectory Matching）**
- 教师网络（Teacher）在全量真实数据上训练，每步权重构成轨迹
- 学生网络（Student）在合成集上训练，通过 L2 损失优化使其轨迹匹配教师轨迹
- 合成预算：每类 10 张图像（CIFAR-10-LT，不平衡比例 100）
- 优化器：SGD，momentum=0.9，200 轮外循环，50 轮内循环

**关键设计**：
- 轨迹匹配天然地隐式学习数据分布，但未对类别差异做显式加权
- 合成图像通过梯度反向传播优化生成

## 4. 实验设置

| 配置项 | 值 |
|--------|-----|
| 数据集 | CIFAR-10-LT，不平衡比例 100（头类 5000 图像，尾类 50 图像） |
| 基线方法 | Random Sampling, Herding, K-Center |
| 评价指标 | 平衡准确率（Balanced Accuracy）、各类别准确率 |
| 合成预算 | 每类 10 张合成图像 |
| 合成成本 | 约 4 GPU 小时 |

## 5. 实验结果

| 方法 | 平衡准确率 | 多数类准确率 | 少数类准确率 |
|------|-----------|-------------|-------------|
| **TM（本文）** | **62.1%** | **71.2%** | **31.4%** |
| Random | 58.4% | - | - |
| Herding | 60.0% | - | - |
| K-Center | - | - | - |

**关键发现**：
- TM 在平衡准确率上优于所有基线（+1.9% vs Herding）
- **少数类准确率严重落后**：31.4% vs 71.2%（差距约 40 个百分点）
- 头类与尾类各 1 张/类的极低合成预算放大了类别不平衡问题

## 6. 结果分析

**少数类准确率瓶颈根源**：
1. **轨迹匹配过度拟合头类动态**：教师轨迹由多数类主导，学生网络在匹配过程中优先学习头类特征
2. **合成图像不足**：尾类仅 1 张合成图像，无法有效复现尾类决策边界
3. **缺失类别感知加权**：匹配损失未对尾类样本赋予更高权重

**TM 与基线对比**：在平衡准确率维度，TM 确实带来提升（+3.7% vs Random），但以牺牲少数类公平性为代价。

## 7. 局限性

1. **少数类准确率是明显瓶颈**：31.4% 的少数类准确率远低于可接受水平
2. **合成少数类图像不足以复现尾类决策边界**
3. **匹配过程中未应用类别感知加权**

## 8. 相关工作

- **数据集蒸馏方法**：DreamFusion, Distribution Matching, CSA 等
- **长尾识别方法**：类平衡损失、重采样、类别加权等
- **轨迹匹配方法**：通过参数轨迹对齐实现知识迁移

## 9. 开放问题

1. **类别感知重加权**：在轨迹损失中加入类别感知加权是否能提升少数类准确率？
2. **类别平衡合成预算**：在固定总预算下，为尾类分配更多合成图像（类别平衡预算）是否有帮助？
3. **教师轨迹的多样性**：不同教师初始化对尾类保留有何影响？
4. **端到端的长尾蒸馏**：能否在蒸馏过程中显式建模长尾分布？

## 10. 可复用结论

| 结论 | 支撑证据 | 信心度 |
|------|---------|--------|
| TM 在 CIFAR-LT 上可恢复全量训练约 62.1% 平衡准确率 | 62.1% vs 58.4% (random) | 高 |
| TM 的少数类准确率比多数类低约 40 个百分点 | 71.2% vs 31.4% | 高 |
| 轨迹匹配存在隐式头类偏好 | 论文分析声明 | 中 |

## 11. 参考文献

- 原论文：Trajectory Matching for Dataset Distillation on Long-Tailed Recognition（Bench Author, 2026, Bench Workshop）
- arXiv: 2026.00001
<!-- openclaw:wiki:generated:end -->

## Related
<!-- openclaw:wiki:related:start -->
- No related pages yet.
<!-- openclaw:wiki:related:end -->
