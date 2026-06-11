# SGG Datasets

> 场景图生成常用数据集索引。

## 图像 SGG 数据集

| 数据集 | 年份 | 图像数 | 对象类别 | 谓词数 | 三元组数 | 备注 |
|--------|------|-------|---------|-------|---------|------|
| **Visual Genome (VG)** | 2016 | 108K | ~80K（常用 150） | ~50K（常用 50） | ~2.3M | SGG 最主流基准，标准 VG-150 版本 |
| **GQA** | 2019 | 113K | 1,703 | 310 | — | 适合语言一致性的 SGG |
| **VRD** | 2017 | 5K | 100 | 70 | 37K | 视觉关系检测标准 |
| **HICO-DET** | 2018 | 47K | — | 117 (HOI) | — | 人-物交互检测 |
| **OI (Open Images) V6** | 2020 | ~9M | 600 | — | — | 大规模开放基准，含关系标注子集 |

## Panoptic SGG 数据集

| 数据集 | 年份 | 图像数 | 对象类 | 谓词数 | 三元组数 | 备注 |
|--------|------|-------|-------|-------|---------|------|
| **PSG** | 2023 | 49K | 56 | 57 | 247K | 首篇 panoptic SGG 基准，含 VG/COCO 子集 |
| **AeroEye** | 2025 | 31K | 19 | 26 | 84K | 航拍 panoptic SGG，无先验关系 |

## 视频 / 动态 SGG 数据集

| 数据集 | 年份 | 视频数 | 对象类 | 谓词数 | 备注 |
|--------|------|-------|-------|-------|------|
| **Action Genome (AG)** | 2020 | 234 | 35 | 25 | 基于 Charades 的时空 SGG |
| **VidOR (Video Object Relation)** | 2019 | 10K | 80 | 50 | 视频关系检测 |
| **PVSG** | 2023 | 229 | 48 | 22 | 视频 panoptic SGG，时空分割 + 关系 |
| **SynADL** | 2022 | 2K | 17 | 23 | 合成航拍视频 SGG |
| **OpenPVSG** | 2025 | 980 | — | — | 开放词汇视频 panoptic SGG |

## 3D SGG 数据集

| 数据集 | 年份 | 场景数 | 对象类 | 关系类 | 备注 |
|--------|------|-------|-------|-------|------|
| **3DSSG** | 2021 | ~1K | — | — | 最主流 3D SGG 基准 |
| **REVERIE / ScanRefer** | 2020 | — | — | — | 3D 视觉语言导航和引用 |
| **Habitat-Matterport 3DSG (HM3DSG)** | 2025 | 1K+ | — | — | 基于 HM3D 的大规模 3DSG 基准 |

## 合成数据集

| 数据集 | 年份 | 规模 | 备注 |
|--------|------|------|------|
| [[synthetic-visual-genome-svg|SVG]] | 2025 | 100K+ | 一键引擎生成的精确标注 SGG 合成数据 |
| [[synthetic-visual-genome-2|SVG 2]] | 2026 | — | 时空 SGG 合成数据（含视频版本） |
| [[hoiverse-synthetic-scene-graph-dataset-hoi|HOIverse]] | 2025 | 30K+ | 合成 HOI + 场景图数据集 |

## 其他数据集

- **SynADL**: 合成航拍驾驶场景 SGG
- **FAST (Urban Scene)**: 城市交通场景 SGG
- **Matterport3D**: 3D 室内场景
- **ScanNet**: 3D 重建 + 语义

## 关键数据集相关论文

- [[panoptic-video-scene-graph-generation|PVSG: Panoptic Video Scene Graph Generation]]
- [[synthetic-visual-genome-svg|SVG: Synthetic Visual Genome]]
- [[hoiverse-synthetic-scene-graph-dataset-hoi|HOIverse]]
- [[factual-benchmark-textual-scene-graph-parsing|FACTUAL: Textual Scene Graph Benchmark]]
- [[2025-05-29-tsg-bench-llm-meets-scene-graph|TSG Bench: LLM Scene Graph Understanding Benchmark]]
