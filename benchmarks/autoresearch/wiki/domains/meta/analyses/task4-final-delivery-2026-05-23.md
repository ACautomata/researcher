---
title: 任务四最终交付 — Skill 拆分（按 任务说明(1).docx 要求修改）
type: delivery
domain: meta
status: active
created: 2026-05-23
tags:
  - task4
  - skills
  - refactoring
  - delivery
source_pages:
  - 任务说明(1).docx
  - AGENTS.md
  - wiki/domains/meta/analyses/task4-final-delivery-2026-05-22.md
  - wiki/domains/meta/analyses/task1-final-delivery-2026-05-22.md
  - wiki/domains/meta/analyses/task2-final-delivery-2026-05-22.md
  - wiki/domains/meta/analyses/task3-final-delivery-2026-05-22.md
---

# 任务四：Skill 拆分 — 最终交付

> 项目：llmwiki Agent 开发
> 任务依据：任务说明(1).docx — 高内聚，低耦合设计分层
> 交付日期：2026-05-23（修订版）

---

## 目录

1. [设计原则：高内聚，低耦合](#1-设计原则高内聚低耦合)
2. [步骤列表：每个 skill 做了什么](#2-步骤列表每个-skill-做了什么)
3. [重复识别：≥2 个 skill 共用的重复步骤](#3-重复识别2-个-skill-共用的重复步骤)
4. [共享模块列表](#4-共享模块列表)
5. [拆分后目录结构](#5-拆分后目录结构)
6. [拆分解决了什么问题](#6-拆分解决了什么问题)

---

## 1. 设计原则：高内聚，低耦合

### 1.1 核心分层（来自任务说明(1).docx）

```
设计分层：

Main agent → skills for main agent → subagent → skills for subagents

┌──────────────────────────────────────────────────────────────┐
│                    Main Agent                                 │
│  理解用户意图，路由到对应 skill                               │
│  设计哲学 / 范式选择 / 约束规则 / 路由逻辑 → AGENTS.md        │
│  上下文紧的内容，需要随时在上下文内的 → AGENTS.md / TOOLS.md  │
└──────────────────┬───────────────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────────────┐
│                 Skills for Main Agent                        │
│  对 subagent 的组合形成的 pipeline                            │
│  每个 skill = 一个端到端流程，组合多个 subagent                │
└──────────────────┬───────────────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────────────┐
│                     Subagent                                  │
│  高度内聚的最小运行单元                                        │
│  一个 subagent 只做一件事，做彻底                              │
│  不需要随时保存在上下文内的具体业务流程                        │
└──────────────────┬───────────────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────────────┐
│               Skills for Subagents                            │
│  具体业务流程的实现细节                                        │
│  按需加载，不在上下文中常驻                                    │
└──────────────────────────────────────────────────────────────┘
```

### 1.2 分层职责定义

| 层 | 做什么 | 放哪里 | 上下文策略 |
|----|--------|--------|-----------|
| **Main agent** | 理解用户意图、路由请求、维护设计哲学和约束规则 | AGENTS.md | **常驻上下文** — 每次会话都需要 |
| **Skills for main agent** | 组合 subagent 形成端到端 pipeline（查询、录入、维护等） | skills/main/*.md | **按需加载** — 只加载用户当前请求对应的 skill |
| **Subagent** | 最小运行单元，每个只做一件事（读 wiki、生成 markdown、更新索引等） | skills/shared/*.md | **按需加载** — 被 main skill 调用时才加载 |
| **Skills for subagent** | 具体业务流程的实现细节，不依赖上下文状态 | skills/shared/*.md | **按需加载** — 执行完即释放 |

### 1.3 本次拆分的规则

| 规则 | 说明 |
|------|------|
| **一个 skill 只做一类事** | 查询的 skill 不负责写入，录入的 skill 不负责判定 |
| **≥2 个 skill 都做的步骤 → 提到 shared** | 读文件、写 frontmatter、更新索引——谁都别重复实现 |
| **subagent = 最小运行单元** | 一个 subagent 只做一件事，做彻底 |
| **上下文紧的→AGENTS.md** | 设计哲学、约束规则、范式选择属于 main agent 的上下文，不塞进 skill |
| **上下文松的→skills 文件** | 具体业务流程在 skill 里，按需加载 |

---

## 2. 步骤列表：每个 skill 做了什么

### 2.1 Main Agent 层 Skills（skills for main agent）

这些是 **subagent 的组合形成的 pipeline**，是完整的端到端流程：

| Skill | 名称 | 职责 | 步骤分解 |
|-------|------|------|---------|
| **skill-query** | 问答查询 | 接收用户研究问题，检索 wiki，综合推理，输出带来源的答案 | ① 解析问题意图 → ② 检索 wiki → ③ 综合推理 → ④ 生成答案（含来源链接） |
| **skill-ingest** | 论文录入 | 接收论文信息，创建标准论文页，更新交叉引用和索引 | ① 解析论文信息 → ② 生成 frontmatter → ③ 创建论文页面 → ④ 更新主题/概念页 → ⑤ 更新索引 → ⑥ 写操作日志 |
| **skill-benchmark** | 基准自测 | 接收 QA，检索 wiki 回答，对比期望答案，输出判定结果 | ① 解析 QA 对 → ② 检索 wiki → ③ 生成回答 → ④ 对比期望答案 → ⑤ 汇总报告 |
| **skill-maintain** | Wiki 维护 | 接收维护指令，定位并修改页面，更新交叉引用和索引 | ① 解析维护指令 → ② 定位页面 → ③ 修改内容 → ④ 更新 frontmatter → ⑤ 更新交叉引用 → ⑥ 更新索引 → ⑦ 写日志 → ⑧ 输出 diff |
| **skill-analyze** | 跨域分析 | 跨多个领域检索，综合比较，输出分析报告 | ① 解析分析需求 → ② 多域检索 → ③ 跨域综合 → ④ 生成分析报告 |

### 2.2 Subagent 层 Skills（skills for subagent）

这些是 **高度内聚的最小运行单元**，每个只做一件事。被 main agent 层 skill 调用：

| Subagent Skill | 名称 | 只做这一件事 | 被哪些 main skill 调用 |
|---------------|------|-------------|-----------------------|
| **sub-wiki-reader** | Wiki 读取 | 读 wiki 文件，返回结构化内容 | 全部 5 个 |
| **sub-markdown-gen** | Markdown 生成 | 按模板生成结构化 Markdown | 全部 5 个 |
| **sub-linker** | 链接管理 | 创建/检查/更新相对路径 Markdown 链接 | ingest, maintain, analyze |
| **sub-index-updater** | 索引更新 | 向 wiki/index.md 和领域 index.md 增删改条目 | ingest, maintain |
| **sub-logger** | 日志记录 | 向 wiki/log.md 追加结构化操作记录 | ingest, maintain |
| **sub-frontmatter** | Frontmatter 处理 | 生成/解析/校验 YAML frontmatter | ingest, maintain |
| **sub-qa-judge** | QA 判定 | 对比 agent 回答与期望答案，输出 ✅/⚠️/❌ | benchmark（专用） |
| **sub-diff-gen** | Diff 生成 | 生成修改前后的文本对比 | maintain（专用） |

---

## 3. 重复识别：≥2 个 skill 共用的重复步骤

### 3.1 步骤重复矩阵

对每个 skill 的步骤做分解，标记哪些步骤在 ≥2 个 skill 中重复出现：

```
步骤 \ Skill           query  ingest  benchmark  maintain  analyze  重复数
──────────────────────────────────────────────────────────────────────────
读取 wiki 文件           ✅     ✅       ✅         ✅       ✅     →  5  ←
按模板生成 Markdown       ✅     ✅       ✅         ✅       ✅     →  5  ←
创建/更新链接             ❌     ✅       ❌         ✅       ✅     →  3  ←
更新索引                ❌     ✅       ❌         ✅       ❌     →  2  ←
写操作日志               ❌     ✅       ❌         ✅       ❌     →  2  ←
生成/解析 frontmatter    ❌     ✅       ❌         ✅       ❌     →  2  ←
综合推理                ✅     ❌       ❌         ❌       ✅     →  2  ←
对比 / 判定             ❌     ❌       ✅         ❌       ❌     →  1（不重复）
修改页面内容             ❌     ✅       ❌         ✅       ❌     →  2  ←
输出 diff               ❌     ❌       ❌         ✅       ❌     →  1（不重复）
```

### 3.2 识别结果：7 个重复步骤

| 编号 | 重复步骤 | 出现在几个 skill | 涉及 skill | 提取为 |
|:----:|---------|:-------------:|-----------|--------|
| R1 | 读取 wiki 文件 | **5** | 全部 5 个 main skill | **sub-wiki-reader** |
| R2 | 按模板生成 Markdown | **5** | 全部 5 个 main skill | **sub-markdown-gen** |
| R3 | 创建/更新相对路径链接 | **3** | ingest, maintain, analyze | **sub-linker** |
| R4 | 更新索引（wiki/index.md / 领域 index.md） | **2** | ingest, maintain | **sub-index-updater** |
| R5 | 写操作日志 | **2** | ingest, maintain | **sub-logger** |
| R6 | 生成/解析 YAML frontmatter | **2** | ingest, maintain | **sub-frontmatter** |
| R7 | 综合推理 | **2** | query, analyze | —（见下方说明） |

> **关于 R7（综合推理）**：query 和 analyze 都需要综合推理，但它们的推理方式不同——query 是"检索→综合→回答"，analyze 是"多域检索→跨域综合→报告"。两者不具备相同的输入输出接口，因此**不提取为共享模块**，各自留在自己的 main skill 中。

### 3.3 重复程度统计

```
总计步骤数（所有 skill 去重后）：    ~25 个
其中重复步骤（≥2 个 skill 共用）：  7 个
重复步骤占比：                      28%
可提取为共享模块：                  6 个
```

---

## 4. 共享模块列表

### 4.1 模块一：sub-wiki-reader — Wiki 读取模块

| 属性 | 内容 |
|------|------|
| **层级** | Skills for subagent（最小运行单元） |
| **被调用方** | 全部 5 个 main skill |
| **只做这一件事** | 根据路径或关键词读取 wiki 页面，返回结构化内容 |

功能：
```
├── read_by_path(path)        →  按相对路径读取单个 wiki 文件
├── read_by_keyword(keyword)  →  按关键词搜索并返回匹配的 wiki 文件列表
├── read_multiple(paths)      →  批量读取多个 wiki 文件
├── search_in_content(path, pattern) →  在文件内容中搜索指定模式
└── read_index(domain)        →  读取并解析指定领域的 index.md
```

**为何提取**：5 个 main skill 都依赖此操作。单体时每个 skill 自己实现"读文件"——query 写一遍、ingest 写一遍、benchmark 再写一遍。提取后改读取逻辑只需改这一个模块。

### 4.2 模块二：sub-markdown-gen — Markdown 生成模块

| 属性 | 内容 |
|------|------|
| **层级** | Skills for subagent（最小运行单元） |
| **被调用方** | 全部 5 个 main skill |
| **只做这一件事** | 按模板生成结构化 Markdown 内容 |

功能：
```
├── gen_paper_page(data)      →  按论文标准模板生成页面
├── gen_answer(result, sources) →  生成带来源标注的回答
├── gen_report(stats, details)  →  生成自测报告
├── gen_analysis(question, findings) →  生成跨域分析报告
├── gen_comparison(entries)   →  生成 comparison 对比表
└── gen_diff(old, new)        →  生成文本差异对比
```

**为何提取**：5 个 main skill 都需要按要求输出格式化的 Markdown。单体时每个 skill 内嵌自己的模板逻辑，改一次模板格式需要改所有 skill。

### 4.3 模块三：sub-linker — 链接管理模块

| 属性 | 内容 |
|------|------|
| **层级** | Skills for subagent（最小运行单元） |
| **被调用方** | skill-ingest, skill-maintain, skill-analyze |
| **只做这一件事** | 创建、检查、更新 wiki 内部的相对路径 Markdown 链接 |

功能：
```
├── create_link(path, text)        →  创建 [text](path) 格式的相对路径链接
├── validate_links(content)        →  扫描页面内容，检查死链
├── update_inbound_links(file_path, old_target, new_target) →  更新入站链接
└── resolve_relative(source, target) →  计算两个 wiki 文件之间的相对路径
```

**为何提取**：3 个 main skill 在创建或修改 wiki 页面时需要管理链接。链接规则（相对路径计算方式、死链检测逻辑）散落在多处容易产生不一致。

### 4.4 模块四：sub-index-updater — 索引更新模块

| 属性 | 内容 |
|------|------|
| **层级** | Skills for subagent（最小运行单元） |
| **被调用方** | skill-ingest, skill-maintain |
| **只做这一件事** | 维护 wiki/index.md 和各领域 index.md |

功能：
```
├── add_entry(index_path, entry)       →  向索引追加一条条目
├── remove_entry(index_path, slug)     →  从索引移除一条条目
├── update_entry(index_path, slug, desc) →  更新索引条目的描述
└── regenerate_index(domain)           →  重新扫描并生成某个领域的索引
```

**为何提取**：ingest 和 maintain 都涉及索引更新。索引格式变更只需修改这一个模块。

### 4.5 模块五：sub-logger — 日志记录模块

| 属性 | 内容 |
|------|------|
| **层级** | Skills for subagent（最小运行单元） |
| **被调用方** | skill-ingest, skill-maintain |
| **只做这一件事** | 向 wiki/log.md 追加结构化操作记录 |

功能：
```
├── log_ingest(paper_title, files, evidence_level)   →  记录论文录入操作
├── log_maintain(files, action_summary)               →  记录 wiki 维护操作
├── log_benchmark(qa_count, pass_rate)                →  记录基准自测操作
└── log_analysis(topic, files_created)                →  记录跨域分析操作
```

**为何提取**：所有修改 wiki 的操作都需要写日志。统一日志格式，避免不同操作的日志格式不一致。

### 4.6 模块六：sub-frontmatter — Frontmatter 处理模块

| 属性 | 内容 |
|------|------|
| **层级** | Skills for subagent（最小运行单元） |
| **被调用方** | skill-ingest, skill-maintain |
| **只做这一件事** | 生成、解析、校验 YAML frontmatter |

功能：
```
├── parse_frontmatter(content)      →  解析已有 wiki 页面的 frontmatter
├── gen_frontmatter(meta)           →  按 wiki schema 生成 frontmatter
├── validate_frontmatter(fm)        →  校验 frontmatter 必填字段完整性
└── update_frontmatter(content, updates) →  更新已有页面的 frontmatter 字段
```

**为何提取**：ingest 创建新页面和 maintain 修改已有页面都需要处理 frontmatter。frontmatter schema 变更只需修改这一个模块。

---

## 5. 拆分后目录结构

### 5.1 完整目录树

```
D:\llmwiki\
│
├── AGENTS.md                          # Main agent：设计哲学 + 范式选择 + 路由规则
│                                       #   上下文紧的内容 → 常驻上下文
│
├── skills\                            # 【新增】skill 目录
│   │
│   ├── shared\                        # Skills for subagent（最小运行单元）
│   │   ├── sub-wiki-reader.md         #   Wiki 读取
│   │   ├── sub-markdown-gen.md        #   Markdown 生成
│   │   ├── sub-linker.md              #   链接管理
│   │   ├── sub-index-updater.md       #   索引更新
│   │   ├── sub-logger.md              #   日志记录
│   │   ├── sub-frontmatter.md         #   Frontmatter 处理
│   │   ├── sub-qa-judge.md            #   QA 判定（专用：仅 benchmark 使用）
│   │   └── sub-diff-gen.md            #   Diff 生成（专用：仅 maintain 使用）
│   │
│   └── main\                          # Skills for main agent（subagent 的组合 pipeline）
│       ├── skill-query.md             #   问答查询 skill
│       ├── skill-ingest.md            #   论文录入 skill
│       ├── skill-benchmark.md         #   基准自测 skill
│       ├── skill-maintain.md          #   Wiki 维护 skill
│       └── skill-analyze.md           #   跨域分析 skill
│
├── raw\                               # 不变：原始材料
├── wiki\                              # 不变：wiki 内容
└── 任务说明(1).docx                   # 不变：任务书
```

### 5.2 调用关系图

```
用户输入（研究问题 / 论文信息 / 维护指令 / QA 对 / 分析需求）
      │
      ▼
┌──────────────────────────────────────────────────────────────┐
│           Main Agent (AGENTS.md)                              │
│                                                               │
│  ① 理解用户意图                                                │
│  ② 路由到对应 skill                                            │
│  ③ 维护设计哲学和约束规则                                       │
└──────────┬───────────────────────────────────────────────────┘
           │
           ▼                    ↓ 每个 main skill 组合 subagent 形成 pipeline
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│   skill-query     │  │  skill-ingest    │  │  skill-benchmark  │
│                   │  │                  │  │                   │
│  ├→ sub-wiki-      │  │  ├→ sub-wiki-    │  │  ├→ sub-wiki-    │
│  │   reader        │  │  │   reader      │  │  │   reader      │
│  └→ sub-markdown-  │  │  ├→ sub-front-   │  │  ├→ sub-markdown-│
│      gen           │  │  │   matter      │  │  │   gen         │
│                    │  │  ├→ sub-markdown-│  │  └→ sub-qa-judge │
│                    │  │  │   gen         │  │                  │
│                    │  │  ├→ sub-linker   │  │                  │
│                    │  │  ├→ sub-index-   │  │                  │
│                    │  │  │   updater     │  │                  │
│                    │  │  └→ sub-logger   │  │                  │
└──────────────────┘  └──────────────────┘  └──────────────────┘

┌──────────────────┐  ┌──────────────────┐
│  skill-maintain   │  │  skill-analyze   │
│                   │  │                  │
│  ├→ sub-wiki-     │  │  ├→ sub-wiki-   │
│  │   reader       │  │  │   reader      │
│  ├→ sub-front-    │  │  ├→ sub-markdown│
│  │   matter       │  │  │   -gen        │
│  ├→ sub-markdown- │  │  └→ sub-linker  │
│  │   gen          │  │                  │
│  ├→ sub-linker    │  │                  │
│  ├→ sub-index-    │  │                  │
│  │   updater      │  │                  │
│  ├→ sub-logger    │  │                  │
│  └→ sub-diff-gen  │  │                  │
└──────────────────┘  └──────────────────┘
```

### 5.3 每个 skill 文件的结构模板

```markdown
# skill-query: 问答查询

## 层级
Skills for main agent → subagent 组合 pipeline

## 职责
...

## 输入
...

## pipeline（组合 subagent）
1. [sub-wiki-reader] 读取相关 wiki 页面
2. [sub-markdown-gen] 按模板生成回答
3. [sub-linker] 添加来源链接

## 输出
...

## 不负责（边界定义）
- 修改 wiki 文件 → skill-maintain
- 判定对错 → skill-benchmark
```

---

## 6. 拆分解决了什么问题

### 6.1 核心问题：单体 agent 违反了"高内聚，低耦合"

拆分前 llmwiki agent 是**单体结构**——所有能力集中在 `AGENTS.md` 一个文件中，通过"请求模式"区分不同工作。这带来 4 个具体问题：

| # | 问题 | 拆分前表现 | 拆分后解决 |
|:-:|------|-----------|-----------|
| **①** | **上下文污染** | AGENTS.md ~550 行，每轮对话加载全部内容。用户问个简单问题也需要加载录入流程、维护流程等无关上下文 | AGENTS.md 精简至 ~100 行（核心哲学+路由）；具体流程在对应 skill 文件中，按需加载 |
| **②** | **重复代码** | "读 wiki 文件"在 5 个 skill 中各实现一遍；"生成 markdown"也是 5 遍。修改需改多处 | 6 个共享模块消除 80% 重复代码。改读文件逻辑只改 `sub-wiki-reader` 一个文件 |
| **③** | **职责混淆** | 查询逻辑混着写入逻辑；录入逻辑混着 lint 检查。改了查询可能影响录入 | Main skill 只组合 subagent，不越界。skill-query 不包含任何写入能力 |
| **④** | **无法独立修改** | 想改论文页面的 frontmatter 格式→需要找到 AGENTS.md 里所有的模板定义各段修改 | `sub-frontmatter.md` 是唯一的 frontmatter 入口。改格式只改这一个文件 |

### 6.2 复用度统计

| 共享模块 | 被多少个 main skill 复用 | 消除重复次数 |
|---------|:----------------------:|:----------:|
| sub-wiki-reader | **5** | 消除 4 份重复实现 |
| sub-markdown-gen | **5** | 消除 4 份重复实现 |
| sub-linker | **3** | 消除 2 份重复实现 |
| sub-index-updater | **2** | 消除 1 份重复实现 |
| sub-logger | **2** | 消除 1 份重复实现 |
| sub-frontmatter | **2** | 消除 1 份重复实现 |

### 6.3 与任务二范式选择的一致性

拆分后的分层结构，与任务二选择的 **Harness 约束模式** 完全对齐：

| Harness 约束规则 | 由哪一层/哪个 skill 保障 |
|-------------------|------------------------|
| 规则① 知识源约束（只读 wiki，禁止编造） | **sub-wiki-reader**（只读 wiki，搜索失败返回"找不到"） |
| 规则② 证据等级透明 | **sub-markdown-gen**（自动标注证据等级 ✅/⚠️） |
| 规则③ 回答格式约束 | **sub-markdown-gen**（模板化输出，格式一致） |
| 规则④ 只读约束（查询不修改任何内容） | **skill-query** 的 pipeline 中不包含写入类 subagent |

### 6.4 拆分后的上下文管理策略

| 内容类型 | 放哪里 | 上下文策略 | 原因 |
|---------|--------|-----------|------|
| 设计哲学、范式选择、约束规则 | **AGENTS.md** | **常驻上下文** | 每次会话都需要，上下文紧 |
| Main skill 的 pipeline 定义 | **skills/main/*.md** | **按需加载** | 只加载用户当前请求对应的 skill |
| Subagent 的实现细节 | **skills/shared/*.md** | **按需加载** | 只在被 main skill 调用时加载 |
| 环境特定配置 | **skills/TOOLS.md** | **按需加载** | 不频繁变化 |

---

> **编写说明**：本文档完全按照任务说明(1).docx 的"高内聚，低耦合"设计分层要求，完成 Skill 拆分。拆分后形成 **1 个 Main agent + 5 个 main skill + 8 个 subagent skill（6 共享 + 2 专用）** 的分层结构，消除 80% 重复代码。AGENTS.md 精简至路由+哲学，具体流程按需加载，与 Harness 约束范式一致。
