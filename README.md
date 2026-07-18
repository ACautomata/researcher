# research-agent

> 跑在 OpenClaw 上的自动化科研 agent（单 main + judge，覆盖论文 ingest / extract / critic / validate / audit）。本仓库是它的 `~/.openclaw` 配置目录，[OpenClaw 本体需单独安装](https://docs.openclaw.ai/install)。

## 快速上手

本仓库是**配置目录**，不是 OpenClaw 运行时本体。装好 OpenClaw、用本仓库的 `openclaw.json` 启动它，最后在浏览器打开 Dashboard 看它工作。

**前置条件**：Node 22.22.3+ / 24.15+ / 25.9+（推荐 Node 24，installer 会自动装）。只想试用 agent **不需要** Docker；跑 benchmark 才需要容器运行时 + Python 3.11+（见[进阶章节](#进阶benchmark-与-ci)）。

> 以下命令为 mac/Linux/WSL2 语义。Windows 原生 PowerShell 需把 `~` 换成 `$HOME`、用编辑器写 `.env`（不要用 `echo '...' >>`），或直接用 WSL2。

```bash
# 1. 安装 OpenClaw 本体（mac/Linux/WSL2；Windows PowerShell: iwr -useb https://openclaw.ai/install.ps1 | iex）
curl -fsSL https://openclaw.ai/install.sh | bash

# 2. 把本仓库作为 ~/.openclaw（HTTPS；若该目录已存在，先 rm -rf 或备份）
git clone https://github.com/ACautomata/research-agent.git ~/.openclaw
cd ~/.openclaw
#   SSH 备选：git clone git@github.com:ACautomata/research-agent.git ~/.openclaw（需先把公钥加到 GitHub，报 Permission denied 就改用 HTTPS）

# 3. 生成 Dashboard 登录 token（强随机，mac/Linux），记下输出
openssl rand -hex 32

# 4. 在 ~/.openclaw/.env 写入（shell export 语法；把上一步输出和你的 minimax key 填进去）
#    export GATEWAY_TOKEN="<上一步的随机串>"
#    export LLM_API_KEY="<你的 minimax API key>"

# 5. 跑 onboarding：探测模型、装开机自启 daemon（会复用本仓库已有的 openclaw.json + workspace）
openclaw onboard --install-daemon
#   中文向导（产品名/命令/key 仍为英文）：OPENCLAW_LOCALE=zh-CN openclaw onboard --install-daemon

# 6. 重启 Gateway 并确认 18789 在监听（若提示未在运行，改用 openclaw gateway start）
openclaw gateway restart
openclaw gateway status

# 7. 打开 Dashboard（自动开浏览器并带 auth）
openclaw dashboard
```

打开后，在 Dashboard 聊天框发一条「ping」，收到 AI 回复即代表整套 agent 跑通。Dashboard 入口是 `http://localhost:18789/`。**若 ping 无回复**：多半是模型鉴权没配好——`openclaw doctor` 看模型是否 OK，并确认 `.env` 里的 `LLM_API_KEY` 已填、`openclaw logs --tail 30` 无 401。

> **`openclaw not found`？** 多为 PATH 问题：`node -v` / `npm prefix -g` / `echo $PATH`，把 npm 全局 bin 加入 PATH。备选 npm 安装：`npm install -g openclaw@latest`（pnpm 须 `pnpm approve-builds -g`；Bun 不能当唯一运行时，仍需 Node 的 `node:sqlite`）。详见[安装指南](https://docs.openclaw.ai/install)与[Onboarding 向导](https://docs.openclaw.ai/start/wizard)。

**关键官方文档**：[安装指南](https://docs.openclaw.ai/install) · [Getting Started 最短路径](https://docs.openclaw.ai/start/getting-started) · [Dashboard 访问与认证](https://docs.openclaw.ai/web/dashboard) · [文档总入口](https://docs.openclaw.ai/)

---

> **读者分流**：只想试用 agent -> 跟着上面「快速上手」走到[进入 Dashboard](#进入-dashboardcontrol-ui) 即可，无需 Docker。想跑 / 改 benchmark -> 直跳[进阶：Benchmark 与 CI](#进阶benchmark-与-ci)。

## 这是什么

本仓库是 `~/.openclaw` 配置目录的 git 化版本（同步到 `ACautomata/research-agent`），**不是** OpenClaw 运行时本体——最大的误解就是「clone 本仓库 = 装好 OpenClaw」。

它跑一个**单 main agent + judge** 的自动化科研 agent：

- **main agent** 做所有领域工作，覆盖 ingest / curate / extract / critic / design / spec / audit / ideate 等研究动词，直接在 Dashboard 聊天里接收自然语言指令，自行决定是否 spawn judge 或自己的隔离子会话（[Agent Workspace 概念](https://docs.openclaw.ai/concepts/agent-workspace)）。
- **judge** 只做质量门与 benchmark 评分，不做面向用户的对话。

skill 分两层：**predicate**（原子研究动词）+ **orchestrator**（按场景用文本引用编排 predicate）。系统只有 main 和 judge 这两个 agent；架构细节见仓库内 `CONTEXT.md` 与 `docs/adr/0001-single-main-agent-two-layer-skills.md`，更多概念见[OpenClaw 文档总入口](https://docs.openclaw.ai/)。

## 进入 Dashboard（Control UI）

[Dashboard](https://docs.openclaw.ai/web/control-ui) 本质是 Gateway 自带的浏览器 Control UI（Vite + Lit SPA），与 Gateway WebSocket 同端口，**不是**独立服务、不用另装 / 另起。本仓库入口就是 `http://localhost:18789/`。

### 最简打开

```bash
# 自动开浏览器并带 auth（推荐）
openclaw dashboard

# headless / SSH：只打印 URL
openclaw dashboard --no-open

# 脚本集成：输出 JSON
openclaw dashboard --json
```

CLI 参数细节见 [`openclaw dashboard` CLI](https://docs.openclaw.ai/cli/dashboard)。

### 手动入口

浏览器打开 `http://localhost:18789/`（注意是 `http` 不是 `https`，本仓库未启 TLS，详见 [Web（http/https 与 TLS）](https://docs.openclaw.ai/web)），在 Control UI settings 里粘贴 `.env` 中的 `GATEWAY_TOKEN`（对应 `openclaw.json` 的 `gateway.auth.token`）。

### 打不开排错清单

1. Gateway 是否在跑：`openclaw gateway status`
2. 端口是否 18789
3. `unauthorized` / `1008` 多半是 token 与 `.env` 不一致（token 漂移）-> 去 `.env` 重新取，**别改 `openclaw.json`**。

首次用新浏览器可能提示 `disconnected (1008): pairing required`：

```bash
openclaw devices list        # 查看待审浏览器/设备
openclaw devices approve <id>  # 批准
```

（飞书 DM 配对是另一套：`openclaw pairing list feishu` / `openclaw pairing approve feishu <CODE>`，见 [Feishu 配对管理](https://docs.openclaw.ai/)。）本机 loopback 访问一般自动放行，详见 [Control UI](https://docs.openclaw.ai/web/control-ui) 与 [Dashboard 访问与认证](https://docs.openclaw.ai/web/dashboard)。

### 远程服务器访问

因 `bind=loopback`，远程服务器必须走 SSH 隧道：

```bash
ssh -N -L 18789:127.0.0.1:18789 user@gateway-host
```

再在本地打开 `http://127.0.0.1:18789/`；可选 Tailscale Serve。

> **安全提示**：Control UI 是 admin 面（聊天 / 配置 / 执行审批），`controlUi.allowInsecureAuth=true` 仅本地便利，勿把端口暴露公网。

## 试用：在 Dashboard 里做什么

可立刻尝试的研究动词（每个一句话示例）：

| 想做的事 | 在聊天里说 |
| --- | --- |
| 论文 PDF 入库 / 深读 | 「跑 ingest / paper-read：\<PDF 或 URL\>」 |
| Reviewer 视角分析 | 「用 critic 分析这篇论文的问题」 |
| 选题头脑风暴 | 「brainstorm 几个研究方向」 |
| 跨论文查询 | 「literature-query：比较这几篇的 X」 |

**完整分析链**：main 直接编排 `paper-read` -> `critic` -> `paper-validate` -> `paper-audit`，每步落盘到 wiki（无 router skill）。

改模型 / 认证重跑 `openclaw onboard`；改其他非推理配置用 `openclaw configure`（详见 [Onboarding 向导](https://docs.openclaw.ai/start/wizard)）。

## 配置与 Secrets

### 两个 `.env` 不要混

| 文件 | 语法 | 用途 | 是否入库 |
| --- | --- | --- | --- |
| 根 `.env` | `export VAR="value"` | gateway / agent 运行时 | 否（gitignored） |
| `docker/.env.bench` | `KEY=value` | 仅 benchmark | 否（gitignored） |

### 根 `.env` 变量表

| 变量 | 必填 | 说明 |
| --- | --- | --- |
| `GATEWAY_TOKEN` | 是 | Dashboard 登录 token，对应 `openclaw.json` 的 `gateway.auth.token`。用 `openssl rand -hex 32` 生成强随机值。 |
| `LLM_API_KEY` | 是 | main agent 默认模型 `minimax/MiniMax-M3` 的 API key（`api_key` 鉴权，见 `openclaw.json` 的 `auth.profiles.minimax:cn`）。未设置时 agent 不会回复；onboarding 会引导配置，确认 `.env` 含此项。 |
| `FEISHU_APP_ID` / `FEISHU_APP_SECRET` | 启用 feishu 时 | 飞书应用凭证。 |
| `DISCORD_BOT_TOKEN` | 启用 discord 时 | Discord bot token。 |

所有 secret 一律走 `${ENV_VAR}` 引用，`openclaw.json` 里从不写明文 token / key。

**永不入库清单**（`.gitignore` 已排除）：`.env`、`secrets.json`、`agents/*/agent/auth-profiles.json`、`agents/*/agent/models.json`、`agents/*/agent/auth-state.json`、`*.key`、`*.pem`、`secrets*`。新 clone 的机器因上述文件不入库，必须自己创建 `.env`，否则没有 token、Dashboard 进不去。

### 通道配置 gotcha

feishu 用 WebSocket 模式：`streaming` 必须是 boolean（不是字符串）、channel 级不能有 `tools` 属性。改配置后 `openclaw gateway restart`。

> **高级路径**：`OPENCLAW_HOME` / `OPENCLAW_STATE_DIR` / `OPENCLAW_CONFIG_PATH` 用于自定义路径或服务账号运行，见 [Getting Started](https://docs.openclaw.ai/start/getting-started)。

## 进阶：Benchmark 与 CI

### 前置（benchmark 专用，与试用 agent 不同）

- **容器运行时**：Docker Desktop（macOS 也可用 Apple `container` CLI；`run_local_benchmark.sh --runtime auto` 自动选择，默认优先 Docker）。
- **Python 3.11+**：`metrics.py` 会用到。
- **`LLM_API_KEY`**：本地和 CI benchmark 都需要。

### 本地 env

复制模板（KEY=value 语法，与根 `.env` 不同）：

```bash
cp docker/.env.bench.example docker/.env.bench
```

填入 `LLM_API_KEY`，其余按需。`docker/.env.bench.example` 是 benchmark LLM 配置的**单一真相源**，默认模型 `minimax/MiniMax-M2.7`（避免与 agent 运行时模型 `MiniMax-M3` 混用）。

| 变量 | 必填 | 说明 |
| --- | --- | --- |
| `LLM_API_KEY` | 是 | LLM provider 的 API Key，本地 benchmark 没有它会直接失败。 |
| `LLM_BASE_URL` | 否 | LLM provider 的 Anthropic-compatible 地址，默认 `https://api.minimaxi.com/anthropic`。 |
| `LLM_MODEL` | 否 | benchmark 使用的模型，默认见 `docker/.env.bench.example`。 |

### 一键跑

```bash
# idea-generate-1 是真实 benchmark 名；用 ls benchmarks/ 查看全部可用 benchmark
benchmarks/_common/run_local_benchmark.sh idea-generate-1
```

脚本自动完成：读 `docker/.env.bench` -> 选容器运行时 -> 起容器 -> 等就绪 -> 跑 `env.sh` 写 fixture -> 跑 `metrics.py` -> 输出 `bench-report.json` 路径。

常用 flag与 LLM 配置优先级：

```bash
benchmarks/_common/run_local_benchmark.sh --runtime docker idea-generate-1     # 强制 Docker
benchmarks/_common/run_local_benchmark.sh --keep-container idea-generate-1     # 保留容器排查
benchmarks/_common/run_local_benchmark.sh --debug idea-generate-1              # 开 debug artifact
# 命令行临时传 LLM 配置（优先级最高）
benchmarks/_common/run_local_benchmark.sh --api-key "你的_key" --base-url "https://api.minimaxi.com/anthropic" --model "minimax/MiniMax-M2.7" idea-generate-1
```

**LLM 配置优先级**：命令行 flag > `docker/.env.bench` > shell 环境变量。手动三步等价 CI（仅用于调试基建）：`bash benchmarks/_common/env_setup.sh && bash benchmarks/<name>/env.sh && python3 benchmarks/<name>/metrics.py`。

### 预烘焙 wiki fixture

benchmark 需要先把论文材料入库到 wiki 时，用统一工具把 `materials/` 预烘焙成 `wiki/main/` fixture，避免每次运行重复 ingest：

```bash
benchmarks/_common/bake_wiki.sh idea-generate-1  # 默认读 benchmarks/<name>/materials/（.md/.pdf/.txt），导出到 wiki/main/
```

flag（`--materials <dir>`、`--runtime docker --keep-container`、`--dry-run`、`--no-patch-envsh`）见 `bake_wiki.sh --help`；烘焙后建议提交 `materials/`、`wiki/main/`、`env.sh` 中的 staging block。

### fork CI secrets

在你 fork 的仓库里配置 GitHub Actions secrets：**Settings -> Secrets and variables -> Actions -> New repository secret**。

| Secret | 必填 | 示例 / 默认值 | 用途 |
| --- | --- | --- | --- |
| `LLM_API_KEY` | 是 | 你的 LLM API Key | main agent 和 LLM judge 都会用它，未配置时 workflow fail-fast。 |
| `LLM_BASE_URL` | 否 | `https://api.minimaxi.com/anthropic` | LLM provider API 地址，不填则用 CI 默认值。 |
| `LLM_MODEL` | 否 | 见 `docker/.env.bench.example` | benchmark 使用的模型，不填则用 CI 默认值。 |
| `BENCH_BASE_RESULTS_JSON` | 否 | 上次 main 跑出的 summary 的 base64 字符串 | 用于 PR 评论展示 delta，没有也能跑。 |

配置完成后：进入 fork 仓库的 **Actions** 页面确认 workflow 未被禁用 -> 从 fork 开 / 更新一个 PR -> 等 `Benchmark` workflow 跑完 -> 确认所有 benchmark job 通过 -> 再向上游开 PR。

### 强制规则与演进

- CI 只调 `openclaw agent --agent main`，不允许在 `metrics.py` / qa.jsonl / prompt 里直接指定其他任务 agent id。
- 新增 benchmark 必须能在 `bench-report.json` 顶层输出 `pass_rate` 与 `avg_score`，否则不会出现在 PR 评论里。
- 细节（`env.sh` / `metrics.py` 两入口、qa schema、judge 路由）见 `CLAUDE.md`「Benchmark CI 流程」与 `benchmarks/_common/`。

> **演进**：ADR-0002（status: accepted）计划用 ClawProBench fork + 确定性 `custom_check` 替换当前 `benchmarks/_common/` harness 并退役 `judge`（fork 跑通后删除 judge + 删旧 `_common/`）。当前仍以 `_common/` + judge 为准，详见 `docs/adr/0002-clawprobench-fork-target-main.md`。

## 贡献与 PR 规则

**开上游 PR 前必须完成**（缺一不可）：

1. 本地跑过相关 benchmark 且通过：`benchmarks/_common/run_local_benchmark.sh <name>`
2. forked repo 的 `Benchmark` GitHub Actions CI 通过
3. PR 描述 / 评论贴出**本地 + fork CI** 两份 benchmark 结果摘要
4. 改 skill / agent / workflow / 配置，必须实际触发 OpenClaw 端到端验证（在 Dashboard 或对话里跑通），不许只靠推理就开 PR

本地测试没跑，或 forked repo CI 没通过，**不要**向上游仓库开 PR。

**secrets 卫生**：永不把 API key 写进代码 / README / issue / PR 描述 / 日志，只放 `.env` / `docker/.env.bench`（本地 gitignored）或 GitHub Actions secrets。

**issue / triage 流程**见 `docs/agents/issue-tracker.md` 与 `docs/agents/triage-labels.md`；五个 triage 标签：`needs-triage` / `needs-info` / `ready-for-agent` / `ready-for-human` / `wontfix`。

