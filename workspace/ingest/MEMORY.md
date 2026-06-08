# MEMORY.md - Initial Memory

_论文 PDF 摄入 agent 的初始记忆。_

## 职责

Paper PDF ingestion → wiki page creation

## 核心规范

- 论文页结构：11 节模板（Citation → Provenance）
- 命名：raw sources 用 `YYYY-MM-DD-short-title.ext`
- 证据等级：abstract-only / skimmed / full-paper / reproduced
- Wiki 内容中文，保留原文标题和引用信息

## 维护规则

- 每次操作后更新 wiki/log.md（追加式）
- 每次新增或更改持久页面后更新 wiki/index.md
- 不确定时标"待验证"
