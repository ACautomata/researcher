# Paper-Review Benchmark 全量报告

**QA 总数**: 112 | **已跑**: 52 | **通过**: 21 | **失败**: 31 | **未跑**: 60
**跑过的通过率**: 21/52 (40%)  |  **已跑均分**: 0.376

## 按模块汇总

| 模块 | 含义 | 总数 | 已跑 | 通过 | 通过率 | 均分 |
|------|------|------|------|------|--------|------|
| S2     | 实验提取         |   22 |   13 |    3 | 3/13 (23%)     | 0.211  |
| S3     | 审稿分析         |   31 |   13 |    6 | 6/13 (46%)     | 0.393  |
| S4     | 验证设计         |   18 |    8 |    4 | 4/8 (50%)      | 0.417  |
| S5     | ClaudeCode提示词 |   16 |    6 |    3 | 3/6 (50%)      | 0.497  |
| S6     | Pipeline审计   |   12 |    5 |    2 | 2/5 (40%)      | 0.369  |
| Seed   | 种子(rules)    |    8 |    4 |    0 | 0/4 (0%)       | 0.138  |
| FLE    | FLE质量评估      |    5 |    3 |    3 | 3/3 (100%)     | 1.000  |

## 全量明细


### S2 实验提取（13/22 已跑，3 通过）

| QA ID | Target | Task Type | Score | 状态 |
|-------|--------|-----------|-------|------|
| s2-incomplete                    | paper-review | experiment-extraction          | 0.897 | ✅ |
| s2-nonstandard                   | paper-review | experiment-extraction          | 0.000 | ❌ |
| s2-toolformer                    | paper-review | experiment-extraction          | 0.000 | ❌ |
| s2-vpt                           | paper-review | experiment-extraction          | 0.000 | ❌ |
| s2-negative-missing-paper        | paper-review | negative-control               | -     | ⬜ |
| neg-nonexistent-material         | paper-review | negative-control-material      | -     | ⬜ |
| neg-truncated-input              | paper-review | negative-control-size          | -     | ⬜ |
| s2-selfrefine                    | paper-review | experiment-extraction          | 0.000 | ❌ |
| s2-tot                           | paper-review | experiment-extraction          | 0.962 | ✅ |
| s2-reflexion                     | paper-review | experiment-extraction          | 0.000 | ❌ |
| s2-tipadapter                    | paper-review | experiment-extraction          | 0.000 | ❌ |
| s2-adalora                       | paper-review | experiment-extraction          | 0.885 | ✅ |
| s2-autocot                       | paper-review | experiment-extraction          | -     | ⬜ |
| s2-tot-search                    | paper-review | experiment-extraction-variant  | 0.000 | ❌ |
| s2-reflexion-memory              | paper-review | experiment-extraction-variant  | 0.000 | ❌ |
| s2-selfrefine-feedback           | paper-review | experiment-extraction-variant  | -     | ⬜ |
| s2-vpt-design                    | paper-review | experiment-extraction-variant  | 0.000 | ❌ |
| s2-autocot-demo                  | paper-review | experiment-extraction-variant  | -     | ⬜ |
| s2-selfinstruct-data             | paper-review | experiment-extraction-variant  | -     | ⬜ |
| s2-autocot-wiki                  | paper-review | experiment-extraction          | 0.000 | ❌ |
| s2-reflexion-wiki                | paper-review | experiment-extraction          | -     | ⬜ |
| s2-selfinstruct-wiki             | paper-review | experiment-extraction          | -     | ⬜ |

### S3 审稿分析（13/31 已跑，6 通过）

| QA ID | Target | Task Type | Score | 状态 |
|-------|--------|-----------|-------|------|
| s3-cherrypick                    | paper-review | cherry-picking                 | 0.500 | ✅ |
| s3-baseline                      | paper-review | baseline-fairness              | 0.625 | ✅ |
| s3-competing                     | paper-review | competing-hypotheses           | 0.000 | ❌ |
| s3-dependency                    | paper-review | dependency-audit               | 0.500 | ✅ |
| s3-negative                      | paper-review | negative-balance               | 0.778 | ✅ |
| s3-tot-competing                 | paper-review | competing-hypotheses           | 0.000 | ❌ |
| s3-tot-scope                     | paper-review | scope-boundary                 | 0.667 | ✅ |
| s3-sr-dependency                 | paper-review | dependency-audit               | -     | ⬜ |
| s3-sr-negative                   | paper-review | negative-balance               | -     | ⬜ |
| s3-ta-competing                  | paper-review | competing-hypotheses           | -     | ⬜ |
| s3-ta-scope                      | paper-review | scope-boundary                 | -     | ⬜ |
| neg-instruction-hijack           | paper-review | negative-control-injection     | -     | ⬜ |
| s3-fedaux-scope                  | paper-review | scope-boundary                 | 0.333 | ❌ |
| s3-selfrefine-scope              | paper-review | scope-boundary                 | -     | ⬜ |
| s3-toolformer-scope              | paper-review | scope-boundary                 | -     | ⬜ |
| s3-reflexion-scope               | paper-review | scope-boundary                 | -     | ⬜ |
| s3-adalora-cherrypick            | paper-review | cherry-picking                 | 0.000 | ❌ |
| s3-vpt-cherrypick                | paper-review | cherry-picking                 | -     | ⬜ |
| s3-toolformer-cherrypick         | paper-review | cherry-picking                 | -     | ⬜ |
| s3-tot-negative                  | paper-review | negative-balance               | -     | ⬜ |
| s3-tipadapter-negative           | paper-review | negative-balance               | -     | ⬜ |
| s3-autocot-negative              | paper-review | negative-balance               | -     | ⬜ |
| s3-selfrefine-baseline           | paper-review | baseline-fairness              | 0.250 | ❌ |
| s3-reflexion-baseline            | paper-review | baseline-fairness              | -     | ⬜ |
| s3-tot-dependency                | paper-review | dependency-audit               | 0.000 | ❌ |
| s3-reflexion-dependency          | paper-review | dependency-audit               | -     | ⬜ |
| s3-adalora-competing             | paper-review | competing-hypotheses           | 0.455 | ❌ |
| s3-vpt-competing                 | paper-review | competing-hypotheses           | -     | ⬜ |
| s3-selfinstruct-competing        | paper-review | competing-hypotheses           | -     | ⬜ |
| s3-autocot-cherrypick            | paper-review | cherry-picking                 | -     | ⬜ |
| s3-selfinstruct-dependency       | paper-review | dependency-audit               | 1.000 | ✅ |

### S4 验证设计（8/18 已跑，4 通过）

| QA ID | Target | Task Type | Score | 状态 |
|-------|--------|-----------|-------|------|
| s4-budget                        | paper-review | validation-design              | 0.625 | ✅ |
| s4-minimal                       | paper-review | validation-design              | 0.500 | ✅ |
| s4-react-budget                  | paper-review | validation-design-budget       | 0.000 | ❌ |
| s4-adalora-budget                | paper-review | validation-design-budget       | 0.833 | ✅ |
| s4-tot-budget                    | paper-review | validation-design-budget       | 1.000 | ✅ |
| s4-vpt-budget                    | paper-review | validation-design-budget       | -     | ⬜ |
| s4-selfrefine-minimal            | paper-review | validation-design-minimal      | 0.375 | ❌ |
| s4-reflexion-minimal             | paper-review | validation-design-minimal      | -     | ⬜ |
| s4-tipadapter-minimal            | paper-review | validation-design-minimal      | -     | ⬜ |
| s4-toolformer-minimal            | paper-review | validation-design-minimal      | -     | ⬜ |
| s4-react-contradict              | paper-review | validation-design-contradiction | 0.000 | ❌ |
| s4-tot-contradict                | paper-review | validation-design-contradiction | -     | ⬜ |
| s4-neg-impossible                | paper-review | validation-design-negative     | 0.000 | ❌ |
| s4-neg-nocode                    | paper-review | validation-design-negative     | -     | ⬜ |
| s4-selfrefine-budget             | paper-review | validation-design-budget       | -     | ⬜ |
| s4-toolformer-budget             | paper-review | validation-design-budget       | -     | ⬜ |
| s4-autocot-budget                | paper-review | validation-design-budget       | -     | ⬜ |
| s4-selfinstruct-budget           | paper-review | validation-design-budget       | -     | ⬜ |

### S5 ClaudeCode提示词（6/16 已跑，3 通过）

| QA ID | Target | Task Type | Score | 状态 |
|-------|--------|-----------|-------|------|
| s5-norepo                        | paper-review | claude-code-generation         | -     | ⬜ |
| s5-largerepo                     | paper-review | claude-code-generation         | 0.000 | ❌ |
| s5-react-largerepo               | paper-review | claude-code-generation-largerepo | 1.000 | ✅ |
| s5-adalora-largerepo             | paper-review | claude-code-generation-largerepo | -     | ⬜ |
| s5-fedaux-norepo                 | paper-review | claude-code-generation-norepo  | 0.857 | ✅ |
| s5-selfinstruct-norepo           | paper-review | claude-code-generation-norepo  | -     | ⬜ |
| s5-tot-specific                  | paper-review | claude-code-generation-specific | 1.000 | ✅ |
| s5-toolformer-prioritize         | paper-review | claude-code-generation-prioritize | -     | ⬜ |
| s5-vpt-prioritize                | paper-review | claude-code-generation-prioritize | 0.125 | ❌ |
| s5-autocot-prioritize            | paper-review | claude-code-generation-prioritize | -     | ⬜ |
| s5-neg-injection                 | paper-review | claude-code-generation-negative | 0.000 | ❌ |
| s5-neg-oversized                 | paper-review | claude-code-generation-negative | -     | ⬜ |
| s5-reflexion-specific            | paper-review | claude-code-generation-specific | -     | ⬜ |
| s5-selfrefine-specific           | paper-review | claude-code-generation-specific | -     | ⬜ |
| s5-toolformer-specific           | paper-review | claude-code-generation-specific | -     | ⬜ |
| s5-autocot-specific              | paper-review | claude-code-generation-specific | -     | ⬜ |

### S6 Pipeline审计（5/12 已跑，2 通过）

| QA ID | Target | Task Type | Score | 状态 |
|-------|--------|-----------|-------|------|
| s6-boundary-new                  | paper-review | pipeline-audit                 | -     | ⬜ |
| s6-cross-new                     | paper-review | pipeline-audit                 | -     | ⬜ |
| s6-boundary-s3-s4                | paper-review | pipeline-audit-boundary        | -     | ⬜ |
| s6-boundary-s2-s3                | paper-review | pipeline-audit-boundary        | 0.846 | ✅ |
| s6-boundary-s4-s3                | paper-review | pipeline-audit-boundary        | 0.000 | ❌ |
| s6-cross-drift                   | paper-review | pipeline-audit-cross           | 0.455 | ❌ |
| s6-cross-orphan                  | paper-review | pipeline-audit-cross           | -     | ⬜ |
| s6-cross-priority                | paper-review | pipeline-audit-cross           | 0.545 | ✅ |
| s6-full-normal                   | paper-review | pipeline-audit-full            | 0.000 | ❌ |
| s6-full-contradict               | paper-review | pipeline-audit-full            | -     | ⬜ |
| s6-boundary-s5-s4                | paper-review | pipeline-audit-boundary        | -     | ⬜ |
| s6-boundary-s2-s4                | paper-review | pipeline-audit-boundary        | -     | ⬜ |

### Seed 种子(rules)（4/8 已跑，0 通过）

| QA ID | Target | Task Type | Score | 状态 |
|-------|--------|-----------|-------|------|
| seed-001                         | -       | wiki-extraction                | 0.079 | ❌ |
| seed-002                         | -       | experiment-extraction          | -     | ⬜ |
| seed-003                         | -       | problem-analysis               | 0.000 | ❌ |
| seed-004                         | -       | validation-design              | -     | ⬜ |
| seed-005                         | -       | claude-code-generation         | 0.000 | ❌ |
| seed-006                         | -       | missing-info                   | -     | ⬜ |
| seed-007                         | -       | stage-boundary                 | 0.474 | ❌ |
| seed-008                         | -       | fact-inference-distinction     | -     | ⬜ |

### FLE 质量评估（3/5 已跑，3 通过）

| QA ID | Target | Task Type | Score | 状态 |
|-------|--------|-----------|-------|------|
| fle-001                          | -       | s3-quality-fle                 | 1.000 | ✅ |
| fle-002                          | -       | s3-quality-fle                 | -     | ⬜ |
| fle-003                          | -       | s3-quality-fle                 | 1.000 | ✅ |
| fle-004                          | -       | s3-quality-fle                 | -     | ⬜ |
| fle-005                          | -       | s3-quality-fle                 | 1.000 | ✅ |