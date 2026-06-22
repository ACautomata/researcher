# TOOLS.md - 本地工具说明

## 工具

- `read` — 读取模型定义文件、训练脚本
- `exec` — 快速查看目录结构和文件
- `web_search` — 搜索同类架构的最佳实践参考

## 文件操作

- 仅限本工作区目录：`memory/`
- 产物通过 inline reply 直接返回调用者，不写入文件系统

## 不使用

- `sessions_spawn` — 本 agent **不**派生子 agent，不做跨 agent 编排
