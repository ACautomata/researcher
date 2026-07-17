# Research-Agent（OpenClaw 配置）上下文

用 OpenClaw 网关跑的单 agent 自动化科研系统。本 CONTEXT 只记这个 **agent 系统的领域语言**--尤其 2026-07「子 agent 收缩」决策引入的两层 skill 架构。研究域术语（论文、实验、证据等级）散见各 predicate skill，待其模糊时再补录于此。

## Language

### Agent 架构

**Main agent**:
绑定消息渠道、与用户对话的唯一 agent；所有领域工作由它自己用 skill 完成，不再 spawn 生产者。
_Avoid_: coordinator、dispatcher、orchestrator（那是 skill 的角色，不是 agent 的）。

**Judge**:
唯一保留的 spawn 子 agent；独立质量门 + benchmark 评分。因 benchmark CI 强制要求、且「自己给自己打分」不独立而保留。
_Avoid_: reviewer（历史名，已被 judge 取代）。

**Spawn**:
经 `sessions_spawn` 启动独立子 agent 会话。两种合法用法：(1) **cross-agent spawn**：仅 judge，用于独立质量门；(2) **spawn self**：main 启动自己的 isolated 子 session，用于批量 / 并行 / context 隔离场景（如 paper-batch-ingest 每篇论文一个 session）。spawn self 仍由 main 的 predicate skill 完成领域工作，不是恢复 producer agent。
_Avoid_: delegate、dispatch（那是 main 在单 context 内走 skill，不是 spawn）。

### Skill 分层

**Predicate skill（谓词 skill）**:
一个原子、可复用的领域能力，只做一个动词的研究动作。当前 8 个：ingest / curate / extract / critic / design / spec / audit / ideate。其中 **critic 独立存在、不被任何 orchestrator 引用**（用户或 main 直接调用）；design + spec 被 paper-validate 引用。
_Avoid_: subagent、worker、module。

**Orchestrator skill（编排 skill）**:
把若干 predicate skill 组合成一个面向用户场景的 skill，通过 reference 编排它们。当前 8 个：paper-ingest（ingest->curate）/ paper-read（ingest->extract）/ paper-validate（design->spec，前置需 critic 产出在 wiki）/ paper-audit（audit）/ literature-query（curate）/ brainstorm（curate->ideate）/ benchmark（cross-agent spawn judge）/ paper-batch-ingest（每篇 spawn self->ingest）。**paper-pipeline 已退役**--"完整分析" 由 main 直接串 read->critic->validate->audit。
_Avoid_: coordination skill、pipeline skill。

**Reference（引用）**:
orchestrator skill 在文本里点名某个 predicate skill，让 main 加载并执行它。是**文本约定，不是代码 import**--grill-with-docs（"Run /grilling, using /domain-modeling"）即此模式的工作实证。
_Avoid_: import、depends_on、调用（skill 之间无函数调用，是 main 依文加载）。

### Benchmark harness (ClawProBench fork)

**ClawProBench**:
本仓库 CI 用的确定性 benchmark harness（产品名；仓库名 `ClawResearchBench`）。fork 自 upstream，改造为门控指定 agent 而非按 model 新建临时 agent。代码 fork 在 `ClawResearchBench` 的 `fork/target-main` 分支，CI 经 `git clone` 钉定 commit，不进本仓库 git 树。

**scenario**:
ClawProBench 的评测单元（YAML），含 `prompt`/`tools`/`custom_check`/`workspace_seed_dir`/`timeout_seconds`/`pass_threshold`。研究场景 `signal_source=workspace_live`（从 agent workspace 产物取分）、`benchmark_status=incubating`、`benchmark_core=false`，不在任何 active profile，须 `--benchmark-status all` 才入选。

**custom_check**:
确定性评分脚本（`custom_checks/*.py`），从 agent workspace 产物取分，**不依赖 judge agent**。这是 fork 取代旧 `benchmarks/_common/judge.py`（spawn judge 评分）的根据。

**profile**:
命名场景切片--`core`/`intelligence`/`coverage`/`native`/`full`。本仓库 CI 跑 research 精选子集（`--benchmark-status all`），非泛化 model ranking。

**target agent**:
fork 后 CI 门控的指定 agent（默认 `main`），复用其 workspace；区别于原样 ClawProBench 按 `--model` 新建的 `ocb6-<model>-<uuid>` 临时 agent。`--agent` 指定，`--model` 改 optional 并从 `openclaw.json` 自动读 main 的 model，result slug 用 `main`。

**FinalScore / pass@3 / pass^3**:
ClawProBench 评分指标。`pass@3` = trials=3 中至少 1 次通过；`pass^3` = 3 次全过；`FinalScore` 综合分（汇总 trials 与场景得分，见 `harness/scoring.py`）。需 trials≥3 才有语义。

**isolated state**:
ClawProBench 的 state 隔离机制（`_uses_isolated_state()`：target state ≠ 默认 `~/.openclaw` 时启用，触发 config/auth seed）。fork 在容器内跑 main agent 真实 state（`/home/node/.openclaw`），隔离关闭，三个 seed 函数全 no-op，零污染--但 `_create_agent` 仍须无条件跳过（其首步 `agents delete --force` 会删 target agent）。

_Avoid_: judge（benchmark 评分改由 custom_check 确定性完成，judge spawn 的唯一理由消失）、临时 agent（fork 不再新建）。
