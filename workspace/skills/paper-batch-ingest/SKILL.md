---
name: paper-batch-ingest
description: Batch-ingest many papers - spawn one subagent (self, isolated context) per paper to run the ingest skill. Triggers: 批量入库, 多篇论文录入, 批量录入论文, batch ingest, ingest multiple papers.
---

# paper-batch-ingest - 多篇论文批量录入

把多篇论文批量录入 wiki。对每篇论文启动一个 subagent（你自己的隔离 session，独立 context），提示它运行 `ingest` predicate 录入。每篇独立 context，避免单次录入多篇时 main context 爆炸；多篇可并行（受 `maxConcurrent` 限制）。

## 编排

对每篇论文调用一次 `sessions_spawn`：

```text
sessions_spawn(
  task="运行 ingest predicate，把论文 <path-or-url> 录入 wiki（target_domain=<domain>）。完成后返回 wiki 路径和 evidence_level；失败则返回具体原因。",
  label="ingest-<unique-slug>",
  context="isolated",
  mode="run",
  runTimeoutSeconds=1800
)
```

**省略 `agentId`**：目标默认是 requester（main 自己），不受 cross-agent `allowAgents` 限制。每篇一个 spawn；连续调用即可并行，超过 `maxConcurrent` 的任务排队。

全部发出后调用 `sessions_yield`，结束当前 turn，等待 completion events。完成是 push-based；不要轮询 `subagents` / `sessions_list` / `sessions_history`。

子 session 共享 main workspace 和 predicate skill，但 context 隔离；默认拿不到 `memory_search` / `memory_get`，所以论文路径、domain 和特殊要求必须完整写入 `task`。

### Pre-check

- 确认论文列表（PDF 路径/URL，每篇一个）。
- 用 `wiki_search` 标记已入库的（默认跳过，除非用户要求重入库）。
- 批量较大时分批 spawn：同时存活的子 session 受 `maxConcurrent`（默认 8）限制，超过则排队。

### 完成后

汇总每篇结果：

- **成功**：wiki 路径 + `evidence_level`。
- **失败**：论文 + 原因（PDF 不可读、提取失败等）。
- **跳过**：已入库且未要求重入库。

失败的列出，可单独重试（再 `sessions_spawn` 一篇）或报告用户。建议下一步：`curate`（lint 模式）批量检查新页面，或 `paper-read` 深读某篇。

## 完成门禁

- 每个输入论文都有且只有一个终态：**成功 / 失败 / 跳过**。
- 每个成功项包含 wiki 路径 + `evidence_level`；每个失败项包含具体原因。
- 已发出的子 session 全部完成或超时后才汇总，不在部分结果到达时提前结束。

## 输入

| Field | Required | Description |
|-------|----------|-------------|
| 论文列表 | 是 | PDF 路径/URL 列表（每篇一行），或一个含论文的目录路径 |
| target_domain | 推荐 | 论文所属领域子树 |
| 重入库已存在 | 否 | 默认跳过已入库；设 true 强制重入库 |
