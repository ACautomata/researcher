# Research-Agent（OpenClaw 配置）上下文

用 OpenClaw 网关跑的单 agent 自动化科研系统。本 CONTEXT 只记这个 **agent 系统的领域语言**——尤其 2026-07「子 agent 收缩」决策引入的两层 skill 架构。研究域术语（论文、实验、证据等级）散见各 predicate skill，待其模糊时再补录于此。

## Language

### Agent 架构

**Main agent (颖姗)**:
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
把若干 predicate skill 组合成一个面向用户场景的 skill，通过 reference 编排它们。当前 8 个：paper-ingest（ingest→curate）/ paper-read（ingest→extract）/ paper-validate（design→spec，前置需 critic 产出在 wiki）/ paper-audit（audit）/ literature-query（curate）/ brainstorm（curate→ideate）/ benchmark（cross-agent spawn judge）/ paper-batch-ingest（每篇 spawn self→ingest）。**paper-pipeline 已退役**——"完整分析" 由 main 直接串 read→critic→validate→audit。
_Avoid_: coordination skill、pipeline skill。

**Reference（引用）**:
orchestrator skill 在文本里点名某个 predicate skill，让 main 加载并执行它。是**文本约定，不是代码 import**——grill-with-docs（"Run /grilling, using /domain-modeling"）即此模式的工作实证。
_Avoid_: import、depends_on、调用（skill 之间无函数调用，是 main 依文加载）。
