# Auto-CoT 实验深化提取

## 0. 文档定位

- **输入材料**：`materials/auto_cot_full.md`（Auto-CoT 论文全文，arXiv 2210.03493，25页）
- **作者**：Zhuosheng Zhang, Aston Zhang, Mu Li, Alex Smola（上海交通大学 + Amazon Web Services）
- **当前阶段**：S2 实验深化提取
- **包含**：实验目标、实验设置、主结果、消融实验、参数分析、效率代价、鲁棒性泛化性、实验现象、证据充分性
- **不包含**：完整问题挖掘、最终结论、方法改进方案（留待 S3/S4/S5）

---

## 1. 实验目标与作者想验证的核心结论

### 核心结论 1：Auto-CoT 在十项推理任务上一致匹配或超越 Manual-CoT 的性能

- **对应实验**：Table 3（10个数据集，GPT-3 text-davinci-002）、Table 4（Codex LLM，3个数据集）
- **证据**：在全部10个 benchmark 上，Auto-CoT 的准确率均等于或高于 Manual-CoT；在 MultiArith 上 92.0 vs 91.7，GSM8K 47.9 vs 46.9，AddSub 84.8 vs 81.3，Coin Flip 99.9 vs 97.2
- **来源**：Table 3, Page 8；Table 4, Page 8

### 核心结论 2：多样性（diversity-based clustering）能有效缓解 Zero-Shot-CoT 的 "misleading by similarity" 问题

- **对应实验**：Table 1（Retrieval-Q-CoT vs Random-Q-CoT vs Manual-CoT）、Figure 2（Unresolving Rate）、Figure 6（Effect of wrong demonstrations）
- **证据**：Retrieval-Q-CoT 在 MultiArith 上仅 82.8% 低于 Random-Q-CoT 的 86.2%；Retrieval-Q-CoT 的 unresolving rate（46.9%）远高于 Random-Q-CoT（25.8%）；Auto-CoT 在 50% 错误 demo 下性能仍不显著下降
- **来源**：Table 1, Page 4；Figure 2, Page 4；Figure 6, Page 9；Section 3.3, Page 5

### 核心结论 3：简单的启发式规则（短问题、短推理链、答案出现在推理中）能有效降低自动构建 demo 中的错误率

- **对应实验**：Table 9（平均错误 demo 数对比）、Figure 10（错误率对比）
- **证据**：使用启发式规则后，MultiArith 上平均错误 demo 从 1.3 降至 0.3，GSM8K 从 3.0 降至 1.7，10个任务中有 7 个任务的错误率降至 20% 以下
- **来源**：Table 9, Page 15；Figure 10, Page 16；Section C.2, Page 15

### 核心结论 4：聚类中心附近的 question 比边缘 question 更适合作为 demonstration

- **对应实验**：Table 8（三种排序策略对比）
- **证据**：MultiArith 上 In-Cluster Min Dist（距中心最近）93.7% vs In-Cluster Random 89.2% vs In-Cluster Max Dist 88.7%
- **来源**：Table 8, Page 15；Section C.1, Page 15

### 核心结论 5：Auto-CoT 在流式（streaming）场景下仍然有效

- **对应实验**：Figure 7（前10个 batch 的准确率）、Figure 11（全部20个 batch）
- **证据**：从 batch 2 开始，Auto-CoT* 的性能即与 Manual-CoT 相当
- **来源**：Figure 7, Page 9；Figure 11, Page 16；Section 5.6, Page 9

---

## 2. 实验设置总览

### 数据集

| 数据集 | 类型 | 样本数 | 平均词数 | 答案格式 | 协议 | 来源 |
|--------|------|--------|---------|---------|------|------|
| MultiArith | 算术推理 | 600 | 31.8 | Number | Unspecified | Roy and Roth, 2015 |
| GSM8K | 算术推理 | 1319 | 46.9 | Number | MIT License | Cobbe et al., 2021 |
| AddSub | 算术推理 | 395 | 31.5 | Number | Unspecified | Hosseini et al., 2014 |
| AQUA-RAT | 算术推理 | 254 | 51.9 | Multiple choice | Apache-2.0 | Ling et al., 2017 |
| SingleEq | 算术推理 | 508 | 27.4 | Number | No License | Koncel-Kedziorski et al., 2015 |
| SVAMP | 算术推理 | 1000 | 31.8 | Number | MIT License | Patel et al., 2021 |
| CSQA | 常识推理 | 1221 | 27.8 | Multiple choice | Unspecified | Talmor et al., 2019 |
| StrategyQA | 常识推理 | 2290 | 9.6 | Yes or No | Apache-2.0 | Geva et al., 2021 |
| Last Letters | 符号推理 | 500 | 15.0 | String | Unspecified | Wei et al., 2022a |
| Coin Flip | 符号推理 | 500 | 37.0 | Yes or No | Unspecified | Wei et al., 2022a |

来源：Table 7, Page 14；Section B.1, Pages 13-14

### Baseline 方法

| 方法 | 描述 | Prompt 结构 | 来源 |
|------|------|------------|------|
| Zero-Shot | 无 CoT，仅用 "The answer is" 提示 | [Q: qtest. A: The answer is.] | Kojima et al., 2022 |
| Zero-Shot-CoT | 使用 "Let's think step by step" 提示 | [Q: qtest. A: [P]]，[P]="Let's think step by step" | Kojima et al., 2022 |
| Few-Shot | 去除 rationales 的 Manual-CoT 版本 | [Q: q_i, A: a_i] × k → [Q: qtest. A: [P]] | Wei et al., 2022a |
| Manual-CoT | 人工设计的 questions + rationales + answers 示例 | [Q: q_i, A: r_i ◦ a_i] × k → [Q: qtest. A: [P]] | Wei et al., 2022a |
| Retrieval-Q-CoT | 基于 Sentence-BERT 相似度检索 top-k 问题，Zero-Shot-CoT 生成 chain | 同 Manual-CoT 结构，但自动生成 | 本文 Section 3 |
| Random-Q-CoT | 随机采样 k 个问题，Zero-Shot-CoT 生成 chain | 同 Manual-CoT 结构，但自动生成 | 本文 Section 3 |
| In-Cluster Sampling | 从与测试问题同一 cluster 中采样问题 | 同 Manual-CoT 结构 | 本文 Section 5.5 |
| Auto-CoT | 聚类→距中心最近→启发式筛选→Zero-Shot-CoT 生成 chain | 同 Manual-CoT 结构 | 本文 Section 4 |

来源：Section 5.1, Page 7；Section 3, Pages 3-5

### 模型与推理配置

| 配置项 | 值 | 来源 |
|--------|---|------|
| 主要模型 | GPT-3 text-davinci-002, 175B 参数 | Section 5.1, Page 7 |
| 辅助模型 | Codex code-davinci-002 | Section 5.4, Page 8 |
| 解码策略 | Greedy decoding | Section B.2, Page 14 |
| max_tokens | 256 | Section B.2, Page 14 |
| temperature | 0 | Section B.2, Page 14 |
| 运行时间 | 2022年7月至9月（OpenAI API） | Section B.2, Page 15（脚注5） |
| 大多数任务 demo 数 k | 8 | Section 5.1, Page 7 |
| AQuA demo 数 k | 4 | Section 5.1, Page 7 |
| Last Letters demo 数 k | 4 | Section 5.1, Page 7 |
| CSQA demo 数 k | 7 | Section 5.1, Page 7 |
| StrategyQA demo 数 k | 6 | Section 5.1, Page 7 |

### Auto-CoT 算法关键参数

| 参数 | 值 | 来源 |
|------|---|------|
| 问题编码 | Sentence-BERT（Reimers and Gurevych, 2019） | Section 4.1, Page 6 |
| 聚类算法 | k-means | Section 4.1, Page 6 |
| 聚类数 k | 与 demo 数一致（多数任务8） | Section 4.1, Page 6 |
| 排序策略 | 按距聚类中心距离升序 | Algorithm 1, Page 7 |
| 问题最大 token 数 | 60 | Section 4.2, Page 7 |
| 推理链最大步骤数 | 5（按 "\n" 计数） | Section 4.2, Page 7 |
| 算术推理任务额外检查 | 答案必须出现在 rationale 中（AQuA 因多选题除外） | Section C.2, Page 15 |
| 流式场景 batch 大小 m | 30（MultiArith） | Section 5.6, Page 9 |

### 论文未提供的实验配置信息

- Sentence-BERT 的具体模型版本（如 all-mpnet-base-v2 或 paraphrase-MiniLM-L6-v2）
- k-means 的随机种子
- 三条随机运行结果的具体数值（仅报告了均值）
- 单个 demo 构建所需的 API 调用次数
- 聚类计算时间的具体数值
- 所有实验的总体 API 调用成本估计

---

## 3. 主结果提取

### Table 3：10个数据集上的准确率（GPT-3 text-davinci-002）

来源：Table 3, Page 8

| 方法 | MultiArith | GSM8K | AddSub | AQuA | SingleEq | SVAMP | CSQA | Strategy | Letter | Coin |
|------|-----------|-------|--------|------|----------|-------|------|----------|--------|------|
| Zero-Shot | 22.7 | 12.5 | 77.0 | 22.4 | 78.7 | 58.8 | 72.6 | 54.3 | 0.2 | 53.8 |
| Zero-Shot-CoT | 78.7 | 40.7 | 74.7 | 33.5 | 78.7 | 63.7 | 64.6 | 54.8 | 57.6 | 91.4 |
| Few-Shot | 33.8 | 15.6 | 83.3 | 24.8 | 82.7 | 65.7 | 79.5 | 65.9 | 0.2 | 57.2 |
| Manual-CoT | 91.7 | 46.9 | 81.3 | 35.8 | 86.6 | 68.9 | 73.5 | 65.4 | 59.0 | 97.2 |
| **Auto-CoT** | **92.0** | **47.9** | **84.8** | **36.5** | **87.0** | **69.5** | **74.4** | **65.4** | **59.7** | **99.9** |

**关键比较**：
- Auto-CoT vs Manual-CoT 差值（Auto-CoT 减 Manual-CoT）：+0.3 (MultiArith), +1.0 (GSM8K), +3.5 (AddSub), +0.7 (AQuA), +0.4 (SingleEq), +0.6 (SVAMP), +0.9 (CSQA), +0.0 (StrategyQA), +0.7 (Last Letter), +2.7 (Coin Flip)
- Auto-CoT 在全部10个数据集上均 **>=** Manual-CoT
- Auto-CoT vs Zero-Shot-CoT 的最大提升：Coin Flip +8.5（99.9 vs 91.4），AddSub +10.1（84.8 vs 74.7）
- 来源：Table 3, Page 8

**注**：Zero-Shot 和 Zero-Shot-CoT 的结果引自 Kojima et al. [2022]，Few-Shot 和 Manual-CoT 的结果引自 Wei et al. [2022a]，Auto-CoT 结果是3次随机运行的平均值。
来源：Section 5.2, Page 8

### Table 4：Codex LLM 上的准确率

来源：Table 4, Page 8

| 方法 | MultiArith | GSM8K | AddSub |
|------|-----------|-------|--------|
| Zero-Shot-CoT | 64.8 | 31.8 | 65.6 |
| Manual-CoT | 96.8 | 59.4 | 84.6 |
| **Auto-CoT** | **93.2** | **62.8** | **91.9** |

**关键比较**：
- Auto-CoT vs Manual-CoT（Codex）：MultiArith 上 Auto-CoT 93.2 < Manual-CoT 96.8（-3.6）；GSM8K 上 Auto-CoT 62.8 > Manual-CoT 59.4（+3.4）；AddSub 上 Auto-CoT 91.9 > Manual-CoT 84.6（+7.3）
- 整体而言 Auto-CoT 仍与 Manual-CoT 竞争
- 来源：Table 4, Page 8；Section 5.4, Page 8

### Table 1：采样方法比较（Retrieval-Q-CoT vs Random-Q-CoT）

来源：Table 1, Page 4

| 方法 | MultiArith | GSM8K | AQuA |
|------|-----------|-------|------|
| Zero-Shot-CoT | 78.7 | 40.7 | 33.5 |
| Manual-CoT | 91.7 | 46.9 | 35.8† |
| Random-Q-CoT | 86.2 | 47.6† | 36.2† |
| Retrieval-Q-CoT | 82.8 | 48.0† | 39.7† |

† 表示使用了带标注推理链的训练集

**关键发现**：
- MultiArith 上 Retrieval-Q-CoT（82.8）< Random-Q-CoT（86.2），说明相似度检索在无人工标注时反不如随机采样
- GSM8K 和 AQuA 上带 † 表示使用了训练集标注的 reasoning chains，此时 Retrieval-Q-CoT 甚至优于 Manual-CoT
- 这验证了 "misleading by similarity" 假说——Zero-Shot-CoT 自动生成的错误 chain 会误导相似问题
- 来源：Table 1, Page 4；Section 3, Pages 3-4

### 多选答案格式

- AQuA：Multiple choice（5选1，选项 A-E）
- CSQA：Multiple choice（5选1，选项 A-E）
- StrategyQA：Yes or No
- Coin Flip：Yes or No
- Last Letter：String
- 其余：Number（阿拉伯数字）
- 来源：Table 7, Page 14

---

## 4. 消融实验提取

### 消融 1：采样策略消融（Retrieval-Q-CoT vs Random-Q-CoT vs clustering-based）

- **消融内容**：对比三种自动构建 demonstrations 的策略
- **测试变体**：
  - Retrieval-Q-CoT：Sentence-BERT 编码 + 余弦相似度检索 top-8 相似问题
  - Random-Q-CoT：随机采样 8 个问题
  - Auto-CoT：k-means 聚类（k=8）+ 每类选距中心最近问题 + 启发式筛选
- **揭示结果**：
  - MultiArith：Auto-CoT (92.0) > Random-Q-CoT (86.2) > Retrieval-Q-CoT (82.8)
  - 多样性采样（Auto-CoT 聚类 + 随机采样）均优于相似度检索
  - 聚类进一步提升性能（对比 Random 的纯随机）
- **来源**：Table 1, Page 4；Table 3, Page 8；Section 3, Pages 3-5

### 消融 2：demonstration 各组件影响（Table 5）

- **消融内容**：对 Manual-CoT 的 demos 分别 shuffle questions、rationales、answers，观察性能变化
- **测试变体**：
  - Manual-CoT（原始）：所有组件正确对齐
  - Shuffle Questions：交换 demo 中的 questions
  - Shuffle Rationales：交换 demo 中的 rationales
  - Shuffle Answers：交换 demo 中的 answers
- **揭示结果**：

| 变体 | MultiArith 准确率 |
|------|-----------------|
| Manual-CoT | 91.7 |
| Shuffle Questions | 73.8（-17.9） |
| Shuffle Rationales | 43.8（-47.9） |
| Shuffle Answers | 17.0（-74.7） |

- **关键发现**：rationale-answer 一致性比 question-rationale 映射更关键
- **来源**：Table 5, Page 13；Appendix A.1, Page 13

### 消融 3：错误 demonstrations 的影响（Figure 6）

- **消融内容**：人工控制 demo 中的错误比例，对比 Auto-CoT（多样性聚类）与 In-Cluster Sampling（同簇采样）
- **测试变体**：
  - Auto-CoT：从不同 cluster 采样的多样化 demo
  - In-Cluster Sampling：从同一 cluster 采样的同质 demo
- **揭示结果**：
  - 错误 demo 比例 12.5%→50% 时，Auto-CoT 准确率从 ~92% 降至 ~88%（仅降约 4%）
  - In-Cluster Sampling 从 ~95% 降至 ~82%（降约 13%）
  - 多样性显著增强了对错误 demo 的鲁棒性
- **来源**：Figure 6, Page 9；Section 5.5, Page 9

### 消融 4：简单启发式规则的效果（Table 9, Figure 10）

- **消融内容**：对比有/无简单启发式规则（问题≤60 tokens，推理链≤5步，答案出现在 rationale 中）下的自动构建 demo 质量
- **揭示结果**：

| 指标 | MultiArith | AddSub | GSM8K | AQuA | SingleEq | SVAMP | CSQA | Strategy | Letter | Coin |
|------|-----------|--------|-------|------|----------|-------|------|----------|--------|------|
| 错误 demo 数（有启发式） | 0.3 | 1.7 | 1.7 | 1.0 | 1.0 | 0.7 | 2.7 | 2.3 | 0 | 0 |
| 错误 demo 数（无启发式） | 1.3 | 5.0 | 3.0 | 2.7 | 2.0 | 3.3 | 3.3 | 2.3 | 3.0 | 1.0 |
| 错误率（有启发式，%） | 4 | 20 | 20 | 25 | 12 | 8 | 38 | 38 | 0 | 0 |
| 错误率（无启发式，%） | 16 | 62 | 37 | 66 | 25 | 41 | 47 | 38 | 75 | 12 |

- **关键发现**：启发式规则在 7/10 任务上将错误率降至 20% 以下；Last Letter 和 Coin Flip 上更降至 0%
- **来源**：Table 9, Page 15；Figure 10, Page 16；Section C.2, Page 15

### 消融 5：聚类内排序策略（Table 8）

- **消融内容**：在一个 cluster 内采样时，不同的排序/采样策略的影响
- **测试变体**（仅使用正确 demo 进行测试）：
  - In-Cluster Min Dist：选距聚类中心最近的问题（Auto-CoT 采用）
  - In-Cluster Random：随机选择
  - In-Cluster Max Dist：选距聚类中心最远的问题
- **揭示结果**：

| 方法 | MultiArith 准确率 |
|------|-----------------|
| Auto-CoT（完整方法） | 93.7 |
| In-Cluster Min Dist | 93.7 |
| In-Cluster Random | 89.2 |
| In-Cluster Max Dist | 88.7 |

- 靠近聚类中心的问题更适合作为 demonstration
- **来源**：Table 8, Page 15；Section C.1, Page 15

### 消融 6：不同聚类数量的影响（Figure 9）

- **消融内容**：在 MultiArith 数据集上测试不同的 k-means 聚类数 k={2, 4, 6, 8}
- **揭示结果**：无论聚类数为多少，总会有一个或多个 cluster 的错误率显著高于其他 cluster（frequent-error cluster 现象稳定存在）
- **来源**：Figure 9, Page 14；Appendix A.2, Pages 13-14

### 消融 7：流式场景 bootstrapping（Figure 7, Figure 11）

- **消融内容**：在流式设置下 Auto-CoT*（bootstrapping 版本）的性能
- **测试变体**：
  - Auto-CoT*：初始空集合 → batch 1 用 Zero-Shot-CoT → 后续 batch 用已有问题和 chain 构建 demo
  - Zero-Shot-CoT（baseline）
  - Manual-CoT（上界参考）
- **揭示结果**：
  - Batch 1：Auto-CoT* 与 Zero-Shot-CoT 准确率相同（无历史数据）
  - Batch 2 起：Auto-CoT* 快速达到与 Manual-CoT 相当的性能
  - 在全部 20 个 batch（600 个测试问题）上持续保持竞争力
- **来源**：Figure 7, Page 9；Figure 11, Page 16；Section 5.6, Page 9

### 论文未提供的消融实验

- 不同编码器（Sentence-BERT 之外）的消融
- 不同聚类算法（如 DBSCAN、层次聚类）的对比
- 启发式规则各子规则（问题长度、推理步骤数、答案检查）的独立贡献
- 不同 k 值对最终性能的系统影响
- 标注推理链（GSM8K 和 AQuA 训练集）对 Retrieval-Q-CoT 与 Auto-CoT 交叉比较的完整消融
- 跨 dataset 迁移性：在一个数据集上构建的 demo 在另一数据集上的效果

---

## 5. 参数敏感性与稳定性分析

### 聚类数 k（即 demonstration 数量）

- 大多数任务 k=8，AQuA 和 Last Letter k=4，CSQA k=7，StrategyQA k=6
- 来源：Section 5.1, Page 7
- **论文未提供**：不同 k 值对同一数据集性能的影响扫描

### 排序策略敏感性

- Min Dist → 93.7%（最好）；Random → 89.2%；Max Dist → 88.7%
- 差距约 5 个百分点，说明排序策略对性能有显著影响
- 来源：Table 8, Page 15

### 启发式规则参数敏感性

- 问题长度阈值：≤60 tokens
- 推理链步骤数阈值：≤5（按 "\n" 计数）
- **论文未提供**：不同阈值（如 40/80/100 tokens，3/7/10 steps）的扫描实验

### 随机种子敏感性

- Auto-CoT 结果为 3 次随机运行的平均值
- **论文未提供**：三次运行的具体数值、标准差、方差
- 来源：Section 5.2, Page 8（提到 "averaged over three random runs"）

### Model 规模敏感性

- 仅测试了 GPT-3 text-davinci-002（175B）和 Codex code-davinci-002
- **论文未提供**：不同规模（如 6.7B/13B/175B 对比）的系统性缩放分析
- 来源：Section 5.1, Page 7；Section 5.4, Page 8

### Retrieval-Q-CoT 的敏感度

- 使用 Sentence-BERT 编码 + 余弦相似度检索
- 在无人工标注时（MultiArith）性能低于 Random-Q-CoT
- 在有标注时（GSM8K†、AQuA†）甚至超越 Manual-CoT
- 来源：Table 1, Page 4

### 错误 demo 比例的鲁棒性

- Auto-CoT 在错误 demo 占比高达 50% 时性能下降不超过约 4 个百分点（Figure 6）
- In-Cluster Sampling 在同样条件下下降约 13 个百分点
- Auto-CoT 对错误 demo 的鲁棒性显著优于同簇采样
- 来源：Figure 6, Page 9

---

## 6. 效率、复杂度与资源代价

### 推理代价

| 维度 | 值 | 来源 |
|------|---|------|
| 基础模型 | GPT-3 text-davinci-002，175B 参数（通过 OpenAI API） | Section 5.1, Page 7 |
| 解码方式 | Greedy decoding, temperature=0 | Section B.2, Page 14 |
| max_tokens | 256 | Section B.2, Page 14 |
| 每次 API 调用生成内容 | 一个 demonstration 的 reasoning chain | Section 4.2, Page 7 |
| 每个数据集 demo 构建 API 调用次数 | k 次（每个 cluster 一次）+ 失败跳过时的额外调用 | Algorithm 2, Page 7 |
| 测试问题推理 API 调用次数 | 每个测试问题 1 次 | Section 4.2, Page 7 |
| 编码计算 | Sentence-BERT 对每个问题编码一次 | Section 4.1, Page 6 |
| 聚类计算 | k-means 一次性计算 | Section 4.1, Page 6 |

### 人工标注代价

| 标注项 | 数量 | 来源 |
|--------|------|------|
| Manual-CoT 人工 demo | 任务特定（8/4/7/6 个） | Section 5.1, Page 7 |
| Auto-CoT 人工标注 | **零**（无需人工） | Abstract, Page 1 |
| GSM8K / AQuA 训练集推理链标注 | 用于 † 实验，非 Auto-CoT 必需 | Section 3, Page 4 |

### 计算与成本

| 维度 | 值 | 来源 |
|------|---|------|
| 运行时间段 | 2022年7月至9月 | Page 15 脚注5 |
| GPU 需求 | 无需本地 GPU（OpenAI API） | Section B.2, Page 14 |
| 端到端 wall-clock time | **论文未提供** | — |
| 单次推理 token 消耗 | **论文未提供**（取决于 demo 数量和问题长度） | — |
| API 调用总成本 | **论文未提供** | — |
| 编码 + 聚类耗时 | **论文未提供** | — |

### Auto-CoT 与 Manual-CoT 人工成本对比

| 方法 | MultiArith | GSM8K | AddSub | AQuA | SingleEq | SVAMP | CSQA | Strategy | Letter | Coin | 来源 |
|------|-----------|-------|--------|------|----------|-------|------|----------|--------|------|------|
| Manual-CoT demo 来源 | 人工设计，5/6 算术任务共享相同 demos | 同上 | 同上 | 同上 | 同上 | 同上 | 人工设计 | 人工设计 | 人工设计 | 人工设计 | Section 5.2, Page 8 |
| Auto-CoT 额外代价 | 仅需编码+聚类+API 调用（自动） | 同上 | 同上 | 同上 | 同上 | 同上 | 同上 | 同上 | 同上 | 同上 | Section 4 |

---

## 7. 鲁棒性、泛化性与补充实验

### 跨任务领域泛化

Auto-CoT 在 3 大类共 10 个 benchmark 上测试：

| 推理类别 | 数据集数 | 数据集 | 来源 |
|---------|---------|--------|------|
| Arithmetic | 6 | MultiArith, GSM8K, AddSub, AQuA, SingleEq, SVAMP | Section B.1, Pages 13-14 |
| Commonsense | 2 | CSQA, StrategyQA | Section B.1, Pages 13-14 |
| Symbolic | 2 | Last Letter Concatenation, Coin Flip | Section B.1, Pages 13-14 |

在所有 10/10 数据集上，Auto-CoT 匹配或超越 Manual-CoT。
来源：Table 3, Page 8

### 跨模型泛化

| 模型 | 数据集 | 关键结果 | 来源 |
|------|--------|---------|------|
| GPT-3 text-davinci-002 (175B) | 全部10个 | Auto-CoT ≥ Manual-CoT | Table 3, Page 8 |
| Codex code-davinci-002 | MultiArith, GSM8K, AddSub | Auto-CoT 2/3 优于 Manual-CoT | Table 4, Page 8 |

**论文未提供**：其他 LLM（如 GPT-3 curie/babbage、LLaMA、Chinchilla、PaLM）上的结果。

### 跨聚类数目鲁棒性（Figure 8, Figure 9）

- MultiArith、AddSub、SingleEq、CSQA 上，无论聚类数为 2/4/6/8，frequent-error cluster 现象稳定存在
- △（最高与最低错误率的差值）：MultiArith △=43，AddSub △=46，SingleEq △=48，CSQA △=19
- 来源：Figure 8, Page 14；Figure 9, Page 14；Appendix A.2, Pages 13-14

### 流式场景泛化

- Auto-CoT* bootstrapping 版本在 MultiArith 流式设置下，从 batch 2 起性能即与 Manual-CoT 相当
- 来源：Figure 7, Page 9；Figure 11, Page 16

### 错误模式分析

| 错误现象 | 证据/数据 | 来源 |
|---------|----------|------|
| Frequent-error cluster 存在 | 某些 cluster 的 Zero-Shot-CoT 错误率高达 52.3%（Cluster 2, MultiArith） | Figure 3, Page 5 |
| Rationale-answer inconsistency | 表6 示例：rationale 中的答案是 29，但正确答案应为 9 | Table 6, Page 13 |
| Retrieval 加重错误 | Retrieval-Q-CoT unresolving rate 46.9% > Random-Q-CoT 25.8% | Figure 2, Page 4 |

### 论文未提供的鲁棒性验证

- 多 seed 运行的均值和标准差（仅提及 3 次运行取平均，未给具体值）
- 统计显著性检验（p-value, confidence interval）
- 不同 Sentence-BERT 模型编码的对比
- 不同聚类算法（DBSCAN, 层次聚类等）的影响
- k-means 初始化敏感性分析
- 训练集大小对 demos 质量的影响（假设仅用测试集）
- 跨语言泛化（仅英文数据集）
- 对抗性设置下的鲁棒性（如刻意构造的困难问题）

---

## 8. 值得关注的实验现象

### 现象 1：相似度检索在无标注时反不如随机采样

- Retrieval-Q-CoT 在 MultiArith 上 82.8% vs Random-Q-CoT 86.2%（无标注 reasoning chains）
- 检索将 Zero-Shot-CoT 的错误聚合到相似问题上，导致 "misleading by similarity"
- 但有标注 reasoning chains 后检索策略最优：GSM8K† 48.0%，AQuA† 39.7%
- **来源**：Table 1, Page 4；Section 3.1, Pages 3-4

### 现象 2：Zero-Shot-CoT 的错误集中在特定 cluster 中

- MultiArith 8 个 cluster 中，cluster 2 的错误率高达 52.3%，而其他 cluster 最低仅约 10%
- 该现象在 AddSub、SingleEq、CSQA 上均存在
- 改变聚类数目（2/4/6/8）现象依然稳定
- **来源**：Figure 3, Page 5；Figure 8, Figure 9, Page 14

### 现象 3：Auto-CoT 对错误 demo 有极强鲁棒性

- Figure 6 中，即使 50% 的 demo 是错误的，Auto-CoT 准确率仅从约 92% 降至约 88%
- 多样性采样的关键是错误分散在不同 cluster——不会出现 cluster 内多重错误叠加
- 仅 1-2 个错误 demo（8 个中的 12.5-25%）几乎不影响性能
- **来源**：Figure 6, Page 9；Section 5.5, Page 9；Section 3.3, Page 5

### 现象 4：Rationale-Answer 一致性极端重要

- Shuffle Answers 导致准确率从 91.7% 暴跌至 17.0%
- Shuffle Rationales 导致 91.7% → 43.8%
- 即使 Shuffle Questions（问题与 chain 错配）也降至 73.8%
- 说明 CoT 场景下 ICL 的行为与标准分类任务的 ICL 有本质差异
- **来源**：Table 5, Page 13；Appendix A.1, Page 13

### 现象 5：聚类中心附近的 question 更适合做 demo

- In-Cluster Min Dist（93.7%）显著优于 Max Dist（88.7%），差距 5 个百分点
- 可能原因是中心问题更具代表性，其 Zero-Shot-CoT 生成的 chain 更可靠
- **来源**：Table 8, Page 15；Section C.1, Page 15

### 现象 6：简单启发式规则效果显著

- 使用启发式规则前，AddSub 的平均错误 demo 数为 5.0（共 8 个 demos，错误率 62%）
- 使用后降至 1.7（错误率 20%），减少了超过一半的错误 demo
- Last Letter 和 Coin Flip 在启发式规则下错误 demo 数为 0
- 符号推理任务（Last Letter, Coin Flip）的自动 demo 构建最可靠
- **来源**：Table 9, Page 15；Figure 10, Page 16

### 现象 7：Zero-Shot-CoT 对不同数据集的表现差异极大

- 在 Coin Flip 上 Zero-Shot-CoT 已达 91.4%，接近 Manual-CoT 的 97.2%
- 在 Last Letter 上仅 57.6%，而 Manual-CoT 为 59.0%（差距较小）
- 在 GSM8K 上仅 40.7%，Manual-CoT 为 46.9%
- Zero-Shot-CoT 自身的推理质量上限会直接影响 Auto-CoT 的 demos 质量
- **来源**：Table 3, Page 8

### 现象 8：Auto-CoT 的零人工优势

- Manual-CoT 需要为每个任务类型单独设计 demos，且不同 annotator 带来高达 28.2% 的准确率差异（引用 Wei et al. 2022a 的发现）
- Auto-CoT 完全自动化，避免了人工设计的主观性和不一致性
- 此外 Auto-CoT 是 task-adaptive 的——每个数据集获得专有的 demos，而 Manual-CoT 的 5/6 算术任务共享同一组 demos
- **来源**：Section 3, Page 3；Section 5.2, Page 8

---

## 9. 证据充分性整理

### 支撑较充分的结论

| 结论 | 证据 | 充分性 |
|------|------|--------|
| Auto-CoT ≥ Manual-CoT（GPT-3） | Table 3 — 10/10 数据集一致达到或超越 | **充分** |
| 多样性缓解 misleading by similarity | Table 1 (3数据集)、Figure 2 (MultiArith)、Figure 6 (MultiArith) | **较充分**（主要基于 MultiArith 的深入分析，其他数据集仅 Table 1 间接支持） |
| 启发式规则减少错误 demo | Table 9 (10数据集) + Figure 10 — 全部 10 个数据集一致 | **充分** |
| 聚类中心 question 更优 | Table 8 — 1 个数据集的 3 种变体对比 | **有限**（仅 MultiArith，仅用正确 demo 过滤后） |
| Auto-CoT 在 Codex 上仍具竞争力 | Table 4 — 3 个数据集上 2/3 超过 Manual-CoT | **较充分**（数据集偏少） |

### 支撑有限的结论

| 结论 | 局限 |
|------|------|
| Reasoning chain 自动生成足够可靠 | Zero-Shot-CoT 在 GSM8K 上准确率仅 40.7%，生成 chain 质量受限 |
| CoT 场景下 ICL 行为不同 | Shuffle 实验仅在 MultiArith 上进行（Table 5） |
| 聚类数 k 的通用规则 | 仅引用 Manual-CoT 的 k 设定，未做 k 值的系统扫描 |
| 流式场景的有效性 | 仅在 MultiArith 上验证（Figure 7, Figure 11），未在其他数据集测试 |
| 跨 LLM 泛化 | 仅测试 GPT-3 和 Codex，且 Codex 实验结果仅在 3 个数据集 |

### 论文未提供的实验信息

- 多 seed 运行的均值和标准差（仅提及 3 次平均）
- 统计显著性检验（p-value, confidence interval）
- 不同 Sentence-BERT 模型/编码器的对比
- 不同聚类算法（DBSCAN, 层次聚类, GMM）的影响
- k-means 初始化随机种子影响
- 非英文数据集的验证
- 不同 LLM backbone（PaLM, LLaMA, Chinchilla 等）上的结果
- 训练集可用时的 Auto-CoT 变体对比
- 自动生成 chain 的质量与人工标注 chain 的细粒度对比
- Demo 顺序（ordering）对 Auto-CoT 性能的影响
- 启发式规则中各子规则（问题长度/推理步数/答案检查）的独立贡献度分析
- 人类对自动生成 demos 的可读性评估

---

## 10. 对后续问题发现最有价值的实验信息

### 可复现的实验设定

- **数据集**：10 个公开 benchmark（MultiArith, GSM8K, AddSub, AQuA, SingleEq, SVAMP, CSQA, StrategyQA, Last Letter, Coin Flip），全部公开可用
- **模型**：GPT-3 text-davinci-002（通过 OpenAI API），Greedy decoding, temperature=0, max_tokens=256
- **编码**：Sentence-BERT（Reimers and Gurevych, 2019）
- **聚类**：k-means，聚类数 = demonstration 数（多数任务 8）
- **启发式规则**：问题 ≤60 tokens，推理步骤 ≤5（"\n" 计数），算术任务额外检查 answer in rationale
- **OpenAI API 运行时间**：2022 年 7 月至 9 月
- **代码开源**：https://github.com/amazon-research/auto-cot

### 值得验证的问题

1. **Zero-Shot-CoT 的错误模式**：是推理步骤缺失、计算错误、还是理解偏差？Auto-CoT 构建的 demos 是否包含类似错误？不同类型的错误对最终性能影响是否相同？
2. **Frequent-error cluster 的根因**：为什么特定 cluster 中的问题 Zero-Shot-CoT 频繁失败？是否由问题模板、词汇模式、或推理复杂度导致？
3. **启发式规则阈值的敏感性**：问题长度 60 tokens 和推理步骤 5 步的阈值是最优的吗？不同数据集是否有不同的最优阈值？
4. **聚类数 k 的影响**：Auto-CoT 是否对 k 值选择鲁棒？Optimal k 是否与数据集的内在结构（如真实类别数）相关？
5. **Rationale-answer 一致性假说**：Zero-Shot-CoT 生成 "正确逻辑但错误答案" 的 chain 到底占比多少？这类 chain 作为 demo 的影响是否与 "错误逻辑+错误答案" 的 chain 不同？
6. **Auto-CoT 与 Manual-CoT 的 demo 质量差异**：自动生成的 demo 与人工设计的 demo 在推理链长度、步骤清晰度、错误类型等方面有何差异？
7. **跨 LLM 泛化**：在小模型（如 GPT-3 curie/davinci 较小版本，或其他开源模型）上 Auto-CoT 是否仍然有效？小模型的 Zero-Shot-CoT 质量更差是否会导致 Auto-CoT 失败？
8. **Streaming 场景下的通用性**：除 MultiArith 外，Auto-CoT* 在其他数据集上的 streaming 表现如何？

### 最值得优先验证的 3 个问题

1. **Auto-CoT 的 demo 错误类型对下游性能的影响机制**（关于错误传播路径的深入分析，关系到方法的可靠性边界）
2. **启发式规则阈值的跨数据集最优值**（对方法落地和应用的可调性至关重要）
3. **跨模型泛化性验证（不同规模 / 不同架构的 LLM）**（决定 Auto-CoT 是否是通用范式）

---

## 11. 一段简短总结

Auto-CoT 在 10 个异构 benchmark（涵盖算术推理、常识推理、符号推理 3 大类）上验证了完全自动构建 CoT demonstrations 的有效性。核心实验发现：(1) Auto-CoT 在全部 10 个数据集上一致匹配或超越依赖人工设计的 Manual-CoT（Table 3）；(2) 多样性聚类采样（Auto-CoT 的核心策略）显著优于相似度检索（Retrieval-Q-CoT）和随机采样（Random-Q-CoT），有效缓解了 Zero-Shot-CoT 错误的 "misleading by similarity" 问题；(3) 简单启发式规则（短问题、短推理链、答案出现在推理中）平均降低错误 demo 比例约 50%，在 7/10 任务上将错误率控制在 20% 以下；(4) rationale-answer 一致性极端重要（Shuffle Answers 导致准确率从 91.7% 暴跌至 17.0%），但 Auto-CoT 通过启发式规则有效控制此风险；(5) 聚类中心附近的 question 生成的 demo 显著优于边缘 question（Table 8, 差距高达 5 个百分点）。证据充分性最强的结论是 Auto-CoT ≥ Manual-CoT（10/10 数据集一致），但跨 LLM 泛化性验证仅限于 GPT-3 和 Codex，聚类策略对不同聚类参数的敏感性、启发式规则阈值、以及错误 demo 类型与性能影响的关系等关键问题均未充分消融。代码已开源，为基础实验复现和验证提供了有利条件。
