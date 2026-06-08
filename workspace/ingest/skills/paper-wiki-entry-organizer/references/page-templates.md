# 页面模板

Wiki 中各类型页面的推荐结构。

## 通用 Frontmatter 字段

每条持久 wiki 页面使用 YAML frontmatter，包含以下字段：

- **title** — 页面标题
- **type** — 页面类型（paper / method / dataset / task / metric / concept / entity / topic / comparison / analysis / reading-note）
- **domain** — 所属领域（必填）
- **status** — seed / active / stable / superseded
- **created** / **updated** — YYYY-MM-DD 格式
- **tags** — 标签列表，保持稀疏有意义
- **source_pages** — 支撑本页的论文页面路径
- **raw_sources** — 原始文件路径（论文页必填，其他类型可选）
- **related_pages** — 非证据性交叉链接（兄弟方法、任务、数据集、比较等）

更新 **updated** 字段当页面内容有实质性变更时。使用 **status: superseded** 代替删除。

## 论文页 Frontmatter

论文页额外包含：

- **paper.title** — 原始论文标题
- **paper.authors** — 作者列表
- **paper.year** — 发表年份
- **paper.venue** — 发表会议/期刊
- **paper.arxiv** / **paper.doi** / **paper.code** / **paper.project** — 链接标识符
- **classification.label** — 分类标签
- **classification.task** — 任务列表
- **classification.method_family** — 方法族
- **classification.modality** — 模态
- **classification.datasets** — 数据集
- **classification.metrics** — 评估指标
- **evidence_level** — abstract-only / skimmed / full-paper / reproduced

### Evidence Level 含义

- **abstract-only**：基于标题、摘要、公开元数据或有限提取
- **skimmed**：读了引言、方法、结果或部分章节
- **full-paper**：全文精读，足以支撑详细综合
- **reproduced**：通过代码、实验或独立计算验证了 claim

## 论文页结构

每篇论文页面推荐包含以下章节：

1. **Citation** — 引用信息
2. **One-Sentence Contribution** — 一句话贡献
3. **Problem Setting** — 问题设置
4. **Method** — 方法
5. **Experiments** — 实验设置
6. **Results** — 结果
7. **Limitations** — 局限性
8. **Reusable Claims** — 可复用的 claim
9. **Connections** — 关联
10. **Open Questions** — 开放问题
11. **Provenance** — 来源追溯

### Experiments 和 Results 最低标准

**Experiments** 必须包含：

- 每个使用的数据集及其大小和 train/test split
- 每个 baseline 方法名称
- 训练设置：模型架构、backbone、优化器、学习率、batch size、epoch 数、硬件
- 评估协议：指标、聚合方式（mean ± std over N runs）
- 消融实验：消融了什么、测试了什么变体、消融揭示了什么

**Results** 必须包含：

- 每个 main claim 至少一个具体数字（如 "AUROC 95.12% vs. MCM 86.05%"，不用 "显著优于 baseline"）
- 论文有表格时，捕获关键行：最佳方法、最强 baseline、差距
- 有消融实验时，捕获完整性能差值（如 "移除 L_reg 后 FPR95 从 8.56 升至 10.73"）
- evidence_level 为 skimmed 且完整结果不可用时，注明已有最佳数字和缺失内容

**反模式**：

- "持续优于 SOTA" 但不命名 SOTA 或差距
- "在多个 benchmark 上表现优越" 但不列 benchmark 或数字
- 列了数据集但不说哪个 baseline 在哪个数据集比较
- 空的或只有一句话的 Results 章节

## 方法页结构

1. **Definition** — 定义
2. **Core Mechanism** — 核心机制
3. **Assumptions** — 假设
4. **Evidence** — 证据
5. **Variants** — 变体
6. **Strengths and Weaknesses** — 优缺点
7. **Connections** — 关联
8. **Open Questions** — 开放问题

## 数据集页结构

1. **Description** — 描述
2. **Use Cases** — 使用场景
3. **Splits and Protocols** — 划分和协议
4. **Known Caveats** — 已知注意事项
5. **Papers Using It** — 使用该数据集的论文
6. **Connections** — 关联
7. **Open Questions** — 开放问题

## 任务页结构

1. **Definition** — 定义
2. **Evaluation Setup** — 评估设置
3. **Common Datasets** — 常用数据集
4. **Common Metrics** — 常用指标
5. **Representative Methods** — 代表方法
6. **Open Questions** — 开放问题

## 指标页结构

1. **Definition** — 定义
2. **Interpretation** — 解释
3. **Failure Modes** — 失败模式
4. **Used By** — 使用者
5. **Connections** — 关联
6. **Open Questions** — 开放问题

## 概念/实体页结构

1. **Definition** 或 **Description**
2. **Current Understanding** — 当前理解
3. **Evidence** — 证据
4. **Connections** — 关联
5. **Open Questions** — 开放问题

## 主题页结构

用于持续综合，不是一次性笔记。

1. **Current Thesis** — 当前论点
2. **Scope** — 范围
3. **Key Threads** — 关键线索
4. **Atomic Claims** — 原子 claim
5. **Evidence** — 证据
6. **Tensions** — 张力/矛盾
7. **Open Questions** — 开放问题

## 比较页结构

用于方法族、基准结果表、数据集/任务覆盖矩阵或时间线发展图。

1. **Question** — 问题
2. **Scope** — 范围
3. **Comparison Table** — 比较表
4. **Findings** — 发现
5. **Caveats** — 注意事项
6. **Evidence** — 证据
7. **Follow-up** — 后续

## 分析页结构

当查询产生可能被复用的洞察时创建。

1. **Question** — 问题
2. **Answer** 或 **Findings** — 答案/发现
3. **Evidence** — 证据
4. **Implications** — 含义
5. **Follow-up** — 后续

## Atomic Claims

主题、方法、比较和分析页面在有用时应积累 atomic claim。

推荐格式：

> **Claim**: 简洁的可证伪陈述
> **Evidence**: 引用论文页，注明 section/table/figure
> **Scope**: 数据集、模态、威胁模型、假设或实验设置
> **Confidence**: low / medium / high
> **Tensions**: 竞争或不兼容的证据（如有）

用 atomic claims 支撑文献综述、实验决策和矛盾追踪。不编造源材料不支持的精度。
