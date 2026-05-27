Review the changes in this pull request.

Read `.github/codex/pr-context.txt` for the PR title and body.

Use `git diff HEAD~1..HEAD` or `git log --oneline -10` to inspect the actual changes.

## Review criteria

1. **Correctness** — logic errors, off-by-one, wrong conditions, missing edge cases
2. **Security** — secrets in code, injection risks, unsafe deserialization
3. **Consistency** — matches existing patterns and conventions in the codebase
4. **Completeness** — no half-finished features, TODOs that block merging

## Output format

Write your review in this exact format:

```
### Review Summary
[Brief summary of the changes and your assessment]

### Findings
- [List any issues found, or "No issues found."]

VERDICT: APPROVE
```

or

```
### Review Summary
[Brief summary of the changes and issues]

### Findings
- [Each issue with file path and line reference]

### Required Changes
- [Specific, actionable changes the author must make]

VERDICT: REQUEST_CHANGES
```

**Important:** You MUST end with exactly `VERDICT: APPROVE` or `VERDICT: REQUEST_CHANGES`. Nothing else should follow the verdict line.
