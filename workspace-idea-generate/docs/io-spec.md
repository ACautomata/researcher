# Idea Generate Input and Output Spec

## 用户输入

Idea Generate 支持三档输入。

### 最小输入

- 研究主题或任务描述。
- 至少一篇论文、论文摘要、wiki 条目或相关笔记。

### 推荐输入

- `paper/` 目录下的论文文件，支持 `.pdf`、`.txt`、`.md`、`.markdown`、`.docx`。
- OpenClaw workspace 中与当前主题相关的 wiki 页面、paper-review 输出或已有分析。
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

### Stage 1: Brief 归一化与上下文摄取

输入：

- 用户自然语言需求。
- 可选 brief 文件。
- 可选 repo、wiki、paper-review 输出、实验记录、用户偏好。

输出：

- 归一化 `Idea Generation Brief`。
- 明确字段缺失和假设。
- 可选 `context-digest.md`，用于记录本轮实际读取的材料、关键证据、实验结果、失败现象、用户约束和假设。

原则：

- 不要求上游 workspace 输出固定 schema。
- 只读取当前任务相关的最小上下文。
- 优先使用用户明确指定的材料，其次读取本地论文、知识库、实验记录和代码约束。

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
- `context-digest.md`
- wiki、paper-review 输出或实验记录。
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
- `anchor_sources`
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
- `wiki_writeback`（当 `anchor_sources` 指向 wiki 论文/页面时必填；说明应回写到 wiki 的痛点、发现或结论）

字段约束：

- `anchor_sources` 必须列出 1 篇具体论文/wiki 页，或同一类型的 2–4 篇相关论文/wiki 页；不要写成泛泛领域名。
- `target_problem` 必须描述一个具体痛点：受影响的机制、数据集/指标/实验设定/适用边界，以及痛点如何从 anchor sources 中暴露出来。
- `mechanism` 必须是针对该痛点的解决思路，不能只是"引入更强模型"或"做更多实验"。

### Stage 5: Dedup and Validation

输入：

- `draft-ideas.json`

输出：

- `ideas.dedup.json`
- `validation.json`

要求：

- 合并重复 idea。
- 保留更具体、证据更强、实验更可控的版本。
- 如果两个 idea 只有泛化说法不同、痛点或 anchor sources 无法区分，应合并或删除较弱版本。
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
- Wiki writeback candidates（当 idea 锚定 wiki 论文时，列出 anchor sources、idea IDs、应回写的结论/发现）。
- Open questions or assumptions。
- Human feedback prompt。

### Stage 7: Human Feedback Refinement

输入：

- 上一轮 `recommended-ideas.md`。
- 上一轮 `ideas.dedup.json`。
- 用户自然语言反馈或 `human-feedback.md`。

输出：

- `recommended-ideas.v2.md` 或后续版本。

反馈可以包括：

- 保留某些 idea。
- 否决某些 idea 并说明原因。
- 新增偏好、风险等级、算力或实现约束。
- 要求围绕某个失败实验、指标短板或论文线索补充 idea。

要求：

- 不覆盖上一轮输出。
- 标明采用了哪些反馈。
- 被否决或降级的 idea 需要保留简短理由。
- 人类选择只改变优先级和方向，不代表 idea 已被验证成功。

## 失败与降级

- 无 `paper/` 目录：要求用户提供材料，或只生成 brief，不生成 ideas。
- PDF/DOCX 抽取失败：记录 unavailable extraction，不让流程静默失败。
- 证据不足：只允许生成 `low-confidence` ideas。
- 没有可用 metric：必须在 open questions 中标注，不得伪造指标。
- 没有代码上下文：implementation_scope 必须写成概念验证或伪代码级别。
- 没有结构化上游输出：继续从 Markdown、日志、表格或用户对话中提取上下文，不要求上游补 schema。
