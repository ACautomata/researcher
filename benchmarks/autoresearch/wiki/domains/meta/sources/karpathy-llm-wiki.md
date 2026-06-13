---
title: LLM Wiki
type: source
domain: meta
status: stable
created: 2026-04-20
updated: 2026-04-25
tags:
  - llm
  - knowledge-management
  - wiki
  - second-brain
raw_sources:
  - raw/sources/2026-04-20-karpathy-llm-wiki.md
---

# LLM Wiki

## 总结

这个来源定义了本仓库的运行模型：一个本地优先知识库，由 LLM 把 raw materials 逐步编译成可维护的 markdown wiki。关键转变是从一次性检索 raw files，转向持续积累 summary、links、synthesis 和 disagreements 的持久 artifact。

## 要点

- raw sources 应保持不可变，并作为 source of truth。
- maintained wiki 是用户阅读、LLM 编辑的工作知识层。
- `AGENTS.md` 这样的 schema 文件是必要的，它让 agent 像有纪律的 maintainer 一样工作。
- `wiki/index.md` 应作为深入阅读前的第一导航层。
- `wiki/log.md` 应长期记录 ingests、queries 和 maintenance。
- 有用的查询输出应回写到 wiki，而不是消失在聊天历史里。

## 为什么重要

这个来源奠定了 vault 的架构和工作流。它意味着 second brain 应随着每次交互变得更结构化、更有用，而不是把每次对话都当成新的检索问题。

## 连接

- [Persistent LLM Wiki](../concepts/persistent-llm-wiki.md)：提炼这里引入的核心概念。
- [Second Brain](../topics/second-brain.md)：把这个模式应用到当前仓库。

## 开放问题

- 这个 vault 到什么规模会需要 `wiki/index.md` 之外的本地搜索工具？
- 用户的哪些 recurring interests 应尽早成为专门 topic 或 entity 页？
- 一个回答什么时候应进入 `analyses/`，什么时候应折叠进已有页面？

## 来源

- [Raw source](../../../../raw/sources/2026-04-20-karpathy-llm-wiki.md)
- [Original URL](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
