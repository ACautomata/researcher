# Implementation Plan

## 1. Project Summary

| field | value |
| --- | --- |
| name | rgb_ir_attention_test |
| task_type | rgb_ir_reid |
| source_type | manual |
| primary_metric | mAP |
| optimization_direction | maximize |

## 2. Selected Baseline Template

| field | value |
| --- | --- |
| selected | rgb_ir_reid |
| fallback | general_pytorch |
| reason | RTS baseline.template is explicitly provided. |
| warnings | [] |

## 3. Files to Create

| path | purpose | module_type |
| --- | --- | --- |
| models/modality_attention.py | Implement modality_attention. | model_component |
| models/shared_embedding.py | Implement shared_embedding. | model_component |
| losses/center_constraint.py | feature compactness constraint | loss |

## 4. Files to Modify

| path | purpose | module_type |
| --- | --- | --- |
| configs/config.yaml | Add project, model, dataset, training, and evaluation settings. | configs |
| train.py | Expose a clean training entry for adapter execution. | train.py |
| models/build.py | Register generated modules for config-based construction. | models |
| losses/build.py | Register generated modules for config-based construction. | losses |
| evaluators/reid_evaluator.py | Implement or update task-specific evaluation. | evaluators |
| datasets/reid_dataset.py | Implement or update task-specific dataset loading. | datasets |
| datasets/rgb_ir_dataset.py | Implement or update task-specific dataset loading. | datasets |
| models/two_stream_baseline.py | Implement or update task-specific model baseline. | models |

## 5. Model Components

| name | type | purpose | input | output | params |
| --- | --- | --- | --- | --- | --- |
| modality_attention | channel_spatial_attention | Not specified | Not specified | Not specified | {} |
| shared_embedding | Not specified | Not specified | Not specified | Not specified | dimension: 512 |

## 6. Loss Functions

| name | weight | params | implementation_file | expected_role |
| --- | --- | --- | --- | --- |
| cross_entropy | 1.0 | {} | built_in_or_template | identity classification or class supervision |
| triplet | 1.0 | margin: 0.3 | built_in_or_template | metric learning supervision |
| center_constraint | 0.01 | {} | losses/center_constraint.py | feature compactness constraint |

## 7. Config Requirements

```yaml
project:
  name: rgb_ir_attention_test
  task_type: rgb_ir_reid
model:
  backbone:
    name: resnet50
    pretrained: true
  components:
  - name: modality_attention
    type: channel_spatial_attention
  - name: shared_embedding
    dimension: 512
  heads:
  - name: identity_classifier
    type: linear
  - name: embedding_head
    type: projection
losses:
- name: cross_entropy
  weight: 1.0
  params: {}
- name: triplet
  weight: 1.0
  params:
    margin: 0.3
- name: center_constraint
  weight: 0.01
  params: {}
training:
  optimizer: adam
  scheduler: cosine
  batch_size: 64
  epochs: 80
  lr: 0.0003
  weight_decay: 0.0005
  mixed_precision: true
dataset:
  use_dummy: true
  modalities:
  - RGB
  - IR
  datasets:
  - name: SYSU-MM01
    path: data/sysu-mm01
    split: standard
    notes: Placeholder path; update before training.
evaluation:
  primary_metric: mAP
  secondary_metrics:
  - rank1
  - rank5
```

## 8. Search Space

```yaml
lr:
  type: float
  low: 1.0e-05
  high: 0.001
  log: true
batch_size:
  type: categorical
  choices:
  - 32
  - 64
center_loss_weight:
  type: float
  low: 0.001
  high: 0.1
  log: true
```

## 9. Validation Checks

- import_check
- dummy_forward
- loss_backward
- one_batch_train
- config_load
- checkpoint_save_load

## 10. Adapter Requirements

| field | value |
| --- | --- |
| adapter_type | pytorch_yaml |
| train_entry | train.py |
| config_path | configs/config.yaml |
| output_dir_arg | Not specified |
| fixed_args | [] |
| param_arg_map | {} |

## 11. Task Card Requirements

```yaml
task_name: rgb_ir_attention_test
adapter:
  adapter_type: pytorch_yaml
  train_entry: train.py
  config_path: configs/config.yaml
  output_dir_arg: Not specified
  fixed_args: []
  param_arg_map: {}
search_space:
  lr:
    type: float
    low: 1.0e-05
    high: 0.001
    log: true
  batch_size:
    type: categorical
    choices:
    - 32
    - 64
  center_loss_weight:
    type: float
    low: 0.001
    high: 0.1
    log: true
objective:
  metric: mAP
  direction: maximize
evaluator:
  type: json_or_log_parser
  metrics:
  - mAP
  - rank1
  - rank5
  - rank10
```

## 12. Manual Review Items

- confirm real dataset path
- confirm whether selected template matches the research idea
- confirm metric implementation
- confirm search space ranges
- confirm generated custom modules match the paper or idea
- confirm RGB/IR pairing strategy and evaluation protocol

## 13. Warnings

- RGB-IR task may require modality fusion component.
