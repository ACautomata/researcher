# Self-Instruct 实验深化提取

## 0. 文档定位

- **输入材料**：`materials/self_instruct_full.md`（Self-Instruct 论文全文，arXiv 2212.10560，ACL 2023，23页）
- **当前阶段**：S2 实验深化提取
- **包含**：实验目标、实验设置、主结果、消融实验、参数分析、效率代价、鲁棒性泛化性、实验现象、证据充分性
- **不包含**：完整问题挖掘、最终结论、方法改进方案（留待 S3/S4/S5）

---

## 1. 实验目标与作者想验证的核心结论

### 核心结论 1：Self-Instruct 框架能显著提升 GPT3 的指令跟随能力

- **对应实验**：Table 3（SUPERNI 零样本评估）、Figure 6（252 条用户导向指令人工评估）
- **证据**：GPT3SELF-INST 在 SUPERNI 上 ROUGE-L 39.9，相比原始 GPT3（ROUGE-L 6.8）绝对提升 33.1%，几乎匹配 InstructGPT001（ROUGE-L 40.8）

### 核心结论 2：Self-Instruct 生成的数据在多样性上远超种子任务

- **对应实验**：Section 3.2（多样性分析）、Figure 3（动宾结构分布）、Figure 4（ROUGE-L 与种子任务重叠分布）
- **证据**：生成指令的 ROUGE-L 与种子指令的分布显示大量新指令与种子任务重叠很低；动宾结构分析表明仅有 14% 的指令落入前 20 种模式

### 核心结论 3：Self-Instruct 数据优于现有公开指令数据集

- **对应实验**：Figure 6（252 条用户导向指令人工评估）
- **证据**：GPT3SELF-INST 性能超过 GPT3+T0 Training 和 GPT3+SUPERNI Training；在 252 条人工评估集上仅比 InstructGPT001 低 5%

### 核心结论 4：Self-Instruct 数据大小与质量均影响最终性能

- **对应实验**：Section 4.5、Figure 7（数据规模和质量消融）
- **证据**：指令数量从 175 增长至 51200 时性能持续提升，在 16K 附近趋于饱和；使用 InstructGPT003 蒸馏输出后性能额外提升约 10%

### 核心结论 5：Self-Instruct 生成的实例存在一定噪声但仍有训练价值

- **对应实验**：Table 2（200 条随机采样人工质量评审）
- **证据**：指令有效率 92%，输入合适率 79%，输出正确率 58%，全部有效仅 54%；但错误实例仍提供格式和部分正确信号

---

## 2. 实验设置总览

### 数据集

| 数据集 | 类型 | 规模 | 评估指标 | 来源 |
|--------|------|------|---------|------|
| SUPERNI 评估集 | 多任务 NLP（119 个任务） | 119 tasks × 100 instances = 11,900 条 | ROUGE-L | Wang et al., 2022 |
| 252 用户导向指令 | 自建人工编写新颖任务 | 252 instructions × 1 instance | 4 级人工评分（A/B/C/D） | 作者子集编写 |

来源：Section 4.3、Section 4.4

### 任务划分

- **SUPERNI**（Experiment 1）：使用标准 zero-shot 评估设置，模型仅看到任务定义，无 in-context 示例。温度=0 确定性生成，无 stop sequences。来源：Section 4.3
- **用户导向指令**（Experiment 2）：作者子集编写 252 条涵盖邮件写作、社交媒体、生产力工具、娱乐、编程等领域的指令。两位作者作为评分者独立评分，评分以 4 级标准（A/B/C/D）进行，模型输出匿名排列。来源：Section 4.4、Appendix B

### Baseline 方法

| 方法 | 模型规模 | 训练数据 | 适用评估 |
|------|---------|---------|---------|
| GPT3（Vanilla） | 175B（davinci） | 仅预训练，无额外微调 | SUPERNI |
| T5-LM | 11B | 仅预训练，无额外微调 | SUPERNI |
| T0 | 11B | PromptSource 指令数据 | SUPERNI |
| Tk-INSTRUCT | 11B | SUPERNI 训练数据 | SUPERNI |
| InstructGPT001 | 175B | 私有用例数据 + 人工标注（RLHF） | SUPERNI、252 用户指令 |
| InstructGPT002 | 175B | 更大量数据和 PPO 算法 | 252 用户指令 |
| InstructGPT003 | 175B | 最先进版本 | 252 用户指令 |
| GPT3 + T0 Training | 175B | PromptSource（50K 实例） | SUPERNI、252 用户指令 |
| GPT3 + SUPERNI Training | 175B | SUPERNI 训练集（50K 实例） | SUPERNI、252 用户指令 |
| GPT3SELF-INST（Ours） | 175B | Self-Instruct 生成数据（52K 指令） | SUPERNI、252 用户指令 |
| GPT3SELF-INST + SUPERNI Training | 175B | Self-Instruct 数据 + SUPERNI 训练集 | SUPERNI |

来源：Section 4.1、Section 4.2

**关键比较设计说明**：SUPERNI 对比主要聚焦 text-davinci-001 版本，因为 001 最接近实验设置（监督微调+人工演示）；002/003 使用了更多数据或算法（如 PPO），难以公平比较。来源：Page 1 脚注 1

### 微调配置

| 配置项 | 值 |
|--------|---|
| 基础模型 | GPT3 "davinci" 引擎（175B） |
| 微调 API | OpenAI Fine-tuning API |
| Prompt 编码方式 | 多种模板混合（Task: 前缀 / Input: 前缀 / Output: 后缀 / 不同换行数） |
| Prompt Loss Weight | 0 |
| 训练轮数 | 2 |
| 超参数 | API 默认值 |

来源：Section 4.1、Section 2.3

### 数据生成配置

| 配置项 | 值 |
|--------|---|
| 种子任务数 | 175（25 分类 + 150 非分类） |
| 生成轮次 | 迭代式（每步采样 8 个任务，6 人工 + 2 模型生成） |
| 指令去重阈值 | ROUGE-L < 0.7 |
| 关键词过滤 | image, picture, graph 等 |
| 实例过滤 | 完全重复、同名但输出不同、过长/过短 |
| OpenAI API 成本 | 数据生成约 $600，微调约 $338 |

来源：Section 2.2、Section 3.1、Appendix A.2、Appendix A.3

### 外部工具与 API

| 用途 | 接口 | 说明 |
|------|------|------|
| 数据生成 | OpenAI GPT3 API（davinci 引擎） | $0.02/1000 tokens（2022 年 12 月定价） |
| 模型微调 | OpenAI Fine-tuning API | 按训练文件 token 数计费 |
| 语法解析 | Berkeley Neural Parser | 用于提取指令中的动宾结构（Section 3.2） |

来源：Appendix A.2、Section 3.2

---

## 3. 主结果提取

### SuperNI 零样本评估（Table 3，PaLM-540B 非 GPT3，此处为 GPT3 175B）

| 模型 | 参数量 | ROUGE-L |
|------|--------|---------|
| GPT3（Vanilla） | 175B | 6.8 |
| T5-LM | 11B | 25.7 |
| **Instruction-tuned w/o SUPERNI** | | |
| T0 | 11B | 33.1 |
| GPT3 + T0 Training | 175B | 37.9 |
| **GPT3SELF-INST (Ours)** | **175B** | **39.9** |
| InstructGPT001 | 175B | 40.8 |
| **Instruction-tuned w/ SUPERNI** | | |
| Tk-INSTRUCT | 11B | 46.0 |
| GPT3 + SUPERNI Training | 175B | 49.5 |
| **GPT3SELF-INST + SUPERNI Training (Ours)** | 175B | 51.6 |

来源：Table 3，Page 6

**关键数字**：
- GPT3SELF-INST vs GPT3：+33.1 绝对 ROUGE-L 提升（39.9 vs 6.8）——来源：Section 1、Page 1
- GPT3SELF-INST vs InstructGPT001：仅差 0.9 ROUGE-L（39.9 vs 40.8）——来源：Table 3
- GPT3SELF-INST vs T0（11B）：+6.8 ROUGE-L（39.9 vs 33.1）——来源：Table 3
- GPT3SELF-INST + SUPERNI Training vs GPT3 + SUPERNI Training：+2.1 ROUGE-L（51.6 vs 49.5）——来源：Table 3

### 252 条用户导向指令人工评估（Figure 6）

| 模型 | Rating A% | Rating A+B% | 关键发现 |
|------|-----------|-------------|---------|
| Vanilla GPT3 | 论文未提供精确 A% | 论文未提供精确 A+B% | 基本无法响应指令 |
| GPT3 + T0 Training | 论文未提供 | 论文未提供 | 低于 GPT3SELF-INST |
| GPT3 + SUPERNI Training | 论文未提供 | 论文未提供 | 低于 GPT3SELF-INST |
| **GPT3SELF-INST** | **论文未提供精确 A%** | **论文未提供精确 A+B%** | **超出其他公开数据集训练的模型** |
| InstructGPT001 | 论文未提供 | 论文未提供 | GPT3SELF-INST 仅差 5%（A+B 算有效时） |
| InstructGPT002 | 论文未提供 | 论文未提供 | 明显高于 GPT3SELF-INST |
| InstructGPT003 | 论文未提供 | 论文未提供 | 最高性能 |

来源：Figure 6，Page 7

**关键数字**：
- GPT3SELF-INST 在 252 条用户导向指令上优于 GPT3+T0 Training 和 GPT3+SUPERNI Training——来源：Section 4.4、Figure 6
- 如将 A+B 视为有效响应，GPT3SELF-INST 仅落后 InstructGPT001 约 5%——来源：Section 4.4、Page 7
- 验证者间一致性：Cohen's κ = 0.58（4 类评分）、0.75（A+B vs C+D 二分）、Spearman ρ = 0.81——来源：Appendix B.2、Page 19-20

### 生成数据统计（Table 1）

| 统计项 | 数值 |
|--------|------|
| 总指令数 | 52,445 |
| - 分类指令数 | 11,584 |
| - 非分类指令数 | 40,861 |
| 总实例数 | 82,439 |
| - 空输入实例数 | 35,878 |
| 平均指令长度 | 15.9 词 |
| 平均非空输入长度 | 12.7 词 |
| 平均输出长度 | 18.9 词 |

来源：Table 1，Page 4

---

## 4. 消融实验提取

### 消融 1：数据规模对性能的影响

- **消融内容**：从 Self-Instruct 生成数据中采样不同数量指令（175、约 800、约 6400、约 51200），微调 GPT3 后在 252 条用户导向指令集上评估
- **测试变体**：
  - 175（仅种子任务）
  - ~800
  - ~6,400
  - ~51,200
- **揭示结果**：
  - 175 条指令：31.0% 评为 A
  - ~800 条指令：36.9% 评为 A
  - ~6,400 条指令：43.7% 评为 A
  - ~51,200 条指令：44.4% 评为 A
  - 性能在 16K 附近趋于饱和
  - 在 SUPERNI 评估上饱和更早（约数百条指令即趋于平稳）
- **来源**：Figure 7、Section 4.5、Page 7-8

### 消融 2：数据质量提升（蒸馏）对性能的影响

- **消融内容**：使用 InstructGPT003 重新生成 Self-Instruct 实例的输出字段，训练 GPT3
- **测试变体**：
  - 原始 GPT3SELF-INST 数据
  - InstructGPT003 蒸馏输出数据
- **揭示结果**：
  - 蒸馏数据训练的模型评 A 比例约 54.4%
  - 相比原始数据最高约 44.4%，提升约 10%
- **来源**：Figure 7、Section 4.5、Page 8

### 消融 3：训练数据来源对比（Self-Instruct vs 公开指令数据集）

- **消融内容**：在 GPT3 上分别使用 Self-Instruct 数据、T0 数据（PromptSource）和 SUPERNI 数据进行微调
- **揭示结果**：GPT3SELF-INST 在 252 条用户导向指令上优于 GPT3+T0 Training 和 GPT3+SUPERNI Training（Figure 6）
- **来源**：Section 4.2、Section 4.4

### 消融 4：Self-Instruct + SUPERNI 联合训练

- **消融内容**：GPT3SELF-INST + SUPERNI Training vs GPT3 + SUPERNI Training
- **揭示结果**：联合训练带来额外 2.1 ROUGE-L 提升（51.6 vs 49.5），证明 Self-Instruct 数据是 SUPERNI 的补充数据
- **来源**：Table 3、Section 4.3

### 消融 5：训练轮数分析

- **消融内容**：未做正式轮数扫描。作者设定 2 个 epoch 以避免过拟合
- **揭示结果**：论文未提供多轮数的对比实验
- **来源**：Section 4.1、Appendix A.3

---

## 5. 参数敏感性与稳定性分析

### 数据生成超参数（Table 4）

| 实验阶段 | Temperature | Top_P | Frequency Penalty | Presence Penalty | Beam Size | Max Length |
|---------|-------------|-------|-------------------|------------------|-----------|------------|
| 生成指令 | 0.7 | 0.5 | 0 | 2 | 1 | 1024 |
| 识别分类任务 | 0 | 0 | 0 | 0 | 1 | 3 |
| 生成实例 | 0 | 0 | 0 | 1.5 | 1 | 300 |
| 评估模型 | 0 | 0 | 0 | 0 | 0 | 1024 |

来源：Table 4、Page 15

### 去重阈值

- ROUGE-L 阈值设为 **0.7**，新指令与池中已有指令相似度 >= 0.7 时丢弃
- 论文未提供阈值的敏感性扫描实验
- 来源：Section 2.2、Page 3

### 种子任务数量与构成

- 种子任务 **175** 个（25 分类 + 150 非分类）
- 论文未提供不同种子数量/比例的消融实验
- 来源：Section 2.2、Page 3

### In-Context 示例比例

- 每步采样 **8 个**任务：**6 个人工**种子 + **2 个**模型生成任务
- 论文未提供不同比例（如 8:0、4:4 等）的扫描实验
- 来源：Section 2.2、Page 3

### 论文未提供

- 不同 ROUGE-L 阈值（如 0.5、0.9）的对比
- 不同 Temperature（如 0.3、1.0）对生成多样性的影响
- 不同 Presence Penalty 值的扫描
- 不同 In-Context 示例数量的消融
- 不同种子任务数量的影响

---

## 6. 效率、复杂度与资源代价

### 数据生成代价

| 维度 | 值 |
|------|-----|
| API 总成本 | 约 $600（2022 年 12 月定价） |
| API 单价 | $0.02 / 1000 tokens（GPT3 "davinci" 引擎） |
| 生成指令数 | 52,445 |
| 生成实例数 | 82,439 |
| 迭代轮次 | 论文未指定具体轮次 |
| 生成最佳超参数 | 见 Table 4（指令生成：temp 0.7, Top_P 0.5, Presence Penalty 2） |

来源：Appendix A.2、Page 14-15

### 微调代价

| 维度 | 值 |
|------|-----|
| 微调成本 | 约 $338 |
| 微调轮数 | 2 epochs |
| Prompt Loss Weight | 0 |
| 模板多样性 | 多种 Instruction/Input/Output 编码方式混用 |
| 训练数据 | 52K 指令 + 82K 实例 |

来源：Appendix A.3、Page 14-15

### 人工标注代价

| 标注项 | 数量 | 说明 |
|--------|------|------|
| 种子任务编写 | 175 tasks（1 instruction + 1 instance each） | 作者及实验室成员编写 |
| 质量评审（Table 2） | 200 instructions × 1 instance | 1 位专家标注者（本文作者） |
| 252 条用户导向指令 | 252 instructions × 1 instance | 两位作者评分，独立标注 |
| 252 条评估评分 | 252 instructions × 多个模型 | 两位作者独立评分，模型匿名化 |

来源：Section 3.3、Section 4.4、Appendix B

### 论文未提供

- 单次 API 调用的平均 token 消耗
- 端到端数据生成时间（wall-clock time）
- 微调的 GPU 显存和训练时间
- 单次推理的延迟
- 不同微调超参数（如 learning rate、batch size）的对比
- OpenAI API 的具体优化器和参数更新细节

---

## 7. 鲁棒性、泛化性与补充实验

### 两套评估集覆盖不同类型的指令跟随

| 评估集 | 任务类型 | 规模 | 评估方式 | 特点 |
|--------|---------|------|---------|------|
| SUPERNI | 典型 NLP 任务（分类为主） | 119 tasks × 100 instances | 自动 ROUGE-L | 传统 NLP benchmark，指令风格统一 |
| 252 用户导向指令 | 用户导向实际应用 | 252 instructions × 1 instance | 人工 4 级评分 | 长/短指令、多样化格式（表格、代码、方程等） |

来源：Section 4.3、Section 4.4

### 生成数据多样性分析

**动宾结构分析（Figure 3）**：
- 52,445 条指令中 26,559 条（约 50.6%）包含"动词-直接名词宾语"结构
- 前 20 个高频动词及其前 4 个直接宾语仅占全部指令的 14%
- 最高频动词：write, give, find, create, make, describe 等
- 来源：Section 3.2、Figure 3、Page 5

**与种子任务重叠（Figure 4）**：
- 生成指令与其最相似种子指令间的 ROUGE-L 分布显示大量新指令与种子差异大
- 种子指令与 SUPERNI 的 ROUGE-L 均值为 0.21
- 种子指令与用户导向指令的 ROUGE-L 均值为 0.34
- 仅 1 条种子指令完全相同地出现在用户导向测试集中（"answer the following question"）
- 来源：Section 3.2、Figure 4、Appendix A.1、Figure 8

**长度分布（Figure 5）**：
- 指令长度集中于 10-20 词
- 非空输入长度集中于 5-15 词
- 输出长度集中于 5-15 词，右偏
- 来源：Figure 5、Page 5

### 数据质量评审（Table 2）

随机采样 200 条指令 × 1 实例的人工评审结果：

| 评审项 | 有效比例 |
|--------|---------|
| 指令描述了一个有效任务 | 92% |
| 输入适合该指令 | 79% |
| 输出是对指令和输入的正确/可接受响应 | 58% |
| 全部字段有效 | 54% |

来源：Table 2、Page 5

### 论文未提供的实验信息

- 不同 LLM backbone（非 GPT3 系列，如 T5、PaLM 等）上的 Self-Instruct 实验结果
- 多轮迭代生成的轮次数量消融
- 不同种子任务数量（如 50、500）的对比
- 不同去重策略（如 semantic similarity 替代 ROUGE-L）的消融
- 不同生成超参数对最终模型性能的影响
- 错误模式分类分析（如具体哪些类型的指令更容易出错）
- 多 seed 运行的均值/标准差
- 统计显著性检验

---

## 8. 值得关注的实验现象

### 现象 1：Self-Instruct 生成数据与典型 NLP 任务分布存在差异

动宾结构分析显示大量生成指令（如 "Write a letter from the perspective of a cat"）与传统 NLP 任务分布不同。在前 20 个高频动词-宾语对中，仅覆盖 14% 的指令，说明数据分布极其分散。这种现象在 SUPERNI 和用户导向指令的对比中尤为明显：SUPERNI 上 Self-Instruct 性能低于直接使用 SUPERNI 训练数据训练，但在用户导向指令上 Self-Instruct 显著优于。

**来源**：Figure 3、Figure 6、Section 4.3、Section 4.4

### 现象 2：数据规模饱和点因评估任务类型而异

在 252 条用户导向指令上性能约在 16K 指令处饱和，但在 SUPERNI 评估上远早（约数百条指令）。这说明生成数据与传统 NLP 任务差异大，SUPERNI 中的典型 NLP 任务从中获益有限。

**来源**：Section 4.5、Page 7-8

### 现象 3：蒸馏显著提升数据质量

使用 InstructGPT003 重新生成输出后，性能从约 44.4%（A 比例）提升至约 54.4%，提升约 10 个百分点。这说明 Self-Instruct 生成数据的最大瓶颈在于输出质量而非指令多样性。

**来源**：Figure 7、Section 4.5

### 现象 4：人工评估中即使评分 C 的响应也有参考价值

在 Table 9 中，评为 C 的响应虽然最终输出错误，但模型展示了大致的解题步骤和格式理解。例如一阶逻辑翻译任务中模型虽翻译错误，但结构上部分正确。这支持了论文的观点——即使含噪声的数据仍有训练价值。

**来源**：Table 9、Page 21

### 现象 5：输出正确率（58%）明显低于指令有效率和输入合适率

Table 2 显示指令有效率 92%，输入合适率 79%，但输出正确率仅 58%，全部字段有效仅 54%。输出的生成是最薄弱的环节，这与蒸馏实验（输出改进带来最大性能提升）一致。

**来源**：Table 2、Page 5

### 现象 6：GPT3 原始模型指令跟随基础能力极差

GPT3（Vanilla）在 SUPERNI 上仅 ROUGE-L 6.8，在 252 条用户导向指令上基本无有效响应（Figure 6）。这个基线极低，说明 175B 的 GPT3 即使经过大规模预训练也缺乏基本的指令跟随能力。

**来源**：Table 3（6.8 ROUGE-L）、Figure 6

### 现象 7：InstructGPT001 与 GPT3SELF-INST 性能接近但训练方式截然不同

InstructGPT001 使用私有用例数据 + 人工标注（RLHF），GPT3SELF-INST 完全使用模型自身生成的自监督数据，两者在 SUPERNI 上仅差 0.9 ROUGE-L（40.8 vs 39.9），在用户导向指令上仅差约 5%。这说明 Self-Instruct 可在大幅降低对人工标注依赖的同时接近商业化系统的性能。

**来源**：Table 3、Figure 6、Section 4.3、Section 4.4

---

## 9. 证据充分性整理

### 支撑较充分的结论

| 结论 | 证据 | 充分性 |
|------|------|--------|
| Self-Instruct 显著提升 GPT3 指令跟随能力 | Table 3——SUPERNI 上 ROUGE-L 6.8 → 39.9（+33.1%）；Figure 6——252 用户指令上远超原始 GPT3 | **充分** |
| Self-Instruct 数据比公开指令数据集更优 | Figure 6——GPT3SELF-INST > GPT3+T0 Training > GPT3+SUPERNI Training（用户导向指令） | **较充分**（仅在 252 条用户指令上验证） |
| 数据规模增加性能递增但趋于饱和 | Figure 7——175~51200 递增：31.0%→44.4%（A 比例），16K 后饱和 | **较充分**（仅单次实验，无多 seed 验证） |
| 数据质量蒸馏提升显著 | Figure 7——原始 44.4% vs 蒸馏 54.4%（A 比例），+10% | **较充分**（仅单次实验） |

### 支撑有限的结论

| 结论 | 局限 |
|------|------|
| Self-Instruct 的通用性（跨 LLM） | 仅测试 GPT3（davinci）系列，未在 T5、PaLM、LLaMA 等模型上验证 |
| 统计显著性 | 未报告多 seed 均值/方差、p-value、confidence interval |
| 去重阈值 0.7 的最优性 | 未做不同阈值消融 |
| 种子任务数量/多样性影响 | 仅使用 175 个种子，未做种子数量消融 |
| 迭代生成策略影响 | 未对比非迭代 vs 迭代生成，未报告迭代轮次 |
| 噪声数据的训练价值机制 | 论文推测噪声实例仍提供有用信号，但缺乏受控实验 |

### 论文未提供的实验信息

- 多 seed 运行的均值和标准差
- 统计显著性检验
- 不同 LLM backbone（非 GPT3）上的结果
- 不同种子任务数量/构成的消融
- 不同 ROUGE-L 去重阈值的比较
- 不同 Presence Penalty / Temperature 的系统扫描
- 非迭代式生成的对比实验
- 迭代轮次的消融
- 过滤/不过滤的对比实验
- 生成数据在更多 downstream benchmark（如 BIG-bench、MMLU）上的表现

---

## 10. 对后续问题发现最有价值的实验信息

### 可复现的实验设定

- SUPERNI zero-shot 评估设置（119 tasks × 100 instances，公开数据集）
- 252 条用户导向指令（公开于 GitHub 仓库）
- 种子任务 175 个（公开于 GitHub 仓库）
- 完整的 Prompt 模板（Table 5-8）
- 所有生成数据 52K 指令 + 82K 实例（公开于 GitHub 仓库）
- 代码开源：https://github.com/yizhongw/self-instruct
- OpenAI API 超参数细节（Table 4）

### 值得验证的问题

1. **Self-Instruct 的跨模型迁移性**：仅 GPT3 上验证，GPT3SELF-INST 数据能否提升其他模型（如 LLaMA、Mistral、T5）的指令跟随能力？
2. **种子任务数量和质量的影响**：175 个种子是否有最优数量？更多高质量种子是否进一步改善？
3. **去重阈值 ROUGE-L 0.7 的最优性**：更严格/宽松的阈值如何影响多样性和质量？
4. **迭代轮次的边际收益**：多轮迭代的收益是否递减？最佳轮次是多少？
5. **输出质量改善策略**：蒸馏带来了 10% 提升，是否有其他策略（如 self-consistency、re-ranking）能进一步改善输出？
6. **数据饱和的真实原因**：16K 后的饱和是数据多样性的天花板还是模型容量的限制？
7. **Self-Instruct 能否用于长文本/复杂推理任务**：论文生成数据以短文本为主，对复杂推理任务的有效性未知

### 最值得优先验证的 3 个问题

1. **跨模型迁移性**（影响最大，决定 Self-Instruct 是否是通用数据生成范式）
2. **输出质量改善路径**（输出正确率仅 58%，蒸馏后 +10%，尚有巨大改善空间）
3. **种子任务的设计原则**（175 个种子的选择是否最优，对下游影响多大）

---

## 11. 一段简短总结

Self-Instruct 在 GPT3 175B 模型上通过自生成指令数据的迭代式 Pipeline（175 种子 → 52K 指令 + 82K 实例），在 SUPERNI 上取得 ROUGE-L 39.9，相比原始 GPT3（6.8）绝对提升 33.1%，几乎匹配 InstructGPT001（40.8），仅差 5% 绝对性能。在 252 条人工评估的用户导向指令上，GPT3SELF-INST 超过使用 PromptSource 或 SUPERNI 公开指令数据训练的模型。数据规模消融（175→51,200 指令）显示性能在 16K 附近饱和；使用 InstructGPT003 蒸馏输出后性能再提升约 10%（44.4%→54.4% A 评比例）。证据充分性最强的结论是 Self-Instruct 提升 GPT3 指令跟随能力（SUPERNI +33.1% + 人工评估双验证），但跨模型泛化性、不同种子数量消融、去重阈值选择、迭代轮次影响等关键问题均未充分验证。数据和代码已全部开源，为复现和后续改进提供了有利条件。
