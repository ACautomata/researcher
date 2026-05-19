"""Generate engineering requirement documents from RTS objects."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from auto_research.rts.schema import ResearchTaskSpecification

_RECOMMENDED_CHECKS = [
    "import_check",
    "dummy_forward",
    "loss_backward",
    "one_batch_train",
    "config_load",
    "checkpoint_save_load",
]

_DEFAULT_PROJECT_FILES = [
    "configs/config.yaml",
    "train.py",
    "test.py",
    "models/",
    "losses/",
    "datasets/",
    "trainers/",
    "evaluators/",
    "scripts/run_train.sh",
    "README.md",
]

_DEFAULT_RISKS = [
    "generated implementation may be a runnable approximation rather than exact paper reproduction",
    "real dataset interface may require manual adaptation",
    "metric implementation may need task-specific refinement",
    "hyperparameter search space may require expert adjustment",
    "paper or idea details may be incomplete or ambiguous",
    "selected baseline template may not perfectly match the research idea",
]


class RequirementGenerator:
    """Convert a ResearchTaskSpecification into stable Markdown requirements."""

    def generate(self, rts: ResearchTaskSpecification) -> str:
        """
        Generate a human-readable engineering requirement document from an RTS.

        The generated text is deterministic and does not mutate the input RTS object.
        """

        sections = [
            "# Requirement Document",
            self._render_document_role(),
            self._render_project_overview(rts),
            self._render_research_problem_and_goal(rts),
            self._render_task_definition(rts),
            self._render_input_output(rts),
            self._render_baseline(rts),
            self._render_model_requirements(rts),
            self._render_loss_requirements(rts),
            self._render_dataset_requirements(rts),
            self._render_training_requirements(rts),
            self._render_evaluation_metrics(rts),
            self._render_search_space(rts),
            self._render_ablation(rts),
            self._render_generated_project(rts),
            self._render_validation_criteria(rts),
            self._render_auto_training_interface(rts),
            self._render_risks(rts),
            self._render_summary(),
        ]
        return "\n\n".join(sections).rstrip() + "\n"

    def save(self, requirement_text: str, output_path: str | Path) -> None:
        """
        Save the generated requirement document to a markdown file.

        Parent directories are created automatically.
        """

        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(requirement_text, encoding="utf-8")

    def _render_document_role(self) -> str:
        return "\n".join(
            [
                "## 1. Document Role in the Auto-Research Pipeline",
                "",
                "This requirement.md is generated from RTS. It is a bridge between "
                "research understanding and code generation.",
                "",
                "Pipeline position:",
                "",
                "```text",
                "idea / paper / manual input",
                "-> RTS",
                "-> requirement.md",
                "-> implementation_plan",
                "-> generated_project",
                "-> task_card / adapter_config",
                "-> existing auto-training module",
                "```",
                "",
                "This document should guide ProjectGenerator and ImplementationAgent. "
                "It is not a paper summary, not final code, and does not directly launch "
                "training. Training is handled by the existing auto_research training framework.",
                "",
                "Upstream inputs include idea reader, paper reader, manual RTS, and RTS "
                "validator. Downstream consumers include implementation planner, project "
                "generator, task card generator, existing auto-training adapters, and the "
                "existing study / objective / recorder system.",
            ]
        )

    def _render_project_overview(self, rts: ResearchTaskSpecification) -> str:
        rows = [
            ("project_name", self._value(rts.meta.project_name)),
            ("source_type", self._value(rts.meta.source_type)),
            ("source_path", self._value(rts.meta.source_path)),
            ("task_type", self._value(rts.task.type)),
            ("learning_paradigm", self._value(rts.task.learning_paradigm)),
            ("description", self._value(rts.meta.description)),
        ]
        return "\n".join(["## 2. Project Overview", "", self._kv_table(rows)])

    def _render_research_problem_and_goal(self, rts: ResearchTaskSpecification) -> str:
        direction = rts.goal.optimization_direction
        if direction == "maximize":
            objective = "The optimization objective is to improve the primary metric."
        elif direction == "minimize":
            objective = "The optimization objective is to reduce the primary metric."
        else:
            objective = (
                "Warning: optimization_direction is not recognized. Confirm whether "
                "the metric should be maximized or minimized."
            )

        rows = [
            ("research_problem", self._value(rts.task.research_problem)),
            ("primary_metric", self._value(rts.goal.primary_metric)),
            ("optimization_direction", self._value(direction)),
            ("secondary_metrics", self._format_list(rts.goal.secondary_metrics)),
        ]
        return "\n".join(
            [
                "## 3. Research Problem and Goal",
                "",
                self._kv_table(rows),
                "",
                objective,
                "",
                self._render_objective_policy(rts),
            ]
        )

    def _render_task_definition(self, rts: ResearchTaskSpecification) -> str:
        baseline = self._baseline_template(rts)
        rows = [
            ("task.type", self._value(rts.task.type)),
            ("input modalities", self._format_list(rts.input.modalities)),
            ("output type", self._value(rts.output.type)),
            ("primary metric", self._value(rts.goal.primary_metric)),
            ("selected baseline template", baseline),
        ]
        return "\n".join(
            [
                "## 4. Task Definition",
                "",
                "Engineering definition for the generated project:",
                "",
                self._kv_table(rows),
            ]
        )

    def _render_input_output(self, rts: ResearchTaskSpecification) -> str:
        input_shape = (
            self._format_list(rts.input.input_shape)
            if rts.input.input_shape
            else "Not specified"
        )
        shape_note = ""
        if not rts.input.input_shape:
            shape_note = (
                "\n\nFirst version may use dummy input shape defined by the selected template."
            )
        rows = [
            ("modalities", self._format_list(rts.input.modalities)),
            ("data_format", self._value(rts.input.data_format)),
            ("input_shape", input_shape),
            ("output.type", self._value(rts.output.type)),
            ("output.dimension", self._value(rts.output.dimension)),
            ("output.description", self._value(rts.output.description)),
        ]
        return "\n".join(["## 5. Input and Output Specification", "", self._kv_table(rows)]) + shape_note

    def _render_baseline(self, rts: ResearchTaskSpecification) -> str:
        rows = [
            ("baseline.template", self._value(rts.baseline.template)),
            ("baseline.name", self._value(rts.baseline.name)),
            ("baseline.source", self._value(rts.baseline.source)),
            ("baseline.description", self._value(rts.baseline.description)),
        ]
        if not self._has_text(rts.baseline.template):
            note = (
                "No explicit baseline template is provided. The system should fall back "
                "to general_pytorch."
            )
        else:
            note = (
                f"ProjectGenerator should prioritize the `{rts.baseline.template}` "
                "template when creating the generated project."
            )
        return "\n".join(
            ["## 6. Baseline Template Requirement", "", self._kv_table(rows), "", note]
        )

    def _render_model_requirements(self, rts: ResearchTaskSpecification) -> str:
        lines = [
            "## 7. Model Requirements",
            "",
            f"Backbone: `{self._format_dict(rts.model.backbone)}`",
            "",
            "Components:",
            "",
        ]
        if rts.model.components:
            lines.append(
                self._format_table(
                    ["name", "type", "purpose", "input", "output", "params"],
                    [
                        [
                            item.get("name"),
                            item.get("type"),
                            item.get("purpose"),
                            item.get("input"),
                            item.get("output"),
                            self._remaining_params(
                                item, {"name", "type", "purpose", "input", "output"}
                            ),
                        ]
                        for item in rts.model.components
                    ],
                )
            )
        else:
            lines.append(
                "First version only requires the selected baseline model. "
                "ImplementationAgent can add modules later based on RTS or manual input."
            )

        lines.extend(["", "Heads:", ""])
        if rts.model.heads:
            lines.append(
                self._format_table(
                    ["name", "type", "output", "params"],
                    [
                        [
                            item.get("name"),
                            item.get("type"),
                            item.get("output"),
                            self._remaining_params(item, {"name", "type", "output"}),
                        ]
                        for item in rts.model.heads
                    ],
                )
            )
        else:
            lines.append("Not specified")
        return "\n".join(lines)

    def _render_loss_requirements(self, rts: ResearchTaskSpecification) -> str:
        rows = [
            [
                item.get("name"),
                item.get("weight"),
                self._format_dict(item.get("params", {})),
                self._loss_role(item.get("name")),
            ]
            for item in rts.losses
        ]
        if not rows:
            rows = [["Not specified", "Not specified", "Not specified", "custom loss defined by RTS"]]
        return "\n".join(
            [
                "## 8. Loss Function Requirements",
                "",
                self._format_table(["name", "weight", "params", "expected role"], rows),
            ]
        )

    def _render_dataset_requirements(self, rts: ResearchTaskSpecification) -> str:
        lines = ["## 9. Dataset Requirements", ""]
        if rts.datasets:
            lines.append(
                self._format_table(
                    ["name", "path", "split", "notes"],
                    [
                        [
                            item.get("name"),
                            item.get("path"),
                            item.get("split"),
                            item.get("notes"),
                        ]
                        for item in rts.datasets
                    ],
                )
            )
        else:
            lines.extend(
                [
                    "- First version should support dummy dataset.",
                    "- Real dataset paths should be configured later through configs/config.yaml.",
                    "- No absolute dataset path should be hard-coded in generated code.",
                ]
            )
        return "\n".join(lines)

    def _render_training_requirements(self, rts: ResearchTaskSpecification) -> str:
        rows = [
            ("optimizer", self._value(rts.training.optimizer, "AdamW")),
            ("scheduler", self._value(rts.training.scheduler, "cosine")),
            ("batch_size", self._value(rts.training.batch_size, "32")),
            ("epochs", self._value(rts.training.epochs, "1 for dummy validation, task-specific value for real training")),
            ("lr", self._value(rts.training.lr, "1e-4")),
            ("weight_decay", self._value(rts.training.weight_decay, "5e-4")),
            ("mixed_precision", self._value(rts.training.mixed_precision, "false")),
        ]
        return "\n".join(
            [
                "## 10. Training Requirements",
                "",
                "Missing fields use recommended defaults in this document only; the RTS "
                "object is not modified.",
                "",
                self._kv_table(rows),
            ]
        )

    def _render_evaluation_metrics(self, rts: ResearchTaskSpecification) -> str:
        all_metrics = self._unique(
            [rts.goal.primary_metric] + rts.goal.secondary_metrics + rts.metrics
        )
        rows = [
            ("primary_metric", self._value(rts.goal.primary_metric)),
            ("secondary_metrics", self._format_list(rts.goal.secondary_metrics)),
            ("all_recorded_metrics", self._format_list(all_metrics)),
        ]
        return "\n".join(
            [
                "## 11. Evaluation Metrics",
                "",
                self._kv_table(rows),
                "",
                "The primary_metric will be used by HPO / sweep objective. Secondary "
                "metrics will be recorded for analysis. The actual metric parser should "
                "be configured through existing evaluators:",
                "",
                "- auto_research/evaluators/json_parser.py",
                "- auto_research/evaluators/log_parser.py",
            ]
        )

    def _render_search_space(self, rts: ResearchTaskSpecification) -> str:
        lines = ["## 12. Hyperparameter Search Space", ""]
        if rts.search_space:
            rows = []
            for name in sorted(rts.search_space):
                spec = rts.search_space[name]
                spec_type = spec.get("type") if isinstance(spec, dict) else None
                rows.append(
                    [
                        name,
                        spec_type,
                        self._range_or_choices(spec),
                        spec.get("log", "false") if isinstance(spec, dict) else "Not specified",
                        spec.get("description", "Not specified")
                        if isinstance(spec, dict)
                        else "Not specified",
                    ]
                )
            lines.append(
                self._format_table(
                    ["parameter", "type", "range_or_choices", "log", "description"],
                    rows,
                )
            )
        else:
            lines.append(
                "This task does not enable automatic hyperparameter tuning yet. "
                "A search_space can be added later to connect to the existing HPO module."
            )
        lines.extend(
            [
                "",
                "search_space will be converted or mapped to the existing "
                "auto_research/search_space module.",
            ]
        )
        return "\n".join(lines)

    def _render_ablation(self, rts: ResearchTaskSpecification) -> str:
        lines = ["## 13. Ablation Study Design", ""]
        if rts.ablation:
            lines.append(
                self._format_table(
                    ["name", "description", "config_overrides"],
                    [
                        [
                            item.get("name"),
                            item.get("description"),
                            self._format_dict(item.get("config_overrides", {})),
                        ]
                        for item in rts.ablation
                    ],
                )
            )
        else:
            lines.extend(
                [
                    "Suggested ablations:",
                    "",
                    f"- compare with selected baseline template: {self._baseline_template(rts)}",
                    "- remove each non-baseline model component",
                    "- remove each auxiliary loss",
                ]
            )
            if rts.search_space:
                lines.append("- test key hyperparameter sensitivity if search_space is provided")
            lines.append("")
            lines.append("These are recommendations only and do not modify RTS.")
        return "\n".join(lines)

    def _render_generated_project(self, rts: ResearchTaskSpecification) -> str:
        lines = [
            "## 14. Generated Project Requirements",
            "",
            "The generated project should include at least:",
            "",
            self._format_list(_DEFAULT_PROJECT_FILES, bullet=True),
        ]
        if rts.implementation.required_files:
            lines.extend(
                [
                    "",
                    "RTS required_files:",
                    "",
                    self._format_list(rts.implementation.required_files, bullet=True),
                ]
            )
        if rts.implementation.expected_modules:
            lines.extend(
                [
                    "",
                    "RTS expected_modules:",
                    "",
                    self._format_list(rts.implementation.expected_modules, bullet=True),
                ]
            )
        if self._has_text(rts.implementation.notes):
            lines.extend(["", f"Implementation notes: {rts.implementation.notes}"])
        lines.extend(
            [
                "",
                "The first generated version should be runnable with dummy data. Real "
                "dataset adaptation can be done later. No absolute paths should be "
                "hard-coded. The generated project should expose a clean training entry "
                "for adapters.",
            ]
        )
        return "\n".join(lines)

    def _render_validation_criteria(self, rts: ResearchTaskSpecification) -> str:
        checks = rts.validation.required_checks
        missing = [item for item in _RECOMMENDED_CHECKS if item not in checks]
        lines = ["## 15. Validation Criteria", ""]
        if missing:
            lines.append(
                "Warning: RTS validation.required_checks does not include all recommended "
                f"checks: {', '.join(missing)}."
            )
            lines.append("")
        lines.append(
            self._format_table(
                ["check", "requirement"],
                [[check, self._validation_check_description(check)] for check in _RECOMMENDED_CHECKS],
            )
        )
        if checks:
            lines.extend(["", "RTS requested checks:", "", self._format_list(checks, bullet=True)])
        lines.extend(
            [
                "",
                "The generated project must pass validation before being submitted to "
                "the existing auto-training module.",
            ]
        )
        return "\n".join(lines)

    def _render_auto_training_interface(self, rts: ResearchTaskSpecification) -> str:
        adapter = self._default_adapter_info(rts)
        rows = [
            ("adapter.type", adapter["type"]),
            ("adapter.train_entry", adapter["train_entry"]),
            ("adapter.config_path", adapter["config_path"]),
            ("adapter.output_dir_arg", adapter["output_dir_arg"]),
            ("adapter.fixed_args", self._format_list(adapter["fixed_args"])),
            ("adapter.param_arg_map", self._format_dict(adapter["param_arg_map"])),
        ]
        return "\n".join(
            [
                "## 16. Interface with Existing Auto-Training Module",
                "",
                "- This module does not reimplement training scheduling.",
                "- This module does not reimplement HPO.",
                "- This module does not reimplement result recording.",
                "- The generated project should be connected to existing auto_research adapters.",
                "- Existing adapters include:",
                "  - pytorch_argparse",
                "  - pytorch_yaml",
                "  - subprocess",
                "",
                self._kv_table(rows),
                "",
                "Fallback recommendations are pytorch_yaml for adapter.type, train.py "
                "for adapter.train_entry, and configs/config.yaml for adapter.config_path.",
                "",
                "Handoff path:",
                "",
                "```text",
                "RTS",
                "-> requirement.md",
                "-> generated_project",
                "-> task_card.yaml",
                "-> existing adapter",
                "-> existing study/objective/recorder",
                "```",
                "",
                "task_card will be generated in a later stage. search_space will be "
                "mapped to the existing search_space module. metrics will be parsed by "
                "existing evaluators. Experiments will be managed by existing study.py "
                "and recorder.py.",
            ]
        )

    def _render_risks(self, rts: ResearchTaskSpecification) -> str:
        risks = rts.risks if rts.risks else _DEFAULT_RISKS
        return "\n".join(
            [
                "## 17. Risks and Manual Confirmation Items",
                "",
                self._format_list(risks, bullet=True),
            ]
        )

    def _render_summary(self) -> str:
        return "\n".join(
            [
                "## 18. Summary for Next Stage",
                "",
                "- ImplementationPlanner should convert this requirement into "
                "implementation_plan.md or implementation_plan.yaml.",
                "- ProjectGenerator should create a runnable project from the selected template.",
                "- ValidationAgent should run dummy validation.",
                "- TaskCardGenerator should generate task_card.yaml for the existing training framework.",
                "- Existing auto-training module should handle training and HPO.",
            ]
        )

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

    def _render_objective_policy(self, rts: ResearchTaskSpecification) -> str:
        policy = rts.objective_policy or rts.extra.get("objective_policy", {})
        if not policy:
            return "Objective policy: single primary metric objective will be used."
        rows = [
            ("type", self._value(policy.get("type"))),
            ("primary_metric", self._value(policy.get("primary_metric"))),
            ("direction", self._value(policy.get("direction"))),
            ("metrics", self._format_dict(policy.get("metrics", {}))),
            ("constraints", self._format_dict(policy.get("constraints", {}))),
        ]
        return "\n".join(["Objective policy:", "", self._kv_table(rows)])

    def _default_adapter_info(self, rts: ResearchTaskSpecification) -> dict[str, Any]:
        return {
            "type": rts.adapter.type or "pytorch_yaml",
            "train_entry": rts.adapter.train_entry or "train.py",
            "config_path": rts.adapter.config_path or "configs/config.yaml",
            "output_dir_arg": rts.adapter.output_dir_arg or "Not specified",
            "fixed_args": rts.adapter.fixed_args,
            "param_arg_map": rts.adapter.param_arg_map,
        }

    def _baseline_template(self, rts: ResearchTaskSpecification) -> str:
        return rts.baseline.template if self._has_text(rts.baseline.template) else "general_pytorch"

    def _format_table(self, headers: list[str], rows: list[list[Any]]) -> str:
        header = "| " + " | ".join(headers) + " |"
        separator = "| " + " | ".join(["---"] * len(headers)) + " |"
        body = [
            "| " + " | ".join(self._table_cell(cell) for cell in row) + " |"
            for row in rows
        ]
        return "\n".join([header, separator, *body])

    def _kv_table(self, rows: list[tuple[str, Any]]) -> str:
        return self._format_table(["field", "value"], [[key, value] for key, value in rows])

    def _format_list(self, values: Any, *, bullet: bool = False) -> str:
        if not values:
            return "Not specified"
        if not isinstance(values, list):
            return str(values)
        if bullet:
            return "\n".join(f"- {self._value(item)}" for item in values)
        return ", ".join(str(item) for item in values)

    def _format_dict(self, value: Any) -> str:
        if not value:
            return "Not specified"
        if not isinstance(value, dict):
            return str(value)
        parts = [f"{key}: {value[key]}" for key in sorted(value)]
        return "; ".join(parts)

    def _remaining_params(self, value: dict[str, Any], skip: set[str]) -> str:
        return self._format_dict({key: item for key, item in value.items() if key not in skip})

    def _range_or_choices(self, spec: Any) -> str:
        if not isinstance(spec, dict):
            return "Not specified"
        if spec.get("type") == "categorical":
            return self._format_list(spec.get("choices", []))
        if spec.get("type") in {"float", "int"}:
            low = spec.get("low", "Not specified")
            high = spec.get("high", "Not specified")
            return f"[{low}, {high}]"
        return "Not specified"

    def _validation_check_description(self, check: str) -> str:
        descriptions = {
            "import_check": "All generated modules can be imported.",
            "dummy_forward": "Model can run a forward pass with dummy inputs.",
            "loss_backward": "Loss can be computed and backpropagated.",
            "one_batch_train": "Trainer can run one batch without crashing.",
            "config_load": "configs/config.yaml can be loaded successfully.",
            "checkpoint_save_load": "Checkpoint save and load both work.",
        }
        return descriptions[check]

    def _value(self, value: Any, fallback: Any = "Not specified") -> str:
        if value is None:
            return str(fallback)
        if isinstance(value, str) and not value.strip():
            return str(fallback)
        return str(value)

    def _table_cell(self, value: Any) -> str:
        text = self._value(value)
        return text.replace("|", "\\|").replace("\n", "<br>")

    def _unique(self, values: list[Any]) -> list[str]:
        result: list[str] = []
        for value in values:
            if self._has_text(value) and value not in result:
                result.append(str(value))
        return result

    def _has_text(self, value: Any) -> bool:
        return isinstance(value, str) and bool(value.strip())
