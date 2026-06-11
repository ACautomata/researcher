# LCompo-SGG: Long-tail Compositional SGG 执行计划

## 总览

```
Week 1: 数据分析 + 构建 split → Week 2: Baseline 诊断 → Week 3: 方法实现 → Week 4: 实验
```

---

## Week 1: 数据分析和 Compositional Split（6 月 9 日 - 6 月 15 日）

### Step 1.1: 统计 VG150 composition coverage（2 天）

```bash
# 在 OpenSGG 项目根目录下新建脚本
mkdir -p tools/analysis
```

#### `tools/analysis/composition_coverage.py`

```python
"""
统计 VG150 中每个 predicate 的:
- frequency
- unique (subject_class, object_class) count
- coverage_ratio = unique_so / frequency
- H/B/T group based on frequency
"""
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from collections import defaultdict, Counter

# --- Config ---
DATA_ROOT = Path("data/vg150")
SPLIT_FILE = DATA_ROOT / "VG150_SGG_split.json"  # 或你的 split 格式
OUTPUT_DIR = Path("reports/composition")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# --- Load data ---
# 需要根据自己的数据格式调整
with open(SPLIT_FILE) as f:
    data = json.load(f)  # 格式: list of {"image_id": ..., "objects": [...], "relations": [...]}

# --- 统计每个 predicate ---
predicate_stats = defaultdict(lambda: {
    "freq": 0,
    "compositions": set(),
    "images": set(),
})

for item in data:
    img_id = item["image_id"]
    for rel in item["relations"]:
        subj_cls = rel["subject"]["class"]
        obj_cls = rel["object"]["class"]
        pred = rel["predicate"]
        predicate_stats[pred]["freq"] += 1
        predicate_stats[pred]["compositions"].add((subj_cls, obj_cls))
        predicate_stats[pred]["images"].add(img_id)

# --- Build DataFrame ---
rows = []
for pred, stats in sorted(predicate_stats.items(), key=lambda x: -x[1]["freq"]):
    freq = stats["freq"]
    comp_count = len(stats["compositions"])
    coverage_ratio = comp_count / freq if freq > 0 else 0
    rows.append({
        "predicate": pred,
        "frequency": freq,
        "unique_compositions": comp_count,
        "coverage_ratio": coverage_ratio,
        "unique_images": len(stats["images"]),
    })

df = pd.DataFrame(rows)
df = df.sort_values("frequency", ascending=False)

# --- 标注 H/B/T ---
# VG150 通常的划分: top ~5-6 predicates = Head, next ~10-15 = Body, rest = Tail
# 或按频率分位数划分
freq_vals = df["frequency"].values
cum_ratio = freq_vals.cumsum() / freq_vals.sum()

def assign_group(freq, cum_ratio_row):
    # 常用划分: Head = 频率总和前 50%, Body = 50-90%, Tail = 后 10%
    # 但更好是按 predicate 排名划分
    pass

# 建议更简单的划分: 按 predicate 数量分
# VG150 有 50 个 predicate
# Head: 排名 1-5, Body: 排名 6-20, Tail: 排名 21-50

def assign_group_simple(rank):
    if rank < 5:
        return "Head"
    elif rank < 20:
        return "Body"
    else:
        return "Tail"

df["group"] = [assign_group_simple(i) for i in range(len(df))]

# --- 输出统计 ---
df.to_csv(OUTPUT_DIR / "predicate_composition_stats.csv", index=False)
print(f"Total predicates: {len(df)}")
print(f"Head: {len(df[df['group'] == 'Head'])}")
print(f"Body: {len(df[df['group'] == 'Body'])}")
print(f"Tail: {len(df[df['group'] == 'Tail'])}")

# 关键统计: 各组平均 composition coverage
for group in ["Head", "Body", "Tail"]:
    gdf = df[df["group"] == group]
    print(f"\n{group}:")
    print(f"  Mean frequency: {gdf['frequency'].mean():.1f}")
    print(f"  Mean unique compositions: {gdf['unique_compositions'].mean():.1f}")
    print(f"  Mean coverage ratio: {gdf['coverage_ratio'].mean():.4f}")

# --- 绘图 1: frequency vs unique compositions ---
fig, ax = plt.subplots(figsize=(10, 6))
colors = {"Head": "#e74c3c", "Body": "#f39c12", "Tail": "#3498db"}
for group in ["Head", "Body", "Tail"]:
    gdf = df[df["group"] == group]
    ax.scatter(gdf["frequency"], gdf["unique_compositions"],
               c=colors[group], label=group, alpha=0.7, s=60)
    for _, row in gdf.iterrows():
        ax.annotate(row["predicate"], (row["frequency"], row["unique_compositions"]),
                    fontsize=7, alpha=0.7)

ax.set_xlabel("Predicate Frequency (log)", fontsize=12)
ax.set_ylabel("Unique (Subject, Object) Compositions", fontsize=12)
ax.set_xscale("log")
ax.set_yscale("log")
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "freq_vs_composition_coverage.png", dpi=150)
print(f"\nSaved: {OUTPUT_DIR / 'freq_vs_composition_coverage.png'}")

# --- 绘图 2: coverage ratio 分布 ---
fig, ax = plt.subplots(figsize=(10, 4))
for i, group in enumerate(["Head", "Body", "Tail"]):
    gdf = df[df["group"] == group]
    ax.hist(gdf["coverage_ratio"], bins=20, alpha=0.6, label=group, color=colors[group])
ax.set_xlabel("Composition Coverage Ratio (unique SO / frequency)")
ax.set_ylabel("Predicate Count")
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "coverage_ratio_distribution.png", dpi=150)

# --- 输出 key observations 用于论文 ---
print("\n=== Key Observations for Paper ===")
print(f"1. Coverage ratio range: {df['coverage_ratio'].min():.4f} - {df['coverage_ratio'].max():.4f}")
print(f"2. Head predicates avg composition count: {df[df['group']=='Head']['unique_compositions'].mean():.1f}")
print(f"3. Tail predicates avg composition count: {df[df['group']=='Tail']['unique_compositions'].mean():.1f}")

# 找同频率但不同 composition coverage 的例子
mid_freq = df[(df["frequency"] > 50) & (df["frequency"] < 200)]
if len(mid_freq) >= 2:
    max_comp = mid_freq.loc[mid_freq["unique_compositions"].idxmax()]
    min_comp = mid_freq.loc[mid_freq["unique_compositions"].idxmin()]
    print(f"\n4. Same freq range, different coverage:")
    print(f"   High coverage: {max_comp['predicate']} (freq={max_comp['frequency']}, comp={max_comp['unique_compositions']})")
    print(f"   Low coverage: {min_comp['predicate']} (freq={min_comp['frequency']}, comp={min_comp['unique_compositions']})")
```

#### 预期输出

- `predicate_composition_stats.csv` — 完整统计表
- `freq_vs_composition_coverage.png` — **论文 Figure 1 候选**
- 控制台输出关键统计数据

---

### Step 1.2: 构建 Compositional Split（2 天）

#### `tools/analysis/make_compositional_split.py`

```python
"""
构造 Compositional SGG split。

策略:
- 对每个 predicate p，收集所有 unique (subject_class, object_class) 组合
- 75% 的 composition 归入训练集，25% 归入测试集
- 保证: 所有 subject class 和 object class 在训练集中都出现过
- 保证: 所有 predicate 在训练集中都出现过（只是某些 composition 没出现）

输出:
- train.json / test.json (或与 OpenSGG 兼容的格式)
"""
import json
import random
import argparse
from pathlib import Path
from collections import defaultdict

def build_composition_split(data, split_ratio=0.75, min_seen_compositions=1, seed=42):
    """
    Args:
        data: list of dicts, each with "relations" containing {subject, object, predicate}
        split_ratio: 多少比例的 composition 用于训练
        min_seen_compositions: 每个 predicate 至少保留多少 composition 在训练集
    """
    random.seed(seed)

    # Step 1: 收集每个 predicate 的所有 composition 和对应的 image_ids
    pred_compositions = defaultdict(lambda: defaultdict(list))
    # pred_compositions[pred][(subj_cls, obj_cls)] = [img_id1, img_id2, ...]

    for item in data:
        img_id = item["image_id"]
        for rel in item["relations"]:
            subj = rel["subject"]["class"]
            obj = rel["object"]["class"]
            pred = rel["predicate"]
            pred_compositions[pred][(subj, obj)].append(img_id)

    # Step 2: 对每个 predicate 划分 composition
    train_compositions = {}  # predicate -> set of (s, o) in train
    test_compositions = {}

    for pred, comp_dict in pred_compositions.items():
        comps = list(comp_dict.keys())
        random.shuffle(comps)

        # 至少保留 min_seen_compositions 个 composition 在训练集
        n_train = max(min_seen_compositions, int(len(comps) * split_ratio))

        # 但确保 train 不为空
        n_train = min(n_train, len(comps) - 1)

        train_comps = set(comps[:n_train])
        test_comps = set(comps[n_train:])

        train_compositions[pred] = train_comps
        test_compositions[pred] = test_comps

    # Step 3: 分配 image 到 train/test
    train_relations = []
    test_relations = []

    for item in data:
        img_id = item["image_id"]
        for rel in item["relations"]:
            subj = rel["subject"]["class"]
            obj = rel["object"]["class"]
            pred = rel["predicate"]

            comp = (subj, obj)
            if comp in train_compositions.get(pred, set()):
                train_relations.append({**item, "image_id": img_id, "relation": rel})
            elif comp in test_compositions.get(pred, set()):
                test_relations.append({**item, "image_id": img_id, "relation": rel})

    # Step 4: Verify
    train_subjects = set()
    train_objects = set()
    train_predicates = set()
    for rel in train_relations:
        r = rel["relation"]
        train_subjects.add(r["subject"]["class"])
        train_objects.add(r["object"]["class"])
        train_predicates.add(r["predicate"])

    test_subjects = set()
    test_objects = set()
    test_predicates = set()
    for rel in test_relations:
        r = rel["relation"]
        test_subjects.add(r["subject"]["class"])
        test_objects.add(r["object"]["class"])
        test_predicates.add(r["predicate"])

    print(f"Train: {len(train_relations)} relations, {len(train_subjects)} subjects, {len(train_objects)} objects, {len(train_predicates)} predicates")
    print(f"Test: {len(test_relations)} relations, {len(test_subjects)} subjects, {len(test_objects)} objects, {len(test_predicates)} predicates")

    # Check: all object/predicate classes in test should be in train
    missing_subjects = test_subjects - train_subjects
    missing_objects = test_objects - train_objects
    missing_predicates = test_predicates - train_predicates

    if missing_subjects:
        print(f"WARNING: {len(missing_subjects)} subjects in test but not in train: {missing_subjects}")
    if missing_objects:
        print(f"WARNING: {len(missing_objects)} objects in test but not in train: {missing_objects}")
    if missing_predicates:
        print(f"WARNING: {len(missing_predicates)} predicates in test but not in train: {missing_predicates}")

    return train_relations, test_relations, {
        "pred_compositions": {p: {"train": len(tc), "test": len(test_compositions.get(p, set()))}
                              for p, tc in train_compositions.items()}
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True, help="Input JSON file")
    parser.add_argument("--output_dir", type=str, default="data/vg150/composition_splits")
    parser.add_argument("--split_ratio", type=float, default=0.75)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--n_splits", type=int, default=3, help="Generate N random splits for stability")
    args = parser.parse_args()

    with open(args.input) as f:
        data = json.load(f)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for seed_offset in range(args.n_splits):
        seed = args.seed + seed_offset
        train, test, stats = build_composition_split(data, args.split_ratio, seed=seed)

        split_dir = output_dir / f"split_{seed_offset}"
        split_dir.mkdir(parents=True, exist_ok=True)

        with open(split_dir / "train.json", "w") as f:
            json.dump(train, f)
        with open(split_dir / "test.json", "w") as f:
            json.dump(test, f)
        with open(split_dir / "stats.json", "w") as f:
            json.dump(stats, f, indent=2)

        print(f"Saved split {seed_offset} to {split_dir}")
```

#### 验证 split 质量

构造完后，跑：

```python
# 在 OpenSGG 中: 检查每个 predicate 中 seen/unseen 分布
# 预期: tail predicate 的 seen composition 数量远少于 head
# 按 H/B/T 分组统计 composition gap
```

**Checklist:**
- [ ] All object classes in test seen in train
- [ ] All subject classes in test seen in train
- [ ] All predicate classes in test seen in train
- [ ] Each predicate has at least 1 seen composition in train (避免 zero-shot predicate)
- [ ] 生成 3 个不同 seed 的 split 用于稳定评估

---

### Step 1.3: Baseline 诊断（2 天，与 Step 1.2 并行）

在 OpenSGG 中：

```bash
# 1. 先用标准 VG150 split 跑 Motifs，记录每个 predicate 的 recall
python tools/train.py --cfg configs/motifs/predcls.yaml \
  --output_dir outputs/diagnostic/motifs_standard

# 2. 生成每个 predicate 的 recall 表
python tools/eval.py --resume outputs/diagnostic/motifs_standard/model.pth \
  --save_per_predicate_reports \
  --output reports/diagnostic/motifs_per_pred_recall.json

# 3. 在 compositional split 上重新评估
# (需要让 eval.py 支持 --split_file 参数)
python tools/eval.py --resume outputs/diagnostic/motifs_standard/model.pth \
  --split_file data/vg150/composition_splits/split_0/test.json \
  --save_per_predicate_reports \
  --output reports/diagnostic/motifs_compositional/test_split_0.json

# 4. 对每个 model （Motifs, VCTree, RelTR）重复
```

#### `tools/analysis/compute_correlations.py`

```python
"""
计算 frequency / composition coverage / recall 之间的相关性。
"""
import json
import pandas as pd
from scipy.stats import pearsonr, spearmanr

# 加载 predicate stats
stats_df = pd.read_csv("reports/composition/predicate_composition_stats.csv")

# 加载 per-predicate recall
with open("reports/diagnostic/motifs_per_pred_recall.json") as f:
    recall_data = json.load(f)

recall_df = pd.DataFrame([
    {"predicate": pred, "recall@50": v.get("recall@50", 0)}
    for pred, v in recall_data.items()
])

# 合并
df = stats_df.merge(recall_df, on="predicate")

# 相关性分析
for col in ["frequency", "unique_compositions", "coverage_ratio"]:
    r_pearson, p_pearson = pearsonr(df[col], df["recall@50"])
    r_spearman, p_spearman = spearmanr(df[col], df["recall@50"])
    print(f"{col} vs recall@50:")
    print(f"  Pearson r={r_pearson:.3f}, p={p_pearson:.2e}")
    print(f"  Spearman r={r_spearman:.3f}, p={p_spearman:.2e}")

# 关键: 控制 frequency 后，composition coverage 是否还显著
from scipy.stats import pearsonr
df["log_freq"] = df["frequency"].apply(lambda x: max(0, x)).apply(lambda x: math.log(x + 1))

# Partial correlation: recall ~ coverage | frequency
# 对 frequency 做回归取残差，再计算 coverage 与残差的相关性
import statsmodels.api as sm
X = sm.add_constant(df[["log_freq"]])
model = sm.OLS(df["recall@50"], X).fit()
residuals = model.resid
r_partial, p_partial = pearsonr(df["coverage_ratio"], residuals)
print(f"\nPartial correlation (coverage | frequency) vs recall:")
print(f"  r={r_partial:.3f}, p={p_partial:.2e}")
```

---

## Week 2: Baseline 诊断 + 方法设计（6 月 16 日 - 6 月 22 日）

### Step 2.1: 完整 baseline 诊断

在三类 baseline 上跑 complete evaluation:

| Baseline | 类型 | 重要性 |
|----------|------|--------|
| Motifs | 经典 | 必跑 |
| VCTree | 经典 | 必跑 |
| RelTR / EGTR | End-to-end | 可选但加分 |
| TDE (Motifs+TDE) | Causal debias | 必跑（主要对比对象）|
| CFA (Motifs+CFA) | Feature augmentation | 必跑 |

每个 baseline 产生三组指标:

```bash
# 标准 VG150 评估
python tools/eval.py --resume <model_path> \
  --output reports/diagnostic/<method>_standard.json

# Composition seen 评估
python tools/eval.py --resume <model_path> \
  --split_file data/vg150/composition_splits/split_0/test.json \
  --filter_type seen \
  --output reports/diagnostic/<method>_comp_seen.json

# Composition unseen 评估
python tools/eval.py --resume <model_path> \
  --split_file data/vg150/composition_splits/split_0/test.json \
  --filter_type unseen \
  --output reports/diagnostic/<method>_comp_unseen.json
```

#### 预期产出：Figure 2（论文核心 Figure）

```
横轴: Head / Body / Tail
纵轴: mR@50

三条线:
- Standard evaluation
- Composition Seen
- Composition Unseen

预期: Tail Unseen << Tail Seen << Standard
如果 TDE/CFA 在 Tail Seen 上 vs baseline 有提升，
但在 Tail Unseen 上没有，这就是核心 observation。
```

#### OpenSGG 兼容性

| 模型 | OpenSGG 支持 | 需要额外工作 |
|------|-------------|------------|
| Motifs | ✅ | 无 |
| VCTree | ✅ | 无 |
| Transformer | ✅ | 无 |
| TDE | 👷 可能需要补 | 加 causal subtraction |
| CFA | 👷 可能需要补 | 加 feature augmentation module |
| RelTR | ❌ | 需要单独集成 |

---

### Step 2.2: 方法设计定稿

#### CVC: Compositionally Verified Concept Relation Head

**整体架构：**

```
输入:
  - visual_pair_feat (from backbone): v ∈ R^d
  - subject class embedding: e_s ∈ R^d
  - object class embedding: e_o ∈ R^d

┌─────────────────────────────────────────┐
│ Feature Branches                         │
│                                         │
│ 1. Visual Concept Branch (visual only)   │
│    z_v = MLP(v) → R^d                    │
│    不含任何 category 信息                  │
│                                         │
│ 2. Composition Shortcut Branch           │
│    z_bias = MLP([e_s, e_o]) → R^d        │
│    只从 category 预测（估计 shortcut）      │
│                                         │
│ 3. Composition Corrector (CVC)           │
│    对 novel composition，从 seen          │
│    composition 迁移知识                    │
│    delta = Corrector(z_v, e_s, e_o)       │
│    只在识别为 "novel composition" 时激活    │
└─────────────────────────────────────────┘

训练:

p_pred = softmax(linear(z_v))
p_bias = softmax(linear(z_bias))

Loss:
  L = CE(p_pred, y)                         # 主分类损失
    + α * KL(z_v || stopgrad(z_bias))       # 对齐：z_v 不应包含 z_bias 信息
    + β * DiversityLoss(z_v, z_v_pool)       # 原型多样性
    - γ * AdvLoss(p_comp_pred, comp_label)  # 判别器：z_v 不能预测 composition ID
  (注: AdvLoss 用 GRL 实现)

推理:
  logits = W·z_v - λ * W·z_bias
  pred = argmax(logits)

对 novel composition:
  similar_comp = find_nearest_seen(z_v, seen_composition_db)
  z_corrected = z_v + Corrector(z_v, e_s - e_similar, e_o - e_similar)
  logits = W·z_corrected - λ * W·z_bias
```

**关键点：** 这是论文的 method section 核心。简洁但有力。

---

## Week 3-4: 实验 + 写作（6 月 23 日 - 7 月 6 日）

### 实验矩阵

| 实验 | 代码 | 预期 |
|------|------|------|
| Main result: Standard + Composition evaluation | `tools/eval.py` | CVC > baselines |
| Ablation: w/wo CVC Corrector | 去掉 Corrector | mUnseen ↓ |
| Ablation: w/wo Adversarial loss | 去掉 GRL | mUnseen ↓, shortcut bias ↑ |
| Ablation: w/wo Bias subtraction | λ=0 | mR@K ↑ but CompGap ↑ |
| Ablation: Corrector variants | seen similarity metric | Cosine > Euclidean |
| Analysis: Per-predicate comp-gap | 每个 predicate | Tail comp-gap > Head |
| Analysis: Feature visualization | t-SNE of z_v | 解耦效果 |
| Generalization: PSG / GQA | 跨数据集 | 验证泛化性 |

### 写作计划

| 章节 | 主要 figure/table | 完成时间 |
|------|-----------------|---------|
| Figure 1: Freq vs Composition coverage | scatter + H/B/T colormap | Week 1 |
| Figure 2: Baseline comp gap | mR@K grouped bar | Week 2 |
| Table 1: Main results | Standard + Comp metrics | Week 3 |
| Table 2: Ablations | 模块消融 | Week 3 |
| Table 3: Analysis | Per-predicate, correlation | Week 4 |
| Abstract + Intro | Thesis + Contribution bullets | Week 3 |
| Method | Architecture figure | Week 3 |
| Related Work | 4 个方向对比 | Week 4 |

---

## Timeline 汇总

```
Week 1 (6/9 - 6/15):
  1.1  Composition coverage 统计分析 ✓
  1.2  Compositional split 构造
  1.3  Baseline (Motifs) 在 standard + comp seen/unseen 上第一次评估
  1.4  [决策点] 如果结果支持 thesis，继续

Week 2 (6/16 - 6/22):
  2.1  完整 baseline 评估（VCTree, TDE, CFA）
  2.2  CVC method 定稿 + 首次实现
  2.3  CVC 在 PredCLS 上调通

Week 3 (6/23 - 6/29):
  3.1  CVC 完整实验（SGCLS, PredCLS, SGDet）
  3.2  Ablation studies
  3.3  Introduction + Method 写作

Week 4 (6/30 - 7/6):
  4.1  补齐实验（PSG, GQA）
  4.2  Related Work + Analysis
  4.3  全文 polish + supplementary
```

---

## 我现在就帮你做什么

最紧迫的是 Step 1.1 — 在 VG150 上跑 composition coverage 分析。

你需要去你的 OpenSGG 环境里执行以下操作：

```bash
# 1. 检查 VG150 数据格式
head -n 5 data/vg150/VG150_SGG_split.json

# 2. 把上面的 analysis/composition_coverage.py 放进去
cp .../composition_coverage.py tools/analysis/

# 3. 运行
python tools/analysis/composition_coverage.py

# 4. 把输出结果发给我
# (predicate_composition_stats.csv  + freq_vs_composition_coverage.png)
```

告诉我 VG150 在你那边的路径和格式，我能直接给你适配好的脚本。
