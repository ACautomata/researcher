"""Command line interface for AutoResearch utility workflows."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

from auto_research.generation.project_generator import ProjectGenerator
from auto_research.generation.task_card_generator import TaskCardGenerator
from auto_research.planning.idea_to_rts import IdeaToRTSConverter
from auto_research.planning.implementation_planner import ImplementationPlanner
from auto_research.planning.requirement_generator import RequirementGenerator
from auto_research.readers.idea_reader import IdeaReader
from auto_research.rts.io import load_rts, save_rts
from auto_research.rts.schema import (
    RTSAdapter,
    RTSBaseline,
    RTSGoal,
    RTSImplementation,
    RTSInput,
    RTSMeta,
    RTSModel,
    RTSOutput,
    RTSTask,
    RTSTraining,
    ResearchTaskSpecification,
)
from auto_research.rts.validation import RTSValidator
from auto_research.validation.project_validator import ProjectValidator
from auto_research.workflows.rts_to_experiment_workflow import RtsToExperimentWorkflow


def main() -> None:
    """Run the AutoResearch command line interface."""

    parser = argparse.ArgumentParser(prog="auto_research")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init-rts", help="Create an example RTS file.")
    init_parser.add_argument("--project-name", required=True, help="RTS project name.")
    init_parser.add_argument("--output", required=True, help="Output YAML or JSON path.")
    init_parser.set_defaults(func=_handle_init_rts)

    idea_parser = subparsers.add_parser(
        "idea-to-rts",
        help="Convert idea text or markdown into an RTS YAML file.",
    )
    idea_input = idea_parser.add_mutually_exclusive_group(required=True)
    idea_input.add_argument("--idea-text", help="Inline idea text.")
    idea_input.add_argument("--idea-file", help="Path to a .txt or .md idea file.")
    idea_parser.add_argument("--project-name", required=True, help="RTS project name.")
    idea_parser.add_argument("--output", required=True, help="Output RTS YAML or JSON path.")
    idea_parser.set_defaults(func=_handle_idea_to_rts)

    validate_parser = subparsers.add_parser("validate-rts", help="Validate an RTS file.")
    validate_parser.add_argument("--rts", required=True, help="Input RTS YAML or JSON path.")
    validate_parser.set_defaults(func=_handle_validate_rts)

    requirement_parser = subparsers.add_parser(
        "rts-to-requirement",
        help="Generate requirement.md from an RTS file.",
    )
    requirement_parser.add_argument("--rts", required=True, help="Input RTS YAML or JSON path.")
    requirement_parser.add_argument("--output", required=True, help="Output markdown path.")
    requirement_parser.add_argument(
        "--allow-invalid",
        action="store_true",
        help="Generate the requirement document even when RTS validation fails.",
    )
    requirement_parser.set_defaults(func=_handle_rts_to_requirement)

    plan_parser = subparsers.add_parser(
        "rts-to-plan",
        help="Generate implementation_plan.yaml and implementation_plan.md from RTS.",
    )
    plan_parser.add_argument("--rts", required=True, help="Input RTS YAML or JSON path.")
    plan_parser.add_argument(
        "--output-yaml",
        required=True,
        help="Output machine-readable implementation plan YAML path.",
    )
    plan_parser.add_argument(
        "--output-md",
        required=True,
        help="Output human-readable implementation plan markdown path.",
    )
    plan_parser.add_argument(
        "--allow-invalid",
        action="store_true",
        help="Generate implementation plans even when RTS validation fails.",
    )
    plan_parser.set_defaults(func=_handle_rts_to_plan)

    generate_parser = subparsers.add_parser(
        "generate-project",
        help="Generate a runnable PyTorch project from RTS and implementation plan.",
    )
    generate_parser.add_argument("--rts", required=True, help="Input RTS YAML or JSON path.")
    generate_parser.add_argument("--plan", required=True, help="Input implementation_plan.yaml path.")
    generate_parser.add_argument(
        "--output-dir",
        required=True,
        help="Directory under which the project folder will be generated.",
    )
    generate_parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace an existing generated project directory.",
    )
    generate_parser.set_defaults(func=_handle_generate_project)

    validate_project_parser = subparsers.add_parser(
        "validate-project",
        help="Validate a generated project before training-framework handoff.",
    )
    validate_project_parser.add_argument(
        "--project-dir",
        required=True,
        help="Generated project directory.",
    )
    validate_project_parser.add_argument(
        "--config",
        default=None,
        help="Optional config path. Defaults to PROJECT_DIR/configs/config.yaml.",
    )
    validate_project_parser.add_argument(
        "--timeout",
        type=int,
        default=300,
        help="Per-command validation timeout in seconds.",
    )
    validate_project_parser.set_defaults(func=_handle_validate_project)

    task_card_parser = subparsers.add_parser(
        "generate-task-card",
        help="Generate task_card.yaml for a validated generated project.",
    )
    task_card_parser.add_argument("--project-dir", required=True, help="Generated project directory.")
    task_card_parser.add_argument("--plan", required=True, help="Input implementation_plan.yaml path.")
    task_card_parser.add_argument("--output", required=True, help="Output task_card.yaml path.")
    task_card_parser.add_argument(
        "--allow-unvalidated",
        action="store_true",
        help="Allow task card generation without a passing validation_result.json.",
    )
    task_card_parser.set_defaults(func=_handle_generate_task_card)

    workflow_parser = subparsers.add_parser(
        "run-from-rts",
        help="Run the end-to-end RTS to generated experiment workflow.",
    )
    workflow_parser.add_argument("--rts", required=True, help="Input RTS YAML or JSON path.")
    workflow_parser.add_argument(
        "--output-dir",
        default="./generated_projects",
        help="Generated projects output directory.",
    )
    workflow_parser.add_argument("--overwrite", action="store_true", help="Overwrite generated project.")
    workflow_parser.add_argument(
        "--enable-training",
        action="store_true",
        help="Submit generated task card to existing training framework.",
    )
    workflow_parser.add_argument(
        "--enable-hpo",
        action="store_true",
        help="Run HPO through the existing study framework when training is enabled.",
    )
    workflow_parser.add_argument(
        "--allow-invalid-rts",
        action="store_true",
        help="Continue workflow even if RTS validation fails.",
    )
    workflow_parser.add_argument(
        "--allow-unvalidated-task-card",
        action="store_true",
        help="Generate task card even if project validation fails.",
    )
    workflow_parser.set_defaults(func=_handle_run_from_rts)

    args = parser.parse_args()
    args.func(args)


def _handle_init_rts(args: argparse.Namespace) -> None:
    rts = build_rgb_ir_reid_example(project_name=args.project_name)
    output_path = Path(args.output)
    save_rts(rts, output_path)
    print(f"Created RTS example: {output_path}")


def _handle_idea_to_rts(args: argparse.Namespace) -> None:
    reader = IdeaReader()
    if args.idea_text is not None:
        idea_text = reader.read_from_text(args.idea_text)
    else:
        idea_text = reader.read_from_file(args.idea_file)
    rts = IdeaToRTSConverter().convert(idea_text, project_name=args.project_name)
    output_path = Path(args.output)
    save_rts(rts, output_path)
    print(f"Created RTS from idea: {output_path}")


def _handle_validate_rts(args: argparse.Namespace) -> None:
    rts = load_rts(args.rts)
    result = RTSValidator().validate(rts)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if not result["passed"]:
        raise SystemExit(1)


def _handle_rts_to_requirement(args: argparse.Namespace) -> None:
    rts = load_rts(args.rts)
    result = RTSValidator().validate(rts)
    if not result["passed"] and not args.allow_invalid:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        raise SystemExit(1)

    generator = RequirementGenerator()
    requirement_text = generator.generate(rts)
    if not result["passed"]:
        warning = _format_validation_warning(result["errors"])
        requirement_text = warning + "\n\n" + requirement_text

    output_path = Path(args.output)
    generator.save(requirement_text, output_path)
    print(f"Created requirement document: {output_path}")


def _handle_rts_to_plan(args: argparse.Namespace) -> None:
    rts = load_rts(args.rts)
    result = RTSValidator().validate(rts)
    if not result["passed"] and not args.allow_invalid:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        raise SystemExit(1)

    planner = ImplementationPlanner()
    plan = planner.build_plan(rts)
    if not result["passed"]:
        plan["warnings"] = [
            "RTS validation failed, but plan generation was allowed by --allow-invalid.",
            *result["errors"],
            *plan.get("warnings", []),
        ]

    markdown_text = planner.render_markdown(plan)
    yaml_path = Path(args.output_yaml)
    markdown_path = Path(args.output_md)
    planner.save_yaml(plan, yaml_path)
    planner.save_markdown(markdown_text, markdown_path)
    print(f"Created implementation plan YAML: {yaml_path}")
    print(f"Created implementation plan markdown: {markdown_path}")


def _handle_generate_project(args: argparse.Namespace) -> None:
    rts = load_rts(args.rts)
    plan_path = Path(args.plan)
    with plan_path.open("r", encoding="utf-8") as handle:
        plan = yaml.safe_load(handle) or {}
    if not isinstance(plan, dict):
        raise SystemExit(f"Implementation plan must be a YAML mapping: {plan_path}")

    result = ProjectGenerator().generate(
        rts=rts,
        plan=plan,
        output_dir=args.output_dir,
        overwrite=args.overwrite,
    )
    print(f"Generated project: {result['project_dir']}")


def _handle_validate_project(args: argparse.Namespace) -> None:
    result = ProjectValidator(timeout=args.timeout).validate(
        project_dir=args.project_dir,
        config_path=args.config,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if not result["passed"]:
        raise SystemExit(1)


def _handle_generate_task_card(args: argparse.Namespace) -> None:
    plan_path = Path(args.plan)
    with plan_path.open("r", encoding="utf-8") as handle:
        plan = yaml.safe_load(handle) or {}
    if not isinstance(plan, dict):
        raise SystemExit(f"Implementation plan must be a YAML mapping: {plan_path}")

    output_path = Path(args.output)
    TaskCardGenerator().generate(
        project_dir=args.project_dir,
        plan=plan,
        output_path=output_path,
        allow_unvalidated=args.allow_unvalidated,
    )
    print(f"Created task card: {output_path}")


def _handle_run_from_rts(args: argparse.Namespace) -> None:
    result = RtsToExperimentWorkflow().run(
        rts_path=args.rts,
        output_dir=args.output_dir,
        enable_training=args.enable_training,
        enable_hpo=args.enable_hpo,
        overwrite=args.overwrite,
        allow_invalid_rts=args.allow_invalid_rts,
        allow_unvalidated_task_card=args.allow_unvalidated_task_card,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if not result["success"]:
        raise SystemExit(1)


def _format_validation_warning(errors: list[str]) -> str:
    lines = [
        "> Validation Warning: RTS validation failed, but requirement generation "
        "was allowed by --allow-invalid.",
        ">",
    ]
    lines.extend(f"> - {error}" for error in errors)
    return "\n".join(lines)


def build_rgb_ir_reid_example(project_name: str) -> ResearchTaskSpecification:
    """Build a small RGB-IR cross-modal person re-identification example RTS."""

    return ResearchTaskSpecification(
        meta=RTSMeta(
            project_name=project_name,
            source_type="manual",
            description="RGB-IR cross-modal person re-identification attention baseline.",
        ),
        task=RTSTask(
            type="rgb_ir_reid",
            research_problem=(
                "Learn discriminative cross-modal embeddings that align RGB and IR "
                "person images for retrieval."
            ),
            learning_paradigm="supervised",
        ),
        goal=RTSGoal(
            primary_metric="mAP",
            optimization_direction="maximize",
            secondary_metrics=["rank1", "rank5"],
        ),
        input=RTSInput(
            modalities=["RGB", "IR"],
            data_format="paired_image_folders",
            input_shape=[3, 256, 128],
        ),
        output=RTSOutput(
            type="embedding",
            dimension=512,
            description="Person identity embedding for cross-modal retrieval.",
        ),
        baseline=RTSBaseline(
            template="rgb_ir_reid",
            name="RGB-IR attention baseline",
            description="Dual-modality baseline with identity and metric learning losses.",
        ),
        model=RTSModel(
            backbone={"name": "resnet50", "pretrained": True},
            components=[
                {"name": "modality_attention", "type": "channel_spatial_attention"},
                {"name": "shared_embedding", "dimension": 512},
            ],
            heads=[
                {"name": "identity_classifier", "type": "linear"},
                {"name": "embedding_head", "type": "projection"},
            ],
        ),
        losses=[
            {"name": "cross_entropy", "weight": 1.0, "params": {}},
            {"name": "triplet", "weight": 1.0, "params": {"margin": 0.3}},
            {"name": "center_constraint", "weight": 0.01, "params": {}},
        ],
        training=RTSTraining(
            optimizer="adam",
            scheduler="cosine",
            batch_size=64,
            epochs=80,
            lr=0.0003,
            weight_decay=0.0005,
            mixed_precision=True,
        ),
        datasets=[
            {
                "name": "SYSU-MM01",
                "path": "data/sysu-mm01",
                "split": "standard",
                "notes": "Placeholder path; update before training.",
            }
        ],
        metrics=["mAP", "rank1", "rank5", "rank10"],
        search_space={
            "lr": {"type": "float", "low": 1e-5, "high": 1e-3, "log": True},
            "batch_size": {"type": "categorical", "choices": [32, 64]},
            "center_loss_weight": {"type": "float", "low": 0.001, "high": 0.1, "log": True},
        },
        ablation=[
            {
                "name": "without_modality_attention",
                "description": "Disable cross-modal attention module.",
                "config_overrides": {"model.components.modality_attention.enabled": False},
            }
        ],
        implementation=RTSImplementation(
            required_files=["train.py", "configs/config.yaml", "models/model.py", "losses.py"],
            expected_modules=["models", "datasets", "losses", "metrics"],
            notes="Generated project should expose a YAML-driven training entry.",
        ),
        adapter=RTSAdapter(
            type="pytorch_yaml",
            train_entry="train.py",
            config_path="configs/config.yaml",
            fixed_args=[],
            param_arg_map={},
        ),
        extra={},
    )


if __name__ == "__main__":
    main()
