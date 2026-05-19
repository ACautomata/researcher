# Validation Report

## Project

- project_dir: generated_projects\rgb_ir_attention_test
- config_path: generated_projects\rgb_ir_attention_test\configs\config.yaml

## Summary

- passed: True
- total_checks: 10

## Checks

### required_files_exist

- passed: True
- details: All required files exist.

### config_exists

- passed: True
- details: Config exists: generated_projects\rgb_ir_attention_test\configs\config.yaml

### py_compile

- passed: True
- details: Command completed successfully.
- command: `S:\anaconda\python.exe -m py_compile train.py test.py`
- returncode: 0
- stdout: None
- stderr: None

### import_check

- passed: True
- details: Command completed successfully.
- command: `S:\anaconda\python.exe -c import models; import losses; import datasets; import trainers; import evaluators`
- returncode: 0
- stdout: None
- stderr: None

### config_load

- passed: True
- details: Command completed successfully.
- command: `S:\anaconda\python.exe train.py --config configs\config.yaml --dry-run`
- returncode: 0
- stdout: dry-run ok
- stderr: None

### dummy_forward

- passed: True
- details: Command completed successfully.
- command: `S:\anaconda\python.exe test.py --config configs\config.yaml --mode dummy-forward`
- returncode: 0
- stdout: {'dummy_forward': True, 'embedding_shape': [2, 128], 'logits_shape': [2, 4]}
- stderr: None

### one_batch_train

- passed: True
- details: Command completed successfully.
- command: `S:\anaconda\python.exe train.py --config configs\config.yaml --max-steps 1`
- returncode: 0
- stdout: {'loss': 1.3936680555343628, 'mAP': 0.12, 'Rank-1': 0.18, 'mINP': 0.08}
- stderr: None

### checkpoint_exists

- passed: True
- details: File exists: generated_projects\rgb_ir_attention_test\outputs\checkpoint.pt

### metrics_json_exists

- passed: True
- details: File exists: generated_projects\rgb_ir_attention_test\outputs\metrics.json

### metrics_json_valid

- passed: True
- details: metrics.json is valid.

## Errors

- None

## Warnings

- None

## Next Steps

- If validation passed, the project is ready for task card generation.
- If validation failed, inspect errors and command stderr before handoff.
