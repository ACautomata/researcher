# TOOLS.md

## Wiki Tools (read-only)

- `wiki_status` — confirm vault is reachable before anchored idea generation
- `wiki_search` — find related papers, prior ideas, open questions for anchoring and deduplication
- `wiki_get` — read a specific wiki page for concrete evidence grounding
- `wiki_lint` — optional pre-flight check for contradictions or unresolved questions on anchor pages

## File Operations

- Read and write within own workspace directory (`idea-runs/`, output files)
- Read paper files when provided

## Not Available

- `sessions_spawn` — this agent does NOT spawn sub-agents
- Wiki write tools — this agent has read-only wiki access
