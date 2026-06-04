#!/usr/bin/env bash
# benchmarks/paper-review/env.sh
# Stages the paper-review seed QA and the FedAux fixture paper into the
# container so the paper-review sub-agent has both the prompts and the
# materials available when the agent runs.
set -euo pipefail

: "${BENCH_CONTAINER:?must be exported by env_setup.sh}"
: "${BENCH_MOUNT:?must be exported by env_setup.sh}"
: "${BENCH_RUN_ID:=local}"

HERE="$(cd "$(dirname "$0")" && pwd)"
QA_SRC="${HERE}/qa.jsonl"
MATERIALS_SRC="${HERE}/materials"
[[ -f "${QA_SRC}" ]] || { echo "missing ${QA_SRC} (run build_qa.py first)" >&2; exit 1; }

log() { printf '\n[paper-review.env] %s\n' "$*"; }

# Bring up a fresh openclaw-bench container for this benchmark so fixtures
# and runtime state from a previous benchmark cannot leak in.
if [[ -f "${BENCH_ENV_FILE}" ]]; then
  # shellcheck disable=SC1090
  . "${BENCH_ENV_FILE}"
  bench_force_recreate
fi

log "staging qa.jsonl"
docker exec "${BENCH_CONTAINER}" mkdir -p \
  "${BENCH_MOUNT}/workspace-paper-review/bench-fixtures"
docker cp "${QA_SRC}" "${BENCH_CONTAINER}:${BENCH_MOUNT}/workspace-paper-review/bench-fixtures/qa.jsonl"

if [[ -d "${MATERIALS_SRC}" ]]; then
  log "staging materials (${MATERIALS_SRC})"
  docker exec "${BENCH_CONTAINER}" mkdir -p \
    "${BENCH_MOUNT}/workspace-paper-review/bench-fixtures/materials"
  tar -C "${MATERIALS_SRC}" -cf - . | \
    docker cp - "${CONTAINER:-${BENCH_CONTAINER}}:${BENCH_MOUNT}/workspace-paper-review/bench-fixtures/materials/" \
    || docker exec "${BENCH_CONTAINER}" bash -lc \
        "rm -rf ${BENCH_MOUNT}/workspace-paper-review/bench-fixtures/materials && mkdir -p ${BENCH_MOUNT}/workspace-paper-review/bench-fixtures/materials"
  for f in "${MATERIALS_SRC}"/*; do
    [[ -f "$f" ]] || continue
    docker cp "$f" "${BENCH_CONTAINER}:${BENCH_MOUNT}/workspace-paper-review/bench-fixtures/materials/$(basename "$f")"
  done
fi

log "ensuring output dir"
docker exec "${BENCH_CONTAINER}" mkdir -p \
  "${BENCH_MOUNT}/workspace-paper-review/outputs/bench-${BENCH_RUN_ID}"

# ---------------------------------------------------------------------------
# Wiki import: call main agent to import the MD materials into the wiki.
# The agent must confirm every staged file was imported; otherwise we write a
# failure marker that metrics.py picks up and the benchmark scores 0.
# ---------------------------------------------------------------------------

# Clean stale marker from a previous run
rm -f "${HERE}/.wiki-import-failed"
rm -f "${HERE}/.wiki-import-stderr.log"

log "staging MD materials into autoresearch inbox"
WIKI_INBOX="${BENCH_MOUNT}/workspace-autoresearch/raw/inbox/bench-${BENCH_RUN_ID}"
docker exec "${BENCH_CONTAINER}" mkdir -p "${WIKI_INBOX}"
STAGED_NAMES=()
for f in "${MATERIALS_SRC}"/*.md; do
  [[ -f "$f" ]] || continue
  name="$(basename "$f")"
  docker cp "$f" "${BENCH_CONTAINER}:${WIKI_INBOX}/${name}"
  STAGED_NAMES+=("${name}")
done
if [[ ${#STAGED_NAMES[@]} -eq 0 ]]; then
  log "FATAL: no .md files found in ${MATERIALS_SRC} — nothing to import"
  touch "${HERE}/.wiki-import-failed"
  log "failure marker written; benchmark will score 0"
  return 0 2>/dev/null || exit 0
fi

# Build the staged-files list and the import prompt dynamically from the
# actual glob — avoids hardcoded filenames drifting out of sync with
# materials/.
STAGED_LIST=""
for name in "${STAGED_NAMES[@]}"; do
  STAGED_LIST+="- ${name}"$'\n'
done
STAGED_BULLETS="${STAGED_LIST%$'\n'}"

log "calling main agent to import ${#STAGED_NAMES[@]} materials into wiki"
IMPORT_SESSION="agent:main:wiki-import-${BENCH_RUN_ID}-$$-$(cat /proc/sys/kernel/random/uuid 2>/dev/null || echo "$$-$RANDOM")"
IMPORT_PROMPT="请将以下 ${#STAGED_NAMES[@]} 份论文材料导入 wiki。

材料位于 workspace-autoresearch/raw/inbox/bench-${BENCH_RUN_ID}/ 目录下：
${STAGED_BULLETS}

请使用 autoresearch 子 agent 的 ingest 流程将这些材料逐个导入 wiki。

完成后请按以下结构逐个文件汇报导入状态（必须使用 JSON 代码块，不要使用其他格式）：

\`\`\`json
{\"files\": [{\"name\": \"<filename>\", \"status\": \"ok|failed\", \"path\": \"<wiki 页面路径或错误原因>\"}]}
\`\`\`

判定规则：所有文件 status 都为 ok 才算导入成功；任何一个为 failed 则整体失败。"

IMPORT_RAW=""
INVOCATION_OK=0
if IMPORT_RAW=$(docker exec -i \
    -e "MINIMAX_API_KEY" -e "MINIMAX_BASE_URL" \
    "${BENCH_CONTAINER}" openclaw agent \
    --agent main \
    --message "${IMPORT_PROMPT}" \
    --json --local \
    --session-key "${IMPORT_SESSION}" \
    --timeout 600 \
    2>"${HERE}/.wiki-import-stderr.log"); then
  INVOCATION_OK=1
fi

# Extract agent text from JSON payloads (mirrors _extract_agent_text in
# run_bench.py: prefers top-level payloads[], then result.payloads[]).
IMPORT_TEXT=$(printf '%s' "${IMPORT_RAW}" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    texts = []
    if isinstance(data, dict):
        payloads = data.get('payloads')
        if isinstance(payloads, list) and payloads:
            joined = '\n'.join(p.get('text','') for p in payloads if isinstance(p, dict) and p.get('text'))
            if joined.strip():
                print(joined)
                sys.exit(0)
        result = data.get('result')
        if isinstance(result, dict):
            payloads = result.get('payloads')
            if isinstance(payloads, list) and payloads:
                joined = '\n'.join(p.get('text','') for p in payloads if isinstance(p, dict) and p.get('text'))
                if joined.strip():
                    print(joined)
                    sys.exit(0)
except Exception:
    pass
" 2>/dev/null) || IMPORT_TEXT=""

if [[ ${INVOCATION_OK} -ne 1 ]]; then
  log "FATAL: docker exec failed; see ${HERE}/.wiki-import-stderr.log"
  head -5 "${HERE}/.wiki-import-stderr.log" 2>/dev/null | sed 's/^/  | /' || true
  touch "${HERE}/.wiki-import-failed"
  log "failure marker written; benchmark will score 0"
elif [[ -z "${IMPORT_TEXT}" ]]; then
  log "FATAL: agent returned no parseable text; see ${HERE}/.wiki-import-stderr.log"
  head -5 "${HERE}/.wiki-import-stderr.log" 2>/dev/null | sed 's/^/  | /' || true
  touch "${HERE}/.wiki-import-failed"
  log "failure marker written; benchmark will score 0"
else
  # Structural success check: the agent must report every staged filename
  # with status=ok. A loose substring grep would let a passing mention of
  # the success word slip through; require explicit per-file status.
  missing_ok=()
  for name in "${STAGED_NAMES[@]}"; do
    if ! printf '%s' "${IMPORT_TEXT}" | grep -q "\"name\":[[:space:]]*\"${name}\"" \
       || ! printf '%s' "${IMPORT_TEXT}" | grep -q "\"status\":[[:space:]]*\"ok\""; then
      missing_ok+=("${name}")
    fi
  done
  if [[ ${#missing_ok[@]} -eq 0 ]]; then
    log "wiki import succeeded (${#STAGED_NAMES[@]} files)"
  else
    log "FATAL: agent did not confirm ok for: ${missing_ok[*]}"
    touch "${HERE}/.wiki-import-failed"
    log "failure marker written; benchmark will score 0"
  fi
fi

log "env ready"
