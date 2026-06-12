# TOOLS.md — Local Notes

## 会话管理工具

本 agent 是 depth-1 orchestrator（当 `maxSpawnDepth >= 2` 时），拥有以下会话管理权限：

- `sessions_spawn` — 派发子任务给 worker subagents（ingest, curate, extract, critic, design, spec, audit, ideate, judge）
- `subagents` — 查看子任务状态
- `sessions_list` — 列出活跃 session
- `sessions_history` — 查看历史 session

**注意：** 本 agent 不能进一步派发给其他 orchestrator（depth-2 的 worker 没有 `sessions_spawn` 权限）。

## Wiki 工具 (read-only)

- `wiki_search` — 查 wiki 以理解上下文（仅读）
- `wiki_get` — 读 wiki 页面（仅读）
- `wiki_lint` — 不直接使用；这是 curate 的职责

## 文件操作

- 仅可读写 `workspace/orchestrate/` 目录下的文件 (memory/、MEMORY.md、HEARTBEAT.md、DREAMS.md)
- 不可读写其他 agent workspace 下的文件

## 不使用的工具

- 论文分析工具 — 那是 worker 的职责
- 实验执行工具 — 那是 extract / critic / design / spec 的职责
- wiki 写入工具（`wiki_apply`）— 本 agent 不直接写 wiki 页面；子 agent（extract/critic/design/spec/audit/ideate/curate）自行负责其产出的 write-back
- PDF 提取工具 — 那是 ingest 的职责

## 为什么分开

Skills 定义工具怎么用，这个文件记录本 agent 特有的配置和路径。分开意味着更新 skills 不会丢失本地笔记。
