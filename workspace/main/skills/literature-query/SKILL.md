## literature-query

### 概述 / Overview

Literature query and cross-paper comparison skill. Main agent delegates to **curate** to search, synthesize, and compare insights across papers in the wiki.

**Trigger words**: 文献查询, 对比论文, 跨论文比较, wiki里有没有, 查一下某篇论文, literature query, compare papers, cross-paper.

### 应用场景 / Scenario

User wants to query, compare, or synthesize information across papers already in the wiki.

- "对比这几篇论文的方法差异"
- "Wiki 里有没有关于 XX 的内容"
- "这几篇论文在 YY 数据集上表现如何"

### Subagent 调用链 / Agent Chain

1. **curate** — Wiki curation, quality linting, cross-paper comparison, literature queries

### 编排步骤 / Orchestration Steps

#### Step 1: 知识检索 (main agent)

1. Read `/workspace/shared/memory-wiki/index.md`, locate relevant pages.
2. Extract key facts related to the user query.
3. If wiki insufficient, use browser to supplement (arXiv, Google Scholar).

#### Step 2: 派发 curate

```
sessions_spawn(
  agentId: "curate",
  task: """{query_type: "lint" | "compare" | "query"} on the following scope.

## 查询范围
- 目标论文/关键词: {paper titles, keywords, or domain}
- Wiki 路径: {relevant wiki page paths; "未找到" if none}
- 对比维度: {methods / datasets / metrics / all; for compare mode}

## 用户问题
{user's original question, verbatim}

## 上下文
- 已读取的 Wiki 页面: {path list; none if absent}
- Wiki 关键事实摘要: {claims, experiments, results}
- 网络补充来源: {URLs; none if absent}

## 输出要求
- 引用 page_id 或路径, 标注 evidence_level
- 矛盾点明确标出, 数量化优于定性""",
  mode: "run",
  runTimeoutSeconds: 600
)
```

**Timeout**: 600s. Wiki read-only operations are fast.

#### Step 3: Reviewer 质量门

Route curate output through reviewer (runTimeoutSeconds: 300, context: "isolated").
If FAIL, send fix prompt back to curate's original session via `sessions_send`. Re-review after fix.

#### Step 4: 结果汇报

Present reviewer-passed results with page paths and evidence_level labels.

#### Error Handling

- **curate timeout**: Retry once with narrower scope; fallback to direct wiki answer with caveat.
- **Wiki empty**: Inform user, suggest ingesting papers first (autoresearch).
- **reviewer FAIL**: Loop back to curate (max 2 rounds); escalate to user.

### 输入规范 / Input Specification

| Field | Required | Description |
|-------|----------|-------------|
| query | Yes | Natural language question or comparison request |
| papers | No | Paper titles, wiki paths, or keywords to scope |
| dimensions | No | Comparison axes: methods, datasets, metrics, results |

### 输出规范 / Output Specification

- **Query mode**: Structured answer with citations, evidence levels, identified gaps.
- **Compare mode**: Aligned table with evidence_level per row, contradictions flagged.
- **Lint mode**: Dashboard of wiki quality issues by type, with fix suggestions.

### 示例 / Examples

**Example 1: Cross-paper comparison**

User: "对比 MHKC 和 FedProx 在非 IID 场景下的收敛性"

1. Main agent finds MHKC and FedProx pages in wiki.
2. Spawns curate with `query_type: "compare"`, dimensions: methods + convergence.
3. Reviewer verifies output references real pages and numbers match.
4. User receives comparison table with evidence levels.

**Example 2: Literature query**

User: "Wiki 里有没有关于差分隐私在联邦学习中应用的内容"

1. Main agent searches wiki for "差分隐私" + "联邦学习".
2. Found → spawns curate with `query_type: "query"`.
3. Not found → suggests ingesting papers first via autoresearch.
4. Reviewer validates citations and evidence levels.
5. User receives structured summary with page references.
