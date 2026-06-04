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

完成后请在回复中按顺序逐个文件汇报导入状态：
- 每个文件成功后必须包含其原始文件名（如 ${STAGED_NAMES[0]}），并在该文件行旁边写出「导入成功」
- 任何文件失败则在该文件行旁边写出「导入失败」并说明原因
- 全部成功后再额外写一句「全部导入成功」作为汇总

判定规则：所有文件都出现「导入成功」字样才算整体成功；任何「导入失败」则整体失败。"

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
  # Success gate: the agent is instructed (above) to reply 「导入成功」 on
  # success and 「导入失败」 on failure. A plain substring match is the
  # right granularity here — the benchmark PR rejected a stricter JSON-shape
  # gate because the LLM does not reliably emit valid JSON for this kind of
  # free-form summary, and a hard-zero on the whole bench is worse than
  # accepting an occasional false positive from an honest "导入成功" reply.
  # We additionally require every staged filename to appear in the reply
  # so the agent can't pass with a vacuous success message.
  missing_files=()
  for name in "${STAGED_NAMES[@]}"; do
    printf '%s' "${IMPORT_TEXT}" | grep -qF "${name}" || missing_files+=("${name}")
  done
  if [[ ${#missing_files[@]} -gt 0 ]]; then
    log "FATAL: agent reply did not mention every staged file: ${missing_files[*]}"
    log "reply (first 400 chars): ${IMPORT_TEXT:0:400}"
    touch "${HERE}/.wiki-import-failed"
    log "failure marker written; benchmark will score 0"
  elif printf '%s' "${IMPORT_TEXT}" | grep -qF "导入失败"; then
    log "FATAL: agent reported 导入失败 in its reply"
    log "reply (first 400 chars): ${IMPORT_TEXT:0:400}"
    touch "${HERE}/.wiki-import-failed"
    log "failure marker written; benchmark will score 0"
  elif ! printf '%s' "${IMPORT_TEXT}" | grep -qF "导入成功"; then
    log "FATAL: agent reply did not contain 导入成功"
    log "reply (first 400 chars): ${IMPORT_TEXT:0:400}"
    touch "${HERE}/.wiki-import-failed"
    log "failure marker written; benchmark will score 0"
  else
    log "wiki import succeeded (${#STAGED_NAMES[@]} files)"
  fi
fi

log "env ready"
