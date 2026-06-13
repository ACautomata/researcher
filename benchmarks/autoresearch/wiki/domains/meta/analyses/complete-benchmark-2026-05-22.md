---
title: Complete Benchmark — 50 QA Pairs
type: analysis
domain: meta
status: active
created: 2026-05-22
updated: 2026-05-22
tags:
  - qa
  - benchmark
  - needle-test
source_pages:
  - wiki/domains/meta/analyses/needle-tests-2026-05-05.md
  - wiki/domains/meta/analyses/benchmark-expansion-2026-05-22.md
---

# Complete Benchmark：50 QA Pairs

## 结构总览

```
50 QA pairs
├── Seed QA（人工构建）35 题
│   ├── Distillation           Q1-Q3     (3 题)
│   ├── OOD Detection          Q4-Q5     (2 题)
│   ├── Spectrum               Q6-Q7     (2 题)
│   ├── Autonomous Driving     Q8-Q9     (2 题)
│   ├── Federated Learning     Q10-Q12   (3 题)
│   ├── LLM Reasoning          Q16-Q19   (4 题)
│   ├── FL Deep                Q20-Q24   (5 题)
│   ├── Distillation Deep      Q25-Q28   (4 题)
│   ├── Cross-Domain           Q13-Q15, Q29-Q31 (6 题)
│   └── Meta                   Q32-Q35   (4 题)
│
├── Expansion QA（LLM 扩充）15 题
│   ├── Distillation           N1-N4     (4 题)
│   ├── Federated Learning     N5-N9     (5 题)
│   ├── Cross-Domain           N10-N12   (3 题)
│   └── Meta & Practical       N13-N15   (3 题)
│
└── 题型分布
    ├── 事实检索       15 题  (30%)
    ├── 跨论文比较     10 题  (20%)
    ├── 机制理解       12 题  (24%)
    ├── 边界判断/量化   5 题  (10%)
    ├── 跨域连接        5 题  (10%)
    └── 结构/反模式     3 题  (6%)
```

## Seed QA（35 题）

完整内容见 [Needle Tests 2026-05-05](needle-tests-2026-05-05.md)。

### 按领域

| 领域 | 题号范围 | 题数 | 题型覆盖 |
|------|---------|------|---------|
| Distillation | Q1-Q3 | 3 | 事实检索、跨论文比较、机制理解 |
| Out-of-Distribution Detection | Q4-Q5 | 2 | 方法区分、核心发现 |
| Spectrum | Q6-Q7 | 2 | 方法链、边界判断 |
| Autonomous Driving | Q8-Q9 | 2 | 方法创新、场景约束 |
| Federated Learning | Q10-Q12 | 3 | 架构理解、跨域连接、分类判断 |
| LLM Reasoning | Q16-Q19 | 4 | 事实检索、机制理解、跨域区分、跨域连接 |
| FL Deep | Q20-Q24 | 5 | 机制理解、方法迁移、跨论文比较、系统设计、量化对比 |
| Distillation Deep | Q25-Q28 | 4 | 事实检索、跨论文比较、机制理解、消融分析 |
| Cross-Domain | Q13-Q15, Q29-Q31 | 6 | 跨域综合、证据等级、孤儿检测、跨域连接、三域交叉 |
| Meta | Q32-Q35 | 4 | 结构完整性、孤儿检测、优先级、反模式 |

## Expansion QA（15 题 - 本文件新增）

完整内容见 [Benchmark LLM Expansion](benchmark-expansion-2026-05-22.md)。

### 按领域

| ID | 领域 | 题型 | 主题 |
|----|------|------|------|
| N1 | Distillation | 机制理解 | Continual Distillation: UKT-UKF trade-off |
| N2 | Distillation | 方法理解 | SE2D 如何平衡 UKT 和 UKF |
| N3 | Distillation | 量化对比 | COBRA 低 IPC 公平性鲁棒性 |
| N4 | Distillation | 跨域连接 | Continual Distillation vs. Dataset Distillation |
| N5 | Federated Learning | 事实检索 | FedHD 的三个核心组件 |
| N6 | Federated Learning | 方法迁移 | FedKPer selective alignment + forgetting |
| N7 | Federated Learning | 量化对比 | FedACT participation fairness 效果 |
| N8 | Federated Learning | 机制理解 | FSCLB 双 sketch 策略 |
| N9 | Federated Learning | 跨论文比较 | FedHarmony vs. COBRA 哲学共性 |
| N10 | Cross-Domain | 跨域连接 | "受控增量整合"三域体现 |
| N11 | Cross-Domain | 三域交叉 | UKF vs. FL forgetting 统一理解 |
| N12 | Cross-Domain | 跨域识别 | Wiki 中基于 matching 的方法家族 |
| N13 | Meta | 证据等级 | Continual Distillation evidence_level 影响 |
| N14 | Meta | 反模式 | Method/Dataset/Metric 页独立化进度 |
| N15 | Meta | 维护建议 | Wiki 改进优先级排序 |

## Benchmark 使用说明

### 运行方式

Seeding：Claude Code 逐条在 **干净 session** 中提给 llmwiki agent，每条包含完整输入（提问 + 可选的背景材料说明）。

Evaluation：对 agent 回复，与"期望答案"逐点对比：
- ✅ 完全通过：核心结论正确，关键细节齐全
- ⚠️ 部分通过：核心结论正确但关键细节缺失
- ❌ 不通过：核心结论错误或无法从 wiki 检索到答案

### 更新策略

- 每次 major ingest 后随机选 5-8 题执行捞针
- 新增加论文 → 新增对应 QA
- 发现知识缺口 → 转化为新测试题
- 期望答案随 wiki 演化同步更新
