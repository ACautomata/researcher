# LCompo-SGG: Execution Strategy (No Code)

**论文核心命题：** SGG 长尾问题的深层原因是 compositional sparsity，而非单纯 frequency imbalance。Tail predicate 因为出现的 (subject, object) 组合太少，模型记住的是 category co-occurrence 而非 visual relation concept。现有 debiasing 方法在 standard mR@K 上的提升不必然带来 novel composition 上的泛化。

---

## Phase 1: 数据验证 — 证明 thesis 成立（3-4 天）

**目标：** 在写任何方法之前，先用数据说服自己（和未来的 reviewer）composiitonal sparsity 是一个真实且被忽视的问题。

### Step 1.1: Composition coverage 统计（1 天）

**做什么：**
对 VG150 的 training split，统计每个 predicate 的三个基础数字：
- **frequency:** 该 predicate 的总标注数
- **unique compositions:** 出现了多少种不同的 (subject_class, object_class) 组合
- **coverage_ratio:** unique_compositions / frequency（表示组合多样性）

按 frequency 排序分为 Head / Body / Tail（建议：Top-5 Head，6-20 Body，21-50 Tail）。

**观察什么：**
- Tail group 的 mean coverage_ratio 是否显著低于 Head group？
- 找具体的 predicate pair：frequency 相近但 coverage 差异大（例如都是 100 次左右，一个在 5 种组合中出现，一个在 20 种中出现）。这是论文中最有力的定性证据。

**输出：**
- 一张散点图（x=frequency, y=unique_compositions, 颜色=H/B/T）
- 一组统计数据（各组均值、极值、correlation）
- 2-3 个具体 predicate 对比例子

**判断继续还是调整：**
- ✅ Tail coverage 明显更低 → 继续 Phase 1.2
- ❌ Tail 和 Head 的 coverage 没有显著差异 → thesis 不成立，需要重新思考方向

### Step 1.2: 构造 Compositional Split（1 天）

**做什么：**
构造一个新的 train/test split，划分逻辑不是按 predicate class 或按 image，而是按 (subject, object) composition。对每个 predicate p，它出现的所有 (s, o) 组合中，75% 进入训练集，25% 进入测试集。

**强制约束（必须检查）：**
- 测试集中所有 object class 必须出现在训练集中
- 测试集中所有 subject class 必须出现在训练集中
- 测试集中所有 predicate 必须出现在训练集中
- 即：只 hold out (s, p, o) 这种 composition，不 hold out 任何单个元素

**生成 3 个 seed 的 split** 用于后续统计稳定性。

**检查输出：**
- 每个 predicate 在训练集中至少还有 composition
- 所有 class 在训练集中都已看到
- 各组 predicate 的 seen/unseen 比例大致均匀

### Step 1.3: Baseline 诊断（1-2 天）

**做什么：**
拿一个训练好的 baseline 模型（Motifs 最简单），在三个设置下分别评估：
1. **Standard VG150 test** — baseline 的标准表现
2. **Composition Seen** — 在 compositional test split 中，只保留那些 composition 在训练集中出现过的样本
3. **Composition Unseen** — 在 compositional test split 中，只保留 composition 在训练集中没出现过的样本

按 H/B/T 分组报告 mR@20 和 mR@50。

**关键观察（论文核心 Figure 的 base）：**
- Head / Body / Tail 各自的 Seen vs Unseen gap
- Tail Unseen 是否远低于 Tail Seen？
- 如果有多个 baseline（Motifs, VCTree, Transformer），对比它们之间的 gap 是否一致

**预期结果（支持 thesis）：**
Tail Unseen 显著低于 Tail Seen，且这个 gap 明显大于 Head 或 Body 的 gap。这意味着：传统 H/B/T 划分只看 frequency，但 unseen composition 上的表现揭示了另一个维度的问题。

**如果结果漂亮 → 论文 Sec 3.1（Motivating Analysis）的素材已经够了。**

---

## Phase 2: 方法设计 + 实现（7-10 天）

**目标：** 设计一个方法，核心目标不是"提升 mR@K"，而是"在 unseen composition 上缩小 H/B/T gap"。

### 核心思路

当前 SGG 模型的 predicate prediction 依赖于两条路径：
1. **Visual path:** 从 union feature + geometry 提取的视觉关系特征
2. **Category shortcut path:** 从 (subject class, object class) 推断的统计先验

Tail predicate 因为数据少，模型过度依赖路径 2。在 novel composition 上路径 2 失效，所以 recall 断崖下降。

**方法的核心逻辑：** 削弱路径 2，强化路径 1，同时让路径 1 学到可跨 composition 迁移的 visual concept。

### 建议方法架构（三部分）

**A. 双分支预测器**
- Visual branch: 只接受 visual pair feature（union feature + geometry + subject/object visual feature），不接受 category 信息
- Bias branch: 只接受 subject class embedding + object class embedding，不接受视觉信息
- 两个分支各自输出 predicate logits

**B. 解耦训练**
- Adversarial 训练：在 visual branch 的 feature 上加 gradient reversal layer，接一个 composition 分类器（预测 (s, o) pair 属于哪个 composition group）。让 visual feature 不能编码 category 信息。
- Bias subtraction：推理时 final logits = visual_logits - λ * bias_logits。λ 是超参，控制 shortcut 抑制强度。
- 正面对齐：对同样的 (s, o) pair 在不同图像中的 visual feature 做 contrastive learning，增强同一 predicate 在不同 composition 下的视觉一致性。

**C. Novel Composition Correction（可选强化版）**
- 维护一个 seen composition prototype 库
- 对 novel composition，在视觉空间中找到最相似的 seen composition prototype
- 用 correction network 估计 unseen → seen 的偏移量，调整 visual feature

### MVP 实现顺序

| 阶段 | 实现内容 | 预期时间 |
|------|---------|---------|
| MVP-1 | Visual branch + Bias branch 双分支 | 2 天 |
| MVP-2 | Bias subtraction 推理 | 0.5 天 |
| MVP-3 | Adversarial training（GRL + composition classifier） | 2 天 |
| MVP-4 | Contrastive loss 增强 | 1 天 |
| MVP-5 | Novel composition corrector | 2-3 天（可选） |

**不做的事情（避免 scope creep）：**
- 不做 LLM/VLM
- 不做 codebook / tokenizer
- 不做 hierarchical anything
- 不做 generative model
- 不做 external knowledge

### 在 OpenSGG 中的集成方式

你的方法只需要替换 predicate head。Backbone（Motifs/VCTree/Transformer）不变。

- 输入：backbone 输出的 pair feature（visual union feature, subject feature, object feature, spatial feature）+ subject/object class embedding
- 输出：50-class predicate logits
- 训练：CE loss + adversarial loss + contrastive loss
- 推理：visual_logits - λ * bias_logits

---

## Phase 3: 实验验证（10-14 天）

### 实验 1: 主结果

| Setting | 你要证明的点 |
|---------|------------|
| Standard PredCLS (R/mR@K) | 方法不破坏 standard performance |
| Composition Seen (mR@K) | 方法在 seen 上持平或小幅提升 |
| Composition Unseen (mR@K) | **方法在 unseen 上显著提升（核心贡献）** |
| H/B/T breakdown | Tail 的 unseen gain > Head/Body |

**对比 baseline：**
- Motifs（vanilla）
- Motifs + Reweighting（最简单的 fairness baseline）
- Motifs + TDE（最经典的 causal debias）
- Motifs + CFA（最近的 feature augmentation）
- VCTree（另一个 backbone）
- VCTree + 方法（验证可插拔）

### 实验 2: Ablation

| 去掉什么 | 预期影响 | 证明 |
|---------|---------|------|
| Bias subtraction（λ=0） | Unseen 下降，Seen 可能上升 | bias branch 有效 |
| Adversarial loss | Visual feature 能预测 composition，unseen 下降 | 解耦是必要的 |
| Contrastive loss | 各 composition 间 visual feature 不一致，unseen 下降 | 跨 composition 对齐有效 |
| Novel composition corrector | 极 rare composition 的 recall 下降 | correction 有效 |

### 实验 3: 分析实验（论文加分项）

1. **Visual feature 的 t-SNE 可视化：** baseline vs 方法，看各 predicate 的 visual feature 是否更聚类、更 separable
2. **Bias branch 分析：** bias_logits 在 seen vs unseen 上的置信度差异
3. **Per-predicate 详细报告：** 选 5 个代表性的 predicate（高 freq 高 coverage、高 freq 低 coverage、低 freq 高 coverage、低 freq 低 coverage），展示详细 recall
4. **λ 敏感性分析：** bias subtraction 强度对 trade-off 的影响
5. **Composition coverage 连续性分析：** 按 coverage_ratio 分桶（不是 H/B/T），看 recall 和 coverage 的单调关系

### 实验 4: 跨数据集泛化（如果有时间）

- 在 GQA 或 PSG 上重复 compositional split 评估
- 不要求重训模型，用 VG150 训好的直接 zero-shot 评估

---

## Phase 4: 论文写作（7-10 天）

### 论文结构（CVPR 9 pages）

**Sec 1: Introduction（1 page）**
- SGG 的任务定义和长尾问题
- 传统 bias: frequency imbalance
- **我们的发现：** frequency 不是全部，compositional sparsity 是隐藏维度
- Thesis + 方法一句话 + contribution bullets

**Sec 2: Related Work（1-1.5 pages）**
- Debiased SGG（TDE, CFA, etc.）— 他们没考虑 composition
- Compositional generalization in vision — 在其他领域存在，在 SGG 中未系统化
- Relation representation learning — 现有方法都基于 atomic classification

**Sec 3: Compositional Sparsity in SGG（1-1.5 pages）—— 这篇论文的亮点**
- 3.1: 统计分析：freq vs coverage 的 disalignment
- 3.2: 诊断实验：现有方法在 unseen composition 上失败
- 3.3: LCompo-SGG 评估协议定义
- Figure 1 + Figure 2

**Sec 4: Method（1.5-2 pages）**
- 4.1: 双分支架构
- 4.2: Adversarial composition debiasing
- 4.3: Cross-composition contrastive alignment
- 4.4: Novel composition correction
- Architecture figure

**Sec 5: Experiments（2-2.5 pages）**
- 5.1: 设置（datasets, metrics, baselines, implementation details）
- 5.2: 主结果（Table 1: Standard + Compositional metrics）
- 5.3: Ablation（Table 2）
- 5.4: 分析实验（t-SNE, per-predicate, λ analysis）
- 5.5: 跨数据集（如果有）

**Sec 6: Conclusion（0.5 page）**

---

## Timeline 汇总

| 日期 | 阶段 | 交付物 |
|------|------|--------|
| 6/9 - 6/10 | Phase 1.1 | VG150 composition coverage 统计 + 图 |
| 6/11 | Phase 1.2 | Compositional split（3 seeds）|
| 6/12 - 6/14 | Phase 1.3 | Baseline 诊断结果 |
| **6/14** | **决策点** | Thesis 是否立住 |
| 6/15 - 6/16 | Phase 2 MVP-1/2 | 双分支 + bias subtraction 实现 |
| 6/17 - 6/18 | Phase 2 MVP-3 | Adversarial training 实现 |
| 6/19 | Phase 2 MVP-4/5 | Contrastive loss + corrector |
| 6/20 - 6/22 | Phase 3 实验 | 第一轮实验结果 |
| **6/22** | **决策点** | 方法是否有效 |
| 6/23 - 6/28 | Phase 3 补全 | 多 backbone + ablation + 分析 |
| 6/29 - 7/4 | Phase 4 写作 | 初稿完成 |
| 7/5 - 7/6 | 修改 + supplementary | 定稿 |

---

## 风险清单

| 风险 | 概率 | 影响 | 应对 |
|------|------|------|------|
| Composition coverage 和 frequency 高度相关，不是独立维度 | 中 | 高 | 做 partial correlation（控制 frequency 后 coverage 是否还显著）|
| 方法在 Seen 上掉点 | 中 | 中 | Bias subtraction 用较小 λ 起步；用 R@K/mR@K 一起报告 |
| Adversarial training 不稳定 | 中 | 中 | GRL 的 λ_grl 从 0 开始 warmup |
| Unseen composition 样本太少导致统计不稳定 | 高 | 中 | 多 seed split 取 mean/std；reasonable threshold |
| Novel composition corrector 太复杂 | 中 | 低 | 先跑 MVP-1~4，corrector 作为 bonus |

---

## 一个建议

Phase 1（数据验证 + baseline 诊断）是最重要的。如果你做完 Phase 1 发现 thesis 立住了（Tail composition coverage 显著低 + baseline 在 unseen 上垮掉），那你在没写一行方法代码的情况下已经有两个 figures 和一个 strong motivation。这时候投 CVPR 的概率已经高于你写 tokenizer 方向。

反过来，如果 Phase 1 的数据不支持 thesis（composition coverage 和 frequency 几乎完全共线，或者 baseline 在 unseen 上没怎么掉），那早发现早转向。

所以：**先跑数据，再说方法。**
