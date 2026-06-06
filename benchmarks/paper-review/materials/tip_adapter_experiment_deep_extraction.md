# Tip-Adapter 实验深化提取

## 0. 文档定位

- **输入材料**：`materials/tip_adapter_full.md`（Tip-Adapter 论文全文，arXiv 2207.09519，22页）
- **当前阶段**：S2 实验深化提取
- **包含**：实验目标、实验设置、主结果、消融实验、参数分析、效率代价、鲁棒性泛化性、实验现象、证据充分性
- **不包含**：完整问题挖掘、最终结论、方法改进方案（留待 S3/S4/S5）

---

## 1. 实验目标与作者想验证的核心结论

### 核心结论 1：Training-free cache model 可以达到与 training-required 方法相当的性能

- **对应实验**：Table 1 (16-shot ImageNet)、Table 2 (ImageNet 所有 shot)、Figure 5 (10 个数据集)
- **证据**：Tip-Adapter 无需训练在 16-shot ImageNet 上达到 62.03%，超过 Zero-shot CLIP (+1.70%)，接近 CLIP-Adapter 63.59% 和 CoOp 62.95%（两者均需 200 epoch 训练）

### 核心结论 2：Tip-Adapter-F 以极少的训练 epoch 达到 SOTA

- **对应实验**：Table 1 (效率对比)、Table 2 (ImageNet 所有 shot)、Figure 5 (10 个数据集)
- **证据**：Tip-Adapter-F 仅需 20 epoch (5 分钟) 在 16-shot ImageNet 上达到 65.51%，超越 CLIP-Adapter 的 200 epoch (50 分钟) 和 CoOp 的 200 epoch (14 小时 40 分钟)

### 核心结论 3：Fine-tuning keys（而非 values 或 CLIP encoders）是最优的微调策略

- **对应实验**：Table 6 (Appendix A，不同模块微调对比)
- **证据**：仅微调 Ftrain 达到 65.51%（5分钟），微调 Ltrain 降至 60.90%，同时微调 CLIP visual + textual encoder 导致过拟合降至 51.22%

### 核心结论 4：Cache model 在不同视觉 backbone 上均有效

- **对应实验**：Table 3 (不同视觉编码器，16-shot ImageNet)
- **证据**：Tip-Adapter-F 在 ResNet-50 (65.51)、ResNet-101 (68.56)、ViT-B/32 (68.65)、ViT-B/16 (73.69)、RN50x16 (75.81) 上均超越所有 baseline

### 核心结论 5：Cache model 具有更强的分布偏移鲁棒性

- **对应实验**：Table 5 (ImageNet → ImageNetV2, ImageNet-Sketch)
- **证据**：Tip-Adapter 在 ImageNet-Sketch 上 35.90% 超越 CLIP-Adapter 35.68% 和 CoOp 31.04%，训练无关的 cache 构造减轻了过拟合风险

---

## 2. 实验设置总览

### 数据集

| 数据集 | 类型 | 类别数 | 测试集规模 | 评估指标 | 来源 |
|--------|------|--------|-----------|---------|------|
| ImageNet | 通用图像分类 | 1000 | 完整测试集 | Top-1 Accuracy (%) | Deng et al., 2009 |
| StanfordCars | 细粒度汽车分类 | 196 | 完整测试集 | Top-1 Accuracy (%) | Krause et al., 2013 |
| UCF101 | 动作识别 | 101 | 完整测试集 | Top-1 Accuracy (%) | Soomro et al., 2012 |
| Caltech101 | 通用物体识别 | 101 | 完整测试集 | Top-1 Accuracy (%) | Fei-Fei et al., 2004 |
| Flowers102 | 细粒度花卉分类 | 102 | 完整测试集 | Top-1 Accuracy (%) | Nilsback & Zisserman, 2008 |
| SUN397 | 场景识别 | 397 | 完整测试集 | Top-1 Accuracy (%) | Xiao et al., 2010 |
| DTD | 纹理分类 | 47 | 完整测试集 | Top-1 Accuracy (%) | Cimpoi et al., 2014 |
| EuroSAT | 卫星图像分类 | 10 | 完整测试集 | Top-1 Accuracy (%) | Helber et al., 2019 |
| FGVCAircraft | 细粒度飞行器分类 | 100 | 完整测试集 | Top-1 Accuracy (%) | Maji et al., 2013 |
| OxfordPets | 宠物分类 | 37 | 完整测试集 | Top-1 Accuracy (%) | Parkhi et al., 2012 |
| Food101 | 食物分类 | 101 | 完整测试集 | Top-1 Accuracy (%) | Bossard et al., 2014 |

来源：Section 4.1, Page 9

### Few-shot 设置

- Shot 数：1, 2, 4, 8, 16
- 测试方式：使用完整测试集进行评估（full test sets），与传统 full-training 方法一致
- 每个 shot 设定：每个类别选取 K 张标注图像用于训练
- 来源：Section 4.1, Page 9

### Baseline 方法

| 方法 | 类型 | 训练方式 | 说明 |
|------|------|---------|------|
| Zero-shot CLIP | 零样本 | 无训练 | 纯预训练知识，无额外训练样本 |
| Linear-probe CLIP | 线性探针 | 训练线性分类器 | 在 frozen CLIP 后训练额外线性分类器 |
| CoOp | 提示学习 | 训练 learnable prompts | 16-token prompts，class token 放在末尾，无 class-specific context |
| CLIP-Adapter | 特征适配器 | 训练两层 MLP | 仅使用 visual adapter 的最佳变体 |
| Tip-Adapter (ours) | 缓存模型适配 | 无训练 | Key-value cache model，训练无关 |
| Tip-Adapter-F (ours) | 缓存模型适配 | Fine-tune keys | 仅微调 cache keys，20 epoch |

来源：Section 4.1, Page 9

### 模型与训练配置

| 配置项 | 值 |
|--------|---|
| 视觉编码器 (默认) | ResNet-50 |
| 文本编码器 | Transformer |
| 编码器权重来源 | CLIP 预训练权重 [48]，训练时冻结 |
| 数据预处理 | 随机裁剪、缩放、随机水平翻转（同 CLIP 协议） |
| 提示策略 | ImageNet：7 模板 prompt ensembling；其他 10 数据集：单一半手工 prompt |
| Batch size (Tip-Adapter-F) | 256 |
| Learning rate (Tip-Adapter-F) | 0.001 |
| 优化器 | AdamW + cosine scheduler |
| 训练 epoch | 10 个数据集：20 epoch；EuroSAT：100 epoch |
| Tip-Adapter 超参 α | 默认 1.0 |
| Tip-Adapter 超参 β | 默认 5.5 |

来源：Section 4.1, Pages 9-10

### 论文未提供的实验设置信息

- 具体的 prompt ensembling 7 模板内容（论文引用 [48] 但未在本论文中列出）
- 其他 10 数据集使用的单一半手工 prompt 的具体文本
- GPU 型号详细信息（仅提及 RTX 3090）
- 代码依赖库版本
- 数据增强的详细参数（如裁剪尺寸等）
- 随机 seeds 列表

---

## 3. 主结果提取

### ImageNet (Table 2, Figure 4)

| Shot | Zero-shot CLIP | Linear-probe CLIP | CoOp | CLIP-Adapter | Tip-Adapter | Tip-Adapter-F |
|------|---------------|-------------------|------|-------------|-------------|---------------|
| 1-shot | 60.33 | 22.17 | 57.15 | 61.20 | 60.70 | 61.32 |
| 2-shot | 60.33 | 31.90 | 57.81 | 61.52 | 60.96 | 61.69 |
| 4-shot | 60.33 | 41.20 | 59.99 | 61.84 | 60.98 | 62.52 |
| 8-shot | 60.33 | 49.52 | 61.56 | 62.68 | 61.45 | 64.00 |
| 16-shot | 60.33 | 56.13 | 62.95 | 63.59 | 62.03 | 65.51 |

来源：Table 2, Page 9

**关键数字**：
- Tip-Adapter (无训练) vs Zero-shot CLIP: 在所有 shot 上均超越 Zero-shot CLIP，16-shot 时 +1.70%
- Tip-Adapter vs Linear-probe CLIP (1-shot): +38.53%（60.70 vs 22.17）
- Tip-Adapter vs Linear-probe CLIP (2-shot): +29.06%（60.96 vs 31.90）
- Tip-Adapter-F 相对于 Tip-Adapter 的增量：1-shot +0.62%, 2-shot +0.73%, 4-shot +1.54%, 8-shot +2.55%, 16-shot +3.48%
- Tip-Adapter-F 16-shot 65.51% 为所有方法最优

来源：Section 4.2, Page 10

### 效率对比 (Table 1, 16-shot ImageNet)

| 方法 | 训练需求 | 训练 Epoch | 训练时间 | 准确率 | 准确率增益 | 推理速度 | GPU 显存 |
|------|---------|-----------|---------|--------|-----------|---------|---------|
| Zero-shot CLIP | 无需训练 | 0 | 0 | 60.33 | 0 | 10.22ms | 2227MiB |
| Linear-probe CLIP | 需要 | - | 13min | 56.13 | -4.20 | - | - |
| CoOp | 需要 | 200 | 14h 40min | 62.95 | +2.62 | 299.64ms | 7193MiB |
| CLIP-Adapter | 需要 | 200 | 50min | 63.59 | +3.26 | 10.59ms | 2227MiB |
| Tip-Adapter | 无需训练 | 0 | 0 | 62.03 | +1.70 | 10.42ms | 2227MiB |
| Tip-Adapter-F | 需要 | 20 | 5min | 65.51 | +5.18 | 10.53ms | 2227MiB |

来源：Table 1, Page 2

**关键数字**：
- Tip-Adapter-F 训练时间仅为 CLIP-Adapter 的 1/10 (5min vs 50min)，准确率提升 +1.92% (65.51 vs 63.59)
- Tip-Adapter-F 训练时间仅为 CoOp 的 1/176 (5min vs 14h40min)，准确率提升 +2.56% (65.51 vs 62.95)
- Tip-Adapter 推理速度 10.42ms 几乎等同于 Zero-shot CLIP 的 10.22ms（仅增加 0.20ms）
- Tip-Adapter GPU 显存 2227MiB，与 Zero-shot CLIP 相同；CoOp 需要 7193MiB（3.2 倍）

来源：Section 4.2, Page 10

### 不同视觉编码器结果 (Table 3, 16-shot ImageNet)

| 方法 | ResNet-50 | ResNet-101 | ViT-B/32 | ViT-B/16 | RN50x16 |
|------|-----------|-----------|----------|----------|---------|
| Zero-shot CLIP | 60.33 | 62.53 | 63.80 | 68.73 | 70.94 |
| CoOp | 62.95 | 66.60 | 66.85 | 71.92 | - |
| CLIP-Adapter | 63.59 | 65.39 | 66.19 | 71.13 | - |
| Tip-Adapter | 62.03 | 64.78 | 65.61 | 70.75 | 72.95 |
| Tip-Adapter-F | **65.51** | **68.56** | **68.65** | **73.69** | **75.81** |

来源：Table 3, Page 10

**关键数字**：
- Tip-Adapter-F 在所有编码器上均为最优
- CoOp 在 RN50x16 上的结果未提供（论文标注 "-"）
- CLIP-Adapter 在 RN50x16 上的结果未提供（论文标注 "-"）
- Tip-Adapter-F (RN50x16) 75.81% 为所有编码器配置下最高值

来源：Section 4.2, Page 10

### 其他 10 个数据集结果 (Figure 5)

**16-shot 下各数据集 Zero-shot CLIP 基线及 Tip-Adapter/Tip-Adapter-F 性能（从图中读取近似值）：**

| 数据集 | Zero-shot CLIP | Tip-Adapter (约) | Tip-Adapter-F (约) |
|--------|---------------|-----------------|-------------------|
| EuroSAT | ~53 | ~86 | ~90+ |
| Flowers102 | ~66 | ~90 | ~93+ |
| DTD | ~43 | ~62 | ~65+ |
| FGVCAircraft | ~18 | ~31 | ~36 |
| StanfordCars | ~59 | ~70 | ~75 |
| UCF101 | ~65 | ~74 | ~78 |
| SUN397 | ~62 | ~70 | ~74 |
| Caltech101 | ~88 | ~92 | ~93 |
| OxfordPets | ~86 | ~88 | ~90 |
| Food101 | ~77 | ~78 | ~80 |

来源：Figure 5, Page 11

**关键数字**：
- Tip-Adapter 在所有 10 个数据集上均提升 Zero-shot CLIP（无训练）
- EuroSAT 上提升最大（约 33 个百分点）
- Tip-Adapter-F 在所有数据集上一致最优

来源：Section 4.3, Page 11

### 论文未提供的主结果信息

- 10 个数据集的具体数值（仅以折线图 Figure 5 呈现，无表格数值）
- 各个 shot 在 10 个数据集上的完整数值（Figure 5 为折线图，仅能读出趋势）
- 不同 backbone 在其他 10 个数据集上的结果
- Tip-Adapter 和 Tip-Adapter-F 在更多 shot（32/64/128）下在其他数据集上的结果
- 多次运行的均值和标准差

---

## 4. 消融实验提取

### 消融 1：Residual Ratio α

- **消融内容**：控制 cache model 预测与 CLIP 预训练预测的融合比例
- **测试变体**：α = 0.0, 0.5, 1.0, 2.0, 3.0, 4.0（β 固定为 5.5）
- **揭示结果**：
  - α = 0.0 时为 Zero-shot CLIP（60.33%）
  - α = 1.0 时最优（62.03%），说明先验知识与 few-shot 知识同等重要
  - α > 1.0 时性能下降（α=4.0 时降至 59.14%），说明过量使用 few-shot 知识有害
- **来源**：Table 4 (顶部), Section 4.4, Page 12

### 消融 2：Sharpness Ratio β

- **消融内容**：控制激活函数 φ 中相似度的锐度
- **测试变体**：β = 1.5, 3.5, 5.5, 7.5, 9.5, 11.5（α 固定为 1.0）
- **揭示结果**：
  - β 的变化对性能影响有限（61.40%~62.03%）
  - β = 5.5 时最优（62.03%）
  - 过大的 β 使仅有最相似样本产生大权重，过小的 β 使各样本权重均匀化
- **来源**：Table 4 (第二部分), Section 4.4, Page 12

### 消融 3：Cache 大小

- **消融内容**：在 16-shot 训练集中，随机分组构建不同大小的 cache
- **测试变体**：Cache size = 0, 1, 2, 4, 8, 16
- **揭示结果**：
  - Cache size = 0 时 = Zero-shot CLIP（60.33%）
  - Cache 越大，性能越高：size 1 → 61.45%, size 2 → 61.71%, size 4 → 61.79%, size 8 → 61.83%, size 16 → 62.03%
  - 更多样本缓存更多 few-shot 知识 → 更高精度
  - 每个 size 使用 5 次随机分割取平均
- **来源**：Table 4 (第三部分), Section 4.4, Page 12

### 消融 4：更多 Shot 下固定 Cache Size 为 16

- **消融内容**：当训练样本超过 16-shot 时，通过分组聚合将 cache 限制为 16 个原型
- **测试变体**：Shot = 16, 32, 64, 128
- **揭示结果**：
  - Tip-Adapter: 16→62.03%, 32→62.51%, 64→62.88%, 128→63.15%
  - Tip-Adapter-F: 16→65.47%, 32→66.58%, 64→67.96%, 128→69.74%
  - Tip-Adapter 在 cache size 固定为 16 时性能提升缓慢（饱和趋势）
  - Tip-Adapter-F 通过微调可以突破这一限制
- **来源**：Table 4 (底部), Section 4.4, Page 12

### 消融 5：Prompt 设计

- **消融内容**：对比不同 prompt 策略对性能的影响
- **测试变体**：Single prompt ("a photo of a [CLASS].") vs Prompt ensembling (7 模板) vs Learnable prompt (CoOp)
- **揭示结果**：
  - Zero-shot CLIP: Single 58.24% vs Ensembling 60.33%（差距 2.09%）
  - Tip-Adapter: Single 60.82% vs Ensembling 62.03%（差距 1.21%）
  - Tip-Adapter-F: Single 65.03% vs Ensembling 65.51%（差距 0.48%）
  - 性能越高的方法对 prompt 变化越不敏感
  - CoOp 使用 learnable prompt 达到 62.95%（其 prompt 为优化所得，非手工）
- **来源**：Figure 6, Section 4.4, Page 13

### 消融 6：不同微调模块 (Appendix A)

- **消融内容**：系统性地微调不同模块组合
- **测试变体**：7 种组合（固定/微调 visual encoder, textual encoder, Ftrain, Ltrain）
- **揭示结果**：

| Vis. | Tex. | Ftrain | Ltrain | Accuracy | Training Time |
|------|------|--------|--------|---------|--------------|
| - | - | - | - | 62.03 | 0 |
| - | - | ✓ | - | 65.51 | 5min |
| - | - | - | ✓ | 60.90 | 5min |
| - | - | ✓ | ✓ | Collapsed | - |
| ✓ | - | - | - | 62.84 | 8min |
| - | ✓ | - | - | 63.15 | 1h 20min |
| ✓ | ✓ | - | - | 51.22 | 1h 27min |

- 仅微调 Ftrain（keys）在准确率和训练时间之间取得最佳平衡
- 微调 Ltrain（values）降低性能（60.90%），因为 one-hot 标签不应被改变
- 同时微调 visual + textual encoder 导致严重过拟合（51.22%）
- 来源：Table 6, Appendix A, Page 15

### 消融 7：视觉 vs 文本缓存

- **消融内容**：将 Tip-Adapter 的 logits 方程分解为视觉缓存检索和文本缓存检索两部分（Eq. 9）
- **测试变体**：视觉缓存（Fvis, Lvis）vs 文本缓存（Ftex = Wc, Ltex = I）
- **揭示结果**：
  - 论文未单独报告视觉缓存或文本缓存独立使用的性能
  - Eq. (9) 将 Tip-Adapter 重新表述为同时从两种缓存检索的形式
  - 本质上 α 控制视觉和文本缓存的相对权重
- **来源**：Section 3.2, Page 8

---

## 5. 参数敏感性与稳定性分析

### Residual Ratio α 敏感性 (Table 4)

| α | 准确率 (%) |
|---|-----------|
| 0.0 | 60.33 |
| 0.5 | 61.44 |
| 1.0 | **62.03** |
| 2.0 | 61.41 |
| 3.0 | 60.36 |
| 4.0 | 59.14 |

**观察**：α 从 0 到 1 时性能单调上升，1 到 4 时单调下降。最优值在 α=1.0，且 α=0.5/2.0 时仍有 61.4% 以上，说明 Tip-Adapter 对 α 在一定范围内（0.5~2.0）有较好的鲁棒性。

### Sharpness Ratio β 敏感性 (Table 4)

| β | 准确率 (%) |
|---|-----------|
| 1.5 | 61.82 |
| 3.5 | 61.91 |
| 5.5 | **62.03** |
| 7.5 | 61.76 |
| 9.5 | 61.62 |
| 11.5 | 61.40 |

**观察**：β 在 1.5~11.5 范围内最大波动仅 0.63%，说明 Tip-Adapter 对 β 比较不敏感。最优在 β=5.5，但所有配置均超过 61.4%。

### Cache Size 敏感性 (Table 4)

| Cache Size | 准确率 (%) |
|-----------|-----------|
| 0 | 60.33 |
| 1 | 61.45 |
| 2 | 61.71 |
| 4 | 61.79 |
| 8 | 61.83 |
| 16 | **62.03** |

**观察**：Cache size 从 0 到 1 时提升最大（+1.12%），之后增益递减。Size 2 时已达 61.71% 接近最优。

### More Shots (Fixed Cache Size 16) (Table 4)

| Shot | Tip-Adapter | Tip-Adapter-F |
|------|------------|---------------|
| 16 | 62.03 | 65.47 |
| 32 | 62.51 | 66.58 |
| 64 | 62.88 | 67.96 |
| 128 | 63.15 | 69.74 |

**观察**：Tip-Adapter 在固定 cache size 下性能增长缓慢（16→128 shot 仅 +1.12%），呈现饱和趋势。Tip-Adapter-F 的增益更显著（16→128 shot +4.27%）。

### Prompt 设计敏感性 (Figure 6)

| 方法 | Single Prompt | Prompt Ensembling | 差距 |
|------|--------------|-------------------|------|
| Zero-shot CLIP | 58.24 | 60.33 | -2.09 |
| CoOp | - | 62.95 | - |
| CLIP-Adapter | 63.04 | 63.59 | -0.55 |
| Tip-Adapter | 60.82 | 62.03 | -1.21 |
| Tip-Adapter-F | 65.03 | 65.51 | -0.48 |

**观察**：prompt 敏感性从高到低：Zero-shot CLIP > Tip-Adapter > CLIP-Adapter / Tip-Adapter-F。性能更强的方法对 prompt 变化越不敏感。CoOp 使用 learnable prompt，不适用该对比。

### 论文未提供的参数分析

- α 和 β 的联合网格搜索（论文仅做了单变量扫描）
- Cache size 在更多 shot（>16）下不固定 cache size 的对比
- Learning rate 的敏感性分析
- Cosine scheduler 参数的影响
- Optimizer 选择的影响（仅使用 AdamW）
- Batch size 的影响（仅使用 256）
- EuroSAT 需要 100 epoch 而其他数据集仅 20 epoch 的原因未说明
- 不同数据集的 α 最优值是否相同（文中提及 α 在 domain gap 大时应设大，但未给出具体数据集的最优 α）
- 多次运行的统计方差（标准差、置信区间等）

---

## 6. 效率、复杂度与资源代价

### 训练效率

| 维度 | Tip-Adapter | Tip-Adapter-F | CLIP-Adapter | CoOp |
|------|------------|--------------|-------------|------|
| 训练需求 | 无需训练 | 需微调 | 需训练 | 需训练 |
| 训练 Epoch | 0 | 20 | 200 | 200 |
| 训练时间 | 0 | 5min | 50min | 14h 40min |
| 推理速度 | 10.42ms | 10.53ms | 10.59ms | 299.64ms |
| GPU 显存 | 2227MiB | 2227MiB | 2227MiB | 7193MiB |
| 额外可学习参数 | 0 | 16×1000×1024 (keys, ImageNet) | MLP 参数 | 16-token prompts |
| 训练前预处理 | 提取 NK 个训练图像特征 | 提取 NK 个训练图像特征 | 无 | 无 |

来源：Table 1, Page 2; Section 4.1, Page 9

### 关键效率对比

- Tip-Adapter 训练时间 + 推理时间 < Zero-shot CLIP 推理时间（0 vs 0，额外的矩阵乘法可忽略）
- Tip-Adapter-F 训练时间仅为 CoOp 的 1/176，为 CLIP-Adapter 的 1/10
- CoOp 推理速度 299.64ms 大幅慢于其他方法，因为每步需通过完整文本编码器在线计算 learnable prompts
- Linear-probe CLIP 使用 logistic regression，无法按 epoch 衡量训练时间，且推理速度在 GPU 上无可比性
- Tip-Adapter 和 CLIP-Adapter 可在开始时缓存 CLIP 的文本特征，但 CoOp 需要每次迭代重新计算

来源：Section 4.2, Page 10

### 模型参数量

| 方法 | 可学习参数量 | 说明 |
|------|------------|------|
| Tip-Adapter (16-shot ImageNet) | 0 | 完全非参数化 |
| Tip-Adapter-F (16-shot ImageNet) | 16×1000×C | 仅 cache keys 可学习 |
| ResNet-50 (fully trained) | 25.6M | 全数据集训练的对比基线 |
| DeiT-T (fully trained) | 6.0M | 全数据集训练的对比基线 |
| Tip-Adapter (Appendix C) | 0 (76.1% acc) | 16-shot，零参数 |
| Tip-Adapter-F (Appendix C) | 6.2M (79.4% acc) | 16-shot，6 分钟训练 |

来源：Table 7, Appendix C, Page 17

### 推理计算量

- 测试图像每步需做：CLIP visual encoder forward (一次) + 两个矩阵乘法（与 cache keys 和与 Wc）
- 矩阵乘法维度：1×C 与 C×NK（相似度计算），1×NK 与 NK×N（值聚合）
- 对于 ImageNet 16-shot: N=1000, K=16, NK=16000, C=1024 (ResNet-50)
- 额外计算量远小于 CLIP visual encoder 本身的计算量

来源：Section 3.1, Page 5-6

### 人工标注代价

| 标注项 | 数量 |
|--------|------|
| Few-shot 训练集 | 每个数据集 N×K 张图像（已有标注，无需额外标注） |
| Prompt 模板 | 7 个 prompt 模板（引自 CLIP [48]） |
| 其他 10 数据集 prompt | 每个 1 个 handcrafted prompt |

### 论文未提供的效率信息

- 提取 NK 个训练图像特征的具体时间
- 单次推理的 token 消耗
- 端到端 wall-clock time（含数据加载、预处理等）
- CPU 内存消耗
- 更大 backbone（如 ViT-L）时的训练/推理时间
- 训练时的 GPU 利用率
- 非 ImageNet 数据集上的推理速度
- Tip-Adapter-F 在不同 epoch 下的 loss 收敛曲线

---

## 7. 鲁棒性、泛化性与补充实验

### 跨数据集泛化

Tip-Adapter 在 11 个广泛使用的图像分类数据集上测试：

| 类别 | 数据集 | 领域 |
|------|--------|------|
| 通用分类 | ImageNet | 日常物体（1000 类） |
| 细粒度分类 | StanfordCars, Flowers102, FGVCAircraft, OxfordPets | 特定物体子类 |
| 场景识别 | SUN397 | 室内外场景 |
| 纹理识别 | DTD | 纹理图案 |
| 卫星图像 | EuroSAT | 遥感地物 |
| 动作识别 | UCF101 | 人类动作 |
| 食物识别 | Food101 | 食物类别 |
| 通用识别 | Caltech101 | 日常物体（101 类） |

来源：Section 4.1, Page 9

11/11 数据集上 Tip-Adapter（无训练）均超越 Zero-shot CLIP。
11/11 数据集上 Tip-Adapter-F 为所有方法中最优。

来源：Section 4.3, Page 11

### 跨 backbone 泛化 (Table 3)

| Backbone | 架构 | 参数量 | Tip-Adapter-F 最优 |
|----------|------|--------|-------------------|
| ResNet-50 | CNN | 25.6M | 65.51 |
| ResNet-101 | CNN | 44.5M | 68.56 |
| ViT-B/32 | Transformer | ~86M | 68.65 |
| ViT-B/16 | Transformer | ~86M | 73.69 |
| RN50x16 | CNN (16x 计算量) | ~400M | 75.81 |

来源：Table 3, Page 10

**论文未提供**：CoOp 和 CLIP-Adapter 在 RN50x16 backbone 上的结果。

### 分布偏移鲁棒性 (Table 5)

16-shot ImageNet 训练 → 目标数据集测试：

| 方法 | ImageNet (源) | ImageNetV2 (目标) | ImageNet-Sketch (目标) |
|------|--------------|------------------|----------------------|
| Zero-shot CLIP | 60.33 | 53.27 | 35.44 |
| Linear-probe CLIP | 56.13 | 45.61 | 19.13 |
| CoOp | 62.95 | 54.58 | 31.04 |
| CLIP-Adapter | 63.59 | 55.69 | 35.68 |
| Tip-Adapter | 62.03 | 54.60 | 35.90 |
| Tip-Adapter-F | 65.51 | **57.11** | **36.00** |

来源：Table 5, Section 4.5, Page 13

**关键数字**：
- Tip-Adapter（无训练）在 ImageNet-Sketch 上 35.90% 超越 CLIP-Adapter 35.68% 和 CoOp 31.04%
- Tip-Adapter-F（微调后）在 ImageNetV2 上仅 +2.51% 相对于 Tip-Adapter，但在 ImageNet-Sketch 上仅 +0.10%
- Linear-probe CLIP 在分布偏移下性能下降最严重（ImageNet-Sketch 19.13%，比 Zero-shot 低 16.31%）
- CoOp 在 ImageNet-Sketch 上从源 62.95% 降至 31.04%（下降 31.91%），过拟合最严重

来源：Section 4.5, Page 13

### 对比全数据集训练方法 (Appendix C, Table 7)

| 方法 | 训练集 | 训练时间 | 参数量 | ImageNet 准确率 |
|------|--------|---------|--------|----------------|
| ResNet-50 | 全量 (1.2M) | >1 天 | 25.6M | 74.2 |
| ResNet-101 | 全量 (1.2M) | >1 天 | 44.5M | 77.4 |
| DeiT-T | 全量 (1.2M) | >1 天 | 6.0M | 72.2 |
| DeiT-S | 全量 (1.2M) | >1 天 | 22.1M | 79.9 |
| Tip-Adapter (ViT-L) | 16-shot (16K) | 0 | 0 | 76.1 |
| Tip-Adapter-F (ViT-L) | 16-shot (16K) | 6 min | 6.2M | 79.4 |

来源：Table 7, Appendix C, Page 17

**关键数字**：
- Tip-Adapter (16-shot, 0 参数) 准确率 76.1%，超越 ResNet-50 (74.2%) 和 DeiT-T (72.2%)
- Tip-Adapter-F (16-shot, 6 分钟) 准确率 79.4%，接近 DeiT-S (79.9%) 但仅使用 1.3% 的训练数据
- 训练时间从 >1 天降至 0 或 6 分钟

### Performance Gain without Training (Appendix B, Figure 8)

16-shot 设置下 Tip-Adapter 相对于 Zero-shot CLIP 的绝对提升：

| 数据集 | 绝对提升 (%) |
|--------|-------------|
| EuroSAT | 33.02 |
| Flowers102 | 23.87 |
| DTD | 18.73 |
| FGVCAircraft | 12.66 |
| StanfordCars | 11.03 |
| UCF101 | 9.23 |
| SUN397 | 8.33 |
| Caltech101 | 4.26 |
| OxfordPets | 2.31 |
| ImageNet | 1.70 |
| Food101 | 0.51 |

来源：Figure 8, Appendix B, Page 16

**观察**：Domain gap 越大，Tip-Adapter 的提升越显著。EuroSAT（卫星图像）与 CLIP 预训练数据（日常场景）差距最大，提升最多。Food101（食物图像）与 CLIP 预训练数据最接近，提升最小。

### t-SNE 可视化 (Figure 7)

- 可视化对象：cache model 中的 keys Ftrain
- 数据集：ImageNet 16-shot 中的 10 个类别
- 从左到右：训练前（Tip-Adapter）→ 训练中 → 训练后（Tip-Adapter-F）
- 观察：训练前各聚类已有较好的区分度；训练中同一类别逐渐聚集，不同类别间距增大

来源：Section 5, Figure 7, Page 14

### 论文未提供的鲁棒性/泛化信息

- 在其他 CLIP 变体（如 OpenCLIP、SLIP 等）上的结果
- 跨数据集迁移（source→target 除 ImageNet→V2/Sketch 外无其他组合）
- 对输入噪声（对抗攻击、常见 corruptions）的鲁棒性
- 不同 cache 构造方式（随机分组以外的策略，如 K-means 聚类）的影响
- 多次运行的均值和方差
- 统计显著性检验
- ImageNetV2 和 ImageNet-Sketch 上的详细 shot 扫描
- 除 ImageNet 外其他数据集的分布偏移实验

---

## 8. 值得关注的实验现象

### 现象 1：Training-free Tip-Adapter 在 1-shot/2-shot 下大幅超越 Linear-probe CLIP

1-shot 时 Tip-Adapter (60.70%) vs Linear-probe CLIP (22.17%)，提升 +38.53%；2-shot 时 +29.06%。这是因为 Linear-probe 在极少量样本下无法训练有效分类器，而 Tip-Adapter 通过检索机制利用了 CLIP 预训练特征的对齐性。

**来源**：Table 2, Page 9

### 现象 2：Training-free 方法达到或接近需要 200 epoch 训练的 methods

Tip-Adapter (62.03%) 接近 CLIP-Adapter (63.59%) 和 CoOp (62.95%)，两者均需 200 epoch。这挑战了"few-shot 适配必须经过参数更新"的直觉。

**来源**：Table 1, Page 2; Table 2, Page 9

### 现象 3：Fine-tuning keys (Ftrain) 远优于微调 values (Ltrain) 或 CLIP encoders

微调 Ftrain 获得 +3.48% 提升（65.51%），而微调 Ltrain 反而降低性能（60.90%）。同时微调两者导致训练崩溃。微调 CLIP 双 encoder 导致严重过拟合（51.22%），比 Zero-shot CLIP 还低 9.11%。

**来源**：Table 6, Appendix A, Page 15

### 现象 4：Tip-Adapter 的分布偏移鲁棒性优于 CoOp 和 CLIP-Adapter

Tip-Adapter 在 ImageNet-Sketch 上（35.90%）高于 CoOp (31.04%) 和 CLIP-Adapter (35.68%)，虽然在源域 ImageNet 上 Tip-Adapter (62.03%) 低于两者。这说明训练无关的 cache 构造减轻了过拟合，在分布偏移场景下反而具有优势。

**来源**：Table 5, Page 13

### 现象 5：Domain gap 越大，Tip-Adapter 的增益越显著

EuroSAT 上 Tip-Adapter 提升 Zero-shot CLIP 达 33.02%，但 Food101 上仅 0.51%。这与 CLIP 预训练数据的分布有关——预训练数据包含大量食物图像，但很少包含卫星图像。

**来源**：Figure 8, Appendix B, Page 16

### 现象 6：性能越高的方法对 prompt 变化越不敏感

从 Single prompt 到 prompt ensembling 的差距：Zero-shot CLIP -2.09%，Tip-Adapter -1.21%，CLIP-Adapter -0.55%，Tip-Adapter-F -0.48%。说明更强的适配方法或训练可以减少对 prompt 工程的依赖。

**来源**：Figure 6, Page 13

### 现象 7：16-shot (0 参数) + ViT-L 超越全量训练 ResNet-50

Tip-Adapter (ViT-L, 16-shot, 0 参数, 0 训练时间) 达到 76.1%，超过 ResNet-50 (74.2%, 全量 1.2M 图像, 25.6M 参数, >1 天训练)。

**来源**：Table 7, Appendix C, Page 17

### 现象 8：Cache size 在 0->1 时性能跳跃最大

Cache size 从 0 到 1 提升 +1.12%（60.33→61.45），但从 1 到 2 仅 +0.26%，从 8 到 16 仅 +0.20%。说明即使每个类别仅缓存 1 个样本也能带来大部分收益。

**来源**：Table 4, Page 12

---

## 9. 证据充分性整理

### 支撑较充分的结论

| 结论 | 证据 | 充分性 |
|------|------|--------|
| Training-free cache model 有效 | Table 2 (5 个 shot 设置)、Figure 5 (10 个数据集)、Figure 8 (11 个数据集提升) — 11/11 数据集一致 | **充分** |
| Tip-Adapter-F 达到 SOTA | Table 1、Table 2、Table 3 (5 种 backbone)、Figure 5 (10 个数据集) — 所有配置下一致最优 | **充分** |
| 仅微调 keys 最优 | Table 6 (7 种微调组合)，结果一致且符合理论预期 | **充分** |
| 效率优势显著 | Table 1 (训练时间、推理速度、GPU 显存三维度对比) | **充分** |
| Tip-Adapter 在分布偏移场景具有鲁棒性 | Table 5 (2 个目标数据集)，但仅基于 ImageNet 源域 | **有限** |

### 支撑有限的结论

| 结论 | 局限 |
|------|------|
| 跨 backbone 泛化 | CoOp 和 CLIP-Adapter 在 RN50x16 上的结果缺失，无法完整对比 |
| α 与 domain gap 的关系 | 论文声称 α 应随 domain gap 增大而增大，但未给出跨数据集的实验验证 |
| Cache 构造策略的最优性 | 仅测试了随机分组平均，未比较 K-means、K-center 等聚类策略 |
| Fine-tuning 的收敛分析 | 仅报告 20 epoch 后的结果，未展示收敛曲线或 epoch sweep |
| Statistical significance | 未报告多 seed 均值和标准差 |
| 跨模型泛化 | 仅使用 CLIP (ResNet-50 + Transformer) 作为 backbone，未在非 CLIP 模型上验证 |

### 论文未提供的实验信息

- 多次运行的均值和标准差
- 统计显著性检验（p-value, confidence interval）
- 非 CLIP 模型上的结果
- 不同 cache 构造策略的系统对比
- 其他数据集的 α/β 最优值
- 除 ImageNet→V2/Sketch 外的跨域迁移实验
- 训练收敛曲线（loss/accuracy vs epoch）
- 不同 optimizer 选择的对比
- 不同数据增强策略的影响
- 针对训练集噪声的鲁棒性
- Cache model 中 keys 更新的梯度分析

---

## 10. 对后续问题发现最有价值的实验信息

### 可复现的实验设定

- 11 个公开数据集（ImageNet, StanfordCars, UCF101, Caltech101, Flowers102, SUN397, DTD, EuroSAT, FGVCAircraft, OxfordPets, Food101）——均可从公开来源获取
- CLIP 预训练权重从 [48] 获取（公开可用）
- 代码开源：https://github.com/gaopengcuhk/Tip-Adapter
- 明确的数据预处理协议（同 CLIP [48]）
- 明确的超参数（α=1.0, β=5.5, batch size 256, lr=0.001, AdamW, cosine scheduler, 20 epoch）
- 明确的 few-shot 划分（K-shot N-class，每组随机选取 K 张训练图像）
- 测试于完整测试集（非小样本 query set）

### 值得验证的问题

1. **Training-free cache model 的极限**：在更大 shot（>128）下 Tip-Adapter 性能为何饱和？是 cache size 瓶颈还是 CLIP 特征表达能力瓶颈？
2. **α 依赖 domain gap 的定量评估**：论文声称 domain gap 越大 α 应越大，但未量化——需要建立 domain gap 度量与最优 α 的映射关系
3. **Cache model 的泛化机制**：为什么训练无关的 cache 构造在分布偏移场景下表现出更好的鲁棒性？其蕴含的归纳偏置是什么？
4. **CLIP encoder 是否需要适配**：Table 6 显示微调 CLIP encoder 导致过拟合——这是否是数据量不足造成的？在更多 shot 下是否改善？
5. **Cache 构造策略的最优性**：随机分组平均 vs. K-means 聚类构建 cache 原型是否有显著差异？
6. **跨数据集的 α/β 稳定性**：α=1.0, β=5.5 对所有 11 个数据集是否均接近最优？

### 最值得优先验证的 3 个问题

1. **α 和 β 的跨数据集最优值分布**（关系到方法的通用性和调参成本）
2. **Cache 构造策略对比**（随机分组 vs 聚类 vs 核心集选择，关系到方法的实际性能上限）
3. **分布偏移场景的深入分析**（仅 2 个目标数据集，不足以下定论，需要更多目标域验证）

---

## 11. 一段简短总结

Tip-Adapter 在 11 个图像分类数据集上验证了 training-free cache model 用于 CLIP few-shot 适配的有效性。核心实验发现：(1) Tip-Adapter 无需训练即可在 16-shot ImageNet 上达到 62.03%，接近需要 200 epoch 训练的 CLIP-Adapter (63.59%) 和 CoOp (62.95%)；(2) Tip-Adapter-F 仅需 5 分钟（20 epoch）微调即可达到 65.51% SOTA；(3) 仅微调 cache keys（而非 values 或 CLIP encoders）是最优策略；(4) 训练无关的 cache 构造在分布偏移场景下表现出更强的鲁棒性（ImageNet-Sketch 超越 CoOp 4.86%）。证据充分性最强的结论是 Tip-Adapter 和 Tip-Adapter-F 在 11/11 数据集上均有效，但跨数据集 α/β 最优值、cache 构造策略对比、统计显著性和更广泛的分布偏移验证等关键问题均未充分覆盖。代码开源可用，为基础实验复现提供了有利条件。
