# TOOLS.md - Local Notes

## Wiki 工具 (read+write)

Wiki 是本 agent 的主战场。优先用 memory-wiki 工具操作,**不要**直接读写 `~/.openclaw/wiki/main/` 文件树。

- `wiki_status` — 查 vault 模式 / 健康度 / Obsidian CLI 状态;每次会话首次写 wiki 之前先跑一次。
- `wiki_search` — 搜 wiki 页面;通过 mode flag 切换 person lookup / question routing / source evidence / 原始 claim 钻取。
- `wiki_get` — 按 id 或 path 读单页;找不到时会回落到 shared memory corpus。
- `wiki_apply` — 做有限范围的 synthesis 或 metadata 修改,比手写页面更稳。
- `wiki_lint` — 跑 provenance gap / contradiction / open question 结构检查;每次大批量改 wiki 后必跑。

## 文件操作

- 仅可读写 `workspace/curate/` 目录下的文件 (memory/、MEMORY.md、HEARTBEAT.md、DREAMS.md、本目录配置)
- 不可读写 raw/ 下的原始文件 (那是 ingest agent 的职责)
- 不可读写其他 agent workspace 下的文件

## 不使用的工具

- `sessions_spawn` — 本 agent 不 spawn 子 agent,所有任务在自身 session 内完成
- PDF 提取工具 — 那是 ingest agent 的职责
- 实验执行工具 — 那是 extract / critic / design / spec 的职责

## 为什么分开

Skills 定义工具怎么用,这个文件记录本 agent 特有的配置和路径。分开意味着更新 skills 不会丢失本地笔记。

Dashboard 自动写到 `~/.openclaw/wiki/main/reports/` (`open-questions.md`、`contradictions.md`、`stale-pages.md`、`claim-health.md` 等)。要查 wiki 健康度时用 `wiki_get` 读这些 dashboard,不要扫文件。
