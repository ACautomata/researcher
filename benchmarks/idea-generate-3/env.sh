#!/usr/bin/env bash
# Shard of idea-generate benchmark.
set -euo pipefail

: "${BENCH_CONTAINER:?must be exported by env_setup.sh}"
: "${BENCH_MOUNT:?must be exported by env_setup.sh}"

HERE="$(cd "$(dirname "$0")" && pwd)"
PARENT="$(cd "${HERE}/../idea-generate" && pwd)"
# shellcheck disable=SC1090
. "${PARENT}/_env_shared.sh"
