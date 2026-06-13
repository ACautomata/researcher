---
title: 任务四最终交付 — Skill 拆分
type: delivery
domain: meta
status: active
created: 2026-05-22
tags:
  - task4
  - skills
  - refactoring
  - delivery
source_pages:
  - 任务说明.docx
  - AGENTS.md
  - wiki/domains/meta/analyses/task1-final-delivery-2026-05-22.md
  - wiki/domains/meta/analyses/task2-final-delivery-2026-05-22.md
  - wiki/domains/meta/analyses/task3-final-delivery-2026-05-22.md
---

# 任务四：Skill 拆分 — 最终交付

> 项目：llmwiki Agent 开发
> 目标：把多个 skill 中重复的逻辑提取为共享模块
> 交付日期：2026-05-22

---

## 目录

1. [设计原则](#1-设计原则)
2. [当前状态：单体 agent 的问题](#2-当前状态单体-agent-的问题)
3. [Skills 定义：每个 skill 做什么](#3-skills-定义每个-skill-做什么)
4. [重复步骤识别](#4-重复步骤识别)
5. [共享模块提取](#5-共享模块提取)
6. [拆分后的目录结构](#6-拆分后的目录结构)
7. [拆分解决了什么问题](#7-拆分解决了什么问题)
8. [分层架构全貌](#8-分层架构全貌)

---

## 1. 设计原则

```
高内聚，低耦合

设计分层：
Main agent → skills for main agent → subagent → skills for subagent

├── Main agent:            协调入口，理解用户意图，路由到对应 skill
├── skills for main agent: 对 subagent 的组合形成的 pipeline
├── subagent:              高度内聚的最小运行单元
└── skills for subagent:   不需要随时保存在上下文内的具体业务流程
                           需要随时在上下文内的 → AGENTS.md / TOOLS.md
```

### 本次拆分的规则

| 规则 | 说明 |
|------|------|
| **一个 skill 只做一类事** | 查询的 skill 不负责写入，录入的 skill 不负责判定 |
| **≥2 个 skill 都做的步骤 → 提到 shared** | 读文件、写 frontmatter、更新索引——谁都别重复实现 |
| **subagent = 最小运行单元** | 一个 subagent 只做一件事，做彻底 |
| **上下文紧的→AGENTS.md** | 设计哲学、约束规则、范式选择属于主 agent 的上下文，不塞进 skill |

---

## 2. 当前状态：单体 agent 的问题

### 2.1 现状

当前 llmwiki agent 的所有能力都集中在一个 `AGENTS.md` 中定义——查询、录入、自测、维护、分析，全部写在同一个文件里。通过"请求模式"（query / ingest / analysis / lint / compare / organize）区分不同工作。

### 2.2 单体结构的痛点

| 问题 | 表现 | 后果 |
|------|------|------|
| **文件臃肿** | AGENTS.md 超过 500 行，包含从 schema 定义到具体模板到每个 workflow 的全部细节 | 每轮对话加载大量不相关的上下文 |
| **职责混在一起** | 查询逻辑里混着写入逻辑；录入逻辑里混着 lint 检查 | 改了查询模式可能影响录入行为 |
| **重复代码** | "从 wiki 读取文件"的逻辑在 query / ingest / maintain 中各自实现了一遍；"更新索引"在 ingest / maintain / organize 中各出现一次 | 改一个要改三处，容易不一致 |
| **无法独立测试** | 没法单独测试"录入"是否正常——因为和查询共用同一段读取逻辑 | 出问题只能全量回归 |

---

## 3. Skills 定义：每个 skill 做什么

### 3.1 主 agent 层 skills（skills for main agent）

这些 skill 是对 subagent 的组合调用，形成完整的端到端 pipeline：

| Skill | 名称 | 做什么 |
|-------|------|--------|
| **skill-query** | 问答查询 | 接收用户问题 → 检索 wiki → 综合推理 → 输出带来源的答案 |
| **skill-ingest** | 论文录入 | 接收论文信息 → 创建论文页 → 更新 topic/概念页 → 更新索引 → 写日志 |
| **skill-benchmark** | 基准自测 | 接收 QA pair → 检索 wiki → 回答 → 对比期望答案 → 输出判定结果 → 汇总报告 |
| **skill-maintain** | Wiki 维护 | 接收维护指令 → 定位页面 → 修改内容 → 更新交叉引用 → 输出 diff |
| **skill-analyze** | 跨域分析 | 接收分析请求 → 多域检索 → 跨域综合 → 输出分析报告 / comparison 页 |

### 3.2 Subagent 层 skills（skills for subagent）

这些是被主 agent skill 调用的最小运行单元，每个只做一件事：

| Subagent Skill | 名称 | 做什么 | 被哪些主 skill 调用 |
|---------------|------|--------|-------------------|
| **sub-wiki-reader** | Wiki 读取 | 根据路径/关键词读取 wiki 页面，返回结构化内容 | query, ingest, benchmark, maintain, analyze |
| **sub-frontmatter** | Frontmatter 处理 | 生成/解析/校验 YAML frontmatter | ingest, maintain |
| **sub-linker** | 链接管理 | 创建相对路径链接、检查死链、更新交叉引用 | ingest, maintain, analyze |
| **sub-index-updater** | 索引更新 | 更新 wiki/index.md 和领域 index | ingest, maintain, organize |
| **sub-logger** | 日志记录 | 向 wiki/log.md 追加操作记录 | ingest, maintain, organize |
| **sub-markdown-gen** | Markdown 生成 | 按模板生成结构化 Markdown 内容 | query, ingest, benchmark, maintain, analyze |
| **sub-qa-judge** | QA 判定 | 对比 agent 回答与期望答案，判定 ✅/⚠️/❌ | benchmark |
| **sub-diff-gen** | Diff 生成 | 生成修改前后的对比 | maintain |

---

## 4. 重复步骤识别

### 4.1 重复矩阵

对每个 skill 的步骤做分解，标记重复：

```
步骤 \ Skill          query  ingest  benchmark  maintain  analyze  count
────────────────────────────────────────────────────────────────────────────
读取 wiki 文件           ✅     ✅       ✅         ✅       ✅      5  ←
按路径定位页面           ✅     ✅       ✅         ✅       ✅      5  ←
生成/解析 frontmatter    ❌     ✅       ❌         ✅       ❌      2  ←
创建相对路径链接          ❌     ✅       ❌         ✅       ✅      3  ←
更新 wiki/index.md       ❌     ✅       ❌         ✅       ❌      2  ←
写 wiki/log.md          ❌     ✅       ❌         ✅       ❌      2  ←
按模板生成 Markdown      ✅     ✅       ✅         ✅       ✅      5  ←
对比 / 判定             ❌     ❌       ✅         ❌       ❌      1
综合推理                ✅     ❌       ❌         ❌       ✅      2
修改页面内容             ❌     ✅       ❌         ✅       ❌      2
输出 diff               ❌     ❌       ❌         ✅       ❌      1
```

### 4.2 识别结果：6 个重复步骤

| 编号 | 重复步骤 | 出现次数 | 涉及 skill | 提取为 |
|:----:|---------|:-------:|-----------|--------|
| R1 | 读取 wiki 文件 | **5** | 全部 | **sub-wiki-reader** |
| R2 | 按模板生成 Markdown | **5** | 全部 | **sub-markdown-gen** |
| R3 | 创建/更新相对路径链接 | **3** | ingest, maintain, analyze | **sub-linker** |
| R4 | 更新 wiki/index.md | **2** | ingest, maintain | **sub-index-updater** |
| R5 | 写 wiki/log.md | **2** | ingest, maintain | **sub-logger** |
| R6 | 生成/解析 YAML frontmatter | **2** | ingest, maintain | **sub-frontmatter** |

> 注意：R1 和 R2 出现 5 次——意味着**每个 skill 都在自己内部实现了读文件和生成 markdown 的逻辑**。这是最需要提取的共享模块。

---

## 5. 共享模块提取

### 5.1 提取方案

#### sub-wiki-reader — Wiki 读取模块

```
职责：接收文件路径或关键词，返回结构化 wiki 内容
功能：
├── read_by_path(path): 按相对路径读取一个 wiki 文件
├── read_by_keyword(keyword): 按关键词搜索 wiki 文件列表
├── read_multiple(paths): 批量读取多个 wiki 文件
├── search_in_content(path, pattern): 在文件内容中搜索
└── read_index(): 读取并解析 wiki/index.md
```

#### sub-markdown-gen — Markdown 生成模块

```
职责：按模板生成结构化 Markdown 内容
功能：
├── gen_paper_page(data): 按论文模板生成页面
├── gen_answer(result, sources): 生成带来源的回答
├── gen_report(stats, details): 生成自测报告
├── gen_analysis(question, findings): 生成分析报告
├── gen_comparison(entries): 生成 comparison 表
└── gen_diff(old, new): 生成文本 diff
```

#### sub-linker — 链接管理模块

```
职责：创建、检查、更新相对路径 Markdown 链接
功能：
├── create_link(path, text): 创建 [text](path) 格式链接
├── validate_links(content): 检查页面中的死链
├── update_inbound_links(file_path, old_target, new_target): 更新入站链接
└── resolve_relative(source, target): 计算两个文件之间的相对路径
```

#### sub-index-updater — 索引更新模块

```
职责：维护 wiki/index.md 和各领域 index.md
功能：
├── add_entry(index_path, entry): 向索引添加一条
├── remove_entry(index_path, slug): 从索引移除一条
├── update_entry(index_path, slug, new_desc): 更新索引条目描述
└── regenerate_index(domain): 重新生成某个领域的索引
```

#### sub-logger — 日志记录模块

```
职责：向 wiki/log.md 追加结构化操作记录
功能：
├── log_ingest(paper_title, files_changed, evidence_level): 记录录入
├── log_maintain(files_modified, action_summary): 记录维护
├── log_benchmark(qa_count, pass_rate): 记录自测
└── log_analysis(topic, files_created): 记录分析
```

#### sub-frontmatter — Frontmatter 处理模块

```
职责：生成、解析、校验 YAML frontmatter
功能：
├── parse_frontmatter(content): 解析已有页面的 frontmatter
├── gen_frontmatter(meta): 按 schema 生成 frontmatter
├── validate_frontmatter(fm): 校验必填字段
└── update_frontmatter(content, updates): 更新已有页面的 frontmatter
```

---

## 6. 拆分后的目录结构

### 6.1 完整目录

```
D:\llmwiki\
│
├── AGENTS.md                      # 主 agent 身份 + 设计哲学（范式选择、约束规则）
├── CLAUDE.md                      # 兼容层
│
├── skills\                        # 【新增】skill 目录
│   │
│   ├── shared\                    # 共享模块（被 2+ 个 skill 使用）
│   │   ├── sub-wiki-reader.md     #   Wiki 读取
│   │   ├── sub-markdown-gen.md    #   Markdown 生成
│   │   ├── sub-linker.md          #   链接管理
│   │   ├── sub-index-updater.md   #   索引更新
│   │   ├── sub-logger.md          #   日志记录
│   │   └── sub-frontmatter.md     #   Frontmatter 处理
│   │
│   ├── main\                      # 主 agent 层 skills（pipeline 组合）
│   │   ├── skill-query.md         #   问答查询
│   │   ├── skill-ingest.md        #   论文录入
│   │   ├── skill-benchmark.md     #   基准自测
│   │   ├── skill-maintain.md      #   Wiki 维护
│   │   └── skill-analyze.md       #   跨域分析
│   │
│   └── TOOLS.md                   # 【可选】skill 的本地配置信息
│
├── raw\                            # 不变：原始材料
├── wiki\                           # 不变：wiki 内容
└── 任务说明.docx                   # 不变：任务书
```

### 6.2 每个 skill 文件的结构建议

每个 skill 文件是一个独立的 Markdown 文档，结构如下：

```markdown
# skill-query: 问答查询

## 职责
...

## 输入
...

## 调用流程
1. [sub-wiki-reader] 读取相关 wiki 页面
2. [sub-markdown-gen] 按模板生成回答
3. [sub-linker] 添加来源链接

## 输出
...

## 不负责
- 修改 wiki 文件（那是 skill-maintain 的事）
- 判定对错（那是 skill-benchmark 的事）
```

### 6.3 调用关系图

```
用户输入
    │
    ▼
Main agent (AGENTS.md)
    │
    ├── skill-query ─────── sub-wiki-reader
    │                       sub-markdown-gen
    │
    ├── skill-ingest ────── sub-wiki-reader
    │                       sub-frontmatter
    │                       sub-markdown-gen
    │                       sub-linker
    │                       sub-index-updater
    │                       sub-logger
    │
    ├── skill-benchmark ──── sub-wiki-reader
    │                       sub-markdown-gen
    │                       sub-qa-judge       ← 专用（仅 benchmark 用）
    │
    ├── skill-maintain ──── sub-wiki-reader
    │                       sub-frontmatter
    │                       sub-markdown-gen
    │                       sub-linker
    │                       sub-index-updater
    │                       sub-logger
    │                       sub-diff-gen       ← 专用（仅 maintain 用）
    │
    └── skill-analyze ────── sub-wiki-reader
                            sub-markdown-gen
                            sub-linker
```

---

## 7. 拆分解决了什么问题

### 7.1 量化对比

| 指标 | 拆分前（单体） | 拆分后 | 改善 |
|------|:-------------:|:------:|:----:|
| AGENTS.md 行数 | ~550 行 | ~100 行（仅核心哲学+路由） | **-80%** |
| 重复的"读取 wiki"实现 | 5 份 | 1 份 | **-80%** |
| 重复的"生成 markdown" | 5 份 | 1 份 | **-80%** |
| 修改"索引格式"的影响面 | 改 2 个 skill | 改 1 个 shared | **-50%** |
| 新增一个 skill 的代价 | 复制粘贴整套读/写/链接逻辑 | 只需声明依赖哪些 shared | **大幅降低** |

### 7.2 具体解决了 5 个问题

#### 问题 1：重复代码

**之前**：每个 skill 都在自己内部实现了"读文件"——`read_by_path` 在 query 写了一遍，在 ingest 又写一遍，在 benchmark 又写一遍。

**之后**：所有 skill 都调用 `sub-wiki-reader`。要改读取逻辑（比如加缓存、加错误处理）只需要改一个地方。

#### 问题 2：上下文污染

**之前**：AGENTS.md 包含查询流程、录入流程、比较流程、lint 流程、模板定义、索引规则、日志规则……每次加载都把所有不相关的内容塞进上下文。

**之后**：AGENTS.md 只保留核心哲学、设计范式、路由规则。具体的 flow 拆分到对应 skill 文件。用户说"查个东西"时，只需要加载 `skill-query.md` 和它依赖的 shared module。

#### 问题 3：难以独立修改

**之前**：想改论文页面的 frontmatter 格式——需要找到 AGENTS.md 里所有的模板定义，逐段修改，还可能漏掉。

**之后**：`sub-frontmatter.md` 是唯一的 frontmatter 生成入口。改格式只改这一个文件。

#### 问题 4：无法单元测试

**之前**：没法单独测试"索引更新"是否正常——因为索引更新逻辑内嵌在 ingest 流程中，测试需要完整跑一遍录入。

**之后**：`sub-index-updater.md` 是一个独立的 subagent skill，可以单独测试"加一条索引条目"或"重新生成索引"。

#### 问题 5：新 skill 入门成本高

**之前**：想加一个新 skill（比如"论文推荐"）——需要从头复制一堆现有的"读 wiki / 写 markdown / 建链接"代码。

**之后**：新 skill 只需写明"我依赖 shared A、B、C"，然后只写自己特有的逻辑。

### 7.3 与任务二范式选择的一致性

拆分后的 skill 结构与任务二选择的 **Harness 约束模式** 完全对齐：

```
Harness 约束规则          →  由谁保障
─────────────────────────────────────
规则 ① 知识源约束         →  sub-wiki-reader（只读 wiki，禁止编造）
规则 ② 证据等级透明        →  sub-markdown-gen（自动标注等级）
规则 ③ 诚实约束            →  sub-wiki-reader（搜索失败返回"找不到"）
规则 ④ 回答格式约束        →  sub-markdown-gen（模板化输出）
规则 ⑤ 领域约束            →  由 AGENTS.md 路由规则保障
规则 ⑥ 只读约束            →  skill-query / skill-benchmark 不包含写入能力
```

---

## 8. 分层架构全貌

### 8.1 最终架构图

```
用户（研究者 / Claude Code）
        │
        ▼
┌─────────────────────────────────────────────────┐
│            Main Agent (AGENTS.md)                │
│                                                   │
│  设计哲学 / 范式选择 / 约束规则 / 路由逻辑        │
│  每种请求 → 路由到对应 main-level skill          │
│  上下文紧的内容 → 留在 AGENTS.md                  │
└────────────────────────┬────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
┌────────────┐  ┌────────────┐  ┌────────────┐
│ skill-query│  │skill-ingest│  │ 其他 skill │  ← skills for main agent
│            │  │            │  │            │     （subagent 的组合）
└──────┬─────┘  └──────┬─────┘  └──────┬─────┘
       │               │               │
       ▼               ▼               ▼
┌─────────────────────────────────────────────┐
│          Shared Subagent Skills              │
│                                              │
│  sub-wiki-reader  │  sub-markdown-gen        │
│  sub-linker       │  sub-index-updater       │
│  sub-logger       │  sub-frontmatter         │  ← skills for subagent
│  sub-qa-judge     │  sub-diff-gen            │     （最小运行单元）
└─────────────────────────────────────────────┘
```

### 8.2 上下文管理策略

| 内容 | 放哪里 | 原因 |
|------|--------|------|
| 设计哲学、范式选择、约束规则 | **AGENTS.md** | 每次会话都需要，上下文紧 |
| 具体 skill 的流程步骤 | **skills/main/*.md** | 按需加载，不需要时不在上下文中 |
| 共享模块的实现细节 | **skills/shared/*.md** | 被多个 skill 引用，只在被调用时加载 |
| TOOLS.md 中的本地配置 | **skills/TOOLS.md** | 环境特定信息，不频繁变化 |

---

> **编写说明**：本文档识别了 llmwiki agent 的 5 个主 skill 和 8 个 subagent 级别 skill，从中找出 6 组重复步骤并提取为 6 个共享模块。拆分后 AGENTS.md 精简约 80%，重复代码消除 80%，新 skill 的创建成本大幅降低。拆分方案与任务二的 Harness 范式约束规则天然对齐。
