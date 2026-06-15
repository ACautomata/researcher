#!/usr/bin/env python3
"""One-shot helper: convert benchmarks/paper-review/seed_qa.json -> qa.jsonl
(compliant with benchmarks/_common/qa_schema.json). If fle_qa.json exists
(from prepare_fle.py), its items are merged in so the Focus-Level Eval
quality-evaluation QA items are included in the benchmark run.

Re-runnable; outputs are deterministic. Run from repo root:
  python3 benchmarks/paper-review/build_qa.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SRC = ROOT / "benchmarks" / "paper-review" / "seed_qa.json"
FLE_SRC = ROOT / "benchmarks" / "paper-review" / "fle_qa.json"
DST = ROOT / "benchmarks" / "paper-review" / "qa.jsonl"
SHARD_SIZE = 5


def normalize_material_text(text: str) -> str:
    return (text or "").replace(
        "benchmark/materials/fle/",
        "benchmarks/paper-review/materials/fle/",
    )


def convert(item: dict) -> dict:
    sa = item.get("standard_answer") or item.get("gold_answer") or {}
    must = sa.get("must_contain") or []
    fields = sa.get("fields") or []
    must_not = sa.get("must_not_contain") or []
    vp = sa.get("violation_penalty")
    ga: dict = {
        "must_contain": must + fields,
        "fields": fields,
        "key_behavior": sa.get("key_behavior", ""),
    }
    if isinstance(vp, (int, float)):
        ga["violation_penalty"] = vp
    if must_not:
        ga["must_not_contain"] = must_not
        ga.setdefault("violation_penalty", 1)
    question = item.get("question", "")
    qa_id = item.get("id") or item.get("qa_id")
    if not qa_id:
        raise ValueError(f"QA item missing id/qa_id: {item!r}")
    task_type = item.get("capability") or item.get("task_type")
    return {
        "qa_id": qa_id,
        # CI invokes main; target_agent makes the benchmark directive force
        # delegation to paper-review. The runner scores the relayed final
        # Markdown answer directly.
        "agent": "main",
        "target_agent": "paper-review",
        "skill": item.get("skill"),
        "task_type": task_type,
        "input_material": normalize_material_text(item.get("input_material", "")),
        "question": question,
        "gold_answer": ga,
        "rubric": item.get("rubric") or sa.get("key_behavior", "Match the must_contain and key_behavior."),
        "rubric_dimensions": item.get("dimensions") or item.get("rubric_dimensions", []),
        "pass_threshold": 0.5,
        "judge": item.get("judge", "agent"),
        "weight": 1.0,
    }


def load_fle_items() -> list[dict]:
    """Load FLE QA items if the file exists. Returns validated items
    with fields normalized for qa.jsonl compatibility."""
    if not FLE_SRC.exists():
        print(f"[build_qa] {FLE_SRC} not found — run prepare_fle.py first to generate FLE QA items")
        return []

    try:
        items = json.loads(FLE_SRC.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"[build_qa] WARNING: {FLE_SRC} is invalid JSON ({e}), skipping", file=sys.stderr)
        return []

    if not isinstance(items, list):
        items = [items]

    # Normalize: FLE items are already in qa.jsonl format (from prepare_fle.py),
    # so just validate required fields exist.
    validated = []
    for item in items:
        if "qa_id" not in item or "question" not in item:
            print(f"[build_qa] WARNING: skipping FLE item missing qa_id/question", file=sys.stderr)
            continue
        item.setdefault("agent", "main")
        item.setdefault("pass_threshold", 0.5)
        item.setdefault("weight", 1.0)
        item["input_material"] = normalize_material_text(item.get("input_material", ""))
        validated.append(item)

    print(f"[build_qa] Loaded {len(validated)} Focus-Level Eval QA items from {FLE_SRC}")
    return validated


def main() -> int:
    # 1. Load seed QA
    seed_items = json.loads(SRC.read_text(encoding="utf-8"))
    seed_lines = [json.dumps(convert(i), ensure_ascii=False) for i in seed_items]
    print(f"[build_qa] {len(seed_lines)} seed QA items from {SRC}")

    # 2. Load FLE QA (if available)
    fle_items = load_fle_items()
    fle_lines = [json.dumps(item, ensure_ascii=False) for item in fle_items]

    # 3. Merge and write
    all_lines = seed_lines + fle_lines
    DST.write_text("\n".join(all_lines) + "\n", encoding="utf-8")
    print(f"[build_qa] wrote {DST} ({len(all_lines)} total QA items: "
          f"{len(seed_lines)} seed + {len(fle_lines)} FLE)")

    # CI/local shard runs use paper-review-1..N directories. Keep those
    # shard qa.jsonl files in lockstep with the first 24 seed QA items; FLE
    # items are intentionally excluded from these shards.
    for idx in range(0, len(seed_lines), SHARD_SIZE):
        shard_num = idx // SHARD_SIZE + 1
        shard_dir = ROOT / "benchmarks" / f"paper-review-{shard_num}"
        if not shard_dir.exists():
            continue
        shard_lines = seed_lines[idx:idx + SHARD_SIZE]
        (shard_dir / "qa.jsonl").write_text("\n".join(shard_lines) + "\n", encoding="utf-8")
        print(f"[build_qa] wrote {shard_dir / 'qa.jsonl'} ({len(shard_lines)} seed QA items)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
