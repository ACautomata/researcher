"""End-to-end RTS to generated experiment workflow."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from auto_research.core.study import run_study
from auto_research.generation.project_generator import ProjectGenerator
from auto_research.generation.task_card_generator import TaskCardGenerator
from auto_research.planning.implementation_planner import ImplementationPlanner
from auto_research.rts.io import load_rts
from auto_research.rts.validation import RTSValidator
from auto_research.validation.project_validator import ProjectValidator


class RtsToExperimentWorkflow:
    """Run the full RTS-to-generated-project workflow."""

    def run(
        self,
        rts_path: str | Path,
        output_dir: str | Path = "./generated_projects",
        enable_training: bool = False,
        enable_hpo: bool = False,
        overwrite: bool = False,
        allow_invalid_rts: bool = False,
        allow_unvalidated_task_card: bool = False,
    ) -> dict[str, Any]:
        """Run RTS loading, planning, project generation, validation, and task-card generation."""

        output_root = Path(output_dir)
        output_root.mkdir(parents=True, exist_ok=True)
        result = self._initial_result(rts_path)
        errors: list[str] = result["errors"]
        warnings: list[str] = result["warnings"]
        report_path = output_root / "final_report.md"
        project_dir: Path | None = None

        try:
            rts = load_rts(rts_path)
            result["project_name"] = rts.meta.project_name
            result["rts_path"] = str(Path(rts_path))

            validation = RTSValidator().validate(rts)
            if validation.get("warnings"):
                warnings.extend(str(item) for item in validation["warnings"])
            if not validation.get("passed", False):
                errors.extend(str(item) for item in validation.get("errors", []))
                if not allow_invalid_rts:
                    result["success"] = False
                    report_path = output_root / f"{rts.meta.project_name or 'workflow'}_final_report.md"
                    result["final_report_path"] = str(report_path)
                    self._write_final_report(result, report_path)
                    return result

            planner = ImplementationPlanner()
            plan = planner.build_plan(rts)
            project_result = ProjectGenerator().generate(
                rts=rts,
                plan=plan,
                output_dir=output_root,
                overwrite=overwrite,
            )
            project_dir = Path(project_result["project_dir"])
            result.update(
                {
                    "project_dir": project_result["project_dir"],
                    "requirement_path": project_result["requirement_path"],
                    "implementation_plan_yaml_path": project_result[
                        "implementation_plan_yaml_path"
                    ],
                    "implementation_plan_md_path": project_result[
                        "implementation_plan_md_path"
                    ],
                    "generation_report_path": project_result["generation_report_path"],
                }
            )
            report_path = project_dir / "final_report.md"

            validation_result = ProjectValidator().validate(project_dir)
            result["validation_result_path"] = validation_result["validation_result_path"]
            result["validation_passed"] = validation_result["passed"]
            if validation_result.get("warnings"):
                warnings.extend(str(item) for item in validation_result["warnings"])
            if validation_result.get("errors"):
                errors.extend(str(item) for item in validation_result["errors"])

            if validation_result["passed"] or allow_unvalidated_task_card:
                task_card_path = project_dir / "task_card.yaml"
                task_card = TaskCardGenerator().generate(
                    project_dir=project_dir,
                    plan=plan,
                    output_path=task_card_path,
                    allow_unvalidated=allow_unvalidated_task_card,
                )
                result["task_card_path"] = str(task_card_path)
            else:
                warnings.append(
                    "Task card generation skipped because project validation failed."
                )
                task_card = None

            if enable_training:
                if not result["task_card_path"]:
                    warnings.append("Training was not launched because task_card.yaml was not generated.")
                else:
                    result["training_submitted"] = True
                    result["training_result"] = self._run_training(
                        task_card_path=Path(result["task_card_path"]),
                        enable_hpo=enable_hpo,
                    )

            result["success"] = not errors or (
                bool(result["task_card_path"]) and result["validation_passed"]
            )
        except Exception as exc:
            errors.append(f"{type(exc).__name__}: {exc}")
            result["success"] = False
        finally:
            if project_dir is not None:
                report_path = project_dir / "final_report.md"
            result["final_report_path"] = str(report_path)
            self._write_final_report(result, report_path)

        return result

    def _run_training(self, task_card_path: Path, enable_hpo: bool) -> dict[str, Any]:
        """Use the existing study CLI API for optional training submission."""

        args = argparse.Namespace(
            task_card=str(task_card_path),
            study_name=None,
            storage=None,
            n_trials=None if enable_hpo else 1,
            timeout=None,
            direction="maximize",
            output_root=None,
            dry_run=False,
            seed=None,
        )
        try:
            return_code = run_study(args)
            return {
                "launched": True,
                "mode": "hpo" if enable_hpo else "single_trial",
                "return_code": return_code,
            }
        except Exception as exc:
            return {
                "launched": False,
                "mode": "hpo" if enable_hpo else "single_trial",
                "error": f"{type(exc).__name__}: {exc}",
            }

    def _initial_result(self, rts_path: str | Path) -> dict[str, Any]:
        return {
            "success": False,
            "project_name": "",
            "project_dir": "",
            "rts_path": str(Path(rts_path)),
            "requirement_path": "",
            "implementation_plan_yaml_path": "",
            "implementation_plan_md_path": "",
            "generation_report_path": "",
            "validation_result_path": "",
            "validation_passed": False,
            "task_card_path": "",
            "training_submitted": False,
            "training_result": {},
            "final_report_path": "",
            "errors": [],
            "warnings": [],
        }

    def _write_final_report(self, result: dict[str, Any], path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self._render_final_report(result), encoding="utf-8")

    def _render_final_report(self, result: dict[str, Any]) -> str:
        return "\n".join(
            [
                "# Final Report",
                "",
                "## 1. Workflow Summary",
                "",
                f"- success: {result['success']}",
                f"- project_name: {result['project_name'] or 'Not specified'}",
                f"- project_dir: {result['project_dir'] or 'Not generated'}",
                "",
                "## 2. RTS Validation",
                "",
                f"- rts_path: {result['rts_path']}",
                f"- validation_blocking_errors: {bool(result['errors']) and not result['project_dir']}",
                "",
                "## 3. Requirement Document",
                "",
                f"- requirement_path: {result['requirement_path'] or 'Not generated'}",
                "",
                "## 4. Implementation Plan",
                "",
                f"- yaml: {result['implementation_plan_yaml_path'] or 'Not generated'}",
                f"- markdown: {result['implementation_plan_md_path'] or 'Not generated'}",
                "",
                "## 5. Generated Project",
                "",
                f"- generation_report_path: {result['generation_report_path'] or 'Not generated'}",
                "",
                "## 6. Project Validation",
                "",
                f"- validation_passed: {result['validation_passed']}",
                f"- validation_result_path: {result['validation_result_path'] or 'Not generated'}",
                "",
                "## 7. Task Card",
                "",
                f"- task_card_path: {result['task_card_path'] or 'Not generated'}",
                "",
                "## 8. Training Submission",
                "",
                f"- training_submitted: {result['training_submitted']}",
                f"- training_result: {result['training_result'] or {}}",
                "",
                "## 9. Errors",
                "",
                self._list_or_none(result["errors"]),
                "",
                "## 10. Warnings",
                "",
                self._list_or_none(result["warnings"]),
                "",
                "## 11. Next Steps",
                "",
                "- Review generated requirement.md, implementation_plan.md, validation_report.md, and task_card.yaml.",
                "- Use the existing AutoResearch training framework to run the generated task card.",
                "",
            ]
        )

    def _list_or_none(self, items: list[str]) -> str:
        if not items:
            return "- None"
        return "\n".join(f"- {item}" for item in items)
