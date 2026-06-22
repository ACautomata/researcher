---
name: optimizer
description: 模型架构优化编排 skill。Main 将架构优化任务直接派发给 optimizer agent。
---

# optimizer

## 概述

模型架构优化任务编排。用户需要对模型进行结构层面的改进时，main 直接派发给 optimizer agent。

**Trigger words**: "架构优化", "模型改进", "architecture", "网络结构", "改模型", "层数调整", "注意力"

## 应用场景

- 用户模型精度上不去，怀疑是架构瓶颈
- 需要压缩模型参数量/加速推理
- 需要评估架构改动的收益和风险

## 编排步骤

1. Main 了解需求（代码路径 + 优化目标）
2. 直接派发 optimizer agent
3. Main + Judge 审查方案质量
4. 向用户汇报

## 路由规则

| 用户意图 | Worker | Skill |
|---------|--------|-------|
| 架构优化 | optimizer | skills/optimizer/ |
