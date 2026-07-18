#!/usr/bin/env python3
"""Render a single PR comment from ClawProBench per-scenario result files.

Each matrix job runs exactly one scenario (fork ``run.py run --scenario <id>``)
and emits ``result_main_<ts>.json`` containing that one scenario's trials. The
bootstrap renames it to ``result_<scenario>.json`` before uploading, so the
aggregate step can merge-multiple without timestamp collisions.

This renderer reads each file's ``scenarios[]`` and re-aggregates across files
(per-file top-level ``overall_score``/``strict_pass_rate`` describe a single
scenario, not the suite). It is self-contained — it does NOT import the legacy
``benchmarks/_common/report_pr.py`` (that file is retired in the cleanup PR).

Inputs (env):
  BENCH_RESULTS_DIR     -- dir containing result_<scenario>.json (default: bench-results)
  BENCH_EXPECTED_SCENARIOS -- optional comma-separated scenario ids; when set,
                              missing/extra ids are surfaced as warnings (does not fail).
  BENCH_BASE_SUMMARY    -- optional path to a previous summary for delta
  BENCH_COMMENT_MARKER  -- hidden HTML marker (default: openclaw-clawprobench-report)
  GH_TOKEN / gh CLI     -- for posting; if missing, the body is printed to stdout.

Output: prints the rendered Markdown body; upserts a PR comment if gh + PR context.
"""
from __future__ import annotations

import glob
import json
import os
import subprocess
import sys
from pathlib import Path

MARKER = os.environ.get(
    "BENCH_COMMENT_MARKER", "<!-- openclaw-clawprobench-report -->"
)


def _load(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _scenario_view(report: dict) -> dict | None:
    """Pull the single scenario this file ran. Returns None if absent."""
    scenarios = report.get("scenarios") or []
    if not scenarios:
        return None
    s = scenarios[0]
    return {
        "scenario_id": s.get("scenario_id", Path("unknown").stem),
        "name": s.get("name", s.get("scenario_id", "?")),
        "difficulty": s.get("difficulty", "?"),
        "avg_score": float(s.get("avg_score", 0.0)),
        "pass_rate": float(s.get("pass_rate", 0.0)),
        "pass_at_k_any": bool(s.get("pass_at_k_any", False)),  # pass@3: >=1 trial passed
        "strict_pass_k": bool(s.get("strict_pass_k", False)),  # pass^3: all trials passed
        "pass_count": int(s.get("pass_count", 0)),
        "trial_count": int(s.get("trial_count", 0)),
        "trials_per_scenario": int(report.get("trials_per_scenario", s.get("trial_count", 0))),
        "report_path": report.get("summary", {}).get("report_path", ""),
    }


def _delta(base: dict, current: dict) -> str:
    """Delta vs a prior summary {avg_score, pass_at_3_rate, pass_cubed_rate}."""
    if not base:
        return "—"
    d = current["avg_score"] - base.get("avg_score", 0.0)
    arrow = "🟢" if d > 0.005 else ("🔴" if d < -0.005 else "⚪")
    return f"{arrow} {d:+.3f}"


def render(results_dir: Path, base: dict | None) -> tuple[str, dict]:
    paths = sorted(glob.glob(str(results_dir / "result_*.json")))
    if not paths:
        return f"{MARKER}\n_No ClawProBench result files found in {results_dir}._\n", {}

    views: list[dict] = []
    for p in paths:
        report = _load(Path(p))
        view = _scenario_view(report)
        if view is None:
            continue
        views.append(view)

    n = len(views)
    if n == 0:
        return f"{MARKER}\n_No scenarios found in result files under {results_dir}._\n", {}

    pass_at_3 = sum(1 for v in views if v["pass_at_k_any"])
    pass_cubed = sum(1 for v in views if v["strict_pass_k"])
    avg_score = sum(v["avg_score"] for v in views) / n
    trials = sum(v["trial_count"] for v in views)
    summary = {
        "scenarios_run": n,
        "pass_at_3_rate": pass_at_3 / n,
        "pass_cubed_rate": pass_cubed / n,
        "avg_score": avg_score,
        "total_trials": trials,
    }

    lines = [MARKER, "# ClawProBench Report (target: main/颖姗)", ""]
    lines.append(f"- Run id: `{os.environ.get('BENCH_RUN_ID', 'local')}`")
    lines.append(f"- Commit: `{os.environ.get('BENCH_COMMIT', 'unknown')}`")
    lines.append(f"- Model: `{os.environ.get('LLM_MODEL', 'minimax/MiniMax-M3')}`")
    lines.append(f"- Fork pin: `{os.environ.get('CLAWPROBENCH_PIN', '5b368ea')}`")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|---|---:|")
    lines.append(f"| Scenarios run | {n} |")
    lines.append(f"| Trials | {trials} |")
    lines.append(f"| pass@3 rate (≥1 trial pass) | {summary['pass_at_3_rate'] * 100:.1f}% ({pass_at_3}/{n}) |")
    lines.append(f"| pass^3 rate (all trials pass) | {summary['pass_cubed_rate'] * 100:.1f}% ({pass_cubed}/{n}) |")
    lines.append(f"| Avg score | {avg_score:.3f} {_delta(base or {}, {'avg_score': avg_score})} |")
    lines.append("")
    lines.append("| Scenario | Difficulty | Trials | pass@3 | pass^3 | Avg |")
    lines.append("|---|---|---:|:---:|:---:|---:|")
    for v in sorted(views, key=lambda x: x["scenario_id"]):
        lines.append(
            f"| `{v['scenario_id']}` | {v['difficulty']} | {v['trial_count']} | "
            f"{'✅' if v['pass_at_k_any'] else '❌'} | {'✅' if v['strict_pass_k'] else '❌'} | "
            f"{v['avg_score']:.3f} |"
        )
    lines.append("")

    # Expected-scenario coverage check (warn-only; partial matrix runs are valid).
    expected = [s.strip() for s in os.environ.get("BENCH_EXPECTED_SCENARIOS", "").split(",") if s.strip()]
    if expected:
        got = {v["scenario_id"] for v in views}
        missing = [s for s in expected if s not in got]
        extra = sorted(got - set(expected))
        if missing:
            lines.append(f"**⚠️ Missing {len(missing)} expected scenario(s):** {', '.join(f'`{m}`' for m in missing)}")
            lines.append("")
        if extra:
            lines.append(f"**ℹ️ {len(extra)} unexpected scenario(s):** {', '.join(f'`{e}`' for e in extra)}")
            lines.append("")

    lines.append(f"_Aggregate of {n} scenario(s), {trials} trial(s). Deterministic custom_check grading._")
    return "\n".join(lines) + "\n", summary


def post_comment(body: str) -> bool:
    """Upsert the comment via gh api. Returns True on success."""
    pr = os.environ.get("BENCH_PR_NUMBER")
    repo = os.environ.get("BENCH_REPO")
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not (pr and repo and token):
        return False
    list_cmd = ["gh", "api", f"repos/{repo}/issues/{pr}/comments", "--paginate"]
    env = os.environ.copy()
    env["GH_TOKEN"] = token
    try:
        out = subprocess.run(list_cmd, capture_output=True, text=True, env=env, check=True)
    except subprocess.CalledProcessError:
        return False
    try:
        comments = json.loads(out.stdout or "[]")
    except json.JSONDecodeError:
        comments = []
    existing_id = None
    for c in comments:
        if MARKER in (c.get("body") or ""):
            existing_id = c.get("id")
            break
    if existing_id:
        cmd = ["gh", "api", "-X", "PATCH", f"repos/{repo}/issues/comments/{existing_id}", "-f", f"body={body}"]
    else:
        cmd = ["gh", "api", "-X", "POST", f"repos/{repo}/issues/{pr}/comments", "-f", f"body={body}"]
    try:
        subprocess.run(cmd, capture_output=True, text=True, env=env, check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def _load_base() -> dict | None:
    """Resolve the base summary for delta comparison.

    BENCH_BASE_SUMMARY may be either a file path OR a base64-encoded JSON
    string (the latter is how it's stored as a repo secret per CLAUDE.md).
    """
    raw = os.environ.get("BENCH_BASE_SUMMARY")
    if not raw:
        return None
    # Path.exists() raises OSError(ENAMETOOLONG) on Linux when `raw` is a long
    # base64 blob (the secret form easily exceeds NAME_MAX), instead of
    # returning False. Guard the probe so the aggregate step falls through to
    # the base64 branch instead of crashing. (os.path.exists swallows this;
    # pathlib.Path.exists does not.)
    try:
        if Path(raw).exists():
            return _load(Path(raw))
    except OSError:
        pass
    # Treat as base64-encoded JSON (the secret form).
    try:
        import base64
        return json.loads(base64.b64decode(raw).decode("utf-8"))
    except Exception:
        return None


def main() -> int:
    results_dir = Path(os.environ.get("BENCH_RESULTS_DIR", "bench-results"))
    base = _load_base()
    body, _ = render(results_dir, base)
    if not post_comment(body):
        print(body)
    return 0


if __name__ == "__main__":
    sys.exit(main())
