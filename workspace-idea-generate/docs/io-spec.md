# Idea Generate Input and Output Spec

## 用户输入

Idea Generate 支持三档输入。

### 最小输入

- 研究主题或任务描述。
- 至少一篇论文、论文摘要、wiki 条目或相关笔记。

### 推荐输入

- `paper/` 目录下的论文文件，支持 `.pdf`、`.txt`、`.md`、`.markdown`、`.docx`。
- 当前 baseline 描述。
- 可用数据集和评价指标。
- 可用代码或仓库路径。
- 已知失败实验或现象。
- 计算资源和时间约束。

### 高质量输入

- 多篇同方向论文。
- 已整理 wiki 页面。
- 实验日志或失败记录。
- 当前方法的 ablation 结果。
- 明确的目标会议、论文方向或研究偏好。

## 处理流程

### Stage 1: Brief 归一化

输入：

- 用户自然语言需求。
- 可选 brief 文件。
- 可选 repo、wiki、实验记录。

输出：

- 归一化 `Idea Generation Brief`。
- 明确字段缺失和假设。

### Stage 2: Paper Context 构建

输入：

- `paper/` 目录或用户提供的文本材料。

输出：

- `paper-context.json`
- `paper-context.md`

内容包括：

- 论文列表。
- 标题或可识别来源。
- 抽取字符数。
- abstract、method、experiment、limitation、future work 等 snippets。

### Stage 3: Evidence Analysis

输入：

- `paper-context.md`
- wiki 或实验记录。
- brief。

输出：

- `paper-analysis.md`

内容包括：

- paper-by-paper summary。
- cross-paper common findings。
- limitations、gaps、future-work signals。
- transferable insights。
- constraint notes。

### Stage 4: Candidate Idea Draft

输入：

- brief。
- paper-analysis。
- generation strategies。

输出：

- `draft-ideas.json`

每个 idea 必须包含：

- `idea_id`
- `title`
- `one_sentence_hypothesis`
- `target_problem`
- `mechanism`
- `paper_insight_or_limitation`
- `evidence_chain`
- `minimum_experiment`
- `expected_metric_change`
- `implementation_scope`
- `risks`
- `confidence`
- `recommendation_reason`

### Stage 5: Dedup and Validation

输入：

- `draft-ideas.json`

输出：

- `ideas.dedup.json`
- `validation.json`

要求：

- 合并重复 idea。
- 保留更具体、证据更强、实验更可控的版本。
- validation 失败时必须修正，而不是跳过。

### Stage 6: Markdown Export

输入：

- `ideas.dedup.json`
- `paper-context.json`
- `paper-analysis.md`

输出：

- `recommended-ideas.md`

结构：

- Brief topic and scope。
- Processed paper list。
- Paper-by-paper summary。
- Cross-paper summary。
- Main limitations or gaps。
- Recommended ideas ranked by priority。
- Open questions or assumptions。

## 失败与降级

- 无 `paper/` 目录：要求用户提供材料，或只生成 brief，不生成 ideas。
- PDF/DOCX 抽取失败：记录 unavailable extraction，不让流程静默失败。
- 证据不足：只允许生成 `low-confidence` ideas。
- 没有可用 metric：必须在 open questions 中标注，不得伪造指标。
- 没有代码上下文：implementation_scope 必须写成概念验证或伪代码级别。

