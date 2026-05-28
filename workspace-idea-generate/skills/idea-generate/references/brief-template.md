# Idea Generation Brief

Use this template to normalize the generation context before producing ideas.

```text
research_topic:
target_task:
current_baseline:
available_data:
available_code:
available_compute:
preferred_metrics:
hard_constraints:
known_failures:
desired_risk_level:
```

Fill unknown fields conservatively and label them as assumptions.

## Field Guidance

- `research_topic`: required unless it can be inferred from paper titles or user context.
- `target_task`: task setting, benchmark, dataset, or application scenario.
- `current_baseline`: current method, code baseline, or paper baseline to improve.
- `available_data`: datasets, splits, labels, data scale, and known caveats.
- `available_code`: repository path, framework, modules that can or cannot be changed.
- `available_compute`: GPU/CPU, time budget, experiment scale, network limits.
- `preferred_metrics`: metrics the idea should improve or monitor.
- `hard_constraints`: boundaries the generated ideas must obey.
- `known_failures`: failed experiments, negative results, or weak phenomena.
- `desired_risk_level`: low-risk, medium-risk, or exploratory.

If a field is missing but not blocking, write `ASSUMPTION:` and continue. Ask a follow-up only when there is no research topic, no evidence material, or an unresolved hard constraint.
