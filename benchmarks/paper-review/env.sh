#!/usr/bin/env bash
# benchmarks/paper-review/env.sh
# Stages the paper-review seed QA and the FedAux fixture paper into the
# container so the paper-review sub-agent has both the prompts and the
# materials available when the agent runs.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
RUNTIME_ENV_FILE="${BENCH_RUNTIME_ENV_FILE:-${ROOT}/.bench-runtime/bench-runtime.env}"
if [[ -f "${RUNTIME_ENV_FILE}" ]]; then
  set -a
  # shellcheck disable=SC1090
  . "${RUNTIME_ENV_FILE}"
  set +a
fi

: "${BENCH_CONTAINER:?must be exported by env_setup.sh}"
: "${BENCH_MOUNT:?must be exported by env_setup.sh}"
: "${BENCH_RUN_ID:=local}"

HERE="$(cd "$(dirname "$0")" && pwd)"
QA_SRC="${HERE}/qa.jsonl"
MATERIALS_SRC="${HERE}/materials"
[[ -f "${QA_SRC}" ]] || { echo "missing ${QA_SRC} (run build_qa.py first)" >&2; exit 1; }

log() { printf '\n[paper-review.env] %s\n' "$*"; }

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

log "env ready"
