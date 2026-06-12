# TOOLS.md

## Wiki 工具（memory-wiki，read+write）

- `wiki_status` — 确认 vault 在线
- `wiki_search` — 搜索论文条目、claim、实验设计
- `wiki_get` — 按 id/path 拉取单页详情
- `wiki_lint` — 检查 wiki 内容一致性；`wiki_apply` 写入后跑一次验证质量
- `wiki_apply` — 完成提示词生成后，将任务提示词归档到论文 wiki 页面

> **Write-Back 原则**：读取 wiki 后产生的产出必须 write back，建立与读取内容的联系。

## 文件操作

- 可读写本 agent workspace 目录内的文件（`memory/` 等）
- 产物通过 inline reply 直接返回调用者，不写入 outputs/
- 只读访问上游阶段产出（wiki、S2-S4 文档）

## 限制

- 无 `sessions_spawn` 权限——本 agent 不派生子 agent
- 不修改其他 agent 的产出
