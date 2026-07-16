---
status: accepted
---

# 收缩为单 main agent + 两层 predicate/orchestrator skill

## Context

网关原跑 9 个 spawn 子 agent（ingest/curate/extract/critic/design/spec/audit/ideate/judge）的 hub-and-spoke。每个子 agent 都是「一个 prompt + 一个 skill」，无独立 tools/model——spawn 的唯一价值是 context 隔离。但 `delegationMode: "prefer"` + main 的「你是 dispatcher，不是 analyst」指令**强制委派**，即便模型对单 agent skill 使用的可靠性更高；每次 spawn 还要重读 SOUL/USER/MEMORY、多一个 handoff 失败点。

## Decision

删 8 个生产者子 agent，每个折成一个 **predicate skill**（原子、可复用的领域能力），归单 main agent 所有。场景由 **orchestrator skill** 通过 reference（文本约定，`grill-with-docs` 即工作实证）编排 predicate。**仅保留 judge** 为 spawn 子 agent：benchmark CI 强制要求专门 judge agent（`run_bench.py` hard-assert + CLAUDE.md §bench 规则 3），且「自己给自己打分」不独立。

退役的 6 段 `paper-pipeline` 拆成内聚的 orchestrator——paper-read（ingest→extract）、paper-validate（design→spec）、paper-audit（audit）——加已有的 paper-ingest（ingest→curate）。`critic` 保持独立 predicate（无 orchestrator 包它）。「完整分析」由 main 直接串 read→critic→validate→audit，不再有 router。main workspace 扁平到 `~/.openclaw/workspace`（无 per-agent 子目录）；judge 在 `~/.openclaw/judge`。

## Why

让系统对齐模型的实际训练分布（单 agent skill 使用 ≫ 深度多 agent 编排），消除 handoff 失败和 per-spawn context 开销，得到扁平、可读的 workspace——同时保住唯一有硬外部依赖（judge/CI）和独立性要求（质量门）的那个 spawn。

## Consequences

- **失去** per-stage context 隔离和流水线并行。缓解：拆成短 orchestrator + 每个 predicate 把完整产出写进 wiki，context 有界且持久。
- 「reply 必须 inline 完整内容」规则（spawn 模型设计）收敛成 main 一条 standing order；单 orchestrator 内 full-inline 可接受，跨 orchestrator 靠 wiki。
- benchmark judging 不受影响（judge 保留）。

## Amendment: spawn self for batch isolation

批量 / 并行场景可用 `sessions_spawn` 启动 main 自己的 isolated 子 session。例如 `paper-batch-ingest` 对每篇论文 spawn 一个 self subagent，在各自 context 里运行 `ingest` predicate。

这不恢复 producer agent：子 session 仍是 main 身份、共享 main workspace 与 predicate skills；`agents.list` 仍只有 main + judge，cross-agent `allowAgents` 仍只有 judge。它只把 OpenClaw 的同 agent context 隔离能力用于天然可并行的批处理。
