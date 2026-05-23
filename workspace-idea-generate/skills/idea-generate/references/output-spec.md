# Output Spec

Return:

1. one normalized Idea Generation Brief
2. one short evidence summary
3. 5-10 candidate Idea Cards
4. optional open questions

For each Idea Card:

- keep it concise
- include `paper_insight_or_limitation`
- include at least 2 evidence anchors when possible in `evidence_chain`
- include one `minimum_experiment`
- include at least one expected metric in `expected_metric_change`
- include one main `risks` entry
- include `recommendation_reason`

Prefer fewer high-signal cards over a longer list of weak ideas.

## Required Quality Checks

Before export, verify:

- every idea follows `idea-card-template.md`
- weak evidence is marked `low-confidence`
- every idea names a minimum validation experiment
- every idea names at least one metric
- every idea respects code, data, compute, and time constraints from the brief
- open questions are listed instead of silently filled in
