# TOOLS.md - 本地说明

## 约定

- 输出优先使用 Markdown，方便直接落到 Obsidian 或仓库里
- 严格遵循 `paper-experiment-deep-extractor` skill 的 11 节输出结构
- 可复用的流程经验放进 `MEMORY.md`

## 工作区内技能

- `paper-experiment-deep-extractor`（S2：实验深度提取）

## Wiki 工具（memory-wiki，read+write）

- `wiki_status` — 确认 vault 在线且可读
- `wiki_search` — 搜既有论文条目 / 相关 claim / 已记录的实验设计
- `wiki_get` — 按 id/path 拉单页详情，作为实验提取的输入
- `wiki_lint` — 引用 wiki 内容前跑一次确认没有 contradiction；`wiki_apply` 写入后跑一次验证质量
- `wiki_apply` — 完成提取后，将 12 节实验提取文档的关键产出 write back 到论文 wiki 页面

> **Write-Back 原则**：读取 wiki 后产生的产出必须 write back，建立与读取内容的联系。

## 文件操作

- 仅限本工作区目录：`memory/`
- 产物通过 inline reply 直接返回调用者，不写入文件系统

## 不使用的工具

- `sessions_spawn` — 本 agent **不**派生子 agent，不做跨 agent 编排
