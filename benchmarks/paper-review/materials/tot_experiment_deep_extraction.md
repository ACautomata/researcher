# ToT 实验深化提取

## 0. 文档定位

- **输入材料**：`materials/tot_full.md`（Tree of Thoughts 论文全文，arXiv 2305.10601，NeurIPS 2023，14页）
- **当前阶段**：S2 实验深化提取
- **包含**：实验目标、实验设置、主结果、消融实验、参数分析、效率代价、鲁棒性泛化性、实验现象、证据充分性
- **不包含**：完整问题挖掘、最终结论、方法改进方案（留待 S3/S4/S5）

---

## 1. 实验目标与作者想验证的核心结论

### 核心结论 1：ToT 在需要规划或搜索的复杂推理任务上显著优于 CoT 和 IO

- **对应实验**：Table 2（Game of 24）、Figure 5（Creative Writing）、Table 3（Mini Crosswords）
- **证据**：Game of 24 上 GPT-4 + CoT 仅 4% 成功率，ToT 达到 74%（18.5 倍提升）；Creative Writing 上 ToT 的 GPT-4 连贯性评分 7.56 高于 CoT 的 6.93 和 IO 的 6.19；Mini Crosswords 上 ToT 词级成功率 60% 远高于 IO 的 14% 和 CoT 的 15.6%

### 核心结论 2：ToT 通过探索多条推理路径、自我评估和前瞻/回溯实现全局最优决策

- **对应实验**：Figure 1（框架对比示意图）、Figure 2（Game of 24 的 thought 生成与评估）、Figure 4（Creative Writing 的 plan 投票）、Figure 6（Mini Crosswords 的 DFS 搜索）
- **证据**：三种任务上 ToT 均利用不同的 thought 分解、生成、评估和搜索策略，在每个任务上均优于单路径方法；消融实验显示 breadth（b=1→5 从 45% 提升至 74%）、pruning 和 backtracking 均有独立贡献

### 核心结论 3：ToT 是通用且模块化的框架，可适配不同任务特性

- **对应实验**：Table 1（三种任务配置概览）、Figure 2/4/6（不同 thought 生成和评估策略）
- **证据**：同一框架下，Game of 24 使用 3-step BFS + propose prompt + value evaluation（sure/maybe/impossible），Creative Writing 使用 2-step BFS + i.i.d. sampling + vote，Mini Crosswords 使用 10-step DFS + propose prompt + per-clue evaluation——三种不同配置均取得最优结果

### 核心结论 4：ToT 的节点效率显著高于独立采样的 best-of-k

- **对应实验**：Figure 3(a)（Game of 24 的 scale 分析）
- **证据**：ToT 访问同等数量节点时成功率远高于 IO/CoT 的 best-of-k 采样；ToT（b=5）使用约 5.5k 生成 tokens 即达 74%，而 best-of-100 CoT 使用 6.7k tokens 仅 49%

### 核心结论 5：ToT 在较弱语言模型上同样有效

- **对应实验**：Table 5（Game of 24 GPT-4 vs GPT-3.5）、Table 6（Creative Writing GPT-4 vs GPT-3.5）
- **证据**：GPT-3.5 + ToT 在 Creative Writing 上评分 6.62 超过 GPT-4 + IO（6.19）且接近 GPT-4 + CoT（6.93），验证 ToT 在较弱模型上同样带来提升

---

## 2. 实验设置总览

### 数据集

| 数据集 | 类型 | 规模 | 评估指标 | 来源 |
|--------|------|------|---------|------|
| Game of 24 | 数学推理（24点游戏） | 100 games（从1362道题中取标号901-1000的较难题） | 成功率（有效方程=24，每个数字恰好用一次） | 4nums.com |
| Creative Writing | 创意写作（4段结尾固定） | 100 inputs（每 input 4个随机句子） | GPT-4 zero-shot 1-10连贯性评分（5次平均）+ 人工对比 | randomwordgenerator.com |
| Mini Crosswords | 5×5填字游戏 | 20 games（从156道题中取标号1,6,...,91,96） | Letter/Word/Game 三级成功率 | GooBix |

### 任务划分

- **Game of 24**：使用 4nums.com 上全部 1362 道题，取按人类解题时间排序后较难的 901-1000 号共 100 题作为测试集（Section 4.1, Page 5）
- **Creative Writing**：从 randomwordgenerator.com 采样 100 组随机句子，每组 4 句作为段落结尾约束；无 groundtruth passage，依赖自动评分和人工评估（Section 4.2, Page 6）
- **Mini Crosswords**：从 GooBix 获取 156 道 5×5 填字游戏，取标号 1,6,11,...,91,96 共 20 题测试，标号 136,141,146,151,156 共 5 题用于 prompt 构建（Section 4.3, Page 7）

### Baseline 方法

| 方法 | 类型 | 适用任务 |
|------|------|---------|
| IO prompting | 标准输入输出提示 | Game of 24（5-shot）、Creative Writing（zero-shot）、Mini Crosswords（5-shot） |
| CoT prompting | 链式思维提示 | Game of 24（5-shot + 3 intermediate equations）、Creative Writing（zero-shot + brief plan）、Mini Crosswords（5-shot + intermediate words h1..5 then v1..5） |
| CoT-SC (k=100) | CoT + 自一致性采样 | Game of 24 |
| IO + Iterative Refine (k=10/5) | IO + 迭代修正 | Game of 24（k=10）、Creative Writing（k≤5） |
| Best of k sampling | 取 k 次采样中最好结果 | Game of 24（用于对比） |

### 模型与推理配置

| 配置项 | 值 |
|--------|---|
| 主实验模型 | GPT-4（Chat Completion mode） |
| 对比模型 | GPT-3.5-turbo（Appendix B.2） |
| 采样温度 | 0.7 |
| 实验时间 | 2023年5月5日-16日 |
| 各方法采样数 | IO/CoT: 100次（Game of 24）、10次（Creative Writing）、10次（Mini Crosswords） |

### ToT 配置（三种任务）

| 配置项 | Game of 24 | Creative Writing | Mini Crosswords |
|--------|-----------|-----------------|----------------|
| Thought 步数 | 3步（中间方程） | 1步（写作计划） | 5-10步（逐词填充，可变） |
| Thought 生成策略 | propose prompt（1-shot） | CoT-style i.i.d. sampling（zero-shot） | propose prompt（5次建议） |
| Thought 评估策略 | value evaluation（sure/maybe/impossible，每 thought 采样3次） | vote prompt（zero-shot，每步投票5次） | per-clue possibility evaluation + confidence sorting |
| 搜索算法 | BFS | BFS | DFS |
| Breadth limit b | 5 | 1 | 1 |
| 其他参数 | — | — | DFS step limit=100 |
| 最终输出 | BFS 最优路径 | 投票选出的最佳 passage | 最深探索状态 |

### 外部资源

- Game of 24：无需外部工具，仅 LM 推理
- Creative Writing：无需外部工具，仅 LM 生成
- Mini Crosswords：无需外部工具，仅 LM 推理

---

## 3. 主结果提取

### Game of 24（Table 2, Page 6）

| 方法 | 成功率 |
|------|--------|
| IO prompt | 7.3% |
| CoT prompt | 4.0% |
| CoT-SC (k=100) | 9.0% |
| **ToT (ours) (b=1)** | **45%** |
| **ToT (ours) (b=5)** | **74%** |
| IO + Refine (k=10) | 27% |
| IO (best of 100) | 33% |
| CoT (best of 100) | 49% |

来源：Table 2, Page 6

**关键数字**：
- ToT(b=5) vs CoT: +70%（74% vs 4%），绝对提升 70 个百分点
- ToT(b=5) vs CoT-SC(k=100): +65%（74% vs 9.0%）
- ToT(b=5) vs CoT (best of 100): +25%（74% vs 49%）
- ToT(b=1) 即超越所有纯采样方法（45% vs 33%/49%）

### Creative Writing（Figure 5, Page 7）

| 方法 | GPT-4 平均连贯性评分（1-10） |
|------|-----------------------------|
| IO | 6.19 |
| CoT | 6.93 |
| **ToT** | **7.56** |
| IO + refine | 7.67 |
| ToT + refine | 7.91 |

来源：Figure 5(a), Page 7

**人工对比结果**（Figure 5(b), Page 7）：
- ToT 优于 CoT：41/100 对
- CoT 优于 ToT：21/100 对
- 两者相似：38/100 对

来源：Figure 5(b), Page 7

**评分可靠性**：5 次评分标准差平均约 0.56，评分一致性较好（Section 4.2, Page 6）

### Mini Crosswords（Table 3, Page 8）

| 方法 | Letter 成功率 (%) | Word 成功率 (%) | Game 成功率 (%) |
|------|-----------------|----------------|----------------|
| IO | 38.7 | 14 | 0 |
| CoT | 40.6 | 15.6 | 1 |
| **ToT (ours)** | **78** | **60** | **20** |
| +best state（oracle） | 82.4 | 67.5 | 35 |
| -prune（无剪枝） | 65.4 | 41.5 | 5 |
| -backtrack（无回溯） | 54.6 | 20 | 5 |

来源：Table 3, Page 8

**关键数字**：
- ToT Word 成功率 vs IO: +46%（60% vs 14%）
- ToT Word 成功率 vs CoT: +44.4%（60% vs 15.6%）
- ToT 解决 4/20 局完整游戏（IO/CoT 分别 0/20 和 1/20）

### 补充任务结果（Table 4, Page 9, Appendix B.1）

| 方法 | GSM8K（100 random subset） | StrategyQA（100 random dev） |
|------|--------------------------|----------------------------|
| IO | 51 | 73 |
| CoT | 86 | 82 |
| **ToT (zero-shot)** | **90** | **83** |

来源：Table 4, Page 9

**关键观察**：在 GPT-4 + CoT 已表现很好的任务上，ToT 提升有限（GSM8K: +4, StrategyQA: +1）

---

## 4. 消融实验提取

### 消融 1：ToT Breadth（b=1 vs b=5）——Game of 24

- **消融内容**：改变 BFS 中每步保留的最优候选数 b
- **测试变体**：
  - b=1（每步只保留 1 个最优候选）
  - b=5（每步保留 5 个最优候选）
- **揭示结果**：
  - b=1: 45%
  - b=5: 74%
  - 增加 breadth 带来 29 个百分点的提升，说明多路径探索对 24 点任务至关重要
- **来源**：Table 2, Section 4.1, Page 6

### 消融 2：ToT 节点效率 vs. Best-of-k 采样效率（Figure 3(a)）

- **消融内容**：比较 ToT 的节点访问效率与 IO/CoT 独立采样的 best-of-k 曲线
- **揭示结果**：
  - ToT（b=1~5）的 success rate vs. 节点数曲线远陡于 IO/CoT（best of 1~100）的曲线
  - CoT best-of-100 使用约 6.7k tokens 达 49%，ToT 使用约 5.5k tokens 达 74%
  - 说明搜索（树结构探索）比独立采样（bandit）在节点效率上有本质优势
- **来源**：Figure 3(a), Page 6

### 消融 3：Error Analysis——CoT vs ToT 各步失败率（Figure 3(b)）

- **消融内容**：在 Game of 24 上分析 CoT 和 ToT 样本在哪一步失败
- **揭示结果**：
  - 约 60% 的 CoT 样本在第一步即失败（即前三个词如"4 + 9"）
  - ToT（b=5）在第一步探索多种可能，避免"左到右解码"的早期错误
  - 说明从左到右自回归解码在需要规划的推理任务上的根本局限性
- **来源**：Figure 3(b), Section 4.1, Page 6

### 消融 4：Mini Crosswords——Pruning 和 Backtracking 的贡献（Table 3）

- **消融内容**：在 Mini Crosswords 上分别移除 pruning 和 backtracking
- **测试变体**：
  - 完整 ToT（DFS + pruning + backtracking）
  - -prune：移除状态评估剪枝，允许探索所有分支
  - -backtrack：移除回溯的贪婪策略（类似 b=1 的 BFS，允许覆盖，最多 20 步）
- **揭示结果**：
  - 完整 ToT: Word 60%, Game 20%
  - -prune: Word 41.5%, Game 5%（-prune 下降显著）
  - -backtrack: Word 20%, Game 5%（-backtrack 下降更严重）
  - pruning 和 backtracking 各自都有重要贡献，backtracking 的贡献更大
- **来源**：Table 3, Section 4.3, Page 8

### 消融 5：Mini Crosswords——Oracle Best State vs. Heuristic Best State

- **消融内容**：比较从 DFS 搜索树中选择 heuristic 最佳状态 vs. oracle 最佳状态（已知问题答案）
- **揭示结果**：
  - Heuristic：Game 4/20（20%）
  - Oracle（+best state）：Game 7/20（35%）
  - 输出启发式可进一步改进（+3 局完整游戏）
- **来源**：Table 3, Section 4.3, Page 8

### 消融 6：GPT-4 vs GPT-3.5 对比（Table 5, Table 6）

**Game of 24（Table 5, Page 9）**：

| 方法 | GPT-4 | GPT-3.5 |
|------|-------|---------|
| IO | 7.3% | 6% |
| CoT | 4.0% | 3% |
| **ToT** | **74%** | **19%** |

来源：Table 5, Page 9

**Creative Writing（Table 6, Page 9）**：

| 方法 | GPT-4 | GPT-3.5 |
|------|-------|---------|
| IO | 6.19 | 4.47 |
| CoT | 6.93 | 5.16 |
| **ToT** | **7.56** | **6.62** |

来源：Table 6, Page 9

**揭示结果**：
- 两个任务上"ToT > CoT > IO"的顺序对 GPT-3.5 同样成立
- GPT-3.5 + ToT（Creative Writing 6.62）> GPT-4 + IO（6.19）≈ GPT-4 + CoT（6.93）
- Game of 24 上 GPT-3.5 的 ToT（19%）远低于 GPT-4（74%），差距巨大（-55%），且 GPT-3.5 需用 3-shot propose prompt（而 GPT-4 只需 1-shot）

### 消融 7：Generation vs Evaluation 瓶颈分析（Appendix B.2）

- **消融内容**：在 Game of 24 上交换 GPT-4 和 GPT-3.5 的 thought generation 和 state evaluation 角色
- **测试变体**：
  - GPT-4 generation + GPT-3.5 evaluation：64%
  - GPT-3.5 generation + GPT-4 evaluation：31%
  - 两者均 GPT-4：74%
- **揭示结果**：
  - thought generation 是瓶颈（64% vs 31%，generation 能力强时结果好得多）
  - 使用不同模型做 generation 和 evaluation 可在保持较好结果（64%）的同时降低成本
- **来源**：Appendix B.2, Page 11

### 消融 8：零样本 ToT 在新任务上的泛化

- **消融内容**：用简单零样本 ToT（类似 Creative Writing 的 plan→vote→write→vote 结构）在 GSM8K 和 StrategyQA 上测试
- **揭示结果**：
  - GSM8K: CoT 86 → ToT 90（+4）
  - StrategyQA: CoT 82 → ToT 83（+1）
  - 提升有限，因 GPT-4 + CoT 已在这些任务上表现很好
- **来源**：Appendix B.1, Table 4, Page 9

---

## 5. 参数敏感性与稳定性分析

### Thought 分解粒度

| 任务 | Thought 粒度 | 步数 | 是否可控？ |
|------|------------|------|-----------|
| Game of 24 | 一行中间方程（如"13-9=4"） | 3（固定） | 是——问题结构天然决定 |
| Creative Writing | 一段写作计划 | 1（仅中间 step） | 设计选择——1 步已足够 |
| Mini Crosswords | 一个词及其位置 | 5-10（可变） | 取决于搜索路径 |

来源：Table 1, Page 5

### Breadth Limit b 的敏感性

- Game of 24: b=1→45%, b=5→74%（+29%，显著）
- 论文未提供 b=2,3,4 的中间值扫描
- 论文未提供 b>5 的结果（受资源限制或已饱和）

### Thought Generation 策略选择

| 策略 | 适用场景 | 用法 |
|------|---------|------|
| i.i.d. sampling（CoT prompt） | Thought 空间丰富（如整段计划） | Creative Writing |
| Sequential propose（propose prompt） | Thought 空间受限（如单行方程、单个词） | Game of 24, Mini Crosswords |

来源：Section 3, Pages 3-4

### State Evaluation 策略选择

| 策略 | 方法 | 适用场景 |
|------|------|---------|
| 独立评估（value） | 给每个 state 打 sure/maybe/impossible（1-10 或分类） | Game of 24 |
| 投票选择（vote） | 对比多个 state 选出最佳 | Creative Writing |
| 混合策略 | 对剩余 clue 逐一评估可能性 + confidence 排序 | Mini Crosswords |

### 搜索算法选择

- **BFS**：Game of 24（depth=3, b=5）、Creative Writing（depth=2, b=1）
- **DFS**：Mini Crosswords（depth≤10, step limit=100）
- 论文未系统对比 BFS vs DFS 在同一任务上的表现
- 论文提及 A* 和 MCTS 可作未来工作，但未实验（Section 3, Page 4）

### 采样次数敏感性

#### Creative Writing 评分一致性
- 5 次 GPT-4 评分标准差平均约 0.56（Section 4.2, Page 6）
- 论文未提供评分分布或不同评分策略的对比

#### Game of 24 Value Evaluation 采样次数
- 每 thought 采样 3 次（Section 4.1, Page 5）
- 论文未提供 1/2/5 次采样的对比

#### Creative Writing Vote 采样次数
- 每步投票 5 次（Section 4.2, Page 6）
- 论文未提供不同 vote 次数的敏感性分析

### 温度参数

- 所有实验使用采样温度 0.7（Section 4, Page 5）
- 论文未提供不同温度的消融

### GPT-3.5 Prompt 适配

- Game of 24 上 GPT-3.5 的 propose prompt 从 1-shot 改为 3-shot（Appendix B.2, Page 11）
- 说明 GPT-3.5 的 thought generation 能力较弱，需要更多示例

### 论文未提供的参数分析

- Breadth 中间值（b=2,3,4）的扫描
- Temperature 消融
- Step limit 消融
- Vote/value 采样次数消融
- 不同 prompt 模板的影响
- 多 seed 均值和标准差

---

## 6. 效率、复杂度与资源代价

### Token 消耗与成本对比——Game of 24（Table 7, Page 11）

| 方法 | Generate/Prompt Tokens | Cost per case | 成功率 |
|------|----------------------|--------------|--------|
| IO (best of 100) | 1.8k / 1.0k | $0.13 | 33% |
| CoT (best of 100) | 6.7k / 2.2k | $0.47 | 49% |
| **ToT** | **5.5k / 1.4k** | **$0.74** | **74%** |

来源：Table 7, Page 11

**关键观察**：ToT 使用 5.5k 生成 tokens（接近 100 次 CoT 的 6.7k），但成功率达 74%（vs CoT 49%）。成本约 0.74/题，是为性能提升付出的额外代价。

### Token 消耗与成本对比——Creative Writing（Table 8, Page 11）

| 方法 | Generate/Prompt Tokens | Cost per case |
|------|----------------------|--------------|
| IO | 0.9k / 0.4k | $0.06 |
| CoT | 0.9k / 0.4k | $0.07 |
| **ToT** | **4k / 2.9k** | **$0.32** |

来源：Table 8, Page 11

**关键观察**：ToT 成本约为 IO/CoT 的 5 倍（$0.32 vs $0.06/$0.07），与 b=5 设计一致（5 个 plan × 5 个 passage）。

### 总实验成本（Appendix B.3, Page 11）

- Game of 24 主实验：$0.74 × 100 = ~$74
- Creative Writing 主实验：$0.32 × 100 = ~$32
- Crosswords DFS 实验：~$100 以内
- 总计：约 $206（论文原文写 Game of 24 + Creative Writing 约 $106，Crosswords 额外 ~$100）

### 相对计算开销

- ToT 比 CoT 多消耗 5-100 倍生成 tokens，取决于 prompt 和搜索算法（Appendix B.3, Page 11）
- BFS 可提前停止（找到解即终止）或缩减 beam size 来优化效率
- 开源 LM（如 LLaMA）有望降低此类成本（论文展望）

### 论文未提供的效率信息

- 单次推理的 wall-clock time
- 多线程/并行化对延迟的影响
- GPT-4 API 各实验的具体延迟分布
- 与 CoT-SC (k=100) 的时间对比（仅 token 数对比，未提时间）
- Mini Crosswords DFS 的 token 消耗和成本明细
- GPT-3.5 实验的成本对比

---

## 7. 鲁棒性、泛化性与补充实验

### 多领域泛化

ToT 在 3 个完全不同类型的任务上测试：

| 任务 | 能力要求 | 推理类型 |
|------|---------|---------|
| Game of 24 | 数学推理、算术计算 | 演绎推理、搜索 |
| Creative Writing | 创意写作、规划、语言生成 | 开放生成、规划 |
| Mini Crosswords | 词汇推理、约束满足 | 约束搜索、回溯 |

3/3 任务上 ToT 均显著优于 IO/CoT/CoT-SC 基线。

### 跨语言模型泛化（GPT-3.5）

- **Game of 24**：GPT-3.5 ToT 19% 远低于 GPT-4 的 74%（但"ToT > CoT > IO"顺序一致）
- **Creative Writing**：GPT-3.5 ToT 6.62 > GPT-4 IO（6.19）≈ GPT-4 CoT（6.93）
- 在较弱模型上 ToT 仍有效，但绝对性能取决于基础模型能力
- 来源：Appendix B.2, Tables 5, 6, Page 9

### 零样本 ToT 泛化到新任务

- **GSM8K**（100 随机子集）：CoT 86 → ToT 90（+4）
- **StrategyQA**（100 random dev）：CoT 82 → ToT 83（+1）
- ToT 可快速适配新任务（仅需定义 answer format 和 vote prompt）
- 来源：Appendix B.1, Table 4, Page 9

### Thought Generation 瓶颈分析

- Game of 24: GPT-4 gen + GPT-3.5 eval = 64%, GPT-3.5 gen + GPT-4 eval = 31%
- 瓶颈在 thought generation，而非 evaluation
- 可用混合模型策略在性能与成本之间折中
- 来源：Appendix B.2, Page 11

### 状态评估器的不完美性

- Mini Crosswords 中，即使游戏实际已解决，评估器仍可能将某些词判断为"impossible"而剪枝（Section 4.3, Page 8）
- 例如，GPT-4 将 "agend" 视为 "agenda" 的拼写错误，但实际 "agend" 是 "agendum" 的旧形式
- 无剪枝（-prune）变体可解 4/20 局游戏，其中 3 局是有剪枝版本无法在 100 步内求解的
- 说明更优的剪枝启发式对 DFS 至关重要

### 论文未提供的泛化性信息

- 非 GPT 系列模型（如 LLaMA、PaLM）上的 ToT 结果
- 多 seed 运行的均值和标准差
- 统计显著性检验
- 不同任务上 ToT 超参数的系统敏感度分析
- 更大规模任务（如 10×10 或标准尺寸填字游戏）上的测试
- 复杂编程或数据分析任务上的验证

---

## 8. 值得关注的实验现象

### 现象 1：ToT 在 Game of 24 上取得 18.5 倍于 CoT 的提升

- CoT 仅 4%，ToT(b=5) 达 74%，体现 ToT 对需要探索和规划的任务的巨大价值
- CoT 的"伪链式"推理（自回归 token 级生成）在需要全局规划的数学推理上几乎失效
- **来源**：Table 2, Page 6

### 现象 2：约 60% 的 CoT 样本在第一步即失败

- Game of 24 上 CoT 生成的前三个词（如 "4 + 9"）就已偏离正确方向
- 暴露了从左到右自回归解码在处理需要战略前瞻的推理任务时的根本局限
- **来源**：Figure 3(b), Section 4.1, Page 6

### 现象 3：ToT 的节点效率远高于独立采样

- Figure 3(a) 显示 ToT（b=1~5）的成功率-节点曲线远优于 IO/CoT 的 best-of-k 曲线
- 相同 token 预算下 ToT 获得显著更高的成功率
- 搜索（树结构探索）在节点效率上优于采样（bandit）
- **来源**：Figure 3(a), Page 6

### 现象 4：Thought Generation 是 Game of 24 的瓶颈而非 Evaluation

- GPT-4 gen + GPT-3.5 eval = 64%（接近 GPT-4 全栈的 74%）
- GPT-3.5 gen + GPT-4 eval = 31%（显著下降）
- 生成高质量候选 thought 比评估它们的质量更难
- 混合模型策略可在大幅降低成本的同时保持较好性能
- **来源**：Appendix B.2, Page 11

### 现象 5：ToT 在简单任务上收益递减

- GSM8K: CoT 86 → ToT 90（+4）
- StrategyQA: CoT 82 → ToT 83（+1）
- 当基模型配合 CoT 已很强时，ToT 的搜索增强收益有限
- StrategyQA 的瓶颈是外部知识而非推理，搜索无法弥补知识缺口
- **来源**：Table 4, Appendix B.1, Page 9

### 现象 6：Pruning 和 Backtracking 各自独立贡献，且 Backtracking 更重要

- 完整 ToT: Word 60%（Mini Crosswords）
- -prune: 41.5%（下降 18.5%）
- -backtrack: 20%（下降 40%）
- 无回溯的方法（贪婪填充）性能接近随机基线
- **来源**：Table 3, Section 4.3, Page 8

### 现象 7：即使游戏已解决，状态评估器仍误判

- 某些正确解被评估器标记为"impossible"而剪枝
- 原因是 5×5 填字游戏的设计包含罕见或旧式单词，GPT-4 无法识别
- 无剪枝版本能解出有剪枝版本无法求解的局
- 对知识不确定场景，外部检索或网页交互可能有助于改善评估
- **来源**：Section 4.3, Page 8

### 现象 8：人工评估一致性验证了自动评分的可靠性

- Creative Writing 的 GPT-4 自动评分与人工偏好一致
- 41/100 人工偏好 ToT > CoT，21/100 偏好 CoT > ToT
- 5 次 GPT-4 评分的标准差仅约 0.56
- **来源**：Figure 5(b), Section 4.2, Page 6-7

### 现象 9：GPT-3.5 + ToT 可超越 GPT-4 + IO/CoT

- Creative Writing 上 GPT-3.5 + ToT（6.62）> GPT-4 + IO（6.19）≈ GPT-4 + CoT（6.93）
- 表明搜索增强可部分弥补基础模型能力的差距
- **来源**：Table 6, Appendix B.2, Page 9

### 现象 10：Game of 24 上 GPT-3.5 需更多 shot 才能工作

- GPT-4 的 propose prompt 仅需 1-shot
- GPT-3.5 需要 3-shot 才能产生可用的 thought 建议
- 进一步印证 thought generation 是主要瓶颈
- **来源**：Appendix B.2, Page 11

---

## 9. 证据充分性整理

### 支撑较充分的结论

| 结论 | 证据 | 充分性 |
|------|------|--------|
| ToT >> CoT/IO 在需要规划/搜索的任务上 | Table 2（Game of 24: +70%）、Figure 5（Creative Writing: 多项证据）、Table 3（Mini Crosswords: +44.4% word-level）——三种异构任务一致 | **充分** |
| Breadth（多路径探索）贡献显著 | Table 2（b=1→45%, b=5→74%）、Figure 3(a)（节点效率曲线） | **较充分**（但未扫描 b=2,3,4） |
| Pruning 和 Backtracking 各自独立贡献 | Table 3（-prune: 41.5%, -backtrack: 20% vs full 60%） | **较充分**（仅 Mini Crosswords 一个 benchmark） |
| Thought Generation 是瓶颈 | Appendix B.2（gen-eval swap: 64% vs 31%） | **较充分**（仅 Game of 24 一个任务） |
| CoT 第一步失败率高 | Figure 3(b)（~60% CoT 第一步失败） | **较充分**（仅 Game of 24 分析） |

### 支撑有限的结论

| 结论 | 局限 |
|------|------|
| ToT 跨模型通用性 | 仅测试 GPT-4 和 GPT-3.5，未在 LLaMA、PaLM、Claude 等模型上验证 |
| ToT 统计显著性 | 未报告多 seed 均值/方差、p-value、confidence interval |
| 最优搜索算法的普适性 | BFS 和 DFS 分别在不同任务上测试，未在同一任务上系统对比 |
| 最优 thought 粒度的普适性 | 每种任务仅测试一种 thought 分解方案 |
| ToT 在真实应用上的有效性 | 仅测试 3 个人工构造的任务，未在编程、数据分析、机器人等真实场景验证 |
| 零样本 ToT 的通用性 | 仅测试 GSM8K 和 StrategyQA，且各取 100 子集 |

### 论文未提供的实验信息

- 多 seed 运行的均值和标准差
- 统计显著性检验
- Breakdown 参数扫描：b=2,3,4 / temperature / vote count / value sample count
- 不同 LM backbone（非 OpenAI）的系统性对比
- 更大规模任务（如标准填字游戏）的测试
- 不同 search algorithm（A*, MCTS）的对比实验
- 失败模式的 systematic error classification（仅 CoT vs ToT 的 step-level failure，非更细粒度的 error taxonomy）
- ToT 在编程、数学证明、代码生成等任务上的测试
- GPT-4 评分与人工评分之间的相关系数

---

## 10. 对后续问题发现最有价值的实验信息

### 可复现的实验设定

- **Game of 24**：4nums.com 1362 题中取 901-1000 号 100 题；IO 5-shot；CoT 5-shot + 3 中间方程；ToT BFS b=5；温度 0.7
- **Creative Writing**：randomwordgenerator.com 100 组输入（每组 4 句）；IO/CoT zero-shot；ToT 深度 2（plan→passage），k=5, b=1, vote 5 次
- **Mini Crosswords**：GooBix 156 题中取 1,6,...,91,96 共 20 题；IO 5-shot；CoT 5-shot + h1..5→v1..5 中间词；ToT DFS，step limit=100
- **GSM8K / StrategyQA**：各 100 random 子集；零样本 ToT（plan→vote→solution→vote）
- **代码与 Prompt**：https://github.com/princeton-nlp/tree-of-thought-llm（代码 + 完整 prompts + trajectories 均开源）

### 值得验证的问题

1. **Thought Generation 瓶颈的根因**：是 GPT-3.5 本身的生成能力弱，还是 propose prompt 设计问题？尝试更好的 prompt 或结构化输出是否能缩小差距？
2. **Breadth-深度权衡**：对给定任务，b 多大足够？是否存在饱和点？b 与问题复杂度、LM 能力的关系是什么？
3. **搜索算法选择**：BFS 与 DFS 在同一任务上的对比如何？是否 MCTS 或 A* 能带来进一步提升？
4. **状态评估器的校准**：Game of 24 的 sure/maybe/impossible 评为和 Mini Crosswords 的 per-clue 评估有多准确？评估错误对最终性能有多大影响？
5. **跨 LLM 泛化**：非 GPT 系列模型上的 ToT 行为是否一致？开源模型（LLaMA 等）的 scaling 规律？
6. **ToT 在真实场景的适用性**：编程、数据分析、事实性问答等真实决策任务上的表现？
7. **Cost-performance Pareto frontier**：不同任务上 ToT vs best-of-k 的 token 效率和成本曲线？

### 最值得优先验证的 3 个问题

1. **Thought generation bottleneck analysis**（关系 ToT 的方法论核心，决定搜索空间生成质量的关键因素）
2. **Cross-LLM generalization**（决定 ToT 是否是通用推理范式，非 GPT-4 specific）
3. **Search algorithm comparison（BFS vs DFS vs MCTS）**（直接关系到 ToT 框架的算法最佳实践和部署决策）

---

## 11. 一段简短总结

ToT 在 3 个异构挑战任务（Game of 24、Creative Writing、Mini Crosswords）上验证了将经典搜索方法（BFS/DFS）与 LM 的语义级 thought 生成和 self-evaluation 相结合的有效性。核心实验发现：(1) Game of 24 上 ToT(b=5) 74% 远超 CoT 4%，暴露了自回归解码在需要全局规划的任务上的根本局限；(2) ToT 的树结构节点效率显著高于独立采样（bandit）模式；(3) thought generation 是主要瓶颈（GPT-4 gen + GPT-3.5 eval = 64% vs 反向组合 31%）；(4) pruning 和 backtracking 各自独立贡献，backtracking 更重要（-backtrack 从 60% 降至 20%）；(5) GPT-3.5 + ToT 可超越 GPT-4 + IO/CoT，体现搜索增强可部分弥补模型能力差距。证据充分性最强的结论是 ToT >> CoT 在三种需规划/搜索的任务上（3/3 任务一致），但搜索算法对比、跨 LLM 泛化性、state evaluation 校准、任务实用性和统计显著性等关键问题均未充分验证。代码和 prompts 已全部开源，为可复现验证提供了有利条件。
