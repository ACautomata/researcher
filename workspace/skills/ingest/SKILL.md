---
name: ingest
description: Ingest a paper PDF into the wiki as an evidence-traceable paper page, always inside an isolated subagent via the official memory-wiki pipeline (wiki ingest → wiki compile → wiki_lint). Triggers: 入库, ingest paper, add to wiki, 文献笔记, 整理这篇论文.
---

# ingest — 论文 PDF → 结构化 wiki 页面（隔离 subagent + 官方流水线）

## Mission

将研究论文 PDF 转化为符合 wiki 规范的结构化论文页面，确保每条 claim 可追溯到原始来源。这是研究 wiki 的唯一入库入口。

**始终以隔离 subagent 运行**：本 predicate 声明它始终在隔离 subagent（spawn self）内执行。无论由单篇 `ingest`、`paper-ingest`、`paper-read` 还是 `paper-batch-ingest` 触发，main 一律 spawn 一个 isolated subagent 跑本 skill —— PDF 全文永不进 main context。隔离语义由本 predicate 自带，orchestrator 自动继承，无需各自声明。

## 前置条件

- 依赖 **memory-wiki 插件已启用**。`openclaw wiki` CLI（`wiki ingest` / `wiki compile` / `wiki lint`）与 `wiki_apply` / `wiki_lint` / `wiki_search` / `wiki_get` 工具由该插件提供，默认可能未启用；未启用时本 skill 的入库步骤不可用。启用插件 / 改 `openclaw.json` 属独立 runtime 配置变更（需重启 gateway），不在本 skill 职责内。

## When to use

- 新论文 PDF 需要加入 wiki
- 用户请求"入库这篇论文""加入 wiki""整理这篇论文"
- `raw/inbox/` 中有待处理的论文

不要用于：文献查询、跨论文比较、wiki 质量审计（那是 `curate`）。

## 核心原则

- Raw sources 不可变；不修改 `raw/` 下原始文件
- Wiki 受证据约束，不发明不存在的知识；每条持久 claim 追溯到论文页章节和原始来源
- 区分证据等级：`abstract-only` / `skimmed` / `full-paper` / `reproduced`
- 走官方 memory-wiki 流水线建页，不做 freeform page surgery

## 语言

- Wiki 内容默认中文
- 保留原始论文标题、作者、DOI、arXiv、代码链接的原文
- Raw sources 保持原文不变

## 职责边界

**做：**

- 捕获 raw source（PDF），规范命名移入 `raw/sources/`（不可变保留）
- 提取全文，仅作撰写页面的工作材料（不入库、不灌满 vault）
- 组装 11 节论文页 md，staged 到 `raw/sources/<slug>.md`
- 经官方流水线入库：`openclaw wiki ingest <staged md>` → `openclaw wiki compile`
- 跑 `wiki_lint` 校验；成功后删除 staged md，返回 wiki 路径 + `evidence_level`
- 更新 wiki 索引和日志（窄更新，经 `wiki_apply`）

**不做：**

- 不回答文献查询 / 跨论文比较 / wiki 质量 lint（那是 `curate`）
- 不做实验深度提取（那是 `extract`）
- **不用 `wiki_apply` 从零建整页**——那是 freeform page surgery，违背官方定位

## 输入

| Field | Required | Description |
|-------|----------|-------------|
| `pdf_path` | 是 | 源 PDF 路径（`raw/inbox/` 或 `raw/sources/`）或可访问 URL |
| `target_domain` | 推荐 | 论文所属领域子树 |
| `evidence_level` | 否 | 基于 PDF 访问程度（全文提取成功默认 `full-paper`）|

## 执行流程（Capture → Extract → Create → Ingest → Verify）

### 1. Capture
捕获 raw source，规范命名移入 `raw/sources/`（PDF 不可变保留，供溯源与重放入库）。验证文件存在、可读、非空。失败重试一次。

### 2. Extract
提取全文。**仅作撰写页面的工作材料**——不入库、不作为持久页面内容。验证文本长度足够、包含论文结构。失败尝试替代方法一次。

### 3. Create（组装 + staged）
按论文页模板（见 `references/page-templates.md`）组装 11 节论文页 markdown，staged 到 `raw/sources/<slug>.md`，供 `wiki ingest` 消费。填写全部通用 frontmatter 与论文专属 frontmatter（`paper.*`、`classification.*`、`evidence_level`）。包含全部 11 节：Citation, One-Sentence Contribution, Problem Setting, Method, Experiments, Results, Limitations, Reusable Claims, Connections, Open Questions, Provenance。

### 4. Ingest（官方流水线建页）
`openclaw wiki ingest raw/sources/<slug>.md` 然后 `openclaw wiki compile`，使新页面对 `wiki_search` / `wiki_get` 可见。**这是唯一建页路径**；不经 `wiki_apply` 建页。

> **重入库分支（更新已存在页面）**：若 `wiki_search` 发现该论文已有页面，改为对该页做窄更新（synthesis/metadata），经 `wiki_apply`，**不建重复页**。仅在此分支使用 `wiki_apply`。

### 5. Verify
跑 `wiki_lint`（结构、provenance gaps、矛盾、open questions）。成功后**删除 staged md**（`raw/sources/<slug>.md`）——wiki 是页面唯一持久副本，PDF 与提取文本按不可变 raw 原则保留。返回 wiki 路径 + `evidence_level`；失败返回具体原因（PDF 不可读、提取失败、lint 阻塞等）。

### 更新索引与日志
入库成功后，用 `wiki_apply` 对 wiki index 与 log 做追加式窄更新（见 `references/wiki-conventions.md` 的 index/log 规则）。

## 完成门禁

- 一个 raw source（PDF）已捕获且不可变保留；一份全文已提取（仅作工作材料）
- 一个论文页已经官方流水线入库（`wiki ingest` + `wiki compile`），对 `wiki_search`/`wiki_get` 可见
- 页面符合论文模板（**>= 100 行**、有 `evidence_level`、Results 有具体数字）
- `wiki_lint` 通过；staged md 已删除
- 重入库走 `wiki_apply` 窄更新，未产生重复页
- Wiki 索引和日志已更新
- 返回 wiki 路径 + `evidence_level`（成功）或具体原因（失败）

## 质量规则

遵循 `references/wiki-conventions.md` 的命名、索引、日志、链接规范。此外：

- 不编造 claim——每条 claim 追溯到论文页章节
- Experiments 必须包含数据集大小、baseline 名称、训练设置（架构/backbone/优化器/lr/batch/epoch/硬件）、评估协议、消融
- Results 必须为每个 main claim 包含具体数字（如 "AUROC 95.12% vs. MCM 86.05%"，不用"显著优于 baseline"）
- 缺失信息标注"原文未报告"
- 更新已有页面优先于创建重复页面
