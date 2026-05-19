# Requirement Document

## 1. Document Role in the Auto-Research Pipeline

This requirement.md is generated from RTS. It is a bridge between research understanding and code generation.

Pipeline position:

```text
idea / paper / manual input
-> RTS
-> requirement.md
-> implementation_plan
-> generated_project
-> task_card / adapter_config
-> existing auto-training module
```

This document should guide ProjectGenerator and ImplementationAgent. It is not a paper summary, not final code, and does not directly launch training. Training is handled by the existing auto_research training framework.

Upstream inputs include idea reader, paper reader, manual RTS, and RTS validator. Downstream consumers include implementation planner, project generator, task card generator, existing auto-training adapters, and the existing study / objective / recorder system.

## 2. Project Overview

| field | value |
| --- | --- |
| project_name | rgb_ir_attention_test |
| source_type | manual |
| source_path | Not specified |
| task_type | rgb_ir_reid |
| learning_paradigm | supervised |
| description | RGB-IR cross-modal person re-identification attention baseline. |

## 3. Research Problem and Goal

| field | value |
| --- | --- |
| research_problem | Learn discriminative cross-modal embeddings that align RGB and IR person images for retrieval. |
| primary_metric | mAP |
| optimization_direction | maximize |
| secondary_metrics | rank1, rank5 |

The optimization objective is to improve the primary metric.

## 4. Task Definition

Engineering definition for the generated project:

| field | value |
| --- | --- |
| task.type | rgb_ir_reid |
| input modalities | RGB, IR |
| output type | embedding |
| primary metric | mAP |
| selected baseline template | rgb_ir_reid |

## 5. Input and Output Specification

| field | value |
| --- | --- |
| modalities | RGB, IR |
| data_format | paired_image_folders |
| input_shape | 3, 256, 128 |
| output.type | embedding |
| output.dimension | 512 |
| output.description | Person identity embedding for cross-modal retrieval. |

## 6. Baseline Template Requirement

| field | value |
| --- | --- |
| baseline.template | rgb_ir_reid |
| baseline.name | RGB-IR attention baseline |
| baseline.source | Not specified |
| baseline.description | Dual-modality baseline with identity and metric learning losses. |

ProjectGenerator should prioritize the `rgb_ir_reid` template when creating the generated project.

## 7. Model Requirements

Backbone: `name: resnet50; pretrained: True`

Components:

| name | type | purpose | input | output | params |
| --- | --- | --- | --- | --- | --- |
| modality_attention | channel_spatial_attention | Not specified | Not specified | Not specified | Not specified |
| shared_embedding | Not specified | Not specified | Not specified | Not specified | dimension: 512 |

Heads:

| name | type | output | params |
| --- | --- | --- | --- |
| identity_classifier | linear | Not specified | Not specified |
| embedding_head | projection | Not specified | Not specified |

## 8. Loss Function Requirements

| name | weight | params | expected role |
| --- | --- | --- | --- |
| cross_entropy | 1.0 | Not specified | identity classification or class supervision |
| triplet | 1.0 | margin: 0.3 | metric learning supervision |
| center_constraint | 0.01 | Not specified | feature compactness constraint |

## 9. Dataset Requirements

| name | path | split | notes |
| --- | --- | --- | --- |
| SYSU-MM01 | data/sysu-mm01 | standard | Placeholder path; update before training. |

## 10. Training Requirements

Missing fields use recommended defaults in this document only; the RTS object is not modified.

| field | value |
| --- | --- |
| optimizer | adam |
| scheduler | cosine |
| batch_size | 64 |
| epochs | 80 |
| lr | 0.0003 |
| weight_decay | 0.0005 |
| mixed_precision | True |

## 11. Evaluation Metrics

| field | value |
| --- | --- |
| primary_metric | mAP |
| secondary_metrics | rank1, rank5 |
| all_recorded_metrics | mAP, rank1, rank5, rank10 |

The primary_metric will be used by HPO / sweep objective. Secondary metrics will be recorded for analysis. The actual metric parser should be configured through existing evaluators:

- auto_research/evaluators/json_parser.py
- auto_research/evaluators/log_parser.py

## 12. Hyperparameter Search Space

| parameter | type | range_or_choices | log | description |
| --- | --- | --- | --- | --- |
| batch_size | categorical | 32, 64 | false | Not specified |
| center_loss_weight | float | [0.001, 0.1] | True | Not specified |
| lr | float | [1e-05, 0.001] | True | Not specified |

search_space will be converted or mapped to the existing auto_research/search_space module.

## 13. Ablation Study Design

| name | description | config_overrides |
| --- | --- | --- |
| without_modality_attention | Disable cross-modal attention module. | model.components.modality_attention.enabled: False |

## 14. Generated Project Requirements

The generated project should include at least:

- configs/config.yaml
- train.py
- test.py
- models/
- losses/
- datasets/
- trainers/
- evaluators/
- scripts/run_train.sh
- README.md

RTS required_files:

- train.py
- configs/config.yaml
- models/model.py
- losses.py

RTS expected_modules:

- models
- datasets
- losses
- metrics

Implementation notes: Generated project should expose a YAML-driven training entry.

The first generated version should be runnable with dummy data. Real dataset adaptation can be done later. No absolute paths should be hard-coded. The generated project should expose a clean training entry for adapters.

## 15. Validation Criteria

| check | requirement |
| --- | --- |
| import_check | All generated modules can be imported. |
| dummy_forward | Model can run a forward pass with dummy inputs. |
| loss_backward | Loss can be computed and backpropagated. |
| one_batch_train | Trainer can run one batch without crashing. |
| config_load | configs/config.yaml can be loaded successfully. |
| checkpoint_save_load | Checkpoint save and load both work. |

RTS requested checks:

- import_check
- dummy_forward
- loss_backward
- one_batch_train
- config_load
- checkpoint_save_load

The generated project must pass validation before being submitted to the existing auto-training module.

## 16. Interface with Existing Auto-Training Module

- This module does not reimplement training scheduling.
- This module does not reimplement HPO.
- This module does not reimplement result recording.
- The generated project should be connected to existing auto_research adapters.
- Existing adapters include:
  - pytorch_argparse
  - pytorch_yaml
  - subprocess

| field | value |
| --- | --- |
| adapter.type | pytorch_yaml |
| adapter.train_entry | train.py |
| adapter.config_path | configs/config.yaml |
| adapter.output_dir_arg | Not specified |
| adapter.fixed_args | Not specified |
| adapter.param_arg_map | Not specified |

Fallback recommendations are pytorch_yaml for adapter.type, train.py for adapter.train_entry, and configs/config.yaml for adapter.config_path.

Handoff path:

```text
RTS
-> requirement.md
-> generated_project
-> task_card.yaml
-> existing adapter
-> existing study/objective/recorder
```

task_card will be generated in a later stage. search_space will be mapped to the existing search_space module. metrics will be parsed by existing evaluators. Experiments will be managed by existing study.py and recorder.py.

## 17. Risks and Manual Confirmation Items

- generated implementation may be a runnable approximation rather than exact paper reproduction
- real dataset interface may require manual adaptation
- metric implementation may need task-specific refinement
- hyperparameter search space may require expert adjustment
- paper or idea details may be incomplete or ambiguous
- selected baseline template may not perfectly match the research idea

## 18. Summary for Next Stage

- ImplementationPlanner should convert this requirement into implementation_plan.md or implementation_plan.yaml.
- ProjectGenerator should create a runnable project from the selected template.
- ValidationAgent should run dummy validation.
- TaskCardGenerator should generate task_card.yaml for the existing training framework.
- Existing auto-training module should handle training and HPO.
