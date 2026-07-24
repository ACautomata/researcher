---
name: paper-validate
description: Turn a paper's problems into executable validation (design → spec). Requires critic's analysis already in the wiki. Triggers: 验证设计, paper-validate, 设计验证实验, 验证实验, 怎么验证这个 claim.
---

# paper-validate — 验证实验设计 + 实现规格

把论文已识别的问题转成可执行的验证。

**前置依赖**：需要 `critic` 的问题分析已在 wiki。`paper-validate` 不自动运行 `critic`（critic 是独立 predicate）。

## 编排

1. **`design`** — 基于 `critic` 问题分析，产出验证实验设计（备好 md 经 `ingest` 写入 wiki）。
2. **`spec`** — 基于 `design`，生成 claude-code 任务提示词（备好 md 经 `ingest` 写入 wiki）。

### Pre-check

用 `wiki_search` 检查 `critic` 问题分析是否已在 wiki。**缺失则不自动运行 `critic`**——先运行 `critic`（或完整分析链的 read→critic），再回来 `paper-validate`。

### 完成后

呈现优先验证实验、claude-code 任务提示词要点，附 wiki 路径。建议下一步：把 spec 提示词发给 claude-code 执行，或 `paper-audit` 审计整条链。

## 输入

| Field | Required | Description |
|-------|----------|-------------|
| 论文（wiki page） | 是 | 已入库的论文 |
| critic 问题分析（wiki） | 是（前置） | 必须已存在 |
| 代码仓库路径 | 否 | `spec` 生成时参考 |
