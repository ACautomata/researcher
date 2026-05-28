# Idea Generate Skill Split Plan

## 当前 skill 列表

当前 workspace 只有一个专用 skill：

- `skills/idea-generate/`: 从论文和上下文生成结构化 research idea cards。

## 当前脚本职责

- `build_paper_context_pack.py`: 从 `paper/` 抽取文本和关键 snippets。
- `idea_dedup.py`: 对候选 idea 做近重复合并。
- `validate_idea_cards.py`: 检查 idea card 必填字段和基本质量门槛。
- `write_idea_markdown.py`: 将 JSON idea cards 写成 `recommended-ideas.md`，并附带轻量的人类反馈提示。

## 重复逻辑识别

虽然当前只有一个 skill，但内部已经出现可共享边界：

- Brief schema: `SKILL.md`、`brief-template.md`、输出文档都会重复描述用户输入字段。
- Idea card schema: `idea-card-template.md`、`output-spec.md`、`validate_idea_cards.py`、`write_idea_markdown.py` 都依赖同一组字段。
- Evidence handling: paper context、paper analysis、idea evidence chain 都需要统一的 evidence anchor 表达。
- Context intake: OpenClaw workspace 中的 wiki、paper-review 输出、实验日志和用户偏好需要被压缩成可追溯的 context digest。
- Human feedback: 一轮输出后的保留、否决、偏好和新约束需要能进入第二轮排序或生成。
- Quality gate: hard rules、validation script、自测 benchmark 都需要复用同一套检查标准。
- Markdown export: benchmark report、recommended ideas、analysis artifact 都需要稳定的输出结构。

## 暂不立即拆分的原因

- 当前 agent 最小可运行单元仍是 idea generation。
- 提前拆成多个 skills 会增加 main agent 派发复杂度。
- 现阶段更重要的是先稳定输入输出、benchmark 和 validation。
- 反馈闭环先作为 workflow 规则和 Markdown artifact 支持，不引入独立自动 parser。

## 后续拆分目标

当出现第二个 idea 相关 skill 或重复逻辑继续扩大时，再拆出共享模块：

```text
workspace-idea-generate/
  skills/
    shared/
      brief-schema.md
      idea-card-schema.md
      evidence-anchor-rules.md
      quality-gates.md
      markdown-artifact-rules.md
    idea-generate/
      SKILL.md
      references/
      scripts/
```

## 共享模块职责

- `brief-schema.md`: 统一 brief 字段、缺失字段处理、假设标注。
- `idea-card-schema.md`: 统一 idea card 字段、字段含义、允许值。
- `evidence-anchor-rules.md`: 规定 evidence chain 如何引用 paper snippets、wiki、实验日志和代码位置。
- `quality-gates.md`: 统一 idea 质量检查、自测评价标准、validation 规则。
- `markdown-artifact-rules.md`: 统一最终 Markdown artifact 的结构和风格。

## 拆分解决的问题

- 避免 schema 在多个文件中漂移。
- 让 validation、benchmark 和 final export 使用同一套质量规则。
- 方便未来增加 `idea-evaluate`、`idea-to-experiment`、`idea-to-prd` 等 skill。
- 保持 subagent 高内聚，具体业务流程放 skill，共享稳定规则放 shared。
