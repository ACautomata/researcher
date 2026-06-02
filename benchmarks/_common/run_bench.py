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
import re
import subprocess
import sys
import time
from pathlib import Path

# Allow `python3 -m` and direct invocation both.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from judge import judge_with_agent, judge_with_rules  # noqa: E402
else:
    from .judge import judge_with_agent, judge_with_rules  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent


def load_qa(path: Path) -> list[dict]:
    qas: list[dict] = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        qa = json.loads(line)
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
    final answer.

    Returns (cleaned_agent_text, session_key). With --json, openclaw writes
    the structured reply to stdout and all diagnostics to stderr, so we
    capture them separately and only look at the JSON payload[].text fields
    for the actual agent answer.
    """
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
    # Propagate the LLM provider credentials into the container. Without
    # these the embedded openclaw agent cannot reach the model.
    cmd = [
        "docker", "exec", "-i",
        "-e", "MINIMAX_API_KEY", "-e", "MINIMAX_BASE_URL",
        container, "openclaw", "agent",
        "--agent", agent_id, "--message", prompt, "--json", "--local",
        "--session-key", session_key,
        "--timeout", str(qa.get("timeout_seconds", 1800)),
    ]
    if model:
        cmd += ["--model", model]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True,
                              timeout=qa.get("timeout_seconds", 1800) + 60)
    except subprocess.TimeoutExpired:
        return ("", session_key)
    # Per docs.openclaw.ai/tools/agent-send: with --json, the structured
    # payload (including payloads[].text = the agent's reply) is on stdout;
    # diagnostics, context-engine warnings, and lane errors all go to stderr.
    # We deliberately keep them separate and only return the agent text.
    return (_extract_agent_text(proc.stdout or "", proc.stderr or ""), session_key)


# Lines we know are diagnostic noise from openclaw, not the agent's answer.
_NOISE_PREFIXES = (
    "[diagnostic]",
    "[context-engine]",
    "[gateway]",
    "[plugins]",
    "[secrets]",
    "[heartbeat]",
    "[ws]",
    "[memory-core]",
    "[memory-wiki]",
    "[memory-qmd]",
    "[qmd]",
    "[sandbox]",
    "[auth]",
    "[lanes]",
    "[tools]",
    "[secrets-ref]",
    "[secrets-store]",
    "[secrets-warning]",
    "[fallback]",
    "[init]",
    "[post-init]",
    "[config]",
    "[bridge]",
    "[obsidian]",
    "[vault]",
    "[wiki]",
    "[router]",
    "[worker]",
    "[spawn]",
    "[retry]",
    "[loop]",
    "Config health-state write failed",
    "=== ",
    "初始化",
    "配置",
    "启动",
    "挂载",
    "检测",
    "ℹ️",
    "已",
    "正在",
    "整体",
    "上下文",
    "最大",
    "API",
    "Base",
    "Gateway",
    "沙箱",
    "插件",
    "允许",
    "当前",
    "目标",
    "开放",
)

# Regex matching a *whole* log/diagnostic line that has a `[tag]` prefix and
# no real agent content.  Used as a second pass after prefix matching.
_BRACKET_TAG_RE = re.compile(r"^\s*\[(?P<tag>[a-zA-Z0-9_.-]+)\]\s*(?P<rest>.*)$")

# Diagnostic lines that look like free-form English status text, not
# agent prose.  Anything matching one of these is dropped.
_NOISE_SUBSTRINGS = (
    "Context engine ",
    "quarantining it for this process",
    "falling back to default engine",
    "Context engine \"",
    "failed during resolve: not registered",
    "failed to start",
    "lane task error",
    "Traceback (most recent call last)",
    "TypeError:",
    "RuntimeError:",
    "Error response from daemon",
    "EACCES:",
    "ENOENT:",
    "openclaw configuration is invalid",
    "secret reference is unresolved",
    "no API key found for provider",
    "Authentication failed",
    "401 Unauthorized",
    "403 Forbidden",
)

_ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


def _strip_diagnostics(text: str) -> str:
    """Drop lines that look like openclaw stderr leakage from a non-JSON reply.

    Passes:
    1. ANSI escape removal + trim.
    2. Drop lines that start with any known noise prefix.
    3. Drop lines that match a `[tag] ...` diagnostic shape.
    4. Drop lines whose body contains a known noise substring.
    5. Keep everything else.
    """
    cleaned_lines: list[str] = []
    for line in text.splitlines():
        stripped = _ANSI_RE.sub("", line).strip()
        if not stripped:
            continue
        if any(stripped.startswith(p) for p in _NOISE_PREFIXES):
            continue
        if _BRACKET_TAG_RE.match(stripped):
            # Looks like a `[foo] ...` log line.  Only keep if the tag is
            # clearly NOT in our diagnostic tag list.  For safety, drop ALL
            # bracketed-tag lines; real agent text never starts with `[tag]`.
            continue
        if any(sub in stripped for sub in _NOISE_SUBSTRINGS):
            continue
        cleaned_lines.append(stripped)
    return "\n".join(cleaned_lines)


def _extract_agent_text(stdout: str, stderr: str) -> str:
    """Pick the agent's final text out of an `openclaw agent --json` reply.

    Strategy:
    1. Try to parse stdout as JSON. The docs document shape:
         {"payloads": [{"text": "...", "mediaUrl": null}, ...], "meta": {...}}
       We concatenate every payloads[].text (the agent may emit multiple
       text parts) and return that.
    2. If stdout is empty or unparsable, fall back to stderr, but run
       the diagnostic-stripping pass first -- when context-engine plugin
       fails, openclaw writes ~2kB of `[context-engine] ... [diagnostic] ...`
       noise to stderr and no real agent text appears.
    3. If after stripping nothing usable remains, return a sentinel
       "(no agent response — only diagnostic output)" so downstream
       judges and the report get a clear signal instead of 2kB of noise.
    """
    if stdout.strip():
        try:
            data = json.loads(stdout)
        except json.JSONDecodeError:
            return _strip_diagnostics(stdout)

        # Common shape: top-level "payloads" list.
        if isinstance(data, dict):
            payloads = data.get("payloads")
            if isinstance(payloads, list) and payloads:
                texts = [p.get("text", "") for p in payloads if isinstance(p, dict)]
                joined = "\n".join(t for t in texts if t)
                if joined.strip():
                    return _strip_diagnostics(joined)
            # Some embedded-fallback responses nest under "result.payloads".
            result = data.get("result")
            if isinstance(result, dict):
                payloads = result.get("payloads")
                if isinstance(payloads, list) and payloads:
                    texts = [p.get("text", "") for p in payloads if isinstance(p, dict)]
                    joined = "\n".join(t for t in texts if t)
                    if joined.strip():
                        return _strip_diagnostics(joined)

    # Fallback: stderr.  Strip diagnostic noise and return what remains.
    cleaned_stderr = _strip_diagnostics(stderr)
    if not cleaned_stderr.strip():
        return "(no agent response — only diagnostic output)"
    return cleaned_stderr


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
        qas = load_qa(qa_path)
        results: list[dict] = []
        for qa in qas:
            t0 = time.time()
            answer, session_key = run_agent(container, agent_id, qa, run_id, model)
            elapsed = time.time() - t0
            mode = qa.get("judge", "rules")
            # LLM judge still calls main for consistency with the dispatch path.
            verdict = (judge_with_agent(qa, answer, agent_id="main", model=model)
                       if mode == "agent" else judge_with_rules(answer, qa))
            # Debug: surface the first 200 chars of the agent's reply so
            # zero-score failures are easy to diagnose from CI logs.
            head = (answer or "").replace("\n", "\\n")[:200]
            print(f"  [{qa['qa_id']}] score={verdict.get('score', 0):.3f} "
                  f"pass={verdict.get('pass', False)} "
                  f"len(answer)={len(answer or '')} head={head!r}",
                  file=sys.stderr)
            results.append({
                "qa_id": qa["qa_id"], "task_type": qa.get("task_type"),
                "target_agent": qa.get("target_agent"),
                "weight": qa.get("weight", 1.0),
                "score": verdict.get("score", 0.0), "pass": verdict.get("pass", False),
                "rationale": verdict.get("rationale", ""),
                "elapsed_seconds": round(elapsed, 1),
                "session_key": session_key, "raw_output": answer[:2000],
            })
        weight_total = sum(r["weight"] for r in results) or 1.0
        weighted = sum(r["score"] * r["weight"] for r in results) / weight_total
        passed = sum(1 for r in results if r["pass"])
        report = {
            "benchmark": bench_name, "agent": agent_id, "run_id": run_id,
            "model": model or "default", "total": len(results), "passed": passed,
            "pass_rate": passed / len(results) if results else 0.0,
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
