---
title: Self-Test Report — Benchmark Execution Report
type: analysis
domain: meta
status: active
created: 2026-05-22
updated: 2026-05-22
tags:
  - qa
  - self-test
  - benchmark
  - report
source_pages:
  - wiki/domains/meta/analyses/needle-tests-2026-05-05.md
  - wiki/domains/meta/analyses/benchmark-expansion-2026-05-22.md
  - wiki/domains/meta/analyses/complete-benchmark-2026-05-22.md
---

# Self-Test Report 2026-05-22

## 1. 测试方法论

### 1.1 测试目标

验证 llmwiki agent（在 AGENTS.md 上下文下运行的 Claude Code）能否从 wiki 内容中正确检索并综合出 QA pairs 的期望答案。

### 1.2 测试方式

**Seed QA（35 题）**：已由 Claude Code 于 2026-05-20 执行完毕。执行方式：每条 Q 在干净 session 中提给 agent，agent 基于 wiki 内容检索回答，对比期望答案判定 pass/partial/fail。

**Expansion QA（15 题）**：待 Claude Code 执行（本次报告中提供预期答案和验证页面，实际执行时间戳待补充）。

### 1.3 判定标准

| 等级 | 定义 | 处理 |
|------|------|------|
| ✅ 完全通过 | 核心结论正确，关键细节齐全，可直接从 wiki 检索 | 无操作 |
| ⚠️ 部分通过 | 核心结论正确但关键细节缺失（wiki 有相关但不够完整） | 补充对应页面 |
| ❌ 不通过 | 核心结论错误，或无法从 wiki 检索到答案 | 修正对应页面 |

### 1.4 测试输入格式

每条测试用例在 Claude Code 中以以下格式提交：

```
## 问题

[提问内容]

## 背景

[相关 wiki 路径 / 可选上下文]

请基于 wiki 内容回答上述问题。
```

---

## 2. Seed QA 执行结果（35 题）

> 数据源：[Needle Tests 2026-05-05](needle-tests-2026-05-05.md) 执行报告

### 2.1 汇总

```
35 题
├── ✅ 完全通过  32 题 (91.4%)
├── ⚠️ 部分通过   3 题  (8.6%)
└── ❌ 不通过     0 题  (0.0%)
```

**可回答率：100%**（无一道题"查不到"）
**完全通过率：91.4%**

### 2.2 逐题详情

| 题号 | 领域 | 题型 | 结果 | 说明 |
|------|------|------|------|------|
| Q1 | Distillation | 事实检索 | ✅ | ProCo 的 retrieval-based correspondence consistency metric 已明确记录 |
| Q2 | Distillation | 跨论文比较 | ✅ | RLDD vs ProCo 差异清晰 |
| Q3 | Distillation | 机制理解 | ✅ | TAFAP trajectory vs snapshot 持久性差异完整 |
| Q4 | OOD | 跨论文比较 | ✅ | LSN vs NegPrompt 核心差异明确 |
| Q5 | OOD | 机制理解 | ⚠️ | 核心定性发现存在但缺定量细节（prompt 数 8 vs 2，epoch 25 vs 5） |
| Q6 | Spectrum | 方法链 | ✅ | 5 步 pipeline 完整 |
| Q7 | Spectrum | 边界判断 | ✅ | 4 项局限均有记录 |
| Q8 | Autonomous Driving | 方法创新 | ✅ | PDQN 混合动作空间明确 |
| Q9 | Autonomous Driving | 场景约束 | ⚠️ | RSS 模型和 MSR 已记录，但绝对碰撞率 2.45% 未记录 |
| Q10 | FL | 架构理解 | ✅ | EASE 三锚 + BKE/GSD/PFL 完整 |
| Q11 | FL | 跨域连接 | ✅ | FedHD↔distillation 连接存在 |
| Q12 | FL | 分类判断 | ✅ | AgentReputation 标记已记录 |
| Q13 | Cross-Domain | 跨域比较 | ✅ | 联邦蒸馏跨 3 域连接完整 |
| Q14 | Cross-Domain | 证据等级 | ⚠️ | 期望答案已过时（5/5 状态 6 篇 full-paper，当前 14 篇） |
| Q15 | Cross-Domain | 孤儿检测 | ✅ | 6 篇 orphan 可验证 |
| Q16 | LLM Reasoning | 事实检索 | ✅ | CoRD predictive perplexity + 优于 PRM/Binary Judgment |
| Q17 | LLM Reasoning | 机制理解 | ✅ | 策展式两局限完整 |
| Q18 | LLM Reasoning | 跨域区分 | ✅ | 模型级 vs 数据级蒸馏区分明确 |
| Q19 | LLM Reasoning | 跨域连接 | ✅ | CoRD 逐步协同 + FedHD 课程联邦共性可从页面合成 |
| Q20 | FL Deep | 机制理解 | ✅ | FedSD2C 双层信息损失完整 |
| Q21 | FL Deep | 方法迁移 | ✅ | FedHAW hypergradient 迁移洞察明确 |
| Q22 | FL Deep | 跨论文比较 | ✅ | FedHarmony vs FedAvg 差异完整 |
| Q23 | FL Deep | 系统设计 | ✅ | FedACT alignment scoring 完整 |
| Q24 | FL Deep | 量化对比 | ✅ | 硬件 / JCT 8.3× / Acc +44.5% 全部验证 |
| Q25 | Distillation Deep | 事实检索 | ✅ | COBRA barycenter 完整记录 |
| Q26 | Distillation Deep | 跨论文比较 | ✅ | COBRA vs RLDD 正交互补明确 |
| Q27 | Distillation Deep | 机制理解 | ✅ | COBRA"只改 target 不改 loss" 明确 |
| Q28 | Distillation Deep | 消融分析 | ✅ | RLDD 三组件贡献 (-10%/-2%/-1%) 验证 |
| Q29 | Cross-Domain | 跨域连接 | ✅ | FedSD2C vs ProCo 压缩哲学可从页面合成 |
| Q30 | Cross-Domain | 跨域连接 | ✅ | TAFAP ↔ CoRD 共享哲学可独立验证 |
| Q31 | Cross-Domain | 三域交叉 | ✅ | cross-modal coupling 三重角色可合成 |
| Q32 | Meta | 结构完整性 | ✅ | comparison 缺口可验证 |
| Q33 | Meta | 孤儿检测 | ✅ | 6 篇孤儿论文 + 重组方案可检索 |
| Q34 | Meta | 优先级 | ✅ | 升级优先级可从 evidence_level 和引用度推理 |
| Q35 | Meta | 反模式 | ✅ | 4 项结构问题可验证 |

### 2.3 3 题部分通过的改进建议

| 题号 | 缺失内容 | 改进动作 | 优先级 |
|------|---------|---------|--------|
| Q5 | LSN Table 5 中 positive/negative prompt 数 (8 vs 2) 和 epoch (25 vs 5) | 在 LSN 论文页补充具体数字 | P0 |
| Q9 | PALCAS 的绝对碰撞率 (2.45% at 60% CAV) | 在 PALCAS 论文页实验结果中补充 | P0 |
| Q14 | 期望答案过时（反映 5/5 而非 5/20 状态） | 更新期望答案为"列出当前 full-paper"或改为动态描述 | P0 |

---

## 3. Expansion QA 执行计划（15 题）

### 3.1 测试用例分布

| ID | 领域 | 题型 | 验证页面 |
|----|------|------|---------|
| N1 | Distillation | 机制理解 | Continual Distillation paper |
| N2 | Distillation | 方法理解 | Continual Distillation paper |
| N3 | Distillation | 量化对比 | COBRA paper |
| N4 | Distillation | 跨域连接 | CD paper + Dataset Distillation concept |
| N5 | FL | 事实检索 | FedHD paper |
| N6 | FL | 方法迁移 | FedKPer paper + FL Heterogeneity topic |
| N7 | FL | 量化对比 | FedACT paper |
| N8 | FL | 机制理解 | FSCLB paper |
| N9 | FL / Cross-Domain | 跨论文比较 | FedHarmony + COBRA + FL Heterogeneity topic |
| N10 | Cross-Domain | 跨域连接 | FedHD + CoRD + CD |
| N11 | Cross-Domain | 三域交叉 | CD + FedKPer + FL Heterogeneity topic |
| N12 | Cross-Domain | 跨域识别 | TAFAP + COBRA + FedHD + FedACT |
| N13 | Meta | 证据等级 | CD paper |
| N14 | Meta | 反模式 | AGENTS.md + Needle Tests Q35 |
| N15 | Meta | 维护建议 | Needle Tests execution report |

### 3.2 期望答案摘要

> 详细期望答案见 [Benchmark LLM Expansion](benchmark-expansion-2026-05-22.md)。

| ID | 期望答案核心要点 |
|----|----------------|
| N1 | UKT = 外部数据带来未见领域知识；UKF = 后续教师覆盖先前知识；矛盾在于外部数据同时触发两者 |
| N2 | SE2D 通过 logit preservation 同时提升 UKT（保留教师响应模式）和降低 UKF（惩罚 logits 偏离） |
| N3 | IPC=1 时 COBRA EOD 4.9 vs Vanilla 17.2；样本越少 barycenter 保护越突出 |
| N4 | CD = 模型级蒸馏；DD = 数据级压缩；损失函数本质不同（KL divergence vs. gradient/distribution matching） |
| N5 | FedHD 三组件：GM Feature Alignment + One-to-One Distillation + Curriculum Federation |
| N6 | Selective alignment 通过部分参数对齐改进 generalization-personalization trade-off；第三维度：forgetting |
| N7 | JCT 8.3× 减少 + Acc 44.5% 提升；说明 fair scheduling 不只是伦理需求 |
| N8 | 特征 sketch（count sketch）+ 梯度 sketch；SVD 间接行列式处理加性噪声 |
| N9 | 共性：拒绝群体比例加权；不同：场景（FL聚合 vs. 集中蒸馏）+ 替代方案（共识 vs. barycenter） |
| N10 | FedHD 课程联邦 + CoRD 逐步解码 + CD SE2D logit preservation，共享"基线→增量整合"哲学 |
| N11 | 共享"新知识覆盖旧知识"机制；场景不同（蒸馏管道 vs. 联邦训练） |
| N12 | 6 种 matching 范式散布在蒸馏和 FL 域，尚无统一 comparison 页 |
| N13 | CD evidence_level = skimmed；核心概念可信但定量数据需验证 |
| N14 | Method/Dataset/Metric 页 0 创建，违反 DRY 原则 |
| N15 | P0: 修复 Q5/Q9/Q14 缺失；P1: 创建 comparison 页；P2: 消除孤儿论文 |

### 3.3 执行指引

在 Claude Code 中执行 Expansion QA 的标准流程：

```bash
# 对每道题，在干净 session 中执行：
# 1. 创建新会话
# 2. 读取 AGENTS.md + wiki/index.md
# 3. 提问
# 4. 对比期望答案判定结果
# 5. 记录到下方执行记录表
```

---

## 4. 综合分析

### 4.1 覆盖率分析

```mermaid
饼图：覆盖分布
领域覆盖率（基于论文数）：
- Distillation：5 篇论文 → 7 题 (14%)    ⚠️ 相对不足
- OOD Detection：2 篇论文 → 2 题 (4%)
- Spectrum：1 篇论文 → 2 题 (4%)
- Autonomous Driving：1 篇论文 → 2 题 (4%)
- Federated Learning：12 篇论文 → 13 题 (26%)  ✅ 覆盖充分
- LLM Reasoning：1 篇论文 → 4 题 (8%)
- Meta / Cross-Domain：— → 20 题 (40%)  ✅
```

### 4.2 质量评估

**优势：**
- 可回答率 100% — 无题目的答案完全"查不到"
- 完全通过率 91.4% — 多数期望答案可直接从 wiki 检索
- 题型丰富 — 6 种题型覆盖从事实检索到反模式分析
- 跨域连接题目质量高 — 体现了 wiki 的知识关联优势

**不足：**
- 按论文数的覆盖率不均衡（Federated Learning 12 篇 vs. Spectrum 1 篇）
- 3 题部分通过全部是"定量细节缺失" — wiki 在定性描述上强，但具体数字需要补充
- 跨域题目依赖 agent 的合成推理能力（非纯检索）

### 4.3 改进建议

**内容层面：**
1. P0（立即修复）：LSN 论文补充 prompt 数/epoch 数、PALCAS 补充绝对碰撞率、更新 Q14 期望答案
2. P1（短期）：按 Q35 反模式清单创建首批 comparison 页（LSN vs NegPrompt）
3. P2（长期）：创建首批 method/dataset/metric 独立页、消除孤儿论文

**Benchmark 层面：**
4. 每次 major ingest 后随机选 5-8 题执行
5. 新增论文后同步创建 1-2 道对应 QA
6. 季度性更新期望答案以匹配 wiki 演化

---

## 5. 版本记录

| 日期 | 版本 | 内容 | 执行人 |
|------|------|------|--------|
| 2026-05-05 | v1 | 初始 15 题测试集创建 | — |
| 2026-05-20 | v2 | 扩展至 35 题（+LLM Reasoning / FL Deep / Distillation Deep / Meta） | — |
| 2026-05-20 | v2-exec | 首次全量执行：32/35 ✅ (91.4%) | Claude |
| 2026-05-22 | v3 | 扩展至 50 题（+Continual Distillation / FedHD / FedKPer / FSCLB / Cross-Domain / Meta Practical） | OpenClaw |
| 2026-05-22 | v3-exec | Expansion QA 待执行 | — |
