#!/usr/bin/env bash
# benchmarks/_common/bake_wiki.sh
#
# Bake a benchmark's research wiki from raw materials.
#
# What this does (the four steps the goal describes):
#   1. Boot the same container CI uses (env_setup.sh: pulls image, runs compose /
#      Apple `container`, copies the repo into /home/node/.openclaw, waits healthy).
#   2. Stage the materials/ folder (or any folder) into the main agent's workspace
#      inside the container at /home/node/.openclaw/workspace/main/materials/.
#   3. Call `openclaw agent --agent main` and ask it to ingest every paper file in
#      that folder into the research wiki (paper-ingest: ingest -> curate).
#   4. Copy the resulting wiki/main vault out of the container into
#      benchmarks/<bench>/wiki/main/, then patch benchmarks/<bench>/env.sh so the
#      benchmark stages that baked vault via `docker cp` at run time.
#
# After baking, run the benchmark the usual way (run_local_benchmark.sh <bench> or
# CI) and the agent will find the pre-baked wiki pages instead of having to ingest
# raw materials at runtime.
#
# Usage:
#   benchmarks/_common/bake_wiki.sh <benchmark>
#   benchmarks/_common/bake_wiki.sh --materials path/to/papers idea-generate-1
#   benchmarks/_common/bake_wiki.sh --runtime container --keep-container idea-generate-1
#
# Credentials come from (priority order): --api-key/--base-url/--model CLI flags,
# then docker/.env.bench, then the LLM_* environment. Same precedence as
# run_local_benchmark.sh.
set -euo pipefail

# macOS tar emits `._*` (AppleDouble) metadata files that would otherwise be
# staged into the container and exported as junk. Disable that at the source.
export COPYFILE_DISABLE=1

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
RUNTIME="${BENCH_CONTAINER_RUNTIME:-auto}"
KEEP_CONTAINER="${BENCH_KEEP_CONTAINER:-}"
DRY_RUN=0
PATCH_ENV=1
MATERIALS=""
TIMEOUT="1800"
CLI_MODEL=""
CLI_BASE_URL=""
CLI_API_KEY=""
BENCH=""

usage() {
  cat <<'USAGE'
usage: benchmarks/_common/bake_wiki.sh [options] <benchmark>

Bake a benchmark wiki from raw materials in the CI bench container.

Options:
  --materials DIR       Materials source dir (default: benchmarks/<bench>/materials).
                        May contain .md / .pdf / .txt paper files; subdirs are walked.
  --runtime docker|container|auto
                        Container runtime (default: auto).
  --timeout SEC         Per-agent ingestion call timeout in seconds (default: 1800).
  --keep-container      Leave the bench container running after baking.
  --dry-run             Boot + stage materials, but do not call the agent or export.
  --no-patch-envsh      Do not patch benchmarks/<bench>/env.sh.
  --model MODEL         Override LLM model.
  --base-url URL        Override LLM provider base URL.
  --api-key KEY         Override LLM provider API key.
  -h, --help            Show this help.

Examples:
  benchmarks/_common/bake_wiki.sh idea-generate-1
  benchmarks/_common/bake_wiki.sh --materials ../some/papers idea-generate-1
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --materials) MATERIALS="${2:?--materials needs a value}"; shift 2 ;;
    --runtime) RUNTIME="${2:?--runtime needs a value}"; shift 2 ;;
    --timeout) TIMEOUT="${2:?--timeout needs a value}"; shift 2 ;;
    --keep-container) KEEP_CONTAINER=1; shift ;;
    --dry-run) DRY_RUN=1; shift ;;
    --no-patch-envsh) PATCH_ENV=0; shift ;;
    --model) CLI_MODEL="${2:?--model needs a value}"; shift 2 ;;
    --base-url) CLI_BASE_URL="${2:?--base-url needs a value}"; shift 2 ;;
    --api-key) CLI_API_KEY="${2:?--api-key needs a value}"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    --*) echo "unknown option: $1" >&2; usage >&2; exit 2 ;;
    *)
      [[ -n "${BENCH}" ]] && { echo "unexpected extra argument: $1" >&2; exit 2; }
      BENCH="$1"; shift ;;
  esac
done

[[ -n "${BENCH}" ]] || { usage >&2; exit 2; }
case "${RUNTIME}" in docker|container|auto) ;; *) echo "bad --runtime: ${RUNTIME}" >&2; exit 2 ;; esac

BENCH_DIR="${ROOT}/benchmarks/${BENCH}"
[[ -d "${BENCH_DIR}" ]] || { echo "benchmark not found: ${BENCH_DIR}" >&2; exit 2; }

# Default materials source: benchmarks/<bench>/materials.
MATERIALS_DIR="${MATERIALS:-${BENCH_DIR}/materials}"
[[ -d "${MATERIALS_DIR}" ]] || {
  echo "materials dir not found: ${MATERIALS_DIR}" >&2
  echo "create it (e.g. benchmarks/${BENCH}/materials/ with .md/.pdf/.txt papers) or pass --materials DIR" >&2
  exit 2
}

# --- Credentials (same precedence as run_local_benchmark.sh) ------------------
LOCAL_ENV_FILE="${BENCH_LOCAL_ENV_FILE:-${ROOT}/docker/.env.bench}"
if [[ -f "${LOCAL_ENV_FILE}" ]]; then
  set -a; # shellcheck disable=SC1090
  . "${LOCAL_ENV_FILE}"; set +a
fi
[[ -n "${CLI_API_KEY}" ]] && export LLM_API_KEY="${CLI_API_KEY}"
[[ -n "${CLI_BASE_URL}" ]] && export LLM_BASE_URL="${CLI_BASE_URL}"
[[ -n "${CLI_MODEL}" ]] && export LLM_MODEL="${CLI_MODEL}"
: "${LLM_BASE_URL:=https://api.minimaxi.com/anthropic}"
: "${LLM_MODEL:=minimax/MiniMax-M2.7}"
export LLM_API_KEY LLM_BASE_URL LLM_MODEL
[[ -n "${LLM_API_KEY:-}" ]] || {
  echo "LLM_API_KEY is not set. Use --api-key, export it, or set it in docker/.env.bench." >&2
  exit 64
}

# Tag this run distinctly from normal benchmark runs so its container name does
# not collide with a concurrent benchmark run.
safe_bench="$(printf '%s' "${BENCH}" | tr -c 'A-Za-z0-9_.-' '-')"
export BENCH_RUN_ID="${BENCH_RUN_ID:-bake-${safe_bench}-$$}"
export BENCH_CONTAINER_RUNTIME="${RUNTIME}"

BAKE_OUT="${BENCH_DIR}/wiki/main"
BAKE_DEBUG_DIR="${BENCH_DIR}/.bake-debug"
mkdir -p "${BAKE_DEBUG_DIR}"

CONTAINER_MATERIALS="/home/node/.openclaw/workspace/main/materials"
MOUNT="/home/node/.openclaw"
SESSION_KEY="agent:main:bake-${BENCH}-${$}"

log() { printf '\n[bake_wiki] %s\n' "$*"; }
die() { printf '\n[bake_wiki][FATAL] %s\n' "$*" >&2; exit 1; }

# Insert/replace a managed block in <bench>/env.sh that `docker cp`s the baked
# wiki/main into the container at benchmark time. Idempotent: the block is
# delimited by literal markers and replaced wholesale on every bake.
patch_envsh() {
  local envsh="$1"
  [[ -f "${envsh}" ]] || { echo "[bake_wiki] no env.sh at ${envsh}; skipping patch" >&2; return 0; }
  local tmp; tmp="$(mktemp)"
  # Drop any prior managed block (inclusive of the markers) using literal
  # substring matching so the markers need no regex escaping.
  awk '
    index($0, ">>> bake_wiki: stage baked wiki/main (managed") { skip=1; next }
    index($0, "<<< bake_wiki: stage baked wiki/main <<<")      { skip=0; next }
    skip { next }
    { print }
  ' "${envsh}" >"${tmp}"

  cat >>"${tmp}" <<'ENVEOF'

# >>> bake_wiki: stage baked wiki/main (managed by benchmarks/_common/bake_wiki.sh) >>>
# Replaced on every bake_wiki.sh run; hand-edits inside the markers will be lost.
if declare -F bench_container_cli >/dev/null 2>&1 && [[ -n "${BENCH_CONTAINER:-}" && -n "${BENCH_MOUNT:-}" ]]; then
  _bake_wiki_src="$(cd "$(dirname "$0")" && pwd)/wiki/main"
  if [[ -d "${_bake_wiki_src}" ]]; then
    printf '\n[bake_wiki] staging baked wiki/main -> %s/wiki/main\n' "${BENCH_MOUNT}"
    bench_container_cli exec "${BENCH_CONTAINER}" rm -rf "${BENCH_MOUNT}/wiki/main"
    bench_container_cli exec "${BENCH_CONTAINER}" mkdir -p "${BENCH_MOUNT}/wiki"
    bench_container_cli cp "${_bake_wiki_src}" "${BENCH_CONTAINER}:${BENCH_MOUNT}/wiki"
    bench_container_cli exec "${BENCH_CONTAINER}" chown -R 1000:1000 "${BENCH_MOUNT}/wiki/main" 2>/dev/null || true
  else
    printf '\n[bake_wiki] no baked wiki/main at %s; skipping stage\n' "${_bake_wiki_src}" >&2
  fi
fi
# <<< bake_wiki: stage baked wiki/main <<<
ENVEOF
  mv "${tmp}" "${envsh}"
  echo "[bake_wiki] patched ${envsh}"
}

# --- Container lifecycle ------------------------------------------------------
ENV_FILE=""
cleanup() {
  local status=$?
  if [[ -z "${KEEP_CONTAINER}" && -f "${ENV_FILE}" ]]; then
    # shellcheck disable=SC1090
    . "${ENV_FILE}"
    bench_teardown >/dev/null 2>&1 || true
  fi
  exit "${status}"
}
trap cleanup EXIT

# Step 1: boot the CI bench container (pulls image, compose/container up, copies
# repo, waits healthy). env_setup.sh exports BENCH_ENV_FILE pointing at a
# sourceable file with the bench_* helpers.
log "booting CI bench container (runtime=${RUNTIME}, run_id=${BENCH_RUN_ID})"
bash "${ROOT}/.github/bench/env_setup.sh"
ENV_FILE="${ROOT}/.bench-runtime/bench-runtime-env.sh"
[[ -f "${ENV_FILE}" ]] || die "env_setup.sh did not produce ${ENV_FILE}"
# shellcheck disable=SC1090
. "${ENV_FILE}"
[[ -n "${BENCH_CONTAINER:-}" ]] || die "BENCH_CONTAINER not set after env_setup.sh"
log "container: ${BENCH_CONTAINER} (cli=${BENCH_CONTAINER_CLI})"

# Make sure the agent-writable dirs are owned by uid 1000 before we stage files.
bench_container_cli exec "${BENCH_CONTAINER}" bash -lc '
  set -e
  mkdir -p "${BENCH_MOUNT:-/home/node/.openclaw}/workspace/main/materials"
  mkdir -p "${BENCH_MOUNT:-/home/node/.openclaw}/wiki/main"
  chown -R 1000:1000 "${BENCH_MOUNT:-/home/node/.openclaw}/workspace" \
                     "${BENCH_MOUNT:-/home/node/.openclaw}/wiki" 2>/dev/null || true
' >/dev/null

# Step 2: stage materials into the main agent workspace inside the container.
log "staging materials: ${MATERIALS_DIR} -> ${CONTAINER_MATERIALS}"
bench_container_cli exec "${BENCH_CONTAINER}" rm -rf "${CONTAINER_MATERIALS}"
bench_container_cli exec "${BENCH_CONTAINER}" mkdir -p "${CONTAINER_MATERIALS}"
# Copy the tree (dirs + files). -C lets tar carry relative paths; the materials
# dir name becomes the container subdir so subdirs (e.g. wiki/, fle/) are kept.
MATERIALS_BASENAME="$(basename "${MATERIALS_DIR}")"
MATERIALS_PARENT="$(cd "${MATERIALS_DIR}/.." && pwd)"
tar -C "${MATERIALS_PARENT}" -cf - "${MATERIALS_BASENAME}" \
  | bench_container_cli exec -i "${BENCH_CONTAINER}" tar -xf - -C "${CONTAINER_MATERIALS}"
# Flatten: if the source was a single dir, its contents end up nested one level
# deeper under CONTAINER_MATERIALS/<basename>. Move them up so the agent sees a
# flat list, then remove the wrapper.
bench_container_cli exec "${BENCH_CONTAINER}" bash -lc "
  set -e
  cd '${CONTAINER_MATERIALS}/${MATERIALS_BASENAME}' 2>/dev/null || exit 0
  # shopt -s dotglob so hidden files move too.
  shopt -s dotglob nullglob 2>/dev/null || true
  for item in *; do mv -f \"\$item\" '${CONTAINER_MATERIALS}/'; done
  rmdir '${CONTAINER_MATERIALS}/${MATERIALS_BASENAME}' 2>/dev/null || true
  # Drop any macOS AppleDouble / .DS_Store junk that slipped past COPYFILE_DISABLE.
  find '${CONTAINER_MATERIALS}' \( -name '._*' -o -name '.DS_Store' \) -delete 2>/dev/null || true
  chown -R 1000:1000 '${CONTAINER_MATERIALS}' 2>/dev/null || true
  echo '--- staged files ---'
  find '${CONTAINER_MATERIALS}' -type f ! -name '._*' ! -name '.DS_Store' | sort
"
log "materials staged"

# Count wiki pages before ingestion so we can report the delta.
count_wiki_pages() {
  bench_container_cli exec "${BENCH_CONTAINER}" bash -lc '
    find "${BENCH_MOUNT:-/home/node/.openclaw}/wiki/main" \
      -type f -name "*.md" ! -name "index.md" ! -name "WIKI.md" \
      ! -name "AGENTS.md" ! -name "inbox.md" ! -name "._*" 2>/dev/null | wc -l | tr -d " "
  '
}
PAGES_BEFORE="$(count_wiki_pages)"
log "wiki pages before ingestion: ${PAGES_BEFORE}"

if [[ "${DRY_RUN}" == "1" ]]; then
  log "DRY-RUN: skipping agent call and wiki export"
  log "would call: openclaw agent --agent main --timeout ${TIMEOUT} on ${CONTAINER_MATERIALS}"
  exit 0
fi

# Step 3: ask the main agent to ingest every paper file into the wiki.
log "calling main agent to ingest materials (timeout=${TIMEOUT}s)"
PROMPT_FILE="${BAKE_DEBUG_DIR}/ingest_prompt.txt"
cat >"${PROMPT_FILE}" <<PROMPT
你的唯一任务：将下面目录中的所有论文文件入库到研究 wiki，不做其他分析。

## 待入库目录
${CONTAINER_MATERIALS}/

## 要求
1. 列出该目录（含子目录）下所有论文文件（.md / .pdf / .txt）。每个文件代表一篇论文的全文或摘要；文件名即论文标题来源，若正文内有更准确标题则以正文为准。
2. 对每个文件按 paper-ingest 流程入库：自己运行 ingest skill 创建结构化 wiki paper page（11 节模板与 frontmatter 规范），再运行 curate skill 做质量 lint。这些能力现在是你的 predicate skill。对于论文数量较多的情况，可对每篇论文 spawn 一个 self subagent（paper-batch-ingest 的隔离 session）各自完成 ingest，避免单 context 堆积；小批量可直接自己逐篇处理。
3. 逐篇完成，不要遗漏；不要做 extract/critic/design/spec 等其他阶段的分析。
4. wiki 页面默认用中文撰写，保留论文原文标题、作者、DOI/arXiv/代码链接。

## 完成后汇报
在回复末尾，用以下格式逐一列出创建/更新的 wiki 页面（相对 wiki/main 的路径），便于核对：
INGESTED_PAGES:
- <relative/path/to/page.md>
PROMPT

# Wall-clock guard a bit above the per-call timeout. `openclaw agent --timeout`
# bounds the *agent's* own turns, but the CLI process itself can hang after the
# session ends (observed under provider 4xx storms). A host-side watchdog kills
# the exec + the lingering in-container `openclaw-agent` process so baking
# always proceeds to the export step.
WALL=$(( TIMEOUT + 180 ))
AGENT_STDOUT="${BAKE_DEBUG_DIR}/agent_stdout.json"
AGENT_STDERR="${BAKE_DEBUG_DIR}/agent_stderr.txt"
: >"${AGENT_STDOUT}"; : >"${AGENT_STDERR}"

run_agent_call() {
  bench_container_cli exec -i \
    -e LLM_API_KEY -e LLM_BASE_URL \
    "${BENCH_CONTAINER}" \
    openclaw agent \
      --agent main \
      --message "$(cat "${PROMPT_FILE}")" \
      --json --local \
      --session-key "${SESSION_KEY}" \
      --timeout "${TIMEOUT}" \
    >"${AGENT_STDOUT}" 2>"${AGENT_STDERR}"
}

# Background the call so we can poll; recover if the CLI hangs.
set +e
run_agent_call &
AGENT_PID=$!
elapsed=0
while kill -0 "${AGENT_PID}" 2>/dev/null; do
  sleep 3
  elapsed=$(( elapsed + 3 ))
  if (( elapsed >= WALL )); then
    log "agent call did not return in ${WALL}s; killing exec + in-container openclaw-agent"
    bench_container_cli exec "${BENCH_CONTAINER}" pkill -f "openclaw agent" 2>/dev/null || true
    kill "${AGENT_PID}" 2>/dev/null || true
    wait "${AGENT_PID}" 2>/dev/null || true
    break
  fi
done
wait "${AGENT_PID}" 2>/dev/null
AGENT_RC=$?
set -e

log "agent call returned (exit=${AGENT_RC})"
if [[ ${AGENT_RC} -ne 0 ]]; then
  log "agent call exited non-zero; stderr tail:"
  tail -n 40 "${AGENT_STDERR}" >&2 || true
fi
# Always keep the raw reply for forensics regardless of exit code.

PAGES_AFTER="$(count_wiki_pages)"
log "wiki pages after ingestion: ${PAGES_AFTER} (delta: $(( PAGES_AFTER - PAGES_BEFORE )))"

if [[ "${PAGES_AFTER}" == "${PAGES_BEFORE}" ]]; then
  log "WARNING: no new wiki pages detected. Inspect ${AGENT_STDOUT} / ${AGENT_STDERR}."
  log "exporting the vault anyway (it may still contain partial/index updates)."
fi

# Step 4: export the baked wiki/main out of the container.
log "exporting container ${MOUNT}/wiki/main -> ${BAKE_OUT}"
rm -rf "${BAKE_OUT}"
mkdir -p "${BAKE_OUT%/main}"
# Drop macOS junk from the container vault (the repo copy may have created it),
# then exclude plugin cache + lock dirs: cache is regenerable and stale locks
# could block later wiki writes inside the benchmark container.
bench_container_cli exec "${BENCH_CONTAINER}" bash -lc '
  find "${BENCH_MOUNT:-/home/node/.openclaw}/wiki/main" \
    \( -name "._*" -o -name ".DS_Store" \) -delete 2>/dev/null || true
'
bench_container_cli exec "${BENCH_CONTAINER}" tar -cf - -C "${MOUNT}/wiki" \
  --exclude='main/.openclaw-wiki/cache' \
  --exclude='main/.openclaw-wiki/locks' \
  --exclude='main/._*' \
  --exclude='main/.DS_Store' \
  main \
  | tar -xf - -C "${BAKE_OUT%/main}"
log "exported. files:"
find "${BAKE_OUT}" -type f | sort | sed 's/^/  /' | head -n 50

if [[ "${PATCH_ENV}" == "1" ]]; then
  log "patching ${BENCH_DIR}/env.sh to stage the baked vault"
  patch_envsh "${BENCH_DIR}/env.sh"
fi

log "done. baked vault: ${BAKE_OUT}"
log "next: run the benchmark — benchmarks/_common/run_local_benchmark.sh ${BENCH}"
exit 0
