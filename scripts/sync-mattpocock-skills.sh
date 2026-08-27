#!/usr/bin/env bash
#
# sync-mattpocock-skills.sh — 把上游 github.com/mattpocock/skills 正式发布的 skill
# 以「实体文件」vendor 进本仓库 workspace/skills/，并用锁文件钉住上游 commit SHA,
# 实现「装好在仓库里 + 可重跑同步上游」。
#
# 为什么不用符号链接 / submodule / subtree：
#   - OpenClaw 枚举 skill 目录用 readdirSync(withFileTypes).filter(isDirectory()),
#     对符号链接目录返回 false → 符号链接形式的 skill 会被静默跳过。
#   - 部署链 bench_tar_repo 打的是工作树 tar;submodule 若未 --recurse-submodules
#     则为空目录,运行时缺 skill。
#   - 上游 skill 嵌套在 skills/<分类>/<名>/,OpenClaw 读平铺 workspace/skills/<名>/,
#     subtree 之后仍需一步摊平。故统一用本脚本做实体文件 vendoring。
#
# 用法：
#   scripts/sync-mattpocock-skills.sh                 # 同步到上游 main 最新
#   scripts/sync-mattpocock-skills.sh --ref v1.2.4    # 钉到某个 tag/branch/sha
# 同步后用 git status / git diff 审阅,再自行 commit。
#
set -euo pipefail

UPSTREAM_URL="https://github.com/mattpocock/skills.git"
REF="main"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST_DIR="${REPO_ROOT}/workspace/skills"
LOCK_FILE="${DEST_DIR}/.mattpocock-upstream.lock"

while [ $# -gt 0 ]; do
  case "$1" in
    --ref) REF="${2:?--ref 需要一个值}"; shift 2 ;;
    -h|--help) sed -n '2,20p' "${BASH_SOURCE[0]}"; exit 0 ;;
    *) echo "未知参数: $1" >&2; exit 2 ;;
  esac
done

command -v git >/dev/null 2>&1 || { echo "需要 git" >&2; exit 1; }
command -v jq  >/dev/null 2>&1 || { echo "需要 jq"  >&2; exit 1; }

OLD_SHA=""
[ -f "${LOCK_FILE}" ] && OLD_SHA="$(jq -r '.sha // empty' "${LOCK_FILE}")"

TMP="$(mktemp -d)"; trap 'rm -rf "${TMP}"' EXIT
echo ">> 拉取上游 ${UPSTREAM_URL} @ ${REF}"
git clone --quiet "${UPSTREAM_URL}" "${TMP}/up"
git -C "${TMP}/up" checkout --quiet "${REF}"
NEW_SHA="$(git -C "${TMP}/up" rev-parse HEAD)"

if [ "${NEW_SHA}" = "${OLD_SHA}" ]; then
  echo ">> 已是最新（${NEW_SHA}），无需同步。"; exit 0
fi

# 旧的可管理清单（本次运行前由本脚本安装的那些;手写 skill 不在其中,绝不动）
OLD_LIST="${TMP}/old.txt"; : > "${OLD_LIST}"
[ -f "${LOCK_FILE}" ] && jq -r '.installed[]?' "${LOCK_FILE}" > "${OLD_LIST}" 2>/dev/null || true
NEW_LIST="${TMP}/new.txt"; : > "${NEW_LIST}"

# 读上游正式发布清单（plugin.json 的 skills[];自动剔除 deprecated/in-progress/misc）
PLUGIN_JSON="${TMP}/up/.claude-plugin/plugin.json"
[ -f "${PLUGIN_JSON}" ] || { echo "上游缺少 .claude-plugin/plugin.json" >&2; exit 1; }

jq -r '.skills[]' "${PLUGIN_JSON}" | sed 's|^\./||' | while IFS= read -r rel; do
  name="$(basename "${rel}")"
  src="${TMP}/up/${rel}"
  dest="${DEST_DIR}/${name}"
  [ -f "${src}/SKILL.md" ] || { echo "  跳过 ${name}（缺 SKILL.md）"; continue; }
  # 碰撞保护：目标已存在且不在我们的管理清单 → 是本仓库手写/外来 skill,绝不动
  if [ -e "${dest}" ] && ! grep -qx "${name}" "${OLD_LIST}"; then
    echo "  跳过 ${name}（与本仓库已有 skill 重名）"; continue
  fi
  rm -rf "${dest}"
  mkdir -p "${dest}"
  ( cd "${src}" && tar -cf - . ) | ( cd "${dest}" && tar -xf - )
  echo "${name}" >> "${NEW_LIST}"
  echo "  装入 ${name}"
done

# 上游已下架、但我们之前装过的 → 移除（只删我们管理的）
while IFS= read -r name; do
  [ -z "${name}" ] && continue
  if ! grep -qx "${name}" "${NEW_LIST}"; then
    rm -rf "${DEST_DIR:?}/${name}"; echo "  移除 ${name}（上游已下架）"
  fi
done < "${OLD_LIST}"

# 写锁文件（点开头 → OpenClaw 扫描器跳过;且 isDirectory 过滤本就不认文件）
INSTALLED_JSON="$(jq -R . < "${NEW_LIST}" | jq -sc 'sort')"
jq -n \
  --arg url "${UPSTREAM_URL}" --arg ref "${REF}" --arg sha "${NEW_SHA}" \
  --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" --argjson installed "${INSTALLED_JSON}" \
  '{upstream:$url, ref:$ref, sha:$sha, syncedAt:$ts, installed:$installed}' \
  > "${LOCK_FILE}"

echo ""
echo "== 完成 =="
echo "  上游 SHA : ${OLD_SHA:-<首次>} -> ${NEW_SHA}"
echo "  已安装   : $(grep -c . "${NEW_LIST}" 2>/dev/null || echo 0) 个 skill -> workspace/skills/"
echo "下一步: git add workspace/skills scripts → git commit"
