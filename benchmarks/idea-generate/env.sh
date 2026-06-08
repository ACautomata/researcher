#!/usr/bin/env bash
# benchmarks/idea-generate/env.sh
# Writes the QA seed into the mounted workspace, so the agent's idea-generate
# skill can find it, and stages a tiny test paper fixture in the autoresearch
# wiki so the agent has something concrete to reference.
set -euo pipefail

: "${BENCH_CONTAINER:?must be exported by env_setup.sh}"
: "${BENCH_MOUNT:?must be exported by env_setup.sh}"
: "${BENCH_RUN_ID:=local}"

HERE="$(cd "$(dirname "$0")" && pwd)"
QA_SRC="${HERE}/qa.jsonl"
[[ -f "${QA_SRC}" ]] || { echo "missing ${QA_SRC}" >&2; exit 1; }

log() { printf '\n[idea-generate.env] %s\n' "$*"; }

# Bring up a fresh openclaw-bench container for this benchmark so fixtures
# and runtime state from a previous benchmark cannot leak in.
if [[ -f "${BENCH_ENV_FILE}" ]]; then
  # shellcheck disable=SC1090
  . "${BENCH_ENV_FILE}"
  bench_force_recreate
fi

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
