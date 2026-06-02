#!/usr/bin/env python3
"""benchmarks/_common/run_bench.py

Generic driver for any benchmark directory that follows the unified interface
(env.sh + qa.jsonl + metrics.py).

**CI policy: every benchmark calls only the `main` agent.** The main agent is
responsible for delegating to the appropriate sub-agent via `sessions_spawn`.
Each QA's `target_agent` field names the sub-agent main should spawn; if
absent, main runs the task itself.

Per-benchmark `metrics.py` becomes a 6-line shim:

    from pathlib import Path
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_common"))
    from run_bench import main
    main("paper-review")
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

# Allow `python3 -m` and direct invocation both.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from judge import judge_with_agent, judge_with_rules  # noqa: E402
else:
    from .judge import judge_with_agent, judge_with_rules  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent


def _substitute_run_id(value: Any, run_id: str) -> Any:
    """Replace the schema placeholder used by QA fixtures with the active run id."""
    if isinstance(value, str):
        return value.replace("bench-<run>", f"bench-{run_id}").replace("<run>", run_id)
    if isinstance(value, list):
        return [_substitute_run_id(v, run_id) for v in value]
    if isinstance(value, dict):
        return {k: _substitute_run_id(v, run_id) for k, v in value.items()}
    return value


def load_qa(path: Path, run_id: str) -> list[dict]:
    qas: list[dict] = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        qa = _substitute_run_id(json.loads(line), run_id)
        qa.setdefault("qa_id", f"qa-{i:03d}")
        qa.setdefault("agent", qa.get("agent") or "main")
        qa.setdefault("pass_threshold", 0.5)
        qa.setdefault("weight", 1.0)
        qa.setdefault("judge", "rules")
        qas.append(qa)
    return qas


def run_agent(container: str, agent_id: str, qa: dict, run_id: str,
              model: str | None) -> tuple[str, str]:
    """Always invokes `agent_id` (which the CI contract pins to `main`).
    If the QA carries a `target_agent` field, the prompt is wrapped so main
    delegates to that sub-agent via sessions_spawn and returns the sub-agent's
    final answer."""
    target = qa.get("target_agent")
    prompt = qa["question"]
    if qa.get("input_material"):
        material = qa["input_material"]
        if isinstance(material, dict):
            material = material.get("content") or Path(material["path"]).read_text(encoding="utf-8")
        prompt = f"{material}\n\n---\n\n{prompt}"
    if target and target != agent_id:
        prompt = (
            f"[BENCHMARK DIRECTIVE — read carefully]\n"
            f"This task must be executed by the `{target}` sub-agent.\n"
            f"Use the sessions_spawn tool to delegate:\n"
            f"  sessions_spawn(agentId=\"{target}\", task=<the full task below>, "
            f"mode=\"run\", runTimeoutSeconds={qa.get('timeout_seconds', 1800)})\n"
            f"Then return the sub-agent's final reply as your only output.\n"
            f"Do NOT solve the task yourself. Do NOT add commentary. Return the "
            f"sub-agent's reply verbatim.\n\n"
            f"---\n\n{prompt}"
        )
    session_key = f"agent:{agent_id}:bench-{run_id}-{qa['qa_id']}"
    cmd = [
        "docker", "exec", "-i", container, "openclaw", "agent",
        "--agent", agent_id, "--message", prompt, "--json", "--local",
        "--session-key", session_key,
        "--timeout", str(qa.get("timeout_seconds", 1800)),
    ]
    if model:
        cmd += ["--model", model]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True,
                             timeout=qa.get("timeout_seconds", 1800) + 60)
    except subprocess.TimeoutExpired:
        return ("", session_key)
    return ((out.stdout or "") + "\n" + (out.stderr or ""), session_key)


def _candidate_artifact_paths(artifact: str, bench_name: str) -> list[str]:
    mount = os.environ.get("BENCH_MOUNT", "/home/node/.openclaw")
    artifact = artifact.lstrip("/")
    paths = [f"{mount}/{artifact}"]
    if artifact.startswith("wiki/"):
        paths.insert(0, f"{mount}/workspace-autoresearch/{artifact}")
    elif artifact.startswith("outputs/"):
        paths.insert(0, f"{mount}/workspace-paper-review/{artifact}")
    elif artifact.startswith("idea-runs/"):
        paths.insert(0, f"{mount}/workspace-idea-generate/{artifact}")
    elif not artifact.startswith("workspace-"):
        paths.append(f"{mount}/benchmarks/{bench_name}/{artifact}")
    return list(dict.fromkeys(paths))


def verify_expected_artifacts(container: str, bench_name: str, qa: dict) -> dict:
    expected = qa.get("expected_artifacts") or []
    if not expected:
        return {"score": 1.0, "pass": True, "rationale": "no expected_artifacts declared", "missing": []}
    missing: list[str] = []
    for artifact in expected:
        candidates = _candidate_artifact_paths(str(artifact), bench_name)
        test_expr = " || ".join(f"test -s {json.dumps(p)}" for p in candidates)
        out = subprocess.run(["docker", "exec", container, "bash", "-lc", test_expr],
                             capture_output=True, text=True)
        if out.returncode != 0:
            missing.append(str(artifact))
    score = (len(expected) - len(missing)) / len(expected)
    return {
        "score": round(score, 4),
        "pass": not missing,
        "rationale": "all expected artifacts exist" if not missing else f"missing expected_artifacts={missing[:5]}",
        "missing": missing,
    }


def _combine_verdicts(score_verdict: dict, artifact_verdict: dict) -> dict:
    if not artifact_verdict.get("pass", True):
        score = min(float(score_verdict.get("score", 0.0)), float(artifact_verdict.get("score", 0.0)))
        return {
            **score_verdict,
            "score": round(score, 4),
            "pass": False,
            "rationale": f"{score_verdict.get('rationale', '')}; {artifact_verdict.get('rationale', '')}".strip("; "),
            "missing_artifacts": artifact_verdict.get("missing", []),
        }
    return score_verdict


def main(bench_name: str, agent_id: str | None = None) -> int:
    """Run a benchmark. `agent_id` is the CI-side caller; the contract forces
    this to `main`. Per-QA sub-agent routing goes through `target_agent`."""
    qa_path = Path(os.environ.get("BENCH_QA_PATH", ROOT / "benchmarks" / bench_name / "qa.jsonl"))
    report_path = Path(os.environ.get("BENCH_REPORT_PATH",
                                       ROOT / "benchmarks" / bench_name / "bench-report.json"))
    container = os.environ.get("BENCH_CONTAINER", "")
    run_id = os.environ.get("BENCH_RUN_ID", f"local-{int(time.time())}")
    model = os.environ.get("BENCH_MODEL")
    # Hard policy: CI only ever calls `main`. Sub-agents are reached through
    # main's sessions_spawn, never directly.
    agent_id = agent_id or os.environ.get("BENCH_AGENT") or "main"
    assert agent_id == "main", (
        f"CI policy violation: benchmarks may only target the `main` agent, "
        f"got agent_id={agent_id!r}. Set `target_agent` on the QA to route "
        f"through sessions_spawn instead."
    )

    if not container:
        print(f"[{bench_name}] BENCH_CONTAINER not set; skipping agent calls (dry-run).", file=sys.stderr)
        # Still emit a stub report so PR comment machinery has something to read.
        report = {"benchmark": bench_name, "agent": agent_id, "run_id": run_id,
                  "model": model or "default", "total": 0, "passed": 0,
                  "pass_rate": 0.0, "avg_score": 0.0, "results": [],
                  "skipped": "no container"}
    else:
        qas = load_qa(qa_path, run_id)
        results: list[dict] = []
        for qa in qas:
            t0 = time.time()
            answer, session_key = run_agent(container, agent_id, qa, run_id, model)
            elapsed = time.time() - t0
            mode = qa.get("judge", "rules")
            if mode == "skip":
                verdict = {"score": None, "pass": None, "rationale": "judge mode is skip", "skipped": True}
            elif mode == "agent":
                # LLM judge still calls main for consistency with the dispatch path.
                verdict = judge_with_agent(qa, answer, agent_id="main", model=model, container=container)
            else:
                verdict = judge_with_rules(answer, qa)
            if mode != "skip":
                verdict = _combine_verdicts(verdict, verify_expected_artifacts(container, bench_name, qa))
            results.append({
                "qa_id": qa["qa_id"], "task_type": qa.get("task_type"),
                "target_agent": qa.get("target_agent"),
                "weight": qa.get("weight", 1.0),
                "score": verdict.get("score"), "pass": verdict.get("pass"),
                "skipped": verdict.get("skipped", False),
                "rationale": verdict.get("rationale", ""),
                "missing_artifacts": verdict.get("missing_artifacts", []),
                "elapsed_seconds": round(elapsed, 1),
                "session_key": session_key, "raw_output": answer[:2000],
            })
        scored = [r for r in results if not r.get("skipped")]
        weight_total = sum(r["weight"] for r in scored) or 1.0
        weighted = sum(float(r.get("score") or 0.0) * r["weight"] for r in scored) / weight_total
        passed = sum(1 for r in scored if r["pass"])
        report = {
            "benchmark": bench_name, "agent": agent_id, "run_id": run_id,
            "model": model or "default", "total": len(scored), "skipped": len(results) - len(scored),
            "passed": passed, "pass_rate": passed / len(scored) if scored else 0.0,
            "avg_score": round(weighted, 4), "results": results,
        }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    results_dir = Path(os.environ.get("BENCH_RESULTS_DIR", ROOT / "bench-results"))
    results_dir.mkdir(parents=True, exist_ok=True)
    (results_dir / f"{bench_name}.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[{bench_name}] {report['passed']}/{report['total']} passed, avg_score={report['avg_score']:.3f}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: run_bench.py <bench_name>", file=sys.stderr)
        sys.exit(2)
    bench = sys.argv[1]
    sys.exit(main(bench))
