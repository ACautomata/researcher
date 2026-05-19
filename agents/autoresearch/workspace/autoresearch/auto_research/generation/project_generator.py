"""Generate runnable PyTorch projects from RTS and implementation plans."""

from __future__ import annotations

from pathlib import Path
import shutil
from typing import Any

import yaml

from auto_research.generation.code_snippets import loss_snippet, model_component_snippet
from auto_research.generation.config_generator import ConfigGenerator
from auto_research.planning.implementation_planner import ImplementationPlanner
from auto_research.planning.requirement_generator import RequirementGenerator
from auto_research.rts.io import save_rts
from auto_research.rts.schema import ResearchTaskSpecification


class ProjectGenerator:
    """Generate a runnable PyTorch project from a plan."""

    def __init__(self, template_root: str | Path | None = None):
        """Initialize the project generator."""

        if template_root is None:
            template_root = Path(__file__).resolve().parents[1] / "templates"
        self.template_root = Path(template_root)
        self.config_generator = ConfigGenerator()
        self.requirement_generator = RequirementGenerator()
        self.planner = ImplementationPlanner()

    def generate(
        self,
        rts: ResearchTaskSpecification,
        plan: dict[str, Any],
        output_dir: str | Path,
        overwrite: bool = False,
    ) -> dict[str, str]:
        """Generate a project directory from RTS and implementation plan."""

        output_root = Path(output_dir)
        project_name = rts.meta.project_name or "generated_project"
        project_dir = output_root / project_name
        template_name = self._select_template(plan)
        template_dir = self.template_root / template_name

        if not template_dir.exists():
            template_name = "general_pytorch"
            template_dir = self.template_root / template_name

        self._copy_template(template_dir, project_dir, output_root, overwrite)

        rts_path = project_dir / "rts.yaml"
        requirement_path = project_dir / "requirement.md"
        plan_yaml_path = project_dir / "implementation_plan.yaml"
        plan_md_path = project_dir / "implementation_plan.md"
        report_path = project_dir / "generation_report.md"
        config_path = project_dir / "configs" / "config.yaml"

        save_rts(rts, rts_path)
        requirement_text = self.requirement_generator.generate(rts)
        requirement_path.write_text(requirement_text, encoding="utf-8")
        self._save_yaml(plan, plan_yaml_path)
        plan_md_path.write_text(self.planner.render_markdown(plan), encoding="utf-8")

        config = self.config_generator.generate(rts, plan, project_dir)
        self.config_generator.save(config, config_path)
        self._create_extra_files(project_dir, plan)
        report_path.write_text(
            self._render_generation_report(project_name, template_name, plan),
            encoding="utf-8",
        )

        run_script_path = project_dir / "scripts" / "run_train.sh"
        return {
            "project_dir": str(project_dir),
            "selected_template": template_name,
            "config_path": str(config_path),
            "rts_path": str(rts_path),
            "requirement_path": str(requirement_path),
            "implementation_plan_yaml_path": str(plan_yaml_path),
            "implementation_plan_md_path": str(plan_md_path),
            "generation_report_path": str(report_path),
            "run_script_path": str(run_script_path),
        }

    def _select_template(self, plan: dict[str, Any]) -> str:
        template = plan.get("template", {})
        selected = template.get("selected") or template.get("selected_template")
        return str(selected or "general_pytorch")

    def _copy_template(
        self,
        template_dir: Path,
        project_dir: Path,
        output_root: Path,
        overwrite: bool,
    ) -> None:
        output_root.mkdir(parents=True, exist_ok=True)
        if project_dir.exists():
            if not overwrite:
                raise FileExistsError(
                    f"Generated project already exists: '{project_dir}'. "
                    "Pass overwrite=True to replace it."
                )
            resolved_project = project_dir.resolve()
            resolved_root = output_root.resolve()
            if resolved_project == resolved_root or resolved_root not in resolved_project.parents:
                raise ValueError(f"Refusing to remove unsafe project path: '{project_dir}'.")
            shutil.rmtree(project_dir)
        shutil.copytree(template_dir, project_dir)

    def _create_extra_files(self, project_dir: Path, plan: dict[str, Any]) -> None:
        for item in plan.get("files_to_create", []):
            path_text = item.get("path")
            module_type = item.get("module_type")
            if not path_text:
                continue
            target = project_dir / str(path_text)
            target.parent.mkdir(parents=True, exist_ok=True)
            if module_type == "model_component":
                source = model_component_snippet(target.stem)
            elif module_type == "loss":
                source = loss_snippet(target.stem)
            else:
                source = '"""Generated placeholder module."""\n'
            target.write_text(source, encoding="utf-8")

    def _render_generation_report(
        self,
        project_name: str,
        template_name: str,
        plan: dict[str, Any],
    ) -> str:
        warnings = plan.get("warnings", [])
        warning_lines = "\n".join(f"- {item}" for item in warnings) if warnings else "- None"
        return "\n".join(
            [
                "# Generation Report",
                "",
                f"- project: {project_name}",
                f"- selected_template: {template_name}",
                "- generated_by: auto_research.generation.ProjectGenerator",
                "",
                "## Warnings",
                "",
                warning_lines,
                "",
            ]
        )

    def _save_yaml(self, data: dict[str, Any], path: Path) -> None:
        with path.open("w", encoding="utf-8") as handle:
            yaml.safe_dump(data, handle, sort_keys=False, allow_unicode=True)
