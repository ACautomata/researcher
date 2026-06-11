---
title: "EchoScene: Indoor Scene Generation via Information Echo over Scene Graph Diffusion"
type: paper
domain: scene-graph
status: active
created: 2026-06-10
updated: 2026-06-10
tags:
  - scene-graph-generation
  - 3d-scene-graph
  - scene-generation
  - ECCV-2024
  - diffusion-model
  - 3d-indoor
raw_sources:
  - raw/sources/2024-05-02-echoscene-indoor-scene-generation-via-information-echo-scene-graph-diffusion.pdf
  - raw/sources/2024-05-02-echoscene-indoor-scene-generation-via-information-echo-scene-graph-diffusion.txt
related_pages:
  - scenescene-commonscenes
  - graph-to-3d
  - diffuscene
  - instructscene
  - 3d-front-dataset
  - sg-front-dataset

paper:
  title: "EchoScene: Indoor Scene Generation via Information Echo over Scene Graph Diffusion"
  authors:
    - "Guangyao Zhai"
    - "Evin Pınar Örnek"
    - "Dave Zhenyu Chen"
    - "Ruotong Liao"
    - "Yan Di"
    - "Nassir Navab"
    - "Federico Tombari"
    - "Benjamin Busam"
  year: 2024
  venue: "ECCV 2024"
  arxiv: "2405.00915"
  code: "https://github.com/GY80742/EchoScene"
  project: "https://sites.google.com/view/echoscene"

classification:
  label: "EchoScene"
  task:
    - "3D indoor scene generation"
    - "scene graph conditioned generation"
    - "controllable scene synthesis"
  method_family:
    - "diffusion models"
    - "dual-branch diffusion"
    - "graph diffusion"
    - "information echo"
  modality:
    - "3D scenes"
    - "scene graphs"
  datasets:
    - "SG-FRONT"
  metrics:
    - "FID"
    - "FIDCLIP"
    - "KID"
    - "SG constraint accuracy"
    - "Chamfer Distance"

evidence_level: full-paper
---

## Citation

```
@inproceedings{zhai2024echoscene,
  title={EchoScene: Indoor Scene Generation via Information Echo over Scene Graph Diffusion},
  author={Zhai, Guangyao and {\"O}rnek, Evin P{\i}nar and Chen, Dave Zhenyu and Liao, Ruotong and Di, Yan and Navab, Nassir and Tombari, Federico and Busam, Benjamin},
  booktitle={European Conference on Computer Vision (ECCV)},
  year={2024}
}
```

## One-Sentence Contribution

提出基于信息回响（Information Echo）机制的双分支（布局+形状）场景图扩散模型，通过每个节点独立去噪进程间的全局信息交换，实现可控、一致的 3D 室内场景生成。

## Problem Setting

可控场景生成（CSG）：从场景图输入生成完整 3D 室内场景，支持用户通过编辑场景图（添加/删除节点、修改关系）交互式操控生成结果。核心挑战来自场景图的不定节点数、多边组合和节点/边操作引起的动态图结构变化。

## Method

### 整体架构

EchoScene 包含两个处理阶段：
1. **图预处理**：使用 triplet-GCN 编码器将语义场景图编码为潜在关系嵌入，支持图操控（节点添加、关系变更）
2. **双分支生成**：布局分支 + 形状分支，每个分支为图中每个节点分配独立的去噪进程

### 信息回响机制（Information Echo）

核心创新点。每个去噪时间步，每个节点的去噪进程向**信息交换单元 U**发送当前去噪数据 + 其他节点属性，U 基于图边使用 triplet-GCN 聚合所有进程的信息后回传给各节点去噪器作为条件信号。

**关键公式**（单步条件去噪）：
```
d_{t-1}^i = (1/√α_t) * (d_t^i - ((1-α_t)/√(1-α̅_t)) * ε_θ(d_t^i, π(t), C_Dt)) + σ_t * z
C_Dt = U(G_Dt),  G_Dt = {V_Dt, E}
```

每次发送+接收构成一次"信息回响"，在每个时间步重复。

### 布局分支

- 每个对象的边界框参数化为 8 维：位置 (x,y,z)、尺寸 (l,h,w)、偏航角 (sin θ, cos θ)
- 布局回响：所有节点交换当前扩散边界框信息，确保布局符合场景图空间约束
- 1000 个时间步，权重共享的去噪器 γ_θ
- 训练损失：标准的 DDPM 噪声预测损失 L_layout

### 形状分支

- 预训练 VQ-VAE 作为形状编码器/解码器，在瓶颈处使用 LDM
- 形状回响：扩散的形状码经 3D 卷积 + 展平后对齐维度，然后通过形状交换单元 U_s 进行信息交换
- 解决了 CommonScenes 的隔离问题——每个生成进程只关注自身而忽略其他节点的形状外观
- 训练损失：标准的 LDM 噪声预测损失 L_shape

### 双分支联合训练

总损失：L = λ₁·L_layout + λ₂·L_shape，支持端到端同步训练。

### 操控策略

- **本文策略（扩散逆工作流）**：从伪图（假关系）出发，经操控恢复为 ground truth 图，无需 GAN 判别器
- **之前方法（VAE+GAN）**：需要输入侧 ground truth 边界框 + GAN 判别器辅助输出预测，训练不稳定

## Experiments

### 数据集

- **SG-FRONT**：基于 3D-FRONT 的场景图数据集
  - 15 种关系类型
  - 45K 对象实例
  - 三种房间类型：Bedroom、Living room、Dining room

### 评估指标

- **生成保真度**：FID、FIDCLIP、KID（在 256² 分辨率俯视图渲染上衡量）
- **场景图一致性**：6 种约束准确率（left/right, front/behind, smaller/larger, taller/shorter, close_by, symmetrical）
- **物体间一致性**：Chamfer Distance（CD），测量场景中应一致的物体形状距离

### Baselines

**Retrieval-based**：3D-SLN、Progressive layout（Graph-to-3D）、Graph-to-Box（Graph-to-3D）、CommonLayout（CommonScenes）、DiffuScene、InstructScene*（仅布局解码器）

**Generative**：Graph-to-3D（VAE 建模形状+布局）、CommonScenes（VAE 布局 + LDM 形状）、CommonLayout+SDFusion、EchoLayout+SDFusion、EchoScene

### 训练设置

- 硬件：单张 NVIDIA A40 GPU（40GB）
- 优化器：AdamW，初始学习率 1e-4
- 损失权重：λ₁ = λ₂ = 1.0
- 去噪时间步：1000

### 消融实验

三种消融设置：
1. **w/o π(t)**：去除显式时间信息编码
2. **w/o shape echoes**：去除形状回响（形状分支降级）
3. **Ours with concat**：用拼接替代交叉注意力作为条件方式

## Results

### 场景生成保真度（Tab. 1）

FID / FIDCLIP / KID（×0.001），256² 分辨率，越低越好：

| 方法 | 形状表示 | Bedroom FID ↓ | Bedroom FIDCLIP ↓ | Bedroom KID ↓ | Living FID ↓ | Living FIDCLIP ↓ | Living KID ↓ | Dining FID ↓ | Dining FIDCLIP ↓ | Dining KID ↓ |
|------|---------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Retrieval-based** | | | | | | | | | | |
| 3D-SLN | Retrieval | 57.90 | 5.45 | 3.85 | 77.82 | 7.02 | 3.65 | 69.13 | 7.99 | 6.23 |
| Progressive | Retrieval | 58.01 | 5.67 | 7.36 | 79.84 | 7.41 | 4.24 | 71.35 | 8.28 | 6.21 |
| Graph-to-Box | Retrieval | 54.61 | 5.26 | 2.93 | 78.53 | 6.88 | 3.32 | 67.80 | 7.75 | 6.30 |
| CommonLayout | Retrieval | 52.69 | 5.22 | 2.82 | 76.52 | 6.58 | 2.08 | 65.10 | 7.55 | 6.11 |
| DiffuScene | Retrieval | 52.02 | 5.01 | 2.52 | 81.61 | 7.52 | 1.23 | 65.90 | 7.39 | 0.09 |
| InstructScene* | Retrieval | 45.40 | 3.87 | 1.06 | 75.83 | 6.98 | 4.15 | 61.56 | 6.49 | 4.90 |
| **EchoLayout (Ours)** | **Retrieval** | **46.53** | **4.24** | **0.33** | **75.54** | **6.35** | **1.60** | **59.66** | **6.24** | **2.63** |
| **Generative** | | | | | | | | | | |
| Graph-to-3D | DeepSDF | 63.72 | 6.01 | 17.02 | 82.96 | 7.80 | 11.07 | 72.51 | 7.25 | 12.74 |
| CommonLayout+SDFusion | txt2shape | 68.08 | 5.61 | 18.64 | 85.38 | 7.23 | 10.04 | 64.02 | 6.92 | 5.08 |
| EchoLayout+SDFusion | txt2shape | 57.68 | 4.96 | 10.54 | 83.66 | 6.83 | 9.62 | 65.55 | 7.02 | 4.99 |
| CommonScenes | rel2shape | 57.68 | 4.86 | 6.59 | 80.99 | 7.05 | 6.39 | 65.71 | 7.04 | 5.47 |
| **EchoScene (Ours)** | **echo2shape** | **48.85** | **4.26** | **1.77** | **75.95** | **6.73** | **0.60** | **62.85** | **6.28** | **1.72** |

**关键结论**：
- EchoScene 在所有三个房间类型上全面超越 CommonScenes：Bedroom FID 改善 15%（57.68→48.85），FIDCLIP 改善 12%（4.86→4.26），KID 改善 73%（6.59→1.77）
- EchoLayout 优于前一 SoTA CommonLayout 的所有指标
- EchoScene 在 generative 方法中整体最优，尽管 retrieval 方法由于 test mesh 对齐得分更高

### 场景图约束准确率（Tab. 2）

**关系变更（Change）模式**：

| 方法 | left/right | front/behind | smaller/larger | taller/shorter | close_by | symmetrical |
|------|:---:|:---:|:---:|:---:|:---:|:---:|
| EchoLayout (Ours) | 0.94 | 0.93 | 0.92 | 0.92 | 0.72 | 0.56 |
| EchoScene (Ours) | 0.94 | **0.96** | 0.92 | 0.93 | 0.74 | 0.50 |

**节点添加（Addition）模式**：

| 方法 | left/right | front/behind | smaller/larger | taller/shorter | close_by | symmetrical |
|------|:---:|:---:|:---:|:---:|:---:|:---:|
| EchoLayout (Ours) | **0.98** | **0.99** | **0.97** | **0.96** | 0.74 | 0.58 |
| EchoScene (Ours) | **0.98** | **0.99** | **0.96** | **0.96** | **0.76** | 0.49 |

**无操作（None）模式**：

| 方法 | left/right | front/behind | smaller/larger | taller/shorter | close_by | symmetrical |
|------|:---:|:---:|:---:|:---:|:---:|:---:|
| EchoLayout (Ours) | 1.00 | 0.99 | 0.95 | 0.96 | 0.74 | **0.67** |
| EchoScene (Ours) | 0.98 | 0.99 | 0.96 | 0.96 | 0.74 | 0.55 |

**关键结论**：
- EchoScene 在关系变更和节点添加模式下大部分约束保持最优
- symmetrical 约束下降——论文指出这是因为 symmetrical 是极端稀有标注（在 SG-FRONT 中仅 0.9% 出现率），残差回响修正将潜在码向学习分布扩散导致微小变化
- InstructScene 在全局 FID 上表现优秀（Tab.1），但难以同时维持多个图约束

### 物体间一致性（Tab. 3）

Chamfer Distance（×0.001），越低越好：

| 方法 | Bedroom Ward. | Bedroom N.stand | Dining Chair | Dining Table | Living Chair | Living Table |
|------|:---:|:---:|:---:|:---:|:---:|:---:|
| CommonScenes | 0.61 | 2.69 | 6.64 | 11.75 | 1.96 | 9.04 |
| **EchoScene** | **0.14** | **1.68** | **0.99** | **3.02** | **1.75** | **1.26** |

所有 6 类物体的 CD 均大幅下降，形状回响有效解决了 CommonScenes 的生成隔离问题。

### 消融实验（Tab. 4）

| 消融 | FID ↓ | FIDCLIP ↓ | KID ↓ | mSG ↑ |
|------|:---:|:---:|:---:|:---:|
| Ours w/o π(t) | 40.55 | 3.14 | 1.69 | 0.87 |
| Ours w/o shape echoes | 46.88 | 3.81 | 4.17 | 0.88 |
| Ours with concat | 48.32 | 3.82 | 6.87 | 0.87 |
| **Ours (full)** | **39.74** | **3.14** | **1.24** | **0.88** |

**消融结论**：
- **w/o π(t)**：去掉时间编码影响微弱，说明模型仍能从去噪步骤中学习时间信息
- **w/o shape echoes**：FID 从 39.74 降至 46.88（+7.14），KID 从 1.24 升至 4.17（+2.93×），但 mSG 不受影响，证实形状回响影响保真度而非布局
- **Ours with concat**：拼接替代交叉注意力后 FID 从 39.74 升至 48.32（+8.58），所有指标全面下降

### 定性结果

- 与 Graph-to-3D 和 CommonScenes 对比，EchoScene 生成更整洁的布局（如床和床头柜不再扭曲）、更高的形状一致性（椅子保持统一风格，餐桌无误生成）
- 可与 SceneTex 组合生成带纹理的场景（5 种风格：French-country、Baroque、Bohemian、Midcentury、Modern、Japanese）

## Limitations

1. **仅生成语义无纹理场景**：需要外接纹理生成器（如 SceneTex）才能获得逼真纹理
2. **稀有关系性能下降**：symmetrical 关系仅占 0.9% 标注，残差回响修正导致该约束准确率下降
3. **计算开销**：每个节点独立去噪进程，场景复杂度大时计算成本线性增长
4. **单数据集验证**：仅在 SG-FRONT 上评估，跨数据集泛化性待验证

## Reusable Claims

> **Claim 1**: 信息回响机制通过去噪进程中节点间的全局状态交换，可显著提升多物体场景生成的形状一致性和布局合规性。
> **Evidence**: Tab.3 CD 值全面优于 CommonScenes（Bedroom 衣柜 CD 0.14 vs 0.61，餐桌 CD 3.02 vs 11.75）；Tab.4 移除 shape echoes 后 FID 降 7.14、KID 升 2.93×。
> **Scope**: 3D 室内场景，SG-FRONT 数据集
> **Confidence**: high

> **Claim 2**: 扩散模型逆工作流策略（从伪图出发恢复 ground truth）无需 GAN 辅助即可实现场景图操控，比 VAE+GAN 方案更稳定。
> **Evidence**: Tab.2 EchoScene/布局在关系变更和节点添加模式下大多数约束准确率领先；无 GAN 训练不稳定问题。
> **Scope**: 场景图操控（节点添加、关系变更）
> **Confidence**: medium

> **Claim 3**: π(t) 时间编码对性能影响微弱，去噪步骤本身已蕴含足够的时间信息。
> **Evidence**: Tab.4 w/o π(t) 仅 FID 从 39.74 升至 40.55（+0.81），FIDCLIP 不变。
> **Scope**: SG-FRONT，1000 步扩散
> **Confidence**: medium

## Connections

- **CommonScenes**[58]：前身工作，VAE+GAN 处理布局、LDM 做形状。EchoScene 全文多处对比，信息回响解决了 CommonScenes 的隔离问题
- **Graph-to-3D**[15]：VAE 布局生成+DeepSDF 形状。EchoScene 的扩散架构在角度学习（整洁 vs 扭曲）上有明显优势
- **DiffuScene**[53]：并发工作，场景图扩散但将对象建模为 set，未利用多边信息
- **InstructScene**[32]：基于指令的 3D 室内场景合成，全局保真度好但难以维持多重图约束
- **SG-Adapter**：同为场景图→场景生成方向，但 EchoScene 是 3D 端到端生成
- **SceneTex**[9]：外接纹理生成，EchoScene 的生成场景可直接兼容
- **3D-FRONT**[16]：底层室内场景数据集，SG-FRONT 在其上添加场景图标注

## Open Questions

1. EchoScene 是否能泛化到室外或非结构化场景图？
2. 稀有关系（symmetrical 0.9%）导致的性能下降是否有数据增强或重采样方案？
3. 每个节点独立去噪进程的计算瓶颈能否通过自适应节点分组缓解？
4. 信息回响机制是否可迁移到其他图结构生成任务（如分子图、程序图）？

## Provenance

- **Raw source**: `raw/sources/2024-05-02-echoscene-indoor-scene-generation-via-information-echo-scene-graph-diffusion.pdf`
- **Extracted text**: `raw/sources/2024-05-02-echoscene-indoor-scene-generation-via-information-echo-scene-graph-diffusion.txt`
- **Evidence level**: full-paper（全文精读，实验表格和结果已完整捕获）
- **Analysis date**: 2026-06-10
