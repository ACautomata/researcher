# TOOLS.md - Local Notes

This workspace mainly uses the `idea-generate` skill workflow.

## Conventions

- Default paper input folder: `paper/`.
- Default generated run folder: `idea-runs/YYYYMMDD-HHMMSS-<topic-slug>/`.
- Final human-readable output: `recommended-ideas.md`.
- Preserve intermediate `paper-context.md`, `paper-analysis.md`, and JSON idea files inside the run folder.

## Workspace Skill

- `idea-generate`: extracts paper context, synthesizes opportunity buckets, deduplicates candidate idea cards, validates required fields, and writes recommended ideas to Markdown.

## Requirement Docs

- `docs/task-requirements.md`: maps the meeting task document to this workspace.
- `docs/progress-report.md`: PR-ready four-task progress overview.
- `docs/design-paradigm.md`: checklist plus harness design choice.
- `docs/io-spec.md`: user-facing input, processing stages, and outputs.
- `docs/skill-split.md`: current split decision and future shared module boundaries.

## Benchmark Docs

- `benchmarks/seed-qa.md`: manually written seed QA cases.
- `benchmarks/benchmark-spec.md`: expansion and scoring rules.
- `benchmarks/self-test-report-template.md`: PR self-test report format.
