---
status: accepted
---

# 三 predicate skill (ideate/critic/design) md 产出加 `category` tag

## Context

`ingest` 的 md 写入分支统一消费 7 个 predicate 的 markdown（`extract` / `critic` / `design` / `spec` / `audit` / `ideate` / `curate`，见 [ingest SKILL.md](../../workspace/skills/ingest/SKILL.md) line 27）。外部统计脚本读 wiki 落盘 md 时无法可靠区分这 7 类来源——页面名、frontmatter、章节结构都跟来源 skill 不强绑定（同一论文页可能由 `ingest` PDF 分支建，也可能由 `critic` md 分支追加；idea card 页与跨论文比较页都是 wiki page，外部看不出来源）。

设计约束：tag 必须在 markdown 内合法；`ingest` 经 `wiki ingest` → `wiki compile` 落盘后保留；视觉上像副标题但不是真 `##` heading（不抢现有 frontmatter / section 层级）；便于外部正则一抓。

## Decision

给三个"思考型" predicate (`ideate` / `critic` / `design`) 的 md 产出添加 `` `category: <value>` `` inline code tag，紧贴 `# Title` 下空一行。值与 skill 名 1:1（`idea` / `critic` / `design`），冗余型——给外部脚本一个不依赖 skill 重命名的稳定 key。

其他 4 个会经 `ingest` md 写入分支的 predicate（`extract` / `spec` / `audit` / `curate`）**不加 tag**，构成**非对称契约**：外部脚本拿到的 md 可能带或不带 tag，需 fallback 处理 "missing category"。

契约执行点：

- **仅文档化**（M2 决策）：在三个 SKILL.md 的"输出结构"段落加 tag 模板说明 + "完成门禁"段落加硬约束。
- **不**改 `ingest` SKILL.md 加 tag 校验（不强制代码约束）。
- **不**改 ClawProBench `custom_check` 加 tag 验证。
- **不**跑实际 wiki_lint 验证（inline code 在 `# Title` 下空一行的 lint 行为未实测）。

## Consequences

- **非对称契约**：后端 / 统计脚本需 fallback 处理 4 类没 tag 的 md。可接受：4 类是"事实型 / 元型 / 工程型"，与 3 类"思考型"在统计场景下语义不同，缺 tag 即按"非思考型"归类。
- **冗余型耦合**：tag 值 = skill 名，skill 重命名必须同步改 tag 值 + 外部脚本。代价低：tag 只 3 个值，重命名需走 ADR。
- **契约仅文档化**：不强制 ingest 校验，违规 md 仍可入 wiki；外部脚本可能拿到缺 tag 的"思考型" md 漏归类。可接受：违规被"完成门禁"挡住。
- **wiki_lint 未验证风险**：inline code 在 `# Title` 下空一行的位置是 markdown 通用元素，不撞 frontmatter 命名空间，理论不应拦截，但未实测。lint 失败时再回头处理。
- **作用域冻结**：未来新增会产 md 的 predicate，默认**不加** tag。要加需新 ADR 显式批准，避免隐性扩张。

## Considered Options

- **(a) HTML comment** `<!-- category: idea -->`: 后端正则最简；但视觉完全隐藏，不符合"副标题"视觉约束——否决。
- **(b) YAML frontmatter** `category: idea` 加进已有 frontmatter: 跟 `paper.*` / `classification.*` 命名空间潜在冲突，且 `wiki_lint` 对 frontmatter 行为未实测——否决。
- **(c) inline bold KV** `**Category**: idea`: 视觉最像"metadata header"；但后端需正则 `\*\*(\w+)\*\*:\s*(\S+)` 锁结构，复杂度高——否决。
- **(d) inline code KV** `` `category: idea` ``: 视觉像 tag/badge；后端正则 `` `category:\s*(\S+)` `` 一抓；不撞 frontmatter；选中。
- **值域维度**：冗余型（值 = skill 名，1:1）vs 子类型型（值 = skill 内子分类）。选冗余型——统计场景不需要子类型粒度，避免引入未列清的子类型清单。
- **作用范围**：A 只 3 个 skill / B 全 7 个 / C 先 3 个后扩。选 A——原话明确，且 B 会让"思考型 vs 非思考型"区分消失，统计场景下失去信号。
- **持久化**：M1 最小（只改 SKILL.md）/ M2 文档+ADR / M3 完整（+ ingest 校验 + 验证）。选 M2——决策持久化但零代码风险。