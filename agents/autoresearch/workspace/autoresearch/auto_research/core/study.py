"""CLI entrypoint for task-card-driven Optuna studies."""

from __future__ import annotations

import argparse
from copy import deepcopy
from pathlib import Path
from typing import Any

from auto_research.core.objective import create_objective
from auto_research.core.safety import SafetyStopStudyError
from auto_research.core.task_card import (
    create_adapter_from_task_card,
    load_task_card,
    validate_task_card,
)


def build_arg_parser() -> argparse.ArgumentParser:
    """Build the CLI parser for running studies."""

    parser = argparse.ArgumentParser(description="Run an AutoResearch Optuna study.")
    parser.add_argument("--task-card", required=True, help="Path to the task card YAML file.")
    parser.add_argument("--study-name", default=None, help="Optional Optuna study name override.")
    parser.add_argument("--storage", default=None, help="Optional Optuna storage URL or SQLite path.")
    parser.add_argument("--n-trials", type=int, default=None, help="Maximum number of trials.")
    parser.add_argument(
        "--timeout",
        type=int,
        default=None,
        help="Optional study-level timeout in seconds for Optuna optimization.",
    )
    parser.add_argument(
        "--direction",
        default="maximize",
        choices=("maximize", "minimize"),
        help="Optimization direction.",
    )
    parser.add_argument(
        "--output-root",
        default=None,
        help="Override the task card output root for generated trial directories.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print trial commands without executing training.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Optional random seed for the Optuna sampler.",
    )
    return parser


def run_study(args: argparse.Namespace) -> int:
    """Run a study from parsed CLI arguments."""

    optuna = _import_optuna()

    task_card = load_task_card(args.task_card)
    if args.output_root is not None:
        task_card = deepcopy(task_card)
        task_card.setdefault("adapter", {})
        task_card["adapter"]["output_root"] = args.output_root

    is_valid, message = validate_task_card(task_card)
    if not is_valid:
        raise ValueError(f"Task card validation failed: {message}")

    adapter = create_adapter_from_task_card(task_card)
    objective = create_objective(task_card, adapter, dry_run=args.dry_run)

    study_name = args.study_name or task_card["task_name"]
    storage = _normalize_storage(args.storage)
    sampler = optuna.samplers.TPESampler(seed=args.seed)
    study = optuna.create_study(
        study_name=study_name,
        storage=storage,
        sampler=sampler,
        direction=args.direction,
        load_if_exists=True,
    )

    n_trials = args.n_trials
    if n_trials is None:
        constraints = task_card.get("constraints", {})
        max_trials = constraints.get("max_trials")
        if isinstance(max_trials, int) and not isinstance(max_trials, bool) and max_trials > 0:
            n_trials = max_trials

    try:
        study.optimize(
            objective,
            n_trials=n_trials,
            timeout=args.timeout,
            catch=(),
        )
    except SafetyStopStudyError as exc:
        print(str(exc))

    print(f"Study name: {study.study_name}")
    print(f"Direction: {args.direction}")
    print(f"Trials: {len(study.trials)}")
    if getattr(study, "best_trial", None) is not None:
        print(f"Best value: {study.best_trial.value}")
        print(f"Best params: {study.best_trial.params}")
    return 0


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint used by ``python -m auto_research.core.study``."""

    parser = build_arg_parser()
    args = parser.parse_args(argv)
    return run_study(args)


def _import_optuna() -> Any:
    """Import Optuna lazily with a clear runtime error when missing."""

    try:
        import optuna  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "Optuna is required to run studies. Install the project dependencies first, "
            "for example with 'pip install -e .'."
        ) from exc

    return optuna


def _normalize_storage(storage: str | None) -> str | None:
    """Normalize SQLite paths into Optuna storage URLs."""

    if storage is None or not storage.strip():
        return None

    stripped = storage.strip()
    if "://" in stripped:
        return stripped

    if stripped.endswith(".db") or stripped.endswith(".sqlite") or stripped.endswith(".sqlite3"):
        return f"sqlite:///{Path(stripped).resolve().as_posix()}"

    return stripped


if __name__ == "__main__":
    raise SystemExit(main())
