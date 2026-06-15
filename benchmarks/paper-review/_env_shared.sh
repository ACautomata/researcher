#!/usr/bin/env bash
# benchmarks/paper-review/_env_shared.sh
# Shared env logic for paper-review shards.
# Called from each shard's env.sh.
#
# Responsibility: prepare container filesystem only.
# - Stage wiki fixtures into the wiki vault (~/.openclaw/wiki/main/)
# - Stage full-text papers into the vault
# - Link benchmarks/ into workspace for path resolution
# qa.jsonl is read by run_bench.py on the host — no need to stage it.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
# When sourced from a shard (paper-review-N/env.sh), $HERE resolves
# to the shard directory. Materials live under paper-review/, so pin
# MATERIALS_ROOT to the parent regardless of who sources this file.
MATERIALS_ROOT="${HERE}"
if [[ ! -d "${MATERIALS_ROOT}/materials" ]]; then
  MATERIALS_ROOT="$(cd "${HERE}/../paper-review" && pwd 2>/dev/null || echo "${HERE}")"
fi
log() { printf '\n[paper-review.env] %s\n' "$*"; }

# CI: the setup job tears down its container; each bench matrix job
# runs on a different runner and MUST recreate the container.
# Local: container already exists from env_setup.sh; skip recreate.
if [[ -n "${CI:-}" || -n "${GITHUB_ACTIONS:-}" ]]; then
  if [[ -n "${BENCH_ENV_FILE:-}" && -f "${BENCH_ENV_FILE}" ]]; then
    # shellcheck disable=SC1090
    . "${BENCH_ENV_FILE}"
    bench_force_recreate
  fi
elif [[ -n "${BENCH_ENV_FILE:-}" && -f "${BENCH_ENV_FILE}" ]]; then
  # shellcheck disable=SC1090
  . "${BENCH_ENV_FILE}"
fi
if ! declare -F bench_container_cli >/dev/null; then
  bench_container_cli() {
    local cli="${BENCH_CONTAINER_CLI:-${BENCH_CONTAINER_RUNTIME:-docker}}"
    [[ "${cli}" == "auto" ]] && cli=docker
    "${cli}" "$@"
  }
fi

# ── 1. Stage wiki fixtures into the wiki vault ─────────────────────
# openclaw.json configures memory-wiki vault at ~/.openclaw/wiki/main.
# QA prompts reference wiki files via this vault path.
WIKI_VAULT="${BENCH_MOUNT}/wiki/main"
MATERIALS_SRC="${MATERIALS_ROOT}/materials"
CONTAINER_MATERIALS="${BENCH_MOUNT}/benchmarks/paper-review/materials"

log "staging wiki materials -> ${WIKI_VAULT}"
bench_container_cli exec "${BENCH_CONTAINER}" mkdir -p "${WIKI_VAULT}"

if bench_container_cli exec "${BENCH_CONTAINER}" test -d "${CONTAINER_MATERIALS}"; then
  # CI recreates the container in the matrix job. Copy from the repo snapshot
  # already reapplied inside the container so vault staging does not depend on
  # host docker cp paths or permissions after bench_force_recreate.
  bench_container_cli exec "${BENCH_CONTAINER}" bash -lc \
    "set -e
     if [ -d '${CONTAINER_MATERIALS}/wiki' ]; then
       cp -a '${CONTAINER_MATERIALS}/wiki/.' '${WIKI_VAULT}/'
     fi
     find '${CONTAINER_MATERIALS}' -maxdepth 1 -type f -exec cp {} '${WIKI_VAULT}/' \\;
     count=\$(find '${WIKI_VAULT}' -maxdepth 1 -type f | wc -l | tr -d ' ')
     test \"\${count}\" -gt 0
     echo \"staged \${count} wiki vault files\""
elif [[ -d "${MATERIALS_SRC}" ]]; then
  log "container materials missing; falling back to host copy"

  # Wiki entries
  if [[ -d "${MATERIALS_SRC}/wiki" ]]; then
    for f in "${MATERIALS_SRC}/wiki"/*; do
      [[ -f "$f" ]] || continue
      bench_container_cli cp "$f" "${BENCH_CONTAINER}:${WIKI_VAULT}/$(basename "$f")"
    done
  fi

  # Full-text papers
  for f in "${MATERIALS_SRC}"/*; do
    [[ -f "$f" ]] || continue
    bench_container_cli cp "$f" "${BENCH_CONTAINER}:${WIKI_VAULT}/$(basename "$f")"
  done
else
  log "WARNING: materials dir not found; wiki vault may be empty"
fi
log "staged materials into wiki vault"

# ── 2. Link/copy benchmark materials into workspace ─────────────────
# Most agents should read the staged wiki vault (~/.openclaw/wiki/main).
# Some file tools resolve user-mentioned benchmark paths from workspace/main,
# so copy paper-review materials there as a sandbox-safe fallback.
log "staging benchmark materials into workspace"

# Symlink benchmarks/ into worker workspaces where symlinks are accepted.
# Do not symlink inside workspace/main: the agent sandbox may reject links that
# resolve outside its root. workspace/main gets a real materials copy below.
bench_container_cli exec "${BENCH_CONTAINER}" bash -lc \
  "for ws in workspace workspace/extract workspace/critic workspace/design workspace/spec workspace/audit; do
     mkdir -p '${BENCH_MOUNT}/\${ws}'
     rm -f '${BENCH_MOUNT}/\${ws}/benchmarks'
     ln -s '${BENCH_MOUNT}/benchmarks' '${BENCH_MOUNT}/\${ws}/benchmarks'
   done" || log "WARNING: symlink step failed (non-fatal)"

# For workspace/main, use real material copies. This avoids "symlink escapes
# sandbox root" errors while preserving compatibility with file-path prompts.
bench_container_cli exec "${BENCH_CONTAINER}" bash -lc \
  "rm -rf '${BENCH_MOUNT}/workspace/main/benchmarks' '${BENCH_MOUNT}/workspace/main/wiki/benchmarks'
   mkdir -p '${BENCH_MOUNT}/workspace/main/benchmarks/paper-review' '${BENCH_MOUNT}/workspace/main/wiki/benchmarks/paper-review'
   mkdir -p '${BENCH_MOUNT}/workspace/main/wiki'" || log "WARNING: mkdir step failed (non-fatal)"

if bench_container_cli exec "${BENCH_CONTAINER}" test -d "${BENCH_MOUNT}/benchmarks/paper-review/materials"; then
  bench_container_cli exec "${BENCH_CONTAINER}" cp -a \
    "${BENCH_MOUNT}/benchmarks/paper-review/materials" \
    "${BENCH_MOUNT}/workspace/main/benchmarks/paper-review/" || true
  bench_container_cli exec "${BENCH_CONTAINER}" cp -a \
    "${BENCH_MOUNT}/benchmarks/paper-review/materials" \
    "${BENCH_MOUNT}/workspace/main/wiki/benchmarks/paper-review/" || true
  log "staged materials into workspace/main"
else
  log "WARNING: materials dir not found in container — agent may fail to read wiki files"
fi

# ── 3. Output directories ──────────────────────────────────────────
log "ensuring output dirs"
bench_container_cli exec "${BENCH_CONTAINER}" mkdir -p \
  "${BENCH_MOUNT}/workspace/extract/outputs/bench-${BENCH_RUN_ID}"

log "env ready"
