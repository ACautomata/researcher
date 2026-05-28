# Interactive Refinement

Idea Generate should treat human review as part of the idea workflow. The first `recommended-ideas.md` is not the final decision; it is a review artifact that helps the user select, reject, or redirect ideas.

## Feedback Inputs

After reading `recommended-ideas.md`, the user may provide feedback in natural language or in a lightweight file such as `human-feedback.md`.

Recognized feedback types:

- keep selected ideas
- reject ideas with reasons
- prefer lower-cost, higher-risk, more theoretical, or more implementation-ready directions
- add or tighten constraints
- request more ideas from a specific evidence source or failure mode
- ask for a revised ranking

## Suggested Feedback File

```markdown
# Human Feedback

## Keep
- idea-002

## Reject
- idea-004: evidence is too weak

## Preferences
- prefer low-cost validation
- use existing experiment results first

## New Constraints
- do not require a new dataset
- only change scoring or loss

## Follow-up Request
Generate a revised recommendation list with two additional ideas based on failed experiments.
```

## Refinement Workflow

Use this workflow for a second pass:

1. Read the previous run directory.
2. Read `recommended-ideas.md`, `ideas.dedup.json`, and any user feedback.
3. Preserve kept ideas unless the user asks to rewrite them.
4. Demote or remove rejected ideas and record the reason.
5. Add new constraints and preferences to the brief or context digest.
6. Re-rank existing ideas or generate a small number of new candidates.
7. Write a new output file such as `recommended-ideas.v2.md`.

Do not overwrite the previous recommendation file. Do not claim that a human-selected idea is proven; selection only changes priority and direction.

## Output Expectations

The revised output should include:

- what feedback was applied
- which ideas were kept, removed, revised, or newly added
- the revised ranked ideas
- any remaining open questions

Keep the loop lightweight. This workspace should support user-guided iteration, not full autonomous experiment execution.
