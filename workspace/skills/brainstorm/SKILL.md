---
name: brainstorm
description: Generate evidence-grounded research ideas (curate → ideate). Triggers: brainstorm ideas, research ideas, generate ideas, research directions, find research gaps, 科研 idea, 研究思路, 头脑风暴.
---

# brainstorm — 研究 idea 生成

基于 wiki 证据生成研究 idea；每个 idea 锚定到命名痛点，非空想。

## 编排

1. **`curate`** — 跨论文比较 + lint，为 idea 生成准备精选上下文（每个 claim 引用 `page_id`）。
2. **`ideate`** — 基于上下文生成 idea card（5-10 张，每张锚定论文集群 + 命名痛点；含最小验证实验、预期指标、风险）。

### Pre-flight

用 `wiki_get` 读 wiki 索引和相关领域页面。不足时 browser 搜 arXiv/Scholar。收集 page ID、摘要、缺口组成上下文包。

### 完成后

1. 呈现 idea 摘要表 + 详细 card。
2. 如有 wiki 回写候选，运行 `curate` 更新 wiki。
3. 建议下一步（跑实验、深挖、入库更多论文）。

## 输入

| Field | Required | Description |
|-------|----------|-------------|
| Domain / topic | 否 | idea 生成范围，缺省全部 wiki 论文 |
| Paper list | 否 | 指定论文（标题、wiki 路径、URL） |
| Constraints | 否 | 方法、数据集、问题、时间范围 |

最少需要 domain/topic 或至少一个论文引用。都没有则询问用户。
