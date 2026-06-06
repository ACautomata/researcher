#!/usr/bin/env python3
"""One-shot helper: convert benchmarks/paper-review/seed_qa.json -> qa.jsonl
(compliant with benchmarks/_common/qa_schema.json). Re-runnable; outputs are
deterministic. Run from repo root:
  python3 benchmarks/paper-review/build_qa.py
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SRC = ROOT / "benchmarks" / "paper-review" / "seed_qa.json"
DST = ROOT / "benchmarks" / "paper-review" / "qa.jsonl"


def convert(item: dict) -> dict:
    sa = item.get("standard_answer") or {}
    must = sa.get("must_contain") or []
    fields = sa.get("fields") or []
    must_not = sa.get("must_not_contain") or []
    vp = sa.get("violation_penalty")
    ga: dict = {
        "must_contain": must + fields,
        "fields": fields,
        "key_behavior": sa.get("key_behavior", ""),
    }
    if must_not:
        ga["must_not_contain"] = must_not
        ga["violation_penalty"] = vp if isinstance(vp, (int, float)) else 1
    return {
        "qa_id": item["id"],
        # CI policy: every benchmark calls only `main`. Sub-agent routing
        # is decided by main at runtime via `sessions_spawn`; no per-QA
        # `target_agent` field is allowed (see benchmarks/_common/qa_schema.json).
        "agent": "main",
        "skill": item.get("skill"),
        "task_type": item.get("capability"),
        "input_material": item.get("input_material", ""),
        "question": item.get("question", ""),
        "expected_artifacts": [f"workspace-paper-review/outputs/bench-<run>/{item['id']}.md"],
        "gold_answer": ga,
        "rubric": sa.get("key_behavior", "Match the must_contain and key_behavior."),
        "rubric_dimensions": item.get("dimensions", []),
        "pass_threshold": 0.5,
        "judge": "agent",
        "weight": 1.0,
    }


def main() -> int:
    items = json.loads(SRC.read_text(encoding="utf-8"))
    lines = [json.dumps(convert(i), ensure_ascii=False) for i in items]
    DST.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {DST} ({len(lines)} QA)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
