#!/usr/bin/env python3
"""Reusable scoring for benchmark metrics.py scripts.

Two judges:
  judge_with_rules(answer, qa)  -- rule-based, uses qa.gold_answer and must_contain-style hints.
  judge_with_agent(qa, answer, agent_id, model=None) -- LLM judge via `openclaw agent --json --local`.

Both return a dict: {score: float (0-1), pass: bool, rationale: str, dimensions?: dict}.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from typing import Any

# --- Rule-based judge --------------------------------------------------------

_KEYWORD_HINT = re.compile(r"必须[：:]\s*([^\n]+)|must_contain[：:]\s*([^\n]+)", re.I)


def _extract_must_contain(gold: Any) -> list[str]:
    """Pull a flat list of required tokens out of a gold_answer.

    Recognized shapes:
      - string: "Term1\nTerm2" (one per line) or "Term1, Term2"
      - object: {"must_contain": ["Term1", ...]} or {"fields": [...]}
    """
    if gold is None:
        return []
    if isinstance(gold, str):
        m = _KEYWORD_HINT.search(gold)
        if m:
            tail = m.group(1) or m.group(2) or ""
            return [t.strip() for t in re.split(r"[\n,，；;]", tail) if t.strip()]
        return [t.strip() for t in re.split(r"[\n,，；;]", gold) if t.strip() and len(t.strip()) > 1]
    if isinstance(gold, dict):
        out = list(gold.get("must_contain") or [])
        out += list(gold.get("fields") or [])
        return [str(t) for t in out if str(t).strip()]
    return []


def _behavior_checks(answer: str, qa: dict) -> list[str]:
    """Encode common behavioral rubric constraints for the rule judge.

    Rule-scored QAs often carry their real requirements in `rubric` or
    `gold_answer.key_behavior`; these checks keep obvious violations from
    passing on keyword coverage alone.
    """
    text = answer or ""
    lower = text.lower()
    rubric = " ".join(str(v) for v in [qa.get("rubric"), (qa.get("gold_answer") or {}).get("key_behavior") if isinstance(qa.get("gold_answer"), dict) else None] if v)
    missing: list[str] = []
    forbidden_phrases = ["可能是", "应该是", "probably", "should be"]
    if any(term in rubric for term in ["不出现", "No '", "no '", "No fabrication", "no fabrication", "不要夸大", "unsourced"]):
        hits = [phrase for phrase in forbidden_phrases if phrase.lower() in lower]
        if hits:
            missing.append("forbidden speculative/unsourced phrasing: " + ", ".join(hits[:5]))
    if "No fabricated numbers" in rubric or "no fabricated numbers" in rubric:
        allowed_numbers = {"0.18", "0.16", "40", "20", "1", "5"}
        numbers = set(re.findall(r"(?<![A-Za-z])\d+(?:\.\d+)?%?", text))
        fabricated = sorted(n for n in numbers if n.rstrip("%") not in allowed_numbers)
        if fabricated:
            missing.append("potential fabricated numbers: " + ", ".join(fabricated[:5]))
    for required in re.findall(r"(?:names?|mentions?|包含|必须包含|必须包含具体|必须).*?([A-Za-z][A-Za-z0-9@_-]+)", rubric):
        if required.lower() not in lower:
            missing.append(f"rubric keyword missing: {required}")
    return missing


def judge_with_rules(answer: str, qa: dict) -> dict:
    """Score an answer against qa.gold_answer with simple keyword coverage.

    Score = covered / required (0 if no requirements). Pass when score >= qa.pass_threshold.
    """
    required = _extract_must_contain(qa.get("gold_answer"))
    if not required:
        # No gold answer means we can only do a soft pass: not-empty + length sanity.
        text = (answer or "").strip()
        if not text:
            return {"score": 0.0, "pass": False, "rationale": "empty answer, no gold to check against"}
        score = min(1.0, len(text) / 200.0)
        return {"score": score, "pass": score >= qa.get("pass_threshold", 0.5),
                "rationale": f"no gold_answer; scored on length={len(text)}"}

    text = (answer or "").lower()
    missing = [r for r in required if r.lower() not in text]
    behavior_missing = _behavior_checks(answer, qa)
    covered = len(required) - len(missing)
    score = covered / len(required)
    if behavior_missing:
        score = min(score, max(0.0, 1.0 - (len(behavior_missing) / max(1, len(required)))))
    all_missing = missing + behavior_missing
    return {
        "score": round(score, 4),
        "pass": score >= qa.get("pass_threshold", 0.5) and not behavior_missing,
        "rationale": f"covered {covered}/{len(required)}; missing={all_missing[:5]}",
        "missing": all_missing,
    }


# --- LLM judge ---------------------------------------------------------------


def judge_with_agent(qa: dict, answer: str, agent_id: str = "main",
                     model: str | None = None, timeout: int = 600,
                     container: str | None = None) -> dict:
    """Run a one-shot LLM judge via the openclaw CLI.

    The judge prompt asks for a JSON verdict: {"score": 0-1, "rationale": "..."}.
    Falls back to rule scoring if the CLI is unavailable.
    """
    rubric = qa.get("rubric") or "Score how well the answer matches the gold answer on a 0-1 scale."
    gold = qa.get("gold_answer")
    prompt = (
        "You are a strict benchmark judge. Read the QA, the reference answer, and the candidate. "
        "Reply with a single JSON object: {\"score\": <0..1>, \"rationale\": \"<one short sentence>\"}.\n\n"
        f"QA: {qa.get('question', '')}\n\n"
        f"REFERENCE: {json.dumps(gold, ensure_ascii=False) if gold else '(none)'}\n\n"
        f"RUBRIC: {rubric}\n\n"
        f"CANDIDATE:\n{(answer or '')[:8000]}\n"
    )

    openclaw_cmd = ["openclaw", "agent", "--agent", agent_id, "--message", prompt, "--json", "--local",
                    "--session-key", f"agent:{agent_id}:bench-judge-{os.getpid()}", "--timeout", str(timeout)]
    cmd = ["docker", "exec", "-i", container, *openclaw_cmd] if container else openclaw_cmd
    if model:
        cmd += ["--model", model]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 30)
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        # Fallback: degrade to rules so the report still has a score.
        fallback = judge_with_rules(answer, qa)
        fallback["rationale"] = f"agent judge unavailable ({e}); " + fallback["rationale"]
        return fallback

    text = (out.stdout or "") + "\n" + (out.stderr or "")
    m = re.search(r"\{.*?\"score\".*?\}", text, re.S)
    if not m:
        fallback = judge_with_rules(answer, qa)
        fallback["rationale"] = f"agent judge parse fail; " + fallback["rationale"]
        return fallback
    try:
        verdict = json.loads(m.group(0))
        score = float(verdict.get("score", 0.0))
    except (ValueError, TypeError):
        fallback = judge_with_rules(answer, qa)
        fallback["rationale"] = "agent judge JSON parse fail; " + fallback["rationale"]
        return fallback
    score = max(0.0, min(1.0, score))
    return {"score": round(score, 4),
            "pass": score >= qa.get("pass_threshold", 0.5),
            "rationale": str(verdict.get("rationale", ""))[:500]}


# --- Entry point for direct CLI use -----------------------------------------


def main() -> int:
    """CLI: `python3 judge.py rules|agent <qa.json> <answer.txt>` prints JSON verdict."""
    if len(sys.argv) != 4:
        print("usage: judge.py {rules|agent} <qa.json> <answer.txt>", file=sys.stderr)
        return 2
    mode, qa_path, ans_path = sys.argv[1], sys.argv[2], sys.argv[3]
    with open(qa_path, "r", encoding="utf-8") as f:
        qa = json.load(f)
    with open(ans_path, "r", encoding="utf-8") as f:
        answer = f.read()
    if mode == "rules":
        verdict = judge_with_rules(answer, qa)
    elif mode == "agent":
        verdict = judge_with_agent(qa, answer)
    else:
        print(f"unknown mode: {mode}", file=sys.stderr)
        return 2
    print(json.dumps(verdict, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
