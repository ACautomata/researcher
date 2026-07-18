---
name: ideate
description: Generate or persist evidence-grounded research idea cards anchored to named pain points. Use for research ideas, research directions, or a brainstorm workflow that needs candidate cards or reviewed-card persistence.
---

# ideate — 研究 idea 生成

## Mission

将论文、wiki 上下文、实验记录和项目约束转化为有证据支撑、可比较、可验证的 Idea Card。每张 card 必须锚定具体论文/wiki 页面，或暴露同一痛点的 2–4 篇论文集群。

Card schema 见 `references/idea-card-template.md`；完整输出格式见 `references/output-spec.md`；可选的机会桶策略见 `references/generation-strategies.md`。

## 模式

| 输入 | 行为 | 写入 |
| --- | --- | --- |
| 默认 brief 或 `candidate_only: true` | 标准化 brief → 构建证据上下文 → 生成、去重、校验 card | 默认：写入；`candidate_only`：仅内联返回 |
| `reviewed_cards` | 验证上游已审查的 card，原样持久化 | 仅整批校验通过后写入 |

predicate 不自行裁定最终赢家：它要么生成候选，要么持久化调用方提供的 `survived` 集合。

## 生成路径

1. 标准化 Idea Generation Brief（`references/brief-template.md`）；至少需要研究主题和一项论文、wiki 或实验材料。
2. 提取命名痛点、局限性/未来工作信号，按机会桶生成并去重 card。
3. 每张 card 遵循模板，证据可追溯，含具体 `target_problem`、最小实验、预期指标、风险；弱支撑标记 `low-confidence`。不把输入没有说明的论文事实当作证据。
4. 默认模式生成 5–10 张高信号 card；`candidate_only` 只为分配视角生成 1–3 张完整 card，并在 reply 内联返回，不写 wiki。
5. 默认模式在本会话首次写入前运行 `wiki_status`，然后通过 `wiki_apply` 写入完整输出、更新必要索引，并在 reply 内联返回 card 与写入位置。

## 已审查 Card 持久化

当调用方提供 `reviewed_cards` 时：

1. 先全量验证：每张 card 符合模板、证据可追溯，且有 `challenge`、`verdict: survived`、`verdict_reason`。
2. 任一 card 不合格时，返回完整问题清单；**整个批次不得调用 `wiki_apply`**。空集合同样不写入。
3. 全部通过后，原样写入该批 cards；不生成、去重、合并、补充或改写任何 card/审计记录。优先写入调用方指定的 wiki path；未指定时遵循现有 wiki convention。
4. 写入前运行 `wiki_status`，写入后运行 `wiki_lint`。仅修复本次造成的页面容器、索引、链接或 metadata 问题；不得修改 card 正文、`challenge`、`verdict` 或 `verdict_reason`。修复后再次 lint。
5. 在 reply 内联返回完整持久化 cards、写入位置和 lint 结果。

## 完成门禁

- 生成路径：每张 card 满足模板的证据、痛点、实验、指标和风险要求；去重后每个集群只有最强变体。
- 候选路径：1–3 张完整 card，且没有 wiki 写入。
- 已审查持久化：整批都已验证为 `survived`，或整批拒绝写入；成功写入后 lint 通过。
