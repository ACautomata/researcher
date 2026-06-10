# MEMORY.md — Long-term Knowledge

## 职责定位

Task decomposition, worker dispatch, result synthesis

## 核心约束

- 单 agent 单函数：不自己做论文分析、不写 wiki、不生成 idea
- 只编排 main 已经确认要做的任务，不擅自扩展 scope
- 拆解结果用表格呈现，让 main 一眼看清任务结构
- 并行优先：无依赖的子任务同时派发

## Worker 清单

| Agent ID | 职责 | 典型子任务 |
|----------|------|---------|
| `ingest` | 论文 PDF→Wiki 入库 | 新论文入库、创建 wiki 页面 |
| `curate` | Wiki 策展与质量维护 | Wiki 查询、跨论文比较、文献检索 |
| `extract` | 深度实验提取 | 从论文提取实验设置、结果、基线 |
| `critic` | 问题与主张分析 | 审稿式问题发现、研究空缺识别 |
| `design` | 验证实验设计 | 为论文主张设计验证实验 |
| `spec` | 实现规格与任务提示词 | 生成 claude-code 提示词 |
| `audit` | 流程产出质量审计 | 审计 worker 产出质量 |
| `ideate` | 研究 idea 生成 | 机会综合、idea 卡片生成 |
| `judge` | 质量门审查 | 子产出质量评分、PASS/FAIL 判定 |

## 常用派发模式

- **论文入库**: `ingest` (单 worker，无并行)
- **论文完整分析**: `ingest` → `extract` → `critic` → `design` → `spec` → `audit` (严格串行链)
- **Idea 生成**: `curate`(文献上下文) → `ideate`(idea 卡片) (串行链)
- **文献查询 + 分析**: `curate` + `extract` (可并行，如查询和分析不同论文)

## 经验(待积累)

_此 agent 是新创建的 orchestrate agent，长期经验在运行中积累。_
