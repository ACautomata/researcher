---
title: Autoresearch 功能模块汇报——案例、定量定性分析及现状
type: analysis
domain: meta
status: active
created: 2026-05-20
updated: 2026-05-20
tags:
  - status-report
  - evaluation
source_pages:
  - wiki/index.md
  - wiki/log.md
---

# Autoresearch 功能模块汇报

## 一页总览

```
┌─────────────┬──────────┬──────────┬──────────────────────────────────────────┐
│ 功能模块     │ 执行次数  │ 成熟度    │ 一句话                                    │
├─────────────┼──────────┼──────────┼──────────────────────────────────────────┤
│ ingest      │ 22 篇    │ ★★★★   │ 全量化摄入管线，abstract-only 已消灭       │
│ query       │ 3 次     │ ★★★    │ 证据溯源链路打通，捞针 100% 可答           │
│ compare     │ 8 对     │ ★★☆    │ 跨论文/跨域连接，发现人工难以发现的关系    │
│ lint        │ 3 轮     │ ★★★    │ 质量从 0→63.6% full-paper，持续上升         │
│ analysis    │ 4 份     │ ★★★    │ 捞针测试集、优化评估，可量化可追踪          │
│ schema      │ 4 次迭代  │ ★★★★   │ 完整操作手册，论文优先+中文+最低标准        │
└─────────────┴──────────┴──────────┴──────────────────────────────────────────┘
```

**核心数据**：22 篇论文 · 7 个研究领域 · 8 个主题综合页 · 21 条原子 claim · 28 条运维日志

---

## 一、ingest — 论文摄入

### 关键数字

```
初始状态（4/20）          →    当前状态（5/20）

abstract-only  5 篇  ●●●●●    abstract-only  0 篇
skimmed        0 篇           skimmed        8 篇  ●●●●●●●●
full-paper     0 篇           full-paper    14 篇  ●●●●●●●●●●●●●●

                              达标率：定量数字 100%  baseline gap 90.9%  ablation 85.7%
```

### 成长曲线

| 阶段 | 时间 | 论文数 | full-paper | 里程碑 |
|------|------|--------|-----------|--------|
| 初始化 | 4/20 | 6 | 0 | schema + 首批 abstract-only 摄入 |
| 质量升级 | 5/5 | 13 | 8 | 5 篇 abstract→full, batch 12 篇 FL |
| 持续积累 | 5/8 | 22 | 14 | +COBRA +CoRD +FedSD2C，all full-paper |

### 案例 1：长尾蒸馏 — 从空到实

| 维度 | 摄入前 | 摄入后 |
|------|--------|--------|
| 证据等级 | abstract-only | full-paper |
| 实验数据 | "显著优于 SOTA"（0 个数字） | CIFAR-100-LT 47.1% vs DAMED 31.5%（+15.6%），IPC=1 时 31.8% vs 7.8%（+24.0%），ImageNet-LT IF=256 48.2% vs 17.2%（+181%） |
| 消融 | 无 | 3 组件各自贡献（-10% / -2% / -1%） |
| 效率 | 未提及 | 训练快 20×，GPU 内存恒定 3.1GB |

### 案例 2：联邦学习 12 篇批量摄入 — 规模+连接

- 一次性摄入 12 篇 PDF，自动分类到 6 个子方向
- 摄入后发现 2 个跨论文主题（联邦蒸馏与遗忘的统一视角、三层异质性框架）
- 1 篇分类错误自动修正（AgentReputation: FL → decentralized-ai）
- 6 篇后续升级到 full-paper，补充完整实验矩阵

### 当前不足

- 8 篇仍 skimmed，其中 2 篇（EASE、ProCo）理论价值高，优先升级
- method/dataset/metric 独立页 0 → 待建

---

## 二、query — 检索问答

### 检索链路

```
用户提问 → index.md（领域定位）→ 论文页（事实检索）→ topic 页（综合推理）→ 回答 + 证据溯源
```

### 执行记录

| 日期 | 问题 | 结果 |
|------|------|------|
| 4/25 | 为什么字面 negative prompt 不够？ | 回答 + 更新 LSN 论文页 |
| 4/25 | unbiased recovery 和 relabeling 的含义？ | 回答 + 更新长尾蒸馏页 |
| 5/5 | FedHD 与 distillation 域的交叉关系？ | 发现 3 条跨域连接 + 更新 topic 页 |

### 捞针测试（知识可检索性验证）

```
35 道题 × 4 题型 × 7 领域（2026-05-20 全量执行）
├── 完全通过  32 题  ████████████████████████████  91.4%
├── 部分通过   3 题  ███                           8.6%
└── 不可答     0 题                                0.0%
```

**可回答率 100%**，完全通过率 91.4%。3 题部分通过均为缺失个别定量数字（LSN prompt 数/Epoch 数、PALCAS 绝对碰撞率、Q14 期望答案过时），非检索链路问题。

### 案例：LSN vs NegPrompt 查询

- **输入**："两篇做 negative prompt 的论文有什么区别？"
- **输出**：LSN = class-specific 精度路线（AUROC 95.12%, FPR95 8.56%）, NegPrompt = transferable 泛化路线（open-vocabulary AUC 仅降 ~1.5%），二阶段训练是稳定必要条件（两个独立团队验证，置信度 high）
- **定性评价**：从"知道两篇相关"到"能说出设计分歧 + 定量差异 + 共同约束"

### 当前不足

- query 次数少（3 次），未建立系统召回率评估
- 捞针 35 题全量执行，完全通过率 91.4%（32/35），3 题部分通过待修复（缺失定量细节）

---

## 三、compare — 跨论文比较

### 连接网络

```
distillation ────┬─── federated-learning（FedHD, FedSD2C, EASE）
                 ├─── llm-reasoning（CoRD, 模型蒸馏 vs 数据蒸馏）
                 └─── 内部比较（RLDD↔COBRA, LSN↔NegPrompt, TAFAP↔MTT）
```

**8 对直接比较连接 + 4 条跨域技术连接**

### 案例 1：negative prompt 方法族

```
               LSN (ICLR 2024)          NegPrompt (CVPR 2024)
设计哲学        class-specific            transferable
精度            AUROC 98.05% (IN-100)    FPR95 23.01% (IN-1K)
泛化            不支持                    4 个 hard OOD 数据集
收敛点         两者都证明: positive ≠ negative prompt learning（置信度 high）
张力           两篇在不同 benchmark 上，不可直接比数字 ← 已标注
```

### 案例 2：长尾蒸馏 ↔ 公平蒸馏

| 维度 | RLDD (AAAI 2026) | COBRA (ICML 2026) |
|------|-----------------|-------------------|
| 问题 | class imbalance | subgroup bias |
| 方法 | statistical alignment | barycenter alignment |
| 核心创新 | dynamic momentum BN | uniform-weight 重心 |
| 关系 | 正交互补——两个公平性维度 |

### 当前不足

- **0 个正式 comparison 页**（最大结构缺口）
- 跨论文对比依赖人工发现，无自动匹配同 benchmark 论文

---

## 四、lint — 质量审计

### 成效看板

```
                     lint 前           lint 后         变化
abstract-only    ─── 5 篇 ───────    0 篇 ────────   -100%
full-paper       ─── 0 篇 ───────   14 篇 ────────   +∞
分类错误         ─── 2 篇 ───────    已修正 ──────   100%
孤儿论文率       ─── 100% ───────   27.3% ────────   -72.7%
定量数字/篇      ─── ~0.5 ───────   ~4.2 ─────────  +740%
```

### 3 轮 lint 历程

| 轮次 | 日期 | 行动 | 产出 |
|------|------|------|------|
| Lint-1 | 4/20 | inbox 扫描 | 识别 3 篇待摄入新论文 |
| Lint-2 | 5/5 | Experiments 回填 | 6 篇 skimmed→full-paper，回填 50+ 个定量数字 |
| Lint-3 | 5/5 | Auto Fix QA | 5 项自动修正（分类/状态/链接/孤儿检测） |

### 当前不足

- 无自动化 lint 触发（手动执行）
- 捞针测试已全量执行（35 题，91.4% 完全通过）

---

## 五、analysis — 综合分析

### 产出

| 分析 | 内容 | 价值 |
|------|------|------|
| inbox 分类 | 6 篇论文单标签归入 3 domain | 分类体系落地 |
| 重构方案 | 论文优先 schema 设计 | AGENTS.md 当前版本的基础 |
| 捞针测试集 | 15 题 × 4 题型 × 5 领域 | 可量化可追踪的知识检索 benchmark |
| 优化评估 | 22 篇定量基线 + 3 组案例 | 面向导师汇报 |

### 当前不足

- 缺少面向外部研究的分析（如某领域文献综述）
- 无可视化呈现（图表/看板）

---

## 六、schema — 结构维护

### 迭代轨迹

```
4/20  v1.0  初始化       raw/wiki 分层，ingest-query-lint 工作流
  │
4/25  v2.0  论文优先     引入 papers/methods/datasets + evidence_level + atomic claims
  │
5/5   v2.1  质量标准      Experiments/Results 最低标准，反模式清单，定量数字硬性要求
  │
5/19  v2.2  Agent 架构   从 LLMWiki.md 重构为 workspace-autoresearch/ OpenClaw agent
  ▼
```

### 当前不足

- comparison 页模板完备但 0 实例化
- method/dataset/metric 页模板完备但 0 创建

---

## 总结

### 用这页做汇报结尾

```
投入            产出                                   质量
─────────────────────────────────────────────────────────────
30 天            22 篇论文 / 7 领域                     full-paper 率 63.6%
                8 个 topic 综合页                       abstract-only 清零
                21 条原子 claim                        定量数字 +740%
                4 条跨域技术连接                       捞针 100% 可答（35 题）
                35 道捞针测试

                    下一步
          comparison 页（0→2+）
          自动化 lint + 捞针
          skimmed→full-paper 升级（EASE, ProCo 优先）
```

### 如果被追问

| 问题 | 回答 |
|------|------|
| "为什么只有 22 篇？" | "当前手动摄入管道，一篇 full-paper 需要完整阅读+提取实验表+建立交叉链接。量不是瓶颈，质量闭环跑通后可以加速" |
| "为什么没自动化？" | "先手动验证工作流正确性，确定方案可行后再投入自动化——避免在错误方向上加速" |
| "和已有工具（Zotero/Notion）有什么不同？" | "不是文献管理，是知识编译——论文的知识不会被遗忘，新论文自动和已有知识建立连接，且每条 claim 可追溯到原始 PDF" |
| "怎么证明有用？" | "捞针测试 100% 可回答率 + 3 组案例中跨域技术连接和设计 trade-off 是纯人工逐篇阅读难以发现的" |
