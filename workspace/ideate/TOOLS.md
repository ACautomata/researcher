# TOOLS.md

## Wiki Tools (read+write)

- `wiki_status` — confirm vault is reachable before anchored idea generation
- `wiki_search` — find related papers, prior ideas, open questions for anchoring and deduplication
- `wiki_get` — read a specific wiki page for concrete evidence grounding
- `wiki_lint` — optional pre-flight check for contradictions or unresolved questions on anchor pages; run after `wiki_apply` writes to verify quality
- `wiki_apply` — write back idea cards and cross-paper insights to wiki after generation

> **Write-Back 原则**：读取 wiki 后产生的产出必须 write back，建立与读取内容的联系。

## File Operations

- Read and write within own workspace directory for internal state only (`memory/`, script intermediates)
- Primary delivery: return complete idea cards inline in reply text
- Do NOT use `idea-runs/` as a delivery interface for other agents to discover by path
- Read paper files when provided

## Not Available

- `sessions_spawn` — this agent does NOT spawn sub-agents
