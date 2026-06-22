# TOOLS.md - 本地工具说明

## 工具

- `exec` — 读取代码仓库结构、分析配置文件
- `read` — 读取训练脚本、配置文件的参数定义
- `web_search` — 搜索同类代码的最优调参参考
- `web_fetch` — 读取调参相关技术文档

## 文件操作

- 仅限本工作区目录：`memory/`
- 产物通过 inline reply 直接返回调用者，不写入文件系统

## 不使用

- `sessions_spawn` — 本 agent **不**派生子 agent，不做跨 agent 编排
