# DiScGraph: Dependency-Aware Discrete Diffusion for Scene Graph Generation

- **标题（EN）**：Dependency-Aware Discrete Diffusion for Scene Graph Generation
- **标题（CN）**：依赖感知离散扩散的场景图生成
- **作者**：Rajalaxmi Rajagopalan, Romit Roy Choudhury（University of Illinois, Urbana-Champaign）
- **发表**：arXiv 2605.09065, 2026年5月
- **领域**：scene-graph
- **证据等级**：full-paper
- **代码**：未开源
- **标签**：`discrete-diffusion` `scene-graph-generation` `text-to-sg` `factorized-diffusion`

## 核心贡献

提出 **DiScGraph**，首个针对场景图结构特点设计的**层级约束离散扩散模型**。核心创新是将离散扩散从**独立分类变量**扩展为**依赖感知的分层过程**：

1. **层级图表示** `SG = {(V, E, R⁺), eij=0⇒rij=0}` — 将边存在性（结构）与关系语义解耦，避免长尾关系与"无关系"类竞争
2. **边门控前向加噪**（Edge-Gated Forward Process） — 关系仅在活跃边上加噪，静默边上强制为零
3. **分解式反向采样器**（Factorized Reverse Sampler） — 按 `V→E→R` 顺序条件预测，保持语义一致性
4. **推理时文本条件生成** — 通过 CLIP 奖励倾斜采样（Reward-Tilted Sampling）+ Sequential Monte Carlo 粒子重采样，无需重新训练

## 方法详解

### 层级场景图表示（Sec 3.1）

将标准图状态 `G = (V, E)` 分解为：
- `V`：物体类别（Kobj 类）
- `E`：边存在性（0/1）
- `R⁺`：关系语义（Krel 类），仅当 `eij=1` 时有意义

有效场景图空间定义为：`SG = {(V, E, R⁺) : eij=0 ⇒ rij=0}`

### 边门控前向加噪（Sec 3.2）

前向过程分解为：

`q(xt | xt-1) = qV(Vt | Vt-1) · qE(Et | Et-1) · qR(R⁺t | R⁺t-1, Et, Et-1)`

关系加噪仅在活跃边上进行：
- `eij,t=0` → `qR = δ₀(rij,t)`（强制为0）
- `eij,t=1` → `qR = (1-β)δ(rij,t-1) + β·πR`（标准分类加噪）

使用混合随机+掩码（Hybrid Random + Mask）加噪策略，吸收掩码保留结构、隐藏语义。

### 分解式反向采样器（Sec 3.3）

干净状态预测按层级分解：

`pθ(V₀, E₀, R₀ | xt) = pθ(V₀ | xt) · pθ(E₀ | V₀, xt) · pθ(R₀ | V₀, E₀, xt)`

反向转移保持约束：

`pθ(xt-1 | xt) = pθ(Vt-1 | xt) · pθ(Et-1 | Vt-1, xt) · pθ(Rt-1 | Vt-1, Et-1, xt)`

### 奖励倾斜推理（Sec 3.4）

`pθ(Gt-1 | Gt; T) ∝ pθ(Gt-1 | Gt) · exp(β·R(Ĝ₀, T))`

使用 CLIP 相似度作为奖励函数 `R(Ĝ₀, T)`，通过 SMC 粒子滤波实现无训练的条件生成。

## 实验设置

### 数据集
- **Visual Genome (VG)** — 标准SGG协议
- **COCO-Stuff** — 目标检测场景
- **LAION-SG** — 大规模SG数据集（1M+）

### 结构指标（无条件SG生成）
- **N-MMD**（节点分布MMD）、**R-MMD**（关系分布MMD）
- **ID-MMD / OD-MMD**（入度/出度分布MMD）
- **Triplet-TV**（三元组分布TV距离）
- **Rare-K-TV**（长尾关系生成能力）
- **Attach-TV**（语义一致性：给定V预测R的能力）

### 布局指标
- F1-std、F1-Area、F1-Freq、F1-Box

### 图像生成指标
- FID、CLIP-I2T、CLIP-I2I、BLIP-VQA、ImageReward (IR)
- SG-IoU、Entity-IoU、Relation-IoU

## 主要结果

### 无条件SG生成（Table 1）

| 数据集 | 方法 | N-MMD↓ | R-MMD↓ | TRIP-TV↓ | R-K-TV↓ | AT-TV↓ |
|--------|------|---------|---------|-----------|---------|---------|
| VG | DiGress | 7.63e-3 | 7.26e-3 | 0.7730 | 0.8622 | 0.4561 |
| VG | DiffuseSG | 8.21e-3 | 1.11e-2 | 0.6390 | 0.826 | 0.2916 |
| VG | **DiScGraph** | **4.59e-3** | **5.78e-3** | **0.4920** | **0.5194** | **0.1766** |
| COCO | DiGress | 7.81e-4 | 8.86e-4 | 0.4147 | 0.855 | 0.3775 |
| COCO | DiffuseSG | 3.93e-4 | 6.45e-5 | 0.3106 | 0.814 | 0.2916 |
| COCO | **DiScGraph** | **3.97e-4** | **5.39e-5** | **0.2100** | **0.6661** | **0.1204** |
| LAION-SG | DiGress | 3.42e-3 | 9.78e-3 | 0.8188 | 0.9164 | 0.5526 |
| LAION-SG | DiffuseSG | 1.36e-3 | 9.66e-3 | 0.7025 | 0.8973 | 0.5440 |
| LAION-SG | **DiScGraph** | **9.81e-4** | **6.35e-3** | **0.5693** | **0.7746** | **0.4238** |

DiScGraph 在所有指标上全面超越 DiGress（通用离散图扩散）和 DiffuseSG（连续图扩散），尤其在关系建模（R-MMD、R-K-TV、AT-TV）上优势显著。

### SG-to-Image 生成（Table 4）

| 数据集 | 方法 | FID↓ | BLIP-VQA↑ | ImageReward↑ |
|--------|------|------|-----------|-------------|
| CompSGBench | SDXL | 31.34 | 0.6425 | 1.1286 |
| CompSGBench | ComposeDiff | 49.72 | 0.3860 | -0.9213 |
| CompSGBench | CO3 | 36.06 | 0.6724 | 1.2070 |
| CompSGBench | **DiScGraph** | 33.85 | **0.7854** | **1.4512** |
| COCO | SDXL | 43.02 | 0.6001 | 0.6409 |
| COCO | CO3 | 40.26 | 0.6282 | 0.8857 |
| COCO | **DiScGraph** | **38.68** | **0.6734** | **1.1028** |

DiScGraph 在 CompSGBench 和 COCO 上 BLIP-VQA 和 ImageReward 均超越文本-only 方法（SDXL、ComposeDiffusion、CO3）。

### 结构图像指标（Table 5）

| 方法 | SG-IoU↑ | E-IoU↑ | R-IoU↑ |
|------|----------|--------|---------|
| SDXL | 0.3260 | 0.7620 | 0.7188 |
| CO3 | 0.4271 | 0.7945 | 0.7203 |
| **DiScGraph** | **0.5629** | **0.8357** | **0.8299** |

DiScGraph 在图级、实体级和关系级 IoU 上均大幅领先基线，尤其关系级 IoU (0.8299 vs SDXL 0.7188)。

### Layout 生成（Table 2）

| 数据集 | 方法 | F1-std↑ | F1-Area↑ | F1-Box↑ |
|--------|------|----------|----------|---------|
| VG | DiffuseSG | 0.1753 | 0.3296 | 0.7210 |
| VG | **DiScGraph** | **0.1790** | **0.3302** | **0.7540** |
| COCO | DiffuseSG | 0.4644 | 0.5153 | 0.8023 |
| COCO | **DiScGraph** | **0.4724** | **0.5371** | **0.8010** |

### SG补全任务（Table 3）

| 数据集 | 方法 | Single Object w100↑ | Single Relation w100↑ |
|--------|------|---------------------|----------------------|
| VG | DiGress | 86.6 | 88.8 |
| VG | DiffuseSG | 90.0 | 93.5 |
| VG | **DiScGraph** | **95.3** | **98.7** |
| CompSGBench | DiGress | 82.5 | 70.5 |
| CompSGBench | DiffuseSG | 85.0 | 83.5 |
| CompSGBench | **DiScGraph** | **92.6** | **94.6** |

### Layout-to-Image（Table 6, COCO）

| 方法 | FID↓ | CLIP-I2T↑ | BLIP-VQA↑ | IR↑ |
|------|------|-----------|-----------|------|
| LayoutDM | 72.32 | 0.5204 | 0.6519 | 0.9206 |
| LayoutLLM-T2I | 69.01 | 0.6789 | 0.8714 | 1.2966 |
| LDM | 68.84 | 0.6828 | 0.8286 | 1.3552 |
| **DiScGraph** | 71.59 | 0.6802 | 0.8599 | 1.3548 |

DiScGraph 的 layout head 与 LLM-augmented layout 方法（LayoutLLM-T2I、LDM）竞争力相当，无需额外 LLM。

### 消融实验（Table 7）

| ID | 配置 | N-MMD | R-MMD | TRIP-TV | R-K-TV |
|----|------|-------|-------|---------|---------|
| 1 | Joint (E,R) | 0.0077 | 0.0078 | 0.6910 | 0.8118 |
| 2 | + Factorized State | 0.0066 | 0.0066 | 0.5822 | 0.6099 |
| 3 | + Dependency Sampler | **0.0046** | **0.0058** | **0.4878** | **0.5199** |
| 4 | + Layout Head | 0.0046 | 0.0058 | 0.4920 | 0.5194 |

关键结论：分解式状态提升结构和关系指标，依赖感知采样器提升语义一致性（Triplet-TV 从 0.5822 → 0.4878），layout head 几乎不损害 SG 质量。

## 与现有工作的关系

- **vs DiGress** [Vignac+ 2023]：DiGress 将节点和边视为独立分类变量，不适合场景图的强依赖和长尾分布。DiScGraph 用分解式状态和条件采样器替代。
- **vs DiffuseSG** [Yang+ 2024]：连续扩散模型通过阈值化映射到离散结果，无法充分利用图结构。DiScGraph 使用原生离散扩散。
- **vs 文本组合方法**（CO3、ComposeDiffusion）：推理时干预的文本方法性能受限，场景图提供更丰富的结构化条件。

## 局限与未来工作

1. 奖励模型（CLIP）质量限制文本条件生成效果
2. Graph Transformer 平方复杂度，大规模场景需稀疏注意力
3. 离散采样器质量受限，需采样细化策略
4. 多地物子图布局预测可能歧义
5. 缺乏大规模 SG 条件图像生成器（LAION-SG 是初期工作）

## BibTeX

```bibtex
@article{rajagopalan2026discgraph,
  title={Dependency-Aware Discrete Diffusion for Scene Graph Generation},
  author={Rajagopalan, Rajalaxmi and Choudhury, Romit Roy},
  journal={arXiv preprint arXiv:2605.09065},
  year={2026}
}
```
