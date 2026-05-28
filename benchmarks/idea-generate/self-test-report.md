# Idea Generate Self-Test Report

## Summary

- Test date: 2026-05-28
- Tested commit: local working tree on `feat-idea-generate-workspace`
- Agent version / branch: `workspace-idea-generate`
- Benchmark version: `benchmarks/idea-generate/seed-qa.md`
- Number of QA cases: 5
- Passed: 5
- Failed: 0
- Main conclusion: All seed QA cases passed. The workflow produced evidence-grounded, constraint-aware, testable idea recommendations across paper-only, code-constrained, failed-experiment, weak-evidence, and constraint-heavy cases.

## Environment

- Runtime: Codex sub-agent clean-session simulation
- Model: inherited current Codex model
- Clean session method: five independent sub-agents were spawned without parent context; each received only one QA case plus the benchmark scoring rubric.
- Notes: No repository files were edited by the sub-agents. Scores are rubric-based self-test results for seed QA behavior.

## Results

| QA ID | Task Type | Score | Pass/Fail | Main Issue |
| --- | --- | ---: | --- | --- |
| QA-001 | Paper-only | 12/12 | PASS | None |
| QA-002 | Paper plus code | 12/12 | PASS | None |
| QA-003 | Failed experiment driven | 12/12 | PASS | None |
| QA-004 | Weak evidence | 12/12 | PASS | None |
| QA-005 | Constraint-heavy | 12/12 | PASS | None |

## Failure Analysis

No failed seed QA cases.

## PR Notes

- Covered task types: paper-only idea generation, paper plus code constraints, failed experiment driven generation, weak evidence handling, and constraint-heavy generation.
- Known gaps: benchmark execution is still manual/sub-agent based; no automated `run_benchmark.py` or judge/report runner is implemented yet.
- Follow-up benchmark expansion: add cross-paper contradiction and transfer-driven cases after the initial workspace PR lands.
- Prompt or skill changes made after testing: none.
