---
title: Research Paper Wiki Rearchitecture Proposal 2026-04-25
type: analysis
domain: meta
status: active
created: 2026-04-25
updated: 2026-04-25
tags:
  - schema
  - research-papers
  - wiki-architecture
source_pages:
  - wiki/domains/meta/sources/karpathy-llm-wiki.md
raw_sources:
  - raw/sources/2026-04-20-karpathy-llm-wiki.md
---

# Research Paper Wiki Rearchitecture Proposal 2026-04-25

## 问题

如果本仓库的主要用途是科研论文知识库，而不是通用 second brain，现有 LLM Wiki schema 应如何修改？

## 答案

当前 wiki 已经有有用的持久层：raw sources、source pages、concepts、topics、analyses、index 和 log。为了更适合科研论文，schema 应更 paper-native，把 papers、claims、methods、experiments、datasets、metrics、tasks 和 citation relationships 变成一等对象。

推荐方向：保留现有 domain 架构，但让每个研究 domain 以 `papers/` 为核心，并加入若干研究专用知识层。

## 建议结构

每个研究 domain 可以包含：

```text
wiki/domains/<domain>/
  papers/          # 每篇论文一个规范页面
  methods/         # 算法、模型设计、训练目标、procedure
  datasets/        # benchmark datasets、生成数据集、domain corpora
  tasks/           # problem settings 和 evaluation tasks
  metrics/         # AUROC、FPR95、top-1 accuracy、calibration error 等
  concepts/        # 更宽的理论概念和研究词汇
  topics/          # 演化中的研究线索综合
  comparisons/     # 方法族、benchmark、数据集/任务覆盖矩阵等
  reading-notes/   # 可选的临时读书笔记
  analyses/        # 可复用 memo、答案、综述和计划
```

迁移时保留旧 `sources/` 页面作为跳转页，避免历史链接断裂。

## Paper 页面模板

每篇论文页应捕捉：

1. 书目信息：title、authors、venue、year、arXiv/DOI、code、project page。
2. 分类信息：primary domain、research task、method family、supervision setting、modality、datasets、metrics。
3. 一句话贡献：最紧凑地表达论文 claim。
4. 问题设定：它解决什么假设、限制或 gap。
5. 方法：核心机制、训练信号、架构、目标函数和 inference procedure。
6. 实验：datasets、baselines、metrics、ablations、compute 或实现约束。
7. 结果：headline numbers 和 qualitative findings。
8. 限制：作者声明的限制和 wiki 推断的薄弱点。
9. 可复用 claims：可被 concept/topic/comparison 页引用的原子命题。
10. 连接：prior work、follow-up work、sibling methods、contradictory evidence。
11. 开放问题：需要从 PDF 正文、代码或后续论文验证的点。
12. 来源：raw PDF/text 路径和抽取 caveats。

## Frontmatter 变更

论文页应加入结构化字段，例如：

```yaml
---
title: Paper Title
type: paper
domain: distillation
status: seed | active | stable | superseded
created: YYYY-MM-DD
updated: YYYY-MM-DD
paper:
  title: Paper Title
  authors:
    - Author Name
  year: 2026
  venue: AAAI 2026
  arxiv: ""
  doi: ""
  code: ""
  project: ""
classification:
  label: distillation
  task:
    - dataset distillation
  method_family:
    - trajectory matching
  modality:
    - image
  datasets:
    - CIFAR-10
  metrics:
    - accuracy
evidence_level: abstract-only | skimmed | full-paper | reproduced
raw_sources:
  - raw/sources/example.pdf
related_pages:
  - wiki/domains/distillation/concepts/dataset-distillation.md
---
```

最重要的新增字段是 `evidence_level`，因为当前有些页面只基于摘要或有限 PDF 抽取。这个不确定性必须可见。

## 原子 Claims 层

topic、method、comparison 和 analysis 页面应在有用时积累原子 claims：

- 声明：短、可证伪的研究陈述。
- 证据：paper page 和 section/table/figure（如果已知）。
- 范围：dataset、modality、assumption 或 threat model。
- 置信度：low、medium、high。
- 张力：冲突论文或不可兼容的评估设置。

这会让 wiki 更适合写 related work、设计实验和发现矛盾。

## Comparison 页面

应添加 `comparisons/` 页面来保存可复用表格：

- method family comparisons；
- benchmark result tables；
- dataset/task coverage matrices；
- assumption and limitation matrices；
- chronological development maps。

例如 OOD detection 应有一个 `negative-prompt-ood-methods.md` comparison 页，区分 learned negative prompts、transferable negative prompts、baselines、datasets 和 metrics。

## Index 变化

`wiki/index.md` 应更研究导向：

- domain overview；
- open reading queue；
- paper pages by domain；
- methods by domain；
- datasets and metrics；
- comparison pages；
- high-value open questions。

这样 index 不会退化成文件清单。

## Ingest 工作流变化

论文 ingest 应分阶段：

1. 捕获 raw PDF/text 和 metadata。
2. 创建带 `evidence_level` 的 paper page。
3. 抽取结构化书目信息。
4. 填写 contribution、method、experiments、results、limitations 和 provenance。
5. 只在中心或高复用时创建/更新 method、task、dataset、metric 和 concept pages。
6. 给相关 topic 页添加 atomic claims。
7. 如果论文改变 method family 或 benchmark 状态，更新 comparison pages。
8. 更新 `wiki/index.md` 并追加 `wiki/log.md`。

## 迁移状态

- `AGENTS.md` 已改为论文优先 schema。
- 现有研究 domain 的论文页已从 legacy `sources/` 迁移到 canonical `papers/`。
- 旧 `sources/` 页面保留为 `superseded` 跳转页。
- `wiki/` 维护层已切换为默认中文呈现。

## 建议

保留现有 domain 架构，但把知识单元明确为“论文 + 可复用研究对象”。schema 应优化回答这些问题：

- 这篇论文到底贡献了什么？
- 它属于哪个 method family？
- 它使用了哪些 datasets 和 metrics？
- 哪些 claims 被支持、支持较弱或存在冲突？
- 它与邻近论文如何比较？
- 下一步应读什么或验证什么？

## 后续

下一步应为当前论文建立首批 `methods/`、`datasets/`、`tasks/`、`metrics/` 和 `comparisons/` 页面，尤其是 negative-prompt OOD comparison 和 dataset-distillation method family comparison。
