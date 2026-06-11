---
title: "Importance Weighted Structure Learning for Scene Graph Generation"
type: paper
domain: scene-graph
status: active
created: 2026-06-10
updated: 2026-06-10
tags: scene-graph-generation, structure-learning, variational-inference, CVPR-2022
source_pages: []
raw_sources:
  - raw/sources/2022-05-17-importance-weighted-structure-learning-for-sgg.pdf
related_pages: []
paper:
  title: "Importance Weighted Structure Learning for Scene Graph Generation"
  authors: "Daqi Liu, Miroslaw Bober, Josef Kittler"
  year: 2022
  venue: "CVPR 2022"
  arxiv: "2205.07017"
  doi: null
  code: null
  project: null
classification:
  label: "scene-graph-generation"
  task: ["Scene Graph Generation"]
  method_family: "Variational Inference, Importance Weighted Lower Bound, Entropic Mirror Descent"
  modality: "Image"
  datasets: ["Visual Genome", "Open Images V6"]
  metrics: ["mR@K", "R@K", "wmAPrel", "wmAPphr"]
evidence_level: full-paper
---

## Citation

Daqi Liu, Miroslaw Bober, Josef Kittler. "Importance Weighted Structure Learning for Scene Graph Generation." CVPR 2022. arXiv:2205.07017.

## One-Sentence Contribution

提出用 importance weighted lower bound 替代传统 ELBO 作为变分推断目标，并结合 entropic mirror descent 求解约束变分推理，提升场景图生成中长尾谓词检测能力。

## Problem Setting

Scene Graph Generation (SGG) 是结构化预测任务：给定输入图像 x，通过 MAP 估计 z\* = arg max_z p_θ(z|x) 推断最优的场景图解释。由于输出变量间存在指数级的依赖关系（m 个物体 + n 个谓词），直接计算 p_θ(z|x) 在计算上不可行。

传统方法使用 mean field variational Bayesian (MFVB) 框架，其中：
- **变分推断**：用完全分解的变分分布 q(z) = Π q_i(z_i) 近似后验 p_θ(z|x)
- **变分学习**：通过交叉熵损失拟合后验
- **推理目标**：经典 ELBO

核心缺陷：ELBO 是高松散的下界，其导出的变分近似低估了底层复杂的后验分布，导致生成性能不理想。

## Method

### 核心创新

1. **Importance Weighted Lower Bound (IWLB)**：用 s 样本重要性加权下界 L_s 替代 ELBO：
   - L_s = E_{z^1,...,z^s~q(z)}[log (1/s) Σ_i s_θ(x,z^i)/q(z^i)]
   - s=1 时退化为 ELBO
   - s → ∞ 时成为 log 配分函数的无偏估计
   - 任意 s > 1 都比 ELBO 更紧

2. **Gumbel-Softmax Sampler**：从可重参数化的 Gumbel-Softmax 分布中采样可微的类别变量，替代传统不可微的分类采样，支持梯度回传

3. **Entropic Mirror Descent (EMD)**：求解约束优化问题（π ∈ Δ^{v-1} 概率单纯形），比传统投影梯度法收敛更快

4. **全局上下文建模**：引入全局区域提案 b_g 和全局特征 y_g，通过 pairwise 势函数 ψ^p_b(x_p_j, x_g, z_p_j, z_g) 和 ψ^o_b(x_o_i, x_g, z_o_i, z_g) 融入全局上下文信息

### Scoring Function

对数评分函数包含：
- 物体单势 ψ^o_u(x_o_i, z_o_i)
- 谓词单势 ψ^p_u(x_p_j, z_p_j)
- 物体-谓词对势 ψ^o_b(x_o_i, x_p_j, z_o_i, z_p_j)
- 物体-物体对势 ψ^o_b(x_o_i, x_o_l, z_o_i, z_o_l)
- 物体-全局对势 ψ^o_b(x_o_i, x_g, z_o_i, z_g)
- 谓词-全局对势 ψ^p_b(x_p_j, x_g, z_p_j, z_g)

特征学习函数 (h_o_θ, h_p_θ, g_op_θ, g_oo_θ, g_og_θ, g_po_θ, g_pg_θ) 由视觉感知模块 + MLP 构成。

### 算法流程

1. 随机初始化 θ
2. 对每个迭代：
   - 随机初始化 π
   - 从 Gumbel 分布中采样 s 个噪声
   - 通过 Gumbel-Softmax 重参数化计算输出样本
   - 计算重要性权重和 IWLB
   - 用 EMD 求解约束优化更新 π
   - 从更新后的 π 计算 surrogate logit φ 和 logp_θ(z|x)
   - 交叉熵损失更新 θ
   - 退火温度 τ

## Experiments

### Visual Genome

**数据集配置**：
- 108,077 张图像，平均每张 38 个物体、22 个关系
- 选最常见 150 个物体类别和 50 个谓词类别
- 训练集 70% / 测试集 30%，验证集从训练集随机选 5k
- 按训练样本数分为 head(>10k)、body(0.5k~10k)、tail(<0.5k)

**评估协议**：
- 主要指标：mean Recall@K (mR@K)
- 三个子任务：PredCls / SGCls / SGDet

**实现细节**：
- Backbone：ResNeXt-101-FPN
- 检测器：Faster-RCNN
- 训练策略：step training，冻结视觉感知模型
- 数据重采样：bi-level resampling（image-level over-sampling t=0.07 + instance-level under-sampling γ_d=0.7）
- Batch size：12
- 优化器：SGD，lr = 0.008 × bs
- 变分推理样本数 s=50，变分学习样本数 s=8000(SGDet)/5000(PredCls,SGCls)
- 训练迭代：4000

**Baseline 方法**：RelDN, Motifs, G-RCNN, MSDN, GPS-Net, VCTree-TDE, BGNN

### Open Images V6

**数据集配置**：
- 126,368 训练图像、5,322 测试图像、1,813 验证图像
- 采用 [19][39][51] 的数据处理协议

**评估协议**：
- mR@50, R@50, wmAPrel, wmAPphr
- Weighted score = 0.2×R@50 + 0.4×wmAPrel + 0.4×wmAPphr

**实现细节**：
- Backbone：ResNeXt-101-FPN
- 检测器：Faster-RCNN
- Batch size：12
- 优化器：Adam, lr=0.0001
- 变分推理 s=50，变分学习 s=5000

### Ablation Study

消融数量样本对 SGDet 性能的影响（Visual Genome）：

| s | mR@20 | mR@50 | mR@100 |
|---|-------|-------|--------|
| 10 | 9.9 | 13.1 | 15.5 |
| 30 | 10.7 | 13.5 | 15.6 |
| 50 | 10.6 | 13.7 | 15.9 |

s>50 后性能提升不明显但计算成本急剧增加，因此 s=50。

## Results

### Visual Genome — 主要结果 (Table 1)

| Method | PredCls mR@50/100 | SGCls mR@50/100 | SGDet mR@50/100 | SGDet(R@100) Head/Body/Tail/Mean |
|--------|-------------------|-----------------|-----------------|----------------------------------|
| BGNN (SOTA) | 30.4/32.9 | 14.3/16.5 | 10.7/12.6 | 33.4/13.4/6.4/17.7 |
| **IWSL** | **30.0/32.1** | **17.4/18.9** | **13.7/15.9** | **30.6/16.5/10.7/19.3** |

- SGDet mR@50：IWSL 13.7 vs. BGNN 10.7，提升 **28%**
- SGDet mR@100：IWSL 15.9 vs. BGNN 12.6，提升 **26.2%**
- Body 组 R@100：IWSL 16.5 vs. BGNN 13.4
- Tail 组 R@100：IWSL 10.7 vs. BGNN 6.4
- PredCls 与 BGNN 相当（略低 0.4 mR@50）

### Visual Genome — Balance Adjustment (Table 2)

| Method | PredCls mR@50/100 | SGCls mR@50/100 | SGDet mR@50/100 |
|--------|-------------------|-----------------|-----------------|
| Motifs+BA | 29.7/31.7 | 16.5/17.5 | 13.5/15.6 |
| VCTree+BA | 30.6/32.6 | 20.1/21.2 | 13.5/15.7 |
| Transformer+BA | 31.9/34.2 | 18.5/19.4 | 14.8/17.1 |
| **IWSL+BA** | **36.9/39.2** | **20.7/22.2** | **16.1/18.6** |

- PredCls mR@50：IWSL+BA 36.9 vs. Transformer+BA 31.9，提升 **15.7%**
- 提升主要来自：1) semantic adjustment 的转移矩阵映射到更有信息的预测；2) balanced predicate learning 丢弃 head 组冗余样本、保留 body/tail 组样本

### Open Images V6 (Table 3)

| Method | mR@50 | R@50 | wmAPrel | wmAPphr | score_wtd |
|--------|-------|------|---------|---------|-----------|
| BGNN | 40.45 | 74.98 | 33.51 | 34.15 | 42.06 |
| **IWSL** | **42.18** | 74.68 | 33.11 | 34.33 | 41.87 |

- mR@50：IWSL 42.18 vs. BGNN 40.45，领先 **1.73 个百分点**
- 其他指标与 BGNN 相当或略低

## Limitations

1. **计算开销**：s=50 样本时性能最优，但 s>50 后计算成本急剧增长，限制更大样本量应用
2. **PredCls 未超越**：在 Visual Genome PredCls 任务上 IWSL (30.0) 略低于 BGNN (30.4)，表明使用更多训练信息时（ground-truth box 和 label），IWLB 的优势不显著
3. **无代码开源**：论文未提供代码链接，可复现性存疑
4. **仅两数据集验证**：仅在 VG 和 OI V6 上验证，泛化性有待更多 benchmark 检验

## Reusable Claims

1. **IWLB > ELBO**：重要性加权下界（s>1）严格优于 ELBO，能有效缓解变分后验低估问题，适用于结构化预测任务
2. **EMD 替代 MPNN**：Entropic Mirror Descent 收敛快于传统消息传递策略，适合求解概率单纯形约束的变分推理
3. **长尾提升明显**：IWLB 结合 EMD 特别有利于提高 body 和 tail 组的谓词检测性能（Body R@100 16.5, Tail R@100 10.7）
4. **与 BA 策略互补**：IWSL+BA 进一步大幅提升 PredCls 性能（mR@50 从 30.0 升至 36.9）

## Connections

- 方法论直接继承自 **IWAE** (Burda et al., ICLR 2016)：将重要性加权变分下界从生成模型推广到结构化预测
- 与 **BGNN** (Li et al., CVPR 2021) 直接对比：用 IWLB+EMD 替代传统 MPNN-based MFVI
- Gumbel-Softmax 采样器来自 **Categorical Reparameterization** (Jang et al., ICLR 2017) 和 **Concrete Distribution** (Maddison et al., ICLR 2017)
- 平衡调整策略 BA 来自 **From General to Specific** (Guo et al., ICCV 2021)
- 与因果去偏方法 **VCTree-TDE** (Tang et al., CVPR 2020) 的方向不同但互补

## Open Questions

1. IWSL 在 PredCls 任务上未能超越 BGNN，是否意味着 ground-truth 信息充沛时 ELBO 已足够好？
2. 更大样本量（s > 50）的探索受限，是否有更高效的 IWLB 近似方法可降低计算开销？
3. IWSL+BA 将 semantic adjustment 和 IWLB 结合的效果机制需要进一步分析
4. 能否将 IWLB 推广到其他结构化预测任务（如人体姿态估计、语义解析等）？
5. 无开源代码，核心方法（EMD 求解变分推理）的实现细节需要复现验证

## Provenance

- 原始 PDF：raw/sources/2022-05-17-importance-weighted-structure-learning-for-sgg.pdf (arXiv:2205.07017, 11 pages)
- 全文提取：raw/sources/2022-05-17-importance-weighted-structure-learning-for-sgg.txt (57,576 chars)
- 提取质量：良好，保留标题、摘要、方法、实验表格、参考文献
- 证据等级：full-paper — 全文精读，表格数据完整捕获
