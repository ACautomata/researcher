#!/usr/bin/env bash
# benchmarks/autoresearch/env.sh
# Stages qa.jsonl into the autoresearch workspace. QAs in this benchmark
# test wiki fact-recall and cross-paper comparison against the existing
# wiki content (no fresh paper ingest).
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
log() { printf '\n[autoresearch.env] %s\n' "$*"; }

log "staging qa.jsonl"
docker exec "${BENCH_CONTAINER}" mkdir -p \
  "${BENCH_MOUNT}/workspace-autoresearch/bench-fixtures"
docker cp "${HERE}/qa.jsonl" "${BENCH_CONTAINER}:${BENCH_MOUNT}/workspace-autoresearch/bench-fixtures/qa.jsonl"

log "ensuring scratch dir"
docker exec "${BENCH_CONTAINER}" mkdir -p \
  "${BENCH_MOUNT}/workspace-autoresearch/bench-${BENCH_RUN_ID}"

log "staging autoresearch wiki fixtures"
docker exec "${BENCH_CONTAINER}" bash -lc "mkdir -p ${BENCH_MOUNT}/workspace-autoresearch/wiki/domains/distillation/papers ${BENCH_MOUNT}/workspace-autoresearch/wiki/domains/outofdistributiondetection/papers"
docker exec -i "${BENCH_CONTAINER}" bash -lc "cat > ${BENCH_MOUNT}/workspace-autoresearch/wiki/domains/distillation/papers/proco.md" <<'EOF'
# ProCo

ProCo measures cross-modal correspondence with correspondence coverage. It frames multimodal distillation around whether visual and text representations cover the needed cross-modal pairs.
EOF
docker exec -i "${BENCH_CONTAINER}" bash -lc "cat > ${BENCH_MOUNT}/workspace-autoresearch/wiki/domains/distillation/papers/tafap.md" <<'EOF'
# TAFAP

TAFAP prefers trajectory alignment over a single snapshot because a snapshot is diluted by later training steps, while a trajectory preserves the full optimization dynamics.
EOF
docker exec -i "${BENCH_CONTAINER}" bash -lc "cat > ${BENCH_MOUNT}/workspace-autoresearch/wiki/domains/outofdistributiondetection/papers/negprompt.md" <<'EOF'
# NegPrompt

NegPrompt learns transferable negative prompts across distributions. LSN is class-specific and less transferable, while NegPrompt focuses on distribution-transferable prompts.
EOF

log "env ready (wiki fixtures staged)"
