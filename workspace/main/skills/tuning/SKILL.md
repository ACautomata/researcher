---
name: tuning
description: 调参优化编排 skill。Main 将调参任务直接派发给 tuning agent。
---

# tuning

## 概述

调参优化任务编排。当用户需要对算法代码进行超参优化时，main 理解需求后直接派发给 tuning agent。

**Trigger words**: "调参", "tuning", "超参数优化", "hyperparameter", "参数调优", "优化参数", "搜索参数"

## 应用场景

- 用户有代码仓库，需要对模型超参数进行系统优化
- 需要确定最优的搜索策略和搜索空间
- 需要在有限预算内找到最佳参数组合

## 编排步骤

### Step 1: Main 了解需求

1. 目标代码仓库路径
2. 调参目标（精度/延迟/参数量）
3. 已有配置文件（如有）
4. 计算预算（如有）

### Step 2: 直接派发 tuning

```
sessions_spawn(
  agentId: "tuning",
  task: "对以下代码仓库进行调参优化分析...",
  mode: "run",
  runTimeoutSeconds: 600
)
```

### Step 3: 接收结果 + Judge 审查

- Main 接收 tuning 返回的调参方案
- 派发 judge 审查方案质量
- 向用户汇报

## 路由规则

| 用户意图 | Worker | Skill |
|---------|--------|-------|
| 调参优化 | tuning | skills/tuning/ |
