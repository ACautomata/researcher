"""Build machine-readable and human-readable implementation plans from RTS."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from auto_research.planning.baseline_selector import BaselineSelector
from auto_research.rts.schema import ResearchTaskSpecification

_BASE_MODEL_COMPONENT_NAMES = {"baseline", "backbone", "classifier"}
_BASE_LOSS_NAMES = {"cross_entropy", "triplet", "mse", "l1"}
_DEFAULT_VALIDATION_CHECKS = [
    "import_check",
    "dummy_forward",
    "loss_backward",
    "one_batch_train",
    "config_load",
    "checkpoint_save_load",
]


class ImplementationPlanner:
    """Convert RTS objects into implementation plans."""

    def __init__(self) -> None:
        """Initialize the planner with the default baseline selector."""

        self.baseline_selector = BaselineSelector()

    def build_plan(self, rts: ResearchTaskSpecification) -> dict[str, Any]:
        """Build a machine-readable implementation plan from RTS."""

        template_selection = self.baseline_selector.select(rts)
        warnings = list(template_selection.get("warnings", []))
        files_to_create = self._build_files_to_create(rts, warnings)
        files_to_modify = self._build_files_to_modify(rts)
        adapter_requirements = self._build_adapter_requirements(rts)
        task_card_requirements = self._build_task_card_requirements(
            rts,
            adapter_requirements,
        )

        return {
            "project": {
                "name": self._value(rts.meta.project_name),
                "task_type": self._value(rts.task.type),
                "source_type": self._value(rts.meta.source_type),
                "primary_metric": self._value(rts.goal.primary_metric),
                "optimization_direction": self._value(rts.goal.optimization_direction),
            },
            "template": {
                "selected": template_selection["selected_template"],
                "fallback": template_selection["fallback_template"],
                "reason": template_selection["reason"],
                "warnings": template_selection["warnings"],
            },
            "files_to_create": files_to_create,
            "files_to_modify": files_to_modify,
            "model_components": self._build_model_components(rts),
            "losses": self._build_losses(rts),
            "config_requirements": self._build_config_requirements(rts),
            "search_space": dict(rts.search_space),
            "validation_checks": self._build_validation_checks(rts),
            "adapter_requirements": adapter_requirements,
            "task_card_requirements": task_card_requirements,
            "manual_review_items": self._build_manual_review_items(rts),
            "warnings": warnings,
        }

    def render_markdown(self, plan: dict[str, Any]) -> str:
        """Render implementation plan as human-readable markdown."""

        sections = [
            "# Implementation Plan",
            self._render_project_summary(plan),
            self._render_selected_template(plan),
            self._render_files_to_create(plan),
            self._render_files_to_modify(plan),
            self._render_model_components(plan),
            self._render_losses(plan),
            self._render_config_requirements(plan),
            self._render_search_space(plan),
            self._render_validation_checks(plan),
            self._render_adapter_requirements(plan),
            self._render_task_card_requirements(plan),
            self._render_manual_review_items(plan),
            self._render_warnings(plan),
        ]
        return "\n\n".join(sections).rstrip() + "\n"

    def save_yaml(self, plan: dict[str, Any], output_path: str | Path) -> None:
        """Save a machine-readable implementation plan YAML file."""

        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as handle:
            yaml.safe_dump(plan, handle, sort_keys=False, allow_unicode=True)

    def save_markdown(self, markdown_text: str, output_path: str | Path) -> None:
        """Save a human-readable implementation plan markdown file."""

        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(markdown_text, encoding="utf-8")

    def _build_files_to_create(
        self,
        rts: ResearchTaskSpecification,
        warnings: list[str],
    ) -> list[dict[str, str]]:
        files: list[dict[str, str]] = []
        for component in rts.model.components:
            name = str(component.get("name", "")).strip()
            if not name or name in _BASE_MODEL_COMPONENT_NAMES:
                continue
            files.append(
                {
                    "path": f"models/{name}.py",
                    "purpose": self._value(component.get("purpose"), f"Implement {name}."),
                    "module_type": "model_component",
                }
            )

        for loss in rts.losses:
            name = str(loss.get("name", "")).strip()
            if not name or name in _BASE_LOSS_NAMES:
                continue
            files.append(
                {
                    "path": f"losses/{name}.py",
                    "purpose": self._loss_role(name),
                    "module_type": "loss",
                }
            )

        if self._is_rgb_ir_reid(rts) and not self._has_fusion_component(rts):
            warnings.append("RGB-IR task may require modality fusion component.")

        return files

    def _build_files_to_modify(self, rts: ResearchTaskSpecification) -> list[dict[str, str]]:
        paths = [
            "configs/config.yaml",
            "train.py",
            "models/build.py",
            "losses/build.py",
        ]
        task_type = rts.task.type
        if task_type in {"person_reid", "rgb_ir_reid"} or "reid" in task_type:
            paths.extend(["evaluators/reid_evaluator.py", "datasets/reid_dataset.py"])
        if task_type == "rgb_ir_reid":
            paths.extend(["datasets/rgb_ir_dataset.py", "models/two_stream_baseline.py"])
        if task_type == "pose_estimation":
            paths.extend(["evaluators/pose_evaluator.py", "datasets/pose_dataset.py"])
        if task_type in {"shadow_removal", "diffusion_restoration"}:
            paths.extend(["evaluators/restoration_evaluator.py", "datasets/image_pair_dataset.py"])

        return [
            {
                "path": path,
                "purpose": self._file_modify_purpose(path),
                "module_type": self._module_type_for_path(path),
            }
            for path in self._unique(paths)
        ]

    def _build_model_components(self, rts: ResearchTaskSpecification) -> list[dict[str, Any]]:
        return [
            {
                "name": self._value(component.get("name")),
                "type": self._value(component.get("type")),
                "purpose": self._value(component.get("purpose")),
                "input": self._value(component.get("input")),
                "output": self._value(component.get("output")),
                "params": self._remaining_params(
                    component,
                    {"name", "type", "purpose", "input", "output"},
                ),
            }
            for component in rts.model.components
        ]

    def _build_losses(self, rts: ResearchTaskSpecification) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = []
        for loss in rts.losses:
            name = self._value(loss.get("name"))
            implementation_file = (
                f"losses/{name}.py" if name not in _BASE_LOSS_NAMES else "built_in_or_template"
            )
            result.append(
                {
                    "name": name,
                    "weight": loss.get("weight", "Not specified"),
                    "params": loss.get("params", {}),
                    "implementation_file": implementation_file,
                    "expected_role": self._loss_role(name),
                }
            )
        return result

    def _build_config_requirements(self, rts: ResearchTaskSpecification) -> dict[str, Any]:
        return {
            "project": {
                "name": self._value(rts.meta.project_name),
                "task_type": self._value(rts.task.type),
            },
            "model": {
                "backbone": dict(rts.model.backbone),
                "components": list(rts.model.components),
                "heads": list(rts.model.heads),
            },
            "losses": list(rts.losses),
            "training": {
                "optimizer": rts.training.optimizer or "AdamW",
                "scheduler": rts.training.scheduler or "cosine",
                "batch_size": rts.training.batch_size or 32,
                "epochs": rts.training.epochs or 1,
                "lr": rts.training.lr or 1e-4,
                "weight_decay": rts.training.weight_decay or 5e-4,
                "mixed_precision": (
                    rts.training.mixed_precision
                    if rts.training.mixed_precision is not None
                    else False
                ),
            },
            "dataset": {
                "use_dummy": True,
                "modalities": list(rts.input.modalities),
                "datasets": list(rts.datasets),
            },
            "evaluation": {
                "primary_metric": self._value(rts.goal.primary_metric),
                "secondary_metrics": list(rts.goal.secondary_metrics),
            },
        }

    def _build_validation_checks(self, rts: ResearchTaskSpecification) -> list[str]:
        return list(rts.validation.required_checks or _DEFAULT_VALIDATION_CHECKS)

    def _build_adapter_requirements(self, rts: ResearchTaskSpecification) -> dict[str, Any]:
        return {
            "adapter_type": rts.adapter.type or "pytorch_yaml",
            "train_entry": rts.adapter.train_entry or "train.py",
            "config_path": rts.adapter.config_path or "configs/config.yaml",
            "output_dir_arg": rts.adapter.output_dir_arg or "Not specified",
            "fixed_args": list(rts.adapter.fixed_args),
            "param_arg_map": dict(rts.adapter.param_arg_map),
        }

    def _build_task_card_requirements(
        self,
        rts: ResearchTaskSpecification,
        adapter_requirements: dict[str, Any],
    ) -> dict[str, Any]:
        metrics = self._unique(
            [rts.goal.primary_metric] + list(rts.goal.secondary_metrics) + list(rts.metrics)
        )
        return {
            "task_name": self._value(rts.meta.project_name),
            "adapter": adapter_requirements,
            "search_space": dict(rts.search_space),
            "objective": {
                "metric": self._value(rts.goal.primary_metric),
                "direction": self._value(rts.goal.optimization_direction),
            },
            "objective_policy": self._objective_policy(rts),
            "evaluator": {
                "type": "json_or_log_parser",
                "metrics": metrics,
            },
        }

    def _build_manual_review_items(self, rts: ResearchTaskSpecification) -> list[str]:
        items = [
            "confirm real dataset path",
            "confirm whether selected template matches the research idea",
            "confirm metric implementation",
            "confirm search space ranges",
            "confirm generated custom modules match the paper or idea",
        ]
        task_type = rts.task.type
        if task_type == "rgb_ir_reid":
            items.append("confirm RGB/IR pairing strategy and evaluation protocol")
        if task_type == "pose_estimation":
            items.append("confirm keypoint format and heatmap resolution")
        if task_type in {"shadow_removal", "diffusion_restoration"}:
            items.append("confirm image pair format and evaluation metrics")
        return items

    def _objective_policy(self, rts: ResearchTaskSpecification) -> dict[str, Any]:
        if rts.objective_policy:
            return dict(rts.objective_policy)
        extra_policy = rts.extra.get("objective_policy", {})
        if isinstance(extra_policy, dict) and extra_policy:
            return dict(extra_policy)
        return {
            "type": "single_metric",
            "primary_metric": self._value(rts.goal.primary_metric),
            "direction": self._value(rts.goal.optimization_direction),
            "metrics": {},
            "constraints": {},
        }

    def _render_project_summary(self, plan: dict[str, Any]) -> str:
        return "\n".join(
            [
                "## 1. Project Summary",
                "",
                self._kv_table(plan.get("project", {})),
            ]
        )

    def _render_selected_template(self, plan: dict[str, Any]) -> str:
        return "\n".join(
            [
                "## 2. Selected Baseline Template",
                "",
                self._kv_table(plan.get("template", {})),
            ]
        )

    def _render_files_to_create(self, plan: dict[str, Any]) -> str:
        return "\n".join(
            [
                "## 3. Files to Create",
                "",
                self._items_table(
                    ["path", "purpose", "module_type"],
                    plan.get("files_to_create", []),
                ),
            ]
        )

    def _render_files_to_modify(self, plan: dict[str, Any]) -> str:
        return "\n".join(
            [
                "## 4. Files to Modify",
                "",
                self._items_table(
                    ["path", "purpose", "module_type"],
                    plan.get("files_to_modify", []),
                ),
            ]
        )

    def _render_model_components(self, plan: dict[str, Any]) -> str:
        return "\n".join(
            [
                "## 5. Model Components",
                "",
                self._items_table(
                    ["name", "type", "purpose", "input", "output", "params"],
                    plan.get("model_components", []),
                ),
            ]
        )

    def _render_losses(self, plan: dict[str, Any]) -> str:
        return "\n".join(
            [
                "## 6. Loss Functions",
                "",
                self._items_table(
                    ["name", "weight", "params", "implementation_file", "expected_role"],
                    plan.get("losses", []),
                ),
            ]
        )

    def _render_config_requirements(self, plan: dict[str, Any]) -> str:
        return "\n".join(
            [
                "## 7. Config Requirements",
                "",
                "```yaml",
                yaml.safe_dump(
                    plan.get("config_requirements", {}),
                    sort_keys=False,
                    allow_unicode=True,
                ).rstrip(),
                "```",
            ]
        )

    def _render_search_space(self, plan: dict[str, Any]) -> str:
        return "\n".join(
            [
                "## 8. Search Space",
                "",
                "```yaml",
                yaml.safe_dump(
                    plan.get("search_space", {}),
                    sort_keys=False,
                    allow_unicode=True,
                ).rstrip(),
                "```",
            ]
        )

    def _render_validation_checks(self, plan: dict[str, Any]) -> str:
        return "\n".join(
            [
                "## 9. Validation Checks",
                "",
                self._list_block(plan.get("validation_checks", [])),
            ]
        )

    def _render_adapter_requirements(self, plan: dict[str, Any]) -> str:
        return "\n".join(
            [
                "## 10. Adapter Requirements",
                "",
                self._kv_table(plan.get("adapter_requirements", {})),
            ]
        )

    def _render_task_card_requirements(self, plan: dict[str, Any]) -> str:
        return "\n".join(
            [
                "## 11. Task Card Requirements",
                "",
                "```yaml",
                yaml.safe_dump(
                    plan.get("task_card_requirements", {}),
                    sort_keys=False,
                    allow_unicode=True,
                ).rstrip(),
                "```",
            ]
        )

    def _render_manual_review_items(self, plan: dict[str, Any]) -> str:
        return "\n".join(
            [
                "## 12. Manual Review Items",
                "",
                self._list_block(plan.get("manual_review_items", [])),
            ]
        )

    def _render_warnings(self, plan: dict[str, Any]) -> str:
        return "\n".join(
            [
                "## 13. Warnings",
                "",
                self._list_block(plan.get("warnings", [])),
            ]
        )

    def _items_table(self, headers: list[str], items: list[dict[str, Any]]) -> str:
        if not items:
            return "Not specified"
        rows = [[self._format_cell(item.get(header, "Not specified")) for header in headers] for item in items]
        return self._table(headers, rows)

    def _kv_table(self, mapping: dict[str, Any]) -> str:
        if not mapping:
            return "Not specified"
        rows = [[key, self._format_cell(value)] for key, value in mapping.items()]
        return self._table(["field", "value"], rows)

    def _table(self, headers: list[str], rows: list[list[Any]]) -> str:
        header = "| " + " | ".join(headers) + " |"
        separator = "| " + " | ".join(["---"] * len(headers)) + " |"
        body = ["| " + " | ".join(self._format_cell(cell) for cell in row) + " |" for row in rows]
        return "\n".join([header, separator, *body])

    def _list_block(self, items: list[Any]) -> str:
        if not items:
            return "Not specified"
        return "\n".join(f"- {self._format_cell(item)}" for item in items)

    def _file_modify_purpose(self, path: str) -> str:
        if path == "configs/config.yaml":
            return "Add project, model, dataset, training, and evaluation settings."
        if path == "train.py":
            return "Expose a clean training entry for adapter execution."
        if path.endswith("build.py"):
            return "Register generated modules for config-based construction."
        if path.startswith("evaluators/"):
            return "Implement or update task-specific evaluation."
        if path.startswith("datasets/"):
            return "Implement or update task-specific dataset loading."
        if path.startswith("models/"):
            return "Implement or update task-specific model baseline."
        return "Update generated project integration."

    def _module_type_for_path(self, path: str) -> str:
        return path.split("/", maxsplit=1)[0]

    def _loss_role(self, name: Any) -> str:
        roles = {
            "cross_entropy": "identity classification or class supervision",
            "triplet": "metric learning supervision",
            "center_constraint": "feature compactness constraint",
            "contrastive": "representation alignment",
            "mse": "reconstruction supervision",
            "l1": "reconstruction supervision",
            "dice": "segmentation overlap supervision",
            "focal": "hard example or class imbalance handling",
        }
        return roles.get(str(name), "custom loss defined by RTS")

    def _remaining_params(self, item: dict[str, Any], skip: set[str]) -> dict[str, Any]:
        return {key: value for key, value in item.items() if key not in skip}

    def _is_rgb_ir_reid(self, rts: ResearchTaskSpecification) -> bool:
        modalities = {str(item).upper() for item in rts.input.modalities}
        return rts.task.type == "rgb_ir_reid" and {"RGB", "IR"}.issubset(modalities)

    def _has_fusion_component(self, rts: ResearchTaskSpecification) -> bool:
        for component in rts.model.components:
            name = str(component.get("name", "")).lower()
            component_type = str(component.get("type", "")).lower()
            if "fusion" in name or "fusion" in component_type:
                return True
        return False

    def _unique(self, values: list[Any]) -> list[Any]:
        result: list[Any] = []
        for value in values:
            if value and value not in result:
                result.append(value)
        return result

    def _value(self, value: Any, fallback: str = "Not specified") -> str:
        if value is None:
            return fallback
        if isinstance(value, str) and not value.strip():
            return fallback
        return str(value)

    def _format_cell(self, value: Any) -> str:
        if value is None:
            text = "Not specified"
        elif isinstance(value, (dict, list)):
            text = yaml.safe_dump(value, sort_keys=False, allow_unicode=True).strip()
        else:
            text = str(value)
        return text.replace("|", "\\|").replace("\n", "<br>")
