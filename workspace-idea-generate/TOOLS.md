# TOOLS.md - Local Notes

This workspace mainly uses the `idea-generate` skill workflow.

## Conventions

- Default paper input folder: `paper/`.
- Default generated run folder: `idea-runs/YYYYMMDD-HHMMSS-<topic-slug>/`.
- Final human-readable output: `recommended-ideas.md`.
- Preserve intermediate `context-digest.md`, `paper-context.md`, `paper-analysis.md`, and JSON idea files inside the run folder.
- Follow-up outputs should use versioned names such as `recommended-ideas.v2.md` instead of overwriting the first recommendation file.

## Workspace Skill

- `idea-generate`: intakes OpenClaw workspace context, extracts paper context, synthesizes opportunity buckets, deduplicates candidate idea cards, validates required fields, supports human feedback refinement, and writes recommended ideas to Markdown.

## Requirement Docs

- `docs/task-requirements.md`: maps the meeting task document to this workspace.
- `docs/progress-report.md`: PR-ready four-task progress overview.
- `docs/design-paradigm.md`: checklist plus harness design choice.
- `docs/context-intake.md`: flexible OpenClaw workspace context intake rules.
- `docs/interactive-refinement.md`: human feedback and second-pass recommendation workflow.
- `docs/io-spec.md`: user-facing input, processing stages, and outputs.
- `docs/skill-split.md`: current split decision and future shared module boundaries.

## Benchmark Docs

- `../benchmarks/idea-generate/seed-qa.md`: manually written seed QA cases.
- `../benchmarks/idea-generate/benchmark-spec.md`: expansion and scoring rules.
- `../benchmarks/idea-generate/self-test-report-template.md`: PR self-test report format.
