# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is the `~/.openclaw` configuration directory for an OpenClaw AI agent gateway. It tracks non-sensitive configuration files in git, synced to `git@github.com:ACautomata/research-agent.git`.

All changes are made via SSH to the remote server. Local clone is at `/Users/junran/Documents/research-agent/`.

## Architecture

This repo follows OpenClaw's hub-and-spoke multi-agent pattern. The main agent (颖姗) is bound to messaging channels and delegates specialized tasks to sub-agents via `sessions_spawn`.

- **openclaw.json** — Main gateway configuration. All secrets use `${ENV_VAR}` references resolved from `.env` (which is gitignored).
- **agents/main/agent/models.json** — Custom model provider definitions (currently MiniMax Anthropic-compatible endpoints).
- **canvas/index.html** — OpenClaw Canvas web UI.
- **workspace/** — Main agent (颖姗) working directory. Contains SOUL.md, AGENTS.md, IDENTITY.md, USER.md, TOOLS.md, MEMORY.md, HEARTBEAT.md, DREAMS.md. See [docs](https://docs.openclaw.ai/concepts/agent-workspace).
- **workspace-autoresearch/** — Sub-agent workspace for the Autoresearch agent. Mirrors the main workspace structure with SOUL.md, AGENTS.md, IDENTITY.md, USER.md, TOOLS.md, MEMORY.md, HEARTBEAT.md, DREAMS.md. This agent is spawned by 颖姗 for paper ingest, literature queries, cross-paper comparison, and wiki quality auditing.
- **workspace-paper-review/** — Agent workspace for paper review and validation experiment design. Contains SOUL.md, AGENTS.md, USER.md, memory/, and skills/ for the 5-stage paper analysis pipeline.
- **workspace-idea-generate/** — Sub-agent workspace for the Idea Generate agent. Contains the `idea-generate` skill for paper-grounded research idea cards, opportunity synthesis, deduplication, validation, and Markdown export.
- **workspace-reviewer/** — Sub-agent workspace for the Reviewer agent. Reviews sub-agent outputs and benchmark candidate answers with a strict pass/fail quality gate.
- **benchmarks/** — Developer benchmarks and evaluation datasets for testing agent capabilities.

## Key Configuration Details

- **Gateway**: loopback-bound on port 18789, token auth via `${GATEWAY_TOKEN}`.
- **Model**: Primary `minimax/MiniMax-M2.7`, fallback `minimax/MiniMax-M2.7-highspeed`. Provider auth uses `minimax-oauth` (handled by the minimax plugin).
- **Channels**: Feishu configured with WebSocket mode, pairing DM policy, allowlist group policy. Requires `${FEISHU_APP_ID}` and `${FEISHU_APP_SECRET}` in `.env`.
- **Memory**: QMD backend indexing `**/*.md` in workspace.
- **TTS**: Edge TTS with `zh-CN-XiaoxiaoNeural`.
- **Browser**: Headless Chromium at `/usr/bin/chromium`, no sandbox.
- **Session**: `dmScope: "per-peer"` — each user gets an independent DM session context.

### Gotchas

- Feishu channel: `streaming` must be boolean, not string. No `tools` property at channel level.
- Config validation errors appear in gateway logs on startup.
- `plugins.installs.*.installPath` is the resolved install directory; keep managed installs as absolute paths.
- QMD `paths[].path` entries resolve relative to the agent workspace directory; use `.` for the workspace root.
- External tools (Context7, WebReader) have weekly rate limits — use Playwright to read docs.openclaw.ai as fallback.
- `.env` uses `export VAR="value"` format (shell export syntax).

## Operations

```bash
# Restart gateway after config changes
openclaw gateway restart

# Verify config after restart
openclaw logs --tail 15

# View live logs
openclaw logs --follow

# Check version
openclaw --version

# Feishu pairing management
openclaw pairing list feishu
openclaw pairing approve feishu <CODE>
```

## Architectural Rules

### Workspace Naming

Workspace directories follow the OpenClaw convention `workspace-<agentId>`:

- **Main agent**: `workspace/` (no suffix — the default agent)
- **Sub-agents**: `workspace-<agentId>/` where `<agentId>` matches the `id` field in `openclaw.json` → `agents.list[]`

Examples: `workspace-autoresearch/`, `workspace-paper-review/`.

When adding a new agent, create the workspace directory, register it in `openclaw.json` under `agents.list` with a matching `workspace` path, and add the workspace to `.gitignore`'s runtime-state exceptions.

### Agent Design Pattern

The system uses a **main agent → main agent skills → subagent → subagent skills** delegation chain:

1. **Main agent (颖姗)** — bound to messaging channels, handles user-facing conversation, routing, and orchestration.
2. **Main agent skills** — live at `skills/<skill-name>/` (project root). These compose subagent capabilities into user-facing workflows (e.g. `idea-generate` orchestrates paper context extraction, idea scoring, and output formatting).
3. **Subagents** — each registered in `openclaw.json` under `agents.list`, spawned by the main agent via `sessions_spawn`. Each subagent owns a **single domain of responsibility**:
   - `autoresearch` — paper ingest, wiki maintenance, literature queries, cross-paper comparison.
   - `paper-review` — paper analysis pipeline (wiki entry → experiment extraction → review → validation design → codex prompt).
   - `idea-generate` — paper-grounded research idea generation, opportunity synthesis, deduplication, validation, and export.
   - `reviewer` — strict quality review of sub-agent outputs and benchmark agent-judge scoring.
4. **Subagent skills** — live at `workspace-<agentId>/skills/<skill-name>/`. These handle domain-specific subtasks within the subagent's responsibility scope.

**Constraints:**

- **Single minimal function per subagent.** Each subagent implements exactly one atomic capability. If a subagent grows to handle multiple distinct functions, split it. The litmus test: can you describe what the subagent does in a single verb phrase? If not, it's too broad.
- Main agent skills orchestrate subagents. They should not reimplement logic that belongs in a subagent skill.
- Subagent skills should be self-contained and produce outputs that downstream stages or other agents can consume.
- The `agents.defaults.subagents.allowAgents` list in `openclaw.json` controls which subagents the main agent may spawn. Update it when adding new subagents.
- Main agent's AGENTS.md and TOOLS.md define how subagents are invoked. Keep orchestration logic in main agent skills (`skills/<skill-name>/`), not scattered across workspace files.

### Benchmark CI 流程

仓库 `benchmarks/` 下任何 benchmark **必须**遵守以下约束，缺一不可，PR 校验会失败：

1. **统一入口**：每个 benchmark 目录必须有 `env.sh` 和 `metrics.py` 两个入口，CI 流程按统一方式调用。CI 调度脚本在 `benchmarks/_common/run_bench.py`，自定义 metrics.py 必须通过它路由。
2. **QA schema**：benchmark 题目必须符合 `benchmarks/_common/qa_schema.json`；每条 QA 一行 JSON，存在 `benchmarks/<name>/qa.jsonl`。schema 接受额外字段（`additionalProperties: true`），但禁止删掉必填字段。
3. **强制 main agent 路由**：CI 流程的 benchmark 任务**只**调用 `openclaw agent --agent main ...`，不允许在 `metrics.py`、qa.jsonl 或 prompt 里直接指定其他任务 agent id。如果某条 QA 需要让特定子 agent 干活，必须在 QA 里加 `target_agent: "<subagent-id>"` 字段；`run_bench.py` 会自动在 prompt 前加一段 `[BENCHMARK DIRECTIVE]`，要求 main 用 `sessions_spawn` 委派给 `target_agent`，并把子 agent 的回复原文返回。`run_bench.py` 对非 main 任务调用做了 hard assert 保护；但 `judge: "agent"` 的 LLM 评分必须使用专门的 `reviewer` agent。
4. **统一 env 前置**：在跑任何 benchmark 自己的 `env.sh` 之前，CI 必先跑 `benchmarks/_common/env_setup.sh`，用 `docker compose -f docker/docker-compose.bench.yml up -d` 启动 `justlikemaki/openclaw-docker-cn-im` 镜像，把当前仓库 rsync 进容器内 `/home/node/.openclaw`，等 `openclaw health` 就绪，再跑一次 `--agent main --message "ping" --local` 冒烟。benchmark 的 `env.sh` 只能在此基础上做 fixture 写入，**禁止**重启容器、改镜像、或重写统一 env。
5. **Metrics 可复用**：`metrics.py` 必须直接调用 `benchmarks/_common/run_bench.py`（即 6 行 shim），不要自己写 `docker exec openclaw agent`。判分优先用 `benchmarks/_common/judge.py` 提供的 `judge_with_rules` / `judge_with_agent`；自己写 judge 时必须基于 QA 的 `gold_answer.must_contain` 或 `rubric`，禁止用硬编码字符串比对。
6. **PR 评论字段**：CI 会在 PR 评论里汇总每个 benchmark 的 `pass_rate` 和 `avg_score`；新增 benchmark 必须能输出这两个汇总字段（在 `bench-report.json` 顶层），否则不会出现在 PR 评论里。
7. **本地可复现**：`bash benchmarks/_common/env_setup.sh && bash benchmarks/<name>/env.sh && python3 benchmarks/<name>/metrics.py` 应当能跑通；CI 与本地行为一致。
8. **不要把 secrets 写进仓库**：`MINIMAX_API_KEY` 走 GitHub Actions secret；本地开发用 `docker/.env.bench`（已 gitignore 候选）。`docker/.env.bench.example` 是只读模板。

GitHub 仓库必须配置以下 secret（你最后手动加）：

| Secret | 必填 | 用途 |
| --- | --- | --- |
| `MINIMAX_API_KEY` | 是 | LLM provider key，给 main agent 和 LLM judge 用。未配置时 workflow fail-fast。 |
| `MINIMAX_BASE_URL` | 否 | 默认 `https://api.minimaxi.com` |
| `BENCH_BASE_RESULTS_JSON` | 否 | 上次 main 跑出的 summary（base64 字符串），用于 PR 评论做 delta 对比 |

### Adding New Agents

When creating a new subagent:

1. Add an entry to `agents.list` in `openclaw.json` with `id`, `name`, and `workspace` path.
2. Create `workspace-<agentId>/` with standard workspace files (SOUL.md, AGENTS.md, USER.md, TOOLS.md, MEMORY.md, HEARTBEAT.md, DREAMS.md).
3. Add the agent ID to `agents.defaults.subagents.allowAgents`.
4. Write skills under `workspace-<agentId>/skills/` following the single-responsibility principle.
5. If the main agent needs to orchestrate this subagent, create or update a main agent skill under `skills/`.

## PR Rules

- **Benchmark results required.** When a PR touches `benchmarks/` or any skill/agent that has benchmark coverage, the benchmark test results must be pasted into the PR description or a PR comment. Do not open a PR without them.
- **Test new features before PR.** Every new feature (skill, agent, workflow, config change) must be tested via OpenClaw — actually trigger the agent in conversation and verify it works end-to-end. Do not open the PR without doing this.

## Gitignore Strategy

`.env` and `auth-profiles.json` contain secrets — never track them. Runtime data (`logs/`, `tasks/`, `*.sqlite`), QMD caches (`qmd/`, `agents/*/qmd/`), CLI-managed dirs (`extensions/`), and channel data (`qqbot/`) are excluded. Agent workspaces and their checked-in skills are tracked, while runtime state inside those workspaces is ignored. `openclaw.json` is tracked because all tokens are env var references.
