---
title: Persistent LLM Wiki
type: concept
domain: meta
status: seed
created: 2026-04-20
updated: 2026-04-25
tags:
  - llm
  - knowledge-management
  - workflow
source_pages:
  - wiki/domains/meta/sources/karpathy-llm-wiki.md
raw_sources:
  - raw/sources/2026-04-20-karpathy-llm-wiki.md
---

# Persistent LLM Wiki

## 定义

Persistent LLM Wiki 是一种工作流：agent 持续把原始材料编译成互相链接的 markdown 知识库。它不是每次查询都从 raw 文件重新发现事实，而是随着时间积累结构化总结、连接、张力和综合。

## 当前理解

- wiki 位于用户与 raw sources 之间。
- raw 层不可变，用来保存 provenance。
- wiki 层会随着新来源进入而持续修订。
- schema 层约束 agent 行为，让维护工作可重复、可纪律化。
- 查询输出本身也可以成为 wiki 中的 durable artifact。

## 证据

- [LLM Wiki](../sources/karpathy-llm-wiki.md)：提出 raw/wiki/schema 架构和 ingest-query-lint 循环。

## 连接

- [Second Brain](../topics/second-brain.md)：本仓库对这个概念的实现。
- [LLM Wiki](../sources/karpathy-llm-wiki.md)：基础来源页。

## 开放问题

- 什么时候应创建新的 concept page，什么时候应把综合保留在更宽的 topic page？
- 当 vault 变大后，检索是否仍应 index-first，还是加入本地 CLI 搜索工具？
