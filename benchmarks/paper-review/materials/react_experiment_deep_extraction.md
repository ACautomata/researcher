# ReAct 实验深化提取

## 0. 文档定位

- **输入材料**：`materials/react_full.md`（ReAct 论文全文，arXiv 2210.03629，ICLR 2023，33页）
- **当前阶段**：S2 实验深化提取
- **包含**：实验目标、实验设置、主结果、消融实验、参数分析、效率代价、鲁棒性泛化性、实验现象、证据充分性
- **不包含**：完整问题挖掘、最终结论、方法改进方案（留待 S3/S4/S5）

---

## 1. 实验目标与作者想验证的核心结论

### 核心结论 1：Reasoning + Acting 协同优于纯 Reasoning 或纯 Acting

- **对应实验**：Table 1 (HotpotQA + Fever)、ALFWorld Table、WebShop 结果
- **证据**：ReAct 在两个 knowledge reasoning benchmark 上均优于 Act-only；在两个 decision making benchmark 上大幅超越 IL/RL 方法

### 核心结论 2：ReAct 显著减少 hallucination

- **对应实验**：Table 2（成功/失败模式分析）
- **证据**：CoT 的 hallucination 失败率 56%，ReAct 为 0%；CoT 的 false positive 率 14%，ReAct 为 6%

### 核心结论 3：ReAct + CoT-SC 组合最优

- **对应实验**：Table 1 (ReAct→CoT-SC, CoT-SC→ReAct)、Figure 2
- **证据**：HotpotQA 最佳方法 ReAct→CoT-SC (EM 35.1)；Fever 最佳方法 CoT-SC→ReAct (Acc 64.9)。两者仅需 3-5 个 CoT-SC sample 即达到 21-sample CoT-SC 的性能

### 核心结论 4：ReAct 在 finetuning 场景下 scaling 表现最优

- **对应实验**：Figure 3（scaling 结果）
- **证据**：PaLM-8B finetuned ReAct 超越所有 PaLM-62B prompting 方法；PaLM-62B finetuned ReAct 超越所有 540B prompting 方法

### 核心结论 5：稀疏 reasoning 对 interactive decision making 有效且必要

- **对应实验**：ALFWorld（ReAct vs Act vs ReAct-IM）、WebShop（ReAct vs Act vs IL vs IL+RL）
- **证据**：ALFWorld ReAct 71% vs Act 45%（best of 6）；WebShop ReAct 成功率 66.6% vs Act 55.6%，绝对提升 10% vs IL+RL

---

## 2. 实验设置总览

### 数据集

| 数据集 | 类型 | 规模 | 评估指标 | 来源 |
|--------|------|------|---------|------|
| HotpotQA | 多跳问答 | 7405 test (fullwiki setting) | EM | Yang et al., 2018 |
| Fever | 事实验证 | 6666 test | Accuracy | Thorne et al., 2018 |
| ALFWorld | 文本游戏（具身AI） | 134 unseen eval games, 6 task types | Success rate (%) | Shridhar et al., 2020b |
| WebShop | 网页导航（在线购物） | 500 test instructions, 1.18M products | Average score + Success rate (%) | Yao et al., 2022 |

### 任务划分

- HotpotQA / Fever：使用标准 test set，从训练集随机选 6/3 个例子构建 in-context prompt
- ALFWorld：134 个 unseen evaluation games，task-specific setup（每种任务类型独立评估）
- WebShop：500 test instructions，标准 test split

### Baseline 方法

| 方法 | 类型 | 适用 benchmark |
|------|------|---------------|
| Standard prompting | 无 reasoning 无 action | HotpotQA, Fever |
| CoT (Wei et al., 2022) | Reasoning only | HotpotQA, Fever |
| CoT-SC (Wang et al., 2022a) | CoT + self-consistency (21 samples, temp=0.7) | HotpotQA, Fever |
| Act-only | Action only (类 WebGPT 风格) | HotpotQA, Fever, ALFWorld, WebShop |
| BUTLER (Shridhar et al., 2020b) | Imitation learning (10^5 expert trajectories/task) | ALFWorld |
| IL / IL+RL (Yao et al., 2022) | Imitation learning / IL + RL | WebShop |
| ReAct-IM | ReAct + Inner Monologue 风格 dense thought | ALFWorld (ablation) |

### 模型与推理配置

| 配置项 | 值 |
|--------|---|
| 基础模型 (prompting) | PaLM-540B |
| 基础模型 (finetuning) | PaLM-8B, PaLM-62B |
| 解码策略 | Greedy decoding (prompting) |
| CoT-SC 温度 | 0.7 |
| CoT-SC 采样数 | 21 (default), 3-5 (与 ReAct 组合时) |
| HotpotQA 最大步数 | 7 |
| Fever 最大步数 | 5 |
| ALFWorld prompt 构造 | 每种 task type 从 3 条 annotated trajectory 中选 2 条，6 permutations |
| WebShop prompt | 1-2 shot in-context examples |
| Finetuning 数据量 | 3,000 trajectories with correct answers (bootstrap from ReAct) |

### 外部工具

| Benchmark | 外部接口 | 说明 |
|-----------|---------|------|
| HotpotQA | Wikipedia API | 搜索 Wikipedia 并返回页面摘要 |
| Fever | Wikipedia API | 同上 |
| ALFWorld | 环境 text interface | 文本动作 + 文本观察 |
| WebShop | 网页环境 | 搜索、点击、选择选项、购买 |

---

## 3. 主结果提取

### HotpotQA + Fever (Table 1, PaLM-540B prompting)

| 方法 | HotpotQA EM | Fever Acc |
|------|------------|-----------|
| Standard | 27.1 | 51.1 |
| CoT | 28.9 | 56.3 |
| Act | 24.3 | 57.8 |
| ReAct | 27.4 | 60.9 |
| CoT-SC | 33.8 | 60.6 |
| ReAct → CoT-SC | **35.1** | 62.0 |
| CoT-SC → ReAct | 32.2 | **64.9** |

来源：Table 1, Page 5

**关键数字**：
- ReAct vs Act on HotpotQA: +3.1 EM (27.4 vs 24.3)
- ReAct vs Act on Fever: +3.1 Acc (60.9 vs 57.8)
- ReAct vs CoT on Fever: +4.6 Acc (60.9 vs 56.3)
- ReAct vs CoT on HotpotQA: -2.0 EM (27.4 vs 29.4) — ReAct 略逊
- ReAct→CoT-SC 仅需 3-5 samples 即匹配 CoT-SC 21-sample 性能

来源：Table 1, Figure 2, Page 5-6

### ALFWorld (6 task types, 134 unseen eval games)

| Method | Pick | Clean | Heat | Cool | Look | Pick 2 | All |
|--------|------|-------|------|------|------|--------|-----|
| Act (best of 6) | 88 | 42 | 74 | 67 | 72 | 41 | 45 |
| ReAct (avg) | 65 | 39 | 83 | 76 | 55 | 24 | 57 |
| ReAct (best of 6) | **92** | **58** | **96** | **86** | **78** | **41** | **71** |
| ReAct-IM (best of 6) | 62 | 68 | 87 | 57 | 39 | 33 | 53 |
| BUTLER (best of 8) | 33 | 26 | 70 | 76 | 17 | 22 | 37 |

来源：Table in Page 8

**关键数字**：
- ReAct (best of 6) All: 71% vs Act: 45% — 绝对提升 **26%**
- ReAct (best of 6) All: 71% vs BUTLER: 37% — 绝对提升 **34%**
- ReAct 仅用 2-shot prompting vs BUTLER 10^5 expert trajectories

### WebShop (500 test instructions)

| Method | Average Score | Success Rate |
|--------|--------------|--------------|
| IL | 50.9 | 19.5 |
| IL + RL | 62.3 | 42.0 |
| Act (1-shot) | 62.3 | 55.6 |
| ReAct (1-shot) | **66.6** | **57.7** |
| ReAct (2-shot) | **68.9** | **66.6** |

来源：Table in Page 9

**关键数字**：
- ReAct (2-shot) vs IL+RL: 绝对 success rate 提升 **24.6%**（66.6 vs 42.0）
- ReAct (2-shot) vs Act (1-shot): 绝对 success rate 提升 **11.0%**（66.6 vs 55.6）
- ReAct 仅用 1-2 shot prompting vs IL+RL 使用 1,012 human trajectories

---

## 4. 消融实验提取

### 消融 1：四路方法消融（Standard vs CoT vs Act vs ReAct）

- **消融内容**：系统性地从 ReAct trajectory 中移除 thought、action 或两者
- **测试变体**：
  - Standard：移除 thought + action + observation
  - CoT：仅保留 thought（reasoning only）
  - Act：仅保留 action + observation（acting only）
  - ReAct：完整的 thought + action + observation
- **揭示结果**：
  - HotpotQA：CoT (28.9) > ReAct (27.4) > Standard (27.1) > Act (24.3) — reasoning 贡献大于 acting
  - Fever：ReAct (60.9) > Act (57.8) > CoT (56.3) > Standard (51.1) — acting（检索外部知识）贡献大于 reasoning
  - 两个 benchmark 得出相反结论，说明 reasoning 和 acting 的价值取决于任务特征
- **来源**：Table 1, Section 3.3

### 消融 2：ReAct-IM（Inner Monologue 风格 dense thought）

- **消融内容**：将 ReAct 的稀疏 thought 替换为 Inner Monologue 风格的 dense thought
- **测试变体**：ReAct-IM — 每步 action 前都有一句 thought
- **揭示结果**：
  - ALFWorld All: ReAct (71%) vs ReAct-IM (53%) — 稀疏 thought 显著优于密集 thought（+18%）
  - 在某些 task 上 ReAct-IM 甚至不如 Act（如 Pick: 62 vs 88）
- **来源**：Section 4, ALFWorld table

### 消融 3：ReAct + CoT-SC 组合策略

- **消融内容**：两种组合方向
  - ReAct→CoT-SC：ReAct 在最大步数内失败 → fallback 到 CoT-SC
  - CoT-SC→ReAct：CoT-SC 多数答案置信度低（< n/2）→ fallback 到 ReAct
- **揭示结果**：
  - HotpotQA 上 ReAct→CoT-SC 最优（35.1）
  - Fever 上 CoT-SC→ReAct 最优（64.9）
  - 组合方法仅需 3-5 samples 即超越 CoT-SC 的 21-sample 性能
- **来源**：Table 1, Figure 2, Section 3.2

### 消融 4：Prompting vs Finetuning

- **消融内容**：对比 prompting ReAct 与 finetuning ReAct（3000 条 bootstrap trajectory）
- **测试变体**：4 methods × 3 model sizes (8B/62B/540B) × 2 learning paradigms
- **揭示结果**：
  - Prompting：小模型 (8B/62B) 上 ReAct 最差（难以从 in-context 学到 reasoning+acting）
  - Finetuning：ReAct 在所有模型规模下最优，PaLM-8B finetuned ReAct > PaLM-62B prompted 所有方法
- **来源**：Figure 3, Section 3.3

### 消融 5：Thought 密度对比

- **消融内容**：ALFWorld 上 sparse thought vs. dense thought (ReAct-IM)
- **揭示结果**：Sparse thought 显著优于 dense thought（All: 71% vs 53%），说明在交互式任务中推理应简洁、仅在关键决策点触发
- **来源**：Section 4, Appendix

---

## 5. 参数敏感性与稳定性分析

### 模型规模 Scaling (Figure 3)

| 模型规模 | 学习方法 | ReAct HotpotQA EM | 最佳 baseline |
|---------|---------|------------------|---------------|
| PaLM-8B | Prompting | ~10 (最低) | Standard ~15 |
| PaLM-8B | Finetuning | ~22 (最高) | Act ~20 |
| PaLM-62B | Prompting | ~18 | CoT ~23 |
| PaLM-62B | Finetuning | ~28 (最高) | Act ~25 |
| PaLM-540B | Prompting | 27.4 | CoT-SC 33.8 |

**观察**：ReAct 在 prompting 场景下小模型表现最差（需要同时学习 reasoning 和 acting），但在 finetuning 场景下 scaling 曲线最陡——从最差变为最优。

### CoT-SC 采样数敏感性 (Figure 2)

- 随 #CoT-SC samples 增加（1→21），所有方法性能提升
- ReAct + CoT-SC 组合方法在 3-5 samples 处即饱和
- CoT-SC 单独使用需要 21 samples 才能达到最佳性能

### ALFWorld Prompt 鲁棒性

- 每种 task type 使用 6 种不同 prompt permutation（从 3 条 trajectory 中选 2 条排列）
- ReAct (avg): 57%, ReAct (best of 6): 71% — 存在显著 prompt 方差（14% 差距）
- Act (avg): 论文未提供，Act (best of 6): 45%

**论文未提供**：Act 的 avg performance、多个 seed 的标准差

---

## 6. 效率、复杂度与资源代价

### 推理代价

| 维度 | 值 |
|------|---|
| HotpotQA 最大搜索步数 | 7 |
| Fever 最大搜索步数 | 5 |
| 每步操作 | 生成 thought → 生成 action → 等待 Wikipedia API 返回 observation |
| Wikipedia API 调用 | 每次 search action 触发一次 API 调用 |
| CoT-SC 额外开销 | 21 次采样 × 每次生成完整 CoT trajectory |

### 人工标注代价

| 标注项 | 数量 |
|--------|------|
| HotpotQA prompt trajectories | 6（从训练集随机选） |
| Fever prompt trajectories | 3（从训练集随机选） |
| ALFWorld prompt trajectories | 3 per task type × 6 types = 18 |
| WebShop prompt trajectories | 1-2 |
| Finetuning bootstrap data | 3,000 trajectories（ReAct 自动生成） |
| Success/failure mode analysis (Table 2) | 200 trajectories（人工标注） |

### 模型与计算

| 维度 | 值 |
|------|---|
| Prompting 模型 | PaLM-540B（通过 API） |
| Finetuning 模型 | PaLM-8B, PaLM-62B |
| ALFWorld 环境 | 每 task instance 可包含 50+ locations，50+ expert steps |
| WebShop 环境 | 1.18M 商品，12k 人工指令 |
| Finetuning 数据生成 | 使用 ReAct prompting 生成 3,000 条正确 trajectory → bootstrap finetuning |

### 论文未提供

- Wikipedia API 调用的具体延迟
- 单次 inference 的 token 消耗
- 端到端 wall-clock time
- GPU 显存 / 训练时间（finetuning 场景）

---

## 7. 鲁棒性、泛化性与补充实验

### 多领域泛化

ReAct 在 4 个完全不同类型的 benchmark 上测试：

| Benchmark | 领域 | 交互方式 |
|-----------|------|---------|
| HotpotQA | 多跳知识推理 | Wikipedia API |
| Fever | 事实验证 | Wikipedia API |
| ALFWorld | 具身 AI（文本） | 环境 text interface |
| WebShop | 电商网页导航 | 网页交互 |

4/4 benchmark 上 ReAct 均优于 Act-only baseline（或提供了组合最优方案）。

### 成功/失败模式分析 (Table 2)

对 HotpotQA 上 200 条 trajectory 的人工标注：

| 模式 | ReAct | CoT |
|------|-------|-----|
| **Success: True Positive** | 94% | 86% |
| **Success: False Positive** | 6% | 14% |
| **Failure: Reasoning Error** | 47% | 16% |
| **Failure: Search Result Error** | 23% | — |
| **Failure: Hallucination** | 0% | 56% |
| **Failure: Label Ambiguity** | 29% | 28% |

### 论文未提供

- Fever 上的 success/failure mode 分析（仅 HotpotQA）
- ALFWorld / WebShop 上的 error 分类
- 多 seed 运行的均值和方差
- 统计显著性检验（p-value, confidence interval）
- 不同 Wikipedia API 实现的影响分析
- 不同 LLM backbone（非 PaLM）上的结果

---

## 8. 值得关注的实验现象

### 现象 1：Reasoning 和 Acting 的相对价值是 task-dependent

HotpotQA 上 CoT (reasoning-only) 优于 ReAct，Fever 上 ReAct (reasoning+acting) 优于 CoT。说明两类能力在不同任务上的贡献权重不同：
- 需要结构化推理的任务（multihop QA）→ reasoning 更重要
- 需要外部事实检索的任务（fact verification）→ acting 更重要

**来源**：Table 1

### 现象 2：Finetuning 逆转了 ReAct 的 scaling 劣势

Prompting 场景下 ReAct 在 8B/62B 模型上是最差方法（难以从 few-shot 学到 reasoning+acting），但 finetuning 后 ReAct 在所有规模下都是最优。这说明 ReAct 的能力可以被学习，但 prompting 的 in-context learning 不足以传递这种复合技能。

**来源**：Figure 3

### 现象 3：稀疏 thought 显著优于密集 thought

ALFWorld 上 ReAct（稀疏 thought）vs ReAct-IM（每步都有 thought）：71% vs 53%。原因论文未对此现象提供解释。一种观察是密集 thought 可能干扰 action 生成或使 trajectory 过长导致模型迷失，但论文未做受控实验验证。这与直觉（越多 reasoning 越好）相反。

**来源**：Section 4, ALFWorld table

### 现象 4：搜索质量是 ReAct 的致命瓶颈

23% 的 ReAct 失败归因于 search result error——搜索返回空或不含有效信息。一旦搜索失败，模型很难恢复。这暴露了推理-行动循环对工具质量的强依赖。

**来源**：Table 2

### 现象 5：ReAct 的 reasoning error 显著高于 CoT（47% vs 16%）

ReAct 的 thought-action-observation 结构约束虽然增强了 factuality，但同时降低了推理灵活性——模型更容易陷入重复循环或推理错误。这是 factuality vs flexibility 的 trade-off。

**来源**：Table 2

### 现象 6：小样本 prompting 超越大量训练数据

ALFWorld：ReAct 2-shot (71%) vs BUTLER 10^5 expert trajectories (37%)
WebShop：ReAct 2-shot (66.6% SR) vs IL+RL 1,012 human trajectories (42.0% SR)

**来源**：Section 4

---

## 9. 证据充分性整理

### 支撑较充分的结论

| 结论 | 证据 | 充分性 |
|------|------|--------|
| ReAct > Act on all benchmarks | Table 1、ALFWorld table、WebShop table — 4/4 benchmark 一致 | **充分** |
| ReAct 减少 hallucination | Table 2 — 人工标注 200 trajectory，ReAct 0% vs CoT 56% | **较充分**（仅 HotpotQA，未在其他 benchmark 验证） |
| ReAct + CoT-SC 组合最优 | Figure 2、Table 1 — 两个 benchmark 上均验证 | **较充分**（仅 PaLM-540B） |
| Finetuning 逆转 scaling 劣势 | Figure 3 — 8B/62B/540B 三种规模 | **较充分**（仅 HotpotQA） |
| 稀疏 thought > 密集 thought | ALFWorld table — ReAct-IM ablation | **有限**（仅 ALFWorld 1 个 benchmark） |

### 支撑有限的结论

| 结论 | 局限 |
|------|------|
| ReAct 的通用性（跨 LLM） | 仅测试 PaLM 系列，未在 GPT、Claude 等模型上验证 |
| ReAct 的统计显著性 | 未报告多 seed 均值/方差、p-value、confidence interval |
| Thought 密度的最优策略 | 仅对比 sparse vs dense 两种极端，无中间配置扫描 |
| ReAct reasoning error 的根因 | 归因于"结构约束降低灵活性"，但未做受控实验验证 |
| Prompt 敏感性 | ALFWorld 6 permutations 间有显著方差（avg 57% vs best 71%），未系统分析 |

### 论文未提供的实验信息

- 多 seed 运行的均值和标准差
- 统计显著性检验
- 不同 LLM backbone 的结果（仅 PaLM 系列）
- 不同 Wikipedia API 实现/版本的对比
- ALFWorld / WebShop 的 error 分类分析
- 搜索失败后的恢复策略对比
- Thought 长度的敏感性分析
- Act-only baseline 的 avg performance（仅 best of 6）

---

## 10. 对后续问题发现最有价值的实验信息

### 可复现的实验设定

- HotpotQA fullwiki setting（标准 benchmark，公开可用）
- Fever test set（标准 benchmark，公开可用）
- ALFWorld 134 unseen eval games（公开环境）
- WebShop 500 test instructions（公开环境）
- Prompt 模板在 Appendix C（完整可复用）
- 代码开源：https://react-lm.github.io/

### 值得验证的问题

1. **Reasoning error (47%) 的根因**：是 thought 格式问题、action 干扰、还是 PaLM 特定行为？换模型后是否改善？
2. **稀疏 thought 的最优密度**：ALFWorld 上 sparse > dense，但最优稀疏度未确定——每 N 步一个 thought？仅在关键决策点？
3. **搜索失败的恢复**：23% 失败来自搜索噪声——加入 search reformulation 或 fallback retrieval 是否可改善？
4. **跨 LLM 泛化**：GPT-4/Claude 上的 ReAct 表现是否一致？PaLM 特定行为有多少？
5. **Prompt 敏感性量化**：ALFWorld avg 57% vs best 71%（14% gap）——需要系统测试 prompt engineering 的影响

### 最值得优先验证的 3 个问题

1. **Reasoning error root cause analysis**（影响最大，关系到方法鲁棒性）
2. **Cross-LLM generalization**（决定 ReAct 是否是通用范式）
3. **Search failure recovery**（23% 失败占比最高，直接改善空间大）

---

## 11. 一段简短总结

ReAct 在 4 个异构 benchmark（HotpotQA、Fever、ALFWorld、WebShop）上验证了 reasoning+acting 协同的有效性。核心实验发现：(1) ReAct 在所有 benchmark 上优于 Act-only，hallucination 从 56%（CoT）降至 0%；(2) ReAct+CoT-SC 组合以 3-5 samples 达到 21-sample CoT-SC 性能；(3) finetuning 后 ReAct 从最差变为最优（8B finetuned > 62B prompted）；(4) 稀疏 thought 显著优于密集 thought（+18% on ALFWorld）。证据充分性最强的结论是 ReAct > Act（4/4 benchmark 一致），但跨 LLM 泛化性、统计显著性、search failure recovery 和 reasoning error 根因等关键问题均未充分验证。代码开源可用，为基础实验复现和验证提供了有利条件。
