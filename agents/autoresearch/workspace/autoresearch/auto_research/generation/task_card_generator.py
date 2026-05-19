"""Generate AutoResearch task cards for generated projects."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from auto_research.core.task_card import validate_task_card


class TaskCardGenerator:
    """Convert a generated project and implementation plan into task_card.yaml."""

    def generate(
        self,
        project_dir: str | Path,
        plan: dict[str, Any],
        output_path: str | Path | None = None,
        allow_unvalidated: bool = False,
    ) -> dict[str, Any]:
        """Generate a task card dictionary, optionally saving it to disk."""

        root = Path(project_dir)
        self._check_generation_inputs(root, allow_unvalidated=allow_unvalidated)

        task_name = self._task_name(plan, root)
        adapter_requirements = plan.get("adapter_requirements", {})
        adapter_type = adapter_requirements.get("adapter_type") or "pytorch_yaml"
        search_space = dict(plan.get("search_space", {}))
        objective = self._objective(plan)

        task_card = {
            "task_name": task_name,
            "adapter": self._adapter_section(root, adapter_type, adapter_requirements),
            "search_space": search_space,
            "score": {
                "primary_metric": objective["metric"],
                "invalid_score": -1000000000,
            },
            "constraints": {
                "timeout": 300,
                "max_trials": 5,
            },
            "safety": {
                "allow_commands": ["python", "python3"],
            },
            "objective": objective,
            "objective_policy": self._objective_policy(plan, objective),
            "evaluator": {
                "type": "json",
                "metrics_path": str((root / "outputs" / "metrics.json").resolve()),
            },
            "run": {
                "project_dir": str(root.resolve()),
                "output_dir": str((root / "outputs").resolve()),
            },
        }

        secondary_metrics = self._secondary_metric_weights(plan)
        if secondary_metrics:
            task_card["score"]["secondary_metrics"] = secondary_metrics

        is_valid, message = validate_task_card(task_card)
        if not is_valid:
            raise ValueError(f"Generated task card is not compatible: {message}")

        if output_path is not None:
            self.save(task_card, output_path)

        return task_card

    def save(self, task_card: dict[str, Any], output_path: str | Path) -> None:
        """Save a task card dictionary to YAML."""

        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as handle:
            yaml.safe_dump(task_card, handle, sort_keys=False, allow_unicode=True)

    def _check_generation_inputs(self, root: Path, *, allow_unvalidated: bool) -> None:
        if not root.exists() or not root.is_dir():
            raise FileNotFoundError(f"Generated project directory does not exist: '{root}'.")

        required_files = [root / "configs" / "config.yaml", root / "train.py"]
        missing = [str(path) for path in required_files if not path.exists()]
        if missing:
            raise FileNotFoundError(f"Generated project is missing required files: {missing!r}.")

        validation_path = root / "validation_result.json"
        if not validation_path.exists():
            if allow_unvalidated:
                return
            raise FileNotFoundError(
                "validation_result.json is required before generating task_card.yaml. "
                "Run validate-project first or pass allow_unvalidated=True."
            )

        try:
            validation_result = json.loads(validation_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"validation_result.json is not valid JSON: {exc}") from exc

        if validation_result.get("passed") is not True and not allow_unvalidated:
            raise ValueError(
                "Project validation did not pass. Refusing to generate task_card.yaml "
                "without allow_unvalidated=True."
            )

    def _adapter_section(
        self,
        root: Path,
        adapter_type: str,
        adapter_requirements: dict[str, Any],
    ) -> dict[str, Any]:
        train_entry = root / str(adapter_requirements.get("train_entry") or "train.py")
        config_path = root / str(adapter_requirements.get("config_path") or "configs/config.yaml")
        output_root = root / "autoresearch_outputs"

        if adapter_type == "pytorch_argparse":
            return {
                "type": "pytorch_argparse",
                "train_entry": str(train_entry.resolve()),
                "output_dir_arg": str(adapter_requirements.get("output_dir_arg") or "--output-dir"),
                "fixed_args": list(adapter_requirements.get("fixed_args", [])),
                "param_arg_map": dict(adapter_requirements.get("param_arg_map", {})),
                "output_root": str(output_root.resolve()),
                "metrics_filenames": ["metrics.json"],
            }

        if adapter_type == "subprocess":
            return {
                "type": "subprocess",
                "command_template": [
                    "python",
                    str(train_entry.resolve()),
                    "--config",
                    str(config_path.resolve()),
                    "--max-steps",
                    "1",
                ],
                "output_root": str(output_root.resolve()),
                "metrics_filenames": ["metrics.json"],
            }

        return {
            "type": "pytorch_yaml",
            "train_entry": str(train_entry.resolve()),
            "base_config_path": str(config_path.resolve()),
            "config_arg_name": "--config",
            "output_dir_key": "output.dir",
            "fixed_args": list(adapter_requirements.get("fixed_args", [])),
            "param_key_map": self._param_key_map(adapter_requirements, root),
            "output_root": str(output_root.resolve()),
            "metrics_filenames": ["metrics.json"],
        }

    def _param_key_map(self, adapter_requirements: dict[str, Any], root: Path) -> dict[str, str]:
        explicit = dict(adapter_requirements.get("param_arg_map", {}))
        if explicit:
            return explicit

        config = self._load_generated_config(root)
        training = config.get("training", {}) if isinstance(config, dict) else {}
        mapping: dict[str, str] = {}
        for key in ("lr", "batch_size", "epochs", "weight_decay"):
            if key in training:
                mapping[key] = f"training.{key}"
        return mapping

    def _load_generated_config(self, root: Path) -> dict[str, Any]:
        config_path = root / "configs" / "config.yaml"
        try:
            data = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
        except (OSError, yaml.YAMLError):
            return {}
        return data if isinstance(data, dict) else {}

    def _task_name(self, plan: dict[str, Any], root: Path) -> str:
        project = plan.get("project", {})
        name = project.get("name")
        if isinstance(name, str) and name.strip():
            return name
        task_card_requirements = plan.get("task_card_requirements", {})
        name = task_card_requirements.get("task_name")
        if isinstance(name, str) and name.strip():
            return name
        return root.name

    def _objective(self, plan: dict[str, Any]) -> dict[str, str]:
        task_card = plan.get("task_card_requirements", {})
        objective = task_card.get("objective", {}) if isinstance(task_card, dict) else {}
        metric = objective.get("metric")
        direction = objective.get("direction")
        project = plan.get("project", {})
        return {
            "metric": str(metric or project.get("primary_metric") or "loss"),
            "direction": str(direction or project.get("optimization_direction") or "maximize"),
        }

    def _objective_policy(
        self,
        plan: dict[str, Any],
        objective: dict[str, str],
    ) -> dict[str, Any]:
        task_card = plan.get("task_card_requirements", {})
        policy = task_card.get("objective_policy", {}) if isinstance(task_card, dict) else {}
        if isinstance(policy, dict) and policy:
            return policy
        return {
            "type": "single_metric",
            "primary_metric": objective["metric"],
            "direction": objective["direction"],
            "metrics": {},
            "constraints": {},
        }

    def _secondary_metric_weights(self, plan: dict[str, Any]) -> dict[str, float]:
        task_card = plan.get("task_card_requirements", {})
        evaluator = task_card.get("evaluator", {}) if isinstance(task_card, dict) else {}
        metrics = evaluator.get("metrics", []) if isinstance(evaluator, dict) else []
        objective_metric = self._objective(plan)["metric"]
        result: dict[str, float] = {}
        for metric in metrics:
            if metric and metric != objective_metric:
                result[str(metric)] = 0.0
        return result
