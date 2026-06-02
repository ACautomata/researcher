#!/usr/bin/env bash
# benchmarks/idea-generate/env.sh
# Writes the QA seed into the mounted workspace, so the agent's idea-generate
# skill can find it, and stages a tiny test paper fixture in the autoresearch
# wiki so the agent has something concrete to reference.
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
[[ -f "${QA_SRC}" ]] || { echo "missing ${QA_SRC}" >&2; exit 1; }

log() { printf '\n[idea-generate.env] %s\n' "$*"; }

log "staging qa.jsonl -> ${BENCH_MOUNT}/workspace-idea-generate/benchmark-${BENCH_RUN_ID}.jsonl"
docker exec "${BENCH_CONTAINER}" mkdir -p \
  "${BENCH_MOUNT}/workspace-idea-generate/bench-fixtures"
docker cp "${QA_SRC}" "${BENCH_CONTAINER}:${BENCH_MOUNT}/workspace-idea-generate/bench-fixtures/qa.jsonl"

log "staging scratch output dir"
docker exec "${BENCH_CONTAINER}" mkdir -p \
  "${BENCH_MOUNT}/workspace-idea-generate/idea-runs/bench-${BENCH_RUN_ID}"

log "smoke: idea-generate skill available?"
docker exec "${BENCH_CONTAINER}" bash -lc \
  "test -f ${BENCH_MOUNT}/workspace-idea-generate/skills/idea-generate/SKILL.md && echo OK || echo MISSING"
log "env ready"
