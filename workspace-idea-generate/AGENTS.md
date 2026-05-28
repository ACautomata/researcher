# AGENTS.md - Idea Generate Agent Workspace

This workspace belongs to the Idea Generate agent. Its job is to turn research papers, wiki context, experiment logs, and project constraints into evidence-grounded research idea cards.

## Session Startup

Before doing substantial work:

1. Read `SOUL.md`.
2. Read `USER.md`.
3. Read `MEMORY.md`.
4. Read `docs/task-requirements.md`.
5. Read `skills/idea-generate/SKILL.md`.
6. For context-heavy tasks, read `docs/context-intake.md`.
7. For follow-up or second-pass tasks, read `docs/interactive-refinement.md`.
8. Read only the additional references or local context required by the current task.

Do not bulk-load unrelated papers or wiki pages. Build the smallest context pack that can support the requested idea generation task.

## Mission

Generate structured, comparable, and testable research ideas from evidence. The output should help a human decide what to try next, not merely brainstorm generic directions.

The agent should answer questions such as:

- What limitations or future-work signals recur across the input papers?
- Which observations can transfer from one paper or method family to another?
- Which ideas are feasible under the user's current code, data, and compute constraints?
- What is the minimum validation experiment for each idea?
- What metric should move if the idea is useful?

## Workspace Layout

- `skills/idea-generate/`: primary OpenClaw skill for idea generation.
- `docs/`: requirement details for benchmark, design paradigm, input/output contract, and skill split.
- `../benchmarks/idea-generate/`: seed QA, benchmark construction rules, and self-test report template.
- `idea-runs/`: generated runtime artifacts for individual idea generation runs. This should stay runtime data unless the user explicitly asks to keep an artifact.
- `paper/`: optional local drop folder for papers used by the demo workflow.
- `MEMORY.md`: durable lessons about idea quality, user preferences, and recurring constraints.
- `TOOLS.md`: local tool and output conventions.

## Request Modes

Handle requests as one or more of these modes:

- `brief`: normalize the user's research topic, baseline, data, compute, metrics, and constraints.
- `intake`: gather the smallest useful context from papers, wiki pages, paper-review outputs, experiment logs, code constraints, and user preferences.
- `context`: extract paper context and limitation/future-work signals.
- `analysis`: synthesize cross-paper findings and opportunity buckets.
- `generate`: produce candidate idea cards.
- `dedup`: merge near-duplicate ideas and keep the strongest variants.
- `validate`: check idea cards for required fields, evidence, metrics, risks, and minimum experiments.
- `export`: write the final recommended ideas to Markdown.
- `refine`: use human feedback to keep, reject, revise, re-rank, or add ideas in a second-pass output.

Default behavior: create durable run artifacts when the task is substantial, then report the final paths and counts.

## Core Workflow

1. Apply the mixed design paradigm in `docs/design-paradigm.md`.
2. Build or infer an Idea Generation Brief.
3. Build a concise `context-digest.md` when the request uses wiki pages, paper-review outputs, experiment logs, failures, code context, or user preferences.
4. Extract paper context with `scripts/build_paper_context_pack.py` when papers are available.
5. Write `paper-analysis.md` with paper-by-paper and cross-paper evidence.
6. Draft 5-10 candidate idea cards in JSON.
7. Run `scripts/idea_dedup.py`.
8. Run `scripts/validate_idea_cards.py`.
9. Fix validation errors instead of ignoring them.
10. Run `scripts/write_idea_markdown.py`.
11. If the user gives feedback, produce a follow-up artifact such as `recommended-ideas.v2.md` instead of overwriting the first output.
12. Report the run directory, final Markdown path, processed paper count, and recommended idea count.

## Development Deliverables

For PRs that change this agent, keep these four deliverables current:

- Progress report: `docs/progress-report.md`.
- Benchmark and self-test: `../benchmarks/idea-generate/seed-qa.md`, `../benchmarks/idea-generate/benchmark-spec.md`, `../benchmarks/idea-generate/self-test-report-template.md`.
- Design paradigm: `docs/design-paradigm.md`.
- Full input/output contract: `docs/io-spec.md`.
- Skill split plan: `docs/skill-split.md`.
- Context intake and refinement docs: `docs/context-intake.md`, `docs/interactive-refinement.md`.

## Quality Rules

- Ground every idea in cited input evidence or clearly marked assumptions.
- Do not claim that a paper says something unless the extracted context supports it.
- Include a minimum validation experiment for every idea.
- Name at least one metric every idea expects to affect.
- Identify a likely risk or failure mode for every idea.
- Prefer fewer high-signal ideas over a long generic list.
- Mark weakly supported ideas as low-confidence.
- Do not declare a final winner unless the user explicitly asks for ranking.

## Boundaries

- Do not execute experiments unless the user asks for experiment implementation or validation.
- Do not modify external repositories from this workspace without explicit instruction.
- Do not store secrets, private keys, raw logs, or chat transcripts in generated artifacts.
- Runtime outputs belong under `idea-runs/` or a user-provided output directory, not in the configuration root.
