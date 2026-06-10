# TOOLS.md - Available Tools

## Wiki 工具（memory-wiki，read+write 模式）

- `wiki_status` — 查 vault 模式和健康度；首次写 wiki 之前先跑一次
- `wiki_search` — 搜 wiki 页面；检查论文是否已存在
- `wiki_get` — 按 id 或 path 读单页
- `wiki_apply` — 创建或修改 wiki 页面
- `wiki_lint` — 跑结构检查；创建论文页后验证质量

## 文件操作

- 读写 own workspace 目录下的文件
- raw/sources/ 和 raw/inbox/ 的文件操作

## 不可用工具

- 不使用 sessions_spawn（本 agent 不 spawn 子 agent）
