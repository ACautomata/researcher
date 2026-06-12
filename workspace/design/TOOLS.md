# TOOLS.md - 本地说明

## Wiki 工具（read+write）

本 agent 通过 wiki 工具访问论文信息：

- `wiki_status` — 确认 vault 在线且可读
- `wiki_search` — 搜索论文条目、相关 claim、已有实验设计
- `wiki_get` — 按 id/path 拉取单页详情
- `wiki_lint` — 引用 wiki 前确认无 contradiction；`wiki_apply` 写入后跑一次验证质量
- `wiki_apply` — 完成实验设计后，将验证方案 write back 到论文 wiki 页面

> **Write-Back 原则**：读取 wiki 后产生的产出必须 write back，建立与读取内容的联系。发现 wiki 缺失或错误时，同样通过 wiki_apply 修正。

## 文件操作

可在本 workspace 目录内读写文件（memory/ 等）。产物通过 inline reply 返回调用者，不写入 outputs/。

## 无子 agent 调度

本 agent 不使用 sessions_spawn，不调度其他 agent。

## 工作区内技能

- `paper-validation-experiment-designer`（S4）
