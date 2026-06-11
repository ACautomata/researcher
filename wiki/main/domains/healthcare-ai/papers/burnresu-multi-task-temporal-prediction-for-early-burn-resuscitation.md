---
title: "BurnResu: A Multi-Task Temporal Prediction Framework for Early Burn Resuscitation"
type: paper
domain: healthcare-ai
status: active
created: 2026-06-05
updated: 2026-06-05
tags:
  - burn-resuscitation
  - multi-task-learning
  - temporal-modeling
  - clinical-decision-support
  - deep-learning
raw_sources:
  - ../../../sources/2026-BurnResu-Multi-Task-Temporal-Prediction-Framework-for-Early-Burn-Resuscitation.pdf
  - ../../../sources/2026-BurnResu-Multi-Task-Temporal-Prediction-Framework-for-Early-Burn-Resuscitation.txt
paper:
  title: "BurnResu: A Multi-Task Temporal Prediction Framework for Early Burn Resuscitation"
  authors:
    - Xinyu Liu
    - Jingyuan Lang
    - Xiaoguang Lin
    - Haisheng Li
    - Ranran Sun
    - Xueliang Zhao
    - Qihan Wu
    - Zhiqiang Yuan
    - Ning Li
    - Gaoxing Luo
  year: 2026
  venue: "Expert Systems with Applications (submitted)"
  doi: null
  arxiv: null
  code: "https://github.com/Aveouter/BurnResu"
  project: null
classification:
  label: "Clinical Decision Support / Temporal Deep Learning"
  task:
    - Fluid-type classification (crystalloid, colloid, glucose)
    - Infusion-rate regression
  method_family:
    - Multi-task learning
    - Temporal convolutional network
    - Causal self-attention
    - FiLM-based conditioning
    - Zero-inflated log-normal regression
  modality:
    - Vital signs (HR, BP, SpO2, CVP, RR, temperature)
    - Baseline demographics (age, BMI, TBSA, inhalation injury)
    - Fluid administration history
  datasets:
    - Single-center burn resuscitation dataset (364 patients, Southwest Hospital, Chongqing, 2016–2023)
  metrics:
    - AUC
    - Macro-F1
    - MAE
    - R²
    - RMSE
evidence_level: full-paper
---

## Citation

> Xinyu Liu, Jingyuan Lang, Xiaoguang Lin, Haisheng Li, Ranran Sun, Xueliang Zhao, Qihan Wu, Zhiqiang Yuan, Ning Li, Gaoxing Luo. "BurnResu: A Multi-Task Temporal Prediction Framework for Early Burn Resuscitation." Submitted to *Expert Systems with Applications* (Manuscript ESWA-D-26-21224). 2026.

## One-Sentence Contribution

提出 BurnResu，一个分层时序深度学习框架，联合预测烧伤休克复苏中的输液类型（晶体/胶体/葡萄糖）和输液速率，在 364 例重度烧伤患者回顾性队列上 AUC 0.816、MAE 27.44 mL/h。

## Problem Setting

**临床背景**：烧伤休克是重度烧伤（TBSA>30%）患者早期死亡的主要原因。液体复苏需要在低灌注与液体过载之间取得平衡。临床常用 Parkland、Brooke、TMMU 等经验公式，但这些公式提供群体水平估计，无法适应个体患者的血流动力学演变。

**任务定义**：在伤后 72 小时内，每小时预测下一小时的输液类型（晶体液/胶体液/葡萄糖）及对应的输液速率。这是一个滚动预测问题：每个时间点用截止到该时刻的所有可用信息进行预测。

**数据特点**：异质性顺序数据，包括基线特征（TBSA、年龄、吸入性损伤等）、每小时生命体征、尿量、既往输液历史。数据存在缺失值和不规则采样问题。

**挑战**：
1. 输液决策包含分类（选择哪种液体）和回归（多大速率）两个耦合任务
2. 生理信号存在多尺度时间依赖（分钟级血流动力学反应 vs. 小时级体液转移）
3. 真实世界临床数据存在缺失、噪声和不规则性
4. 预测结果需要时间一致性和生理合理性（不能出现突变的输液轨迹）

## Method

### 整体架构

BurnResu 采用三级分层架构，模拟临床推理过程：

1. **Baseline Encoder**：将静态人口学/伤情特征（TBSA、年龄、BMI、吸入性损伤等）映射到潜在嵌入 **b'** ∈ ℝ^128，为下游时间推理提供患者特异性初始化。

2. **Multi-Scale Temporal Encoder**：双路径设计——
   - **Dilated TCN 路径**：4 个残差块，卷积核 3，膨胀率 {1,2,4,8}，指数增长感受野，编码细粒度局部动态 {**h**_t}
   - **Causal Self-Attention 路径**：2 层，4 头注意力，前馈维度 256，建模长程跨特征交互，严格因果掩码防止未来信息泄露
   - 两条路径输出融合为统一时间状态

3. **Conditioned Decoder**：通过 FiLM 机制将基线嵌入 **b'** 调制到时间特征上——
   - **h̃**_t = (1 + tanh(γ)) ⊙ **h**_t + β，其中 γ, β 由 **b'** 通过可学习的仿射变换派生
   - 使相同的时间模式能根据患者临床背景产生不同输液响应
   - 分类头预测液体类型（晶体/胶体/葡萄糖），Zero-Inflated Log-Normal (ZILN) 回归头估计相应输液速率

### 损失函数

多目标联合损失：L = λ_cls L_cls + L_reg + L_tem

- **L_cls**：Tversky loss，平衡类别不平衡下的精确率和召回率
- **L_reg** = λ_cum L_cum + λ_pos L_pos：L_cum 惩罚累积剂量偏差；L_pos 仅在输液发生时应用 log-transformed Huber loss
- **L_tem** = λ_cp L_cp + λ_tv L_tv + λ_pre L_pre：变化点惩罚（输液开始/停止）、总变分约束（抑制振荡）、预条件化（稳定早期预测）
- 权重：λ_cls=1.0, λ_cum=0.5, λ_pos=1.0, λ_cp=0.1, λ_tv=0.05, λ_pre=0.05（验证集网格搜索确定）

### 数据预处理

- 缺失值：单独神经网络插补模型（仅在训练集上拟合），前向方式使用过去和同期观测值
- 患者级划分，不跨 set 泄漏
- 基线特征在入院时记录；时序变量按时间对齐并截断

## Experiments

### 数据集

- **来源**：西南医院烧伤研究所（陆军军医大学），2016.7–2023.12
- **纳入标准**：TBSA > 30%，伤后 48h 内入院
- **排除标准**：病历不完整，未入 ICU
- **最终队列**：364 例患者（451 例初筛）
- **患者特征**：男性 74.66%，中位年龄 45 岁，中位 BMI 22.9 kg/m²，中位 TBSA 45%，吸入性损伤 14.6%
- **划分**：患者级随机划分 70%/15%/15%（训练/验证/测试）
- **时间范围**：伤后 72 小时，每小时预测窗口

### Baseline 方法

**机器学习模型**：Regression、Random Forest、SVM、XGBoost、GBR
**深度学习模型**：LSTM、CNN、Transformer
**开放循环 CDSS**：Salinas et al. 模型（指数衰减曲线 + 尿量引导调整）
**消融变体**：4 种架构消融（w/o Temporal Enc./w/o Baseline Enc./w/o self-attention/w/o TCN/w/o FiLM）

### 训练设置

- **框架**：PyTorch 1.13
- **硬件**：NVIDIA A100 GPU
- **优化器**：Adam，学习率 1×10⁻³，StepLR 每 100 epoch 衰减
- **训练轮数**：最多 500 epoch，early stopping 基于验证集
- **推理速度**：每患者完整 72h 轨迹 < 5秒

### 评估指标

- **分类**：Macro-F1（主要）、AUC、Accuracy、Recall
- **回归**：MAE、R²、RMSE（仅正流期间计算）
- 决策阈值通过验证集温度缩放和阈值优化确定

### 消融实验

| 变体 | AUC | F1 | MAE | RMSE |
|------|:---:|:--:|:---:|:----:|
| w/o Temporal Enc. | 0.703 | 0.629 | 72.42 | 110.5 |
| w/o Baseline Enc. | 0.735 | 0.652 | 74.32 | 120.8 |
| w/o self-attention | 0.814 | 0.633 | 74.67 | 112.7 |
| w/o TCN | 0.810 | 0.693 | 27.63 | 60.59 |
| w/o FiLM | 0.806 | 0.683 | 28.88 | 64.12 |
| **BurnResu (Full)** | **0.816** | **0.743** | **27.44** | **60.04** |

消融发现：移除时序编码器（Temporal Enc.）导致性能最大降幅（AUC↓0.113，MAE↑44.98），确认时序生理动态是主要信息源。移除基线编码或 FiLM 调节也各有可量化退化。

## Results

### 主要结果（表3）

| 模型 | Acc | Recall | F1 | AUC | MAE | R² | RMSE |
|------|:---:|:------:|:--:|:---:|:---:|:-:|:----:|
| GBR | 0.727 | 0.761 | 0.672 | 0.763 | **30.62** | 0.759 | 69.42 |
| LSTM | 0.736 | 0.768 | 0.687 | 0.798 | 73.86 | 0.286 | 119.6 |
| CNN | 0.747 | 0.781 | 0.688 | 0.803 | 27.78 | 0.810 | 61.59 |
| Transformer | 0.744 | 0.747 | 0.690 | 0.804 | 30.90 | 0.795 | 63.98 |
| **BurnResu (Full)** | **0.742** | **0.813** | **0.743** | **0.816** | **27.44** | **0.820** | **60.04** |
| Salinas CDSS | — | — | — | — | 76.8 | 0.18 | 129.7 |

- **流体类型分类**：macro-AUC 0.816，macro-F1 0.696
  - 晶体：Precision 0.685, Recall 0.836, F1 0.752, AUC 0.794
  - 胶体：Precision 0.668, Recall 0.798, F1 0.727, AUC 0.834
  - 葡萄糖：Precision 0.492, Recall 0.801, F1 0.609, AUC 0.820
- **输液速率估计**：MAE 27.44 mL/h, R² 0.820, RMSE 60.04 mL/h
- **与传统公式对比**：BurnResu 各类别平均相对误差均控制在 40% 以内，Day 2 优势尤为显著——传统公式由于动态生理变化而偏差最大
- **ROC-AUC 对比**：传统 ML 方法 AUC 0.72–0.80（曲线较平），深度学习方法持续更好，BurnResu 达到最陡起步和最大 AUC（0.816）

### 临床效用

- 72 小时累计输液量预测与真实临床记录高度匹配
- 能捕捉早期大容量复苏和后期控制性缩减的两个阶段
- 保持合理的组分比例（晶体/胶体/葡萄糖），超越固定公式假设的个性化能力

## Limitations

1. **纯监督学习**：依赖高质量标注数据，未来可探索自监督或强化学习
2. **单中心回顾性数据**：限制泛化能力，需要多中心验证
3. **决策建模而非效果研究**：模型学习的是临床医生的实际行为模式（可能非最优），不等于治疗最优性，不建立因果疗效证据
4. **葡萄糖预测变异性高**（F1 0.609, Precision 0.492）：与临床实践中葡萄糖使用不频繁且依赖个体化判断有关
5. 需要前瞻性研究支持临床部署

## Reusable Claims

> **Claim**: 多尺度时序架构（Dilated TCN + Causal Self-Attention）在中等规模临床队列（n=364）上优于纯 LSTM 或 Transformer 基线
> **Evidence**: 表3：BurnResu AUC 0.816 vs. LSTM 0.798, Transformer 0.804; R² 0.820 vs. LSTM 0.286, Transformer 0.795
> **Scope**: 单中心烧伤复苏数据集
> **Confidence**: medium（单中心）

> **Claim**: 时序生理动态是输液需求的主要信息源——移除时序编码器后 AUC 从 0.816 降至 0.703（↓13.9%），MAE 从 27.44 升至 72.42（↑164%）
> **Evidence**: 表4：消融实验
> **Scope**: 同一数据集
> **Confidence**: medium

> **Claim**: FiLM 调节机制提供患者特异性适应，在几乎不增加参数的情况下优于简单特征拼接（AUC 0.816 vs. 0.806）
> **Evidence**: 表4
> **Scope**: 同一数据集
> **Confidence**: medium

> **Claim**: 包含累积剂量保真度、变化点惩罚和总变分约束的决策优先损失函数优于标准逐点回归损失
> **Evidence**: 表4 与其他 DL 基线对比。联合任务配方使 MAE 27.44 明显低于单任务 LSTM 73.86
> **Scope**: 同一数据集
> **Confidence**: medium

## Connections

- **Salinas et al. (2011)**：开放循环 CDSS，使用指数衰减曲线 + 尿量引导调整；BurnResu 将其用作基线（AUC 不适用，MAE 76.8 vs. 27.44）
- **Multi-task learning**：Caruana (1997) 奠定理论基础；本工作扩展了联合分类-回归范式到烧伤复苏
- **FiLM**：Perez et al. (2018) 视觉推理中的特征线性调节层；本工作将其引入临床时序建模
- **Temporal modeling**：TCN (Bai et al. 2018) + Transformer 双路径设计

## Open Questions

1. 是否能在多中心数据上保持 AUC > 0.80？
2. 葡萄糖预测的高精度（Recall 0.801）与低精确率（Precision 0.492）矛盾，是否有更好的类别平衡策略？
3. 模型学的"临床决策模式"与实际最优治疗策略之间的差距有多大？
4. 能否通过强化学习从回顾性决策模式进一步优化到治疗策略？
5. 模型在高变异患者（如老年、吸入性损伤）上的分层性能如何？

## Provenance

- **PDF 源文件**：`sources/2026-BurnResu-Multi-Task-Temporal-Prediction-Framework-for-Early-Burn-Resuscitation.pdf`
- **提取文本**：`sources/2026-BurnResu-Multi-Task-Temporal-Prediction-Framework-for-Early-Burn-Resuscitation.txt`
- **提取日期**：2026-06-05
- **证据等级**：full-paper（全文精读，提取 54K 字符，覆盖所有主要章节、表 1-5、图 1-6）
- **处理方法**：PyMuPDF 提取全文文本 → 结构化分析 → 创建 paper page
