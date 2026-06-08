#!/usr/bin/env python3
"""Validate idea card JSON for the paper demo."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


REQUIRED_FIELDS = [
    "idea_id",
    "title",
    "one_sentence_hypothesis",
    "anchor_sources",
    "target_problem",
    "mechanism",
    "paper_insight_or_limitation",
    "evidence_chain",
    "minimum_experiment",
    "expected_metric_change",
    "implementation_scope",
    "risks",
    "confidence",
    "recommendation_reason",
]


def is_empty(value: object) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, (list, tuple, dict)):
        return len(value) == 0
    return False


GENERIC_ANCHOR_TERMS = {
    "paper",
    "papers",
    "wiki",
    "literature",
    "related work",
    "survey",
    "domain",
    "field",
    "area",
    "federated learning literature",
    "related literature",
    "prior work",
}

GENERIC_ANCHOR_FRAGMENTS = (
    "literature",
    "related work",
    "prior work",
    "field",
    "domain",
    "area",
)

CONCRETE_ANCHOR_MARKERS = (
    "/",
    ".md",
    ".pdf",
    "arxiv",
    "doi",
    "http",
    "wiki/",
    "paper:",
    "title:",
)

PAPER_ID_RE = re.compile(r"^p\d{1,3}$", re.IGNORECASE)

CONCRETE_ANCHOR_WORDS = {"paper", "wiki", "arxiv", "doi", "title"}

CONCRETE_PROBLEM_MARKERS = (
    "mechanism",
    "module",
    "dataset",
    "metric",
    "baseline",
    "ablation",
    "setting",
    "split",
    "boundary",
    "failure",
    "limitation",
    "claim",
    "experiment",
    "benchmark",
    "evaluation",
    "noise",
    "robust",
    "泛化",
    "鲁棒",
    "基准",
    "指标",
    "数据集",
    "机制",
    "模块",
    "消融",
    "边界",
    "失败",
    "限制",
    "实验",
)


def anchor_items(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


def has_generic_anchor(anchors: list[str]) -> bool:
    for anchor in anchors:
        normalized = " ".join(anchor.lower().split())
        if normalized in GENERIC_ANCHOR_TERMS:
            return True
        if any(fragment in normalized for fragment in GENERIC_ANCHOR_FRAGMENTS) and not any(
            marker in normalized for marker in CONCRETE_ANCHOR_MARKERS
        ):
            return True
    return False


def looks_like_title(anchor: str) -> bool:
    words = [word for word in re.split(r"\W+", anchor.strip()) if word]
    if len(words) < 3:
        return False
    return not all(word.lower() in CONCRETE_ANCHOR_WORDS for word in words)


def is_concrete_anchor(anchor: str) -> bool:
    lowered = anchor.lower()
    return (
        PAPER_ID_RE.fullmatch(anchor.strip()) is not None
        or any(marker in lowered for marker in CONCRETE_ANCHOR_MARKERS)
        or looks_like_title(anchor)
    )


def has_concrete_anchor(anchors: list[str]) -> bool:
    return all(is_concrete_anchor(anchor) for anchor in anchors)


def describes_concrete_problem(text: str) -> bool:
    lowered = text.lower()
    return len(text) >= 30 and any(marker in lowered for marker in CONCRETE_PROBLEM_MARKERS)


def has_wiki_anchor(anchors: list[str]) -> bool:
    return any(
        "wiki" in anchor.lower()
        or anchor.lower().endswith(".md")
        or "/papers/" in anchor.lower()
        or "/domains/" in anchor.lower()
        for anchor in anchors
    )


def validate(ideas: list[dict]) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    for idx, idea in enumerate(ideas, 1):
        label = idea.get("idea_id") or f"idea[{idx}]"
        for field in REQUIRED_FIELDS:
            if field not in idea or is_empty(idea.get(field)):
                errors.append(f"{label}: missing required field `{field}`")
        evidence = idea.get("evidence_chain")
        confidence = str(idea.get("confidence", "")).lower()
        if is_empty(evidence) and "low" not in confidence:
            errors.append(f"{label}: missing evidence must be marked low-confidence")
        anchors = anchor_items(idea.get("anchor_sources"))
        if not anchors:
            errors.append(f"{label}: anchor_sources must name specific paper/wiki sources")
        if len(anchors) > 4:
            errors.append(f"{label}: anchor_sources must contain one source or a same-type cluster of 2-4 sources")
        if has_generic_anchor(anchors):
            errors.append(f"{label}: anchor_sources must not be generic domain labels")
        if anchors and not has_concrete_anchor(anchors):
            errors.append(f"{label}: anchor_sources must name concrete papers, wiki paths, URLs, arXiv IDs, or DOIs")
        if has_wiki_anchor(anchors) and is_empty(idea.get("wiki_writeback")):
            errors.append(f"{label}: wiki-anchored ideas must include wiki_writeback")
        target_problem = str(idea.get("target_problem", "")).strip()
        if not describes_concrete_problem(target_problem):
            errors.append(f"{label}: target_problem must describe a concrete mechanism/evaluation/limitation pain point")
        metric = idea.get("expected_metric_change")
        if is_empty(metric):
            errors.append(f"{label}: expected_metric_change must name at least one metric")
        if len(str(idea.get("minimum_experiment", ""))) < 20:
            warnings.append(f"{label}: minimum_experiment looks too short")
    return {
        "valid": not errors,
        "idea_count": len(ideas),
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: validate_idea_cards.py <ideas.json> <validation.json>", file=sys.stderr)
        return 2
    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    ideas = json.loads(input_path.read_text(encoding="utf-8-sig"))
    if not isinstance(ideas, list):
        print("Input must be a JSON array.", file=sys.stderr)
        return 2
    report = validate([idea for idea in ideas if isinstance(idea, dict)])
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print("valid" if report["valid"] else "invalid")
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
